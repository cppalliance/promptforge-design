---
produced: 2026-09-19
title: agent runtime field survey - non-tool extension kinds in MCP, Claude Code, OpenAI Agents SDK, LangGraph, Pydantic AI, Google ADK, Letta, Claude Agent SDK
---

# Agent runtime field survey: what a capability can contribute besides tools

This file records, per system, the extension kinds that are not model-callable tools, using each system's own documentation as the source. Every quoted definition carries the URL it was taken from. All pages were fetched on 2026-09-19. Quotes are verbatim except that em dashes and double dashes in source text have been normalized to a single dash per this workspace's formatting rule. Where a page could not be fetched, that is stated in the Gaps section and nothing was invented for it. For each kind the entry gives: (a) a one-sentence description, (b) a verbatim definition quote with URL, (c) lifecycle (when it attaches), (d) what it needs from the host, (e) what it hands the run.

One framing note before the catalog. Two of the surveyed systems have independently converged on the exact abstraction PromptForge is designing. Pydantic AI now has a first-class `Capability` type that "can provide any combination of" tools, lifecycle hooks, instructions, model settings, and models, and calls it "the primary extension point." Claude Code's plugin is a bundle of skills, agents, hooks, MCP servers, LSP servers, monitors, channels, themes, and output styles. Both are catalogued below because they are the closest existing answers to the question "what else can an activation unit contribute."

## Model Context Protocol

Source: the current protocol revision is `2026-07-28` per https://modelcontextprotocol.io/specification/versioning ("The current protocol version is 2026-07-28."). The per-primitive pages fetched were the `2025-06-18` revision because the `2026-07-28` sub-pages under `/basic/deprecated` returned 404. The `2026-07-28` overview page was fetched and differs in two important ways noted under Sampling and Roots below.

The `2026-07-28` overview lists server features as "Resources: Context and data, for the user or the AI model to use", "Prompts: Templated messages and workflows for users", "Tools: Functions for the AI model to execute", and client features as only "Elicitation: Server-initiated requests for additional information from users" (https://modelcontextprotocol.io/specification/2026-07-28). The `2025-06-18` overview additionally listed client features "Sampling: Server-initiated agentic behaviors and recursive LLM interactions" and "Roots: Server-initiated inquiries into uri or filesystem boundaries to operate in" (https://modelcontextprotocol.io/specification/2025-06-18). The `2026-07-28` overview also adds an Extensions section: "Tasks: Asynchronous execution of long-running operations, with polling, mid-flight input, and durable handles", "Skills over MCP: Rich, structured instructions for agent workflows, discovered and consumed through MCP", "MCP Apps: Interactive UI elements (charts, forms, video players) rendered inline within conversations" (https://modelcontextprotocol.io/specification/2026-07-28). The base protocol also moved from "Stateful connections" and "Server and client capability negotiation" (2025-06-18) to "Stateless, self-contained requests" and "Per-request capability negotiation" (2026-07-28).

### Resources and resource templates

(a) A server exposes URI-addressed data (text or binary) that the host may put into model context, with optional parameterized URI templates and change subscriptions.

(b) "Resources allow servers to share data that provides context to language models, such as files, database schemas, or application-specific information. Each resource is uniquely identified by a URI." and "Resources in MCP are designed to be application-driven, with host applications determining how to incorporate context based on their needs." and "Resource templates allow servers to expose parameterized resources using URI templates. Arguments may be auto-completed through the completion API." Capability flags: "`subscribe`: whether the client can subscribe to be notified of changes to individual resources. `listChanged`: whether the server will emit notifications when the list of available resources changes." Annotations: "`audience`: An array indicating the intended audience(s) for this resource. Valid values are `"user"` and `"assistant"`." and "`priority`: A number from 0.0 to 1.0 indicating the importance of this resource." (https://modelcontextprotocol.io/specification/2025-06-18/server/resources)

(c) Lifecycle: declared per connection at capability negotiation; listed and read per request; subscriptions live for the connection.

(d) Needs from host: a transport, a URI namespace, optionally a filesystem or data backend, a notification channel back to the client.

(e) Hands the run: a mount-like namespace of readable content plus a change-notification stream; the host decides whether and when content enters the prompt.

### Prompts

(a) A server publishes named, argument-taking message templates that a user (not the model) selects, typically as slash commands.

(b) "Prompts allow servers to provide structured messages and instructions for interacting with language models. Clients can discover available prompts, retrieve their contents, and provide arguments to customize them." and "Prompts are designed to be user-controlled, meaning they are exposed from servers to clients with the intention of the user being able to explicitly select them for use." A prompt definition includes "`name`: Unique identifier for the prompt", "`arguments`: Optional list of arguments for customization"; messages carry "`role`: Either "user" or "assistant"" and content that may be text, image, audio, or "Embedded resources allow referencing server-side resources directly in messages" (https://modelcontextprotocol.io/specification/2025-06-18/server/prompts)

(c) Lifecycle: listed per connection, instantiated per request when a user invokes one.

(d) Needs from host: a user-facing invocation surface (command palette, slash menu), argument collection UI.

(e) Hands the run: a fully formed message sequence (prompt text plus embedded resources) injected at the user's chosen moment.

### Completions

(a) A server offers argument autocompletion for prompt arguments and resource-template URI parameters.

(b) "The Model Context Protocol (MCP) provides a standardized way for servers to offer argument autocompletion suggestions for prompts and resource URIs. This enables rich, IDE-like experiences where users receive contextual suggestions while entering argument values." Reference types: "`ref/prompt` References a prompt by name" and "`ref/resource` References a resource URI". (https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/completion)

(c) Lifecycle: per keystroke, before a prompt or resource request is committed.

(d) Needs from host: an interactive text-entry UI that can debounce and render suggestions.

(e) Hands the run: nothing directly; it improves the argument values that feed prompts and resource reads.

### Logging

(a) A server streams structured, severity-leveled log notifications to the client, which controls the minimum level.

(b) "The Model Context Protocol (MCP) provides a standardized way for servers to send structured log messages to clients. Clients can control logging verbosity by setting minimum log levels, with servers sending notifications containing severity levels, optional logger names, and arbitrary JSON-serializable data." Levels follow "the standard syslog severity levels specified in RFC 5424" (debug through emergency). Clients "MAY send a `logging/setLevel` request"; servers "send log messages using `notifications/message` notifications". (https://modelcontextprotocol.io/specification/2025-06-18/server/utilities/logging)

(c) Lifecycle: for the life of the connection; level is set per connection.

(d) Needs from host: a sink for notifications, a level-setting control, optional persistence.

(e) Hands the run: an observability stream, not model-visible content.

### Sampling (client feature; absent from the 2026-07-28 client feature list)

(a) A server asks the client to run an LLM completion on its behalf, with model preferences instead of model names, so servers need no API keys and the human stays in the loop.

(b) "The Model Context Protocol (MCP) provides a standardized way for servers to request LLM sampling ("completions" or "generations") from language models via clients. This flow allows clients to maintain control over model access, selection, and permissions while enabling servers to leverage AI capabilities - with no server API keys necessary." and "there SHOULD always be a human in the loop with the ability to deny sampling requests." Model preferences: "`costPriority`", "`speedPriority`", "`intelligencePriority`" plus "hints" that "are advisory - clients make final model selection". (https://modelcontextprotocol.io/specification/2025-06-18/client/sampling). The 2026-07-28 overview no longer lists Sampling under client features (https://modelcontextprotocol.io/specification/2026-07-28).

(c) Lifecycle: per request, nested inside another server operation.

(d) Needs from host: model access, a user approval UI, rate limiting.

(e) Hands the run: a model-call channel granted to a capability, gated by user consent.

### Elicitation (client feature; the only client feature retained in 2026-07-28)

(a) A server pauses to ask the user for structured input against a flat JSON schema; the user can accept, decline, or cancel.

(b) "The Model Context Protocol (MCP) provides a standardized way for servers to request additional information from users through the client during interactions. This flow allows clients to maintain control over user interactions and data sharing while enabling servers to gather necessary information dynamically. Servers request structured data from users with JSON schemas to validate responses." Schema limits: "elicitation schemas are limited to flat objects with primitive properties only". Response actions: "Accept (`action: "accept"`): User explicitly approved and submitted with data", "Decline (`action: "decline"`): User explicitly declined the request", "Cancel (`action: "cancel"`): User dismissed without making an explicit choice". Constraint: "Servers MUST NOT use elicitation to request sensitive information." (https://modelcontextprotocol.io/specification/2025-06-18/client/elicitation)

(c) Lifecycle: per request, nested inside a tool call or other server operation.

(d) Needs from host: user interaction (a form renderer), schema validation, a way to attribute the request to the requesting server.

(e) Hands the run: a human-in-the-loop wait that returns structured data or a refusal.

### Roots (client feature; absent from the 2026-07-28 client feature list)

(a) The client tells servers which filesystem directories they may operate in, and notifies on change.

(b) "Roots define the boundaries of where servers can operate within the filesystem, allowing them to understand which directories and files they have access to. Servers can request the list of roots from supporting clients and receive notifications when that list changes." A root's "`uri`: Unique identifier for the root. This MUST be a `file://` URI in the current specification." (https://modelcontextprotocol.io/specification/2025-06-18/client/roots). Not listed under client features in the 2026-07-28 overview (https://modelcontextprotocol.io/specification/2026-07-28).

(c) Lifecycle: per connection; list-changed notifications during the session.

(d) Needs from host: a workspace model, path validation, user consent.

(e) Hands the run: a filesystem scope policy (boundary), not content.

### Notifications and subscriptions (cross-cutting)

(a) Servers and clients push unsolicited change events: resource list changed, resource updated, prompt list changed, roots list changed, log messages.

(b) "When the list of available resources changes, servers that declared the `listChanged` capability SHOULD send a notification: `notifications/resources/list_changed`" and "Clients can subscribe to specific resources and receive notifications when they change" via `resources/subscribe` and `notifications/resources/updated` (https://modelcontextprotocol.io/specification/2025-06-18/server/resources). "When roots change, clients that support `listChanged` MUST send a notification: `notifications/roots/list_changed`" (https://modelcontextprotocol.io/specification/2025-06-18/client/roots).

(c) Lifecycle: for the life of the connection.

(d) Needs from host: a bidirectional transport and an event loop that can re-list or re-read on notification.

(e) Hands the run: invalidation signals that keep injected context fresh.

### Extensions in 2026-07-28: Tasks, Skills over MCP, MCP Apps

(a) Opt-in extensions layered over the core protocol for long-running asynchronous operations, structured instruction bundles, and inline UI.

(b) "Beyond the core protocol, MCP defines optional extensions that add modular, specialized, or experimental functionality. Extensions are always opt-in and require explicit support from both client and server, negotiated during initialization." Listed: "Tasks: Asynchronous execution of long-running operations, with polling, mid-flight input, and durable handles", "Skills over MCP: Rich, structured instructions for agent workflows, discovered and consumed through MCP", "MCP Apps: Interactive UI elements (charts, forms, video players) rendered inline within conversations". (https://modelcontextprotocol.io/specification/2026-07-28)

(c) Lifecycle: negotiated per connection (or per request under the stateless model); Tasks have durable handles that outlive a single request.

(d) Needs from host: durable storage for task handles, a polling loop, a UI surface for Apps, an instruction loader for Skills.

(e) Hands the run: a durable job handle, prompt-fragment bundles, and rendered UI. The individual extension pages were not fetched; only the overview text is quoted.

## Claude Code

Sources: https://code.claude.com/docs/en/hooks , https://code.claude.com/docs/en/skills , https://code.claude.com/docs/en/plugins-reference , https://code.claude.com/docs/en/memory , https://code.claude.com/docs/en/sub-agents , https://code.claude.com/docs/en/output-styles , https://code.claude.com/docs/en/permissions . All fetched 2026-09-19.

### Hooks (lifecycle events with five handler types)

(a) User-registered handlers that fire at named lifecycle points, receive JSON about the event, and can observe, inject context, or block.

(b) "Hooks are user-defined shell commands, HTTP endpoints, MCP tool calls, LLM prompts, or subagents that execute automatically at specific points in Claude Code's lifecycle." Cadences: "per session: `SessionStart` and `SessionEnd`", "per turn: `UserPromptSubmit`, `Stop`, and `StopFailure`", "on every tool call inside the agentic loop: `PreToolUse` and `PostToolUse`". The full event table as fetched: `SessionStart`, `Setup`, `UserPromptSubmit`, `UserPromptExpansion`, `PreToolUse`, `PermissionRequest`, `PermissionDenied`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `Notification`, `MessageDisplay`, `SubagentStart`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `Stop`, `StopFailure`, `TeammateIdle`, `InstructionsLoaded`, `ConfigChange`, `CwdChanged`, `DirectoryAdded`, `FileChanged`, `WorktreeCreate`, `WorktreeRemove`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `Elicitation`, `ElicitationResult`, `SessionEnd`. Handler types: "Command hooks (`type: "command"`)", "HTTP hooks (`type: "http"`)", "MCP tool hooks (`type: "mcp_tool"`)", "Prompt hooks (`type: "prompt"`): send a prompt to a Claude model for single-turn evaluation", "Agent hooks (`type: "agent"`): spawn a subagent that can use tools like Read, Grep, and Glob to verify conditions before returning a decision." Context injection: "The `additionalContext` field passes a string from your hook into Claude's context window. Claude Code wraps the string in a system reminder and inserts it into the conversation at the point where the hook fired." Decision control on `PreToolUse`: "`permissionDecision` (allow/deny/ask/defer)". Exit code 2 on `PreToolUse` "Blocks the tool call"; on `Stop` "Prevents Claude from stopping, continues the conversation"; on `PreCompact` "Blocks compaction"; on `WorktreeCreate` the hook "prints path on stdout" and "Replaces default git behavior". (https://code.claude.com/docs/en/hooks)

(c) Lifecycle: registered per session from settings files, skill frontmatter, or agent frontmatter; skill-declared hooks have a `once` option: "If `true`, Claude Code removes the hook after its first successful run."

(d) Needs from host: process spawning (command), network (http), an MCP connection (mcp_tool), model access (prompt, agent), a clock for timeouts, a JSON stdin/stdout contract.

(e) Hands the run: a gate (allow/deny/ask/defer), prompt text (`additionalContext`), a display transform (`MessageDisplay`), a worktree path, and observability.

### Skills (SKILL.md)

(a) A directory with a `SKILL.md` whose body is instructions loaded into context on demand, with frontmatter controlling who may invoke it, which tools are pre-approved, model and effort overrides, whether it forks into a subagent, and dynamic shell-injected context.

(b) "Skills extend what Claude can do. Create a `SKILL.md` file with instructions, and Claude adds it to its toolkit. Claude uses skills when relevant, or you can invoke one directly with `/skill-name`." and "Unlike CLAUDE.md content, a skill's body loads only when it's used, so long reference material costs almost nothing until you need it." Frontmatter fields include `disable-model-invocation`, `user-invocable`, `allowed-tools` ("Tools Claude can use without asking permission during the turn that invokes this skill. The grant clears when you send your next message."), `disallowed-tools` ("Tools removed from Claude's available pool while this skill is active."), `model` ("Model to use when this skill is active. The override applies for the rest of the current turn"), `effort`, `context` ("Set to `fork` to run in a forked subagent context"), `agent`, `background`, `hooks` ("Hooks that Claude Code registers when the skill is invoked and keeps running for the rest of the session"), `paths` ("Glob patterns that limit when this skill is activated"), `shell`. Dynamic context: "The `` !` `` syntax runs shell commands before the skill content is sent to Claude. The command output replaces the placeholder, so Claude receives actual data, not the command itself." Content lifecycle: "When you or Claude invoke a skill, the rendered `SKILL.md` content enters the conversation as a single message and stays there across later turns." Compaction: "Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens." (https://code.claude.com/docs/en/skills)

(c) Lifecycle: description indexed per session; body loaded per invocation and persists across turns; permission grant is per turn; hooks registered by a skill persist for the session.

(d) Needs from host: a filesystem to discover `SKILL.md`, a shell for `!` injection, the permission system, the subagent spawner.

(e) Hands the run: prompt text, a temporary permission policy, a model/effort override, optionally a subagent delegation, and hooks.

### Subagents

(a) A markdown-defined agent with its own system prompt, tool allowlist, model, permission mode, MCP servers, hooks, persistent memory, and optional worktree isolation, run in a separate context window and returning only a summary.

(b) "Each subagent runs in its own context window with a custom system prompt, specific tool access, and independent permissions. When Claude encounters a task that matches a subagent's description, it delegates to that subagent, which works independently and returns results." Frontmatter fields: `tools`, `disallowedTools`, `model`, `permissionMode` ("`default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan`"), `maxTurns`, `skills` ("Skills to preload into the subagent's context at startup. The full skill content is injected, not only the description."), `mcpServers`, `hooks` ("Lifecycle hooks scoped to this subagent"), `memory` ("Persistent memory scope: `user`, `project`, or `local`. Enables cross-session learning"), `background`, `omitClaudeMd`, `effort`, `isolation` ("Set to `worktree` to run the subagent in a temporary git worktree"), `initialPrompt`. (https://code.claude.com/docs/en/sub-agents)

(c) Lifecycle: definition loaded per session; instance spawned per delegation; `memory` directory persists across sessions.

(d) Needs from host: model access, a second context window, the permission system, git for worktree isolation, a persistent directory for memory.

(e) Hands the run: a delegation target with a bounded policy, and a summary result.

### Plugins (the bundle)

(a) A self-contained directory that ships several component kinds at once, installed at user, project, or local scope.

(b) "A plugin is a self-contained directory of components that extends Claude Code with custom functionality. Plugin components include skills, agents, hooks, MCP servers, LSP servers, and monitors." Also "Plugins can also ship output styles in an `output-styles/` directory" (https://code.claude.com/docs/en/output-styles) and themes: "Plugins can ship color themes that appear in `/theme`". Persistent data: "The `${CLAUDE_PLUGIN_DATA}` directory resolves to `~/.claude/plugins/data/{id}/`" and "the data directory outlives any single plugin version". (https://code.claude.com/docs/en/plugins-reference)

(c) Lifecycle: installed once; enabled per scope; components activate per session.

(d) Needs from host: a plugin cache, a per-plugin persistent data directory, dependency installation (Node.js), scope resolution.

(e) Hands the run: every component kind below at once.

### LSP servers (plugin component)

(a) A plugin declares a language server so Claude gets live code intelligence.

(b) "Plugins can provide Language Server Protocol (LSP) servers to give Claude real-time code intelligence while working on your codebase." Configured via "`.lsp.json` in plugin root, or inline in `plugin.json`" mapping a language to `command`, `args`, and `extensionToLanguage`. (https://code.claude.com/docs/en/plugins-reference)

(c) Lifecycle: process started per session when the plugin is active.

(d) Needs from host: process spawning, file-extension routing, a JSON-RPC transport.

(e) Hands the run: a background service that enriches tool results (diagnostics, symbols), not a model-callable tool.

### Monitors (plugin component)

(a) A plugin declares a long-lived shell process whose stdout lines are delivered to Claude as notifications.

(b) "Plugins can declare background monitors that Claude Code starts automatically when the plugin is active. Each monitor runs a shell command for the lifetime of the session and delivers every stdout line to Claude as a notification, so Claude can react to log entries, status changes, or polled events without being asked to start the watch itself." Start control: "`when` Controls when the monitor starts. `"always"` starts it at session start and on plugin reload, and is the default. `"on-skill-invoke: "` starts it the first time the named skill in this plugin is dispatched". (https://code.claude.com/docs/en/plugins-reference)

(c) Lifecycle: per session (or from first skill invocation) until session end; "If you disable a plugin mid-session, Claude Code doesn't stop monitors that are already running".

(d) Needs from host: process spawning, a notification queue into the conversation, a task panel.

(e) Hands the run: an inbound event stream (a transport into the conversation).

### Channels (plugin component)

(a) A plugin binds an MCP server to a message channel that injects content into the conversation, with per-channel user configuration such as bot tokens.

(b) "The `channels` field lets a plugin declare one or more message channels that inject content into the conversation. Each channel binds to an MCP server that the plugin provides." and "The `server` field is required and must match a key in the plugin's `mcpServers`. The optional per-channel `userConfig` uses the same schema as the top-level field, letting the plugin prompt for bot tokens or owner IDs when the plugin is enabled." (https://code.claude.com/docs/en/plugins-reference)

(c) Lifecycle: per session while the plugin is enabled; user config collected at enable time.

(d) Needs from host: an MCP connection, secret storage for sensitive config, a way to inject inbound messages.

(e) Hands the run: an external transport (Telegram, etc.) that feeds the conversation.

### Memory files (CLAUDE.md, .claude/rules, auto memory)

(a) Persistent instruction files loaded at session start (or lazily by path glob), plus notes Claude writes for itself across sessions.

(b) "CLAUDE.md files are markdown files that give Claude persistent instructions for a project, your personal workflow, or your entire organization. You write these files in plain text; Claude reads them at the start of every session." Rules: "Rules can also be scoped to specific file paths, so they only load into context when Claude works with matching files" and "Rules without `paths` frontmatter are loaded at launch with the same priority as `.claude/CLAUDE.md`." Auto memory: "Auto memory lets Claude accumulate knowledge across sessions without you writing anything." with note types "`user`", "`feedback`", "`project`", "`reference`"; loaded "Every session (first 200 lines or 25KB)". Both are "context, not enforced configuration. To block an action regardless of what Claude decides, use a PreToolUse hook instead." Scopes: managed policy, user, project, local. (https://code.claude.com/docs/en/memory)

(c) Lifecycle: per session at start; path-scoped rules lazily per matching file; auto memory persists per repository.

(d) Needs from host: filesystem discovery in load order, a git-derived project identity, a persistent memory directory.

(e) Hands the run: prompt text, positioned as "a user message after the system prompt" (https://code.claude.com/docs/en/output-styles).

### Permission modes and rules

(a) A tiered policy layer deciding which tool calls run automatically, prompt, or are denied, expressed as modes plus allow/ask/deny rules, extended by hooks.

(b) Modes as fetched: "`default` Prompts for permission on first use of each tool", "`acceptEdits` Automatically accepts file edits and common filesystem commands", "`plan` Claude reads files and runs read-only shell commands to explore but doesn't edit your source files", "`auto` Auto-approves tool calls with background safety checks that verify actions align with your request", "`dontAsk` Auto-denies every call that would otherwise prompt", "`bypassPermissions` Skips permission prompts, except for the actions no mode auto-approves". Hook interplay: "PreToolUse hooks run before the permission prompt" and "Hook decisions don't bypass permission rules. Claude Code evaluates deny and ask rules regardless of what a PreToolUse hook returns". (https://code.claude.com/docs/en/permissions)

(c) Lifecycle: mode set per session and switchable mid-session; rules persisted per repository in `settings.local.json`; skill `allowed-tools` grants are per turn.

(d) Needs from host: a rule matcher, a prompt UI, a classifier model for `auto`, settings persistence.

(e) Hands the run: a policy (gate) applied to every tool call.

### Output styles

(a) A markdown file that replaces or augments Claude Code's default system-prompt instructions to change role, tone, and format for every response.

(b) "Output styles change how Claude responds, not what Claude knows. They set Claude's role, tone, and output format for every response." and "An output style changes the instructions Claude Code gives Claude." with "Custom output styles leave out Claude Code's built-in software engineering instructions ... unless `keep-coding-instructions` is set to `true`." Plugin override: "`force-for-plugin` Plugin output styles only: apply this style automatically whenever the plugin is enabled, without requiring users to select it." (https://code.claude.com/docs/en/output-styles)

(c) Lifecycle: per session (read at startup), switchable; applies to the main conversation and forks, not other subagents.

(d) Needs from host: settings storage for the selection, system-prompt assembly.

(e) Hands the run: system-prompt text (replacement, not append).

## OpenAI Agents SDK (Python)

Sources: https://openai.github.io/openai-agents-python/agents/ , https://openai.github.io/openai-agents-python/guardrails/ , https://openai.github.io/openai-agents-python/handoffs/ , https://openai.github.io/openai-agents-python/sessions/ , https://openai.github.io/openai-agents-python/tracing/ , https://openai.github.io/openai-agents-python/tools/ . Fetched 2026-09-19.

### Guardrails (input, output, tool)

(a) Validation functions attached to an agent or a tool that can raise a tripwire to halt the run, run in parallel or blocking mode.

(b) "Guardrails enable you to do checks and validations of user input and agent output." Kinds: "Input guardrails run on the initial user input", "Output guardrails run on the final agent output", and "Tool guardrails wrap `FunctionTool` instances and let you validate or block calls to those tools before and after execution." Placement: "Input guardrails run only for the first agent in the chain. Output guardrails run only for the agent that produces the final output." Execution modes: "Parallel execution (default, `run_in_parallel=True`): The guardrail runs concurrently with the agent's execution." and "Blocking execution (`run_in_parallel=False`): The guardrail runs and completes before the agent starts." Tripwire: "The runner immediately raises an `InputGuardrailTripwireTriggered` or `OutputGuardrailTripwireTriggered` exception and halts agent execution." Tool guardrail outcomes: "Input tool guardrails run before the tool executes and can skip the call, replace the output with a message, or raise a tripwire." (https://openai.github.io/openai-agents-python/guardrails/)

(c) Lifecycle: per agent (colocated on the `Agent`), evaluated per run (input/output) or per tool call (tool guardrails).

(d) Needs from host: optionally model access (guardrails commonly run a cheaper agent), the session store (for persistence rules on tripwire), a cancellation path.

(e) Hands the run: a gate with a halt signal, plus content replacement/redaction.

### Handoffs

(a) A delegation primitive where one agent transfers the conversation to another, exposed to the model as a tool, with input filters over the history the receiver sees.

(b) "Handoffs allow an agent to delegate tasks to another agent." and "Handoffs are represented as tools to the LLM. So if there's a handoff to an agent named `Refund Agent`, the tool would be named `transfer_to_refund_agent`." Customization: "`on_handoff`: A callback function executed when the handoff is invoked", "`input_filter`: This lets you filter the input received by the next agent", "`is_enabled`: Whether the handoff is enabled. This can be a boolean or a function". History semantics: "When a handoff occurs, it's as though the new agent takes over the conversation, and gets to see the entire previous conversation history." (https://openai.github.io/openai-agents-python/handoffs/)

(c) Lifecycle: declared per agent; invoked per run when the model selects it; "Handoffs stay within a single run."

(d) Needs from host: the run loop, history transformation, tracing.

(e) Hands the run: control transfer to another agent plus a filtered transcript.

### Sessions (conversation memory)

(a) A pluggable store that persists conversation items across runs so callers do not thread `to_input_list()` manually.

(b) "The Agents SDK provides built-in session memory to automatically maintain conversation history across multiple agent runs, eliminating the need to manually handle `.to_input_list()` between turns." and "Sessions stores conversation history for a specific session, allowing agents to maintain context without requiring explicit manual memory management." Example backend: `SQLiteSession("conversation_123")`. Exclusivity: "In the same run, a session cannot be combined with the run-level continuation options `conversation_id`, `previous_response_id`, or `auto_previous_response_id`." (https://openai.github.io/openai-agents-python/sessions/)

(c) Lifecycle: per session id, across runs.

(d) Needs from host: storage (SQLite or other), a session id.

(e) Hands the run: a store handle that the runner reads before and writes after each run.

### Lifecycle hooks (RunHooks, AgentHooks)

(a) Observer callbacks at agent, LLM, tool, and handoff boundaries, scoped to a whole run or to one agent.

(b) "There are two hook scopes: `RunHooks` observe the entire `Runner.run(...)` invocation, including handoffs to other agents. `AgentHooks` are attached to a specific agent instance via `agent.hooks`." Events: "`on_agent_start` ... `on_agent_end`", "`on_llm_start` / `on_llm_end`: immediately around each model call", "`on_tool_start` / `on_tool_end`: around each local tool invocation", "`on_handoff`: when control moves from one agent to another." (https://openai.github.io/openai-agents-python/agents/)

(c) Lifecycle: per run (RunHooks) or per agent (AgentHooks).

(d) Needs from host: the run context wrapper (carries shared usage state).

(e) Hands the run: observability and side effects (pre-fetching, usage recording); not a gate.

### Dynamic instructions and prompt templates

(a) The system prompt may be a function of run context, or a reference to a platform-hosted prompt template with variables.

(b) "`instructions` System prompt or dynamic instructions callback." and "you can also provide dynamic instructions via a function. The function will receive the agent and context, and must return the prompt." Templates: "You can reference a prompt template created in the OpenAI platform by setting `prompt`." with `id`, `version`, `variables`, or "generate the prompt dynamically at run time". (https://openai.github.io/openai-agents-python/agents/)

(c) Lifecycle: evaluated per model request.

(d) Needs from host: the run context object; network access to the platform for hosted templates.

(e) Hands the run: prompt text.

### Context (dependency injection)

(a) A caller-supplied object passed to every agent, tool, handoff, and hook as a grab bag of dependencies and state.

(b) "Context is a dependency-injection tool: it's an object you create and pass to `Runner.run()`, that is passed to every agent, tool, handoff etc, and it serves as a grab bag of dependencies and state for the agent run. You can provide any Python object as the context." (https://openai.github.io/openai-agents-python/agents/)

(c) Lifecycle: per run.

(d) Needs from host: nothing; the host supplies it.

(e) Hands the run: typed service handles (the analogue of `RunServices`).

### Tracing processors

(a) Built-in span collection for generations, tools, handoffs, guardrails, with pluggable processors that add or replace export destinations.

(b) "The Agents SDK includes built-in tracing, collecting a comprehensive record of events during an agent run: LLM generations, tool calls, handoffs, guardrails, and even custom events that occur." Extension points: "`add_trace_processor()` lets you add an additional trace processor that will receive traces and spans as they are ready." and "`set_trace_processors()` lets you replace the default processors with your own trace processors." Privacy: "you can disable capturing that data via `RunConfig.trace_include_sensitive_data`." (https://openai.github.io/openai-agents-python/tracing/)

(c) Lifecycle: per process (global `TraceProvider`), spans per run.

(d) Needs from host: a clock, network for export, background flushing.

(e) Hands the run: observability; no model-visible effect.

### Model settings and tool-use behavior

(a) Per-agent tuning of the model call and of how tool results terminate or continue the loop.

(b) "`model_settings` Model tuning parameters such as `temperature`, `top_p`, and `tool_choice`." and "The `tool_use_behavior` parameter in the `Agent` configuration controls how tool outputs are handled" with values "`run_llm_again`", "`stop_on_first_tool`", "`StopAtTools(stop_at_tool_names=[...])`", and "`ToolsToFinalOutputFunction`: A custom function that processes tool results and decides whether to end the run with a final output or continue processing with the LLM." (https://openai.github.io/openai-agents-python/agents/)

(c) Lifecycle: per agent, applied per model request.

(d) Needs from host: the model adapter.

(e) Hands the run: a policy over the loop's termination and the model's sampling parameters.

### Hosted and built-in execution tools (as capability kinds, not function tools)

(a) Provider-executed abilities and local execution surfaces that bypass the function-tool pipeline entirely.

(b) The tools page groups "Hosted tools" ("web search, file search, code interpreter, hosted MCP, image generation") and "Local runtime tools" including `ComputerTool`. The guardrails page states: "Hosted tools (`WebSearchTool`, `FileSearchTool`, `HostedMCPTool`, `CodeInterpreterTool`, `ImageGenerationTool`) and built-in execution tools (`ComputerTool`, `ShellTool`, `ApplyPatchTool`, `LocalShellTool`) do not use this guardrail pipeline". The tools page also documents "Hosted container shell + skills" and "Programmatic Tool Calling". (https://openai.github.io/openai-agents-python/tools/ and https://openai.github.io/openai-agents-python/guardrails/)

(c) Lifecycle: per agent declaration; execution per model turn on the provider side or in a local runtime.

(d) Needs from host: provider account features (hosted) or a local shell/computer surface.

(e) Hands the run: an execution environment or a provider-side retrieval/search surface. Also relevant: "`SandboxAgent` builds on the same ideas, then adds `default_manifest`, `base_instructions`, `capabilities`, and `run_as` for workspace-scoped runs." (https://openai.github.io/openai-agents-python/agents/)

### MCP servers on the agent

(a) An agent lists MCP servers whose tools are prepared into the request, with `mcp_config` controlling schema strictness and failure formatting.

(b) "`mcp_servers` MCP servers that provide MCP-backed tools to the agent." and "`mcp_config` Fine-tune how MCP tools are prepared, such as converting their schemas to strict mode and formatting MCP failures." (https://openai.github.io/openai-agents-python/agents/)

(c) Lifecycle: per agent; connection per run.

(d) Needs from host: transport to the server.

(e) Hands the run: a tool source plus a preparation policy. Listed here for completeness; it is a tool pack.

## LangGraph

Sources: https://langchain-ai.github.io/langgraph/concepts/persistence/ (redirects to the LangChain docs), https://docs.langchain.com/oss/python/langgraph/checkpointers , https://docs.langchain.com/oss/python/langgraph/stores , https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/ (Interrupts page), https://docs.langchain.com/oss/python/langgraph/use-time-travel , https://langchain-ai.github.io/langgraph/concepts/streaming/ . Fetched 2026-09-19. The `durable_execution` URL redirected to the Persistence page; durability modes are documented on the Checkpointers page.

### Checkpointers (thread-scoped state persistence)

(a) A pluggable saver that snapshots the full graph state at every super-step under a thread id, enabling resume, HITL, time travel, and fault tolerance.

(b) "Checkpointers persist a thread's graph state as checkpoints. Use them for short-term, thread-scoped memory, including conversation continuity, human-in-the-loop workflows, time travel, and fault tolerance." Table: "Persists: Graph state snapshots; Scope: A single thread; Access pattern: Pass a `thread_id` in graph config." (https://docs.langchain.com/oss/python/langgraph/durable-execution , which serves the Persistence page). Per-task writes: "As each node within a super-step finishes, its outputs are written to the checkpointer's `checkpoint_writes` table as task entries linked to the in-progress checkpoint. These per-task writes are what enable pending writes recovery". (https://docs.langchain.com/oss/python/langgraph/checkpointers)

(c) Lifecycle: bound at graph compile (`compile(checkpointer=...)`); written per super-step and per task; keyed per thread.

(d) Needs from host: durable storage (Postgres, SQLite, in-memory), a serializer (with optional encryption), a thread id.

(e) Hands the run: a store handle for state, and the ability to resume.

### Durability modes

(a) A per-invocation setting trading persistence guarantees for latency.

(b) "LangGraph supports three durability modes that let you balance performance and data consistency. You can specify the durability mode when calling any graph execution method" ... "`"exit"`: LangGraph persists changes only when graph execution exits - successfully, with an error, or due to a human-in-the-loop interrupt." ... "`"async"`: LangGraph persists changes asynchronously while the next step executes." ... "`"sync"`: LangGraph persists changes synchronously before the next step starts. This ensures that LangGraph writes every checkpoint before continuing execution". (https://docs.langchain.com/oss/python/langgraph/checkpointers)

(c) Lifecycle: per invocation.

(d) Needs from host: the checkpointer.

(e) Hands the run: a durability policy.

### Store (cross-thread long-term memory)

(a) A namespaced key-value store, optionally with semantic search, accessible from any node and shared across threads.

(b) "Stores persist application-defined data outside the graph state. Use them for long-term, cross-thread memory, including user preferences, facts, and shared knowledge." and "Memories are namespaced by a `tuple`" ... "the store also supports semantic search, allowing you to find memories based on meaning rather than exact matches. To enable this, configure the store with an embedding model". Access: "You can access the store and the `user_id` from any node by using the `Runtime` object." Base contract: "`aput`", "`aget`", "`adelete`", "`asearch`", "`alist_namespaces`". (https://docs.langchain.com/oss/python/langgraph/stores)

(c) Lifecycle: bound at compile; lives across threads and runs.

(d) Needs from host: storage backend, optionally an embedding model.

(e) Hands the run: a store handle injected via `Runtime`.

### Interrupts (human-in-the-loop)

(a) A dynamic pause anywhere in node code that persists state and waits indefinitely for a `Command(resume=...)`.

(b) "Interrupts allow you to pause graph execution at specific points and wait for external input before continuing. This enables human-in-the-loop patterns where you need external input to proceed. When an interrupt is triggered, LangGraph saves the graph state using its persistence layer and waits indefinitely until you resume execution." Requirements: "A checkpointer to persist the graph state", "A thread ID in your config", "To call `interrupt()` where you want to pause (payload must be JSON-serializable)". (https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)

(c) Lifecycle: per node execution; the wait can span processes.

(d) Needs from host: a checkpointer, a thread id, an external channel to collect the resume value.

(e) Hands the run: a human-in-the-loop wait with a typed resume value.

### Time travel (replay and fork)

(a) Re-execute from any prior checkpoint, or branch with modified state.

(b) "LangGraph supports time travel through checkpoints: Replay: Retry from a prior checkpoint. Fork: Branch from a prior checkpoint with modified state to explore an alternative path." and "`update_state` does not roll back a thread. It creates a new checkpoint that branches from the specified point. The original execution history remains intact." (https://docs.langchain.com/oss/python/langgraph/use-time-travel)

(c) Lifecycle: on demand against stored history.

(d) Needs from host: a checkpointer with history (`get_state_history`).

(e) Hands the run: a resume point and a branching primitive.

### Streaming modes

(a) Multiple concurrent projections of graph execution (state updates, LLM tokens, custom events, checkpoints, tasks, debug).

(b) "This page covers LangGraph's stream-mode API. It exposes graph execution through stream modes such as `updates`, `values`, `messages`, `custom`, `checkpoints`, `tasks`, and `debug`." and "For new applications, we recommend event streaming - the typed-projection API introduced in LangGraph v1.2. Event streaming gives you separate iterators per projection (messages, values, subgraphs, output)". (https://langchain-ai.github.io/langgraph/concepts/streaming/)

(c) Lifecycle: per invocation.

(d) Needs from host: an async iterator consumer.

(e) Hands the run: an observability and UI transport.

## Pydantic AI

Sources: https://ai.pydantic.dev/capabilities/ , https://ai.pydantic.dev/hooks/ , https://ai.pydantic.dev/dependencies/ , https://ai.pydantic.dev/agents/ , https://ai.pydantic.dev/toolsets/ , https://ai.pydantic.dev/output/ , https://ai.pydantic.dev/durable_execution/overview/ . Fetched 2026-09-19.

### Capability (the bundle itself)

(a) A first-class composable unit that bundles tools, hooks, instructions, model settings, and model selection, passed via `capabilities=[...]`; this is the closest published analogue to PromptForge's `Capability`.

(b) "A capability is a reusable, composable unit of agent behavior. Instead of threading multiple arguments through your `Agent` constructor - instructions here, model settings there, a toolset somewhere else, a history processor on yet another parameter - you can bundle related behavior into a single capability and pass it via the `capabilities` parameter." Contribution kinds: "Tools - via toolsets or native tools", "Lifecycle hooks - intercept and modify model requests, tool calls, and the overall run", "Instructions - static or dynamic instruction additions", "Model settings - static or per-step model settings", "Models - static or adaptive model selection and application-specific model ID resolution". Positioning: "This makes them the primary extension point for Pydantic AI. Whether you're building a memory system, a guardrail, a cost tracker, or an approval workflow, a capability is the right abstraction." On-demand loading: "Add `defer_loading=True` and the bundle becomes an on-demand capability that stays collapsed to a one-line catalog entry until the model loads it". Events: "Reusable capabilities can publish typed `CapabilityEvent` s for coordination and observability." (https://ai.pydantic.dev/capabilities/)

The published capability index groups shipped capabilities into: Harnesses (Coder, Researcher), Execution environments (FileSystem, Shell, Modal Sandbox), Tools and native abilities (MCP, Image Generation, Native Tool, ...), Web and research, Reasoning/planning/delegation (Thinking, Planning, Subagents, Dynamic Workflow, Advisor), Context management (Code Mode, Tool Search, Compaction, Tool Output Limits), Knowledge and memory (Memory, Conversation Search, Skills, Repo Context), Control and safety (Guardrails, Spend Limits, Tool approval, Handle Deferred Tool Calls, System Reminders), Self-extension (Capability Creation), Execution runtime (Durable execution, Step Persistence, Instrumentation, Managed Prompt, Thread Executor), Loop customization. (https://ai.pydantic.dev/capabilities/)

(c) Lifecycle: declared per agent; "Capabilities can be always-on or loaded by the model on demand."

(d) Needs from host: the agent loop's hook points, the toolset registry, the model adapter, `RunContext`.

(e) Hands the run: any combination of the kinds below.

### Hooks (lifecycle interception)

(a) Before/after/wrap/error hooks around the run, each graph node, each model request, tool validation, tool execution, output validation, output processing, tool preparation, deferred tool resolution, and event streaming.

(b) "Hooks let you intercept and modify agent behavior at every stage of a run - model requests, tool calls, streaming events - using simple decorators or constructor arguments." Families as fetched: Run hooks (`before_run`, `after_run`, `wrap_run`, `on_run_error`) "fire once per agent run"; Node hooks "fire for each graph step (`UserPromptNode`, `ModelRequestNode`, `CallToolsNode`)"; Model request hooks "fire around each LLM call. `ModelRequestContext` bundles `model`, `messages`, `model_settings`, and `model_request_parameters`. To swap the model for a given request, set `request_context.model` to a different `Model` instance." and "To skip the model call entirely, raise `SkipModelRequest(response)`"; Tool validation hooks "fire when the model's JSON arguments are parsed and validated"; Tool execution hooks "fire when the tool function runs" and "To skip execution, raise `SkipToolExecution(result)`"; Output validation hooks; Output processing hooks; Tool preparation "`prepare_tools` handles function tools; `prepare_output_tools` handles output tools separately" and "Filters or modifies tool definitions the model sees on each step"; Deferred tool call hook "Resolves deferred tool calls (approval-required or externally-executed) inline during a run." (https://ai.pydantic.dev/hooks/)

(c) Lifecycle: per run, per node, per model request, per tool call, per output, as named.

(d) Needs from host: the run graph, model adapter, tool manager, an approval channel for deferred calls.

(e) Hands the run: a gate (skip/approve/defer), a model swap, tool-list filtering, and result transformation.

### Dependencies (deps type) and RunContext

(a) A typed object passed at run time and surfaced to system prompts, tools, and validators via `RunContext[Deps]`.

(b) "Pydantic AI uses a dependency injection system to provide data and services to your agent's system prompts, tools and output validators." and "Dependencies are accessed through the `RunContext` type, this should be the first parameter of system prompt functions etc." Also: "In addition to `.deps`, `RunContext` provides access to the running agent via `.agent`" and "Dependency fields can also be referenced in instructions and descriptions via template strings - for example, `TemplateStr('Hello {{name}}')` renders `name` from the deps object at runtime." Testing: "Override the dependencies of the agent for the duration of the `with` block". (https://ai.pydantic.dev/dependencies/)

(c) Lifecycle: per run (`deps=` argument), type fixed per agent.

(d) Needs from host: nothing; host constructs it.

(e) Hands the run: service handles (the analogue of `RunServices`).

### Instructions and system prompts (static, dynamic, runtime, toolset-provided)

(a) Prompt text from four sources, ordered so static text precedes dynamic text for cache stability.

(b) "Static instructions: These are known when writing the code and can be defined via the `instructions` parameter of the `Agent` constructor. Dynamic instructions: These rely on context that is only available at runtime and should be defined using functions decorated with `@agent.instructions`. ... Runtime instructions: These are additional instructions for a specific run that can be passed to one of the run methods using the `instructions` argument." and "Each instruction is internally classified as either static ... or dynamic (from `@agent.instructions` functions, runtime instructions, or toolset instructions). Static instructions are always sorted before dynamic ones. This ordering enables providers that support prompt caching ... to cache the stable static prefix". Distinction: "`instructions` when you want your request to the model to only include system prompts for the current agent; `system_prompt` when you want your request to the model to retain the system prompts used in previous requests". (https://ai.pydantic.dev/agents/). Toolset instructions: "A `FunctionToolset` can provide instructions that are automatically included in the model request. This lets each toolset carry its own usage guidance alongside its tools". (https://ai.pydantic.dev/toolsets/)

(c) Lifecycle: static per agent; dynamic re-evaluated per model request; runtime per run.

(d) Needs from host: `RunContext`, a clock if instructions embed dates.

(e) Hands the run: prompt text with a cache-aware ordering rule.

### Output validators and output functions

(a) Async validation functions on the final output that can force a model retry within a retry budget.

(b) "Pydantic AI provides a way to add validation functions via the `agent.output_validator` decorator." and "Each `ModelRetry` raised here consumes one unit of the run's output retry budget. The budget defaults to `1` and can be set on the agent with `AgentRetries` via `Agent(retries={'output': N})`". (https://ai.pydantic.dev/output/)

(c) Lifecycle: per output (including partials during streaming).

(d) Needs from host: `RunContext`, IO if validation needs it.

(e) Hands the run: a gate with a retry signal.

### Toolsets with lifecycle, filtering, approval, deferred loading

(a) A composable collection of tools with per-run and per-step lifecycle hooks and wrappers that filter, rename, prefix, require approval, or defer loading.

(b) "A toolset represents a collection of tools that can be registered with an agent in one go. They can be reused by different agents, swapped out at runtime or during testing, and composed in order to dynamically filter which tools are available, modify tool definitions, or change tool execution behavior." Lifecycle: "`for_run(ctx)` - called once per agent run, before `__aenter__`. Return a fresh instance to isolate state between runs." and "`for_run_step(ctx)` - called at the start of each run step." Approval: "`ApprovalRequiredToolset` wraps a toolset and lets you dynamically require approval for a given tool call based on a user-defined function". (https://ai.pydantic.dev/toolsets/)

(c) Lifecycle: per agent, per run, per step.

(d) Needs from host: the tool manager, an approval channel.

(e) Hands the run: tools (the least interesting case) plus an approval gate and per-run state isolation.

### Usage limits

(a) Caps on tokens, requests, tool calls, and cost for a run.

(b) "Pydantic AI offers a `UsageLimits` structure to help you limit your usage (tokens, requests, tool calls, and cost) on model runs. You can apply these settings by passing the `usage_limits` argument to the `run{_sync,_stream}` functions." (https://ai.pydantic.dev/agents/)

(c) Lifecycle: per run.

(d) Needs from host: usage accounting, a price table for cost.

(e) Hands the run: a budget policy that aborts with `UsageLimitExceeded`.

### Durable execution (Temporal, DBOS, Prefect, Restate, others)

(a) Engine integrations that keep one run alive across crashes and restarts, distinct from conversation storage.

(b) "Pydantic AI allows you to build durable agents that can preserve their progress across transient API failures and application errors or restarts, and handle long-running, asynchronous, and human-in-the-loop workflows with production-grade reliability." and "Durability is not storage. A durable engine keeps one run alive across crashes and restarts. It does not store your chat threads". Engines: "Temporal, DBOS, Prefect, Restate, AWS Lambda" plus "Kitaru, Apache Airflow". Extension hook: "Capability authors can also move custom hook work into engine activities, steps, or tasks with durable capability operations." (https://ai.pydantic.dev/durable_execution/overview/)

(c) Lifecycle: per run, spanning processes.

(d) Needs from host: a workflow engine, deterministic replay discipline.

(e) Hands the run: durability (checkpointed activities) and long waits.

## Google Agent Development Kit

Sources: https://google.github.io/adk-docs/callbacks/ , https://google.github.io/adk-docs/plugins/ , https://google.github.io/adk-docs/sessions/ , https://google.github.io/adk-docs/sessions/memory/ , https://google.github.io/adk-docs/artifacts/ , https://google.github.io/adk-docs/agents/llm-agents/ , https://google.github.io/adk-docs/evaluate/ . Fetched 2026-09-19.

### Callbacks (before/after agent, model, tool)

(a) Per-agent functions at six points whose return value either allows the default step or overrides it.

(b) "Callbacks are a cornerstone feature of ADK, providing a powerful mechanism to hook into an agent's execution process. They allow you to observe, customize, and even control the agent's behavior at specific, predefined points without modifying the core ADK framework code." Points: `Before Agent`, `After Agent`, `Before Model`, `After Model`, `Before Tool`, `After Tool`. Control: "`return None` (Allow Default Behavior)" versus returning an object: "`before_agent_callback` → `Content`: Skips the agent's main execution logic", "`before_model_callback` → `LlmResponse`: Skips the call to the external Large Language Model", "`before_tool_callback` → Python: `dict` ... Skips the execution of the actual tool function", "`after_model_callback` → `LlmResponse`: Replaces the `LlmResponse` received from the LLM", "`after_tool_callback` → ... Replaces the result returned by the tool." (https://google.github.io/adk-docs/callbacks/)

(c) Lifecycle: per agent, fired per request / per model call / per tool call.

(d) Needs from host: `CallbackContext` or `ToolContext` "including the invocation details, session state, and potentially references to services like artifacts or memory".

(e) Hands the run: a gate with short-circuit replacement, plus state mutation.

### Plugins (runner-wide callback packages)

(a) A class registered once on the `Runner` whose callbacks apply globally to every agent, tool, and model call, with additional hooks at user-message, runner start/end, and event points.

(b) "A Plugin in Agent Development Kit (ADK) is a custom code module that can be executed at various stages of an agent workflow lifecycle using callback hooks." and "While a typical Agent Callback is configured on a single agent, a single tool for a specific task, a Plugin is registered once on the `Runner` and its callbacks apply globally to every agent, tool, and LLM call managed by that runner." Hook points: "Callbacks are available when a user message is received, before and after an `Runner`, `Agent`, `Model`, or `Tool` is called, for `Events`, and when a `Model`, or `Tool` error occurs. These callbacks include, and take precedence over, the any callbacks defined within your Agent, Model, and Tool classes." First hook: "A User Message callback (`on_user_message_callback`) happens when a user sends a message ... Returns a `types.Content` object to replace the user's original message." Prebuilt: "Reflect and Retry Tools", "BigQuery Analytics", "Context Filter: Filters the generative AI context to reduce its size", "Global Instruction: Plugin that provides global instructions functionality at the App level", "Save Files as Artifacts", "Logging". (https://google.github.io/adk-docs/plugins/)

(c) Lifecycle: per runner (process), applied to every invocation.

(d) Needs from host: the runner's dispatch points.

(e) Hands the run: policy, prompt injection (Global Instruction), context trimming, retries, logging.

### Session service and state

(a) A service owning conversation threads (`Session`), their event history, and per-session key-value `State`.

(b) "`Session`: The Current Conversation Thread ... Contains the chronological sequence of messages and actions taken by the agent (referred to `Events`)". "`State` (`session.state`): Data Within the Current Conversation". "`SessionService`: Manages the different conversation threads (`Session` objects). Handles the lifecycle: creating, retrieving, updating (appending `Events`, modifying `State`), and deleting individual `Session` s." (https://google.github.io/adk-docs/sessions/)

(c) Lifecycle: per runner; sessions persist per user/app.

(d) Needs from host: storage backend (in-memory, database, cloud).

(e) Hands the run: a store handle for history and scratch state.

### Memory service

(a) A searchable long-term store fed from completed sessions or explicit entries.

(b) "The `BaseMemoryService` (or `Service` in Go) defines the interface for managing this searchable, long-term knowledge store." Operations: "`add_session_to_memory`: Takes a completed `Session` and adds relevant information to the long-term knowledge store", "`add_events_to_memory`: Appends a delta of events", "`add_memory`: Adds explicit `MemoryEntry` objects directly", "Searching Information (`search_memory`): Lets an agent (typically via a `Tool`) query the knowledge store". Implementations: "InMemoryMemoryService", "VertexAiMemoryBankService" ("Extracts meaningful information from conversations and consolidates it with existing memories powered by LLM"), "VertexAiRagMemoryService". (https://google.github.io/adk-docs/sessions/memory/)

(c) Lifecycle: per runner; ingestion at session end or per turn.

(d) Needs from host: storage, optionally an LLM for consolidation, an embedding/RAG backend.

(e) Hands the run: a store handle for cross-session recall.

### Artifact service

(a) Named, versioned binary blobs scoped to a session or a user, saved and loaded via context.

(b) "In ADK, Artifacts represent a crucial mechanism for managing named, versioned binary data associated either with a specific user interaction session or persistently with a user across multiple sessions." and "An Artifact is essentially a piece of binary data (like the content of a file) identified by a unique `filename` string within a specific scope (session or user). Each time you save an artifact with the same filename, a new version is created." Service: "Their storage and retrieval are managed by a dedicated Artifact Service (an implementation of `BaseArtifactService`" with "`InMemoryArtifactService`", "`GcsArtifactService`", "`FileArtifactService`". (https://google.github.io/adk-docs/artifacts/)

(c) Lifecycle: per runner; versions accumulate per filename.

(d) Needs from host: blob storage.

(e) Hands the run: a versioned file store (a mount-like surface for binary outputs).

### Planner

(a) A pluggable reasoning strategy attached to an `LlmAgent`.

(b) "`planner` (Optional): Assign a `BasePlanner` instance to enable multi-step reasoning and planning before execution. There are two main planners: `BuiltInPlanner`: Leverages the model's built-in planning capabilities (e.g., Gemini's thinking feature)." and "`PlanReActPlanner`: This planner instructs the model to follow a specific structure in its output: first create a plan, then execute actions (like calling tools), and provide reasoning for its steps." (https://google.github.io/adk-docs/agents/llm-agents/)

(c) Lifecycle: per agent, applied per model request.

(d) Needs from host: model thinking configuration or prompt shaping.

(e) Hands the run: prompt structure and model settings.

### Code executor

(a) A pluggable executor that runs code blocks the model emits.

(b) "`code_executor` (Optional): Provide a `BaseCodeExecutor` instance to allow the agent to execute code blocks found in the LLM's response." (https://google.github.io/adk-docs/agents/llm-agents/)

(c) Lifecycle: per agent, invoked per response containing code.

(d) Needs from host: a sandbox or interpreter.

(e) Hands the run: an execution environment.

### Evaluation

(a) A framework for scoring trajectories and final responses against test cases.

(b) "Due to the probabilistic nature of models, deterministic "pass/fail" assertions are often unsuitable for evaluating agent performance. Instead, we need qualitative evaluations of both the final output and the agent's trajectory - the sequence of steps taken to reach the solution." and "Agent evaluation can be broken down into two components: 1. Evaluate Trajectory and Tool Use". (https://google.github.io/adk-docs/evaluate/)

(c) Lifecycle: offline / per test run.

(d) Needs from host: stored traces, a scorer.

(e) Hands the run: nothing at activation; it consumes run traces.

## Letta (MemGPT lineage)

Sources: https://docs.letta.com/guides/agents/memory , https://docs.letta.com/guides/agents/memory-blocks , https://docs.letta.com/guides/agents/archival-memory , https://docs.letta.com/guides/agents/multi-agent-shared-memory , https://docs.letta.com/api/resources/agents/methods/create/ , https://www.letta.com/blog/sleep-time-compute/ , https://docs.letta.com/guides/agents/sleep-time-agents (currently serves a "Memory & dreaming" page about MemFS). Fetched 2026-09-19.

### Memory blocks (core memory, in-context)

(a) Labeled, size-limited text sections pinned into the system prompt that the agent edits through memory tools and the developer edits through the API.

(b) "Memory blocks are structured sections of the agent's context window that persist across all interactions. They are always visible - no retrieval needed. Under the hood, memory blocks are simply prepended to the agent's prompt in an XML-like format." Structure: "A `label`, which is a unique identifier for the block; A `description`, which describes the purpose of the block; A `value`, which is the contents/data of the block; A `limit`, which is the size limit (in characters) of the block". Read-only: "Memory blocks are read-write by default ... but can be set to read-only by setting the `read_only` field to `true`." Framing: "Memory blocks aren't just storage - they're a coordination primitive that enables sophisticated agent behavior." (https://docs.letta.com/guides/agents/memory-blocks). Deprecation notice on the shared-memory page: "This guide describes one in-context memory block attached to multiple agents using Letta's legacy v1 API. Memory blocks may be deprecated in the future. We do not recommend building on memory blocks anymore. Use shared memory repositories for new work, and make a best effort to migrate agents to MemFS." (https://docs.letta.com/guides/agents/multi-agent-shared-memory)

(c) Lifecycle: attached per agent (or shared), present in every prompt, persisted in the database.

(d) Needs from host: persistent storage, prompt assembly that renders blocks, memory-editing tools with a character budget.

(e) Hands the run: prompt text that is writable by the model and by external processes.

### Archival memory (out-of-context vector store)

(a) An unbounded, semantically searchable store queried on demand via tools, not pinned to context.

(b) "Archival memory is a semantically searchable database where agents can store facts, knowledge, and information for long-term retrieval. Unlike memory blocks, archival memory fragments cannot be pinned to the context window, and must be queried on-demand via tools." Characteristics: "Agent-immutable", "Unlimited storage", "Semantic search", "Tagged organization". Distinction from conversation search: "Archival memory is for intentional storage ... Conversation search is for historical retrieval". (https://docs.letta.com/guides/agents/archival-memory)

(c) Lifecycle: per agent, persistent.

(d) Needs from host: a vector database and embedding model.

(e) Hands the run: a store handle reached through tools.

### Shared memory blocks between agents

(a) One block attached to several agents so an update by any writer is immediately visible to all.

(b) "Shared memory blocks let multiple agents access and update the same memory. When one agent updates the block, all others see the change immediately. This enables real-time coordination without explicit agent-to-agent messaging." Concurrency: "`memory_insert` Appending new info - Concurrent-safe? Yes (append-only)", "`memory_rethink` Full rewrites - No (last-writer-wins)". External sync: "Sync data into shared blocks from databases, webhooks, or scheduled jobs". (https://docs.letta.com/guides/agents/multi-agent-shared-memory)

(c) Lifecycle: block outlives any agent; attach and detach at any time.

(d) Needs from host: shared persistent storage with consistent reads.

(e) Hands the run: a shared, prompt-visible coordination channel.

### Sleep-time agents

(a) A background agent that owns memory-editing tools and rewrites the primary agent's shared blocks between turns, on a configurable frequency.

(b) API reference: "`enable_sleeptime`: optional boolean. If set to True, memory management will move to a background agent thread." and the group field "`sleeptime_agent_frequency`: optional number" (https://docs.letta.com/api/resources/agents/methods/create/). Letta's own blog: "When you create agents with this type, Letta actually creates two agents under the hood: a primary agent and a sleep-time agent. ... the primary agent is not provided with tools to edit its core memory ... These tools are attached to the sleep-time agent, which has the ability to manage both the in-context memory of the primary agent as well as its own in-context memory." and "the primary and sleeptime agents can be configured independently with different underlying models" (https://www.letta.com/blog/sleep-time-compute/). The current docs page at the sleep-time URL describes the successor in Letta Code: "Dreaming uses background subagents to review recent conversations, consolidate useful lessons, and update memory without interrupting your active work. Configure dreaming with `/sleeptime` in the CLI or Dream settings in the app. Choose when it runs: after a set number of completed agent steps or when the context window is compacted." (https://docs.letta.com/guides/agents/sleep-time-agents)

(c) Lifecycle: per agent group; triggered every N turns or at compaction.

(d) Needs from host: a scheduler tied to turn counts, a second model budget, shared block storage.

(e) Hands the run: a schedule plus a background writer of prompt-visible memory.

### MemFS (git-backed memory filesystem)

(a) The newer memory substrate: a directory tree the agent inspects and edits, versioned in git, shared across conversations.

(b) "Letta agents use MemFS, a git-backed memory filesystem that they can inspect and edit. Memory is shared across the agent's conversations and improves as the agent learns durable information about you and its work." (https://docs.letta.com/guides/agents/sleep-time-agents)

(c) Lifecycle: per agent, persistent, versioned.

(d) Needs from host: a filesystem and git.

(e) Hands the run: a mount with version history. The dedicated MemFS page was not fetched.

## Claude Agent SDK

Sources: https://platform.claude.com/docs/en/agent-sdk/overview , https://platform.claude.com/docs/en/agent-sdk/hooks , https://platform.claude.com/docs/en/agent-sdk/permissions , https://platform.claude.com/docs/en/agent-sdk/sessions , https://platform.claude.com/docs/en/agent-sdk/subagents , https://platform.claude.com/docs/en/agent-sdk/cost-tracking , https://platform.claude.com/docs/en/agent-sdk/todo-tracking , https://platform.claude.com/docs/en/agent-sdk/custom-tools . Fetched 2026-09-19.

The overview enumerates the capability kinds the SDK exposes: "Built-in tools", "Hooks: Run custom code at key points in the agent lifecycle", "Subagents: Spawn specialized agents for focused subtasks", "MCP: Connect external tools and data sources via the Model Context Protocol", "Permissions: Control which tools run automatically, which need approval", "Sessions: Maintain context across exchanges, resume or fork later", "Skills, commands, and memory: Load automatically from your project's `.claude/` and from `~/.claude/`", "Plugins: Package skills, agents, hooks, and MCP servers, and load them by local path" (https://platform.claude.com/docs/en/agent-sdk/overview).

### Hooks (in-process callbacks)

(a) Callback functions in the host process, registered per event with optional matchers, that can block, modify, inject context, or approve.

(b) "Hooks are callback functions that run your code in response to agent events, like a tool being called, a session starting, or execution stopping." Uses: "Block dangerous operations before they execute", "Transform inputs and outputs to sanitize data, inject credentials, or redirect file paths", "Require human approval for sensitive actions". Event table (Python/TypeScript availability noted per row) includes `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PostToolBatch`, `UserPromptSubmit`, `UserPromptExpansion`, `MessageDisplay`, `Stop`, `StopFailure`, `SubagentStart`, `SubagentStop`, `PreCompact`, `PostCompact`, `PreModelSwitch`, `PostModelSwitch`, `PermissionRequest`, `PermissionDenied`, `SessionStart`, `SessionEnd`, `Notification`, `Setup`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `Elicitation`, `ElicitationResult`, `ConfigChange`, `InstructionsLoaded`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged`, `FileChanged`, `DirectoryAdded`. (https://platform.claude.com/docs/en/agent-sdk/hooks)

(c) Lifecycle: registered per `query()`; fired per event.

(d) Needs from host: the SDK event bus; nothing external.

(e) Hands the run: gates, input rewriting, context injection.

### Permissions (evaluation order, modes, canUseTool)

(a) An ordered pipeline: hooks, deny rules, ask rules, permission mode, allow rules, then a runtime `canUseTool` callback.

(b) "When Claude requests a tool, the SDK checks permissions in this order: Hooks ... Deny rules ... Ask rules ... Permission mode ... Allow rules ... canUseTool callback". Modes: "`default`", "`dontAsk`", "`acceptEdits`", "`bypassPermissions`", "`plan`", "`auto` Model-classified approvals". Dynamic: "Call `set_permission_mode()` (Python) or `setPermissionMode()` (TypeScript) to change the mode mid-session." (https://platform.claude.com/docs/en/agent-sdk/permissions)

(c) Lifecycle: per query, switchable mid-session; subagents inherit with restrictions.

(d) Needs from host: a callback for approvals, settings files, a classifier for `auto`.

(e) Hands the run: a policy gate with a human-approval fallback.

### Sessions (continue, resume, fork, SessionStore)

(a) On-disk conversation transcripts that can be continued, resumed by id, or forked, with an adapter for cross-host storage.

(b) "A session is the conversation history the SDK accumulates while your agent works. ... The SDK writes it to disk automatically so you can return to it later." and "Sessions persist the conversation, not the filesystem. To snapshot and revert file changes the agent made, use file checkpointing." Fork: "Fork is different: it creates a new session that starts with a copy of the original's history. The original stays unchanged." Cross-host: "Attach a `sessionStore` / `session_store` adapter so the SDK mirrors transcripts to your own backend and another host can resume them." (https://platform.claude.com/docs/en/agent-sdk/sessions)

(c) Lifecycle: per session id, across processes.

(d) Needs from host: disk or a store adapter, a working-directory key.

(e) Hands the run: a resumable transcript store and a branching primitive.

### Subagents (programmatic AgentDefinition)

(a) Separate agent instances with their own prompt, tools, and model, defined in code or as files, returning only a final message.

(b) "Subagents are separate agent instances that your main agent can spawn to handle focused subtasks." Benefits: "Context isolation: each subagent runs in its own conversation ... only its final message returns to the parent", "Parallelization", "Specialized instructions and knowledge", "Tool restrictions". Definition routes: "Programmatically: use the `agents` parameter in your `query()` options", "Filesystem-based: define agents as markdown files in `.claude/agents/`", "Built-in general-purpose". (https://platform.claude.com/docs/en/agent-sdk/subagents)

(c) Lifecycle: definitions per query; instances per delegation.

(d) Needs from host: model access, a second context.

(e) Hands the run: a delegation target.

### Cost and usage tracking, budget

(a) Per-step token usage, per-model cost, cumulative estimated cost on the result message, and a hard USD budget.

(b) "The `total_cost_usd` and `costUSD` fields are client-side estimates, not authoritative billing data." and "The result message ... includes `total_cost_usd`, the cumulative estimated cost across all steps in that call." Budget: "`maxBudgetUsd` (TypeScript) or `max_budget_usd` (Python) is compared against the same running total". Subagent bounding: "To bound how much subagents can add to `total_cost_usd`, set the depth, concurrency, and spend limits on the query." (https://platform.claude.com/docs/en/agent-sdk/cost-tracking)

(c) Lifecycle: per query; accumulate across queries yourself.

(d) Needs from host: a price table, usage fields from the API.

(e) Hands the run: a budget policy and an accounting stream.

### Todo and task tracking

(a) Structured task tools whose calls stream as `tool_use` blocks so the host can render progress; enabled per model or by opt-in.

(b) "In a session that has the task-tracking tools, Claude keeps a written todo list, updating each item's status as it works. You see each change in the message stream as a structured tool call." Tools: "`TodoWrite`, `TaskCreate`, `TaskGet`, `TaskUpdate`, `TaskList`". Lifecycle: "Created ... `pending`", "Activated ... `in_progress`", "Completed", "Removed ... `status: "deleted"`". (https://platform.claude.com/docs/en/agent-sdk/todo-tracking)

(c) Lifecycle: per session.

(d) Needs from host: a stream consumer.

(e) Hands the run: a progress-state channel (these are tools, but their value is the observable state model they expose to the host).

### Custom tools via in-process MCP server

(a) Host-defined tools served over an in-process MCP server rather than a subprocess. Listed for completeness because it is the SDK's route for tools; page fetched (https://platform.claude.com/docs/en/agent-sdk/custom-tools) but not quoted here since tools are out of scope.

## Optional systems (brief)

### Vercel AI SDK: language model middleware

(a) Provider-agnostic wrappers around the model call that transform params or wrap generate/stream.

(b) "Language model middleware is a way to enhance the behavior of language models by intercepting and modifying the calls to the language model. It can be used to add features like guardrails, RAG, caching, and logging in a language model agnostic way." Implementation surface: "`transformParams`", "`wrapGenerate`", "`wrapStream`". Built-ins: "`extractReasoningMiddleware`", "`extractJsonMiddleware`", "`simulateStreamingMiddleware`", "`defaultInstructionsMiddleware`: Applies default instructions when a call does not provide its own instructions", "`defaultSettingsMiddleware`", "`addToolInputExamplesMiddleware`". (https://ai-sdk.dev/docs/ai-sdk-core/middleware)

(c) Lifecycle: per wrapped model, applied per call, composed in order.

(d) Needs from host: the model adapter.

(e) Hands the run: prompt injection, default settings, output post-processing, caching.

### smolagents: executors and sandboxes

(a) A `CodeAgent` runs model-written Python either in a restricted local AST interpreter or in a remote sandbox selected by `executor_type`.

(b) "By default, the `CodeAgent` runs LLM-generated code in your environment." Local executor: "code execution in `smolagents` is not performed by the vanilla Python interpreter. We have re-built a more secure `LocalPythonExecutor` from the ground up." with "imports are disallowed unless they have been explicitly added to an authorization list" and "The total count of elementary operations processed is capped". Remote: "It's simpler to set up using `executor_type="blaxel"`, `executor_type="e2b"`, `executor_type="modal"`, or `executor_type="docker"`". (https://huggingface.co/docs/smolagents/tutorials/secure_code_execution)

(c) Lifecycle: per agent; sandbox created per run and cleaned up on exit.

(d) Needs from host: a sandbox provider account or Docker, credential handling.

(e) Hands the run: an execution environment with an import allowlist and operation cap.

Not surveyed: Microsoft AutoGen / Agent Framework middleware, CrewAI memory and knowledge sources, Mastra workflows and memory. See Gaps.

## Cross-system taxonomy

Every non-tool kind above falls into one of thirteen families. The families are ordered roughly by how directly they touch the model: the first three shape what the model sees, the next three constrain what it may do, the middle group deals with state and time, and the last group is about where and how work runs. Table 1 lists each family, the systems that have a named instance of it, and the canonical name each system uses. The name in the table is the name the system's documentation uses; where a system has several instances in one family they are listed together.

Three observations follow from the table. First, prompt injection and lifecycle hooks are universal: every surveyed system has both, and in several (Claude Code hooks via `additionalContext`, Pydantic AI toolset instructions, ADK Global Instruction plugin) the two are the same mechanism. Second, "memory" splits cleanly into two families that no system conflates: a thread-scoped transcript store (sessions, checkpointers) and a cross-thread knowledge store (LangGraph Store, ADK MemoryService, Letta archival, Claude auto memory). Letta is the outlier that additionally makes memory prompt-visible and model-writable (blocks). Third, scheduling is rare: only Letta (sleep-time frequency, dreaming at compaction) and Claude Code (monitors, scheduled tasks referenced from the skills page) have a capability that fires on its own clock rather than in response to a loop event.

Table 1. Cross-system taxonomy of non-tool extension kinds.

| Family | Systems that have it | Canonical name in each system |
| --- | --- | --- |
| Prompt and context injection | MCP, Claude Code, OpenAI Agents SDK, LangGraph (via Store reads in nodes), Pydantic AI, Google ADK, Letta, Claude Agent SDK, Vercel AI SDK | MCP: prompts, resources, Skills over MCP; Claude Code: CLAUDE.md, `.claude/rules`, skills, output styles, hook `additionalContext`; OpenAI: `instructions` callback, prompt templates, `RECOMMENDED_PROMPT_PREFIX`; Pydantic AI: instructions (static/dynamic/runtime/toolset), System Reminders, Repo Context; ADK: `instruction`, Global Instruction plugin, planner; Letta: memory blocks, MemFS; Agent SDK: `UserPromptSubmit` hook context, memory files; Vercel: `defaultInstructionsMiddleware`, RAG `transformParams` |
| Lifecycle hooks and interception | Claude Code, OpenAI Agents SDK, Pydantic AI, Google ADK, Claude Agent SDK, Vercel AI SDK | Claude Code: hooks (33 events, 5 handler types); OpenAI: `RunHooks`, `AgentHooks`; Pydantic AI: `Hooks` capability (run, node, model request, tool validate, tool execute, output validate, output process, prepare_tools, deferred_tool_calls, event stream); ADK: callbacks (before/after agent, model, tool), plugins (runner-wide); Agent SDK: hooks; Vercel: `wrapGenerate`, `wrapStream` |
| Approval and guardrail gates | MCP (indirectly), Claude Code, OpenAI Agents SDK, Pydantic AI, Google ADK, Claude Agent SDK | MCP: host consent principles, `PreToolUse`-adjacent `Elicitation` hook in Claude Code; Claude Code: permission modes, allow/ask/deny rules, `PreToolUse` `permissionDecision`; OpenAI: input/output/tool guardrails with tripwires, `needs approval` on tools; Pydantic AI: Guardrails, `ApprovalRequiredToolset`, `requires_approval`, output validators, `SkipToolExecution`; ADK: `before_*` callbacks returning an override, plugins for policy; Agent SDK: permission pipeline (hooks, deny, ask, mode, allow, `canUseTool`) |
| Human-in-the-loop waits | MCP, LangGraph, Pydantic AI, Claude Code, Claude Agent SDK | MCP: elicitation (accept/decline/cancel), sampling approval; LangGraph: `interrupt()` and `Command(resume=...)`; Pydantic AI: `DeferredToolRequests` / `DeferredToolResults`, `ApprovalRequired`, `CallDeferred`; Claude Code: `PermissionRequest`, `Elicitation`, `AskUserQuestion`; Agent SDK: `canUseTool` callback, `Elicitation` hook |
| Thread memory and transcript stores | OpenAI Agents SDK, LangGraph, Google ADK, Claude Agent SDK, Letta | OpenAI: Sessions (`SQLiteSession` etc.); LangGraph: checkpointers (`PostgresSaver`, `SqliteSaver`); ADK: `SessionService`, `session.state`; Agent SDK: sessions (continue/resume/fork, `SessionStore`); Letta: messages, conversations, recall |
| Cross-thread knowledge stores | LangGraph, Google ADK, Letta, Claude Code, Pydantic AI | LangGraph: Store (`BaseStore`, namespaces, semantic search); ADK: `MemoryService` (`add_session_to_memory`, `search_memory`); Letta: archival memory, shared blocks, MemFS; Claude Code: auto memory, subagent `memory` scope; Pydantic AI: Memory capability, Conversation Search |
| Durability, checkpointing, and time travel | LangGraph, Pydantic AI, MCP (2026-07-28 Tasks), Claude Agent SDK | LangGraph: durability modes (`exit`/`async`/`sync`), replay, fork via `update_state`; Pydantic AI: Durable execution (Temporal, DBOS, Prefect, Restate), Step Persistence (`continue_run`, `fork_run`); MCP: Tasks extension with durable handles; Agent SDK: file checkpointing, session fork |
| Scheduling and background activity | Letta, Claude Code | Letta: sleep-time agents (`enable_sleeptime`, `sleeptime_agent_frequency`), dreaming at step count or compaction; Claude Code: plugin monitors (`when: always` / `on-skill-invoke`), scheduled tasks |
| Transports, channels, and notifications | MCP, Claude Code, LangGraph | MCP: notifications (`list_changed`, `resources/updated`), logging, subscriptions; Claude Code: plugin channels (MCP-bound message channels), monitors (stdout lines as notifications), `Notification` hook; LangGraph: stream modes and event streaming |
| Sandboxes and execution environments | Google ADK, smolagents, Pydantic AI, OpenAI Agents SDK, Claude Code | ADK: `code_executor` (`BaseCodeExecutor`), artifacts; smolagents: `LocalPythonExecutor`, `executor_type` (e2b, docker, modal, blaxel); Pydantic AI: FileSystem, Shell, Modal Sandbox, Code Mode; OpenAI: hosted code interpreter, `ShellTool`, `ComputerTool`, `SandboxAgent`; Claude Code: subagent `isolation: worktree`, `WorktreeCreate` hook |
| Sub-agent delegation | Claude Code, OpenAI Agents SDK, Pydantic AI, Google ADK, Letta, Claude Agent SDK | Claude Code: subagents, skills with `context: fork`, agent teams; OpenAI: handoffs, agents-as-tools; Pydantic AI: Subagents, Dynamic Workflow, Advisor; ADK: sub-agents via `before_tool_callback` "or another agent"; Letta: sleep-time agent, dreaming subagents; Agent SDK: `AgentDefinition`, built-in general-purpose |
| Observability, tracing, and evaluation | MCP, OpenAI Agents SDK, Pydantic AI, Google ADK, Claude Agent SDK, LangGraph | MCP: logging (`notifications/message`, `logging/setLevel`); OpenAI: traces and spans, `add_trace_processor`, `set_trace_processors`; Pydantic AI: Instrumentation (OpenTelemetry), `CapabilityEvent`; ADK: Logging plugin, BigQuery Analytics, evaluation framework; Agent SDK: usage on every message, `PostToolUse` audit hooks; LangGraph: `debug` and `checkpoints` stream modes |
| Cost and budget | Pydantic AI, Claude Agent SDK, OpenAI Agents SDK, MCP | Pydantic AI: `UsageLimits` (tokens, requests, tool calls, cost), Spend Limits capability; Agent SDK: `total_cost_usd`, `max_budget_usd`, subagent spend limits; OpenAI: usage on `RunContextWrapper`, `MaxTurnsExceeded`; MCP: sampling `costPriority` hint |
| Model selection and settings | Claude Code, OpenAI Agents SDK, Pydantic AI, Google ADK, MCP, Vercel AI SDK | Claude Code: skill/subagent `model` and `effort`, `PreModelSwitch` hook; OpenAI: `model_settings`, `tool_use_behavior`; Pydantic AI: capability-provided model settings and adaptive models, `request_context.model` swap in hooks; ADK: `BuiltInPlanner` thinking config; MCP: sampling `modelPreferences`; Vercel: `defaultSettingsMiddleware` |

Table 1 has thirteen rows because model selection did not fit cleanly into either the prompt family or the hooks family and appears in six systems, so it earned its own row. The scope and workspace-boundary kind (MCP roots, Claude Code `additionalDirectories` and `CwdChanged`, Pydantic AI FileSystem root) is folded into the sandbox family since all three express "where the run may act."

Mapping to PromptForge's current shape: `RunServices` today is the dependency-injection family (OpenAI `context`, Pydantic AI `deps`, ADK `CallbackContext`), and its two fields (virtual filesystem, cancellation) correspond to the sandbox family and to a slice of the hooks family. `Contribution` being tools-only means PromptForge currently covers none of the thirteen rows except the one the owner calls least interesting. The deferred items in its doc comment (mounts, prompt fragments, Lua surface) map to the sandbox row, the prompt-injection row, and to a scripting surface no surveyed system exposes as a contribution kind, though Pydantic AI's Code Mode and smolagents' code agents are the nearest analogues. Co-activation conflicts have a direct precedent in Claude Code's plugin and skill name-resolution rules and in Pydantic AI's `Capability(id=...)`, though neither documents an explicit conflict declaration.

## Gaps

The following pages could not be fetched or were not fetched, and nothing was written from memory for them.

- MCP `2026-07-28` per-primitive pages: the deprecated-features registry at `https://modelcontextprotocol.io/specification/2026-07-28/basic/deprecated` returned 404, and the individual pages for the Tasks, Skills over MCP, and MCP Apps extensions were not fetched. Primitive definitions were therefore quoted from the `2025-06-18` revision. The `2026-07-28` overview was fetched and its feature lists are quoted; whether Sampling and Roots are formally deprecated or merely moved is not confirmed here.
- Letta: `https://docs.letta.com/guides/agents/architectures/sleeptime-agents` returned 404, and both `.../architectures/sleeptime` and `.../sleep-time-agents` now serve a "Memory & dreaming" page about MemFS rather than the older sleep-time agent guide. Sleep-time agent definitions were taken from the Create Agent API reference (docs.letta.com) and from Letta's own engineering blog. The dedicated MemFS page and the "context hierarchy" page were not fetched.
- LangGraph: the `durable_execution` concept URL redirects to the Persistence page; durability modes (`exit`, `async`, `sync`) were quoted from the Checkpointers page instead. The Interrupts page was fetched from the old `human_in_the_loop` URL; the newer `docs.langchain.com` interrupts page was not fetched separately.
- Google ADK: the callbacks page did not include a separate list of callback types beyond the six named; the code-executor and planner detail pages, the session-service implementations page, and the evaluation how-to were not fetched (only the overview pages).
- OpenAI Agents SDK: the `running_agents`, `context`, `mcp`, and `lifecycle` API reference pages were not fetched; hook events are quoted from the Agents page summary rather than the full Lifecycle reference.
- Claude Code: the `agent-teams`, `scheduled-tasks`, `checkpointing`, `settings`, and `plugins` (non-reference) pages were not fetched; scheduled tasks and agent teams are mentioned only where the fetched pages referenced them.
- Claude Agent SDK: `custom-tools` was fetched but not quoted (tools are out of scope); `mcp`, `file-checkpointing`, and `streaming-input` were not fetched.
- Optional systems not surveyed at all: Microsoft AutoGen / Agent Framework middleware, CrewAI memory and knowledge sources, Mastra workflows and memory. Vercel AI SDK middleware and smolagents executors were fetched and included.