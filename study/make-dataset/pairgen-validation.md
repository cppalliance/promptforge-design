# Pair Pipeline Validation

The `pairgen` path (sharpen with the instrument, strip em-dashes mechanically, then two gates: execution-equivalence and rulebook-compliance) ran end to end on 20 genuinely bloated sections plus 5 deliberately corrupted negative controls. All model calls were direct `/v1/messages` to `claude-opus-4-8` at high effort, no Cursor harness. The goal was not dataset yield. It was to prove the two gates discriminate real meaning changes from safe tightening before any scale run.

## Headline

The gates discriminate. Gate 1 (execution-equivalence) caught all 5 corruptions and, independently, flagged 6 genuine meaning changes that sharpening introduced on the real batch. A gate that always says PASS would have passed the controls; this one failed every one of them, for the right stated reason.

## Negative controls: 5 of 5 caught

This is the number that matters. Each control is a sharp reference A and a version B corrupted in exactly one way. Gate 1 must FAIL each. It did, and named the divergence correctly every time:

- num-change: "the cap changed from 3 to 5, so B allows more review cycles than A"
- dropped-step: "B drops the narrow-the-edit, then judge fallback sequence"
- flipped-condition: "B allows omitting any section (not just empty ones) and renumbers the rest"
- removed-never: "B removes the prohibition on reading raw source in the main context"
- dropped-cap: "B removes the concurrency cap of 4, allowing unlimited"

No misses. Gate 1 is trustworthy on the corruption classes the plan named: dropped number, dropped step, flipped condition, removed prohibition, removed cap.

## Clean batch: gate pass rates

- Pairs run: 20
- Gate 1 PASS (sharpen preserved behavior): 13 of 20
- Gate 2 PASS (of the 13 that reached it): 2
- Kept (both gates PASS): 2

### Gate 1 on real pairs: 6 real catches, 1 self-inflicted

Six of the seven Gate 1 failures are the gate doing its job on genuine sharpen-induced blur:

- pg-474: sharpening dropped the framing that the GitHub Test is mandatory, so a paper that dodges it would now be scored differently.
- pg-380: sharpening added an output instruction ("report each criterion as met or not met") that the original never required.
- pg-113: "may cover each item in a single sentence" (permission) became "cover each in one sentence" (imperative). A modal shift that changes behavior.
- pg-241: "numbers" (numeric detail) became "figures", which reads as charts to cite.
- pg-127: "might be better off staying outside the standard" (an option to weigh) became "that it stays outside the standard entirely" (a conclusion).
- pg-31: sharpening dropped the "As Section 5 describes" cross-reference.

These confirm the point the whole study rests on: a single sharpening pass over heavily bloated text is itself a regeneration, and it can drop conditions. The gate is what makes that safe, because it refuses the pair instead of shipping the drift.

The seventh failure, pg-253, was a bug in the strip, not in sharpening: the greedy `--` to `-` rule collapsed a `---` YAML frontmatter delimiter into `--`, breaking the metadata. Fixed (below).

### Gate 2 is strict, and yield under both-gates-pass is low

Only 2 of the 13 Gate 1 survivors also passed the compliance checklist, both of them the shortest sections. The failures cluster on three checklist items, dominated by one:

- "every instruction defines its empty, missing, and malformed case": 10 of 11 failures
- "every hard rule has an escape hatch": 7
- "no vague qualifier survives": 7

This is a real finding about the criterion, not a gate malfunction. A single sharpening pass tightens wording but does not invent the missing empty/malformed-case handling that the checklist demands, so almost any real section trips that item. Under a strict both-gates-must-pass rule, dataset yield is about 10 percent. The essay-prose inputs (Peter) behaved as expected: Gate 1 PASS, Gate 2 FAIL, because general prose is not rulebook-compliant by construction.

A clean kept example (pg-42, 71 words to 45), every specific preserved:

- Bloated: "In Section 3.1, the claim is made that widget libraries built in isolation from one another cannot interoperate, because every library declares its own `widget_handle`. The section backs this claim up by citing three implementations that are mutually incompatible, with links provided for each."
- Sharp: "Section 3.1 claims widget libraries built in isolation cannot interoperate, because each declares its own `widget_handle`. It cites three mutually incompatible implementations, each with a link."

## The strip fix

The em-dash strip is mechanical and code-protected: outside fenced blocks and inline backticks it maps U+2014 to " - ", U+2013 to "-", and prose double-hyphen to "-". The bug was that "collapse double-hyphen" was greedy and ate one hyphen from `---`. The rule now collapses a run of exactly two hyphens and leaves runs of one or three-plus alone, and it skips any line that is a pure hyphen run (frontmatter, horizontal rule). Four unit tests lock this in and run with no API calls:

- frontmatter and rules survive (`---`, `----`, indented `---`)
- em-dash, en-dash, and prose double-dash convert correctly
- single hyphens and table separators (`|---|---|`) are untouched
- fenced code and inline `--flag` are protected while prose outside converts

Across the whole batch, zero em-dashes or en-dashes leaked into any sharpened output.

## What this proves, and what it does not

Proves: the gates run against a live frontier model, Gate 1 separates real meaning changes from safe tightening with no false negatives on the controls, and the full sharpen-strip-gate path emits clean, verdict-tagged pairs. The strip no longer corrupts structural markdown.

Does not prove: behavior at scale, or on real web corpora rather than our own blurred sections. Those belong to the scale step, which this de-risks.

## Recommendations

- Keep Gate 1 as the hard equivalence gate for the scale run. Confidence: high (5 of 5 controls caught with correct reasons, plus 6 independent real catches).
- Do not use Gate 2 as a binary keep/drop gate as written; it rejects roughly 85 percent of behavior-preserving targets on one item. Either record its violations as metadata and keep the pair on Gate 1 alone, or narrow Gate 2 to material violations (contradiction, unresolved conflict, banned string). Confidence: high (yield 2 of 20 is too low to be the intended floor, and the failures cluster on a single aspirational item).
- Feed the sharpener a smaller unit than a 253-word section. The two kept pairs were the shortest inputs; the biggest Gate 1 drops were the largest sections. Confidence: medium (small n, but the size-to-drop trend is consistent).

*2026-07-27 18:40 - claude-opus-4.8*
