# Promptforge-core session, largest (reduced)

*2026-08-14 16:13 - transcript b8440861-d85a-4986-b36c-db83d1478b25*

*Prompts p376-p511 of 511. Part 5 of 5.*

## Prompts

**[p376]** hmm I see what you mean. Yes this is a big change. previously we could assume the vm was fixed after the preamble ran. but now, it can change after each completion

**[p377]** One thing I know for certain. If we are going to work on building an analytical pipeline, it is absolutely essential for development and debugging, to be able to re-run the prompt from any step. So we need those intermediate outputs as files which can be read in.

**[p379]** okay but what about when we want a coding agent to have access to everything

**[p380]** So for the, for the tools changing, like for first exposing search and then exposing fetch, let's just put that off to the side. Let's, let's just put that in the not to be implemented part of the plan. And then for the overlay, so I guess this is a core feature, this isn't a tool in the sense that, like, you load it separately, like this tool has to be integrated into the core because you have the mount. I mean, this isn't like a normal thing, right? I mean, it affects the Lua.

**[p381]** Yes I think so we need files. And what about ls, grep?

**[p382]** no to list and grep. we are just exploring not planning that.

**[p383]** Right now, we're registering the search as a web search, right? Because we're asking for the need, we're saying we need to be able to search the web. In the prologue. And that And when we expose the tool to the model, we're giving it the same description. But I don't know that we should be doing that, because why does the model care that it's the web? The model just cares that it's searching. Like for example, what if we connect it to a workspace search tool? Or what if we connect it to an MCP search? Or what if we connect it to a rag index? Like when the model only the, the language that the model's using only cares that it's doing some type of searching and that it has to fill in the information in the tool. So I'm thinking we need to be able to rebind the tool in the preamble or even In the H2 or H3, what, like, when you when you inject a tool, we should be able to re to rewrite the description so that we could fit it to what the model expects. This way, the prompt can be written agnostic. Like, the prompt shouldn't say "search the web," the prompt should just say "search."

**[p384]** yes exactly. do models prefer tools.add("search") or tools.add("WebSearch")? Is there a training bias?

**[p385]** What about SearchInfo, FetchInfo, ReadFile, WriteFile, AppendFile ?

**[p386]** we are already rebinding the name in the preamble. the tool.need call establishes the name, and the prompt owns it

**[p388]** so then briefer.md should read
tools.add("search_info")
because snake_case beats single word?

**[p389]** what if I want to build a composite search tool that searches the web and mcp?

**[p390]** Okay, but option B, the Lua as tool, this is simpler than what we had before, 'cause before we were talking about reopening the closed toolset, but this isn't that, this is just a function, the toolset remains closed after the preamble, and. It's, it's easier. Or is it? How do we deal with it?

**[p391]** Okay, but now here's the problem. So we do the search, we search web, we search MCP, but how do we do the fetch? If we get an MCP result, then how do we then tell it to fetch it? Do we have to have like a combined fetch too?

**[p392]** I don't know. This is, so I have one MCP server and it has multiple sources, like it's got the Boost mailing list, it's got the WG21 mailing list, and so this creates a problem because I want the briefer to be generic, but I wanna be able to say, you know, I wanna be able to tell it, okay, use MCP or not, because if my report is destined for the public, I'm not allowed to quote the reflector. So we're actually seeing, we're actually seeing a downside of the pipeline, which is the pipeline is, you're not, the pipeline is rigid. Right? Like when we have Cursor or Claude Code as the orchestrator, it can shape the prompt, right? Like it can reinterpret the instructions to suit them to whatever you ask for. But we can't do that here. We can't shape anything here because we're doing the tools are, are based on, they're in Lua, and the orchestrator, the prompt, the LLM, it can't touch the Lua So we would have to like have a configuration file ahead of time that says that when you run the briefer, now you're allowed to consider these sources.

**[p393]** First of all, the preamble. Okay, the preamble is the H1 code. The prologue and the epilogue are for the sections, is that correct? The plan should enforce that terminology throughout the entire repo. I want every file checked.

**[p395]** its 180 occurrences not 180 files. there's no one to break, this is unshipped. the preamble is meaningfully different from the prologue

**[p396]** I want this to be the first step of the store plan

**[p397]** Question I'm thinking that the, that the preamble has to have inference. Because how are we gonna process the args? Like we need inference, we the model needs to be able to take control and do some tool calls. Like the model needs to be able to parse that string and figure shit out. Right? But then we need the tools to be open. Because if the model, if the model realizes, "Well, we need MCP, but now we have dynamic tool sets, how's that gonna work? "

**[p398]** I think we need first class objects in the Lua. "Tool" needs to be an object type and if you write tools["search"] it gives you the object and it has properties you can inspect and invoke. in other words its a Lua table. And Model needs to be a thing. so you can ask for a model and call infer() or turn() or whatever on it. And the preamble should be able to declare global variables. For example a list of tools. and then in any section you can write

**[p399]** tools.need( search_tools )

**[p400]** and this will work because search_tools is an array of Tool

**[p401]** You're saying full agent programming language, but all we're doing is adding one function. So if you're saying that one function turns it into a full agent programming language, then f-f-what, there's nothing this isn't a future architecture to capture. This is just a natural falling out of making these things first-class objects, and I would argue that they should have been first-class objects in the first place, because that's just good programming hygiene. You always encapsulate, you always model, because this gives us a unit test. We can, we can model, we can have an abstraction that represents a model, an abstraction that represents a tool, and we can put in the mock, and we can test it. And we can have different tool types. I mean, this is just normal. This is a This refactoring should actually help the code become more simple, if anything. And also, let me show you the other problem that it solves. Look at what we can do:

[p402-p406] Example: `tools.add("search")`, then `model.infer("search for {{args}}")` with only one tool available, then `tools.add("fetch")` and fall through to prose "Fetch information about {{args}}".

**[p407]** lets defer overlay store and make the terminology rename and the first-class-objects the sole work

**[p408]** [subagent search directive] Also, what else should we turn into an object? So we have tool, we have model, what else is there?

**[p409]** Wait a minute, hold on. If you seal up on infer, then we can't adjust, we can't add the tool in the preamble. We can't add the, or the prologue, like we can't add search and then infer and then add fact. That pattern breaks.

**[p412]** it sounds to me like the only point to the phase transition is to protect the epilog

**[p413]** so then the prose in the markdown is just an internal call to model:infer() ?

**[p418]** 1. what happens to this syntax: tools.calls["search"]
2. why even have an epilog why not just allow any number of alternating lua/prose?

**[p420]** so the context just grows in a section?

**[p421]** Something about this isn't right, because we go to the epilogue only when the turn ends without a tool call. So if we do a fetch, then the turn isn't ending, so that means it has to go back. It's gonna stay in that prose.

**[p422]** But then the code that you just showed me doesn't work. This code doesn't work.

**[p423]** tools.add("search")
Search for {{ args }}

**[p424]** tools.add("fetch")
Now fetch the top result from the search.

**[p425]** store.write("result.md", reply)
return reply

**[p426]** Lua needs a way To say That We only advance, we advance on a tool call. Maybe.

**[p427]** One thing that I don't like about infer Is calling model infer. It's not you're putting prose in the code. Prose in the code is ugly. I want prose to be in the markdown section where it can be nicely formatted, where you can have bold, you can have italics, you can have bullets, you can have paragraphs, you can have block quotes, you can have URLs. It's beautiful.

**[p429]** But then, how do you do How do you do the model doing its own how do you make it so that the model can decide when it wants to stop? I guess maybe so that, so that, okay, the last pros section is the loop. That's the only thing that can be a loop, right? So the last probe section has the special property that if there's no tool call, that's the final reply. And if you don't like it, then open another H2. Right? Like if you gonna wanna go back to the singles. So any, any, any prose that's not last is a single shot, it always falls through. The last prose only goes to the epilogue if the reply has no tool call.

**[p430]** So if we're doing this, then if we want, if we really want two loops in one section, we can have the Lua, we can have a function. Instead of infer, we can have execute, and it can mention two different h twos. So the Lua can invoke an H2 itself, so that's like a subroutine. That's powerful, and that's not much more work. We already, we already have that code. We already have to execute sections, so why not give it, make it a function that Lua can call? Hello!

**[p431]** Right, exactly, but wait, we didn't collapse the pipeline. The default is to run the sections in order. And we still have the context clearing go-to, didn't we? We implemented the go-to, correct? Any Lua can call goto and transfer control to another section, and it's a context clearing goto.

**[p432]** yes add execute and add goto and I want the design docs cleaned up. our conversation is preeminent.

**[p433]** local step = tasks["## Research"]
execute(step) -- equivalent to execute("## Research")
goto(step) -- equivalent to goto("## Research")

[p437-p441] User asked for the work in a separate git worktree from the master tip commit, explicitly not a cloud agent (repeated twice).

**[p442]** ugh... _G? fuck that! how about jump("## Report") ?

**[p445]** are you still doing replay for the preamble?

**[p446]** I thought we talked about this. We said that we can't replay, because if we replay, what if there's inference? This wasn't in the plan, and what happened?

**[p448]** Question Does Lua have a way of duplicating? Virtual machine. Like just make a complete duplicate of a context.

**[p450]** Thinking, I wanna have like a general purpose. Method. I wanna basically Given a VM Serialize the state, but it should be generic, 'cause we have the globals. I mean, it's really just the globals. And then? Maybe we need the chunk? But we could serialize bytecode. And then bring it back in a new VM. I mean, and then every time we need a new VM, we just clone the preamble. Why wouldn't that work? Like, I don't wanna write code that's, because here's the problem, then every time I add something, now we have to modify the serialization. But if we could do generic serialization and duplication of a virtual machine, then we never have to worry about it, like it'll never break, and we don't have to worry.

**[p451]** I'm gonna push back on that. Apparently, what, so what you're saying is. The Rust user data And see closures. But we can index those, like we could create a table out-s-that sits outside of the VM, and we give an unique ID to each Rust user data and each C closure, and that ID tells us how to clone it. And so any piece of code that installs a rust user data in Lua also has to give instructions for duplicating itself. There's What do you think about that?

**[p453]** Oh, this doesn't sit well with me. I don't think this is a good thing to do. I think This isn't right. I think we have to have a replay. Or else how can we get functions? Like we need to have shared, not having shared functions is a disaster. We have to have shared functions. So. I'm not sure how we do that, but there has to be a way. Maybe we can have a Lua section. Beyond the, after a divider? I don't know. In the H1, what do we do? How do we make this happen? So So H1 can have inference, right? So H1 can alternate just like the H2s. You can have, you have Lua inference, Lua inference, Lua inference, and the last inference terminates on when there's a lack of a tool call, and then we have a possibility of one more Lua block. So it's just like the others. The difference is in the type of environment that we have, but there has to be a way where we can specify, okay, here's a chunk that you play back.

[p454-p456] Question: should a bare untagged code fence be allowed in addition to a ```lua fence?

**[p457]** What is our current solution to sharing library functions?

**[p459]** is there a way to copy the functions?

**[p460]** but we have the problem of side effects. if the preamble calls an expensive function like infer() then we have a problem. and we also later will want to allow a prompt to import lua libraries. this is how authors augment their prompt with code. for example calling into a C library. For example git

**[p461]** yeah this solves it. "```lua shared" is the only solution. does "lua shared" inherit the environment of the previous lua chunks in the preamble?

**[p462]** yes.. question: so "lua shared" doesn't actually execute during the preamble, it is only parsed into bytecode?

**[p463]** there's no "today's prompts"

**[p464]** I'm not sure what "runs at bind" means. Also, won't shared functions want to touch sys, var, et. al. "?

[p466-p467] [pasted: assistant explanation of the two-phase lifecycle, "Bind" (resolve tools.need against the live registry by executing H1 in a special VM) vs "Execute" (sections fire, models infer, store written)]

[p468-p469] User asked for a walkthrough of a concrete example prompt: H1 with tools.need("search", ...) and log("test"), prose "Say hello, world", trailing lua store.write("hello.md", reply).

**[p470]** I don't think this works. The two-phase treatment of the preamble is a brittle hack. I think we should instead just bite the bullet and run the H1 lua chunks fully. Capture their state changes (for example, tool binds). Serialize specific globals like var. anything done to `store` will of course be preserved since `store` lives across all lua chunks. do you understand? analyze the consequences of this.

**[p471]** hell yes :) and when you apply this model I want you to go through every. fucking. line. of. code. and make sure there is no trace of the old way, and the new way is applied in the simplest fashion. In fact before you go at it , I want the plan to reflect the imlpementation strategy in broad stores: a subsection per-file inside the plan with a few bullets explaining the broad strokes.

**[p473]** Prompt.replay is a good name, it tells you how it works so there is no confusion.

**[p474]** what if there's more than one `lua shared`? I say error. and no "lua shared" after h1 ends

**[p478]** each commit that changes the prompting language should also edit the @promptforge/user-guide.md . Add sections to it if you must. Or delete them. Make sure that everything in the user guide is correct for each commit. Also, this is very good, put it in the user-guide in the commit which adds the feature:

**[p479]** A section is a sequence of blocks:

**[p480]** [lua] [prose] [lua] [prose] ... [lua]

**[p481]** I like these rules too but note that we renamed it to jump() because goto() is reserved. The plan should sweep the entire repo for the word "goto" and fix it. Do that as the very first step (and run the tests and commit that change).

**[p482]** And I like these rules, the user-guide should have a "quick reference" at the end (before the big robot image) with a compact set of rules for how the prompting language works:

**[p483]** Rules:

**[p484]** Non-final prose blocks: single-shot. One model round (may include tool calls for that round). Control moves to the next lua block after the model responds. Conversation accumulates.

**[p485]** Final prose block: full tool loop. Model keeps calling tools until it produces text. That text becomes reply. Same as today.

**[p486]** Lua blocks: run sequentially. Can mutate tool scope (tools.add), write to store, inspect reply, call execute() or goto(), call model:infer() explicitly.

**[p487]** One conversation per section. Context grows across all blocks within the section. Cleared between sections.

**[p488]** Sections are subroutines. execute("## Name", input?) runs a section in a fresh VM, full tool loop, returns its reply. Like fanout but sequential and single.

**[p489]** goto("## Name") transfers control. Context clears. The current section stops. The named section runs next. No return to caller.

[p490-p491] Branch correction: user stopped everything because the agent was on the wrong branch; work belongs on master, cherry-pick the two new commits and continue there.

[p492-p495] Environment troubleshooting: an "inherited gateway credentials" bug; user directed a one-commit fix with tests, one review round, amend, and folding in an unrelated report.

**[p500]** Search the PromptForge repository. We got a lot of little loose files to do and design and architecture and all that shit. Find all those little loose files, determine what's inside of them, see if it's out of date, find out if we really need it. I wanna trim all that shit 'cause it's just creating a lot of noise.

**[p501]** do 1 and do we need this STATUS and DEVELOPMENT shit?

**[p504]** Okay, here's what we need. I wanna have. A store Object, which saves everything in files, and this is for like debugging, so after we do a run, we can inspect. The files, and also when we run again. The prompt can check to see if the files already exist, and then it can skip the step.

**[p505]** Yes, it's the same as the MEM store, it's just persistent. And I wanna be clear about something, this isn't a general-purpose file system, this is strictly for debugging. When we go to do the file system, when we want to do the string replacement, and we want to apply deltas, and we want to do some agentic coding, that's gonna be a different class entirely. The store is for-is a virtual file system for analytical pipeline that needs to have file-shaped intermediate values.

**[p506]** I would say the caller has to provide. The path, and there's no default, the caller has to do it. We don't wanna have def we don't wanna start having defaults because then we're spreading behavior around. The, the prompt engine shouldn't have any behaviors that it chooses on its own. It has to be told what to do every single time. The whole system is designed to make things explicit. The moment we start using defaults, now the defaults can change, yada, yada, yada.

**[p507]** no design doc

**[p508]** @promptforge/crates/promptforge-dev needs an option to create a dir in the same place as the tool with the same name as the tool minus exteions

[p510-p511] Environment troubleshooting: a scratch path kept leaking into a promptforge path; user flagged it twice.

## Plans

### section-lua-lifecycle

*Refactor sections into shared compiled Lua, preamble, prose, and epilog phases with isolated per-section VMs; add an authoritative `design-core.md` (complete current design, not a patch note) while retaining `design-core-orig.md` as history.*

Settled design: one optional `lua prompt` library before the first H2 (duplicates or late ones rejected so misplaced code cannot silently become prose); each section has optional leading-lua preamble, middle prose, optional trailing-lua epilog, other fences stay prose; all Lua compiled at parse so a successful `Prompt` is fully syntax-validated; shared source compiled once but executed independently per section VM (helpers written once, isolated closures/globals per branch); one VM per whole section; scalar return from preamble or epilog ends the run, nil falls through; the store remains the only intentional mutable channel across sections - functions, closures, globals, `var`, tools, `reply` are branch-local by construction; mutable run-global Lua is explicitly excluded.

### prompt-fixtures-logging

*Add correlated observer traces and constrained Lua logging, remove unused author prompt versions, and establish file-based prompt fixtures complementing inline unit tests.*

Principles: one execution ID threaded unchanged through parse/bind/run (an execution ID, never a thread ID, since async tasks move between OS threads); observers own their own synchronization and `log()` holds no lock across an await; `print` hardened out, `log(message)` constrained to one single-line UTF-8 string of at most 256 chars; Lua log text is the single explicit author-controlled exception to the observer's payload-free detail rule (no args, replies, tool results, credentials, paths, or store contents); the unused author YAML `version:` field is removed while `promptforge:` engine-version gating stays; inline tests stay authoritative for narrow edge cases while file fixtures cover complete author-shaped stories.

### promptforge-dev-loop

*Add a dev-run subcommand (plus watch mode) to promptforge-core-tests against a locally cached Qwen3.5 9B on GPU llama-server, with verbose trace output.*

Principles: the fixed scenarios keep the small model and stay byte-for-byte deterministic; dev keeps result on stdout and all trace on stderr; ordinary `cargo test` stays fully offline; hand-rolled argv, no clap, matching workspace convention.

### models debug cluster

*DebugCapture seam for raw payloads, payload-free observer details for empty/truncated turns, then prompt-level model bindings (`models.need` / `models.use`) with gateway catalog metadata and per-call temperature/thinking.*

Decisions: a separate opt-in `DebugCapture` on `RunOptions` - the Observer stays payload-free; `models.need(alias, description, opts?)` in H1, `models.use(alias)` in H2; `context`/`thinking` filter the catalog while `temperature`/`max_tokens` ride per request; identity is alias-to-binding (ModelId + invocation), not to weights, so same weights with different params is legal; no `models.use` means host default model (existing prompts unbroken); the gateway serves catalog metadata via `GET /v1/models` and stays request-passthrough - rejected: hosts inventing model metadata out of band.

### completion normalize layer

*A slender CompletionNormalizer module in core (drop-in trait) making empty final content a hard error, keeping wire quirks out of execute and hosts.*

Rationale and locked policy: one door for wire quirks (field synonyms, empty content, null-content tool calls) so hosts stay dumb; hard-failing empty content breaks prompts that today "succeed" with an empty reply (briefer's silent empty evidence.md) - that breakage is the point; not adopting `genai`/`rig`/an external crate now - the module is the seam; never promote `reasoning_content` into the answer; a final turn with no tool calls and empty content is an error even when reasoning is present; tool calls with empty content remain valid.

### webfetch soft errors

*Recoverable web_fetch target failures return Ok tool text the model can read (industry soft-error practice); SSRF and URL-admission failures keep aborting.*

Policy: HTTP 4xx/5xx, unsupported/missing content type, timeout, too-large, undecodable charset, DNS failure are soft `Ok(model_facing_text)`; invalid URL, blocked scheme/port/userinfo/IP, redirect refused stay hard `Err`. The HTTP error body never enters the tool result (untrusted, not useful); the message names status + final URL + a next-move hint. The execute loop contract is unchanged - webfetch simply stops returning `Err` for the recoverable class.

### extract promptforge-dev crate

*Extract the interactive prompt runner into a `promptforge-dev` crate that talks to an already-running gateway; keep the 0.6B scenario suite self-contained in core-tests.*

Locked decisions: dev never starts infrastructure (requires a running gateway, hard-fails friendly otherwise); the scenario suite keeps its sidecar temporary gateway so inference tests stay self-contained; server knobs leave the CLI and live only in the operator's `gateway.toml`; the model catalog is fetched from the live gateway, not pinned, so prompts track the deployment; dump-before-run so stale traces never masquerade as current; observer/debug stay out of the result stream.

### local.toml bigger model

*Create an operator gateway profile for the pinned Qwen3.5-9B so promptforge-dev binds it instead of Anthropic Sonnet.* (Operator config only.)

### gateway download progress

*Indicatif progress bar for large GGUF downloads on a TTY; periodic tracing logs when not a TTY.*

### Tool dialect plugins

*Replace ad-hoc ContentFence hacks and prompt-side tool_code instructions with a catalog-selected ToolDialect plugin registry so prompts stay dialect-agnostic.*

Principles: the dialect is set by operator config on the gateway model entry (the vLLM `--tool-call-parser` role), advertised on `GET /v1/models`, frozen onto the bound model - rejected: sniffing completion text, hardcoding model names in author prompts; author prompts say "use search/fetch" with no format recipes - the dialect injects a synthetic harness prefix built from live tool schemas, which is harness text, not author Markdown; unknown dialect id is a hard error, no silent fallback; default is `openai`; wire quirks live in the normalize/dialect family, not in execute or hosts.

### Commit local WIP

*Commit six uncommitted files as two focused commits, leaving the tree clean.* (Process plan; no design content.)

### Write-through store traces

*promptforge-dev writes `.trace/` turn JSON and store files as events happen instead of buffering until run end. Dev-crate only.* Principle: clear the dump dir once at start, mirror every mutation immediately, end-of-run reconciles without wiping `.trace/`.

### Fanout and gateway concurrency

*Wire llama `--parallel` to gateway lane concurrency and run fanout arms concurrently in core.*

Principles: one knob - lane concurrency is both the gateway admit limit and llama `--parallel`; core fires all arms at once, the gateway queue is the throttle; replies stay ordered by arm index; fail-fast aborts siblings and propagates the first error, same invoker-visible behavior as sequential; the store stays shared and mutex-safe - authors must not assume arm N sees arm N-1 writes; nested fanout remains a non-goal.

### Briefer evidence thickening

*Prompt/context-engineer briefer.md for thick clean evidence on local Qwen; cut Report until evidence is thick; log every experiment; 3-round no-improvement stop per subject.*

Principles: write only from fetched page bodies (search hits are leads, not facts); UNKNOWN over invention; entity check before vulnerability claims; roll back any change that lowers score or adds hard fails - cosmetic diffs do not count as improvement.

### Supervise local llama-server

*When llama-server dies after readiness, the next chat request respawns it on the same port and identity instead of a permanent 502.*

Decisions: lazy ensure-alive on send, not a background watchdog; respawn once with the same port/alias/api-key, retry the request once; cooldown caps respawn storms. Out of scope: crash prevention (operator config), changing `/health` semantics.

### Try Qwen 27B

*Add a Qwen3.5-27B gateway profile, smoke it, run briefer once to compare evidence against the 9B baseline.* (Operator task.)

### Store real plus virtual

*A layered OverlayStore lets Lua read real confined files and virtual run files through the same store API, without turning the CLI into a surprise disk writer.*

Principles: one Lua surface (`store.read/write/inject/glob`); read path is tombstone -> mem -> confined fs; writes land in mem (copy-on-write from disk); delete tombstones base files so reads do not resurrect them; glob is union minus tombstones; confinement is hard and fails closed; CLI/MCP default unchanged (memory-only, no mount); no seeding the whole tree into memory - overlay reads are lazy; `store.inject` still wraps reads - real file bytes are untrusted in model context, no silent trusted FS injection. Rejected: a separate `fs.*` table as the only solution (forces prompts to know two worlds); CLI mounting `$PWD` by default; dual authorities without tombstones (delete would not stick). Tombstone-only deletes by default - a prompt cannot destroy author inputs via `store.delete`.

### H1 once no replay

*Postmortem: preamble-infer vs replay was discussed but never made a plan step, so per-section H1 replay stayed. Fix: run H1 exactly once as a live preamble; stop shared-bytecode re-execution in section VMs.*

Rationale: the failure was process - the insight was real in conversation but never written as a plan todo, so execution followed the plan literally. Replay only made sense when H1 was pure declarations; with infer or store writes it multiplies cost and corrupts state. Decisions: bind stays declaration-only (`model:infer` hard-errors there); the live preamble runs once at execute start with host injection and the infer hook; section VMs install frozen bindings only; H1-defined functions are no longer available in section VMs.

### File-backed store

*A FileStore backend persists the virtual store as flat files in a caller-provided directory, enabling post-run inspection and cross-run resume via store.exists.*

Principles: the caller provides the path explicitly - no defaults, no derivation; the engine remains a pure executor; no new `StoreRef` constructor or convenience method - the caller does the plumbing; `execute::run` does not know or care whether the backend is memory or files - the `Store` trait contract is unchanged; resume logic (`store.exists` then skip) is prompt-author Lua code, not engine behavior; each caller sets its own policy (dev uses `<stem>.store/`, CLI gets an opt-in `--store <dir>`, MCP stays memory-only). The plan's embedded design-doc contract: every design element states what is observed, how it is structured, and why; include an element only if changing it would change anything the user sees or names, the shape of the system, or something costly to reverse; a name is a design decision; implementation detail is left out.

## Design Documents Written

[pasted: two successive versions of `promptforge/briefer.md`, the evidence-only recon prompt (~100 lines each): H1 `models.always("writer", ...)` + `tools.need("search"/"fetch")`, Main fans out `### Web Search` over `### Topics` and concatenates into `store.write("evidence.md", ...)`; Web Search arm enforces a hard 3-turn budget (search once, fetch 2-3 URLs, then write), fetch-backed verbatim quotes with URLs, UNKNOWN over invention, hard entity check, plain-markdown output with no fence wrappers, and a Lua epilog asserting search/fetch were called and stripping accidental fence wrappers]

StrReplace-edited design docs (path only): design-core.md (both worktrees), README.md, briefer.md, AGENTS.md, STATUS.md, promptforge-dev README.md and design.md, design-gateway.md.
