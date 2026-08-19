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
- statement: Capabilities are added as new small tools in a library, and even harness-side processing such as dividing the input into sections can itself be exposed as a tool call.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p16] [p18]
  rejected-alternative: hardcoding processing steps into the harness
  endorsement: n/a

- statement: A section may carry an optional code fence of user-definable Lua that defines preconditions and inserts tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p25]; 2026-08-02-1134-mcp-client-large-part1.md [p25], [p45]
  rejected-alternative: none
  endorsement: n/a

- statement: Pipelines never block on mid-run user questions; where interaction is supported it happens through a runtime-level pattern gated by an explicit unattended/interactive mode toggle.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part1.md [p41] [p43]; 2026-08-02-1134-mcp-client-large-part1.md [p41], [p43]
  rejected-alternative: AskQuestion-style mid-run prompting
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
  citation: 2026-07-30-0654-map-reduce-synthesis.md [design documents section]; 2026-07-28-2238-orchestrator-design-continued.md [p16, plans section]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p16]; 2026-08-02-1134-mcp-client-large-part1.md [p16]
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
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p65, p117, p74]; 2026-08-02-1134-mcp-client-large-part5.md [p410]
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
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p15, plans section]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p15]; 2026-08-02-1134-mcp-client-large-part1.md [p15]; 2026-08-02-1134-mcp-client-large-part5.md [plans: orchestrator design document]
  rejected-alternative: a hardcoded per-pipeline orchestration program
  endorsement: n/a

- statement: A prompt is sliced into sections with stable ids addressable by the harness, and the entry section is named main.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p14]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p14]; 2026-08-02-1134-mcp-client-large-part1.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: A context-clearing transition (goto) destroys the current context and starts fresh from the target section's prompt with only the passed string, params, and state-store access.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p14, p75, p120]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p14]; 2026-08-02-1134-mcp-client-large-part1.md [p14]
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
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p13, plans section]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p13]; 2026-08-02-1134-mcp-client-large-part1.md [p13], [p30]
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
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p17, p85, p119]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p17]; 2026-08-02-1134-mcp-client-large-part1.md [p17]
  rejected-alternative: exposing the prompt's full tool set to every section
  endorsement: n/a

- statement: Subagent dispatch references a section by id (for example "## Research") and the runtime supplies that section's exact text as the subagent prompt; the model never paraphrases or reconstructs subagent instructions, so there is no prompt drift or contamination.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p20, plans section]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p20]; 2026-08-02-1134-mcp-client-large-part1.md [p20]
  rejected-alternative: the orchestrator model composing the subagent prompt itself
  endorsement: n/a

- statement: A prompt can spawn subagents to arbitrary nesting depth - a subagent may itself use subagents - bounded by a configurable safety valve on depth and total tasks.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p18, plans section]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p18]; 2026-08-02-1134-mcp-client-large-part1.md [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: Markdown syntax declares a fanout in which each spoke (an H3 child section) has its own prompt, and the harness provides a way to combine all fanout results into a single document with optional order preservation.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p44, p46]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p44] [p46]; 2026-08-02-1134-mcp-client-large-part1.md [p44] [p46]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness offers virtual file tools (create, append, read, delete) backed by in-memory blobs rather than real files; the agent cannot tell the difference.
  scope: core
  source: user-stated
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p46]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p46]; 2026-08-02-1134-mcp-client-large-part1.md [p46]
  rejected-alternative: giving pipeline agents direct access to the real filesystem
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
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p116]; 2026-08-08-1223-gateway-local-inference.md [p16], 2026-08-02-1134-mcp-client-large-part3.md [p211]
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
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p220, p221, p222]; 2026-08-14-1613-promptforge-core-largest-part3.md [p220], [p221], [p222]
  rejected-alternative: none
  endorsement: n/a

- statement: Long-running operations such as multi-gigabyte model downloads display graphical progress: a bar, a spinner, and a percentage.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p233, p235]; 2026-08-14-1613-promptforge-core-largest-part3.md [p233], [p235]
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
- statement: A shared config never mentions specific models; model-specific settings live only in that model's own config file.
  scope: gateway
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p309], [p310]
  rejected-alternative: naming qwen or gemma inside common.toml
  endorsement: n/a

- statement: Stale cache files are cleaned up automatically rather than left behind.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p223]; 2026-08-09-1058-promptforge-core-large-part3.md [p223]
  rejected-alternative: none
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

- statement: Run artifacts are written through as they are produced, turn by turn, not buffered and dumped at the end of the run.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part3.md [p290], [p298], [p299]; 2026-08-14-1612-file-backed-store-execution.md [p3]
  rejected-alternative: waiting to write all the JSON turn files at the end
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

- statement: The empty-turn clean exit applies only when finish_reason is "stop" and at least one tool call was successfully dispatched earlier in the loop; empty turns with a missing or non-stop finish reason fail closed as EmptyModelReply.
  scope: core
  source: ai-proposed
  citation: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [plans section], [p6]
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

---

---
produced: 2026-08-19
title: PromptForge design principles mined from architect-vibe-planning part 4 (semantic blur, sharpen instrument, dataset gates)
---

# 2026-07-28-0207-architect-vibe-planning-part4.md

```yaml
- statement: An agent handed a bounded research task plans the work, forms hypotheses, runs the experiments, and returns clean results without checking in.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p175]
  rejected-alternative: none
  endorsement: n/a

- statement: A plan must be standalone: a fresh context can load it and resume the work with no prior state.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p176]
  rejected-alternative: none
  endorsement: n/a

- statement: An experiment log is append-only; each experiment records hypothesis, method, results, finding, and commit hash, with a git commit at every checkpoint, so the log is the reload point for a fresh context.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p176]
  rejected-alternative: none
  endorsement: n/a

- statement: Build training pairs by degrading a known-sharp target, never by sharpening a raw bloated input; raw bloat carries off-topic content that would teach the model relevance judgments.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p197]
  rejected-alternative: (raw bloated plan, sharpened plan) pairs
  endorsement: n/a

- statement: Blur is produced by the model's natural resampling; never steer the model toward bloat.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p198]
  rejected-alternative: steering the model into bloating
  endorsement: n/a

- statement: Crisp instructions survive blur because a reword converges back to execution semantics; descriptive prose drifts because its language is interpretive.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p200]
  rejected-alternative: none
  endorsement: n/a

- statement: Attach the rationale to every rule; the model generalizes from the reason, while a bare rule is pattern-matched and leaves the model hallucinating when the input does not perfectly match.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p204], [p214]
  rejected-alternative: reasonless rules, and the "escape hatch" framing in place of a rationale
  endorsement: n/a

- statement: Each concept is referred to by one name, not more.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p205]
  rejected-alternative: the ambiguous phrasing "One term names each concept"
  endorsement: n/a

- statement: A sharpening instrument aligns the model generally; it does not prescribe task-specific diagnostic algorithms.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p216]
  rejected-alternative: including the analytical-framework cluster in the sharpener
  endorsement: n/a

- statement: Datasets built from different sources are kept distinct from each other, each with its own experiment log.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p188]
  rejected-alternative: none
  endorsement: n/a
```
```yaml
- statement: The plan is the source of truth; a design that changes is regenerated from an updated plan, never patched in place.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: patching the generated document in place
  endorsement: affirmed

- statement: The non-expansion guarantee is enforced mechanically outside the model; the guardrail's worst case is returning the input verbatim.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: trusting the model to enforce its own length limit
  endorsement: affirmed

- statement: A compression pair is kept only when no model would behave differently following the compressed text instead of the original (execution-equivalence).
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: A quality gate is validated with negative controls; a gate that cannot fail is worthless, the same trap as a test that cannot fail.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: The meaning gate is directional, blurred input to sharp target, because a specific dropped by the blur would otherwise train the compressor to hallucinate.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: A compressor only cuts; it never adds a specific that is absent from the source.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: bundling add-rigor rules (quantify every quantity, define the empty case) into a compressor
  endorsement: affirmed

- statement: Blur is irreversible from within the regeneration chain; the training target must be the true pre-blur original, never a re-sharpened blur.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: re-sharpening a blurred text to recover the original
  endorsement: affirmed

- statement: A blurred document is fixed by hand with targeted, non-regenerative edits; regeneration is the blur.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p223]
  rejected-alternative: fixing blur by regenerating or rebuilding the document
  endorsement: n/a

- statement: Ship the sharp-enough and stop regenerating; an ambiguity audit has no fixed point, and chasing perfection is the blur trap applied to process.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: one more tightening pass
  endorsement: affirmed

- statement: A gate that catches nothing beyond another gate is redundant cost; keep the one gate that discriminates.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: running both Gate 1 and Gate 2
  endorsement: affirmed
```

## Not converted

- Small models carry a narrow vocabulary; vocabulary lives in pretraining, not in the fine-tune set. [p184]
- Before trusting the model's judgment, the user asks it to rate its own confidence. [p187]
- Early hypothesis that blur is near-lossless; measurement disproved it, a single pass drops or alters a specific in 43-54% of cases. [p199]
- The user interrogates every phrase of the rulebook; no wording survives unexamined. [p208], [p209], [p211], [p219]
- The endeavor keeps living out its own thesis: every tightening pass regenerates the disease it studies. [p220], [p221]
- A report about bloat that is itself bloated fails on contact. [plans section]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from dokuman each-crate session (execution model, Lua sandbox, fanout, SSRF boundary)
---

# 2026-08-12-1534-dokuman-each-crate

```yaml
- statement: Execution is a free function over caller-owned resources; the engine holds no global state.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md], 2026-08-02-1134-mcp-client-large-part3.md [p215]
  rejected-alternative: engine-owned global state shared across runs
  endorsement: unaddressed

- statement: The H1 section resolves first, then H2 sections execute top to bottom.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: A prompt is a single Markdown file: YAML frontmatter for metadata, embedded Lua for logic, and prose blocks for model instructions.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: Fanout maps a worker section over a list section, running the arms in parallel with isolated state per arm.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: fanout arms that share mutable state
  endorsement: unaddressed

- statement: The result of a run is a string.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The web fetch tool enforces an SSRF boundary on the pages it retrieves.
  scope: boundary: webfetch<->web
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md, CHANGELOG.md]
  rejected-alternative: unrestricted outbound fetching
  endorsement: unaddressed
```

## Not converted

- Assembling the combined user guide should be a program that does one thing, not a prompt. (Excluded as a technology choice for repo tooling, not a language or engine behavior.) [p5]
- Stating a fact is not a request: the user stopped the agent for making unrequested changes after being told only that cppa uses Jekyll. [p23], [p24], [p25]
- Generated documentation belongs in the crate it documents, overriding default output routing. [p1], [p2]
- Git history should be kept clean: rewrite out a revert commit and the commit it reverts rather than layering corrections. [p29], [p30]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from gateway local-inference session (gateway centrality, profiles, devices, queuing, no-defaults, sys.model)
---

# 2026-08-08-1223-gateway-local-inference

```yaml
- statement: The executor never knows whether a model is local or remote; it just talks to the gateway.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p16], [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway is configured from one centralized file that lists every model, and a model entry may carry the URL where its weights are downloaded on demand.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: Model download and caching live in the gateway, never in the core or the test harness; callers and tests supply only configuration naming the source URL and pin.
  scope: boundary: core<->gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p41], [p42]
  rejected-alternative: core tests standing up llama-server and fetching GGUF weights themselves
  endorsement: n/a

- statement: The gateway multiplexes many competing callers onto shared inference hardware and owns the queue and the concurrency limits, so a prompt can fan out fifty wide and the gateway interleaves the callers.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p18]
  rejected-alternative: building concurrency limits into the prompt executor
  endorsement: n/a

- statement: Concurrency limits attach to hardware devices, not to models; the configuration lets an admin group the models and endpoints that share one physical device (a local card, a specific run pod) under a single limit.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p25]
  rejected-alternative: per-model limits
  endorsement: n/a

- statement: Gateway configuration is organized into named profiles, each a complete package of models and settings sized to fit the hardware and suited to a specific workflow; the gateway runs exactly one profile at a time.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p35]
  rejected-alternative: one general-purpose configuration holding every model at once
  endorsement: n/a

- statement: Profiles can be switched at runtime through a remote admin command, so a batch script can reconfigure the gateway for a workload before running its prompts.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p35]
  rejected-alternative: none
  endorsement: n/a

- statement: Profile switching is immediate, not graceful: in-flight local requests are dropped, because the local machine has a single operator who knows what they are doing.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: graceful drain of in-flight requests before switching
  endorsement: n/a

- statement: A profile can inherit another profile recursively, like include files.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway never auto-selects a profile; the operator names the profile explicitly.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: auto-selecting a profile
  endorsement: n/a

- statement: Small utility models (embeddings, classifiers, rerankers) are co-located with the gateway rather than called over a network, and they may run on CPU where that is enough.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p19], [p20], [p21]
  rejected-alternative: serving utility models from a remote endpoint
  endorsement: n/a

- statement: No defaults, everything explicit: every prompt declares the model it needs, or explicitly says it accepts anything, and at minimum states its required context and whether it needs thinking; implicit configuration is the enemy of precision.
  scope: global
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p58], [p60], [p62], 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p66]
  rejected-alternative: DEFAULT_MODEL and PROMPTFORGE_MODEL environment-variable fallbacks
  endorsement: n/a

- statement: The effective model name is exposed to the prompt as sys.model, usable in prose substitution and in Lua, so a report can footer itself with the model that produced it without hardcoding.
  scope: core
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p54]
  rejected-alternative: none
  endorsement: n/a

- statement: sys.model is unavailable during the prologue (the H1 Lua block); it exists only after the section's model scope closes, so the epilog is its intended consumer.
  scope: core
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p55]
  rejected-alternative: putting model in the initial pre-preamble sys object, which would miss section-local models.use
  endorsement: n/a

- statement: Within a local device, concurrency is divided into named lanes so a fast utility model is never queued behind a long generative call, while two generative calls still cannot run simultaneously.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: one flat concurrency limit per local device
  endorsement: unaddressed

- statement: Queued requests are scheduled fairly across callers, round-robin, so no single caller starves the others.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: When the gateway queue is full, it rejects requests immediately with backpressure (HTTP 503) rather than queueing without bound; the executor retries or reports failure.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: unbounded queueing
  endorsement: unaddressed

- statement: When the active profile changes, the model catalog changes with it, and any bindings cached in an executor are stale; the executor must re-fetch the catalog on its next run.
  scope: boundary: core<->gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- The gateway executable may be as big as it needs to be; operational simplicity beats binary size [p16].
- The author works through an AI-driven workflow and feels layers of software between operator and machine; the design should collapse those layers [p16].
- Quantization quality bar: "Q4 sounds terrible" - skepticism toward heavy quantization for serious work [p4].
- GPU support must not be forced on anyone; a machine without CUDA still gets a working gateway [p46] - excluded as a build/technology choice, kept as a sensibility note.
- Build order preference: easiest and most useful first, hardest and most risky last [p38].
- Review process preference: exactly one round of review, edits made in the review context, because further rounds keep finding things forever [p45].
- Deadline temperament: "you will get it done in 2 hours" [p40].

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 3 (prompt file format, call syntax, per-section tool restriction, gateway proxy, logical model routing)
---

# 2026-08-02-1134-mcp-client-large-part3

```yaml
- statement: A prompt file is markdown with YAML frontmatter, an H1 title, human-readable text, and headed sections that nest recursively from H2 through H6.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p137]-[p144]
  rejected-alternative: none
  endorsement: n/a

- statement: Model sessions come in both streaming and non-streaming forms, because downstream consumers (talktron) need a streaming session.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p170]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p170], [p171]
  rejected-alternative: none
  endorsement: n/a

- statement: A conversation never flips between physical endpoints, because switching endpoints loses the KV cache.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p210]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p210]
  rejected-alternative: flipping one conversation across multiple endpoints
  endorsement: n/a

- statement: An executor run is not tied to one base URL; each H2 step can use a different logical model, and each logical model can point to a different physical model.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p212]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p212]
  rejected-alternative: binding a whole run to a single base URL
  endorsement: n/a

- statement: The executor carries no base_url; endpoint configuration lives in the model config.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p213]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p213]
  rejected-alternative: an executor-level base_url setting
  endorsement: n/a

- statement: Each prompt carries a per-prompt file that maps prompt-level model ids to gateway model ids.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p214]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p214]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway is a proxy to an upstream OpenAI-compatible endpoint, and gateways chain: a local gateway can forward to a company gateway that forwards to a remote endpoint guarded by a whitelist.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p216]-[p218]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p216], [p217], [p218]
  rejected-alternative: none
  endorsement: n/a

```

## Not converted

- Make a little progress on a lot of things instead of a lot of progress on a few; build the known quantity (the gateway) first while the control flow is still uncertain. (Work-sequencing philosophy.) [p189]
- The user wrote Beast and knows SSE cold; the irritation is at being lectured, not at the technology. (Temperament.) [p183]
- Open question, unresolved in this unit: should skipping a heading level be an error? [p145]
- Open question, unresolved in this unit: AGENTS.md or CLAUDE.md? [p146]
- AGENTS.md should carry a command that keeps the docs up to date on every commit. (Repo-process directive, not language or engine behavior.) [p168]
- Hard-code the Anthropic base URL for now and point the HTTP layer at the gateway later. (Excluded as a technology/scaffolding choice, not a behavior.) [p149], [p169]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP server planning session (explicit invocation, fixed tool list, live reload, minimal core, plain-prose design docs, hypothesis collapse)
---

# 2026-08-03-2040-plan-the-mcp-server

```yaml
- statement: The MCP server has exactly one job, serving PromptForge prompts to a calling harness; anything beyond that is out of scope.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p2]
  rejected-alternative: a broader server surface beyond prompt-serving
  endorsement: n/a

- statement: A PromptForge prompt is a command; it runs only because a caller named it, never because a model noticed a tool that looked relevant.
  scope: mcp
  source: user-corrective
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p58], [p59]
  rejected-alternative: publishing each prompt as its own tool so a model can select it ambiently
  endorsement: n/a

- statement: PromptForge is a deterministic pipeline whose product is a finished report, designed for unattended server deployment running reports at scale; interactive invocation exists for development, testing, and explicit local runs.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p58], [p59]
  rejected-alternative: a general-purpose prompting language invoked conversationally
  endorsement: n/a

- statement: The server's published tool list is small and fixed (list_prompts, run_prompt, check_run, need_prompt) and never changes at runtime, so a prompt saved seconds ago is callable immediately with no reconnect and no list-changed machinery.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section]
  rejected-alternative: dynamic per-prompt tools with notifications/tools/list_changed
  endorsement: affirmed

- statement: need_prompt resolves an inexact name for an intent the user already stated; it never discovers a capability the user did not ask for.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p60]
  rejected-alternative: a classifier-backed chooser that recommends prompts for a task
  endorsement: affirmed

- statement: Tool descriptions are written in the register of a command interpreter; no trigger phrasing, no "use this when", nothing that competes with a client's own tools for selection.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p15], [p58]
  rejected-alternative: tool descriptions optimized to win model selection
  endorsement: affirmed

- statement: The server hard-codes no knowledge of any specific client or harness; it behaves the way conventional MCP servers behave.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p25], [p26]
  rejected-alternative: client-specific special cases such as Cursor-aware behavior
  endorsement: n/a

- statement: The prompt directory is watched live and prompts reload without a server restart; a prompt that breaks stays listed, carrying its error, rather than silently disappearing.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p6], [plans section]
  rejected-alternative: requiring a restart or a new chat to pick up prompt edits
  endorsement: n/a

- statement: The prompt catalog is configured with both individual prompt files and whole directories via wildcard, with exceptions.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p4], [p5]
  rejected-alternative: none
  endorsement: n/a

- statement: A long-running run keeps the calling client informed with live progress notifications, so the client sees work happening instead of waiting on a silent timer.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p32]
  rejected-alternative: a bare admission timer with no progress signal
  endorsement: n/a

- statement: Boot validation refuses an incoherent catalog; all failures accumulate and print before a nonzero exit, so a client never sees a silently missing tool.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section]
  rejected-alternative: starting the service with only the valid subset of prompts
  endorsement: unaddressed

- statement: Design work separates fact-finding from prose; one agent states plain facts and a separate fresh agent composes the prose in a given register, because writing under context pressure is what produces riddling language.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p77], [p78]
  rejected-alternative: writing the prose in the same commit and context that did the design work
  endorsement: n/a

- statement: Do more with less; if an established facility can implement a feature, use it instead of building new infrastructure, and keep the core a minimal set of small primitives reused everywhere.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p61]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p15]; 2026-08-09-1058-promptforge-core-large-part1.md [p26], 2026-08-14-1613-promptforge-core-largest-part1.md [p26]; 2026-08-14-1613-promptforge-core-largest-part3.md [p267]
  rejected-alternative: inventing new frontmatter when Lua already works
  endorsement: n/a

- statement: Reading a prompt file never runs anything inside it; a parsed prompt is inert data that can be constructed, inspected, and enumerated on a server surface without executing prompt code.
  scope: core
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: The design document is revised in the same commit as the step that changes the design, so the document is accurate per commit.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p17], [plans section]
  rejected-alternative: batching documentation updates after implementation
  endorsement: n/a

- statement: Design documents state what happens, not what property a thing has.
  scope: global
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p68], [p73]
  rejected-alternative: aphoristic property statements such as "parsing is total and produces no side effects"
  endorsement: affirmed

- statement: Never count what you do not name; a sentence like "two of those five are refuted" must name the two.
  scope: global
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p68], [p76]
  rejected-alternative: unnamed counts that send the reader hunting
  endorsement: affirmed

- statement: Superseded or rejected design content is preserved in a residue sidecar alongside the design document, not deleted.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p64], [p65]
  rejected-alternative: deleting leftover design material during a reorganization
  endorsement: n/a

- statement: Recovered design rationale is hypothesis collapse; generate competing explanations for each design element, kill them with structural evidence (plausibility kills nothing), state survivors confidently, leave what cannot be collapsed openly unresolved, and never apply an archive-proposed collapse without human approval.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p80], [p81]
  rejected-alternative: fluent single-explanation rationale written without evidence
  endorsement: n/a
```

## Not converted

- A design document is mostly why; code contains what, and where nothing forces a choice, that fact is worth stating rather than papering over. [plans section]
- The bet behind rationale recovery: most design choices are forced by constraints that are themselves visible in the code, so the why is largely recoverable. [plans section]
- Contingency is unrecoverable from code; numbers chosen inside a range, facts learned outside the repository, and deleted alternatives leave no trace, so a high open count is honest archaeology, not failure of effort. [plans section]
- "What lost and why" is the most valuable line a design document has. [plans section]
- The user wants prompts to be first-class citizens in the harness and research output delivered into the chat, not into side boxes. [p24]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core-large part 5 (first-class tools/models, section lifecycle, store, dialects, fanout)
---

# 2026-08-09-1058-promptforge-core-large-part5.md

```yaml
- statement: A pipeline must be re-runnable from any step, with every intermediate output persisted as a file that can be read back in, because development and debugging of an analytical pipeline depend on it.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p377]
  rejected-alternative: none
  endorsement: n/a

- statement: The tool.need call establishes a tool's name and the prompt owns that name from then on; rebinding happens in the preamble.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p386]
  rejected-alternative: none
  endorsement: n/a

- statement: Because the engine's pipeline is rigid and the orchestrating model cannot reshape the Lua at runtime, behavioral variation (such as which sources a prompt may consult) must be supplied through ahead-of-time configuration.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p392]
  rejected-alternative: relying on an orchestrator to reinterpret and reshape the prompt's instructions at runtime
  endorsement: n/a

- statement: The language has exactly three named Lua phases - the preamble (the H1 code) and the per-section prologue and epilogue - and this terminology is enforced consistently across the entire repo.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p393]
  rejected-alternative: none
  endorsement: n/a

- statement: The preamble can run model inference with tool calls, so the model can parse the argument string and take control before any section runs.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p397]
  rejected-alternative: none
  endorsement: n/a

- statement: Tools and models are first-class Lua objects: a tool is an inspectable, invocable table, a model exposes infer()/turn(), and the preamble can declare globals such as tool lists that any section can use - encapsulation that also makes both mockable and unit-testable.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p398-p401]
  rejected-alternative: treating tools and models as opaque registrations rather than encapsulated objects
  endorsement: n/a

- statement: Tool registration stays open between inference calls within a phase, so the add-search, infer, add-fetch pattern keeps working; the toolset must not be sealed at the first infer().
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p409]
  rejected-alternative: sealing the toolset on the first inference call
  endorsement: n/a

- statement: Prose lives in markdown sections, never inside Lua code; prose in code is rejected because markdown is where bold, italics, bullets, paragraphs, block quotes, and URLs can be properly formatted.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p427]
  rejected-alternative: passing prose as string arguments to model.infer()
  endorsement: n/a

- statement: Non-final prose sections are single-shot and always fall through; the last prose section is the tool loop and proceeds to the epilogue only when the reply contains no tool call.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p429]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua can invoke another H2 section as a subroutine through execute(), reusing the engine's existing section-execution machinery.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p430, p432, p433]
  rejected-alternative: none
  endorsement: n/a

- statement: Any Lua can call goto to transfer control to another section, and goto is context-clearing.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p431, p432, p433]
  rejected-alternative: none
  endorsement: n/a

- statement: The shared preamble program is never re-executed for each section; its objects are serialized out of the preamble VM and into each section VM, because replaying would re-run any inference the preamble performed.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p448-p450]
  rejected-alternative: replaying the shared H1 program inside every section VM
  endorsement: n/a

- statement: The store is the only intentional cross-section mutable channel; Lua functions, closures, globals, var, tools, and reply are branch-local by construction.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: mutable run-global Lua state
  endorsement: affirmed

- statement: A scalar top-level return from either preamble or epilog ends the run; a preamble return skips prose, model, and epilog; nil continues sequential fall-through.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle], 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p25]
  rejected-alternative: none
  endorsement: affirmed

- statement: The shared library is compiled once and its bytecode executed independently in every section VM, so each section receives isolated functions, closures, and mutable globals.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: none
  endorsement: corrected

- statement: All wire quirks - field synonyms, empty content, tool-call-with-null-content - are normalized in one module, and execute, clients, and hosts stay dumb; a final turn with no tool calls and empty content is a hard error even when reasoning is present, reasoning is never promoted into the answer, and breaking prompts that silently succeeded with empty replies is the intended effect.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: completion normalize layer]
  rejected-alternative: scattering wire-quirk handling across execute, client, and hosts
  endorsement: unaddressed

- statement: Recoverable tool target failures (HTTP errors, unsupported content type, timeout, too large, undecodable charset, DNS) return Ok with model-readable text naming status, final URL, and a next move, so the tool loop continues; admission and policy failures (invalid URL, blocked scheme/port/userinfo/IP literal, redirect refused) remain hard errors, and the untrusted HTTP error body is never placed in the tool result.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: webfetch soft errors]
  rejected-alternative: aborting the tool call on recoverable target failures
  endorsement: unaddressed

- statement: Prompts stay dialect-agnostic: the operator declares each model's tool dialect on the gateway, the gateway advertises it, core freezes it onto the bound model, and the tool loop selects the normalization plugin without ever asking the prompt what format to use; an unknown dialect id is a hard error with no silent fallback.
  scope: boundary: gateway<->core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Tool dialect plugins]; 2026-08-14-1613-promptforge-core-largest-part3.md [p250]
  rejected-alternative: sniffing completion text in the prompt surface or hardcoding model names inside prompts
  endorsement: unaddressed

- statement: Fanout fires all arms at once while the gateway admits up to its lane concurrency and queues the rest fairly; replies stay ordered by arm index, the first arm error aborts its siblings with the same visible behavior as sequential fail-fast, and authors must not assume one arm sees another arm's store writes.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Fanout and gateway concurrency]; 2026-08-14-1613-promptforge-core-largest-part3.md [p311], [p312]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- [p376] After first-class tools arrive, the VM can no longer be assumed fixed once the preamble has run; it can change after each completion.
- [p395] Unshipped code earns no compatibility concessions: "there's no one to break."
- [p401] Encapsulation is plain programming hygiene; an abstraction earns its keep by being mockable and testable.
- [p411] Big changes get a deep, subagent-driven evaluation before adoption; thoroughness scales with blast radius.
- [p412] The phase transition's only real point is to protect the epilogue.
- [p432] The conversation is preeminent: design documents must be rewritten to match what was settled in discussion.
- [p436] Documentation teaches progressively: one new concept per section, no forward references, every example a complete runnable prompt.
- [p440] Front-page documentation is crisp, bottom-line-up-front, dense and scannable - it says what the thing is rather than performing cool.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge.md session, Aug 16 afternoon (H1-only prompts, reply variable, tool call limits)
---

# 2026-08-16-1431-promptforge-md-aug16-afternoon.md

```yaml
- statement: Everything in the language behaves as consistently as possible, unless there is a really good reason for an exception.
  scope: global
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20]
  rejected-alternative: none
  endorsement: n/a

- statement: When execution enters a section, the model's previous reply is always available in the reply variable; a jump carries the reply into the destination section.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20], [p21]
  rejected-alternative: jump() dropping the reply so Lua cannot transfer it into the next block
  endorsement: n/a

- statement: There is a single reply variable; incoming_reply, reply, and last_reply are folded into one name, reply.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p22]
  rejected-alternative: three separate variables incoming_reply, reply, and last_reply
  endorsement: n/a

- statement: A prompt with no H2 sections is valid: the H1 runs its Lua and prose blocks, and when the model does not end in a tool call, execution ends and the model's reply becomes the prompt output.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p13]
  rejected-alternative: requiring at least one H2 section per prompt
  endorsement: n/a

- statement: For an H1-only prompt, the output priority is: the H1 Lua return value, then the H1 model reply, then a "done" fallback.
  scope: core
  source: ai-proposed
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Prompts are executed as MCP tool calls, and promptforge.md itself runs the MCP server.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p9]
  rejected-alternative: none
  endorsement: n/a

- statement: The root toml is not used at all.
  scope: global
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p10]
  rejected-alternative: configuration through a root toml file
  endorsement: n/a

- statement: The model discovers the MCP API by querying it once, keeping the API in context, rather than having the API documentation embedded up front.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p44]
  rejected-alternative: embedding the MCP API documentation in the context
  endorsement: n/a

- statement: Tool call limits are per-section; a global limit makes no sense other than being set to a very large number, because a global limit forces the author to re-check it every time sections are added.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p49]
  rejected-alternative: a meaningful global tool call limit
  endorsement: n/a

- statement: The language can express the universal search/fetch pattern with per-turn tool availability, where search is available only on the first turn and fetch only on the second and later turns.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p63]
  rejected-alternative: none
  endorsement: n/a

- statement: Constraining a section's toolset must not otherwise change its behavior; the section behaves the same as the traditional unconstrained form, only with a restricted toolset.
  scope: core
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p64]
  rejected-alternative: a constrained-toolset formulation that alters section behavior
  endorsement: n/a

- statement: The conversation history is not rewritten to scrub tool offerings or tool calls, because the model would see information appearing out of nowhere.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p61]
  rejected-alternative: scrubbing the tool offering and tool call from history
  endorsement: n/a

- statement: Migrating the whole conversation is a design non-goal.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p65]
  rejected-alternative: whole-conversation migration
  endorsement: n/a

- statement: A fenced block whose contents contain backticks is written with a 4-tick outer fence.
  scope: global
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p4]
  rejected-alternative: triple-backtick fences around blocks with interior backticks
  endorsement: n/a
```

## Not converted

- [p29] Whether {{ reply }} substitution injects information versus instructions is ambiguous and was raised as an open question, never resolved into a rule.
- [p30] Imperfect model output is acceptable because the user can always fix it.
- [p67] Tool call limits may be unnecessary at all; a large model concludes before overflow and a small model's context fills up and errors, which is a natural bound.

---

# 2026-08-05-2249-section-lua-lifecycle.md

## Candidates

(none - the unit is a single plan-execution dispatch prompt; it directs workflow, not language or engine behavior, so nothing passes the altitude test)

## Not converted

- When executing a plan, do not pause for reversible choices: make the plan's stated decision, record any necessary falsifier in design-core.md, and continue. [p1]
- Preserve the original design document (design-core-orig.md) byte-for-byte as the historical record. [p1]
- Fix every failure you introduce; run targeted tests as you proceed, then the full verification commands. [p1]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the two-repo commit review step (2026-08-03 18:27)
---

# 2026-08-03-1827-two-repo-commit-review.md

```yaml
- statement: A tool-call loop terminates ordinarily with no signal from the prompt; when the model has nothing left to do it says so in prose, and the executor moves on.
  scope: core
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [design documents section]
  rejected-alternative: an explicit termination signal emitted by the prompt
  endorsement: n/a

- statement: A forward-design residue states plainly at its top that it is forward design, names what exists today, and points at the crate's as-built document.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: residue that reads as if it describes the built world
  endorsement: n/a

- statement: Documentation of the built world must be accurate in both directions; claiming something unbuilt that ships is as wrong as claiming built what is not.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: checking only for claims of built features that do not exist
  endorsement: n/a

- statement: A repointing commit changes only the pointer; any change of meaning beyond the pointer is a defect.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: folding content edits into a rename or repointing commit
  endorsement: n/a

- statement: When a rename makes a bare filename ambiguous, every surviving reference must be found and updated, including citations and quoted sentences, not just links.
  scope: global
  source: user-corrective
  citation: 2026-08-03-1827-two-repo-commit-review.md [design documents section]
  rejected-alternative: updating only formal path references and leaving prose mentions
  endorsement: n/a
```

## Not converted

- Review is read-only: the reviewer reports findings and never fixes or commits anything itself. A work-discipline rule for the review step, not a rule of the language or engine.
- Report back in under 80 words with the finding count and the most serious finding. A terse-reporting preference, bookkeeping.
- Write nothing for a check that passes. A signal-to-noise preference for review output, subsumed by the review discipline.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from Brave web search tools planning chat
---

# 2026-07-29-0937-brave-web-search-tools.md

```yaml
- statement: The gateway must not depend on core.
  scope: boundary: gateway<->core
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p11]
  rejected-alternative: the gateway linking against core
  endorsement: n/a

- statement: The gateway owns provider API keys and serves remote tools as bearer-authenticated HTTP routes.
  scope: gateway
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p14]
  rejected-alternative: distributing provider keys to core or the CLI
  endorsement: n/a

- statement: The gateway is both the model router and the provider of remote tool routes.
  scope: gateway
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p5, p6]
  rejected-alternative: none
  endorsement: n/a

- statement: Fundamental tools are built into core so that a downstream user who links only core (with their own CLI) still gets them.
  scope: core
  source: user-corrective
  citation: 2026-07-29-0937-brave-web-search-tools.md [p14, p17, p18]
  rejected-alternative: shipping the tools as a separate linkable crate
  endorsement: n/a

- statement: There are no cargo feature flags and exactly one build configuration; if binary size becomes a problem, the crate is split later.
  scope: global
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p19]
  rejected-alternative: conditional compilation via feature gates
  endorsement: n/a

- statement: Only provider-backed tools live behind the gateway; local tools run in-process in core (web search goes through the gateway, web fetch stays local).
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p10, p13, p14]
  rejected-alternative: routing all tool calls through the gateway
  endorsement: n/a

- statement: The executor runs a bounded tool-call loop: execute each tool call, append results as tool-role messages, re-send to the model, and stop after a capped number of iterations.
  scope: core
  source: ai-proposed
  citation: 2026-07-29-0937-brave-web-search-tools.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: A prompt declares the tools it uses in frontmatter, and the executor matches those names against the tool instances it was given.
  scope: core
  source: ai-proposed
  citation: 2026-07-29-0937-brave-web-search-tools.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: Tools implement a common trait exposing name, description, JSON parameter schema, and an async call method; remote tools are reached through a proxy implementation of the same trait.
  scope: core
  source: ai-proposed
  citation: 2026-07-29-0937-brave-web-search-tools.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The gateway starts normally when a tool's config section is absent; the tool is simply unavailable.
  scope: gateway
  source: ai-proposed
  citation: 2026-07-29-0937-brave-web-search-tools.md [plans section]
  rejected-alternative: failing startup on missing tool config
  endorsement: unaddressed

- statement: A feature that calls an external service must ship with a manual integration test that exercises the real service, and that test must actually be run to prove it works.
  scope: global
  source: user-corrective
  citation: 2026-07-29-0937-brave-web-search-tools.md [p26, p27]
  rejected-alternative: mock-only tests
  endorsement: n/a

- statement: User-facing configuration surface (config file keys and similar) must be documented.
  scope: global
  source: user-stated
  citation: 2026-07-29-0937-brave-web-search-tools.md [p22]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- "Hell no to shellout" [p15] - implementation preference (no shelling out to subprocesses), fails the altitude test.
- "I don't want a bunch of junk" [p21] - temperament about keeping dependencies lean; a preference, not a directive.
- "what is a Trait?" [p12] and "what is feature-gate?" [p16] - clarifying questions, no principle stated.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from compaction-algorithm session part 3 (call syntax, per-section tool surface, gateway topology, model mapping)
---

# 2026-07-30-1046-compaction-algorithm-large-part3

```yaml
- statement: Prompt documents support nested sections recursively, from H2 all the way down through H6.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p144]
  rejected-alternative: none
  endorsement: n/a

- statement: Surface syntax favors natural human-readable phrasing over function-call notation, because the language is written for humans to read.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p155], [p156], [p157], [p158]; 2026-08-02-1134-mcp-client-large-part3.md [p155]-[p158]
  rejected-alternative: function-call notation such as call( "return", "x" )
  endorsement: n/a

- statement: The engine gives the model a handful of well-described tools plus a prose prompt and lets the model figure out the action on its own.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p158]; 2026-08-02-1134-mcp-client-large-part3.md [p158]
  rejected-alternative: none
  endorsement: n/a

- statement: The number of tools injected into the model's context is kept minimal; call() exists so the context is not stuffed with tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p163]; 2026-08-02-1134-mcp-client-large-part3.md [p163]
  rejected-alternative: injecting one tool per capability
  endorsement: n/a

- statement: The tool surface is specialized per section; a section that always falls through gets no call() tool injected at all.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p164]
  rejected-alternative: offering the full call() surface to every section
  endorsement: n/a

- statement: A section that only ever jumps with clear offers a restricted goto() with no mode parameter, so the model does not have to pick a call kind.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p222]; 2026-08-02-1134-mcp-client-large-part3.md [p164], [p222]
  rejected-alternative: offering the full multi-mode call() to a single-behavior section
  endorsement: n/a

- statement: The language provides both a dramatically simple single-concern call and a full swiss-army call, because decisions are what small models are worst at while frontier models handle multiple call kinds without trouble.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p222], [p223]; 2026-08-02-1134-mcp-client-large-part3.md [p223]
  rejected-alternative: standardizing on one call form for all models
  endorsement: n/a

- statement: Every markdown feature of the prompt format ships with a corresponding test.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]; 2026-08-02-1134-mcp-client-large-part3.md [p173]
  rejected-alternative: none
  endorsement: n/a

- statement: Model-specific translation to and from tool calls is the gateway's responsibility, not the executor's.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p185], [p186], [p187]
  rejected-alternative: the executor handling per-model tool-call translation
  endorsement: n/a

- statement: Components do not share schema definitions; each side of a boundary owns its own schemas, because sharing them is unnecessary coupling.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190], [p191], [p192]; 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]
  rejected-alternative: a shared schema package used by both executor and gateway
  endorsement: n/a

- statement: Exactly one machine holds the provider API key, because global rate limits cannot otherwise be enforced.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p211]
  rejected-alternative: distributing provider keys across multiple machines
  endorsement: n/a

- statement: The executor is just a function call: it holds no endpoint, credential, or provider knowledge of its own; the LLM credential lives in the gateway, and the executor knows no vendor.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p215], 2026-08-02-1134-mcp-client-large-part5.md [plans: gateway v0]
  rejected-alternative: the executor holding the vendor key directly
  endorsement: n/a

```

## Not converted

- [p145] Open question, never resolved in this unit: should skipping a heading level be an error?
- [p189] Sequencing temperament: make a little progress on a lot of things instead of a lot of progress on a few; build the known-quantity skeleton (the gateway) first while control flow is still uncertain.
- [p158] Aesthetic conviction: there is something powerful about a small tool set plus prose with the model left to figure it out (partially converted into the tool-minimality and model-autonomy records above).

---
---
produced: 2026-08-19
title: PromptForge design principles mined from MCP client continued chat (tool picker, need strings, choose_mcp_tool, context rewrite)
---

# 2026-08-02-1419-mcp-client-continued

```yaml
- statement: Need strings are author-register capability descriptions - clean, parameter-free statements of what the tool does - not runtime user utterances.
  scope: mcp
  source: user-corrective
  citation: 2026-08-02-1419-mcp-client-continued.md [p58]
  rejected-alternative: need strings phrased like user prompts or utterances
  endorsement: n/a

- statement: Tool-need resolution runs locally and deterministically with no LLM in the resolution path; an LLM is at most an optional escalation, never the default matcher.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p27]
  rejected-alternative: an LLM as the primary matcher in the final system
  endorsement: n/a

- statement: A matching technique is adopted only after it proves itself on tests against real data; no matcher ships on intuition or on synthetic benchmarks alone.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p17]
  rejected-alternative: adopting a classifier without empirical validation
  endorsement: n/a

- statement: Tool selection is framed as ranking - given the catalog, which tool best fits the need - not as an independent binary fit judgment per tool.
  scope: mcp
  source: user-corrective
  citation: 2026-08-02-1419-mcp-client-continued.md [p25]
  rejected-alternative: asking of each tool separately "is this a fit for the need"
  endorsement: n/a

- statement: When no single tool wins clearly, the resolver surfaces a shortlist of about three rather than forcing a top-1 guess, and a better-informed decider settles the near-tie.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p69]
  rejected-alternative: always returning a single best-guess tool
  endorsement: n/a

- statement: Duplicate tools in the author's own catalog are a configuration error and fail loud; duplicates arising from intentionally imported foreign servers must be given an explicit disambiguation path.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p61]
  rejected-alternative: silently picking among duplicate tools
  endorsement: n/a

- statement: Absence is a first-class outcome: when nothing clears the similarity floor the resolver reports "no tools available" instead of binding the least-bad candidate.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p66]
  rejected-alternative: always returning the best available tool even on a poor match
  endorsement: n/a

- statement: Tool annotations may only improve confidence as tiebreakers; resolution must work without them.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p56]
  rejected-alternative: treating annotations as necessary for resolution
  endorsement: n/a

- statement: Dynamic tool discovery is strictly opt-in: the author explicitly adds the built-in choose_mcp_tool, and it is the only dynamic path, not an escalation fallback from static binding.
  scope: mcp
  source: user-corrective
  citation: 2026-08-02-1419-mcp-client-continued.md [p63]
  rejected-alternative: choose_mcp_tool as an automatic escalation path
  endorsement: n/a

- statement: choose_mcp_tool returns one or more tool descriptors, or a "no tools available" error, and it complements static launch-time binding rather than replacing it.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: On dynamic resolution the harness rewrites the context - the chosen descriptor placed before the prompt prose and the discovery exchange excised - so a dynamically discovered tool executes exactly as if it had been statically bound.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p67]
  rejected-alternative: appending the discovery results to the context like an ordinary tool result
  endorsement: n/a

- statement: Tool selection stays in the main context, which the author already governs (model choice, rewrite opt-out, full task history); the model that selects a tool is the model that will use it, so there is no chooser/executor capability mismatch and no orphan subcontext with its own unanswered model configuration.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p71], [design documents section]
  rejected-alternative: a fresh subcontext that retrieves and selects the tool, with a chooser context distinct from the executing model
  endorsement: n/a

- statement: For genuinely hard selection, a strong reasoning model can select the tool and pass the descriptor through a context-clearing goto into a fresh context where a cheaper model executes.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p72]
  rejected-alternative: none
  endorsement: n/a

- statement: Crates are kept small enough that a coding LLM can hold an entire crate in a single context window.
  scope: global
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p79]
  rejected-alternative: none
  endorsement: n/a

- statement: Resolution is a single four-outcome decision - clear bind, own-catalog duplicate (fail loud), foreign overlap (surface shortlist), absence (fail loud) - gated by a calibrated similarity floor plus a top-1-vs-top-2 margin.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1419-mcp-client-continued.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: The MCP client crate stays pure protocol; all resolution semantics live in a separate crate so protocol consumers never load the embedding model.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1419-mcp-client-continued.md [design documents section]
  rejected-alternative: embedding the resolver in the MCP client crate
  endorsement: affirmed
```

## Not converted

- The author controls all the MCP servers, so hardening against hostile servers feels like wasted effort - a threat-model posture, not a directive. [p14]
- Accuracy is felt as a per-call error rate ("0.80 means one out of five tool calls will be wrong") - the stakes framing behind the abstention design. [p32]
- "Do everything asynchronously" - a working-style preference for the spike tooling, not the engine. [p46]
- Dataset-building craft: generate need strings with multiple models, and derive them by paraphrasing the descriptions of tools the author already intends to use. [p51] [p59] [p60]
- Inspect raw samples together before trusting a metric ("pick 30 descriptions at random... let's look at it together"). [p57]
- Process preferences: design doc first, then dataset, then reconcile the cited numbers; every design gets a companion rationale document mined from the chat history. [p75] [p82]
- A stream of clever matcher variants (vocabulary word-counts, noun/verb embedding channels, category routing with per-category models, dynamic LoRA pools) - all later measured and rejected; the temperament is propose freely, then let measurement kill. [p28] [p29] [p30] [p31] [p33]
- A trivial-reject pre-filter with no false rejections, pairing and categorizing tools to discard obvious mismatches fast - proposed, later rejected as hard category routing. [p55]
- Reconciliation rule from the plan: preliminary figures must be replaced by reproduced numbers, and any figure that moves enough to threaten a design choice gets flagged rather than silently patched. [plans section]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 5 (vfs access, fall-through protection, context clearing, subhead naming, MCP service shape)
---

# 2026-08-02-1134-mcp-client-large-part5

```yaml
- statement: A prompt must be readable on its face; a reader can look at it and understand what it does, with no invisible action left to the model's interpretation.
  scope: global
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p362]
  rejected-alternative: dispatch expressed as literal text the model interprets, e.g. task("### Researcher", "Find and save a source about {{ args }}")
  endorsement: n/a

- statement: An overarching design theme of the language is that it closely resembles the ordinary theory of computation; shared top-level reusable sections are subroutines, a staple of computation.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p385]
  rejected-alternative: none
  endorsement: n/a

- statement: Every transfer to another H2 is context-clearing, and sequential fall-through never accumulates context.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p414], [p415]
  rejected-alternative: fall-through that appends each section into a growing shared context
  endorsement: n/a

- statement: A PromptForge file requires YAML frontmatter carrying a promptforge version number; major versions are incompatible changes, a file without the version is not a PromptForge prompt and runs the traditional full-file way, and the engine offers a detection function rather than running plain prompts itself.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p402], [p403], [p407], [p427]
  rejected-alternative: a fallback mode for files without YAML, or the engine running plain prompts
  endorsement: n/a

- statement: A "---" line directly under an H2 heading protects that section from fall-through; the executor skips it and proceeds to the next section, and the mechanism survives the user cutting and pasting sections around.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p382], [p383], [p387], [p388], [p389], [p390]
  rejected-alternative: a single "---" below which no execution occurs at all
  endorsement: n/a

- statement: Every subhead begins with a valid identifier as its first word, lowercase-normalized, and anything after it on the heading line is a comment; H2 names are unique across the file, H3 names are unique only within their enclosing H2, and H1 is not a subhead.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p381], [p391], [p392], [p393], [p394]
  rejected-alternative: none
  endorsement: n/a

- statement: An H2 transfers control to its H3 sections explicitly; there is no implicit descent into child sections.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p400], [p401]
  rejected-alternative: none
  endorsement: n/a

- statement: Cyclic calls between sections are permitted because some tools require cycles; runaway execution is bounded by budgets - nesting limit, step budget, tool budget - not by structural prohibition.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p369], [p371], [p372]
  rejected-alternative: restricting calls so sections may only call same-or-lower heading levels
  endorsement: n/a

- statement: Default control flow (fall-through) is a property of the executor over the markdown, not of Lua; making it happen inside Lua would be clumsy.
  scope: boundary: markdown<->lua
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p363]
  rejected-alternative: implementing fall-through inside the Lua block
  endorsement: n/a

- statement: Lua has equal access to the virtual file system; the scripting layer is not a second-class citizen relative to the rest of the engine.
  scope: boundary: lua<->vfs
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p349]
  rejected-alternative: none
  endorsement: n/a

- statement: Every protection the engine imposes can be disabled; an author building an agent, harness, or IDE must have a way to turn all the settings off.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p354]
  rejected-alternative: compulsory protections with no opt-out
  endorsement: n/a

- statement: The engine exposes system facts to prompts through a sys object, including the current date and time and the elapsed run time directly, because prompts need to inject them.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p419], [p420]
  rejected-alternative: none
  endorsement: n/a

- statement: The MCP service is long-running rather than launched per invocation: it loads and syntax-checks its fixed set of prompts, loads libraries, and holds open-weight models in memory once, and it also hosts an MCP client because the prompts it runs make outbound MCP calls such as web search and web fetch.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p440]
  rejected-alternative: a stdio service the editor launches and tears down on every call
  endorsement: n/a

- statement: The MCP service exposes exactly two tools - enumerate the runnable prompts and run a prompt - because client context degrades when too many tools are installed; prompt-to-prompt calls inside a run never round-trip through MCP, and editor routing lives in a Cursor rule that sends files bearing promptforge frontmatter to the service.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p435], [p441]
  rejected-alternative: exposing one tool per prompt to the editor
  endorsement: n/a

- statement: The CLI and the MCP service share identical run semantics - same detection, tool selection, sandbox store, and executor - with no duplicated virtual file system or tool wiring between them.
  scope: boundary: cli<->mcp
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p437]
  rejected-alternative: duplicating the vfs inside the MCP service
  endorsement: n/a

- statement: Per-section tool scoping is opt-in: a section's Lua block names its tools and the runtime advertises and dispatches only those, so a section can never hold a tool it did not ask for, and a scoped name absent from the run's tools is a hard error, never silently dropped.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: per-section tool scoping]; 2026-07-28-2238-orchestrator-design-continued.md [p17, p85, p119]; 2026-07-30-1046-compaction-algorithm-large-part1.md [p17]; 2026-08-02-1134-mcp-client-large-part1.md [p17]
  rejected-alternative: opt-out scoping where a section gets all frontmatter tools unless it subtracts
  endorsement: affirmed

- statement: A section's Lua block runs in a sandbox: empty globals, only safe standard-library subsets, no io/os/require/load/package/debug, and an instruction-count hook that aborts a runaway block.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: lua args substitution]; 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- "The markdown is the program, the model is the CPU, embedded Lua is the microcode, and the harness is the instruction decoder" - the defining metaphor of the whole design.
- Model sovereignty: every design decision (context clearing, flat tool calls, per-section scoping, fan-out to small models) is chosen to make mid-size open-weight models reliable.
- Integrity stance: subagent prompts are shipped verbatim from named sections rather than paraphrased by the model; what you test is what runs.
- Unit of testing equals unit of composition; each section is testable in isolation with known inputs.
- Honest-limits temperament on guard-wrapping untrusted tool output: a probabilistic mitigation, not a boundary; the hard controls are scoping and context-clearing isolation.
- Sequencing preference: structure the work as the shortest line to a working Cursor integration and push all later complexity much later.
- Lesson from Playbooks prior art: never put a compilation step between the prompt author and the model; the raw markdown is the program.
- Development ergonomics: the service picks up config and directory changes without a restart, and invoking an uninstalled prompt simply errors.

---
---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core large session part 1 (tool needs, H1 structure, fanout, tracing, logging, testing, CLI dev loop)
---

# 2026-08-09-1058-promptforge-core-large-part1.md

```yaml
- statement: Never provide two ways of doing the same thing, unless there is a really good documented reason.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26], 2026-08-14-1613-promptforge-core-largest-part1.md [p26]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p165]
  rejected-alternative: duplicate facilities for the same capability
  endorsement: n/a

- statement: Tool declarations live in the H1 preamble of the prompt, not in YAML front matter.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26], 2026-08-14-1613-promptforge-core-largest-part1.md [p26]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p45]
  rejected-alternative: tool front matter
  endorsement: n/a

- statement: A prompt declares the tool capabilities it needs as descriptive need strings rather than hard-coded tool names; the harness resolves each need to a tool by semantic match (embedding and reranking) and binds it to a local symbol the prose can reference precisely, and a need that resolves to no tool or to an ambiguous tool is an error.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p27-p31], 2026-08-14-1613-promptforge-core-largest-part1.md [p27], [p28]; 2026-08-03-2040-plan-the-mcp-server.md [p60], 2026-08-09-1058-promptforge-core-large-part5.md [p383]; 2026-08-02-1419-mcp-client-continued.md [p39]
  rejected-alternative: hard-coded tool names in prompts
  endorsement: n/a

- statement: Ambiguity or duplication in tool binding is an error; mapping the same tool to two different ids is rejected.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p35], 2026-08-14-1613-promptforge-core-largest-part1.md [p35]
  rejected-alternative: silently allowing duplicate tool bindings
  endorsement: n/a

- statement: After the H1 preamble runs, the harness compares all bound tools pairwise and fails the prompt if any two are too similar to disambiguate.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p36-p37], 2026-08-14-1613-promptforge-core-largest-part1.md [p36]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt file is an H1 section containing a lua preamble fence, prose, and a lua epilogue fence, followed by H2 sections.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p6-p12], 2026-08-14-1613-promptforge-core-largest-part1.md [p7]
  rejected-alternative: a trailing lua code fence after the section body
  endorsement: n/a

- statement: The H1 is required; anything between the YAML front matter and the H1 is ignored.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p23], 2026-08-14-1613-promptforge-core-largest-part1.md [p23]
  rejected-alternative: meaningful content between front matter and H1
  endorsement: n/a

- statement: After the H1 preamble executes, the prompt-global Lua state becomes read-only, and each fanout arm receives its own copy of shared functions rather than sharing mutable state.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p15-p21], 2026-08-14-1613-promptforge-core-largest-part1.md [p15]
  rejected-alternative: shared mutable global state across fanout arms
  endorsement: n/a

- statement: Every harness operation reports its activity to an optional caller-installed observer; trace events are reduced to a Section string and a Detail string.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p39-p40], 2026-08-14-1613-promptforge-core-largest-part1.md [p39], [p40]
  rejected-alternative: a taxonomy of typed trace event structures
  endorsement: n/a

- statement: Prompts have a log() facility whose output is concurrency-safe and tagged with a per-execution id.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p53-p56], 2026-08-14-1613-promptforge-core-largest-part1.md [p56]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompt behavior is tested with standalone prompt files, not inline strings in test code.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p46-p47], 2026-08-14-1613-promptforge-core-largest-part1.md [p46]
  rejected-alternative: inline prompt strings in test code
  endorsement: n/a

- statement: Integration tests exercise real inference and tool calling end to end, using a locally cached model so repeated runs are cheap and offline.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p61-p70]
  rejected-alternative: integration tests without a real model
  endorsement: n/a

- statement: There is a command-line runner that executes a prompt file with real inference, picks up what it needs from the prompt's directory, and shows debug logging, so prompts can be iterated quickly without extra infrastructure.
  scope: cli
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p76-p77], 2026-08-14-1613-promptforge-core-largest-part1.md [p76], [p77]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- p13: design documents should explain rationale and features, not just instructions (documentation practice, not engine behavior).
- p24: nothing has shipped yet, so backward breakage is not a concern (project-stage note).
- p41: idea of a fine-tuned small open-weight model that summarizes a prompt into a short label (open question, undecided).
- p42-p45: break work into per-step commits with review before continuing, never stop to ask (workflow temperament, not PromptForge design).
- p48-p50: whether the "version" key should be required and how it differs from "promptforge" (unresolved questions).
- p54: whether Lua print should be disabled or remapped (unresolved question).
- p65-p68: whether an OpenAI-shaped llama-server endpoint duplicates promptforge-gateway (unresolved question).

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core largest session part 1 (tool needs, observer, lua environment, CLI dev loop)
---

# 2026-08-14-1613-promptforge-core-largest-part1

```yaml
- statement: Within a section the lua fence comes before the prose, so a preamble can never be confused with an epilogue.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p22]
  rejected-alternative: none
  endorsement: n/a

- statement: Functions shared by many sections are defined once in the prompt's global lua rather than duplicated per section.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p14]
  rejected-alternative: duplicating shared functions in each section that uses them
  endorsement: n/a

- statement: The lua environment provides a log() facility, useful in tests to confirm execution reached a certain point; print is disabled or remapped to it.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p55]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- [p24] Nothing has shipped, so backward compatibility is not a constraint; break freely.
- [p41] Inclination toward a fine-tuned small open-weight model that computes a short description of a prompt; undecided whether to use it.
- [p43] Plans are executed as individual steps, each with its own commit plus code review and amended commit, never stopping to ask the user.
- [p20] Aversion to code paths that can theoretically fail but never actually do, because they produce code that appears to ignore errors.
- [p13] A design document should explain the rationale and the features, not just instructions.

---
---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge.md session Aug 15 (env resolution, secrets hygiene, mention-to-run, minimal core instructions)
---

# 2026-08-15-2006-promptforge-md-aug15

```yaml
- statement: A PromptForge program is activated by mentioning its file in any model context; the model loads it, builds it if necessary, and runs it, with no manual terminal steps.
  scope: global
  source: user-stated
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p5]
  rejected-alternative: running the program from a terminal by hand
  endorsement: n/a

- statement: The gateway resolves environment variables from the operating system environment directly, never through a shell, because it runs as a system service on production machines where no shell inheritance exists.
  scope: gateway
  source: user-corrective
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p4], [p5], [p13]
  rejected-alternative: resolving variables through shell inheritance
  endorsement: n/a

- statement: Secrets such as API keys must never enter the model's context.
  scope: boundary: gateway<->model
  source: user-stated
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p6]
  rejected-alternative: passing the API key through the prompt or the core instruction file
  endorsement: n/a

- statement: The core instruction file (promptforge.md) stays minimal; new features and operational details must not bloat it.
  scope: global
  source: user-stated
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p6], [plans section]
  rejected-alternative: documenting environment-variable handling inside promptforge.md
  endorsement: n/a

- statement: When engine behavior changes, the core instruction file is updated in the same pass; stale instructions are treated as defects.
  scope: global
  source: user-corrective
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p21]
  rejected-alternative: leaving outdated instructions in place after a behavior change
  endorsement: n/a

- statement: Env file resolution walks the config inheritance chain from the specified TOML all the way to the end, combining every .env file encountered along the way.
  scope: core
  source: user-corrective
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p11], [p12]
  rejected-alternative: stopping at the first encountered .env file, or taking the env file co-located with the specified config
  endorsement: n/a

- statement: The language's instructions explicitly forbid the model from reading any .env file into its context.
  scope: global
  source: user-stated
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p22]
  rejected-alternative: none
  endorsement: n/a

- statement: The repository provides a top-level gitignored directory for local prompts and configuration that remains indexed and readable by the IDE.
  scope: global
  source: user-stated
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p28], [p29]
  rejected-alternative: none
  endorsement: n/a

- statement: Every user-facing binary loads its .env file at startup, before config interpolation resolves ${VAR} references.
  scope: global
  source: ai-proposed
  citation: 2026-08-15-2006-promptforge-md-aug15.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: A missing .env file is not an error; binaries start and run normally without one, so production environments with no .env keep working.
  scope: global
  source: ai-proposed
  citation: 2026-08-15-2006-promptforge-md-aug15.md [plans section]
  rejected-alternative: failing startup when no .env file is present
  endorsement: unaddressed

- statement: .env files are gitignored so secrets never enter version control.
  scope: global
  source: ai-proposed
  citation: 2026-08-15-2006-promptforge-md-aug15.md [plans section], [p18], [p19]
  rejected-alternative: none
  endorsement: affirmed
```

## Not converted

- [p14] Demands complete test coverage for every change; "make fucking sure" is the temperament, not a rule.
- [p15] Applies the standing rulebooks (rust, vibe) to all implementation work; a process preference, not engine behavior.
- [p24] Clutter at the repository root is a defect; an aesthetic about repo hygiene.
- [p28] Wary of dot-prefixed directory names confusing the IDE; a tooling instinct behind the local-directory rule.
- [p10] Naming-symmetry instinct: config.toml pairs with config.env; superseded by the inheritance-chain resolution rule.
- [p5] Everything should "just work" from a mention; impatience with manual steps, partially converted into the activation principle.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the promptforge.md session of Aug 18 morning (fanout arrays, tools.local, model selection, infer semantics)
---

# Design principles mined from 2026-08-18-1126-promptforge-md-aug18-morning.md

```yaml
- statement: When a prompt has one output file and the invocation does not map it to a real path, the MCP server returns exactly that file's contents for display in chat, with no separator line and no filename label.
  scope: mcp
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p29] [p30] [p31] [p39]
  rejected-alternative: appending a decorated copy of the output after the chat reply, with a separator line and the filename
  endorsement: n/a

- statement: Fanout's fundamental operation is executing a set of sections in parallel; fanout() takes a worker section plus either a list-section name or an array of items, and items() returns a section's parsed list as an array for that purpose.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p45] [p108] [p109]
  rejected-alternative: none
  endorsement: n/a

- statement: Every error reported to the prompt author carries the file and line number in the prompt that produced it.
  scope: global
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p54]; 2026-08-14-1613-promptforge-core-largest-part3.md [p279], [p280], [p313]
  rejected-alternative: errors that lack the prompt's file and line location
  endorsement: n/a

- statement: Declarations freeze before the epilogue: once a Lua block has no following prose block, the model and tools tables are made immutable before that block runs, since further mutation would be useless.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p56] [p59] [p60]
  rejected-alternative: an open/closed tool-scope lifecycle tracked across every block
  endorsement: n/a

- statement: Inline inference is referentially transparent: model::infer inside a Lua block is always equivalent to ending the block, interpolating the result as prose, and continuing in a new block; the epilogue is defined as the Lua code followed by no inference call and no prose.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p71] [p72] [p73] [p74] [p75]
  rejected-alternative: none
  endorsement: n/a

- statement: A section's model is chosen exactly once, in the section's first Lua block, and locks for the rest of the section; any prose or inference before a model has been selected is an error.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p62] [p67] [p175] [p177]
  rejected-alternative: none
  endorsement: n/a

- statement: All Lua chunks in one H2 section share a single VM, so state passes between chunks through plain globals.
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p103] [p125] [p127]
  rejected-alternative: per-chunk environments with closures re-installed between blocks
  endorsement: n/a

- statement: The Lua environment is installed once on entry to an H2 and then left alone; the tool schema sent to the model is computed fresh just before each prose call instead of being maintained by scope open/close machinery.
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p124] [p154]
  rejected-alternative: a tool loop that mutates the environment between blocks and a closed-scope schema path
  endorsement: n/a

- statement: Engine capabilities are not gated on document structure; fanout() is allowed whether or not a section has child headings.
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p138]
  rejected-alternative: restricting fanout() to sections with child headings
  endorsement: n/a

- statement: An error in any Lua chunk stops the entire prompt run.
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p149]
  rejected-alternative: continuing the run past a chunk error
  endorsement: n/a

- statement: A prompt can declare a model-callable tool backed by a Lua function, registered from any Lua chunk in the H2 and effective for the next prose call; Lua-backed tools have the same capabilities as native tools.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p99] [p144] [p160]
  rejected-alternative: none
  endorsement: n/a

- statement: A Lua-backed tool declares a parameter schema derived from its function declaration; the model is not left to infer argument shapes from prose context.
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p117] [p120]
  rejected-alternative: schema-less local tools presenting only name and description (ai-proposed in the tools-local plan, corrected)
  endorsement: n/a

- statement: Lua tool handlers cannot jump; ordinary section Lua can jump, including Lua reached through execute().
  scope: core
  source: user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p162] [p163]
  rejected-alternative: allowing jump() from tool handlers
  endorsement: n/a

- statement: infer() is a blocking call with a fresh context: a string goes in and a string comes out, with no tools, no shared conversation history, and no reply side effects, using the model selected for the H2.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p165] [p182]
  rejected-alternative: infer with tools and history, and a two-argument infer that picks a model per call
  endorsement: n/a

- statement: Model selection is a default plus per-section override: models.default sets the prompt-wide model, a section may override it once, and switching models means starting a new H2 with context carried forward explicitly through reply.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p168] [p179]
  rejected-alternative: models.only, an all-or-nothing lock that forecloses per-section overrides
  endorsement: n/a

- statement: A small set of flexible, multi-purpose primitives should compose into maximum possibility while keeping the prompt author brief; verbosity is a design failure.
  scope: global
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p168]
  rejected-alternative: none
  endorsement: n/a

- statement: Constraints should fall out of the existing rules naturally rather than being coded as explicit special-case checks.
  scope: global
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p176] [p177] [p178]
  rejected-alternative: hand-coded guard checks for each constraint
  endorsement: n/a

- statement: Data arriving from external sources is untrusted and injection-prone; the design of data passing to tools and fanout arms must account for that.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p110]
  rejected-alternative: none
  endorsement: n/a

- statement: The model may emit many tool calls in a single response; the engine collects them, executes them, and rendezvous the results before continuing.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p96]
  rejected-alternative: one completion round-trip per tool call
  endorsement: n/a
```

## Not converted

- Less code to maintain beats bespoke machinery; prefer nil-ing out a table over building a dedicated error path. [p53] [p54]
- When a feature is removed, leave a short comment explaining why, written for a fresh-context reader. [p162]
- A Lua tool that combines deterministic data with a one-shot inference is the most powerful operation available: determinism plus model judgment. [p162]
- A silent no-op (tools.add between prose blocks) is taken as evidence of insufficient test coverage. [p145]
- The primitives should feel like one family: fanout is like infer. [p87]
- An itch for a general cleanup pass that finds stale, redundant, or tightened code across the codebase. [p134] [p158]
- Instinct against duplicating data: pass store paths rather than copying section strings. [p105] [p106]
