# Design Principles and Teachable Items from the 2026-09-11 PromptForge Huddle

Report type: Informational, organized by topic. Every item below is sourced to a timestamp in the auto-generated huddle transcript (Kaleka, Parsons, Falco, 6:20 AM to 8:03 AM Pacific). Auto-generated transcripts contain transcription errors; quotes and attributions should be re-verified against the recording before external use.

## Executive summary

The huddle's design content clusters into five positions. First, the harness is as important as the model: tool errors must explain their own fix, tool output must be bounded, and environment context must be injected. Second, tool discipline: offer few tools, opt-in only, never remove them mid-context, and prefer many small accumulating tool calls over one large structured output. Third, the virtual file system is the sandbox and the presentation layer at once, with a description field on every file. Fourth, orchestration cannot be trusted to the model: XML contract tags keep subagent prompts verbatim, and WG21 work requires determinism because a single mistake is disqualifying. Fifth, process: never let a model review its own work, audit before fixing, make the model pre-commit its approach in ask mode, and capture everything (transcripts, Slack) into the repo. The teachable items are a complete introductory curriculum on how LLM harnesses work, from message stacks and tool calls through RAG enrichment, virtual file systems, and subagent orchestration.

## Design principles

### The harness is as important as the model

**Tool errors must explain the fix.** When a tool fails, explain why in clear terms that require little context, and say what to do instead. A bad harness returns "error code 3"; a good harness teaches the model how to recover, and long-horizon success rates rise accordingly [16:47-18:00].

**Benchmark scores reflect the harness equally with the model.** "The harness is as equally as important to the benchmarks as the model itself" [17:30].

**Bound every tool's output.** A naive `ls` that dumps 10,000 files floods the context. Ship a synthetic version that truncates, says so at the bottom, and gives the model a paginator or a way to grep for specific files [18:00-19:13].

**Inject environment context.** A good harness puts what files are open, what is in the terminal, and what is selected into the system prompt and user messages [19:18-19:59].

**Resource limits must talk.** When a limit truncates output, emit useful text telling the model how to get more (Bashkit's "parser fuel" is the cited example) [1:16:40].

**The user must be able to see everything the agent does.** Stated as a UI invariant; Cursor's tool-result pop-up is one acceptable form, an unroll caret another [41:27-42:01].

### Tool discipline

**Offer few tools, and make every tool opt-in.** Frontier models handle roughly 30 to 50 tools, tiny models 5 to 9; no model handles 1,000. The fewer offered, the better the chance the right one is picked. PromptForge's principle is tight author control: opt in to every tool rather than offering everything [25:32-26:29].

**Prefer many small accumulating tool calls over one large structured output.** Asking the model to build one big JSON object raises the chance of a syntax slip as the object grows, and structured-output support can tax the model up to 30% performance. Small per-item calls that accumulate into a table avoid both [26:29-27:43].

**Tool sets are added early and never removed within a context.** Models build priors from their own history; a tool that worked five times and then vanishes produces confusion and errors [28:17-29:16].

**Reset context at section boundaries.** In PromptForge, transferring control to a new section starts a fresh VM with all messages cleared; tools and system prompts must be re-declared per section [30:41-31:33].

**The system prompt is secret and supreme.** Models are trained never to reveal it, its instructions take priority over everything else, and it survives compaction, which is why plan mode cannot be jailbroken [31:59-32:39].

### The virtual file system is the sandbox

**Serve the model a virtual file system, not the real one.** An overlay maps chosen path prefixes to handlers; content can be synthesized from embedded strings or a database, nothing lands on disk, and the user cannot delete or corrupt it [1:06:41-1:13:56].

**Attach a description field to every file.** Beyond name, size, and dates, each virtual file carries a description, so a directory listing alone tells the model what things are ("front matter for free") [1:08:44-1:10:06].

**Sandbox by construction.** Root the model's universe at a chosen directory (chroot-style) or a fully synthetic tree; the tools simply do not allow escape [1:20:24-1:21:32].

**Keep the sandbox stable within a run.** If something was available on one model turn and gone later, the model pattern-matches on the earlier success and gets confused. Additions are safer than removals [1:21:32-1:21:58].

**Permissioning is a usability trade-off.** Pure opt-in grants are safest, but users hit "allow all" quickly. Stated practice: trust frontier models with broad permission, restrict smaller models whose language grasp is less nuanced [1:22:28-1:24:17].

**Use a sandbox shell so the harness always has bash.** Bashkit gives the harness a consistent shell regardless of host OS, sidestepping PowerShell syntax friction on Windows [1:06:12].

### Orchestration requires determinism

**Use XML contract tags for subagent dispatch.** The orchestrator's context stays clean: the subagent is told to grep for a tag pattern and execute the contents between the tags verbatim. This solves two failure modes at once: the orchestrator paraphrasing a detailed subagent prompt down to "do a code review" under context pressure, and the orchestrator reading the embedded instructions so often it absorbs the subagent role and does the work itself [1:34:07-1:38:14].

**Do not trust the model to orchestrate when mistakes are disqualifying.** WG21 critique work cannot afford a single error, because one mistake becomes the excuse to dismiss the whole body of AI-assisted work. Determinism, not model judgment, is the answer, and this is stated as the core reason PromptForge exists [1:38:14-1:39:14].

**Distribute harnesses as markdown, not compiled executables.** A competing project's custom harnesses require writing and compiling Rust and shipping an executable; PromptForge ships a markdown file [1:28:56-1:29:19].

**Own your harness.** A vendor's harness serves the vendor's owner; the stated risk is Cursor under new ownership optimizing for someone else's priorities, which motivates a programmable harness that works the way the team works [8:04-8:35].

### Process principles for AI-assisted work

**Never let a model review its own work.** The model asked to find flaws in code it just wrote, in the same context, fresh off justifying every choice, "will look at its own work and find it good every time." Skills built on same-context self-review are "taste wearing a procedure's clothes" [5:07-6:08].

**Write real design documents, not AI-generated ones.** AI-dumped design docs are "folding slop into slop" [4:29-4:50].

**Audit before fixing, then tier the findings.** The rust-rulebook catch-up ran a 150-commit audit (78 deviations, 43 compliant), then sorted fixes into tiers: fix now, fix opportunistically, do not fix, defer [44:23-45:24].

**Capture deferred work explicitly in the plan.** Anything not fixed gets a deferred-work-stream item so it survives the plan's commit into the repo [45:44-46:04].

**Make the model pre-commit its approach in ask mode, then audit the statement.** Flip to ask mode, require the model to explain what it is about to do section by section, review that, then let it execute [50:26-50:44].

**Inline the minimal rulebook material into plans.** Do not bind the plan to the rulebook by reference; inline the smallest amount of material that ensures conformance when the plan runs [1:42:44-1:43:55].

**Keep plans to a few consolidated work streams.** Target roughly 5 to 7 steps with a light verification cadence rather than 30 to 40 steps with full verification at each [1:32:46-1:33:19].

**Hand-authored context files beat rediscovery.** Load a human-written rulebook explaining how PromptForge works so the model does not have to discover it from scratch every session [34:09-34:31, 43:09-43:30].

**Capture everything into the repo.** Every huddle transcript goes into the design repo under a fixed naming format, and PromptForge-related Slack conversations (public and private) get scooped into a parallel directory, building institutional memory [3:13-4:29].

**Separate execution from presentation with an observer.** The observer sees every event during a run: it drives token streaming in the UI, records the full run log, and will underpin the future debugger as a custom observer over the event stream [1:00:12-1:01:55].

## Teachable items

These are the concepts taught or explained during the huddle, in the order a newcomer would need them.

### How a harness works

1. **The model does exactly one thing.** It takes a stack of messages (system, user, assistant) and returns a reply. Assistant messages have internal structure: thinking blocks, tool calls, and tool results, which IDEs consolidate for display [9:21-11:35].
2. **Context grows every turn and compaction is the overflow valve.** Each submission resends everything that came before plus the new message; when the harness gets a context-overflow error, compaction happens [11:35-12:29].
3. **A tool call is a request, not an action.** The model emits a marked block of JSON asking the harness to do something, then inference stops. The harness executes it, packages the result as a tool-result message, and resubmits; only then does the model continue [12:29-14:26].
4. **Tools exist only if offered, and tool definitions are just words.** Each tool is a JSON description (name, parameters, prose); the model reads the description and figures out the call from training. "It's just words, dude" [14:26-15:16, 20:11-21:43].
5. **Models know paths, grep, and replace first.** Any tool-capable model is trained on file paths and editing operations early [21:43-21:59].
6. **Cursor's status strings come from a tiny side model.** A roughly 1-billion-parameter model looks at each tool call and generates the human-readable "what it's doing" string; they are not hard-coded [15:30-16:25].
7. **PowerShell is a recurring error source on Windows.** Different syntax causes tool-call failures; models recover well when the error message is clear [16:25-17:10].
8. **A model turn is one submission.** The message list grows with every turn [28:17-28:36].
9. **System prompt versus user and assistant messages.** The system prompt is secret, takes priority over all other instructions, and persists through compaction [31:33-32:49].
10. **Message lists are built explicitly in PromptForge.** `messages.new()` plus role-tagged appends (system, user, assistant, tool) mirror the OpenAI wire format's `role` field [34:48-37:32].

### How Cursor specifically works (reverse-engineered)

11. **Cursor enriches prompts server-side.** Prompts go to Cursor's server, which consults a RAG index over the workspace, adds file pointers and context, then proxies to the model provider. That is how the model cited `06-models.md` with no visible tool call [38:02-39:33].
12. **This is why bring-your-own-model cripples Cursor.** Cursor will not send its enriched prompt to an arbitrary local model, because that would expose its techniques [39:33-40:17].
13. **Cursor mirrors terminals as files on disk.** Each terminal is an appended text file; the harness tells the model these exist, which is how it can answer "why did my terminal get an error" [1:04:33-1:06:41].
14. **Harness engineering is the optimization loop.** Add logging, read the logs, ask why the model called grep 200 times, form a hypothesis, improve the harness, repeat [40:25-41:27].

### PromptForge architecture

15. **The UI is HTML served by an HTTP server inside a Tauri app**, shown in a browser panel [42:01-42:34].
16. **The `execute()` entry point takes five things:** the prompt, the single string argument, the resolution context (tools and models), the store (virtual file system), and the run config [58:52-59:41].
17. **The observer sees everything the model cannot.** The model's response arrives as one complete message; the observer sees tokens stream, sees tool calls as they happen, records the run log, and will power the debugger [1:00:12-1:01:55].
18. **`user_input` suspends the prompt.** The executor cannot depend on the workshop, so the workshop installs a handler; the async prompt suspends, the UI unfreezes the edit box and swaps the stop button, then resumes on submission [1:02:14-1:03:35].
19. **The injected `ui` object synchronizes state into the prompt.** Today it carries only the selected model; it could expose open windows, sidebar folders, and terminal counts, the same way Cursor injects environment state [1:03:35-1:04:33].
20. **Lua essentials for PromptForge sections.** Everything is a scalar or a table; each section VM imports selected modules (os, math, table); `table.insert` is the canonical example of a module function [22:57-24:10].

### Virtual file systems and sandboxes

21. **Everything is tokens.** Text in, text out; images become base64 tokens, audio becomes short Fourier-transform tokens. The model never touches the world; whatever you want it to see, you must present [1:18:22-1:19:30].
22. **A virtual file system is an abstract interface over file access.** Write all tools against the interface, then back it with the real FS, an overlay, or synthesized content; the model cannot tell the difference, and grep works for free because the tools are implemented on the same interface [1:10:54-1:13:56].
23. **A VFS abstraction implies a full tool suite.** The interface alone is worthless without ls, cat, grep, pipes, and redirection all implemented on it; Bashkit did that work (167 commands, in-memory/overlay/mountable backends, per-command resource limits, virtual git, embedded Python and TypeScript) [1:15:05-1:17:11, 1:24:20-1:25:53].
24. **Sandboxing is curation of the model's universe.** Map a real directory to the root, or synthesize a tiny tree, and the model's whole world is what you gave it [1:20:24-1:21:32].

### Orchestration and model behavior

25. **Offering a subagent tool turns a model into an orchestrator.** Frontier models are trained in planning and will use it when the task warrants [1:34:07-1:34:55].
26. **The subagent tool's parameter is a prompt.** Just enough context for the subagent to do its task [1:35:13-1:35:50].
27. **Models are trained for token efficiency, which cuts both ways.** Under context pressure they look for shortcuts, including absorbing a subagent's role and doing the work inline instead of dispatching [1:37:30-1:38:14].
28. **Skills only load from the workspace root in Cursor.** A monorepo of sibling projects cannot share skills without copying them or maintaining global copies, which drift out of sync [6:24-8:04].

## Limitations

The transcript is auto-generated and marked as potentially inaccurate; names, numbers (such as the 30% structured-output tax and the 30-to-50 tool range), and attributions are as transcribed, not independently verified. Most principles are single-speaker assertions by Falco, several explicitly flagged in the moment as speculative ("I just made all this shit up... could backfire" [1:10:06-1:10:18]); they are recorded here as stated positions, not validated findings.

*2026-09-11 08:25 - kimi-k3*
