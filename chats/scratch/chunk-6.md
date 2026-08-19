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
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p155], [p156], [p157], [p158]
  rejected-alternative: function-call notation such as call( "return", "x" )
  endorsement: n/a

- statement: The engine gives the model a handful of well-described tools plus a prose prompt and lets the model figure out the action on its own.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p158]
  rejected-alternative: none
  endorsement: n/a

- statement: The number of tools injected into the model's context is kept minimal; call() exists so the context is not stuffed with tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p163]
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
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p222]
  rejected-alternative: offering the full multi-mode call() to a single-behavior section
  endorsement: n/a

- statement: The language provides both a dramatically simple single-concern call and a full swiss-army call, because decisions are what small models are worst at while frontier models handle multiple call kinds without trouble.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p222], [p223]
  rejected-alternative: standardizing on one call form for all models
  endorsement: n/a

- statement: The engine supports both streaming and non-streaming model sessions.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p170], [p171]
  rejected-alternative: none
  endorsement: n/a

- statement: Every markdown feature of the prompt format ships with a corresponding test.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]
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
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190], [p191], [p192]
  rejected-alternative: a shared schema package used by both executor and gateway
  endorsement: n/a

- statement: A single executor run is not tied to one base URL; each H2 step can use a different logical model, and each logical model can point to a different physical model.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p212]
  rejected-alternative: binding a run to a single endpoint
  endorsement: n/a

- statement: A conversation never flips back and forth between multiple physical endpoints, because doing so loses the KV cache pairs.
  scope: gateway
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p210]
  rejected-alternative: flipping a conversation between multiple endpoints
  endorsement: n/a

- statement: Exactly one machine holds the provider API key, because global rate limits cannot otherwise be enforced.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p211]
  rejected-alternative: distributing provider keys across multiple machines
  endorsement: n/a

- statement: Endpoint configuration such as base_url lives in the model config, not in the executor.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p213]
  rejected-alternative: the executor carrying a base_url
  endorsement: n/a

- statement: Each prompt carries a per-prompt file that maps prompt-level model ids to gateway model ids.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p214]
  rejected-alternative: none
  endorsement: n/a

- statement: The executor is just a function call; it holds no endpoint or provider knowledge of its own.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p215]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway is a proxy, and gateways can be chained (a local gateway can point at a company gateway, which points at the remote inference host).
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p216], [p217], [p218]
  rejected-alternative: none
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
- statement: A prompt declares each capability it needs as a plain-English description in its Lua prelude, and the harness binds each declared need to a concrete MCP tool when the prompt loads.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p39]
  rejected-alternative: naming each tool explicitly in the Lua for every section
  endorsement: n/a

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

- statement: Tool selection stays in the main context, which the author already governs (model choice, rewrite opt-out, full task history); no orphan subcontext with its own unanswered model configuration.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1419-mcp-client-continued.md [p71]
  rejected-alternative: a fresh subcontext that retrieves and selects the tool
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

- statement: The model that selects a tool is the model that will use it, so there is no chooser/executor capability mismatch.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1419-mcp-client-continued.md [design documents section]
  rejected-alternative: a separate chooser context distinct from the executing model
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

- statement: A PromptForge prompt is best thought of as a function - parameters in, string out, side effects possible - a linear pipeline that can have forks and fanouts, with a natural size limit on the program it can represent; deeper recursive structure is what separate files are for.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p410]
  rejected-alternative: perfect recursive section structure inside one file
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
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: per-section tool scoping]
  rejected-alternative: opt-out scoping where a section gets all frontmatter tools unless it subtracts
  endorsement: affirmed

- statement: The runtime contains no orchestration logic, prompt assembly, or step ordering; all of that lives in the markdown.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: orchestrator design document]
  rejected-alternative: hardcoded per-pipeline orchestration code in the runtime
  endorsement: unaddressed

- statement: A section's Lua block runs in a sandbox: empty globals, only safe standard-library subsets, no io/os/require/load/package/debug, and an instruction-count hook that aborts a runaway block.
  scope: core
  source: ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: lua args substitution]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The LLM credential lives in the gateway, not the executor; the executor knows no vendor.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part5.md [plans: gateway v0]
  rejected-alternative: the executor holding the vendor key directly
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
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26]
  rejected-alternative: duplicate facilities for the same capability
  endorsement: n/a

- statement: Prefer the smallest facility that covers the most use; do not invent a new facility when an existing one can handle the case.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26]
  rejected-alternative: a dedicated new facility duplicating an existing one
  endorsement: n/a

- statement: Tool declarations live in the H1 preamble of the prompt, not in YAML front matter.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26]
  rejected-alternative: tool front matter
  endorsement: n/a

- statement: A prompt declares the tool capabilities it needs as descriptive need strings rather than hard-coded tool names; the harness resolves each need to a tool by semantic match and binds it to a local symbol the prose can reference precisely.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p27-p31]
  rejected-alternative: hard-coded tool names in prompts
  endorsement: n/a

- statement: A need that cannot be resolved to one unambiguous tool is an error.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p27]
  rejected-alternative: none
  endorsement: n/a

- statement: Ambiguity or duplication in tool binding is an error; mapping the same tool to two different ids is rejected.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p35]
  rejected-alternative: silently allowing duplicate tool bindings
  endorsement: n/a

- statement: After the H1 preamble runs, the harness compares all bound tools and fails the prompt if two or more are too similar to disambiguate.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p36-p37]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt file is an H1 section containing a lua preamble fence, prose, and a lua epilogue fence, followed by H2 sections.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p6-p12]
  rejected-alternative: none
  endorsement: n/a

- statement: The H1 is required; anything between the YAML front matter and the H1 is ignored.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p23]
  rejected-alternative: meaningful content between front matter and H1
  endorsement: n/a

- statement: After the H1 preamble executes, the prompt-global Lua state becomes read-only, and each fanout arm receives its own copy of shared functions rather than sharing mutable state.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p15-p21]
  rejected-alternative: shared mutable global state across fanout arms
  endorsement: n/a

- statement: Every harness operation reports its activity to an optional caller-installed observer; trace events are reduced to a Section string and a Detail string.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p39-p40]
  rejected-alternative: a taxonomy of typed trace event structures
  endorsement: n/a

- statement: Prompts have a log() facility whose output is concurrency-safe and tagged with a per-execution id.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p53-p56]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompt behavior is tested with standalone prompt files, not inline strings in test code.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p46-p47]
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
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p76-p77]
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
- statement: A prompt is an H1 name section containing a lua preamble fence, prose, and a lua epilog fence, followed by H2 sections.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p7]
  rejected-alternative: a trailing lua code fence after the section body
  endorsement: n/a

- statement: Within a section the lua fence comes before the prose, so a preamble can never be confused with an epilogue.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p22]
  rejected-alternative: none
  endorsement: n/a

- statement: The H1 section is required, and anything between the YAML front matter and the H1 is ignored.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p23]
  rejected-alternative: none
  endorsement: n/a

- statement: Create the smallest facility that lets the system do as much as possible; never invent a new facility when an existing one can handle the job.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p26]
  rejected-alternative: none
  endorsement: n/a

- statement: Never have two ways of doing the same thing, unless there is a really good documented reason.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p26]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool declarations live in the prompt's H1 section, not in YAML front matter; tool front matter is removed.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p26]
  rejected-alternative: declaring tools in YAML front matter
  endorsement: n/a

- statement: A prompt declares the tool capabilities it needs as descriptive sentences (need strings); the harness resolves each need to a tool by embedding and reranking, so the prompt never hard-codes a tool name, and a need that resolves to no tool or to an ambiguous tool is an error.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p27]
  rejected-alternative: hard-coded tool names in the prompt
  endorsement: n/a

- statement: A need binds to a local name, so the prose can reference the resolved tool by a precise local symbol.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p28]
  rejected-alternative: none
  endorsement: n/a

- statement: Ambiguity or duplication in tool binding is an error; mapping the same tool to two different ids is an error.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p35]
  rejected-alternative: allowing one tool to be bound under multiple ids
  endorsement: n/a

- statement: After the H1 preamble runs, the harness compares all bound tools pairwise and fails if any two are too similar.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p36]
  rejected-alternative: none
  endorsement: n/a

- statement: Every harness operation reports its activity to an optional observer that the caller installs, providing detailed tracing as a cross-cutting concern.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p39]
  rejected-alternative: none
  endorsement: n/a

- statement: An observer event is just two strings, a Section and a Detail.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p40]
  rejected-alternative: a typed taxonomy of structured event kinds
  endorsement: n/a

- statement: Functions shared by many sections are defined once in the prompt's global lua rather than duplicated per section.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p14]
  rejected-alternative: duplicating shared functions in each section that uses them
  endorsement: n/a

- statement: The prompt's global lua loads and executes once, then becomes read-only, so fan-out arms can share global state safely.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p15]
  rejected-alternative: fan-out arms accessing global mutable state
  endorsement: n/a

- statement: The lua environment provides a log() facility, useful in tests to confirm execution reached a certain point; print is disabled or remapped to it.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p55]
  rejected-alternative: none
  endorsement: n/a

- statement: Each concurrent execution instance gets its own id, and log output is tagged with the id of the instance that produced it.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p56]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompt tests are written as standalone prompt files, not inline strings in test code.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p46]
  rejected-alternative: prompts embedded as inline strings in test code
  endorsement: n/a

- statement: The CLI provides a fast development loop: edit a prompt, run it from the command line with real inference, see debug logging of what it is doing, see the answer, and iterate quickly without building infrastructure.
  scope: cli
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p77]
  rejected-alternative: none
  endorsement: n/a

- statement: The runner executable takes the prompt as a command line argument and picks up everything it needs from the directory containing the prompt.
  scope: cli
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part1.md [p76]
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
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p54]
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

- statement: The language never offers two features that do the same thing a different way; each primitive has one distinct job, so prose is prose and infer is something else.
  scope: global
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p165]
  rejected-alternative: infer as an alternate spelling of prose
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
