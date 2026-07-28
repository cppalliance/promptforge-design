#!/usr/bin/env python3
"""Parse awesome-chatgpt-prompts CSV into pairgen pair records.

Extracts the `prompt` column, filters to a word-count band, dedupes, and
samples diversely across the length range. Emits pairgen "pair" JSONL.

Usage:
  python parse-csv.py --csv awesome-prompts.csv --out e3-in.jsonl \
      --n 30 --min 50 --max 500
"""
import argparse
import csv
import json
import re

# Some rows carry very large multiline prompts; lift the default field cap.
csv.field_size_limit(10_000_000)


def slug(s, n=24):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    return s[:n] or "prompt"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=30, help="0 = emit all qualifying")
    ap.add_argument("--min", type=int, default=50)
    ap.add_argument("--max", type=int, default=500)
    a = ap.parse_args()

    seen = set()
    rows = []
    with open(a.csv, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            p = (row.get("prompt") or "").strip()
            wc = len(p.split())
            if wc < a.min or wc > a.max:
                continue
            key = p[:80]
            if key in seen:
                continue
            seen.add(key)
            rows.append((wc, slug(row.get("act", "")), p))

    rows.sort()  # by word count
    if a.n and a.n < len(rows):
        # even stride across the sorted range for length diversity
        stride = len(rows) / a.n
        picked = [rows[int(i * stride)] for i in range(a.n)]
    else:
        picked = rows

    with open(a.out, "w", encoding="utf-8") as w:
        for wc, act, p in picked:
            rec = {"kind": "pair", "source": f"acgp-{act}", "bloated": p}
            w.write(json.dumps(rec) + "\n")
    wcs = sorted(wc for wc, _, _ in picked)
    print(
        f"qualifying: {len(rows)} | emitted: {len(picked)} -> {a.out} | "
        f"wc min {wcs[0]} median {wcs[len(wcs)//2]} max {wcs[-1]}"
    )


if __name__ == "__main__":
    main()
