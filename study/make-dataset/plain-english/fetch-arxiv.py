#!/usr/bin/env python3
"""Fetch sharp arXiv abstracts across categories as blur source passages.

Abstracts are dense, meaning-complete, and span broad technical vocabulary -
ideal sharp originals. Shells out to curl (proven to work in this env) against
the arXiv Atom API over HTTPS, parses <summary>, filters by word count,
dedupes, and writes {source, id, text} JSONL.

Usage: python fetch-arxiv.py --out passages.jsonl --n 100 --min 80 --max 250
"""
import argparse
import json
import re
import subprocess
import time
import xml.etree.ElementTree as ET

CATEGORIES = [
    "cs.CL", "cs.LG", "math.NA", "math.PR", "q-bio.NC",
    "econ.EM", "stat.ME", "physics.optics", "astro-ph.GA", "cond-mat.soft",
]
NS = {"a": "http://www.w3.org/2005/Atom"}


def curl(url):
    return subprocess.run(
        ["curl", "-sS", "--max-time", "30",
         "-H", "User-Agent: promptforge-study/1.0 (research)", url],
        capture_output=True, text=True, encoding="utf-8",
    ).stdout


def clean(t):
    return re.sub(r"\s+", " ", t).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--n", type=int, default=100)
    ap.add_argument("--min", type=int, default=80)
    ap.add_argument("--max", type=int, default=250)
    ap.add_argument("--per-cat", type=int, default=25)
    a = ap.parse_args()

    seen, rows = set(), []
    for cat in CATEGORIES:
        if len(rows) >= a.n:
            break
        url = (
            "https://export.arxiv.org/api/query?search_query=cat:"
            f"{cat}&start=0&max_results={a.per_cat}"
            "&sortBy=submittedDate&sortOrder=descending"
        )
        xml = curl(url)
        try:
            root = ET.fromstring(xml)
        except ET.ParseError:
            print(f"  parse error for {cat}, skipping")
            time.sleep(3)
            continue
        got = 0
        for e in root.findall("a:entry", NS):
            sm = e.find("a:summary", NS)
            idn = e.find("a:id", NS)
            if sm is None or sm.text is None or idn is None:
                continue
            text = clean(sm.text)
            wc = len(text.split())
            if wc < a.min or wc > a.max:
                continue
            key = (idn.text or "").strip()
            if key in seen:
                continue
            seen.add(key)
            rows.append({"source": "arxiv", "id": key, "text": text})
            got += 1
        print(f"  {cat}: +{got} (total {len(rows)})")
        time.sleep(3)  # arXiv politeness

    rows = rows[: a.n]
    with open(a.out, "w", encoding="utf-8") as w:
        for r in rows:
            w.write(json.dumps(r) + "\n")
    wcs = sorted(len(r["text"].split()) for r in rows)
    print(f"wrote {len(rows)} arXiv abstracts -> {a.out}"
          + (f" | wc {wcs[0]}/{wcs[len(wcs)//2]}/{wcs[-1]}" if wcs else ""))


if __name__ == "__main__":
    main()
