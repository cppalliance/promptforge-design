"""Large-scale real-need eval: all TOOLRET human/benchmark queries at ~10k scale.

Efficient single pass (no per-example catalog files): embed the whole distractor
pool and all gold tools once, then for each query sample a matched positive catalog
(gold + D distractors) and negative catalog (D+1 distractors, no gold) in memory.

Reports top-1, recall@3, and an abstention threshold sweep (coverage / accuracy /
false-bind) - the same metrics as the small evals, at 40x the data.
"""

from __future__ import annotations

import argparse
import json
import random

import numpy as np

from build_toolret_eval import doc_to_tool, QUERY_CONFIGS, TOOL_CONFIGS  # reuse parsing
from common import RESULTS_DIR


def load_pool(rng):
    from datasets import load_dataset

    pool = []
    for cfg in TOOL_CONFIGS:
        try:
            t = load_dataset("mangopy/ToolRet-Tools", cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  skip tools {cfg}: {e}")
            continue
        split = list(t.keys())[0]
        for row in t[split]:
            try:
                doc = json.loads(row["documentation"]) if isinstance(row["documentation"], str) else row["documentation"]
            except Exception:  # noqa: BLE001
                continue
            pool.append(doc_to_tool(doc, server=f"toolret_{cfg}"))
    rng.shuffle(pool)
    return pool


def load_queries(cap, rng, all_configs):
    """Return list of (need, [gold_tools], cfg).

    Fixes over the first version: (1) collect ALL relevant docs per query as gold
    (multi-gold configs were under-counted before); (2) drop degenerate configs whose
    labels are constant/near-constant across unrelated queries (e.g. ultratool, where
    every query's gold is the same wrong tool).
    """
    from datasets import get_dataset_config_names, load_dataset

    cfgs = get_dataset_config_names("mangopy/ToolRet-Queries") if all_configs else QUERY_CONFIGS
    per_cfg = {}
    for cfg in cfgs:
        try:
            d = load_dataset("mangopy/ToolRet-Queries", cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  skip queries {cfg}: {e}")
            continue
        split = list(d.keys())[0]
        rows = []
        for r in d[split]:
            try:
                labels = json.loads(r["labels"]) if isinstance(r["labels"], str) else r["labels"]
            except Exception:  # noqa: BLE001
                continue
            need = (r.get("query") or "").strip()
            golds = [doc_to_tool(l["doc"], server=f"toolret_{cfg}") for l in labels
                     if l.get("relevance", 1) and isinstance(l.get("doc"), dict)]
            if need and golds:
                rows.append((need, golds, cfg))
        if not rows:
            continue
        # degeneracy filter: if too few distinct gold names across many queries, drop it
        distinct = {g.name for _, gs, _ in rows for g in gs}
        if len(rows) >= 20 and len(distinct) <= 2:
            print(f"  drop degenerate config {cfg}: {len(distinct)} distinct golds over {len(rows)} queries")
            continue
        per_cfg[cfg] = rows

    items = [it for rows in per_cfg.values() for it in rows]
    rng.shuffle(items)
    return items[:cap]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--all-configs", action="store_true", default=True)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    from methods import auto_device

    rng = random.Random(args.seed)
    pool = load_pool(rng)
    queries = load_queries(args.n, rng, args.all_configs)
    print(f"pool={len(pool)} tools  queries={len(queries)}  model={args.model}")

    model = SentenceTransformer(args.model, device=auto_device())
    pool_texts = [t.enriched_text() for t in pool]
    pool_vecs = model.encode(pool_texts, normalize_embeddings=True, batch_size=256, show_progress_bar=False)
    # flat-encode all gold texts, with per-query offsets (multi-gold)
    flat_golds, offs = [], []
    for _, golds, _ in queries:
        offs.append((len(flat_golds), len(flat_golds) + len(golds)))
        flat_golds.extend(g.enriched_text() for g in golds)
    gold_vecs = model.encode(flat_golds, normalize_embeddings=True, batch_size=256, show_progress_bar=False)
    q_vecs = model.encode([q for q, _, _ in queries], normalize_embeddings=True, batch_size=256, show_progress_bar=False)

    D = args.distractors
    npool = len(pool)
    top1 = rec3 = 0
    pos_top_scores = []
    pos_correct_flags = []
    neg_top_scores = []
    per_cfg = {}
    for i, (need, golds, cfg) in enumerate(queries):
        qv = q_vecs[i]
        a, b = offs[i]
        gvecs = gold_vecs[a:b]                      # all relevant golds for this query
        ng = b - a
        idx = rng.sample(range(npool), D + D + 1)
        pos_idx = idx[:D]
        neg_idx = idx[D:2 * D + 1]
        # positive catalog: all golds + D distractors; a hit = top pick is ANY gold
        cand = np.vstack([gvecs, pool_vecs[pos_idx]])
        sims = cand @ qv
        order = np.argsort(-sims)
        ranks_of_golds = [int(np.where(order == g)[0][0]) for g in range(ng)]
        best_gold_rank = min(ranks_of_golds)
        is_top1 = best_gold_rank == 0
        top1 += is_top1
        rec3 += best_gold_rank < 3
        pos_top_scores.append(float(sims[order[0]]))
        pos_correct_flags.append(is_top1)
        nsims = pool_vecs[neg_idx] @ qv
        neg_top_scores.append(float(nsims.max()))
        c = per_cfg.setdefault(cfg, [0, 0])
        c[1] += 1
        c[0] += is_top1

    N = len(queries)
    # threshold sweep for abstention
    cand_thr = sorted(set(round(s, 3) for s in pos_top_scores))[::max(1, len(pos_top_scores) // 200)]
    sweep = []
    pos_scores = np.array(pos_top_scores)
    pos_correct = np.array(pos_correct_flags)
    neg_scores = np.array(neg_top_scores)
    for thr in cand_thr:
        acc_mask = pos_scores >= thr
        cov = float(acc_mask.mean())
        acc = float(pos_correct[acc_mask].mean()) if acc_mask.any() else float("nan")
        fb = float((neg_scores >= thr).mean())
        sweep.append({"thr": thr, "coverage": cov, "acc_on_accepted": acc, "false_bind": fb})

    out = {
        "model": args.model, "n_queries": N, "pool": npool, "distractors": D,
        "top1": top1 / N, "recall@3": rec3 / N,
        "per_config_top1": {k: v[0] / v[1] for k, v in sorted(per_cfg.items())},
        "sweep": sweep,
    }
    print(json.dumps({k: v for k, v in out.items() if k != "sweep"}, indent=2))
    (RESULTS_DIR / f"toolret_large_{args.model.split('/')[-1]}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print("wrote", RESULTS_DIR / f"toolret_large_{args.model.split('/')[-1]}.json")


if __name__ == "__main__":
    main()
