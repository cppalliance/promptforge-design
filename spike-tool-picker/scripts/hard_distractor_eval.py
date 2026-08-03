"""Re-score the already-generated author-register needs against HARD distractors.

Reuses data/lua_needs.jsonl (author-register need -> gold tool). For each need, the
distractors are the gold tool's NEAREST neighbors in the catalog (the hardest possible
confusers), excluding near-identical duplicates (cosine >= dup_thr) so we test
disambiguation among genuinely-distinct-but-similar tools, not equivalent republishes.
Compares random vs hard distractors side by side. No API calls; GPU only.
"""

from __future__ import annotations

import argparse
import json

import numpy as np

from common import DATA, RESULTS_DIR
from lua_register_eval import load_automatelab


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--dup-thr", type=float, default=0.98)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    from methods import auto_device
    import random

    rng = random.Random(args.seed)
    needs = [json.loads(l) for l in (DATA / "lua_needs.jsonl").open(encoding="utf-8")]
    tools = load_automatelab()
    by_q = {t.qualified: i for i, t in enumerate(tools)}
    needs = [n for n in needs if n["gold"] in by_q]

    model = SentenceTransformer(args.model, device=auto_device())
    pool = np.asarray(model.encode([t.enriched_text() for t in tools], normalize_embeddings=True,
                                   batch_size=256, show_progress_bar=False), dtype=np.float32)
    qv = np.asarray(model.encode([n["need"] for n in needs], normalize_embeddings=True,
                                 batch_size=256, show_progress_bar=False), dtype=np.float32)
    D = args.distractors
    npool = len(tools)

    def score(catalog_fn):
        top1 = rec3 = 0
        for i, n in enumerate(needs):
            g = by_q[n["gold"]]
            dist = catalog_fn(g)
            cand = np.concatenate([[g], dist])
            sims = pool[cand] @ qv[i]
            order = np.argsort(-sims)
            gr = int(np.where(order == 0)[0][0])
            top1 += gr == 0
            rec3 += gr < 3
        return top1 / len(needs), rec3 / len(needs)

    # precompute gold neighbor lists
    def hard(g):
        s = pool @ pool[g]
        s[g] = -1
        neigh = np.argsort(-s)
        out = [j for j in neigh if s[j] < args.dup_thr][:D]
        return np.array(out, dtype=np.int64)

    def rand(g):
        return np.array([j for j in rng.sample(range(npool), D + 2) if j != g][:D], dtype=np.int64)

    r_top1, r_rec3 = score(rand)
    h_top1, h_rec3 = score(hard)
    out = {"model": args.model, "n": len(needs), "distractors": D, "dup_thr": args.dup_thr,
           "random": {"top1": r_top1, "recall@3": r_rec3},
           "hard_neighbor": {"top1": h_top1, "recall@3": h_rec3}}
    print(json.dumps(out, indent=2))
    (RESULTS_DIR / "hard_distractor.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
