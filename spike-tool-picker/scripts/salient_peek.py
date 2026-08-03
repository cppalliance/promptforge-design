"""Pick 30 random real needs and show the single most salient word in each.

Salient = highest-IDF content token (rare across the query set, not a stopword,
not a bare number). Deterministic given the seed. Just for eyeballing.
"""

from __future__ import annotations

import json
import math
import random
import re

STOP = set(
    "the a an and or of to for in on with without into from by is are be can could would "
    "i we you it this that these those my our your need want would like please help me get "
    "find using use able so which what how do does using given all any some new as at any "
    "have has want wanted create make set list show tell give provide return".split()
)


def tokens(s):
    return [w for w in re.findall(r"[a-zA-Z][a-zA-Z0-9_.-]+", s.lower()) if len(w) >= 3 and w not in STOP]


def main():
    from datasets import get_dataset_config_names, load_dataset

    cfgs = get_dataset_config_names("mangopy/ToolRet-Queries")
    rng = random.Random(7)
    rng.shuffle(cfgs)
    needs = []
    for cfg in cfgs[:12]:
        try:
            d = load_dataset("mangopy/ToolRet-Queries", cfg)
        except Exception:  # noqa: BLE001
            continue
        sp = list(d.keys())[0]
        for r in d[sp]:
            q = (r.get("query") or "").strip()
            if 3 <= len(q.split()) <= 40:
                needs.append(q)
    # document frequency over the need set
    df = {}
    for q in needs:
        for w in set(tokens(q)):
            df[w] = df.get(w, 0) + 1
    N = len(needs)
    idf = {w: math.log(N / c) for w, c in df.items()}

    sample = rng.sample(needs, 30)
    print(f"(idf over {N} needs)\n")
    for q in sample:
        ts = tokens(q)
        if not ts:
            best = "-"
        else:
            best = max(ts, key=lambda w: idf.get(w, math.log(N)))
        disp = q if len(q) <= 100 else q[:97] + "..."
        print(f"- **{best}** - {disp}")


if __name__ == "__main__":
    main()
