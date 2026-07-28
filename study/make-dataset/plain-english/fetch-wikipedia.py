#!/usr/bin/env python3
"""Fetch Wikipedia lead extracts as blur source passages.

Lead sections are meaning-dense modern English across every domain - broad
vocabulary. Shells out to curl against the Action API with generator=random
plus plain-text intro extracts (batch, many per call), filters by word count,
dedupes by title, and writes {source, id, text} JSONL.

Usage: python fetch-wikipedia.py --out passages.jsonl --n 100 --min 60 --max 200
"""
import argparse
import json
import re
import subprocess
import time

API = (
    "https://en.wikipedia.org/w/api.php?format=json&action=query"
    "&generator=random&grnnamespace=0&grnlimit=20"
    "&prop=extracts&exintro&explaintext"
)


def curl(url):
    return subprocess.run(
        ["curl", "-sS", "--max-time", "30",
         "-H", "User-Agent: promptforge-study/1.0 (research; contact vinnie)", url],
        capture_output=True, text=True, encoding="utf-8",
    ).stdout


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--min", type=int, default=60)
    ap.add_argument("--max", type=int, default=200)
    ap.add_argument("--max-calls", type=int, default=40)
    a = ap.parse_args()

    seen, rows = set(), []
    for call in range(a.max_calls):
        if len(rows) >= a.n:
            break
        out = curl(API)
        try:
            d = json.loads(out)
        except json.JSONDecodeError:
            time.sleep(1)
            continue
        pages = d.get("query", {}).get("pages", {})
        for p in pages.values():
            title = p.get("title", "")
            text = clean(p.get("extract", ""))
            wc = len(text.split())
            if wc < a.min or wc > a.max:
                continue
            if title in seen:
                continue
            seen.add(title)
            rows.append({"source": "wikipedia", "id": title, "text": text})
        print(f"  call {call + 1}: total {len(rows)}")
        time.sleep(1)  # politeness

    rows = rows[: a.n]
    with open(a.out, "w", encoding="utf-8") as w:
        for r in rows:
            w.write(json.dumps(r) + "\n")
    wcs = sorted(len(r["text"].split()) for r in rows)
    print(f"wrote {len(rows)} Wikipedia leads -> {a.out}"
          + (f" | wc {wcs[0]}/{wcs[len(wcs)//2]}/{wcs[-1]}" if wcs else ""))


if __name__ == "__main__":
    main()
