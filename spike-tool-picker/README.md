# MCP tool-selection classifier spike

A throwaway spike answering one question: will a classifier reliably map a
prompt's English capability need to the right tool from connected MCP servers?

Answer: yes with a small embedding model, no with zero-shot NLI. See
[report/FINDINGS.md](report/FINDINGS.md).

## Layout

- `scripts/` - the harness
  - `common.py` - Tool / Catalog / EvalExample types and IO
  - `methods.py` - NLI, embedding, BM25, and LLM (OpenAI + Anthropic) scorers
  - `build_seed_eval.py` - hand-authored eval from real, well-known MCP servers
  - `build_real_eval.py` - bias-resistant eval: real hackathon tools + Claude-written
    needs + matched positive/negative catalogs
  - `nli_framing_sweep.py` - sweeps NLI direction/template/tool-text framings
  - `run_eval.py` - runs methods over an eval set, writes per-example rankings
  - `analyze.py` - top-1, abstention/false-bind sweep, calibration AUROC, bootstrap CIs
- `data/mcp_catalogs/` - catalog JSON files (seed_* and real_*)
- `data/eval/` - `seed.jsonl`, `core.jsonl`, `real.jsonl`
- `results/` - run outputs (`matrix_real.jsonl`, `matrix_seed.jsonl`, ...) and
  `analysis_*.json`
- `report/FINDINGS.md` - the verdict

## Reproduce

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu124
./.venv/Scripts/python.exe -m pip install transformers datasets sentence-transformers rank-bm25 scikit-learn sentencepiece protobuf

# build datasets (real needs generation requires ANTHROPIC_API_KEY)
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/build_seed_eval.py
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/build_real_eval.py --n-tools 200

# run the matrix and analyze
NLI="valhalla/distilbart-mnli-12-1,MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli,facebook/bart-large-mnli"
EMB="BAAI/bge-small-en-v1.5,BAAI/bge-base-en-v1.5,sentence-transformers/all-MiniLM-L6-v2"
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/run_eval.py --eval real --methods nli,embed,bm25 --nli-models "$NLI" --nli-configs best,best_desc --embed-models "$EMB" --out results/matrix_real.jsonl
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/analyze.py --results results/matrix_real.jsonl --name real_final
```

Set `SPIKE_THREADS` to cap CPU threads per process; scorers auto-use CUDA when
available. This is a spike: the code is disposable, the findings are the artifact.
