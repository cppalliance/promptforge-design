#!/usr/bin/env python3
"""Assemble the clean training dataset from all experiment outputs.

Two pair types:
  - blur-to-original: input is a blurred first-gen section, target is the true
    sharp original (E4). Clean by construction; the target is known-sharp.
  - bloat-to-sharp: input is bloated text, target is the instrument-sharpened
    version, kept only where gate1 PASS (execution-equivalent) (E2-off, E3, E5,
    E6). A valid compression pair even though it is not the source's original.

Dedupes bloat-to-sharp by input text. Emits dataset-clean.jsonl and prints
counts, compression distribution, and source distribution.
"""
import glob
import json
import statistics as st


def wc(s):
    return len(s.split())


def load(path):
    try:
        return [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    except FileNotFoundError:
        return []


D = "experiments"
out = []

# blur-to-original from E4 (all passes)
for f in sorted(glob.glob(f"{D}/e4-roundtrip/e4-blur.shard*.jsonl")):
    for r in load(f):
        b, o = r["blurred"], r["original"]
        if b and o and b != o:
            out.append({
                "type": "blur-to-original",
                "source": f"first-gen-p{r['pass']}",
                "input": b,
                "target": o,
                "input_words": wc(b),
                "target_words": wc(o),
            })

# bloat-to-sharp from gate1-passing kept pairs across runs
seen = set()
bloat_sources = [
    ("e2-off", f"{D}/e2-gate-modes/e2-off-out.jsonl"),
    ("e3-web", f"{D}/e3-shitprompts/e3-out.jsonl"),
    ("e5-high", f"{D}/e5-effort/e5-high-out.jsonl"),
    ("e5-medium", f"{D}/e5-effort/e5-medium-out.jsonl"),
    ("e6-minimal", f"{D}/e6-multipass/e6-out.jsonl"),
]
for tag, path in bloat_sources:
    for r in load(path):
        if r.get("gate1") != "PASS" or not r.get("sharpened"):
            continue
        key = r["bloated"][:120]
        if key in seen:
            continue
        seen.add(key)
        out.append({
            "type": "bloat-to-sharp",
            "source": tag,
            "input": r["bloated"],
            "target": r["sharpened"],
            "input_words": wc(r["bloated"]),
            "target_words": wc(r["sharpened"]),
        })

with open(f"{D}/dataset-clean.jsonl", "w", encoding="utf-8") as w:
    for r in out:
        w.write(json.dumps(r) + "\n")

# stats
by_type = {}
for r in out:
    by_type.setdefault(r["type"], []).append(r)
print(f"total clean pairs: {len(out)} -> {D}/dataset-clean.jsonl")
for t, rs in by_type.items():
    ratios = [r["target_words"] / max(1, r["input_words"]) for r in rs]
    print(
        f"  {t}: {len(rs)} pairs | input median {st.median(r['input_words'] for r in rs):.0f}w "
        f"target median {st.median(r['target_words'] for r in rs):.0f}w | "
        f"size ratio median {st.median(ratios):.2f}"
    )
srcs = {}
for r in out:
    srcs[r["source"]] = srcs.get(r["source"], 0) + 1
print("source distribution:", dict(sorted(srcs.items())))
