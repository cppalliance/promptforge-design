"""Measure near-duplicate prevalence in a real 9,922-tool catalog.

For each tool, find its nearest neighbor (max cosine to any other tool) using
bge-small embeddings of the enriched text. Report the distribution, counts above
several thresholds, and whether near-duplicate pairs are cross-server (the foreign-
import case) or same-server (a likely config smell). This sets the "fail loud on
duplicates" threshold and estimates how often the ambiguous outcome fires.
"""

from __future__ import annotations

import json

import numpy as np

from common import RESULTS_DIR
from lua_register_eval import load_automatelab


def main():
    from sentence_transformers import SentenceTransformer
    from methods import auto_device

    tools = load_automatelab()
    model = SentenceTransformer("BAAI/bge-small-en-v1.5", device=auto_device())
    vecs = model.encode([t.enriched_text() for t in tools], normalize_embeddings=True, batch_size=256, show_progress_bar=False)
    vecs = np.asarray(vecs, dtype=np.float32)
    n = len(tools)

    nn_sim = np.zeros(n, dtype=np.float32)
    nn_idx = np.zeros(n, dtype=np.int64)
    chunk = 512
    for s in range(0, n, chunk):
        e = min(s + chunk, n)
        block = vecs[s:e] @ vecs.T          # (chunk, n)
        for r in range(e - s):
            block[r, s + r] = -1.0          # exclude self
        nn_idx[s:e] = block.argmax(axis=1)
        nn_sim[s:e] = block.max(axis=1)

    pct = {p: float(np.percentile(nn_sim, p)) for p in (50, 75, 90, 95, 99)}
    out = {"n_tools": n, "nn_sim_percentiles": pct, "thresholds": {}}
    for thr in (0.90, 0.95, 0.98, 0.99):
        mask = nn_sim >= thr
        cross = same = 0
        for i in np.where(mask)[0]:
            j = nn_idx[i]
            if tools[i].server != tools[j].server:
                cross += 1
            else:
                same += 1
        out["thresholds"][str(thr)] = {
            "tools_with_nn_above": int(mask.sum()),
            "frac": float(mask.mean()),
            "cross_server": cross,
            "same_server": same,
        }

    print(json.dumps(out, indent=2))
    print("\nExample near-duplicate pairs (nn_sim >= 0.97):")
    shown = 0
    for i in np.argsort(-nn_sim):
        if nn_sim[i] < 0.97:
            break
        j = nn_idx[i]
        if i < j:  # print each pair once
            print(f"  {nn_sim[i]:.3f} | [{tools[i].server}::{tools[i].name}] <> [{tools[j].server}::{tools[j].name}]")
            shown += 1
            if shown >= 15:
                break
    (RESULTS_DIR / "dup_scan.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
