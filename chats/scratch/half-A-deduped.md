---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from the agentic IDE (vibbi) research session (copy-Cursor directive, autonomous execution, trust boundary, streaming render)
---

# 2026-07-31-1516-agentic-ide-research

```yaml
- statement: When any UI behavior or appearance is in doubt, the implementation copies Cursor exactly, with VS Code as the secondary reference, down to fonts, icons, and layout.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p46], [p49], [p81]
  rejected-alternative: designing UI elements from first principles or original designs
  endorsement: n/a

- statement: Before building an interface, subagents research how the reference product does it and the findings are codified in a master document of UI rules.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p40], [p43], [p44], [p46], [p49]
  rejected-alternative: building UI incrementally without a written reference standard
  endorsement: n/a

- statement: Every panel divider is draggable and every window is dockable.
  scope: core
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p46], [p49]
  rejected-alternative: fixed panel layouts
  endorsement: n/a

- statement: Refactoring happens continuously at every step, each file holds a single concern, refactoring is scheduled as explicit slices targeting subsets of existing code, and technical debt is never allowed to accumulate.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p49], [p57]
  rejected-alternative: deferring cleanup to a later dedicated phase
  endorsement: n/a

- statement: Autonomous execution continues without stopping until the assigned work is done, pausing only when user input is genuinely required or the outcome diverges significantly from expectation.
  scope: global
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p87], [p109]; 2026-07-28-0207-architect-vibe-planning-part2.md [p104] [p106]
  rejected-alternative: stopping to check in at intermediate milestones
  endorsement: n/a

- statement: Applying an input to a plan and running the plan are distinct operations; an instruction to update a plan is never an instruction to execute it.
  scope: core
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p36]
  rejected-alternative: treating a plan revision as authorization to run it
  endorsement: n/a

- statement: When the user declares a working mode, the system stays in that mode until told otherwise.
  scope: core
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p35]
  rejected-alternative: leaving plan mode to act once the plan looks ready
  endorsement: n/a

- statement: The embedded browser is a full browser, and the LLM must eventually be able to drive it as a tool.
  scope: core
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p18], [p21]
  rejected-alternative: a limited in-editor preview pane
  endorsement: n/a

- statement: LLM access goes through a gateway reached by URL, with API keys supplied through the environment.
  scope: gateway
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p33], [p37]
  rejected-alternative: storing provider keys in settings files
  endorsement: n/a

- statement: Markdown preview renders local images scaled to the viewport width rather than forcing horizontal scroll, shows XML tags as visible text, and hides HTML comments.
  scope: core
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p96], [p97], [p100], [p102], [p103]
  rejected-alternative: GitHub-style rendering that strips XML tags
  endorsement: n/a

- statement: UI zoom applies to the entire interface, including the content of embedded web panels.
  scope: core
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p42], [p46]
  rejected-alternative: zooming only the chrome while embedded content keeps its own scale
  endorsement: n/a

- statement: Feature parity with the reference product is completed before differentiating AI/MCP features are built, and the roadmap is adjusted to reflect that order.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p63], [p113]
  rejected-alternative: building AI-native differentiators ahead of baseline parity
  endorsement: n/a

- statement: Secrets and privileged calls live only in the trusted backend; app UI runs in the trusted context while third-party web content runs isolated, and a secret never reaches an untrusted context.
  scope: boundary: app<->web
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Panel]
  rejected-alternative: making LLM calls from the frontend with the key present in the webview
  endorsement: unaddressed

- statement: Model output is treated as untrusted input: it is rendered sanitized with hardened links, and script/event-handler payloads are asserted inert by tests, including mid-stream.
  scope: core
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Best-Practices Upgrade]
  rejected-alternative: rendering raw HTML from model output
  endorsement: unaddressed

- statement: Incremental streaming rendering never flashes broken markup: partial syntax buffers until disambiguated, the DOM grows append-only, and the finalized render equals an atomic render of the same text.
  scope: core
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Best-Practices Upgrade]
  rejected-alternative: re-rendering the full accumulated string on each token
  endorsement: unaddressed

- statement: Streaming output follows the bottom only while the user is already at the bottom; a user scroll-up detaches the follow behavior and the view is never yanked back down.
  scope: core
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Best-Practices Upgrade]
  rejected-alternative: forcing scroll-to-bottom on every streamed chunk
  endorsement: unaddressed

- statement: Agent actions run with a human in the loop: the loop interrupts for approve, edit, or reject before resuming; edits are checkpointed and rollback-able; and the shell boundary is treated as not checkpointable.
  scope: core
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Roadmap]
  rejected-alternative: fully autonomous tool-calling without approval gates or rollback
  endorsement: unaddressed

- statement: Extensibility is provided through existing open protocols (MCP and LSP) rather than a bespoke plugin API; a plugin system is considered only after the protocols prove insufficient.
  scope: mcp
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Roadmap]
  rejected-alternative: a bespoke plugin API
  endorsement: unaddressed

- statement: Each chat tab is an independent conversation with its own identity derived from the tab, so many conversations coexist in one window.
  scope: core
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Cursor-like Workbench], [p46]
  rejected-alternative: a single global conversation per window
  endorsement: affirmed

- statement: Work proceeds in slices, each built by one agent, reviewed by a fresh agent, and fixed by a third, with each fix landing in its own commit; a git-mutating command never runs concurrently with a file-writing agent.
  scope: global
  source: ai-proposed
  citation: 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Best-Practices Upgrade]
  rejected-alternative: one agent building and reviewing its own work in a single pass
  endorsement: unaddressed
```

## Not converted

- API-lean and call-chain-lean matter to the author, not file-size lean; "bloated" means over-engineered call chains, not bundle size. [p7], [p8]
- Technology choices are validated against ecosystem popularity and prior art before adoption. [p2], [p40], [p43], [p44]
- Hard-delete preference: when the user says delete, there is no trash staging step. [p25]
- Non-blocking robustness concerns are deferred explicitly ("we can worry about it later") rather than fixed on the spot. [p106], [p107]
- Components are named and organized so separately developed repos can merge into one workspace later. [p12], [p17], [p20], [p22]

*2026-08-19 06:10 - kimi-k3*

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from compaction algorithm session part 5 (theory of computation, readability, fall-through protection, subhead identifiers, tool scoping, guard-wrapped untrusted output)
---

# 2026-07-30-1046-compaction-algorithm-large-part5

```yaml
- statement: An overarching design theme of the language is that it closely resembles the ordinary theory of computation; shared top-level reusable sections are subroutines, a staple of computation.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p385]
  rejected-alternative: none
  endorsement: n/a

- statement: A reader must be able to look at a prompt and understand what it does; there must be no invisible action whose meaning is subject to interpretation by the model.
  scope: global
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p360-p362]
  rejected-alternative: dispatch expressed as literal text the model is expected to interpret and act on
  endorsement: n/a

- statement: PromptForge must be usable with power equal to or greater than an agentic harness like Cursor or Claude Code.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p348]; 2026-08-02-1134-mcp-client-large-part4.md [p348]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua has equal access to the virtual file system.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p349]
  rejected-alternative: none
  endorsement: n/a

- statement: An embedder building a harness or IDE must be able to disable all of the engine's protective settings.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p354]
  rejected-alternative: protections that are always on with no escape hatch
  endorsement: n/a

- statement: Fall-through is control flow of the markdown section structure, not of Lua; Lua does not fall through and is not made to.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p363]
  rejected-alternative: implementing default fall-through inside the Lua executor
  endorsement: n/a

- statement: Cyclic section calls are permitted; runaway execution is bounded by budgets (nesting limit, step budget, tool budget), not by forbidding cycles.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p369-p372]
  rejected-alternative: restricting calls to an acyclic graph (an H3 may only call H3 and below)
  endorsement: n/a

- statement: A section's Lua block is the first fenced lua block in the section, and only whitespace may appear between the section heading and that fence.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p379]
  rejected-alternative: none
  endorsement: n/a

- statement: H2 section names must be unique; H3 names must be unique within their parent section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p381]
  rejected-alternative: none
  endorsement: n/a

- statement: Control-flow syntax must survive the user cutting and pasting sections around in the document.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p390]
  rejected-alternative: positional control-flow markers whose meaning depends on where they sit in the file
  endorsement: n/a

- statement: Every subhead's first word must be a valid identifier; anything after whitespace following that word is an ignored comment, and the name is lowercase-normalized.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p391-p393]
  rejected-alternative: none
  endorsement: n/a

- statement: H2 is a subhead; H1 is not.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p394-p395]
  rejected-alternative: none
  endorsement: n/a

- statement: Per-section tool scoping is opt-in: a section receives only the tools its Lua block names with tools.add(), a section that names no tools gets none, and a scoped name absent from the run's tools is a hard error, never silently dropped.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: per-section tool scoping]; 2026-07-28-0925-orchestrator-design-document.md [p17]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p85]; 2026-08-02-1134-mcp-client-large-part4.md [p328], [p329]
  rejected-alternative: opt-out scoping where a section starts with all frontmatter tools
  endorsement: affirmed

- statement: Attacker-controllable tool output is automatically wrapped in a guard block declaring the content data rather than commands, triggered by a tool-declared untrusted-output property, with marker strings inside the content escaped so the delimiter cannot be forged.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: guard-wrap untrusted tool output], [p333-p335]; 2026-08-02-1134-mcp-client-large-part4.md [p333], [p334], [p335]
  rejected-alternative: a separate safe-fetch tool (web_fetch_safe) chosen per call
  endorsement: corrected

- statement: All model-side control flow goes through a single unified call tool with a type discriminator (return, goto, task, fanout), keeping the control-flow tool count at one.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions]
  rejected-alternative: a separate tool per control-flow verb
  endorsement: unaddressed

- statement: A section ends when the model replies with text and no tool calls, and that text becomes the run result.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions], [plans: multi-turn research prompt]
  rejected-alternative: an explicit termination call required to end a section
  endorsement: affirmed

- statement: Template substitution is single-pass: scalars render as strings, tables as JSON, and a missing key is a hard error.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: Lua args substitution], [p364-p365]
  rejected-alternative: none
  endorsement: affirmed

- statement: The executor holds no vendor credentials; a gateway owns the LLM credential and model-name routing, and the executor talks only to the gateway.
  scope: gateway
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: gateway v0]
  rejected-alternative: the executor reading the vendor API key directly
  endorsement: unaddressed

- statement: Subagent dispatch is verbatim: a task call resolves the section reference in the harness and ships the prompt author's exact words, so the model never paraphrases the subagent's instructions and there is no prompt drift.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: Orchestrator Design Document], [p362]; 2026-07-28-0925-orchestrator-design-document.md [p20]
  rejected-alternative: the model composing or rewriting the subagent's prompt at dispatch time
  endorsement: affirmed
```

## Not converted

- "Should we do files or should we do state?" [p341] - an open musing on the state model, no directive landed.
- Line-offset table versus character ranges for edit tools [p343-p344] - a question about established practice, not a position.
- Sharded-mutex lock contention idea [p350-p351] - a performance implementation note the user explicitly deferred ("not something to worry about now").
- Sub-agent doing web search then web fetch into a virtual file [p355] - a usage scenario probing capability, not a directive.
- The web_fetch SSRF security surface (CIDR tables, redirect re-checks, size caps, content-type routing) [plans: webfetch crate extraction] - tool implementation spec, not language or engine behavior.
- Model tiering per section [plans: Orchestrator Design Document] - a convertible principle dropped only because the 20-candidate cap favored more general records.
- Lua sandbox contents (empty globals, safe stdlib only, instruction-count hook) [plans: Lua args substitution] - convertible but dropped at the cap; the module allowlist is also partly a technology choice.
- State tiering (files primary, counters for audit, store for the rest) [plans: PromptForge Executor Tranche 1] - convertible but dropped at the cap.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 2 (Lua substitution, tool discovery, bindings, control flow, gateway, MCP export)
---

# 2026-08-02-1134-mcp-client-large-part2

```yaml
- statement: A prompt is a single markdown file that is one function - it takes well-defined parameters declared in machine-readable YAML front matter and returns a string, and it may also produce side effects such as files written through tools.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p117]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p65, p117]
  rejected-alternative: none
  endorsement: n/a

- statement: The design starts from the prompt and adds structured programming into it, never the other way around; a prompt with zero Lua still works like a plain orchestration, so Lua is additive, not required.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p118]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p118]
  rejected-alternative: starting with an interpreted host language and bolting prompts onto it
  endorsement: n/a

- statement: Every design choice is evaluated by whether it relieves pressure on the context window so smaller models can run the prompt; moving orchestration logic into deterministic Lua reduces the model sophistication required.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p119]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p119]
  rejected-alternative: none
  endorsement: n/a

- statement: Invocation runs in both directions - Lua code can call the model, and the model can route and orchestrate with multi-turn decision making when a task requires it.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p66]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua state is substituted into prompt text through a substitution syntax, and that substitution is what makes prompt assembly deterministic.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p66]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: The tool surface offered to a section stays small enough for a small orchestrator model (roughly five to seven tools); a section is offered only the tools it needs, and control-flow primitives may collapse into a single tool with a mode parameter if small models struggle.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p85], [p119], [p120]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt is self-contained; running it never requires a companion Rust file backing its operations.
  scope: global
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p86]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p86]
  rejected-alternative: every prompt backed by its own Rust code
  endorsement: n/a

- statement: The schema attaches to the tool, not to the prompt, so fifty prompts sharing a tool do not repeat the schema fifty times.
  scope: boundary: prompt<->tool-binding
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p90]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p90]
  rejected-alternative: declaring the schema in each prompt's front matter
  endorsement: n/a
```

## Not converted

- [p76] Naming preference: "args" over "params" for prompt parameters.
- [p84] Anxiety that twenty large per-tool schemas recreate the pydantic burden, just shifted into Lua.
- [p92], [p93] Open sandboxing worries: infinite loops in prompt Lua, and tools gaining file read/write through the Lua library.
- [p94] Belief that people will use prompt Lua for general-purpose computation, so static tool detection may never be complete.
- [p96], [p100] Open exploration of making the file the unit of state, tempered by the corrective that structured data like breadcrumbs still exists.
- [p123], [p129] Build-sequencing preference: one big plan implemented in subtractive tranches, starting from a hello-world executor invoked from the command line.
- [p130], [p131], [p132] Repo bookkeeping preferences: a cumulative status file and AGENTS.md at the root rather than .mdc rules.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the orchestrator design document chat - sections, goto, tool-call state, verbatim dispatch, Lua, fanout
---

# 2026-07-28-0925-orchestrator-design-document.md

```yaml
- statement: State is built through flat tool calls into a persistent store, not returned out of the model as structured output.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p13]
  rejected-alternative: Pydantic structured output passed out of the model orchestrator
  endorsement: n/a

- statement: A pipeline document is parsed into sections with stable IDs, and the entry section is named main.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: goto destroys the current context and starts a fresh context from the target section's prompt with only params and state-store access; a section may goto itself.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p14, p74, p75]
  rejected-alternative: compacting the transcript to make room in a continuing context
  endorsement: n/a

- statement: A new pipeline is a new markdown file; one general-purpose harness runs any assay-shaped pipeline without new orchestration code.
  scope: global
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p15]
  rejected-alternative: hundreds of lines of per-pipeline Python glue
  endorsement: n/a

- statement: Model tier is declared per section, so a pipeline hops between model tiers per step.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: Task nesting is arbitrary in principle but bounded by a configurable safety valve (max depth, max total tasks).
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: Deeply nested task chains are debugged by making each subtask well tested and well defined; the unit of testing is the unit of composition.
  scope: global
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p19]
  rejected-alternative: none
  endorsement: n/a

- statement: Deterministic orchestration (step ordering, fanout of N) runs in the harness or Lua without inference; only decision-bearing orchestration (choosing between step A and step B) is left to the model in prose.
  scope: core
  source: user-corrective
  citation: 2026-07-28-0925-orchestrator-design-document.md [p69]
  rejected-alternative: purely declarative Lua with all branching paid for in model inference
  endorsement: n/a
```
```yaml
- statement: call() runs a referenced section in the same context while task() runs it in a fresh subcontext; both reference the prompt by section name instead of passing prompt text, so fewer output tokens are consumed and the context never holds both prompts.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p73]
  rejected-alternative: none
  endorsement: n/a

- statement: Fanout spoke identity (such as a file index) is assigned by the harness, never calculated by the model, to minimize inference.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p67]
  rejected-alternative: the model computing each spoke's unique name or index
  endorsement: n/a

- statement: Sections inherit their parent's context like a stack.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p67]
  rejected-alternative: none
  endorsement: n/a

- statement: The harness offers virtual files (CreateFile, AppendFile, DeleteFile) as in-memory blobs the agent cannot distinguish from real files, plus a combine operation that merges fanout results into a single document with optional order preservation.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p46]
  rejected-alternative: none
  endorsement: n/a

- statement: Pipelines never use AskQuestion; user interaction is a runtime-level pattern with an unattended/interactive mode toggle.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p41, p43]
  rejected-alternative: the AskQuestion tool inside pipelines
  endorsement: n/a

- statement: Embedded Lua is kept minimal; putting too much logic in Lua re-implements the orchestrator inside the markdown and defeats the purpose.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p68]
  rejected-alternative: an orchestrator written in Lua embedded in the markdown file
  endorsement: n/a

- statement: A section may carry an optional Lua block that defines preconditions, postconditions, and tool injection.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p25]
  rejected-alternative: none
  endorsement: n/a

- statement: The runtime never contains orchestration logic, prompt assembly, or step ordering (those live in the markdown); the tool library never contains pipeline-specific logic (each tool is a thin, flat-signature function).
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0925-orchestrator-design-document.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: No compilation step sits between the prompt author and the model; the raw markdown is the program.
  scope: core
  source: ai-proposed
  citation: 2026-07-28-0925-orchestrator-design-document.md [design documents section]
  rejected-alternative: compiling markdown to an intermediate representation before execution (Playbooks lesson)
  endorsement: unaddressed

- statement: Adoption is a proof-of-concept alongside the existing assay pipeline, starting with PaperGate, not a rewrite.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0925-orchestrator-design-document.md [plans section]
  rejected-alternative: rewriting assay on the new runtime up front
  endorsement: unaddressed
```

## Not converted

- Model sovereignty: the standing temperament that every design decision should make mid-size open-weight models reliable at roughly 1/100th of frontier API cost (design document BLUF).
- "Minimize the amount of inference" as a general instinct behind several rulings [p67, p69].
- The transcript compaction algorithm (recursive halving, fidelity gradient, prompt reinjection, pre-compaction at 90%) - real directives, but scoped to Mentographist and explicitly declared not part of the orchestrator [p2, p15, p31, plans appendix].
- Chat-format preferences ("dont code fence me" [p12, p26], blockquote user text [p59]) - transcript formatting, not PromptForge design.
- Open-weight hardware and latency discussion (model sizes, gaming cards, STT/TTS budget) [p4-p10, p38] - capability scouting, no behavioral directive.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge-core work session part 4 (tool-call normalization, dialects, epilogue assertions, tool scoping, Lua-as-tool)
---

# 2026-08-09-1058-promptforge-core-large-part4

```yaml
- statement: Tool-call syntax is normalized per model through a normalization layer, so prompt text never contains model-specific invocation details.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p250]
  rejected-alternative: embedding model-specific tool-call formats in the prompt itself
  endorsement: n/a

- statement: The normalization layer is abstracted behind clean interfaces with no hardcoding, so it works for all models.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p250], [p253]
  rejected-alternative: hardcoded per-model handling
  endorsement: n/a

- statement: Adding a model must not require the operator to set its dialect; the engine discovers which dialect a model needs on its own.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p253]
  rejected-alternative: operator-configured dialect per model
  endorsement: n/a

- statement: Each model dialect is a self-contained pluggable module, one per source file, collected under a single dialects location.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p254]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt can assert required tool usage in its epilogue, e.g. assert(tools.calls["search"] > 0), and the count is per-VM.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p265], [p266], [p268]
  rejected-alternative: none
  endorsement: n/a

- statement: Do more with less: expressive general primitives are preferred over dedicated single-purpose features.
  scope: global
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p267]
  rejected-alternative: a dedicated require_called directive for mandatory tool calls
  endorsement: n/a

- statement: A failed tool call still counts as a call, because assertions measure whether the model is performing, not whether the tool is performing.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p271]
  rejected-alternative: counting only successful tool calls
  endorsement: n/a

- statement: Naming an unknown tool alias is a hard error with clear diagnostics.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p271]
  rejected-alternative: silently ignoring or warning on unknown aliases
  endorsement: n/a

- statement: Tool references are scoped, not globally "registered"; naming an unscoped yet global tool is a hard error.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p272], [p273]
  rejected-alternative: a global tool registry where any name resolves
  endorsement: n/a

- statement: Assertion failures in a prompt report the source file and line number.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p279], [p280], [p313]
  rejected-alternative: assertion failures without source locations
  endorsement: n/a

- statement: Run artifacts are written incrementally as turns complete and files arrive, not buffered and dumped at the end of the run.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p290], [p298], [p299]
  rejected-alternative: waiting to write all JSON turn files at the end
  endorsement: n/a

- statement: Concurrency is implemented in both the gateway and the core, with per-model concurrency limits set in each model's own config file.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p305], [p307]
  rejected-alternative: none
  endorsement: n/a

- statement: Shared configuration contains no model-specific entries; anything naming a model lives in that model's own config file.
  scope: gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p309], [p310]
  rejected-alternative: mentioning specific models in the common config
  endorsement: n/a

- statement: Cancellation (ctrl+C) must keep working cleanly under concurrent execution.
  scope: gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p317]
  rejected-alternative: none
  endorsement: n/a

- statement: Access control applies to the model, not to Lua: every H2 section that injects tools also injects which files those tools may access.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p368]; 2026-08-14-1613-promptforge-core-largest-part4.md [p368]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p328], [p329]
  rejected-alternative: protecting the machine by restricting the Lua API instead of the prompt's tools
  endorsement: n/a

- statement: Tool availability can be scoped by turn within a section, e.g. only web_search on the first turn, then web_fetch and web_search from later turns.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p372]; 2026-08-14-1613-promptforge-core-largest-part4.md [p372]
  rejected-alternative: making all of a section's tools available on every turn
  endorsement: n/a

- statement: A tool can be implemented as an inline Lua function acting as a front end to a real tool, and it can enable further tools at call time (e.g. tools.add for fetch); the prompt author opting in is what makes this acceptable.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p373], [p374]; 2026-08-14-1613-promptforge-core-largest-part4.md [p373]
  rejected-alternative: requiring a Rust function for every tool, even one that just sets a variable
  endorsement: n/a
```

## Not converted

- Skepticism about Gemma's reliability at tool calling ("that's its one fucking job") - a model-quality grievance, not a directive [p249], [p303].
- Staged definition of "beautiful" output (parity with local qwen, then surpass it, then three rounds of no improvement before switching subjects) - an experimentation methodology [p320].
- Optimize web-search agents for as few turns as possible - a tuning preference [p321].
- Do not bias a prompt toward a class of subject ("don't make the prompt biased to favor non-profits"; say "corporate filings") - a prompt-authoring neutrality preference [p325], [p326].
- A/B test thinking on/off across models and iterate until no axis improves; review code every 3 commits - a working style [p346], [p348].
- Commit uncommitted WIP before starting plan work - a workflow habit [p259], [p291].
- Preference for cribbing other people's code from the internet to make things work - an implementation attitude [p253].

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the 2026-07-30 design-context session (control flow, async tasks, fan-out, XML blocks)
---

# 2026-07-30-0534-promptforge-design-context.md

```yaml
- statement: The author organizes sections however they want; cycles are legal, dormant sections are legal, and an unreachable section is not an error.
  scope: global
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p4], [plans section]
  rejected-alternative: boot-time graph validation rejecting unreachable sections
  endorsement: n/a

- statement: The Lua return keyword ends the run, and it can be called from check.
  scope: core
  source: user-corrective
  citation: 2026-07-30-0534-promptforge-design-context.md [p11]
  rejected-alternative: none
  endorsement: n/a

- statement: A goto carries a value as its second parameter, and the destination section receives that value under the name "result".
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p12], [p13], [p14], [p17], [p18]
  rejected-alternative: calling the carried value an "injection"
  endorsement: n/a

- statement: The value passed on a control-flow transfer is explicit and visible, so a reader of the prompt source can see it.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p15]
  rejected-alternative: none
  endorsement: n/a

- statement: A task is either synchronous or asynchronous; a synchronous task behaves like a function call with a context reset, and an asynchronous task requires a rendezvous.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p22]
  rejected-alternative: none
  endorsement: n/a

- statement: An asynchronous task delivers its result by performing a normal control-flow transfer (goto, return, etc.), which the executor waits for.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p23]
  rejected-alternative: none
  endorsement: n/a

- statement: A section may goto itself to clear its own context, enabling a perpetually running task alongside the main context.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p24], [p25]
  rejected-alternative: none
  endorsement: n/a

- statement: When a section with a pending async task moves on or returns, the pending task is cancelled and the section receives a cancellation message, typically a diagnostic.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p26]
  rejected-alternative: none
  endorsement: n/a

- statement: Launching an async task immediately returns a unique ID; the model can cancel a task by ID, and task launches carry timestamps.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p27], [p28]
  rejected-alternative: none
  endorsement: n/a

- statement: Language keywords use the vocabulary models already speak, e.g. "spawn" for launching asynchronous sub-agents.
  scope: global
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p30], [p31]
  rejected-alternative: none
  endorsement: n/a

- statement: A fork spawns an asynchronous task while the caller falls through, and forks are not required to rejoin; a forked section may loop until a condition is met and never come back.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p34], [p35]
  rejected-alternative: requiring forks to always come together
  endorsement: n/a

- statement: Fan-out is restricted to the fanning section's own children; a section cannot fan out to another H2 or its children.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p39]
  rejected-alternative: unrestricted fan-out across sections
  endorsement: n/a

- statement: XML blocks may appear anywhere in the document; the harness extracts them into a table, and nothing inside XML tags counts as prompt text.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p41]
  rejected-alternative: none
  endorsement: n/a

- statement: XML is reserved for model-facing markup, not for the harness's grouping; section headings are the grouping mechanism.
  scope: core
  source: user-corrective
  citation: 2026-07-30-0534-promptforge-design-context.md [p53]
  rejected-alternative: XML tags as the harness's grouping and batching system
  endorsement: n/a

- statement: No heading level is special; any named section may be referenced.
  scope: core
  source: user-corrective
  citation: 2026-07-30-0534-promptforge-design-context.md [p54]
  rejected-alternative: restricting references to one designated heading level
  endorsement: n/a

- statement: The prompt requires no separate manifest of its blocks.
  scope: core
  source: user-corrective
  citation: 2026-07-30-0534-promptforge-design-context.md [p60]
  rejected-alternative: a "blocks:" manifest
  endorsement: n/a

- statement: Bulleted and numbered lists are always split, even when the author intended them as model prose.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p61]
  rejected-alternative: none
  endorsement: n/a

- statement: The prompts passed to fan-out arms need not be known ahead of time; the model decides at runtime what sub-agent work to spawn based on what it has learned.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p50]
  rejected-alternative: rigid, statically fixed fan-out rules in Lua
  endorsement: n/a
```

## Not converted

- A prompt is a work of art; the single-prompt format is loved for its own sake. [p4]
- Design documents are provisional and lower priority than the conversation, always; conversation decisions override anything written in them. [p5], [p6], [plans section]
- Lua spawning sub-agents and blocking to collect their results into variables or a map was explored as a scenario, not decided. [p32]
- Dividing the problem space into synchronous and asynchronous halves is the way to make progress. [p36]
- Manual per-item fan-out markup that turns thirty lines into a hundred is not worth it; the ergonomics were left unresolved. [p46]
- Cuts to the design documents happen as they come up in conversation; no speculative purge. [plans section]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from top-to-bottom repo review session (crate-serial review, fresh contexts, API tightening cadence, refactor-rust tool)
---

# 2026-08-10-0856-repo-review-top-to-bottom

```yaml
- statement: Large review work proceeds one crate at a time in dependency order; the next crate begins only after the current crate is fully implemented and verified green.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p1], [p5]
  rejected-alternative: interleaving crates or running multiple rounds of review and fixes
  endorsement: n/a

- statement: Every unit of review work runs in a fresh subagent context that is never reused, and the main context receives only completion status, a short summary, and the artifact path; raw source and full findings stay out of the main context.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p1], [plans section]; 2026-08-11-1510-repo-review-continued.md [p1], [plans section]
  rejected-alternative: reusing agents or pulling full findings into the main conversation
  endorsement: n/a

- statement: The public API is tightened continuously as development proceeds, because API growth drives quadratic dependency growth and per-commit tightening keeps total debt work linear.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p32], [p36]
  rejected-alternative: deferring all API and hygiene cleanup to one large effort at the end
  endorsement: n/a

- statement: A smaller API is always better than a larger one.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p52]
  rejected-alternative: none
  endorsement: n/a

- statement: API design proceeds by considering how each function interacts with the others in pairs, in triples, and all together, finding common usage patterns and expressing them with a simpler design.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p53]
  rejected-alternative: evaluating each API function in isolation
  endorsement: n/a

- statement: A refactoring tool separates its work into API review, light hygiene, and heavy hygiene; the per-commit default is the light pair (API review plus light hygiene), and heavy hygiene is opt-in and periodic because additive best-practices work can bloat the code into negative return.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p36], [p45], [p47]
  rejected-alternative: running full best-practices hygiene on every commit
  endorsement: n/a

- statement: The human, not the model, decides when deep cleanup is warranted; the model cannot reliably detect that an API has quiesced, since zero measured churn may only mean many small commits.
  scope: global
  source: user-corrective
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p41]
  rejected-alternative: automated churn metrics triggering the heavy hygiene pass
  endorsement: n/a

- statement: The human declares which activities are in bounds and how much time is available; the model then decides how much work to do and orders the steps so that the easiest steps and the steps that shrink downstream work come first, with pure deletions undertaken before anything else.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p42], [p43]
  rejected-alternative: the model pacing itself by estimated hours of runtime
  endorsement: n/a
```

```yaml
- statement: A tool tracks where it left off by reading the recent commit log (a bounded window such as the last 7 days), never by stamping SHAs into commit messages or keeping a state file.
  scope: global
  source: user-corrective
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p49], [p50]
  rejected-alternative: commit-message SHA stamps or a persistent state file
  endorsement: n/a

- statement: A tool always prints one line listing its functions and the active default before doing any work, defaulting to the lightest highest-dividend function, so the user can abort and escalate scope.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p45]
  rejected-alternative: none
  endorsement: n/a

- statement: A tool is self-contained: its rulebook is inlined at the bottom of the tool file in uniquely named XML-tagged blocks, and subagents are dispatched with a tiny prompt carrying only the tool path, the tag name, and the instruction to grep for the tag and execute the enclosed block.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p44]
  rejected-alternative: subagents reading external rulebook paths or receiving large inlined prompts
  endorsement: n/a

- statement: A run lands its result only when verification is green; on failure it rolls back with a reset (never a revert) and redoes the work.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p20], [plans section]
  rejected-alternative: landing red, or undoing failure with a revert commit
  endorsement: n/a

- statement: When restarting from an earlier state, whatever is good in the discarded work is preserved, and the model (not the user) decides how much to roll back.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p19]
  rejected-alternative: asking the user how much to roll back, or discarding the work wholesale
  endorsement: n/a

- statement: A one-off cleanup effort is generalized into a reusable prompt that runs against recent changes as development proceeds, so debt is paid continuously instead of in one large effort at the end.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p31]
  rejected-alternative: repeating ad-hoc top-to-bottom reviews after debt accumulates
  endorsement: n/a

- statement: A review run actions only findings introduced by the commits under review; pre-existing debt in untouched code is grandfathered, so re-scanning an already-clean commit yields nothing and no watermark is needed.
  scope: global
  source: ai-proposed
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [plans section]
  rejected-alternative: actioning all findings anywhere in the scanned code
  endorsement: affirmed
```

## Not converted

- Flavor text must be genuine, lightly adapted Gibson fragments with every sentence reviewed for sense; nonsense imagery is called out by name. (aesthetic craft standard, [p54]-[p57])
- The finished result must be chefs-kiss; the recurring worry is whether the work is making the code cleaner or just bloating and smearing it around. (quality temperament, [p22], [p23], [p59])
- Wip commits pushed to the remote are a cheap backup and are kept. (pragmatism, [p26], [p27])
- The mess is self-diagnosed: vibe-coding for days without technical-debt refactors along the way is what produced the findings pileup. (philosophy of debt, [p30])
- When a run goes sideways, stop and interrogate the state before touching anything: is the top commit better than before, and how much would a reset lose. (temperament under failure, [p10]-[p12])

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from architect and vibe-coding planning session part 1 (plan-as-source, regeneration, blur, compression)
---

# 2026-07-28-0207-architect-vibe-planning-part1

```yaml
- statement: A failed run discards all partial results and starts over from the beginning; resumability is not a goal.
  scope: core
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p3]
  rejected-alternative: checkpointed orchestration that restarts surgically from the failing stage
  endorsement: n/a

- statement: Intermediate values produced during a run are examinable, because inspecting them is how runs get debugged.
  scope: core
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p3]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt artifact is revised by editing the plan that created it and regenerating the artifact, never by having the model rewrite the artifact itself.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p6], [p24], [p33]
  rejected-alternative: bringing the artifact into a new revision pass and letting the model rewrite it
  endorsement: n/a

- statement: The originating plan is the source of truth for an artifact and is preserved for the life of the artifact.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p24], [p33]
  rejected-alternative: treating the generated artifact as the canonical version
  endorsement: n/a

- statement: A modification is never planned against the generated artifact; it is merged back into the original plan, so a plan's input is never another plan's output.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p42]
  rejected-alternative: chaining a modification plan whose input is the previous plan's generated output
  endorsement: n/a

- statement: After regeneration, a comparison step diffs the new artifact against the previous revision and carries forward whatever was good that got lost, including rationale that was sanded down.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p34], [p47]
  rejected-alternative: none
  endorsement: n/a

- statement: Small tweaks made after an artifact is created are appended to its plan as individual instructions, so they are incorporated at the next regeneration instead of being edited into the artifact.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p57]
  rejected-alternative: going back into plan mode and regenerating the whole plan for each small tweak
  endorsement: n/a

- statement: Compressing a prompt sentence is only valid when the shorter sentence means the same thing in execution, or is even more aligned than the original.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p56]
  rejected-alternative: shortening for token count alone
  endorsement: n/a

- statement: Whether a compression preserved meaning is judged objectively by how the instruction will execute, and a frontier model can make that judgment by comparing the two sentences; the standard is global and has nothing to do with the author's personal style.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p58]
  rejected-alternative: training the compressor on the author's personal style
  endorsement: n/a

- statement: Sharpening a blurred plan requires external information: the previous revision as an additional input, plus the author's stable repertoire of prompt techniques that every artifact draws on.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p55]
  rejected-alternative: sharpening from the blurred artifact alone
  endorsement: n/a

- statement: Prompt artifacts must stay lean; a revision that grows the artifact is a failure mode, not an improvement.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p1], [p49], [p50]
  rejected-alternative: accepting growth as the natural cost of revision
  endorsement: n/a
```

## Not converted

- Every time a model rewrites an artifact it resamples toward the mean of the distribution (top-k) and away from argmax, like gaussian blur in semantic space; only a significant correction counteracts it. [p1], [p3]
- First-pass generation is the sharpest pass: one pass, one prompt. [p3], [p4]
- The blur of a regenerated artifact is proportional to how many tokens of the input came from the model. [p38]
- The output of a blurred plan can still be as sharp as the original, because the plan's design choices survive even when its rationale is sanded down. [p47]
- No comparison algorithm, however good, prevents slow bloat over repeated regenerate-and-repair cycles; blurred content smears and takes up more space. [p48], [p49]
- Cropping a blurred plan makes it smaller but loses information each time, so over many cycles the plan returns to the same size with its instructions sanded down. [p54]
- A model cannot sharpen without external information. [p55]
- Open question the user kept circling: what operation shrinks a plan without blurring it, and how can a model compress without smoothing? [p51], [p53]
- Cursor plan files are machine-local and not portable via git; skills are the better portable mechanism today. (Excluded as a technology/mechanism choice, not a behavior.) [p12], [p22]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from compaction algorithm session part 2 (function model, control flow, tool discovery, gateway, MCP)
---

# 2026-07-30-1046-compaction-algorithm-large-part2

```yaml
- statement: Work is spread across files by decomposing into separate prompt files; calling another prompt by filename invokes it as a function; directories serve as namespaces; intra-process prompt-to-prompt calls go direct, not through MCP.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p117, p120]; 2026-08-02-1134-mcp-client-large-part2.md [p117], [p120]
  rejected-alternative: routing in-process prompt-to-prompt calls through MCP or sockets
  endorsement: n/a

- statement: Every section heading is also a function - it returns a string and takes only a string, and that string is supplied by the node that transfers control to it.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p65]
  rejected-alternative: none
  endorsement: n/a

- statement: Control transfer is expressed through three primitives with distinct context semantics - call preserves context and returns to the caller, task runs in a fresh context but still returns a result, goto transfers control without returning and clears context - and these may collapse into a single tool with a mode parameter if small models cannot handle multiple control-flow tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p65, p120]; 2026-08-02-1134-mcp-client-large-part2.md [p120]
  rejected-alternative: none
  endorsement: n/a

- statement: The user cannot declare arbitrary globals; only a fixed set of objects is accessible from prompt code.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p71]; 2026-08-02-1134-mcp-client-large-part2.md [p71]
  rejected-alternative: arbitrary user-declared globals
  endorsement: n/a

- statement: A prompt's key-value parameters are read-only and visible to every section and to any Lua anywhere in the prompt, so values never have to be passed from section to section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p74]; 2026-08-02-1134-mcp-client-large-part2.md [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: Section transitions are context-clearing by default - falling through to the next section is the default when no explicit control flow is specified, the model's narration and throat-clearing is trimmed rather than carried forward, the preferred advance mechanism is a tool call where the model explicitly passes only the curated context the next section needs, and running off the end terminates the prompt with a default completion message that can be overridden in YAML, so termination is always well-defined.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p75, p121]; 2026-08-02-1134-mcp-client-large-part2.md [p75], [p121]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10]
  rejected-alternative: bare goto as the advance mechanism, which cannot pass a curated instruction string
  endorsement: n/a

- statement: Structured data passes between Lua and the model as JSON assembled in Lua and returned by the model via macro substitution, and the tool-call mechanism structures the payload under the hood so the encoding can be swapped.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p78, p79]; 2026-08-02-1134-mcp-client-large-part2.md [p78], [p79]
  rejected-alternative: pydantic-style schema conformance with injected system-prompt overhead
  endorsement: n/a

- statement: Prompts operate in a semantic space of abstract operations (e.g. add claim, remove claim) that know nothing about the storage backend; a per-prompt configuration file binds each abstract tool to a concrete implementation, and the bindings are generic so the backend (Postgres, SQLite, MySQL) is never hardcoded into the tool.
  scope: boundary: prompt<->tool-bindings
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p88]; 2026-08-02-1134-mcp-client-large-part2.md [p88]
  rejected-alternative: hardcoding the database backend into the tool
  endorsement: n/a

- statement: Tools are discovered, not declared - at load time the harness parses the prompt's Lua with everything stubbed, intercepts tool-registration calls, enumerates and deduplicates the required tools, fails to load with an error if any binding is missing, and offers a command that emits an empty bindings template for the user to fill in.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p89, p91, p95]; 2026-08-02-1134-mcp-client-large-part2.md [p89], [p91]
  rejected-alternative: listing required tools in the YAML front matter
  endorsement: n/a

- statement: Not all prompt state reduces to files; structured data such as breadcrumbs requires a structured representation.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p96, p100]
  rejected-alternative: the file as the sole unit of state
  endorsement: n/a

- statement: All inference traffic bottlenecks through a single gateway process that enforces global concurrency limits across all apps, languages, and machines; loopback connections require no API keys, while remote intranet access uses whitelisted IPs or API keys.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p116]; 2026-08-02-1134-mcp-client-large-part2.md [p116]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompts can be exported as MCP tools via configuration, with the YAML front matter supplying everything needed to define the tool; the server monitors the prompt directory and refreshes its cache without restart as a developer convenience; and the server can itself act as an MCP client to other services.
  scope: mcp
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p122]; 2026-08-02-1134-mcp-client-large-part2.md [p122]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- Planning workflow preference: put everything in one plan, implement a working subset, subtract it, and iterate in tranches across the executor, gateway, and MCP service [p123].
- Repo bookkeeping preference: keep a status file (AGENTS.md at the root, not .mdc) that all changes must update so a fresh context knows the project state [p130, p131, p132].
- Doubt, unresolved: Lua will be used for general-purpose computation, so static detection of every tool call may not be reliable - this tensions with the load-time tool-discovery principle [p94].
- Open worries with no directive: Lua code going into an infinite loop, and tools gaining file read/write access through the Lua library [p92, p93].
- Design pressure, not a directive: many large per-tool schemas risk recreating the pydantic burden by shifting it into Lua [p84].

---

---
produced: 2026-08-19
title: PromptForge design principles mined from MCP client evening chat (tool-picker crate, frontmatter tool needs, classifier validation)
---

# 2026-08-02-2331-mcp-client-evening.md

```yaml
- statement: The Lua interface must be able to add every tool from an MCP client in one call, and to ask for a tool that matches a description.
  scope: boundary: lua<->mcp
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p11]; 2026-08-02-1034-mcp-client-harness.md [p11]
  rejected-alternative: requiring each tool to be named individually
  endorsement: n/a

- statement: Tool selection runs once at startup, locally, and must be universally available with no network dependency.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: A classifier-based design must be validated with real training data and measured tests before it is adopted into the system.
  scope: global
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p17]
  rejected-alternative: adopting the classifier on intuition without evidence
  endorsement: n/a

- statement: The tool picker depends only on an abstract tool-catalog type defined as its input contract, never on MCP; catalog producers feed it from outside.
  scope: boundary: tool-picker<->mcp
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p20]
  rejected-alternative: a direct MCP dependency inside the picker
  endorsement: n/a

- statement: The tool picker must not depend on Lua; the Lua verbs and context-rewrite hook are integration-layer work in the caller.
  scope: boundary: tool-picker<->lua
  source: user-corrective
  citation: 2026-08-02-2331-mcp-client-evening.md [p21]
  rejected-alternative: a Lua dependency inside the picker crate
  endorsement: n/a

- statement: Model weights are pinned, fetched at build time only if absent, kept out of git, and embedded into the library so any linked executable is self-contained with no external files.
  scope: global
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p22]
  rejected-alternative: checking the model into git, or shipping it as an external runtime file
  endorsement: n/a

- statement: Evaluation datasets live outside the crate they exercise.
  scope: global
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p28]
  rejected-alternative: none
  endorsement: n/a

- statement: The implementation repo must not refer to the design repo.
  scope: global
  source: user-corrective
  citation: 2026-08-02-2331-mcp-client-evening.md [p29]
  rejected-alternative: cross-references from the implementation repo to design documents
  endorsement: n/a

- statement: Tool resolution is deterministic: the same catalog, need, and config yield the same outcome across runs.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: The resolver returns tool descriptors, not concrete tools; the caller maps a chosen descriptor to an actual tool.
  scope: boundary: tool-picker<->core
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: returning dyn Tool and taking a dependency on the core crate
  endorsement: affirmed

- statement: Every distinct outcome of a resolution policy is exercised by its own test with a crafted mini-catalog.
  scope: global
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: affirmed
```

## Not converted

- [p9] The user reasons that the tool-indirection layer only buys one saved round of inference, and that needs stated in prose could drive the tools.add list directly; analysis on the way to [p10], not a standalone directive.
- [p13] Pasted research finding that tool routing should key on the (server_id, tool_name) pair rather than a concatenated string; the user asked what it meant but never adopted it.
- [p14] The user questions why hardening matters when they control all the MCP servers; a preference signal about threat-model scope, never resolved into a directive.
- [p18] Terminology question about "spike" as a term of art; teaching exchange only.
- [p31-33] The user weighs model tiers for subagent work, then declines to change anything and orders the run; temperament, not a rule.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 4 (goto context injection, state vars, facts bag, prefix-body-suffix, line-driven file tools)
---

# 2026-08-02-1134-mcp-client-large-part4

```yaml
- statement: State transfer between sections is a single operation; without a transfer mechanism, propagating state costs two tool calls instead of one.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p227], [p228]
  rejected-alternative: propagating state with two tool calls
  endorsement: n/a

- statement: goto performs direct context injection: the argument string is copied into a new context, its Lua is executed, and its prompt is run, with arguments resolved at the call site.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p229], [p230], [p231]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p229], [p231]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua chunks return values with Lua's native return semantics, not through a special identifier or descriptor convention.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p234], [p235]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p235]
  rejected-alternative: a declared identifier or descriptor inspected by the Rust side
  endorsement: n/a

- statement: A section reached by goto is not reusable as a function called from multiple sites, because control always transfers to the same destination afterward.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p242]
  rejected-alternative: treating return-goto as a reusable multi-call-site function
  endorsement: n/a

- statement: A tool takes a single string argument; the prompt itself deduces the structured values from that string as its first step and stores them.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p251]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p251]
  rejected-alternative: requiring the caller to infer structured arguments such as name and mission
  endorsement: n/a

- statement: State is carried as a key/value block written by Lua and injected into the context on every goto, with the executor choosing the enclosing tag.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p254], [p255], [p256]
  rejected-alternative: none
  endorsement: n/a

- statement: On a tool call in a multi-turn context, the facts bag is removed from the transcript, the tool results are injected, and then the facts bag is added back.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p257], [p258], [p259], [p260]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p257]
  rejected-alternative: leaving the facts bag permanently in the transcript
  endorsement: n/a

- statement: Every heading's context is prefix, body, and suffix: the prefix is inherited cumulatively by child headings, the body is throwaway, and the suffix floats.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p268], [p269], [p270], [p271]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p269], [p270], [p271]
  rejected-alternative: none
  endorsement: n/a

- statement: Parallel analysis is expressed by the prompt author as nested subsections over shared data, not by an explicit fanout mechanism or an engine-imposed cap.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p272], [p273], [p274]
  rejected-alternative: a fanout mechanism with engine-side caps
  endorsement: n/a

- statement: A design document holds only decisions and rationale; Rust types and code are removed from it as implementation proceeds, and the master plan tracks only unbuilt design.
  scope: global
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p280], [p310]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p280], [p310]
  rejected-alternative: design documents carrying Rust types and declarations
  endorsement: n/a

- statement: The engine exposes system constants - sys.when for the prompt's launch time and sys.now for the current time - and gives every context a unique incrementing id.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p284], [p285], [p286]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p284], [p285], [p286]
  rejected-alternative: none
  endorsement: n/a

- statement: The context must not accumulate permanent residue across turns.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p287], [p288]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p288]
  rejected-alternative: accumulating permanent entries in the context so the model can detect time passing
  endorsement: n/a

- statement: Context needs are declared by the prompt's Lua and injected by the engine; the model does not pull them.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p290]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p290]
  rejected-alternative: the model requesting context items itself
  endorsement: n/a

- statement: The engine implements all features and lets the caller decide among them, with sensible defaults.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p316]
  rejected-alternative: shipping a curated subset of features
  endorsement: n/a

- statement: File tools are line-number driven: the engine maps line numbers to character offsets for virtual and real files, and supports edit in place.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p343], [p344], [p347]
  rejected-alternative: character-range-only file addressing
  endorsement: n/a
```

## Not converted

- The best engineers are lazy; the best kind of feature delivers everything with the minimal implementation (p231).
- Earlier design documents are bloat to be mined for ideas, not followed (p232, p233).
- Build in the smallest testable increments: Lua first, then args, then substitution, with an echo tool as the first commit (p250, p276, p293).
- Every commit carries tests, code review, and docs, and each commit makes progress on its own rather than needing a later commit to realize it (p292, p312).
- Keep a lightweight vibe-coding addendum and inject it into the context periodically to keep it fresh (p297-p302).
- Loading a how-to-write-prompts guide into plans works like a miracle (p299).
- Prefix caching is irrelevant at 3B model scale; tiny context windows are what drive the context engineering (p258, p259).

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the context-planning chat (store inject trust split, explicit fanout, models.always)
---

# 2026-08-08-0029-promptforge-context-planning

```yaml
- statement: Accessing a name that is not in the sys table is a hard error, never a silent empty value.
  scope: core
  source: user-corrective
  citation: 2026-08-08-0029-promptforge-context-planning.md [p15]
  rejected-alternative: silently returning nil for unknown sys fields
  endorsement: n/a

- statement: Untrusted content injected into the model context is wrapped in a unique XML tag carrying a random nonce and prefaced by a notice that the enclosed text is data, not instructions.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p17]
  rejected-alternative: injecting stored content into the context raw
  endorsement: n/a

- statement: Content that forges the untrusted envelope's open or close tags is defanged before injection.
  scope: core
  source: ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The store's read API is split by trust and presentation: read_lines returns numbered lines for editing, read returns verbatim contents for trusted handoff, and inject returns verbatim contents inside the untrusted envelope for model-facing use.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p22]
  rejected-alternative: a single read call with a trusted/untrusted flag
  endorsement: n/a

- statement: Line numbers are a navigation and editing aid, not a security control; trust is carried by the untrusted envelope alone.
  scope: core
  source: ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: treating numbered output as safe for model consumption
  endorsement: affirmed

- statement: Section addresses are always explicit: APIs take the full markdown heading line including the ### marker, and a mismatch is a hard error that lists the available sibling headings in the same form.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p35]
  rejected-alternative: bare heading names without the ### marker
  endorsement: n/a

- statement: Fanout is always invoked explicitly through a fanout call; the engine never infers a fanout from the presence of a bullet list.
  scope: core
  source: ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: inferring fanout from bullets without an explicit call
  endorsement: affirmed

- statement: In a fanout, the list section supplies only items: it contains list prose and carries no Lua.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p35]
  rejected-alternative: colocating the arm's Lua with the bullet list
  endorsement: n/a

- statement: The subagent section is the arm template: its leading Lua is the shared preamble for every arm, its trailing Lua the shared epilog, and its prose substitutes the per-arm item.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p35]
  rejected-alternative: none
  endorsement: n/a

- statement: Each fanout arm runs in a fresh VM built from the shared template and receives its per-arm values (the item text and a task id) through a sealed sys, without overloading the section identity.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p47]
  rejected-alternative: overloading the section identity variable with per-arm data
  endorsement: n/a

- statement: The invoking Lua owns the reduce step: fanout is a blocking call that returns each arm's final reply in order, and store writes from arm epilogs stay visible to the reducer.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p33]
  rejected-alternative: none
  endorsement: n/a

- statement: The model's previous reply is bound as reply and can be substituted anywhere in the section, including the preamble, the prose, and the epilog.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p55]
  rejected-alternative: exposing reply only in the epilog
  endorsement: n/a

- statement: The entire markdown document is parsed once up front, so no markdown parsing happens at run time and a run-time syntax error is impossible or nearly so.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p62]
  rejected-alternative: parsing markdown lazily at run time, e.g. a bullets() call that takes raw markdown text
  endorsement: n/a

- statement: An operation belongs on the abstraction it acts on; pulling bullets out of markdown is not a store operation.
  scope: core
  source: user-corrective
  citation: 2026-08-08-0029-promptforge-context-planning.md [p60]
  rejected-alternative: store.bullets_from
  endorsement: n/a

- statement: A prompt can declare a prompt-wide default model binding once in the H1 shared library; a section that omits models.use inherits it, and a section can override it for itself.
  scope: core
  source: user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p83]
  rejected-alternative: repeating models.use in every section
  endorsement: n/a

- statement: Only one model can be the prompt-wide default, unlike tools where several can be always-on; default declarations live in the H1 shared library and must be declared before use.
  scope: core
  source: ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Fanout arm boundaries are logged as fixed, payload-free detail lines.
  scope: core
  source: ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- Wants the assistant to push back on weak designs and approve good ones, with more dialogue [p48].
- Prefers direct answers without hedging: "Don't fence answers" [p51].
- Security mechanisms must justify themselves: asked whether the data-not-instructions preface actually makes a difference [p26].
- Names should come from vocabulary every prompt writer already owns: "reply" is right because everyone understands "the model's reply" [p58].
- Floats naming ideas as questions, expecting discussion rather than immediate execution [p45].
- Ship the static form first and add the dynamic feature later [p63].
- Prefers compact tests, ideally plain markdown files and logging over Lua test harnesses [p70] [p71].
- Workflow discipline: one adversarial review per commit with fixes amended in, design doc and user docs kept current as work proceeds [p74].

---

# Design-principle candidates: 2026-08-14-1613-promptforge-core-largest-part2.md

```yaml
- statement: A failed tool.need fails the prompt immediately with an error.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p95]; 2026-08-09-1058-promptforge-core-large-part2.md [p95]
  rejected-alternative: continuing the run after a required tool fails to bind
  endorsement: n/a

- statement: There is exactly one tools.add entry point, not multiple variants.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p90]; 2026-08-09-1058-promptforge-core-large-part2.md [p90]
  rejected-alternative: multiple overloaded versions of tools.add
  endorsement: n/a

- statement: Whether model thinking is on or off is controlled by the prompt, not by the gateway.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p107]; 2026-08-09-1058-promptforge-core-large-part2.md [p107]
  rejected-alternative: a gateway-level thinking toggle
  endorsement: n/a

- statement: Models are declared in the prompt's introduction via models.add with attributes like thinking and context size, and a section selects its model with model("name").
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p108]; 2026-08-09-1058-promptforge-core-large-part2.md [p109]-[p112]
  rejected-alternative: declaring model settings in the frontmatter
  endorsement: n/a

- statement: Provider-specific special cases live in a single normalization layer so the rest of the engine talks to all models universally.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p122]; 2026-08-09-1058-promptforge-core-large-part2.md [p122]
  rejected-alternative: scattering per-provider special cases and one-off targeted fixes throughout the codebase
  endorsement: n/a

- statement: An empty model response is never acceptable; empty response is always a hard fail.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p124]; 2026-08-09-1058-promptforge-core-large-part2.md [p124]
  rejected-alternative: treating an empty response as a valid result
  endorsement: n/a

- statement: A tool call counts as a model response.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p126]; 2026-08-09-1058-promptforge-core-large-part2.md [p126]
  rejected-alternative: none
  endorsement: n/a

- statement: Each run deletes the previous trace on launch; a developer who wants to keep a trace backs it up himself.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p128], [p165]; 2026-08-09-1058-promptforge-core-large-part2.md [p128]
  rejected-alternative: accumulating trace files across runs
  endorsement: n/a

- statement: Model binding is much looser than tool binding and resolves through the same semantic picker used for tools.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p133]; 2026-08-09-1058-promptforge-core-large-part2.md [p133]
  rejected-alternative: strict model-name binding that fails hard on mismatch
  endorsement: n/a

- statement: When fetched evidence is unusable, the run aborts rather than continues, because a hallucinated evidence packet taints the entire downstream result.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p174]
  rejected-alternative: soft-returning fetch failures and letting the prompt hallucinate past them
  endorsement: n/a

- statement: Execution parameters such as context size, thinking, and resource caps are properties of the prompt, set in its lua, not in the frontmatter and not on the command line.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p154], [p205]
  rejected-alternative: frontmatter keys or command-line flags for context_max_tokens and no_think
  endorsement: n/a

- statement: Content injected into the context from external sources is treated as untrusted input.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p159], [p161]
  rejected-alternative: none
  endorsement: n/a

- statement: Errors reported to the prompt author include the prompt's line number.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p164]
  rejected-alternative: error messages without source line locations
  endorsement: n/a

- statement: A tool's call budget is declared at the tools.add call site.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p170]
  rejected-alternative: none
  endorsement: n/a

- statement: Turn limits are a property of the subagent, expressed as config.max_turns, and exhausting the budget removes all of the subagent's tools.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p175], [p176]
  rejected-alternative: attaching max_turns to individual tools
  endorsement: n/a

- statement: Tool selection is semantic; a prompt must never have to repeat a tool's description verbatim to get the tool invoked.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p193]
  rejected-alternative: verbatim matching of tool descriptions
  endorsement: n/a

- statement: Missing gateway credentials produce a clear, specific error rather than an opaque tool-bind failure.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p99]; 2026-08-09-1058-promptforge-core-large-part2.md [p99]
  rejected-alternative: failing the tool bind with no explanation when the token is absent
  endorsement: n/a

- statement: Integration tests require an already-running, already-configured gateway; the test never launches the gateway itself.
  scope: boundary: core<->gateway
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p201]
  rejected-alternative: tests spawning their own gateway instance
  endorsement: n/a

- statement: A small local model runs without the gateway so integration tests can exercise real inference with a simple setup.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p202]
  rejected-alternative: routing all test inference through the gateway
  endorsement: n/a
```

## Not converted

- Temperature should be zero for analytical pipelines [p105] - a usage preference, not an engine directive.
- The Observer API could grow a side channel for verbose debug logging [p105] - a floated question, never confirmed as a directive.
- Puzzlement that turning off thinking could ever be good [p106] - a teaching moment about model behavior, no rule.
- Architecture should be "lean, slender, and good" [p122] - temperament behind the normalization-layer principle, not itself a rule.
- If the store is a real filesystem, intermediate artifacts like evidence.md become useless files [p162] - a stated worry, no directive issued.
- Turnaround time on changes is painfully slow [p91] - impatience with the dev loop, no design rule.
- Reports should put date and model on their own italic paragraph at the bottom [p207] - a per-prompt output formatting choice, not engine behavior.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge.md Aug 16 midday session (mechanical execution, runtime metadata discovery, env file split, config key naming)
---

# 2026-08-16-1229-promptforge-md-aug16-midday

```yaml
- statement: Executing a "promptforge <name> [input]" command is mechanical - stand up the gateway and MCP server, make the call, report the result - with no exploration, analysis, or pre-validation.
  scope: global
  source: user-corrective
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p5]
  rejected-alternative: proactively poking around the filesystem and analyzing before making the call
  endorsement: n/a

- statement: The promptforge skill must state an unambiguous, explicit procedure for what to do when the "promptforge {prompt} {args}" command is given.
  scope: global
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p6]
  rejected-alternative: an open-ended instruction that invites interpretation
  endorsement: n/a

- statement: A prompt's parameter mapping is learned at runtime from the MCP server's description of the prompt's metadata, never hardcoded into the skill.
  scope: mcp
  source: user-corrective
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p7]
  rejected-alternative: hardcoding an understanding of args, input_file, and similar parameters into the procedure
  endorsement: n/a

- statement: PromptForge prompts are not advertised individually by the MCP server; discovering them requires querying the server first.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p8]
  rejected-alternative: per-prompt advertisement by the server
  endorsement: n/a

- statement: list_prompts is called once per session and the metadata stays in context; it is called again only when the user says the input/output contract changed.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p9]
  rejected-alternative: re-querying prompt metadata on subsequent invocations
  endorsement: n/a

- statement: The MCP server has a single flat environment file; hierarchical environment files belong to the gateway's configuration alone.
  scope: boundary: gateway<->mcp
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p17], [p18], [p24]
  rejected-alternative: attaching the hierarchical env-file scheme to the MCP service
  endorsement: n/a

- statement: Configuration key names follow the provider's own terminology - if Anthropic says API key, the config says API key.
  scope: global
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p24], [p28]
  rejected-alternative: inconsistent or invented key names across the repo
  endorsement: n/a

- statement: The MCP server's sole role is serving PromptForge prompts; capabilities beyond that, such as proxying to external MCP services, do not belong in it.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p27]
  rejected-alternative: building an MCP proxy or other non-prompt-serving features into the MCP server
  endorsement: n/a

- statement: Running a prompt separates one-time setup (gateway, MCP server, metadata discovery) from the repeatable call, so subsequent invocations skip straight to the call.
  scope: global
  source: ai-proposed
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [plans section]
  rejected-alternative: repeating the full setup procedure on every invocation
  endorsement: affirmed

- statement: A prompt call is error-driven - the agent calls run_prompt without checking whether the prompt exists and reports whatever comes back, letting the server's error be the feedback.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [plans section]
  rejected-alternative: pre-validating the prompt's existence before calling
  endorsement: affirmed

- statement: Procedural obligations embedded in prose get skipped; a printable per-step checklist with checkboxes makes required actions (like committing) mechanically visible and gates the next step on completion.
  scope: global
  source: ai-proposed
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [plans section]
  rejected-alternative: a numbered per-step procedure in prose
  endorsement: affirmed
```

## Not converted

- Curiosity about the difference between an API key and a bearer token; a terminology question that informed the rename but carries no directive. [p26]
- Open question the user left unresolved: how does a PromptForge prompt call an MCP service that is not a PromptForge prompt - an MCP proxy in the gateway was floated, not decided. [p27], [p29], [p30]
- Musing on whether more thinking would have prevented the skipped commits; a temperament question, not a directive. [p38]
- promptforge.md names local/prompts.toml as the prompt registry. (Config-location fact, not a behavior.) [p4]
- The gateway should read gateway.toml from promptforge/local. (Config-location decision, not a behavior.) [p13], [p14]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge.md session Aug 19 (untrusted global, shared-chunk replay, heading-level uniformity, execute chains, fanout collections)
---

# 2026-08-19-0048-promptforge-md-aug19

```yaml
- statement: Wrapping untrusted content is a global function untrusted(s) that takes any string and wraps it with the injected tag and the machine instruction to treat the contents as data, not instructions; it is not a method on store.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p3], [p4], [plans section]
  rejected-alternative: an inject method on the store (store.inject is removed, not kept as sugar)
  endorsement: n/a

- statement: A prompt-facing break such as removing store.inject is accepted without bumping the promptforge frontmatter version off 1; it is not an engine major.
  scope: global
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p4], [plans section]
  rejected-alternative: versioning the engine major for prompt-facing breaks
  endorsement: n/a

- statement: log is available in both the shared chunk and the section chunks.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p6]
  rejected-alternative: none
  endorsement: n/a

- statement: The shared chunk is compiled once under a minimal environment (log only) so compile errors surface before any section runs; each section run then builds a fresh VM, installs the full host environment, replays the shared chunk, and runs the section's chunks, with an empty compiled chunk substituted when no shared section exists so the startup path is unconditional.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p7], [plans section]
  rejected-alternative: branching section-startup logic on whether a shared section was specified
  endorsement: n/a

- statement: During shared-chunk replay, tools, models, var, reply, and jump are blocked at the top level (a hard phase error naming the blocked global) while remaining available inside shared functions called later.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p9], [plans section]
  rejected-alternative: replaying with the full environment and tightening later
  endorsement: n/a

- statement: store.read takes a line range as (startLine, endLine), not (startLine, lineCount), because every line is tagged with its absolute number and a count form would force subtraction.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p12], [p17], [p18]
  rejected-alternative: a (startLine, lineCount) range form
  endorsement: n/a

- statement: Line numbering is provided by a dedicated store.read_numbered, not by a global numbered() function that composes strings in memory.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p16]
  rejected-alternative: a global numbered() function useful only when manipulating a composed string in memory
  endorsement: n/a

- statement: list_from_section(name) is a free function returning a section's bullet items as an array of strings; it can access only sibling sections at the same nesting level and child sections, and fanout's second parameter is always a collection, with each arm's item arriving as one member's Lua value.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p22], [p23], [p24]
  rejected-alternative: none
  endorsement: n/a

- statement: Subroutines and fanout workers are shared by making them siblings of the sections that use them; the scoping rules must include siblings or sharing is impossible.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p25], [p49]
  rejected-alternative: none
  endorsement: n/a

- statement: A horizontal rule "---" marks a section to be skipped by execution and fall-through, and content after it is expository prose for the reader that does not affect execution; the rule is uniform with no special casing (the blank line is required), and skipping applies even when the rule appears at the start of a section reached by a chain.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p26], [p30], [p32], [p35], [p65]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p382-p389]
  rejected-alternative: special-cased parsing of horizontal-rule placement
  endorsement: n/a

- statement: Heading levels execute under identical rules at every level: an H3 falls through to the next H3 exactly as an H2 falls to the next H2, and "---", jump(), and execute() work the same way at each level, scoped to that heading's siblings and its children one level down.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p39], [p40]
  rejected-alternative: per-level execution semantics
  endorsement: n/a

- statement: Fall-through never crosses heading levels; the transfer from HN to H(N+1) must be explicit (jump or execute), and once the transfer happens the sibling walk proceeds normally at the deeper level.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p41]
  rejected-alternative: implicit fall-through from a parent level into its children
  endorsement: n/a

- statement: execute() starts a new chain that runs to its end, like calling a different prompt whose pieces happen to live in the same file; it is recursive, and when the chain ends its reply is returned to the caller of execute.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p55], [p58], [p60]
  rejected-alternative: an asymmetric model where an execute-entered subroutine runs under JumpPolicy::Reject while a jump-entered one may jump
  endorsement: n/a

- statement: With subroutines, jump, and goto allowed, the same hazards as any programming language apply (infinite loops, wrong targets, unpredictable behavior); coherence is the prompt author's responsibility, not the engine's.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p60]
  rejected-alternative: engine-enforced guardrails on control flow
  endorsement: n/a

- statement: Fanout arms are not special-cased: arms can jump, execute, fanout, and list_from_section like any section.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p78], [p79]
  rejected-alternative: stubbed control globals in arms (jump rejected, execute/fanout/list_from_section failing loudly)
  endorsement: n/a

- statement: There is no limit on the total number of fanout items, only a limit on concurrent fanout.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p80]
  rejected-alternative: a total item cap (max_fanout_items)
  endorsement: n/a

- statement: Work lands in individual commits that can each be tested, and every commit pays down technical debt: review the whole of every file touched, combine or eliminate functions, remove the obsolete, and take available simplifications.
  scope: global
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p21], [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: Tests cover the absence of behavior (removed names erroring, blocked actions failing, invalid inputs rejected) and not only the presence of new behavior.
  scope: global
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p21], [plans section]
  rejected-alternative: testing only what was added
  endorsement: n/a

- statement: Captured bindings install after the shared replay, so a tool or model alias wins a name collision with a shared global.
  scope: core
  source: ai-proposed
  citation: 2026-08-19-0048-promptforge-md-aug19.md [plans section]
  rejected-alternative: installing captured bindings before replay
  endorsement: affirmed

- statement: fanout's second parameter dispatches on type: a string names a list section, an array table is the collection, and anything else is a loud Lua error.
  scope: core
  source: ai-proposed
  citation: 2026-08-19-0048-promptforge-md-aug19.md [plans section]
  rejected-alternative: silently iterating a hash-keyed table in unstable order
  endorsement: affirmed
```

## Not converted

- Prefer shipping the permissive, simpler design now and tightening later with evidence ([p11]); in tension with the replay gate that was ultimately adopted.
- A correct generalization should simplify the implementation by eliminating special cases ([p43], [p60]).
- Ask for evidence before choosing an API shape, then answer from first principles when the evidence is already in hand ([p17], [p18]).
- Efficiency instinct: an API that forces reading 5,000 lines to extract 400 is wasteful ([p15]).
- Delight in elegant synthesis wherever it comes from; the jump-into-child-walk solution was found by the AI and credited as luck ([p66]-[p72]).
- Plans should stand alone ([p81]).

---

---
produced: 2026-08-19
title: PromptForge design principles mined from architect-vibe-planning part 2 (vibe methodology, prompt compression)
---

# 2026-07-28-0207-architect-vibe-planning-part2.md

```yaml
- statement: Everything the executor does runs in subagents, in parallel when possible, so the main context and the plan stay potent; attention to recent content degrades as old material fills the context.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60] [p84]
  rejected-alternative: doing work in the main context
  endorsement: n/a

- statement: Every step of an implementation plan ends with working code, real non-trivial tests, and a checkpoint of finished functionality.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: none
  endorsement: n/a

- statement: After every commit the AI reviews its own code, red-teams the tests, removes the technical debt it finds, verifies the tests pass, and amends the commit instead of adding a new one.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: committing first and cleaning up in later commits
  endorsement: n/a

- statement: Before implementing anything, the executor spawns subagents to search the web for current information about what it is about to do, unless it is certain it already knows.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: relying on the model's prior knowledge
  endorsement: n/a

- statement: Plans are refined hierarchically: a high-level ordered plan, then a finer-grained plan per component, decomposed until each step is the smallest unit of functionality that leads to a testable thing.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: none
  endorsement: n/a

- statement: Implementation begins only from a design document whose high-level decisions are already made, so the model's only job is to implement.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: letting the model make high-level decisions during implementation
  endorsement: n/a

- statement: Design decisions the AI makes during implementation are recorded in a per-crate design.md, with a top-level design document holding the cross-package decisions.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]; 2026-08-02-2331-mcp-client-evening.md [p30]
  rejected-alternative: none
  endorsement: n/a

- statement: Comments appear only where something is surprising or non-standard; code is never annotated with restatements of the obvious.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: narrating code line by line
  endorsement: n/a

- statement: Code hygiene rules are language-independent, general principles (DRY, single responsibility) expressed as unambiguous tests that can be applied to AI-written code.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: language-specific style rules
  endorsement: n/a

- statement: A compressor must never expand its input; when it cannot find a shortening, it emits the input verbatim.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p62] [p82]; 2026-07-28-0207-architect-vibe-planning-part1.md [p57]
  rejected-alternative: none
  endorsement: n/a

- statement: Compression is idempotent: a second compression pass over the output changes nothing.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p71] [p82]
  rejected-alternative: none
  endorsement: n/a

- statement: Compression must be smart generative rewriting, not the deletion of tokens.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p81]
  rejected-alternative: LLMLingua-style subtractive token dropping
  endorsement: n/a

- statement: The compressor is single-purpose: it compresses and does nothing else, with no tool calls and no thinking.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p70]
  rejected-alternative: a general-purpose model that also compresses
  endorsement: n/a

- statement: Generated prose must not contain formulaic AI rhetorical tics such as "This is not merely an observation" or "deserves emphasis rather than apology".
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p99] [p108] [p110]
  rejected-alternative: a length pass that leaves the rhetorical patterns in place
  endorsement: n/a

- statement: Every sentence in a written artifact must justify its presence; anything not needed is cut.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p113]
  rejected-alternative: none
  endorsement: n/a

- statement: During plan implementation the plan file itself is never edited.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p103] [p105]
  rejected-alternative: none
  endorsement: n/a

- statement: The plan file is preserved and evolved across the session and kept compressed so it stays potent.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p95]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- Compression is the most valuable substance in the AI universe; the antislab. [p67]
- Start from the most compressed version of the idea, the highest-frequency signals; the chat itself is the substance and the human supplies the decision-making. [p68]
- Distrust quick confident answers; demand to see the actual mechanism, not a simulation of one. [p85]
- A report should open experientially and take the reader on the same journey the author took. [p94]
- An illustrative example may be approximate if it is close enough to reality to teach the reader. [p98]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from compaction-algorithm session part 4 (goto args, Lua return, fork rendezvous, context prefix inheritance, sys constants)
---

# 2026-07-30-1046-compaction-algorithm-large-part4

```yaml
- statement: A rendezvous section that is data-dependent on multiple fork arms waits until every arm it depends on has completed before it executes.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]; 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247]
  rejected-alternative: none
  endorsement: n/a

- statement: Propagating state is a single tool call carrying all values at once, not one tool call per value.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p228], [p265]; 2026-08-02-1134-mcp-client-large-part4.md [p265]
  rejected-alternative: one set call per value, requiring multiple tool calls to move state
  endorsement: n/a

- statement: Running a plan generates the design document after implementation completes, so the document is always in sync with the built code.
  scope: global
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p318], [p319]
  rejected-alternative: generating the design document before or separately from the implementation
  endorsement: n/a
```

## Not converted

- "The best engineers are lazy" - the best feature gives everything for the minimal implementation (p231).
- design-promptforge.md is overengineered bloatslop; mine it for ideas only (p232, p233).
- Build in the smallest testable increments: Lua plus args plus substitution first, "echo" as the first commit, fall-through as one testable thing (p250, p276, p293).
- Args without Lua is too little; Lua is needed to return values (p277, p278).
- Prefix caching is irrelevant at 3B; a 3B model has a tiny context window (p258, p259).
- The consolidated single tool call existed because small-model sections were assumed to need many call kinds at once; large models may not need it (p224, p225).
- Each commit must have tests, code review, docs, and user docs, and each commit must make self-sufficient progress rather than needing a later commit to retroactively realize it (p292, p312).
- Wants a lightweight vibe-coding how-to, roughly one fifth of how-to-vibe-code, injected into context periodically (p297-p302); loading how-to-write-prompts.md into plans "works like a miracle" (p299).
- Implement all features and let the caller decide, with sensible defaults (p316).

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client and agentic harness session (tool needs, choose_mcp_tool, context rewrite, resolver crate)
---

# 2026-08-02-1034-mcp-client-harness

```yaml
- statement: A prompt declares its tool needs at load time as a list of local aliases, each paired with a plain-language description of the capability it needs, and the harness binds each alias to the best-matching available tool.
  scope: core
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p39]; 2026-08-02-2331-mcp-client-evening.md [p10]
  rejected-alternative: none
  endorsement: n/a

- statement: Need strings are written in the prompt author's register as clean, parameter-free capability descriptions that read like a tool's own documentation, not as runtime user utterances; authors typically paraphrase the description of the tool they already intend to use.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p58], [p60]
  rejected-alternative: using runtime user utterances as the need-string distribution
  endorsement: n/a

- statement: Tool resolution runs locally with no LLM in the resolution machinery.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p27]
  rejected-alternative: an LLM-based matcher in the resolution path
  endorsement: n/a

- statement: Static launch-time binding (add_need) and dynamic runtime discovery (choose_mcp_tool) are complementary surfaces that share one resolution engine; neither replaces the other.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: Dynamic tool discovery is an opt-in surface the prompt author selects explicitly; it is the only path when chosen, not an escalation path the engine falls into on its own.
  scope: mcp
  source: user-corrective
  citation: 2026-08-02-1034-mcp-client-harness.md [p63], [p64]
  rejected-alternative: dynamic selection as an escalation path entered automatically
  endorsement: n/a

- statement: Dynamic tool selection returns a tool descriptor (name, description, input schema), never an invocation: one descriptor on a clear win, a shortlist on a genuine tie, and a "no tools available" error on absence.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: On dynamic resolution the harness rewrites the context so the chosen tool descriptor sits before the prompt prose and the discovery exchange is excised, then re-generates; a dynamically discovered tool lands in the identical execution state as a statically bound one.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p67]
  rejected-alternative: appending the discovery results to the context
  endorsement: n/a

- statement: Selection among a returned shortlist happens in the main context, which the author already governs (model choice, rewrite opt-out, instructions), rather than in a separate subcontext that would need its own model and configuration answers.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p70], [p71]
  rejected-alternative: a dedicated selection subcontext with its own model configuration
  endorsement: n/a

- statement: A prompt can use a strong reasoning model to select a tool, then a context-clearing goto to pass the tool descriptor into a fresh context where a cheaper model executes.
  scope: core
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p72]
  rejected-alternative: none
  endorsement: n/a

- statement: Duplicate tools within the author's own catalog are a configuration error and fail loud; duplicates arising from intentionally imported foreign servers must have an explicit disambiguation path.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p61]
  rejected-alternative: silently picking one of the duplicates
  endorsement: n/a

- statement: Absence of a matching tool fails loud; abstention is a first-class resolution outcome, not an afterthought.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p61], [p66]
  rejected-alternative: binding to the nearest tool regardless of confidence
  endorsement: n/a

- statement: Tool annotations (such as readOnlyHint or destructiveHint) may improve resolution confidence or break ties, but resolution must work without them; they are never required.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p56]
  rejected-alternative: depending on annotations as a necessary input
  endorsement: n/a

- statement: Tool identity is the (server, tool) pair; routing keys on the pair, not on a concatenated name string.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p13]
  rejected-alternative: routing on a concatenated server-plus-tool name string
  endorsement: n/a

- statement: Crates are kept small enough that a coding LLM can hold an entire crate in a single context window.
  scope: global
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p79]
  rejected-alternative: none
  endorsement: n/a

- statement: The tool resolver lives in its own crate, separate from the MCP protocol client, so protocol-only consumers (such as the CLI) do not carry the matching model.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p78], [p79]
  rejected-alternative: embedding the resolver in the MCP client crate
  endorsement: n/a

- statement: Resolution is gated on a similarity floor plus a top-1-vs-top-2 margin, yielding four outcomes: clear bind, own-catalog ambiguity (fail loud), foreign-server ambiguity (surface a shortlist), and absence (fail loud).
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1034-mcp-client-harness.md [design-mcp-toolpicker.md section]; 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Because the right tool is almost always in the top few candidates, resolution surfaces a shortlist for a well-informed decider to settle near-ties rather than forcing a single top-1 answer.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1034-mcp-client-harness.md [rationale.md section], [p25], [p26], [p69]
  rejected-alternative: forcing a single top-1 binding in all cases
  endorsement: affirmed
```

## Not converted

- Skepticism about hardening when the operator controls all MCP servers: "why do I care about all of this hardening if I control all the mcp servers?" [p14]
- Preference for partial fine-tuning that buys a bounded improvement without degeneracy, rather than going "all the way" [p22]
- Eval data should be generated by multiple models (ChatGPT, Claude, Gemini, Cursor) to avoid same-generator bias [p51]
- Working style: run all jobs asynchronously so the conversation can continue [p23], [p46]
- Inspect raw data samples together before committing to a theory ("pick 30 descriptions at random... let's look at it together") [p57]
- Plans should ship with a separate rationale document that mines the chat history and explains the why behind the design [p82]
- A fast, high-confidence "trivial reject" stage may drop clearly mismatched tools before finer matching, tolerating false negatives but never false positives [p55]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from modify-the-store (store input files, MCP gateway file mapping, sandboxed file IO)
---

# 2026-08-15-1851-modify-the-store

```yaml
- statement: The executor receives a store instance as a parameter; the store is not part of the prompt.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p2]
  rejected-alternative: none
  endorsement: n/a

- statement: File-in/file-out prompt execution runs against an in-memory store so a run performs no disk IO.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p1]
  rejected-alternative: reading and writing real disk files during the run
  endorsement: n/a

- statement: A prompt is agnostic to how its inputs arrive; the executor exposes only a store, and the gateway translates between the calling environment and the executor.
  scope: boundary: mcp<->core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p12]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway owns the store lifecycle: it seeds inputs, hands control to the prompt, then regains control and decides the disposition of outputs.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p4]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway reads caller-specified input files into the store itself; file contents never pass through the orchestrating model's tokens.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p6]
  rejected-alternative: the orchestrator inlining existing file contents into the tool call
  endorsement: n/a

- statement: A caller supplies each input as either a file path or inline text; the gateway normalizes both into the store and the prompt never knows which.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: Supplying both an input file and input text for one input is a validation error at the gateway.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p23]
  rejected-alternative: silently accepting both
  endorsement: n/a

- statement: Output files are written to real filesystem paths chosen by the caller; permissions and authorization are the orchestrator's responsibility, not the gateway's.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p5]
  rejected-alternative: the gateway managing output permissions itself
  endorsement: n/a

- statement: The gateway has the option to inline an output file in its response instead of writing it to disk.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p21]
  rejected-alternative: none
  endorsement: n/a

- statement: The MCP server maps caller inputs to the store deterministically, without using inference.
  scope: mcp
  source: user-corrective
  citation: 2026-08-15-1851-modify-the-store.md [p18]
  rejected-alternative: an inference-based mapping of caller inputs to store entries
  endorsement: n/a

- statement: MCP tool schemas are kept as small as possible so smaller models can fill them in correctly.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p13]
  rejected-alternative: none
  endorsement: n/a

- statement: Textual args remain separate from file inputs so a caller can attach additional commands alongside a file input.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p19]
  rejected-alternative: merging file inputs into args
  endorsement: n/a

- statement: Prompts declare expected input and output files in frontmatter as store-relative paths, with descriptions used for documentation and MCP schema generation.
  scope: core
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: When a prompt declares input files, the server validates that every declared input has a supplied value, rejects the call if any are missing, and seeds the store before execution.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Output extraction is best-effort: a declared output the prompt never wrote is returned as absent rather than failing the run.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: failing the run when a declared output is missing
  endorsement: affirmed

- statement: Default configuration enables no tools; every tool is opt-in so the sandbox is real.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p47]
  rejected-alternative: registering WebFetch and WebSearch by default
  endorsement: n/a

- statement: The gateway is started first; the MCP server and the dev runner both call through it.
  scope: global
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p38]
  rejected-alternative: none
  endorsement: n/a

- statement: Local MCP prompts live in a gitignored directory; dropping a prompt file into it makes the prompt live.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p40]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt containing only Lua, with no prose outside code fences, runs without a gateway.
  scope: core
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [design docs section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: LLM-facing quickref documentation is compressed to minimal tokens, and references other repo files rather than restating their contents.
  scope: global
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p36]
  rejected-alternative: duplicating YAML format and prompt structure documentation inside the quickref
  endorsement: n/a
```

## Not converted

- [p13] Hesitation about gateway-side URL fetching: if the model might do the fetching itself, gateway fetching becomes ambiguous. Unresolved preference, no directive landed.
- [p19] Open question whether the common one-file-in/one-file-out case deserves its own special syntax. Floated, never decided.
- [p27] Documentation workflow preference: integrate new design into the existing per-crate design docs instead of generating a new document. Process directive, not engine behavior.
- [p34] Rule-authoring philosophy: loosen a workspace rule with an "unless" clause and tighten rulebooks into standalone imperatives. About rule governance, not PromptForge.
- [p56] Temperament about verified work: every commit must have tests that were actually run, confirmed commit by commit. Process demand, not a design principle.
- [p58] Session-reuse goal for the quickref: services launched once should be remembered and reused across repeated prompt runs in the same chat. A doc purpose statement, not a directive on the engine.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core large session part 2 (prompts p79-p155)
---

# Design principle candidates: 2026-08-09-1058-promptforge-core-large-part2.md

```yaml
- statement: Misusing an API function produces a warning rather than silent wrong behavior.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p86]
  rejected-alternative: silently accepting the wrong function with no warning
  endorsement: n/a

- statement: Prompt code fences carry the bare lua tag with no extra annotation word.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p87]
  rejected-alternative: a "lua prompt" fence tag
  endorsement: n/a

- statement: Prompt configuration is written as Lua calls in the prompt body, never in frontmatter.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p108], [p154]
  rejected-alternative: frontmatter configuration
  endorsement: n/a

- statement: A subsection inherits its parent section's model unless it specifies its own.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p142]; 2026-08-14-1613-promptforge-core-largest-part2.md [p142]
  rejected-alternative: non-inheriting model resolution
  endorsement: n/a

- statement: Analytical pipelines run at temperature zero.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p105]
  rejected-alternative: nonzero temperature for analytical work
  endorsement: n/a

- statement: Recoverable web_fetch failures soft-return instead of hard-failing.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p146]
  rejected-alternative: hard-failing the prompt on a recoverable fetch error
  endorsement: n/a

- statement: Runs are observable: logs expose what the engine wrote into each produced artifact.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p97], [p105]
  rejected-alternative: logs that omit what went into run artifacts
  endorsement: n/a

- statement: Models are reached through the gateway rather than through bespoke direct wiring in the test harness.
  scope: boundary: core<->gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p140]
  rejected-alternative: wiring a local model directly into core-tests, bypassing the gateway
  endorsement: n/a
```

## Not converted

- Minute-scale per-prompt latency is treated as a defect worth attacking, not a fact of life [p81], [p91].
- Heavyweight process rulebooks get lightened when they slow the development loop [p116].
- Review loops stop after one round of amend; more rounds only surface noise [p117].
- Architecture should be lean and slender; scope creep that later proves necessary is accepted by definition, because that is what normalizing means [p122], [p124].
- Abstraction risks such as trait cosplay are discounted when removal is trivially easy [p124].
- Defaults are interrogated against intuition before acceptance, as with the skepticism that turning off thinking could help analysis [p106].

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core largest session part 4 (p327-p375)
---

# 2026-08-14-1613-promptforge-core-largest-part4.md

```yaml
- statement: The store exposes real files and virtual (memory) files at the same time; both are available concurrently, not as mutually exclusive modes.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p367]; 2026-08-09-1058-promptforge-core-large-part4.md [p367]
  rejected-alternative: a store model that supports only one kind of file at a time
  endorsement: n/a

- statement: Sandboxing applies to the prompt-facing tool surface, not to the Lua API; Lua code can read and write both real files and memory files.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p368]; 2026-08-09-1058-promptforge-core-large-part4.md [p368]
  rejected-alternative: sandboxing Lua so it cannot write files
  endorsement: n/a

- statement: No parallel mechanisms; a single, small, well-designed set of primitives services all needs, and an existing mechanism such as tool scoping is leaned on as far as it can go before anything new is added.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p371]; 2026-08-09-1058-promptforge-core-large-part4.md [p371]
  rejected-alternative: adding a new mechanism alongside an existing one that already covers the need
  endorsement: n/a

- statement: Tools support multi-turn interaction, because tools that do coding work such as refactoring a source file need sustained access across turns.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p370]
  rejected-alternative: single-turn tool calls only
  endorsement: n/a

- statement: Explicit user opt-in legitimizes otherwise restricted behavior; consent is the gate for powerful capabilities.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p374]
  rejected-alternative: restricting the behavior outright regardless of user consent
  endorsement: n/a
```

## Not converted

- Empirical tuning temperament: A/B test model features (thinking on/off) and adjust parameters until no axis shows further improvement. [p346]
- Autonomous execution working style: run the plan without stopping until no reliable progress remains, keeping code clean with a review every three commits. [p348]
- Deliberation before action: discuss a plan from all angles with pros and cons before editing it. [p369]
- Cost-of-change as a decision input: before adopting a design, ask how much churn it would cause in the source. [p374]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge-core largest session part 5 (first-class tools/models, section lifecycle, lua shared, H1-once, file-backed store)
---

# 2026-08-14-1613-promptforge-core-largest-part5

```yaml
- statement: An analytical pipeline persists intermediate outputs as files so that any step can be re-run during development and debugging.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p377]
  rejected-alternative: none
  endorsement: n/a

- statement: The overlay store is integrated into the core engine, not packaged as a separately loadable tool, because it affects the Lua mount.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p380]
  rejected-alternative: overlay as a tool loaded separately from core
  endorsement: n/a

- statement: Prompts are written agnostic of the tool backend; the prompt says "search", never "search the web", and the tool's name and description are established by tool.need and can be rewritten when the tool is injected.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p383], [p386]
  rejected-alternative: hardcoding the backend into prompt text and tool descriptions
  endorsement: n/a

- statement: Behavioral variation of a prompt comes from ahead-of-time configuration; the orchestrating model cannot reshape the Lua at runtime the way an agentic host reshapes instructions.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p392]
  rejected-alternative: runtime reinterpretation of the pipeline by the model
  endorsement: n/a

- statement: Terminology is fixed and enforced repo-wide: the preamble is the H1 code, while prologue and epilogue belong to sections.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p393], [p395]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool and Model are first-class Lua objects (tables) that can be inspected and invoked, which also makes them mockable in unit tests; the preamble can declare globals such as lists of tools usable in any section.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p398], [p400], [p401]
  rejected-alternative: none
  endorsement: n/a

- statement: The toolset is not sealed at the first inference; tools.add between inference rounds within a section must keep working.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p409]
  rejected-alternative: sealing the toolset when infer begins
  endorsement: n/a

- statement: Prose lives in markdown sections where it can be richly formatted, never as string literals embedded in Lua code.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p427]
  rejected-alternative: passing prose as strings to model:infer()
  endorsement: n/a

- statement: A section is a sequence of alternating lua and prose blocks; non-final prose blocks are single-shot and always fall through, the final prose block runs the full tool loop until a reply with no tool call, and one conversation grows across all blocks of a section and is cleared between sections.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p479]-[p487]
  rejected-alternative: none
  endorsement: affirmed

- statement: Sections are subroutines: execute("## Name") runs a section in a fresh VM and returns its reply, while jump("## Name") transfers control with a context-clearing, no-return goto; the default remains running sections in order.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p242]
  rejected-alternative: treating goto-with-return as a reusable function callable from many places
  endorsement: n/a

- statement: The control-transfer function is named jump() because goto is reserved in Lua, and the rename is swept across the entire repo as the first step of the work.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481]
  rejected-alternative: exposing sections through _G, or keeping the name goto()
  endorsement: n/a

- statement: The H1 preamble runs exactly once as a live preamble; per-section replay is abandoned because replay multiplies inference cost and corrupts state once the preamble can infer or write to the store.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p446], [p470]
  rejected-alternative: two-phase preamble treatment and shared-bytecode re-execution in section VMs
  endorsement: n/a

- statement: A single "```lua shared" chunk per prompt is parsed into bytecode but not executed during the preamble; a second one, or one appearing after the H1 ends, is an error.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p461], [p462], [p474]
  rejected-alternative: generic VM serialization and cloning to share functions
  endorsement: n/a

- statement: Every commit that changes the prompting language also updates the user guide in the same commit, adding or deleting sections so the guide is correct for each commit.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p478]
  rejected-alternative: none
  endorsement: n/a

- statement: A name is a design decision and must say how the mechanism works, so there is no confusion.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p473]; 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: n/a

- statement: The store is a virtual filesystem for file-shaped intermediate values in analytical pipelines; it is strictly for debugging and resume, not a general-purpose filesystem for agentic coding, which is a different class entirely.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p504], [p505]
  rejected-alternative: a general-purpose filesystem supporting string replacement and delta application
  endorsement: n/a

- statement: The engine has no defaults and no self-chosen behavior; the caller provides every path explicitly, because the whole system is designed to make things explicit.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p506]
  rejected-alternative: engine-provided default paths
  endorsement: n/a

- statement: All Lua is compiled at parse time so a successfully parsed Prompt is fully syntax-validated; there is one VM per whole section; the store is the only intentional mutable channel across sections, with functions, closures, globals, var, tools, and reply branch-local by construction; mutable run-global Lua is explicitly excluded.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: none
  endorsement: corrected

- statement: Wire quirks (field synonyms, empty content, null-content tool calls) enter through one normalizer door so hosts stay dumb; a final turn with no tool calls and empty content is a hard error even when reasoning is present; reasoning_content is never promoted into the answer.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: completion normalize layer]
  rejected-alternative: adopting an external crate (genai, rig) instead of an in-core seam
  endorsement: unaddressed

- statement: Fanout fires all arms at once with the gateway queue as the throttle; replies stay ordered by arm index; fail-fast aborts sibling arms and propagates the first error; the store stays shared and mutex-safe, so authors must not assume arm N sees arm N-1 writes.
  scope: boundary: core<->gateway
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: Fanout and gateway concurrency]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- [p384], [p388] Open question on tool-naming training bias (snake_case vs single word vs WebSearch); no directive reached.
- [p401] Temperament: "you always encapsulate, you always model" as general programming hygiene.
- [p412] Observation that the only point of the phase transition is to protect the epilog; analytical, not a directive.
- [p448]-[p451] Exploration of generic VM serialization and cloning (with an ID-table scheme for Rust userdata); abandoned in favor of "lua shared".
- [p500], [p501] Housekeeping preference: trim loose design/status files that create noise.
- [p508] Feature spec for a promptforge-dev option to create a same-named directory next to a tool; implementation detail, not a behavior principle.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from repo review continued session (fresh contexts, findings-driven API redesign, independent source audit, fix-forward retry, de-inlined rulebooks, lean prompts)
---

# 2026-08-11-1510-repo-review-continued

```yaml
- statement: Review and modification are separate phases: all findings for a crate are gathered before any file is modified, and the complete findings set is what drives the changes.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p1]
  rejected-alternative: interleaving review and fixes file by file
  endorsement: n/a

- statement: A redesign is derived from the complete findings set: each API change must both reduce the chance of a finding recurring and make the surface smaller and more robust; change for change's sake is rejected.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p1], [plans section]; 2026-08-10-0856-repo-review-top-to-bottom.md [p1]
  rejected-alternative: fixing findings one by one in place without rethinking the API
  endorsement: n/a

- statement: Stages that consume a previous stage's output run serially; only independent per-unit work runs in parallel.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: parallelizing stages that depend on each other's artifacts
  endorsement: affirmed

- statement: Every finding receives an explicit disposition: fixed, or rejected with specific contrary evidence.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: letting findings drop silently
  endorsement: affirmed

- statement: Completion is judged by an independent fresh-context audit of the actual source, not by the worker's self-report and not by gates alone; compile, lint, and test gates do not catch behavioral or design findings.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p24], [plans section], [design documents section]; 2026-08-10-0856-repo-review-top-to-bottom.md [plans section], [p24]
  rejected-alternative: trusting the fix agent's own all-green report
  endorsement: affirmed

- statement: On verification failure, fix forward: the verifier's concrete file:line NOT-FIXED list goes back into a fixer on the same candidate, and discard-and-restart happens only when progress stalls or the round budget is spent.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p54], [plans section]
  rejected-alternative: discarding a mostly-correct candidate and restarting blind from the original head
  endorsement: affirmed

- statement: The intended public API is machine-checked against the actual public API; drift between them fails verification.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p31], [p32], [plans section]
  rejected-alternative: hand-maintained API inventories
  endorsement: affirmed

- statement: A prompt whose subagents share its run and filesystem references shared rulebooks by path instead of inlining them; inlining shared rules into each prompt is the anti-pattern, and only artifacts read by a non-sharing reader inline their rules.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p53], [plans section]
  rejected-alternative: inlining rulebook blocks into the tool prompt
  endorsement: n/a

- statement: A prompt artifact that has grown to thousands of lines is defective and gets compressed: tighten every instruction, one instruction per line, delete hedges, quantify every quantity.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p52], [p53], [plans section]
  rejected-alternative: accepting bulk as the natural cost of completeness
  endorsement: n/a

- statement: When a design changes, the new design is written as one fresh document, the residue goes into a separate document, and the superseded documents are deleted.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p6]
  rejected-alternative: accumulating overlapping design documents
  endorsement: n/a

- statement: An artifact shaped by a style rulebook never cites that rulebook.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: none
  endorsement: affirmed
```

## Not converted

- Trust the frontier model's competence instead of enumerating hygiene basics: "I dont have to tell you what those are I hope, you are a frontier model." [p1]
- The quality bar for the result: code getting smaller, clearer, bounded API surface, crisp, understandable, without the smell of AI slop smearing and bloating everything. [p39], [p44]
- Vibe-coding for days without interim technical-debt refactors is why so many findings accumulated. [p30]
- Much time is wasted because correction subagents keep making mistakes. [p40]
- Autonomous-execution preference: run the plan without stopping for confirmation; on failure roll back and redo, so the user returns to a clean result. [p20]
- Reset, do not revert; force-pushing is fine on a solo repo. (Git mechanics, a technology choice.) [p15], [p19], [p20]
- wip commits pushed to the remote are a cheap backup; keep them. [p26], [p27]
- Use cargo public-api as the ground truth for the workflow. (Excluded as a technology choice; the technology-agnostic form was converted above.) [p31], [p32]
- The improvised review process was preferred over the pre-written refactor-rust tool: faster and more grounded in reality. [p49], [p50], [p51]








