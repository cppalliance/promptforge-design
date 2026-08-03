"""Build a bias-resistant eval set from real MCP tools + independently-written needs.

Source: alihmaou/Agents_MCP_Hackathon_Tools_List (2086 real MCP tools, 218 servers),
saved to data/raw_hackathon_tools.jsonl.

Two things make this resistant to the authorship bias of the seed set:
  1. Needs are written by Claude from the tool's name + function, with an explicit
     instruction NOT to reuse distinctive words from the description. So the query
     vocabulary is independent of the description vocabulary the matchers see.
  2. Each need gets a matched pair of catalogs built from REAL distractor tools:
       - positive: gold tool + K random distractors from other servers
       - negative: K+1 random distractors, with the gold tool's entire server
         excluded, so the correct action is to abstain.
     This yields real top-1 accuracy and a real false-bind rate with no hand
     labeling and no synthetic negatives.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
import urllib.request

from common import Catalog, EvalExample, Tool, CATALOGS_DIR, DATA, EVAL_DIR, save_catalog, save_eval

RAW = DATA / "raw_hackathon_tools.jsonl"
ANTHROPIC_MODEL = os.environ.get("SPIKE_GEN_MODEL", "claude-haiku-4-5")


def load_raw_tools() -> list[Tool]:
    tools: list[Tool] = []
    seen = set()
    with RAW.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            name = (r.get("Tool name") or "").strip()
            desc = (r.get("Tool description") or "").strip()
            space = (r.get("Space name") or "").strip().replace("::", "_")
            if not name or not desc or not space:
                continue
            q = f"{space}::{name}"
            if q in seen:
                continue
            seen.add(q)
            inputs = [p.strip() for p in (r.get("Tool inputs") or "").split(",") if p.strip()]
            tools.append(Tool(server=space, name=name, description=desc, params=inputs))
    return tools


def anthropic_generate(prompts_block: str, max_tokens: int = 1500, retries: int = 4) -> str:
    key = os.environ["ANTHROPIC_API_KEY"]
    body = json.dumps(
        {
            "model": ANTHROPIC_MODEL,
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompts_block}],
        }
    ).encode()
    last = ""
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages",
                data=body,
                headers={
                    "x-api-key": key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
            )
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read())
            return "".join(b.get("text", "") for b in data.get("content", []))
        except Exception as e:  # noqa: BLE001
            last = str(e)
            time.sleep(2 * (attempt + 1))
    print(f"  [anthropic] failed after {retries}: {last}")
    return ""


def gen_needs(tools: list[Tool], per_call: int) -> dict[str, str]:
    """Return qualified_tool -> need string, generated in batches."""
    out: dict[str, str] = {}
    for i in range(0, len(tools), per_call):
        chunk = tools[i : i + per_call]
        listing = "\n".join(
            f"{j}. name={t.name} | function={t.description}" for j, t in enumerate(chunk)
        )
        prompt = (
            "For each tool below, write ONE realistic first-person user request "
            "(a capability need) that this tool would satisfy. Rules: max 14 words; "
            "phrase it as a user goal, not a tool description; DO NOT reuse distinctive "
            "nouns/verbs from the tool's function text - use natural synonyms and the "
            "user's framing. Return ONLY a JSON array of strings, one per tool, in order.\n\n"
            f"{listing}"
        )
        raw = anthropic_generate(prompt)
        needs = None
        try:
            start = raw.find("[")
            end = raw.rfind("]")
            needs = json.loads(raw[start : end + 1])
        except Exception:  # noqa: BLE001
            needs = None
        if not needs or len(needs) != len(chunk):
            print(f"  [gen] chunk {i}: parse fail (got {None if needs is None else len(needs)}), skipping")
            continue
        for t, n in zip(chunk, needs):
            if isinstance(n, str) and n.strip():
                out[t.qualified] = n.strip()
        print(f"  [gen] {len(out)} needs so far ...")
    return out


def build(n_tools: int, distractors: int, per_call: int, seed: int) -> None:
    rng = random.Random(seed)
    all_tools = load_raw_tools()
    print(f"real tools: {len(all_tools)} across {len({t.server for t in all_tools})} servers")

    by_server: dict[str, list[Tool]] = {}
    for t in all_tools:
        by_server.setdefault(t.server, []).append(t)

    # Sample tools spread across servers (prefer servers with a few tools).
    servers = [s for s, ts in by_server.items() if len(ts) >= 2]
    rng.shuffle(servers)
    sampled: list[Tool] = []
    si = 0
    while len(sampled) < n_tools and servers:
        s = servers[si % len(servers)]
        pool = [t for t in by_server[s] if t not in sampled]
        if pool:
            sampled.append(rng.choice(pool))
        si += 1
        if si > n_tools * 20:
            break
    print(f"sampled {len(sampled)} tools for needs")

    needs = gen_needs(sampled, per_call)
    print(f"generated {len(needs)} needs")

    examples: list[EvalExample] = []
    for idx, t in enumerate(sampled):
        if t.qualified not in needs:
            continue
        need = needs[t.qualified]
        # positive catalog: gold + distractors from OTHER servers
        others = [x for x in all_tools if x.server != t.server]
        rng.shuffle(others)
        pos_tools = [t] + others[:distractors]
        rng.shuffle(pos_tools)
        pos_id = f"real_pos_{idx:04d}"
        save_catalog(Catalog(pos_id, pos_tools), CATALOGS_DIR / f"{pos_id}.json")
        examples.append(EvalExample(need=need, catalog_id=pos_id, gold=t.qualified, tags=["positive", "real", "mixed"]))
        # negative catalog: distractors only, gold's server fully excluded
        neg_tools = others[distractors : distractors * 2 + 1]
        neg_id = f"real_neg_{idx:04d}"
        save_catalog(Catalog(neg_id, neg_tools), CATALOGS_DIR / f"{neg_id}.json")
        examples.append(EvalExample(need=need, catalog_id=neg_id, gold=None, tags=["hard_negative", "real", "matched"]))

    save_eval(examples, EVAL_DIR / "real.jsonl")
    pos = sum(1 for e in examples if e.gold)
    neg = sum(1 for e in examples if not e.gold)
    print(f"real eval examples: {len(examples)}  positives: {pos}  hard_negatives: {neg}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-tools", type=int, default=200)
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--per-call", type=int, default=12)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    build(args.n_tools, args.distractors, args.per_call, args.seed)
