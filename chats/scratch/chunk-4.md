---
produced: 2026-08-19
title: PromptForge design principles mined from architect vibe-planning chat part 3 (blur dataset, sharpening, prompt tightening)
---

# 2026-07-28-0207-architect-vibe-planning-part3.md

```yaml
- statement: Prompts are written to read beautifully as human prose; readability outranks token-count reduction.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p118]
  rejected-alternative: extractive token dropping applied to the author's prompts
  endorsement: n/a

- statement: Tightening a prompt means making it aligned and unambiguous, not making it shorter.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p146]
  rejected-alternative: reading "tighten" as size reduction
  endorsement: n/a

- statement: Prompt-tightening rules propagate transitively; applying the rulebook to a plan tightens the tool the plan produces, and a tool that produces tools passes the applicable rules down to its products.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p157]
  rejected-alternative: applying tightening only to the plan document itself
  endorsement: n/a

- statement: Expansion of text must be natural expansion; a blurring pass never invents justification or context that the source did not contain.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p126]
  rejected-alternative: expanding points with additional context or justification (hallucination)
  endorsement: n/a

- statement: Blur-training source material must be first-generation, human-authored prompts; AI-generated output is not valid training input.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p137]
  rejected-alternative: training on AI-generated outputs
  endorsement: n/a

- statement: Model calls for sharpening and validation run bare against the model, without a host harness's system prompt, prompt engineering, or injected context.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p154]
  rejected-alternative: running validation through Cursor's harness with its system context
  endorsement: n/a

- statement: A style rule belongs in mechanical sharpening only if it can be applied mechanically; prose rules that require judgment are not worth encoding.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part3.md [p165]
  rejected-alternative: encoding the full prose rulebook into the sharpening instrument
  endorsement: n/a
```

## Not converted

- A rulebook that is itself the product of blurring can still produce sharp outputs [p122-p123].
- Token dropping has legitimate uses (tool catalogs over 100 tools, shrinking WG21 papers) even though it is wrong for the author's own prompts [p117-p118].
- The author's prompt-writing practice: enter plan mode, state the goal, apply how-to-write-prompts.md, keep refining, ask for a review pass that tightens, then run [p156].
- Test your own prior before acting on it: verify that sharpening a sharply produced tool actually strips what you predicted it would strip [p158].
- A high-value, high-leverage audit warrants line-by-line comparison of original against sharpened output [p160].
- The prompt rulebook absorbs external influence (an Anthropic context-engineering blog post) and may drift ahead of older exemplars [p150].

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from collapse-fanout-arm engine plan review (arm unification, special-casing over extraction)
---

# 2026-08-19-0447-collapse-fanout-arm-review

```yaml
- statement: A fanout arm executes through the same code path and the same functions as normal flow; the only difference is that an arm receives extra inputs (taskid, item).
  scope: core
  source: user-corrective
  citation: 2026-08-19-0447-collapse-fanout-arm-review.md [p2]
  rejected-alternative: a separate arm-execution path with its own functions
  endorsement: n/a

- statement: When two flows differ only in minor details, unify them into one implementation and add small special-casing for the differences, rather than extracting a parallel implementation.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0447-collapse-fanout-arm-review.md [p3]
  rejected-alternative: extracting a separate implementation for the near-duplicate flow
  endorsement: n/a
```

## Not converted

- Plans are organized into discrete steps, each with tests, commit, review, fix, amend (development-process directive, not engine behavior).
- Each plan step includes a debt-reduction pass: a subagent reviews every modified file for duplicate code, simplification opportunities, and unused functions (development-process directive).
- Fix iterations are unlimited, but review iterations are capped (development-process directive).
- Tests are expected to pass at every commit (stated as an incredulous question, p7).

---

---
produced: 2026-08-19
title: PromptForge design principles mined from compaction-algorithm session part 1 (orchestrator, sections, tools, fanout)
---

# 2026-07-30-1046-compaction-algorithm-large-part1.md

```yaml
- statement: Structured results are assembled from a small set of tool calls rather than returned out of the model as a structured data object.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p13]
  rejected-alternative: passing Pydantic models out of the orchestrator, which routes every model call through an expensive guidance layer [p30]
  endorsement: n/a

- statement: The harness slices the input prompt into sections, each section carries a stable id, and the entry section is named "main".
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: The model advances the pipeline by invoking a tool call that discards the current context and starts a fresh context at another section, carrying forward the state accumulated by prior tool calls.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p14]
  rejected-alternative: multi-turn continuation within one growing context
  endorsement: n/a

- statement: A pipeline is a single markdown file executed by one general-purpose harness, so new pipelines are prototyped and iterated without writing new harness code.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p15]
  rejected-alternative: a bespoke coded pipeline per task shape
  endorsement: n/a

- statement: Model tier is selectable per step, so a pipeline can hop between model sizes from section to section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: Each section declares the tools it allows, keeping the per-step tool list small so the model does not get confused.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p17]
  rejected-alternative: exposing the full tool library at every step
  endorsement: n/a

- statement: Capabilities are added as new small tools in a library, and even harness-side processing such as dividing the input into sections can itself be exposed as a tool call.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p16] [p18]
  rejected-alternative: hardcoding processing steps into the harness
  endorsement: n/a

- statement: A prompt can spawn subagents to arbitrary nesting depth, guarded by a safety valve, so a prompt can subagent an algorithm that itself uses subagents.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: A subagent's prompt is referenced by section (for example Task("## Research")) and supplied verbatim by the harness, never regenerated by the orchestrator model, so the prompt cannot drift or be contaminated.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p20]
  rejected-alternative: the orchestrator model re-inventing the subagent prompt from its own interpretation
  endorsement: n/a

- statement: A section may carry an optional code fence of user-definable Lua that defines preconditions and inserts tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p25]
  rejected-alternative: none
  endorsement: n/a

- statement: Pipelines never block on mid-run user questions; where interaction is supported it happens through a runtime-level pattern gated by an explicit unattended/interactive mode toggle.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p41] [p43]
  rejected-alternative: AskQuestion-style mid-run prompting
  endorsement: n/a

- statement: Fanout is declared with markdown syntax that states "this is a fanout", with each spoke having its own prompt section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p44]
  rejected-alternative: enumerating fanout spokes as a flat bulleted list in one prompt
  endorsement: n/a

- statement: The harness provides an easy way to combine all fanout results into a single document, with the option of preserving order or not.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p46]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness offers virtual files through CreateFile, AppendFile, and DeleteFile tools backed by in-memory blobs, and the agent cannot tell they are not real files.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p46]
  rejected-alternative: writing intermediate results to real files on disk
  endorsement: n/a

- statement: Features are designed as specific examples of one general principle rather than as special cases.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p48]
  rejected-alternative: a collection of per-feature special cases
  endorsement: n/a
```

## Not converted

- [p19] Deeply nested task chains are debugged by making each subtask well tested and well defined - an engineering practice, not a language or engine directive.
- [p45] Putting the prompt itself in Lua as individual sections means the tool can write itself - an intriguing consequence, not a directive.
- [p12] "Dont code fence me" - a preference about assistant response style, not a system behavior.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from file-backed store execution unit (dev runner FileStore wiring)
---

# 2026-08-14-1612-file-backed-store-execution

```yaml
- statement: The dev runner derives the store path from the prompt file: same directory, same stem, no extension, as a subdirectory (prompts/research-person.md -> prompts/research-person/).
  scope: cli
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: none
  endorsement: n/a

- statement: Store path derivation is the dev runner's policy, not the engine's.
  scope: boundary: cli<->core
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: the engine owning store path policy
  endorsement: n/a

- statement: With a file-backed store, run state is already on disk, so no post-run dump or copy-out step is needed.
  scope: core
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: a post-run dump that reconciles an in-memory store out to disk
  endorsement: n/a

- statement: Library code propagates errors; it does not unwrap.
  scope: global
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: unwrap/expect in library code
  endorsement: n/a

- statement: New dependencies are not introduced to solve a problem.
  scope: global
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: pulling in a new crate
  endorsement: n/a
```

## Not converted

- Working-style preference: do not commit, leave changes in the worktree, and return a terse status (done or blocked, files touched, test command) under a tight token budget.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from the map-reduce synthesis chat unit
---

# 2026-07-30-0654-map-reduce-synthesis.md

```yaml
- statement: Fan-out dispatches parallel subagents, each in a fresh context, and merges their stores when they complete.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Model selection is per-section: a section's Lua block chooses the model slot that executes it.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Models are tiered by task weight, with small models assigned to mechanical work and a large driver model reserved for orchestration.
  scope: global
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Reduction over fan-out results begins on partial results as the first workers return, rather than blocking until every worker has finished.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [plans section]
  rejected-alternative: a wait-for-all barrier before the reduce step runs
  endorsement: affirmed

- statement: Pipeline stages that feed one another share a model family so that prompt caching survives across stage boundaries.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: Static instructions precede dynamic content in a prompt, and a section's preamble stays byte-stable, so the cacheable prefix is preserved.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: A section's output contract is ordinary markdown regardless of which model slot executes it; swapping the model behind a section does not change the section.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- The user worried whether a small fine-tuned reduce model can robustly handle inputs containing code fences and mixed languages (C++, JavaScript); a robustness concern raised as a question, never resolved into a directive [p8].
- Model sovereignty as a design goal: the design prefers self-hosted small models over frontier APIs for cost and speed independence; a philosophy, not a rule [design documents section].
- Report-craft preferences (inverted pyramid, inline hyperlinks, answer-first headings) govern the design documents PromptForge produces, not the language or engine itself [p2].

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 1 (sectioned prompts, tool-call orchestration, fanout, call semantics)
---

# 2026-08-02-1134-mcp-client-large-part1

```yaml
- statement: A pipeline is authored as a single markdown file executed by one general-purpose harness, so new pipelines are prototyped and iterated without writing new Python.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p15]
  rejected-alternative: a bespoke hand-written Python pipeline per task (the assay approach)
  endorsement: n/a

- statement: A prompt is divided into sections, each with a stable id, and the entry section is named "main".
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: The model moves between sections through a tool call that discards the current context and starts a fresh context at the target section, while state accumulated through earlier tool calls persists.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p14]
  rejected-alternative: carrying one growing context through the whole pipeline
  endorsement: n/a

- statement: Structured results are assembled by giving the model a small set of tool calls that build the data, not by passing a schema object out of the orchestrator.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p13], [p30]
  rejected-alternative: routing every model call through a Pydantic validation layer
  endorsement: n/a

- statement: The model tier is chosen per step, so one pipeline can hop between model sizes across its sections.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: Each section declares the tools it allows, keeping the exposed tool list small so the model is not confused.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p17]
  rejected-alternative: exposing the full tool set to every section
  endorsement: n/a

- statement: A prompt can spawn a subagent, and a subagent can spawn further subagents to arbitrary nesting depth, bounded by a safety valve.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: A subagent's prompt is referenced by section (Task("## Research")) rather than passed as model-written text, so the prompt comes from the file and the orchestrator cannot drift or contaminate it.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p20]
  rejected-alternative: the orchestrator re-inventing the subagent prompt from its own interpretation
  endorsement: n/a

- statement: A section may carry an optional block of user-defined embedded code that sets preconditions and injects tools.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p25], [p45]
  rejected-alternative: none
  endorsement: n/a

- statement: Pipelines never ask the user questions mid-run; interaction, when needed, goes through a runtime-level pattern governed by an unattended/interactive mode toggle.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p41], [p43]
  rejected-alternative: AskQuestion-style interactive prompts inside a pipeline
  endorsement: n/a

- statement: The language has markdown syntax that declares a fanout in which each spoke is its own section with its own prompt.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p44]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness provides an operation that combines all fanout results into a single document, with the option to preserve spoke order or not.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p46]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness offers virtual files - create, append, and delete operations over in-memory blobs that the agent treats as real files.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p46]
  rejected-alternative: giving the agent real filesystem access
  endorsement: n/a

- statement: The basic unit of operation is the function: an inference that takes structured key-value inputs and returns a string, and may have side effects.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p65]
  rejected-alternative: none
  endorsement: n/a

- statement: Every section is a function that accepts exactly one string, supplied by the node that transfers control to it, and returns a string.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p65]
  rejected-alternative: sections taking structured key-value inputs like top-level prompts
  endorsement: n/a

- statement: There is exactly one control-transfer tool, call, whose first parameter selects the transfer type: goto, function call, context-preserving goto, or return.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p65]
  rejected-alternative: a separate tool per transfer type
  endorsement: n/a

- statement: A control transfer carries a string payload to its destination, where it becomes the beginning of the destination's prompt or is first manipulated by the destination's embedded code.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part1.md [p65]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- Deeply nested task chains stay debuggable when each subtask is well tested and well defined. [p19]
- Open question: how the tool-call approach to structured output recognizes failure modes the way Pydantic does. [p24]
- A tool can write itself when its prompt lives in embedded code as individual sections. [p45]
- Most feature requests are specific examples of a few general principles. [p48]
- A design document should be richly detailed enough for any frontier model to produce working code including tests. [p37]
- Compaction with prompt re-injection belongs to the Mentographist app, not this system; the user explicitly separated the two. [p15], [p31]
- The detour on running an unmodified prompt by passing it whole to one model was explicitly excluded from the plan. [p51], [p54]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from orchestrator design continued chat (sections, goto, tool-call state, bindings, gateway, MCP)
---

# 2026-07-28-2238-orchestrator-design-continued.md

```yaml
- statement: Every prompt is a single markdown file and one function - it takes well-defined parameters declared in machine-readable YAML front matter (readable, read-only, from every section) and returns a string, and may also produce side effects through tools.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p65, p117, p74]
  rejected-alternative: none
  endorsement: n/a

- statement: PromptForge starts with the prompt and adds structured programming (Lua) into it; a prompt with zero Lua still works as a plain orchestration, so Lua is additive, never required.
  scope: global
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p118]
  rejected-alternative: host-language-first frameworks (Python, Go) with prompts bolted on
  endorsement: n/a

- statement: One generic fixed harness runs any pipeline of the same shape; orchestration logic, prompt assembly, and step ordering live in the markdown, never in the harness, so a new pipeline is a new markdown file rather than new orchestration code.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p15, plans section]
  rejected-alternative: a hardcoded per-pipeline orchestration program
  endorsement: n/a

- statement: A prompt is sliced into sections with stable ids addressable by the harness, and the entry section is named main.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: A context-clearing transition (goto) destroys the current context and starts fresh from the target section's prompt with only the passed string, params, and state-store access.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p14, p75, p120]
  rejected-alternative: carrying or compacting accumulated context across steps
  endorsement: n/a

- statement: Falling through to the next section is the default control flow and is context-clearing; running off the last section ends the run with a default message that the YAML front matter can override.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p75, p121]
  rejected-alternative: requiring an explicit exit or transition from every section
  endorsement: n/a

- statement: Control transfer is three primitives - call (preserving context, returns to caller), task (fresh-context subagent, returns a result), goto (non-returning, clears context) - which may collapse into a single tool with a mode parameter if small models cannot handle multiple control-flow tools.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p65, p120]
  rejected-alternative: none
  endorsement: n/a

- statement: Both Lua and the model can initiate control transfer; deterministic routing lives in Lua while the model routes when multi-turn judgment is required, such as guided web search.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p66]
  rejected-alternative: restricting control flow to only the model or only the scripting layer
  endorsement: n/a

- statement: State is built incrementally through a small set of tool calls with flat argument signatures, not by passing structured output out of the model.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p13, plans section]
  rejected-alternative: Pydantic-style structured output routed through a conformance layer with injected guidance
  endorsement: n/a

- statement: The executor substitutes Lua state into prompt text by name, so structured return values are assembled deterministically in Lua and returned via substitution rather than emitted by the model.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p66, p78]
  rejected-alternative: model-conformant JSON produced under constrained decoding
  endorsement: n/a

- statement: Each section declares its allowed tools and the model sees only the few it needs (roughly 5-10), keeping small orchestrator models reliable.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p17, p85, p119]
  rejected-alternative: exposing the prompt's full tool set to every section
  endorsement: n/a

- statement: Subagent dispatch references a section by id (for example "## Research") and the runtime supplies that section's exact text as the subagent prompt; the model never paraphrases or reconstructs subagent instructions, so there is no prompt drift or contamination.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p20, plans section]
  rejected-alternative: the orchestrator model composing the subagent prompt itself
  endorsement: n/a

- statement: A prompt can spawn subagents to arbitrary nesting depth - a subagent may itself use subagents - bounded by a configurable safety valve on depth and total tasks.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p18, plans section]
  rejected-alternative: none
  endorsement: n/a

- statement: Markdown syntax declares a fanout in which each spoke (an H3 child section) has its own prompt, and the harness provides a way to combine all fanout results into a single document with optional order preservation.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p44, p46]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness offers virtual file tools (create, append, read, delete) backed by in-memory blobs rather than real files; the agent cannot tell the difference.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p46]
  rejected-alternative: giving pipeline agents direct access to the real filesystem
  endorsement: n/a

- statement: Model tier is selectable per section, so a pipeline can hop between model sizes (for example a large orchestrator and small extraction or verification models) step by step.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p16, plans section]
  rejected-alternative: one fixed model for the whole pipeline
  endorsement: n/a

- statement: Prompts operate in a semantic space of abstract tools (add claim, remove claim) that know nothing about storage; a per-prompt bindings file maps each abstract tool to a concrete implementation, the schema attaches to the tool rather than the prompt so shared tools are specified once, and backends are never hardcoded into tools.
  scope: boundary: prompt<->bindings
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p88, p90]
  rejected-alternative: tools with built-in database knowledge and per-prompt schema repetition
  endorsement: n/a

- statement: The harness discovers a prompt's required tools by parsing and stub-running its Lua and intercepting tool registration (Lua exposes only a fixed set of host objects, no arbitrary user globals); loading fails with an error on any missing binding, and a command can emit an empty bindings template listing every discovered tool for the user to fill in.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p71, p89, p91, p95]
  rejected-alternative: declaring tool lists in YAML front matter
  endorsement: n/a

- statement: All inference traffic bottlenecks through a single gateway process that enforces global concurrency limits across all apps, languages, and machines; loopback connections need no API key while remote access uses whitelisted IPs or API keys.
  scope: gateway
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p116]
  rejected-alternative: each application managing its own inference concurrency
  endorsement: n/a

- statement: Any prompt can be exported as an MCP tool purely from its YAML front matter (parameters plus description); the server watches the prompt directory and refreshes its cache without restart, and the server can itself act as an MCP client to other services.
  scope: mcp
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p122]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- Recursive transcript compaction (halving cycles, prompt reinjection, pre-compaction at 90% capacity, full transcript persisted): a Mentographist algorithm, explicitly declared unrelated to the orchestrator.
- Evaluate every design choice by whether it relieves context-window pressure so smaller models suffice: a design heuristic, not a behavior of the language or engine.
- Open-weight model tier economics and "this runs at scale, not on macbooks": deployment posture, not language design.
- Interactive prompts (AskQuestion) have no place in these pipelines: a pipeline-authoring convention rather than an engine behavior.
- Tranche-based plan implementation (implement a subset, subtract it, plan the next) and research-before-writing report workflow: process guidance, not PromptForge design.
- "Don't code fence me": chat output-formatting preference.

---

# 2026-08-09-1058-promptforge-core-large-part3.md

```yaml
- statement: Context values injected into a prompt can be marked as untrusted input, and data joined from web fetches must be treated as untrusted.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p159, p161]
  rejected-alternative: none
  endorsement: n/a

- statement: The store is not a raw file system dump; intermediate run artifacts must not surface as stray user-visible files.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p162]
  rejected-alternative: a store that is literally the file system, emitting files like evidence.md as side effects
  endorsement: n/a

- statement: A run deletes all of its trace files on launch.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p165]
  rejected-alternative: none
  endorsement: n/a

- statement: When fetched evidence is unusable, the whole run aborts rather than continuing, because a hallucinated evidence packet taints the entire downstream result.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p173, p174]
  rejected-alternative: continuing the run with an empty or failed evidence packet
  endorsement: n/a

- statement: Turn limits are a property of the subagent's own configuration (e.g. config.max_turns(8)), not of individual tools.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p175]
  rejected-alternative: per-tool max_turns settings
  endorsement: n/a

- statement: When a subagent's budget is exhausted, all of its tools are taken away.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p176]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool matching is semantic and must not depend on matching the tool description verbatim.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p193]
  rejected-alternative: verbatim string matching against tool descriptions
  endorsement: n/a

- statement: Integration tests do not launch the gateway; they require that the gateway is already running and already holds the configuration it needs.
  scope: boundary: tests<->gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p201]
  rejected-alternative: tests spawning their own gateway instance
  endorsement: n/a

- statement: A small local model is kept runnable without the gateway, so integration tests can exercise real inference and expand the testing surface without the bulk of spawning the gateway.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p202]
  rejected-alternative: requiring the gateway for every inference-level test
  endorsement: n/a

- statement: Every user-facing crate carries its own documentation: a README.md in the crate root with full, friendly instructions, plus a design.md explaining the design choices.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p204]
  rejected-alternative: none
  endorsement: n/a

- statement: Model requirements such as minimum context size and no_think are properties of the prompt, declared by the prompt itself, not command-line flags.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p205, p206]
  rejected-alternative: passing context_max_tokens and no_think on the command line
  endorsement: n/a

- statement: Configuration is organized as a hierarchy of TOML files in which a common base file is inherited by model-specific files.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p220, p221, p222]
  rejected-alternative: none
  endorsement: n/a

- statement: Stale cache files are cleaned up rather than left in place.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p223]
  rejected-alternative: none
  endorsement: n/a

- statement: Long-running operations such as multi-gigabyte model downloads display graphical progress: a bar, a spinner, and a percentage.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p233, p235]
  rejected-alternative: silent downloads with no progress indication
  endorsement: n/a

- statement: The program that puts a prompt into dev mode lives in its own crate, separate from the simplified test crate.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p203, p204]
  rejected-alternative: folding dev mode into the test crate
  endorsement: n/a
```

## Not converted

- An untrustworthy model is useless no matter its size; frustration that a 27B-parameter model hallucinates (p244).
- Empirical observation that the smaller model outperformed the larger one on the briefer task (p243).
- Curiosity about load times for trillion-parameter models on a Blackwell B300 rack (p186).
- Adding temperature floated as a tuning lever for search behavior (p179).
- Open question of how to close the output-quality gap with the current model (p190).

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge-core largest session part 3 (config inheritance, tool-call dialects, epilogue assertions, write-through runs, concurrency)
---

# 2026-08-14-1613-promptforge-core-largest-part3

```yaml
- statement: Model configuration forms an inheritance hierarchy: a shared common config is inherited by per-model config files.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p220], [p221], [p222]
  rejected-alternative: none
  endorsement: n/a

- statement: A shared config never mentions specific models; model-specific settings live only in that model's own config file.
  scope: gateway
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p309], [p310]
  rejected-alternative: naming qwen or gemma inside common.toml
  endorsement: n/a

- statement: Stale cache files are cleaned up automatically rather than left behind.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p223]
  rejected-alternative: none
  endorsement: n/a

- statement: Long-running operations such as a multi-gigabyte model download show live graphical progress: a bar, a spinner, and a percentage.
  scope: cli
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p233], [p235]
  rejected-alternative: none
  endorsement: n/a

- statement: Per-model tool-call formats are normalized behind an abstraction layer, so a prompt never contains model-specific tool-call syntax and the same prompt works for all models.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p250]
  rejected-alternative: hardcoding model-specific tool-call formats into the prompt itself
  endorsement: n/a

- statement: Behavior that varies by model lives behind abstract interfaces; nothing model-specific is hardcoded.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p250], [p253]
  rejected-alternative: hardcoded per-model special cases
  endorsement: n/a

- statement: Adding a model never requires the operator to specify its tool-call dialect; the system discovers the dialect itself, for example from the model's card.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p253]
  rejected-alternative: operator-set dialect per added model
  endorsement: n/a

- statement: Each tool-call dialect is a self-contained pluggable module, one source file per dialect, so dialects can be added or cribbed from existing code without touching the rest.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p254]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt can assert postconditions on tool usage in its epilogue, such as requiring that a named tool was called at least once.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p265], [p266]
  rejected-alternative: none
  endorsement: n/a

- statement: Do more with less: prefer expressing behavior through an existing general mechanism over adding a dedicated construct.
  scope: global
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p267]
  rejected-alternative: a dedicated require_called directive
  endorsement: n/a

- statement: Tool-call assertion counts are scoped per VM, not global to the run.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p268]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool-call assertions measure whether the model performed, not whether the tool succeeded; a failed tool call still counts as a call.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p271]
  rejected-alternative: counting only successful tool calls
  endorsement: n/a

- statement: Referencing an unknown tool alias is a hard error with a clear diagnostic.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p271]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool references are scoped; naming a global tool without its scope is a hard error.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p272], [p273]
  rejected-alternative: resolving names against a flat "registered" set
  endorsement: n/a

- statement: An assertion failure in a prompt reports the source file and line number.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p279], [p280], [p313]
  rejected-alternative: assertion failures without source locations
  endorsement: n/a

- statement: Run artifacts are written through as they are produced, turn by turn, not buffered and dumped at the end of the run.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p290], [p298], [p299]
  rejected-alternative: waiting to write all the JSON turn files at the end
  endorsement: n/a

- statement: Fanout executes its arms concurrently.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p311], [p312]
  rejected-alternative: none
  endorsement: n/a

- statement: Execution concurrency is a per-model configuration value, tuned per model.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p305], [p306], [p307]
  rejected-alternative: a single global concurrency setting
  endorsement: n/a

- statement: Interrupting with Ctrl+C cancels a concurrent run cleanly.
  scope: cli
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p317], [p318]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt must not smuggle bias into its criteria; evaluation wording stays neutral toward outcomes.
  scope: global
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p325], [p326]
  rejected-alternative: criteria worded to favor non-profits instead of neutral phrasing like "corporate filings"
  endorsement: n/a
```

## Not converted

- [p244] A model that hallucinates is useless no matter its size; trust in the model's output is the whole point (temperament about model quality, not an engine directive).
- [p249], [p250] Frustration that tool-calling is a model's one job; the urgency behind the normalization layer, already captured as a candidate.
- [p319], [p320], [p321] Iterative prompt-tuning methodology: stage quality targets against a baseline, log what works and what does not, roll back anything that regresses, minimize agent turns, and stop after three rounds without improvement (a practice, not a rule of the language or engine).
- [p255] Preference for asynchronous background research while prompting continues (agent workflow, not PromptForge behavior).

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge.md Aug 18 afternoon session (empty-turn policy, tool-loop exit, MCP env loading, gateway parity)
---

# 2026-08-18-1639-promptforge-md-aug18-afternoon

```yaml
- statement: Tool calls made during a prose tool loop count as output; the model is not required to spend tokens on filler text such as "done" to close the loop.
  scope: core
  source: user-stated
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p3]
  rejected-alternative: requiring a non-empty text reply to validate a turn
  endorsement: n/a

- statement: A tool loop that ends with an empty-text turn is a clean exit, not an error, when at least one tool call was made during the loop.
  scope: core
  source: user-stated
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p6]
  rejected-alternative: treating every empty model reply as an EmptyModelReply error
  endorsement: n/a

- statement: The empty-turn clean exit applies only when finish_reason is "stop" and at least one tool call was successfully dispatched earlier in the loop; empty turns with a missing or non-stop finish reason fail closed as EmptyModelReply.
  scope: core
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section]
  rejected-alternative: accepting any empty turn once a tool call has occurred
  endorsement: affirmed

- statement: Empty-turn acceptance is default behavior with no opt-in flag, and an accepted empty exit binds reply to the empty string.
  scope: core
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section]
  rejected-alternative: an opt-in flag or configuration setting
  endorsement: affirmed

- statement: The MCP server loads the name-matched .env file beside its config, working just like the gateway, so no manual environment sourcing is needed at startup.
  scope: mcp
  source: user-stated
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p7]
  rejected-alternative: requiring manual env sourcing before server startup
  endorsement: n/a

- statement: Environment variable precedence in the MCP server matches the gateway: the process environment wins and the env file supplies defaults.
  scope: boundary: gateway<->mcp
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section]
  rejected-alternative: env file overriding the process environment
  endorsement: affirmed

- statement: Env-file values loaded by the MCP server never leak into the process environment; they are held in memory only.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section]
  rejected-alternative: mutating the process environment (unsafe under Rust edition 2024)
  endorsement: affirmed

- statement: Hot-reloading the MCP server config also picks up changes to the name-matched env file, with no separate reload path.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section]
  rejected-alternative: none
  endorsement: affirmed
```

## Not converted

- [p5] A prose section whose last turn emits a tool call loops back into inference - the user's surprise at discovering existing loop behavior, not a directive.
- [plans section, out of scope] Outbound history serializes assistant tool turns as `"content": ""`; left as-is through the gateway until it actually breaks - a deferred fix, not a behavioral directive.
- [p10], [p12] Model thinking-level selection (Kimi K3 Low vs High vs Max) - operational tuning question, not a PromptForge design principle.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from recover-core-design-rationale session (autonomous plans, system-organized design documents, uncertainty-to-prose rule)
---

# 2026-08-04-1426-recover-core-design-rationale

```yaml
- statement: A plan executes fully autonomously; it must never use AskQuestion or otherwise pause for user interaction.
  scope: global
  source: user-corrective
  citation: 2026-08-04-1426-recover-core-design-rationale.md [p4]
  rejected-alternative: interactive plans that stop to ask the user questions mid-run
  endorsement: n/a

- statement: A recovered design document is organized by the system, not by the evidence ledger; the ledger is consulted as evidence and never transcribed, and a document a reader could rebuild by rewording the ledger row by row has failed.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: a per-record document that recites each ledger verdict with record IDs attached
  endorsement: unaddressed

- statement: Uncertainty is spent only where a reader can act on it: a reason the code forced is stated as fact, an unsettled reason the reader cannot act on is omitted silently, and an unsettled reason a reader could build on gets one explicit warning sentence.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: labeling every open element as open throughout the document
  endorsement: unaddressed

- statement: A design document body carries no record identifiers and no verdict vocabulary; the ledger is the committed audit trail and the evidence ratio is reported by a separate step.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: tracing every claim to a record ID inside the document prose
  endorsement: unaddressed

- statement: An unconfirmed archive proposal never becomes rationale in the document; a reason is stated only where the code forced it or the author confirmed it.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: promoting unanswered adjudication proposals into stated design rationale
  endorsement: unaddressed

- statement: Recovery stays blind to the existing design document, so the recovered document is independent and the two can be compared.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: letting the recovery read the prior design document as a reference
  endorsement: unaddressed

- statement: Deferred adjudication is a clean outcome, not a failure: the run proceeds on the settled ledger with no proposal applied and no verdict moved, and the deferral measures what code and archive recover without a human.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: blocking the run until every adjudication batch is answered
  endorsement: unaddressed

- statement: Shape authority lives in one general block; step-level instructions narrow it but never override it, because a specific instruction beats a general one when they conflict.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: per-step mandates that restate and displace the general document spec
  endorsement: unaddressed

- statement: A plan never hard-codes values from a previous run; run-specific counts are written in run-independent phrasing so the plan's structure does not depend on one run's exact numbers.
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: baking the last run's exact record count into the plan text
  endorsement: unaddressed

- statement: Review checks for a generated document are document-level (could a reader who never saw the evidence learn how the system works) rather than record-level (does every claim trace to a record).
  scope: core
  source: ai-proposed
  citation: 2026-08-04-1426-recover-core-design-rationale.md [plans section]
  rejected-alternative: review checks that demand per-record traceability in the prose
  endorsement: unaddressed
```

## Not converted

- "This is a stinking pile of shit" [p2] - the user delivers blunt quality verdicts without criteria; the defect and fix direction must be inferred from the artifact.
- The plan's document-shape principles were never explicitly endorsed in this unit; the only user correction after the plan targeted its use of AskQuestion [p4].
