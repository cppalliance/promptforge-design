"""Eval in the CORRECT register: author-written capability descriptions, not user prompts.

The Lua need string is a clean, general, parameter-free description of what a tool
should do - it reads like a tool doc ("Insert a record into the database log table"),
not a user utterance ("insert my order #4123 into the prod DB before 5pm"). Our prior
evals used utterance-style needs; this one uses author-register needs.

For each real tool (automatelab catalog, 9,922 tools) we ask an LLM to paraphrase its
function into an author-style capability line (different wording, no parameter values,
no user framing), then match it against the catalog with real distractors. Matched
positive/negative catalogs give top-1, recall@3, and abstention. Generation rotates
across models to blunt single-generator bias.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import time
import urllib.request

import numpy as np
import pandas as pd

from common import Tool, DATA, RESULTS_DIR

GEN_MODELS = ["claude-haiku-4-5", "claude-sonnet-4-6"]


def load_automatelab():
    df = pd.read_parquet(DATA / "automatelab_tools.parquet")
    tools = []
    for _, r in df.iterrows():
        name = str(r["tool_name"]).strip()
        desc = str(r["tool_description"]).strip()
        server = str(r["server_name"]).strip()
        if not name or not desc or desc == "None":
            continue
        params = []
        try:
            sch = json.loads(r["input_schema"]) if isinstance(r["input_schema"], str) else r["input_schema"]
            params = list((sch or {}).get("properties", {}).keys())
        except Exception:  # noqa: BLE001
            pass
        tools.append(Tool(server=server, name=name, description=desc, params=params[:8]))
    return tools


def anthropic(model, prompt, max_tokens=1200, retries=4):
    key = os.environ["ANTHROPIC_API_KEY"]
    body = json.dumps({"model": model, "max_tokens": max_tokens, "messages": [{"role": "user", "content": prompt}]}).encode()
    last = ""
    for a in range(retries):
        try:
            req = urllib.request.Request(
                "https://api.anthropic.com/v1/messages", data=body,
                headers={"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": "application/json"})
            with urllib.request.urlopen(req, timeout=90) as resp:
                data = json.loads(resp.read())
            return "".join(b.get("text", "") for b in data.get("content", []))
        except Exception as e:  # noqa: BLE001
            last = str(e); time.sleep(2 * (a + 1))
    print("  gen fail:", last); return ""


def gen_needs(tools, per_call, rng):
    out = {}
    for i in range(0, len(tools), per_call):
        chunk = tools[i:i + per_call]
        model = GEN_MODELS[(i // per_call) % len(GEN_MODELS)]
        listing = "\n".join(f"{j}. {t.name}: {t.description}" for j, t in enumerate(chunk))
        prompt = (
            "For each tool, write ONE clean capability description a developer would put in a "
            "config to request this kind of tool. Style: general, imperative, parameter-free, "
            "like a tool's own one-line doc. Examples: 'Retrieve a WG21 paper's markdown given the "
            "paper number'; 'Insert a record into the database log table'. Do NOT include specific "
            "values, user framing ('I want'), or the tool's exact name. Paraphrase the function. "
            "Return ONLY a JSON array of strings in order.\n\n" + listing)
        raw = anthropic(model, prompt)
        try:
            arr = json.loads(raw[raw.find("["):raw.rfind("]") + 1])
        except Exception:  # noqa: BLE001
            arr = None
        if arr and len(arr) == len(chunk):
            for t, n in zip(chunk, arr):
                if isinstance(n, str) and n.strip():
                    out[t.qualified] = n.strip()
        print(f"  generated {len(out)} needs ({model})")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="BAAI/bge-small-en-v1.5")
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--distractors", type=int, default=39)
    ap.add_argument("--per-call", type=int, default=12)
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    from sentence_transformers import SentenceTransformer
    from methods import auto_device

    rng = random.Random(args.seed)
    all_tools = load_automatelab()
    print(f"automatelab usable tools: {len(all_tools)}")
    sampled = rng.sample(all_tools, min(args.n, len(all_tools)))
    needs = gen_needs(sampled, args.per_call, rng)
    sampled = [t for t in sampled if t.qualified in needs]
    print(f"\nSAMPLE author-register needs:")
    for t in sampled[:10]:
        print(f"  [{t.name}] {needs[t.qualified]}")

    model = SentenceTransformer(args.model, device=auto_device())
    pool_vecs = model.encode([t.enriched_text() for t in all_tools], normalize_embeddings=True, batch_size=256, show_progress_bar=False)
    by_q = {t.qualified: i for i, t in enumerate(all_tools)}
    q_vecs = model.encode([needs[t.qualified] for t in sampled], normalize_embeddings=True, batch_size=256, show_progress_bar=False)

    D = args.distractors
    npool = len(all_tools)
    top1 = rec3 = 0
    pos_scores, pos_correct, neg_scores = [], [], []
    for i, t in enumerate(sampled):
        qv = q_vecs[i]
        gold_idx = by_q[t.qualified]
        idx = [j for j in rng.sample(range(npool), D + D + 3) if j != gold_idx]
        pos_idx = idx[:D]; neg_idx = idx[D:2 * D + 1]
        cand = np.vstack([pool_vecs[gold_idx][None, :], pool_vecs[pos_idx]])
        sims = cand @ qv
        order = np.argsort(-sims)
        gold_rank = int(np.where(order == 0)[0][0])
        is1 = gold_rank == 0
        top1 += is1; rec3 += gold_rank < 3
        pos_scores.append(float(sims[order[0]])); pos_correct.append(is1)
        neg_scores.append(float((pool_vecs[neg_idx] @ qv).max()))

    N = len(sampled)
    pos_scores = np.array(pos_scores); pos_correct = np.array(pos_correct); neg_scores = np.array(neg_scores)
    sweep = []
    for thr in sorted(set(round(s, 3) for s in pos_scores)):
        m = pos_scores >= thr
        sweep.append({"thr": thr, "coverage": float(m.mean()),
                      "acc_on_accepted": float(pos_correct[m].mean()) if m.any() else float("nan"),
                      "false_bind": float((neg_scores >= thr).mean())})
    out = {"model": args.model, "n": N, "pool": npool, "top1": top1 / N, "recall@3": rec3 / N, "sweep": sweep}
    print(json.dumps({k: v for k, v in out.items() if k != "sweep"}, indent=2))
    (RESULTS_DIR / "lua_register.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    # save the generated needs for inspection
    with (DATA / "lua_needs.jsonl").open("w", encoding="utf-8") as f:
        for t in sampled:
            f.write(json.dumps({"need": needs[t.qualified], "gold": t.qualified}) + "\n")


if __name__ == "__main__":
    main()
