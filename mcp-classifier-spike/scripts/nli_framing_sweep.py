"""Sweep NLI framing (direction x tool_field x template) to find the best setup.

NLI is directional and phrasing-sensitive, so a bad zero-shot score may be a
framing artifact rather than a real ceiling. This tries a matrix of framings on
the core subset and reports top-1 accuracy, near-duplicate accuracy, and the
score's AUROC as an abstention signal, so we can judge NLI at its best, not its
first naive configuration.
"""

from __future__ import annotations

import argparse
import json

from analyze import auroc
from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval
from methods import NLIScorer

TEMPLATES = {
    "need_premise": [
        "This request requires a tool that can {tool}",
        "To do this the user needs a tool that will {tool}",
        "This is a request to {tool}",
    ],
    "tool_premise": [
        "This tool can {need}",
        "This tool can be used to {need}",
        "This is useful to {need}",
    ],
}


def eval_config(scorer, examples, catalogs):
    pos = [e for e in examples if e.gold]
    neg = [e for e in examples if not e.gold]
    nd = [e for e in pos if "near_duplicate" in e.tags]
    n_correct = 0
    correct_scores = []
    wrong_scores = []
    neg_top_scores = []
    nd_correct = 0
    for e in pos:
        tools = catalogs[e.catalog_id].tools
        scores = scorer.score(e.need, tools)
        order = sorted(range(len(tools)), key=lambda i: scores[i], reverse=True)
        top = tools[order[0]].qualified
        ok = top == e.gold
        n_correct += ok
        (correct_scores if ok else wrong_scores).append(scores[order[0]])
        if "near_duplicate" in e.tags:
            nd_correct += ok
    for e in neg:
        tools = catalogs[e.catalog_id].tools
        scores = scorer.score(e.need, tools)
        neg_top_scores.append(max(scores))
    return {
        "top1": n_correct / len(pos) if pos else float("nan"),
        "near_dupe": nd_correct / len(nd) if nd else float("nan"),
        "abstain_auroc": auroc(correct_scores, wrong_scores),
        "mean_correct_score": sum(correct_scores) / len(correct_scores) if correct_scores else float("nan"),
        "mean_neg_top": sum(neg_top_scores) / len(neg_top_scores) if neg_top_scores else float("nan"),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="valhalla/distilbart-mnli-12-1")
    ap.add_argument("--eval", default="core")
    ap.add_argument("--tool-fields", default="description,name_desc,name")
    ap.add_argument("--name", default="framing")
    args = ap.parse_args()

    examples = load_eval(EVAL_DIR / f"{args.eval}.jsonl")
    catalogs = load_all_catalogs()
    examples = [e for e in examples if e.catalog_id in catalogs]
    fields = args.tool_fields.split(",")

    rows = []
    for direction, templates in TEMPLATES.items():
        for tf in fields:
            for ti, tmpl in enumerate(templates):
                scorer = NLIScorer(args.model, tmpl, direction=direction, tool_field=tf)
                m = eval_config(scorer, examples, catalogs)
                del scorer
                row = {"direction": direction, "tool_field": tf, "template_i": ti, "template": tmpl, **m}
                rows.append(row)
                print(
                    f"{direction:13} {tf:11} t{ti} top1={m['top1']:.3f} nd={m['near_dupe']:.3f} "
                    f"auroc={m['abstain_auroc']:.3f} mc={m['mean_correct_score']:.2f} mn={m['mean_neg_top']:.2f}  | {tmpl}"
                )

    rows.sort(key=lambda r: (0 if r["top1"] != r["top1"] else -r["top1"]))
    print("\nTOP 5 framings by top1:")
    for r in rows[:5]:
        print(f"  top1={r['top1']:.3f} {r['direction']}/{r['tool_field']}/t{r['template_i']}: {r['template']}")
    out = RESULTS_DIR / f"framing_{args.name}.json"
    out.write_text(json.dumps({"model": args.model, "eval": args.eval, "rows": rows}, indent=2), encoding="utf-8")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
