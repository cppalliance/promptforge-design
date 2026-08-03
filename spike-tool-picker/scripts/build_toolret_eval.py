"""Third, fully-independent eval built from TOOLRET (ACL 2025).

TOOLRET queries are human/benchmark-authored (not LLM-generated) and carry a gold
tool document, so this removes the "needs written by one LLM" caveat of the real
(hackathon) eval. Same protocol as build_real_eval: matched positive (gold + real
distractors) and negative (distractors only) 40-tool catalogs, giving top-1 and a
real false-bind rate.

Sources:
  - mangopy/ToolRet-Queries  (35 configs; we sample a domain spread)
  - mangopy/ToolRet-Tools    (configs: code/customized/web) as the distractor pool
"""

from __future__ import annotations

import argparse
import json
import random

from common import Catalog, EvalExample, Tool, CATALOGS_DIR, EVAL_DIR, save_catalog, save_eval

QUERY_CONFIGS = ["apibank", "metatool", "gorilla-huggingface", "restgpt-spotify", "appbench", "gpt4tools"]
TOOL_CONFIGS = ["code", "customized", "web"]


def doc_to_tool(doc: dict, server: str) -> Tool:
    name = (
        doc.get("name")
        or doc.get("api_name")
        or doc.get("tool_name")
        or doc.get("functionality")
        or "tool"
    )
    if isinstance(name, str):
        name = name.strip()[:80] or "tool"
    desc = doc.get("description")
    if not desc:
        parts = []
        for k in ("domain", "framework", "functionality", "usage", "note", "api_call"):
            v = doc.get(k)
            if isinstance(v, str) and v:
                parts.append(f"{k}: {v}")
        desc = ". ".join(parts) if parts else json.dumps(doc)[:400]
    params = doc.get("api_arguments") or doc.get("parameters") or doc.get("required_parameters") or []
    if isinstance(params, dict):
        params = list(params.keys())
    if not isinstance(params, list):
        params = []
    params = [str(p)[:40] for p in params][:8]
    return Tool(server=server, name=str(name), description=str(desc)[:600], params=params)


def load_distractor_pool(cap: int, rng: random.Random) -> list[Tool]:
    from datasets import load_dataset

    pool: list[Tool] = []
    for cfg in TOOL_CONFIGS:
        try:
            t = load_dataset("mangopy/ToolRet-Tools", cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  [tools {cfg}] skip: {e}")
            continue
        split = list(t.keys())[0]
        for row in t[split]:
            try:
                doc = json.loads(row["documentation"]) if isinstance(row["documentation"], str) else row["documentation"]
            except Exception:  # noqa: BLE001
                continue
            pool.append(doc_to_tool(doc, server=f"toolret_{cfg}"))
    rng.shuffle(pool)
    print(f"distractor pool: {len(pool)} tools")
    return pool[: cap] if cap and len(pool) > cap else pool


def build(n_per_config: int, distractors: int, seed: int) -> None:
    from datasets import load_dataset

    rng = random.Random(seed)
    pool = load_distractor_pool(cap=6000, rng=rng)

    examples: list[EvalExample] = []
    idx = 0
    for cfg in QUERY_CONFIGS:
        try:
            d = load_dataset("mangopy/ToolRet-Queries", cfg)
        except Exception as e:  # noqa: BLE001
            print(f"  [queries {cfg}] skip: {e}")
            continue
        split = list(d.keys())[0]
        rows = list(d[split])
        rng.shuffle(rows)
        taken = 0
        for r in rows:
            if taken >= n_per_config:
                break
            try:
                labels = json.loads(r["labels"]) if isinstance(r["labels"], str) else r["labels"]
            except Exception:  # noqa: BLE001
                continue
            gold_lab = next((l for l in labels if l.get("relevance", 1)), labels[0] if labels else None)
            if not gold_lab or "doc" not in gold_lab:
                continue
            need = (r.get("query") or "").strip()
            if not need:
                continue
            gold = doc_to_tool(gold_lab["doc"], server=f"toolret_{cfg}")
            dists = rng.sample(pool, distractors * 2 + 2)
            pos_tools = [gold] + dists[:distractors]
            rng.shuffle(pos_tools)
            pos_id = f"real_toolret_pos_{idx:04d}"
            save_catalog(Catalog(pos_id, pos_tools), CATALOGS_DIR / f"{pos_id}.json")
            examples.append(EvalExample(need=need, catalog_id=pos_id, gold=gold.qualified, tags=["positive", "toolret", cfg]))
            neg_id = f"real_toolret_neg_{idx:04d}"
            save_catalog(Catalog(neg_id, dists[distractors : distractors * 2 + 1]), CATALOGS_DIR / f"{neg_id}.json")
            examples.append(EvalExample(need=need, catalog_id=neg_id, gold=None, tags=["hard_negative", "toolret", cfg]))
            idx += 1
            taken += 1
        print(f"  [{cfg}] took {taken}")

    save_eval(examples, EVAL_DIR / "toolret.jsonl")
    pos = sum(1 for e in examples if e.gold)
    print(f"toolret eval: {len(examples)} examples, {pos} positives, {len(examples)-pos} negatives")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--n-per-config", type=int, default=35)
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    build(args.n_per_config, args.distractors, args.seed)
