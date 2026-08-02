"""Assemble needs.jsonl: attach id-referenced distractors and equivalent-golds to each need.

For each need's gold tool:
  - equivalent_gold_ids : catalog tools with cosine >= dup_thr (near-identical; excluded from
    distractors so an equivalent pick is never scored wrong, and recorded for duplicate analysis).
  - hard_distractor_ids : the gold's nearest neighbors below dup_thr (hardest confusers).
  - random_distractor_ids : random tools, excluding gold and equivalents.
Catalog embeddings (bge-small) are cached under embeddings/, keyed by catalog hash.
"""

from __future__ import annotations

import argparse
import json
import random

import numpy as np

from common import DATA, EMB, catalog_hash, load_catalog


def embed_catalog(tools, model_id):
    from sentence_transformers import SentenceTransformer
    h = catalog_hash(tools)
    cache = EMB / f"catalog_{model_id.split('/')[-1]}_{h}.npy"
    if cache.exists():
        return np.load(cache)
    m = SentenceTransformer(model_id, device="cuda" if _cuda() else "cpu")
    v = np.asarray(m.encode([t.enriched_text() for t in tools], normalize_embeddings=True,
                            batch_size=256, show_progress_bar=False), dtype=np.float32)
    EMB.mkdir(exist_ok=True)
    np.save(cache, v)
    return v


def _cuda():
    try:
        import torch
        return torch.cuda.is_available()
    except Exception:  # noqa: BLE001
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--embed", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--dup-thr", type=float, default=0.98)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    tools = load_catalog()
    pool = embed_catalog(tools, args.embed)
    n = len(tools)
    raw = [json.loads(l) for l in (DATA / "needs_raw.jsonl").open(encoding="utf-8")]

    out = DATA / "needs.jsonl"
    D = args.distractors
    with out.open("w", encoding="utf-8") as f:
        for i, r in enumerate(raw):
            g = r["gold_id"]
            sims = pool @ pool[g]
            sims[g] = -1.0
            order = np.argsort(-sims)
            equivalents = [int(j) for j in order if sims[j] >= args.dup_thr]
            eq_set = set(equivalents) | {g}
            hard = [int(j) for j in order if sims[j] < args.dup_thr][:D]
            rand_pool = [j for j in range(n) if j not in eq_set]
            random_d = rng.sample(rand_pool, D)
            f.write(json.dumps({
                "id": i, "need": r["need"], "band": r["band"], "gold_id": g,
                "equivalent_gold_ids": equivalents[:10], "hard_distractor_ids": hard,
                "random_distractor_ids": random_d, "gen_model": r["gen_model"],
            }) + "\n")
    print(f"needs.jsonl: {len(raw)} cases (distractors={D}, dup_thr={args.dup_thr})")


if __name__ == "__main__":
    main()
