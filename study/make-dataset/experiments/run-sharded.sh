#!/usr/bin/env bash
# Run pairgen over an input JSONL using N concurrent shards, then concatenate.
# Reused by every experiment to cut wall-clock ~Nx. pairgen already retries
# 429/5xx with backoff, so concurrency is safe against rate limits.
#
# Usage: run-sharded.sh <input.jsonl> <out.jsonl> <shards> [extra pairgen args...]
# Prints "DONE ..." on completion; poll the .run.log for that marker.
set -uo pipefail
IN="$1"; OUT="$2"; SHARDS="$3"; shift 3
EXTRA="$*"
DIR="$(dirname "$OUT")"
BASE="$(basename "$OUT" .jsonl)"
PAIRGEN=./pairgen/target/release/pairgen
INSTR=sharpen-instrument.md

python - "$IN" "$DIR/$BASE" "$SHARDS" <<'PY'
import sys, json
inp, prefix, shards = sys.argv[1], sys.argv[2], int(sys.argv[3])
lines = [l for l in open(inp, encoding='utf-8') if l.strip()]
fs = [open(f"{prefix}.shard{i}.jsonl", "w", encoding="utf-8") for i in range(shards)]
for i, l in enumerate(lines):
    fs[i % shards].write(l)
for f in fs:
    f.close()
print(f"split {len(lines)} recs into {shards} shards")
PY

pids=()
for i in $(seq 0 $((SHARDS-1))); do
  # shellcheck disable=SC2086
  $PAIRGEN --instrument "$INSTR" --input "$DIR/$BASE.shard$i.jsonl" \
    --out "$DIR/$BASE.shard$i.out.jsonl" $EXTRA > "$DIR/$BASE.shard$i.plog" 2>&1 &
  pids+=($!)
done
echo "launched ${#pids[@]} shards: ${pids[*]}"
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
cat "$DIR/$BASE".shard*.out.jsonl > "$OUT" 2>/dev/null
echo "DONE shards=$SHARDS fail=$fail out=$OUT lines=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
