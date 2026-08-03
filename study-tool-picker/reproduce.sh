#!/usr/bin/env bash
# Reproduce the MCP tool-picker study end to end.
# Usage: bash reproduce.sh [N_TOOLS]   (default 1500; use 9922 for the full corpus)
set -e
cd "$(dirname "$0")"
PY=../spike-tool-picker/.venv/Scripts/python.exe
export PYTHONPATH=scripts HF_HUB_DISABLE_TELEMETRY=1
N="${1:-1500}"

"$PY" scripts/build_catalog.py
"$PY" scripts/generate.py --n "$N"      # needs ANTHROPIC_API_KEY
"$PY" scripts/build_eval.py
"$PY" scripts/eval.py
echo "Done. See RESULTS.md"
