# Modify the store session

*2026-08-15 18:51 - transcript b9c7e469-a015-460d-a8dd-f94b4446856a*



## Prompts



**[p1]** Hey, listen up, here's what I want. I wanna modify the store. So that It can be passed in, and it can have files already in it. And so what I wanna be able to do is I wanna be able to make a prompt that That has input files. And I'm not exactly sure how the prompt advertises that, maybe it's in the YAML, I don't know. But For example, I wanna make a, I wanna do a version of Papergate, where you, you input the paper down, and then it does its processing, and then it leaves behind a report in a file, and the file is becomes output. So it takes a file as input, it gives a file as output, but we wanna be able to use the memory store so that there's no actual disk IO, so it's all like in a sandbox and safe. @promptforge

**[p2]** Wait a minute, I'm not, I don't know if I'm thinking about Oh yeah, files dot inputs. Files the prompt expects to find already in the store, yeah. Actually, that sounds right. Because. Because It doesn't go in the args, the args is textual input, but this goes this is, this is initialized as a parameter to the execution function, right? Like there's no it's not part of the prompt. So, what, what, what's actually being passed in is an instance of the store.

**[p3]** The question is, how would the I guess the file so the files parameter would specify the file name? 'Cause this is different. Like. Because if you go through this, if you go through the API, you have to pass a store and the file has to be at a certain file name. But if you go through the MCP, obviously we can't pass a store, we can only pass full paths. So how does this work?

**[p4]** I think this sounds largely correct, but I think the The MCP server. The, the PromptForge MCP server has to map the file name to the store, and I think It also, we, we also need to make a choice on which, which store to use. Should we use a memory store? That would be the safest one. So that means that the MCP gateway programmatically reads the files in and it loads up the store, and then it runs the prompt, and then the prompt does what it wants, it goes to town. It can read, it can even modify, it can create, and then, but as long as, but it has to leave behind its outputs in the files that it promised. And then when it's done The gateway gets control again, and now it makes the decision on what to do with the files. It could output it into the chat, right? It could put it in a different path, and we have, we have to figure that out.

**[p5]** I think, I think We wanna let the caller say, okay, put the file here. Like for example, when you call the The MTP server will, will, will advertise to the model that it can. That the model can specify the output file, and then if it, if it does that, then the gateway, the MCP server, will take the memory file in the store, which the prompt put at a specific file name, and then it'll write that into the output file name in the real file system that the orchestrator who invoked the gateway specified. I think that's the safest thing to do because then we don't have to worry about any permissions, we don't have to worry about authorization, we put it all on the orchestrator to handle that.

**[p6]** Right, so I feel like, but on the in what's files? The input file, you're are you I don't like what you're doing with the input file. That wastes, that means the orchestrator has to waste output tokens on a file that already exists. No, that doesn't make sense. What we should do instead is, it should, the MCP gateway should just read the file and put it in the store, don't you think?

**[p7]** Tell me what the yammo looks like.

**[p8]** I prefer

**[p9]** input:

**[p10]** output:

**[p11]** how do we add text inputs later

**[p12]** No, no, I don't. I think we need to design this, we need to think about it a little better because it's, this feels like it's very specific to files. Like, I think On the prompt side, the prompt has to see files. It just makes sense because. It already handles files and the prompt doesn't care how it gets it. So whether we're getting text from JSON, whether we're getting the model is orchestrating and just putting a prompt in there directly in quotes, or whether it's pointing it at a file, the prompt itself, the prompt for the prompt itself shouldn't care. The executor should just offer the store parameter in its API. But then what does care is the gateway, the MCP server. So the MCP server's job is to translate back and forth between The orchestration environment that's invoking the MCP and the PromptForge ex-exec executor. And we wanna be flexible, so in the chat, show me, show me a couple of different options, just for the input. Let's do just the input. Show me a couple of options on how we can handle multimodal text input.

**[p13]** I'm not sure about fetching URLs. I don't know about that one. 'Cause what if, what if we want the model to do the fetching for some reason? Then it would be ambiguous. No, I'm thinking for input you could use either a file. Or text. I'm trying to figure out how to make the schema small. Because so it makes it easier for like a smaller model to fill in.

**[p14]** That's not, you're not understanding what I'm saying. What we want, we want something that allows the orchestrator, it allows the caller to specify a path, and then the gateway will read the file in to the store, or to specify text, and then the gateway will transfer the text into the store. The prompt itself doesn't know. That's the whole point of this.

**[p15]** So show me what the mcp advertisement would look like.

**[p16]** this looks very complicated

**[p17]** what is this "additionalProperties" ?

**[p18]** we can't do this. the promptforge mcp server needs to be able to map the caller's inputs to the Store without using inference

**[p19]** I don't, it's not, I think, I don't think this is ambiguous, but I'm trying to juggle opposing needs. First, I wanna, I wanna make it as simple as possible. Because I want, the simpler it is, the, the more likely that a smaller model is gonna be able to call it correctly. And I'm trying to decide if I should even allow multiple inputs and outputs. Maybe there should be a syntax for, like, maybe there's, maybe the case of one file in, one file out should be It should be a known case, 'cause it's so common. I don't know. And then Like for example, let's say we're gonna do something that, like, a paper gate, or it can only accept one paper. So why do we even need to give it a name? Like, why, why doesn't the caller just say, "Here's the input blob, " and then. There can be, we need args as to be separate because someone could specify a paper, you could, someone could specify a file input, but then they want to give additional commands, like for example, that you might want to say, "Uh, you know

**[p20]** I'm feeling this. And what if you wanna do input text?

**[p21]** And what about for output file, what if we wanted to go to the chat? Like what if we don't wanna write to a file? There should, we should have the option. Like the gate, the MCP server should h it should have the option of inlining the output file in its response.

**[p22]** Yeah, this sounds good. I like this a lot. So is that gonna be easy to specify, or models gonna have a hard time with these, all these little features and like all these little differences? And what does the YAML look like?

**[p23]** Required, but what if the wait a minute, what if a model specifies both an input file and input text? Do we have the gateway just given error?

**[p24]** Okay, I, I think this works for me. I think this works for me let's put it in the plan.

**[p25]** dont forget tests, the user's guide, the design guides

**[p26]** add @tools-public/rulebooks/rust-rulebook.md @tools-public/rulebooks/vibe-rulebook.md @tools-public/tools/architect.md

**[p27]** So for the architect, don't generate new design document, integrate it into the existing ones, and keep in mind there's multiple crates, each has their own design doc, okay?

**[p28]** review the plan

**[p29]** I thought that the promptforge-core package offered a function to parse the frontmatter?

**[p30]** what is a "seed_store" ?

**[p31]** mock_store

**[p32]** did you commit as you went?

**[p33]** doesn't @tools-public/rulebooks/vibe-rulebook.md say to commit each unit of work?

**[p34]** fix the rulebook and the workspace rule. make the workspace rule looser by adding an "unless" and make the rulebook tighter by writing it as imperative as it breaks the @tools-public/rulebooks/prompts-rulebook.md rules

**[p35]** do not create a new workspace rule

**[p36]** Listen up, here's what I want you to do. I want you to create this, I want you to put it into this file, instructions for the LLM on how to use PromptForge, but I want this to be very compressed. I just want the minimum. I want it to say how to launch the gate, how to launch the MCP server, how to launch the gateway, and how to launch an individual prompt using the dev tool, and like what goes in the YAML What goes in the Tamil configuration files and basically that sort of thing. And the goal is that the user, for example, me in Cursor, is I open up a fresh chat and then I just mention this file and then the model will load it and then it'll know how to do, it'll know how to do Prompt Forge, you know what I'm saying? But I this has to be compact. So I want the plan that you're about to make to have a list of bullets and s and sections that mirrors what it's gonna put in the actual file. @promptforge/promptforge.md

**[p37]** But I thought you need to use cargo.

**[p38]** Each section have a description of what the thing does? Like, for example, if you run the MCP server, you should have, you should run the gateway first. You should probably list them in the order that they need to be run.

**[p39]** To prevent the duplication, this should reference other files. Like for example, the YAML format, you should just reference the file that has it. For prompt structure, you should reference that file. Make it relative to the repo.

**[p40]** we need a gitignored directory in the repo which is used to hold local mcp prompts so the promptforge.md can configure the gateway. lets call it prompts-mcp

**[p41]** briefer.md will move to it

**[p42]** the local mcp server needs a toml file that serves the prompts-mcp dir

**[p43]** can't we just include the dir itself in the catalog

**[p44]** Did the mcp service do away with per-prompt config?

**[p45]** do we need an entry for each prompt or does it default properly

**[p46]** And the defaults. So for the defaults, do the defaults get access to all the tools? How does that work?

**[p47]** I'm wondering if we shouldn't even register those two tools. I'm thinking the MCP server should register nothing, and it's up to the user to put WebFetch and WebSearch in there. This way you can otherwise you can't have a real sandbox.

**[p48]** make sure that the plan's config puts back webfetch and websearch for the defaults in the TOML

**[p49]** add @tools-public/rulebooks/vibe-rulebook.md and @tools-public/rulebooks/rust-rulebook.md

**[p50]** @promptforge/research/2026-08-03-recover-rationale-promptforge-core.md does this have any purpose

**[p51]** show me one thing of value it offers

**[p52]** I think the file is worthless and I deleted it

**[p53]** run promptforge prompt echo

**[p54]** how is it possible if you literally just finished building things?

**[p55]** so you were told to write tests and run them but you didn't do the work?

**[p56]** I need you to go commit by commit, actually run the tests and make sure they work. amend the commit as needed. when you are done I want a commit log where every commit has tests and runs them

**[p57]** run promptforge echo

**[p58]** I want @promptforge/promptforge.md to have a minimal set of instructions so that if I write "promptforge echo.md this is the text" then it will launch the gateway, launch the mcp server, and then issue the toolcall. and in that chat context, the orchestrator will remember that those services were launched and then I can run the promptforge prompts over and over do you understand?

**[p59]** apply @tools-public/rulebooks/prompts-rulebook.md to promptforge.md



## Plans

### Store input files support

*Add support for pre-seeding the MemStore with input files before a prompt run, and for declaring input/output files in prompt frontmatter, enabling sandboxed file-in/file-out prompt execution without disk IO.*

# Store Input Files Support

## Current Architecture

The run pipeline is:

1. MCP `run_prompt` receives `{ prompt: "name", args: "raw string" }`
2. Runner creates a fresh empty `StoreRef::memory()` ([runner.rs:273](promptforge/crates/promptforge-mcp-server/src/server/runner.rs))
3. `execute::run()` takes `store: &StoreRef` and threads it through all sections
4. Lua code accesses files via `store.write()`, `store.read()`, etc.
5. Run completes, returns a string; the store is dropped (contents lost)

The store is already a trait (`dyn Store + Send`) behind `StoreRef` - it can be pre-populated before the run starts. The `MemStore` uses a `BTreeMap<String, String>` internally.

## Design

### 1. Frontmatter: declare `files` (inputs and outputs)

Add an optional `files` key to `Frontmatter`:

```yaml
---
name: papergate
description: Analyze a WG21 paper and produce a gating report
promptforge: 1
files:
  inputs:
    - path: paper.md
      description: The paper markdown to analyze
  outputs:
    - path: report.md
      description: The gating report produced by analysis
---
```

- `files.inputs` - files the prompt expects to find already in the store when it starts
- `files.outputs` - files the prompt will leave in the store when it finishes (informational/contractual)

Both are optional. The `path` is the store-relative path; `description` is for documentation and for MCP schema generation.

### 2. MCP schema: expose `files` as a tool parameter

When a prompt declares `files.inputs`, the `run_prompt` schema gains a `files` parameter (JSON object mapping path to content string):

```json
{
  "prompt": "papergate",
  "args": "",
  "files": {
    "paper.md": "# P2996R7\n..."
  }
}
```

The server validates that every declared input path has a value in the `files` object (reject if missing), then seeds the store before calling `execute::run`.

### 3. MCP result: return output files

When a prompt declares `files.outputs`, after the run completes the runner reads those paths from the store and includes them in the structured result alongside the text return value:

```json
{
  "status": "completed",
  "value": "Analysis complete.",
  "files": {
    "report.md": "# Papergate Report\n..."
  }
}
```

### 4. MemStore: add `with_files` constructor

Add a convenience method to `MemStore`:

```rust
impl MemStore {
    pub fn with_files(files: impl IntoIterator<Item = (String, String)>) -> MemStore {
        MemStore {
            files: files.into_iter().collect(),
        }
    }
}
```

And on `StoreRef`:

```rust
impl StoreRef {
    pub fn with_files(files: impl IntoIterator<Item = (String, String)>) -> StoreRef {
        StoreRef::new(Box::new(MemStore::with_files(files)))
    }
}
```

## Key Files to Modify

- `promptforge/crates/promptforge-core/src/parser/build.rs` - extend `Frontmatter` with `files` field
- `promptforge/crates/promptforge-core/src/store/mem.rs` - add `MemStore::with_files`
- `promptforge/crates/promptforge-core/src/store.rs` - add `StoreRef::with_files`
- `promptforge/crates/promptforge-mcp-server/src/tools.rs` - extend `run_prompt` schema conditionally
- `promptforge/crates/promptforge-mcp-server/src/server/runner.rs` - seed store from `files` param, extract outputs after run
- `promptforge/crates/promptforge-mcp-server/src/result.rs` - extend `RunResult` to carry output files
- `promptforge/crates/promptforge-cli/src/main.rs` - allow CLI to pass files (optional, lower priority)

## Decisions to Confirm

- Frontmatter uses `deny_unknown_fields`, so adding `files` requires the serde model change first or nothing parses
- Output file extraction is best-effort: if the prompt declares an output but doesn't write it, include it as null/absent rather than failing the run
- The `files` MCP parameter is a flat `{ path: content }` JSON object (not an array), for natural MCP tool-call ergonomics


Todos:

- Add MemStore::with_files and StoreRef::with_files constructors
- Add optional files field (inputs/outputs) to Frontmatter struct
- Extend run_prompt MCP schema to accept files parameter when prompt declares inputs
- Seed the store from the files parameter before calling execute::run
- After run completes, read declared output paths from the store and include in result
- Add tests for store seeding, frontmatter parsing, and round-trip file IO

### Fix commit rule conflict

*Resolve the conflict between the system-level "never commit unless asked" rule and the vibe-rulebook's "commit each step" instruction by adding a workspace override rule and tightening the vibe rulebook's commit language.*

# Fix Commit Rule Conflict

## Problem

The system prompt says "NEVER commit changes unless the user explicitly asks you to." The vibe-rulebook says "you commit" after each step and "never stop for ordinary user confirmation." These conflict, and the system prompt wins by default, causing the vibe rulebook to be silently ignored.

## Changes

### 1. New workspace rule: `c:\Users\Vinnie\src\cursor\.cursor\rules\always.mdc`

Add to the existing always-applied rule:

```
- Commit without asking when a loaded rulebook or plan instructs per-step commits. The system default ("never commit unless asked") yields to an explicit commit cadence in a governing document the user loaded for the session.
```

This is an "unless" that loosens the system constraint when - and only when - a user-loaded rulebook explicitly commands it.

### 2. Tighten the vibe rulebook: `c:\Users\Vinnie\src\cursor\tools-public\rulebooks\vibe-rulebook.md`

The current commit instruction is buried mid-paragraph in "The Loop":

> Then work the steps in order. For each step: a coder subagent implements it; you commit; a review-and-fix subagent applies...

The prompts-rulebook (section 5) says: "Write instructions in imperative second person, present tense" and "One instruction per sentence." The commit behavior should be a standalone imperative, not embedded in a flow description.

Replace the paragraph with a structured per-step sequence, one instruction per line:

```
Per step, in order:
1. Dispatch the coder subagent to implement the step.
2. Stage and commit the result. Use a message naming the step's intent.
3. Dispatch the review-and-fix subagent with the commit's diff.
4. Amend the commit if review-and-fix dirtied the tree.
5. Run Verify when scheduled.
```

This makes "commit" an unambiguous imperative at a fixed point in the sequence, not a clause buried in narrative. The existing "Per step:" line near the bottom already partially restates this - unify them so the instruction appears once, as a numbered sequence.


Todos:

- Add commit-override clause to always.mdc workspace rule
- Rewrite the commit instruction as standalone imperative per prompts-rulebook rules

### Promptforge quickref file

*Write a compressed LLM quickref into promptforge.md covering launch commands, config formats, YAML frontmatter, and prompt structure - minimal tokens, maximum utility for a fresh chat context.*

# PromptForge Quickref

Write into `promptforge/promptforge.md`. The file's purpose: an LLM loads it at the start of a chat and immediately knows how to write and run PromptForge prompts. Compressed - no tutorial prose, no rationale, just the facts.

## Sections (mirrors the output file structure)

### 1. Dev Runner
- Command: `promptforge-dev [--watch] [--capture-raw] <prompt.md> [input]`
- Required env: `PROMPTFORGE_GATEWAY_URL`, `PROMPTFORGE_GATEWAY_KEY`
- `[input]` becomes `args` in the prompt
- `--watch` reruns on save

### 2. MCP Server
- Command: `promptforge-mcp-server serve [--stdio] <prompts.toml>`
- HTTP default: `127.0.0.1:9310/mcp`, bearer auth
- `--stdio`: JSON-RPC over stdin/stdout

### 3. Gateway
- Command: `promptforge-gateway serve [--profile NAME | config.toml]`
- Required env: `PROMPTFORGE_GATEWAY_KEY`, plus API keys per endpoint

### 4. `prompts.toml` (MCP server config)
- Minimal example showing `[server]`, `[gateway]`, `[paths]`, `[catalog]`
- Key fields only

### 5. `gateway.toml` (gateway config)
- Minimal example showing `[server]`, `[[endpoint]]`, `[[model]]`
- One remote endpoint, one model
- `[tools.web_search]` for web search

### 6. YAML Frontmatter
- Table of fields: `name`, `description`, `promptforge`, `default_return`, `max_tool_iterations`, `input`, `output`
- All types and constraints in one compact table

### 7. Prompt Structure
- H1 (exactly one) - title + tool/model resolution in Lua
- H2 sections - executed top-to-bottom
- ` ```lua ` fences for executable Lua
- ` ```lua shared ` for shared library
- Prose becomes model turns
- Substitution: `{{ args }}`, `{{ var.x }}`, `{{ reply }}`

### 8. Lua API (one-line per function)
- `tools.need(alias, description)`, `tools.add(alias...)`
- `models.always(alias, description)`, `models.need(alias, desc, opts)`, `models.use(alias)`
- `store.read(path)`, `store.write(path, content)`, `store.read_lines(path)`, `store.append(path, content)`, `store.str_replace(path, old, new)`, `store.delete(path)`, `store.glob(pattern)`, `store.exists(path)`
- `var.x = ...`, `args`, `reply`, `log(msg)`
- `return value` (ends run), `jump("## Section")`, `execute("## Section", input?)`

### 9. One Complete Example
- A prompt with tools.need, models.always, store, and substitution - showing the full pattern in ~15 lines

## Constraints

- Target: under 300 lines total
- No prose paragraphs - bullet lists, tables, and code blocks only
- No rationale or "why" - just "what" and "how"
- One example per concept, not three


Todos:

- Write the compressed quickref into promptforge/promptforge.md

## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge\promptforge.md

# PromptForge Quickref

This file is loaded into an orchestration model's context so it understands how to write and run PromptForge prompts.

## 1. Gateway

- **What:** HTTP proxy routing model completions to upstream providers (Anthropic, OpenAI, local llama-server). Start first.
- Command: `cargo run -p promptforge-gateway -- serve gateway.toml`
- Env: `PROMPTFORGE_GATEWAY_KEY`, plus per-endpoint keys (e.g. `ANTHROPIC_API_KEY`)
- Default bind: `127.0.0.1:8081`

## 2. MCP Server

- **What:** Exposes prompts as MCP tools to an orchestrator (Cursor, Claude Code). Resolves names, runs prompts, streams progress.
- **Requires:** running gateway.
- Command: `cargo run -p promptforge-mcp-server -- serve [--stdio] <prompts.toml>`
- HTTP default: `127.0.0.1:9310/mcp`, bearer auth
- `--stdio`: JSON-RPC over stdin/stdout (for Cursor MCP config)
- Env: `PROMPTFORGE_MCP_TOKEN`, `PROMPTFORGE_GATEWAY_KEY`

## 3. Dev Runner

- **What:** Single-prompt edit-run loop for authoring. Runs one prompt, prints result, optionally watches.
- **Requires:** running gateway.
- Command: `cargo run -p promptforge-dev -- [--watch] [--capture-raw] <prompt.md> [input]`
- Env: `PROMPTFORGE_GATEWAY_URL`, `PROMPTFORGE_GATEWAY_KEY`
- `[input]` becomes `args` in the prompt; `--watch` reruns on save

## 4. `prompts.toml` (MCP server config)

Minimal:

```toml
[server]
token = "${PROMPTFORGE_MCP_TOKEN}"

[paths]
prompts = "prompts-mcp"

[gateway]
url = "http://127.0.0.1:8081/v1"
key = "${PROMPTFORGE_GATEWAY_KEY}"

[tools]
web_fetch = true
web_search = true
```

- `[tools]` defaults to nothing enabled (true sandbox). Enable what the prompts need.
- `[catalog]` optional: `include`/`exclude` globs relative to `[paths].prompts`
- `[prompts.NAME]` optional: per-prompt overrides (`enabled = false`, `file = "path"`)
- Full schema: `crates/promptforge-mcp-server/design-mcp-server.md`

## 5. `gateway.toml` (gateway config)

Minimal remote:

```toml
[server]
bind = "127.0.0.1:8081"
key = "${PROMPTFORGE_GATEWAY_KEY}"

[[endpoint]]
id = "anthropic"
protocol = "openai"
base_url = "https://api.anthropic.com/v1"
api_key = "${ANTHROPIC_API_KEY}"
concurrency = 10

[[model]]
name = "claude-sonnet-4-6"
description = "A model suited for careful analysis, coding, and general assistance"
context = 200000
thinking = "never"
upstream = "claude-sonnet-4-6"
endpoints = ["anthropic"]
```

- `[[local_model]]` for GGUF: `source`, `sha256`, `context`, `gpu_layers`, `flash_attention`
- `[tools.web_search]`: `provider = "brave"`, `api_key = "${BRAVE_API_KEY}"`
- Full schema: `crates/promptforge-gateway/design-gateway.md`

## 6. YAML Frontmatter

| Field | Required | Type | Meaning |
|---|---|---|---|
| `name` | yes | string | Identifier, `^[a-z][a-z0-9_]{0,47}$` |
| `description` | yes | string | One-line for listings and retrieval |
| `promptforge` | yes | int | Engine major version. Only `1` today |
| `default_return` | no | string | Returned on fall-through |
| `max_tool_iterations` | no | int 1-1000 | Tool-loop cap (default 24) |
| `input` | no | object | `path` + `description` of expected store input |
| `output` | no | object | `path` + `description` of produced store output |

Authoritative schema: `crates/promptforge-core/src/parser/build.rs`

## 7. Prompt Structure and Lua API

- Exactly one **H1** - title + H1 Lua (tool/model resolution)
- One or more **H2** sections - executed top-to-bottom (fall-through)
- ` ```lua ` fences for executable Lua; ` ```lua shared ` for shared library
- Prose becomes model turns; substitution: `{{ args }}`, `{{ var.x }}`, `{{ reply }}`
- Lua return (scalar) ends the run early

Key Lua API:
- `tools.need(alias, desc)` - resolve a tool by description
- `tools.add(alias...)` - make resolved tools available to the model
- `models.always(alias, desc)` / `models.need(alias, desc, opts)` / `models.use(alias)`
- `store.read(path)`, `store.write(path, content)`, `store.append(path, content)`
- `store.read_lines(path)`, `store.str_replace(path, old, new)`, `store.delete(path)`
- `store.glob(pattern)`, `store.exists(path)`, `store.inject(path)`
- `var.x = ...`, `args`, `reply`, `log(msg)`
- `return value`, `jump("## Section")`, `execute("## Section", input?)`

Full reference: `guide/src/prompt-files.md` (structure), `guide/src/lua.md` (Lua API)

## 8. Example

```markdown
---
name: research_person
description: Research a person from the open web
promptforge: 1
max_tool_iterations: 20
---

# Research a Person

` ``lua
tools.need("search", "Search the web and return results.")
tools.need("fetch", "Fetch a web page as markdown.")
models.always("researcher", "A model suited for careful analysis")
` ``

## Research

` ``lua
tools.add("search", "fetch")
` ``

Research this person using live web tools. Return a factual summary.

{{ args }}
```

More examples: `prompts/`

## 9. Local MCP Prompts

- `prompts-mcp/` - gitignored directory for local prompts served by the MCP server
- `prompts-mcp.toml` - config serving that directory (also gitignored)
- Drop any `.md` prompt file into `prompts-mcp/` and it's live (with `--watch`)
- Launch: `cargo run -p promptforge-mcp-server -- serve prompts-mcp.toml`


### c:\Users\Vinnie\src\cursor\promptforge\promptforge.md

# PromptForge Quickref

Load this file to write and run PromptForge prompts. The repo root is `c:\Users\Vinnie\src\cursor\promptforge`.

## Running a prompt

When the user says `promptforge <prompt.md> [input]`:

1. Check terminals for a running `promptforge-gateway`. If absent, start one in a background terminal from the repo root:
   ```
   cargo run -p promptforge-gateway -- serve gateway.toml
   ```
   Wait for the line containing "listening" before proceeding.
2. Export env vars in the execution shell if not already set:
   ```
   export PROMPTFORGE_GATEWAY_URL=http://127.0.0.1:8081/v1
   export PROMPTFORGE_GATEWAY_KEY=dev-secret
   ```
3. Run the prompt from the repo root:
   ```
   cargo run -p promptforge-dev -- <prompt.md> [input]
   ```

The gateway persists for the session. Skip step 1 on subsequent runs.

If the prompt contains only Lua (no prose outside fences), it runs without a gateway.

Prompts in `prompts-mcp/` use path `prompts-mcp/<name>.md`.

## Components

| Component | Command | Env required | Default bind |
|---|---|---|---|
| Gateway | `cargo run -p promptforge-gateway -- serve gateway.toml` | `PROMPTFORGE_GATEWAY_KEY`, `ANTHROPIC_API_KEY` | `127.0.0.1:8081` |
| MCP Server | `cargo run -p promptforge-mcp-server -- serve [--stdio] <prompts.toml>` | `PROMPTFORGE_MCP_TOKEN`, `PROMPTFORGE_GATEWAY_KEY` | `127.0.0.1:9310` |
| Dev Runner | `cargo run -p promptforge-dev -- [--watch] [--capture-raw] <prompt.md> [input]` | `PROMPTFORGE_GATEWAY_URL`, `PROMPTFORGE_GATEWAY_KEY` | n/a |

Start the gateway first. The MCP server and dev runner both call through it.

## `prompts.toml` (MCP server config)

```toml
[server]
token = "${PROMPTFORGE_MCP_TOKEN}"

[paths]
prompts = "prompts-mcp"

[gateway]
url = "http://127.0.0.1:8081/v1"
key = "${PROMPTFORGE_GATEWAY_KEY}"

[tools]
web_fetch = true
web_search = true
```

- `[tools]` defaults to nothing enabled (true sandbox). Enable per prompt needs.
- `[catalog]` optional: `include`/`exclude` globs relative to `[paths].prompts`.
- `[prompts.NAME]` optional: per-prompt overrides (`enabled = false`).
- Full schema: `crates/promptforge-mcp-server/design-mcp-server.md`

## `gateway.toml` (gateway config)

```toml
[server]
bind = "127.0.0.1:8081"
key = "${PROMPTFORGE_GATEWAY_KEY}"

[[endpoint]]
id = "anthropic"
protocol = "openai"
base_url = "https://api.anthropic.com/v1"
api_key = "${ANTHROPIC_API_KEY}"
concurrency = 10

[[model]]
name = "claude-sonnet-4-6"
description = "A model suited for careful analysis, coding, and general assistance"
context = 200000
thinking = "never"
upstream = "claude-sonnet-4-6"
endpoints = ["anthropic"]
```

- `[[local_model]]` for GGUF: `source`, `sha256`, `context`, `gpu_layers`, `flash_attention`.
- `[tools.web_search]`: `provider = "brave"`, `api_key = "${BRAVE_API_KEY}"`.
- Full schema: `crates/promptforge-gateway/design-gateway.md`

## YAML Frontmatter

| Field | Required | Type | Meaning |
|---|---|---|---|
| `name` | yes | string | Identifier, `^[a-z][a-z0-9_]{0,47}$` |
| `description` | yes | string | One-line for listings and retrieval |
| `promptforge` | yes | int | Engine major. Only `1` runs today |
| `default_return` | no | string | Returned on fall-through |
| `max_tool_iterations` | no | int 1-1000 | Tool-loop cap (default 24) |
| `input` | no | object | `path` + `description` of expected store input |
| `output` | no | object | `path` + `description` of produced store output |

Authoritative schema: `crates/promptforge-core/src/parser/build.rs`

## Prompt Structure

- Exactly one **H1** - title + H1 Lua (tool/model resolution)
- One or more **H2** sections - executed top-to-bottom
- ` ```lua ` fences for executable Lua; ` ```lua shared ` for shared library
- Prose outside fences becomes model turns
- Substitution: `{{ args }}`, `{{ var.x }}`, `{{ reply }}`
- Scalar `return` from Lua ends the run

## Lua API

| Function | Effect |
|---|---|
| `tools.need(alias, desc)` | Resolve a tool by description |
| `tools.add(alias...)` | Make resolved tools available to the model |
| `models.always(alias, desc)` | Bind a model for this section |
| `models.need(alias, desc, opts)` | Bind with options (thinking, context, temperature) |
| `models.use(alias)` | Switch to a previously bound model |
| `store.read(path)` | Read file verbatim |
| `store.write(path, content)` | Create or overwrite file |
| `store.append(path, content)` | Append to file |
| `store.read_lines(path)` | Read with line numbers |
| `store.str_replace(path, old, new)` | Edit by unique anchor |
| `store.delete(path)` | Remove file |
| `store.glob(pattern)` | List matching paths |
| `store.exists(path)` | Check existence |
| `store.inject(path)` | Read wrapped in untrusted envelope |
| `return value` | End run, return value |
| `jump("## Section")` | Transfer control |
| `execute("## Section", input?)` | Run section as subroutine |
| `var.x = ...` | Cross-section state |
| `log(msg)` | Emit to observer |

Full reference: `guide/src/prompt-files.md` (structure), `guide/src/lua.md` (API)

## Example

```markdown
---
name: research_person
description: Research a person from the open web
promptforge: 1
max_tool_iterations: 20
---

# Research a Person

```lua
tools.need("search", "Search the web and return results.")
tools.need("fetch", "Fetch a web page as markdown.")
models.always("researcher", "A model suited for careful analysis")
```

## Research

```lua
tools.add("search", "fetch")
```

Research this person using live web tools. Return a factual summary.

{{ args }}
```

More examples: `prompts/`

## Local MCP Prompts

- `prompts-mcp/` - gitignored directory for local prompts
- `prompts-mcp.toml` - config serving that directory (also gitignored)
- Drop a `.md` prompt file into `prompts-mcp/` and it is live (with `--watch`)
- Launch: `cargo run -p promptforge-mcp-server -- serve prompts-mcp.toml`


StrReplace-edited design docs (path only): `c:\Users\Vinnie\src\cursor\promptforge\promptforge.md`
