---
produced: 2026-09-19
title: promptforge and bashkit capability survey - non-tool contribution kinds the design already anticipates (mounts, prompt fragments, Lua surface, input broker, observers, store, guards)
---

# PromptForge and bashkit capability survey

Scope: what the PromptForge design already names or implies as a run-scoped contribution a `Capability` could own that is not a tool pack, and what bashkit would contribute if it were a capability. Read-only survey of `promptforge/` and `bashkit/`; every claim cites `path:line`. Where the sources are silent the entry says "not in the sources".

## 1. The current contract

The activation unit is defined in `promptforge/crates/promptforge-api-types/src/capabilities.rs`. The module doc states the shape and the growth intent:

> "A capability is the activation unit: code that runs at run setup and makes services available to the run. Capabilities are delivered in packs (crates now, DLLs via adapters later) and identified by a 2-segment [`GlobalName`] ... At prepare time the executor activates each declared capability by calling [`Capability::create`] with the run's [`RunServices`]; the returned [`Contribution`] is v1 tools-only and grows without redesign." (`promptforge/crates/promptforge-api-types/src/capabilities.rs:3-11`)

The trait:

> "pub trait Capability: Send + Sync {
>     fn id(&self) -> &CapabilityId;
>     fn description(&self) -> &str;
>     fn conflicts(&self) -> &[CapabilityId] { &[] }
>     fn create(&self, services: &RunServices) -> Result<Contribution, CapabilityError>;
> }" (`promptforge/crates/promptforge-api-types/src/capabilities.rs:285-315`, method bodies and doc comments elided)

The `conflicts` doc is the only place in the code that names the bashkit/terminal pair:

> "Co-activation rules attach at the capability level: bashkit and a terminal are two filesystem realities, and a context gets one or the other, never both. The default is no conflicts. Prepare checks the declared present capabilities pairwise - the check is symmetric, so only one member of a pair needs to name the other - and fails preparation naming both members of a conflicting pair." (`promptforge/crates/promptforge-api-types/src/capabilities.rs:295-300`)

`RunServices` is already declared open for exactly the non-tool bridges this survey is about:

> "What a capability is given at activation. Non-exhaustive so new fields (the input broker, the observer, the model client) can be added when a bridge capability needs them without breaking existing capability implementations. Host-supplied per-capability config arrives here, never via the prompt." (`promptforge/crates/promptforge-api-types/src/capabilities.rs:317-322`)

> "pub struct RunServices { pub vfs: VfsRef, pub cancel: CancelHandle, }" (`promptforge/crates/promptforge-api-types/src/capabilities.rs:325-330`)

`Contribution` names three deferred kinds by name:

> "What a capability contributes to a run. v1 is tools-only: mounts, prompt fragments, and Lua surface are deferred until the capabilities that need them land. The struct is [`Default`] and grows without redesign." (`promptforge/crates/promptforge-api-types/src/capabilities.rs:350-354`)

> "pub struct Contribution { pub tools: Vec<Arc<dyn Tool>>, }" (`promptforge/crates/promptforge-api-types/src/capabilities.rs:365-369`)

The registry is explicit and host-built; linking registers nothing (`promptforge/crates/promptforge-api-runtime/src/capabilities.rs:3-6`), duplicates and punctuation twins are rejected (`:6-10`), and the first-party `Web` capability is re-exported through the facade "so hosts never name the internal pack crate (the one-door rule)" (`:66-68`).

The activation loop in `promptforge/crates/promptforge-api-runtime/src/execute/environment.rs` runs inside `Environment::prepare`. The per-run VFS is built first, and its doc explains why it is a fresh router and not an overlay:

> "The per-run VFS is a fresh router mounting the environment's [`base_vfs`] at `/` plus a fresh memory backend at the store mount - never an overlay: an overlay shares the base's claims table, which is only correct for two views of the same storage, and concurrent runs' stores are different storage." (`environment.rs:103-108`)

> "ctx.vfs = VfsRef::builder().mount("/", self.base_vfs.clone()).mount(promptforge_vfs::STORE_MOUNT, shared_vfs::MemoryBackend::new()).build();
> let services = RunServices::new(ctx.vfs.clone(), ctx.cancel.clone().unwrap_or_default());" (`environment.rs:152-159`, reflowed)

Resolution against the registry preserves declaration order; a missing required capability lands in `Requirements::missing_required`, an absent optional is skipped with a log line (`environment.rs:163-181`). The conflict check is pairwise and symmetric, and a conflicting pair activates neither member (`environment.rs:182-203`):

> "if first.conflicts().contains(second_id) || second.conflicts().contains(first_id) { tracing::warn!(... "conflicting capabilities declared; neither activates"); requirements.conflicts.push(CapabilityConflict { first: first_id.clone(), second: second_id.clone() }); conflicted[i] = true; conflicted[j] = true; }" (`environment.rs:189-201`, reflowed)

Activation itself:

> "match capability.create(&services) { Ok(contribution) => { tracing::info!(capability = %id, "capability activated"); activated.push((id.clone(), contribution)); } Err(error) => { tracing::warn!(... "capability activation failed; it contributes nothing to the run"); if !*optional { requirements.missing_required.push(id.clone()); } } }" (`environment.rs:211-230`, reflowed)

> "ctx.tools = assemble_catalog(&activated); ... ctx.tool_bindings = fill_tool_bindings(prompt, &ctx.tools, &activated_ids, &mut requirements); ctx.model_bindings = fill_model_bindings(prompt, ctx.model.as_ref(), &mut requirements);" (`environment.rs:232-237`)

The only consumer of a `Contribution` today is `assemble_catalog`, which reads `.tools`. Everything a capability might contribute beyond that has no consumer in `prepare` yet.

The `Environment` doc records what is deployment-constant versus per-run: "built once per host and never rebuilt: everything that can change per run rides the [`RunContext`]. Model-free" (`environment.rs:21-24`). The `base_vfs` field "never carries the store mount (prepare adds a fresh per-run memory backend there)" (`environment.rs:39-41`).

## 2. Contribution kinds the design already names

The dividing rule for what belongs in a capability at all is stated in the capabilities plan:

> "Runtime vs capability dividing line: the criterion is not 'is it language surface' but 'does it reach outside the run.' The store is always present (pure interiority: the run's own scratchpad, defined by the run's determinism contracts; same for `var`, `log`, the models namespace, cancellation). A Lua `fs` table reaches through the VFS to host files, so it is a capability. Never package an interior primitive as a capability; never assume an exterior one." (`promptforge/vibe/2026-09-13-1-capabilities-global-naming.md:56`)

So the kinds below split into two groups: things the design says a capability should contribute (mounts, prompt fragments, Lua surface, bridges to host services) and things the design says are interior and must stay runtime-owned (store, `var`, `log`, models namespace, cancellation, guards, compaction). The second group is recorded because it bounds the first.

### 2.1 Mounts (deferred, mechanics already designed)

What it is: a capability adds a backend at a prefix of the run's VFS router, so Lua `store.*` or a future `fs` table, and tools, see capability-owned storage at a path.

Where it lives today: mounting is a `VfsRefBuilder` operation in `shared-vfs` (`promptforge/crates/shared-vfs/src/router.rs:359-370`: "pub fn mount(mut self, prefix: &str, backend: impl Vfs + 'static) -> VfsRefBuilder", panicking on a non-absolute prefix or a duplicate). `VfsRef::builder()` builds an immutable mount table (`promptforge/crates/shared-vfs/src/handle.rs:204-209`), and an overlay method returns "a handle with `backend` mounted at `prefix` over this handle's namespace. The claims table is shared" (`handle.rs:211-213`). Only `Environment::prepare` mounts anything today: the base at `/` and a fresh `MemoryBackend` at `STORE_MOUNT` (`environment.rs:152-158`). `STORE_MOUNT` is `"/_promptforge/store"` (`promptforge/crates/promptforge/vfs/src/lib.rs:15`).

What would change: `Contribution` gains a mounts field and `prepare` overlays them after `create`. The plan already fixes the mechanics and the claims reasoning:

> "When mounts land, the mechanics will be: a capability sees the base router during `create` and requests mounts; those mounts are then overlaid onto the run's router afterward. An overlay shares the run's claims table, which is correct here because capability storage is run-scoped - same run, same storage. Only the per-run store needed a fresh claims table, because two concurrent runs' stores are different storage." (`promptforge/vibe/2026-09-13-1-capabilities-global-naming.md:192`)

The `RunContext.vfs` sketch in the same plan says the router "mounts env.base_vfs (shared storage, base claims catch cross-run host-file conflicts) + fresh memory backend at the store mount (per-run storage, per-run claims). NOT an overlay" (`2026-09-13-1-capabilities-global-naming.md:366-373`). `shared-vfs` is "the permanent bottom of the dependency stack: std only ... no promptforge policy" (`promptforge/crates/shared-vfs/src/lib.rs:5-7`), so a mount contribution is a pure `shared-vfs` value with no policy attached; the policy gate is `promptforge-vfs` (`promptforge/vibe/archdoc.md:15`).

The capabilities plan lists the motivating capabilities as "capabilities that create things (fs, bashkit) are self-contained" (`2026-09-13-1-capabilities-global-naming.md:193`) and the decision record says a capability "makes services available (tools, mounts, prompt fragments, clients)" (`:570`).

### 2.2 Prompt fragments (deferred, trust already decided)

What it is: text a capability injects into the model-facing context, the canonical example being AGENTS.md injection.

Where it lives today: nowhere in code. The plan names it as a designed-and-deferred contribution: "v1 contributes tools - mounts, prompt fragments like AGENTS.md injection, and Lua surface are designed and deferred" (`2026-09-13-1-capabilities-global-naming.md:47`; repeated at `:78`). The origin is the Everruns survey: "its harness features - tools, shells, AGENTS.md injection - live in a composable capability layer below the UI, never in it" (`:42`).

What would change: `Contribution` gains a fragments field, and the fragments flow through the existing untrusted guard. The plan's security requirement is already fixed:

> "Prompt fragments carry `OutputTrust`; AGENTS.md content arrives `Untrusted` and flows through the existing guard-wrap machinery." (`2026-09-13-1-capabilities-global-naming.md:162`)

`OutputTrust` is the tools vocabulary type (`promptforge/crates/promptforge-api-types/src/tools.rs:10,20`), and the guard-wrap is `GuardNonce::wrap`: "Tool results from untrusted sources and stored content bound for a model are wrapped in an XML-style envelope whose tag name includes a random nonce ... One nonce is minted per run" (`promptforge/crates/promptforge-api-types/src/untrusted.rs:3-7`). Where in the context a fragment lands (system message, pinned user context) is not in the sources; the field comparison's Finding 5 says Goose "rebuilds persistent and ephemeral system contributions in stable keyed order before inference" (`promptforge/vibe/agent-runtime-field-comparison-and-adoption.md:76`), which is the closest prior art the repo records.

### 2.3 Lua surface (deferred; the `fs` table and `user_input()` are the named cases)

What it is: a capability installs a Lua namespace or global in every section VM.

Where it lives today: the Lua host surface is installed by `promptforge/crates/promptforge/lua/`. The namespaces are `models` ("The Lua `models` host table: `use` / `default` / `get` / `infer`", `promptforge/crates/promptforge/lua/src/models/mod.rs:1`), `tools` ("The `tools` namespace: scoping, invocation, and counts", `tools/mod.rs:1`; `add`, `always`, `add_local`, `call`, `allow_tasks`, `calls` at `:6-12`), `store` (`host.rs:228-231`: "an always-on `store` table whose methods (`write`, `append`, `read`, `read_numbered`, `str_replace`, `delete`, `glob`, `exists`) are backed by the [`Store`] facade over the caller's VFS access capability"), plus globals `log` (`host.rs:57-86`), `untrusted` (`host.rs:92-107`), `ui()` (`host.rs:116-134`), `var` (`sys.rs:3-16`), and `compactors` (`compactors.rs:16-18`). None of these is capability-installed; the VM "only calls the installers in setup order" (`tools/mod.rs:14-15`).

What would change: `Contribution` gains a Lua-surface field and the VM setup calls capability installers. The plan names two concrete cases. First, the `fs` table: "A Lua `fs` table reaches through the VFS to host files, so it is a capability" (`2026-09-13-1-capabilities-global-naming.md:56`). Second, `user_input()` moving into a bridge capability:

> "When `user-input` converts: it contributes the model-visible input tool plus the `user_input()` Lua global, both wired to `RunServices.input`; no broker installed degrades to today's unavailable-fallback and is reported as a service gap (a `Requirements` field to add then)." (`2026-09-13-1-capabilities-global-naming.md:193`)

The DLL path is separately deferred: "the declarative Lua-surface bridge (data schema plus generic host bridge over the addon `call` ABI); revisit if a DLL ever needs Lua surface" (`:640`). Any Lua surface a capability adds is bound by A8 and A9 (section 5).

### 2.4 Input broker (a bridge capability consuming a `RunServices` field)

What it is: the host policy behind operator input, today a `RunContext` field, designed to become a `RunServices` field a `user-input` capability consumes.

Where it lives today: `promptforge/crates/promptforge-api-runtime/src/input.rs`. "The broker backs the script-side `user_input()` function only ... No `user_input` tool is advertised to the model" (`input.rs:3-11`). The trait:

> "#[async_trait::async_trait] pub trait InputBroker: Send + Sync { async fn user_input(&self, execution: &str, section: &str) -> Result<InputOutcome, InputError>; }" (`input.rs:128-137`)

Three host policies are the broker's: blocking, unavailable-fallback, failure (`input.rs:13-18`). It rides `RunContext.input: Option<Arc<dyn InputBroker>>` (`promptforge/crates/promptforge-api-runtime/src/execute/config.rs:205`), set by `RunContext::input_broker` (`config.rs:296-305`). In the harness plan the trait moves to `crates/harness/capabilities/` alongside `Capability` and `Tool` (`promptforge/vibe/2026-09-18-4-sans-io-engine-harness.md:165`), which is where it sits now: "the `Capability`, `Tool`, and `InputBroker` traits the first-party capability crates implement" (`promptforge/crates/harness/capabilities/src/lib.rs:1-4`). The same plan then deletes the async trait "at Step 47 once `InputPerformer` replaces its o[nly consumer]" (`2026-09-18-4-sans-io-engine-harness.md:299`), and the engine sees only a `UserInput` effect (`:119`).

What would change: the distinction the plan draws is between self-contained and bridge capabilities:

> "capabilities that create things (fs, bashkit) are self-contained; capabilities that bridge to host services (user-input, later MCP-with-user-servers) consume a `RunServices` field the host fills. Both declare identically in frontmatter; the difference is invisible to the prompt author." (`2026-09-13-1-capabilities-global-naming.md:193`)

The field comparison's Finding 4 is the source of this direction: "Promote Workshop input into a generic elicitation protocol. The field treats human input as a durable host-owned wait usable by deterministic Lua and autonomous model tools" (`agent-runtime-field-comparison-and-adoption.md:13`), and the interactive-webhook plan settled `user_input` as "a Workshop-registered tool, never advertised to models, returning trusted, structured output" (`promptforge/vibe/2026-08/2026-08-31-7-interactive-webhook-tool.md:169`) with the input wait registry as Workshop machinery (`WaitRegistry`, `:359-364`).

### 2.5 Observers, events, and the run log (runtime-owned; the design forbids capability influence)

What it is: the write-only report seam (`Observer`), the event stream that replaces it, and the harness's Turso run log.

Where it lives today: `Observer` in `promptforge/crates/promptforge-api-types/src/observe.rs:441-448`: "Reports one typed [`Observation`] ... Reports must not affect any execution decision. Implementations must return promptly and must not panic." `NullObserver` is the silent default (`observe.rs:614-618`). The section-lifecycle plan fixed the charter: "Observation is synchronous, non-blocking, report-only, and never consulted for a decision. Recording and null observers must produce identical outputs, errors, ordering, and side effects" (`promptforge/vibe/2026-08/2026-08-05-1-section-lua-lifecycle.md:87`). The harness plan replaces the trait with values: "Event: something the engine reports ... Returned as values alongside effects; replaces today's `Observer` callback trait" (`2026-09-18-4-sans-io-engine-harness.md:55`), and the run log is "an append-only Turso record of every run and, per run, every effect, answer, and event in loop order, indexed by task ... nothing reads an answer row back into the engine" (`promptforge/crates/harness/log/README.md:3`).

What would change if a capability contributed it: the design says it should not. `RunServices` may grow "the observer" as a field a capability reads (`capabilities.rs:319-320`), so a capability may be a sink; but the Observer charter and the sans-io plan both forbid a capability from becoming a decision input. The old `EventLog` read side (`2026-08-31-7-interactive-webhook-tool.md:167`: "read-only history backed by the `EventLog` trait, distinct from the Observer") is deleted by the harness plan, "its read-side role passing to the `TaskEvents` effect" (`2026-09-18-4-sans-io-engine-harness.md:220`). A capability-owned observer or log sink is therefore a harness performer concern, not a `Contribution` field. Not in the sources: any plan text proposing a capability-contributed observer.

### 2.6 Store (interior; explicitly not a capability)

What it is: the run-scoped scratchpad at `STORE_MOUNT`, reached from Lua as `store.*`.

Where it lives today: `promptforge/crates/promptforge/vfs/src/lib.rs:12-25` (`STORE_MOUNT`, `empty()`), the Store facade in `crates/promptforge/store/`, Lua install in `host.rs:262-383`, and the leaf-yield path `run_store_op` (`host.rs:398-423`). The harness plan makes store operations an effect: "`Store` (a store operation with the chain's access handle)" (`2026-09-18-4-sans-io-engine-harness.md:119`), with the claims rule "a store operation's access handle is released before the result is delivered" (`:122`).

What would change: nothing. "The store is always present (pure interiority ...). Never package an interior primitive as a capability" (`2026-09-13-1-capabilities-global-naming.md:56`). The section-lifecycle decision "Store is the sole cross-section mutable channel" (`2026-08-05-1-section-lua-lifecycle.md:230`) still stands. The store is recorded here because a mount contribution (2.1) sits beside it in the same router and must not share its fresh claims table.

### 2.7 Timers and clock (engine effects; deferred as Lua surface, not capability territory)

What it is: a `Timer` effect and a deferred `now()`.

Where it lives today: `Timer` is an engine effect in the harness plan: "`Timer` (seconds)" (`2026-09-18-4-sans-io-engine-harness.md:119`), and "the engine has no clock" (`:105`). `now()` is deferred: "a bare global yield shim producing a `Now` effect answered with a `Timestamp`. Revisit: first consumer" (`:339`). The harness performs timers (`:3`: "tokio, the model client, capabilities, input waits, timers").

What would change: not in the sources. Nothing proposes a capability-owned timer; timers are a performer the harness owns, consistent with the engine holding no clock.

### 2.8 Model bindings and the model client (runtime fill; the client is a possible `RunServices` field)

What it is: declared model roles filled at prepare into `ModelBindings`; the gateway client that performs `Chat`.

Where it lives today: `fill_model_bindings` in `prepare` (`environment.rs:237`); `RunContext.model` and `model_bindings` (`config.rs:209-218`); the Lua `models` table selects among pre-filled roles (`models/mod.rs:3-8`). The plan: "Models are declared requirements, host-satisfied ... v1's fill is deliberately trivial - every slot gets the host's current model" (`2026-09-13-1-capabilities-global-naming.md:50`). The Environment is "Model-free: the gateway's model list is a host-UI concern and never crosses this interface" (`environment.rs:23-24`).

What would change: `RunServices` may grow "the model client" (`capabilities.rs:319-320`) so a capability can call a model during activation or from a tool, but the fill itself stays a host function: "Multi-model satisfaction is deferred as a smarter fill function, not a structural change" (`2026-09-13-1-capabilities-global-naming.md:50`). Not in the sources: a capability contributing model descriptors or a fill policy. Model tool dialects are gateway-resolved and never author- or capability-named ("Author prompt never names a dialect", `promptforge/vibe/2026-08/2026-08-08-8-tool-dialect-plugins.md:243`; control plane table at `:95-101`).

### 2.9 Guards and untrusted content (runtime-owned; a consumer of fragments and tool output)

What it is: the per-run `GuardNonce` and the `untrusted(s)` global.

Where it lives today: `promptforge/crates/promptforge-api-types/src/untrusted.rs:51-59` ("Constructed only by [`GuardNonce::fresh`] ... one value is minted at run start and shared by every [`GuardNonce::wrap`] in the run"); Lua global at `host.rs:92-107`. Archdoc A6: "The executor neutralizes chat-template control delimiters in untrusted tool and Lua text, but never rewrites assistant replay or tool-call wire payloads" (`promptforge/vibe/archdoc.md:25`).

What would change: nothing structural; the guard is what a prompt-fragment contribution (2.2) and every untrusted tool output pass through. `OutputTrust` on `ToolOutput` is the vocabulary a capability already uses to mark its outputs (`tools.rs:10,20`). Not in the sources: a capability contributing its own guard or inventory.

### 2.10 Compaction (deferred framework; Lua policy, not a capability)

What it is: the `compactors` global and overflow handling.

Where it lives today: `promptforge/crates/promptforge/lua/src/compactors.rs:1-18`: "`compactors.fail` is the only shipped policy and the omitted-compactor default ... Replacement-returning custom callbacks, budget records, replacement validation, measurable progress, bounded retry, and in-place history replacement belong to the deferred compactor framework." The harness plan defers it again (`2026-09-18-4-sans-io-engine-harness.md:346`).

What would change: not in the sources. The field comparison's Finding 2 prescribes a projection over durable history (`agent-runtime-field-comparison-and-adoption.md:11`), and the webhook plan records the user's preference for a speculative sidecar summarizer (`2026-08-31-7-interactive-webhook-tool.md:584`). Both frame compaction as author or runtime policy, never as a capability.

### 2.11 Discovery and the open toolset (deferred capabilities that contribute a tool but change advertising)

What it is: `promptforge/discovery`, a capability whose tool searches the run's catalog and marks matches advertised; and the host-push offering of capabilities per run.

Where it lives today: deferred. "the discovery capability (`promptforge/discovery`, the picker as an ordinary optional capability) ... it contributes a search tool over the run's catalog; progressive discovery is an advertising problem, not a binding problem - dispatch rejects unadvertised aliases and a search result marks its matches advertised for the rest of the run" (`2026-09-13-1-capabilities-global-naming.md:643`). The motivation names bashkit: "capabilities like bashkit carry 142 commands, and advertising every schema drowns frontier models" (`:579`). The open toolset carries "the host-push `offering: Vec<CapabilityId>` RunContext field" (`:656`).

What would change: this is a tool contribution with a side effect on run state (the advertised set), so it needs the catalog visible at call time: "the tool resolves the catalog lazily at call time (capability `create` order precedes catalog assembly)" (`:643`). It is the one deferred case where a contribution mutates something other than the catalog.

### 2.12 Sub-runs and the prompt-pack (deferred; a capability whose tools are prompts)

What it is: "a capability whose contribution is a directory of prompts, one tool per prompt" (`2026-09-13-1-capabilities-global-naming.md:528`).

What would change: the sub-run adapter needs the parent's Environment and a derived `RunContext` with `CancelHandle::child()` and depth accrual (`:657`); `Environment.max_depth` and `RunContext.depth` exist for it (`environment.rs:42-44`, `config.rs:196-199`). This is still a tools-only contribution, but it is the first that needs `RunServices` to expose the Environment, which the sources do not add.

## 3. Bashkit as a capability

### What bashkit is

Bashkit describes itself as a sandboxed in-process bash interpreter with its own filesystem: "Awesomely fast virtual sandbox with bash and file system. Written in Rust." (`bashkit/README.md:9`). The feature list (`bashkit/README.md:15-29`):

- "Secure by default - No process spawning, no filesystem access, no network access unless explicitly enabled" (`:15`)
- "Sandboxed, in-process execution - All 167 commands reimplemented in Rust, no `fork`/`exec`" (`:17`)
- "Virtual filesystem - InMemoryFs, OverlayFs, MountableFs with optional RealFs backend (`realfs` feature)" (`:18`)
- "Resource limits - Command count, loop iterations, function depth, output size, filesystem size, parser fuel" (`:19`)
- "Network allowlist - HTTP access denied by default, per-domain control" (`:20`)
- "Multi-tenant isolation - Each interpreter instance is fully independent" (`:21`)
- "Custom builtins - Extend with domain-specific commands" (`:22`)
- "LLM tool contract - `BashTool` with discovery metadata, streaming output, and system prompts" (`:23`)
- "Script analysis - Inspect commands, arguments, and file writes before running, to drive permission prompts" (`:24`)
- "Snapshotting - Serialize shell state and VFS contents for checkpoint/resume workflows" (`:25`)
- "Async-first - Built on tokio" (`:27`)

The workspace has nine crates: `bashkit`, `bashkit-bench`, `bashkit-capi`, `bashkit-cli`, `bashkit-coreutils-port`, `bashkit-eval`, `bashkit-js`, `bashkit-python`, `bashkit-wasm` (directory listing of `bashkit/crates/`). `AGENTS.md` describes `knowledge/` as "the canonical OKF bundle and persistent project memory" (`bashkit/AGENTS.md:22`) and lists the durable knowledge areas including `foundations/vfs`, `security/threat-model`, `integrations/tool-contract`, `integrations/script-analysis`, `security/http-transport`, and `security/credential-injection` (`bashkit/AGENTS.md:24-60`).

### The filesystem reality

"Every Bashkit script runs against an in-memory virtual filesystem (VFS), not the host disk ... the bytes live in memory and disappear when the interpreter is dropped. Path traversal like `../../../etc/passwd` is normalised away, and symlinks are stored but never followed. The host is invisible by default; you grant access deliberately, never by accident." (`bashkit/docs/filesystem.md:3-8`). "there is no real filesystem to escape to unless you mount one" (`:10-11`).

The layering stack composes "read-only enforcement, text mounts, and host mounts over an in-memory base, and swap mounts at runtime" (`filesystem.md:14-17`). Implementations: `InMemoryFs` (default, seeds `/`, `/tmp`, `/home`, `/home/user`, `/dev`), `OverlayFs` (copy-on-write with whiteouts), `MountableFs` (longest-prefix mounts, "Always the outermost layer"), `NamespaceFs` (static rebased subtrees with per-mount access), `ReadOnlyFs` (denies every mutation), `RealFs` (host directory, "Read-only (safe) or read-write (dangerous)") (`filesystem.md:78-84`). A custom backend implements `FsBackend` and is wrapped in `PosixFs` for POSIX semantics (`filesystem.md:52-58`). Host access is "opt-in and read-only by default" (`filesystem.md:87-88`). Binding parity exposes `files`, `mounts: [{ host_path, vfs_path?, writable? }]`, and `readonly_filesystem` (`filesystem.md:191-195`).

### Why "two filesystem realities"

PromptForge's phrase appears three times: `capabilities.rs:295-297`, `environment.rs:115-117` ("bashkit vs terminal: two filesystem realities, and a context gets one or the other, never both"), and `2026-09-13-1-capabilities-global-naming.md:151,161`. The sources do not expand the phrase further. Read against bashkit's own docs the meaning is direct: a bashkit run's `cat`, `ls`, and redirections resolve against bashkit's in-memory VFS ("not the host disk", `filesystem.md:3-4`), while a terminal capability would resolve the same commands against the host disk. A prompt that lists a directory would get two different answers depending on which one the model happened to call, so the design gives a context exactly one. That reading is an inference from the two documents; the sources state the rule, not the rationale.

### What bashkit would contribute beyond tools

Reading bashkit's builder surface against `Contribution` and `RunServices`:

- A tool. `BashTool` "exposes everything a model needs to call a shell safely: discovery metadata (name, description, input schema), a system prompt describing the sandbox, streaming output" (`bashkit/docs/llm-tools.md:3-7`). This is the tool-pack case and the least interesting one.
- A prompt fragment. `tool.system_prompt()` is part of the tool contract (`llm-tools.md:25,44-45`; `README.md:98`). Bashkit expects the host to inject sandbox-describing text into the model's context. In PromptForge terms that is a prompt fragment (2.2), and it carries `OutputTrust` since bashkit's prompt text is host-authored, not fetched.
- A mount, in either direction. Bashkit's `MountableFs` and `NamespaceFs` accept arbitrary `FileSystem` implementations (`filesystem.md:113-133`), and a custom `FsBackend` "(a database, object store, key-value store)" can back it (`filesystem.md:56-57`). So a bashkit capability can either expose its `InMemoryFs` at a prefix of PromptForge's router (a mount contribution, 2.1) or mount PromptForge's `RunServices.vfs` into bashkit's namespace so `store.*` files are visible to the shell. Which direction is chosen is not in the sources.
- A sandbox reality. The `Bash` instance is the reality: "Each `Bash` instance is fully isolated, no shared state between tenants" (`README.md:632`); "All 167 commands are reimplemented in Rust, no `fork`, `exec`, or shell escape" (`README.md:626`). The conflict declaration in PromptForge (`conflicts()`) is how this reality is made exclusive.
- A resource-limit policy. `ExecutionLimits` and `ExecutionProfile` ("`Standard`, `Hardened`, `Interactive`", `bashkit/docs/configuration.md:30-36`) cap commands, loop iterations, function depth, stdout/stderr bytes, filesystem bytes and file count, parser fuel and AST depth (`README.md:629-631`). "Profiles never enable network access" (`configuration.md:37`). PromptForge's own `RunLimits` (`config.rs:57-67`: tool iterations, fanout concurrency, response bytes, Lua memory, Lua log events, request timeout) does not cover any of these, so the limit policy is capability-owned configuration, which the contract says "arrives here, never via the prompt" (`capabilities.rs:321-322`).
- A network policy. "`curl`, `wget`, and `http` are the only way a script can reach the network, and they are default-deny ... You opt in host by host with a `NetworkAllowlist`" (`bashkit/docs/networking.md:3-5`); matching is literal scheme, host, port, path prefix with no DNS at check time (`networking.md:59-68`), plus private-range SSRF refusal at connect time (`networking.md:70-77`). Requests "flow through the same hooks pipeline ... so a host can observe, rewrite, or cancel an outbound request before it leaves" (`networking.md:123-126`). This overlaps PromptForge's A3 policy for `promptforge-webfetch` (`archdoc.md:22`); the sources do not say which governs when both are active.
- A pre-execution analysis. `analyze()` "parses a script and reports what it statically refers to ... It never executes anything. It exists for the question every agent host has to answer: the model produced this command, do I run it, or ask the user first?" (`bashkit/docs/script-analysis.md:3-8`). It is "advisory, not a boundary" (`:46`). In PromptForge terms this is an approval hook between a model's tool call and its dispatch; the capabilities plan places that checkpoint at the capability level ("high-risk gating attach at the capability level; the subagent spawn is the policy/approval checkpoint for sandbox-escaping work", `2026-09-13-1-capabilities-global-naming.md:161`). No `Contribution` or `RunServices` field exists for it.
- A snapshot. "Bashkit can serialize an interpreter into opaque bytes and restore it later. Use snapshots for checkpoint/resume flows" capturing shell state, VFS contents, and session counters (`bashkit/docs/snapshotting.md:3-11`). This maps onto the harness plan's deferred resume-by-re-execution (`2026-09-18-4-sans-io-engine-harness.md:338`) as capability-owned state the harness would have to persist; nothing in PromptForge defines such a hook.
- Custom builtins. "Register your own commands as bash builtins. They share the interpreter's VFS and shell state" (`README.md:262-264`), with "execution-scoped VFS/request handles by default" (`README.md:295-296`). A PromptForge capability could register PromptForge tools as bash builtins, making the shell a second dispatch surface. Not in the sources on the PromptForge side.

The webfetch-style credential rule is worth noting for a bashkit bridge: bashkit lists `security/credential-injection` ("Per-host HTTP credential injection without exposing secrets", `bashkit/AGENTS.md:53`) and `security/http-transport` ("route curl/wget via host egress boundary", `:54`). If a bashkit capability ever carried credentials, A2 and the sans-io rule that "The engine holds no credentials" (`2026-09-18-4-sans-io-engine-harness.md:132`) put them on the harness side of the capability, never in the engine.

## 4. Prior field comparison findings

`promptforge/vibe/agent-runtime-field-comparison-and-adoption.md` judges PromptForge against Tactus, IronCrew, Leeway, Goose, and agent-runtime (`:3`). Its eight findings (`:10-18`), each marked for whether it implies a non-tool capability contribution:

1. "Adopt Tactus and IronCrew's callable episode boundary" - every model-facing section becomes one callable agent context (`:10`). Runtime structure; no capability kind implied.
2. "Steal Goose's dual-visibility compaction model" - keep the event log, replace only the model projection (`:11`). Runtime policy (2.10); no capability kind implied.
3. "Centralize tool-protocol healing before every provider call" (`:12`). A runtime projector; no capability kind implied.
4. "Promote Workshop input into a generic elicitation protocol ... a durable host-owned wait usable by deterministic Lua and autonomous model tools" (`:13`). Implies the input-broker bridge capability (2.4): "Lua and optional model tools should call the same `user_input` primitive, while the launch host chooses blocking, immediate fallback, or failure" (`:72`).
5. "Bind system, tools, model, and compaction policy into episode identity" (`:14`). Implies that any capability contribution (tool schemas, prompt fragments) becomes part of a sealed identity: "seal the effective system prompt, ordered tool schemas, model options, compaction policy, and projection rules at the first model call" (`:78`). It constrains contributions rather than adding a kind.
6. "Return autonomous decisions through typed signals" (`:15`). Runtime `tool_loop()` return shape; no capability kind implied.
7. "Persist reconstructible effects rather than opaque executor stacks" (`:16`). Implies capability-held state (bashkit snapshots, section 3) would need a persistence hook; the harness log is the PromptForge answer, and "nothing reads it back into the engine" (`2026-09-18-4-sans-io-engine-harness.md:76`).
8. "Split orchestration centers before adding these mechanisms" (`:17`). Structural; it is the origin of the 500-line ceiling pressure and says "interaction brokering should become separate modules" (`:96`), which is where the input broker now lives.

The report's own execution order places the broker fifth: "Lift `user_input` into the generic wait protocol and expose the same broker to Lua and optional model tools, satisfying Finding 4" (`:118`). Findings 4, 5, and 7 are the ones that touch capability contributions; the remainder are engine-internal.

## 5. Constraints on any new contribution kind

Any field added to `Contribution` or `RunServices` has to satisfy the following, each quoted from the governing document.

Sans-io engine. The engine performs no I/O and holds no host trait objects, so a contribution the engine consumes must be data, and a contribution that does work must be performed by the harness. "Engine (`promptforge-api-runtime` and its private crates under `crates/promptforge/`): a deterministic state machine. Given the same `RunContext` and the same sequence of answers it produces the same effects, events, and ids. It performs no I/O, reads no clock, and holds no host trait objects." (`promptforge/vibe/2026-09-18-4-sans-io-engine-harness.md:162`). "`step` returns the effects to perform and the events produced; nothing in the engine awaits, blocks, reads a clock, or calls a host callback." (`:69`). Capability activation itself moves to the harness: "Harness run preparation: parse; resolve declared capabilities, check co-activation conflicts, activate with `RunServices { vfs, cancel }`, assemble the `ToolCatalog` and the id-to-implementation table" (`:215`), and the engine's `ToolBinding` "carries id, alias, schema, description, output kind, and conflicts, never an implementation" (`:782`).

No credentials in the engine. "The engine holds no credentials and opens no connections; the harness holds the model client and capability implementations, as `workshop-sessions` does today." (`2026-09-18-4-sans-io-engine-harness.md:132`). Archdoc A2: "Vendor credentials remain inside the Gateway process; Workshop and CLI reach credentialed model providers only through server-side Gateway relays that never expose vendor bearer keys to browser or Lua code." (`promptforge/vibe/archdoc.md:21`). The harness's `GatewayBinding` redacts its key in `Debug` (`promptforge/crates/harness-api/src/harness.rs:34-44`).

Effects as data, one answer per effect. "Effect: a leaf yield turned into a value the engine returns to its host; the host performs it and returns an `EffectAnswer`." (`2026-09-18-4-sans-io-engine-harness.md:54`). "Each effect has a serializable projection, `EffectRecord`, which is the effect minus live handles (the store access); the log stores records, and only records deserialize." (`:119`). "`Done` is never reported while any issued effect is unanswered" (`:122`). A capability that needs a new leaf interaction needs a new effect kind and a harness performer, not a callback.

Frozen, methodless handles and typed yields (A8, A9). "A8. The Lua VM boundary accepts scheduler state changes only from typed `Request` variants yielded by the installed shim; direct or malformed yields fail without changing scheduler state." (`archdoc.md:27`). "A9. The Lua VM boundary exposes host capabilities as namespace functions over plain values (`models.*`, `tools.*`, `store.*`); handles are frozen, inspectable, and methodless, with an optional leading handle argument selecting an explicit binding. The chainable `messages.new()` builders are the sole deliberate exception." (`archdoc.md:28`). The harness plan applied A9 to its own new handles: "`Task` handles are methodless (lua AGENTS.md and archdoc A9 forbid colon methods on host handles; user chose to drop the methods rather than take an exception)" (`2026-09-18-4-sans-io-engine-harness.md:298`). Any Lua surface a capability contributes (2.3) must be a namespace of functions over plain values.

Interior versus exterior. "Never package an interior primitive as a capability; never assume an exterior one." (`2026-09-13-1-capabilities-global-naming.md:56`).

Untrusted content is guard-wrapped, wire payloads are never rewritten (A6). "The executor neutralizes chat-template control delimiters in untrusted tool and Lua text, but never rewrites assistant replay or tool-call wire payloads." (`archdoc.md:25`). "Prompt fragments carry `OutputTrust`; AGENTS.md content arrives `Untrusted` and flows through the existing guard-wrap machinery." (`2026-09-13-1-capabilities-global-naming.md:162`).

Observation never decides. "Reports must not affect any execution decision." (`promptforge/crates/promptforge-api-types/src/observe.rs:447`). "Recording and null observers must produce identical outputs, errors, ordering, and side effects." (`2026-08-05-1-section-lua-lifecycle.md:87`).

Claims per storage, not per namespace. "an overlay shares the base's claims table, which is only correct for two views of the same storage" (`environment.rs:105-106`); "An overlay shares the run's claims table, which is correct here because capability storage is run-scoped - same run, same storage." (`2026-09-13-1-capabilities-global-naming.md:192`). A mount contribution overlays; it never builds a second router.

Containment and identity. "Every contributed tool's id lives under the capability's own id: `namespace/pack/name` for a `namespace/pack` capability. Containment is total and is checked when the run's catalog is assembled." (`capabilities.rs:280-282`). Any new contribution kind that carries names (a Lua namespace, a mount prefix) has no stated containment rule yet; not in the sources.

Host config, never prompt config. "Host-supplied per-capability config arrives here, never via the prompt." (`capabilities.rs:321-322`). Bashkit's limits, allowlist, and mounts are host config under this rule.

One-door rule. "PromptForge is one door: crates outside the promptforge-* family may depend only on promptforge-api-runtime and promptforge-api-types, never on the internal promptforge-* substrate crates" (`promptforge/AGENTS.md:31`); the harness has the same rule with `harness-api` as its door (`AGENTS.md:28`). "The first-party capability rides the facade so hosts never name the internal pack crate (the one-door rule)." (`promptforge/crates/promptforge-api-runtime/src/capabilities.rs:66-67`). A bashkit capability crate would sit in `crates/harness/` and be registered by `harness-sessions` (`2026-09-18-4-sans-io-engine-harness.md:165`).

500-line files and flat directories. "No file exceeds 500 lines. If an edit would push a file past 500, split first, then edit." (`promptforge/AGENTS.md:60`). "Workspace lints: `unsafe_code` forbidden, `unwrap_used`/`expect_used` denied, pedantic clippy; files under 500 lines; flat source directories" (`2026-09-18-4-sans-io-engine-harness.md:90`). `environment.rs` is 274 lines; `capabilities.rs` (types) is already 505 lines (tests live in a sibling file via `#[path]`, `capabilities.rs:23-25`). The enforced check covers "the Rust files in the workshop-* and harness-* crates carrying the marker" (`AGENTS.md:60`), so the types file is under the prose rule but not the mechanical one today; when the contract moves to `crates/harness/capabilities/` (`2026-09-18-4-sans-io-engine-harness.md:165`) it enters the enforced scope, and any new `Contribution` field splits it first.

No structural enforcement without approval. "Repository policy binds plans. A plan cannot introduce a source parser, snapshot, allowlist, count, ceiling, topology check, import walker, or other structural enforcement unless the user explicitly approves that exception." (`promptforge/AGENTS.md:40`). "The capability co-activation conflict check is behavior validation at prepare, not a source parser." (`2026-09-13-1-capabilities-global-naming.md:58`).

Non-exhaustive growth, not redesign. `Contribution` "is [`Default`] and grows without redesign" (`capabilities.rs:353-354`); `RunServices` is `#[non_exhaustive]` (`capabilities.rs:324`). `RunContext.model` "Grows into a catalog or policy in the deferred multi-model future - a field change, never a signature change." (`config.rs:212-214`).

Determinism. "Two runs with the same seed, `started_at`, and answers produce identical effect and event sequences" (`2026-09-18-4-sans-io-engine-harness.md:81`). A contribution that introduces nondeterminism inside the engine (a live clock, an unordered collection iterated by `pairs`) breaks the replay contract recorded under Deferred (`:337`).

## 6. Gaps

Looked for and did not find:

- Any code or plan text specifying the shape of the deferred `mounts`, `fragments`, or Lua-surface fields on `Contribution`. The names appear (`capabilities.rs:352`; `2026-09-13-1-capabilities-global-naming.md:47,78,192`) but no type sketch exists.
- Any plan text for a bashkit capability itself. Bashkit is named only as the conflict example (`capabilities.rs:296`, `environment.rs:115`), as a self-contained capability in the bridge discussion (`2026-09-13-1-capabilities-global-naming.md:193`), and as the 142-command motivation for discovery (`:579`). No crate, no `conflicts()` implementation, no mount direction, no limit or allowlist mapping.
- A "terminal" capability. The word appears only in the bashkit pairing; no design for a host-shell capability exists in either repository.
- An expansion of "two filesystem realities" beyond the phrase. Section 3 marks the reading as inference.
- A containment or naming rule for non-tool contributions (Lua namespace names, mount prefixes). Only tool ids have one (`capabilities.rs:280-282`).
- A `Requirements` field for a missing host service behind a bridge capability. The plan says one is "a `Requirements` field to add then" (`2026-09-13-1-capabilities-global-naming.md:193`); `requirements.rs` was not read for this survey and no such field is referenced from `environment.rs`.
- A capability-contributed observer, event sink, timer, compactor, or model fill policy. Every source frames these as runtime or harness-owned.
- An approval or pre-dispatch hook where bashkit's `analyze()` could attach. The plan places gating "at the capability level" (`2026-09-13-1-capabilities-global-naming.md:161`) without a contract.
- A persistence hook for capability state across resume (bashkit snapshots). The harness log persists effects, answers, and events only (`promptforge/crates/harness/log/README.md:3`).
- How a bashkit `NetworkAllowlist` composes with the A3 webfetch policy when both capabilities are active.
- `bashkit/docs/scripted-tools.md`, `git.md`, `request-signing.md`, and the `knowledge/` tree were not read; the `scripted_tool` feature ("Compose ToolDef+callback pairs into multi-tool bash scripts", `bashkit/README.md:26`) may be relevant to registering PromptForge tools as builtins and is unexamined.
- The current state of the sans-io plan's execution. `crates/harness/` exists with `capabilities`, `log`, `models`, `runner`, `sessions` and `harness-api` (directory listing), and `harness-capabilities` names the three traits (`lib.rs:1-4`), but `environment.rs` still performs activation and `RunContext` still carries `observer`, `input`, `on_delta`, and `debug` (`config.rs:200-207`), so the move described at `2026-09-18-4-sans-io-engine-harness.md:782` has not landed in the files read.
