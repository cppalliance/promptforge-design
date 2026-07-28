# Pairgen Experiment Log

Append-only record of the experiment battery. Each experiment tests one variable in the sharpen-strip-gate pipeline to find the configuration that maximizes training-pair yield while preserving Gate 1 (execution-equivalence) discrimination. This file is the reload point: a fresh session reads it to see which experiments are done and resumes from the first incomplete one.

Baseline from the prior validation run (`pairgen-validation.md`): 20 bloated inputs, Gate 1 PASS 13/20, Gate 2 PASS 2/13, kept 2/20 (10%). Gate 1 caught 5/5 negative controls. The two kept pairs were the smallest inputs (57w, 71w).

Each entry uses this format:

- **Hypothesis**: one sentence
- **Started** / **Completed**: ISO timestamps
- **Inputs**: count and source
- **Configuration**: model, effort, gate2 mode
- **Results**: gate1 pass X/N, gate2 pass Y/Z, kept K/N
- **Compression**: median input words to output words
- **Key finding**: one sentence
- **Commit**: hash

---

## E0: Initialize experiment infrastructure

- **Started**: 2026-07-27
- **Actions**: Built and tested pairgen (4/4 unit tests pass), verified ANTHROPIC_API_KEY present, created `experiments/` scratch dirs, added experiment output patterns to `.gitignore`, initialized this log.
- **Configuration**: pairgen defaults model=claude-opus-4-8, effort=high, gate2=strict.
- **Key finding**: infrastructure ready; baseline is 10% yield under strict both-gates.
- **Completed**: 2026-07-27

---

## E1: Slice-then-sharpen

- **Hypothesis**: Sharpening ~100w chunks has a higher gate1 pass rate than sharpening 300w+ sections.
- **Started / Completed**: 2026-07-27
- **Inputs**: 9 papergate pass-6 bloated sections (235-1130w) as whole; the same 9 sliced into 52 chunks (median 78w). 61 pairs total.
- **Configuration**: model=claude-opus-4-8, effort=high, gate2=strict, 4 concurrent shards.
- **Results**:
  - whole: gate1 6/9 (66%), gate2 0/9, kept 0/9
  - sliced: gate1 32/52 (61%), gate2 0/52, kept 0/52
  - sliced gate1 by band: 0-80w 62%, 80-110w 52%, 110-200w 75% (no monotonic size effect)
- **Compression**: ~0.84-0.85 (15-16% reduction) for both.
- **Key finding**: Hypothesis refuted. Slicing does not raise the gate1 pass rate (~60% either way) and shows no monotonic size effect. Gate2 strict rejects 100% here (0/61), confirming it is the binding constraint, not size. Slicing does multiply pair count ~5.8x (52 vs 9) at equal gate1 rate, so it helps volume, not quality.
- **Implication**: The lever is gate2 mode (E2), not input size. Slicing is worth keeping only as a volume multiplier.
- **Commit**: `exp-1: slice-then-sharpen`

---
