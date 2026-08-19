# Compaction algorithm session, large

*2026-07-30 10:46 - transcript e0e75624-f18d-4c1c-938c-edc40bfd7e79*



*Prompts p1-p62 of 397. Part 1 of 5. The Plans and Design Documents sections are in part 5.*



## Prompts



**[p1]** what do you think of this algorithm:
Vinnie  [5:19 PM]
@Will Pak what do you think of this compaction algorithm?

**[p2]** Given a transcript with N lines of turns
Ask the model to compress the first N/2 lines in half
Replace the first N/2 lines of the transcript with the compressed version
Also, when creating the new transcript, the original prompt is prepended to the beginning. This way a summarized context always has the fresh prompt.
so 1,000 lines becomes 750 lines. and when the 750 grows to 1,000 we compress again. but the first half of the post-compaction transcript looks like this:
|<- 250 line compacted summary ->|<- 250 lines uncompacted ->|so we would be turning that into
|<- 125 double-compacted ->|<- 125 line compacted ->|<- 500 lines full ->|(edited)
[5:22 PM]We always save the complete uncompacted lines to the database, so we can reconstruct the entire original conversation at any time
[5:23 PM]Furthermore, if the conversation limit is say 1,000 lines, we begin compaction early (at say, 900 lines). This way when we reach the context limit, we already have the compacted summary and the user does not need to wait for the next turn.
[5:24 PM]I am also wondering if open-weight models could serve as an orchestration layer. All we need to do is inject a Task tool for spawning subagents (edited) 
[5:24 PM]This needs to be researched

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

**[p33]** update the plan with all the good findings

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

**[p47]** what do you think of this idea

**[p48]** the scope is not as big as you might think. a lot of these are just specific examples of a general principle. like the tools

**[p49]** Let's take a detour for just a moment and then return back to this. What is the practicality of implementing a harness that can, for example, run something like @tools-public/tools/diligence.md without modification?

**[p50]** This is a detour - brand new architecture. how much python do we need to make this work unmodified (and what tools)

**[p51]** you are overthinking it. I am essentially asking, how do we just do what cursor does? I'm not asking to decompose based on section headings. Just pass the entire prompt to a model and say "do it"

**[p52]** and if we used Opus 4.8 Max with 1M context?

**[p53]** but we know Cursor does quite a lot for us surely it can't be that easy. Cursor handles multiple models and makes it seamless

**[p54]** okay thanks. none of that detour should affect the plan. Update the plan for what we know

**[p55]** when the plan runs I want every idea to be enriched with subagent web search, look for prior art, look for related work, look for anything that would be a subcomponent to build the idea, look for information about performance, metrics, model tier, and so on. don't write before researching and think deeply I want a fantastic report. write the report to @wg21-paperflow/promptforge.md

**[p56]** I want the transcript of this design discussion to be written to a markdown file. Leave out chain of thought. I only want the user prompts and the LLM replies and the subagent reports. Show me a one-page sample including 1 of each of thoese ellements before we commit

**[p57]** yes. write this entire transcript in that style to a markdown file

**[p58]** this looks like its going to fail at the end with "Edit attempted". shouldn't you be periodically checkpointing

**[p59]** start over. I want the user text to be in blockquote

**[p60]** get rid of ### Assistant and the blank line that follows

**[p61]** where's the chat transcript where we designed the talktron

**[p62]** @c:\Users\Vinnie\.cursor\plans\orchestrator_design_document_165f20dc.plan.md reset this plan so we can work on it and run it again, and the output will go to @promptforge-design as promptforge-design.md
