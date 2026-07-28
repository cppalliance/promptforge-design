# Semantic Blur and Prompt Deblurring: Study Findings

The complete findings from the compression/deblurring investigation: the thesis, the experiments that tested it, what blur actually is when measured, the datasets built, the model design, an audit of the sharpening instrument itself, and the meta-lesson the endeavor taught by living it out.

## Thesis

An LLM asked to "revise" or "rewrite" a prompt does not edit it; it regenerates it, resampling from the training distribution. Each pass moves the text toward the mean: blander, more hedged, more exhaustive, less specific. This is semantic blur, the text analog of pushing an image through latent space and back. The goal of good prompting is the opposite direction, toward the argmax and the tail of the distribution, where the sharp, specific, load-bearing tokens live. Blur is irreversible from within the chain: by the data processing inequality, mutual information with the original intent only decreases with each regeneration, so no amount of further regeneration recovers what was lost.

## What the experiments established

- **The gates.** Gate 1 (execution-equivalence: would a model behave differently following B instead of A) discriminates: it caught 5 of 5 deliberate corruptions and, independently, real sharpen-induced drops. Gate 2 (full checklist compliance) is too strict, rejecting ~90% of behavior-preserving targets on one aspirational item. Gate1-only yields 90% versus strict's 10%; a narrowed Gate 2 caught nothing Gate 1 missed. Use Gate 1 alone. (Confidence: high.)
- **Input size is irrelevant to quality (E1).** Gate 1 pass rate was ~60% whether a section was sharpened whole or sliced into ~100-word chunks; no monotonic size effect. Slicing multiplies pair count at equal quality, nothing more.
- **Web prompts are a contaminated source (E3).** 23% gate1 pass. The instrument's gap-filling rules ("quantify every quantity", "define the empty case") make it invent specifics on vague input ("provide clear options" becomes "provide 2-4 options"), which Gate 1 correctly rejects. The training source must already contain its specifics.
- **Blur is irreversible, confirmed (E4).** Sharpening a blurred passage lands no closer to the original than the blur was (word-sequence similarity 0.446 vs 0.447, closer only 51% of the time). Sharpening produces a valid compression, not the lost original. The training target must therefore be the true pre-blur original, captured before any regeneration.
- **Effort (E5):** medium and high effort were within gate noise; medium is marginally cheaper and no worse.
- **Recovery (E6):** a gentle minimal-change re-sharpen recovers 72% of Gate 1 failures, implying a two-pass aggressive-then-minimal path reaches ~90% yield.

## What blur actually is (measured, not assumed)

- **Not almost-lossless.** A single "rewrite, preserve meaning" pass drops or alters a specific in 43-54% of cases; by pass 10, 81%. The directional gate is therefore mandatory: an ungated pair whose blur dropped a fact would train the model to hallucinate it back.
- **A reword toward the mean, not an expansion.** Among meaning-preserved pairs, ~54% of words change at essentially constant length (about +6% words, and ~1 in 4 blurs is actually shorter). The signal is different, blander wording, not more of it.
- **Depth is counterproductive.** Over 10 chained passes, expansion stayed flat (~1.07x) while the gate pass rate collapsed 56 to 27 to 19%. Blurring harder adds no compression signal and compounds drift.
- **The command-versus-description law.** Crisp instructions survive blur far better than descriptive prose, because a command has an execution semantics a reword converges back to, while a description has interpretive latitude that drifts. Measured pass rates: scientific abstracts 45%, Wikipedia 56%, instruction-flavored content higher. The target domain, prompts and plans, is the favorable regime. The dramatic bloat originally observed on real prompts (+18% to +146%) came from revision-with-added-content, a different operation than a bare rewrite, which barely expands.

## The reframe

The tool is a deblurrer and resharpener, not a shortener. It restores sharp wording and specificity; it does not primarily shorten. The clean way to supervise it is sharp target plus controlled degradation: take a known-sharp original, degrade it, and train (degraded to sharp). Because the delta is only the degradation, meaning is anchored and the model learns pure reversal, with the gate removing any pair where the degradation dropped a fact.

## Datasets produced (committed)

- **Prompt corpus:** 337 pairs. 286 blur-to-original (target is the true sharp first-gen text) plus 51 gate1-verified bloat-to-sharp.
- **arXiv:** 137, **Wikipedia:** 169 (blur-to-original, shallow blur, for vocabulary breadth). Finding: dense human prose is a weak compression source (it barely blurs) but a valid reword/deblur signal; the strong compression signal comes from sources with expansion room (AI-generated or genuinely bloated text).
- The first-gen corpus (85 prompts, ~1,961 blurrable sections) scales the prompt source to ~12,000 pairs at modest settings.

## Model and training design

- **Size and method:** a 2-3B model, fine-tuned (not trained from scratch); the base understands meaning already, so this adds one narrow skill.
- **Vocabulary:** lives in pretraining, not the fine-tune set. Prefer an English-heavy base (FineWeb-Edu). Narrow fine-tuning biases output style, not readable vocabulary; the real risk is the model regressing rare words toward its own narrow mean, countered by a preserve-rare-tokens training rule.
- **Determinism:** temperature 0, single-thread CPU, fixed summation order gives true idempotence. Floating-point non-associativity is why GPU temp-0 still flips a near-tie token ("a" to "the"), and one flip diverges the rest of the sequence.
- **Guardrails, mechanical not model-trusted:** output token count must not exceed input (the model can never expand, worst case returns the input); em-dash and structural-markdown strip applied outside the model.
- **Curriculum (untested):** general/broad compression first, the user's prompt style last, with a small rehearsal mix to prevent forgetting. A/B against single-stage before believing it.

## The instrument audit (a study within the study)

Auditing the sharpening instrument against its sources found the instrument itself had degraded during its one-time distillation, in several distinct ways:

- a lexical blur ("Use one term per concept" became the ambiguous "One term names each concept"),
- a reorder that split a rule from its remedy (the vague-qualifier rule),
- stripped reasons (the scope rule lost its "models read literally" mechanism),
- scope-creep (a whole analytical-framework tier that prescribes a diagnostic algorithm rather than aligning prose), and
- undefined terms ("write each result" never defines "result").

Provenance from git: the sources are stable. `how-to-write-prompts.md` was born tight on 2026-07-08 (Claude Fable 5); its slop entered with the sections added 2026-07-25 (Claude Opus 5). `german.md` is lean but reasonless, and its reasonless style, misapplied to how-to's reason-rich rules during distillation, is what stripped the reasons. The decisive point: a blurred rulebook still produces sharp outputs (the experiments confirm the sharpened targets kept their specifics), so the instrument's imperfections never actually blocked anything.

## The meta-lesson

The endeavor proved its own thesis by living it out. Two circles ran at once:

- **You cannot fix blur by regenerating,** because regeneration is the blur. Every proposed "rebuild the instrument" was another pass through the distribution. The only blur-free operations are a human with a delete key (cropping, which removes tokens without resampling the survivors) and targeted, non-regenerative edits that preserve the sharp original.
- **An audit for ambiguity has no fixed point.** Language is never perfectly unambiguous, so a line-by-line hunt always finds one more imperfection. Chasing perfection is the trap, and it is the blur trap applied to process: the anti-bloat project accreted six plan files and an unbounded audit, bloating exactly like the artifacts it studied.

The exit is not a cleaner lap. It is to ship the sharp-enough, stop regenerating, and use targeted edits for the few genuine defects.

## Where it stands, and recommendations

- The datasets are built and committed; they stand on their own. (Confidence: high.)
- Keep Gate 1 as the hard gate; drop Gate 2. (Confidence: high.)
- The training target must be the true pre-blur original, never a re-sharpened blur. (Confidence: high.)
- Leave the instrument in place; it produces sharp outputs. If closure is wanted, make only the two surgical fixes (the one-term line, the vague-qualifier reorder) as targeted edits, never a rebuild. (Confidence: high.)
- Do not scale web prompts. The in-domain source is the user's own prompts and plans, degraded from a sharp target. (Confidence: high on web; medium-high on plans as the next source.)
- If resumed, the next real step is a plan/prompt deblurring dataset: sharpen once to a clean target, degrade it, keep (degraded to sharp) pairs under Gate 1. (Confidence: medium.)

*2026-07-28 - claude-opus-4.8*
