# Compaction algorithm session, large

*2026-07-30 10:46 - transcript e0e75624-f18d-4c1c-938c-edc40bfd7e79*



*Prompts p63-p133 of 397. Part 2 of 5. The Plans and Design Documents sections are in part 5.*



## Prompts



**[p63]** now create a new plan which is a duplicate of this plan but without any of the talktron or context compaction

**[p64]** go through this design doc @promptforge-design/design/design-promptforge.md and give me a numbered list of features

**[p65]** I wanna keep talking about it, so now I'm thinking, so now I'm thinking that the basic unit of operation is the function. Basically, it's a inference and a function, the return value is a string. It's just a string and the inputs are-is a structured input key value pair, I guess and Every prompt, for each prompt, is a function. You pass in parameters and it returns a string, but it can have side effects. Okay, now. Every section heading. Is also A function. But It returns a string, but it can only take a string. And the string that it takes is defined by the node that transfers control over to it. So for example, if you're in a section and then we do a go-to. Well, we have to, we pass a string. We have to pa we can pass an optional string. And the goto is actually, there's, there's only gonna be one tool for transferring control. And we can make it, let's say that it's ca we'll give it the name call. And the first parameter to call is the type of call. It's a goto? It's a Function? It's Context preserving goto maybe, I don't know, but, you know, there's a type. or, or it could even be a return. Maybe, maybe it's also a return, but it takes a string. And that string is passed to the destination. And if the destination is a node, then that becomes the beginning of the prompt, like that gets, that gets injected, or it can go to the Lua, and then the Lua can like manipulate it, something. What do you think about that?

**[p66]** So the model has to be able to route, because what we, we, we wanna let the model orchestrate sometimes, like when it really has to make a decision, we need to let it route. Like the, the model spawns the task. For example, if it's doing a guided web search, we can't do that in Lua. It has to do a web search, and then it has to pick, and then it has to choose the page, it has to look at the page, then it has to keep making decisions, the multi-turn decision making. And so we need both. We need call from Lua And we need call from the model, like that's where the power is. But also, I think we need a substitution syntax. Like there has to be some kind of syntax where that means that in the prompt, the, the harness, the, the, the pro-prompt forge executor has to perform a substitution from a Lua variable. So in Lua, there's a state, and every element, it's a, it's a table, and each element has a name, and then you can, you can quote the state as a substitution in the prompt And that gives you determinism.

**[p67]** how do we handle all the corner cases and quoting rules to do the substitution of {{ }}

**[p68]** we are doing this in Rust

**[p69]** just implementation and you will need to update the plan at some point.

**[p70]** My question, my question is, how do I do the substitution? Do I, do I compile the text with Lua and that gives me like, what, a fragment? What's the name of it in Lua? what do they call it?

**[p71]** So the user can't declare arbitrary globals, there's only a fixed number of objects that they can access.

**[p72]** Spawn a subagent and update the plan. And make it Lua instead of Python, go through, rewrite the whole thing, and I want a table towards the top. The list of objects, a list of functions, and then for each object and each function separately, I want to explain like what it is. I want dense enumeration of all the features that we've talked about towards the top so that I can review it. I want the plan to read like an inverted pyramid, and I want an executive summary at the top. But I want you to do this in a subagent, the subagent can reference this chat by its full path so that we can keep talking. And you won't try to update the plan until that sub-agent is done, so we can talk. And when the sub-agent is done, then your restriction on changing the plan from the main context will be lifted. Are we clear?

**[p73]** Okay, so I think we need to think it through. Like what are the subheadings? So if i have an h two Basically, main is a function that takes key value pairs and returns a string. Well, it doesn't need to return a string. Like It can, but if The primary from a different subhead than that one  is responsible for returning the stinrg.

**[p74]** Actually, I think, I think every section can see the key value inputs to the prompt, and they're read-only, I think. Maybe, I don't know, but any, any piece of Lua anywhere in the prompt should be able to access the, the parameters. So, so if there's a file name and we wanna have, like, every section does something to the file, we wanna, we want them to be able to go from section to section accessing that value, we don't wanna have to pass it around.

**[p75]** In light of this. Basically, because this is kind of biased towards implementing pipelines, then I think on an H2 you run it, and if it falls through, then you just go to the next H2. And, but that has to be context clearing. That's the equivalent of "go to" and then the next section. And then you keep doing that, and if you run off the end, then the prompt ends and it, there's like a default message that says, "Okay, it's done. And If You can specify that string in the yaml. If you want to override it, or if you don't specify it in the YAML, then the ex-the executor gives a default. So it's always well-defined, and it keeps your prompt short if you're, if it's the simple case, like if, let's say you have three steps, and you're gonna process a file, each step accesses the path, it does its thing, it starts in a fresh context, it accumulates state, and then it's done.

**[p76]** instead of params what do you think of args

**[p77]** So are these args, are they just always strings? What if there's a table? What if the lua code puts a table there? What if there's a floating point number there? What if there's a, I don't know, an object? I don't know. What are the top possible Lua things?

**[p78]** Why can't we use turn? Why can't JSON? Why can't we use JSON? That's elegant. Then the Lua can assemble a JSON object and then The LLM can return it using a macro substitution. That's like pedantic, that's pydantic with perfect return and no overhead.

**[p79]** And I would go one step farther, I wouldn't even use Jason, I would say. I would make, I would say tool call, instead of call, make it say tool call, and tool call will. Under the hood, structure the data, structure the table however the model thinks it's best, or however the harness thinks it's best. Is there, is there a utility there? Like, what if someone wants to use, like, there's this other form of JSON that's like more compact? You know what I'm talking about? Then we could do that under the hood.

**[p80]** That's Yeah.

**[p81]** Find a sub agent and update the plan for the new stuff, just like we did.

**[p82]** The, the plan needs to show the YAML. Or is, yeah, the YAML front matter, like what are all the keys? Should, tell me now.

**[p83]** The state tool? What is that?

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

**[p97]** spawn a subagent and look at  @wg21-paperflow/packages/assay

**[p98]** spawn a subagent asynchronously have a look at @tools-public/tools/staker.md 
also spawn another subagent async and have a look at @tools-public/tools/diligence.md 
and do the same for @tools-public/tools/code/boost-review.md

**[p99]** also spawn an async subagent for @tools-public/tools-wg21/papergate.md

**[p100]** This can't be right. What about the "breadcrumbs?" That's structured data!!

**[p101]** show me exactly the diligence dataflow

**[p102]** make up a promptgate diligence prompt. it doesn't have to be perfect just capture each idiom. not the whole tool. this is a simplified prompt to understand. write to @promptforge-design

**[p103]** @promptforge-design/example-diligence.md:62 wtf is this?

**[p104]** spawn a subagent update the plan for what we learned @c:\Users\Vinnie\.cursor\plans\orchestrator_design_document_165f20dc.plan.md

**[p105]** link promptforge_orchestrator_only.plan.md. for me

**[p106]** it won't open.

**[p107]** what are the dates on those

**[p108]** can you please link promptforge_orchestrator_only.plan.md  for me

**[p109]** its becaose of windows paths

**[p110]** No I got it open finally.

**[p111]** @c:\Users\Vinnie\.cursor\plans\promptforge_orchestrator_only.plan.md

**[p112]** @promptforge-design make a markdown file with a working file:/// link to the plan in it - design-plans.md

**[p113]** what is relevant in here to the plan

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

**[p124]** Okay, so I guess we need a minimal prompt forge? And then we need We need a A gateway. That's it. But don't, shouldn't we really I don't know. Really put it all in one plan? Look at this gate, look at what i have for the gateway.@promptforge-design/design/design-gateway.md

**[p125]** what is pinning

**[p126]** I thought it was sticky to the connection

**[p127]** I thought it was using HTTP/1.1 keepalive

**[p128]** put the "New-not in the plan yet, relevant" and "refines" in an inactive part of the plan "to explore later"

**[p129]** What's the smallest thing we can implement? Can we just implement the executor and we just, and have a, a frontier model invoke it using the shell command from the command line? And it doesn't even do any inference, it'll just like, I don't know, print "Hello, world".

**[p130]** Here's my question: what kind of log should we put into the repo? Should we put like a development log? Do we just rely on the commit log? Maybe if the commit messages are rich enough, we can just look at that to see where we're at, but how do we show the what's cumulative? What do we do? How do we show like what's there so if we start over with the fresh context, the model knows what the fuck to do?

**[p131]** Like it, and then. Do you wanna make like an agents dot md or a cloud dot md at the root that says that any changes have to update this status file?

**[p132]** I dont want no mdc. rather have AGENTS.md in the repo. start a new plan plan to build in@promptforge the executor. this will be a multi-crate repo

**[p133]** do not look at the python implementation
