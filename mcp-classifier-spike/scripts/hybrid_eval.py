"""Hybrid lexical+dense fusion: does adding a BM25 word-count signal help embeddings?

For each example we rank the catalog three ways - BM25 (lexical), a dense embedding
model, and their reciprocal-rank fusion (RRF) - and report top-1 and recall@3. RRF
combines rankings deterministically: score(tool) = sum over rankers of 1/(c + rank).
This tests the productive form of "do a word-count pass": fuse it with embeddings
rather than prefilter with it. Fully local, no LLM.
"""

from __future__ import annotations

import argparse
import json

from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval
from methods import BM25Scorer, EmbeddingScorer


def ranks_from_scores(scores):
    order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    rank = [0] * len(scores)
    for r, i in enumerate(order):
        rank[i] = r
    return rank


def top1_recall(pick_order, tools, gold, k=3):
    top1 = tools[pick_order[0]].qualified == gold
    ink = any(tools[i].qualified == gold for i in pick_order[:k])
    return top1, ink


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="real")
    ap.add_argument("--embed", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--c", type=float, default=60.0)
    args = ap.parse_args()

    examples = [e for e in load_eval(EVAL_DIR / f"{args.eval}.jsonl") if e.gold]
    catalogs = load_all_catalogs()
    examples = [e for e in examples if e.catalog_id in catalogs]
    bm25 = BM25Scorer()
    emb = EmbeddingScorer(args.embed)

    agg = {m: {"top1": 0, "rec3": 0} for m in ("bm25", "embed", "rrf")}
    for e in examples:
        tools = catalogs[e.catalog_id].tools
        bs = bm25.score(e.need, tools)
        es = emb.score(e.need, tools)
        br = ranks_from_scores(bs)
        er = ranks_from_scores(es)
        rrf = [1.0 / (args.c + br[i]) + 1.0 / (args.c + er[i]) for i in range(len(tools))]
        for m, sc in (("bm25", bs), ("embed", es), ("rrf", rrf)):
            order = sorted(range(len(tools)), key=lambda i: sc[i], reverse=True)
            t1, r3 = top1_recall(order, tools, e.gold)
            agg[m]["top1"] += t1
            agg[m]["rec3"] += r3

    n = len(examples)
    out = {"eval": args.eval, "embed": args.embed, "n": n,
           "results": {m: {"top1": v["top1"] / n, "recall@3": v["rec3"] / n} for m, v in agg.items()}}
    print(json.dumps(out, indent=2))
    (RESULTS_DIR / f"hybrid_{args.eval}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
