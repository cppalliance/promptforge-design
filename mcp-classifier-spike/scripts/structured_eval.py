"""Structured verb/noun reranking: split need and tool into noun and verb channels,
compare each in embedding space, and use them to re-rank the embedding top-k.

Motivation: a whole-sentence embedding blends action and object into one vector, so
an action mismatch (read_file vs write_file) can hide behind a strong object match.
Comparing verbs separately and nouns separately may recover that lost signal. To
avoid the fusion-hurts failure mode, the structured signal only RE-RANKS the base
embedding top-k (it cannot drop the gold below the shortlist), and the channel
weights are swept. We report top-1 overall and top-1 on near-duplicate cases.
"""

from __future__ import annotations

import argparse
import json

import numpy as np

from common import EVAL_DIR, RESULTS_DIR, load_all_catalogs, load_eval

WEIGHTS = [(0.0, 0.0), (0.5, 0.0), (0.0, 0.5), (0.5, 0.5), (1.0, 0.5), (0.5, 1.0), (1.0, 1.0)]
K = 5


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eval", default="seed")
    ap.add_argument("--embed", default="BAAI/bge-small-en-v1.5")
    args = ap.parse_args()

    import spacy
    from sentence_transformers import SentenceTransformer
    from methods import auto_device

    nlp = spacy.load("en_core_web_sm", disable=["ner", "parser"])
    model = SentenceTransformer(args.embed, device=auto_device())

    def split(text: str):
        doc = nlp(text)
        nouns = " ".join(t.lemma_.lower() for t in doc if t.pos_ in ("NOUN", "PROPN"))
        verbs = " ".join(t.lemma_.lower() for t in doc if t.pos_ == "VERB")
        return nouns, verbs

    examples = [e for e in load_eval(EVAL_DIR / f"{args.eval}.jsonl") if e.gold]
    catalogs = load_all_catalogs()
    examples = [e for e in examples if e.catalog_id in catalogs]

    # aggregate top1 per weight combo (rerank within base top-k), plus near-dupe subset
    agg = {w: {"top1": 0, "nd_top1": 0} for w in WEIGHTS}
    nd_total = 0

    def enc(strings):
        # empty strings -> zero vectors so cosine contributes 0
        idx = [i for i, s in enumerate(strings) if s.strip()]
        vecs = np.zeros((len(strings), model.get_sentence_embedding_dimension()), dtype=np.float32)
        if idx:
            e = model.encode([strings[i] for i in idx], normalize_embeddings=True, show_progress_bar=False)
            for j, i in enumerate(idx):
                vecs[i] = e[j]
        return vecs

    for e in examples:
        tools = catalogs[e.catalog_id].tools
        is_nd = "near_duplicate" in e.tags
        nd_total += is_nd
        nf, nv = split(e.need)
        tf = [t.enriched_text() for t in tools]
        tn, tv = zip(*[split(x) for x in tf]) if tools else ([], [])
        need_full = model.encode(e.need, normalize_embeddings=True, show_progress_bar=False)
        tool_full = model.encode(list(tf), normalize_embeddings=True, show_progress_bar=False)
        base = tool_full @ need_full
        nvec = enc([nf]); nver = enc([nv])
        tnv = enc(list(tn)); tvv = enc(list(tv))
        noun_s = tnv @ nvec[0]
        verb_s = tvv @ nver[0]
        base_order = np.argsort(-base)[:K]
        for w in WEIGHTS:
            a, b = w  # a=verb weight, b=noun weight
            fused = base + a * verb_s + b * noun_s
            best = max(base_order, key=lambda i: fused[i])
            correct = tools[best].qualified == e.gold
            agg[w]["top1"] += correct
            if is_nd:
                agg[w]["nd_top1"] += correct

    n = len(examples)
    out = {"eval": args.eval, "embed": args.embed, "k": K, "n": n, "n_near_dupe": nd_total, "weights": []}
    for w in WEIGHTS:
        out["weights"].append(
            {
                "verb_w": w[0], "noun_w": w[1],
                "top1": agg[w]["top1"] / n,
                "near_dupe_top1": (agg[w]["nd_top1"] / nd_total) if nd_total else None,
            }
        )
    print(json.dumps(out, indent=2))
    (RESULTS_DIR / f"structured_{args.eval}.json").write_text(json.dumps(out, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
