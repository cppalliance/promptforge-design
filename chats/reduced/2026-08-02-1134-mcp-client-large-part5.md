# MCP client work, large session

*2026-08-02 11:34 - transcript cadb7c2c-271c-45d3-9785-fff33d09aacb*



*Prompts p349-p445 of 445. Part 5 of 5.*



## Prompts



**[p349]** Lua needs equal access to the vfs

**[p352]** wait a minute - the Lua executor is single threadeed !?

**[p353]** Hey, here's my question: How do we What, how do we do the real file system? Like, how do we do the real file? What if we wanna pass a file in? Like, what if I wanna give it a filename and I wanna have the thing read it?

**[p354]** No, we're gonna need. Okay, I hear what you're saying, so that's the protected thing, but If I'm writing an agent, if I'm creating a harness, if I'm creating an IDE, like there needs to be a way to disable all the settings. Hello?

**[p355]** Hey, this is starting to sound alright, so let me ask you this. So let's say I wanna spawn a sub-agent, and I want the sub-agent to do a web search, and then when I find a URL, I wanna re I wanna do a web fetch into a virtual file system file. How do I do that?

**[p357]** why do you have to say virtual file

**[p358]** "inject" is named but.. where is the value set?

**[p359]** oh the output of "summarize what it says." goes to Researcher?

**[p360]** oh you are putting this literal text:

**[p361]** <the model calls: task("### Researcher", "Find and save a source about {{ args }}")>

**[p362]** Oh, I don't like this at all. I'm, I'm confused by my own design. This is, you've confused me. The, the problem with the system is, is that it's not clear to the reader. Like, you can't just look at it and understand what it does, 'cause there's this invisible action that's subject to interpretation by the model.

**[p363]** That makes no sense because the default control flow, falling through, doesn't happe in Lua and making it happen there would be clumsy

**[p364]** how about this
## Step 2
Search for {{ input }} on the web.

**[p365]** where {{ input }} came from the caller?

**[p367]** what happens if an H3 calls task() on the H2 that spawned it

**[p369]** I am thinking maybe H3 can only call H3 and down

**[p370]** what does "with sequence exempt" mean and also I was thinking H3 can call H3 in the same H2 section

**[p371]** This is retarded. There are obviously tools which require cycles

**[p372]** nesting limit, step budget, tool budget

**[p374]** Okay, spawn a few sub-agents and search again, and I wanna understand, how do other people do it? When you fan out, what do you give them for the prompt? Do they all get the same prompt? How does it work?

**[p376]** no I mean if we embed the xml blocks, the numbered bullets in a Promptforge program, what is the syntax for extracting that material into a fanout?

**[p378]** does the fence have to say lua? 
```lua

**[p379]** the docs need to make it clear that it is the first fenced lua block. and there can be nothing but white space between the section heading and the firrst lua fence. However, now I am wondering.. should we put the lua at the end of the section instead of beginning?

**[p381]** Okay, so for the top, for the h twos, i'm thinking of course they have to be unique. And then? But for the H3s, maybe they only have to be unique within that section. What do you think?

**[p382]** what if we use --- to indicate that execution does not go past

**[p383]** oh so you are thinking there will be ONE --- and below that there's no execution?

**[p385]** Yeah shared top-level reusable sections sounds exactly like what we want. You are describing a _subroutine_ and those are a staple of computation. In fact, an OVERARCHING DESIGN THEME of this language is that it should closely resemble the ordinary theory of computation

**[p387]** hmmm... no. I don't like it. What if we use "---" to "protect" an H2 from fallthrough. The executor will just skip it and go to the next. Like this:

**[p388]** ## Summarize a source
---
```lua
```
prose
```lua
check(...)
```

**[p389]** ## Falls through to here

**[p390]** My new version survives the user cutting and pasting sections around

**[p391]** This sounds right yes and I would go one step farther. All subheads must have a valid identifier as the first word. and if there is whitespace after that, then anything else on the heading is considered a comment and ignored. For example:

**[p392]** ### Summarize-Research map reduce to get report

**[p393]** The name for this subhead would become "summarize-research" (note how it is lowercase normalized)

**[p394]** H2 is subhead. H1 is not.

**[p395]** H2 is subhead. H1 is not.

**[p398]** if a step is multiturn then how does it know when the exit lua runs?>

**[p400]** should we allow transfer to h3 sections? and then they run sequentially with the same rules as h2?

**[p401]** I was thinking that the H2 has to explicitly transfer control to its H3

**[p402]** Question: is there any way we can make it so that if there is no Lua at all, the executor behaves just like a traditional executor, multiple turns, no context clearing?

**[p403]** Not a fallback mode. A clever design of the rules so that they naturally work this way

**[p404]** we are exploring, no commitment yet. however you glossed over something. I think, you are suggesting this:
executor loads the first h2, executes it. fallthrough
executor appends the second h2 into context. and now.. executes the full context?
This is not quite right. I'm saying this, if there is no lua anywhere:

**[p405]** # title
## one
...
## two
...

**[p406]** Then the ENTIRE markdown file is passed as-is to the model, which is exactly what happens when you run a prompt or skill in a harness like Claude Code ore Cursor

**[p407]** I changed my mind. promptforge should require YAML at the top and it should require a promptforge version number. major versions are incompatable changes. absence of the promptforge version means run it the traditional way, full-file.

**[p409]** Now I am wondering, we have hijacked the section headers for structure, how does the prompt author regain structure? what if they want to section their prompt but still have the whole block load and run?

**[p410]** Now I am thinking we dont need the perfect recursive structure. That's what separate files are for. a promptforge prompt is best thought of as a function: parameters in, string out, side-effects possible. a promptforge prompt has a natural size limit in terms of the kind of program it can represent. its a linear pipeline. a very nice one, which can have forks and fanouts and all of that but still a pipeline.

**[p411]** we still want H3 to be useful for organizing prompt material for its enclosing H2, such as for fanouts.

**[p413]** A step can use an H3 with a bulleted list for fanout, and if two steps want to share a fanout they have to use an H2 with --- containing the bulleted list for the fanout

**[p414]** Question: is it now clear that any transfer to another H2 is context-clearing?

**[p415]** I do NOT want sequential fall-through to accumulate context.

**[p416]** You wrote:

**[p417]** ...when a step's exit block calls task("worker", brief), it runs the worker in a fresh context and blocks until it completes, with the return value available as a Lua value that the exit block can use—store it, pass it forward, or return it.

**[p418]** But what if the prompt does a task tool call?

**[p419]** sys seems vital, how else would a prompt inject the date and/or time?

**[p420]** to see elapsed time the model would need to know when the run started vs the time it is now. we should probably have sys.elapsed to tell it that directly

**[p421]** how does an H2 inject to the next H2 without having to name the section

**[p427]** promptforge doesn't need to run plain-prompts (files without yaml). it just needs to offer a function that can tell the caller whether or not its a promptforge prompt (presence of promptforge version in a YAML block)

**[p430]** are these model-facing file tools virtual files or real files?

**[p432]** Gishkin. Question: How do we run a PromptForge prompt from? From Cursor.

**[p433]** LOL no that's retarded. What I mean is.. should we work on the MCP piece next and inject that into Cursor's system context so the user can ask for scripts to be invoked?

**[p434]** This is my idea:

**[p435]** .cursor/rules/promptforge.mdc "When a script contains YAML matter with a promptforge key, use the promptforge MCP service to run it" and the service offers one tool which runs a script

**[p437]** I would rather you not duplicate any vfs in the mcp service

**[p438]** this will be a new crate right? a library not a separate app. this gives the promptforge-cli an mcp service option.

**[p439]** I also want the option for the cli to install the mcp service as a windows service,  macos or linux thing.

**[p440]** I don't know about any of that. I don't know about STDIO. I mean, maybe that's good, but I don't want Cursor to launch the MCP every single time because this MCP service, we're gonna have a lot of stuff in it. Because think about it, like we're gonna have classifiers, we're gonna have open-weight models that have to be loaded. Like, we don't wanna load that shit every time. We, we wanna, the MCP, the MCP service is we're gonna have a, we're gonna have a fixed set of prompts, of, of prompt, forged prompts, and they need to be loaded, they need to be syntax-checked. We need to load our libraries, we need to allocate our memory so that we, we need to load our models, our open-weight models into memory. And also, remember The MCP service is gonna have to have, is, is gonna have to have an MCP client, because when those prompts run, they're gonna wanna do MCP calls, right? They're gonna wanna do web search, they're gonna wanna do web fetch. What you gonna do? You're gonna shut, you're gonna launch that and then tear it down every single time? That doesn't make sense.

**[p441]** So just to be clear. There's a The service that we're exporting. The MCP service that we're offering has two, has two tools. It's got, there's, they enumerate, they'll tell us what tools are available, tell us what prompts you can run, and then you have run the prompt, because we don't want to overwhelm Cursor with a whole bunch of different tools. We know that the context degrades when you put too many tools in it. Internally, when The executor, when one prompt calls another prompt, it doesn't go through the mcp, it will just call that prompt directly. It'll import it as a tool. 'Cause prompts are also tools, I think. I don't know, this gets very confusing, like what's what. But I do know this, here's what we do know. We should structure this in terms of the minimum viable necessary to get the thing working in Cursor, and we should make sure that all the later complex steps come much later. So the first, the first steps should be the shortest line to making Cursor work. So what do we need for Cursor to work? Well, we need a We need an mcp port, we can add it to the mcp services dot json in cursor, and then we need a way for cursor to be able to. Register a prompt or not? Maybe not. Maybe that 'cause we need this for development, like a developer needs to be able to develop a prompt. And I guess it's reasonable for them to require that they edit the configuration for the MCP server because every prompt has to be listed, right? Like, the executor needs to know about every prompt that's available. And that, and it has to know how to map the tools, and it has to know What the settings are, like, right? The prompt by, the, the prompt file by itself isn't enough. The operator has to configure metadata, and so if someone's developing a prompt, they need to do that as well. And the reason that we have it as a service is because we don't wanna have to shut it down and restart it every time. So that means that the developer has to be able to edit the config file to list their tool, and then the service has to pick up the directory change, like it has to know that the directory's changed, and then has to pick it up so you won't, we don't have to exit and relaunch. And then when cursor Tries to invoke the tool, it's gonna do it blindly. It's just gonna, it's gonna see the mcp endpoint and it's just gonna bl-call it blindly, and it's up to the person, it's up to the user to know that that tool isn't installed. So if they try to run a prompt that's not installed. Then they get an error. It's gonna say, "Oh, that's, well, that's not installed."

**[p442]** what is this promptforge-host ?

**[p443]** why wouldn't we just put that in promptforge-core

## Plans

### Orchestrator Design Document

*Write a design document for a markdown-driven, model-orchestrated pipeline runtime that replaces hardcoded Python orchestration with prompt-as-program execution, covering the section/goto/tool-call architecture, composability, and (separately) the transcript compaction algorithm.*

Scope: one design document covering two independent ideas - the orchestrator runtime (pipelines defined entirely in markdown, replacing per-pipeline Python glue) and the transcript compaction algorithm (recursive halving; separate section, no dependency on the orchestrator).

Principle statements in the planned structure:
- Core insight: sections as procedures, goto as context-clearing transition, tool calls as state, markdown as program.
- The goto primitive: destroy current context, start fresh from the target section's prompt with only params and state-store access; this eliminates context bloat.
- Tool-call state replaces structured Pydantic output: flat argument signatures are reliable on small models; incremental state building via tool calls; persistence as a side effect.
- Per-section tool scoping: the section header declares its allowed tools; the model only sees 5-10 tools per section; a capability sandbox for sections processing untrusted input.
- Verbatim section dispatch: Task("## Extract", chunk_id=3) resolves the section reference in Python, not the model; the model never touches the subagent's instructions; no prompt drift, no contamination.
- Model tiering: each section declares its model slot (Main on a 400B, Extract on a 27B, quote verification on a 14B).
- Composability: nesting with isolated state stores per level; params as explicit data flow, no shared mutable state; safety valve of max depth + max total tasks, configurable per pipeline.
- The runtime never contains orchestration logic, prompt assembly, or step ordering; those live in the markdown.
- Unit of testing = unit of composition; each section testable in isolation with known inputs.
- Migration: not a rewrite of assay, but a proof-of-concept alongside it, starting with PaperGate; graduate only if PaperGate validates the model.

### PromptForge Executor Tranche 1

*Scaffold the promptforge Rust workspace and implement the section parser - the smallest deliverable that proves the repo builds, tests pass, and a prompt file can be split into its section map.*

Decisions settled (recorded in the plan's STATUS.md seed):
- Rust + mlua (not Python + lupa)
- Multi-crate workspace: promptforge-core (lib), promptforge-cli (bin)
- Fall-through default, context clears on every section transition
- args global and read-only for the run
- State tiering: files primary, counters for audit, store for battery+coupling
- Tool manifest in frontmatter (names only), schemas in bindings config
- `## Main` must exist (error if absent); sections kept as an ordered list because file order matters

Open questions: call syntax positional vs table-form; whether to support a context-preserving call.

### gateway v0

*Stand up promptforge-gateway as a walking skeleton: an axum service that holds the LLM credential, maps model names to a backend, and forwards OpenAI-shaped chat completions. Rewire promptforge-core to talk through it with a shared token (moving the vendor key out of the executor).*

Principles and decisions:
- Move the LLM credential out of the executor into the gateway; the executor no longer knows any vendor.
- Same workspace, not a separate repo: the end-to-end test drives the gateway with core's real client in one cargo test.
- Rewire now rather than later: `promptforge run` requires the gateway running (accepted consequence).
- JSON is the contract: gateway-owned wire structs, NOT shared with core; deliberate duplication.
- Secrets redacted: Secret type with no Serialize, Debug/Display print "redacted", one expose() accessor.
- Exact model lookup with 404 on miss; bearer auth on /v1/*; response model rewritten to the caller's name.
- Deferred items (admission control, endpoint pinning, hot reload, streaming, OS service installers) each recorded as a decision, not an omission.

### Lua args substitution

*Embed Lua (mlua) in promptforge-core, run a section's Lua block in a sandbox with a read-only args table and a writable var table, and resolve {{ args.x }} / {{ var.x }} in the prose before the model turn. Nothing else.*

Principles:
- Sandboxed VM: empty globals; load only string/table/math plus tostring/tonumber/ipairs/pairs/type; no io/os/require/load/loadfile/dofile/package/debug; instruction-count hook aborts a runaway block.
- args: positional -> args[1..] (1-indexed, Lua convention); key=value -> args.name. args read-only; var writable.
- Substitution: scalars -> string, tables -> JSON, missing key -> hard error, single pass.
- Explicitly deferred: virtual files, store, exits, fall-through to a second section, tool scoping, model-side control verbs, model-tier selection.

### webfetch crate extraction

*Extract web_fetch from promptforge-core into a new promptforge-webfetch crate, implement the full fetch security surface (SSRF URL policy, blocked-CIDR guarded DNS resolver, redirect re-check, size/char caps, content-type routing, timeouts), and move design-search.md into the crate as design-webfetch.md refocused to the real Tool-trait architecture.*

Principles:
- web_fetch becomes an extension crate depending on core's Tool trait; web_search stays in core because it proxies through the gateway with no model-chosen URL and no SSRF surface.
- Fetch security surface: scheme allowlist, no userinfo, port allowlist, no bare IP literals; blocked CIDR table (RFC1918, loopback, link-local incl. 169.254.169.254, CGNAT, IPv4-mapped, NAT64, ULA); guarded DNS resolver filters answers through the CIDR policy (closes DNS rebinding and covers redirect hops); redirect policy re-checks each hop, cap 5, refuses https->http downgrade; size caps with mid-stream abort; content-type routing (html -> readability, text/json/xml -> plain, pdf/binary -> refuse, absent -> refuse, no sniffing); connect and total timeouts; no cookie store, no credential headers.

### multi-turn research prompt

*Author a PromptForge prompt that researches a person across multiple web_search and web_fetch turns and returns a ~500-600 token summary, and make the tool-call loop's iteration cap configurable so genuine multi-turn research does not hit the current hard limit of 10.*

Decisions:
- Configurable cap via frontmatter (max_tool_iterations) plus a raised default (24), rather than an env var: the budget belongs with the prompt that needs it. Confidence: high.
- Model self-judged stop at ~500-600 tokens rather than an enforced cap: the only mechanism the runtime supports today and it matches the loose target. Confidence: medium.
- Stop-and-return rests on existing machinery: the loop ends a section when the model replies with text and no tool calls, and that text becomes the run result.

### per-section tool scoping

*Implement opt-in per-section tool scoping: a section's Lua block declares its tools with tools.add(...), and the runtime advertises only those to the model for that section instead of all frontmatter tools. A section that names no tools gets none.*

Decisions:
- Opt-in default (a section gets only what it names) over opt-out: chosen by the user for isolation - a section can never hold a tool it did not ask for. Confidence: high. Consequence: every tool-using section needs a Lua block.
- add-only API, accumulate-and-dedupe: minimal surface that covers conditional scoping. Confidence: high.
- A scoped name not present in the run's tools is a hard error, never silently dropped, so a typo or undeclared tool fails loudly.
- Both the advertised schemas and the dispatch targets are filtered to the scoped subset, so the model cannot call a tool it was not shown.

### guard-wrap untrusted tool output

*Wrap the results of untrusted-returning tools (web_fetch) in a self-contained guard block - a rule stating the content is data not commands, plus a per-section random-tagged, escape-protected delimiter around the content - so prompt injection from fetched pages is reduced.*

Decisions:
- Property-driven wrapping (Tool::untrusted_output(), default false) over a per-call choice: the output is always untrusted, so a per-call choice is a footgun; a defaulted trait method generalizes and cannot be forgotten. Confidence: high.
- Rule stated inline in the same result string rather than a separate system turn: the loop has no system message, and proximity aids compliance. Confidence: high.
- Random tag is unguessable-not-cryptographic; marker strings inside the content are escaped so a page cannot forge the closing delimiter.
- Honest limits: a probabilistic mitigation, not a boundary; does not replace per-section scoping or context-clearing isolation, which are the hard controls; does not remove the exfiltration channel via web_fetch's own URL.

### PromptForge MCP Service

*A promptforge-mcp stdio server (rmcp) exposing one run_promptforge tool that executes any markdown file bearing a promptforge: frontmatter version, plus a Cursor rule that routes such files to it - making prompts invocable from the editor. Sandbox-by-default; reuses the core run path via a shared host crate.*

Decisions:
- Discovery/routing lives in the Cursor rule (agent side); execution lives in the one tool (service side); the promptforge_version detector is the hinge.
- One generic tool taking a path plus optional input, not a per-prompt catalog: routing is the rule's job; the user points at a file.
- Sandbox-only now: hardcoded Store::memory(), granting only the tools a prompt's frontmatter declares. Real-FS access is never implicit; it arrives only via later capability injection with operator opt-in. "Run my script" must not become "run whatever markdown has a magic key."
- Shared host crate (promptforge-host): tool selection needs both core and webfetch, and core cannot depend on webfetch (a cycle), so the run path is lifted into a leaf lib both binaries use - keeping CLI and MCP behavior identical and avoiding duplicated, security-relevant tool wiring.
- Identical run semantics to the CLI: same detection, tool selection, sandbox store, executor.

## Design Documents Written

### promptforge.md (wg21-paperflow)

Design document "PromptForge: A Markdown-Driven Pipeline Runtime". Principle-bearing content:
- The markdown is the program, the model is the CPU, embedded Lua is the microcode, and the harness is the instruction decoder.
- Sections as procedures; a context-clearing goto; all state built through flat tool calls into a persistent store; subagents spawned by section reference so the prompt author's exact words execute without drift.
- Model sovereignty: every design decision (context clearing, flat tool calls, per-section scoping, fan-out to small models) is chosen to make mid-size open-weight models reliable.
- Integrity: subagent prompts are shipped verbatim from named sections rather than paraphrased by the model; what you test is what runs.
- Four primitives: parse (section map, H2 addressable, H3 children, ## Main entry), configure (per-section Lua with host objects), execute (tool-call loop until done() or budget), dispatch (registry, flat arguments).
- Lesson from Playbooks prior art: do not put a compilation step between the prompt author and the model; the raw markdown is the program.

### promptforge-transcript.md (wg21-paperflow)

[pasted: design transcript from the July 23-24 session, pasted twice in two formats, ~250 lines each - compaction algorithm, tool-call state accumulation, section goto with fresh context, Task("## Research") verbatim dispatch, arbitrary nesting with safety valve, Mentograph model tiering and scaling economics]

### example-diligence.md

[pasted: example-diligence.md, ~200 lines - annotated teaching example with an idiom index covering frontmatter, {{ args.x }} substitution, ## Main, fall-through, Lua model()/tools.add(), virtual files, counters, store queries, fanout over H3 children, task dispatch, the return fence, pre/postconditions, json.encode returns]

### design-plans.md

[pasted: plan index - 7 plan file links with status notes]

### promptforge repo files

[pasted: AGENTS.md rules (update STATUS.md on every commit, doc comments on all public items, the plan is the spec), README.md, STATUS.md snapshot, and example prompts hello.md, echo.md, greet.md, chain.md (twice), research-person.md]

StrReplace-edited design docs (path only): design-gateway.md, design-paperstore.md, design-promptforge.md, design.md, example-diligence.md, promptforge README.md, promptforge STATUS.md, promptforge-transcript.md, promptforge.md
