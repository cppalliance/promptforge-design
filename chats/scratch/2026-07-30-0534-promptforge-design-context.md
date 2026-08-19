# Promptforge-design context session

*2026-07-30 05:34 - transcript b03df60c-25ca-4e1b-aa1a-e0adf26399f9*



## Prompts



**[p1]** context: @promptforge-design

**[p2]** show a link to the plan we are working on

**[p3]** fix the windows pathj

**[p4]** Change my mind, I think you need to, the, the prompt has to be able to transfer anywhere. Let them, let the author organize it however they want. We can't predict all the organizations, and we know that we can have cycles. So a prompt is a work of art. I love the single prompt format, you can tell I have so many of them, and, and this is, you know, it is what it is.

**[p5]** those design documents were an over-engineering, they are lower priority than our conversation. always.

**[p6]** the plan should mark those documents as provisional. take the good ideas. edit them to remove the bad ideas.

**[p7]** dont create a new plan. put it in @c:\Users\Vinnie\.cursor\plans\promptforge_orchestrator_only.plan.md delete the plan you just made

**[p8]** you can edit plans in plan mode duh

**[p9]** Okay, let's first of all, why do we need break section?

**[p10]** Linear pipeline, you just fall off the end of your section and you go to the next one, and then you don't have to name the next section. I don't understand. Why are we keep going around in circles? Show me the table of controls. Show me the table of control flows. I want the Agent side and I want the Lua side as columns.

**[p11]** I thought we agreed that return was gonna, in Lua, was gonna end the run, because we can use the return keyword, we can call it from check. What happened? You lost the design, you lost the plan that specified that you should update the documents in plan mode.

**[p12]** Okay, but if I thought goto had a second parameter. That was the input.

**[p13]** Then how does the model perform a goto that has a label and the Injected value. Show me the, show me the pros.

**[p14]** Okay, now show me the recipient, show me the destination, and how to access the variable.

**[p15]** We talked about it, we said we're gonna make it visible so that if you can actually read the code.

**[p16]** not really no.

**[p17]** Like the word "injection," just to be clear, I want a different word. And shouldn't we be putting it at the end? No, not really.

**[p18]** result

**[p19]** And I want to see it clearly in the plan. I want to have a nice table, and I want to have one or two sentences each outside the table.

**[p20]** why is there a question mark after result, i.e. result?

**[p21]** if its a convention keep it

**[p22]** task can be synchronous or asynchronous. if synchronous then its like a function call with context reset. if async then we need a rendezvous in the case ehtere areo

**[p23]** consider a function that spawns an async research task. after that the function continues in multi-turn. eventually the async task finishes  and then either executor waits for the task to call goto, return, etc.. and injects the result

**[p24]** 1. if the task ends early it just waits.
2. Section A has the option goto("## Section A") to clear its own context

**[p25]** yes and this is how you have a "research task" going nonstop, while the main context is getting bugfixes and speedups

**[p26]** Right, so what the question you should be asking is, what if the main section tries to move on or tries to return? So in that case, if it has pend-if it has a pending task, then that task needs to be cancelled, and then the message needs to go to main and, and it needs to say, "Hey, I got cancelled." Like, the message that main gets from the async research task is that's usually gonna be like a diagnostic, right? 'Cause the research task is just gonna store it either in a virtual file or it's gonna put it in a variable. And then we can, when we I don't know, when we launch the task, maybe we can choose, or maybe, maybe when we inject the tool, maybe when we scope the tool to the section, we say, "Hey, this tool's async." Would this work?

**[p27]** I feel like if you, if a, if a, if an async task is launched, then the harness has to immediately return a, a value like a number or an ID immediately, and it has to be unique. This way, if you launch, there are four tasks and they're asynchronous, now you have all the numbers. And then, when it's, if it's cancelled, then it has to give its number back. Or something like that.

**[p28]** We need the number, we need the ID, because we have to give, like, we have to give the harness the ability to cancel. We need to let the model cancel the task, like, if it's stuck. Like, there should be timestamps when a task is launched, it'll say, "So-and-so launched at this time, and here's your data.

**[p29]** Wait, you're talking about, oh, tasks. Oh, like list tasks.

**[p30]** Well. I think it should be Something else. How about What do you think of spawn?

**[p31]** But you in the, in the, in the, in the LLM, people say spawn three asynchronous sub-agents. Will that map correctly? Like, will the model know what the fuck to do?

**[p32]** Yeah, so. So what if Lua what can Lua initiate? Can they, can it spawn three sub-agents? And then, how does the context get them? What if Lua wants to wait? Like what if Lua's the one who wants to block? And they wanna run, they fire off three sub-agents, and then they wait, and each time one of the sub-agents finishes, they collect the result, and they collect the result, maybe in three variables, or maybe in a map, and then now the Lua has all that data, and then maybe it does something, maybe it calculates SHA-256 hash, maybe it checks the database to see if there's something, something that's similar that exists in latent space, who the fuck knows?

**[p33]** How can you say that there's, that you're just eliminating everything, right? Think about what you're saying.

**[p34]** What about a fork? That means the context decides to spawn another asynchronous task. But, and then back, and then back in the, in the collar, they just do, they, they continue, they fall through. Now you have a fork. Now the forks always come together, or do they? I don't know.\

**[p35]** No, I don't think they always come together. Like, I could see forking a, I can see forking a section that calls itself over and over again until some condition is met, right? And then, and then it never comes back.

**[p36]** I think in the for the sake of making progress, I think it would be best for us to divide the problem space synchronous and asynchronous. Divide it up. Show me.

**[p37]** Wait, are you telling me that fan out is map reduce?

**[p38]** What happens when each context is like really different? Like what happens when you have like a hundred rules and you want every batch of ten rules to be run in one of the FAN out? How do you do that?

**[p39]** See now for fan out, if you're fanning out, this is where I feel like you should be restricted to your section. Like you shouldn't be allowed to fan out to another H2 or its children, you should only be fanning out. On your own h threes. Think of the consequences of that.

**[p40]** So this is starting to sound right, like this sounds a lot better. But also, maybe if you have, let's say you have a hundred tests, maybe you put ten each in their own XML bracket, like, "We can use XML. Open tag, close tag, and then, now you can share the rules. So if you have, if you have two or three twos in a row, and they all wanna use the rules, they can refer to an XML. XML can be a variable in the Lua, and we parse the XML blocks that are in the document.

**[p41]** How do we How do we parse that XML? That's my question. And what are the rules? Can xml appear inside a subhead? Do we have to put them all at the end? Is that like, what do we do? Or maybe they can, they can be in a section. Oh yeah, that's it. Okay, so any section can have XML, h2, h3, at the end of the document, at be at after the h1, before the h1, it doesn't matter. But for the purposes of execution, it's as if those XML sections weren't there, because the harness will find them and it will put them in a table in the entire block of text, and nothing inside the XML tags will count as Prompt

**[p42]** The problem of course is, what if you're using an XML tag to give it emphasis? Like, what if you make the tag like, oh, we're already using the tag for the unique ID for the injection attack. How do you do about that?

**[p43]** "sect" instead of "section" ?

**[p44]** can the LLM query sections that way

**[p45]** Okay, update the plan. Might as well just update everything that you're confident about, leave out the risky stuff. Clean up the plan, review the plan, tidy it up, make it nice and compressed so I can read it.

**[p46]** Here, this is where I'm not clear. So let's say you have a hundred items, you divide them into groups of ten, you put XML tags around it, and now you can fan out, but you gotta do it manually, which kinda sucks. Then we've got, now let's say you have a list of thirty things, and you wanna slice them individually, now you gotta do thirty fan outs, now you've got thirty pairs of tags, so what was, you know, thirty lines, now is ninety, no, a hundred, a hundred lines. It's not really worth it. What do you think?

**[p47]** Your idea is to parse an o-an ordered list?

**[p48]** Wow, that's pretty bad. That's fucking horrible.

**[p49]** Well, it's not just thirty rules, right? Because you need the you wanna, you wanna have the opportunity to set up a context. And when the rule just gets injected into it. I mean, for all we know, maybe that's the, the result, right? Like. The, the section that you're calling receives the result, and that's like its packet that makes it, you know, it does whatever it has to do.

**[p50]** There's a problem here because. Okay, let's say I have a function, and I get a, and it, and it receives a result. And the result is the name of a company. And so now, I spawn a sub-agent, I get some background information, the sub-agent returns, okay, now I have more information about this company. Now the AI realizes, oh. We need to spawn one sub-agent to look at their IRS forms, then we need another sub-agent to look up their bullshit, and then we need a third one to look up their principles. Right? You don't know ahead of time, you don't know ahead of time what you need to search for in the sub-agent. That's the power of having a model. If you're calling it from the Lua and you just have some rigid rules, okay, yeah, big deal, I mean, it's company syntax, but really the hard part is in the model. Because like, let's say you get a company name, if it's a big tech company, maybe you wanna know how many microchips they buy, or let's say you get a medical, you get a pharmacy, you wanna know how many needles they buy, and so you don't know the prompt ahead of time that you're passing to the fin out.

**[p51]** Okay, did we make some decisions? Okay, so what do we do? Do we take every XML block and put it in a sections? How do we do it? Are they global or are they local to the heading? How does this work? And then what do we do with bullets? Bullets and numbers, we treat them the same? What do we do?

**[p52]** So I'm asking, so any XML block anywhere will be picked up, and then within the XML block, if there's a bulleted list, then that'll get skipped.

**[p53]** Oh, no. I'm starting to think the XML was a mistake. See, when I write a prompt. Put the XML block because the AI can find it easily. Models are trained on XML, and I tell the sub agent to grep, but we don't need that here because we're dividing, we're, we're dissecting the prompt ourselves. So really the XML is just for us. So now I'm wondering, maybe we shouldn't be using this XML, we should be using the section headings, because We want to leave the XML for the, for the model to be able to spot. We don't want to use the XML as a, as a grouping system for the harness.

**[p54]** Directionally correct but the level should not be special. We should probably just allow the use of any named section

**[p55]** repeat what you said but without using a fence

**[p56]** which plan are we editing

**[p57]** fix the windows path

**[p58]** still broken

**[p59]** That's the one

**[p60]** I don't want a "blocks:" manifest why do we need that?

**[p61]** yes and we will split bullets/lists no matter what even if it is intended as model prose



## Plans

### Design Docs Provisional

*Mark the PromptForge design documents as provisional reference material, fix the unreachable-section boot error, and establish that conversation decisions override the documents.*

# Mark Design Documents as Provisional

## Status change

Add a status line to each design document's HTML comment header marking it **provisional** - good ideas to draw from, not a binding specification. Conversation decisions override anything written in these files.

Files to update:
- [design.md](c:\Users\Vinnie\src\cursor\promptforge-design\design\design.md) - system architecture
- [design-promptforge.md](c:\Users\Vinnie\src\cursor\promptforge-design\design\design-promptforge.md) - prompt language
- [design-gateway.md](c:\Users\Vinnie\src\cursor\promptforge-design\design\design-gateway.md) - gateway crate
- [design-paperstore.md](c:\Users\Vinnie\src\cursor\promptforge-design\design\design-paperstore.md) - paperstore extension
- Other `design-*.md` files in the same directory

Each file's existing STATUS comment gets updated to include "provisional - conversation decisions take priority."

## Concrete fix: unreachable sections

In `design.md` and `design-promptforge.md`, the non-goals state:

> a section reached by nobody is a boot error

Change this: an unreachable section is **not an error**. The author organizes sections however they want. Cycles are legal. Dormant sections are legal. The prompt is the author's work of art.

Locations to edit:
- `design.md` line ~376 in the non-goals list: "No implicit advance between sections...a section reached by nobody is a boot error"
- `design-promptforge.md` references to boot-time graph validation rejecting unreachable sections

## Ongoing convention

Further cuts happen as they come up in conversation. No speculative purge.


Todos:

- Add provisional status to each design document's header comment
- Remove unreachable-section-is-boot-error from design.md and design-promptforge.md
