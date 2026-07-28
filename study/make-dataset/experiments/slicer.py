#!/usr/bin/env python3
"""Slice text into word-count-bounded chunks at natural boundaries.

Reads a JSONL where each record has a text field (default "bloated") and a
"source" label. Splits each record's text into chunks targeting a word count,
never splitting mid-sentence, and emits one pairgen "pair" record per chunk
with source "<orig>#c<N>". Reused by E1 (slice papergate bloat) and E4 (slice
first-gen prompts before blurring).

Usage:
  python slicer.py --in in.jsonl --field bloated --out out.jsonl \
      --target 100 --max 140 --min 40
"""
import argparse
import json
import re


def split_sentences(text):
    # Split on sentence-final punctuation followed by whitespace. Keeps the
    # punctuation with the preceding sentence. Good enough for prose prompts.
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def chunk_text(text, target, max_words, min_words):
    """Greedily pack paragraphs into chunks near `target` words. Split any
    paragraph longer than max_words at sentence boundaries. Merge a trailing
    chunk below min_words into the previous chunk."""
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    units = []
    for p in paras:
        if len(p.split()) <= max_words:
            units.append(p)
        else:
            # break the oversized paragraph into sentence groups
            cur, cur_w = [], 0
            for s in split_sentences(p):
                sw = len(s.split())
                if cur and cur_w + sw > max_words:
                    units.append(" ".join(cur))
                    cur, cur_w = [], 0
                cur.append(s)
                cur_w += sw
            if cur:
                units.append(" ".join(cur))

    chunks, cur, cur_w = [], [], 0
    for u in units:
        uw = len(u.split())
        if cur and cur_w + uw > target and cur_w >= min_words:
            chunks.append("\n\n".join(cur))
            cur, cur_w = [], 0
        cur.append(u)
        cur_w += uw
    if cur:
        chunks.append("\n\n".join(cur))

    # merge a too-small tail into the previous chunk
    if len(chunks) >= 2 and len(chunks[-1].split()) < min_words:
        chunks[-2] = chunks[-2] + "\n\n" + chunks[-1]
        chunks.pop()
    return chunks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--field", default="bloated")
    ap.add_argument("--out", required=True)
    ap.add_argument("--target", type=int, default=100)
    ap.add_argument("--max", type=int, default=140)
    ap.add_argument("--min", type=int, default=40)
    a = ap.parse_args()

    n_in = n_out = 0
    with open(a.out, "w", encoding="utf-8") as w:
        for line in open(a.inp, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            n_in += 1
            src = r.get("source", f"rec{n_in}")
            text = r[a.field]
            for i, ch in enumerate(chunk_text(text, a.target, a.max, a.min), 1):
                rec = {"kind": "pair", "source": f"{src}#c{i}", "bloated": ch}
                w.write(json.dumps(rec) + "\n")
                n_out += 1
    print(f"sliced {n_in} records into {n_out} chunks -> {a.out}")


if __name__ == "__main__":
    main()
