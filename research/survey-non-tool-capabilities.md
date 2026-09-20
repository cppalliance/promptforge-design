# What a PromptForge capability could contribute besides tools

Report type: analytical / recommendation. Written for the PromptForge owner. The decision it serves: which fields to add to `Contribution` and `RunServices`, and in what order.

## Summary

Today a capability can hand a run exactly one thing: a list of tools. That was a deliberate first step, and the doc comment on `Contribution` says as much. This report looked at everruns, zeroclaw, zed, bashkit, and eight public agent frameworks and found thirty capabilities that hand the run something else, from a filesystem mount to a hook that holds a tool call until a person answers. Between them they need six new kinds of contribution:

- a mount: a filesystem backend placed at a path in the run's VFS
- prompt text: a named piece of the system prompt or the per-turn context, marked trusted or untrusted
- Lua functions: a namespace installed in every section VM
- a hook: code that runs before a tool call, after a tool result, before the tool list goes to the model, or on each chunk of model output
- a command: an action an operator can run without involving the model
- saved state: bytes the harness stores so a run can resume, plus a teardown call when the run ends

They also need four new handles on `RunServices`: the input broker, a secrets store, a schedule store, and the parent `Environment`. A capability consumes each of these; it provides none of them, which is why they belong on the services side.

The recommendation is to add each field only when the first capability that needs it is built, in this order: `agents-md` (prompt text), `user-input` (input broker and Lua functions), `bashkit` (mounts, hooks, saved state, and the first real conflict pair), `approval` (hooks made general), then `skills` and `mcp`. The order follows the design's own rule that a field arrives with the capability that needs it, and it puts the cheapest field first and the capability that exercises the most machinery third. Four of the thirty (budget, compaction, request shaping, model routing) cross rules PromptForge has already written down. Listing them lets the owner turn them down on the record instead of rediscovering the objection when someone proposes them later.

The evidence for growing `Contribution` this way is strong, and it comes from systems that started in different places and arrived at the same shape. Everruns, a hosted agent product, gives its `Capability` trait about forty methods; tools are one return value among mounts, prompt text, hooks, commands, MCP servers, and child-agent definitions, and several of its shipped capabilities contribute no tools at all. Pydantic AI, a Python library, now ships a `Capability` type that bundles tools, hooks, instructions, and model settings and calls it "the primary extension point". Claude Code plugins bundle skills, agents, hooks, MCP servers, channels, and output styles. Zed, an editor, builds a thread from six inputs (project rules, MCP registry, profile, environment, action log, sandbox grants) and then registers tools against them.

The systems disagree on packaging and agree on three rules. The runtime treats every contribution generically and never checks which capability it came from. Prompt text is a named slot with a trust level, never a string appended in activation order. And permission checks belong to the host: a capability supplies the rule, the host runs the prompt.

## 1. What exists today

A capability is "the activation unit: code that runs at run setup and makes services available to the run". The executor calls `create(&RunServices)` once per run and gets back a `Contribution`. `RunServices` has two fields, `vfs` and `cancel`, and its doc comment says the input broker, the observer, and the model client can be added later. `Contribution` has one field, `tools`, and its doc comment says "mounts, prompt fragments, and Lua surface are deferred until the capabilities that need them land". Both types were written with growth in mind: `RunServices` is `#[non_exhaustive]` and `Contribution` derives `Default`, so adding a field breaks no existing capability. The only code that reads a `Contribution` today is `assemble_catalog`, which reads `.tools`.

The plan already states the rule for what a capability may own and what the runtime keeps. The test is whether the thing reaches outside the run: "Never package an interior primitive as a capability; never assume an exterior one." So the store, `var`, `log`, the models namespace, and cancellation stay in the runtime. That test is what keeps the store and the timer off the list below; both appear in Appendix A with the quotes that place them in the runtime.

The sans-io plan adds a second constraint. It makes the engine a state machine that "performs no I/O, reads no clock, and holds no host trait objects", and moves capability activation into the harness. In practice the harness will call `create` and hold whatever comes back, and the engine will see only tool ids and schemas. So anything a capability contributes must either be plain data the engine can hold or code the harness runs when it performs an effect. A third rule governs configuration: per-capability settings "arrive here, never via the prompt", so limits, allowlists, and credentials come from the host at registration. Bashkit's execution limits and network allowlist are the first concrete case of such settings.

Sources: promptforge `crates/promptforge-api-types/src/capabilities.rs:3-11,317-330,350-369`; `crates/promptforge-api-runtime/src/execute/environment.rs:232`; `vibe/2026-09-13-1-capabilities-global-naming.md:56`; `vibe/2026-09-18-4-sans-io-engine-harness.md:162,215`.

## 2. How the survey was done

Five surveys ran in parallel on 2026-09-19. Four read local checkouts: everruns, zeroclaw, zed, and PromptForge together with bashkit. The fifth read the public documentation for MCP, Claude Code, the OpenAI Agents SDK, LangGraph, Pydantic AI, Google ADK, Letta, and the Claude Agent SDK. Running them in parallel kept each one narrow enough to read whole files; the everruns survey alone worked through a `capabilities/mod.rs` that runs past 2,800 lines. Each survey pulled verbatim quotes before writing anything and cited every claim to a file and line or a URL. Where a source said nothing, the survey wrote "not in the sources".

The surveys turned up 15, 18, 20, and 65 candidate kinds respectively, with heavy overlap. The overlap is the useful part: when three codebases with no shared history build the same thing, the design is settled enough to copy. This report merges the candidates into thirty capabilities. Each entry is one thing a prompt author could declare in frontmatter, given an illustrative id like `promptforge/skills`. Each is rated one of three ways. "Planned" means PromptForge's own plans already name it. "New" means nothing in PromptForge forbids it and it needs one new field. "Conflicts with a rule" means PromptForge has already written a rule it would break.

## 3. The thirty capabilities

Table 1 groups the thirty into seven families, ordered from what the model reads to what the run can start. Seven entries are already planned, nineteen are new, and four conflict with a rule. Each entry below gets a short description and a sources line giving the file and line each claim rests on.

Table 1. Thirty capabilities that contribute more than tools.

| # | Capability | What it hands the run besides tools | Who does this today | Rating |
| --- | --- | --- | --- | --- |
| 1 | `agents-md` | Untrusted prompt text from workspace instruction files | everruns, zed, Claude Code | Planned |
| 2 | `facts` | Prompt text that changes every turn (time, budget left), kept out of the cached prefix | everruns | New |
| 3 | `skills` | A catalog in the prompt, a read-only mount, a loader that resolves at call time | zed, zeroclaw, Claude Code, MCP | New |
| 4 | `identity` | Trusted prompt text describing the agent's persona | zeroclaw, Claude Code | New |
| 5 | `mcp` (beyond tools) | MCP prompts as commands, resources as a mount, elicitation as user input | MCP spec; zed (prompts only) | New |
| 6 | `bashkit` | A mount, prompt text, resource limits, a network allowlist, a pre-run check, saved state | bashkit | Planned |
| 7 | `terminal` | An OS sandbox around each command, per-run write grants, prompt text describing them | zed, zeroclaw | Planned (as the capability bashkit conflicts with) |
| 8 | `fs` | A Lua `fs` namespace over the VFS | PromptForge plan only | Planned |
| 9 | `sandbox-remote` | A container or remote sandbox with start, pause, checkpoint, and teardown | everruns | New |
| 10 | `approval` | A hook that blocks a tool call until a person answers | zed, everruns, zeroclaw, Claude Code | New |
| 11 | `guardrails` | Hooks that check tool arguments and results against host rules | everruns, OpenAI, Pydantic AI | New |
| 12 | `output-guard` | A hook on streamed model output for prompt echo, injection, leaked secrets | everruns, zeroclaw | New |
| 13 | `budget` | A "remaining budget" fact and a hook that stops the run | Pydantic AI, everruns, Claude Agent SDK | Conflicts with a rule |
| 14 | `trust` | A flag that hides tools and prompt text when the workspace is untrusted | zed, zeroclaw | New |
| 15 | `user-input` | A `user_input()` Lua function and an input tool, both wired to the input broker | PromptForge plan; MCP, LangGraph | Planned |
| 16 | `plan` | A Lua namespace that publishes a checklist to the host UI | zed, Claude Agent SDK | New |
| 17 | `channel` | A reply tool, untrusted prompt text about the channel, and a route for approval prompts | zeroclaw, Claude Code | New |
| 18 | `memory` | A cross-run store shown as prompt text, a mount, and a write tool | Letta, everruns, zeroclaw | New |
| 19 | `knowledge` | A retrieval index plus a hook that attaches citations to output | everruns, LangGraph | New |
| 20 | `secrets` | Credential handles for other capabilities; nothing visible to the model | zeroclaw, everruns | New |
| 21 | `compaction` | Hooks that filter history and build the model's view of it | everruns | Conflicts with a rule |
| 22 | `loop-guard` | A hook that detects repeated calls and injects a reminder or blocks | everruns, zeroclaw | New |
| 23 | `discovery` | A search tool that changes which tools are advertised | PromptForge plan; everruns, Pydantic AI | Planned |
| 24 | `request-shaping` | Provider request options: cache breakpoints, parallel calls | everruns | Conflicts with a rule |
| 25 | `model-router` | Choosing the model per role or per call | Pydantic AI, everruns, zed | Conflicts with a rule |
| 26 | `sub-runs` | Child runs from a prompt directory or spawned dynamically, with narrower policy | PromptForge plan; everruns, Claude Code | Planned |
| 27 | `schedule` | Future work registered in a host store, re-entering as a new run | everruns, zeroclaw, Letta | New |
| 28 | `hooks` | User-written lifecycle hooks, as data, run by a central executor | everruns, Claude Code | New |
| 29 | `commands` | Operator actions that run without the model | everruns, zed | New |
| 30 | `action-log` | A record of every file read and edit, for review and stale-read warnings | zed | New |

### 3.1 What the model reads

**1. `agents-md`.** Reads `AGENTS.md`, `CLAUDE.md`, `.rules`, and similar files from the workspace and puts them in the model's context. PromptForge already names this and has settled the trust question: the text arrives untrusted and goes through the existing guard wrap. It is also the cheapest of the thirty to build, because the files come through the VFS PromptForge already has and the only new machinery is the prompt-text field. Everruns moved this text out of the system prompt into a per-turn user message after finding that file instructions belong below the harness's own instructions and outside the provider's cached prefix; the move decides the trust question and the caching question at the same time. Zed reads the first match from a list of nine filenames per worktree and has a test that personal instructions render before project rules.

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:47,162`; everruns `crates/core/src/capabilities/mod.rs:505-513`; zed `crates/prompt_store/src/prompts.rs:22-32`, `crates/agent/src/templates.rs:150-156`.

**2. `facts`.** Small values that change every turn, such as the current time or the remaining budget. Without a place for them, a prompt that needs the time either bakes a stale value into the system prompt or spends a tool call on it every turn. Everruns splits these from static prompt text: static facts go into the cached prefix, dynamic facts go into a `<facts>` block at the end of the conversation so the cache survives. Its `current_time` builtin exists so the model knows the time without a tool call. In PromptForge the engine has no clock, so the harness would fill these in when it performs a `Chat` effect, which keeps the engine deterministic and keeps the clock where the sans-io plan already puts it.

Sources: everruns `crates/core/src/capabilities/facts.rs:27-48`, `crates/builtins/src/current_time.rs:52-56`; promptforge `vibe/2026-09-18-4-sans-io-engine-harness.md:105`.

**3. `skills`.** Folders with a `SKILL.md` file. The prompt gets a short catalog (name, description, path); the body loads only when the model or the user asks for it. The catalog is small on purpose, since a skill body can run to tens of kilobytes and loading every body every turn would crowd out the conversation. Zed caps the catalog at 50 KB and builds the loader with a closure that reads the current skill list at call time, so skills added after the run started are still visible. That resolver matters for PromptForge because activation happens once at prepare, before the run starts, and anything discovered later needs a way back in. Everruns turns skill folders into read-only mounts under `/.agents/skills/`. Zeroclaw audits each skill before loading it. MCP 2026-07-28 added "Skills over MCP" as an extension. This is the clearest case where prompt text and a mount arrive together.

Sources: zed `crates/agent/src/templates/system_prompt.hbs:220-247`, `crates/agent/src/agent.rs:806-815`; everruns `crates/core/src/capabilities/mod.rs:976-977`; zeroclaw `crates/zeroclaw-runtime/src/skills/mod.rs:98-110`; modelcontextprotocol.io/specification/2026-07-28.

**4. `identity`.** A persona document written by the operator and rendered as a trusted section of the prompt. PromptForge has no host-side equivalent today; whatever voice an agent has comes from the author's prompt. Zeroclaw loads the document from markdown or JSON with sections for identity, psychology, and language style. Claude Code ships the same idea as "output styles" inside plugins. It matters here because it is trusted prompt text from host config, the opposite case from entry 1, and the two together show why the field needs a trust level.

Sources: zeroclaw `crates/zeroclaw-runtime/src/identity.rs:1-39`; code.claude.com/docs/en/output-styles.

**5. `mcp` beyond tools.** MCP servers offer three things: tools, prompts ("templated messages and workflows for users"), and resources ("context and data"). No local runtime surveyed uses the last two, because each built MCP support for tools first and never returned for the rest. Zed turns prompts into slash commands but throws away resource content with a warning, and advertises no client features. Everruns maps servers to tools only. The mapping for PromptForge follows from how the spec defines each primitive: prompts are user-selected, so they become commands; resources are host-decided, so they become a read-only mount the host chooses whether to expose; and MCP elicitation goes through the input broker.

Sources: modelcontextprotocol.io/specification/2025-06-18 and 2026-07-28; zed `crates/agent/src/tools/context_server_registry.rs:450-455`, `crates/context_server/src/protocol.rs:43-47`; everruns `crates/mcp/src/capability.rs:47-50`.

### 3.2 Filesystem and shell

**6. `bashkit`.** A bash interpreter that runs in-process against an in-memory filesystem; it never touches the host disk unless a directory is mounted in. PromptForge names it only as the example conflict: "bashkit and a terminal are two filesystem realities, and a context gets one or the other, never both." Besides its `BashTool`, bashkit would contribute more than any other entry. It needs a mount, in one of two directions: PromptForge's VFS mounted into bashkit's namespace, or bashkit's filesystem mounted at a prefix of the run's VFS. It supplies its own system-prompt text via `tool.system_prompt()`. Its `ExecutionLimits` cover command count, loop iterations, output bytes, and filesystem bytes, none of which PromptForge's `RunLimits` cover. Its `NetworkAllowlist` is default-deny per host. Its `analyze()` function inspects a script before running it, for the question "the model produced this command, do I run it, or ask the user first?" And it can snapshot the shell and filesystem to bytes for resume. No design for a bashkit capability exists in either repository. Building one would settle four open questions at once (the mount direction, how a capability declares limits, where a pre-dispatch check attaches, and what the harness persists for resume), which is why recommendation 3 puts it third rather than last.

Sources: bashkit `README.md:9`, `docs/filesystem.md:3-8,56-57,113-133`, `docs/llm-tools.md:25`, `docs/configuration.md:30-36`, `docs/networking.md:3-5`, `docs/script-analysis.md:3-8`, `docs/snapshotting.md:3-11`; promptforge `capabilities.rs:295-297`, `crates/promptforge-api-runtime/src/execute/config.rs:57-67`.

**7. `terminal`.** A real shell on the host. PromptForge needs this entry mostly so the conflict pair has two members, and the sandbox design can follow zed's. Zed wraps each agent command in Seatbelt, Bubblewrap, or WSL-Bubblewrap with a list of writable paths, and warns that the list must come from the project's worktrees rather than the command's working directory, "which is model-controlled and would let the model widen its own writable scope". Grants last for one call, one thread, or forever; they exist because a sandbox that never asks is either too tight to be useful or too loose to be a sandbox. The prompt text describing the sandbox renders only when the terminal tool is present. Zeroclaw's `Sandbox` trait wraps every spawned command and must fail closed when it cannot preserve normal shell semantics. In PromptForge the word "terminal" appears only in the sentence that names bashkit's conflict.

Sources: zed `crates/acp_thread/src/terminal.rs:35-71`, `crates/acp_thread/src/acp_thread.rs:136-141`, `crates/agent/src/templates.rs:318-321`; zeroclaw `crates/zeroclaw-runtime/src/security/traits.rs:7-30`.

**8. `fs`.** A Lua `fs` table that reads and writes files through the VFS. PromptForge's plan says this must be a capability because it reaches host files; `store` stays built in because it reads only the run's own scratch mount, while `fs` can reach whatever the environment mounted at `/`. Archdoc A9 governs its shape: functions over plain values, frozen handles, no methods. No other surveyed system lets a capability add scripting functions; the closest is everruns' experimental `lua_code_mode`, which hides tools and has the model call them from a Lua script. So this field has no external template, and its containment rule (which namespace names a capability may claim) is still unwritten.

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:56`, `vibe/archdoc.md:28`; everruns `knowledge/execution/capabilities.md:1334-1338`.

**9. `sandbox-remote`.** A container or hosted sandbox tied to the run. It is a third filesystem beside bashkit and the terminal and would most likely join the same conflict set. Everruns runs one per session with options to start it early, pause it when idle, checkpoint it, and delete it; its Docker variant starts on first use and lasts for the session. Those lifecycle verbs are the point, since a run that ends without deleting its container keeps paying for it. Everruns has no teardown method on capabilities, and says so: "Unregistering is deliberately absent: removal raises lifetime questions - in-flight tool calls, spawned processes." That gap is why PromptForge should add a teardown call before shipping anything that holds an external resource.

Sources: everruns `crates/platform/src/capabilities/session_sandbox.rs:1-4,91-104`, `knowledge/execution/capabilities.md:253-255,760-765,1349`.

### 3.3 Permission and safety checks

**10. `approval`.** Stops a tool call until a person says yes. Every system surveyed puts the decision in the host, and three details recur that each close a hole a naive gate leaves open. Zed's tool trait has two policy flags; everything else comes from an `authorize` call the tool awaits, with a hardcoded floor that settings cannot lower and a pending prompt that watches settings so one "always" answer resolves sibling calls. Everruns' gate takes its approver as a constructor argument because "a registered gate with nowhere to ask is either a deadlock or a silent allow", and a transport failure blocks rather than allows. Zeroclaw gives each delegate agent a fresh allowlist so "always" grants never transfer. PromptForge's plan puts "high-risk gating at the capability level" but has no contract for it, so this entry is where that contract would be written.

Sources: zed `crates/agent/src/tool_permissions.rs:11-12,207-231`, `crates/agent/src/thread.rs:5684-5787`; everruns `crates/builtins/src/tool_approval.rs:10-13,33-62`; zeroclaw `crates/zeroclaw-runtime/src/approval/mod.rs:141-150`; promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:161`.

**11. `guardrails`.** Deterministic checks on tool arguments and results, configured by the host: regex, blocklist, tool pattern, or a model judge. PromptForge's untrusted-content guard (A6) covers one specific attack, chat-template delimiters; this entry is the general mechanism for everything else a host wants to check. Everruns attaches these to its hook points and contributes nothing when no checks are configured. The rule that matters for PromptForge is how they combine: hooks run for every tool the agent calls, including tools other capabilities contributed, and the first hook to block wins.

Sources: everruns `crates/builtins/src/guardrails.rs:3-6,99-107`, `crates/core/src/capabilities/mod.rs:751-756`; openai.github.io/openai-agents-python; ai.pydantic.dev/hooks.

**12. `output-guard`.** Watches the model's own output. Everruns' canary guard withholds a message when the model echoes the first sentence of its system prompt, a cheap check that catches the most common form of prompt leakage. Its streaming guards are armed once per message and run after every batch of deltas, which is what makes them usable on a stream: the guard sees partial text without waiting for the message to finish. Zeroclaw classifies text as safe, suspicious, or blocked, and scrubs credentials before text reaches any log. In PromptForge this would sit next to the A6 guard and run in the harness as it streams a `Chat` effect.

Sources: everruns `knowledge/execution/capabilities.md:994-996,1456`, `crates/core/src/capabilities/mod.rs:987-999`; zeroclaw `crates/zeroclaw-runtime/src/security/prompt_guard.rs:7-29`, `security/mod.rs:76-85`.

**13. `budget`.** Conflicts with a rule. Pydantic AI, everruns, and the Claude Agent SDK all cap tokens, calls, or dollars per run. PromptForge's `RunLimits` already lives in the runtime, and limits are interior by the design's own test; yet `RunLimits` counts iterations and bytes and has no field for tokens or cost, so a spend cap has nowhere to live today. What a capability could still add is a "remaining budget" fact (entry 2) and a hook that stops the run against a host counter. It is worth building in that reduced form once facts and hooks exist. Confidence: medium, because the runtime already owns half of it.

Sources: everruns `crates/builtins/src/budgeting.rs:3-5`, `crates/core/src/tool_context.rs:104-105`; promptforge `config.rs:57-67`; ai.pydantic.dev; platform.claude.com.

**14. `trust`.** Hides tools and prompt text when the workspace or the message source is untrusted. It sits above approval because a tool that is absent cannot be argued into use by an injected instruction; hiding is stronger than gating. Zed's restricted mode removes `fetch` and `terminal` whatever the profile says, through a trait method that defaults to allowed, and does not load project skills until the worktree is trusted. Zeroclaw stamps every turn with where it came from and whether the sender is trusted, and sub-turns never get memory injected. This is a flag on a contribution, because it changes what exists; a hook would only change what is allowed.

Sources: zed `crates/agent/src/thread.rs:5127-5134`, `docs/src/ai/skills.md:178-181`; zeroclaw `crates/zeroclaw-api/src/ingress.rs:46-65`.

### 3.4 Talking to people and channels

**15. `user-input`.** PromptForge's plan already specifies it: a `user_input()` Lua function plus an input tool, both wired to `RunServices.input`; if no broker is installed, the run degrades to the current fallback and reports the gap. Making this a capability instead of a built-in is what lets a headless host run the same prompt: it leaves the capability out, and the run reports a missing service instead of hanging on a question nobody will answer. The `InputBroker` trait exists today, but it hangs off `RunContext`; moving it to `RunServices` is the change. The rest of the field agrees that human input is a host-owned wait: MCP elicitation is the one client feature kept in the 2026-07-28 revision, and LangGraph's `interrupt()` and Pydantic AI's deferred tool calls have the same shape. This entry adds the first new `RunServices` field and the first Lua contribution.

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:193`, `crates/promptforge-api-runtime/src/input.rs:13-18,128-137`, `config.rs:205`; modelcontextprotocol.io/specification/2026-07-28.

**16. `plan`.** A checklist the run publishes to the host UI, giving it a structured view of progress during a long run. Zed renders a plan with pending, in-progress, and completed entries from any agent. In PromptForge this is a small Lua namespace whose calls become events. Events are report-only and never change execution, and a plan is outbound only, so the two fit without a new rule.

Sources: zed `crates/acp_thread/src/acp_thread.rs:1952-1962`; promptforge `crates/promptforge-api-types/src/observe.rs:447`.

**17. `channel`.** Binds a run to a chat platform or webhook. It is the first entry where a run is started by something other than an operator at a keyboard, which is why the trust tagging matters more than the transport. Zeroclaw treats each channel as a trust boundary; the orchestrator owns spawning and dispatch, and the channel may add only one verbatim mention string to the prompt. Everruns puts participant names in the per-turn context because they are "the same trust class as workspace `AGENTS.md`". In PromptForge the listener is harness infrastructure; the capability contributes a reply tool, untrusted prompt text about the channel, and a binding so approval prompts route back to it.

Sources: zeroclaw `crates/zeroclaw-api/src/channel.rs:767-791,948-953`; everruns `crates/builtins/src/channel_context.rs:8-11`; code.claude.com/docs/en/plugins-reference.

### 3.5 Things that outlive the run

**18. `memory`.** A store shared across runs. Letta makes memory blocks visible in the prompt and writable by the model. Everruns' `memory` capability is only a mount, read-only or read-write, rated medium risk because a writable shared mount lets one session influence the next; that rating is the useful detail, since it names how one run's mistake becomes every later run's premise. Zeroclaw keeps the backend behind a trait but has one renderer, in the turn engine, deciding when to inject recalled memory. The lesson is that the mount and the prompt text belong to the capability, and the decision of when to inject belongs to the host.

Sources: docs.letta.com; everruns `crates/platform/src/capabilities/memory.rs:34-62`; zeroclaw `crates/zeroclaw-runtime/src/agent/memory_inject.rs:1-22`.

**19. `knowledge`.** A retrieval index. The search tool is ordinary. What makes this more than a tool pack is everruns' pair of hooks that attach citations to the model's text and stamp a verification verdict on each, "decoupled from the feeds so any feed can be paired with any verifier". Host-verified citations are what separate a retrieval tool from a model that claims to have read something.

Sources: everruns `crates/platform/src/capabilities/knowledge_index.rs:3-4`, `crates/core/src/capabilities/mod.rs:1019-1055`; langchain-ai.github.io/langgraph.

**20. `secrets`.** Credential handles for other capabilities' tools, with nothing visible to the model. Today the only credentialed capability is `promptforge/web`, which receives its gateway token at construction, so this handle is not needed until a second capability wants credentials. Zeroclaw's plugin ABI lets a guest ask only for a logical name, so it cannot reach another plugin's secrets, and refuses the request during load, serving it only during execution. Everruns says plainly that capability config "is not a secret store". PromptForge's rule is stricter still: the engine holds no credentials. So this is a `RunServices` field on the harness side, with no `Contribution` field at all.

Sources: zeroclaw `wit/v0/secrets.wit:3-9,26-30`; everruns `crates/capability/src/reference.rs:29-31`; promptforge `vibe/2026-09-18-4-sans-io-engine-harness.md:132`, `crates/promptforge/web/README.md`.

### 3.6 Shaping history and the tool list

**21. `compaction`.** Conflicts with a rule. Everruns ships compaction as a capability with three hooks: one that filters loaded messages, one that builds the model's view of them without touching storage, and one policy the loop calls without knowing which capability supplied it. PromptForge frames compaction as author-side Lua policy; `compactors.fail` is the only shipped policy and the framework has been deferred twice. Everruns' split is still worth studying, because keeping storage lossless and projecting a view for the model is the same shape PromptForge's earlier field comparison recommended. A hook that supplies the model's view of history would let a capability help later, but the policy should stay with the author. Confidence: medium, because the deferred framework has no shape yet.

Sources: everruns `crates/core/src/capabilities/mod.rs:649-658,721-729`, `crates/builtins/src/compaction.rs:406-476`; promptforge `crates/promptforge/lua/src/compactors.rs:1-18`, `vibe/2026-09-18-4-sans-io-engine-harness.md:346`, `vibe/agent-runtime-field-comparison-and-adoption.md:11`.

**22. `loop-guard`.** Notices when a run repeats itself and injects a reminder or blocks. It is the kind of check nobody writes into a prompt and everybody wants after the first runaway run. Everruns does this with a post-load message filter and a pre-dispatch check. Zeroclaw goes further and drops the agent's autonomy one level when it sees regression. This is a hook with no tool and no prompt text of its own.

Sources: everruns `knowledge/execution/capabilities.md:949,986`; zeroclaw `crates/zeroclaw-runtime/src/trust/types.rs:134-147`.

**23. `discovery`.** PromptForge's plan already names it: a search tool over the run's catalog whose results mark tools as advertised for the rest of the run, because "capabilities like bashkit carry 142 commands, and advertising every schema drowns frontier models". It exists because of bashkit; a shell with that many commands cannot advertise them all. Everruns and Pydantic AI have the same idea under "tool search". It is a tool, but one that changes run state other than the catalog, so it needs to see the catalog at call time.

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:579,643`; everruns `crates/core/src/capabilities/mod.rs:1061-1067`; ai.pydantic.dev/capabilities.

**24. `request-shaping`.** Conflicts with a rule. Everruns lets a capability set prompt-cache options, driver-specific request options, and a parallel-tool-calls preference. PromptForge resolves dialects in the gateway and says the author never names one; letting a capability reach in would give one decision two owners. The one piece that fits is a marker for where the volatile facts tail (entry 2) begins, so the cache breakpoint lands before it.

Sources: everruns `crates/core/src/capabilities/mod.rs:686-705`; promptforge `vibe/2026-08/2026-08-08-8-tool-dialect-plugins.md:243`, `environment.rs:23-24`.

**25. `model-router`.** Conflicts with a rule. Pydantic AI capabilities can pick the model; zed forces subagents onto a configured model; everruns swaps a capability's implementation by model. PromptForge fills model roles with a host function, and today that fill is deliberately trivial: every role gets the host's current model. The plan says better filling is "a smarter fill function, not a structural change", and a capability that picked models would bypass that function. A capability may use the model client from `RunServices` but should not choose the model.

Sources: ai.pydantic.dev/capabilities; zed `crates/agent/src/thread.rs:1336-1339`; everruns `crates/core/src/capabilities/mod.rs:389-401`; promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:50`.

### 3.7 Starting and scheduling work

**26. `sub-runs`.** PromptForge's plan names a "prompt pack": a directory of prompts, one tool each, that needs the parent `Environment`, a child cancel handle, and depth accounting. Everruns adds "blueprints", child agents with private tools that never appear in the parent's list, and caps depth and descendant count. Zeroclaw checks that a child's policy is a subset of the parent's; without that rule a child that could widen its own policy would turn every sub-run into an escalation path. The tools here are ordinary; the new pieces are the `Environment` handle on `RunServices` and the narrowing rule.

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:528,657`; everruns `crates/core/src/capabilities/mod.rs:962-971`, `crates/platform/src/capabilities/subagents.rs:91-138`; zeroclaw `crates/zeroclaw-runtime/src/subagent/mod.rs:15-18`.

**27. `schedule`.** Lets a run register future work. Everruns offers one-shot and cron schedules through a host store, and one of its hooks schedules a continuation after a usage-limit error without contributing any tools. Zeroclaw stamps each fired turn with `Cron` as its origin, which is what lets approval and memory policy treat a scheduled run differently from one started at a keyboard. Only Letta's sleep-time agents and Claude Code's monitors fire on their own clock. In PromptForge this is a tool plus a `RunServices.schedule` handle; the poller belongs to the harness, since the engine has no clock.

Sources: everruns `crates/platform/src/capabilities/session_schedule.rs:1-6,53-57`, `crates/builtins/src/usage_limit_auto_continue.rs:9-16`; zeroclaw `crates/zeroclaw-api/src/ingress.rs:36-53`.

**28. `hooks`.** Lifecycle hooks written by users in config or frontmatter. Everruns accepts them as data only and runs them from a central executor "so global timeout/output/sandbox limits cannot be bypassed"; it has six events and only two can block. Claude Code documents 33 events and five handler types. The rule both follow: hooks are code when the host trusts the author, and data when they cross a boundary. Anything from frontmatter is the data form, for the same reason credentials stay out of the prompt: frontmatter is author territory, and the host must be able to bound what it does.

Sources: everruns `crates/core/src/user_hook_types.rs:25-43`, `crates/core/src/capabilities/mod.rs:894-896`; code.claude.com/docs/en/hooks.

**29. `commands`.** Actions an operator runs directly, without the model. Everruns' `/btw` reuses the session context, disables tools, and persists nothing. Zed sends MCP prompts and skills to its command palette over the same channel external agents use, and a built-in always wins an unqualified name. Commands are how MCP prompts (entry 5) and skills (entry 3) become invocable by a person, so this field arrives with whichever of those is built first. In PromptForge, Workshop would show them; the capability supplies the descriptor and the code to run.

Sources: everruns `crates/core/src/capabilities/mod.rs:926-935`, `crates/builtins/src/btw.rs:9-10`; zed `crates/agent/src/agent.rs:172-177,1490-1497`.

**30. `action-log`.** Records every file the run read or edited so the host can show a review diff and warn the model when a file changed underneath it. The stale-read warning addresses a bug every multi-tool run eventually hits: one tool edits a file another tool read earlier, and the model reasons from the old contents. Zed's log is linked from a subagent to its parent so both views work, and every mutating tool receives it at construction. PromptForge's VFS claims exist for concurrency and know nothing about review, so this would be a post-tool hook plus per-run state the host UI reads.

Sources: zed `crates/action_log/src/action_log.rs:51-65`, `crates/agent/src/thread.rs:2133-2142`.

## 4. What this means for `Contribution` and `RunServices`

### 4.1 Six new fields cover all thirty

Table 2 reduces the thirty to six kinds, and no entry needs a kind outside them, which is some evidence the list is complete. Hooks are needed most often (thirteen entries) and come in five flavors: before a tool call, after a tool result, before the tool list goes to the model, on each chunk of model output, and when building the model's view of history. Prompt text is next (nine entries).

Table 2. The six kinds of contribution the thirty capabilities need.

| Kind | What the capability hands the run | How the host combines them | Needed by entries |
| --- | --- | --- | --- |
| Mount | A `shared-vfs` backend at an absolute path | Distinct paths; overlaid on the run's router, sharing its claims table | 3, 5, 6, 8, 18 |
| Prompt text | A named slot, a trust level, whether it changes per turn, and the text or a function that renders it | The executor owns slot order and drops empties; untrusted slots are guard-wrapped and kept out of the cached prefix | 1, 2, 3, 4, 6, 7, 13, 17, 18 |
| Lua functions | A namespace of functions over plain values, per archdoc A8 and A9 | The namespace name sits under the capability id | 8, 15, 16 |
| Hook | Code for one of the five hook points | Run in priority order; first block wins; always in the harness, never in the engine | 6, 7, 10, 11, 12, 13, 14, 19, 21, 22, 23, 28, 30 |
| Command | A descriptor and the code to run | A built-in wins an unqualified name; otherwise prefixed by capability | 5, 29 |
| Saved state | Opaque bytes, plus a `teardown` method on `Capability` | The harness stores the bytes beside the run log; teardown runs on cancel and on completion | 6, 9, 30 |

A capability also needs to declare what it requires: which `RunServices` handles, resource limits, network hosts, and other capabilities. Zeroclaw's rule for these is the right one: a declaration is intent, not a grant, and the host intersects it with its own config. PromptForge already has half of this, since a missing required capability lands in `Requirements::missing_required` at prepare. A missing handle should land there the same way; that is one more field on `Requirements`, and no new mechanism.

`RunServices` grows by `input` (entries 10, 15, 17), `secrets` (6, 17, 20), `schedule` (27), and `environment` (26). The model client and observer already reserved in its doc comment are used by entries 12, 16, and 19. Each handle should be a typed field. A string-keyed map would let a capability compile against a handle the host never provides and fail at run time instead. Zeroclaw makes the same argument: "Adding a service is an explicit API change, and a store cannot be constructed while a required service is missing."

Sources: promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:192`, `crates/promptforge-api-runtime/src/execute/requirements.rs:20-23`; zeroclaw `crates/zeroclaw-plugins/src/services.rs:11-15`, `docs/book/src/architecture/decisions/ADR-014-plugin-egress-authority.md:44,63`.

### 4.2 Three lessons every system agrees on

The runtime never checks which capability a contribution came from. Everruns says this four times in its doc comments: the loop "knows nothing about any specific capability's behavior", invokes compaction "without matching on a capability ID", and so on. PromptForge already works this way for tools through `assemble_catalog`. Each new field needs the same treatment: a typed slot in `Contribution` and generic code in the harness that reads it. There should never be an `if id == "promptforge/bashkit"` anywhere. The payoff is that a new capability never needs an engine change, and when one seems to, the missing piece is a field.

Prompt text is a named slot with a trust level. Everruns has three places prompt text can go (cached prefix, per-turn untrusted context, volatile tail) and moved `AGENTS.md` between them once it understood the instruction hierarchy. Zed's template has fixed slots with one producer each and tests on their order. Zeroclaw renders every section from one context of resolved facts so the prompt cannot describe a shell other than the one that will run. A `Vec<String>` joined in activation order would lose all of that. PromptForge's guard wrap already supplies the trust half of this design; the slot and volatility halves are new.

Permission checks belong to the host. Zed's tool trait has two policy flags; everything else comes from an `authorize` call the tool awaits. Everruns' pre-tool hooks run for every tool, including those other capabilities contributed. Zeroclaw enforces policy at the dispatch site and reads it fresh on every call instead of snapshotting it. For PromptForge that puts the approval loop in the harness code that performs a `Tool` effect. A capability contributes the rule; the input broker is how the loop reaches a person, which also keeps the broker as the one path to a human and lets the harness log every wait as an effect.

Everything contributed should also record which capability produced it, as PromptForge's tool containment rule already does for tools and as everruns' `SystemPromptAttribution` does for prompt text; without that, a conflict report or an approval prompt cannot name its source. And `conflicts()` has no counterpart in any of the three runtimes, but it needs a `dependencies()` partner and a list of required handles to express "this capability needs the input broker" or "skills needs mounts".

Sources: everruns `crates/core/src/capabilities/mod.rs:639-640,666-668,676-677,722-724,751-756,1478-1481`, `crates/builtins/src/agent_instructions.rs:12-15`; zed `crates/agent/src/templates.rs:36-61,318-321`, `crates/agent/src/thread.rs:5122-5134`; zeroclaw `crates/zeroclaw-runtime/src/agent/prompt.rs:130-134`, `crates/zeroclaw-config/src/policy.rs:358`.

### 4.3 Other designs considered

A trait with forty methods, like everruns. PromptForge should keep `create` returning a value. The sans-io plan wants contributions as data the harness owns, and `Contribution` is already a struct with `Default`. A wide trait would also put per-run state back into a process-global object, which is the problem everruns solves with session-keyed side tables. The trait gains only `teardown`.

Declarative manifests, like zeroclaw's WIT worlds or Claude Code's plugin directories. PromptForge's plan is crates now and DLLs later. Everruns shows the two coexist: hooks are trait objects when trusted and JSON specs when they cross a boundary. The JSON forms should arrive with entry 28, since nothing earlier in the order needs them.

Probing instead of declaring, like zed's `Option<Rc<dyn Trait>>` accessors. That works when the host is a UI that can hide a button. Two filesystem realities cannot be hidden, so `conflicts()` is right for them. Probing fits the optional `RunServices` handles, which is what "no broker installed degrades to today's fallback" already describes, so the two approaches divide the work between them.

Doing nothing and expressing everything as tools. A tool cannot block another tool, cannot put text in the system prompt, cannot change what `store.*` sees, and has no teardown. Bashkit, which PromptForge already names, could not be built. This option is set aside.

## 5. Recommendations

Owner: the PromptForge owner. Next step for each: a vibe plan in `promptforge/vibe/` naming the capability that brings the field in.

1. Add prompt text to `Contribution`, with slot, trust level, and per-turn flag, and build `agents-md` on it. It is already planned, needs no new `RunServices` field, and settles the design eight later entries reuse. Getting the slot and trust shape right here avoids reworking it under bashkit. Confidence: high, because the plan already fixes the trust rule and three systems converge on the slot design.

2. Move `InputBroker` to `RunServices.input`, add Lua functions to `Contribution`, and build `user-input`. The plan specifies this almost verbatim, and it is the first test of the "missing service lands in `Requirements`" path. Confidence: high, because the plan text is explicit.

3. Build `bashkit` and let it bring in mounts, resource and network declarations, a pre-dispatch hook, saved state with teardown, and the first `conflicts()` pair. It needs five of the six kinds and is the one capability PromptForge already depends on for its conflict design. The mount direction is the one design question the sources leave open and should be decided in the plan. Confidence: high on the fields; medium on which way the mount goes, which no source decides.

4. Turn the single hook from step 3 into the five hook points of Table 2, in the harness only, and build `approval` on them using the input broker from step 2. Thirteen entries need hooks, and approval has the clearest agreement across systems on how hooks combine. The three details from entry 10 (hardcoded floor, fresh allowlist per delegate, block on transport failure) should be in the first version. Confidence: high on placing them in the harness; medium on the exact set of five.

5. Build `skills` (prompt text plus a mount plus a call-time resolver) and then `mcp` beyond tools (prompts as commands, resources as a mount), adding commands to `Contribution`. Both reuse fields from steps 1 and 3, and MCP's non-tool features are unused by every local runtime surveyed. Confidence: medium, because Workshop has no design for showing commands.

6. Turn down entries 13, 21, 24, and 25 as written, and reopen each only as a hook or a fact on a field that already exists. Each crosses a rule PromptForge has written down, and each has a reduced form that does not. Confidence: high, because the rules are quoted in Appendix B.

7. Add `dependencies()` to `Capability` and a list of required handles beside `conflicts()`. This is what lets prepare report "skills needs mounts" before activation, instead of failing inside `create`. Confidence: medium, because it is useful but no named capability is blocked on it yet.

8. Do not let a capability contribute an observer, a timer, the store, a compactor, or model selection. Every source places these in the runtime or the harness. Confidence: high, because the quotes are in Appendix A.

## 6. What this report does not know

The sans-io harness plan is not built yet. `environment.rs` still activates capabilities and `RunContext` still holds the observer, input broker, and delta callback. Every sentence above that says "in the harness" describes the plan; the code has not caught up. The phrase "two filesystem realities" appears three times in PromptForge and is never explained; the reading in entry 6 comes from bashkit's own documentation. The capability ids in Table 1 are made up for this report. No type sketch for the six fields exists in PromptForge; Table 2 is a proposal. The MCP 2026-07-28 pages for individual primitives returned 404, so those definitions come from the 2025-06-18 revision, and it is not confirmed whether sampling and roots were removed or moved. Some zeroclaw modules (`doctor/`, `control_plane/`, `multimodal.rs`, `calendar/`) and bashkit's `scripted-tools.md` and `knowledge/` tree were not read. AutoGen, CrewAI, and Mastra were not surveyed. None of these gaps changes the recommended order; they change how much of steps 3 and 5 is design work rather than transcription.

## 7. References

Primary sources, as read on 2026-09-19:

- PromptForge: `crates/promptforge-api-types/src/capabilities.rs`; `crates/promptforge-api-runtime/src/{capabilities.rs, input.rs, execute/environment.rs, execute/config.rs, execute/requirements.rs}`; `crates/promptforge/web/README.md`; `vibe/archdoc.md`; `vibe/2026-09-13-1-capabilities-global-naming.md`; `vibe/2026-09-18-4-sans-io-engine-harness.md`; `vibe/2026-08/2026-08-08-8-tool-dialect-plugins.md`; `vibe/agent-runtime-field-comparison-and-adoption.md`; `crates/promptforge/lua/src/compactors.rs`.
- bashkit: `README.md`; `docs/{filesystem, networking, script-analysis, snapshotting, configuration, llm-tools}.md`; `AGENTS.md`.
- everruns: `crates/capability/src/*`; `crates/core/src/capabilities/mod.rs`; `crates/core/src/{tool_hooks, tool_context, lifecycle_hooks, llm_error_hook, user_hook_types, session_services, capability_types}.rs`; `crates/builtins/src/*`; `crates/platform/src/capabilities/*`; `knowledge/execution/capabilities.md`.
- zeroclaw: `crates/zeroclaw-api/src/{hook, channel, memory_traits, runtime_traits, peripherals_traits, grants, ingress, tool}.rs`; `crates/zeroclaw-runtime/src/{approval, security, sop, skills, cron, heartbeat, agent/prompt.rs, agent/memory_inject.rs, trust}`; `crates/zeroclaw-plugins/src/*`; `wit/v0/*`; `docs/book/src/architecture/decisions/ADR-{002,014,015}.md`.
- zed: `crates/agent/src/{thread, agent, tool_permissions, sandboxing, templates, tools/skill_tool, tools/context_server_registry}.rs`; `crates/acp_thread/src/{acp_thread, connection, terminal, mention}.rs`; `crates/agent_servers/src/acp.rs`; `crates/agent_skills/agent_skills.rs`; `crates/context_server/src/protocol.rs`; `crates/extension/src/{extension_manifest, extension}.rs`; `crates/prompt_store/src/prompts.rs`; `crates/action_log/src/action_log.rs`; `docs/src/ai/*`.
- Web: modelcontextprotocol.io/specification/{2025-06-18, 2026-07-28}; code.claude.com/docs/en/{hooks, skills, sub-agents, plugins-reference, output-styles, permissions}; openai.github.io/openai-agents-python; langchain-ai.github.io/langgraph; ai.pydantic.dev/{capabilities, hooks}; google.github.io/adk-docs; docs.letta.com; platform.claude.com.

Research notes written for this report on 2026-09-19: "everruns capability survey", "zeroclaw capability survey", "zed agent capability survey", "promptforge and bashkit capability survey", and "agent runtime field survey".

## Appendix A: things that looked like capabilities but are not

Each of these came up in at least one survey as something capability-like, and each has a quote that places it elsewhere. The store is interior: "Never package an interior primitive as a capability" (promptforge `vibe/2026-09-13-1-capabilities-global-naming.md:56`). Timers are engine effects the harness performs, because "the engine has no clock" (`vibe/2026-09-18-4-sans-io-engine-harness.md:105,119`). Observers and the run log are report-only: "Reports must not affect any execution decision" (`observe.rs:447`), and "nothing reads an answer row back into the engine" (`crates/harness/log/README.md:3`). Zeroclaw's HMAC tool receipts attach where a result re-enters the context and belong to the runtime (`tool_receipts.rs:12-16`). Zeroclaw's tunnels and hardware peripherals are daemon infrastructure; their connect, disconnect, and health methods informed the teardown recommendation but the things themselves are not run-scoped. Model providers belong to the gateway under archdoc A2. Everruns' LLM error hook is folded into entry 27. Zed's context mentions and thread persistence are Workshop and harness-log concerns. The eval harness is a way of hosting the agent, so it contributes nothing to a run.

## Appendix B: rules any new field must respect

Each is quoted so a future plan can check itself against the governing text and not depend on this report's paraphrase.

The engine "performs no I/O, reads no clock, and holds no host trait objects" (promptforge `vibe/2026-09-18-4-sans-io-engine-harness.md:162`), and its `ToolBinding` holds "never an implementation" (`:782`). "The engine holds no credentials and opens no connections" (`:132`). Effects are data: "Each effect has a serializable projection, `EffectRecord`" (`:119`). Lua handles are "frozen, inspectable, and methodless" (`vibe/archdoc.md:28`). Untrusted text is guard-wrapped and wire payloads are never rewritten (`archdoc.md:25`; `vibe/2026-09-13-1:162`). A mount overlays the run's router and shares its claims table (`vibe/2026-09-13-1:192`). Every tool id lives under its capability's id (`capabilities.rs:280-282`); no such rule exists yet for Lua namespaces or mount paths. Per-capability config comes from the host, never the prompt (`capabilities.rs:321-322`). Files stay under 500 lines, and `capabilities.rs` is already at 505, so it splits before any field is added (`AGENTS.md:60`). Structural enforcement needs explicit approval (`AGENTS.md:40`). Two runs with the same seed, start time, and answers must produce the same effects and events (`vibe/2026-09-18-4:81`).

*2026-09-19 10:55 - Claude Fable 5.1*
