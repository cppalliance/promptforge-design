---
produced: 2026-09-30
title: how agent harnesses, frameworks, protocols, workflow engines and runtimes let a parent agent introspect spawned subagents - cursor reads, event streams, final-result-only, file channels - compared with PromptForge tasks.events
---

# Introspecting spawned subagents: hosts read the child's history, models get its final answer

- Type: research survey, first pass 2026-09-30, verified against primary sources 2026-10-01
- Question: how do other systems let a parent agent, or the code driving it, inspect the subagents it spawned, while they run and after they finish?
- Compared against: PromptForge `tasks.events` and the model's `task_events` built-in
- Coverage: eight research passes, 99 system sections and two pattern studies (a section sometimes groups a product family)
- Verification: six independent checkers re-checked 120 claim items, and I fetched five hosted pages the first pass could not reach

## Abstract

The survey found no system that gives a parent model an incremental, access-checked read of a child agent's event history. That combination is what `task_events` gives a PromptForge model. For code, the picture differs. When Lua or host code reads a child's history, `tasks.events` matches a well-established design: a cursor read on an append-only log that the host stores.

Prior art splits by audience. Host code and human viewers get the full child history, by cursor, page token, or push stream. The parent model gets the child's final message or a status. The few exceptions return summaries, not events.

Two model-facing poll tools have been withdrawn. opencode removed its `task_status` tool 11 days after adding it. Claude Code deprecated and later removed `TaskOutput`, and a closed feature request was titled "Subagent's TaskOutput should return final result text, not full JSONL log". Codex's V2 `wait_agent` returns no content, yet one commenter on an open issue measured about 117,000 input tokens per wait. These reports mark the risk a model-facing `task_events` must design against: size and polling cost.

Three precedents fit an engine that emits events and a host that owns storage. The Claude Agent SDK `SessionStore` is a host-owned store with two required methods. Dagster's `get_records_for_run(run_id, cursor)` returns records, a cursor, and `has_more`. DBOS records every stream read made from workflow code as a step, so replay sees the same values.

It is very likely that no widely used open-source system ships the same combination as `task_events`. Confidence: medium, because the researchers could not read most hosted documentation sites and judged closed-source products from changelogs, issues, and documentation mirrors.

A second pass re-checked 120 claim items against primary sources. Ninety held as written, 29 needed correction, none was contradicted, and one could not be verified. This version applies every correction, and Table 5 lists them.

## Question

`tasks.events(task, {last})` returns a task's reported events as plain Lua tables, in sequence order. The value `last` is the highest sequence number the reader already saw, so a repeat call returns only newer events. The engine keeps no history. The host answers each read from its own log (`promptforge/crates/promptforge-internal/engine/src/execute/scheduler/task_events.rs`).

Lua code may read tasks it started, and a task may read itself. The model's `task_events` built-in may read only tasks the model started. The model receives one JSON event per line, wrapped as untrusted text under the run's nonce (same file). The engine records the host's answer, which copies every event returned (`promptforge/crates/promptforge/src/effect.md`).

This report uses four terms. The parent spawns a child, meaning a subagent or task. A reader is whoever inspects the child: the model, Lua or host code, or a person. Host code is the code of the application that embeds a runtime. A cursor is any value that names a position in a child's history, including a sequence number, an item id, or a page token.

## Method

Eight researchers each covered one family: the Claude products, OpenAI systems, the LangChain family, Python multi-agent frameworks, coding-agent harnesses, workflow engines, non-AI runtimes and log systems, and protocols with observability tools. Each answered five questions per system: how the child launches, what the parent can see, by what mechanism, whether the model can read it, and what maintainers or users say about it.

Web search and web fetch refused all eight researchers ("Interaction not available to subagent"). They read GitHub source at named commits, in-repo documentation, issues, and pull requests through read-only `gh` calls instead.

A second pass followed. Six independent checkers re-read the primary sources for 120 claim items and did not rely on the first pass's notes. Their counts were 21 of 25, 8 of 11, 22 of 25, 4 of 9, 12 of 20, and 23 of 30 items confirmed as written. I separately fetched five hosted pages: the Claude Code subagent documentation, the Claude Agent SDK subagent documentation, the MCP Tasks extension specification, OpenAI's background-mode guide, and Anthropic's multi-agent research post.

Every claim below passed this check unless the text marks it second-hand, meaning it rests on a user's report of what they saw, not on code or documentation.

## Results

### The parent model usually gets a final message or a status

Table 1 summarizes each family. In every family that involves a model, the model-facing column is thinner than the host-facing column.

*Table 1. What each family lets a parent model read of a child, and what it gives host code. Counts are system sections in the researchers' notes. Cells were re-checked in the second pass.*

| Family (sections) | Parent model can read | Host code and viewers can read |
|---|---|---|
| Claude products (9) | The final message plus a completion push; a child's transcript file, or a background child's output file, through `Read` | Hook events tagged with `agent_id` (since version 2.1.69); streamed messages tagged with `parent_tool_use_id`; `get_subagent_messages(limit, offset)`; a per-child event log by opaque page cursor in the Managed Agents API |
| OpenAI systems (9) | Status and final text; the V2 `wait_agent` tool returns no content | Codex `thread/items/list` with an exclusive "after" anchor; Agents SDK `on_stream` push; Responses `starting_after`; Agents API `after` ids |
| LangChain family (10) | The final message; an async status tool; supervisor `full_history` (default `last_message`) merges child messages into one list | Namespaced streams; `get_state(subgraphs=True)`; `get_state_history`; the Agent Streaming Protocol `since` cursor |
| Python frameworks (14) | Text only: the final answer, the last message, or all child messages joined, depending on a setting; shared-transcript frameworks have no parent-child read | `run_stream`; event handlers; CrewAI's event record; ADK `after_timestamp`; AG2 `History.get_events()` |
| Coding harnesses (14) | A final result in most; Goose and the Cline SDK also return progress summaries; Aider and Plandex have no subagent concept; Amp is unverified | opencode `/sync/history`; OpenHands `start_id` and `page_id`; Gemini CLI `subscribe` |
| Workflow engines (14) | Not applicable; none is model-aware | Id, result, cancel, and signal from parent code; page-token or cursor reads for outside clients; DBOS and Dagster allow a rich read from code |
| Non-AI runtimes (10, plus 2 pattern studies) | Not applicable | Outcome or exit reason, plus a live snapshot of running children; history only from opt-in tracing or logging, such as Erlang's `sys:log` (last 10 events by default), Go's execution trace, and tokio-console's bounded window |
| Protocols and observability (19) | The final report; vendor MCP servers over trace backends, scoped by API key | A2A `GetTask` and events; MCP `tasks/get` snapshot; AG-UI tagged stream; trace APIs |

Four systems go beyond a result string for the model, and none returns events. Goose's `load(source, peek: true)` returns elapsed time, turn count, idle time, and a buffered tool-call count. Goose also injects a "Background tasks:" digest into each parent turn, except when the model's context limit is below 32,000.

The Cline SDK's `team_list_runs` returns `lastProgressAt`, `currentActivity`, and a result preview cut to 400 characters. Its `team_read_mailbox` takes `unreadOnly` and marks what it returns as read, a server-side marker that works as a cursor. Magentic-One has its orchestrator model write a JSON progress ledger each round from a shared transcript that holds the workers' final messages. Agno gives the model a shared task list with results and notes.

### Two model-facing poll tools were withdrawn, and a third returns no content

opencode merged a `task_status` polling tool in [PR 27084](https://github.com/anomalyco/opencode/pull/27084) on 2026-05-14. It merged [PR 29179](https://github.com/anomalyco/opencode/pull/29179), "remove the need for polling from experimental background agents", on 2026-05-25. Background subagents now post a synthetic completion message to the parent, and the task tool text says "DO NOT sleep, poll for progress, ask the task for status".

Claude Code's changelog shows version 2.1.83 as "Deprecated `TaskOutput` tool in favor of using `Read` on the background task's output file path". Version 2.1.277 reads "Removed the deprecated TaskOutput tool" ([CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md)). A closed feature request, [issue 16789](https://github.com/anthropics/claude-code/issues/16789), is titled "Subagent's TaskOutput should return final result text, not full JSONL log". Its opening report concerns a subagent reading another agent's output. A later comment, written against version 2.1.22, describes the full log flooding the main agent's context.

Codex's V2 `wait_agent` description says it "Does not return the content; returns either a summary of which agents have updates (if any), an interruption summary for steered input, or a timeout summary" ([source](https://github.com/openai/codex/blob/da2e174a66a6572204a91373321b7d22d87fb12e/codex-rs/core/src/tools/handlers/multi_agents_spec.rs)). On [issue 35108](https://github.com/openai/codex/issues/35108), still open, a commenter measured 6,787,563 input tokens across the polling turns, "about 117k input tokens per wait on average". Mastra users reported that full child tool results reach the parent's context (issues 15823 and 15436, both closed). Issue 24160 reports storage amplification across nested delegation instead.

### Hosts read the full history, and the usual pull is a cursor on an append-only log

Table 2 lists the cursor shapes found. Fourteen of the sixteen rows read an ordered history from a position the reader supplies. A2A and MCP return a snapshot or a bounded tail instead.

*Table 2. How host code reads a child's or run's history, by cursor shape. The last column records the second-pass result.*

| System | Read | Cursor | Check |
|---|---|---|---|
| Redis Streams | `XREAD` | Entry id; returns only ids "greater than the one we specified", so exclusive | Confirmed |
| OpenAI Responses background mode | Stream resume | `starting_after` a `sequence_number`, which the guide calls a "cursor"; a user's pasted error said "more than 5 minutes old" | Confirmed |
| opencode | `POST /sync/history` | `{aggregateID: lastSeq}`; returns events with a greater per-session integer sequence | Confirmed |
| Agent Streaming Protocol (LangGraph) | Stream resume | `since` in the request; `seq` is optional and monotonic; servers "may keep a ring buffer" and should report a miss so the client can "resync through state commands" | Corrected |
| Codex app server | `thread/items/list` | Opaque cursor, or an item anchor that "resumes exclusively after that item" and needs a non-empty `turnId` | Confirmed |
| OpenAI Agents API | `subagents/{id}/items` | `after` id; `order=asc` must be set because the default is `desc` | Confirmed |
| Temporal and Cadence | `GetWorkflowExecutionHistory` | `next_page_token`, with a long poll (`wait_new_event` in Temporal, `wait_for_new_event` in Cadence); the public API has no "after sequence N" argument | Corrected |
| AWS Step Functions | `GetExecutionHistory` | `nextToken`, which expires after 24 hours | Confirmed |
| Airflow | Task log read | Signed `continuation_token` | Confirmed |
| DBOS | `read_stream(workflow_id, key, offset)` | Integer offset; a read from workflow code is recorded as a step | Confirmed |
| Dagster | `get_records_for_run(run_id, cursor, ...)` and `watch(run_id, cursor, callback)` | String cursor; returns records, cursor, and `has_more` | Confirmed |
| Google ADK | `GetSessionConfig(after_timestamp)` | Float timestamp, an inclusive `>=` filter, over a pluggable session service | Confirmed |
| Claude Agent SDK | `get_subagent_messages(limit, offset)` | Offset and limit | Confirmed |
| Claude Managed Agents | Per-child thread events | "Opaque cursor for the next page" | Corrected |
| A2A | `GetTask` with `history_length` | At most N recent messages; no cursor | Confirmed |
| MCP Tasks | `tasks/get` | Whole-state snapshot; no history | Confirmed |

OpenAI's guide says to "keep track of a 'cursor' corresponding to the `sequence_number` you receive in each streaming event", and that background responses from Zero Data Retention projects are "temporarily stored to disk for roughly 10 minutes to enable asynchronous execution and polling" ([guide](https://developers.openai.com/api/docs/guides/background)).

Protocol maintainers say the cursor is the missing piece. A2A [epic 1986](https://github.com/a2aproject/A2A/issues/1986), open since 2026-06-25, lists two criteria: events "carry a monotonic, per-task sequence/generation number", and `SubscribeToTask` "accepts a last-seen cursor and has defined replay-or-gap semantics". A2A [epic 1991](https://github.com/a2aproject/A2A/issues/1991), also open, covers gaps in task history and querying. MCP [issue 3237](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3237), open since 2026-08-14, is titled "Tasks extension (SEP-2663): no interoperable surface for partial output of a running task". It proposes a `task-log://{taskId}` resource, and one part of the proposal is a monotonic sequence number so a reconnecting client resumes without gaps.

Dagster's code shows the same shape in full. Its storage API returns `EventLogConnection(records, cursor: str, has_more: bool)` and defines `watch(run_id, cursor, callback)` as the push form ([base.py at d802ff7](https://github.com/dagster-io/dagster/blob/d802ff733482a864d29fd35f78d756c504812e91/python_modules/dagster/dagster/_core/storage/event_log/base.py)). The `get_logs_for_run` docstring says "Legacy support for integer offset cursors". Integer cursors still work with a deprecation warning, and string cursors are base64 JSON that can hold an offset or a storage id.

### The host often owns the storage behind a small interface

The Claude Agent SDK `SessionStore` is the closest match (read at commit db750b20 of the Python SDK). It requires two methods, `append` and `load`, and probes the optional ones at run time. Child transcripts sit under separate keys, `subagents/agent-<id>`. The `uuid` field is an idempotency key. A failed append gets up to three attempts in all, then is dropped with a `mirror_error` message while the run continues. Flush runs per turn by default, or eagerly for near real time.

Other host-owned stores exist. Google ADK reads through a pluggable `BaseSessionService`. Dagster defines the run log behind an abstract storage class. IBM's archived ACP had a pluggable `Store` for memory, Redis, or PostgreSQL. Inngest AgentKit takes a host-supplied history adapter, and Mastra's background-task manager requires a configured storage backend.

The OpenAI Agents SDK keeps no history in its tracing: tracing processors receive traces and spans, and the Cookbook shows a host writing spans to JSONL. The SDK does keep conversation history, through Sessions. Codex always writes rollout files and, when `CODEX_ROLLOUT_TRACE_ROOT` is set, an append-only `trace.jsonl` with a writer-assigned `seq`.

The opposite design is a store whose schema the product defines. Temporal, Inngest, DBOS, and Hatchet keep history in a database that the operator or application provisions, and Restate ships a built-in replicated log. In each, the application does not implement the storage interface.

### Several systems give the model and the host separate channels

Seven systems split the model's view from the host's view of the same child, and one Deep Agents issue discusses the same split:

- AG2 sends the parent stream only lifecycle events and one usage rollup. The child's full history sits on its own stream in shared storage. The `TaskProgress` event type is marked transient, though AG2 v1.1.1 subagent tools never emit it; only `Task.progress()` does.
- Google ADK, in shared-session mode, records child events in the session log and drops events whose `branch` or `isolation_scope` do not match when it builds the model's prompt. The log itself stays unfiltered. Classic `AgentTool` forwards no child events at all.
- OpenHands V0 keeps child events in the parent's single log and drops everything between the delegate action and its observation from the parent's prompt history.
- Gemini CLI returns `llmContent` to the model and `returnDisplay`, the last three activities, to humans.
- A Vercel AI SDK tool can set what the model sees with `toModelOutput`, while the interface receives the full `UIMessage`. Without `toModelOutput`, the whole tool result goes to the model as JSON.
- Zed's tool call holds `{session_id, message_start_index, message_end_index}`. The code comment says "Don't show this to the model", and only the index range is hidden: the model still receives the `session_id` and the output.
- Claude Managed Agents shows a "condensed view" on the session stream and keeps each child's full log on its own thread.
- Deep Agents [issue 2512](https://github.com/langchain-ai/deepagents/issues/2512), open, asks to preserve a subagent's full content. A maintainer proposes the split: `ToolMessage.content` for the model and `ToolMessage.artifact` for code.

### Some systems avoid a pull read altogether

Table 3 lists ten designs that give the parent no cursor read. Anthropic describes the file pattern in its research system: "Subagents call tools to store their work in external systems, then pass lightweight references back to the coordinator" ([post](https://www.anthropic.com/engineering/multi-agent-research-system), published 2025-06-13). The same post says its lead agents run subagents synchronously, so "the lead agent can't steer subagents, subagents can't coordinate, and the entire system can be blocked while waiting for a single subagent to finish searching". It names "full production tracing" as the way its engineers diagnose failed agents.

Claude Code's documentation says subagent transcripts are stored at `~/.claude/projects/{project}/{sessionId}/subagents/agent-{agentId}.jsonl`. The Agent SDK documentation says "The parent receives the subagent's final message verbatim as the Agent tool result" ([Claude Code docs](https://code.claude.com/docs/en/sub-agents), [SDK docs](https://code.claude.com/docs/en/agent-sdk/subagents)). A changelog entry adds that background completion notifications include an output file path. Users pasted that path in issues 39791 and 96956, and the subagent documentation does not describe it, so this part is second-hand.

*Table 3. Designs that give the parent no cursor read of a child. All rows were re-checked; corrections are applied.*

| Design | Example | How the parent reads | Reported cost |
|---|---|---|---|
| File as channel | Claude Code background child; the Anthropic research system | `Read` or `tail` on an output file, or a reference to an artifact | Users report files missing before the parent read them (issue 19295), lost after compaction (23821), and uncapped at about 190 GB per file (47771); none has a maintainer reply |
| Tagged push into one stream | AG-UI `subagentRunId`; OpenAI hosted multi-agent `agent.agent_name` | No per-child read; the reader filters one multiplexed stream | No per-child read |
| Announce, then push | Agent Client Protocol subagent RFD (draft, behind `unstable_subagents`) | Events "flow automatically"; no attach, subscribe, or history method; an explicit `unknown` state | A late reader cannot catch up |
| Whole-state snapshot | MCP `tasks/get`; A2A `GetTask` | One status with a result, or a bounded tail of messages | No history; issue 3237 and epic 1986 ask for one |
| Checkpoint as history | LangGraph `get_state_history` | Newest first with a `before` cursor | The cursor runs backward, opposite to `last` |
| Model-written ledger | Magentic-One | The orchestrator fills a JSON progress ledger each round | Progress is a model's judgment, not a recorded fact |
| Child writes into parent state | Trigger.dev `metadata.parent.set` | The parent reads its own metadata | A metadata blob with `append`, not an ordered event log; any code can read another run's metadata with `runs.retrieve()` |
| Child writes a file, parent tails it | Dagster Pipes | A `message_reader` tails the file | The child must cooperate |
| Mailbox files | Claude agent teams | Mailbox files, a shared task list, and an idle notice with the teammate's final answer | No model-facing transcript read |
| Separate process polled by CLI | Claude `claude agents` view; a Continue prompt file that runs `cn -p` as a background job | JSON from a command-line tool; Continue's `CheckBackgroundJob` tool | No cursor in the agent view; Continue has no built-in background subagent |

### A read inside a deterministic run must be recorded

DBOS states the rule most directly: "When called from workflow code, each value read is checkpointed to the database as a step, so a replayed workflow re-yields the values it originally read instead of re-reading a stream that may have advanced since" ([docs at 4069d9a](https://github.com/dbos-inc/dbos-docs/blob/4069d9abef31caa9981caacf2c3cf776cb05542b/docs/python/reference/contexts.md)). Temporal's Workflow Streams take another route. Their documentation says "Subscribing from inside the Workflow that hosts the stream isn't supported", while subscribers elsewhere, such as Activities of other Workflows, can read. For Updates to another workflow, Temporal's documentation routes the call through an Activity.

### AI systems rarely limit who reads whom, and runtimes limit it at the handle

No AI system surveyed enforces "a parent reads only the children it spawned" at the API. The nearest case is Deep Agents' async tools, which resolve ids only from the model's own `async_tasks` state and answer "No tracked task found" otherwise.

MCP's Tasks extension has no `tasks/list`. Its specification says "Because there is no `tasks/list`, a server cannot inadvertently leak the existence of one caller's tasks to another". It requires task ids with enough entropy that "a third party cannot enumerate or guess them", and an authorization check on every task request ([specification](https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks)).

Observability servers vary. The Langfuse and Phoenix MCP servers let an agent query traces across a project, and Phoenix keys are not project-scoped. The AgentOps server reads one trace or span by id within the key's project and has no list or search tool.

Runtimes enforce ownership at the handle. Elixir's `Task` raises unless the caller is the owner. A Java structured-concurrency scope lets only the owner thread fork and join. Linux `wait` returns `ECHILD` for a non-child. The Yama setting (`ptrace_scope` mode 1) allows `ptrace` only on descendants unless the observed process names another process with `PR_SET_PTRACER`, and root is exempt. Linux `hidepid=2` hides another user's `/proc/<pid>` entry, and the kernel documentation adds that existence "can be learned by other means, e.g. by kill -0 $PID".

On trust, Claude Code scans each subagent's final report before the parent reads it. The scan inserts a backslash into text that imitates Claude Code's own tags and prepends a `[harness: subagent output matched instruction-shaped pattern(s):` marker line (documentation, version 2.1.210 or later). The documentation adds that the scan does not judge whether content is malicious. Version 2.1.277 also delivers subagent results "under a header marking them as subagent output, with the result indented, so text in a subagent's result cannot pass as the session's own instructions" (changelog).

Mastra wraps referenced child text in "a fresh, unpredictable tag", but only when `enableResultReferences` is on, and the next subagent reads that text, not the parent model. The MCP specification applies the standard trust model to `inputRequests` payloads and adds "A task is not a higher-trust channel". Tool texts lean the other way. The opencode task text says "The agent's outputs should generally be trusted", and the Cursor Task tool text, read in this session, says "The subagent's outputs should generally be trusted". The OpenHands task tool says "The agent's results are authoritative".

### Users report six recurring problems

Table 4 groups the problems by what a reader of a child's history needs.

*Table 4. Recurring user reports about child visibility, with what each implies. All rows were re-checked; corrections are applied.*

| Problem | Where reported | Implication |
|---|---|---|
| A reader cannot tell which child produced an event | Claude hook issues 7881 (2025-09-19), 14859, and 29068, until version 2.1.69 added `agent_id` on 2026-03-05; Codex issue 44095 asks for a `spawn_tool_use_id`; Deep Agents issues 876 and 1355 | Stamp each event with its task and parent task, and make the spawn site joinable to the child id |
| Child output floods the parent's context | Claude issue 16789; Mastra issues 15823 and 15436; Microsoft Agent Framework issue 2796, which asks for a `return_mode`; smolagents issue 2424 | Cap the model-facing size and flag truncation |
| Polling burns tokens | Codex issue 35108 | Prefer a blocking wait or a push over repeated reads |
| A terminal event is missing or mismatched | Claude `SubagentStop` reports, issues 89555 and 78463 | Let a reader detect "ended" from the log itself |
| Token totals are wrong across nested runs | AG2 ADR 0014 (110 of 1,100 tokens counted, and double counts); CrewAI issue 7259; PydanticAI issue 6886; ADK issue 4377 | Record per-round deltas, and never sum a cumulative field |
| History is lost or expires | Responses stream replay; the Agent Streaming Protocol's ring buffer; Claude output files reported missing (issue 19295) | Define retention and the answer for a trimmed or unknown position |

## Discussion

The results support seven judgments about `tasks.events`. Each states a likelihood or a recommendation, and a separate confidence.

### The Lua read follows prior art, and the model read departs from it

Lua is a code reader, and code readers have strong precedent. Dagster, DBOS, CrewAI, ADK, and AG2 all let code read a child's history, and several do it by cursor (Tables 1 and 2). The model reader has almost none: no surveyed system gives a parent model an incremental event read, and two that gave it a poll tool removed it. I recommend deciding the two readers separately. Keep the Lua read as designed. Keep the model read, but constrain it as the next judgment describes. Confidence: high for the Lua read, because five shipped systems let code read a child's history. Confidence: medium for the model read, because the evidence is about other designs, not this one.

### The model read needs a size cap and a steer toward waiting

The reports behind the withdrawn and reworked tools concern size and polling cost (Table 4). It is likely that an uncapped or often-polled `task_events` would reproduce those reports. PromptForge differs in two ways that help: the read is incremental by `last`, and `await_tasks` already gives a blocking wait. Four additions are worth weighing, in this order. First, a per-read `limit`. Second, a size cap with a `truncated` flag, as PydanticAI's harness does on the events it emits, with a 4,096-character cap; its delegate tool still returns the full output to the model. Third, a liveness summary cheaper than events, such as Goose's idle time and Cline's `lastProgressAt`, so the model does not read events only to learn whether a task is stuck. Fourth, tool text that steers the model to `await_tasks`, as opencode's text does with "DO NOT sleep, poll for progress, ask the task for status". Confidence: medium, because the reports describe tools unlike `task_events`, and PromptForge's cursor may already remove most of the cost.

### The cursor contract should state its edge cases

Redis returns ids "greater than the one we specified", so its cursor is exclusive, as `last` is. Pekko's `eventsByPersistenceId` is inclusive, and its tag queries may re-deliver an event. ADK's `after_timestamp` is an inclusive `>=` filter on a float, so a reader sees the boundary event again; an integer sequence avoids that.

The docs for `last` should say plainly that it is exclusive and that sequence numbers are dense and per task. They should also say what a read returns when `last` is ahead of the log or the host has trimmed older events. Kafka raises an out-of-range error, and tokio-console reports a `dropped_events` count. An explicit marker such as "events before sequence N are gone" would keep a model from assuming it holds the whole history. Dagster's string cursors replaced integer offsets, and integer cursors still work with a deprecation warning. The docs should therefore call `last` a sequence number that the host maps to its own storage position. Confidence: high that stating exclusivity costs nothing. Confidence: medium for the gap marker, which is my inference from the prior art, not a shipped design.

### A host-owned log needs idempotent append, a failure rule, and an attempt marker

The `SessionStore` shows what a minimal host contract has to say: an `append` that tolerates redelivery through an idempotency key, a rule for failed writes, and a flush cadence. Observers differ on failure. PydanticAI says a listener that raises aborts the parent run, while AG2's `TaskMirror` swallows hub errors so it "must never crash the agent's turn". Pick one rule and document it.

If a task can be retried, give each event an attempt marker. Temporal's documentation says a stream subscriber "sees output from all attempts" of a retried Activity. PromptForge already records the host's answer to each read, which is the DBOS rule, so replay sees the same events. That record copies every event returned, so history reads grow the log (`effect.md`). A per-read `limit` also bounds that growth. Confidence: medium, because the growth matters only for long runs with frequent reads.

### The access rule exceeds prior art, and the engine already hides unowned ids

No AI system surveyed limits child reads to the spawner, and the closest precedents are runtime handles and Linux `ptrace` rules. The Linux lesson is that hiding a process from listings does not hide its existence. The engine already follows it: an id naming no task "is refused the same way as one the caller does not own, so a caller learns nothing about tasks it never started" (`task_events.rs`). It is very likely that this rule is uncommon among agent systems. Confidence: medium, because absence was judged from sources the checkers read, not from an exhaustive search.

### The trust wrapper matches the field, and three refinements are worth weighing

Claude Code, Mastra, and the MCP specification all mark someone else's text as such, and PromptForge does too, under the reader's run nonce (`task_events.rs`). Three refinements come from the reports. A fresh delimiter for each read, as Mastra uses, would shrink the window if a child ever sees an earlier wrapped read; this is my reasoning, not a reported bug. Engine-written entries, such as "task ended" or "cancelled by parent", could get a different tag from child-written text, as PydanticAI [issue 8995](https://github.com/pydantic/pydantic-ai/issues/8995) proposes; it is an idea issue that says "no commitment implied". Truncation must not strand the reader: Claude [issue 90544](https://github.com/anthropics/claude-code/issues/90544) reports a flagged report clipped to about 2,500 characters, with a repair path that re-ran the child, and later commenters measured about 4,000 characters on the teammate idle-notification path. A truncated read should therefore say how to continue from the cursor. Confidence: low to medium, because two of the three rest on single reports or my own inference.

### Each alternative to a model-facing event read gives up the "what happened" view

The credible alternatives are five. A final result only is the norm, and it keeps context small. A file channel is simplest, and its failure modes are missing files, loss at compaction, and no size cap (Table 3). A push, as in Goose's digest and opencode's completion message, stays small when the pushed text is small, but Mastra users reported large pushes that cost context the model did not need. A model-written ledger records a judgment, not a fact. A status snapshot, as in MCP and A2A, has no history. None gives a reader the "what happened" view that the guide's chapter on task events promises Lua authors: checking what a task did, adding up what its model calls cost, and following a long task while it runs. Doing nothing, meaning Lua-only reads, is the safest option and keeps the strongest precedent. Its cost is that a model cannot audit the tasks it spawned. Confidence: medium, because the value of that audit to a model is untested.

## Verification

The second pass checked 120 claim items. Ninety held as written, 29 needed correction, none was contradicted, and one could not be verified. The unverifiable item is the date IBM's ACP repository was archived, which GitHub does not expose; this report states no date for it. Table 5 lists the corrections, in the order they appear above.

*Table 5. Corrections the second pass made to the first draft.*

| First draft said | Primary source says | Where |
|---|---|---|
| Claude users asked for `agent_id` "for years" | Asked from 2025-09-19 (issue 7881); version 2.1.69, published 2026-03-05, added it | Table 4 |
| Hook and stream events are tagged with `agent_id` | Hooks include `agent_id`; streamed messages include `parent_tool_use_id` | Table 1 |
| Managed Agents use an "opaque forward-only page token" | The thread events call returns an "Opaque cursor for the next page"; "forward-only" is on the thread list call | Table 2 |
| Issue 90544 clips a report at about 2,500 characters | Later commenters measured about 4,000, on the teammate idle-notification path | Discussion |
| Agent Protocol v3 has a strictly increasing `seq` | `seq` is optional and monotonic; "v3" names LangGraph's `stream_events(version="v3")` | Table 2 |
| Issues 2512, 876, and 1355 are in LangChain or LangGraph | All three are in `langchain-ai/deepagents`; the content and artifact split is a maintainer's proposal | Channels, Table 4 |
| The Agents SDK "keeps no history at all" | Its tracing keeps none; Sessions keep conversation history | Storage |
| ADK hides child events "at read time" | It hides them when building the model's prompt; classic `AgentTool` forwards none | Channels |
| Python frameworks return "a string, the final answer or the last message" | AutoGen's default joins every non-user message; behavior varies by setting | Table 1 |
| Cline's `team_read_mailbox` takes `markRead` | The schema has only `unreadOnly`; the code marks reads itself | Results |
| Zed hides session information from the model | It hides the index range; the model still receives `session_id` | Channels |
| Continue has a background subagent the parent polls | A prompt file runs `cn -p`; a separate `CheckBackgroundJob` tool reads it | Table 3 |
| opencode, Cursor, and OpenHands all say child output "should generally be trusted" | The phrase is in opencode and Cursor; OpenHands says "authoritative" | Access |
| Coding harnesses return "one result string in all but two" | Aider and Plandex have no subagent concept; Amp is unverified | Table 1 |
| Temporal's call is `GetWorkflowHistory` | It is `GetWorkflowExecutionHistory`; Cadence's long-poll field is `wait_for_new_event` | Table 2 |
| Workflow Streams "refuse in-workflow subscription" | Only subscription from the hosting workflow is unsupported | Deterministic reads |
| Trigger.dev metadata is "latest value only, no log" | `metadata.parent` also has `append` | Table 3 |
| Dagster "moved from integer offsets to string cursors" | Integer cursors still work with a deprecation warning | Table 2 text |
| Five engines keep the log "in their own databases" | Only Restate ships its own; the others use a database the operator or application provisions | Storage |
| Linux `hidepid=2` "hides contents but not existence" | It hides the whole entry; existence leaks through `kill -0` | Access |
| Erlang has history "only in separate tools" | `sys:log` is in the standard library and any process can read it | Table 1 |
| MCP says "it is unsafe for a server to support `tasks/list` at all" | That wording is not on the specification page I read; the page says "Because there is no `tasks/list`..." | Access |
| Observability MCP servers give "project-wide read" | AgentOps reads one trace or span by id; Phoenix keys are not project-scoped | Access |
| Mastra issue 24160 is about child results in the parent's context | It reports pubsub and storage amplification | Withdrawn polls |
| PydanticAI's 4,096-character cap limits what the model reads | The cap applies to the event copy; the delegate tool returns full output | Discussion |
| Temporal and DBOS readers both see every attempt | Confirmed for Temporal only | Discussion |
| Goose injects a digest into each parent turn | It skips the digest when the model's context limit is below 32,000 | Results |
| Responses replay "expires" | The guide says Zero Data Retention data is kept roughly 10 minutes; "5 minutes" is a user's pasted error | Table 2 |
| MCP issue 3237 asks for a monotonic sequence number | That is one part of a `task-log://{taskId}` resource proposal | Table 2 text |
| PydanticAI issue 8995 proposes a design | It is an idea issue that says "no commitment implied" | Discussion |

## Limitations

- **Researchers had no live web.** Web search and fetch refused all eight first-pass researchers and all six checkers. I fetched five hosted pages myself. Hosted pages still unread include the other OpenAI developer guides, the platform documentation for Claude Managed Agents, and the Letta, Braintrust, Langfuse, and Phoenix references. Two third-party mirrors, `ericbuess/claude-code-docs` at 663ff198 and `thevibeworks/claude-code-docs` at 2afa0f0e, stood in for Managed Agents documentation.
- **Closed-source products.** Claude Code internals are judged from its changelog, documentation, and issues. Cursor is judged from its tool text, and Amp's subagent readback was not verified.
- **User reports without maintainer replies.** Claude issues 19295, 23821, 47771, 89555, 78463, and 90544 record what users saw. The word "deleted" in issue 19295 is the reporter's inference.
- **No code was run.** Every behavior claim comes from source, documentation, or issue text.
- **Gaps in the notes.** Fuchsia is unverified and from memory. Akka was not read directly; Pekko was. The JEP 453 text was not fetched; the Javadoc was read. The commit references for Temporal's `sdk-python` tag and Dagster's 1.13.24 tag in the first-pass notes were off; the cited file text matches the commits named here.
- **Leads not opened.** The DeepSeek Harness subagent design that PydanticAI issue 8995 adapts; Microsoft Agent Framework ADR 0024 on prompt-injection defense; the `prompt_injection_defender` capability in pydantic-ai-harness; the Codex Desktop `codex_app.read_thread` tool, known only from issue text; and how a client tails an open Temporal workflow.

The first-pass evidence and the checkers' verdicts, with quotes, URLs, and commits for the 99 sections, sit in working files and can be promoted on request.

## References

Hosted pages fetched for this report:

- Claude Code [subagent documentation](https://code.claude.com/docs/en/sub-agents) and [Agent SDK subagent documentation](https://code.claude.com/docs/en/agent-sdk/subagents)
- [MCP Tasks extension specification, 2026-07-28](https://tasks.extensions.modelcontextprotocol.io/specification/2026-07-28/tasks)
- OpenAI [background mode guide](https://developers.openai.com/api/docs/guides/background)
- Anthropic, ["How we built our multi-agent research system"](https://www.anthropic.com/engineering/multi-agent-research-system), 2025-06-13

Claude and OpenAI:

- Claude Code [CHANGELOG](https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md) (2.1.69, 2.1.83, 2.1.277) and issues [7881](https://github.com/anthropics/claude-code/issues/7881), [14859](https://github.com/anthropics/claude-code/issues/14859), [16789](https://github.com/anthropics/claude-code/issues/16789), [29068](https://github.com/anthropics/claude-code/issues/29068), [90544](https://github.com/anthropics/claude-code/issues/90544)
- Claude Agent SDK [`types.py` at db750b20](https://github.com/anthropics/claude-agent-sdk-python/blob/db750b20a88ae9645b1674d95193a88c89a265f9/src/claude_agent_sdk/types.py) and Anthropic SDK [`threads.py` at 18f25547](https://github.com/anthropics/anthropic-sdk-python/blob/18f25547f20cf5f01da69ac611e700e3bc9ebf21/src/anthropic/resources/beta/sessions/threads/threads.py)
- Codex [`multi_agents_spec.rs` at da2e174](https://github.com/openai/codex/blob/da2e174a66a6572204a91373321b7d22d87fb12e/codex-rs/core/src/tools/handlers/multi_agents_spec.rs), [issue 35108](https://github.com/openai/codex/issues/35108), and [openai-python issue 2828](https://github.com/openai/openai-python/issues/2828)
- OpenAI Agents SDK [sessions documentation at 28e9f4f](https://github.com/openai/openai-agents-python/blob/28e9f4fca26dd1c7e679398b87182868ecfad714/docs/sessions/index.md)

LangChain and Python frameworks:

- LangChain [Agent Streaming Protocol at fb81f3e](https://github.com/langchain-ai/agent-protocol/blob/fb81f3e27ee507557926ecf923d0f933a1c76d44/streaming/README.md) and Deep Agents issues [2512](https://github.com/langchain-ai/deepagents/issues/2512), [876](https://github.com/langchain-ai/deepagents/issues/876), [1355](https://github.com/langchain-ai/deepagents/issues/1355)
- ADK [`_contents.py`](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/flows/llm_flows/context/_contents.py) and [`agent_tool.py`](https://github.com/google/adk-python/blob/53b3706e04fab34d1d53808a5f62cfe9b025f893/src/google/adk/tools/agent_tool.py) at 53b3706
- AutoGen [`_task_runner_tool.py` at 83afbf5](https://github.com/microsoft/autogen/blob/83afbf5857aac683340d4c692194e548b1e8edda/python/packages/autogen-agentchat/src/autogen_agentchat/tools/_task_runner_tool.py), Strands [`_agent_as_tool.py` at 64a6862](https://github.com/strands-agents/sdk-python/blob/64a6862b8c3053368544a78d4c1c6c31d560d258/src/strands/agent/_agent_as_tool.py), Microsoft Agent Framework [issue 2796](https://github.com/microsoft/agent-framework/issues/2796), and PydanticAI [issue 8995](https://github.com/pydantic/pydantic-ai/issues/8995)

Coding harnesses:

- opencode [PR 27084](https://github.com/anomalyco/opencode/pull/27084) and [PR 29179](https://github.com/anomalyco/opencode/pull/29179)
- Cline [`team-tools.ts` at 8eee168](https://github.com/cline/cline/blob/8eee168b80127b0c94bad849323754b5864865e7/sdk/packages/core/src/extensions/tools/team/team-tools.ts), Zed [`spawn_agent_tool.rs` at 74c134a](https://github.com/zed-industries/zed/blob/74c134a3c12418cc095122fff938ef1c2504ae06/crates/agent/src/tools/spawn_agent_tool.rs), Continue [`checkBackgroundJob.ts` at 5522c6f](https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/tools/checkBackgroundJob.ts), OpenHands [`definition.py` at fad6377](https://github.com/OpenHands/software-agent-sdk/blob/fad63774459171b08f889b12fd3b4d6346168c3e/openhands-tools/openhands/tools/task/definition.py), and Aider [`architect_coder.py` at 5dc9490](https://github.com/Aider-AI/aider/blob/5dc9490bb35f9729ef2c95d00a19ccd30c26339c/aider/coders/architect_coder.py)

Workflow engines and runtimes:

- Dagster [`event_log/base.py` at d802ff7](https://github.com/dagster-io/dagster/blob/d802ff733482a864d29fd35f78d756c504812e91/python_modules/dagster/dagster/_core/storage/event_log/base.py), DBOS [contexts reference at 4069d9a](https://github.com/dbos-inc/dbos-docs/blob/4069d9abef31caa9981caacf2c3cf776cb05542b/docs/python/reference/contexts.md) and [FAQ](https://github.com/dbos-inc/dbos-docs/blob/4069d9abef31caa9981caacf2c3cf776cb05542b/docs/faq.md)
- Temporal [API protos at 46ee8b8](https://github.com/temporalio/api/blob/46ee8b820cff353e92fa8c9d052414d4e573feb7/temporal/api/workflowservice/v1/request_response.proto) and [Workflow Streams documentation at 6078cc6](https://github.com/temporalio/documentation/blob/6078cc666dac27afca38493d5ea5b64cce4e477f/docs/encyclopedia/workflow-message-passing/workflow-streams.mdx)
- Trigger.dev [metadata documentation at a7629e8](https://github.com/triggerdotdev/trigger.dev/blob/a7629e80908b4fc665d8e12d2f977d0ebda4c41c/docs/runs/metadata.mdx), Linux [`proc.rst`](https://github.com/torvalds/linux/blob/551c722f40809618230001baccf219193e22fc5a/Documentation/filesystems/proc.rst), and Erlang/OTP [`sys.erl` at ad05823](https://github.com/erlang/otp/blob/ad05823719d77c8faee87348ea39513d4e2f99c5/lib/stdlib/src/sys.erl)

Protocols and observability:

- A2A [epic 1986](https://github.com/a2aproject/A2A/issues/1986) and [epic 1991](https://github.com/a2aproject/A2A/issues/1991); MCP [issue 3237](https://github.com/modelcontextprotocol/modelcontextprotocol/issues/3237) and the [ext-tasks specification at 5246bc3](https://github.com/modelcontextprotocol/ext-tasks/blob/5246bc3d0253c1c4b09e682f690b7e8b97362500/specification/2026-07-28/tasks.md)
- AG-UI [subagents documentation](https://github.com/ag-ui-protocol/ag-ui/blob/release/2026-09-30/docs/concepts/subagents.mdx), AgentOps [`routes.py`](https://github.com/AgentOps-AI/agentops/blob/main/app/api/agentops/public/routes.py), Mastra [issue 24160](https://github.com/mastra-ai/mastra/issues/24160), Vercel AI SDK [`tool.ts` at ai@7.0.126](https://github.com/vercel/ai/blob/ai@7.0.126/packages/provider-utils/src/types/tool.ts), and VoltAgent [subagent source](https://github.com/VoltAgent/voltagent/blob/main/packages/core/src/agent/subagent/index.ts)

PromptForge: `promptforge/crates/promptforge-internal/engine/src/execute/scheduler/task_events.rs`, `promptforge/crates/promptforge/src/effect.md`, and `promptforge/guide/src/language/16-task-events.md`.

---

*2026-10-01 - Claude Sonnet 5.5 (Cursor agent). First pass from eight parallel research passes; second pass by six independent checkers, plus my own fetches of five hosted pages and my own source checks.*
