<!-- source: promptforge-design/research/feature-survey-everruns.md (2026-09-12), analyzed against promptforge executor seams -->

# Everruns Capabilities: Promptforge Integration Paths

Each numbered feature below carries its description from the Everruns feature survey, followed by its promptforge integration path. Integration classes:

- **Prompt** - representable today with Lua + existing tools + store; no new machinery.
- **Tool** - a new tool or capability crate registered in the catalog over existing seams (VFS, dispatch, broker); no executor changes.
- **Executor** - requires integration into the executor core (models.loop dispatch, context projection, task runtime, output path).
- **Host** - host/platform concern (Workshop, CLI, future cloud host); the executor already exposes the seam, or the feature lives outside the run entirely.

Summary verdict: the large majority land as Prompt or Tool. The genuine Executor integrations are few and mostly already anticipated by deferred unified-model contracts: compaction, tool search, loop/budget guards, guardrails, and the task runtime for subagents/background work.

---

## 1. Programming model

1. **Agent as immutable definition** - Everruns captures instructions, model, provider, tools, capabilities, files, hooks, workspace, and MCP servers in a validated builder, snapshotted at session creation. *Integration: Prompt - the prompt file is the agent definition; YAML frontmatter (harness binding) plus frozen per-run parsing already gives immutability and snapshot semantics.*

2. **Engine-owned sessions** - an Engine owns the session catalog; create/resume/attach reopen isolated multi-turn conversations. *Integration: Host - session catalog and resume live in the host (Workshop has this; a headless host constructs runs directly); the executor is deliberately sessionless.*

3. **Turn model with steering** - send starts or steers a turn mid-flight; Turn carries response, stop reason, iterations, tool calls. *Integration: Prompt - Lua owns the message array, so steering is appending a user message between `models.loop` calls; the generic input broker (active unified-model scope) covers mid-turn injection.*

4. **Context inspection** - `Session::inspect` returns the next-call assembly without running hooks. *Integration: Executor (small) - Lua can already inspect its own message array; a `tools`/`models` scope-inspection accessor is a minor addition to the existing Lua namespaces, not new machinery.*

5. **Per-message controls** - model override, locale, reasoning effort per turn. *Integration: exists - `models.use` / explicit handles give per-call model selection; reasoning effort rides the model handle.*

6. **Input/Reason/Act sans-IO kernel** - pure planner over a serializable TurnState shared by in-process and durable hosts. *Integration: exists in spirit - `models.loop` is the Rust-backed loop; promptforge's determinism comes from the claims model and the uniform yield protocol rather than a serializable turn state, which is a deferred (cold-restore) contract.*

7. **Offline simulator** - deterministic simulated model, no network. *Integration: Host - a simulated model is a host-supplied entry in the model catalog; the executor cannot tell the difference.*

## 2. Typed tools

8. **`#[tool]` macro with schema derivation** - attribute macro turns an async fn into a schema-carrying tool. *Integration: Tool - promptforge tools are Rust `Tool` impls in the catalog today; a derive macro is author ergonomics, not a capability requirement.*

9. **Manual FunctionTool with redacted internal errors** - name, schema, async handler; handler Err hidden from the model. *Integration: exists - the tool catalog and model-visible error vocabulary already do this.*

10. **Capability handlers (multi-tool packages with typed I/O and progress)** - packages of tools plus instructions plus call-scoped cancellation. *Integration: Tool - this is the planned capability crate shape: a crate registering several tools plus a prompt fragment under one global namespace; cancellation already rides the run cancel token.*

11. **Tool registry contract with fingerprints and narration** - engine-facing registry with sanitization and parallel limits. *Integration: exists - `ToolCatalog`/`ToolId`; narration is an Observer concern.*

12. **Tool hints (readonly/destructive/background/concurrency)** - hints drive scheduling and approval gates. *Integration: Tool - annotations already exist in the picker catalog (`ToolAnnotations`); surfacing them to the policy layer is wiring, not machinery.*

13. **Tool call repair** - malformed tool-call args get a salvage pass plus bounded re-prompt instead of failing the turn. *Integration: Executor - intercepts malformed calls inside the `models.loop` dispatch path; cannot be a tool because the failure happens before any tool runs.*

14. **Tool output pipeline (hard limit, persistence, distillation)** - truncate oversized outputs; persist or distill large ones via the session filesystem. *Integration: Tool - persistence and distillation are store operations a wrapper tool performs before returning; the hard size cap is a dispatch wrapper the host installs around the catalog, no executor change.*

15. **Background executable tools with progress sinks** - tools declaring background support run async with progress. *Integration: Executor - requires the deferred task runtime (async call operations, task IDs, lifecycle events); progress reporting itself already flows through `shared-progress`.*

## 3. Capability model and workspace/shell

16. **Capability model (tools + prompt fragments + mounts as one opt-in unit)** - attachable at harness/agent/session, explicit registration. *Integration: Tool - this is the registry + YAML-binding design from the harness plan; the executor already consumes whatever catalog it is handed.*

17. **Session filesystem** - sandboxed workspace tools with read-only default and explicit write opt-in. *Integration: exists - VFS mounts plus `ModePolicy` (Ask/Plan/Agent) and read-only backends.*

18. **Bashkit shell** - in-process sandboxed bash over the session VFS with limits and default-deny networking. *Integration: Tool - the completed spike: bashkit's 142 commands behind `FsBackend`-over-`VfsRef`, registered as one capability crate; no executor involvement.*

19. **Lua scripting capability with code mode** - sandboxed Lua VM with fs/json/tools bridges. *Integration: exists natively - promptforge's sections are Lua; `tools.call` from Lua is the code-mode pattern already.*

20. **Web fetch with SSRF controls** - fetch/extract/crawl to markdown over governed egress. *Integration: exists - `promptforge-webfetch`; SSRF/egress policy is a host configuration concern.*

21. **Cloud/self-hosted sandboxes (Daytona, E2B, Docker, Deno, Sprites)** - remote exec and file I/O with per-session lifecycle. *Integration: Tool, with the exclusivity rule - each is an HTTP-API tool set, but per the 2026-09-12 decision, real-exec capabilities bind only in a dedicated terminal subagent prompt, never mixed with bashkit in one context.*

22. **Headless browser (Browserless)** - navigate, screenshot, scrape, interact over CDP. *Integration: Tool - HTTP/WebSocket API tools; secret placeholders map to host-seeded store values.*

23. **Search (Brave, DuckDuckGo, Parallel)** - web search and instant answers. *Integration: Tool - `promptforge-web-search` exists; additional providers are new tool crates over HTTP.*

24. **Knowledge bases with hybrid retrieval and citations** - org-scoped indexes, ANN+BM25, claim-level citations. *Integration: Tool - query tools over whatever vector backend the host provides (the workspace already operates a Pinecone MCP server with exactly this shape); citation verification is prompt-level composition over `models.infer`.*

25. **Provider-executed server tools (OpenRouter)** - provider-side web search/fetch/image. *Integration: Host/gateway - a provider wire concern, invisible to the executor.*

26. **Session utilities (current time, message metadata, session metadata, KV/secrets, session SQL)** - small agent-facing state and context tools. *Integration: Tool - time and metadata are trivial tools; KV/secrets are additional VFS mounts (a secrets mount the policy never lets the model read directly); session SQLite is one new tool crate (rusqlite) or a VFS backend.*

27. **Stateless todo list** - plan state kept only in conversation tool history. *Integration: Prompt - a Lua table plus a couple of local tools (`tools.add_local`); no runtime support needed.*

## 4. Context management

28. **Compaction (auto cascade, native, observation masking, summarization; proactive at 85%)** - compacts the model view while storage stays lossless, with durable checkpoints. *Integration: Executor - the compactor slot is already inside `models.loop` (`compactors.fail` shipped, the framework is a deferred unified-model contract); new strategies are pure Lua or Rust compactors plugged into that slot, so each strategy itself is Prompt/Tool once the slot exists.*

29. **Infinity context (query_history over trimmed history)** - recent window in the prompt, older messages pulled on demand. *Integration: Tool - one `query_history` tool over the host-owned `EventLog` trait (which exists), plus a prompt-side trimming convention; no executor change.*

30. **Tool search / deferred schemas** - large catalogs stay out of the prompt until a search tool surfaces them. *Integration: Executor - deferred advertising changes the context projection computed per dispatch (which schemas go out); the search tool itself is an ordinary tool over the catalog. Note the tension with the exact-binding direction: deferred schemas serve model-facing discovery, not author-facing binding.*

31. **Prompt caching** - mark stable prefixes for providers that cache. *Integration: Host/gateway - a provider wire concern; the executor's per-dispatch projection already isolates this.*

## 5. Instructions, skills, plugins

32. **AGENTS.md injection** - hierarchical instruction files injected as leading user-role context with size budgets. *Integration: Prompt - once fs read tools exist, a prompt (or stock harness prelude) reads `AGENTS.md` through the VFS and prepends it to the message array; making it declarative harness frontmatter later is sugar over exactly this.*

33. **Skills with progressive disclosure** - SKILL.md packages discovered under `/.agents/skills/`, activated on demand. *Integration: Prompt + Tool - discovery is `glob`/`read` over a skills mount; `activate_skill` is one tool that reads the body into context; frontmatter flags (`user-invocable`) are host/UI concerns.*

34. **Skills registry (org-wide packages, validation)** - stored packages assignable as virtual capabilities. *Integration: Host - package storage and validation live outside the run; the run only sees a mounted directory.*

35. **Plugins compiling to declarative capability contributions** - trusted directories compiled into instructions + tools + scoped MCP. *Integration: Host/build - a plugin is compiled down to harness frontmatter plus catalog registrations before the run starts.*

36. **Agentic Resource Discovery (mid-session attach of MCP/A2A resources)** - discover and attach resources against allowlisted registries with trust gates. *Integration: Tool + Executor seam - discovery and attach-request are tools, but attaching a resource mid-run mutates the live tool catalog, which today is fixed at run start; needs a catalog-add seam (small) plus Policy `Ask` for the trust gate (exists).*

## 6. Events and observability

37. **Event log as source of truth** - one append-only log; messages, streams, replay are projections. *Integration: exists as traits - `Observer` + `EventLog` in `promptforge-core-support` with the durable JSONL impl currently in Workshop; the planned harness move relocates it, no executor change.*

38. **Live event stream (bounded broadcast, lag reported)** - reviewed event kinds plus canonical JSON. *Integration: exists - the Observer stream; bounded broadcast is a host wrapper.*

39. **Canonical event taxonomy** - turn/reason/act/tool/llm/context event kinds. *Integration: exists - `Observation` kinds; taxonomy growth is additive.*

40. **SSE consumption with resume** - live tail with `since_id`. *Integration: Host - workshop-server already does this over the event log.*

41. **OpenTelemetry / Braintrust exporters** - per-turn traces with gen-AI conventions. *Integration: Host - alternate Observer implementations; the executor never knows.*

42. **Reasoning as ordered replayable artifacts** - reasoning as content parts with phase metadata. *Integration: exists - reasoning deltas flow through the model client; persisting them as ordered parts is an event-log schema concern.*

43. **ATIF trajectory export** - fold sessions into interchange format. *Integration: Host - a renderer over the event log.*

## 7. Lifecycle, cancellation, hooks

44. **Cooperative cancellation** - tokens, teardown of in-flight tools, committed hooks never interrupted. *Integration: exists - cancel tokens through RunConfig and the yield protocol.*

45. **Application lifecycle hooks (agent/turn/tool/completion)** - awaited non-mutating hooks with pre/post failure semantics. *Integration: Host - an Observer wrapper intercepts exactly these boundaries; no executor change.*

46. **Engine tool hooks (pre/post tool use, output hard limit)** - hooks inside dispatch. *Integration: Tool - a host-installed wrapper around the tool catalog intercepts before/after every call; the catalog is already host-supplied.*

47. **User hooks (shell hooks that block, mutate, audit)** - user automation on lifecycle events. *Integration: exists as a seam - the VFS `Policy` verdicts (Allow/Deny/Ask with reasons) are the block path; mutation and audit are host policy implementations.*

## 8. Model providers

48. **Provider abstraction with custom drivers** - streaming chat, model listing, native compact. *Integration: exists - the model client plus gateway; custom providers are host catalog entries.*

49. **Model profiles registry (limits, cost, modalities)** - hardcoded metadata keyed by wire id. *Integration: Host/gateway - routing and cost metadata live beside the gateway, not in the executor.*

50. **Provider retries with backoff** - transient 429/5xx handling. *Integration: exists - model-client concern.*

51. **Reasoning effort and execution phases** - streaming reasoning, Commentary vs FinalAnswer. *Integration: exists - carried by the model client and message model.*

52. **Tool schema compatibility normalization** - provider strict-subset projection. *Integration: exists - per-dispatch provider projection is an active unified-model contract.*

## 9. Memory and persistence

53. **Persistence tiers (volatile, local durable, platform durable)** - memory, SQLite, PostgreSQL. *Integration: Host - promptforge's tier story is event-log backend + VFS backend selection, both host-chosen; no executor change.*

54. **Bounded history API with cursors** - stable paged snapshots under concurrent append. *Integration: Host - a read API over the `EventLog` trait.*

55. **Memory mounts (org/agent/user-scoped file memory)** - durable named file memory mounted into sessions. *Integration: Tool/VFS - additional read-only or read-write host mounts with policy; the mount machinery exists.*

56. **Session work and wakes (background tasks, leases, idempotency)** - application tasks owned by a session. *Integration: Executor - needs the deferred task runtime; wake-on-schedule additionally needs a host timer (Host).*

57. **Workspaces and environments (multi-head, Git heads)** - scoped workspace binding. *Integration: exists - `HostBackend::rooted` mounts plus policy; Git-head tracking is a host concern.*

## 10. Reliability and self-regulation

58. **Loop detection (repeated tool-call signatures)** - flags an agent stuck repeating itself. *Integration: Executor - the detector must see the call stream inside `models.loop`; a natural sibling of the compactor slot (a loop-guard hook consulted per round).*

59. **Progress guard (exploration without progress)** - nudges when no forward progress. *Integration: Executor - same seam as loop detection, plus a definition of progress over events; heuristic policy itself can live in Lua.*

60. **Budgets (usd/tokens, soft pause/warn/stop)** - enforced caps with ledger. *Integration: Executor + Host - token/cost metering already flows to the Observer; enforcement needs a budget check inside the `models.loop` precheck (Executor), while ledgers, periods, and pause/resume are Host.*

61. **Usage-limit auto-continue** - resume after plan limits reset. *Integration: Host - a scheduler that re-invokes `run` when the provider window resets.*

62. **Guardrails (regex, blocklist, LLM judge, MCP checks; block vs log)** - declarative checks on output and tool calls, including streaming output replacement. *Integration: Executor - output-stage checks and `OutputReplaced`-style rewriting must sit in the streaming/output path; tool-call checks ride the dispatch wrapper (Tool). The LLM judge itself is just `models.infer`.*

63. **Prompt canary (withhold output on system-prompt echo)** - leak detection. *Integration: Executor - same output-path seam as guardrails; the canary value is host config.*

64. **Tool approval / human-in-the-loop** - approver seam with auto vs requires_approval. *Integration: exists - VFS `Policy` Ask verdicts plus the generic input broker are exactly this; extending Ask from fs ops to tool calls is a policy-wrapper (Tool-level).*

65. **Error disclosure control** - how much error detail the model sees. *Integration: exists - the model-visible error vocabulary is already a deliberate, frozen boundary.*

## 11. Multi-agent

66. **Subagents (spawn_agent with nesting caps, no privilege escalation)** - child sessions in isolated contexts. *Integration: Executor - `call` gives synchronous sub-prompts today; background/detached subagents with nesting caps need the deferred task runtime. The capability-exclusivity pattern (terminal subagent) works over plain `call` now.*

67. **Agent handoff (allowlisted transfer, no shared credentials)** - pass the task to another first-class agent. *Integration: Prompt - handoff is `call` plus return; the allowlist is frontmatter binding (you can only call what you bound).*

68. **A2A delegation (outbound Agent2Agent)** - delegate to remote agents. *Integration: Tool - an HTTP client tool set; auth via host-seeded secrets.*

69. **Session participants (multi-agent/multi-user, @addressing)** - host vs member roles in one session. *Integration: Host - session membership and routing live outside the run; a run sees one input broker.*

70. **Session tasks (uniform registry for subagents, background tools, monitors)** - lifecycle, messaging, input requests, artifacts. *Integration: Executor (task runtime) + Host (registry storage and reaping).*

71. **Blueprint subagents (GitHub Scout: host has no GitHub tools, spawns read-only scout)** - privilege separation by construction. *Integration: Prompt - exactly the terminal-exclusivity pattern: the parent never binds GitHub tools; the scout prompt binds only read-only ones.*

72. **Cursor Cloud Agents delegation** - launch and follow up on cloud coding agents. *Integration: Tool - HTTP API tools.*

73. **Multi-agent pipelines (chained sessions)** - orchestrate agents in sequence. *Integration: Prompt - `call` chains today; parallel pipelines need deferred `fanout`.*

## 12. Durable execution platform

74. **Event-sourced workflows with replay recovery** - append-only workflow events, snapshot-assisted replay, crash reclaim. *Integration: Host/platform (large) - promptforge's determinism primitives (claims, uniform yields, journaled store) are the executor half; durable replay and cold restore are explicitly deferred unified-model contracts, not harness work.*

75. **Checkpointed turn execution** - only engine-owned state checkpointed between phases. *Integration: Executor (deferred) - the incarnation/cold-restore contract; out of scope for the harness layer.*

76. **Activity queue with retries, timeouts, circuit breakers, DLQ** - distributed work units. *Integration: Host/platform - a future cloud host concern; the in-process executor needs none of it.*

77. **Snapshots and continue-as-new** - roll long histories into fresh workflows. *Integration: Host/platform - event-log compaction at rest.*

78. **Forward-progress seal (stuck-turn guard)** - seal a repeatedly reclaimed turn as dead. *Integration: Host - a supervisor policy over run attempts; Workshop's supervisor FSM is the embryo.*

79. **Workflow signals (cancel, shutdown, user_message)** - external signals into running workflows. *Integration: exists - cancel token plus input broker cover the in-process equivalents.*

80. **Stateless workers, control plane, durable ops API, host composition boundary** - the distributed platform. *Integration: Host/platform - out of scope for the harness; the design constraint it imposes (hosts share one effectful path) is already satisfied by RunConfig being the single entry.*

## 13. Scheduling and triggers

81. **Agent triggers, session schedules, durable cron, workflow timers, webhooks** - time- and event-based run initiation. *Integration: Host - a trigger is a host calling `run` on a schedule; in-run waits (sleep-until) would need a timer yield (small Executor addition, deferred tasks territory), but run initiation needs nothing.*

## 14. Multi-tenancy and security

82. **Organizations, roles, policy authorization, audit, encryption at rest** - platform tenancy. *Integration: Host/platform - none of it touches the executor; promptforge's equivalent boundary is the VFS policy plus host-seeded secrets.*

83. **Egress governance (SSRF controls, allow/block lists, default-deny)** - network policy. *Integration: Tool config - webfetch/web-search tools take egress policy at construction; bashkit networking is default-deny by its own design.*

84. **MCP URL elicitation (pause turn for browser consent)** - secrets never pass through client or model. *Integration: Tool + existing broker - the elicitation is a blocking `user_input`-style broker request (the broker is already generic); requires MCP client support first (see 86).*

## 15. Distribution

85. **Apps and channels (Slack, AG-UI, webhook, A2A, public chat, voice)** - bind agents to inbound surfaces with routing and lifecycle. *Integration: Host - a channel is a host that constructs runs from external events; Workshop's HTTP/WS adapter is the in-tree example.*

86. **MCP server and client** - expose agents as MCP; mount remote servers as virtual capabilities. *Integration: Tool (client) + Host (server) - the client is a bridge that registers remote MCP tools into the catalog under an `mcp_<server>__*` namespace (fits the global naming system directly); the server is a host exposing prompts over MCP.*

87. **Agent versions (immutable snapshots, pinning, rollback)** - versioned behavior definitions. *Integration: Host - prompt files plus git give immutable versions today; a registry is host storage.*

88. **CLI and SDKs** - scriptable agent management. *Integration: Host - the `promptforge` facade is the library entry; a CLI is a thin host over it.*

89. **File-defined agents** - agents authored as importable files. *Integration: exists natively - a promptforge prompt is a file-defined agent; this is the prompting language's core identity.*

## 16. Harnesses

90. **Harness as data (capabilities + prompt + files + model defaults, with inheritance)** - resolved at session start. *Integration: the planned design - YAML frontmatter binding global capability names, with a parent key for inheritance; resolution happens before `run`, so the executor sees only a finished catalog and config.*

91. **Built-in harness catalog (base, generic, platform-chat, data-analyst)** - stock compositions. *Integration: Prompt - stock harnesses are shipped prompt files / frontmatter presets; content, not code.*

92. **Two-level coding execution (VFS for light work, real exec for builds)** - prompt-steered tool choice. *Integration: Prompt - the exclusivity pattern: bashkit in the main context, terminal subagent for real work, store as the handoff channel.*

93. **Sandbox abstraction (one logical sandbox, disposable incarnations, fencing)** - provider-neutral sandbox with checkpointed recovery. *Integration: mostly N/A - bashkit-over-VFS plus the terminal-subagent rule gives one filesystem reality per context without the provider-incarnation machinery; revisit only if promptforge ever adopts remote sandboxes.*

94. **Managed session sandboxes (auto-start, idle pause, recovery volumes)** - control-plane reconciled lifecycle. *Integration: Host/platform - only relevant alongside remote sandbox providers.*

## 17. Evaluation and quality

95. **Evals (real sessions, scorers, durable runs)** - behavioral tests over real executions. *Integration: Host - an eval host runs prompts and scores outputs; promptforge's determinism (claims, journaled store) makes runs replayable, which is the hard part already done.*

96. **SWE-bench harness** - benchmark on eval machinery. *Integration: Host - an eval target once bashkit and terminal subagents exist.*

97. **Observers (online LLM-judge scoring of production traffic)** - asynchronous scoring, never on the hot path. *Integration: Host - an Observer implementation that feeds events to a judge model.*

98. **Agent checks (advisory lint/health on config)** - structure, completeness, cost analysis. *Integration: Host/tooling - static analysis over prompt files plus `Session::inspect`-style context assembly.*

99. **External results import and ATIF dataset export** - interchange of eval outcomes. *Integration: Host - renderers over the event log.*

100. **Failure injection (fail-rs style fault testing)** - deterministic fault seams. *Integration: exists as practice - promptforge already favors behavior tests with deterministic fault injection (cancel tokens, policy verdicts, and the yield protocol are the seams).*

---

## Totals

- **Prompt (no new machinery):** 1, 3, 24, 27, 28 (strategies), 29, 32, 33, 62 (judge), 64, 67, 71, 73, 90, 91, 92 - 16 features
- **Tool (new tools/capability crates over existing seams):** 8, 10, 12, 14, 18, 21, 22, 23, 26, 36, 46, 55, 63 (config), 66 (sync call today), 68, 72, 83, 84, 86 (client) - 19 features
- **Executor (core integration):** 4 (minor), 13, 15, 28 (slot), 30, 36 (catalog-add seam), 56, 58, 59, 60 (precheck), 62 (output path), 66 (task runtime), 70, 75 (deferred), 81 (timer yield, optional) - 15 features, of which the load-bearing ones (compactor slot, task runtime, output path, loop guards) are already deferred unified-model contracts
- **Host / platform (outside the run):** the remaining ~50, including the entire durable-platform and multi-tenancy surface

**Bottom line:** the executor does not need to become a harness. It needs four seams it already has or has already deferred by design (compactor slot, task runtime, output-path guardrails, loop/budget guards in `models.loop`). Everything else composes as prompts, tools, capability crates, and hosts - which is exactly the registry-plus-data harness shape in the design plan.

*2026-09-12 18:30 - kimi-k3*



