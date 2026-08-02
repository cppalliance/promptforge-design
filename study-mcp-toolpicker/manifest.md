# Dataset manifest

Provenance for the reproducible artifacts in this directory.

- Catalog source: `automatelab/mcp-servers-tool-catalog` (real MCP `tools/list` dumps), copied from `../mcp-classifier-spike/data/automatelab_tools.parquet`.
- Catalog: 9,922 usable tools (name + description + input-schema params); `data/catalog.jsonl`, id-indexed.
- Catalog embedding hash: `1f1f51fe403b452c` (see `embeddings/catalog_*_1f1f51fe403b452c.npy`).
- Needs: 29,226 across 9,742 tools x 3 bands (restatement / synonym / goal). ~180 tools dropped from ~9 generation chunks that failed JSON parse (~2%).
- Need generators: `claude-haiku-4-5` and `claude-sonnet-4-6`, alternating per chunk (20 tools/chunk, `max_tokens` scaled to chunk size).
- Eval models: `BAAI/bge-small-en-v1.5`, `sentence-transformers/all-MiniLM-L6-v2` (CUDA).
- Distractors per case: 39; duplicate threshold 0.98 (equivalent-golds excluded from distractors); seed 0.
- Regenerate: `bash reproduce.sh 9922` (needs `ANTHROPIC_API_KEY`).

*2026-08-02 - Opus 4.8 (Cursor agent)*
