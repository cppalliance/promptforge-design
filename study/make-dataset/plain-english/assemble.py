#!/usr/bin/env python3
"""Two-phase assembler for the plain-English blur datasets.

gate-input: read blur output, strip synthetic headings (and any leading
  "# Rewritten Text" boilerplate) from original and blurred, and emit pairgen
  control records {kind:control, source, a:original, b:blurred} so gate1 runs
  the directional meaning check gate1(A=original, B=blurred).

finalize: read the gate output, keep only gate1 PASS (blur preserved every-
  thing in the original), and emit training pairs
  {type:"blur-to-original", source, input:blurred, target:original, ...}.
  Also print stats and a few gate-FAIL drops for the log.

Usage:
  python assemble.py gate-input --blur blur.jsonl --name arxiv --out gate-in.jsonl
  python assemble.py finalize --gate-out gate-out.jsonl --name arxiv --out dataset-arxiv.jsonl
"""
import argparse
import json
import re

HEADING = re.compile(r"^#{1,6}\s")


def strip_lead(text):
    """Drop leading blank lines and heading lines (synthetic ## pNNNN or a
    stray '# Rewritten Text') until real content starts."""
    lines = text.splitlines()
    i = 0
    while i < len(lines) and (not lines[i].strip() or HEADING.match(lines[i].strip())):
        i += 1
    return "\n".join(lines[i:]).strip()


def wc(s):
    return len(s.split())


def gate_input(a):
    n = 0
    with open(a.out, "w", encoding="utf-8") as w:
        for gi, line in enumerate(open(a.blur, encoding="utf-8")):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            orig = strip_lead(r["original"])
            blur = strip_lead(r["blurred"])
            if wc(orig) < 12 or wc(blur) < 12:
                continue
            rec = {
                "kind": "control",
                "source": f"{a.name}-p{r.get('pass', 0)}-{gi}",
                "a": orig,
                "b": blur,
                "corruption": "blur",
            }
            w.write(json.dumps(rec) + "\n")
            n += 1
    print(f"gate-input: wrote {n} control records -> {a.out}")


def finalize(a):
    rows = [json.loads(l) for l in open(a.gate_out, encoding="utf-8") if l.strip()]
    kept, fails = [], []
    for r in rows:
        orig, blur = r.get("control_a", ""), r.get("control_b", "")
        if r.get("gate1") == "PASS":
            kept.append({
                "type": "blur-to-original",
                "source": r.get("source", a.name),
                "input": blur,
                "target": orig,
                "input_words": wc(blur),
                "target_words": wc(orig),
            })
        elif r.get("gate1") == "FAIL":
            fails.append(r)
    with open(a.out, "w", encoding="utf-8") as w:
        for k in kept:
            w.write(json.dumps(k) + "\n")

    n = len(rows)
    passed = len(kept)
    print(f"finalize: gate PASS {passed}/{n} ({100 * passed // max(1, n)}%) -> {a.out}")
    if kept:
        exp = [k["input_words"] / max(1, k["target_words"]) for k in kept]
        import statistics as st
        print(f"  kept median input {st.median(k['input_words'] for k in kept):.0f}w "
              f"target {st.median(k['target_words'] for k in kept):.0f}w "
              f"blur-expansion {st.mean(exp):.2f}x")
    print("  sample gate-FAIL drops (what loss looked like):")
    for r in fails[:3]:
        print(f"   - {r.get('source')}: {r.get('gate1_reason', '')[:110]}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="phase", required=True)
    g = sub.add_parser("gate-input")
    g.add_argument("--blur", required=True)
    g.add_argument("--name", required=True)
    g.add_argument("--out", required=True)
    f = sub.add_parser("finalize")
    f.add_argument("--gate-out", required=True)
    f.add_argument("--name", required=True)
    f.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.phase == "gate-input":
        gate_input(a)
    else:
        finalize(a)


if __name__ == "__main__":
    main()
