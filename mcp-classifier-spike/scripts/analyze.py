"""Analyze run records: accuracy, abstention, calibration, disambiguation.

Reads one or more results JSONL files and produces, per (method, model, template):
  - top1 / top3 accuracy on positives
  - AUROC of the top-1 score separating correct from incorrect top-1 picks
    (how usable the score is as a confidence signal for abstaining)
  - a threshold sweep giving, at each accept threshold: coverage, accuracy on
    accepted positives, and false-bind rate on hard negatives
  - the best threshold under the rule "keep false-bind <= target", with the
    accuracy and coverage achieved there
  - near-duplicate disambiguation accuracy
Bootstrap 95% CIs are reported for headline accuracy.

Everything is written to results/analysis_<name>.json and printed as tables.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path

from common import RESULTS_DIR


def load_records(paths):
    recs = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    recs.append(json.loads(line))
    return recs


def auroc(pos_scores, neg_scores):
    """AUROC via rank-sum (Mann-Whitney). pos = correct top-1, neg = incorrect."""
    if not pos_scores or not neg_scores:
        return float("nan")
    alls = [(s, 1) for s in pos_scores] + [(s, 0) for s in neg_scores]
    alls.sort(key=lambda x: x[0])
    # average ranks
    ranks = [0.0] * len(alls)
    i = 0
    while i < len(alls):
        j = i
        while j + 1 < len(alls) and alls[j + 1][0] == alls[i][0]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j + 1):
            ranks[k] = avg
        i = j + 1
    sum_pos = sum(r for r, (_, lab) in zip(ranks, alls) if lab == 1)
    n_pos = len(pos_scores)
    n_neg = len(neg_scores)
    return (sum_pos - n_pos * (n_pos + 1) / 2.0) / (n_pos * n_neg)


def bootstrap_ci(bools, iters=2000, seed=0):
    if not bools:
        return (float("nan"), float("nan"), float("nan"))
    rng = random.Random(seed)
    n = len(bools)
    means = []
    for _ in range(iters):
        s = sum(bools[rng.randrange(n)] for _ in range(n))
        means.append(s / n)
    means.sort()
    lo = means[int(0.025 * iters)]
    hi = means[int(0.975 * iters)]
    return (sum(bools) / n, lo, hi)


def analyze(records):
    groups = defaultdict(list)
    for r in records:
        if r.get("repeat", 0) != 0:
            continue  # analyze first repeat; determinism checked separately
        groups[(r["method"], r["model_id"], r["template"])].append(r)

    out = {}
    for key, recs in groups.items():
        method, model, template = key
        positives = [r for r in recs if r["gold"] is not None]
        negatives = [r for r in recs if r["gold"] is None]
        near_dupe = [r for r in positives if "near_duplicate" in r["tags"]]

        # accuracy
        top1_correct = [1 if r["top1"] == r["gold"] else 0 for r in positives]
        top3_correct = [1 if (r["gold_rank"] is not None and r["gold_rank"] < 3) else 0 for r in positives]
        acc, acc_lo, acc_hi = bootstrap_ci(top1_correct)
        top3 = sum(top3_correct) / len(top3_correct) if top3_correct else float("nan")

        # score-as-confidence: correct top-1 vs incorrect top-1 (positives only)
        pos_correct_scores = [r["top1_score"] for r in positives if r["top1"] == r["gold"]]
        pos_wrong_scores = [r["top1_score"] for r in positives if r["top1"] != r["gold"]]
        au = auroc(pos_correct_scores, pos_wrong_scores)

        # threshold sweep: accept if top1_score >= thr.
        cand_scores = sorted({round(r["top1_score"], 4) for r in recs})
        sweep = []
        for thr in cand_scores:
            acc_pos = [r for r in positives if r["top1_score"] >= thr]
            cov = len(acc_pos) / len(positives) if positives else 0.0
            acc_on_acc = (sum(1 for r in acc_pos if r["top1"] == r["gold"]) / len(acc_pos)) if acc_pos else float("nan")
            fb = (sum(1 for r in negatives if r["top1_score"] >= thr) / len(negatives)) if negatives else float("nan")
            sweep.append({"thr": thr, "coverage": cov, "acc_on_accepted": acc_on_acc, "false_bind": fb})

        # best threshold under false-bind <= 0.05, maximizing coverage*acc
        best = None
        for row in sweep:
            fb = row["false_bind"]
            if math.isnan(fb) or fb <= 0.05:
                score = row["coverage"] * (0 if math.isnan(row["acc_on_accepted"]) else row["acc_on_accepted"])
                if best is None or score > best["_score"]:
                    best = {**row, "_score": score}

        nd_acc = (sum(1 for r in near_dupe if r["top1"] == r["gold"]) / len(near_dupe)) if near_dupe else float("nan")

        out[f"{method}|{model}|{template}"] = {
            "method": method,
            "model": model,
            "template": template,
            "n_positives": len(positives),
            "n_negatives": len(negatives),
            "top1_acc": acc,
            "top1_acc_ci": [acc_lo, acc_hi],
            "top3_acc": top3,
            "score_auroc": au,
            "near_dupe_acc": nd_acc,
            "best_thr_at_fb5": best,
            "sweep": sweep,
        }
    return out


def determinism_check(records):
    """Return max abs score delta across repeats for identical (method,model,template,need,catalog)."""
    by = defaultdict(dict)
    for r in records:
        k = (r["method"], r["model_id"], r["template"], r["need"], r["catalog_id"])
        by[k][r.get("repeat", 0)] = r["top1_score"]
    max_delta = 0.0
    multi = 0
    for k, reps in by.items():
        if len(reps) > 1:
            multi += 1
            vals = list(reps.values())
            max_delta = max(max_delta, max(vals) - min(vals))
    return {"pairs_with_repeats": multi, "max_top1_score_delta": max_delta}


def fmt(x, nd=3):
    if x is None:
        return "-"
    if isinstance(x, float) and math.isnan(x):
        return "nan"
    return f"{x:.{nd}f}" if isinstance(x, float) else str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", nargs="+", required=True)
    ap.add_argument("--name", default="analysis")
    args = ap.parse_args()

    paths = [Path(p) for p in args.results]
    records = load_records(paths)
    print(f"loaded {len(records)} records from {len(paths)} file(s)")

    analysis = analyze(records)
    det = determinism_check(records)

    rows = sorted(analysis.values(), key=lambda d: (0 if math.isnan(d["top1_acc"]) else -d["top1_acc"]))
    header = f"{'method':6} {'model':52} {'tmpl':11} {'top1':>6} {'ci':>15} {'top3':>6} {'auroc':>6} {'nd':>6} {'best_thr':>8} {'cov@fb5':>8} {'acc@fb5':>8}"
    print("\n" + header)
    print("-" * len(header))
    for d in rows:
        best = d["best_thr_at_fb5"]
        ci = f"[{fmt(d['top1_acc_ci'][0],2)},{fmt(d['top1_acc_ci'][1],2)}]"
        print(
            f"{d['method']:6} {d['model'][:52]:52} {d['template']:11} "
            f"{fmt(d['top1_acc']):>6} {ci:>15} {fmt(d['top3_acc']):>6} {fmt(d['score_auroc']):>6} "
            f"{fmt(d['near_dupe_acc']):>6} "
            f"{fmt(best['thr']) if best else '-':>8} {fmt(best['coverage']) if best else '-':>8} "
            f"{fmt(best['acc_on_accepted']) if best else '-':>8}"
        )

    print(f"\ndeterminism: {det}")

    out_path = RESULTS_DIR / f"analysis_{args.name}.json"
    out_path.write_text(json.dumps({"analysis": analysis, "determinism": det}, indent=2), encoding="utf-8")
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
