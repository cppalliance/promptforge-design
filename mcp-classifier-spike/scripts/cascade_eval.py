"""Two-stage cascade: cheap embedding retrieve -> comparative rerank of the top-k.

Stage 1 (bi-encoder embeddings) sorts the catalog and keeps the top-k shortlist.
Stage 2 (a set-aware method: a cross-encoder reranker, or a listwise LLM that sees
only the k candidates) picks the winner among the shortlist. The listwise stage-2
is cheap because k is small, and it is the only place comparison happens.

Reports:
  - stage1 recall@k        : how often the gold is in the shortlist (the ceiling)
  - stage1 top1            : embeddings alone, for reference
  - cascade top1           : final accuracy after stage-2 picks within the shortlist
  - stage2 pick accuracy   : cascade top1 among only the cases where gold is in top-k
  - false-bind on negatives: for the LLM stage-2 (which can answer "none")
"""

from __future__ import annotations

import argparse
import json

from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval
from methods import AnthropicLLMScorer, CrossEncoderScorer, EmbeddingScorer


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="real")
    ap.add_argument("--stage1", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--k", type=int, default=3)
    ap.add_argument("--stage2", choices=["rerank", "llm"], default="rerank")
    ap.add_argument("--stage2-model", default="BAAI/bge-reranker-v2-m3")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    examples = load_eval(EVAL_DIR / f"{args.eval}.jsonl")
    catalogs = load_all_catalogs()
    examples = [e for e in examples if e.catalog_id in catalogs]
    positives = [e for e in examples if e.gold]
    negatives = [e for e in examples if not e.gold]

    stage1 = EmbeddingScorer(args.stage1)
    if args.stage2 == "rerank":
        stage2 = CrossEncoderScorer(args.stage2_model)
    else:
        stage2 = AnthropicLLMScorer()
        if not stage2.available:
            print("no ANTHROPIC_API_KEY; cannot run llm stage2")
            return

    out_path = args.out or (RESULTS_DIR / f"cascade_{args.eval}_{args.stage2}_k{args.k}.jsonl")
    recs = []

    def shortlist(need, tools):
        s1 = stage1.score(need, tools)
        order = sorted(range(len(tools)), key=lambda i: s1[i], reverse=True)
        return order, s1

    n_recall = 0
    n_stage1_top1 = 0
    n_cascade_top1 = 0
    n_pick_given_present = 0
    n_present = 0
    for e in positives:
        tools = catalogs[e.catalog_id].tools
        order, s1 = shortlist(e.need, tools)
        topk_idx = order[: args.k]
        topk_tools = [tools[i] for i in topk_idx]
        gold_in_topk = any(tools[i].qualified == e.gold for i in topk_idx)
        stage1_top1 = tools[order[0]].qualified == e.gold
        # stage 2 over the shortlist
        s2 = stage2.score(e.need, topk_tools)
        best_local = max(range(len(topk_tools)), key=lambda i: s2[i])
        cascade_pick = topk_tools[best_local].qualified
        cascade_top1 = cascade_pick == e.gold
        n_recall += gold_in_topk
        n_stage1_top1 += stage1_top1
        n_cascade_top1 += cascade_top1
        if gold_in_topk:
            n_present += 1
            n_pick_given_present += cascade_top1
        recs.append(
            {
                "need": e.need, "gold": e.gold, "catalog": e.catalog_id, "tags": e.tags,
                "gold_in_topk": gold_in_topk, "stage1_top1": stage1_top1,
                "cascade_top1": cascade_top1, "cascade_pick": cascade_pick,
            }
        )

    # false-bind: on negatives, does stage2 bind something (llm can say none)
    n_falsebind = 0
    if args.stage2 == "llm":
        for e in negatives:
            tools = catalogs[e.catalog_id].tools
            order, _ = shortlist(e.need, tools)
            topk_tools = [tools[i] for i in order[: args.k]]
            s2 = stage2.score(e.need, topk_tools)
            n_falsebind += 1 if max(s2) > 0 else 0

    P = len(positives)
    summary = {
        "eval": args.eval, "stage1": args.stage1, "stage2": args.stage2,
        "stage2_model": args.stage2_model if args.stage2 == "rerank" else stage2.model_id,
        "k": args.k, "n_positives": P, "n_negatives": len(negatives),
        "recall_at_k": n_recall / P,
        "stage1_top1": n_stage1_top1 / P,
        "cascade_top1": n_cascade_top1 / P,
        "stage2_pick_acc_given_present": (n_pick_given_present / n_present) if n_present else float("nan"),
        "false_bind_rate": (n_falsebind / len(negatives)) if (args.stage2 == "llm" and negatives) else None,
    }
    print(json.dumps(summary, indent=2))
    with open(out_path, "w", encoding="utf-8") as f:
        for r in recs:
            f.write(json.dumps(r) + "\n")
    (RESULTS_DIR / f"cascade_summary_{args.eval}_{args.stage2}_k{args.k}.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
