# Pairgen Experiment Battery: Findings

Six experiments tested one variable each in the sharpen-strip-gate pipeline. The goal was the configuration that maximizes training-pair yield while preserving Gate 1 (execution-equivalence) discrimination. Full method and numbers are in `experiment-log.md`; this is the synthesis.

## Optimal configuration

- **Gate**: Gate 1 (execution-equivalence) alone. Drop Gate 2. Confidence: high (E2: gate1-only yields 90% vs 10% strict; narrowed gate2 caught zero defects beyond gate1, so it is pure redundant cost).
- **Sharpen prompt**: minimal-change for a safety-first compressor, or aggressive-then-minimal two-pass for more compression. Confidence: high on recovery, medium on the exact two-pass yield (E6: minimal recovers 72% of aggressive failures; implied two-pass gate1 ~90%).
- **Effort**: medium. Confidence: low (E5: medium marginally beat high on yield with equal compression, but inside gate noise).
- **Input size**: irrelevant to quality; slice only to multiply volume. Confidence: high (E1: gate1 ~60% whether whole or sliced, no monotonic size effect).
- **Source**: the user's own prompts and blurred versions of them, not web prompts. Confidence: high (E3: web yields 23% because the instrument invents specifics on vague input; E4: first-gen blur is the clean source).

## The core result

Sharpening cannot recover a blurred original (E4): the sharpened output is no closer to the sharp original than the blurred input is (similarity 0.446 vs 0.447; closer only 51% of the time, a coin flip), and it compresses even below the original's length along a different path. Blur is irreversible from within the chain. Two consequences:

1. The training target must be the true original, captured before any blur. The gold pairs are (blurred first-gen section -> original first-gen section), where the target is known-sharp by construction. A learned model can approximate this inverse from many such pairs; a single frontier sharpen pass cannot reconstruct it for one instance.
2. Instrument-sharpening still produces a valid, shorter, execution-equivalent version of any bloated input. That is a legitimate compression pair (bloat -> sharp), just not a reconstruction of a lost original.

## Why web prompts fail (E3)

The instrument's gap-filling rules ("quantify every quantity", "define the empty/missing/malformed case", "escape hatch per hard rule") are correct for tightening prompts that already carry their specifics. On vague web prompts they force the sharpener to INVENT specifics ("provide clear options" becomes "provide 2-4 options"; a revise-until-zero loop appears from nothing), which Gate 1 correctly rejects as behavior change. About a third of web failures were invented constraints, not dropped ones. Arbitrary text is the wrong source; the specifics must already be present.

## The dataset

`dataset-clean.jsonl`, 337 pairs:

- **286 blur-to-original** (gold): input blurred, target the true sharp first-gen section, across blur passes 1-3 from 10 prompts. Median input 172w, target 157w. This is the scalable deblurring signal.
- **51 bloat-to-sharp** (gate1-verified): input bloated, target instrument-sharpened, every pair execution-equivalent. Median 149w to 122w. From E2-off (18), E6-minimal (22), E3-web (7), E5 (4).

Schema per line: `type, source, input, target, input_words, target_words`.

## Scale path

- Blur all 85 first-gen prompts (not 10) at 2-3 variants x 3 passes: order 85 x 8 sections x 3 passes x 2 variants, on the order of thousands of blur-to-original pairs, the training set for a local deblurring model. Confidence: high that the source scales; the mechanism is proven.
- Run pairgen gate1-only, medium effort, minimal-change prompt over any remaining bloated corpus to add bloat-to-sharp pairs, keeping only gate1 PASS. Confidence: high.
- Do not spend more on web corpora. Confidence: high (contaminated, 23% yield).

## Tooling changes made

- pairgen `--gate2-mode {strict,narrowed,off}` (E2) and `--tighten-file` (E6).
- blur-gen default model IDs refreshed (the old IDs 404) (E4).
- Em-dash strip hardened twice: it no longer corrupts `---` frontmatter (validation) or `<!--`/`-->` HTML comments (E6). 5 unit tests, no API calls.
- `run-sharded.sh` runs pairgen in N concurrent shards, cutting wall-clock ~4x. The whole battery (about 900 API calls) ran in well under an hour.

*2026-07-27 - claude-opus-4.8*
