# Architect and vibe-coding planning session

*2026-07-28 02:07 - transcript 02e2ab27-db37-4548-80f8-f0b3046ddb71*

*Prompts p172-p223 of 223. Part 4 of 4. Reduced to principle-bearing core.*

## Prompts

**[p174]** shouldnt that be in the repo?

**[p175]** Hey, here's my question. Do you know what to do? Like, can you operate on your own? Like, can I just give you the task of performing experiments, create hypotheses, do the experiments, and just go? Just like, just go on your own for a few hours or overnight. And when I wake up in the fucking morning, I wanna see a clean dataset. Like, try, you said two hundred and fifty-three word section, try a hundred word section, try two hundred word section. Like, look, identify each variable and adjust it up and adjust it down and actually do the fucking experiments. Make a whole plan. Make a whole plan for each Experiments, and then just do it. Download what you need to do. You don't, you don't need me. You have a frontier model, just get this shit done.

**[p176]** use subagent discipline. create a strong plan. make sure the plan is standalone I will run in a fresh context. you should be fine as long as there's a plan. git commit at every experiment checkpoint. keep an experimental log and append to it each experiment. enough detail so it can be loaded into a fresh context and understand things. what about slicing a prompt up? what about downloading shitprompts from the web? what about downloading goodprompts? What about running sharpen on that?

**[p177]** Pairgen Experiment Battery

**[p178]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p182]** 1. do we have enough training data now, and
2. can we build a second training set using a relaxed version of the sharpener to run on web promptshit?

**[p183]** what if we first fine-tune using relaxed, and then fine-tune using sharp?

**[p184]** the problem I see is that the vocabulary is limited. a small subset of english.

**[p185]** what if we use @tools-public/tools-wg21/retired/plovdiv-assassin.md as a sharpener for regular text to create a sharp version, then train (original, plovdiv-sharpened)?

**[p186]** how about, can you find examples of normal sharp prose on the internet, then blur it, then train on that? this way we get compression of plain english. it has to preserve meaning though. and once you have that then train on the prompt dataset

**[p187]** how confident are you that you can recognize good, compressed human prose? and how confident are you that you can compare the blurred version and know if something was lost?

**[p188]** Set up the experiments again. wikipedia and arxiv. but keep these two datasets distinct from each other and the dataset we just collected. give each an experimental log. run both experiments concurrently using subagents. you know what to do right?

**[p189]** Plain-English Blur Datasets (arXiv + Wikipedia)

**[p195]** what about a relaxed sharpener, one that doesn't require those facts

**[p196]** Plan it in a new plan yes but also, here's another idea. What if we apply the sharpener to the plan files I have saved? in 99% of those cases it should result in a major compression. @plans/source ?

**[p197]** okay but wait a sec. we can't use (bloated plan, sharpened plan) pairs, because often the bloated plan has things that are not even relevant to the plan. I think we need to sharpen the plans, then bloat them algorithmically, then use (algorithmically bloated plan, sharepend plan) as the dataset. What do yo think?

**[p198]** Algorithmic bloat is just the normal conversion to and from latent space which is the whole thesis of this study. We do it on the entire sharpened plan file. we should not try to steer the model into bloating, the bloating happens on its own because of sampling top-k.

**[p199]** Yes I believe this is correct. Verify. "Blur" doesn't lose information (well, almost). Instead, it gives you back something with the same meaning but it took more words to say it.

**[p200]** whether it preserves meaning matters based on the input. if it is a machine instruction then the blur sjhould not lose meaning. if it is something like the abstract from a scientific paper, then it can change because a scientific description is less objective than a command. What do you think?

**[p201]** yeah that feels right and also are you keeping a journal of these discoveries and observations?

**[p202]** I see a problem. This is actually wrong:

**[p203]** > Every hard rule has an escape hatch.

**[p204]** Its not supposed to be "escape hatch" it is supposed to be "rationale, so the model can adapt to a novel application of the rule"

**[p205]** "One term names each concept." this is also wrong. It should be "Each concept is referred to by one name, not more".

**[p206]** We need to look at the entire history of @tools-public/how-to/how-to-write-prompts.md and @tools-public/tools/german.md to understand what the fuck happened.

**[p207]** And I suspect we might have to re-run ALL our experiments.

**[p208]** " without changing what it commands" is awkward phrasing

**[p209]** What does " hand the decision back to the model." mean? is this a good or a bad thing?

**[p210]** is this blurring? I want you to look at the revision history and trace the provenance of this line

**[p211]** what the fuck is this: "State each rule's scope; models stop at the stated reach." ? "stated reach" sounds terrible

**[p212]** how good is the original how-to

**[p213]** what about @tools-public/tools/german.md ?

**[p214]** germand.md is no good then. rules without rationale leaves the model hallucinating when the input doesn't perfectly match the rule

**[p215]** we should either drop german from consideration, or we should really go through every german rule and only if it is truly novel compared to how-to-write-prompts, then work together to figure out how to integrate it as a rule

**[p216]** the analytical framework cluster should not be part of the sharpener. its too specific. the sharpener is supposed to align the model generally not prescribe algorithms

**[p217]** the narrow cut I think is right and also, you might just as a quick experiment, see if this cut is cleanly visible from the commit log. that is, that there is a point in time before which is all the stuff we want, and after which is when the new stuff was added

**[p218]** yes and I want the plan to have the 17 novel in-scope rules with rationale so i can preview it

**[p219]** Question: "write each result to the accumulator as it completes. Rationale: holding all results in memory risks total loss on failure and pressures the context; streaming persists progress incrementally." what is a result? every byte? every sentence? every paragraph?

**[p220]** I am getting exhausted it feels like we keep going in circles. Every time you try to tighten or do something, we get more of the problem that the thesis of this entire endeavor rests on.

**[p221]** Three fucking plans. The irony.

**[p222]** move the dead ones to trash. write a report with all our findings into the repo

**[p223]** my conclusion is that I need to edit the how-to-write-prompts file by hand. human compression.

[Dropped: p172/p179/p191/p193 identical to-do boilerplate, p173/p194 status questions, p180-p181 link troubleshooting, p190/p192 repeats of p178.]

## Plans

### semantic blur report

*Write a research-type report documenting the measured bloat across three prompt files, explaining the resampling mechanism that causes it, and establishing the plan file as the artifact that must be preserved.*

Governing constraint: a report about bloat that is itself bloated fails on contact.

The argument, as point-stating headings: three files grew between 17 and 146 percent while nobody added a feature; each rewrite resamples the whole file; the first version is sharp because it conditions on human intent versus prior model output; the plan file escapes it because decisions are discrete; preserve the plan, regenerate the artifact.

Closing irony, verified in the source: architect.md already states "a design that changes is regenerated from an updated plan" and that findings are resolved "by updating the plan and running it again, never by patching the document in place". The tool prescribes the cure and was not given it.

[Growth figures, qualifier densities, figure list, calibration, todos dropped.]

### compression test architect

*Run a frontier-model compression test on architect.md: compress each paragraph, apply the mechanical non-expansion guardrail, assemble the compressed version, and report token savings.*

The compression mandate per paragraph: "Rewrite this instruction text to use fewer tokens while preserving exactly the same meaning a model would execute. Keep all specific numbers, names, tag names, and schema fields. Use imperative voice, common words, and no filler. If you cannot make it shorter, return it unchanged."

The guardrail: if the compressed version is not strictly shorter, discard it and keep the original. This is mechanical and outside the model.

Scope: a test, not a product. One file, one pass, no fixed-point iteration, no trained model - to see whether the compression concept works on real prompt text and what savings are realistic.

[Batching approach and todos dropped.]

### blur compression report

*Write a research-type report in promptforge covering the measured prompt degradation, its mechanism, the plan-as-source maintenance architecture, the compression experiment, and the full prior-art survey for building a compressor.*

The mechanism, corrected during the inquiry: blur is proportional to how much of the conditioning input is model-generated, not to how much output is generated. This is why v1 is sharp despite being fully generated - its input was human intent - and why every rewrite is blander, since its input is the previous model-generated file plus a small human delta.

The gaussian insight: blur does not only smooth, it widens. A sharp edge becomes a soft gradient occupying more space. "Cap at 3" becoming a twenty-word justified sentence is the same operation. Bloat and blur are one phenomenon, which is why the measured growth and the measured blandness arrive together.

Design section: extractive compression is idempotent, monotonic, and zero-blur by construction, because it cannot emit a token that was not in the input. Generative produces better prose but needs the guardrail, is not idempotent, and carries a little blur. The conclusion is two tools for two audiences rather than one tool that compromises. Verification and determinism decisions: execution-equivalence as the metric, the guardrail enforced outside the model so its worst case is returning the input verbatim, greedy decoding at temperature 0, and CPU inference for true determinism since the residual non-determinism at temperature 0 is GPU floating-point ordering rather than sampling.

The prior-art survey closes on what is unbuilt: the combination of execution-equivalence verification, a mechanical non-expansion guarantee, fixed-point iteration, and deterministic CPU decoding.

[Verified data, figure list, prior-art inventory, calibration, todos dropped.]

### prose pass on report

*Apply the prose rulebook's style-revision passes to prompt-compression-research.md to strip AI-generated idioms - meta-announcements, self-narration, and over-cap machine idioms - with no length pass and no content change.*

This is deletion and local rewrite only, which by the report's own argument is blur-free because unchanged text is never regenerated.

How it runs: directly, as targeted StrReplace edits in the main context, not a subagent swarm. The file is one document with a single voice to hold consistent; splitting it across subagents would fragment exactly the judgment this task needs.

[Idiom inventory, pass details, constraints, verification, todos dropped.]

### teaser cut second pass

*A second, targeted prose pass on prompt-compression-research.md removing the value-teaser and curtain-raiser sentences the first pass missed - lines that announce a point is interesting instead of stating it.*

The targeted class: sentences that advertise a point's significance or tease "the interesting reason" before delivering it. Throat-clearing that makes the reader wait. Same fix as before: pure deletion or a lead-with-the-content rewrite, blur-free.

[Eight-hit inventory, constraints, verification, todos dropped.]

### blur dataset generator

*Build a Rust CLI tool that takes a markdown file, splits it into sections, blurs each section through multiple passes of the Anthropic API using rotating models, and outputs a JSONL training dataset of (blurred, original) pairs at multiple blur levels.*

The blur prompt: "Rewrite the following text. Preserve all meaning." No "expand," no "add context," no system prompt. Let the model's natural resampling do the blurring.

Model rotation (Sonnet, Haiku, Opus) ensures every blur level has a mix across the dataset.

[CLI, crates, rate limiting, validation list, todos dropped.]

### first-gen extractor

*Build a Rust tool that finds the true first-generation version of every tool file across four repos by searching all git histories by basename, extracts each v1, and emits the clean training targets plus a provenance manifest.*

The problem it solves: the sharp training target for the deblurrer is the first-generation version of each tool, before revision blurred it. Finding v1 is hard because files were renamed, moved between directories, and moved across repo boundaries; git --follow cannot cross repos.

The key insight: match by basename, not path. Search every repo's entire history for the creation of any file with that basename, take the globally earliest, and that is the true first generation.

Residual handling: a file whose basename changed AND crossed a repo boundary has no shared name to match on. The tool does not guess at those; it flags bulk-import-looking origins with "possible-earlier-origin" for manual review rather than giving a wrong automatic answer.

[Algorithm steps, CLI, crates, verification, todos dropped.]

### pair pipeline validation

*Build the minimal end-to-end pair-generation path - sharpen plus em-dash strip plus the two gates - and validate it on ~20 bloated inputs with negative controls, proving the gates actually discriminate before any scale run.*

Purpose: prove the one untested link in the generation path - the two gates (execution-equivalence and rulebook-compliance). They are the quality floor of the whole dataset and have never run. Validate them on a small batch, with negative controls, before acquiring corpora or generating at scale.

Gate 1, execution-equivalence: "Would any model, following B instead of A, ever behave differently on any input? Weigh dropped conditions, changed numbers, altered defaults, removed edge cases, narrowed or widened scope." Gate 2, rulebook-compliance against the sharpen-instrument checklist. A pair is kept only if both gates PASS. Dropped pairs are logged with the reason, never repaired.

Negative controls are the point. A gate that always says PASS is worthless, the same trap as a test that cannot fail. Five passing targets are corrupted one way each (drop a number, flip a condition, remove an escape hatch, delete a NEVER, narrow a scope); Gate 1 must FAIL all five, or the gate does not discriminate and the pipeline is not trustworthy.

[Em-dash strip and blur-gen degenerate-input guard details, output schema, crate reuse, todos dropped. A corrupted char-per-line JSON todo dump (~700 lines) and a full duplicate copy of this plan were also dropped.]

### Pairgen Experiment Battery

*Run 6 experiments varying section size, gate mode, input source, effort level, and multi-pass strategy to find the configuration that maximizes pair yield while preserving Gate 1 discrimination. Produce a clean dataset and a complete experiment log. Runs autonomously with subagent discipline, git-committing at every checkpoint.*

Ground rules: subagent per experiment - the main context dispatches each experiment with spec, paths, commands, and success criteria; the subagent runs it, writes results to files, returns a one-line summary. Git commit at every checkpoint. Append-only experiment log; each experiment gets hypothesis, method, results, finding, and commit hash. The log is the reload point for a fresh context.

[The six experiment specs, consolidation step, cost estimates, log format, reload instructions, and todos dropped as test plan.]

### Plain-English Blur Datasets

*Build two distinct pilot datasets - arXiv abstracts and Wikipedia leads - by blurring ~100 sharp human passages each and keeping only (blurred -> original) pairs where a directional meaning gate confirms the blur dropped nothing. Each dataset gets its own log; the two experiments run concurrently in subagents; both stay separate from each other and from the existing prompt dataset.*

Why the gate is directional: input is the blur, target is the human original. If the blur dropped a specific, the target contains something the input lacks, which would train the compressor to hallucinate. So keep a pair only when following the blurred text behaves the same as following the original. This conservative holistic gate also drops pairs where the blur added a spurious constraint, which is safe.

Three datasets now exist and never mix: prompt, arXiv, Wikipedia. Each has its own log.

Concurrency and git: subagents do data work only and return a one-line summary; they do NOT run git. The main context commits sequentially to avoid an index.lock race between concurrent commits.

[Script inventory, gitignore, cost, scale path, todos dropped.]

### Relaxed Cut-Only Compressor

*Build a cut-only "compression instrument" (the sharpen rulebook with all add-rigor rules removed, so it never invents facts) and pilot it on two genuinely-bloated sources - web prompts and the user's own 2,742 plan files - measuring whether it beats the aggressive instrument on gate1 pass rate while still delivering real compression.*

The idea: the sharpen instrument bundles two jobs - cut (remove filler, hedging, redundancy) and add rigor (quantify every quantity, define the empty case, add an escape hatch). The add-rigor rules are why the aggressive instrument INVENTS facts on vague input and fails gate1 ("provide clear options" became "provide 2-4 options"). A compressor should only cut, never add. One binding rule: "Add nothing not present in the source; if a specific is absent, leave it absent."

[Pipeline, input assembly, script change, metrics, gitignore, cost, todos dropped.]

### Plan Deblurring Dataset

*Build in-domain deblurring pairs from the user's 2,742 plan files: sharpen each plan into a crisp instruction target, regenerate it once through the model (natural top-k blur, no steering) to get a blurred input, and keep (blurred -> sharp) pairs where a mandatory directional gate confirms no specific was lost.*

Supersedes the cut-only compressor plan. That approach used the raw bloated plan as input, which is contaminated: a raw plan carries organic, off-topic content, so a (raw -> sharp) pair would train the model to make relevance judgments (a meaning-dropping behavior). The fix is sharp-target-plus-controlled-degradation.

What we now believe (verified this session):

- The tool is a deblurrer / resharpener, not a shortener. Blur rewords ~54% of the words at roughly constant length (+6%), so the signal is wording and specificity, not length.
- Blur is not almost-lossless: a single pass drops or alters a specific in ~43-54% of cases, rising to ~81% by pass 10. So the directional gate is mandatory.
- Command-vs-description law (user's hypothesis, supported by the arXiv failure data): crisp instructions preserve meaning under blur because they have execution semantics that a reword converges back to; descriptions drift because their language is interpretive. Target domain here is plans (instructions), so expected yield is high.
- Clean supervision: sharpen the plan into a crisp target, then blur that target; the delta is pure degradation, meaning is anchored, and no relevance judgment is baked into the pair.

[Layout, step mechanics, reuse, gitignore, cost, todos dropped.]

### Sharpener Instrument Rebuild

*Rebuild sharpen-instrument.md from a known-sharp base rather than patching the accreted one: start from how-to's tight 2026-07-08 birth core, de-slop the later-added sections, integrate the 17 novel in-scope German rules each with a rationale attached, restore the reasons the original distillation stripped, fix the confirmed blur and reorder, and exclude the analytical-framework methodology (narrow cut).*

Why rebuild rather than patch: the distillation introduced several defect types - a lexical blur (one-term), a reorder that split problem from remedy (hand-the-decision), stripped reasons (stated-reach), and scope-creep (a whole analytical-framework tier). how-to-write-prompts.md has a tight 2026-07-08 birth core but acquired slop in sections added 2026-07-25; german.md is lean but reasonless. Rebuilding from the sharp base is cleaner than un-blurring the accretion.

Strategy: base on how-to's 2026-07-08 birth as the general-alignment core; re-add only the wanted later material (sections 9 Context and 10 Propagation), de-slopped one-instruction-per-sentence with reasons kept; integrate the 17 novel in-scope German rules, each with a rationale attached (German omits reasons); restore every reason the first distillation stripped; fix the confirmed one-term blur and the hand-the-decision reorder; exclude the analytical framework entirely (narrow cut) - it prescribes a diagnostic algorithm, not general alignment.

The 17 novel in-scope German rules, with rationale (preview):

1. Pipeline Map (German 1): place a flowchart at the top showing every step, branch, and parallel path; annotate each dependent step with its requirement. Rationale: a model reads steps in encounter order and misses branches, parallelism, and dependencies unless the control flow is shown before the steps.
2. Step Numbering (German 2): number steps from 0 with an execution-context annotation on each header; no sub-numbering, no unnamed steps. Rationale: stable numbers let steps reference each other unambiguously, and the annotation tells the model where each step runs; sub-numbers and unnamed steps make order and identity ambiguous.
3. Batched Output (German 4): when output exceeds one context, split into sequential subagent batches, each receiving the output-so-far plus its inputs. Rationale: a context forced past its output limit truncates; batching bounds each unit to what one context can emit.
4. Parallel Marking (German 5): mark which steps run in parallel and follow each fan-out with a consolidation step. Rationale: unmarked, a model serializes parallel work or leaves fan-out outputs unmerged; an explicit consolidation guarantees recombination.
5. File Isolation (German 7): give each parallel subagent a separate numbered output file. Rationale: concurrent writes to one file corrupt each other; separate files make parallel writes conflict-free by construction.
6. Breadcrumbs (German 8): define a structured summary format carrying the minimum fields downstream steps need. Rationale: without it, a step re-reads and re-loads full upstream research, or misses a field it needed.
7. File Intent (German 9): tag every file research, scratch, or output. Rationale: a file's lifespan and audience are invisible from its bytes; the tag tells the agent what to keep, overwrite, or deliver.
8. Accumulator File (German 10): use one canonical state file with a fixed header schema that each step appends to. Rationale: state scattered in context is lost on compaction; one append-only file is the durable, recoverable record.
9. Stream to File (German 11): write each result to the accumulator as it completes. Rationale: holding all results in memory risks total loss on failure and pressures the context; streaming persists progress incrementally.
10. Scratch Lifecycle (German 14): specify creation, consumption, and retention for each scratch file. Rationale: undefined lifecycle leaves orphans or premature deletion; specifying it keeps the pipeline auditable and safe.
11. Alignment Contract (German 18): for sequential writers, inject a contract - append-only, reuse earlier terms, no contradictions, shared frame. Rationale: independent writers otherwise drift in terminology, contradict earlier sections, and re-frame the same material; the contract keeps a multi-writer document one coherent voice.
12. Section Enforcement (German 19 + 24): enumerate output sections with exact headers and fixed order; none renamed, merged, or reordered; omit an empty section without renumbering the rest. Rationale: consumers and readers rely on stable section identity and order; renaming or reordering breaks references and parsing.
13. Elastic Sizing (German 22): describe what each section covers and let data drive length; no hard word counts. Rationale: a fixed count forces padding when content is thin and truncation when it is rich; coverage plus data-driven length matches output to substance.
14. No Cross-Agent Numbering (German 26): avoid footnote or superscript schemes that require coordination across subagents. Rationale: independent subagents cannot share a counter, so cross-referenced numbers collide; inline hyperlinks need no shared state.
15. Persona Zones (German 30): separate persona into zones - internals rich, progress one clause, output none. Rationale: persona aids voice in tool internals but corrupts deliverables and bloats progress reports; zoning confines flavor to where it helps.
16. Handoff Clarity (German 43): at each step boundary, specify whether data moves through a file or working memory. Rationale: an unstated handoff leaves the model guessing whether to persist or carry data, causing lost data or redundant reads.
17. Challenge Locus (German 44): when a step mixes subagent and main context, specify which part runs where. Rationale: unspecified, the whole step runs in one context, losing the isolation the split was meant to provide.
18. Write Safety (German 49): when multiple subagents could write the same file, specify sequential versus parallel. Rationale: concurrent writes race and corrupt; declaring the mode prevents the conflict by design.

(18 listed; German 24 folded into 12.)

Explicitly excluded:

- Analytical framework (German 53-65): diagnostic methodology, not alignment. Stays in German.
- Redundant with how-to (German 13, 16, 27, 28, 31-40, 42, 45-48, 50, 52): how-to states these, usually with the reason already attached.
- Conflict (German 21 "flat Never X" versus how-to "pair every prohibition with its replacement"): how-to wins; German 21 dropped.

[Validation steps, ordering, and todos dropped. Two further full copies of this plan and their corrupted char-per-line JSON todo dumps (~2,200 lines total) were dropped.]

## Design Documents Written

### sharpen-instrument.md (promptforge/study/make-dataset/)

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

### experiment-log.md (promptforge/study/make-dataset/)

Append-only record of the experiment battery; each experiment tests one variable in the sharpen-strip-gate pipeline. This file is the reload point: a fresh session reads it to see which experiments are done and resumes from the first incomplete one.

Baseline from the prior validation run: 20 bloated inputs, Gate 1 PASS 13/20, Gate 2 PASS 2/13, kept 2/20 (10%). Gate 1 caught 5/5 negative controls. The two kept pairs were the smallest inputs (57w, 71w).

[Entry format template and the E0 infrastructure entry dropped.]

### findings.md (promptforge/study/make-dataset/experiments/)

Optimal configuration: Gate 1 (execution-equivalence) alone - drop Gate 2 (gate1-only yields 90% vs 10% strict; narrowed gate2 caught zero defects beyond gate1, so it is pure redundant cost). Minimal-change sharpen for a safety-first compressor, or aggressive-then-minimal two-pass for more compression (minimal recovers 72% of aggressive failures). Effort medium. Input size irrelevant to quality; slice only to multiply volume. Source: the user's own prompts and blurred versions of them, not web prompts.

The core result: sharpening cannot recover a blurred original - the sharpened output is no closer to the sharp original than the blurred input is (similarity 0.446 vs 0.447, closer only 51% of the time, a coin flip). Blur is irreversible from within the chain. Two consequences: the training target must be the true original, captured before any blur; and instrument-sharpening still produces a valid, shorter, execution-equivalent version of any bloated input - a legitimate compression pair, just not a reconstruction of a lost original.

Why web prompts fail: the instrument's gap-filling rules ("quantify every quantity", "define the empty/missing/malformed case", "escape hatch per hard rule") are correct for tightening prompts that already carry their specifics, but on vague web prompts they force the sharpener to INVENT specifics ("provide clear options" becomes "provide 2-4 options"), which Gate 1 correctly rejects as behavior change. About a third of web failures were invented constraints, not dropped ones. Arbitrary text is the wrong source; the specifics must already be present.

The dataset: 337 pairs - 286 blur-to-original (gold; target is the true sharp first-gen text) plus 51 gate1-verified bloat-to-sharp.

Scale path: blur all 85 first-gen prompts at 2-3 variants x 3 passes for on the order of thousands of blur-to-original pairs; run pairgen gate1-only, medium effort, minimal-change prompt over any remaining bloated corpus; do not spend more on web corpora (contaminated, 23% yield).

[Tooling change list dropped.]

### semantic-blur-report.md (promptforge/study/make-dataset/)

Thesis: an LLM asked to "revise" or "rewrite" a prompt does not edit it; it regenerates it, resampling from the training distribution. Each pass moves the text toward the mean: blander, more hedged, more exhaustive, less specific. This is semantic blur, the text analog of pushing an image through latent space and back. The goal of good prompting is the opposite direction, toward the argmax and the tail of the distribution, where the sharp, specific, load-bearing tokens live. Blur is irreversible from within the chain: by the data processing inequality, mutual information with the original intent only decreases with each regeneration, so no amount of further regeneration recovers what was lost.

What the experiments established: Gate 1 discriminates (caught 5 of 5 deliberate corruptions and, independently, real sharpen-induced drops); Gate 2 is too strict, rejecting ~90% of behavior-preserving targets on one aspirational item - use Gate 1 alone. Input size irrelevant to quality. Web prompts are a contaminated source (23% gate1 pass; the instrument invents specifics on vague input). Blur is irreversible, confirmed. Medium and high effort were within gate noise. A gentle minimal-change re-sharpen recovers 72% of Gate 1 failures.

What blur actually is (measured, not assumed): not almost-lossless - a single "rewrite, preserve meaning" pass drops or alters a specific in 43-54% of cases, 81% by pass 10, so the directional gate is mandatory. A reword toward the mean, not an expansion - among meaning-preserved pairs ~54% of words change at essentially constant length. Depth is counterproductive - over 10 chained passes expansion stayed flat (~1.07x) while the gate pass rate collapsed 56 to 27 to 19%. The command-versus-description law: crisp instructions survive blur far better than descriptive prose, because a command has an execution semantics a reword converges back to, while a description has interpretive latitude that drifts (abstracts 45%, Wikipedia 56%, instruction-flavored content higher). The dramatic bloat originally observed on real prompts (+18% to +146%) came from revision-with-added-content, a different operation than a bare rewrite, which barely expands.

The reframe: the tool is a deblurrer and resharpener, not a shortener. The clean way to supervise it is sharp target plus controlled degradation: take a known-sharp original, degrade it, and train (degraded to sharp). Because the delta is only the degradation, meaning is anchored and the model learns pure reversal, with the gate removing any pair where the degradation dropped a fact.

Model and training design: a 2-3B model, fine-tuned not trained from scratch - the base understands meaning already, so this adds one narrow skill. Vocabulary lives in pretraining, not the fine-tune set; the real risk is the model regressing rare words toward its own narrow mean, countered by a preserve-rare-tokens training rule. Determinism: temperature 0, single-thread CPU, fixed summation order gives true idempotence; floating-point non-associativity is why GPU temp-0 still flips a near-tie token, and one flip diverges the rest of the sequence. Guardrails mechanical, not model-trusted: output token count must not exceed input (the model can never expand; worst case returns the input); em-dash and structural-markdown strip applied outside the model. Curriculum (untested): general/broad compression first, the user's prompt style last, with a small rehearsal mix to prevent forgetting.

The instrument audit (a study within a study): the instrument itself had degraded during its one-time distillation - a lexical blur ("Use one term per concept" became the ambiguous "One term names each concept"), a reorder that split a rule from its remedy (the vague-qualifier rule), stripped reasons (the scope rule lost its "models read literally" mechanism), scope-creep (a whole analytical-framework tier that prescribes a diagnostic algorithm rather than aligning prose), and undefined terms ("write each result" never defines "result"). Provenance from git: how-to-write-prompts.md was born tight on 2026-07-08; its slop entered with the sections added 2026-07-25. german.md is lean but reasonless, and its reasonless style, misapplied to how-to's reason-rich rules during distillation, is what stripped the reasons. The decisive point: a blurred rulebook still produces sharp outputs, so the instrument's imperfections never actually blocked anything.

The meta-lesson: the endeavor proved its own thesis by living it out. You cannot fix blur by regenerating, because regeneration is the blur; the only blur-free operations are a human with a delete key (cropping removes tokens without resampling the survivors) and targeted, non-regenerative edits that preserve the sharp original. And an audit for ambiguity has no fixed point: language is never perfectly unambiguous, so a line-by-line hunt always finds one more imperfection - chasing perfection is the blur trap applied to process. The exit is not a cleaner lap. It is to ship the sharp-enough, stop regenerating, and use targeted edits for the few genuine defects.

Recommendations: keep Gate 1 as the hard gate, drop Gate 2; the training target must be the true pre-blur original, never a re-sharpened blur; leave the instrument in place - if closure is wanted, make only the two surgical fixes (the one-term line, the vague-qualifier reorder) as targeted edits, never a rebuild; do not scale web prompts - the in-domain source is the user's own prompts and plans, degraded from a sharp target; next real step is a plan/prompt deblurring dataset under Gate 1.

StrReplace-edited design docs (path only): experiment-log.md, plain-english/wikipedia/wikipedia-log.md.
