# Sharpening Instrument

Rules for tightening a prompt: making it unambiguous and aligned, cutting dead weight, without changing what it commands. Apply the tier that matches the target, then audit against each rule one at a time.

Two rules bind everything below:

1. Write every instruction so only one reading is possible.
2. Spend the smallest set of high-signal tokens that makes the outcome likely.

Tier by target kind. Tier 0 applies to every prompt. Add Tier 1 when the target defines tools, spawns subagents, or runs unattended. Add Tier 2 when it emits an artifact invoked later on its own. Add Tier 3 when it runs a diagnostic or analytical pipeline.

## Tier 0: Every prompt

### Specify

- Quantify every quantity: "3-5 bullets", not "a few".
- Define each fuzzy term at first use.
- Replace vague qualifiers with a decision rule: "if X do Y; if unsure do Z". "Appropriately", "as needed", "when relevant" hand the decision back to the model.
- Replace an enumerated branch list with the heuristic that generated it when each new case would need a new branch.
- Replace advice that fits any task with the signals, formats, and boundaries specific to this one.
- State each rule's scope; models stop at the stated reach.
- Define the empty, missing, and malformed case for every instruction.
- Give every hard rule one defined action for when its precondition fails; a hard rule with no escape hatch fabricates when reality refuses.
- Ask for above-baseline effort in words; an unstated wish gets the minimal reading.
- Acceptance bar: a colleague with no prior knowledge could execute it without a question.

### Structure

- Separate instructions from data in named containers; say what each holds.
- Pick one markup convention and keep it; the sole exception is a tag on a block dispatched to a subagent by name.
- Keep instructions in prose and lists; reserve JSON for data.
- Put one testable constraint on each line.
- Bullets for parallel rules; numbers for sequences.
- Load the edges: opening and ending are best attended, the middle worst.
- Restate the binding rule at the end of any target over a page.
- Place each rule next to the content it governs; compliance decays with distance.
- Cut every line whose removal changes no behavior: back-references, filler, repeated instructions, meta-commentary, restated priors, rationale that restates the rule, obvious implications.
- Fix typos in load-bearing keywords.

### Examples

- Show the format; an example is a specification, a description is a paraphrase.
- Match each example to the desired output exactly, formatting included; the model copies what it sees over what it reads.
- Give 3-5 examples when format matters, diverse and balanced, not ending on a same-label run.
- Keep examples consistent with the rules; on conflict the model follows the examples.
- Curate canonical examples instead of enumerating edge cases in prose.
- Mark a counter-example as wrong where it stands and put the corrected version beside it.
- Specify output as a schema plus one filled example.
- Name the failure modes excluded: "no preamble, no code fences, no commentary after".
- Order schemas so reasoning fields precede answer fields.

### Voice

- Write every instruction as an imperative command, second person, present tense; if the command implies the prohibition, cut the prohibition.
- One instruction per sentence.
- Start each parallel list item with a verb.
- Delete hedges: "try to", "if possible", "you may want to".
- Neutral register: no courtesy padding, no stakes, no tips, no threats.
- Use a persona to set voice and audience, not to claim accuracy; separate persona into zones (internals rich, progress one clause, output none).
- Replace style-by-reference ("write like X") with concrete sentence-construction rules.
- Pair every prohibition with its replacement; keep it short and adjacent.
- Attach the reason to a non-obvious rule; a model generalizes from the reason and pattern-matches a bare rule.
- Use one term per concept throughout.
- Replace aspirational or metaphorical instructions with behavior the model executes mechanically.
- Back every technical term with a finding; terms as decoration weaken credibility.

### Budgets and conflicts

- Count the hard constraints binding at once; past six, joint compliance collapses.
- Bring the count down by staging across passes, moving format into the example, and deleting what nothing depends on.
- Reserve NEVER, ALWAYS, MUST for invariants whose single violation is unacceptable; cap at three.
- Write judgment calls as decision rules, not absolutes.
- State a priority for every pair of rules that can collide.
- Move guarantees prose cannot deliver into code: schema validation, linters, banned-string checks.
- Apply the detectability test: name what a violation looks like; cut any rule whose violation is unobservable.

### Outcomes

- State the goal, success criteria, and stop condition, then let the model choose the path.
- Prescribe exact steps only where the sequence is the requirement: fragile pipelines, compliance, destructive operations.
- Set an effort budget wherever wandering is possible.
- Cut "think step by step"; state the quality bar and raise the effort setting.
- Start minimal on the strongest model; add only what observed failures demand.
- Name the failure mode before adding tokens for it.
- End hard tasks with self-verification against named criteria.

### Integrity

- Omit unverifiable facts and citations; never fabricate.
- Designate one canonical source when data appears in more than one place; others reference it.
- Give every loop a concrete stop condition; no subjective threshold.
- Define what counts as failure wherever there is retry logic.
- Remove cache-management and standalone "Commands" sections; frontier models handle these.
- Remove inert directives: deviation notices, save reminders, resumption protocols; the platform handles these.

## Tier 1: Tools, agents, unattended runs

### Tool and subagent design

- Write each tool description in four parts: what it does, when to use it, when not to and which sibling covers that case, and each parameter with its exact format.
- Intern test: a newcomer given only the description uses the tool correctly.
- Close open sets with enums; make invalid parameter combinations unrepresentable.
- Give each tool a stop condition and an uncertainty threshold scaled to risk.
- Write each subagent task self-contained: objective, output format, sources and tools, boundaries, effort budget.
- Ship subagent task text verbatim; inject a fixed block by tag reference, passing the file path and tag name, never a paraphrase.
- Route large assembly through the shell rather than one write call.
- Trace every artifact the pipeline names to the step commanded to create it; flag any referenced-but-never-created artifact.
- Cap the tool set at the minimum; remove any tool another covers.
- Disambiguation test: for each situation name the one correct tool.
- Cap each subagent return at 1,000-2,000 tokens of distilled findings, or a summary plus a path.
- Budget the tool's return value, not only its description.
- Give the agent primitives that inspect large data without loading it.

### Context and token economy

- Treat context as an attention budget that depletes, not a container that fills; degradation begins before the window fills, on every model.
- Declare what enters the main context and what never does, as two lists.
- Run a command in the main context only when it bounds its own output independent of state; dispatch everything whose size depends on whether something went wrong.
- Keep identifiers in context and payloads out; load contents through a tool at the moment of use.
- Pre-load what is small, stable, and needed every run and the instructions that bind every step; retrieve volatile data just in time.
- Prefer live navigation over a precomputed index when the data changes between runs.
- Name files and directories so the path alone states purpose; keep sizes, names, and timestamps accurate.
- Pair every grant of autonomy with a heuristic and a stop condition.
- Compact at a quantified trigger; write state to a fixed known path first, then restart from it; clear consumed tool results first, recall over precision.
- Restate the binding rules into context on a fixed step interval.
- Re-audit prescriptive scaffolding on every model upgrade and delete what the new model no longer needs.

### Pipeline and data flow

- Place a flowchart at the top showing every step, branch, and parallel path; state each step's dependency.
- Number steps from 0 with an execution-context annotation on each header; no sub-numbering, no unnamed steps.
- Consolidate always-apply rules into one block at the top.
- Mark which steps run in parallel; follow each fan-out with a consolidation step.
- Assign each parallel subagent a separate numbered file; consolidate in the main context; specify sequential versus parallel to prevent write conflicts by design.
- Route all subagent output to files and return a one-line status; read from files, never from return values.
- Send each subagent only the data its step needs.
- Define a structured summary format carrying the minimum fields downstream steps need; do not force re-reading raw research.
- Tag every file with intent: research persists, scratch is disposable, output is the deliverable.
- Use one accumulator file with a defined header schema; each step appends; stream results as they complete.
- Specify creation, consumption, and retention for each scratch file; never delete, scratch persists as audit.
- Define how file slugs derive from inputs.
- Specify whether data crosses each step boundary through a file or working memory, and which part runs where when a step mixes contexts.
- Restrict model tiers to two, fast and parent; the platform resolves tier to model.

### Output control

- Consolidate all output-formatting rules into one tagged block injected into every writing subagent.
- Inject an alignment contract for sequential writers: append-only, reuse earlier terms, no contradictions, shared frame.
- Enumerate output sections with exact headers and fixed order; none renamed, merged, or reordered; omit an empty section without renumbering the rest.
- Generate section headers from content, not generic categories.
- Describe what each section covers topically and let data drive length; no hard word counts.
- Cover every case in a template including zero elements; specify what an empty section contains.
- Wrap reusable injected content in tags; prose boundaries are ambiguous.
- Move each citation to the rule or instruction that activates it; use a markdown hyperlink where a URL exists, never a superscript; avoid numbering schemes that need cross-agent coordination.
- One sentence per progress report, most important result first.

## Tier 2: Artifact emitters

- Choose how a block travels by whether its reader shares this run: a subagent gets it by tag reference; an emitted artifact gets the rules written in as substance.
- Name no source document for the rules in an emitted artifact; state the rule, strip the provenance.
- Carry the wording and context kernel into every emitted artifact, adapted to its subject: imperative rules, quantities as numbers, an escape hatch per hard rule, a replacement per prohibition, the empty/missing/malformed case, a two-list context declaration, subagent-only exploration, bounded state, capped returns, quantified compaction, a stop condition and progress test per loop.
- Give every tool that emits artifacts a named emission-discipline block and a generation checklist that verifies it, including one line confirming no emitted file names a source for its rules.
- Carry this tier recursively when an emitted artifact emits artifacts of its own.

## Tier 3: Diagnostic and analytical tools

- Group tests into named clusters by structural concern.
- Assess evidence sufficiency before diagnosis; report the gap when too thin.
- Pre-write the blind spot each test misses when it passes clean; feed the gaps into compound analysis.
- Provide the compound step with known failure patterns and run it in an isolated subagent receiving only structured summaries.
- Deploy a challenger at escalating levels: individual findings, candidate actors, compound dynamics.
- Invert surviving findings into demand sentences and research who fulfills each.
- Dedicate a step to whether each finding is improving, stable, or degrading.
- Define explicit confidence levels with evidence thresholds; flag speculation as speculation.
- Evaluate whether domain-specific frameworks strengthen the diagnosis; extract, merge with static rules, rank, select.
- Synthesize one internal thesis naming the dominant dynamic; use it to frame every section, never emit it verbatim.
- Map diagnostic clusters to output sections; never dump all findings into one.
- Report pipeline statistics as summary counts with kill records; no itemized tables.

## Checklist

Run on the sharpened target; each answers yes or no, each no returns to its rule.

- Every quantity is a number or a range; no vague qualifier survives.
- Every rule carries its scope; every instruction defines its empty, missing, and malformed case.
- Every hard rule has an escape hatch.
- Instructions and data sit in separate named containers.
- Every sentence is a command or a fact; no hedges.
- Every prohibition carries its replacement.
- Simultaneous hard constraints number six or fewer; NEVER/ALWAYS/MUST three or fewer.
- No two rules conflict without a stated priority; every rule's violation is observable.
- No line survives whose removal changes no behavior.
- One term names each concept.
- The meaning an executing model would follow is unchanged from the original.
