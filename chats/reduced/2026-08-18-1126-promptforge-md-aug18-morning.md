# Promptforge.md session, Aug 18 morning

*2026-08-18 11:26 - transcript 5dba64ef-41e7-4bfb-a77e-6e3e0f5f2f87*



## Prompts



**[p5]** [troubleshooting: debug the gateway directly with curl; enumerate all gateway URLs and operations; user frustrated with the process]

**[p15]** [testing: run the gateway and show the whole battery of tests]

**[p21]** [troubleshooting: the watcher will not pick up new prompts]

**[p23]** on Windows I dont want polling I want a native directory watcher that works through IOCP

**[p24]** [troubleshooting: how to avoid WSL completely; why Git Bash routes through WSL]

**[p26]** [pasted: explanation that Git Bash and WSL are separate environments; Windows PATH conflict with C:\Windows\System32\bash.exe shadowing Git Bash; fixes via absolute paths, PATH reordering, IDE terminal settings, ~40 lines]

**[p27]** [troubleshooting: user reordered PATH entries and relaunched; recheck]

**[p29]** the mcp server is supposed to return the contents of the output file so it can be displayed in the chat when an output file is not specified

**[p30]** it is supposed to appear in the chat

**[p31]** there's a double output. it shows the chat reply and then shows the "contents" of report.md

**[p32]** who wrote "--- output: report.md ---" ? where is that code

**[p33]** [debugging: output link not clickable; location is runner.rs; newline not rendering correctly in the mcp call box]

**[p38]** but why, this is unintuitive that you need an extra newline. newlines are supposed to work.

**[p39]** I feel like If there's a If the pr if the prompt forge prompt only has one output file. And the invocation doesn't map it to a real file, then that should be the only output. We shouldn't, shouldn't say, we shouldn't put the three dashes, we shouldn't put the name of it, of the file, we should just only, just have the contents.

**[p43]** Question Now I have the sections. How do I fan out? I wanna fan out, I want each fan leg to have its own section, but I don't have these items in a list. How do I inject it? Do I use Lua and like extract each line? Do I use like a pattern match and like put together like an array, like what do I do?

**[p44]** And we're gonna need to update this thing. We need a new feature. So I think, I think Fanout. This just doesn't right. Show me what the fanout API looks like right now.

**[p45]** Let's explore. I, I think this needs to change. I think what is the most fundamental operation of FanOut? I would say that it is It's executing a set of operations in parallel. And that's it. So, but what's an operation? An operation has to be a section. Because we're gonna, it needs tools, so it needs to have a Lua opener, and then it probably wants to do inference, of course, or else we would have just executed Lua to begin with. We don't need, we don't need the parallelism if it's only Lua. So, in other words, it, it has to be a section. We need a section. But then. Yeah, I think we need, it has to be a section. It has to be a section, okay. And then To get the parallelism. We have to inject. Something in there. Make it different. And that's the item. And That's what the second parameter is for. We have a section that has a list. And that gives us the different items. But In lua, we need a better way to do this. We have to allow that second parameter to be. An array. And then, in order to restore the functionality that we're gonna lose, then we need like a function that takes the section name. As a parameter, and it returns an array which is the bullet, which is the numbered list that's in that section. What do you think about that?

**[p47]** Question for you, what's this open tool scope? Like the code talks about the tool scope being open, closed, and all that, and like now that we allow for multiple sections, that aren't we just holding the tool scope open the whole time? Is this just don't tell me this is just for the epilogue. That would be a big waste of having all that code just to keep just so that we could close it right before the end?

**[p48]** I'm confused, you say the set can't change mid-conversation, but we're running prose, how could the set change anyway? The set can only change from Lua. So Closing the tool scope doesn't make any sense.

**[p49]** Seems like a lot of tryhard. To protect against such a trivial case, how much code is involved in the scope opening and closing? Like if we were to remove it, how much would we clean up?

**[p50]** You mean the tool schema sent to the model would silently not match? That's not true. What would it not match?

**[p51]** Instead of We have to move the code that That sends the schema. Do we have to when we, when we compute the schema to send to the model, we just have to move that out of closed scopes, we'll just put it in a function, calculate tools, and then we call that, and then that's what we pass to the model.

**[p52]** Wait a minute. Can we do something like, can we just replace the add function in the tool table? As a, if we want the error, like we don't have to do all this close scopes business, we can just replace, we can, if, if we know that we're in the last Lua block, then we just zap out the, the members of the tool struct that would be destructive.

**[p53]** It sounds to me. Like. Well, first of all, I like the error. I prefer an error over nil. I think. Would nil also generate an error?

**[p54]** No, no, no. It's No, no, no, we're better off with nil because there's less code. The less code we have to maintain, the better. The user still gets the file and line number, and then it'll, it'll, that's enough to know. Like when they see that that file, when they see that there's a, a tool operation in the error log, they'll know. We don't need to go out of our way to, to, to tell them. As long as we put a file and line number, that's the rule. For all errors, there has to be a file and line in, that corresponds to the prompt. So, I'm thinking that, yes, this sounds actually quite good. Is there anything else that we do with these, with these scopes being opened and closed? Is it only the tools?

**[p55]** You say first prose block. No, that's not right. It's not the first prose block, it's It's the setup of the last lua block.

**[p56]** What I'm saying is this. In the epilogue. Before we run the epilogue code, we zap the tables. And the most logical way to do that is after the last prose block runs. Then before we execute the Lua, we manipulate the table, so we have one function to zap the environment, and it'll, it'll nil out the model. And it'll null out the tools. Tables.

**[p57]** Keep saying before pros, it was false. When, when is that the case? To me this is what an H2 looks like:

**[p58]** - lua prologue
- prose
- lua
- prose
- lua
- prose
- lua epilog

**[p59]** we want to zap the model/tools tables just before running "lua epilog"

**[p60]** checking if a prose block follows, this is a good criteria actually. if there's no prose block that follows, then tools.add would be useless

**[p62]** model can only be set once in a section, and always only allowed in the prologue, and once model.need is called then a subsequent call should fail. can we set the model.need=nil?

**[p63]** [discussion: is raw_set to nil the same as deleting the key; setting a table entry to nil releases the key]

**[p66]** Hey, I see a little problem here, because if, if we do model dot always in the pro in the preamble, then now we have a default. And it applies to every subheading, but now for subheading does model dot Use, now it's overriding the default. But it's on I feel like maybe this isn't the right thing to do. Maybe consider evaluate this new API in the preamble if we call always, then we've permanently foreclosed being able to use. Different models in any subheading, so we never allow them in the table. So you have to make a choice: either you use the same model for the entire prompt or you specify the model every single time in the subhead. You

**[p67]** if there's no model.always, then failure to select a model before the first prose or call to model::inference produces an error

**[p68]** I just realized. The user can call model::inference() from the epilog.

**[p69]** Right but the point is that a call to model::infer would make the epilog no longer "a lua block with no prose that follows"

**[p70]** ```lua
x
model::infer(y)
y
```

**[p71]** must always be equivalent to:

**[p72]** ```lua
x
```

**[p73]** {{ y }}

**[p74]** ```lua
z
```

**[p75]** This is a core design principle. These are equivalent. This way there is never any misunderstanding about what does what. this means the "epilog" is the lua code that is not followed by any call to model::infer or prose.

**[p76]** do we still need ToolBag

**[p80]** we should rename model.always to models.only

**[p87]** fanout() is also like infer()

**[p94]** Okay, I wanna talk about the fan out. There's a couple of cases that we need to cover. One is when we want to fan out. Multiple prompts. But what if we just want to do two steps at the same time, and they each have their own section? How's that handled?

**[p95]** Here's the problem that I have What we're asking the model to do is, we're asking it to identify all the sections in the paper, and then we're gonna fan out on each section. But in order to extract the text, we need to take the line number range, and we need to read it from the file. The problem is, if we have the model use output tokens for that, then we're wasting output tokens, and then it, it can paraphrase. We don't want that. So what we wanna do is, we wanna have We want the model to identify the line number ranges, but then we want a deter-deterministic way of taking those line number ranges and putting it into files in the store. So there's a, there's an impedance mismatch here with the transition from From the, from the model to the Lua, and the transition from the Lua to the model, this has resistance. So my idea is this: instead of asking the model to just output a bulleted list Of sections and their line numbers, how about if we offer a custom tool on the spot, like a tool that's backed by just a Lua function, and then we ask the model to call the tool, and the tool has just, really just two parameters, the starting line and the ending line? How easy is that? @promptforge/local/prompts/papergate.md:28-31

**[p96]** Well, I wanna talk about it. What I wanna know is, can a three billion parameter model reliably call this tool? And we're not using PyDantic, so do we need, like, what if the tool what if the tool call fails? and another thing, I don't wanna have to go through ten or fifteen completions. I don't ha I don't wanna have to wait once for each section. I want the tool to be asynchronous. I want the model to emit a tool call for each section. All at once, like if there's twelve sections in the document, then issue twelve tool calls, and then, and then the model's done, and then the LWO will, will collect all those tool calls and execute them, and then, and then we'll get those results. Like it'll be, like we'll have a rendezvous until all the tool calls are done. What do you think about that?

**[p97]** But are you sure about that? Because check the code, do do we handle a model issuing multiple tool calls? That doesn't make sense. What happens if one of the tool calls is a goto? Or a jump. I don't understand. Or what if one of the tool calls is like. Like a fan out? How can that work?

**[p98]** What about, like, WebFetch and WebSearch? The model's gonna give more than one call? Like, can a model do multiple web searches at once? Is that what it's doing? I don't know if I, how I feel about that. They should do one at a time. How do what, what are the, what are the checks and balances there?

**[p99]** Hey, let's, let's plan the feature. So the feature is this, the feature is you can add a tool, and then it's backed by a Lua function, either a closure, inlined into the Call site or calling a named function that's local to the chunk. What do you think about that?

**[p100]** My thinking is this. If you want If you want to make a tool, if you want to make a local tool be globally available, then you put the function in the shared Lua, which is the last section of the h1, and then, or, or it's marked shared, and then you just, every, every section has to register it.

**[p102]** Question is this. I wanna, so the tool is gonna collect the It's gonna collect the sections, I mean, it doesn't have to inject in the store, it could just accumulate in a table. And then And then after the prose executes, then the next lua chunk will look at the table. So how do we create that variable? Can we have a variable in the first Lua chunk and then the function adds it, that becomes the table that the function uses, and then in the second Lua chunk we inspect it? And then we do the fan out based on that.

**[p103]** the VM is the same for the whole H2 so can't we just use

**[p104]** sections = {}

**[p105]** if we wanted them as numbered files in the store, i.e. "chunk-1.md", "chunk-2.md" how would that look

**[p106]** seems wasteful to duplicate the string

**[p107]** I mean the string of the section

**[p108]** fanout takes a list of store paths?

**[p109]** What if I wanted each item to be a string like "startLine=50, endLine=80"

**[p110]** I'm just thinking out loud here. So, for example, okay, we have, so first, we have the problem of, of injection, prompt injection, because this is from a paper, which is an untrusted source, and then we have the problem that the, there's gonna be line numbers potentially or not. Like, if it's just, if we just have a plain string with the line numbers stripped out, then the fan-out arm isn't gonna know how to map those lines to the original file. And then if we ever wanna attach like line numbers as evidence, then we can't do that anymore. So I'm just trying to think about I'm just trying to think of all the ways that, that we can pass the data. to the, to the fan out children and try to get, do what we want. It's, it's kinda complicated.

**[p111]** I mean, I still wanna, no, I wanna, I want the plan to be a good chunk of functionality. I want the plan to be enough to get me past the next chunk of functionality, because just having the local tool isn't really gonna get me anywhere. So, consider this: what if the fan-out child just gets the line numbers and it has to do a tool call? It's given a tool. And it does a toll call, and it asks for those, that line range. Then! But that's no good either, because what if we, we, we should, we probably wanna do that from the Lua, but we can't because we don't have integers. The Lua wants to see integers. We don't have any way of passing like structured data unless it's in the var. The var can have numbers, right? But wait. You can't use the var. Because Devor is a copy, we just isn't isn't Devor a copy of everything?

**[p112]** We're talking, when we do the fan out though, we'll have to make a copy of item. Right? So We set up item to be the table which has everything for all the arms, and then we index it by the arm's ID.

**[p114]** Yes, I want a fresh plan. And I want the tool, I just want the tools dot local.

**[p117]** Okay, we're, we're looking at the local tool plan. What do you mean no schema? We can't, we can't do no schema. Of course we need a schema. We have to pick the parameter types out of the function declaration.

**[p118]** Wow. What would be, which pattern would be easiest for small models to stay aligned with? Like, what do we, what do we want to give the small model?

**[p119]** Question, is there debug info in Lua? Can the can the execution model extract the names of the local variables at least? Or, sorry, the names of the function arguments? Can I get the names of the function arguments? And then maybe I can just have one string, a comma delimited string of types like this:
"string, integer, integer"

**[p120]** table approach. update the plan

**[p121]** Question, is there any other metadata that we might wanna set on the tool? Like, we might wanna indicate whether it can run asynchronously, or is there a way to set an extended description, or is there a way to annotate each parameter more? And would that help?

**[p123]** Ian Question, we don't have any problems, do we? So, do we have to worry about fan out and what happens inside that function? Like, what if the function itself does inference? What if the function tries to do a fan out? What if the function does calls infer, or execute, or jump? Can, can the function call jump?

**[p124]** I'm curious though, you say the tool loop runs Between the law blocks. But why do we do that? Why do we We don't, we shouldn't need that. Like, why, why don't we just set things up once on the entry into the H2 and then leave things alone? Why, why Why do we have a tool loop that changes state? Why do we remove things from the environment? That doesn't make any sense. Show me the code that does that. Show me the file and line.

**[p125]** And you say each block re-installs fresh closures, but no, are we talking about an H2 block or are we talking about a Lua block? Because the two are different things. Like. All the Lua Chunks in the same h two are supposed to share a one vm.

**[p126]** When you say the closures, you mean functions like tools dot add. What do you mean by the closures?

**[p127]** I don't understand, I don't understand why we need to do that. When we create, but each chunk has its own, but a chunk shares the VM. So if I've got two chunks, right, let's say I've got lua pros, lua pros, lua, three chunks. Each of those chunks shares the same VM. Like last reply is just a string. You, you can, we can just set it anytime we want, as long as we're in the lua section. And then in terms of jump, we only need that once. Why would we need it more than once? I don't understand this. They're all just globals to the VM.

**[p129]** yes and help me understand what this "execute reads reply from a live global or an Arc<Mutex<Option<String>>> instead of capturing it" means. As far as I'm concerned, `reply` should be a global in the vm

**[p131]** okay but the Rust function that implements `execute` gets access to the Lua's vm so can't it just read the value of reply at the time execute() is called?

**[p132]** Now I wonder if the section spawned by execute() should even get `reply`. Maybe it should be nil

**[p133]** Yes I think this is the right call. `reply` is kind of meaningless in the context of calling execute(). What if the previous operation was a fanout() ?

**[p134]** [directive: when the plan executes, audit every function in each touched file and remove whatever is not truly needed, e.g. the jump slot poison/mutex machinery, but only after thorough analysis]

**[p138]** Also, I dont see a point to restricting things like fanout() just beause a section has no child headings. this is try-hard. its pointless. it is also wrong, in the case where fanout can accept an array

**[p139]** so for the shared library lua, that chunks is "replayed" into each h2 ?

**[p144]** tools.local needs to be invocable from any lua chunk in an H2 and it should just add the tool for the next prose call

**[p145]** tools.add between prose being a no-op means insufficient test coverage or else we would have caught it

**[p149]** I'm confused. An error in a chunk should stop the whole prompt

**[p152]** I dont care about observation labels. the observer can just observe the section itself. no need for the granularity

**[p153]** log() should be available to any lua chunk

**[p154]** why do we build the tool scope at all? why not build the schema right before running any prose?

**[p156]** Is 2. A sentinel ToolId reasonable? how much debt would we be adding

**[p158]** And Question You notice how, like in this whole conversation, it's been like me discovering that the way that the code works is a little bit unexpected, right? It's like different than how I expected it to work, and we find out little things that have gone stale, we're finding things that no longer hold up based on the changes that we wanna make, or we're finding some stuff that's redundant. My question to you is this, how can I develop a prompt for the model? That will find all that stuff. Like just a general code cleanup, like refactor to make it tighter, remove things that aren't needed. I mean, this seems like a hard problem. Let me show you, let me show you some analysis, and you tell me if it falls into that case. @tools-public/lessons/fan-out-problem-ai-as-critic.md

**[p160]** Oh, by the way, we have a problem with the tool, and what I'm realizing is this: a Lua tool should have all the same capabilities as A regular tool, a native Rust tool. And so for example, it should be possible for Lua to install the task tool, in other words, a tool call that spawns a subagent, runs a prompt, and then returns the result to the Lua or the orchestrator, which could be an LLM. But we can't do that, can we? Are we allowed to call execute from inside the tool function, from a Lua tool function? Can we call fan out?

**[p162]** Let's just remove jump, and I think, so I wanna update the plan. I wanna, when, when we remove jump, I want you to put a nice comment there explaining why, so that we don't have to relearn this over and over again. And just, put like just three or four sentences worth of analysis, it's worth it. A couple of, a few sentences now will save us a headache later. Like, put into that comment what an LLM with a fresh context would like to know, if it makes a change in that area, okay? So now I wanna talk about So I wanna talk about model infer, and I wanna talk about fan out, and I wanna talk about execute. So when we call execute, we have a section as context, but when we call infer, does infer get any tools? I don't think it should. Can you check the code? Of course, fanout can get tools because it's getting a section, and sections can have Lua, and Lua installs tools. And then, as far as jump from a handler, no, you can't jump. But you should be able to jump inside the, the Lua that's inside execute. So if we call execute with the section, that section can jump, right? It can be a long chain. And think about how powerful this is, right? Like We can create a tool, we can create a Lua tool that reads variables from the environment like line numbers, IDs, deterministic strings, and then we can do we can make a quick call to infer to do the inference, and then we can take that, we can extract that, and then we can combine it with the deterministic inputs, and then we can return that string. That's a powerful tool call. That's like a custom agent. That's like an agent that does one thing. It combines deterministic Lua data with a one, one or two shot inference. That's the most like, that's the most powerful operation you can do. You get the best of both, you get the determinism of Lua, and then you get the power of inference.

**[p163]** what kind of nonsense question about jump() is this? Lua needs to jump local tool handlers cannot.

**[p164]** I guess my question is. Do we want, should infer start from a fresh context? And can should you be able to specify the model? 'Cause I can see a use case for doing Infer and then choosing the model, like maybe you just want like a little three billion parameter model real quick, get something quick instead of the full expense of, you know, a frontier model. Maybe you just wanna understand a sentence. Like I can see that'd be That's kind of why I have Infer. Infer was never intended to just be a perfect substitute for Prose. If you want Prose, use Prose. If you want to just do a quick inference inline as, you know, as part of some calculation, then you do that. Search the codebase for any evidence of the design objectives for this. And also, I want your analysis. Tell me what you think. Pros and cons. What do you think of having Infer be fresh context, choice of model, no tools?

**[p165]** So one of the design principles of Prompt, PromptForge is that we never, we don't have features that let you do the same thing just a different way. So that means Prose is Prose. That means Infer has to be different. We don't wanna have Infer just be another version of Prose, because then we have all the same problems. How do you set the tools? How do What happens if you jump? Like, that's a pain. No, I think, I think Infer should be strictly fresh context, and it's a blocking call, and a string goes in and a string comes out. That's it. String in, string out, no tool call. I think that's the right, I think that's the right call. And Yeah, and it shouldn't share the conversation history, it shouldn't set last reply, and I think there should be model infer should have a two-parameter version where you take the model ID and then you have the string. Oh, yeah, and then you have the input, so I guess three parameters. Yeah, you always, the, the, the, the, the string is required. Of course. Oh, 'cause that's just the prompt. Yeah. Okay, so, yeah, there's just the prompt. So infer just takes two parameters, the model and the prompt. Or if you call it with one parameter, you get the current model, the one that's being used by the block. And I, I think your syntax is interesting where you say like tools you say models dot need. You wanna do that? I think But I'm not sure that works, I thought models had to be chosen in the h1. I, I, is, is, is a prompt allowed to just call models dot need? Anywhere?

**[p166]** "this requires the prompt to pre-declare every model it might want to use" Yes

**[p167]** I'm having second thoughts about models.only.

**[p168]** So one of the design principles of PromptForge is that we want every command has to be, should be flexible, it should be able to be multi-purpose and serve duty, and from a small set of primitives, we wanna give the user maximum possibilities. And but another design principle is that we also wanna be we want the user to be able to be brief, we don't wanna be overly verbose. And models dot only, it kinda sucks because I think we should go back to how it was. There's a way to set the default, and then you can override the model per section. That makes more sense because then, like, if you only have one or two exceptions, now you can, you can use models dot, you know, default and That, that seems nicer to me. So I would probably say I want to replace models dot only with models dot default. It doesn't make sense. So if someone wants to do an infer in just one place using a smaller model, now they're forced to call models dot m-m

**[p172]** what does models.use return

**[p173]** can we return a model handle or would that require serializing the model table

**[p174]** Right, so yes, we should return the handle from use, and also, anywhere that we take a model ID, we should allow a model object, of course. So infer should be able to take the model in the first parameter. I don't understand what model:infer is.

**[p175]** So it should be an error to do any inference before setting. It should be an error to do any prose or infer without specifying a model until you call use. So in practical terms, models dot use can only be called in the first Lua block of a section. And the only way to have a section that contains only pros is if you have a model default. This all should be tested, by the way. Every, all these combinations need tests.

**[p176]** You don't have to code this explicitly:

**[p177]** models.use can only be called in the first Lua block of a section. After that, the model is locked for the section. This is a new constraint.

**[p178]** it just naturally falls out of the rules

**[p179]** I don't like switching models because switching a model in the middle of a block has consequences for the KV cache. Because think about it, now we have a prefix, we have a common prefix of prompt, and now we're gonna switch models, that could be going that could be going to a completely different provider, and then, and that's not visible to the programmer, right? Like it's, I don't I just don't think it's friendly. If you wanna switch models, you go to a different H2. If you wanna preserve context, then you pass it forward in the reply.

**[p182]** we need models.get(id). and we need to keep model:infer obviously. Let's ditch the 2-arg infer() and make models.infer always use the model selected for the H2

**[p183]** is there a difference between quick:infer and quick.infer? and what do you think of this change?

**[p187]** Are we gonna allow jump from Lua tool handlers?

**[p188]** what if the prompt has two sections:

**[p189]** ## Gate A

**[p190]** ## Gate B

**[p191]** And I want to install a Lua tool handler which lets the model choose gate a or gate by, and the tool implements this choice by calling jump()?

**[p192]** the epilog would work today

**[p194]** @promptforge/local/prompts/papergate.md:26-28 add the tool, make it record each call into the `sections` variable

**[p195]** @promptforge/local/prompts/papergate.md:31 would sections:insert also work

**[p196]** @promptforge/local/prompts/papergate.md:30 is there a way specify that the function takes 3 args?

**[p197]** @promptforge/local/prompts/papergate.md:44 modify the prose to call the tool

**[p198]** would it be nicer to not name the tool and just talk about behavior

**[p200]** @promptforge/local/prompts/papergate.md:47-48 now modify this so it writes the contents of `sections` as a bulleted list of section names with the line number range in parenthesis at the end



## Plans

### fanout-scope-refactor

*Three changes to promptforge: (1) fanout() accepts a Lua array as second arg + new items() function, (2) replace ToolPhase/ModelRuntime scope lifecycle with a freeze_declarations() that nils mutating table entries before Lua blocks with no following prose, (3) extract_output already fixed (clean output without separator).*

**Goal (fanout array):** `fanout(worker, items)` where `items` is either a section heading string (current) or a Lua array of strings (new). New `items(heading)` function extracts pre-parsed bullet items from a list section.

**Goal (scope lifecycle):** Remove `ToolPhase`, `ModelRuntime` open/closed state, `ClosedScopes`, all scope open/close functions, and all scope-related observer events. Replace with a single `freeze_declarations()` function called before any Lua block that has no following prose block. Schema computation moves out of the closed-scope path into a snapshot function that reads bindings without closing.

[step lists, file-path inventories, code sketches, and test plans dropped]

### tools-local

*Add tools.local(alias, description, handler) to promptforge - a Lua-backed tool that the model can call during inference. The handler is a Lua function that receives args as a table and returns a string.*

`tools.local(alias, description, handler)` declares a tool backed by a Lua function. When the model calls this tool during inference, the tool loop invokes the Lua handler instead of an external service. The handler receives `args` as a Lua table (whatever JSON the model passed) and returns a string (the tool result the model sees).

```lua
tools.local("extract_section", "Extract a range of lines from the paper", function(args)
    -- args is whatever the model passes as JSON, deserialized to a Lua table
    local content = store.read_lines("paper.md")
    -- slice from args.start_line to args.end_line
    store.write("sections/" .. args.name .. ".md", sliced)
    return "stored " .. args.name
end)
```

- Called from any Lua block (H1 or H2 prologue)
- The tool is immediately available to the model (no separate `tools.add` needed - `tools.local` both declares and scopes it)
- Handler defined in `lua shared` can be referenced by name from any section
- Handler has access to the section's `store` and globals (same VM)
- Handler returns a string; errors propagate as tool-call failures

Design decisions:

- **No schema (later reversed in discussion, see [p117]):** The model sees only `{name, description}` with no `parameters` object. This keeps the API simple. The model figures out what to pass from the prompt context.
- **Trusted output:** Local tool output is trusted (no nonce wrapping) since the prompt author wrote the handler. This matches the trust model - the prompt is trusted, external data is not.
- **Same VM:** The handler runs in the section VM that declared it, so it shares globals, store handle, and upvalues. This is what makes the accumulator pattern work.
- **Sequential dispatch:** Multiple local tool calls in one response execute sequentially in the for loop, same as external tools. Fine for store operations.

Rationale for the approach: local tools can't go through `ToolRegistry` in the normal way because they don't exist at H1 resolution time (their handler is a Lua closure tied to a specific VM), the handler needs access to the section VM's state (store, globals), and they are per-section, not global. A local tool is NOT a `dyn Tool` in the registry: the handler is stored in a per-VM local-tools table, included in schema building alongside registry tools, and dispatched in the tool loop before the registry lookup.

[step lists, file-path inventories, and test plans dropped]
