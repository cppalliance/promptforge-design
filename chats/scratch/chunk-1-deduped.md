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
  citation: 2026-07-31-1516-agentic-ide-research.md [p87], [p109]
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
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p348]
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

- statement: A horizontal rule immediately after an H2 heading protects that section from fall-through; the executor skips the protected section and continues at the next one.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p382-p389]
  rejected-alternative: a single horizontal rule below which no execution occurs at all
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
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: per-section tool scoping]; 2026-07-28-0925-orchestrator-design-document.md [p17]
  rejected-alternative: opt-out scoping where a section starts with all frontmatter tools
  endorsement: affirmed

- statement: Attacker-controllable tool output is automatically wrapped in a guard block declaring the content data rather than commands, triggered by a tool-declared untrusted-output property, with marker strings inside the content escaped so the delimiter cannot be forged.
  scope: core
  source: ai-proposed
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: guard-wrap untrusted tool output], [p333-p335]
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
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p117]
  rejected-alternative: none
  endorsement: n/a

- statement: Work is spread across files by decomposing into separate single-function prompt files; directories serve as namespaces for organizing prompts.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p117]
  rejected-alternative: none
  endorsement: n/a

- statement: The design starts from the prompt and adds structured programming into it, never the other way around; a prompt with zero Lua still works like a plain orchestration, so Lua is additive, not required.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p118]
  rejected-alternative: starting with an interpreted host language and bolting prompts onto it
  endorsement: n/a

- statement: Every design choice is evaluated by whether it relieves pressure on the context window so smaller models can run the prompt; moving orchestration logic into deterministic Lua reduces the model sophistication required.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p119]
  rejected-alternative: none
  endorsement: n/a

- statement: Invocation runs in both directions - Lua code can call the model, and the model can route and orchestrate with multi-turn decision making when a task requires it.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua state is substituted into prompt text through a substitution syntax, and that substitution is what makes prompt assembly deterministic.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: The user cannot declare arbitrary globals; only a fixed set of objects is accessible from prompt Lua.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p71]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompt parameters are read-only and visible to every section and every piece of Lua in the prompt, so values never have to be passed from section to section.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: Falling through to the next section is the default transition and it clears context; running off the last section ends the prompt with a well-defined default message that can be overridden in the YAML.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p75], [p121]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10]
  rejected-alternative: none
  endorsement: n/a

- statement: Control flow has three primitives with distinct context semantics - call preserves context and returns, task runs with a fresh context and returns a result, goto transfers control, clears context, and does not return.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p120]
  rejected-alternative: none
  endorsement: n/a

- statement: The tool surface offered to a section stays small enough for a small orchestrator model (roughly five to seven tools); a section is offered only the tools it needs, and control-flow primitives may collapse into a single tool with a mode parameter if small models struggle.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p85], [p119], [p120]
  rejected-alternative: none
  endorsement: n/a

- statement: Between sections, the model's narration and throat-clearing are trimmed rather than carried forward; the preferred advance is a tool call in which the model explicitly passes only the curated context the next section should have.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p121]
  rejected-alternative: a bare goto that carries no curated instruction string
  endorsement: n/a

- statement: Structured results are assembled by Lua as a JSON object and returned by the model through substitution; the harness owns the wire format of a tool call and may change it under the hood.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p78], [p79]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt is self-contained; running it never requires a companion Rust file backing its operations.
  scope: global
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p86]
  rejected-alternative: every prompt backed by its own Rust code
  endorsement: n/a

- statement: A prompt operates on abstract semantic operations (add claim, remove claim) that know nothing about storage; a per-prompt configuration file binds those abstract tools to concrete, backend-agnostic implementations.
  scope: boundary: prompt<->tool-binding
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p88]
  rejected-alternative: hardcoding the database backend into the tool
  endorsement: n/a

- statement: The schema attaches to the tool, not to the prompt, so fifty prompts sharing a tool do not repeat the schema fifty times.
  scope: boundary: prompt<->tool-binding
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p90]
  rejected-alternative: declaring the schema in each prompt's front matter
  endorsement: n/a

- statement: The harness discovers a prompt's required tools by running the Lua with stubs and intercepting every tool-registration call - tools are never declared in front matter - and loading fails with an error when a discovered tool has no binding.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p89], [p91]
  rejected-alternative: listing required tools in the YAML front matter
  endorsement: n/a

- statement: Calling another prompt by filename invokes it as a function; prompt-to-prompt calls inside one process go direct, not through MCP.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p120]
  rejected-alternative: routing in-process prompt calls through MCP sockets
  endorsement: n/a

- statement: All inference traffic bottlenecks through a single gateway process that enforces global concurrency limits across all apps, languages, and machines.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p116]
  rejected-alternative: none
  endorsement: n/a

- statement: Any prompt can be exported as an MCP tool through configuration alone, because the YAML front matter (parameters plus description) supplies everything a tool definition needs.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p122]
  rejected-alternative: none
  endorsement: n/a

- statement: The PromptForge MCP server can itself act as an MCP client, connecting to other MCP services as configured.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p122]
  rejected-alternative: none
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

- statement: The store makes real files and virtual (memory) files available at the same time.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p367]
  rejected-alternative: a store model that supports only one kind of file at a time
  endorsement: n/a

- statement: The Lua API is not sandboxed away from the filesystem; Lua code can read and write both real files and memory files.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p368]
  rejected-alternative: sandboxing Lua so it cannot write files
  endorsement: n/a

- statement: Access control applies to the model, not to Lua: every H2 section that injects tools also injects which files those tools may access.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p368]
  rejected-alternative: protecting the machine by restricting the Lua API instead of the prompt's tools
  endorsement: n/a

- statement: No parallel mechanisms: a single, small, well-designed set of primitives services all needs, so existing mechanisms like tool scoping are leaned on as much as possible.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p371]
  rejected-alternative: adding a new mechanism alongside an existing one that already covers the need
  endorsement: n/a

- statement: Tool availability can be scoped by turn within a section, e.g. only web_search on the first turn, then web_fetch and web_search from later turns.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p372]
  rejected-alternative: making all of a section's tools available on every turn
  endorsement: n/a

- statement: A tool can be implemented as an inline Lua function acting as a front end to a real tool, and it can enable further tools at call time (e.g. tools.add for fetch); the prompt author opting in is what makes this acceptable.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p373], [p374]
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
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p1], [plans section]
  rejected-alternative: reusing agents or pulling full findings into the main conversation
  endorsement: n/a

- statement: An API redesign is judged by whether it both shrinks and cleans the public surface and makes the observed findings structurally less likely to recur.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p1]
  rejected-alternative: fixing findings one by one without rethinking the API that produced them
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

- statement: Completion is gated by an independent verification context; an implementing agent's self-report of "all green" is never trusted on its own.
  scope: global
  source: ai-proposed
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [plans section], [p24]
  rejected-alternative: accepting the fix agent's own green report as completion
  endorsement: affirmed

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
