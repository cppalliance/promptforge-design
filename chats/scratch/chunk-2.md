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

- statement: A compression step must be able to decline: when a sentence is already at its minimum, it says so rather than degrading the sentence.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p57]
  rejected-alternative: a compressor that always produces shorter output
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
- statement: Every prompt is a single markdown file and is one function - it takes well-defined key-value parameters declared in machine-readable YAML front matter and returns a string, and it may produce side effects beyond its return value.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p65, p117]
  rejected-alternative: none
  endorsement: n/a

- statement: Work is spread across files by decomposing into separate prompt files; calling another prompt by filename invokes it as a function; directories serve as namespaces; intra-process prompt-to-prompt calls go direct, not through MCP.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p117, p120]
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
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p65, p120]
  rejected-alternative: none
  endorsement: n/a

- statement: Both Lua and the model can initiate control transfer; the model must be able to route when multi-turn decision-making is required, because some orchestration cannot be done in Lua.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: The executor performs substitution of named values from Lua state into the prompt through a substitution syntax, and this gives determinism.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: The user cannot declare arbitrary globals; only a fixed set of objects is accessible from prompt code.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p71]
  rejected-alternative: arbitrary user-declared globals
  endorsement: n/a

- statement: A prompt's key-value parameters are read-only and visible to every section and to any Lua anywhere in the prompt, so values never have to be passed from section to section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: Section transitions are context-clearing by default - falling through to the next section is the default when no explicit control flow is specified, the model's narration and throat-clearing is trimmed rather than carried forward, the preferred advance mechanism is a tool call where the model explicitly passes only the curated context the next section needs, and running off the end terminates the prompt with a default completion message that can be overridden in YAML, so termination is always well-defined.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p75, p121]
  rejected-alternative: bare goto as the advance mechanism, which cannot pass a curated instruction string
  endorsement: n/a

- statement: Structured data passes between Lua and the model as JSON assembled in Lua and returned by the model via macro substitution, and the tool-call mechanism structures the payload under the hood so the encoding can be swapped.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p78, p79]
  rejected-alternative: pydantic-style schema conformance with injected system-prompt overhead
  endorsement: n/a

- statement: Tool availability is scoped per section; each section sees only the few tools it needs rather than every tool at once.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p85]
  rejected-alternative: making all tools available to every section
  endorsement: n/a

- statement: A prompt is self-contained; it must not require backing host-language code, because requiring a companion Rust file per prompt defeats the purpose of the single-file model.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p86]
  rejected-alternative: a backing Rust file per prompt
  endorsement: n/a

- statement: Prompts operate in a semantic space of abstract operations (e.g. add claim, remove claim) that know nothing about the storage backend; a per-prompt configuration file binds each abstract tool to a concrete implementation, and the bindings are generic so the backend (Postgres, SQLite, MySQL) is never hardcoded into the tool.
  scope: boundary: prompt<->tool-bindings
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p88]
  rejected-alternative: hardcoding the database backend into the tool
  endorsement: n/a

- statement: Tools are discovered, not declared - at load time the harness parses the prompt's Lua with everything stubbed, intercepts tool-registration calls, enumerates and deduplicates the required tools, fails to load with an error if any binding is missing, and offers a command that emits an empty bindings template for the user to fill in.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p89, p91, p95]
  rejected-alternative: listing required tools in the YAML front matter
  endorsement: n/a

- statement: The schema attaches to the tool, not the prompt, so fifty prompts sharing one tool do not repeat the schema fifty times.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p90]
  rejected-alternative: declaring the schema in each prompt
  endorsement: n/a

- statement: Not all prompt state reduces to files; structured data such as breadcrumbs requires a structured representation.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p96, p100]
  rejected-alternative: the file as the sole unit of state
  endorsement: n/a

- statement: Each design choice is evaluated by whether it relieves pressure on the context window so smaller models can be used - more Lua means less model sophistication needed, and the tool count stays within 5-7 for small (7B-14B) orchestrator models.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p119]
  rejected-alternative: none
  endorsement: n/a

- statement: All inference traffic bottlenecks through a single gateway process that enforces global concurrency limits across all apps, languages, and machines; loopback connections require no API keys, while remote intranet access uses whitelisted IPs or API keys.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p116]
  rejected-alternative: none
  endorsement: n/a

- statement: The design starts with the prompt and adds structured programming (Lua) into it, and a prompt written with zero Lua still works like a Cursor orchestration - Lua is additive, never required.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p118]
  rejected-alternative: host-language-first frameworks that bolt prompts onto Python or Go
  endorsement: n/a

- statement: Prompts can be exported as MCP tools via configuration, with the YAML front matter supplying everything needed to define the tool; the server monitors the prompt directory and refreshes its cache without restart as a developer convenience; and the server can itself act as an MCP client to other services.
  scope: mcp
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p122]
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
- statement: A prompt declares the tools it needs in plain-English frontmatter, and a launch-time classifier maps the available MCP offerings to those stated needs.
  scope: core
  source: user-corrective
  citation: 2026-08-02-2331-mcp-client-evening.md [p10]
  rejected-alternative: the Lua naming each tool explicitly for each section
  endorsement: n/a

- statement: The Lua interface must be able to add every tool from an MCP client in one call, and to ask for a tool that matches a description.
  scope: boundary: lua<->mcp
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p11]
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

- statement: The architect-produced design document for a crate lives at that crate's root.
  scope: global
  source: user-stated
  citation: 2026-08-02-2331-mcp-client-evening.md [p30]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool resolution is deterministic: the same catalog, need, and config yield the same outcome across runs.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Tool resolution never guesses: a clear top match binds, a near-tie within the user's own catalog fails loud as a duplicate, a near-tie across foreign servers returns an ambiguity shortlist, and nothing above the similarity floor abstains as absent.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: silently returning the best-effort top match in all cases
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

- statement: A name is a design decision, because names are part of what the user sees; naming is design.
  scope: global
  source: ai-proposed
  citation: 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed
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
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p229], [p230], [p231]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua chunks return values with Lua's native return semantics, not through a special identifier or descriptor convention.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p234], [p235]
  rejected-alternative: a declared identifier or descriptor inspected by the Rust side
  endorsement: n/a

- statement: A section reached by goto is not reusable as a function called from multiple sites, because control always transfers to the same destination afterward.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p242]
  rejected-alternative: treating return-goto as a reusable multi-call-site function
  endorsement: n/a

- statement: A rendezvous section waits until every forked branch it is data-dependent on has completed.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247]
  rejected-alternative: none
  endorsement: n/a

- statement: A tool takes a single string argument; the prompt itself deduces the structured values from that string as its first step and stores them.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p251]
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
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p257], [p258], [p259], [p260]
  rejected-alternative: leaving the facts bag permanently in the transcript
  endorsement: n/a

- statement: Multiple values are stored with one set call, not one tool call per value.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p265]
  rejected-alternative: one tool call per stored value
  endorsement: n/a

- statement: Every heading's context is prefix, body, and suffix: the prefix is inherited cumulatively by child headings, the body is throwaway, and the suffix floats.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p268], [p269], [p270], [p271]
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
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p280], [p310]
  rejected-alternative: design documents carrying Rust types and declarations
  endorsement: n/a

- statement: The engine exposes system constants - sys.when for the prompt's launch time and sys.now for the current time - and gives every context a unique incrementing id.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p284], [p285], [p286]
  rejected-alternative: none
  endorsement: n/a

- statement: The context must not accumulate permanent residue across turns.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p287], [p288]
  rejected-alternative: accumulating permanent entries in the context so the model can detect time passing
  endorsement: n/a

- statement: Context needs are declared by the prompt's Lua and injected by the engine; the model does not pull them.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p290]
  rejected-alternative: the model requesting context items itself
  endorsement: n/a

- statement: The engine implements all features and lets the caller decide among them, with sensible defaults.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p316]
  rejected-alternative: shipping a curated subset of features
  endorsement: n/a

- statement: Tool injection is scoped per section, so declaring many tools in the front matter does not inject all of them into every context.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p328], [p329]
  rejected-alternative: defaulting to all declared tools when no Lua selects them
  endorsement: n/a

- statement: Untrusted web content returned to the model is wrapped in a delimiter and treated as data, never as commands.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p333], [p334], [p335]
  rejected-alternative: ad-hoc delimiters like <<< >>> that models are not trained on
  endorsement: n/a

- statement: File tools are line-number driven: the engine maps line numbers to character offsets for virtual and real files, and supports edit in place.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p343], [p344], [p347]
  rejected-alternative: character-range-only file addressing
  endorsement: n/a

- statement: PromptForge must be usable at a power equal to or greater than an agentic harness like Cursor or Claude Code.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p348]
  rejected-alternative: none
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
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p95]
  rejected-alternative: continuing the run after a required tool fails to bind
  endorsement: n/a

- statement: There is exactly one tools.add entry point, not multiple variants.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p90]
  rejected-alternative: multiple overloaded versions of tools.add
  endorsement: n/a

- statement: Whether model thinking is on or off is controlled by the prompt, not by the gateway.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p107]
  rejected-alternative: a gateway-level thinking toggle
  endorsement: n/a

- statement: Models are declared in the prompt's introduction via models.add with attributes like thinking and context size, and a section selects its model with model("name").
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p108]
  rejected-alternative: declaring model settings in the frontmatter
  endorsement: n/a

- statement: Provider-specific special cases live in a single normalization layer so the rest of the engine talks to all models universally.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p122]
  rejected-alternative: scattering per-provider special cases and one-off targeted fixes throughout the codebase
  endorsement: n/a

- statement: An empty model response is never acceptable; empty response is always a hard fail.
  scope: gateway
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p124]
  rejected-alternative: treating an empty response as a valid result
  endorsement: n/a

- statement: A tool call counts as a model response.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p126]
  rejected-alternative: none
  endorsement: n/a

- statement: Each run deletes the previous trace on launch; a developer who wants to keep a trace backs it up himself.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p128], [p165]
  rejected-alternative: accumulating trace files across runs
  endorsement: n/a

- statement: Model binding is much looser than tool binding and resolves through the same semantic picker used for tools.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p133]
  rejected-alternative: strict model-name binding that fails hard on mismatch
  endorsement: n/a

- statement: An H3 section inherits its H2's model unless it specifies its own.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p142]
  rejected-alternative: none
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
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p99]
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
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p26], [p30], [p32], [p35], [p65]
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
