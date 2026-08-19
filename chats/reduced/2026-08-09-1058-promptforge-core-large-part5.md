# Promptforge-core work session, large

*2026-08-09 10:58 - transcript 8c3c647b-f072-4df7-b9a6-01d1158f1a03*

*Prompts p375-p451 of 451. Part 5 of 5. REDUCED.*

## Prompts

**[p376]** hmm I see what you mean. Yes this is a big change. previously we could assume the vm was fixed after the preamble ran. but now, it can change after each completion

**[p377]** One thing I know for certain. If we are going to work on building an analytical pipeline, it is absolutely essential for development and debugging, to be able to re-run the prompt from any step. So we need those intermediate outputs as files which can be read in.

**[p380]** So for the, for the tools changing, like for first exposing search and then exposing fetch, let's just put that off to the side. Let's, let's just put that in the not to be implemented part of the plan. And then for the overlay, so I guess this is a core feature, this isn't a tool in the sense that, like, you load it separately, like this tool has to be integrated into the core because you have the mount. I mean, this isn't like a normal thing, right? I mean, it affects the Lua.

**[p382]** no to list and grep. we are just exploring not planning that.

**[p383]** Right now, we're registering the search as a web search, right? Because we're asking for the need, we're saying we need to be able to search the web. In the prologue. And that And when we expose the tool to the model, we're giving it the same description. But I don't know that we should be doing that, because why does the model care that it's the web? The model just cares that it's searching. Like for example, what if we connect it to a workspace search tool? Or what if we connect it to an MCP search? Or what if we connect it to a rag index? Like when the model only the, the language that the model's using only cares that it's doing some type of searching and that it has to fill in the information in the tool. So I'm thinking we need to be able to rebind the tool in the preamble or even In the H2 or H3, what, like, when you when you inject a tool, we should be able to re to rewrite the description so that we could fit it to what the model expects. This way, the prompt can be written agnostic. Like, the prompt shouldn't say "search the web," the prompt should just say "search."

**[p386]** we are already rebinding the name in the preamble. the tool.need call establishes the name, and the prompt owns it

**[p390]** Okay, but option B, the Lua as tool, this is simpler than what we had before, 'cause before we were talking about reopening the closed toolset, but this isn't that, this is just a function, the toolset remains closed after the preamble, and. It's, it's easier. Or is it? How do we deal with it?

**[p392]** I don't know. This is, so I have one MCP server and it has multiple sources, like it's got the Boost mailing list, it's got the WG21 mailing list, and so this creates a problem because I want the briefer to be generic, but I wanna be able to say, you know, I wanna be able to tell it, okay, use MCP or not, because if my report is destined for the public, I'm not allowed to quote the reflector. So we're actually seeing, we're actually seeing a downside of the pipeline, which is the pipeline is, you're not, the pipeline is rigid. Right? Like when we have Cursor or Claude Code as the orchestrator, it can shape the prompt, right? Like it can reinterpret the instructions to suit them to whatever you ask for. But we can't do that here. We can't shape anything here because we're doing the tools are, are based on, they're in Lua, and the orchestrator, the prompt, the LLM, it can't touch the Lua So we would have to like have a configuration file ahead of time that says that when you run the briefer, now you're allowed to consider these sources.

**[p393]** First of all, the preamble. Okay, the preamble is the H1 code. The prologue and the epilogue are for the sections, is that correct? The plan should enforce that terminology throughout the entire repo. I want every file checked.

**[p395]** its 180 occurrences not 180 files. there's no one to break, this is unshipped. the preamble is meaningfully different from the prologue

**[p396]** I want this to be the first step of the store plan

**[p397]** Question I'm thinking that the, that the preamble has to have inference. Because how are we gonna process the args? Like we need inference, we the model needs to be able to take control and do some tool calls. Like the model needs to be able to parse that string and figure shit out. Right? But then we need the tools to be open. Because if the model, if the model realizes, "Well, we need MCP, but now we have dynamic tool sets, how's that gonna work? "

**[p398]** I think we need first class objects in the Lua. "Tool" needs to be an object type and if you write tools["search"] it gives you the object and it has properties you can inspect and invoke. in other words its a Lua table. And Model needs to be a thing. so you can ask for a model and call infer() or turn() or whatever on it. And the preamble should be able to declare global variables. For example a list of tools. and then in any section you can write

**[p399]** tools.need( search_tools )

**[p400]** and this will work because search_tools is an array of Tool

**[p401]** You're saying full agent programming language, but all we're doing is adding one function. So if you're saying that one function turns it into a full agent programming language, then f-f-what, there's nothing this isn't a future architecture to capture. This is just a natural falling out of making these things first-class objects, and I would argue that they should have been first-class objects in the first place, because that's just good programming hygiene. You always encapsulate, you always model, because this gives us a unit test. We can, we can model, we can have an abstraction that represents a model, an abstraction that represents a tool, and we can put in the mock, and we can test it. And we can have different tool types. I mean, this is just normal. This is a This refactoring should actually help the code become more simple, if anything. And also, let me show you the other problem that it solves. Look at what we can do:

**[p402-p406]** [example Lua sketch: tools.add("search") then model.infer("search for {{args}}") then tools.add("fetch"), then prose "Fetch information about {{args}}"]

**[p407]** lets defer overlay store and make the terminology rename and the first-class-objects the sole work

**[p408]** Spawn multiple sub-agents and search the codebase. I want an idea, I want an understanding of how much simplification are we gonna get, and I want you to show me what the, what the properties are gonna be on these objects. Also, what else should we turn into an object? So we have tool, we have model, what else is there?

**[p409]** Wait a minute, hold on. If you seal up on infer, then we can't adjust, we can't add the tool in the preamble. We can't add the, or the prologue, like we can't add search and then infer and then add fact. That pattern breaks.

**[p411]** do a deep and thorough evaluation of this change using strict subagent discipline. its a big change and I want to be thorough

**[p412]** it sounds to me like the only point to the phase transition is to protect the epilog

**[p415]** This is good. Update the plan with the findings and everything.

**[p416]** use @tools-public/rulebooks/rust-rulebook.md @tools-public/rulebooks/vibe-rulebook.md @tools-public/rulebooks/prompts-rulebook.md

**[p418]** 1. what happens to this syntax: tools.calls["search"]
2. why even have an epilog why not just allow any number of alternating lua/prose?

**[p421]** Something about this isn't right, because we go to the epilogue only when the turn ends without a tool call. So if we do a fetch, then the turn isn't ending, so that means it has to go back. It's gonna stay in that prose.

**[p422]** But then the code that you just showed me doesn't work. This code doesn't work.

**[p426]** Lua needs a way To say That We only advance, we advance on a tool call. Maybe.

**[p427]** One thing that I don't like about infer Is calling model infer. It's not you're putting prose in the code. Prose in the code is ugly. I want prose to be in the markdown section where it can be nicely formatted, where you can have bold, you can have italics, you can have bullets, you can have paragraphs, you can have block quotes, you can have URLs. It's beautiful.

**[p429]** But then, how do you do How do you do the model doing its own how do you make it so that the model can decide when it wants to stop? I guess maybe so that, so that, okay, the last pros section is the loop. That's the only thing that can be a loop, right? So the last probe section has the special property that if there's no tool call, that's the final reply. And if you don't like it, then open another H2. Right? Like if you gonna wanna go back to the singles. So any, any, any prose that's not last is a single shot, it always falls through. The last prose only goes to the epilogue if the reply has no tool call.

**[p430]** So if we're doing this, then if we want, if we really want two loops in one section, we can have the Lua, we can have a function. Instead of infer, we can have execute, and it can mention two different h twos. So the Lua can invoke an H2 itself, so that's like a subroutine. That's powerful, and that's not much more work. We already, we already have that code. We already have to execute sections, so why not give it, make it a function that Lua can call? Hello!

**[p431]** Right, exactly, but wait, we didn't collapse the pipeline. The default is to run the sections in order. And we still have the context clearing go-to, didn't we? We implemented the go-to, correct? Any Lua can call goto and transfer control to another section, and it's a context clearing goto.

**[p432]** yes add execute and add goto and I want the design docs cleaned up. our conversation is preeminent.

**[p433]** local step = tasks["## Research"]
execute(step) -- equivalent to execute("## Research")
goto(step) -- equivalent to goto("## Research")

**[p435]** yes and I want you to search through the source code in a subagent and find the remaining candidates for reification

**[p436]** Here's what I want you to do. I want you to create a new plan. I want you to create a plan to write the PromptForge user guide, and this is a guide for how to write prompts. And I want this to be a beautiful tutorial. In the plan, I want you to have a bunch of steps, maybe twenty steps, and each step corresponds to a section of the user guide. For example, we're gonna start progressive. We're gonna say, "Here's what a prompt looks like," and we're gonna show them the skeleton. We're gonna show the H1, the YAML at the top, the H2, and it's gonna be very simple. We're gonna basically do like the Hello World, and then each section is gonna add something. Like we're gonna show how to do multiple pros, we're gonna show how to do Epilogue. So we can each thing adds something and then it explains it, and then we start the new section. And then, and then by the end, we show a one prompt that has all the capabilities built into it. And then we have a reference where, where we show each Lua function or each Lua object and we have the shape of what it is.

**[p438]** the file goes in@promptforge as user_guide.md

**[p439]** the fences are fucked. you have to use quad-ticks on the outer blocks

**[p440]** Listen up, here's what I want. Now I want you to change the README itself, the README for the repo. Keep the image, keep the title, and but I want a beautiful README that's crisp and clear. It doesn't look cool, it says what it is. It says, you know, PromptForge is a prompting system that uses Lua and it's deterministic and, you know, all that good stuff. Really market it really well. And I want this to be a Basically, I want the README to be a report, but it's more technical, so it looks like a README, but it also is bottom line up front and inverted pyramid, and it has both. It has little code snippets, it has instructions. Instructions on how to build it, it has instructions on how to run it. The current README is a mess, it's a big pile of glop. I want you to go through it and figure out what do we really need and put it in a different file, and then make the README this beautiful document with a couple of emojis here and there, and maybe some badges to CI, where we're gonna like check CI, can we, can we do like a GitHub CI and have it like GitHub Actions build it? Can we do all that? I want all that good shit, man. I want badges, I want it to look good, you know what I'm talking about? Badges go above the image. So the, there's, the structure is H1, s-short paragraph, sizzle paragraph explaining what it is, and then, well, actually, badges, no, H1, badges. No, not even. Badges first, then the h1, then the sizzle paragraph, then the image, and then the readme. Look at a couple of READMEs from other projects to get an idea, or do you even need that? You know what to do. You know what to do, right?

**[p441]** 1. yes
2. create the workflow I want it built and tested
3. use a subagent, yes copy whatever is there to another file I dont care what you call it but verify each item and make sure it is not stale because we changed a lot. do the subagent async so you can proceed with the other work items
4. Boost Software License and put the license file in the repo

**[p442]** Question. Question: Do you think you can create an image? A portrait image that consists of horizontal strips, like one inch or two inches high, and then you dissect it into multiple images, horizontal strips like a banner, and you give each section of the readme its own little banner, like a cool robotic, you know, themed, but it's just a strip. And then, like, can you do that? Do you, can you make a quick Python tool to slice a PNG? Do you think you can generate an image in Do you think that you can generate an image in strips? Like, will the image generator do that?

**[p443]** So I wanna use the robot theme. I'll, I'll, I'll, the pr the existing prompt for the image, I want you to use that theme, but I don't want the co I don't wanna have everything be the same color. Actually, I want like a grungy dystopian cyberpunk with neon. I'll give you another image as a reference. But there's humanoid robots, there's electronics, there's cyber, there's you know, neurological interfaces, there's like, it's that theme, that dystopian William Gibson theme, you know what I'm talking about, right? @tools-public/how-to/images/how-to-falco.png

**[p444]** yes put it in the plan and 6 sounds good

**[p445]** the GHA should abort the run if the branch is updated

**[p447]** CI failed

**[p448]** @promptforge/user-guide.md:414-418 how can this work? the preamble has its own vm. "search" and "fetch" are locals and they disappear when Main runs

**[p449]** what? no. the shared H1 program is NOT "replayed" - or is it?

**[p450]** that's not right it should not execute the preamble again. instead, it needs to serialize the objects out of one vm and then back into the other. think about it - if the preamble calls infer() then are we going to replay that for every H2?

**[p451]** go through the user guide and for each section, research the code and make sure it sync up. fix the guide if it does not match.

## Plans

### section-lua-lifecycle

*Refactor PromptForge sections into shared compiled Lua, preamble, prose, and epilog phases with isolated per-section VMs. Add a new authoritative `design-core.md` that explains the complete crate design, rationale, invariants, and supported features while retaining `design-core-orig.md` as history.*

Settled design statements of principle:

- Accept one optional fenced `lua prompt` library anywhere before the first H2. Reject duplicates and any `lua prompt` fence after the first H2 so misplaced executable code cannot silently become prose.
- Compile shared source once, but execute its bytecode independently in every section VM. Authors write helpers once while each section or future fan-out branch receives isolated functions, closures, and mutable globals.
- Keep one VM alive for the whole section: load shared library, inject section host globals, run preamble, await the model, bind final text as `reply`, run epilog, then destroy the VM.
- A scalar top-level return from either preamble or epilog ends the run. A preamble return skips prose, model, and epilog. Nil continues current sequential fall-through.
- The store remains the only intentional cross-section mutable channel; Lua functions, closures, globals, `var`, tools, and `reply` are branch-local by construction.
- Rationale for explicit state boundaries and why mutable run-global Lua is excluded. Current non-goals: fan-out execution, child execution, branching, retries, and persistent bytecode.
- Hard error if `tools.add` is called after preamble tool scoping has closed.

### prompt-fixtures-logging

*Add correlated observer traces and constrained Lua logging, remove unused author prompt versions, and establish file-based prompt fixtures that complement existing inline unit tests.*

Statements of principle:

- Observer reports gain a stable execution ID threaded unchanged through every observation; async tasks may move between OS threads, so the identifier is an execution ID, never a thread ID.
- Observer implementations own synchronization; `log()` adds no global lock and never holds a lock across an await.
- Lua logging is constrained: `print` is removed by the hardening pass; `log(message)` accepts exactly one UTF-8 string, at most 256 characters, no newlines or control characters.
- Lua log text is the single explicit author-controlled exception to the observer's otherwise payload-free detail rule. Documentation forbids logging arguments, replies, tool results, credentials, paths, or store contents.
- The unused author-facing YAML `version:` field is removed everywhere, while required `promptforge:` engine-version behavior remains unchanged.
- File fixtures cover complete author-shaped prompt stories; existing inline tests remain authoritative for narrow grammar, sandbox, and tool-loop edge cases. Register each fixture explicitly with `include_str!`; no directory discovery, manifests, generated loaders, or build scripts.
- Decision falsifiers: revise constrained author logs only if real prompt debugging requires multiline or structured values; do not loosen before examples establish the need. Remove author version only while no real compatibility, cache, or negotiation mechanism consumes it.

### promptforge-dev-loop

*Add a fast prompt-development loop to promptforge-core-tests: subcommands to run the existing fixed scenarios or dev-run any prompt file against a locally cached Qwen3.5 9B on a GPU-enabled llama-server, with verbose trace output and watch-mode reruns.*

Statements of principle:

- The fixed scenarios keep the small model and remain byte-for-byte deterministic; dev mode streams `(execution, section, detail)` observer records and Lua `log()` checkpoints to stderr while the final result prints to stdout.
- Ordinary `cargo test` stays fully offline; real downloads and inference happen only in explicit commands.
- Hand-rolled argv, no clap, matches every workspace binary.
- [pasted: model pins, GGUF SHA-256 digests, GPU asset tables, server flag specifications]

### models debug cluster

*Full cluster in dependency order: a payload DebugCapture seam so empty replies are diagnosable, payload-free observer details for empty/truncated turns, then prompt-level model bindings (`models.need` / `models.use`) with gateway catalog metadata and per-call temperature/thinking, plus user-facing docs throughout.*

Decision log (statements of principle):

- Debug vs Observer: separate `DebugCapture` on `RunOptions`; Observer stays payload-free. Falsifier: any host needs payloads through Observer alone.
- Model binding identity: identity is alias to binding (ModelId + invocation), not to weights - same weights with different params is legal.
- No `models.use` means host default client model (existing prompts behave identically).
- Gateway role: catalog metadata + `GET /v1/models`; request body stays passthrough. Hosts must not invent model metadata out of band.
- Constraint vs invocation: `context` and `thinking` capability filter the catalog; `temperature`, `max_tokens`, and switchable `thinking` ride per request.
- Do not run tool-style near-duplicate rejection across model aliases that share weights with different invocation params.

### completion normalize layer

*Introduce a slender CompletionNormalizer API in promptforge-core (one module, drop-in trait) and make empty final content a hard error - the targeted fix for briefer - while keeping special cases out of execute and hosts.*

Statements of principle:

- One door for wire quirks: field synonyms, empty content, tool-call-with-null-content live in one module instead of execute, client, and hosts. Hosts stay dumb.
- Policy (locked): never promote `reasoning_content` into the answer. Final turn with no tool calls and empty/missing `content` is an error, even when reasoning is present. Tool calls with empty `content` remain valid.
- Hard-fail on empty content will break any prompt that today "succeeds" with empty `reply` (briefer's silent empty `evidence.md`). That breakage is the point.
- Not doing: adopting `genai` / `rig` / a separate published crate in this change. The module is the seam; a crate can graduate later if the file grows.

### webfetch soft errors

*Change web_fetch so recoverable target failures (HTTP non-2xx, unsupported/missing content type, timeout, size, charset, DNS) return Ok tool text the model can read, matching industry soft-error practice, while SSRF and URL-admission policy failures keep aborting the tool call.*

Statements of principle:

- Recoverable target failures (HTTP 4xx/5xx, unsupported/missing content type, timeout, too large, undecodable charset, DNS failure) become `Ok(model_facing_text)` so the tool succeeds and the loop continues; policy/admission failures (invalid URL, blocked scheme/port/userinfo/IP literal, redirect refused) remain hard errors.
- Do not put the HTTP error response body into the tool result (it is untrusted HTML and not useful for recovery). Message names status + final URL + a next-move hint.
- No change to the execute loop contract: tools that still return `Err` abort.

### extract promptforge-dev crate

*Extract the interactive prompt runner into a new `promptforge-dev` crate that talks to an already-running gateway, keep the 0.6B scenario suite self-contained in `promptforge-core-tests`, and ship friendly README + design docs for the new tool.*

Locked decisions:

- Dev mode never starts infrastructure. It requires an already-running gateway; hard-fail with a friendly message if env is missing or the gateway is unreachable.
- Scenario suite keeps its sidecar: real-inference integration tests stay self-contained without Brave or a hand-started gateway.
- Server knobs leave the CLI; after the split they belong only in the operator's gateway config.
- Model catalog comes from the live gateway, not pinned, so prompts track the live deployment.
- Dump-before-run so stale traces never masquerade as the current run. Observer/debug stay out of the result stream (stderr / `.trace/` only).

### local.toml bigger model

*Create operator gateway profile for the pinned Qwen3.5-9B local model so `promptforge-dev` binds that model instead of Anthropic Sonnet.* [pasted: TOML profile contents]

### gateway download progress

*Add an indicatif progress bar to promptforge-gateway local artifact downloads so large GGUF fetches are visible on a TTY; non-TTY gets periodic tracing logs.* [implementation detail only]

### Tool dialect plugins

*Replace ad-hoc ContentFence hacks and prompt-side tool_code instructions with a catalog-selected ToolDialect plugin registry: gateway advertises which dialect each model uses, core applies request/response/history normalization so prompts stay dialect-agnostic.*

Statements of principle:

- The operator sets `tool_dialect` on the gateway model entry (same role as vLLM's parser flag); gateway advertises it on `GET /v1/models`; core freezes it onto the bound model at section scope close. The tool loop selects the plugin and never asks the author prompt what format to use.
- Not by sniffing completion text in the prompt author surface, and not by hardcoding model names inside prompts.
- Request-side dialect injection builds synthetic harness text from the live ToolSchema list; author prompts only say "use search/fetch to research X" - no format recipes.
- Unknown catalog dialect id is a hard bind/run error naming the missing plugin; no silent fallback.
- Wire quirks live in the normalize family, not execute/hosts. Prompts stay dialect-agnostic; accrete new models by adding a cribbed plugin plus setting `tool_dialect` on the model entry.

### Commit local WIP

*Commit the six uncommitted promptforge files as two focused commits, leaving the tree clean before write-through trace work.* [bookkeeping only]

### Write-through store traces

*Make promptforge-dev write `.trace/` turn JSON and store files to `<stem>.store/` as events happen, instead of buffering until the run ends. Dev-crate only; no core API change.* [implementation detail only]

### Fanout and gateway concurrency

*Wire local llama `--parallel` to gateway lane concurrency, set Gemma's lane to 2, and run fanout arms concurrently in core so briefer topics overlap under gateway admission.*

Statements of principle:

- Core fires all arms at once; the gateway admits up to P; extra arms wait in the existing fair queue. One knob: local lane concurrency is both the admit limit and llama `--parallel`.
- Fanout replies stay ordered (indexed by arm order); fail-fast aborts siblings on first arm error, same invoker-visible behavior as sequential fail-fast.
- Shared StoreRef stays mutex-safe; authors must not assume arm N sees arm N-1 writes.
- Nested fanout remains a non-goal.

### Briefer evidence thickening

*Prompt- and context-engineer promptforge/briefer.md for thick, clean evidence.md on local Qwen: cut Report until evidence is thick, beat the current Qwen baseline using Opus structure plus subagent web research, log every experiment in gitignored research.md, then Boost and Bloomberg with a 3-round no-improvement stop per subject.*

Statements of principle:

- Anti-hallucination: fetch-only claims; require entity-name check before disaster/vulnerability claims; UNKNOWN over invention. Wrong-entity / hallucination is a hard fail.
- Rollback any change that lowers score or adds hard fails; cosmetic-only diffs do not count as improvement.
- [rest is experiment-loop bookkeeping and scoring rubric]

### Supervise local llama-server

*Fix the zombie-gateway failure mode: when llama-server exits after readiness, the next chat request respawns it on the same port and identity instead of returning a permanent 502. Crash prevention stays operator config, not this change.*

Statements of principle:

- Lazy ensure-alive on send, not a background watchdog. Respawn once with the same port, alias, and api-key, then retry the request once.
- Crash prevention (FA/parallel) stays operator config, not this change.

### Try Qwen 27B

*Add a local gateway profile for unsloth Qwen3.5-27B Q4_K_M, restart the gateway on it, smoke, then run briefer on one known subject to compare evidence quality against the 9B baseline.* [operational only]

### Store real plus virtual

*Replace the memory-only / write-through-mirror store model with a layered OverlayStore so Lua can read real confined files and virtual run files through the same store API at once, without turning the CLI into a surprise disk writer.*

Statements of principle:

- Keep one Lua surface (`store.read` / `write` / `inject` / `glob`); implement a layered backend: mutable memory on top, tombstones, confined read-mostly filesystem below.
- Confinement is hard: all fs access goes through a root plus safe-relative-path rules; reject `..`, absolute, Windows-reserved. Fail closed.
- CLI/MCP default unchanged: memory-only, no unsolicited disk I/O. Making CLI mount `$PWD` by default is rejected (surprise reads/writes, path escape risk).
- Do not seed the entire tree into memory at start; overlay reads are lazy.
- `store.inject` still wraps whatever `read` returns; real file bytes are untrusted when injected into model context. No silent trusted FS injection.
- Tombstone-only deletes for mounted files; a prompt cannot destroy author inputs by calling `store.delete` unless a future opt-in flag says so. Silent dual competing authorities without tombstones are rejected because delete would not stick.
- A separate `fs.*` Lua table as the only solution is rejected: it forces every prompt to know two worlds.

### PromptForge user guide

*Write a progressive tutorial for PromptForge prompt authoring, starting from Hello World and building to a full-featured pipeline prompt, followed by a Lua API reference. Each section adds one capability with a working example.*

Statements of principle:

- Each section adds exactly one new concept with a working example. No forward references: each section uses only concepts introduced in prior sections.
- Voice: direct, technical, no filler. Show the code first, explain after. Every example is a complete runnable prompt.
- [section list and writing mechanics omitted]

### README and CI overhaul

*Replace the current 798-line README with a crisp, marketing-quality front page (badges, sizzle, code snippets, build instructions). Move technical internals to DEVELOPMENT.md (verified not stale). Add GitHub Actions CI workflow and BSL-1.0 LICENSE file.*

Statements of principle:

- New README: crisp, inverted-pyramid, badges + sizzle + image + quick examples + install/build/run + links. Target under 200 lines. Dense, scannable, no glop.
- Each migrated DEVELOPMENT.md section is checked against current code for staleness before inclusion.
- License: Boost Software License 1.0.

## Design Documents Written

[pasted: two revisions of briefer.md (evidence-only recon port; the second folds query hints into prose and trims Topics to heading-only list)]

[pasted: new README.md, badges-first structure with banner strips]

[pasted: user-guide.md, 21-section progressive tutorial plus API reference. Author-visible semantics it records: sections execute in file order with fresh VM and fresh conversation per section; `reply` and the store are the only bridges; substitution applies only to prose, never Lua source; tool/model scope closes on the first prose; non-final prose is single-shot, final prose runs the full tool loop; scalar return from any section Lua ends the run; `sys` table is sealed; `store.inject` wraps content in an untrusted nonce-framed envelope; fanout arms run concurrently and share the store; `execute` caps recursion at 8 and rejects `jump` inside it. Note: p448-p450 above dispute this document's claim that the preamble is "replayed" per section VM.]
