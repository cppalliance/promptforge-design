# Let's plan the MCP server

*2026-08-03 20:40 - transcript 0051b5be-9a70-4012-9dbb-376bbf3f8f21*



## Prompts



**[p2]** Okay, the purpose of this MCP server is to serve PromptGPT prompts, and I think that's it. And so the design might be a little over-engineered. So the whole point of this is so that agentic harnesses like Cursor or Claude Code, they can call in and they can run a PromptForge prompt, and the user configures how they want to expose the, the prompts. They can have the, all the prompts just exposed at runtime, like one big list, or what they can do is there's gonna be a built-in tool. Which is gonna be like the tool picker. The chooser and choose mcp tool and it's gonna use the classifier and. It can be, it can offer advice like a frontier model can say, "Hey, do you have any tools that would like help? " And then another possibility is, is that it can just have like the listing. So progressive tool revelation.

**[p4]** the config needs a directory wildcard option or something

**[p5]** I'm saying both. Individual prompts, or whole directories? what do you think?

**[p6]** I want active directory watch, this needs to be useful for a developer writing a prompt. They can't be restarting the mcp service every time.

**[p7]** wait a sec, can't the developer just start a new chat? when does Cursor build the list?

**[p8]** but run_prompt wants the prompt name and this is fuzzy no?

**[p9]** what if we use the mcp-tool-picker crate and instruct the mode to pass the need string to a need_prompt tool @promptforge-design/study-mcp-toolpicker/design-mcp-toolpicker.md

**[p11]** What in the fuck does this even mean? I do not understand any of it:

**[p12]** > One number to carry into that build, because it changes what you should calibrate against. Your hard-regime figures came from near-neighbor distractors in a 9,922-tool catalog. A prompt catalog is a few dozen deliberately distinct entries, which is the random-distractor regime - top-1 0.929 blended, 0.984 for a restatement-band need. Calibrating the floor against the hard-regime numbers would set it far too conservatively for this use and abstain on needs it should bind.

**[p13]** wtf? I have to choose a number?

**[p15]** The description for need_prompt should be such that a querying model will state it in tool author register is that possible?

**[p17]** is it possible to write the design file as we go? i.e. every time a step would change the design concretely can we update it? what do you think of this idea? so the design is accurate eper-commit

**[p18]** should we update @tools-public/tools/architect.md and/or @tools-public/how-to/vibe-how-to.md to make this handling of design/choices a new feature?

**[p24]** I think so? I dont really understand this. I just want my promptgate prompts to be first class citizens in Cursor. Shouldn't the research person output have gone into the chat rather than in this box?

**[p25]** I don't want hard-coding Cursor knowledge

**[p26]** I want it to behave like how other MCP tools behave. How does mcp pinecone behave? how does the mcp boost mailing list behave?

[troubleshooting: server not appearing in Cursor's tool list; mcp.json entry confirmed, resolved by restarting Cursor - p27, p29, p30]

**[p31]** wtf does "deferred-collect" mean ??

**[p32]** why does there have to be a timer? why can't our mcp server use the progress protocol to keep Cursor in the loop so it see that the thing is working

[directive: spawn subagents and search the web for how other projects handle this, including adjacent topics - p35, p36]

**[p37]** This is the first one:

**[p38]** [pasted: research-person report on Sean Baxter produced by PromptForge, ~19 paragraphs - p38 through p56]

**[p57]** it went straight to the web, no mcp

**[p58]** Okay, I don't know about this, because no, no, no, no, no, the purpose of the MCP is to just be able to, like. We're not gonna be exposing all the tools. Like this, first of all, this report person, like this isn't, this isn't the intention of how PromptForge is supposed to work. PromptForge is very specific. It's like, it's like a command. You don't just invoke a PromptForge prompt in conversation. It's very specific. The purpose of the MCP is for a user to explicitly invoke a PromptForge tool. So I would even go so far as to say that the word PromptForge has to appear in order for the PromptForge MCP to kick in. It's not, it's, it's not like normal tools. The PromptForge is about a pipeline that usually produces a type of report. It's a special, it's not a general purpose prompting language. It's a specific thing. The purpose of the MCP is so that the developer can invoke the scripts for the purposes of usually of testing, but it's also useful locally. But PromptForge is really a system designed to go like on a server, for example, a twenty-four seven process that's constantly running reports, like running a staker report on every company in the Fortune five hundred every month. That's what it's for.

**[p59]** No, developer console undersells it. Like, there's a legitimate use case if a user wants to run a report, like, for example, the dossier system. Like, the dossier system might work better as a prompt gate prompt. Because it's so deterministic and it works, like, has the context isolation, it's got all that good stuff. However, it has to be explicit. Like, it's like a command, it's like the user says, "Run this specific prompt, " that's how it's supposed to work. I think that has to be baked into the design of the MCP. And I also, I wanna rename it to MCP Server. And I've moved the design document, so I think we need a plan, we need a top-to-bottom revision of this whole thing, and we need to look at the other crates, we need to look at the design documents, we need to look at everything top to bottom using sub-agents for cleanliness, and we need to bake a plan to fix the whole thing in one go.@promptforge/crates/promptforge-mcp rename to promptforge-mcp-server. @promptforge/crates/promptforge-mcp/design-promptforge-mcp.md rename that too and fix the contents. @promptforge-design review everything here too

**[p60]** I think there's a confusion because we're talking about the the technology to calc to calculate the tool from the need, and we're we, we still have to have that. I think we still want that feature, but the feature is in the, is in the harness, it's in the executor, it's in the PromptForge core, because a prompt speci a prompt specifies the need strings in its front matter or in the initial Lua of the H1 block, and it says, it says, "Here's the need" in a sentence or two, and then it associates that with The ID, and the ID is internal to the prompt, and what we this, this solves the indirection problem, because we don't want the prompts to have to we don't want the prompts to specify specific tools. So that we have to keep. But we can lose the need string in the MCP server. Maybe, I mean, it's still kinda nice. To have, because if someone asks explicitly like which PromptGATE tool would be best for this need, then it'd be nice to be able to get an answer, but it might, it might not be strictly necessary. For now, the only thing we really need is for the developer to be able to specific execute a specific prompt. However, we've already built out this code, like MCP server already has the packages and everything, so what are we gonna do?

**[p61]** So I think an overarching principle of the whole entire project is we should do more with less. That means if there's an established facility that can implement the new feature, we should use the established facility rather than building out more infrastructure. The fact is that Lua already works, so we should keep using it rather than inventing new front matter. So that's like, that's the litmus test. Like, can we im can something be implemented using what's already there? We want this, we want the core to be minimal. We want a small set of primitives that we could reuse over and over and over again.

**[p62]** design documents for crates belong in the root of the crate not the root of the repo

**[p63]** I want this whole thing to be, I want this plan has to proceed in steps. Like, you can't just do everything at once. I want individual steps, like one design document at a time, and even for a design document, break it down, like re-refactor the old, refactor the big one in place, then transfer over what's there, and then do the thing, right? And then just basically follow the vibe coding rules, but do it for the reorg. @tools-public/how-to/vibe-how-to.md

**[p64]** the residue, the design stuff left over i want in a "residue" sidecar design-core-residue.md for example.
For design docs with no crate, create a folder at crate level with the proper name (e.g. promptforge-mcp-client) and move the design doc from the design repo into there.

**[p65]** actually leave the residue in the design repo as well

**[p66]** non-existent stuff stay in design repo as well. design-mcp has to be renamed design-mcp-client or design-mcp-server pick one

**[p68]** Seriously though, okay, this fucking design core residue, it reads like a fucking murder mystery. It reads like a "who the fuck knows what?" Like, this is so opaque language. Two of those five are refuted by the code rather than merely unbuilt, and the crate's own document says which? What the fuck kind of language is that? Jesus Christ! It's so hard to read. Look!

**[p69]** What it does not do, and cannot be made to do without a change to this document:

**[p70]** Read a file of configuration. Every value arrives through RunConfig.
Know a domain. No schema, no table, no paper, no search provider, no WG21 vocabulary.
Talk to an LLM backend. It holds a GatewayClient its caller constructed.
Persist anything. Storage is an extension's business.
Decide where an output lands. It resolves a declared output name against roots it was handed.
The test of the boundary: a project with no relation to WG21 can depend on this crate, write its own extensions, and get a working prompt runtime without deleting a line.

**[p71]** Two of those five are refuted by the code rather than merely unbuilt, and the crate's own document says which.

**[p72]** is the sentence riddling fixable in @tools-public/tools/architect.md and @tools-public/how-to/vibe-how-to.md  easily?

**[p73]** I don't know about this. This isn't, it's, this is, you're, you're making it too narrow like a counting problem. It's not just, it's not just a counting problem, it's fucking everywhere. Parsing is total and produces no side effects. A prompt isn't her data. What the fuck does this mean?

**[p74]** Parsing is total and produces no side effects. A Prompt is inert data: it can be constructed, inspected, and enumerated on an MCP surface without running any prompt code.

**[p76]** but picking 3 sentences at random means what, that only 3 sentences will be legible?

**[p77]** I think, I think when, when the architect or the vibe coder, when they produce design work, I think they have to just state facts. Not, it's not a design document, they just state facts, factual statements, and then we spawn a separate sub-agent, and that's the writing agent, and that takes the facts and it composes prose, and we give it a register to write in. And the reason that that works is because there's no context pressure. It's not trying to reason, it's not trying to do anything. The, I think the problem is we're trying to do the writing in the same commit That's doing fixing and design work, am I wrong?

**[p78]** would it be possible to do this:
in a fresh subagent, review every line in the entire crate, write out facts that correspond to design
in a separate fresh subagent, take the line by line review and write the design from it

**[p79]** can you first collect all the whys as a list of bulleted statements extracted from the existing design docs, code comments, and commit log, into a "why document" and then go through a single crate source code and do the filtered extraction, and from there use that to reason about hierarchy (what breaks what) to define a design report template and then in one or more subagents write the design document from the report template + the why file + the filtered extraction file?

**[p80]** Can you reverse engineer the rationale? Like for a given feature, for example, for a public function, come up, just use the model's reasoning and come up with like three or four plausible reasons for why it was done that way. I mean, a frontier model can do that. And then as you go, you'll find eventually, s there'll be some subsets of, of reasons that, like, they'll cancel each other out in a way that leaves behind only one possible reason. Like you come across a piece of code that's written a certain way and that collapses some of the reasons for other choices. So we have like a running list of design choices and as we go through the code, we collapse them when we, as we make discoveries, and then whatever's left, we can assume that those are the actual reasons. Then we don't need the why file. This is a genuinely useful tool. Reverse engineering a design doc from an already written codebase is useful.

**[p81]** I like this. This is, we should do this. We should try this. I wanna try this. And let's do this in the core crate. I wanna try it. We're gonna put together a plan, and you're gonna do it. And when you when you collapse, you state that confidently. But then when you can't collapse, keep those design elements separate. And then what we'll do is then we'll do a combination of a human guided answers plus hypothesis collapse using the other stuff in the repo, right? So the first pass, we don't look at the existing design. We, it's a pure reverse engineer. In the second pass, we look at what's there, and then the AI will propose collapses based on what's there. It won't never do it automatically. The, it'll ask the human, and the human The human will say, "Yeah, this makes sense, " and then the human can also provide additional rationale. Just a few sentences from a human can probably collapse a huge amount. So let's do this. Let's go into plan mode. We're gonna do this right now. And when you make the plan, I want it to be ready to run in a fresh context, 'cause we're about at the limit. So make sure you inline everything.@promptforge/crates/promptforge-core



## Plans

### promptforge mcp server

*Build `promptforge-mcp`, a small MCP server that publishes PromptForge prompts to agentic harnesses (Cursor, Claude Code) as tools - some prompts exposed directly, the rest reachable through a progressive listing pair - and add a minimal Observer/Event stream to the core so a run reports live progress.*

Scope: the only job is serving prompts to a calling harness. This build drops the Django endpoints, the run registry, extensions and `[tools]` bindings, output roots, hot reload, and service installation - those were written for a deployment that does not exist yet. Two deviations from design-mcp.md, both forced by what the core actually does today: arguments are a single string (so no `params` schema enters frontmatter), and the result carries the value, not a path (the core writes no output files, so the returned string is the product).

Exposure modes, both live at once: each prompt carries `expose` - `"tool"` publishes it in `tools/list`, `"list"` (default) leaves it reachable only through the progressive pair (`list_prompts`, `run_prompt`). The classifier-backed chooser is the third mode and is deliberately not in this build; it slots in later over the same catalog with no change to what is built here.

Core changes: a new `promptforge_core::observe` (`Observer` trait, `Event` enum, `NullObserver`); `completed` never decreases, and that guarantee is what lets the MCP side latch it. `execute::run` grows one options argument (`RunOptions { observer, client }`), a single breaking change. The explicit client matters because the server configures the gateway in TOML and `std::env::set_var` is unsafe under edition 2024 while the workspace forbids unsafe.

On duplication: a third copy of the gateway's `Secret`/`${VAR}` config interpolation would justify a shared crate; two does not. On the `rmcp` pin: starting greenfield code on 2.x buys a migration in a few weeks, so pin `=3.1.0` and fall back to `=2.2.0` if its `ServerHandler` surface fights us (medium confidence).

Transport and auth: `/healthz` is registered outside the bearer middleware so the exemption is structural. `serve --stdio` is offered because it costs one `rmcp` call and is how a local Claude Code install would attach; the design doc's refusal of stdio assumed a networked workstation only. A call that waits past `admission_timeout` returns `isError: true` naming the wait, so the model can retry.

Progress: `RunStarted` sends frame 0 so the client shows something immediately; `ModelTurn` and `ToolCalled` are logged only, since up to thirty per section would bury the section label. With no `progressToken`, no pump spawns and the run is otherwise identical.

The result: the `content` text block carries the value itself, since it is the entire product of a run in this build.

Boot validation: failures accumulate and are all printed before a nonzero exit; one bad prompt refuses the whole service, so a client never sees a silently missing tool.

Deferred, on purpose: the classifier chooser, `notifications/tools/list_changed` and hot reload, the Django HTTP surface and run registry, elicitation, extensions and output roots, and service installation.

[step list, config schema, code blocks, mermaid diagram, and test plan omitted per reduction rules]

### promptforge mcp server correction

*Correct the MCP server from a surface that competes for a model's tool selection into one that only executes prompts a caller names explicitly, rename the crate and its design document to `promptforge-mcp-server`, and reconcile every design document in both repositories with what is actually true.*

What is wrong: a PromptForge prompt is a command. It is invoked because someone named it - a user asking for a report, a developer testing a pipeline, or eventually a scheduler firing a run. It is never something a model reaches for because it noticed a tool that looked relevant. The system was built on the opposite assumption, and not only in the server: `design.md`, `design-mcp.md`, and `design-promptforge.md` all state the model-selection model, and the code follows. `notes.md` records the design that was rejected - "two MCP tools: `list_prompts`, `run_prompt`". That rejected design is the correct one. This plan is correction and coherence only.

Design decisions:

1. **`run_prompt` is the only way to invoke a prompt.** No prompt is published as a tool of its own, so nothing this server offers can be chosen for a task the caller did not ask for by name. Naming one is what a command is.

2. **The published tool list is fixed at four entries and never changes.** `list_prompts`, `run_prompt`, `check_run`, and `need_prompt` with the `picker` feature. Because the list is static, the client-side caching that shaped two earlier decisions stops mattering: a prompt saved thirty seconds ago is callable immediately with no reconnect, and the `notifications/tools/list_changed` machinery is deleted rather than fixed.

3. **`expose`, the promotion workflow, and the direct/listed distinction are removed, not defaulted off.** An opt-in would preserve the ambient-selection path and its caching problem while leaving the design two shapes to explain. The cost is real and accepted: a prompt can never be called under its own name as a tool, and per-prompt typed argument schemas are permanently off the table.

4. **`need_prompt` resolves an inexact name, it does not discover a capability.** It serves the caller who says "run the promptforge prompt that builds a stakeholder report" without knowing it is called `staker`. That is still explicit invocation - the intent came from the user. What it must never read as is an invitation to go looking for something useful.

5. **The tool text is written in the register of a command interpreter.** No trigger phrasing, no "use this when", nothing that competes for selection against a client's own tools. A model that ignores this and never calls the server is behaving correctly.

6. **A prompt named after a built-in still fails at boot.** "Run `check_run`" is ambiguous to a human and to a model, and a boot refusal naming the file is the only version of that a prompt author can act on.

7. **The crate is `promptforge-mcp-server` and the binary matches.** The old name described a protocol; the new one describes a process, which is what it is.

8. **Every design document in both repositories says the same true thing when this is done.** A corpus where three documents argue for model selection and the code does the opposite is worse than either position; the argument in `design-mcp.md` for rejecting the dispatcher has to be replaced by the argument for accepting it, not merely deleted.

What stays exactly as it is: catalog resolution with its glob-plus-exception rule, per-prompt reload where a broken prompt stays listed carrying its error, the watcher, the deferred-collect ticket and `check_run`, admission, progress notifications, the finished-artifact sentence, boot refusing an incoherent catalog, both transports, and `Catalog::hash`.

On configuration: `default_expose` and per-prompt `expose` are removed, and unknown keys still fail the load with a message naming the key - silently ignoring one would leave an operator believing a prompt was promoted.

House rule carried from the previous plan: a step whose implementation contradicts a decision here revises this plan in the same commit.

Deliberately not in this plan:

- **Somewhere to put a report.** Both repositories specify it - `outputs` in frontmatter, output roots in `prompts.toml`, a result carrying a path rather than a body - but nothing implements it, so a run's product exists only in the reply. This is a `promptforge-core` feature before it is a server one, and it is the obvious next plan.
- **The continuously running report runner.** The real deployment is a process producing reports at scale, monthly. Neither repository designs a scheduler; what exists is `fanout()` over sections, which is one run doing many things, not many runs over many subjects. This needs a design conversation before it can be planned.
- **The dossier system as a prompt.** A strong candidate - its phases are already gather, extract, synthesize, finalize. The frictions are real: the rules live across three files and ad hoc plans rather than one executable spec, its acquisition phase is open-ended and judgment-driven, its Executive Summary is written last from everything before it which fights context clearing, and it needs private sources through several MCP servers rather than the open web.

Execution model: each step is one commit, written in one subagent, reviewed in a second with a fresh view, fixed in a third; git stays in the main context.

[step list, review checklist, the reusable design-doc writing-rules block (~85 lines), mermaid diagram, and todos omitted per reduction rules]

### recover core design rationale

*Recover the design rationale of `promptforge-core` from the code alone by generating competing explanations for each design element and killing the ones the evidence refutes, then let the repository's documents and history propose further collapses that only a human approves, and write a design document from what survives.*

What this is and why it might work: a design document is mostly *why*. Code contains *what*. The bet here is that a large part of the why is recoverable anyway, because most design choices are forced by constraints that are themselves visible in the code - and where nothing forces a choice, that fact is worth stating rather than papering over. The method: for each design element, write down three or four competing explanations, then hunt the crate for evidence that kills them. What survives is the answer. How many survive is itself the finding.

Worked example of an element that collapses: `execute::run` takes its gateway client through `RunOptions` rather than reading the environment. Of four competing reasons (testability; a file-configured caller cannot set the environment; taste; no reason), the workspace's `unsafe_code = "forbid"` plus edition 2024 making `std::env::set_var` unsafe kills all but the second - necessity, not preference. Verdict: **forced**, and the document can say so flatly.

Worked example of an element that does not collapse: `DEFAULT_MAX_TOOL_ITERATIONS` is 24. Measured, derived from a token budget, a generous round number, inherited - nothing in the crate distinguishes them. Verdict: **open** - the honest document says the code does not determine it.

The failure mode this guards against is confident fabrication. A model asked why some code is the way it is will always produce a fluent answer, and a wrong one reads exactly like a right one. Requiring competing explanations and demanding evidence to kill them is what makes "I cannot tell" a reachable answer.

The method, precisely: an element counts as design only if changing it would change what a person sees, reads, writes, types, or names (for a library, the public API and its contracts, emphatically including names), or the shape of the system, or something costly to reverse that nobody sees. Evidence is anything structural - a type, a signature, a lint setting, an edition, a test that would fail otherwise, an absence where a presence would be expected. Plausibility is *not* evidence: "this is the sort of thing people do for testability" kills nothing. A hypothesis dies when evidence makes it impossible or makes it unnecessary. Three verdicts: **forced** (one explanation survives), **narrowed** (two survive; name both and say what would distinguish them), **open** (three or more survive). An element whose hypotheses were never seriously competing is a failure of the method, not a success: if all four candidates are variations of one idea, the collapse is theatre.

Pass 1 is blind, and the isolation is the experiment. It reads the crate's source, tests, and manifests, plus sibling crates only to see how core's API is used; it may not read any design document, residue, README, STATUS, AGENTS, or git history. Comments are treated as absent - deliberately blunt, because deciding which comments give reasons is itself a judgement call, and pass 1 is meant to have none. The cost is real and worth accepting: this crate's comments are unusually good, so pass 1 will report *open* on questions the file plainly answers three lines above. That is the point - it measures what the method recovers when nobody wrote it down, which is the situation the tool exists for.

Pass 2 opens the archive, and the human holds the pen. For every narrowed or open element, search the design documents, residues, and git history, and write a proposal with provenance - a file and line, or a commit hash and its date. Provenance is not decoration: this repository's own history contains reversals (the design corpus argued for model selection; later commits made invocation explicit), residues describe things never built, and many commit messages are self-reported by the agent that wrote the change. No proposal is ever applied automatically: they go to the author in batches of at most five, and a few sentences from the person who made the decision will collapse more than any amount of searching.

The ledger: one record per element, ranked by `Reach` and `Seen by` - how much breaks if this changes, and whether a person ever encounters it. Both are needed, because a single configuration key can have almost no reach and still be the first thing a reader must understand.

Execution model: dispatch every step to a fresh subagent by reference - hand it the plan's path and the step number and nothing else of substance; if a subagent needs to know something, write it into the plan first.

How the prose must read - two rules bind the final document, and they exist partly because the last document produced in this repository was accurate and unreadable:

- **State what happens, not what property a thing has.** Bad: "Parsing is total and produces no side effects. A `Prompt` is inert data: it can be constructed, inspected, and enumerated on an MCP surface without running any prompt code." Good: "Reading a prompt file never runs anything inside it, which is why a server can list prompts and show what each one claims to do without executing them."
- **Never count what you do not name.** "Two of those five are refuted by the code" sends a reader hunting. Name the two.

What this cannot recover, stated up front: contingency - a number chosen inside a range, a fact measured outside the repository, an approach tried and abandoned. The clearest example lives one crate over: the MCP server waits 240 seconds before handing back a run id because Cursor abandons a remote tool call at about 300 seconds - learned from forum threads, appearing in no file. Worse, and unfixable: a deleted alternative leaves no trace. Nobody reading the current server could learn that prompts were once published as individual tools or why that lost, and "what lost and why" is the most valuable line a design document has. A high open count is partly this - not a failure of effort, but the archaeology being genuinely gone.

[step list, review checklist, ledger record format example, mermaid diagram, and todos omitted per reduction rules]

## Design Documents Written

[written: the watch-check test prompt in three variants - one a deliberate parse failure with prose and no H2 section - plus edits to promptforge README.md and STATUS.md; watcher test artifacts]

