---
produced: 2026-09-19
title: zed agent capability survey - non-tool contribution kinds (context servers, rules, skills, ACP, extensions, project context, permissions)
source: c:\Users\Vinnie\cursor\zed
---

# Zed agent capability survey: what gets contributed to a thread besides tools

Scope: the Zed editor repo at `c:\Users\Vinnie\cursor\zed` (local checkout, ~240 crates), read-only. Focus is the native agent (`crates/agent`, `crates/acp_thread`, `crates/agent_servers`, `crates/agent_skills`, `crates/context_server`, `crates/extension*`, `crates/prompt_store`, `crates/agent_settings`) plus the `docs/src/ai/` and `docs/src/extensions/` pages. Every claim cites `path:line` relative to the repo root. Where I could not find evidence I say "not in the sources".

Orientation for the PromptForge reader: Zed's unit of "a thing that is active for a run" is a `Thread` (crates/agent/src/thread.rs) wrapped by an `AcpThread` (crates/acp_thread/src/acp_thread.rs). A `Thread` owns `tools: BTreeMap<SharedString, Arc<dyn AnyAgentTool>>` (thread.rs:1263), but it also owns a `context_server_registry` (1273), a `profile_id` (1274), a `project_context: Entity<ProjectContext>` (1278), `prompt_capabilities_tx/rx` (1285-1286), an `action_log` (1288), and `sandbox_grants` (1297-1302). Those non-tool fields are the subject of this survey.

## How zed structures agent extension

### The extension manifest: what an extension can declare

The manifest struct enumerates every contribution kind an installable extension can carry (crates/extension/src/extension_manifest.rs:83-123):

```
pub struct ExtensionManifest {
    pub id: Arc<str>,
    pub name: String,
    pub version: Arc<str>,
    pub schema_version: SchemaVersion,
    ...
    pub lib: LibManifestEntry,
    pub themes: Vec<RelPathBuf>,
    pub icon_themes: Vec<RelPathBuf>,
    pub languages: Vec<RelPathBuf>,
    pub grammars: BTreeMap<Arc<str>, GrammarManifestEntry>,
    pub language_servers: BTreeMap<LanguageServerName, LanguageServerManifestEntry>,
    pub context_servers: BTreeMap<Arc<str>, ContextServerManifestEntry>,
    pub slash_commands: BTreeMap<Arc<str>, SlashCommandManifestEntry>,
    pub snippets: Option<ExtensionSnippets>,
    pub capabilities: Vec<ExtensionCapability>,
    pub debug_adapters: BTreeMap<Arc<str>, DebugAdapterManifestEntry>,
    pub debug_locators: BTreeMap<Arc<str>, DebugLocatorManifestEntry>,
    pub language_model_providers: BTreeMap<Arc<str>, LanguageModelProviderManifestEntry>,
}
```

Per-kind entries are deliberately thin. A context server entry is empty, `pub struct ContextServerManifestEntry {}` (extension_manifest.rs:363); the extension code, not the manifest, supplies the command at runtime. A slash command entry is `pub struct SlashCommandManifestEntry { pub description: String, pub requires_argument: bool }` (365-369). A debug adapter entry is `pub struct DebugAdapterManifestEntry { pub schema_path: Option<RelPathBuf> }` (371-374). A language model provider entry is `pub struct LanguageModelProviderManifestEntry { pub name: String, pub icon: Option<String> }` (379-387).

Extensions also declare what host powers they need, and the host checks at call time. `ExtensionManifest::allow_exec` fails with "capability for process:exec {desired_command} {desired_args:?} was not listed in the extension manifest" (extension_manifest.rs:164-183). The user-side counterpart is the `granted_extension_capabilities` setting, whose three kinds are `process:exec`, `download_file`, and `npm:install` (docs/src/extensions/capabilities.md:14-28, 43-100). "Restricting or removing a capability will cause an error to be returned when an extension attempts to call the corresponding extension API without sufficient capabilities." (capabilities.md:16).

There is a fossil in the manifest: `AgentServerManifestEntry` with `name`, `env`, `icon`, and per-target `archive`/`cmd`/`args`/`sha256` (extension_manifest.rs:231-269, 271-288). It is defined but not a field of `ExtensionManifest`, and the docs say "As of Zed `v1.5.0`, ACP extensions have been deprecated in favor of the ACP Registry" (docs/src/extensions/agent-servers.md:8). MCP extensions are headed the same way: "We plan to deprecate MCP server extensions in favor of the official MCP registry" (docs/src/extensions/mcp-extensions.md:8).

### The host-side `Extension` trait

Every manifest kind maps to async methods on the host trait (crates/extension/src/extension.rs:49-182). The agent-relevant ones:

```
async fn complete_slash_command_argument(&self, command: SlashCommand, arguments: Vec<String>) -> Result<Vec<SlashCommandArgumentCompletion>>;
async fn run_slash_command(&self, command: SlashCommand, arguments: Vec<String>, worktree: Option<Arc<dyn WorktreeDelegate>>) -> Result<SlashCommandOutput>;
async fn context_server_command(&self, context_server_id: Arc<str>, project: Arc<dyn ProjectDelegate>) -> Result<Command>;
async fn context_server_configuration(&self, context_server_id: Arc<str>, project: Arc<dyn ProjectDelegate>) -> Result<Option<ContextServerConfiguration>>;
async fn get_dap_binary(&self, dap_name: Arc<str>, config: DebugTaskDefinition, user_installed_path: Option<PathBuf>, worktree: Arc<dyn WorktreeDelegate>) -> Result<DebugAdapterBinary>;
```

The extension sees the host only through narrow delegates: `WorktreeDelegate { id, root_path, read_text_file, which, shell_env }` (extension.rs:32-39) and `ProjectDelegate { worktree_ids }` (41-43). Registration fans out through `ExtensionHostProxy`, one `RwLock<Option<Arc<dyn ...Proxy>>>` per kind: theme, grammar, language, language_server, snippet, context_server, debug_adapter_provider, language_model_provider (crates/extension/src/extension_host_proxy.rs:25-36). The context-server proxy is just `register_context_server(extension, server_id, cx)` / `unregister_context_server(server_id, cx)` (353-362). The LLM-provider proxy takes a boxed registration closure, `register_language_model_provider(provider_id, register_fn: LanguageModelProviderRegistration, cx)` (436-445), and on the receiving side `language_models::extension::LanguageModelProviderRegistryProxy` simply calls `register_fn(cx)` and unregisters by id from `LanguageModelRegistry` (crates/language_models/src/extension.rs:38-53). Built-in providers are hidden when an extension with a mapped id is installed: `anthropic`, `openai`, `google -> google-ai`, `openrouter`, `copilot_chat -> copilot-chat` (extension.rs:9-20). How a wasm extension actually implements a provider is not in the sources I read (no `language_model_provider` symbol in `crates/extension_host/src/extension_host.rs` or `wasm_host.rs`, and none in `crates/extension_api/src/extension_api.rs`).

### The context server (MCP) client surface

Zed's MCP client negotiates protocol version, records the server's advertised capabilities, and exposes a `capable()` check (crates/context_server/src/protocol.rs:86-105):

```
pub enum ServerCapability {
    Experimental,
    Logging,
    Prompts,
    Resources,
    Tools,
}
```

Zed itself advertises nothing to the server: `capabilities: types::ClientCapabilities { experimental: None, sampling: None, roots: None }` (protocol.rs:43-47). The docs state the consumed subset: "Zed currently supports MCP's Tools and Prompts features. We welcome contributions that help advance Zed's MCP feature coverage (Discovery, Sampling, Elicitation, etc)." (docs/src/ai/mcp.md:14-15). Resource content in tool results is dropped with a warning: `ToolResponseContent::Resource { .. } => { log::warn!("Ignoring resource content from tool response"); }` and likewise for `ResourceLink` (crates/agent/src/tools/context_server_registry.rs:450-455).

Servers reach the agent through a per-project `ContextServerRegistry` that keeps, per server, both tools and prompts and reloads them on status changes and on the `notifications/tools/list_changed` notification (context_server_registry.rs:42-48, 142-158, 260-279). Configuration comes from settings as one of three shapes, `Stdio { enabled, remote, command }`, `Http { enabled, url, headers, timeout, oauth }`, `Extension { enabled, ... }` (crates/project/src/project_settings.rs:187-217), resolved to `ContextServerConfiguration::{Custom, Extension, Http}` (crates/project/src/context_server_store.rs:160-176).

### The ACP agent-server surface

An external agent is anything implementing `AgentServer` (crates/agent_servers/src/agent_servers.rs:50-104): `logo()`, `agent_id()`, `connect(delegate, project, cx) -> Task<Result<Rc<dyn AgentConnection>>>`, plus optional per-agent default mode and config-option persistence. The native agent is just another implementation: `impl AgentServer for NativeAgentServer` whose `connect` builds `Templates::new()`, a `NativeAgent`, and wraps it as `Rc<dyn acp_thread::AgentConnection>` (crates/agent/src/native_agent_server.rs:23-54). So the same `AcpThread` UI hosts Zed's own agent and Claude/Codex/Gemini over the same trait.

`AgentConnection` is the capability-discovery surface (crates/acp_thread/src/connection.rs:91-260). Beyond `new_session`, `prompt`, `cancel`, and `authenticate`, every extra feature is an `Option<Rc<dyn ...>>` accessor that defaults to `None`: `client_user_message_ids`, `retry`, `request_elicitations`, `truncate`, `set_title`, `model_selector`, `telemetry`, `session_modes`, `session_config_options`, `session_list`, and the `supports_load_session` / `supports_resume_session` / `supports_close_session` / `supports_logout` booleans. The doc comment on `model_selector` states the pattern: "Returns this agent as an [Rc<dyn ModelSelector>] if the model selection capability is supported. If the agent does not support model selection, returns [None]." (connection.rs:227-232).

In the other direction, Zed-as-client tells the agent what it can do: `acp::ClientCapabilities::new().fs(FileSystemCapabilities::new().read_text_file(true).write_text_file(true)).terminal(true).auth(AuthCapabilities::new().terminal(true)).session(...config_options(...boolean(...))).elicitation(ElicitationCapabilities::new().form(...).url(...)).meta(meta)` (crates/agent_servers/src/acp.rs:777-795). The matching request handlers are `handle_request_permission`, `handle_write_text_file`, `handle_read_text_file`, `handle_create_terminal`, `handle_kill_terminal`, `handle_release_terminal`, `handle_terminal_output`, `handle_wait_for_terminal_exit`, `handle_create_elicitation`, and notifications `handle_session_notification`, `handle_complete_elicitation` (acp.rs:710-753).

### The agent skills mechanism

Skills live in a leaf crate with no `worktree` dependency (crates/agent_skills/agent_skills.rs:31-38). A skill is frontmatter plus a lazily read body: `pub struct SkillMetadata { pub name: String, pub description: String, #[serde(default, rename = "disable-model-invocation")] pub disable_model_invocation: bool }` (205-211). Three sources with a fixed precedence (95-109, 121-127):

```
pub enum SkillSource {
    BuiltIn,
    Global,
    ProjectLocal { worktree_id: SkillScopeId, worktree_root_name: Arc<str> },
}
...
pub fn precedence(&self) -> u8 { match self { Self::BuiltIn => 0, Self::Global => 1, Self::ProjectLocal { .. } => 2 } }
```

Limits are constants: `MAX_SKILL_FILE_SIZE: usize = 100 * 1024` and `MAX_SKILL_DESCRIPTIONS_SIZE: usize = 50 * 1024` (47-50). The catalog enters the system prompt as `<available_skills>` with `name`, `description`, `location` per skill, and the model is told to "Use the `skill` tool with the skill's name to get detailed instructions" (crates/agent/src/templates/system_prompt.hbs:220-247). The body is served through the same envelope whether the model or the user triggered the load: "Used by both model-driven activation (the `skill` tool) and user-driven activation (slash commands), so the model sees the same shape regardless of who initiated the load." (crates/agent/src/tools/skill_tool.rs:36-39).

## Candidates

Each candidate is a distinct kind of contribution to the agent that is not "a set of model-callable tools". Format per candidate: (a) description, (b) contribution kind, (c) lifecycle, (d) host services, (e) evidence, (f) wiring and placement.

### 1. Project instruction files (rules files)

(a) The first matching instruction file in each visible worktree root is read verbatim into the system prompt as "Project Rules".

(b) Prompt fragment, scoped per worktree, rendered in a fixed position after personal instructions so project text wins on conflict.

(c) Per project. Rebuilt whenever `project_context_needs_refresh` fires (project events, trust changes, prompt-store updates) and only pushed to the thread when the resulting `ProjectContext` differs, to preserve the provider's prompt cache (crates/agent/src/agent.rs:983-999). Torn down with `ProjectState` when the project is dropped.

(d) Filesystem via the project's buffer store (`project.open_buffer`), the worktree scan (`scan_complete().await`), no network, no secrets.

(e) `pub const RULES_FILE_NAMES: &[&str] = &[".rules", ".cursorrules", ".windsurfrules", ".clinerules", ".github/copilot-instructions.md", "AGENT.md", "AGENTS.md", "CLAUDE.md", "GEMINI.md"]` (crates/prompt_store/src/prompts.rs:22-32). `pub struct RulesFileContext { pub path_in_worktree: Arc<RelPath>, pub text: String, #[serde(skip)] pub project_entry_id: usize }` (prompts.rs:94-102). Loader picks the first present file: `RULES_FILE_REL_PATHS.iter().filter_map(|name| worktree.entry_for_path(name).filter(|entry| entry.is_file())...).next()` (agent.rs:1261-1269). Template: "### Project Rules ... These instructions are scoped to the current project. They take precedence over the personal `AGENTS.md` above when they conflict." (crates/agent/src/templates/system_prompt.hbs:264-277).

(f) `prompt_store::ProjectContext` / `WorktreeContext` (prompts.rs:34-92) is owned by `NativeAgent::ProjectState.project_context: Entity<ProjectContext>` (agent.rs:191-200) and handed to `Thread::new` (agent.rs:740-749). Placement rationale: the rules text is project state, not thread state, so one entity is shared by every thread on that project and by subagents (`Thread::new_subagent` clones `project_context`, thread.rs:1315). Trust gating for rules files is not in the sources (skills are gated, rules loading at agent.rs:1254-1298 has no trust check).

### 2. Personal AGENTS.md (user-global instructions)

(a) `~/.config/zed/AGENTS.md` is loaded into an app-wide global, watched for changes, and rendered above project rules.

(b) Prompt fragment, app-scoped.

(c) Per app. `init` installs a global with a watcher task; "replacing or removing the global cancels the watcher" (crates/agent_settings/src/user_agents_md.rs:53-58, 95-96).

(d) Filesystem watch (`settings::watch_config_file`), a notifier callback for read errors; no network.

(e) Module doc: "Loads `~/.config/zed/AGENTS.md` (or the platform equivalent) into an in-memory global, watches the file for changes, and surfaces read errors through a caller-supplied notifier ... Empty or whitespace-only files are treated as 'no user `AGENTS.md`'." (user_agents_md.rs:1-11). State enum `UserAgentsMdState { Empty, Loaded(SharedString), Error(SharedString) }` (24-33). Consumed at request-build time: `let user_agents_md = UserAgentsMd::global(cx).and_then(|s| s.content().cloned());` (crates/agent/src/thread.rs:4311). Test asserts ordering: "personal AGENTS.md should render before project rules so project rules can override it" (crates/agent/src/templates.rs:150-156).

(f) Lives in `agent_settings`, not `agent`, because it is settings-like config with the same watch/notify pattern as settings.json. Rules-library "default rules" were migrated into this file (docs/src/ai/rules.md:32-37).

### 3. Agent skills (catalog + on-demand loader + slash command)

(a) `SKILL.md` folders under `~/.agents/skills/` and `<worktree>/.agents/skills/` become a catalog in the system prompt, a `skill` tool that serves the body on demand, and `/name` slash commands.

(b) Three contributions at once: a prompt fragment (catalog of name/description/location), a model-callable loader tool, and user-invocable commands. The interesting part is that the catalog and the loader are kept in sync by a resolver closure evaluated at invocation time rather than a snapshot at thread build.

(c) Per project, live. Global and project skill directories are watched; a rescan sets `project_context_needs_refresh` for every project (agent.rs:700-708). Project skills only load from trusted worktrees and a trust-change subscription triggers refresh (agent.rs:887-901, 1045-1069). Catalog budget of 50KB enforced upstream in `select_catalog_skills` (agent.rs:3530).

(d) Filesystem (bounded concurrency `SKILL_IO_CONCURRENCY: usize = 16`, agent_skills.rs:44), worktree scan, trust store, project buffer store for reading `SKILL.md`.

(e) `Skill { name, description, source, directory_path, skill_file_path, load_warnings, disable_model_invocation, embedded_body: Option<&'static str> }` (agent_skills.rs:75-93). Registration: `thread.add_tool(SkillTool::with_body_resolver(skills_resolver_for_project(weak.clone(), project_id), skill_body_resolver_for_project(project.clone(), self.fs.clone())));` with the comment "The resolver closure reads `state.skills` at invocation time, so skills added or removed by the SKILL.md watcher after the thread is constructed are still visible to the model" (agent.rs:806-815). Resolver types: `pub type SkillsResolver = Arc<dyn Fn(&App) -> Arc<Vec<Skill>> + Send + Sync>; pub type SkillBodyResolver = Arc<dyn Fn(Skill, &mut AsyncApp) -> Task<Result<String>> + Send + Sync>;` (skill_tool.rs:116-118). Security: "XML-escape a string so a malicious skill author cannot break out of the `<skill_content>` envelope" (skill_tool.rs:13-16). Trust: "Project-local skills only load from trusted worktrees ... This prevents a malicious project from injecting instructions into your agent's system prompt before you've reviewed what the project ships." (docs/src/ai/skills.md:178-181). Permission: model-invoked skills go through the `skill` tool permission entry keyed by absolute `SKILL.md` path, user-invoked slash commands do not prompt (docs/src/ai/tool-permissions.md:57-62, 312-330). `ToolPermissionScope::AgentSkills` exists as a distinct scope (thread.rs:907-911).

(f) `agent_skills` is a leaf crate: "intentionally does not depend on `worktree`. Callers (e.g. the `agent` crate) construct these from `worktree::WorktreeId::to_usize()`" (agent_skills.rs:33-36). Discovery and budgeting sit in `agent.rs`; rendering sits in `prompt_store::ProjectContext::with_skills` (prompts.rs:72-76); the UI reads a published `SkillIndex` global (agent_skills.rs:182-188, agent.rs:1438-1480). Placement rationale: the catalog is project context (shared, cached), the loader is a tool (per thread), the index is UI state (global).

### 4. MCP prompts as slash commands

(a) Every running context server's `prompts/list` becomes an ACP `AvailableCommand`, pushed to all sessions on that project, with name collisions resolved by server-prefixing.

(b) User-invocable command surface (prompt template injection on demand), not a tool.

(c) Per project, re-pushed whenever `ContextServerRegistryEvent::PromptsChanged` fires or skills change (agent.rs:1415-1435, 1006-1011). Removed when the server stops (context_server_registry.rs:266-279).

(d) The MCP client (stdio or HTTP), the server's `Prompts` capability, no filesystem.

(e) `pub struct ContextServerPrompt { pub server_id: ContextServerId, pub prompt: context_server::types::Prompt }` and `pub enum ContextServerRegistryEvent { ToolsChanged, PromptsChanged }` (context_server_registry.rs:24-32). Only loaded if `client.capable(context_server::protocol::ServerCapability::Prompts)` (217-219). Command construction sets `CommandCategory::Mcp` and maps a single prompt argument to an unstructured input hint; "skip >1 argument commands since we don't support them yet" (agent.rs:1527-1560). Collision rule: "Returns the set of MCP prompt names that must be server-qualified (`/<server>.<name>`) ... A built-in always wins an unqualified invocation" (agent.rs:172-177). `get_prompt` calls `PromptsGet` with arguments (context_server_registry.rs:513-544).

(f) Delivered over the same ACP `SessionUpdate::AvailableCommandsUpdate` channel that external agents use (agent.rs:1490-1497), so the UI's slash popup is agent-agnostic. `CommandCategory { Native, Mcp }` rides in ACP `meta` (crates/acp_thread/src/acp_thread.rs:86-113).

### 5. MCP context server lifecycle, transport, and auth

(a) A configured server (stdio command, HTTP URL with headers/OAuth, or extension-provided command) is started per project, its status tracked, its OAuth challenge surfaced, and its tools/prompts re-fetched on `list_changed`.

(b) Transport plus a lifecycle-state provider (`Starting`, `Authenticating`, `Running`, `Stopped`, `Error`, `AuthRequired`, `ClientSecretRequired`).

(c) Per project (`project.read(cx).context_server_store()`, agent.rs:872). The registry subscribes to store status events and drops a server's tools and prompts when it leaves `Running` (context_server_registry.rs:252-282).

(d) Process spawn (stdio), HTTP client, OAuth flow (crates/context_server/src/oauth.rs, 2551 lines), settings, optional remote execution (`remote: bool` on stdio configs, project_settings.rs:192-194).

(e) `ContextServerStatus::Starting | ContextServerStatus::Authenticating => {}` / `Running => { reload_tools ... reload_prompts }` / `Stopped | Error(_) | AuthRequired | ClientSecretRequired { .. } => { remove }` (context_server_registry.rs:260-279). Notification handling: `client.on_notification("notifications/tools/list_changed", ...)` guarded by `capable(ServerCapability::Tools)` (142-158). Post-initialize auth challenge: "Servers may accept `initialize` unauthenticated and only challenge a later request or notification. Awaiting this is what lets the owner of the connection notice such a challenge" (protocol.rs:131-134). Version pinning: "Per MCP 2025-06-18, HTTP transport must attach the negotiated version as `MCP-Protocol-Version` on every post-initialize request." (protocol.rs:64-67).

(f) `crates/context_server` is protocol only; `project::context_server_store` owns lifecycle; `agent::ContextServerRegistry` adapts to agent tools/prompts. Servers are also forwarded wholesale to external agents (candidate 11). The `Extension` variant carries a `settings: serde_json::Value` (context_server_store.rs:165-169) so an extension's `context_server_configuration` can drive a setup modal (docs/src/ai/mcp.md:82-84).

### 6. Agent profiles (tool availability set + MCP presets + default model)

(a) A named profile decides which built-in tools and which MCP tools a thread may see, and optionally which model becomes default when the profile is selected.

(b) Configuration gate over the tool set (not a permission gate), plus model selection. Profiles filter what the model is offered; they do not decide allow/deny.

(c) Per thread (`Thread.profile_id`, thread.rs:1274), persisted in the thread row (`DbThread.profile: Option<AgentProfileId>`, crates/agent/src/db.rs:68-69). Read from settings on every `enabled_tools` call so setting changes apply on the next turn.

(d) Settings store only.

(e) `pub struct AgentProfileSettings { pub name: SharedString, pub tools: IndexMap<Arc<str>, bool>, pub enable_all_context_servers: bool, pub context_servers: IndexMap<Arc<str>, ContextServerPreset>, pub default_model: Option<LanguageModelSelection> }` (crates/agent_settings/src/agent_profile.rs:102-112). Built-ins `write`, `ask`, `minimal` (16-26). Filter: `if tool.supports_provider(&model.provider_id()) && profile.is_tool_enabled(profile_tool_name)` and for MCP `if profile.is_context_server_tool_enabled(&server_id.0, &tool_name)` (thread.rs:4158-4159, 4183). Docs: "Profiles do not decide whether a tool call is allowed automatically. Use Tool Permissions to control allow, deny, and confirm behavior." (docs/src/ai/agent-profiles.md:10). The `tools!` macro comment lists three silent gates a new tool must pass, the first being the profile allowlist in `assets/settings/default.json` (crates/agent/src/tools.rs:182-196).

(f) Profile data is in `agent_settings`; the filter is `Thread::enabled_tools` (thread.rs:4125-4176). The terminal tool is a special case: two registered variants (`TerminalTool`, `SandboxedTerminalTool`) are exposed under one profile name, "Expose the one matching the current sandbox state to the model under that name" (thread.rs:4132-4134, 4161-4165).

### 7. Tool permission engine (settings-driven approval with hardcoded floor)

(a) Every permission-gated tool call is classified Allow / Deny / Confirm by regex rules over the tool's input, with a precedence order and non-overridable security rules, and the confirm prompt offers "always" options that write back to settings.

(b) Permission gate as a reusable service handed to tools through the event stream, not embedded in each tool.

(c) Per tool call, but the pending prompt watches `SettingsStore` so an "Always for" decision on one call resolves sibling calls in the same turn or in subagents (thread.rs:5738-5745).

(d) Settings store, shell-command parser (`shell_command_parser::extract_commands`), UI prompt.

(e) `pub enum ToolPermissionDecision { Allow, Deny(String), Confirm }` with precedence "1. Hardcoded security rules ... 2. `always_deny` ... 3. `always_confirm` ... 4. `always_allow` ... 5. Tool-specific `default` ... 6. Global `default`" (crates/agent/src/tool_permissions.rs:207-231). `HARDCODED_SECURITY_DENIAL_MESSAGE: "Blocked by built-in security rule. This operation is considered too harmful to be allowed, and cannot be overridden by settings."` (11-12). Substitution ban: "terminal does not allow shell substitutions or interpolations in permission-protected commands. Forbidden examples include $VAR, ${VAR}, $(...), backticks..." (13-17). Three entry points on the event stream: `authorize` (settings-driven), `authorize_always_prompt` ("for example, symlink-escape confirmations or edits that target sensitive settings files"), `authorize_third_party_tool` for MCP keyed by `mcp:<server_id>:<tool_name>` (thread.rs:5684-5787; context_server_registry.rs:17-22). Option shapes: `PermissionOptions { Flat(...), Dropdown(...), DropdownWithPatterns { choices, patterns, tool_name } }` (crates/acp_thread/src/connection.rs:580-588). Two prompt semantics: `AuthorizationKind { PermissionGrant, ActionChoice }`, the latter "for example, 'Save' vs 'Discard' before editing a dirty buffer" (acp_thread.rs:1247-1261).

(f) Decision logic in `agent::tool_permissions`, rule data in `agent_settings::ToolPermissions`, the prompt loop on `ToolCallEventStream` (thread.rs:5484). Placement rationale: tools stay ignorant of policy; they hand `ToolPermissionContext { tool_name, input_values, scope }` (thread.rs:900-904) to the stream and await. External ACP agents get the same UI through `handle_request_permission -> thread.request_tool_call_authorization(tool_call, PermissionOptions::Flat(args.options), AuthorizationKind::PermissionGrant, cx)` (crates/agent_servers/src/acp.rs:4596-4605).

### 8. OS sandbox for terminal and fetch (policy + grants + prompt section)

(a) Agent-run terminal commands are wrapped in Seatbelt / Bubblewrap / WSL-Bubblewrap with a per-thread allowlist of writable paths and hosts; the model can request escalation per call; the user grants once, for the thread, or always; the system prompt describes the live rules.

(b) Execution confinement device, plus per-thread grant state, plus a conditional prompt fragment. This is the clearest example in Zed of one contribution touching three layers at once.

(c) Per thread for grants ("Never persisted - lives and dies with this thread" for the in-memory `sandbox_grants`, thread.rs:1297-1302, though `DbThread.sandbox_grants: DbSandboxGrants` is persisted "so reopening a thread keeps its grants", db.rs:84-89), per app for `agent.sandbox_permissions`, per call for the wrap.

(d) OS sandbox primitives, an in-process HTTP proxy for host allowlists, a per-thread temp dir, git metadata discovery from the project's git store, feature flag.

(e) `pub enum ThreadSandbox { Unsandboxed, Sandboxed(SandboxPolicy) }` with the rationale "'No sandbox' is its own variant rather than a maximally-permissive [`SandboxPolicy`] so that a wide-open but real sandbox ... stays distinguishable from running with no sandbox at all" (crates/agent/src/sandboxing.rs:86-100). `pub struct SandboxWrap { pub writable_paths: Vec<PathBuf>, pub extra_write_paths: Vec<settings::GrantedWritePath>, pub network: SandboxNetworkAccess, pub protected_paths: Vec<PathBuf>, pub allow_fs_write: bool, pub is_local: bool, pub wsl_zed_release: Option<(String, String)> }` (crates/acp_thread/src/terminal.rs:35-71), with the trust note "Pass the project's worktree paths ... here - *not* the command's working directory, which is model-controlled and would let the model widen its own writable scope." (36-39). Grant lifetimes: `SandboxPermission { AllowOnce, AllowThread, AllowAlways, Deny }` (acp_thread.rs:136-141). Prompt: `sandboxing: bool` on `SystemPromptTemplate` renders "## Terminal sandbox" only when the terminal tool is available (crates/agent/src/templates.rs:46-52; system_prompt.hbs:156-212). Policy doc: "enabled iff the user has the `sandboxing` feature flag turned on, the project is local, the platform has an integration, and the user has not persistently allowed unsandboxed execution" (sandboxing.rs:8-11). Docs: "Sandboxing applies only to Zed Agent. It does not sandbox Zed itself, language servers, extensions, tasks, your normal terminal tabs, External Agents, or Terminal Threads." (docs/src/ai/sandboxing.md:23-24).

(f) Glue in `agent::sandboxing`, policy types in the `sandbox` crate, wrap struct in `acp_thread::terminal`, escalation prompt via `ToolCallEventStream::authorize_sandbox` (thread.rs:5789-5801). The per-thread `$TMPDIR` is injected by `NativeThreadEnvironment::create_terminal` and added to the writable scope (agent.rs:3191-3246).

### 9. Worktree trust and restricted mode

(a) Untrusted worktrees put the project in a restricted mode that hides `fetch` and `terminal`, downgrades the profile to `minimal`, and excludes project-local skills.

(b) Policy gate above profiles and permissions, driven by editor state rather than agent settings.

(c) Per project, reactive: `TrustedWorktreesEvent { Trusted(...), Restricted(...) }` (crates/project/src/trusted_worktrees.rs:227-230) triggers a context refresh (agent.rs:893-901).

(d) A global `TrustedWorktrees` store backed by the app DB, keyed by remote host (`RemoteHostLocation { user_name, host_identifier }`, trusted_worktrees.rs:153-157).

(e) `fn allow_in_restricted_mode() -> bool { true }` on `AgentTool` with doc "Tools that return `false` are never exposed to the model while the workspace is restricted, and will fail if invoked in that state." (thread.rs:5127-5134). Test: `fetch_and_terminal_are_forbidden_in_restricted_mode` and "Unknown tools (e.g. MCP tools) are considered allowed." (tools.rs:150-160, 249-263). Filter in `enabled_tools`: `.filter(|(_, tool)| !is_restricted || tool.allow_in_restricted_mode())` (thread.rs:4143-4146). Thread field `profile_downgraded_for_restricted_workspace: bool` (thread.rs:1275-1277).

(f) Trust lives in `project`, not `agent`, because language servers and tasks use the same signal. Placement rationale: a capability that is dangerous in untrusted code should opt out at the trait level (a const-like method), not in each call site.

### 10. Thread environment: terminals, subagents, sibling threads

(a) Tools that need to spawn things receive an `Rc<dyn ThreadEnvironment>` at registration; it can create sandboxed terminals, nested subagents, independent sibling threads, and list available agents/models.

(b) Host device injection. The environment is the one object that crosses from the agent crate into the UI/workspace layer, and it is what makes `TerminalTool`, `SpawnAgentTool`, `CreateThreadTool`, and `ListAgentsAndModelsTool` possible without those tools knowing about GPUI windows.

(c) Per thread; constructed in `register_session` with weak handles to the `AcpThread`, `Thread`, and `NativeAgent` (agent.rs:797-804). Subagent depth capped by `MAX_SUBAGENT_DEPTH` (thread.rs:2185).

(d) Terminal creation with PTY or headless mode, project environment lookup (`directory_environment`), the app's agent registry, git worktree creation for siblings.

(e) Trait (thread.rs:756-801):

```
pub trait ThreadEnvironment {
    fn create_terminal(&self, command: String, extra_env: Vec<acp::EnvVariable>, cwd: Option<PathBuf>, output_byte_limit: Option<u64>, sandbox_wrap: Option<acp_thread::SandboxWrap>, cx: &mut AsyncApp) -> Task<Result<Rc<dyn TerminalHandle>>>;
    fn create_subagent(&self, label: String, cx: &mut App) -> Result<Rc<dyn SubagentHandle>>;
    fn resume_subagent(...) -> Result<Rc<dyn SubagentHandle>> { Err(...) }
    fn create_sibling_thread(&self, request: SiblingThreadRequest, cx: &mut AsyncApp) -> Task<Result<SiblingThreadInfo>> { ... }
    fn list_available_agents(&self, cx: &mut App) -> Result<AvailableAgents> { ... }
}
```

`TerminalHandle { id, current_output, wait_for_exit, kill, was_stopped_by_user }` (738-744); `SubagentHandle { id, num_entries, send }` (746-754). Headless: "Headless hosts (e.g. the eval CLI) have no controlling TTY, so PTY setup fails with `ENOTTY`. Run the command non-interactively and without a PTY in that case." (acp_thread.rs:4419-4422); the eval CLI sets `cx.set_global(acp_thread::HeadlessTerminal(true))` (crates/eval_cli/src/headless.rs:120-123).

(f) Trait in `agent::thread`, production impl `NativeThreadEnvironment` in `agent.rs:3181`, terminal entity in `acp_thread::terminal`. Placement rationale: defaults on optional methods (`resume_subagent`, `create_sibling_thread`, `list_available_agents`) let test and headless environments implement only `create_terminal` and `create_subagent`.

### 11. ACP client services offered to external agents (fs, terminal, permission, elicitation, MCP forwarding)

(a) When Zed hosts an external ACP agent it acts as the agent's client: it answers file reads and writes through the project's buffers (so unsaved edits are visible), runs terminals, shows permission prompts, renders elicitations, and passes its configured MCP servers into every new/load/resume session request.

(b) A bundle of host services exposed over a protocol boundary rather than as in-process trait objects. Notably, MCP servers become a contribution *to another agent*.

(c) Per connection (`AcpConnection`), per session for the thread-bound handlers; MCP list is computed at session creation (`mcp_servers_for_project(&project, cx)` at acp.rs:1612, 1743, 1787).

(d) Project buffer store, action log, terminal, settings for proxy env (`load_proxy_env`, agent_servers.rs:112-135), the MCP configuration.

(e) Handler list and capabilities quoted in section 1 (acp.rs:710-753, 777-795). File read goes through `project.open_buffer` and the action log: `let path = project.project_path_for_absolute_path(&path, cx).ok_or_else(|| acp::Error::resource_not_found(...))?; Ok::<_, acp::Error>(project.open_buffer(path, cx))` (acp_thread.rs:4227-4234). MCP forwarding maps `Custom`/`Extension` stdio configs to `acp::McpServer::Stdio` when `is_local || *remote` and `Http` configs to `acp::McpServer::Http` with headers (acp.rs:4397-4443). Elicitation validation: URL mode "must use HTTP or HTTPS and include a host"; other modes rejected as "unsupported elicitation mode" (acp_thread.rs:443-460). Docs boundary table: "Zed MCP servers | May be forwarded over ACP", "Zed Skills | Do not apply as Zed Skills", "Zed Agent profiles | Do not apply unless the integration says otherwise" (docs/src/ai/external-agents.md:127-136).

(f) `agent_servers::acp` owns the wire handlers; `acp_thread::AcpThread` owns the editor-facing implementations (`read_text_file`, `write_text_file`, `create_terminal`, `request_tool_call_authorization`, `update_plan`). Placement rationale: the native agent and external agents share `AcpThread`, so a file read has identical semantics (unsaved buffer contents, action-log tracking) regardless of which agent asked.

### 12. Optional session capabilities on `AgentConnection` (modes, config options, model selector, session list, history)

(a) An agent advertises extra per-session features by returning `Some(Rc<dyn Trait>)` from an accessor; the UI adapts (mode selector, config toggles, model picker, thread history import).

(b) Capability discovery pattern for non-tool features. Each is a small trait: `AgentSessionModes { current_mode, all_modes, set_mode }`, `AgentSessionConfigOptions { config_options, set_config_option, watch }`, `AgentModelSelector { list_models, select_model, selected_model, favorite_model_ids, toggle_favorite_model, watch, should_render_footer }`, `AgentSessionList { list_sessions, supports_delete, delete_session, delete_sessions, watch, notify_refresh }` (connection.rs:303-329, 387-413, 447-493).

(c) Per session (`session_id` parameter) or per connection (`session_list`). `watch()` returns an optional receiver for agents whose lists change dynamically.

(d) None from the host beyond the connection; the native agent implements them against `LanguageModelRegistry` (agent.rs:219-289) and `ThreadsDatabase` (db.rs:564-606).

(e) `fn session_modes(&self, _session_id: &acp::SessionId, _cx: &App) -> Option<Rc<dyn AgentSessionModes>> { None }` and siblings (connection.rs:239-257). `fn supports_session_history(&self) -> bool { self.supports_load_session() || self.supports_resume_session() }` (157-160). `AgentSessionInfo { session_id, work_dirs, title, updated_at, created_at, meta }` (355-363). Thread import from external agents: "Zed connects to each selected agent over ACP and adds sessions that are not already in your history." (docs/src/ai/external-agents.md:192).

(f) All in `acp_thread::connection`, the smallest common layer between UI and any agent. Placement rationale: the UI compiles against the trait, agents opt in one feature at a time, no manifest field needed.

### 13. Plans and elicitations (structured agent-to-user surfaces)

(a) An agent can publish a plan (checklist with `Pending / InProgress / Completed` entries) and can ask the user structured questions (form) or send them to a URL (OAuth-style) outside the tool-call flow.

(b) UI contribution channels driven by the agent, distinct from tool calls and from permission prompts.

(c) Plan is per thread (`AcpThread::update_plan(&mut self, request: acp::Plan, cx)`, acp_thread.rs:3577). Elicitations are per thread when session-scoped, per connection when request-scoped: "Request-scoped elicitations are connection-level because they can arrive before a session thread exists." (connection.rs:204-206).

(d) None beyond UI.

(e) `pub struct Plan { pub entries: Vec<PlanEntry> }` and `PlanStats { in_progress_entry, pending, completed }` (acp_thread.rs:1952-1962). `pub enum ElicitationStatus { Pending { respond_tx: oneshot::Sender<acp::CreateElicitationResponse> }, Accepted, Declined, Canceled, Completed }` and `ElicitationStore { elicitations: Vec<Elicitation> }` (acp_thread.rs:413-434). Native agent parity: `ThreadEvent::Elicitation(ElicitationRequest)` (thread.rs:883) and a built-in `AskUserTool` (tools.rs:199).

(f) `acp_thread` holds both because they are ACP schema types (`acp::Plan`, `acp::CreateElicitationRequest`) rendered by the shared thread view. Placement rationale: anything in the ACP schema is implemented once for all agents.

### 14. Context mentions (user-side context providers)

(a) The message editor lets the user attach typed context by `@`-mention: files, directories, symbols, past threads, diagnostics, selections, fetched URLs, terminal selections, git diffs, merge conflicts, skills, pasted images.

(b) Context provider catalog on the input side. Each variant is a URI scheme that the thread can re-resolve on load.

(c) Per message; serialized into the thread (`MentionUri` derives `Serialize, Deserialize`).

(d) Project buffers, LSP symbols, diagnostics store, git store, terminal, HTTP fetch, thread DB, skill index.

(e) (crates/acp_thread/src/mention.rs:19-77):

```
pub enum MentionUri {
    File { abs_path: PathBuf },
    PastedImage { name: String },
    Directory { abs_path: PathBuf },
    Symbol { abs_path: PathBuf, name: String, line_range: RangeInclusive<u32> },
    Thread { id: acp::SessionId, name: String },
    Rule { id: serde_json::Value, name: String },   // deprecated, kept for old threads
    Diagnostics { include_errors: bool, include_warnings: bool },
    Selection { abs_path: Option<PathBuf>, line_range: RangeInclusive<u32>, column: Option<u32> },
    Fetch { url: Url },
    TerminalSelection { line_count: u32 },
    GitDiff { base_ref: String },
    MergeConflict { file_path: String },
    Skill { name: String, source: String, skill_file_path: PathBuf },
}
```

Prompt capabilities gate what the input accepts: `acp::PromptCapabilities::new().image(image).embedded_context(true)` where `image` depends on `model.supports_images()` (thread.rs:1306-1311), and the receiver is handed to `AcpThread::new` (agent.rs:773-783).

(f) `MentionUri` in `acp_thread` (shared), the completion menu in `agent_ui::completion_provider` (3132 lines, not read in detail). Placement rationale: the set of context kinds is a closed enum, not a plugin surface; adding one is a code change in three crates.

### 15. Action log (edit tracking, review, stale-read detection)

(a) Every buffer the agent reads or edits is tracked so the UI can show a review diff, the user can accept/reject, and the agent is told when a file changed underneath it.

(b) Cross-tool state provider. Tools do not own their edits; they report to the log, which the review UI and the next request read.

(c) Per thread, with subagents linking to the parent's log: "Useful in cases like subagents, where we want to track individual diffs for this subagent, but also want to associate the reads/writes with a parent review experience" (crates/action_log/src/action_log.rs:57-60; `Thread::new_subagent` at thread.rs:1320-1321).

(d) Project buffers, file mtimes.

(e) `pub struct ActionLog { tracked_buffers: BTreeMap<Entity<Buffer>, TrackedBuffer>, project: Entity<Project>, linked_action_log: Option<Entity<ActionLog>>, last_reject_undo: Option<LastRejectUndo>, file_read_times: HashMap<PathBuf, MTime> }` (action_log.rs:51-65). Tools receive it at construction: `DeletePathTool::new(self.project.clone(), self.action_log.clone())`, `EditFileTool::new(self.project.clone(), cx.weak_entity(), self.action_log.clone(), language_registry.clone())` (thread.rs:2133-2142). External agents' file writes go through the same log in `AcpThread::read_text_file` (acp_thread.rs:4224, 4250).

(f) Separate `action_log` crate consumed by `agent`, `acp_thread`, and `agent_ui`. Placement rationale: review is an editor concern, so the log is neither a tool nor part of the LLM request; it is a side channel every mutating tool must write to.

### 16. Thread persistence and summaries

(a) Threads are saved to a local SQLite-backed store on every observed change, with metadata for listing/grouping, and reloaded (including draft prompt, scroll position, model, profile, and sandbox grants) when reopened. A separate summarization model produces titles and summaries.

(b) Persistence and history provider, plus a secondary model role.

(c) Per thread, debounced through `Session.pending_save: Task<Result<()>>` (agent.rs:209) and triggered by `cx.observe(&thread_handle, move |this, thread, cx| this.save_thread(thread, cx))` (agent.rs:820-822). Per app for the database.

(d) App database, clock (`updated_at`), a second `LanguageModel` (`registry.thread_summary_model(cx)`, agent.rs:791-797).

(e) `pub struct DbThreadMetadata { pub id: acp::SessionId, pub parent_session_id: Option<acp::SessionId>, pub title: SharedString, pub updated_at: DateTime<Utc>, pub created_at: Option<DateTime<Utc>>, pub folder_paths: PathList }` (crates/agent/src/db.rs:29-38). `DbThread` fields include `messages`, `detailed_summary`, `initial_project_snapshot`, `cumulative_token_usage`, `request_token_usage`, `model`, `profile`, `subagent_context`, `speed`, `thinking_enabled`, `thinking_effort`, `draft_prompt`, `ui_scroll_position`, `sandboxed_terminal_temp_dir`, `sandbox_grants` (db.rs:53-89). `ThreadStore { load_thread, save_thread, delete_thread, delete_threads }` (crates/agent/src/thread_store.rs:12-90). Summarization prompts are text assets in `crates/agent_settings/src/prompts/` (`compaction_prompt.txt`, `summarize_thread_prompt.txt`, `summarize_thread_detailed_prompt.txt`).

(f) `agent::db` + `agent::thread_store`, surfaced to the UI through the generic `AgentSessionList` trait (candidate 12), so native and external histories share one sidebar. Placement rationale: the ACP session id is the primary key for both, which is what makes thread import from external agents possible.

### 17. Language model providers and routing (including extension-provided providers)

(a) Models come from registered providers; each provider owns auth, settings UI, default/fast/recommended models, and can be supplied by an extension which then hides the equivalent built-in.

(b) Model client provider with per-role routing (default model, fast model, summary model, subagent model override).

(c) Per app for the registry; per thread for the selected `ThreadModel { Ready(Arc<dyn LanguageModel>), Unresolved(SelectedModel), Unset }` (thread.rs:1212-1216). Subagents can be forced onto a different model: `if let Some(subagent_model) = AgentSettings::get_global(cx).subagent_model.clone() { thread.inherits_parent_model_settings = false; thread.apply_model_selection(&subagent_model, cx); }` (thread.rs:1336-1339).

(d) HTTP client, credential store (`set_api_key`), settings UI hooks.

(e) Trait (crates/language_model/src/language_model.rs:344-396): `fn id(&self) -> LanguageModelProviderId; fn name(&self) -> LanguageModelProviderName; fn icon(&self) -> IconOrSvg; fn default_model(&self, cx) -> Option<Arc<dyn LanguageModel>>; fn default_fast_model(...); fn provided_models(...); fn recommended_models(...); fn is_authenticated(...); fn authenticate(...) -> Task<Result<(), AuthenticateError>>; fn settings_view(...) -> Option<ProviderSettingsView>; fn set_api_key(...)`. Extension hook: manifest `language_model_providers` (extension_manifest.rs:121-122) and proxy `register_language_model_provider(provider_id, register_fn, cx)` (extension_host_proxy.rs:436-445). Model-conditional tools: `fn supports_provider(_provider: &LanguageModelProviderId) -> bool { true }` with doc "Some tools rely on a provider for the underlying billing or other reasons." (thread.rs:5122-5126); `search_web` is Zed-provider-only (docs/src/ai/tools.md:64).

(f) `language_model` (traits, registry) vs `language_models` (concrete providers, extension proxy). Placement rationale: the agent depends only on the trait crate; provider auth UI stays in the provider.

### 18. Prompt templates with filesystem overrides

(a) System and edit prompts are Handlebars templates compiled into the binary, and the prompt store watches an overrides directory so a user can replace any template at runtime.

(b) Prompt fragment source with an override mechanism; the template engine is itself a contribution point (helpers like `contains`).

(c) Per app. Overrides directory is watched; on removal "Restoring built-in prompt templates." (crates/prompt_store/src/prompts.rs:318-321).

(d) Filesystem watch, embedded assets.

(e) Agent templates: `#[derive(RustEmbed)] #[folder = "src/templates"] #[include = "*.hbs"] struct Assets;` and `handlebars.set_strict_mode(true); handlebars.register_helper("contains", Box::new(contains)); handlebars.register_embed_templates::<Assets>()` (crates/agent/src/templates.rs:8-21). Override watcher doc: "This function sets up a file watcher on the prompt templates directory. It performs an initial scan of the directory and registers any existing template overrides. Then it continuously monitors for changes, reloading templates as they are modified or added." (prompts.rs:223-229); path from `paths::prompt_overrides_dir(params.repo_path.as_deref())` (244). Template files present: `system_prompt.hbs`, `experimental_system_prompt.hbs`, `edit_file_prompt_xml.hbs`, `edit_file_prompt_diff_fenced.hbs`, `create_file_prompt.hbs`, `diff_judge.hbs` (crates/agent/src/templates/).

(f) Two engines: `agent::Templates` for the agent's own prompts, `prompt_store::PromptBuilder` for inline-assist/terminal-assist prompts with overrides. Whether the agent's `system_prompt.hbs` is overridable through the same directory is not in the sources (the `Templates` struct registers only embedded assets).

### 19. Extension-contributed debug adapters and slash commands (agent-adjacent)

(a) Extensions register debug adapters and locators into the global `DapRegistry`, and can define slash commands with argument completion. Neither is consumed by the native agent thread today, but both are contribution kinds the extension host already routes.

(b) Registry contributions (debugger) and command contributions (slash commands).

(c) Per app, on extension install/uninstall (`register_debug_adapter` / `unregister_debug_adapter`, crates/debug_adapter_extension/src/debug_adapter_extension.rs:32-65).

(d) Extension host (wasm), `DapRegistry`, worktree delegate for binary lookup.

(e) `pub fn init(extension_host_proxy: Arc<ExtensionHostProxy>, cx: &mut App) { let language_server_registry_proxy = DebugAdapterRegistryProxy::new(cx); extension_host_proxy.register_debug_adapter_proxy(language_server_registry_proxy); }` (debug_adapter_extension.rs:14-17). Slash command trait methods quoted in section 1 (extension.rs:120-131). A debugger-facing agent tool is not in the sources: the built-in tool list (tools.rs:197-222) has no debug tool, and `crates/debugger_tools` contains only `dap_log.rs` (a DAP log viewer). Agent consumption of extension slash commands is not in the sources: the native agent's available commands are only `/compact` plus MCP prompts plus skills (agent.rs:1502-1564).

(f) Both go through `ExtensionHostProxy`; the agent does not subscribe to either. Listed because they show the extension host is already a general registry, so a future agent-visible kind would be one more proxy trait.

### 20. Eval harness (host mode, not a runtime contribution)

(a) A headless CLI boots the same crates without a window, forces non-PTY terminals, and runs tool evals against fixtures with pass/fail processors.

(b) Alternate host environment; interesting because it shows which services the agent actually needs to run (fs, http client, node runtime, language registry, prompt store, settings, no UI).

(c) Per process.

(d) `RealFs`, `ReqwestClient`, `Client::production`, `AppDatabase`, `NodeRuntime`, `LanguageRegistry`, `prompt_store::init`, `terminal_view::init` (crates/eval_cli/src/headless.rs:63-118).

(e) `pub trait EvalOutputProcessor { type Metadata: 'static + Send; fn process(&mut self, output: &EvalOutput<Self::Metadata>); fn assert(&mut self); }` and `OutcomeKind { Passed, Failed, Error }` (crates/eval_utils/src/eval_utils.rs:23-34). In-crate evals gated by feature: `#[cfg(all(test, feature = "unit-eval"))] mod evals;` (tools.rs:11-12) with fixtures under `crates/agent/src/tools/evals/fixtures/`.

(f) `eval_cli` composes the app; `eval_utils` is the assertion harness. Placement rationale: the agent crate never depends on the window system, which is what makes a headless host possible.

## Zed design lessons

Zed never treats "the tool set" as the unit of contribution. The unit is the `Thread`, and a thread is assembled from at least six independent inputs that arrive through different channels and have different lifetimes: a `ProjectContext` entity (rules text, worktree list, skill catalog, shared by every thread on the project and diffed before publishing so the system prompt stays byte-identical when nothing changed, agent.rs:983-999), a `ContextServerRegistry` entity (tools and prompts, per project), a profile id (per thread, from settings), a `ThreadEnvironment` (per thread, injected at `add_default_tools`), an `ActionLog` (per thread, linked for subagents), and the sandbox grant cell (per thread, in-memory plus persisted). Tools are then registered *against* those inputs: `EditFileTool::new(project, weak_thread, action_log, language_registry)` (thread.rs:2137-2142). For PromptForge this argues that `Contribution` should grow fields for prompt fragments and for shared context objects before it grows anything about tools, and that `RunServices` should be the place those shared objects live, because in Zed the equivalent of `create(&RunServices)` is `Thread::new(project, project_context, context_server_registry, templates, default_model, cx)` plus `add_default_tools(environment, cx)`.

Prompt fragments in Zed are typed, positioned, and owned, never free-form appends. The system template has fixed slots (`user_agents_md`, `worktrees[].rules_file`, `skills`, `sandboxing`, `available_tools`) and each slot has one producer (templates.rs:36-61). The order is asserted in tests ("personal AGENTS.md should render before project rules so project rules can override it", templates.rs:150-156), and conditional sections are gated on both the feature state and the tool being present ("the prompt must not describe a sandboxed `terminal` tool the model doesn't have", templates.rs:318-321). The skills catalog sends only name/description/location and defers the body to a tool call, which is progressive disclosure at the contribution level. A PromptForge `Contribution.prompt_fragments` should probably be a map from named slot to text, with the executor owning slot order, rather than a `Vec<String>` the executor concatenates. Confidence: high, based on the explicit ordering tests and the cache-preserving diff.

Permissions are a service handed to the tool, not a property of the tool. The `AgentTool` trait exposes only two policy hooks, `supports_provider` and `allow_in_restricted_mode` (thread.rs:5122-5134); everything else about approval comes from `ToolCallEventStream::authorize*` which the tool awaits (thread.rs:5684-5801). The decision engine lives in `agent::tool_permissions` with a hardcoded floor that settings cannot lower, MCP tools are keyed by a synthetic id (`mcp:<server>:<tool>`) so the same engine covers third-party tools, and pending prompts subscribe to settings so one "always" answer resolves all sibling prompts. The sandbox adds a second, orthogonal gate with its own grant lifetimes (`AllowOnce`, `AllowThread`, `AllowAlways`). The lesson for `Contribution` is that a capability should be able to contribute *policy inputs* (a tool id, an input extractor, a restricted-mode flag, a set of sandbox paths) while the host owns the approval loop; a capability that carried its own approval UI would break the sibling-resolution behavior.

Optional capabilities are discovered by returning `Option<Rc<dyn Trait>>`, not by manifest flags. `AgentConnection` has eleven such accessors that default to `None` (connection.rs:187-257), and the UI simply does not render a mode selector or model picker when the accessor returns `None`. The same pattern appears on `ThreadEnvironment` (default-erroring optional methods) and on `ContextServerRegistry` (capability checks before each `prompts/list` or `tools/list`). This is a cheaper alternative to PromptForge's `conflicts()` declaration for many cases: instead of declaring in advance, a contribution exposes what it has and the host probes. Where Zed does use declarations (the extension manifest), the entries are almost empty (`ContextServerManifestEntry {}`) and exist to gate *host powers* (`process:exec`, `download_file`, `npm:install`), not to describe the contribution.

Trust and project scope are first-class inputs, not afterthoughts. Project-local skills are excluded until the worktree is trusted, restricted mode strips `fetch` and `terminal` regardless of profile, and the sandbox refuses to make git metadata writable under any grant. The two kinds of scope also differ in lifetime: project-scoped inputs (rules, skills, MCP servers) are shared and refreshed reactively, thread-scoped inputs (profile, grants, action log) are persisted in the thread row so a reopened thread resumes with the same policy. A `Contribution` in PromptForge that produced a mount or a prompt fragment would need to say which of those two lifetimes it has, because the caching and persistence behavior differ.

Finally, MCP shows that a contribution can be a *transport* whose payload is decided later. Zed activates a context server per project, then lazily discovers tools and prompts, re-fetches on `list_changed`, and forwards the raw server configuration to external agents so they can connect themselves (acp.rs:4397-4443). Resources, sampling, and elicitation from the MCP side are simply not consumed yet (protocol.rs:43-47, context_server_registry.rs:450-455). The `Contribution` struct's deferred "mounts, prompt fragments, Lua surface" would map onto Zed as: mounts are the worktree list plus sandbox writable paths; prompt fragments are the template slots; there is no Lua-like scripting surface in the agent (not in the sources), the nearest analogue being MCP prompts as slash commands and skills as instruction files.

## Gaps

Things I looked for and did not find in the sources read:

- A debugger-facing agent tool or DAP integration in the native agent. `debug_adapter_extension` registers adapters for the debugger UI; `debugger_tools` is a DAP log viewer; the built-in tool list (tools.rs:197-222) has no debug tool.
- MCP resources, sampling, roots, or elicitation consumed by the native agent. `ServerCapability::Resources` exists (protocol.rs:91) but is never checked in `context_server_registry.rs`; client capabilities are all `None` (protocol.rs:43-47).
- Extension-provided slash commands reaching the native agent thread. The trait methods exist (extension.rs:120-131) but `build_available_commands_for_project` (agent.rs:1502-1564) emits only `/compact` and MCP prompts, and skills are surfaced separately.
- How a wasm extension implements a language model provider. The manifest entry and host proxy exist; no `language_model_provider` symbol appears in `extension_host.rs`, `wasm_host.rs`, or `extension_api.rs`.
- Extension-provided agent servers. `AgentServerManifestEntry` is defined (extension_manifest.rs:231-269) but is not a field of `ExtensionManifest`, and the docs mark ACP extensions deprecated (agent-servers.md:8).
- Trust gating for rules files. Skills are gated on `TrustedWorktrees::can_trust` (agent.rs:1062-1069); `load_worktree_rules_file` (agent.rs:1254-1298) has no such check.
- Whether the agent's own `system_prompt.hbs` is user-overridable. `agent::Templates` registers only embedded assets (templates.rs:15-23); the override watcher belongs to `prompt_store::PromptBuilder`, which serves inline-assist and terminal-assist prompts.
- A generic "context provider" plugin surface. `MentionUri` is a closed enum (mention.rs:19-77); adding a mention kind is a code change.
- Edit prediction context as an agent contribution. `edit_prediction_context::RelatedExcerptStore` (crates/edit_prediction_context/src/edit_prediction_context.rs:40-46) serves edit prediction, not the agent thread; nothing in `agent` imports it.
- A Lua or other embedded scripting surface for the agent. Not in the sources.
- Remote/SSH-specific agent contributions beyond three flags: `remote: bool` on stdio MCP configs (project_settings.rs:192-194), `is_local || *remote` in MCP forwarding (acp.rs:4415), `SandboxWrap.is_local` (terminal.rs:60-63), and `RemoteHostLocation` keying in the trust store (trusted_worktrees.rs:153-157).
- Explicit co-activation conflict declarations between contributions. Zed resolves collisions at merge time instead: duplicate MCP tool names are prefixed with the snake_cased server id (thread.rs:4194-4205), duplicate MCP prompt names are server-qualified (agent.rs:172-189), same-named skills resolve by `SkillSource::precedence` (agent_skills.rs:111-127).

*2026-09-19 10:05 - claude-fable-5.1*
