---
produced: 2026-09-19
title: everruns capability survey - non-tool contribution kinds (mounts, durability, hooks, memory, scheduling, channels, policy)
source: c:\Users\Vinnie\cursor\everruns
---

# everruns capability survey: what a capability contributes besides tools

Scope: read-only survey of `c:\Users\Vinnie\cursor\everruns` (Rust agent runtime, edition 2024). Every claim cites `path:line` relative to the repo root. Quotes are verbatim from source except that em dashes in the original are rendered as a plain dash here. Where the sources do not support a claim the text says "not in the sources".

## What everruns calls a capability

everruns splits "capability" across three layers, and the split itself is the first design lesson.

### Layer 1: the neutral identity and configuration contract (`crates/capability/`)

The crate doc states its role: "One open identity/configuration contract shared by the `everruns` Framework, the hosted product composition, and integration crates" (`crates/capability/src/lib.rs:3-4`). It lists exactly five things it owns (`crates/capability/src/lib.rs:6-20`): `CapabilityId`, `CapabilityRef`, `CapabilitySpec` plus `IntoCapability`, `Definition` (behind feature `definition`), and `CapabilityIdIndex` plus `ActivationSet`. It "deliberately depends on neither `everruns-core` nor `everruns-host`, and carries no Tokio, HTTP, SQLx, OpenAPI, inventory, or platform-record dependency" (`crates/capability/src/lib.rs:22-24`).

Id grammar. "IDs are open strings rather than variants in a central enum, so new capabilities can be added without database migrations or Everruns source edits. A stable identifier is made from ASCII letters, digits, `_`, `-`, `.`, or `:`, starts with a letter or `_`, and fits within 128 bytes; the `__everruns_` namespace is reserved." (`crates/capability/src/id.rs:15-19`). Note that `/` is rejected: the test table lists `("vendor/custom", "may only contain")` as invalid (`crates/capability/src/id.rs:230`). Namespacing is done with a colon prefix, not a slash: "`plugin:` is one of the open reference namespaces (`mcp:`, `skill:`, `declarative:`, `plugin:`)" (`crates/capability/src/id.rs:162-163`). `CapabilityId::new` is infallible; validation happens at boundaries: "boundaries that accept new identifiers (Framework agent build, product write paths) enforce the grammar" (`crates/capability/src/id.rs:21-25`).

Reference. `CapabilityRef` is "a reference to a capability implementation plus per-agent JSON" and "the one semantic model for 'a capability attached to an agent': the Framework activates it, the product persists it ... and worker resolution consumes it. It serializes as `{"ref": "<id>", "config": {...}}` everywhere." (`crates/capability/src/reference.rs:11-17`). Config "defaults to `{}` and must be a JSON object" and "the referenced implementation owns the inner schema" (`crates/capability/src/reference.rs:24-27`). Config is redacted from `Debug` but "it is not a secret store ... Put credentials in a provider-owned secret mechanism and pass only a non-secret handle here." (`crates/capability/src/reference.rs:29-31`).

Spec. `IntoCapability` is "intentionally public and non-sealed. Third-party crates can implement it without depending on `everruns-core` or host internals" (`crates/capability/src/spec.rs:8-9`). "A spec always activates exactly one `CapabilityRef`. With the `definition` feature it may also carry the matching code-defined `Definition` that the host must register." (`crates/capability/src/spec.rs:40-42`). "Duplicate IDs are never merged and later registrations never overwrite earlier ones." (`crates/capability/src/spec.rs:46-47`).

Registry bookkeeping. `CapabilityIdIndex` "Owns the identity bookkeeping every registry needs: which canonical ids exist, which legacy aliases resolve to them, and collision rejection" (`crates/capability/src/registry.rs:10-12`). `ActivationSet` is the "Duplicate-activation guard used when composing an agent's capability set" where "the second activation of the same canonical id fails with `CapabilityError::Duplicate`" (`crates/capability/src/registry.rs:100-105`). `CapabilityError` has four variants: `InvalidId`, `InvalidConfig`, `InvalidDefinition`, `Duplicate` (`crates/capability/src/error.rs:16-44`).

Code-defined `Definition`. "A definition is an immutable value: clone it to install the same capability on several agents. The consuming host registers it privately when the agent's session starts; capability authors never manipulate an engine registry." (`crates/capability/src/definition.rs:85-90`). Its fields are `id, name, description, instructions: Option<String>, metadata: Option<Value>, tools: Vec<Tool>` (`crates/capability/src/definition.rs:92-99`). `instructions` is prompt text: "Add capability-level behavioral guidance to the agent's system prompt." (`crates/capability/src/definition.rs:123`). Validation requires at least one tool: `"capability must define at least one tool"` (`crates/capability/src/definition.rs:200-202`). So at this neutral layer a third-party capability is tools plus a prompt fragment plus opaque metadata. The per-call `Context` is "a narrow projection: identity, locale, progress, and cancellation. Backend stores, credentials, tenant objects, registries, and host extensions intentionally remain host implementation details." (`crates/capability/src/definition.rs:492-495`). Host seams are `ProgressSink` (`crates/capability/src/definition.rs:450-458`) and `CancellationSignal` (`crates/capability/src/definition.rs:460-469`).

### Layer 2: the runtime `Capability` trait (`crates/core/src/capabilities/mod.rs`)

The module doc: "Each capability can contribute: - System prompt additions - Tools for the agent - Behavior modifications (future)" (`crates/core/src/capabilities/mod.rs:4-7`). The "(future)" is stale: the trait now has roughly forty methods. `pub trait Capability: Send + Sync` (`crates/core/src/capabilities/mod.rs:288`). Grouped by what they hand the run:

- Identity and catalog: `id`, `aliases`, `name`, `description`, `localizations`, `status`, `icon`, `category`, `metadata`, `is_guardrail`, `risk_level`, `features`, `config_schema`, `config_ui_schema`, `validate_config`, `dependencies` (`crates/core/src/capabilities/mod.rs:298-387, 551-605, 915-924`).
- Prompt surface: `system_prompt_addition`, `system_prompt_contribution(_with_config)`, `system_prompt_preview`, `conversation_context_contribution(_with_config)`, `facts` (`crates/core/src/capabilities/mod.rs:403-454, 491-532, 731-747`).
- Tools: `tools`, `tools_with_config`, `tool_definitions`, `native_async_tools`, `delegation_target_with_config`, `auto_activates_for` (`crates/core/src/capabilities/mod.rs:291-296, 456-489, 534-538`).
- Filesystem: `mounts`, `contribute_skills` (`crates/core/src/capabilities/mod.rs:540-549, 973-985`).
- History shaping: `message_filter_provider`, `message_filter_config`, `model_view_provider`, `compaction_policy` (`crates/core/src/capabilities/mod.rs:621-658, 721-729`).
- Hooks: `pre_tool_use_hooks(_with_config)`, `post_tool_exec_hooks(_with_config)`, `tool_definition_hooks(_with_config/_with_context)`, `tool_call_hooks`, `finalized_tool_calls_hook`, `narrate`, `user_hooks(_with_config)`, `llm_error_hook`, `output_guardrails`, `post_output_guardrails_with_config`, `post_output_annotation_hooks_with_config`, `citation_verifier_with_config`, `filter_response_text` (`crates/core/src/capabilities/mod.rs:660-673, 715-719, 749-913, 987-1055`).
- Provider request shaping: `tool_search_config`, `prompt_cache_config`, `driver_options`, `parallel_tool_calls_preference`, `error_disclosure`, `resolve_for_model` (`crates/core/src/capabilities/mod.rs:389-401, 675-713`).
- Remote servers and commands: `mcp_servers(_with_config)`, `commands`, `execute_command`, `agent_blueprints` (`crates/core/src/capabilities/mod.rs:607-619, 926-971`).

Registration. `CapabilityRegistry` holds `HashMap<String, Arc<dyn Capability>>` plus a `CapabilityIdIndex` "delegated to the neutral capability contract so the Framework and product resolve identity identically" (`crates/core/src/capabilities/mod.rs:1202-1208`). Integration crates can also self-register through `inventory`: "Integration crates use `inventory::submit!` to register their capabilities without requiring `everruns-core` to know about them at compile time. Host or product composition iterates these descriptors and applies its deployment-grade and feature-selection policy." (`crates/core/src/capabilities/mod.rs:45-49`), with `experimental_only` and `feature_flag` gates (`crates/core/src/capabilities/mod.rs:63-73`). The portable bundle explicitly rejects this: "Registration is explicit: linking this crate has no inventory side effect." (`crates/builtins/src/lib.rs:224`).

Activation. `collect_capabilities_with_configs(capability_configs, registry, ctx)` iterates ordered `CapabilityRef`s (`crates/core/src/capabilities/mod.rs:2416-2420`). For `declarative:` and `plugin:` refs the config itself carries a serialized `DeclarativeCapabilityDefinition` (`crates/core/src/capabilities/mod.rs:2452-2459`). Otherwise the registry is consulted; inert statuses are skipped: "`ComingSoon` is not implemented yet and `Retired` has been removed. Both resolve to a no-op rather than an error so an agent that still references one keeps running." (`crates/core/src/capabilities/mod.rs:2496-2501`). Then `resolve_for_model` may swap in a different implementation while "Attribution stays on the configured `cap_id`/`capability`" (`crates/core/src/capabilities/mod.rs:2502-2518`). The result is `CollectedCapabilities` (`crates/core/src/capabilities/mod.rs:1428-1475`), and `apply_capabilities` folds it into a `RuntimeAgent` plus a `ToolRegistry` (`crates/core/src/capabilities/mod.rs:2760-2816`).

Capability instances are process-global singletons: "the capability is a process-global singleton shared across sessions and a `ToolDefinitionHook::transform` has no session context of its own" (`crates/core/src/capabilities/mod.rs:825-827`). Per-session state therefore lives in what the capability returns (hooks capturing `ctx.session_id`) or in host stores, not in the capability struct.

### Layer 3: implementation bundles

The knowledge spec: "Capability identity/configuration lives in `everruns-capability`. Runtime execution contracts, the registry, and neutral collection algorithms live in `everruns-core`. Portable implementations live in `everruns-builtins`; environment and hosted implementations live in their owning integration/product crates. No implementation bundle registers itself merely by being linked." (`knowledge/execution/capabilities.md:150-155`). `everruns-builtins` "owns no server, database, network transport, process runner, interpreter, or hosted service implementation" (`crates/builtins/src/lib.rs:6-7`). Hosted ones ("Knowledge Bases and Knowledge Indexes, Memories, subagents and agent handoff, background/session tasks and schedules, user hooks ... need hosted persistence or orchestration") live in `everruns-platform` (`docs/framework/capability-boundaries.md:22-27`).

Framework bridge. In the `everruns` crate, `Agent::builder().capability(x)` accepts any `IntoCapability`; validation and duplicate detection happen in `build`: "A stable ID may be activated only once; duplicate inputs are errors rather than last-write-wins overrides." (`crates/everruns/src/agent.rs:947-954`). A `Definition` is adapted to the core trait by `RuntimeDefinition`, which maps `instructions_text` to `system_prompt_addition`, `metadata_value` to `metadata`, and each typed tool to a `CoreToolAdapter` (`crates/everruns/src/capability.rs:99-137`).

## Candidates

Each candidate is a distinct kind of run-scoped or session-scoped contribution that is not merely a set of model-callable tools. Where a capability also ships tools, the tools are noted but are not the point.

### 1. Filesystem mounts (inline, virtual, read-only or read-write)

(a) A capability declares files and directories that are materialized into the session filesystem when the session is created.

(b) Contribution kind: mount. `MountPoint { path, access: MountAccess, source: MountSource, capability_id }` (`crates/core/src/capability_types.rs:338-347`). `MountAccess` is `ReadOnly` (default) or `ReadWrite` (`crates/core/src/capability_types.rs:240-248`). `MountSource` is `InlineFile { content, encoding }`, `InlineDirectory { entries }`, or `Virtual { tree: Arc<VirtualFileTree> }` which is "A virtual file tree served from memory. Read-only, shared across sessions via Arc. No DB rows created" (`crates/core/src/capability_types.rs:259-277`).

(c) Lifecycle: per session, applied once at creation. The server's `SessionService::create` calls `apply_capability_mounts` ("Apply capability mounts (harness + agent + session capabilities) and seed initial files into the session's workspace. Key by workspace_id (not session id) so an attached shared workspace receives them", `crates/server/src/domains/sessions/service.rs:907-911`). Virtual mounts are "registered in the `VirtualMountRegistry` (per-session, in-memory) instead of being written to the database" and "evicted from the registry on session delete" (`knowledge/execution/capabilities.md:1180-1185`). Skill contributions are normalized into mounts too: "Contributions are normalized during capability collection into read-only mount points at `/.agents/skills/{name}/`" (`crates/core/src/capabilities/mod.rs:976-977`).

(d) Host services: a `SessionFileSystem` implementation (`crates/core/src/session_services.rs` is the storage side; `SystemPromptContext.file_store: Option<Arc<dyn SessionFileSystem>>`, `crates/core/src/capabilities/mod.rs:133-134`). No network, clock, or secrets.

(e) Evidence: "Mount points allow capabilities to provide files and directories that are automatically created when a session starts. This is useful for providing sample data, documentation, or configuration files." (`crates/core/src/capabilities/mod.rs:542-544`). The `memory` capability is mount-only: "Mount org-scoped, named Memories into the session workspace as read-only reference data or read-write shared working memory." (`crates/platform/src/capabilities/memory.rs:34-35`), depends on `session_file_system` and contributes feature `file_system` (`crates/platform/src/capabilities/memory.rs:50-56`), and is `RiskLevel::Medium` because "Read-write shared mounts let one session influence future sessions" (`crates/platform/src/capabilities/memory.rs:58-62`). Declarative capabilities carry `files: Vec<DeclarativeCapabilityFile>` with `path, content, access` (`crates/core/src/capabilities/declarative.rs:51-52, 61-67`).

(f) Placement: a trait method on `Capability` (`mounts()`), so any capability may mount. The `memory` implementation is hosted (`everruns-platform`) because it resolves org-scoped Memory records; `data_knowledge` "is the registered built-in that carries mounts in product registries" (`knowledge/execution/capabilities.md:1201-1202`).

### 2. Prompt fragments in two trust tiers (system prompt vs conversation context)

(a) A capability injects text into the model's context, choosing between the cached system-prompt prefix and a per-turn leading user-role message based on trust.

(b) Contribution kind: prompt fragment. `system_prompt_contribution(_with_config)` returns text "included as-is in the final prompt (the capability is responsible for its own XML wrapping)"; default wraps `system_prompt_addition()` in `<capability id="...">` tags (`crates/core/src/capabilities/mod.rs:426-445`). `conversation_context_contribution` "renders as the leading user-role message of every turn: model-visible and re-resolved alongside the system prompt, but never folded into the cached system prompt. This is the correct sink for untrusted workspace content (e.g. AGENTS.md hierarchies): it keeps file instructions below harness safety instructions in the instruction hierarchy and out of the cache-stable prefix." (`crates/core/src/capabilities/mod.rs:505-513`). Each part carries `SystemPromptAttribution { capability_id, content }` (`crates/core/src/capabilities/mod.rs:1478-1481`).

(c) Lifecycle: collected per turn in `collect_capabilities_with_configs` (`crates/core/src/capabilities/mod.rs:2522-2547`); `agent_instructions` is "Re-resolved every turn so edits are picked up immediately" (`crates/builtins/src/agent_instructions.rs:19`). No teardown.

(d) Host services: `SystemPromptContext { session_id, locale, file_store, model, session_storage }` (`crates/core/src/capabilities/mod.rs:128-146`). `agent_instructions` reads the session filesystem; `channel_context` reads the session KV store ("`None` for callers that do not provide one; such capabilities then contribute nothing", `crates/core/src/capabilities/mod.rs:141-145`).

(e) Evidence: content contract, "System prompt additions must NOT repeat information already present in tool names, descriptions, or parameter schemas." (`crates/core/src/capabilities/mod.rs:409-411`). `channel_context`: "Deliberately conversation context, not system prompt. Participant display names and the platform's view report are external user-controlled strings - the same trust class as workspace `AGENTS.md` - so they belong below the harness safety instructions and outside the cache-stable prefix" (`crates/builtins/src/channel_context.rs:8-11`). Prompt-only capabilities exist: OpenUI "provides no tools. It instructs the LLM to output OpenUI Lang code" (`knowledge/execution/capabilities.md:896-898`).

(f) Placement: trait methods on `Capability`; implementations are portable builtins (`agent_instructions`, `channel_context`, `openui`, `a2ui`). Declarative capabilities carry a `system_prompt: Option<String>` field (`crates/core/src/capabilities/declarative.rs:45-46`).

### 3. Facts with volatility routing (cache-friendly dynamic context)

(a) A capability contributes key/value facts and the runtime decides where to render them so provider prompt caching survives.

(b) Contribution kind: prompt fragment with placement policy. `Fact { key, value, volatility }`; `Volatility::Static` is "Folded into the cached system-prompt prefix at build time", `Volatility::Dynamic` "Changes turn to turn (e.g. current time, remaining budget). Appended at the conversation tail each request, outside the cached prefix." (`crates/core/src/capabilities/facts.rs:27-48`).

(c) Lifecycle: `facts()` is "Called both at prompt-assembly time (to fold static facts and detect whether any dynamic facts exist) and per request (to render the live tail block), so implementations must be cheap and side-effect free." (`crates/core/src/capabilities/mod.rs:740-742`). Dynamic facts are re-collected by `ReasonAtom` via `collect_dynamic_facts` (`crates/core/src/capabilities/mod.rs:2006`).

(d) Host services: none required; `FactsContext { session_id }` is "Deliberately minimal - facts are cheap, pure-ish descriptions of current context, not IO. Callers that need wall-clock time read it themselves" (`crates/core/src/capabilities/facts.rs:70-79`).

(e) Evidence: `current_time` "Contribute the current UTC time as a dynamic fact. The runtime appends it to a live `<facts>` block at the conversation tail each turn, so the model always knows 'now' without a tool round-trip and without the changing value invalidating the system-prompt cache." (`crates/builtins/src/current_time.rs:52-56`). Cache interaction: "The Anthropic driver anchors its message-level cache breakpoint on the last *non-volatile* block (`LlmCallConfig.volatile_suffix_len`) so the trailing block rides as an uncached suffix." (`crates/core/src/capabilities/facts.rs:20-22`).

(f) Placement: trait method `facts()`; `current_time` is a portable builtin.

### 4. History shaping: message filters, model-view providers, compaction policy

(a) A capability changes which stored messages are loaded and how they are rendered to the model, without changing what is persisted.

(b) Contribution kind: store-read policy plus view transform. `message_filter_provider()` "modify how messages are loaded from the database. This enables features like: - Time-based filtering ... - Ephemeral message injection (summaries, reminders)" (`crates/core/src/capabilities/mod.rs:621-634`). `model_view_provider()` builds "a prompt-facing model view from lossless stored messages before provider serialization ... Storage messages remain unchanged." (`crates/core/src/capabilities/mod.rs:649-658`). `compaction_policy()`: "The reason atom owns orchestration and invokes the returned implementation without matching on a capability ID." (`crates/core/src/capabilities/mod.rs:721-729`). `ModelViewProvider::apply_model_view(messages, config, context) -> Vec<Message>` with `priority()` ordering (`crates/core/src/capabilities/mod.rs:1411-1422`).

(c) Lifecycle: providers are collected per turn into `CollectedCapabilities.message_filter_providers: Vec<(Arc<dyn MessageFilterProvider>, serde_json::Value)>` "in priority order" (`crates/core/src/capabilities/mod.rs:1448-1449`); `message_filter_config(config, compaction_enabled)` lets one filter "coordinate with a separately selected compaction policy without core matching on either capability's ID" (`crates/core/src/capabilities/mod.rs:637-647`).

(d) Host services: message store (host-side), `ModelViewContext { session_id, prior_usage: Option<&TokenUsage> }` (`crates/core/src/capabilities/mod.rs:1401-1404`); summarization strategies need a utility LLM.

(e) Evidence: `compaction` contributes all three: `message_filter_provider` returns `CompactionFilterProvider`, `model_view_provider` returns `CompactionModelViewProvider` (`crates/builtins/src/compaction.rs:406-412`), `compaction_policy` returns `ConfiguredCompactionPolicy` (`crates/builtins/src/compaction.rs:472-476`). Strategies: "The `auto` cascade: observation masking -> native -> summarization" and "Proactive compaction at a configurable budget threshold, not just on error" (`crates/builtins/src/compaction.rs:10-11`). `loop_detection` uses "`MessageFilterProvider::post_load` only" (`knowledge/execution/capabilities.md:949`); `message_metadata` uses "`ModelViewProvider` only; priority 100, after compaction masking" (`knowledge/execution/capabilities.md:986`).

(f) Placement: trait methods; `compaction`, `loop_detection`, `message_metadata`, `infinity_context` are portable builtins.

### 5. Tool-execution interceptors: pre/post hooks, definition hooks, call hooks, approval gates

(a) A capability installs hooks that run around every tool call in the run, including tools it did not contribute, to block, mutate, or annotate.

(b) Contribution kind: hook / policy. `PreToolUseDecision::{Continue(ToolCall), Block { tool_call, reason, user_message }}` (`crates/core/src/tool_hooks.rs:7-21`); `PreToolUseHook::before_exec(tool_call, tool_def, context) -> PreToolUseDecision` (`crates/core/src/tool_hooks.rs:23-33`); `PostToolExecHook::after_exec(..., result: &mut ToolResult, ...)` with `PostToolExecHookPriority::{Guardrail = 0, Normal = 100}` (`crates/core/src/tool_hooks.rs:35-60`). `ToolDefinitionHook::transform(tools) -> Vec<ToolDefinition>` runs "after the runtime agent has merged and deduplicated its final tool list, before the tool schemas are sent to the LLM" (`crates/core/src/capabilities/mod.rs:796-801, 1058-1068`). `ToolCallHook::{narration, transform_for_execution}` (`crates/core/src/capabilities/mod.rs:1070-1085`). `finalized_tool_calls_hook` is "suitable for policy that needs all calls plus their final schemas before the assistant message is persisted" (`crates/core/src/capabilities/mod.rs:847-855`).

(c) Lifecycle: collected per turn (`crates/core/src/capabilities/mod.rs:2560-2570`); `tool_definition_hooks_with_context` exists so a singleton capability can key per-session state by `ctx.session_id` (`crates/core/src/capabilities/mod.rs:819-834`). `tool_approval` keeps "a single cache of 'always' answers ... shared across the session's turns" (`crates/builtins/src/tool_approval.rs:139-140`).

(d) Host services: `ToolContext` (see candidate 14 for the service enum). `tool_approval` needs a `ToolApprover`: "The approver is a constructor argument rather than a `ToolContext` service because a host without an interactive prompt should not register the gate at all - a registered gate with nowhere to ask is either a deadlock or a silent allow" (`crates/builtins/src/tool_approval.rs:10-13`).

(e) Evidence: "These hooks run before each individual tool is executed - for *every* tool the agent calls (built-in, MCP, or client-side), not just this capability's own tools. A hook can mutate the tool call or block it outright ... which makes this the seam for cross-cutting policy such as approval gating. The first hook to block wins." (`crates/core/src/capabilities/mod.rs:751-756`). `ToolApprover::approve` "Blocks the turn until it answers" and `ApprovalDecision::{Allow, AllowAlways, Reject, RejectAlways, Cancelled, Unavailable}` where `Unavailable` blocks because "a gate that fails open on transport failure is not a gate" (`crates/builtins/src/tool_approval.rs:33-62`). `guardrails` "Attaches the deterministic check engine ... to the existing interception seams - streaming output guardrails and pre/post tool hooks - driven entirely by per-agent config. No checks configured means no hooks contributed" (`crates/builtins/src/guardrails.rs:3-6`). `lua_code_mode` uses a `ToolDefinitionHook` to hide tools so the agent "orchestrates them inside a `lua` script" (`knowledge/execution/capabilities.md:1334-1338`).

(f) Placement: trait methods; `guardrails`, `progress_guard`, `tool_output_persistence`, `tool_output_distillation`, `tool_search` are portable builtins. `tool_approval` is "Not registered by default, it needs a host that can service an interactive prompt" (`knowledge/execution/capabilities.md:957`).

### 6. Output guardrails and post-generation annotation hooks

(a) A capability inspects the assistant's streamed text (per delta) or the finished message (once) and may replace it, or attaches citation annotations and verification verdicts.

(b) Contribution kind: hook / policy over model output. `output_guardrails()`: "Each provider is armed once per assistant message stream with the fully assembled system prompt and per-capability config; the returned per-stream `OutputGuardrailRun` is invoked after every batched delta in the streaming hot path. Returning `Block` aborts the stream" (`crates/core/src/capabilities/mod.rs:987-999`). `post_output_guardrails_with_config()`: "run **once** on the fully assembled assistant message after streaming completes ... They receive an LLM-capable context and may perform I/O (e.g. a moderation classifier)." (`crates/core/src/capabilities/mod.rs:1001-1017`). `post_output_annotation_hooks_with_config()` "attach citation `TextAnnotation`s to the message text" (`crates/core/src/capabilities/mod.rs:1019-1039`); `citation_verifier_with_config()` stamps "a `VerificationVerdict` on each citation. Decoupled from the feeds so any feed can be paired with any verifier." (`crates/core/src/capabilities/mod.rs:1041-1055`).

(c) Lifecycle: per stream. Deliberately not collected at activation: "output guardrails are intentionally NOT collected here. They are re-derived per turn in `ReasonAtom` directly from the resolved capability configs + registry, because they need the assembled system prompt at arming time" (`crates/core/src/capabilities/mod.rs:1470-1474`). "`arm()` returns a fresh `Box<dyn OutputGuardrailRun>` per stream so guardrails can hold cursors, dedup tables, etc. without sharing across sessions" (`knowledge/execution/capabilities.md:1456`).

(d) Host services: streaming guardrails need none (sync, "substring matches, regex, hash lookups; not network calls or LLM inference", `knowledge/execution/capabilities.md:1423`); post-generation ones receive a utility LLM.

(e) Evidence: `prompt_canary_guardrail` "withholds the assistant message when the model echoes the first sentence of its system prompt" using "`output_guardrails()` only" (`knowledge/execution/capabilities.md:994-996`). `guardrails` supports `stage: output | tool_use | tool_output` and `type: regex | blocklist | tool_pattern | llm_judge | mcp | moderation` (`crates/builtins/src/guardrails.rs:99-107`).

(f) Placement: trait methods; `prompt_canary_guardrail` and `guardrails` are portable builtins marked `is_guardrail()` (`crates/builtins/src/guardrails.rs:73-75`); `citation_retrieval` and `citation_verification` are hosted (`crates/platform/src/capabilities/citation_retrieval.rs`, `citation_verification.rs`).

### 7. Lifecycle hooks: user-authored shell hooks and Framework typed closures

(a) A capability contributes handlers that fire at session and turn boundaries (start, prompt submit, tool use, turn end, session end), either as data specs executed by a central sandboxed executor or as in-process closures.

(b) Contribution kind: hook (lifecycle observer/interceptor). Six events: `HookEvent::{SessionStart, UserPromptSubmit, PreToolUse, PostToolUse, TurnEnd, SessionEnd}` (`crates/core/src/user_hook_types.rs:25-32`); only `UserPromptSubmit` and `PreToolUse` `can_block` (`crates/core/src/user_hook_types.rs:40-43`). `SessionLifecycleHook` is "Advisory only - the runtime calls `fire` and logs any failure; it never blocks the session." (`crates/core/src/lifecycle_hooks.rs:73-84`). `TurnLifecycleHook` for `user_prompt_submit` "can *block* (reject the inbound message and abort the turn) and *mutate* (rewrite the user message text)" (`crates/core/src/lifecycle_hooks.rs:8-10`).

(c) Lifecycle: specs are collected at capability collection and adapted centrally: "Contributors return *data only* - the executor is constructed centrally by the core so global timeout/output/sandbox limits cannot be bypassed." (`crates/core/src/capabilities/mod.rs:894-896`). `SessionHookContext { session_id, org_id, agent_id }` is "Lighter than `ToolContext`: at session create/close there is no tool, no turn, and no per-tool stores" (`crates/core/src/lifecycle_hooks.rs:32-40`).

(d) Host services: a `BashHookExecutor` over the `bashkit_shell` sandbox (`crates/core/src/lifecycle_hooks.rs:14-17`; `crates/platform/src/capabilities/user_hooks.rs:63-68`).

(e) Evidence: the `user_hooks` capability "has no tools and no system prompt. Its single job is to surface `UserHookSpec` entries from its config ... and to carry the `disabled_contributions` list that mutes capability-bundled hooks." (`crates/platform/src/capabilities/user_hooks.rs:4-7`). Risk is High because "accepting arbitrary commands from config is a code-execution surface" (`crates/platform/src/capabilities/user_hooks.rs:9-12`). The Framework's typed hooks are a private capability with a reserved id: `LIFECYCLE_HOOK_CAPABILITY_ID = "__everruns_framework_lifecycle_hooks"` (`crates/everruns/src/hooks.rs:27`), `HookPoint::{AgentStart, TurnStart, ToolStart, ToolEnd, Completion}` (`crates/everruns/src/hooks.rs:74-87`), "The contract is intentionally non-mutating: hooks cannot rewrite prompts, tool arguments, tool results, or turn outcomes." (`crates/everruns/src/hooks.rs:9-10`). The builder injects this capability into the agent's ref list at runtime build (`crates/everruns/src/agent.rs:614-623`).

(f) Placement: `user_hooks()` is a trait method any capability may implement to ship "reusable hook bundles (formatters, security guards, audit commands)" (`crates/core/src/capabilities/mod.rs:889-891`); the `user_hooks` capability itself is hosted. The Framework hooks are an internal capability the application never sees.

### 8. LLM error hook (terminal-error recovery, continuation scheduling)

(a) A capability reacts to a turn that failed with a non-retryable provider error, performing a side effect and augmenting the user-facing error.

(b) Contribution kind: hook (error interceptor) plus scheduling side effect. `LlmErrorHook::on_llm_error(&LlmErrorContext) -> LlmErrorHookOutcome` (`crates/core/src/llm_error_hook.rs:70-76`); context carries `session_id, error_code, error_fields, config, services` (`crates/core/src/llm_error_hook.rs:35-47`).

(c) Lifecycle: per terminal error; "Runs only on the terminal (non-retried) error path, before the user-facing error message is emitted." (`crates/core/src/llm_error_hook.rs:71-72`).

(d) Host services: `LlmErrorHookServices { schedule_store: Option<Arc<dyn SessionScheduleStore>> }`, "each field is optional so a hook degrades to a no-op when its service is absent" (`crates/core/src/llm_error_hook.rs:26-32`).

(e) Evidence: `usage_limit_auto_continue` "schedules a one-shot session continuation at `resets_at + delay_seconds` that re-injects `prompt` to resume the interrupted work, and returns an `auto_continue` error field so the user-facing copy promises automatic resumption" (`crates/builtins/src/usage_limit_auto_continue.rs:12-16`); "the capability contributes no tools and no reason-atom special-casing" (`crates/builtins/src/usage_limit_auto_continue.rs:9-10`). It is excluded from the runtime bundle because its "error hook needs a schedule store and poller that the default embedded host does not supply" (`crates/builtins/src/lib.rs:214-215`).

(f) Placement: trait method `llm_error_hook()`; the builtin is portable code but registered only where a schedule store exists.

### 9. Scoped remote MCP servers

(a) A capability contributes MCP server connection configs that are merged into the session's scoped MCP set; separately, each registered MCP server is itself exposed as a virtual capability.

(b) Contribution kind: transport / server registration. `mcp_servers() -> ScopedMcpServers`: "These are merged into harness/agent/session scoped MCP config at runtime. Explicit scoped MCP config overrides capability-contributed defaults by logical server name." (`crates/core/src/capabilities/mod.rs:607-614`). `ScopedMcpServer { transport_type, url, headers, command, args, env, auth mode ... }` "intentionally mirrors the `mcpServers` object shape used by common MCP client config files" (`crates/core/src/mcp_server.rs:329-361`).

(c) Lifecycle: merged per collection (`crates/core/src/capabilities/mod.rs:2476-2478`, `2440`); MCP tool lists are "cached and refreshed periodically" with a "24h TTL" (`crates/mcp/src/capability.rs:13`; `knowledge/execution/capabilities.md:1048`).

(d) Host services: network (HTTP JSON-RPC) and an `McpToolInvoker` (`crates/core/src/tool_context.rs:89, 154`); OAuth secrets under `mcp_oauth:` in the session secret store (`crates/host/src/session_services/capabilities/session_storage.rs:32`).

(e) Evidence: "Each active MCP server becomes a virtual capability that contributes its tools to the agent's tool set." with "Capability ID format: `mcp:{server_id}`" (`crates/mcp/src/capability.rs:6-10`). Declarative capabilities carry `mcp_servers: Option<ScopedMcpServers>` (`crates/core/src/capabilities/declarative.rs:47-48`). Elicitation exists as a module (`crates/mcp/src/elicitation.rs`, `crates/worker/src/mcp_elicitation_consent.rs`). MCP resources, prompts, or sampling exposed as capability contributions: not in the sources.

(f) Placement: `mcp_servers()` is a trait method; `McpCapability` is a virtual capability constructed at runtime from server records in `everruns-mcp`.

### 10. Provider request shaping: tool search, prompt cache, driver options, parallel calls, model-adaptive dispatch

(a) A capability changes how the provider request is built rather than what tools exist.

(b) Contribution kind: request policy. `tool_search_config()` is "Provider-facing deferred tool-loading configuration ... The execution engine consumes this generically and does not match on implementation-owned capability IDs." (`crates/core/src/capabilities/mod.rs:675-683`). `prompt_cache_config()` (`686-692`). `driver_options()` returns "Driver-namespaced opaque per-call options (`"<driver-id>/<option>"`) ... Each entry's shape is owned by the driver crate named in the key; core transports the values untouched." (`694-699`). `parallel_tool_calls_preference()` (`701-705`). `error_disclosure()` (`707-713`). `native_async_tools()` (`289-296`). `resolve_for_model()` is "Model-adaptive dispatch: delegate this capability's contributions to a different underlying capability based on the agent's model." (`389-401`).

(c) Lifecycle: folded into `RuntimeAgent { tool_search, prompt_cache, driver_options, parallel_tool_calls, ... }` at apply time (`crates/core/src/capabilities/mod.rs:2790-2809`); "First contributor wins per key" for driver options (`1456-1458`).

(d) Host services: the provider driver; `SystemPromptContext.model` for dispatch (`crates/core/src/capabilities/mod.rs:135-140`).

(e) Evidence: `auto_tool_search` "picks hosted vs client-side tool search" (`crates/core/src/capabilities/mod.rs:2505`); the `openrouter_server_tools` capability contributes "provider-executed server tools" via driver options (`1456-1457`). `ToolDefinitionHook::applies_with_native_tool_search` exists because client-side deferral and hosted tool search "are mutually exclusive" (`1061-1067`).

(f) Placement: trait methods; `openai_tool_search`, `claude_tool_search`, `tool_search`, `auto_tool_search`, `prompt_caching`, `parallel_tool_calls`, `native_async_tools`, `error_disclosure` are portable builtins (`crates/builtins/src/lib.rs:294-301`).

### 11. User-invocable slash commands (bypassing the model)

(a) A capability contributes `/commands` a human runs directly; they execute in the capability, not through a model tool call.

(b) Contribution kind: command surface. `commands() -> Vec<CommandDescriptor>`: "System commands are user-invocable /slash commands that execute directly without involving the LLM. They are surfaced in the UI command palette alongside invocable skills." (`crates/core/src/capabilities/mod.rs:926-935`). `execute_command(request, ctx)` must be overridden by any capability that declares commands; the default errors (`crates/core/src/capabilities/mod.rs:937-960`).

(c) Lifecycle: per invocation; "Commands that need the session's assembled context or an out-of-band LLM call (e.g. `/btw`) use the host facilities on `CommandExecutionContext::host`" (`crates/core/src/capabilities/mod.rs:946-949`).

(d) Host services: `CommandHost` (turn context, session completion) (`crates/builtins/src/btw.rs:5-8, 99`).

(e) Evidence: `/btw` "reuses the session's merged context, disables tools, and persists nothing, behaving like Claude Code's ephemeral overlay answer" (`crates/builtins/src/btw.rs:9-10`); its `CommandDescriptor { name: "btw", source: CommandSource::System, args: [question] }` (`crates/builtins/src/btw.rs:64-78`). Skills can also be `user_invocable` (`crates/core/src/capabilities/skill_contribution.rs:89-90`).

(f) Placement: trait methods; `btw` and `system_commands` are portable builtins.

### 12. Sub-agent spawning: delegation targets and agent blueprints

(a) A capability contributes a target for the shared `spawn_agent` router, or a pre-built child agent definition whose tools never appear in the parent.

(b) Contribution kind: delegation provider / child-agent template. `delegation_target_with_config() -> Option<DelegationTargetProvider { target_type, tool }>`: "Hosted delegation implementations use this seam so core can assemble a single model-facing tool without knowing capability IDs or product configuration." (`crates/core/src/capabilities/mod.rs:472-482, 1529-1532`). `agent_blueprints() -> Vec<AgentBlueprint>`: "Blueprints are pre-built agent definitions with private tools, baked-in prompts, and fixed/default models ... Blueprint tools never appear in the host agent's tool list." (`crates/core/src/capabilities/mod.rs:962-971`). `AgentBlueprint { id, name, description, model: BlueprintModel::{Fixed, Default, Inherit}, system_prompt, tools, max_turns, config_schema }` (`crates/core/src/capabilities/mod.rs:1129-1163`).

(c) Lifecycle: delegation targets are collected per turn (`crates/core/src/capabilities/mod.rs:2519-2520, 2562-2564`) and merged under `SPAWN_AGENT_CONCURRENCY_CLASS = "spawn_agent"` so "collection keeps the merged tool serialized through this neutral key" (`crates/core/src/capabilities/mod.rs:100-104`). Spawned children are tracked as session tasks: "Background mode (default): returns immediately with a task_id; a detached watcher ... heartbeats the task registry, and settles the task on the child's terminal turn status." (`crates/platform/src/capabilities/subagents.rs:10-15`).

(d) Host services: `SubagentSessionDelegate`, `SessionCreationAuthority`, `SubagentSpawnStore`, `SessionTaskRegistry` (`crates/core/src/tool_context.rs:96-108`).

(e) Evidence: `subagents` is `RiskLevel::High` because "Subagent recursion controls bound org cost/DoS exposure" (`crates/platform/src/capabilities/subagents.rs:91-95`), with config bounds `max_subagent_depth`, `max_active_descendant_tasks`, `max_total_descendant_tasks` (`crates/platform/src/capabilities/subagents.rs:106-138`). `agent_handoff` "is a high-risk orchestration capability for delegating from one configured Agent to another configured Agent through an allowlist and connection gate" (`knowledge/execution/capabilities.md:92-95`). `a2a_agent_delegation` id is defined ungated in core (`crates/core/src/capabilities/mod.rs:92-95`).

(f) Placement: seams in core; implementations `subagents`, `agent_handoff`, `a2a_delegation`, `background_execution` are hosted in `everruns-platform`.

### 13. Scheduling, timers, and durable continuation

(a) A capability lets the run schedule future work (one-shot or cron) that re-enters the session later, backed by a durable scheduler.

(b) Contribution kind: timer / schedule registration through a host store. `SessionScheduleStore::create_schedule(session_id, description, cron_expression, scheduled_at, timezone)` with `create_schedule_enforcing_limits` (`crates/core/src/session_services.rs:71-138`). The durable engine underneath is "A PostgreSQL-backed workflow orchestration engine" with "Event-sourced workflows: All state changes are persisted as events, enabling replay and recovery" (`crates/durable/src/lib.rs:3-7`) exposing `DurableScheduler`, `WorkerPool`, `WorkflowExecutor` (`crates/durable/src/lib.rs:88-101`).

(c) Lifecycle: schedules outlive the turn; "When a schedule fires, you will receive a message with the task description and should execute it. Maximum 5 active schedules per session." (`crates/platform/src/capabilities/session_schedule.rs:53-57`). Continuations from candidate 8 use the same store.

(d) Host services: `ScheduleStore` (`crates/core/src/tool_context.rs:95`), clock, database, and a poller (`crates/builtins/src/lib.rs:214-215`).

(e) Evidence: `session_schedule` "Provides tools for scheduling future work within a session: - `create_schedule`: Schedule a task (one-shot or recurring cron)" (`crates/platform/src/capabilities/session_schedule.rs:1-6`) and contributes feature `"schedules"` (`67-69`). Store-level limits: per-session `MAX_ACTIVE_SCHEDULES_PER_SESSION`, per-org `DEFAULT_MAX_SCHEDULES_PER_ORG`, and `validate_cron_min_interval` (`crates/core/src/session_services.rs:98-126`).

(f) Placement: the tools are a hosted capability; the store trait is a neutral core contract; the scheduler and workflow engine are infrastructure in `everruns-durable`, not a capability. Checkpointing and replay for the agent loop itself are engine and host concerns (`crates/core/src/execution_snapshot.rs`, `crates/core/src/compaction_checkpoint.rs`, `crates/host/src/execution_snapshot.rs`), not capability contributions.

### 14. Session-scoped stores: KV and secrets, SQL, memory mounts, knowledge retrieval, task registry, budget

(a) A capability grants the run access to a session- or org-scoped store, declared as a host service the tools require and surfaced as a UI feature string.

(b) Contribution kind: store handle plus feature flag. The runtime enumerates the services a host may expose: `ToolContextService::{SessionFileSystem, SessionStorageStore, ImageArtifactStore, ProviderCredentialStore, UtilityLlmService, McpInvoker, EgressService, MessageRetriever, SessionStore, AgentStore, ConnectionResolver, ScheduleStore, SubagentSessionDelegate, LeasedResourceStore, SessionResourceRegistry, SessionTaskRegistry, EventEmitter, CapabilityRegistry, ToolRegistry, OrgId, BudgetChecker, PaymentAuthority, SessionCreationAuthority, SubagentSpawnStore, ReasoningEffortHandle}` (`crates/core/src/tool_context.rs:83-109`). "Tools declare the subset they require through `Tool::required_context_services`. Runtime hosts validate those declarations before advertising tools to the model." (`crates/core/src/tool_context.rs:79-81`). `features()` returns "open-ended strings indicating what user-facing functionality this capability enables ... Known features: `"file_system"`, `"schedules"`, `"secrets"`, `"key_value"`, `"sql_database"`, `"leased_resources"`." (`crates/core/src/capabilities/mod.rs:563-579`).

(c) Lifecycle: per session; `SessionStorageStore` is "Storage for session-scoped key/value pairs and secrets" where "Secret storage is for sensitive data that is encrypted at rest" (`crates/core/src/session_services.rs:32-37`). Reserved KV prefixes stop tools forging internal state: `AGENT_RUN_KEY_PREFIX`, ARD attachment prefixes, `THREAD_CONTEXT_KV_KEY` (`crates/host/src/session_services/capabilities/session_storage.rs:17-31`).

(d) Host services: database, encryption key (`SECRETS_ENCRYPTION_KEY`, `knowledge/execution/capabilities.md:795`), vector store and embeddings for `knowledge_index` (`crates/platform/src/capabilities/knowledge_index.rs:20-21`).

(e) Evidence: `session_storage` contributes features `["secrets", "key_value"]` (`crates/host/src/session_services/capabilities/session_storage.rs:116-119`). `knowledge_index` "Binds an agent or harness to one or more org-scoped Knowledge Indexes - source-backed, embedded collections searched semantically with citations." (`crates/platform/src/capabilities/knowledge_index.rs:3-4`). `session_tasks` tools "declare `SessionTaskRegistry` as a hard context-service requirement, so production runtime assembly rejects the capability before model exposure when the host lacks that backend" (`crates/platform/src/capabilities/session_tasks.rs:9-11`). `budgeting` adds "System prompt section informing the agent about budget constraints" and "A check_budget tool" (`crates/builtins/src/budgeting.rs:3-5`); budget enforcement itself is `BudgetChecker` / `PaymentAuthority` in the tool context (`crates/core/src/tool_context.rs:104-105`).

(f) Placement: `session_storage` and `session` live in `everruns-host` (`crates/host/src/session_services/capabilities/`); `session_sql_database`, `memory`, `knowledge_index`, `knowledge_base`, `session_tasks` are hosted in `everruns-platform`; `budgeting` and `self_budget` are portable builtins. Store traits are neutral core contracts.

### 15. Sandboxes and execution environments

(a) A capability provisions an isolated execution environment (WASM-like shell, managed remote sandbox, Docker container) whose lifecycle is tied to the session.

(b) Contribution kind: environment / leased resource. `session_sandbox`: "One managed sandbox per session. The concrete provider is chosen by config (`provider: "daytona"` initially), while the tool surface stays stable." (`crates/platform/src/capabilities/session_sandbox.rs:1-4`). `container_sandbox`: "One sandbox per session (container name derived from session ID)" (`crates/platform/src/container_sandbox/mod.rs:10-11`). `bashkit_shell` provides "WASM-like execution isolation (no system access)" over the session filesystem (`knowledge/execution/capabilities.md:745-749`).

(c) Lifecycle: per session with provider-managed pause/resume/checkpoint: config exposes `auto_start` ("Start the sandbox proactively when the session is created") and `idle_pause_after_seconds` (`crates/platform/src/capabilities/session_sandbox.rs:91-104`); imports include `checkpoint_session_sandbox`, `pause_session_sandbox`, `delete_session_sandbox` (`crates/platform/src/capabilities/session_sandbox.rs:7-11`). Docker containers are "Lazily started on first use, persists for session" (`knowledge/execution/capabilities.md:1349`). Sandbox state rides in the reserved secret name `session_sandbox` (`crates/host/src/session_services/capabilities/session_storage.rs:33-38`).

(d) Host services: `session_storage` (declared dependency, `crates/platform/src/capabilities/session_sandbox.rs:69-71`), network to the provider, Docker Engine REST API for `container_sandbox` ("no `docker` CLI binary dependency", `crates/platform/src/container_sandbox/mod.rs:5-8`), `LeasedResourceStore` (`crates/core/src/tool_context.rs:97`).

(e) Evidence: `container_sandbox` self-registers via `inventory::submit! { IntegrationPlugin { experimental_only: false, feature_flag: Some("container_sandbox"), factory: || Box::new(ContainerSandboxCapability) } }` (`crates/platform/src/container_sandbox/mod.rs:34-40`). Two filesystem realities are reconciled by path translation, not by conflict declaration: "Bash operates with `/workspace` as the root. The adapter translates paths ... This ensures bash and FileSystem capability share the same file namespace." (`knowledge/execution/capabilities.md:760-765`). Missing gated sandboxes fail session creation rather than degrade: "Session creation therefore rejects requests whose effective capability set ... names a **built-in** capability that is not available in this deployment, rather than silently dropping its tools and degrading into a different execution environment" (`knowledge/execution/capabilities.md:284-288`).

(f) Placement: `bashkit_shell` is an integration crate; `session_sandbox` and `container_sandbox` are hosted in `everruns-platform`; `docker_container`, `daytona`, `e2b` are integration plugins registered by inventory under grade and flag policy.

## Everruns design lessons

The relationship between a capability and its tools in everruns is that tools are one of many typed return values, and not a privileged one. The trait has one method group for tools (`tools`, `tools_with_config`, `tool_definitions`) and roughly a dozen others that return hooks, providers, mounts, specs, configs, commands, or blueprints. Nothing in the collection loop treats the tool list as the primary product; `CollectedCapabilities` is a flat record of eighteen independently typed fields (`crates/core/src/capabilities/mod.rs:1428-1475`), and `apply_capabilities` scatters them into a `RuntimeAgent` and a `ToolRegistry` (`crates/core/src/capabilities/mod.rs:2760-2816`). Several shipped capabilities contribute no tools at all: `user_hooks`, `guardrails` with checks, `prompt_canary_guardrail`, `loop_detection`, `progress_guard`, `message_metadata`, `openui`, `a2ui`, `usage_limit_auto_continue`, `channel_context`, `memory`. The implication for PromptForge is that `Contribution` should become a record of independent optional surfaces, each with its own merge rule, rather than a tools vector with extras bolted on.

Every non-tool contribution in everruns is a typed trait object with a narrow, documented invocation point, and the runtime invokes it "generically" without matching on capability ids. The phrase recurs in the sources: the reason atom "knows nothing about any specific capability's behavior" for error hooks (`crates/core/src/capabilities/mod.rs:666-668`); compaction policy is invoked "without matching on a capability ID" (`crates/core/src/capabilities/mod.rs:722-724`); tool search config is consumed generically so the engine "does not match on implementation-owned capability IDs" (`crates/core/src/capabilities/mod.rs:676-677`); `message_filter_config` takes a `compaction_enabled` flag so a filter can coordinate "without core matching on either capability's ID" (`crates/core/src/capabilities/mod.rs:639-640`). The design rule is: when a new behavior needs the engine to know about a capability, add a seam to the trait and a slot in the collected record, never a branch on the id. This is also why `auto_activates_for(&[ToolDefinition])` exists as a generic hook "without teaching core their IDs or deployment ownership" (`crates/core/src/capabilities/mod.rs:484-489`).

The runtime separates cache-stable from volatile and trusted from untrusted at the contribution-kind level, not by convention. There are three distinct prompt sinks: the cached system prefix (`system_prompt_contribution`), the per-turn leading user message for untrusted content (`conversation_context_contribution`), and the trailing `<facts>` block for volatile values (`Volatility::Dynamic`). A capability does not choose a position; it chooses a kind, and the kind carries the placement policy and the trust boundary. PromptForge's deferred "prompt fragments" should probably be at least two kinds from the start, since everruns' own history shows `AGENTS.md` moving from system prompt to conversation context for instruction-hierarchy reasons (`crates/builtins/src/agent_instructions.rs:12-15`).

Hooks are data where they cross a trust boundary and code where they do not. Capability-authored in-process hooks (`PreToolUseHook`, `OutputGuardrail`, `LlmErrorHook`) are `Arc<dyn Trait>` and run with host services. User-authored hooks are `UserHookSpec` JSON validated and adapted centrally so "global timeout/output/sandbox limits cannot be bypassed" (`crates/core/src/capabilities/mod.rs:894-896`). The Framework's application closures are bridged into a private capability under the reserved `__everruns_` namespace (`crates/everruns/src/hooks.rs:27`) so the same collection path handles them. For PromptForge this suggests a `Contribution` can carry both `Arc<dyn Hook>` for host-installed code and a serializable spec form for anything sourced from prompt frontmatter or user config.

Capabilities are process-global singletons; everything per-run flows through the returned values or host stores. The trait is `&self` throughout, the registry holds `Arc<dyn Capability>`, and the doc says plainly that "the capability is a process-global singleton shared across sessions" (`crates/core/src/capabilities/mod.rs:825-826`). Per-session state is either captured into a returned hook via `SystemPromptContext.session_id` (`tool_definition_hooks_with_context`), kept in a host store keyed by session (`SessionStorageStore`, `VirtualMountRegistry`), or created per stream (`OutputGuardrail::arm` returns a fresh run). PromptForge's `create(&RunServices) -> Contribution` is already per-run, which is a simpler model, but the everruns split is a warning about teardown: everruns has no `Capability::deactivate`, and the knowledge spec notes "Unregistering is deliberately absent: removal raises lifetime questions - in-flight tool calls, spawned processes - that the motivating case does not need." (`knowledge/execution/capabilities.md:253-255`). Sandboxes and schedules that outlive a turn are managed by host stores and leased-resource cleanup, not by the capability.

Composition constraints are expressed as dependencies and host-service requirements, not conflicts. `dependencies()` pulls in transitive capabilities topologically (`crates/core/src/capabilities/mod.rs:551-561`); tools declare `required_context_services` and hosts refuse to advertise tools whose services are absent (`crates/core/src/tool_context.rs:79-81`); `features()` aggregates UI flags; `risk_level()` gates assignment. The knowledge spec records the deliberate gap: "Can capabilities conflict? Currently no conflict resolution; later capabilities add to earlier ones" (`knowledge/execution/capabilities.md:1135`) and lists "Conflict Resolution: Handle tool name conflicts between capabilities" under future extension points (`knowledge/execution/capabilities.md:1460`). PromptForge's `conflicts()` is therefore ahead of everruns on that axis; the everruns lesson is that `dependencies()` and a declared list of required host services are the complementary constraints worth adding beside it.

## Gaps

Things looked for and not found in the sources:

- Co-activation conflict declarations. No `conflicts` method or equivalent anywhere in `crates/core/src/capabilities/` (grep for "conflict" returns nothing); the spec explicitly says there is no conflict resolution (`knowledge/execution/capabilities.md:1135`). The bashkit vs filesystem case is solved by path translation onto one shared namespace, not by exclusion.
- A per-run capability instance or teardown hook. There is no `activate`/`deactivate`/`on_session_end` on `Capability`; session-end behavior exists only as user-hook `SessionEnd` events (`crates/core/src/user_hook_types.rs:31`) and host-side leased-resource cleanup (`crates/worker/src/leased_resource_cleanup.rs`).
- MCP resources, prompts, or sampling as capability contributions. `McpCapability` maps tools only (`crates/mcp/src/capability.rs:47-50`). Elicitation exists as a module but its capability-level surface was not traced.
- Model routing or provider selection as a capability contribution. `ModelRouter`, `ModelRouterStrategy`, `ModelRouterRoute` are standalone resources in `crates/core/src/model_router.rs:58-166`, and `everruns-model-profiles` is a static metadata registry (`crates/model-profiles/src/lib.rs:4-8`). The only capability-level model hook is `resolve_for_model`, which swaps implementations based on the model rather than choosing the model.
- Channels and transports (Slack, webhooks, A2A channel, voice) as capabilities. They are apps and channels on the platform side (`README.md:98-101`; `crates/core/src/channel.rs`); the only capability touching a channel is `channel_context`, which reads channel state already persisted by the webhook.
- Secrets or credential brokering as a contribution. Secrets flow through `SessionStorageStore` secrets and `ProviderCredentialStore` (`crates/core/src/tool_context.rs:150-152`), and the `CapabilityRef` doc says config "is not a secret store" (`crates/capability/src/reference.rs:29-31`). No capability contributes a credential resolver.
- Durable execution, checkpointing, or replay as a capability. These are engine and host concerns (`crates/durable/`, `crates/core/src/execution_snapshot.rs`, `crates/core/src/compaction_checkpoint.rs`); capabilities only reach durability indirectly via schedules and the error hook.
- Lua surface as a contribution kind. `lua` and `lua_code_mode` are experimental capabilities that expose a tool and a `ToolDefinitionHook` (`knowledge/execution/capabilities.md:1330-1340`); there is no trait method for contributing Lua bindings.
- A `crates/drivers/src` module: `crates/drivers/` is a directory of independent driver crates with a README, not a crate (`crates/drivers/README.md:3-4`).
- A `CLAUDE.md` with content: it contains only `@AGENTS.md` (`CLAUDE.md:1`).

*2026-09-19 09:50 - claude-fable-5.1*




