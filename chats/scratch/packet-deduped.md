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

---

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
