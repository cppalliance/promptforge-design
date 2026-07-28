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

## E2: Gate 2 modes

- **Hypothesis**: Gate1-only or gate1+narrowed-gate2 raises yield without admitting bad pairs.
- **Started / Completed**: 2026-07-27
- **Inputs**: the 20 validation pairs (`pairgen-in.jsonl`), run once per mode.
- **Configuration**: model=claude-opus-4-8, effort=high; added `--gate2-mode {strict,narrowed,off}` to pairgen; 3 shards per mode, 3 modes concurrent.
- **Results**:
  - strict: gate1 15/20, gate2 PASS 2, kept 2/20 (10%) - matches baseline
  - narrowed: gate1 17/20, gate2 PASS 17, kept 17/20 (85%)
  - off (gate1-only): gate1 18/20, kept 18/20 (90%)
- **Spot-check (off, 5 kept)**: all genuinely sharp; every specific preserved (18 names, 12 pages, "medium tier or higher", version 2.1, "closing paragraph", allocators/iterators). Em-dashes converted to `-`. No junk admitted.
- **Key finding**: Narrowed gate2 caught zero defects beyond gate1 (all 17 gate1-survivors passed it), so it is redundant with gate1 and just costs an extra call. Strict gate2 is the yield killer (rejects on aspirational checklist items). Gate1-only yields 90% with clean output.
- **Decision**: Standard config for E3-E6 is `--gate2-mode off` (gate1-only). Note gate1 has mild run-to-run variance on borderline cases (dropped cross-reference flips PASS/FAIL between runs); acceptable for a training set.
- **Commit**: `exp-2: gate2-modes`

---

## E3: Web shitprompts

- **Hypothesis**: Bloated web prompts, sharpened by the instrument, produce clean training pairs at reasonable yield under gate1-only.
- **Started / Completed**: 2026-07-27
- **Inputs**: 30 prompts from `awesome-chatgpt-prompts` (1504 qualifying at 50-500w; sampled diversely, 50-440w).
- **Configuration**: model=claude-opus-4-8, effort=high, gate2=off, 4 shards.
- **Results**: gate1 7/30 (23%), kept 7/30 (23%), compression 0.86 (14% reduction).
- **Failure breakdown**: of 23 gate1 failures, ~8 were the sharpener ADDING constraints the source never had (invented numbers, edge-case branches, revise-loops, fixed orders), ~15 were dropped/narrowed scope.
- **Spot-check (kept)**: clean (Gomoku board rules, Elasticsearch project spec preserved verbatim).
- **Key finding**: Web prompts are a low-yield, contaminated source (23% vs 60-90% for the user's own prose). The instrument's gap-filling rules ("quantify every quantity", "define the empty case", "escape hatch per hard rule") cause it to INVENT specifics when the source is vague, and gate1 correctly rejects those as behavior changes. This empirically confirms the earlier conclusion: the training source must already contain the specifics (the user's own prompts / blurred versions of them), not arbitrary web text.
- **Decision**: Do not scale web prompts (yield below the 50% threshold). Keep the 7 clean pairs. E4 (blur-sharpen of first-gen prompts) is the right source.
- **Commit**: `exp-3: web-shitprompts`

---

## E4: First-gen blur-sharpen roundtrip

- **Hypothesis**: Blurring a known-sharp first-gen prompt, then sharpening the blurred version, yields a pair execution-equivalent to the blurred input and closer to the original sharp than the blurred version is.
- **Started / Completed**: 2026-07-27
- **Inputs**: 10 first-gen prompts (1000-3000w), split by blur-gen into ~95 sections, blurred 3 passes (1 variant). 286 blur records; pass-3 (95) fed to pairgen. Deviation from plan: used blur-gen's natural section splitting instead of ~100w slices, because E1 refuted the size effect; slicing would add complexity for no benefit.
- **Configuration**: blur-gen models haiku-4-5 / sonnet-4-6 / opus-4-8; pairgen model=claude-opus-4-8, effort=high, gate2=off; 4 shards each stage.
- **Fix**: blur-gen default model IDs were stale (404 on `claude-sonnet-4-20250514` etc.); updated defaults to current IDs.
- **Results**:
  - blur expansion original->blurred: 1.21x mean (bloat confirmed)
  - pairgen gate1 65/95 (68%); compression blur->sharp 0.83
  - similarity to original (difflib word-seq ratio): blurred 0.447, sharpened 0.446 (identical)
  - sharpened closer to original than blurred: 49/95 (51%, coin flip)
  - mean words: original 189, blurred 203, sharpened 171
- **Key finding**: Hypothesis refuted, and this is the pivotal result. Sharpening the blurred text does NOT recover the original: the sharpened output is no closer to the original than the blurred was (0.446 vs 0.447), and it compresses even below the original's length (171 vs 189w) along a different path. Blur is irreversible from within the chain (data processing inequality, confirmed empirically). Instrument-sharpening produces A valid compression, not THE original.
- **Decision**: The training target must be the true original, not a re-sharpened blur. The dataset product from E4 is the 286 (blurred -> original) pairs across passes 1-3, where the target is the known-sharp first-gen text. This is the scalable deblurring-training source (85 first-gen prompts x passes x variants -> thousands of pairs).
- **Commit**: `exp-4: blur-sharpen-roundtrip`

---

## E5: Effort level sweep

- **Hypothesis**: effort=medium produces less aggressive sharpening, fewer gate1 failures, but less compression.
- **Started / Completed**: 2026-07-27
- **Inputs**: 15 (10 web from E3 + 5 papergate from E2), run at high and medium.
- **Configuration**: model=claude-opus-4-8, gate2=off, 3 shards per effort.
- **Results**:
  - high: gate1 6/15 (40%), compression 0.889 (12% reduction)
  - medium: gate1 8/15 (53%), compression 0.894 (11% reduction)
  - gate1 verdict differed on 4/15, flipping both directions (3 high-FAIL->medium-PASS, 1 the reverse)
- **Key finding**: Weak, noisy support for the hypothesis. Medium gave a marginally higher gate1 rate and negligibly less compression (0.5%), but the flips go both ways, so most of the gap is gate run-to-run noise, not a real effort effect. Absolute rates are low here only because the mix is web-heavy (E3 web prompts are ~23% gate1). Medium is marginally safer, faster, and cheaper with no compression penalty.
- **Decision**: Prefer effort=medium for the scale run (equal compression, slightly higher yield, lower cost). Weak preference; either is defensible.
- **Commit**: `exp-5: effort-sweep`

---

## E6: Multi-pass sharpen on gate1 failures

- **Hypothesis**: Gate1 failures can be recovered by a second, gentler sharpen pass with a minimal-change prompt.
- **Started / Completed**: 2026-07-27
- **Inputs**: 36 gate1 failures (12 each from E1, E3, E4; 76 available). Added `--tighten-file` to pairgen to swap in the minimal-change instruction.
- **Configuration**: model=claude-opus-4-8, effort=high, gate2=off, minimal-change TIGHTEN prompt.
- **Results**:
  - recovered (gate1 PASS now): 26/36 (72%); by source e1 9/12, e3 8/12, e4 9/12
  - compression 0.959 (only 4% reduction, vs ~15% for the aggressive default)
- **Key finding**: A minimal-change re-sharpen recovers 72% of failures, confirming most gate1 failures were the aggressive default prompt over-editing (dropping/inventing), not unrecoverable content. Trade-off: recovered pairs are barely compressed (4%). Implied two-pass yield: aggressive (~65% gate1) then minimal on the rest recovers ~0.72 x 35% = ~25%, for ~90% combined gate1 pass.
- **Fix**: Found and fixed a third strip bug - `<!--` and `-->` HTML comment delimiters were corrupted (embedded `--` collapsed). The strip now collapses a 2-hyphen run only when flanked by alphanumerics/whitespace (prose), protecting punctuation-adjacent `--`. Added a unit test (5/5 pass).
- **Decision**: For a meaning-preserving compressor, favor the minimal-change prompt (much safer, ~4% compression) or a two-pass aggressive-then-minimal fallback for higher compression at ~90% yield.
- **Commit**: `exp-6: multipass-sharpen`

---

## Consolidation

- **Completed**: 2026-07-27
- **Dataset**: `experiments/dataset-clean.jsonl`, 337 pairs: 286 blur-to-original (gold, target is true sharp first-gen text, passes 1-3) + 51 bloat-to-sharp (gate1-verified compression pairs from E2-off, E6-minimal, E3-web, E5).
- **Optimal config**: Gate 1 only (drop Gate 2); minimal-change or two-pass sharpen; medium effort; size irrelevant to quality (slice for volume); source is the user's own prompts, not web.
- **Core result**: sharpening cannot recover a blurred original (E4); the training target must be the true original captured before blur, and a learned model must approximate the inverse from many pairs.
- **Findings**: `experiments/findings.md`.
- **Commit**: `exp-final: consolidated dataset`

---
