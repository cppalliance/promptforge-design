"""Test hard category-routing vs soft top-k, to check the mixture-of-experts idea.

Partition each catalog's tools into N clusters (KMeans on tool embeddings). Route
the need to the single nearest cluster centroid, then pick the best tool within
that cluster. Compare to flat embedding argmax over the whole catalog.

The question the MoE/category idea hinges on: does hard routing keep the gold tool
reachable? If routing frequently sends the need to the wrong cluster (dropping the
gold before the expert ever sees it), hard partitioning caps accuracy below the
flat and the soft-top-k cascade, and the extra machinery is a net loss.
Reports, per N: route accuracy (gold's cluster == routed cluster), end-to-end top1,
and flat top1 for reference. Fully local.
"""

from __future__ import annotations

import argparse
import json

import numpy as np
from sklearn.cluster import KMeans

from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval

NS = [3, 5, 8]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="real")
    ap.add_argument("--embed", default="BAAI/bge-small-en-v1.5")
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    from methods import auto_device

    model = SentenceTransformer(args.embed, device=auto_device())
    examples = [e for e in load_eval(EVAL_DIR / f"{args.eval}.jsonl") if e.gold]
    catalogs = load_all_catalogs()
    examples = [e for e in examples if e.catalog_id in catalogs]

    agg = {n: {"route": 0, "e2e": 0} for n in NS}
    flat_top1 = 0
    for e in examples:
        tools = catalogs[e.catalog_id].tools
        tvecs = model.encode([t.enriched_text() for t in tools], normalize_embeddings=True, show_progress_bar=False)
        nvec = model.encode(e.need, normalize_embeddings=True, show_progress_bar=False)
        sims = tvecs @ nvec
        gold_i = next(i for i, t in enumerate(tools) if t.qualified == e.gold)
        flat_top1 += int(int(np.argmax(sims)) == gold_i)
        for n in NS:
            n_eff = min(n, len(tools))
            km = KMeans(n_clusters=n_eff, n_init=5, random_state=0).fit(tvecs)
            labels = km.labels_
            # route need to nearest centroid (cosine ~ dot on normalized; centroids not normalized)
            cents = km.cluster_centers_
            cents_n = cents / (np.linalg.norm(cents, axis=1, keepdims=True) + 1e-9)
            routed = int(np.argmax(cents_n @ nvec))
            gold_cluster = labels[gold_i]
            route_ok = routed == gold_cluster
            agg[n]["route"] += int(route_ok)
            # within routed cluster, pick best by sim
            members = [i for i in range(len(tools)) if labels[i] == routed]
            best = max(members, key=lambda i: sims[i])
            agg[n]["e2e"] += int(best == gold_i)

    N = len(examples)
    out = {"eval": args.eval, "n_examples": N, "flat_top1": flat_top1 / N, "by_N": []}
    for n in NS:
        out["by_N"].append(
            {"N_clusters": n, "route_accuracy": agg[n]["route"] / N, "end2end_top1": agg[n]["e2e"] / N}
        )
    print(json.dumps(out, indent=2))
    (RESULTS_DIR / f"cluster_route_{args.eval}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
