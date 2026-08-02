"""Generate author-register need strings for sampled tools, in 3 bands, multi-model.

Bands (a real author drifts across these when writing a Lua need):
  - restatement : a clean paraphrase of the tool's own one-line doc (the common mode)
  - synonym     : same capability, synonym-swapped wording
  - goal        : the user-goal the tool serves, abstracted from the tool's words

Author register throughout: parameter-free, imperative, no specific values, no
"I want" framing, not the tool's exact name. Rotates across Claude models to blunt
single-generator bias. Writes needs_raw.jsonl: {gold_id, band, need, gen_model}.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
import urllib.request

from common import DATA, load_catalog

MODELS = ["claude-haiku-4-5", "claude-sonnet-4-6"]


def anthropic(model, prompt, max_tokens=1500, retries=4):
    key = os.environ["ANTHROPIC_API_KEY"]
    body = json.dumps({"model": model, "max_tokens": max_tokens,
                       "messages": [{"role": "user", "content": prompt}]}).encode()
    last = ""
    for a in range(retries):
        try:
            req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body,
                                         headers={"x-api-key": key, "anthropic-version": "2023-06-01",
                                                  "content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                return "".join(b.get("text", "") for b in json.loads(resp.read()).get("content", []))
        except Exception as e:  # noqa: BLE001
            last = str(e); time.sleep(2 * (a + 1))
    print("  gen fail:", last); return ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--per-call", type=int, default=10)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    rng = random.Random(args.seed)
    tools = load_catalog()
    sample = rng.sample(tools, min(args.n, len(tools)))
    out = DATA / "needs_raw.jsonl"
    written = 0
    with out.open("w", encoding="utf-8") as f:
        for i in range(0, len(sample), args.per_call):
            chunk = sample[i:i + args.per_call]
            model = MODELS[(i // args.per_call) % len(MODELS)]
            listing = "\n".join(f"{j}. {t.name}: {t.description}" for j, t in enumerate(chunk))
            prompt = (
                "For each tool, write three author-style capability descriptions a developer would put "
                "in config to request this kind of tool. All parameter-free, imperative, no specific "
                "values, no 'I want' framing, and not the tool's exact name.\n"
                "  restatement: a clean paraphrase of the tool's one-line doc.\n"
                "  synonym: same capability, different words/synonyms.\n"
                "  goal: the user goal it serves, abstracted from the tool's wording.\n"
                "Return ONLY a JSON array; each element {\"restatement\":..,\"synonym\":..,\"goal\":..}, in order.\n\n"
                + listing)
            raw = anthropic(model, prompt, max_tokens=max(1500, len(chunk) * 220))
            try:
                arr = json.loads(raw[raw.find("["):raw.rfind("]") + 1])
            except Exception:  # noqa: BLE001
                arr = None
            if not arr or len(arr) != len(chunk):
                print(f"  chunk {i}: parse fail; skipping")
                continue
            for t, bands in zip(chunk, arr):
                for band in ("restatement", "synonym", "goal"):
                    need = (bands.get(band) or "").strip() if isinstance(bands, dict) else ""
                    if need:
                        f.write(json.dumps({"gold_id": t.id, "band": band, "need": need, "gen_model": model}) + "\n")
                        written += 1
            print(f"  {written} needs so far ({model})")
    print(f"needs_raw.jsonl: {written} needs from {len(sample)} tools")
    # eyeball sample
    print("\nSAMPLE:")
    for line in out.open(encoding="utf-8").read().splitlines()[:9]:
        r = json.loads(line)
        print(f"  [{r['band']:11}] {r['need']}")


if __name__ == "__main__":
    main()
