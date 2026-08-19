# Orchestrator Design Document plan

*2026-07-28 09:25 - transcript 7ba89fe2-1b92-4dca-b79d-08ec7cdcdaea*



## Prompts



**[p1]** what do you think of this algorithm: [pasted: Slack exchange with Will Pak introducing a transcript compaction algorithm]

**[p2]** [pasted: compaction algorithm - given a transcript of N lines, ask the model to compress the first N/2 lines in half and replace them; prepend the original prompt to every new compacted context so a summarized context always has the fresh prompt; repeat each time the transcript regrows to the limit (1000 -> 750 -> 1000), producing a fidelity gradient of double-compacted / compacted / full segments; always save the complete uncompacted lines to the database so the original conversation is reconstructible; begin compaction early (~900 of 1000 lines) so the user never waits at the limit; also floats open-weight models as an orchestration layer via an injected Task tool for spawning subagents]

**[p3]** I would use this for @tools-public/tools/mentograph.md

**[p4]** is a frontier model actually needed for interviewing? the largest open-weight models are pretty damn good and this is not a deeply analytical task

**[p5]** I was thinking more along the lines of 800B+ open-weight models

**[p6]** oh shit are you saying we could train a smaller, faster model to conduct interviews?

**[p7]** how do we get speed

**[p8]** so the hardware doesn't affect the speed?

**[p9]** what about the speech to text

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

**[p22]** after transcript compaction dump everything good we came up with for Mentograph including the background research, speech to text to speach, etc

**[p23]** Question: how do subagents return the data? as Pydantic?

**[p24]** There's a problem here. Pydantic recognizes a failure mode. How would we?

**[p25]** question: could each section have an optional code fence with user-definable Lua code to define preconditions and insert tools and what not

**[p26]** why did you fence that exposition

**[p27]** how good is Opus at writing Lua

**[p28]** the pipeline author is you LOL

**[p29]** spawn multiple subagents and search the web for prior art. and for Lua lib bindings for Python

**[p30]** is it just me, or is the Pydantic layer expensive? basically you have to route all your model calls through it, so that it can inject the guidance? or am I wrong? how is it possible that I came up with a better way?

**[p31]** 1. For triple-compacted content in Mentographist, but think about it. The older stuff gets compressed out of existence, and thats ok! we dont need the older stuff because we already captured the user's story. As long as we reinject the prompt at the beginning of the new compacted context, we are aligned. The only downside is that the model can't remember if the user repeats a story. But this is unlikely as people are not going to tell the same story over again.

**[p32]** 2. Okay tell me about multi-turn LLM interactions. The assay pipeline I believe does not do multi-turn? except for the websearch. instead assay just goes to the next step. what's the latency like on multi-turn?

**[p34]** what about a special, small model for compaction that is fine-tuned for only that?

**[p35]** the plan should spawn subagents for each of these ideas and explore existing practice

**[p36]** I mean when the plan runs it should also do research in subagents before writing

**[p37]** I would like several worked examples, each of which combines a few of the ideas together to show how they can work. and then I want one large worked example that shows everything. The resulting design document should be richly detailed enough for any frontier model to produce working code including tests

**[p38]** high end gaming video cards can support how many B parameter models comfortably (with also generous space for kv cache)?

**[p39]** update the plan and stay in plan mode asshole

**[p40]** now lets look at @tools-public/tools/briefer.md and consider how well this maps. are there any steps that would require a large number of tools? how would this work? is it ok for a tool to set multiple metadata fields, do smaller to medium size open-weight models handle that well?

**[p41]** obviously we wont be using AskQuestion in these pipelines

**[p42]** Question about the Diagnosis. Can we just use a separate subagent per test?

**[p43]** finish what you were doing with "I'll add the runtime-level user interaction pattern (not AskQuestion) and the unattended/interactive mode toggle to the plan."

**[p44]** So this is where the orchestrator gets weird. How do we specify the 53 tests? right now they are in a nice bulleted list but if we are going to do this right we need them.. each in their own section? There has to be some markdown syntax to say "this is a fanout with each spoke having its own prompt"

**[p45]** oh I love this! by putting the prompt itself in Lua as individual sections, the tool can write itself.

**[p46]** The harness needs to have an easy way to say "combine all the fanout results into a single document" with the option for preserving order, or not. And we could have "virtual files", i.e. the harness offers tools CreateFile, AppendFile, DeleteFile but these are not real files they are just in-memory blobs. The agent doesn't know any better

**[p48]** the scope is not as big as you might think. a lot of these are just specific examples of a general principle. like the tools

**[p49]** Let's take a detour for just a moment and then return back to this. What is the practicality of implementing a harness that can, for example, run something like @tools-public/tools/diligence.md without modification?

**[p50]** This is a detour - brand new architecture. how much python do we need to make this work unmodified (and what tools)

**[p51]** you are overthinking it. I am essentially asking, how do we just do what cursor does? I'm not asking to decompose based on section headings. Just pass the entire prompt to a model and say "do it"

**[p52]** and if we used Opus 4.8 Max with 1M context?

**[p53]** but we know Cursor does quite a lot for us surely it can't be that easy. Cursor handles multiple models and makes it seamless

**[p54]** okay thanks. none of that detour should affect the plan. Update the plan for what we know

**[p55]** when the plan runs I want every idea to be enriched with subagent web search, look for prior art, look for related work, look for anything that would be a subcomponent to build the idea, look for information about performance, metrics, model tier, and so on. don't write before researching and think deeply I want a fantastic report. write the report to @wg21-paperflow/promptforge.md

**[p56]** I want the transcript of this design discussion to be written to a markdown file. Leave out chain of thought. I only want the user prompts and the LLM replies and the subagent reports. Show me a one-page sample including 1 of each of thoese ellements before we commit

**[p58]** this looks like its going to fail at the end with "Edit attempted". shouldn't you be periodically checkpointing

**[p59]** start over. I want the user text to be in blockquote

**[p60]** get rid of ### Assistant and the blank line that follows

**[p64]** now create a new plan which is a duplicate of this plan but without any of the talktron or context compaction

**[p66]** Okay, I wanna talk about this whole Promptforge thing. So. What do I do with, should I have like subheadings? Should subheadings inherit the parent? And how should the flow, what should, what should the flow look like? When you finish with one subheading, should it just go to the next?

**[p67]** So my thinking is that it's like a stack. You inherit the parent. And for the fan out, I mean, that's a good question. I'm not sure what to do about the fan out. The fan-out has another problem, like what if I wanna give the same instruction five times, but I want each of them to have like an ID, like one, two, three, four, five. Like, for example, let's say I have a variable number of steps, let's say I wanna do a fan-out of N steps, and I want each of them to write a, a unique file name. How do I assign the file index? Like, how do I give each of them a unique file name? I don't know the file name ahead of time, so I can't embed it. Like, this is a real problem. I don't want the model to have to calculate the final name, we want to minimize the amount of inference.

**[p68]** I don't know, I wanna minimize the amount of Lua. I mean, I, because I think I'm concerned that it's gonna be hard for a model to compose a prompt. Like it, it feels like we're going in the direction of just implementing like a, an orchestrator in, in, in Lua, except the code is in the MD file instead. And I mean, if we start putting too much into the Lua, then it kinda defeats the purpose. Am I wrong?

**[p69]** Right. So I'm not sure that I agree with that. I mean, I When you say that Lua should be purely declarative, I don't, I don't agree with that, because why should we pay for inference in order to orchestrate? But there's two kinds of orchestration. One is deterministic orchestration, like, for example, one section goes to another, like what, what step one precedes step two. That's deterministic. But then there's another type of orchestration where the model has a decision, where it, it has a choice between step A or step B, and then it decides which one to take next based on inference. That's a different thing. That obviously stays in the pros, but for, for a fan-out problem Like, for example, let's say we have a battery of fifty tests, like we have a staker stakeholder battery of fifty tests, and we wanna apply them to an input. It makes a lot of sense to do that deterministically, like why should we waste inference having to figure that out? And then we have the problem of the drift of the prompt. But I, we, we solved that with Lua, so I wanna, I want a middle ground.

**[p70]** No, what I'm saying is this, like, yeah, I mean, your Lua function's good, and then we're doing the goto, which is the context clear, but what I'm talking about is, I'm talking about that the The model Can orchestrate without clearing its own context. So it's a like, it's a multi-turn. I wanna have multi-turn.

**[p71]** Kind of but not quite. For example, inside the prompt (not the lua)

**[p72]** 1. If the paper is a library paper, call("### Read Library Paper"), otherwise call("### Read Language Paper").
2. Look through the paper and count the number of wording sections

**[p73]** no actually I am saying that call() runs in the same context. task() runs in a subcontext. the novelty is that call() references the prompt, instead of providing it. fewer output tokens are consumed, and the context doesn't have to have both prompts in window

**[p74]** plus goto("### X")

**[p75]** you could in theory goto yourself

**[p76]** Question. Will a frontier model be able to write prompts? Like, is it gonna understand this Lua? Like, if I, if I give it like a little instruction manual with all the commands, will it understand this shit?

**[p77]** Question: Let's go through the list of items from The other design doc, the bigger design doc. Let's go through that list. I want you to go through it for each one, and I want you to categorize it. Is it very good and obviously beneficial? Is it something that me and you need to talk about? And then, or is it bad? Do it now.



## Plans

### Orchestrator Design Document

*Write a design document for a markdown-driven, model-orchestrated pipeline runtime that replaces hardcoded Python orchestration with prompt-as-program execution, covering the section/goto/tool-call architecture, composability, and (separately) the transcript compaction algorithm.*

Scope: two independent ideas - (1) the orchestrator runtime, a general-purpose Python harness that executes analysis pipelines defined entirely in markdown, replacing the pattern of hundreds of lines of per-pipeline Python glue; (2) the transcript compaction algorithm, a recursive halving strategy for long conversation contexts, a separate section with no dependency on the orchestrator. Audience: someone already proficient with the assay pipeline.

Principles and decision rationale from the plan structure:

- BLUF core insight: sections as procedures, goto as context-clearing transition, tool calls as state, markdown as program. Why it matters: new pipelines without Python, per-section model tiering, prompt-integrity guarantees.
- Three-layer architecture: runtime (generic Python, fixed), tool library (growing, shared across pipelines), pipeline documents (one markdown per pipeline, where all iteration happens).
- Section model: the markdown file is parsed into a section map with stable IDs; each section declares its model tier and tool set; `## Main` is the entry point.
- The goto primitive: destroy the current context, start fresh from the target section's prompt with only params and state-store access. This eliminates context bloat.
- Tool-call state replaces structured Pydantic output: flat argument signatures are reliable on small models, state builds incrementally via tool calls, persistence is a side effect.
- Per-section tool scoping: the section header declares its allowed tools, the runtime filters the registry, the model sees only 5-10 tools per section. Matters for accuracy and for security (capability sandbox for sections processing untrusted input).
- Verbatim section dispatch: `Task("## Extract", chunk_id=3)` resolves the section reference in Python, not the model. The model never touches the subagent's instructions. No prompt drift, no contamination. Prior art cited: the prompt rulebook's ship-verbatim and tag-reference rules.
- Model tiering: each section declares a model slot (Main orchestrates on a 400B, Extract runs on a 27B, quote verification on a 14B); the runtime resolves slots from a services config.
- Composability: Task can reference sections in the same file or external pipeline files. Nesting with isolated state stores per level. Params as explicit data flow, no shared mutable state. Safety valve: max depth plus max total tasks, configurable per pipeline.
- The Python harness (~300 lines) does: section parser, context lifecycle, goto dispatch, tool-call loop, inference client. It explicitly does NOT do: orchestration logic, prompt assembly, step ordering.
- Testing: each section is testable in isolation with known inputs. Unit of testing = unit of composition. No mock pipeline state needed.
- Prompt engineering rules applied to section authoring: six-constraint ceiling per section; decision rules instead of vague qualifiers; escape hatches for hard rules; tool descriptions with what/when/when-not/params; an observable violation test for every rule; goal + success criteria + stop condition rather than step-by-step procedures; standing-text removal test (every line in a section should change behavior).
- Migration path: not a rewrite of assay, but a proof-of-concept alongside it. Start with PaperGate (simpler, two-stage) on the new runtime; graduate to assay-equivalent if PaperGate validates the model.
- Appendix (compaction, unrelated to the orchestrator): recursive halving of the first N/2 lines; fidelity gradient (recent full-resolution, older progressively compressed); structured preamble (prompt + state) exempt from compaction; pre-compaction at 90% capacity to hide latency; full transcript preserved in database; claim-aware compression instructions for interview contexts; explicitly NOT relevant to the orchestrator, which uses goto to clear context instead of compacting it.

## Design Documents Written

### promptforge.md (design document)

BLUF (principle-bearing, kept near-verbatim): The markdown is the program, the model is the CPU, embedded Lua is the microcode, and a ~300-800 line Python harness is the instruction decoder. A pipeline is a set of named sections; the model transitions between them with a context-clearing `goto`, builds all state through flat tool calls into a persistent store, and spawns subagents by section reference so the prompt author's exact words execute without drift. Each section declares its model tier and its scoped tool set in a Lua block that also runs preconditions and postconditions. The same generic runtime runs any pipeline that is "assay-shaped", so a new pipeline is a new markdown file, not hundreds of lines of new Python.

Threefold payoff: iteration speed (a new analysis tool goes from idea to running in an hour, edited in one file, no orchestration code); model sovereignty (every design decision - context clearing, flat tool calls, per-section scoping, fan-out to small models - is chosen to make mid-size open-weight models reliable, at roughly 1/100th of frontier API cost); integrity (subagent prompts ship verbatim from named sections rather than being paraphrased by the model, so what you test is what runs). Recommendation: build it, high confidence - the mechanisms are established practice, the specific composition is novel.

Prior art and rejected alternatives: seven distinguishing features - markdown-as-program, LLM-as-executor, context-clearing goto, tool-call state accumulation, verbatim subagent dispatch by section reference, embedded Lua for per-section configuration, tiny generic runtime. No surveyed system combines all seven. Closest matches and lessons drawn: Agentflow (clean per-phase context boundaries, but inline JS, no tool-call store, no goto, no subagent-by-reference); AIPack (Lua in markdown pipelines, but for map-reduce over fixed stages - the engine executes while the LLM fills slots); Playbooks ("LLM as CPU" with a program counter, but compiled to an intermediate representation - lesson: do not put a compilation step between the prompt author and the model, the raw markdown is the program); StateFlow (LLM as state machine, but does not wipe context between states); Reflexion (register-wipe/memory-keep split, but for task retries, not pipeline progression); Haystack State (tools write to a store the model never sees, but not persisted across transitions). The novelty is the combination: hard per-transition context wipe keyed to named markdown sections as a goto/program counter, all state externalized to a durable store and pulled back through tool calls, per-section Lua configuration, verbatim subagent dispatch.

Architecture principle: the runtime never contains orchestration logic, prompt assembly, or step ordering - those live in the markdown. The tool library never contains pipeline-specific logic - each tool is a thin, flat-signature function. This separation is what lets one runtime run every pipeline. [mermaid diagram of the three layers omitted]

The four primitives (everything else is a composition of these): (1) Parse - read a markdown file into a section map; H2 headings are the primary addressable sections, H3 headings are children individually addressable for fan-out; `## Main` is the entry point. (2) Configure - run a section's optional Lua block exposing five host objects (state, store, tools, params, context); preconditions run before the model launches, postconditions after the model calls `done()`. (3) Execute - run a section as a tool-call loop: build the fresh context (section prose + Lua-injected context + scoped tool schemas), call the model, dispatch each tool call, repeat until `done()` or budget. (4) Dispatch - resolve a tool name to a Python function, validate flat arguments, return a short result string. Every later feature - goto, Task, fanout, virtual files, ask_user, model tiering, postconditions, self-extending pipelines - is a composition of these four.

### promptforge-transcript.md (pasted twice, two formats)

[pasted: promptforge-transcript.md, first copy with "### User" / "### Assistant" headings, ~95 lines: assistant analysis of the compaction algorithm (strengths: logarithmic fidelity decay, no data loss, pre-compaction at 900 lines, prompt prepending; concerns: lossy cascades, rigid 50% ratio, lines vs tokens, boundary artifacts, no landmark preservation) and of Mentograph fit (structured preamble exempt from compaction; claim-aware compression: preserve factual claims and named entities, compress interviewer questions aggressively, subject answers conservatively)]

[pasted: promptforge-transcript.md, second copy with user text in blockquote per [p59], ~280 lines, adding exchanges: open-weight sufficiency for interviewing (the task is instruction following, not chain-of-thought; 70B+ can do it; frontier helps constraint adherence; tiered escalation recommended); 800B+ economics (data sovereignty, no rate limits, fine-tuning rights); distillation of a 14B-30B specialist interviewer from session data; latency engineering (speculative decoding, KV cache reuse, 4-bit quantization, prefill is the real bottleneck); hardware bandwidth table; STT/TTS latency budget (~1.2s to first audio); at-scale serving math (~$0.05 per session-hour, ~100x cheaper than frontier API); assay-replacement analysis (state management across 18 steps is the core problem; hybrid replacing only the Python glue recommended); tool-calls-instead-of-Pydantic exchange (flat 3-7 argument tool calls are reliable on a 14B; persistence becomes a side effect; cross-step data flow becomes pull-based; lowers the model floor dramatically); section/goto exchange (the prompt document is the program, sections are procedures, goto is a context-clearing transition, the context window becomes a register file cleared between instructions, Main is a dispatcher whose context never grows, harness ~200 lines); verbatim Task dispatch exchange (a model restating a prompt edits it; the runtime ships the author's exact words; what you test is what runs); composability exchange (division of labor by model tier; safety valve max depth 4-5, max 100 tasks; isolated state store per Task); testing exchange (debug each subtask in isolation; the unit of testing becomes the unit of composition)]
