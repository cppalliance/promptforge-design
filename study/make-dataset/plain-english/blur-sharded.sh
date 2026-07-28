#!/usr/bin/env bash
# Blur a passages JSONL through blur-gen using N concurrent shards.
# Each passage becomes one section under a unique synthetic "## pNNNN" heading
# so blur-gen splits cleanly; headings are stripped later by assemble.py.
#
# Usage: blur-sharded.sh <passages.jsonl> <out-blur.jsonl> <shards> [blur-gen args...]
# Prints "DONE ..." on completion; poll the .brun.log for that marker.
set -uo pipefail
IN="$1"; OUT="$2"; SHARDS="$3"; PASSES="${4:-3}"
if [ "$#" -ge 4 ]; then shift 4; else shift 3; fi
EXTRA="$*"
DIR="$(dirname "$OUT")"
BASE="$(basename "$OUT" .jsonl)"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BLURGEN="$SCRIPT_DIR/../blur-gen/target/release/blur-gen"

python - "$IN" "$DIR/$BASE" "$SHARDS" <<'PY'
import sys, json
inp, prefix, shards = sys.argv[1], sys.argv[2], int(sys.argv[3])
rows = [json.loads(l) for l in open(inp, encoding='utf-8') if l.strip()]
files = [open(f"{prefix}.shard{i}.md", "w", encoding="utf-8") for i in range(shards)]
for gi, r in enumerate(rows):
    f = files[gi % shards]
    f.write(f"## p{gi:04d}\n\n{r['text'].strip()}\n\n")
for f in files:
    f.close()
print(f"formatted {len(rows)} passages into {shards} shard md files")
PY

pids=()
for i in $(seq 0 $((SHARDS-1))); do
  # shellcheck disable=SC2086
  $BLURGEN --input "$DIR/$BASE.shard$i.md" --output "$DIR/$BASE.shard$i.blur.jsonl" \
    --passes "$PASSES" --variants 1 $EXTRA > "$DIR/$BASE.shard$i.plog" 2>&1 &
  pids+=($!)
done
echo "launched ${#pids[@]} blur shards: ${pids[*]}"
fail=0
for p in "${pids[@]}"; do wait "$p" || fail=1; done
cat "$DIR/$BASE".shard*.blur.jsonl > "$OUT" 2>/dev/null
echo "DONE shards=$SHARDS fail=$fail out=$OUT lines=$(wc -l < "$OUT" 2>/dev/null || echo 0)"
