# Orchestrator Design Document continued (reduced)

*2026-07-28 22:38 - transcript db6e4704-2a00-4555-9b90-c11dedac94c3*



## Prompts



**[p1]** what do you think of this algorithm:

**[p2]** [pasted: Slack message to Will Pak describing a recursive transcript compaction algorithm - compress the first N/2 lines in half on each cycle, prepend the original prompt to every compacted context, persist the full uncompacted transcript to the database, begin compaction early at ~90% capacity to hide latency; also floats open-weight models as an orchestration layer via an injected Task tool]

**[p3]** I would use this for @tools-public/tools/mentograph.md

**[p4]** is a frontier model actually needed for interviewing? the largest open-weight models are pretty damn good and this is not a deeply analytical task

**[p5]** I was thinking more along the lines of 800B+ open-weight models

**[p10]** lol this is running at scale :) I dont need to hear about macbooks

**[p11]** Question: how practical is it for me to replace @wg21-paperflow/packages/assay/src/assay/ and its pipeline with a model-orchestrated prompt? By writing the Task tool?

**[p12]** dont code fence me

**[p13]** okay but think of this - instead of passing Pydantic OUT of the model orchestrator, we can give it a small set of Tool calls which form the pydantic data instead.

**[p14]** it gets better. the python harness can slice the input prompt by section, and each section has a stable id. and the entry section is called "main". Then we add a ToolCall which the model can invoke to throw out the current context and start a new context from another section. In other words the model chooses the next step, but with a fresh context (and the accumulated state from the other toolcalls)

**[p15]** you dont understand, there's no compaction here. The compaction was for Mentographist. Now we're talking about a new Assay pipeline. The Mentographist would necessarily be a totally custom app, because it wants audio, speech, optimization, etc.. What I am ttalking about now is a new general purpose system for the shape of what assay does. Analyzing papers. For example, we could implement @tools-public/tools-wg21/papergate.md this way. The benefit of this new model of orchestration is that it allows for rapid protyping and iteration of new pipelines without fucking with a lot of python. You get the benefit of a single markdown file, much like what we are doing in Cursor, and a single general-purpose Python harness that can run anything that is assay-shaped.

**[p16]** I mean you're talking 30B models but I was thinking more like 400B models. But regardless, with this architecture we could easily hop between model tiers per step. Another thought, for example assay divides the paper up into sections and this is done with python. That could itself be a toolcall.

**[p17]** To keep things focused, the python harness can read the prompt section for the list of allowed tools. this keeps the tool list small so the model doesn't get confused

**[p18]** Now we can design using a library approach. New, small tools written in python. But it gets better. With the Task tool we can nest to arbitrary levels (with a safety valve). A prompt can subagent another algorithm which itself uses subagents. So one could implement reasearch(topic) which spawns subagents, and then call Task( research(topic) )

**[p19]** deeply nested task chains are debugged by making each subtask well tested and well defined

**[p20]** I would also say Task("research.md") could instead be Task("## Research") where it references another section in the same prompt file. This solves the problem where the orchestrator re-invents the prompt causing drift. The prompt comes from Python, not the model's interprertation of the prompt. No contamination.

**[p21]** Let's plan a design document. BLUF, inverted pyramid of techniques. enough for someone to implement where that somene is already proficient at working on the assay pipeline. Pick up all the good stuff we talked about so far (make the Compaction discussion a separate unrelated section coming after the orchestrator idea). Also see if there's anything in @tools-public/how-to/how-to-write-prompts.md which translates well into this new mdel

**[p23]** Question: how do subagents return the data? as Pydantic?

**[p24]** There's a problem here. Pydantic recognizes a failure mode. How would we?

**[p25]** question: could each section have an optional code fence with user-definable Lua code to define preconditions and insert tools and what not

**[p26]** why did you fence that exposition

**[p28]** the pipeline author is you LOL

**[p30]** is it just me, or is the Pydantic layer expensive? basically you have to route all your model calls through it, so that it can inject the guidance? or am I wrong? how is it possible that I came up with a better way?

**[p31]** 1. For triple-compacted content in Mentographist, but think about it. The older stuff gets compressed out of existence, and thats ok! we dont need the older stuff because we already captured the user's story. As long as we reinject the prompt at the beginning of the new compacted context, we are aligned. The only downside is that the model can't remember if the user repeats a story. But this is unlikely as people are not going to tell the same story over again.

**[p34]** what about a special, small model for compaction that is fine-tuned for only that?

**[p37]** I would like several worked examples, each of which combines a few of the ideas together to show how they can work. and then I want one large worked example that shows everything. The resulting design document should be richly detailed enough for any frontier model to produce working code including tests

**[p40]** now lets look at @tools-public/tools/briefer.md and consider how well this maps. are there any steps that would require a large number of tools? how would this work? is it ok for a tool to set multiple metadata fields, do smaller to medium size open-weight models handle that well?

**[p41]** obviously we wont be using AskQuestion in these pipelines

**[p42]** Question about the Diagnosis. Can we just use a separate subagent per test?

**[p44]** So this is where the orchestrator gets weird. How do we specify the 53 tests? right now they are in a nice bulleted list but if we are going to do this right we need them.. each in their own section? There has to be some markdown syntax to say "this is a fanout with each spoke having its own prompt"

**[p45]** oh I love this! by putting the prompt itself in Lua as individual sections, the tool can write itself.

**[p46]** The harness needs to have an easy way to say "combine all the fanout results into a single document" with the option for preserving order, or not. And we could have "virtual files", i.e. the harness offers tools CreateFile, AppendFile, DeleteFile but these are not real files they are just in-memory blobs. The agent doesn't know any better

**[p48]** the scope is not as big as you might think. a lot of these are just specific examples of a general principle. like the tools

**[p49]** Let's take a detour for just a moment and then return back to this. What is the practicality of implementing a harness that can, for example, run something like @tools-public/tools/diligence.md without modification?

**[p51]** you are overthinking it. I am essentially asking, how do we just do what cursor does? I'm not asking to decompose based on section headings. Just pass the entire prompt to a model and say "do it"

**[p54]** okay thanks. none of that detour should affect the plan. Update the plan for what we know

**[p55]** when the plan runs I want every idea to be enriched with subagent web search, look for prior art, look for related work, look for anything that would be a subcomponent to build the idea, look for information about performance, metrics, model tier, and so on. don't write before researching and think deeply I want a fantastic report. write the report to @wg21-paperflow/promptforge.md

**[p65]** I wanna keep talking about it, so now I'm thinking, so now I'm thinking that the basic unit of operation is the function. Basically, it's a inference and a function, the return value is a string. It's just a string and the inputs are-is a structured input key value pair, I guess and Every prompt, for each prompt, is a function. You pass in parameters and it returns a string, but it can have side effects. Okay, now. Every section heading. Is also A function. But It returns a string, but it can only take a string. And the string that it takes is defined by the node that transfers control over to it. So for example, if you're in a section and then we do a go-to. Well, we have to, we pass a string. We have to pa we can pass an optional string. And the goto is actually, there's, there's only gonna be one tool for transferring control. And we can make it, let's say that it's ca we'll give it the name call. And the first parameter to call is the type of call. It's a goto? It's a Function? It's Context preserving goto maybe, I don't know, but, you know, there's a type. or, or it could even be a return. Maybe, maybe it's also a return, but it takes a string. And that string is passed to the destination. And if the destination is a node, then that becomes the beginning of the prompt, like that gets, that gets injected, or it can go to the Lua, and then the Lua can like manipulate it, something. What do you think about that?

**[p66]** So the model has to be able to route, because what we, we, we wanna let the model orchestrate sometimes, like when it really has to make a decision, we need to let it route. Like the, the model spawns the task. For example, if it's doing a guided web search, we can't do that in Lua. It has to do a web search, and then it has to pick, and then it has to choose the page, it has to look at the page, then it has to keep making decisions, the multi-turn decision making. And so we need both. We need call from Lua And we need call from the model, like that's where the power is. But also, I think we need a substitution syntax. Like there has to be some kind of syntax where that means that in the prompt, the, the harness, the, the, the pro-prompt forge executor has to perform a substitution from a Lua variable. So in Lua, there's a state, and every element, it's a, it's a table, and each element has a name, and then you can, you can quote the state as a substitution in the prompt And that gives you determinism.

**[p68]** we are doing this in Rust

**[p71]** So the user can't declare arbitrary globals, there's only a fixed number of objects that they can access.

**[p72]** Spawn a subagent and update the plan. And make it Lua instead of Python, go through, rewrite the whole thing, and I want a table towards the top. The list of objects, a list of functions, and then for each object and each function separately, I want to explain like what it is. I want dense enumeration of all the features that we've talked about towards the top so that I can review it. I want the plan to read like an inverted pyramid, and I want an executive summary at the top. But I want you to do this in a subagent, the subagent can reference this chat by its full path so that we can keep talking. And you won't try to update the plan until that sub-agent is done, so we can talk. And when the sub-agent is done, then your restriction on changing the plan from the main context will be lifted. Are we clear?

**[p73]** Okay, so I think we need to think it through. Like what are the subheadings? So if i have an h two Basically, main is a function that takes key value pairs and returns a string. Well, it doesn't need to return a string. Like It can, but if The primary from a different subhead than that one  is responsible for returning the stinrg.

**[p74]** Actually, I think, I think every section can see the key value inputs to the prompt, and they're read-only, I think. Maybe, I don't know, but any, any piece of Lua anywhere in the prompt should be able to access the, the parameters. So, so if there's a file name and we wanna have, like, every section does something to the file, we wanna, we want them to be able to go from section to section accessing that value, we don't wanna have to pass it around.

**[p75]** In light of this. Basically, because this is kind of biased towards implementing pipelines, then I think on an H2 you run it, and if it falls through, then you just go to the next H2. And, but that has to be context clearing. That's the equivalent of "go to" and then the next section. And then you keep doing that, and if you run off the end, then the prompt ends and it, there's like a default message that says, "Okay, it's done. And If You can specify that string in the yaml. If you want to override it, or if you don't specify it in the YAML, then the ex-the executor gives a default. So it's always well-defined, and it keeps your prompt short if you're, if it's the simple case, like if, let's say you have three steps, and you're gonna process a file, each step accesses the path, it does its thing, it starts in a fresh context, it accumulates state, and then it's done.

**[p76]** instead of params what do you think of args

**[p77]** So are these args, are they just always strings? What if there's a table? What if the lua code puts a table there? What if there's a floating point number there? What if there's a, I don't know, an object? I don't know. What are the top possible Lua things?

**[p78]** Why can't we use turn? Why can't JSON? Why can't we use JSON? That's elegant. Then the Lua can assemble a JSON object and then The LLM can return it using a macro substitution. That's like pedantic, that's pydantic with perfect return and no overhead.

**[p79]** And I would go one step farther, I wouldn't even use Jason, I would say. I would make, I would say tool call, instead of call, make it say tool call, and tool call will. Under the hood, structure the data, structure the table however the model thinks it's best, or however the harness thinks it's best. Is there, is there a utility there? Like, what if someone wants to use, like, there's this other form of JSON that's like more compact? You know what I'm talking about? Then we could do that under the hood.

**[p82]** The, the plan needs to show the YAML. Or is, yeah, the YAML front matter, like what are all the keys? Should, tell me now.

**[p84]** Yeah, the concept makes sense, but a complicated prompt could have like twenty schemas, and they're gonna be big and intimidating, and now we're going back in the direction of pydantic. I know it's not the same, we're not injecting a bunch of shit into the context, but we are shifting it, right? We're shifting it to the Lua, or am I wrong?

**[p85]** Well, I mean, we could have twenty tools, we could have twenty, you know, state setters and, but each Each subhead only needs a few of them, like we don't need all twenty available at once.

**[p86]** Here's the problem I see this ad statement. Like, that means we need Rust code be-backing it. Like, what's add statement? Like, is that a database operation? That means every prompt now has to have a Rust file. But the whole point of this was that we it was self-contained. So now what's going on here?

**[p87]** someone has to connect the model's tool calls to writing to the Postgres or SQLite db. Look: @wg21-paperflow/packages/assay

**[p88]** Yeah, so I think I want a level of indirection like the prompt has these abstractions where it's operating in the semantic space like add claim, remove claim, and these operations aren't they don't know anything about the database. And then, but then in order to run that prompt, you have to have a configuration file just for that prompt that maps, right, that, that has bindings for each of the abstract tools that the model expects. You need to map it into a Rust crate. Now, we can make that generic, like we can make a postgres crate that offers a tool and a way to read a configuration file and automatically binds the postgres operations, like that one can have the schema, but the tool itself shouldn't. Because that makes the tool flexible. Like, m-m-maybe you don't want Postgres, maybe you want SQLite, or maybe you want MySQL, right? We don't wanna hard code it in the tool.

**[p89]** Yeah, not only that, but I want I want I don't want the tools to be listed in the front matter. That doesn't make sense. The, the harness, right? The execution model should be able to take a prompt and figure out what tools it needs, 'cause it can just parse, it can just parse the Lua and like, it can, it can stub everything and then it can just tr-intercept the tools, the, a call to add the tool, and it can know every tool that gets added. So when we load a prompt, we, we do that. We enumerate all the tools, we deduplicate, and then we go and we look it up in our bindings. And if something's missing, of course, we fail to load, we give an error. Otherwise, we apply the binding. And we can have a command that creates the bindings file with empty settings, and then the user fills it in, or the admin.

**[p90]** The schema has to attach to the tool, because think about it, if I have 50 prompts and they all use the same tool, what, they have to repeat the schema 50 times? That doesn't make sense.

**[p91]** So there needs to be a note in the design document, like in the plan, and this has to be very strong, and that is the tool commands, the command like the tools to add the tools and to remove the tools. We have to make sure that anything that we do with that design is done in a way that the harness can run all the Lua and hoover up all the tool calls.

**[p92]** what if the lua code goes into an infinite loop

**[p93]** what if the tool needs to like write files and stuff and it gets access to lua library that reads and writes files

**[p94]** It's the Lua, people are gonna wanna do general purpose computation. Like, people are gonna end up writing functions and generating random numbers and all kinds of shit. So, I'm not confident that we can detect all the tools.

**[p95]** No, but think about the life cycle. Someone downloads a prompt from the internet, they're like, "I'm gonna use this cool prompt," and now they're faced with the problem, they have to configure it. Well, how do they know what tools it needs? It would be nice if you could just, you know, run the orchestrator with the, with the, with the, with the command line flag and say, "list all the tools, " or better yet, output a config file that's like an empty template that has all the tools in it and ready for you to point them to the right thing.

**[p96]** I want you to spawn a subagent and look at, like, look at brefor. I'm gonna show you brefor, and I want you to give me an idea, like, does it really need all these claims and hooks and shit, or can we just get away with, like, blobs, like, just strings? Because think about it, a, a prompt can do everything through files, so if we make file the unit of state, then it's all files. @tools-public/tools/briefer.md

**[p100]** This can't be right. What about the "breadcrumbs?" That's structured data!!

**[p102]** make up a promptgate diligence prompt. it doesn't have to be perfect just capture each idiom. not the whole tool. this is a simplified prompt to understand. write to @promptforge-design

**[p105-p112]** [troubleshooting: file:/// links to the plan file would not open because of Windows paths; eventually resolved, and a design-plans.md with working links was created]

**[p114]** Here are the design principles extracted from the huddle:

**[p115]** Architecture

**[p116]** All inference traffic must bottleneck through a single gateway process (in Rust) to enforce global concurrency limits across all apps, languages, and machines
The gateway is needed because vLLM lacks proper queuing, rate limiting, and 503 responses
Rust is chosen because it compiles to a native binary that can be installed as a Windows service or Unix daemon - always running when the machine starts
Loopback connections don't require API keys; remote intranet access uses whitelisted IPs or API keys
PromptForge as a unit

**[p117]** Every PromptForge prompt is a single markdown file and is one function - it takes well-defined parameters (declared in YAML front matter, machine-readable) and returns a string
A prompt can produce side effects (create files via tools) beyond its return value
The single-file-per-prompt model reflects the existing workflow and should be preserved - if you want to spread work across files, you decompose into individual functions (separate prompt files)
Directories can serve as namespaces for organizing prompts
Prompt-first inversion

**[p118]** Unlike other frameworks that start with the interpreted language (Python, Go) and bolt on prompts, PromptForge starts with the prompt and adds structured programming (Lua) into it
You should be able to write a PromptForge prompt with zero Lua and it works like a Cursor orchestration - Lua is additive, not required
Small-model friendliness (the core pressure-relief principle)

**[p119]** Each design choice is evaluated by whether it relieves pressure on the context window, enabling smaller models
More Lua = less model sophistication needed (offloading orchestration logic from the model to deterministic code)
Eliminating Pydantic removes both the conformance burden on the model and the injected system prompt overhead
Context-clearing transitions (goto) avoid accumulation and let you run with a smaller model
Tool count must stay within 5-7 for small (7B-14B) orchestrator models; control flow primitives may collapse into a single tool with a mode parameter based on testing
Control flow

**[p120]** call - invoke another section/prompt, preserving context, returns to caller
task - invoke with a fresh context (sub-agent), but still returns a result
goto - transfer control to another section/prompt, does not return, clears context
These three may collapse into one tool with an extra parameter if small models can't handle multiple control-flow tools
Calling another prompt by filename (e.g., research.md) invokes it as a function
Intra-process prompt-to-prompt calls go direct (Rust function call), not through MCP - sockets are unnecessary when you're already linked in
Section transitions and context hygiene

**[p121]** Falling through to the next section is the default when no explicit control flow is specified
Between sections, the model's narration and throat-clearing should be trimmed rather than carried forward wholesale
Preferred mechanism: a tool call to advance to the next section where the model explicitly passes only the context it wants the next section to have - this is better than bare goto because it lets you pass a curated instruction string
MCP integration

**[p122]** PromptForge prompts can be exported as MCP tools via configuration - the YAML front matter (parameters + description) provides everything needed to define a tool
The server monitors the prompt directory for file changes and refreshes its cache - no restart needed during development (developer convenience, not a production feature)
The PromptForge MCP server can itself be an MCP client, connecting to other MCP services (e.g., Pinecone) as configured

**[p123]** What do you think about this? How about if I shove everything into the plan, and then I tell you to just implement part of it, just like a subset, and then you subtract the subset that works from the plan, and then we do and then we keep planning, and then we do the next tranche, because we have multiple programs. We have the MCP service, we have the gateway, we have the PromptForge executor, we have a lot of shit going on. What do you think?

**[p129]** What's the smallest thing we can implement? Can we just implement the executor and we just, and have a, a frontier model invoke it using the shell command from the command line? And it doesn't even do any inference, it'll just like, I don't know, print "Hello, world".

## Plans

### Orchestrator Design Document

*Write a design document for a markdown-driven, model-orchestrated pipeline runtime that replaces hardcoded Python orchestration with prompt-as-program execution, covering the section/goto/tool-call architecture, composability, and (separately) the transcript compaction algorithm.*

Principles and decision rationale kept from the plan structure:

- BLUF: sections as procedures, goto as context-clearing transition, tool calls as state, markdown as program. The payoff: new pipelines without Python, per-section model tiering, prompt-integrity guarantees.
- Three-layer architecture: a generic fixed runtime, a slow-growing shared tool library, and one markdown file per pipeline where all iteration happens.
- The goto primitive: destroy the current context, start fresh from the target section's prompt with only params and state-store access. This eliminates context bloat.
- Tool-call state replaces structured Pydantic output: flat argument signatures are reliable on small models, state builds incrementally via tool calls, persistence is a side effect of filing tools, and cross-step data flow becomes pull-based through query tools.
- Per-section tool scoping: the section header declares its allowed tools and the model only sees 5-10 tools per section; doubles as a capability sandbox for sections processing untrusted input.
- Verbatim section dispatch: `Task("## Extract", chunk_id=3)` resolves the section reference in the runtime, not the model. The model never touches the subagent's instructions. No prompt drift, no contamination.
- Model tiering: each section declares its model slot (400B orchestrator, 27B extract, 14B quote verification), resolved from a services config.
- Composability: Task can reference sections in the same file or external pipeline files, with isolated state stores per nesting level. Safety valve: max depth plus max total tasks, configurable per pipeline.
- The Python harness explicitly does NOT contain orchestration logic, prompt assembly, or step ordering; those live in the markdown.
- Testing principle: each section is testable in isolation with known inputs; the unit of testing is the unit of composition.
- Migration path: not a rewrite of assay - a proof-of-concept alongside it, starting with PaperGate (simpler, two-stage), graduating to assay-equivalent if PaperGate validates the model.
- Compaction appendix (explicitly unrelated to the orchestrator): recursive halving, fidelity gradient (recent full-resolution, older progressively compressed), structured preamble exempt from compaction, pre-compaction at 90% capacity, full transcript preserved in the database. The orchestrator clears context via goto instead of compacting.

[Dropped per reducer rules: key-files inventory, todos/step list.]

## Design Documents Written

### c:\Users\Vinnie\src\cursor\wg21-paperflow\promptforge.md

BLUF (kept): PromptForge is a general-purpose runtime that executes analysis pipelines defined entirely in a single markdown document. The markdown is the program, the model is the CPU, embedded Lua is the microcode, and a ~300-800 line Python harness is the instruction decoder. A pipeline is a set of named sections; the model transitions between them with a context-clearing `goto`, builds all state through flat tool calls into a persistent store, and spawns subagents by section reference so the prompt author's exact words execute without drift. Each section declares its model tier and its scoped tool set in a Lua block that also runs preconditions and postconditions. The same generic runtime runs any pipeline that is "assay-shaped" - Assay, PaperGate, Briefer, Diligence - so a new pipeline is a new markdown file, not hundreds of lines of new Python.

The payoff is threefold. First, iteration speed: a new analysis tool goes from idea to running in an hour, edited in one file, with no orchestration code to write or debug. Second, model sovereignty: every design decision (context clearing, flat tool calls, per-section scoping, fan-out to small models) is chosen to make mid-size open-weight models reliable, so the whole stack runs on your own hardware at roughly 1/100th of frontier API cost. Third, integrity: because subagent prompts are shipped verbatim from named sections rather than paraphrased by the model, what you test is what runs.

The recommendation is to build it. Confidence: high. The individual mechanisms are all established practice; the specific composition is novel and no existing system provides it.

Prior art and rejected alternatives (compressed): seven distinguishing features - markdown-as-program, LLM-as-executor, context-clearing goto, tool-call state accumulation, verbatim subagent dispatch by section reference, embedded per-section Lua, tiny generic runtime. No surveyed system combines all seven. Closest matches and what each lacks: Agentflow (clean context boundaries between phases, but inline JavaScript, no tool-call state store, no goto, no subagent dispatch by reference); AIPack (embeds Lua in markdown pipelines, but Lua is map-reduce over fixed stages and the engine, not the LLM, executes the pipeline); Playbooks ("LLM as CPU" with a program counter, but compiled to an intermediate representation - lesson taken: do not put a compilation step between the prompt author and the model; the raw markdown is the program); StateFlow (LLM task-solving as a state machine, but no context wipe between states); Reflexion (register-wipe/memory-keep split, but the reset is for task retries, not pipeline progression); Haystack State (centralized tool-written store, but not persisted across context-clearing transitions).

The four primitives (kept): everything reduces to Parse (markdown into a section map; H2s are addressable sections, H3s are fannable children, `## Main` is the entry point), Configure (a section's optional Lua block exposes five host objects - `state` read-only, `store` query/count, `tools` add/remove, `params`, `context` injection; preconditions run before the model, postconditions after `done()`), Execute (a section is a tool-call loop over a fresh context until `done()` or budget), and Dispatch (resolve a tool name to a function, validate flat arguments, return a short result string). Every other feature - goto, Task, fanout, virtual files, ask_user, model tiering, postconditions, self-extending pipelines - is a composition of these four.

[Dropped: mermaid architecture diagram, runtime line-count estimates, document roadmap.]

### c:\Users\Vinnie\src\cursor\wg21-paperflow\promptforge-transcript.md (two drafts)

[pasted: two drafts of a design-session transcript artifact covering the compaction algorithm, Mentograph model-tiering and distillation economics, and the orchestrator idea. The second draft restyles user turns as blockquotes and drops the "### Assistant" headers per p59-p60. The user turns duplicate the Prompts section above; the assistant exposition's rationale is superseded by the plan and promptforge.md summaries kept above.]

### c:\Users\Vinnie\src\cursor\promptforge-design\example-diligence.md

Simplified Diligence written in PromptForge as a teaching example; every idiom of the language appears at least once. Kept: the idiom index and the frontmatter (the YAML key set per p82). Section bodies dropped.

Idiom index:
- frontmatter: name/description/version/args/tools/default_return
- {{ args.x }} substitution in prose
- ## Main entry point
- fall-through between H2 sections (no explicit exit)
- Lua block: model(), tools.add()
- virtual files: create_file / append_file / read_file
- counters: increment / get_count
- state collection: add_breadcrumb (declared as a tool, filed by the model)
- store queries in Lua: store.count, store.filter, store.group_by
- fan-out over ### children: sections.children + call("fanout", ...)
- subagent dispatch: call("task", "## Section", {...})
- the return fence: call("return", ...) ends the run
- task-target sections sit BELOW the fence, unreachable by fall-through
- preconditions: top-level assert
- postconditions: function check()
- json.encode for a structured return value

Frontmatter keys: name, description, version, args (JSON-schema object with properties/required), tools (list mixing canonical extension tools, core virtual-filesystem and counter tools, and prompt-declared state-collection tools), default_return.

Section layout: Main, Industry, Diagnose, Challenge, Couple, Synthesize, Report (return fence), then below the fence the task targets: Test Battery with individually fannable H3 children (Credential Depth, Staffing Model, Financial Viability) and Company.

### c:\Users\Vinnie\src\cursor\promptforge-design\design-plans.md

[Dropped: plan file link inventory.]


