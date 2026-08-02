"""Run every scoring method over an eval set and record per-example rankings.

Usage:
  python run_eval.py --eval seed --methods nli,embed,bm25 \
      --nli-models facebook/bart-large-mnli,MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli \
      --templates capability,usage --out results/seed_run.jsonl

Each output record is one (method, model, template, example) result with the
top-ranked tools and the fields the analysis needs (gold rank, top-1, margin).
Deterministic methods are run once; `--repeats` re-runs to confirm determinism.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval
from methods import AnthropicLLMScorer, BM25Scorer, CrossEncoderScorer, EmbeddingScorer, NLI_CONFIGS, LLMScorer, NLIScorer


def rank(need, tools, scorer):
    scores = scorer.score(need, tools)
    order = sorted(range(len(tools)), key=lambda i: scores[i], reverse=True)
    ranked = [(tools[i].qualified, float(scores[i])) for i in order]
    return ranked


def eval_method(scorer, method_name, model_id, template, examples, catalogs, repeats, fout):
    n = 0
    t0 = time.time()
    for rep in range(repeats):
        for ex in examples:
            cat = catalogs[ex.catalog_id]
            ranked = rank(ex.need, cat.tools, scorer)
            top1_q, top1_s = ranked[0]
            top2_s = ranked[1][1] if len(ranked) > 1 else float("-inf")
            gold_rank = None
            gold_score = None
            if ex.gold is not None:
                for r, (q, s) in enumerate(ranked):
                    if q == ex.gold:
                        gold_rank = r
                        gold_score = s
                        break
            rec = {
                "method": method_name,
                "model_id": model_id,
                "template": template,
                "repeat": rep,
                "need": ex.need,
                "catalog_id": ex.catalog_id,
                "gold": ex.gold,
                "tags": ex.tags,
                "n_tools": len(cat.tools),
                "top1": top1_q,
                "top1_score": top1_s,
                "top2_margin": float(top1_s - top2_s),
                "gold_rank": gold_rank,
                "gold_score": gold_score,
                "ranked_top5": ranked[:5],
            }
            fout.write(json.dumps(rec) + "\n")
            n += 1
    dt = time.time() - t0
    print(f"  [{method_name}:{model_id}:{template}] {n} records in {dt:.1f}s ({n/max(dt,1e-9):.1f}/s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="seed", help="eval set name (file data/eval/<name>.jsonl)")
    ap.add_argument("--methods", default="nli,embed,bm25")
    ap.add_argument("--nli-models", default="facebook/bart-large-mnli")
    ap.add_argument("--embed-models", default="sentence-transformers/all-MiniLM-L6-v2")
    ap.add_argument("--rerank-models", default="cross-encoder/ms-marco-MiniLM-L-6-v2")
    ap.add_argument("--nli-configs", default="best", help="comma list of names from NLI_CONFIGS")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    examples = load_eval(EVAL_DIR / f"{args.eval}.jsonl")
    catalogs = load_all_catalogs()
    # keep only examples whose catalog is present
    examples = [e for e in examples if e.catalog_id in catalogs]
    print(f"eval={args.eval}  examples={len(examples)}  catalogs={len(catalogs)}")

    out_path = Path(args.out) if args.out else RESULTS_DIR / f"{args.eval}_run.jsonl"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    methods = args.methods.split(",")
    nli_configs = [t.strip() for t in args.nli_configs.split(",") if t.strip()]

    with out_path.open("w", encoding="utf-8") as fout:
        if "bm25" in methods:
            eval_method(BM25Scorer(), "bm25", "bm25", "-", examples, catalogs, args.repeats, fout)
        if "embed" in methods:
            for m in args.embed_models.split(","):
                m = m.strip()
                if m:
                    try:
                        print(f"loading embed {m} ...")
                        eval_method(EmbeddingScorer(m), "embed", m, "-", examples, catalogs, args.repeats, fout)
                    except Exception as e:  # noqa: BLE001
                        print(f"  [embed {m}] FAILED: {e}")
        if "rerank" in methods:
            for m in args.rerank_models.split(","):
                m = m.strip()
                if m:
                    try:
                        print(f"loading rerank {m} ...")
                        eval_method(CrossEncoderScorer(m), "rerank", m, "-", examples, catalogs, args.repeats, fout)
                    except Exception as e:  # noqa: BLE001
                        print(f"  [rerank {m}] FAILED: {e}")
        if "nli" in methods:
            for m in args.nli_models.split(","):
                m = m.strip()
                if not m:
                    continue
                for cfg_name in nli_configs:
                    cfg = NLI_CONFIGS[cfg_name]
                    try:
                        print(f"loading nli {m} config={cfg_name} ...")
                        scorer = NLIScorer(m, cfg["template"], direction=cfg["direction"], tool_field=cfg["tool_field"])
                        eval_method(scorer, "nli", m, cfg_name, examples, catalogs, args.repeats, fout)
                        del scorer
                    except Exception as e:  # noqa: BLE001
                        print(f"  [nli {m}/{cfg_name}] FAILED: {e}")
        if "llm" in methods:
            llm = LLMScorer()
            if llm.available:
                eval_method(llm, "llm", llm.model_id, "-", examples, catalogs, 1, fout)
            else:
                print("  [llm] skipped: no OpenAI API key")
        if "llm_anthropic" in methods:
            allm = AnthropicLLMScorer()
            if allm.available:
                eval_method(allm, "llm", allm.model_id, "-", examples, catalogs, 1, fout)
            else:
                print("  [llm_anthropic] skipped: no ANTHROPIC_API_KEY")

    print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
