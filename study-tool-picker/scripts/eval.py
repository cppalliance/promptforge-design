"""Score the dataset and write RESULTS.md.

For each need, two candidate sets: gold + hard distractors, and gold + random distractors.
Reports top-1 and recall@3 for each regime, broken down by band, for each embedding model,
plus an abstention sweep (positive top-score vs a distractors-only negative catalog) for the
hard regime. Deterministic; reuses cached catalog embeddings.
"""

from __future__ import annotations

import argparse
import json
from collections import defaultdict

import numpy as np

from build_eval import embed_catalog, _cuda
from common import DATA, ROOT, load_catalog, load_needs

BANDS = ["restatement", "synonym", "goal"]


def score_model(model_id, tools, needs):
    from sentence_transformers import SentenceTransformer
    pool = embed_catalog(tools, model_id)
    m = SentenceTransformer(model_id, device="cuda" if _cuda() else "cpu")
    qv = np.asarray(m.encode([nd["need"] for nd in needs], normalize_embeddings=True,
                             batch_size=256, show_progress_bar=False), dtype=np.float32)

    def run(regime):
        by_band = defaultdict(lambda: [0, 0, 0])  # top1, rec3, n
        pos_scores, pos_ok, neg_scores = [], [], []
        for i, nd in enumerate(needs):
            g = nd["gold_id"]
            dist = nd["hard_distractor_ids"] if regime == "hard" else nd["random_distractor_ids"]
            cand = np.array([g] + dist)
            sims = pool[cand] @ qv[i]
            order = np.argsort(-sims)
            gr = int(np.where(order == 0)[0][0])
            ok = gr == 0
            b = by_band[nd["band"]]
            b[0] += ok; b[1] += gr < 3; b[2] += 1
            pos_scores.append(float(sims[order[0]])); pos_ok.append(ok)
            neg = pool[np.array(dist)] @ qv[i]
            neg_scores.append(float(neg.max()))
        return by_band, np.array(pos_scores), np.array(pos_ok), np.array(neg_scores)

    res = {}
    for regime in ("random", "hard"):
        by_band, ps, pok, ns = run(regime)
        tot = [sum(by_band[b][k] for b in by_band) for k in range(3)]
        res[regime] = {
            "overall_top1": tot[0] / tot[2], "overall_rec3": tot[1] / tot[2],
            "by_band": {b: {"top1": by_band[b][0] / by_band[b][2], "rec3": by_band[b][1] / by_band[b][2],
                            "n": by_band[b][2]} for b in BANDS if b in by_band},
        }
        if regime == "hard":
            sweep = []
            for thr in sorted(set(round(float(s), 3) for s in ps)):
                acc = ps >= thr
                cov = float(acc.mean())
                a = float(pok[acc].mean()) if acc.any() else float("nan")
                fb = float((ns >= thr).mean())
                sweep.append((thr, cov, a, fb))
            res["abstain_hard"] = sweep
    return res


def op_point(sweep, budget):
    best = None
    for thr, cov, acc, fb in sweep:
        if fb <= budget and (best is None or cov > best[1]):
            best = (thr, cov, acc, fb)
    return best


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="BAAI/bge-small-en-v1.5,sentence-transformers/all-MiniLM-L6-v2")
    args = ap.parse_args()
    tools = load_catalog()
    needs = load_needs()
    lines = ["# Results", "", f"Cases: {len(needs)} | Catalog: {len(tools)} tools", ""]
    for model_id in args.models.split(","):
        model_id = model_id.strip()
        r = score_model(model_id, tools, needs)
        lines.append(f"## {model_id}")
        for regime in ("random", "hard"):
            rr = r[regime]
            lines.append(f"- {regime} distractors: top-1 {rr['overall_top1']:.3f}, recall@3 {rr['overall_rec3']:.3f}")
            for b in BANDS:
                if b in rr["by_band"]:
                    bb = rr["by_band"][b]
                    lines.append(f"    - {b}: top-1 {bb['top1']:.3f}, recall@3 {bb['rec3']:.3f} (n={bb['n']})")
        lines.append("- abstention (hard regime), max coverage at false-bind budget:")
        for budget in (0.01, 0.05, 0.10):
            op = op_point(r["abstain_hard"], budget)
            if op:
                lines.append(f"    - fb<={budget:.2f}: coverage {op[1]:.2f} at accuracy {op[2]:.3f} (thr {op[0]:.3f})")
        lines.append("")
    (ROOT / "RESULTS.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
