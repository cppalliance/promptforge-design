<!-- source: c:\Users\Vinnie\cursor\everruns (local repo, surveyed 2026-09-12) -->

# Everruns Agentic Feature Survey

Everruns is an open-source Rust framework plus platform for building and operating AI agents: an embeddable application-facing crate (`everruns`), a neutral contracts kernel (`everruns-core`), a sans-IO turn engine (`everruns-engine`), and a durable production platform (control plane, stateless workers, PostgreSQL event-sourced workflows). This report describes each agentic feature found in the repo, organized by layer. Locations cite crates and doc paths inside the repo.

The organizing formula, from the project's own knowledge base: **Harness + Agent + Capabilities** assemble into a runtime agent inside a **Session**, running a durable **Input -> Reason -> Act** loop over an append-only **event log**.

---

## 1. Programming model (framework facade)

- **Agent as immutable definition** - `Agent` captures instructions, model, provider, tools, capabilities, files, hooks, workspace, and MCP servers; `AgentBuilder` validates at `build()` (blank instructions, missing model/provider, duplicate tools, invalid schemas). Agents are snapshotted when a session is created, so concurrent sessions stay isolated. (`crates/everruns/src/agent.rs`)
- **Engine-owned sessions** - `Engine` owns the session catalog and backends; `create(agent)` opens an isolated multi-turn conversation, `resume`/`attach` reopen handles. Default is process-local memory; the `local` feature adds SQLite plus a crash-durable event log. (`everruns::Engine`)
- **Turn model** - `send` accepts input without waiting (starts a turn if idle, steers mid-turn if busy: `SendDisposition::Started|Steered`); `send_and_wait`/`run` wait for the accepting turn; `run_with` adds `RunOptions` for cancellation. A `Turn` projection carries `response`, `stop_reason` (end turn, max tokens, refusal, error, cancelled, ...), `iterations`, `tool_calls`, and `hook_failures`. (`everruns::Session`, `TurnHandle`, `Turn`)
- **Steering** - mid-turn user messages join the active turn at the next reason boundary; queue overflow surfaces as `RunError::SteeringQueueFull`. Platform-side, steering rides durable workflow signals (`user_message`) so it works across worker processes.
- **Context inspection** - `Session::inspect` returns the next-call assembly (model spec, filtered messages, tools, effective instructions, locale, plugin warnings) without running lifecycle hooks. (`everruns::SessionContext`)
- **Per-message controls** - `InputMessage` can carry `Controls`: model override, locale, reasoning effort, speed/service tier - turn-scoped runtime options without rebuilding the agent. (`everruns-core::Controls`)
- **Input/Reason/Act kernel** - the portable agent loop: Input atom loads context, Reason calls the LLM, Act executes tools; a pure planner (`TurnExecution`, `TurnPlan`) decides next steps. One serializable `TurnState` with host-injected effects means in-process and durable hosts cannot drift. (`everruns-engine`; `knowledge/foundations/sans-io-turn-state.md`)
- **Offline simulator** - `Model::simulated` runs a deterministic `llmsim` provider with no network, for tests and demos.

## 2. Typed tools

- **`#[everruns::tool]` macro** - turns an async fn into a zero-arg constructor returning `FunctionTool`; derives the JSON Schema via schemars, supports renames, `Option<T>`, and `Result<T,E>` where `Err` is model-visible. Rejects non-async fns, receivers, generics. (`everruns-macros`)
- **Manual FunctionTool** - name, description, JSON schema, async handler; `ToolResponse::{json,text,error}`; handler `Err` is redacted from the model (internal error path). (`everruns::tool`)
- **Capability handlers** - multi-tool packages with typed Input/Output schemas, capability-level instructions, a `Context` with progress reporting and call-scoped cancellation. (`everruns-capability::definition`)
- **Tool registry contract** - engine-facing `Tool`/`ToolRegistry` with fingerprints, narration, sanitization, and parallel execution limits. (`everruns-core::tools`)
- **Tool hints and policies** - readonly/destructive/background/concurrency hints drive scheduling, UI approval gates, and narration. (`knowledge/execution/tool-execution.md`)
- **Tool call repair** - malformed tool-call arguments get a local salvage pass plus a bounded re-prompt instead of failing the turn. (`tool_call_repair` builtin)
- **Tool output pipeline** - oversized outputs are truncated by an `OutputHardLimitHook`; `tool_output_persistence` and `tool_output_distillation` capabilities persist or distill large outputs through the session filesystem.
- **Background executable tools** - tools declaring `supports_background` run asynchronously with progress sinks; `spawn_background` auto-activates when any tool supports it; runs are mirrored as session tasks. (`everruns-core::background`)

## 3. Capability model (the extension spine)

Capabilities bundle tools + prompt fragments + session state + VFS mounts into one opt-in unit, attachable at harness, agent, or session level. Registration is explicit: linking a crate does nothing until the host registers the capability. Declarative (data-defined) and code-defined capabilities share one registry with atomic ID/alias collision rejection; high-risk capabilities are gated. (`everruns-capability`; `knowledge/execution/capabilities.md`)

### Workspace and shell capabilities

- **Session filesystem** (`session_file_system`, on by default) - sandboxed workspace tools: read/write/edit/list/grep/delete/stat plus bounded batch reads, mounted at `/workspace`, with a `WorkspacePolicy` that defaults to read-only and requires explicit write opt-in. (`integrations/filesystem`)
- **Bashkit shell** (`bashkit_shell`) - in-process sandboxed bash over the session VFS (not a real OS shell) with command/loop/AST limits, indexed grep, output sanitization, streaming progress, and default-deny networking unless HTTP egress is explicitly enabled. (`integrations/bashkit`; `knowledge/execution/bashkit-requirements.md`)
- **Lua** (`lua`, `lua_code_mode`) - sandboxed Lua 5.4 VM (mlua) with memory/instruction/time/output caps, `fs.*`/`json.*` bridges over the session FS, optional allowlisted HTTP, and `tools.*` bridging; `lua_code_mode` routes tool definitions into scripts. Experimental, admin-gated; A/B research against bashkit showed mlua at parity with fewer tool calls. (`integrations/lua`; `research/lua-vs-bash`)
- **Web fetch** (`web_fetch`) - fetch/extract/crawl to markdown over host egress with SSRF controls, optional file download into the workspace, optional bot-auth signing. (`integrations/web-fetch`)

### Sandboxed compute integrations

- **Daytona** (`daytona`) - cloud sandboxes: create/exec/files/git/snapshots; per-session leased sandboxes with durable cleanup. (`integrations/daytona`)
- **E2B** (`e2b`) - cloud sandboxes via Connect-RPC with connection-scoped keys. (`integrations/e2b`)
- **Docker** (`docker_container`) - self-hosted session-scoped containers via Docker Engine API with CPU/memory/pids limits and isolated networks; fills the gap between bashkit and cloud sandboxes. (`integrations/docker`; `knowledge/runtime-resources/container-sandbox.md`)
- **Sprites** (`sprites`) - persistent Firecracker microVMs whose state survives across sessions. (`integrations/sprites`)
- **Deno** (`deno`) - Deno cloud sandboxes (marked unsupported without a paid plan). (`integrations/deno`)
- **Browserless** (`browserless`) - headless cloud browser: navigate, screenshot, scrape, interact over CDP, with secret placeholders in interact steps. (`integrations/browserless`)

### Search and information

- **Brave Search** (`brave_search`) - full web search tool. **DuckDuckGo** (`duckduckgo`) - keyless instant answers. **Parallel** (`parallel_search`) - hosted MCP search/fetch, with a payment-gated variant behind `machine_payments`.
- **Knowledge bases and indexes** - org-scoped document knowledge with hybrid ANN+BM25 retrieval (Turbopuffer backend, server-side RRF, org-prefixed namespaces), claim-level citation retrieval, and citation faithfulness verification. (`everruns-turbopuffer`; platform `knowledge_store`)
- **OpenRouter server tools** - provider-executed web search/fetch/datetime/image tools; also key/workspace policy inspection and a bounded model-scouting blueprint. (`integrations/openrouter-workspace`)

### Agent-facing utilities

- **Current time**, **message metadata** (timestamps for timing-aware reasoning), **session metadata** (inspect/update, automatic titles), **session storage** (key/value plus encrypted secrets), **session SQLite** (per-session SQL database), **stateless todo list** (plan state kept only in conversation tool history), **system commands**, **btw** and **human intent** (human signaling channels).

## 4. Context management

- **Compaction** - strategies: Auto (cascade), native provider compact, observation masking, summarization. Proactive trigger at a configurable percentage of the context budget (default 85%); emits `context.compacting`/`context.compacted` events; durable checkpoints let compacted state survive crashes; cumulative-cost accounting on checkpoints. Storage is lossless; only the model view is compacted. (`everruns-builtins::CompactionCapability`; `knowledge/runtime-resources/compaction.md`)
- **Infinity context** - keeps a recent window in the prompt and exposes `query_history` so the agent pulls older messages on demand; a filter-only mode works without the tool. Project guidance: compaction is the primary strategy, infinity context is the lossless pull backstop, and infinity defers eviction when both are enabled. (`InfinityContextCapability`; `research/infinity_context`)
- **Tool search / deferred schemas** - `ToolSearch::automatic()` picks OpenAI or Claude native tool search when supported, else client-side deferred loading; threshold plus a `never_defer` list keep large tool catalogs out of the prompt until needed. (`auto_tool_search` family)
- **Prompt caching** - marks stable prompt prefixes for providers that support caching. (`PromptCachingCapability`)

## 5. Instructions, skills, plugins

- **AGENTS.md injection** (`agent_instructions`) - hierarchical AGENTS.md-style files from the session filesystem are injected as leading user-role context (not system prompt), wrapped in `<agent-instructions>`, with size budgets. (`everruns-builtins::AgentInstructionsCapability`; `docs/features/agent-instructions.md`)
- **Skills** - agentskills.io packages (a directory with `SKILL.md` plus optional `scripts/`, `references/`, `assets/`) discovered under `/.agents/skills/`; progressive disclosure: names/descriptions ship in `<available_skills>`, the agent calls `activate_skill` to load the full body; frontmatter supports `user-invocable` (slash commands) and `disable-model-invocation`. (`docs/features/skills.mdx`)
- **Skills registry** - org-wide skill packages (SKILL.md or ZIP) with validation, assignable as virtual capabilities `skill:{uuid}`. (`docs/features/skills-registry.md`)
- **Plugins** - `.plugin(path)` compiles a trusted local directory into a declarative capability contribution (instructions + tools + scoped MCP); platform plugins install as `plugin:{install_id}`; portable `plugin.json`/`mcp.json` format with host manifests for Claude/Codex/Cursor. (`everruns::plugin`; `knowledge/integrations/plugins.md`)
- **Agentic Resource Discovery (ARD)** - experimental `discover_resources`/`attach_resource`/`list_attached_resources` against allowlisted registries; mid-session attach of MCP/A2A resources behind trust and SSRF gates. (`everruns-ard`)

## 6. Events and observability

- **Event log as source of truth** - one append-only canonical event log per session; messages, SSE streams, tracing, replay, and reporting are all projections of it. (`docs/explanation/events.md`; `everruns-host::EventLog` with in-memory and JSONL implementations)
- **Live event stream** - `Session::events()` is a bounded broadcast (capacity 4096); lag is reported, never backpressured. Reviewed kinds include input, turn lifecycle, text deltas, output replacement, tool start/progress/delta/complete, reasoning deltas/items, and `ModelGeneration` (tokens/cost/latency). (`everruns::EventStream`)
- **Canonical event taxonomy** - `turn.*`, `reason.*`, `act.*`, `tool.*`, `llm.generation`, `context.compact*`, session lifecycle, file-written, token usage, retry info. (`everruns-core::events`; `docs/event-reference.md`)
- **SSE consumption** - live tail with `since_id` resume for reconnection. (`docs/how-to/consume-events-via-sse.md`)
- **OpenTelemetry** - per-turn `invoke_agent` traces over OTLP with Gen-AI and OpenInference span conventions; tokens, cost, tool timings, errors; privacy off by default. **Braintrust** exporter for session-grouped traces with TTFT. (`docs/observability/`)
- **Reasoning as artifacts** - reasoning is an ordered, replayable content part (`ContentPart::Reasoning`) with phase source metadata, projected at the API edge on both messages and events.
- **ATIF export** - session and eval trajectories fold from the event log into ATIF interchange format. (`knowledge/evaluation/atif-adoption.md`)

## 7. Lifecycle, cancellation, hooks

- **Cooperative cancellation** - `CancellationToken`/`TurnHandle::cancel`; dropping the turn future tears down in-flight tools; pre-cancelled tokens stop before start; completion hooks are never interrupted once committed. Cluster-wide, cancel rides workflow signals plus heartbeat-propagated cancel flags.
- **Application lifecycle hooks** - awaited, non-mutating: `on_agent_start`, `on_turn_start`, `on_tool_start`, `on_tool_end`, `on_completion`. Pre-effect failures block work; post-effect failures land in `Turn::hook_failures`. (`everruns::hooks`)
- **Engine tool hooks** - `PreToolUseHook`, `PostToolExecHook`, `PostActHook`, client-side tool hook, output hard-limit hook, connection/URL elicitation hooks. (`everruns-core::tool_hooks`)
- **User hooks** (`user_hooks`) - user shell hooks on lifecycle/tool events that can block, mutate, or audit; ships as ready-made bundles (block `rm`, format-on-edit, audit). (`docs/capabilities/user-hooks.md`; `examples/hook-bundles`)

## 8. Model providers

- **Provider abstraction** - `Provider` bundles endpoint/auth plus a `ChatDriver`; drivers implement streaming chat, optional model listing, optional native compaction. Ships drivers for OpenAI (Responses + OpenResponses), Anthropic, Gemini, Bedrock, Fireworks, OpenRouter, Meta, MAI, Azure OpenAI, and llmsim. Custom providers implement `ChatDriver` without coupling to a closed enum. (`everruns-provider`; `crates/drivers`)
- **Model profiles** - hardcoded registry (models.dev sourced) of limits, cost, modalities, reasoning effort, verbosity, and structured-output support, keyed by provider wire id; used for enrichment, cost estimates, and routing. (`everruns-model-profiles`)
- **Retries** - provider-level `LlmRetryConfig` (default 2 retries, exponential backoff with jitter, honors retry-after) for transient 429/5xx, separate from durable activity retry.
- **Reasoning and phases** - streaming reasoning deltas; `ReasoningEffort`; Commentary vs FinalAnswer execution phases derived in the Reason atom with optional provider wire mapping. (`knowledge/execution/execution-phases.md`)
- **Tool schema compatibility** - normalizes tool schemas into provider strict-JSON/structured-output subsets when advertising tools.

## 9. Memory and persistence

- **Persistence tiers** - volatile (engine-lifetime memory), local durable (SQLite session/task/schedule state plus crash-durable canonical event log plus Git workspace heads, via `.local(LocalConfig)`), and platform durable (PostgreSQL). (`docs/framework/persistence.md`)
- **Bounded history API** - `session.history()` pages with an opaque cursor (default 100, max 256), stable snapshots under concurrent append; ephemeral stream deltas are excluded from history. (`everruns::history`)
- **Memory mounts** - org/agent/user-scoped file-backed memory stores mounted into session workspaces with privacy rules across sessions; durable named file memory, distinct from vector RAG. (`everruns-platform::Memory`; `docs/features/memory-scopes.md`)
- **Session work and wakes** - application background tasks owned by a session (`WorkQueue`, leases, idempotency keys, `WakePolicy`), at-least-once delivery, pluggable durable backends. (`everruns::work`; `docs/framework/background-work.md`)
- **Workspaces and environments** - multi-head workspaces with read/write scopes; Git heads in local mode; environment binding before or on first send. (`docs/framework/workspaces-and-environments.md`)

## 10. Reliability and self-regulation

- **Loop detection** - flags repeated tool-call signatures. **Progress guard** - nudges when the agent explores without making progress. (`loop_detection`, `progress_guard` builtins)
- **Budgets** - core budget domain (usd/tokens/credits) with soft pause/warn/stop; the `budgeting` capability adds platform-enforced checks plus prompt awareness; `self_budget` is prompt-only indicative guidance; `AgentBuilder::max_iterations` caps reason/act loops per turn (platform default 10). Workers check budgets before spend; soft limits pause sessions. (`everruns-core::budget`; `docs/how-to/enforce-a-budget.md`)
- **Usage-limit auto-continue** - schedule-backed resume after an LLM plan usage limit resets. (`usage_limit_auto_continue`)
- **Guardrails** - declarative checks on model output and tool calls: regex/blocklist, tool restrictions, LLM judge, moderation, MCP-delegated checks; block vs log modes, advisory dry-run, streaming output replacement (`OutputReplaced` events). (`GuardrailsCapability`; `knowledge/execution/guardrails.md`)
- **Prompt canary** - withholds output if the model echoes a system-prompt canary (leak detection). (`PromptCanaryGuardrailCapability`)
- **Tool approval / human-in-the-loop** - `tool_approval` capability with an approver seam (`ApprovalDecision`/`ApprovalMode`); UI policy types `auto` | `requires_approval`; host approval plus tool cancellation wired through durable sessions.
- **Error disclosure** - controlled model-visible error detail (`error_disclosure` builtin).

## 11. Multi-agent features

- **Subagents** (`subagents`) - `spawn_agent` creates child sessions in isolated contexts, background-first, with nesting caps; children inherit the parent harness/config with no privilege escalation; durable reattach after crashes. (`knowledge/runtime-resources/subagents.md`)
- **Agent handoff** - allowlisted transfer to other first-class agents; tools and credentials are not shared. (`knowledge/runtime-resources/agent-handoff.md`)
- **A2A delegation** - outbound Agent2Agent as an opt-in Cargo feature; inbound A2A channel for apps; task results flow back over A2A/MCP.
- **Session participants** - multi-agent/multi-user sessions: host vs member roles, invites, @addressing a member for a single turn. (`docs/features/session-participants.md`)
- **Session tasks** - a uniform registry for subagents, background tools, and monitors: lifecycle, progress, messaging, input requests (answering resumes the task), cancel flags, artifacts, orphan reaping. Separates units of work from leased infrastructure. (`knowledge/runtime-resources/session-tasks.md`)
- **Blueprint subagents** - e.g. GitHub Scout: the host agent gets no GitHub tools; it spawns a read-only scout subagent (code/issues/PR search) that uses the `github` connection. (`integrations/github`)
- **Cursor Cloud Agents** (`cursor`) - delegates coding tasks to Cursor Background/Cloud Agents: launch, follow-up, conversation, list models/repos. (`integrations/cursor`)
- **Multi-agent pipelines** - documented pattern chaining sessions into pipelines. (`docs/how-to/orchestrate-multi-agent-pipelines.md`)

## 12. Durable execution platform

- **Event-sourced workflows** - every turn runs as a deterministic workflow; lifecycle changes are append-only `WorkflowEvent`s; state reconstructs by replay (optionally from snapshots taken every ~1000 events); crash recovery reclaims stale claimed tasks and resumes. Custom engine, deliberately not Temporal. (`everruns-durable`; `docs/explanation/durable-execution.md`)
- **Checkpointed turns** - `DurableExecution` bridges the engine's `TurnExecution` into durable storage; only engine-owned `TurnState` is checkpointed between input/reason/act activities; exactly-once tool results.
- **Activity queue** - activities with `RetryPolicy` (exponential backoff + jitter), schedule-to-start/start-to-close/heartbeat timeouts, distributed circuit breakers with store-shared state, and a dead-letter queue for exhausted work.
- **Continue-as-new** - long histories roll into a fresh workflow with the old one archived.
- **Forward-progress seal** - a turn reclaimed repeatedly with no progress is sealed dead (non-retryable); the control plane emits `turn.sealed` and idles the session. Stuck-turn guard.
- **Workflow signals** - `cancel`, `shutdown`, and `user_message` (steering) delivered into running workflows over gRPC.
- **Stateless workers** - workers hold no durable agent state: claim tasks, execute activities, heartbeat (heartbeats carry cancel requests), complete/fail. Push distribution via NATS-backed task notifications with polling fallback; capacity-aware claiming; stale-claim reclamation. (`everruns-worker`; `everruns-internal-protocol`)
- **Control plane** - org-scoped REST API (agents, sessions, messages, events SSE, harnesses, apps, schedules, budgets, knowledge, memory, MCP, webhooks, files, tasks, sandboxes) plus an internal gRPC `WorkerService`; OpenAPI published; API-key or cookie auth. (`everruns-server`)
- **Durable ops API** - platform-user routes for system health, workers, workflows, task queues, DLQ, circuit breakers, and SSE metrics, gated by `durable.view`/`durable.manage` policies.
- **Host composition boundary** - one effectful path (`HostComposition`, `RuntimeHostAdapter`) shared by the in-process host and durable workers, so local and cluster execution cannot drift. (`everruns-host`)

## 13. Scheduling and triggers

- **Agent triggers** - agent-owned cron schedules with timezone, session mode (shared vs per-invocation), and message templates; fire through a durable activity; outcome history and manual test runs. Replacement for the deprecated App schedule channel. (`docs/features/agent-triggers.md`)
- **Session schedules** - per-session cron/one-shot schedules that inject user messages (`metadata.source = "schedule"`) and wake the session; monitor tasks can run probe tools without a full agent turn; orphan sweep cancels dead monitors.
- **Durable scheduler** - platform-wide cron engine: `FOR UPDATE SKIP LOCKED` polling, multi-instance heartbeats, fair org scheduling, catch-up, max concurrency.
- **Workflow timers** - `StartTimer` actions with timer-fired events.
- **Webhooks** - inbound token-authenticated app-channel webhooks that start sessions/turns with per-channel IP rate limits; outbound task webhooks on terminal session-task transitions with optional HMAC signing.

## 14. Multi-tenancy and security

- **Organizations and roles** - `Organization`, `OrgMembership`, `Principal` with Member/Admin/Owner roles; pluggable org-create policy; org-scoped repositories and vector namespaces.
- **Policy-based authorization** - declarative `Policy`/`Rule` evaluation; deployment- and org-level feature flags.
- **Audit log** - `AuditEvent`/`AuditLogger` for management and agent actions.
- **Threat model as artifact** - stable threat IDs across auth, tenant isolation, permissions, tool execution, LLM integration, sandboxes, durable execution, and channels, each with documented mitigation and test coverage. (`knowledge/security/threat-model.md`)
- **Encryption** - column-level encryption for sensitive stored fields; session secrets store; secure MCP credential handling.
- **Egress governance** - SSRF controls, network allow/block lists, default-deny bashkit networking, dedicated egress service. (`docs/advanced/network-access.md`)
- **MCP URL elicitation** - a turn pauses and opens a browser consent flow for secrets/auth/payment so values never pass through the client or the model; consent persists in session storage and works across worker processes. (`docs/features/mcp-url-elicitation.md`)

## 15. Distribution: apps and channels

- **Apps** - bind a harness + agent to inbound channels with auth modes, session routing (`per_thread`/`per_channel`/`per_user`), and a draft -> publish -> archive lifecycle, so one agent ships to many surfaces independently. (`docs/features/apps.md`)
- **Channels** - Slack bot (HMAC-verified Events API, async replies), AG-UI interactive UI, webhook/HTTP, A2A, FCP HTTP, public chat (stripped tool activity), realtime voice (changelog-era). WhatsApp and web widget listed as planned.
- **MCP server** - Everruns itself is an MCP server (agents/tools exposed, OAuth 2.1); as MCP client it mounts remote servers as virtual capabilities `mcp:{uuid}` with tool discovery, elicitation consent, and SSRF-pinned egress. (`docs/features/mcp.md`)
- **Agent versions** - immutable snapshots with semver and change kinds (manual/patch/rollback/fork); sessions bind a version for deterministic runtime; apps pin default/latest/pinned version policy. (`docs/features/agent-versions.md`)
- **CLI and SDKs** - agent-first CLI (`everruns <noun> <verb>` tree shared by MCP, session shell, and CLI hosts) managing agents, sessions, files, triggers with text/JSON/YAML output; typed Rust/Python/TypeScript SDKs with SSE reconnection.
- **File-defined agents** - agents authored as importable definition files. (`docs/how-to/define-agents-as-files.md`)

## 16. Harnesses (the feature most relevant to promptforge)

- **Harness as base environment** - capabilities + optional system prompt + starter files + model defaults, with live single-parent inheritance (`parent_harness_id`) and merge/chain resolution into a runtime `HarnessDefinition`. Agents and sessions resolve harnesses by id or name. (`knowledge/harnesses/harness-types.md`; `everruns-platform::harness`)
- **Built-in harnesses** - `base` (zero tools, full manual composition), `generic` (batteries: filesystem, bashkit, web fetch, storage, session, schedules, AGENTS.md, skills, infinity context, tool search, compaction, budgeting), `platform-chat` (focused operator surface, no filesystem/shell/web-fetch), `data-analyst` (SQL, charts, persistent memory). Importable examples: `coding-daytona`, `coding-container`, `data-analyst`. (`docs/built-ins/`)
- **Two-level coding execution** - the coding harness steers light work to the workspace VFS/bashkit and real git/build/test to a Daytona sandbox, with prompt-driven tool choice and an edit-test-fix loop. (`knowledge/harnesses/coding-daytona-harness.md`)
- **Sandbox abstraction (proposed)** - one logical sandbox per session (filesystem + optional compute) behind provider-neutral tools, disposable physical incarnations with generation fencing, and agent-step checkpoints so tool results commit only when worktree state is recoverable; consolidates the split-brain VFS-vs-provider-sandbox tools. (`knowledge/harnesses/sandbox-abstraction.md`)
- **Managed session sandboxes** - one sandbox per session with auto-start/resume, idle pause (~3 min), volume recovery on physical loss, and provider-neutral `sandbox_*` tools; leased-resource cleanup survives restarts. (`knowledge/runtime-resources/session-sandbox.md`)

## 17. Evaluation and quality

- **Evals** - org-scoped behavioral tests: cases spawn real sessions, scorers grade 0-1 (expected/forbidden tools, response regex, file expectations, tool-call budgets), durable runs, artifacts link to debuggable conversations; targets are session setups or apps; used to compare models and gate app publishes. (`docs/features/evals.md`)
- **SWE-bench Lite** - coding-agent benchmark on the same eval machinery, separating agent patch generation from official pass/fail scoring. (`evals/swe-bench`)
- **Observers (online evals)** - LLM-as-judge scoring of production traffic, asynchronous, never on the hot path. (`knowledge/evaluation/online-evals.md`)
- **Agent checks** - advisory lint/LLM/health checks on resolved agent config (structure, completeness, cost); never block save/publish. (`docs/features/agent-checks.md`)
- **External results** - import externally executed eval results (e.g. Mira studies) into Everruns reporting; ATIF dataset export.
- **Failure injection** - fail-rs based reliability tests; threat-model tests; DeepSec scanning. (`knowledge/security/security-testing.md`)

## 18. Management UI surfaces (apps/ui, Next.js)

- **Session views** - transcript, timeline, work (tasks/subagents), raw events, files (workspace), cost (token usage); live SSE chat with thinking and tool activity; slash commands with skill autocomplete; MCP elicitation consent dialogs; destructive-tool approval gates.
- **Registries** - agents, harnesses, identities, skills, memory, knowledge indexes, models, capabilities (including declarative), MCP servers, plugins, observers.
- **Ops** - evals runs/compare, durable queues/schedules/workers/workflows/circuit breakers, reports, connections (integration keys/OAuth), providers, payments, feature flags.

## 19. Feature trajectory (CHANGELOG highlights, recent first)

- 0.24: ~3.5x faster agent startup; MCP URL elicitation; Gen-AI/OpenInference traces.
- 0.22: reasoning as ordered replayable artifacts; bounded batch file reads.
- 0.21: chat with harnesses; generated run summaries.
- 0.20: hot-register capabilities on a running runtime; A2A delegation feature.
- 0.19: first-class sandbox and checkpoint records for durable runs.
- 0.18: neutral kernel/platform split; unified in-process and durable execution; multi-head workspaces.
- 0.17.x: steerable sessions; canonical events; session work/wake API; agent plugins; interrupted-turn recovery; host approval; cost-aware context checkpoints; tool narration; session tasks; scoped memory; detached/handoff sessions; background subagents; session forking; tool-call repair; parallel tool calls; knowledge indexes; ARD; guardrails; realtime voice; skills discovery.

---

## Appendix: crate map

| Crate | Role |
|---|---|
| `everruns` | Application facade: Agent/Engine/Session/Turn/events/hooks/tools/MCP/work/local |
| `everruns-core` | Neutral contracts: capabilities, tools, events, messages, budgets, MCP types, subagent delegation, compaction |
| `everruns-engine` | Input/Reason/Act algorithms plus sans-IO turn planner |
| `everruns-capability` | Capability id/config plus code-defined Definition/Handler |
| `everruns-builtins` | Portable policy capabilities (compaction, guardrails, tool search, skills, AGENTS.md, budgets, ...) |
| `everruns-macros` | `#[everruns::tool]` |
| `everruns-provider` / `drivers` | Providers, ChatDriver, streams, retries, compaction, model specs; per-vendor wire drivers |
| `everruns-model-profiles` | Model capability/cost/limits registry |
| `everruns-mcp` | MCP client transport and executor |
| `everruns-ard` | Mid-session resource discovery/attach |
| `everruns-durable` | Event-sourced workflows, activities, retries, circuit breakers, scheduler, snapshots |
| `everruns-host` | Host composition boundary shared by in-process and durable execution |
| `everruns-worker` | Stateless task workers (claim/execute/heartbeat) |
| `everruns-server` | Control plane REST + internal gRPC + storage |
| `everruns-platform` | Platform domain: orgs, budgets, harnesses, apps, triggers, memory, versions |
| `everruns-turbopuffer` | Vector store backend (hybrid ANN+BM25) |
| `everruns-cli` | Agent-first CLI |
| `integrations/*` | Capability crates: bashkit, filesystem, lua, web-fetch, daytona, e2b, docker, deno, sprites, browserless, brave-search, duckduckgo, parallel, github, cursor, openai-image, openrouter-workspace |

*2026-09-12 16:05 - kimi-k3*


