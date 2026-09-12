# The PromptForge Prompting Language

## Philosophy

PromptForge is a literate agent language. Markdown holds readable prompt material, while Lua decides when it becomes a message, when a model runs, which tools execute, how context compacts, and when a section finishes.

Every section entry is one isolated agent context. Its Lua VM survives across that entry, while fall-through, jump, call, and asynchronously called section targets receive fresh VMs with only explicit transfer channels.

The host supplies transport, model-tool continuation, confinement, events, cancellation, scheduling, and waits. Lua owns message construction and reshaping, compaction policy, interaction policy, orchestration, and result mediation.

## Current implementation scope

The active language work renames heading-based `execute` to synchronous `call` and `tool_call` to `tools.call`, adds pending Markdown capture with thematic-break reset and lazy `prose`, removes `reply`, and retains plain message arrays with optional `messages.new()` builders.

The active model runtime retains `models.infer`, adds Rust-backed `models.loop(handle?, messages, compactor?)`, implements the minimum compactor invocation surface with `compactors.fail` as the only policy, validates provider-neutral messages and correlated model-tool exchanges, and reads model and tool selection at call time. All host operations are namespace functions; handles are pure inspectable values with no methods, so there is exactly one way to invoke anything.

The active host work generalizes `user_input()`, adapts its model-visible tool, and preserves minimum Agent-window interaction. Only focused tests and migrations required by these changes are active.

Constructs described below are labeled active (changed by this plan), existing (shipped and unchanged), or deferred (a documented target contract that is inert in this plan). Deferral means no new runtime behavior, parser work, tests, benchmarks, prompt migration, compatibility removal, or public activation unless an active-scope paragraph states otherwise.

## Contents

1. [Current implementation scope](#current-implementation-scope)
2. [Source syntax](#source-syntax)
3. [Modules and prompt execution](#modules-and-prompt-execution)
4. [State and globals](#state-and-globals)
5. [Messages](#messages)
6. [Models](#models)
7. [Tools](#tools)
8. [Store](#store)
9. [Compaction](#compaction)
10. [Control flow](#control-flow)
11. [Host APIs](#host-apis)
12. [Events and persistence](#events-and-persistence)
13. [Errors and limits](#errors-and-limits)
14. [Recipes](#recipes)

## Alphabetical construct index

- A: `args`
- C: `call(heading, input?)`, `call_async(heading, input?)`, cold restore, deferred `compactor(messages, budget)`, `compactors.fail`, deferred `compactors.summarize(options)`
- D: `description`
- E: events, deferred `execute(path, input?)`, deferred `execute_async(path, input?)`
- F: deferred `fanout(section, inputs)`, frontmatter
- H: heading references
- I: `include`, incarnation, inherited Lua, `input`
- J: `jump(heading)`
- L: lifecycle, list sections, `list_from_section(heading)`, `local_include`, `log(message)`, `lua`, `lua inherit`
- M: deferred `markdown` namespace, `max_tool_iterations`, messages, `messages.new()`, `models.loop`, `models.bind`, `models.default`, `models.get`, `models.infer`, `models.use`
- N: `name`
- O: `output`
- P: deferred `pfanout`, `promptforge: 0`, `prose`, provider projection
- R: `require(path)`, `return`
- S: sections, snapshots, `store.append`, `store.delete`, `store.exists`, `store.glob`, `store.read`, `store.read_numbered`, `store.str_replace`, `store.write`, substitution, `sys`
- T: task handles, `tasks.await_all`, thematic break, `tools.add`, `tools["add_local"]`, `tools.always`, `tools.bind`, `tools.call`, `tools.calls`
- U: `ui()`, `untrusted(text)`, `user_input()`
- V: `var`

## Source syntax

This is a complete explicit prompt:

````markdown
---
name: greeting
description: Answer one request
promptforge: 0
---

# Greeting

```lua
models.bind("writer", "concise technical writing")
models.default("writer")
```

## Answer

Answer {{ args }}.

```lua
return models.infer(prose)
```
````

**Frontmatter.** The file starts with YAML containing `name`, `description`, and exactly `promptforge: 0`. Unknown keys fail.

Optional `input` and `output` declarations contain `path` and `description`. Optional `max_tool_iterations` is an integer from 1 through 1000 and defaults to 24.

**Sections.** Exactly one non-empty H1 follows the frontmatter. Text before it is inert preface. H2 through H6 headings form the section tree, levels cannot be skipped, and sibling names must be unique.

Fall-through follows source order. The H1 preamble resolves model and tool bindings and may return a scalar to finish the run. `call`, `call_async`, deferred `execute`, deferred `execute_async`, `jump`, and `list_from_section` are unavailable there.

**Pending prose and thematic breaks.** Each section heading starts an empty pending Markdown buffer. Markdown appends to that buffer.

Any thematic break recognized by the Markdown parser clears the buffer and is not included in `prose`.

Each ordinary Lua fence receives the remaining buffer as its fresh lazy `prose` value and clears the buffer before running. A Lua fence with an empty buffer sees `prose == nil`.

Section end discards any remaining buffer without error or model invocation, so trailing Markdown is naturally inert. Thematic breaks only reset prose capture; they never terminate calls, prevent fall-through, restrict trailing content, or become part of the prompt.

**Lua fences, deferred inheritance, and return.** Exact unindented ordinary `lua` fences execute in source order, and each ordinary fence is a separate coroutine in the same VM. Returning nil continues; returning a scalar finishes the current frame as text; returning a table, function, thread, or userdata fails. The documented deferred `lua inherit` contract forms a contiguous initialization prefix before ordinary executable prose or Lua, collects applicable blocks from the target and its ancestors, and executes them once in root-to-leaf source order on each fresh VM. No inheritance parsing, replay, tests, or migration is active in this plan.

**Prose capture.** Pairing is an implementation association, not a source-validity rule. Markdown before the most recent thematic break is commentary; Markdown after it is available to the next ordinary Lua fence. Unconsumed Markdown is inert, so prose without a following Lua fence is never an error. PromptForge runs no model implicitly. Deferred inherit fences do not consume pending prose.

**Substitution.** `{{ args }}`, `{{ var.key }}`, `{{ sys.key }}`, and a section-global name insert JSON-representable values. Dotted paths index nested data, tables render as compact JSON, and `\{{`, `\}}`, and `\\` escape delimiters and backslashes. The first runtime read of `prose` snapshots current section state, evaluates substitutions once, and memoizes the resulting string. Later reads in that fence return the same string even after state changes. Unread prose performs no substitution and raises no substitution error. Each later Lua fence receives and evaluates its own captured lazy value.

````markdown
First value: {{ var.value }}
```lua
var.value = "first"
first = prose
var.value = "changed"
assert(prose == first)
```

Second value: {{ var.value }}
```lua
second = prose
```
````

Missing, null, malformed, unavailable, or non-JSON values fail at the first read site and may be caught with `pcall`. Bare `{{ var }}`, bare `{{ sys }}`, and recursive `{{ prose }}` are invalid. Assignment to `prose` always fails. Empty output memoizes as the empty string.

**Deferred `markdown` namespace.** A future `markdown` table will give Lua direct access to the Markdown parser (for example `markdown.parse(text)`), following the same namespace convention as `models` and `tools`: namespace functions over plain values, no methods. It is a documented deferred target contract - no parser exposure, tests, or migration in this plan. `list_from_section` remains a control-flow global because it resolves a heading over the document's visible set rather than parsing text.

## Modules and prompt execution

### `require(path)`

**Effect:** Loads one trusted `.lua` module through PromptForge's sandboxed replacement for Lua's package loader. Resolution is relative to the source file containing the call, including when a `lua inherit` block is replayed. The module executes at most once per VM and later calls return its cached value. **Return:** The module's Lua value. **Failure:** A bare name, non-`.lua` extension, absolute path, cycle, conflicting frozen identity, limit breach, or confined-root escape raises a module error. **Example:** `local helpers = require("./lib/helpers.lua")`

**Implementation status.** This is a documented deferred target contract. The current implementation plan must not add `require`, its resolver, cache, tests, benchmarks, prompt migration, or public availability.

**Deferred partial Markdown composition.** `include`, `local_include`, and partial Markdown fragments do not currently exist, so the current plan has no removal, compatibility, testing, or migration work for them. They are future composition features, not rejected designs. Their parsing, lifecycle, VM scope, persistence, and return semantics remain deferred; later plans will implement them. The known distinction is that `require()` returns a cached Lua module value while `include()` does not.

### `execute(path, input?)`

**Effect:** Synchronously invokes one complete trusted `.md` PromptForge document by spawning it through the common task runtime and awaiting its outcome. The child runs through the same formal parser and executor as a root prompt, optionally replaces its `args`, receives fresh prompt and VM state, owns its model and tool bindings, shares the parent run's store and host policy, and inherits cancellation, deadline, and confinement. Parent globals, `var`, and `lua inherit` ancestry do not cross the document boundary. Awaiting suspends only the current fence coroutine. **Return:** The child prompt's final text, or nil when it completed without a scalar result. **Failure:** A bare name, non-`.md` extension, absolute path, malformed complete prompt, execution cycle, nesting limit, failed or cancelled child, conflicting frozen identity, or confined-root escape raises a typed execution error. **Example:** `local report = execute("./prompts/report.md", args)`

**Implementation status.** This is a documented deferred target contract. The current implementation plan must not add path-based `execute`, `execute_async`, their tests, or their prompt migrations.

**Migration order.** After the public `call` and `execute` contracts freeze, rename the current heading-based `execute` operation to `call` as the first child-composition behavior change and preserve its synchronous behavior. Verify that no heading-form `execute` remains and reserve `execute` for this deferred contract; integrate asynchronous section-child behavior only after the common task runtime exists.

### `execute_async(path, input?)`

**Deferred target contract:** Eagerly creates and enqueues the same complete-document task that `execute` will synchronously await, then returns its durable Task handle. The executor controls when queued work becomes running. Its path, input, isolation, failure, cancellation, confinement, and restoration semantics are identical to `execute`. This API is not implemented in the current plan.

**Deferred resolution and caching contract.** Nested `require` and `execute` calls resolve relative to the module or complete prompt that contains them. A replayed inherit block retains its declaring Markdown file as its resolution anchor. Bare names never search the process working directory or `package.path`; PromptForge exposes no unrestricted package searchers or native module loaders. Required modules cache once per VM, while every `execute` call creates a fresh child prompt invocation. An embedded prompt without a source directory may load files only when its host supplies a confined virtual root.

**Deferred confinement contract.** Resolution freezes bytes for the run, canonicalizes every path, and checks symlinks, junctions, and other reparse points against declared roots. Required module and executed prompt bytes participate in incarnation identity when their contracts are implemented. Only trusted code roots may execute. Loading or child execution never promotes data to system authority.

## State and globals

One VM lives from section entry through every fence, suspension, and interactive turn in that entry. It exposes safe base functions plus the `string`, `table`, `math`, and `utf8` libraries. The deferred module contract later adds PromptForge's sandboxed `require`; unrestricted `package`, `io`, `os`, `debug`, `load`, `loadfile`, `dofile`, and native module loading remain unavailable.

A host call resumes its fence coroutine at the same call site. Fall-through, jump, call, and every deferred `call_async` section entry create fresh section VMs. Deferred `execute` and `execute_async` create fresh child prompt invocations with their own section VMs when implemented.

A Lua `local` belongs only to its fence or retained closure, while an ordinary global remains available to later fences in that section VM. Fresh VMs receive only inherited initialization and explicit transfer channels.

A section is active, compacting, or waiting before it becomes completed, failed, or cancelled.

**`args`.** The deeply copied read-only JSON-representable run or child-task input. Omitted child input inherits the caller's current `args`; no mutable Lua reference crosses a VM boundary. Example: `var.request = args`

**`prose`.** The read-only lazy Markdown template captured for the current fence, otherwise nil. Its first runtime read resolves and memoizes substitutions against current section state. Example: `messages[1] = { role = "user", content = prose }`

**`var`.** A non-reassignable JSON clipboard carried by fall-through and jump, cloned into `call` and deferred `call_async` section tasks, and isolated from child writes. Deferred document tasks receive fresh prompt state. Example: `var.draft = models.infer(prose)`

**`sys`.** Immutable sealed metadata fixed at section entry with `when`, `now`, `id`, `section_name`, `execution`, and `section_count`. Model identity, finish reason, request IDs, projection hashes, and metrics remain host-observer data rather than Lua results. Example: `log(sys.section_name)`

### `log(message)`

**Effect:** Emits one bounded diagnostic checkpoint for the current section. **Return:** nil. **Failure:** A non-string, control character, message over 256 characters, or exhausted log quota raises a Lua or quota error. **Example:** `log("draft ready")`

### `untrusted(text)`

**Effect:** Wraps text in the run's guarded envelope before model re-injection. **Return:** The guarded string. **Failure:** A non-string argument raises a Lua type error. **Example:** `local guarded = untrusted(store.read("source.txt"))`

## Messages

Lua owns plain JSON-representable arrays of `system`, `user`, `assistant`, and `tool` records. `content` is a string or a non-empty array of `{ type = "text", text = "Hello" }` and `{ type = "image_url", image_url = { url = "data:image/png;base64,AA" } }` parts. An assistant record may contain visible text plus one normalized call batch; each tool record names its matching `tool_call_id`. Reasoning or thinking content is never a message record: it is a host-observer side channel carried by streaming deltas, canonical thought events, and reasoning-token metrics, and the gateway's chat-template layer owns any provider-specific wire encoding of it.

### `messages.new()`

**Effect:** Creates an optional pure-Lua message list backed by a normal numerically indexed table. Chainable `system(content)`, `user(content)`, `assistant(content)`, `tool(call_id, name, content)`, and `append(record)` methods add ordinary provider-neutral records and return the same list. The methods perform no model calls, tool dispatch, compaction, or hidden retention. Raw arrays remain valid everywhere, and host protocol validation remains authoritative. **Return:** The new message list. **Example:** `local history = messages.new():system("Be concise."):user(prose)`

```lua
local messages = {
    { role = "system", content = "Be concise." },
    { role = "user", content = "Find the answer." },
    {
        role = "assistant",
        content = "I will check.",
        tool_calls = {
            { id = "call_1", name = "search", arguments = { query = "answer" } },
        },
    },
    { role = "tool", name = "search", tool_call_id = "call_1", content = "Result" },
}
```

Multiple system records are legal only as one contiguous leading prefix. A later system role is rejected. PromptForge owns deterministic validation and provider-neutral projection; the gateway owns model-specific chat-template rendering. Projection may combine or map the system prefix but cannot promote any other content into system authority or mutate the Lua array.

Immediately before dispatch, deterministic projection validates roles, parts, unique call IDs, complete call-result correlation, and provider ordering. It may synthesize only missing results for interrupted tail calls, marking synthetic provenance. Every other orphan or split exchange is rejected. Call batches and all results stay atomic through compaction, cancellation repair, and replay.

One request creates one assistant message even when streaming or requesting several tools. Call batches and all results also remain atomic during truncation. Temporary wire normalization strips provenance, retention, timestamps, event IDs, and metrics from provider content.

## Models

Model aliases resolve capabilities in the H1 preamble. Invocation options include `temperature`, `max_tokens`, `context`, and `thinking`.

### `models.bind(alias, capability, options?)`

**Effect:** Resolves and freezes one named model capability. **Return:** A read-only handle with name, model ID, description, context, thinking, temperature, and output limit. **Failure:** A non-H1 call, duplicate alias, missing match, or ambiguous match raises a binding error. **Example:** `models.bind("writer", "careful technical writing", { temperature = 0 })`

### `models.default(alias)` or `models.default(alias, capability, options?)`

**Effect:** Selects the prompt fallback for calls without an explicit model, optionally binding it atomically. **Return:** The selected read-only handle. **Failure:** A second default or unknown alias raises a binding error. **Example:** `models.default("writer")`

### `models.use(alias)`

**Effect:** Selects a bound alias as this section's model. **Return:** The selected read-only handle. **Failure:** An unknown alias raises a Lua error. **Example:** `models.use("writer")`

### `models.get(alias)`

**Effect:** Looks up a bound alias without selecting it. **Return:** Its read-only handle. **Failure:** An unknown alias raises a Lua error. **Example:** `local writer = models.get("writer")`

### `models.infer(handle?, prompt)`

**Effect:** Performs one fresh tool-free text inference using the selected model or, when the first argument is a model handle, that handle's frozen binding. It does not read or mutate a message array or any special output state. **Return:** The completed text. **Failure:** Missing model selection, provider failure, context overflow, or a tool-call response raises a typed error. **Example:** `local title = models.infer("Write a title.")` or `local title = models.infer(models.get("writer"), "Write a title.")`

The one-request provider turn, model identity, finish reason, request IDs, projection hashes, and metrics remain internal Rust and host-observer mechanisms. Lua receives no public `model_turn` API. Every `models.loop` call reads the section's current model selection (`models.default` or `models.use`) and current model-visible tool scope (`tools.always`, `tools.add`, `tools.add_local`) at call time. Passing an explicit handle from `models.get`, `models.use`, `models.bind`, or `models.default` as the leading argument to `models.infer` or `models.loop` runs on its frozen binding at any time, independent of the section's selection. Handles are pure inspectable values with no methods.

## Tools

Bound tools remain unavailable to the model until `tools.always`, `tools.add`, or `tools.add_local` places them in scope. Every model turn then receives that section scope automatically. Direct Lua dispatch may use a bound but unadvertised alias.

### `tools.bind(alias, capability, override?)`

**Effect:** Resolves a host tool in H1 and freezes it under a local alias. **Return:** A read-only Tool with name, description, parameters, wire name, and trust flag. **Failure:** A non-H1 call, no match, ambiguity, duplicate alias, or duplicate selected identity raises a binding error. **Example:** `tools.bind("search", "search authoritative sources")`

### `tools.always(alias_or_tool, override?)`

**Effect:** Adds a bound tool from H1 to every section's model-visible scope, with an optional model-facing description. **Return:** The frozen Tool. **Failure:** A non-H1 call, unknown alias, or conflicting scope raises a binding error. **Example:** `tools.always("search")`

### `tools.add(alias_or_list, override?)`

**Effect:** Adds one bound alias, Tool, or alias array to the current section's model-visible scope. **Return:** nil. **Failure:** An unknown alias, invalid override, or near-duplicate visible schema raises a tool error. **Example:** `tools.add({ "search", "fetch" })`

### `tools["add_local"](alias, description, parameters, handler)`

**Effect:** Registers a model-visible tool whose handler runs in the current VM and may update globals, `var`, or store. **Return:** nil. **Failure:** Alias collision, invalid schema, handler error, non-scalar handler return, suspension, or jump raises a Lua or tool error. **Example:** `tools["add_local"]("ping", "Return pong", {}, function() return "pong" end)`

### `tools.calls[alias]`

**Effect:** Reads attempted model dispatches for an alias in this section, including failed attempts. **Return:** A non-negative integer. **Failure:** An unknown or unseeded alias raises a Lua error. **Example:** `local count = tools.calls.search`

### `tools.call(alias, arguments)`

**Effect:** Directly dispatches any bound tool, named by alias string or Tool object, without advertising it to a model. **Return:** The decoded result as a string or JSON-representable Lua value. **Failure:** Unknown alias, invalid arguments, denial, or tool failure raises a typed Lua error. **Example:** `local result = tools.call("search", { query = "C++" })`

### `models.loop(handle?, messages, compactor?)`

**Effect:** Runs the Rust-backed model and tool protocol using the section's current model selection and model-visible tool scope or, when the first argument is a model handle, that handle's frozen binding. It performs a request precheck, invokes the selected compactor when required, appends each assistant message, dispatches every structured tool-call batch, appends every correlated result, and repeats until it appends a terminal assistant message.

Omitted `compactor` means `compactors.fail`. With no model-visible tools, the loop normally performs one model call. Compacted replacements belong to the deferred compactor framework.

On success, the terminal assistant record is `messages[#messages]`. Callers may retain it, read its content, remove it with `messages[#messages] = nil`, or otherwise reshape the projection. No special output register is mutated.

**Return:** nil.

**Failure:** Missing model selection, malformed messages, unknown aliases, exhausted turns, typed context exhaustion, provider failure, or terminal cancellation raises a typed error without appending a terminal assistant message.

**Example:** `models.loop(messages)`

Model and tool selections are read at call time; `models.use`, `tools.add`, and `tools.add_local` remain available throughout the section and affect the next `models.loop` call. An explicit leading handle runs on its frozen binding at any time. Provider projection is computed per dispatch for whichever model the call targets. The message array is the only continuity state and the author owns it.

Recoverable tool failures and interruptions become correlated results when continuation remains valid. Local tool output is trusted; host tool trust policy controls guarding.

Model-issued structured tool calls have exactly this Rust dispatch path. Direct Lua `tools.call(alias, arguments)` remains a separate existing deterministic author-directed path; internal batch dispatch and result-append machinery are not exposed to Lua.

Model-facing description precedence is a `tools.add` override, then a `tools.bind` or `tools.always` override, then catalog text. Array additions take no per-item overrides.

## Store

**Implementation status.** Existing store behavior may continue unchanged, but the task-aware linearizability, journaling, conflict, ordering, and replay changes described here are deferred and inert.

Store is run-scoped bulk state shared by all tasks. Every operation is linearizable and journaled under its task and operation IDs. Reads observe state at their committed operation sequence and preserve read-your-writes. Causal order consists of same-task program order, parent operations before asynchronous child creation, and a terminal outcome observation before the observer's later operations. Causally unordered destructive mutations by different tasks to one path fail as a conflict; destructive mutations are write, replace, and delete. Concurrent append with append is atomic and permitted. Its byte order follows the persisted commit sequence, is unspecified to authors, and is stable on replay. An unordered append mixed with a destructive mutation conflicts. Each mutation and its operation result commit atomically.

### `store.write(path, text)`

**Effect:** Creates or replaces a virtual file. **Return:** nil. **Failure:** Invalid path, backend failure, or causally unordered same-path mutation raises a store error. **Example:** `store.write("draft.md", draft)`

### `store.append(path, text)`

**Effect:** Appends text, creating the file when absent. **Return:** nil. **Failure:** Invalid path or backend failure raises a store error. **Example:** `store.append("notes.md", "\nNew note")`

### `store.read(path, start?, finish?)`

**Effect:** Reads verbatim text, optionally over an inclusive one-based line range. **Return:** A string. **Failure:** Missing file, invalid path, or invalid range raises a store error. **Example:** `local text = store.read("draft.md", 1, 20)`

### `store.read_numbered(path, start?, finish?)`

**Effect:** Reads the same range with absolute line numbers. **Return:** A numbered string. **Failure:** Missing file, invalid path, or invalid range raises a store error. **Example:** `local lines = store.read_numbered("draft.md", 10, 20)`

### `store.str_replace(path, old, new)`

**Effect:** Replaces the unique occurrence of `old`. **Return:** nil. **Failure:** Empty, missing, or ambiguous anchor, missing file, or invalid path raises a store error. **Example:** `store.str_replace("draft.md", "teh", "the")`

### `store.delete(path)`

**Effect:** Removes a virtual file and is idempotent when absent. **Return:** nil. **Failure:** Invalid path or backend failure raises a store error. **Example:** `store.delete("scratch.txt")`

### `store.glob(pattern)`

**Effect:** Matches virtual paths and sorts them. **Return:** An array of path strings. **Failure:** Empty, oversized, malformed, or control-bearing patterns raise a store error. **Example:** `local files = store.glob("reports/*.md")`

### `store.exists(path)`

**Effect:** Checks one virtual path. **Return:** A boolean. **Failure:** Invalid path or backend failure raises a store error. **Example:** `local ready = store.exists("ready.txt")`

## Compaction

**Implementation status.** Only the minimum compactor invocation surface and `compactors.fail` are active: on precheck or provider overflow the loop invokes the selected compactor with the reason, and `compactors.fail` always raises typed context exhaustion. Custom compactor callbacks, the budget record, replacement validation, measurable-progress checks, in-place history replacement, `compactors.summarize`, pinning helpers, other shipped policies, rich compaction events, and compaction persistence are deferred target contracts, described below for the future framework.

Before dispatch and after a typed provider overflow, the loop budgets the final provider projection. The estimate includes system content, ordered tool schemas, provider template overhead, media, and reserved output, not only Lua message text.

```lua
{
    max_input_tokens = 131072,
    estimated_input_tokens = 118400,
    reserved_output_tokens = 8192,
    target_input_tokens = 90000,
    reason = "precheck",
}
```

The other standard reason is `provider_overflow`. Retention policy lives in the compactor closure, never in message records. A replacement must be a valid array that preserves sealed system content and atomic tool exchanges. It must make measured or conservative token-budget progress; merely returning fewer records is irrelevant. Repeated no-progress or exhausted policy fails deterministically.

### `compactor(messages, budget)`

**Implementation status:** Deferred and inert in the current plan; `compactors.fail` is the only shipped policy.

**Effect:** Applies author policy to the current projection. **Return:** A valid replacement message array. **Failure:** Nil, malformed, oversized with no token progress, changed pins, duplicate IDs, or split exchanges raises a context error. **Example:** For a known history whose second and third records are one complete plain turn: `local compact = function(messages) return { messages[1], table.unpack(messages, 4) } end`

### `compactors.fail(messages, budget)`

**Effect:** Refuses compaction. **Return:** None. **Failure:** Always raises typed context exhaustion. **Example:** `models.loop(messages, compactors.fail)`

### `compactors.summarize(options)`

**Implementation status:** Deferred and inert in the current plan.

**Effect:** Captures a pinned prefix and recent-tail policy, then summarizes complete older turns with the section-selected tool-free inference path. **Return:** A compactor closure. **Failure:** Invalid pins, split exchanges, summary failure, or no token progress raises a context error. **Example:** `local compact = compactors.summarize({ pinned_prefix = 2, keep_recent_turns = 4 })`

A compactor may call tool-free `models.infer` with or without an explicit handle for its summary without changing the section's advertised tools. Compaction changes only the model projection. Its canonical event contains old and new hashes, source spans, policy identity, reason, token estimates, and record counts. It never contains replacement content, injected files, system framing, or tool schemas.

## Control flow

Fall-through visits siblings in source order and carries `var`, but no implicit text result. Thematic breaks only clear pending prose and never affect control flow. A heading reference is one or more `#` characters, required whitespace, and exact heading text. The visible set is the current section's siblings except itself plus its direct children. Resolution never searches farther.

### `list_from_section(heading)`

**Implementation status:** Existing behavior, unchanged by this plan.

**Effect:** Reads a visible list section and strips item markers. **Return:** An ordered array of strings. **Failure:** Malformed reference, invisible target, non-list target, or malformed list raises a parse or Lua error. **Example:** `local topics = list_from_section("### Topics")`

### `call(heading, input?)`

**Implementation status:** Active. Rename the current heading-based `execute` operation to `call` as the first behavior change and preserve its synchronous execution semantics.

**Effect:** Synchronously invokes a visible section as a contained fresh chain and resumes the caller. It optionally replaces `args`, clones `var`, creates a fresh target VM, and discards child clipboard writes. Deferred `lua inherit` later adds lexical initialization. **Return:** Final child text, or nil when it completed without a scalar result. **Failure:** Missing or ambiguous target, recursion over depth eight, or child failure raises a typed Lua error. **Example:** `local answer = call("## Worker", "new input")`

### `call_async(heading, input?)`

**Implementation status:** Deferred and inert in the current plan.

**Effect:** Eagerly creates and enqueues one visible section task, then returns without awaiting it. The executor controls when queued work becomes running. It optionally replaces `args`, clones `var`, creates a fresh section entry initialized from lexical `lua inherit` ancestry and frozen assets, and isolates child clipboard writes. Every child inherits parent cancellation, deadline, confinement, and run services. **Return:** An opaque durable Task handle. **Failure:** Invalid or ambiguous heading, depth over eight, invalid input, or exhausted live-task quota raises before a handle exists. Failures after creation settle the returned task. **Example:** `local research = call_async("## Research", { topic = "allocators" })`

### Task handles

**Implementation status:** Deferred and inert in the current plan, including `tasks.await_all`, task outcomes, structured cancellation, scheduling, persistence, and model-visible subagent adapters.

Task handles are opaque immutable host values and never cross into model content. `task.id` is a stable read-only string. `task:result()` is nonblocking and idempotent, returning nil while the task is nonterminal and its immutable Outcome afterward. `task:await()` suspends the current fence coroutine and returns the terminal Outcome. `task:cancel(reason?)` durably requests cancellation and returns true only when the first request wins before terminal intent has been claimed; it does not promise that an external provider stopped. There is no separate `ready()` because `task:result() ~= nil` is the same observation.

`tasks.await_all(handles, options)` is a Rust-backed container wait over a dense ordered array of distinct same-run tasks. An empty array returns an empty array. `options.mode = "all_settled"` suspends until every task is terminal and returns input-ordered Outcomes. `options.mode = "fail_fast"` atomically requests cancellation of unfinished tasks when the first canonical failed or cancelled outcome appears, drains them, and raises that outcome's TaskError; if all tasks succeed it returns input-ordered Outcomes. Handles remain valid and are never consumed. Race-style `tasks.await_any` is deferred until a concrete use case requires it.

An Outcome is exactly one immutable tagged record. Successful `value` is the target's final text or nil when the target completed without a scalar result:

```lua
{ status = "succeeded", value = string_or_nil }
{ status = "failed", error = task_error }
{ status = "cancelled", error = task_error }
```

A TaskError contains stable `family`, `code`, `message`, `retryable`, and originating `task_id` fields. Child failure is policy-neutral data. `call` and `execute` unwrap unsuccessful outcomes into typed Lua errors; direct task users decide whether to ignore, collect, retry, cancel siblings, or propagate them.

Tasks move through `queued`, `running`, `waiting`, and `closing` before exactly one terminal state: `succeeded`, `failed`, or `cancelled`. Entering `closing` atomically closes the child-creation gate, fixes terminal intent, requests cancellation of every nonterminal descendant, and drains local descendants before publishing the outcome. A parent waiting in `user_input()` remains live and its children continue. Actual parent return, failure, or cancellation closes the scope. Version 0 has no detached or orphan task.

Model-visible subagent tools use this same runtime through a fixed section target in the current implementation scope; fixed document targets remain deferred with `execute`. One tool invocation calls asynchronously, awaits, unwraps, and returns a serializable correlated result; a model never receives a Task handle.

### Deferred `fanout(section, inputs)`

**Target contract:** Thin shipped Lua creates one `call_async` task per ordered input with explicit `{ index = i, value = inputs[i] }` in `args`, then uses Rust-backed `tasks.await_all` in fail-fast mode. The first child failure atomically cancels and drains unfinished tasks and raises its TaskError; success returns ordered child values. The executor controls scheduling and run-wide capacity. Invalid arguments or partial creation failure raise after cancelling and draining tasks already created. Maps are rejected unless the caller first supplies a deterministic key order.

### Deferred `pfanout(section, inputs)`

**Target contract:** The protected variant creates the same ordered section tasks, waits for every task through Rust-backed `tasks.await_all` all-settled mode, and returns input-ordered Outcomes without cancelling siblings because one failed. Invalid arguments or inability to create the batch still raise. The `p` follows Lua's protected-call naming convention.

### `jump(heading)`

**Implementation status:** Existing behavior, unchanged by this plan; the `lua inherit` initialization mentioned below is deferred.

**Effect:** Terminates the current frame and transfers its walk with `var` into a fresh target VM initialized from the target's lexical `lua inherit` ancestry and frozen assets. No implicit text result is transferred. A direct-child transfer walks that child level before the parent level resumes. **Return:** Never returns to the caller. **Failure:** A malformed, missing, or ambiguous visible target raises a Lua error. **Example:** `jump("## Next")`

## Host APIs

**Implementation status.** Generic `user_input()`, its model-visible tool adapter, and the minimum Agent-window integration are active. The built-in chat agent is rewritten from a standalone Lua program into an embedded `chat.md` Markdown prompt at `promptforge: 0` on the unified runtime; external Markdown-agent discovery, UI snapshots, reconnect persistence, and broader Workshop changes are deferred.

### `user_input()`

**Effect:** Requests input through host policy: block for a human, report unavailable immediately, or fail. The optional model tool uses this same broker and records one correlated tool exchange. **Return:** `text, available`; unavailable is exactly `User input is unavailable, use your best judgement.` with `available == false`. **Failure:** Failing policy or terminal host cancellation raises a typed error. **Example:** `local text, available = user_input(); if not available then text = args end`

Unavailable input is a host result, not a user message. Lua alone decides whether to label and project it.

### `ui()`

**Effect:** Requests a fresh non-authoritative host presentation snapshot. **Return:** A table when supplied, commonly with `selected_model` and `workspace_root`, otherwise nil. `selected_model` is non-nil only for the Workshop Agent-window session - a deliberate minimal mechanism to be revisited. **Failure:** Unsupported fields are absent and must not drive correctness. **Example:** `local host_ui = ui()`

## Events and persistence

**Implementation status.** Event-view removal, journal changes, snapshots, incarnation, task persistence, cold restore, and replay are deferred and inert. Existing event and persistence behavior may remain unchanged.

Canonical events are append-only host-owned truth under one gap-free per-run commit sequence. Lua message arrays are mutable model projections, and streaming deltas are ephemeral presentation. Events cover user messages, completed assistant messages and thoughts, model attempts, tool-call batches, updates and results, compactions, input waits and responses, task lifecycle, and terminal outcomes. Prompt Lua has no event-log view; it receives operation results, metrics, counters, input, task handles, and other narrow state APIs instead.

Host event records contain `kind`, `section`, `chain_id`, `depth`, `turn`, and `content`, with optional stable `task_id`, `parent_task_id`, `frame_id`, `operation_id`, `target`, `model`, `tool_call_id`, `finish_reason`, and `metrics`. Task creation precedes start, exactly one terminal event follows descendant drain, and every descendant terminal event precedes its parent's terminal event. Content-bearing records retain their trust classification and never gain authority merely by replay.

Each model attempt records its attempt ID, projection hash, model, finish reason, provider message ID, input, output, cached, and reasoning tokens, plus timing exactly once and links that record to its assistant event. Failed and cancelled attempts remain observable even when they add no model-facing message.

A run owns a unique identity and exclusive ownership epoch. Stable opaque task IDs derive from that run, the incarnation, frame activation, and asynchronous-call operation identity, so replay recreates the same handle and a fork receives a new identity. Every suspending, effectful, or control-flow-relevant host observation is journaled with its operation kind, canonical argument digest, policy identity, and result schema. This includes nil `task:result()` probes, `tasks.await_all` candidate sets, modes, outcomes, cancellation races, store reads, clocks, input, and host snapshots.

A section incarnation hashes prompt source, non-secret host policy, task limits, runtime identity, and every sealed continuing-conversation identity. The deferred module and complete-document contracts add frozen required-module bytes and executed child-prompt source when implemented. Cold restore acquires the next exclusive ownership epoch, verifies the incarnation and journal signatures, creates fresh VMs at section entry, and replays recorded host-call results without repeating completed effects. Scheduling reopens only after every active frame is reconstructed at its durable wait or first unrecorded operation. Drift rejects resume or creates an explicitly linked incarnation.

A snapshot is one atomically committed task-graph and store cut at a fence or host-operation boundary. It contains the event offset, block position, active projections, task states and immutable outcomes, parent links, per-frame replay cursors, operation-journal position, store version, cancellation state, and outstanding waits or children. Store mutation and operation completion commit together, so replay never duplicates a completed append. A snapshot never contains a live coroutine, mutable userdata, tool implementation, credential, provider secret, or wait token.

An external operation recorded as possibly dispatched but not completed reattaches through its stable operation ID when the provider or tool supports it. PromptForge retries only when the host can prove the operation did not start or the remote endpoint can deduplicate it. Otherwise the operation and owning task fail closed with `indeterminate_operation`. PromptForge guarantees durable local task identity and exactly-once local store effects, not provider-independent cancellation or exactly-once remote effects.

## Errors and limits

The active scope defaults to 24 models.loop iterations, model response size 16 MiB, and Lua memory 64 MiB. `models.loop` raises typed context exhaustion when its precheck or provider reports overflow. Hosts may configure supported active bounds.

Active input waits preserve their section VM and follow host wait, failure, and cancellation policy. Deferred limits cover running and live child tasks, child depth, task execution time, replay work, child recursion, and required-module or executed-prompt depth and bytes. Running-capacity saturation, queued-task admission, reconnect lifetime, and cold-session policy remain inert until their owning contracts are implemented.

Failure families are parse, version, binding, completion, tool, store, Lua, quota, substitution, context, module, execution, incarnation, cancelled, and internal. Parse errors distinguish frontmatter, structure, fence, list, and Lua failures. Invalid source, unsafe paths, malformed messages, incarnation drift, and compactor corruption fail without blind retry; marked transport and service failures may be retried only by the Rust models.loop policy.

`pcall` can catch recoverable active host and tool errors. A recoverable model-issued tool interruption becomes a correlated result only when the conversation can validly continue. Deferred task cancellation later closes the child-creation gate, propagates down the task tree, drains descendants, and handles uncertain remote cessation.

## Recipes

Each recipe is complete, explicit, and short. Only recipes labeled active belong to the current implementation scope.

### Deferred fanout review

Use `var.draft` for shared read-only context and explicit task input for each critic. `fanout` here is the thin shipped Lua helper over `call_async` and Rust-backed `tasks.await_all`.

````markdown
---
name: fanout-review
description: Draft once and review in parallel
promptforge: 0
---
# Fanout Review
```lua
models.bind("writer", "concise technical writing")
models.default("writer")
```
## Draft
Draft {{ args }}.
```lua
var.draft = models.infer(prose)
```
## Review
```lua
local reviews = fanout("### Critic", { "accuracy", "clarity" })
return reviews[1] .. "\n" .. reviews[2]
```
### Critic
Review {{ var.draft }} for {{ args.value }}.
```lua
return models.infer(prose)
```
````

### Deferred compact model loop

Pin a stable prefix and let Lua choose retention.

````markdown
---
name: compact-analysis
description: Analyze with tools and compaction
promptforge: 0
---
# Compact Analysis
```lua
models.bind("analyst", "evidence-based analysis")
models.default("analyst")
tools.bind("search", "search authoritative sources")
```
## Investigate
Investigate {{ args }} and cite evidence.
```lua
tools.add("search")
local messages = { { role = "system", content = "Verify claims." }, { role = "user", content = prose } }
local compact = compactors.summarize({
    pinned_prefix = 2, keep_recent_turns = 4,
})
models.loop(messages, compact)
return messages[#messages].content
```
````

### Active interactive or unattended loop

Branch on provenance; `models.loop` appends every assistant and tool record so the message history is complete on return.

````markdown
---
name: analysis-chat
description: Interactive or unattended analysis
promptforge: 0
---
# Analysis Chat
```lua
models.bind("analyst", "evidence-based analysis"); models.default("analyst"); tools.bind("search", "search authoritative sources")
```
## Chat
Be concise, verify claims, and preserve continuity.
```lua
tools.add("search")
local history = messages.new():system(prose)
local last_response = nil
while true do
    local text, available = user_input()
    if not available then if args == "" then return text end; text = args end
    if text == "exit" then return last_response or "Done." end
    history:user(text)
    models.loop(history)
    local response = history[#history].content
    if not available then return response end
    last_response = response
end
```
````

*2026-09-08 20:07 - GPT-5.6 Sol*\
*2026-09-10 01:05 - kimi-k3: synced with unified prompt model plan - models.loop/handle:loop, tools.call, minimal compactor surface, call-time selection (no sealing)*\
*2026-09-10 01:20 - kimi-k3: namespace-only invocation - handles are pure inspectable values; models.infer/models.loop take an optional leading handle, tools.call takes alias or Tool object; colon handle methods removed*
