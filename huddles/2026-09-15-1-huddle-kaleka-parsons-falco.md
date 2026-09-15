Transcript of huddle in Greg on Sep 15 from 10:30 AM to 12:02 PM Pacific Time (US and Canada).

This transcript is auto-generated, so some information may be inaccurate. It won’t be surfaced in search results.
@Greg [1:03]: It's called a host integrator. But that's fine. I think I understand that bullet now. Goals. Rhoda's not.

@Sean Parsons [1:18]: Yeah, let's go to the goals of Treat every model facing section. As an agent context.

@Greg [1:27]: On Vinny's in the chat saying Run does nothing on its own. The host is what connects you all on the outside to the outside world. OK. I see, so that's why it's a an integrator. It's integrating the LLM and

@Greg [1:47]: I guess the person chatting with it. Or Have you ever tried talking to a raw owl? No, I have not. OK, so,

@Greg [2:10]: OK. I guess I don't know if I've talked to Ryle and then.

@Greg [2:29]: I see. Mhm. OK. It's, it's a, a toy for turning regular.

@Greg [2:46]: Sentences into pirate speak. OK. All right, that makes sense. OK, so goals, treat every model facing section, model facing section, so I guess to define that, is that are those the lua blocks that are

@Greg [3:11]: Calling

@Sean Parsons [3:13]: Model facing section.

@Greg [3:14]: Explicitly calling inference or what what qualifies as a model facing section?

@Sean Parsons [3:29]: A model facing section is one that

@Greg [3:30]: Not facing section. One that executes. OK. OK, so that's, I guess, ones that are not, well, OK, so you've got pros, which is in Markdown. And then you can potentially run that, although you don't. Have to, so I'm, I guess it's model facing in that you could pass it to the model,

@Greg [3:54]: And probably will, otherwise, what's the point, if it's not one of the comment sections that we discussed earlier. OK, so each model facing section, which is a combination of markdown and Lua code

@Greg [4:12]: Treat treat each of those as an agent context with one fresh Lo VM per section entry. OK, that makes sense to me. Sean, any questions on that?

@Sean Parsons [4:22]: The one fresh Lua VM per section entry, I guess is like. This is not a simple instance running.

@Greg [4:31]: Yeah, so.

@Sean Parsons [4:34]: Like a Lua VM instance, are we like splitting this out?

@Greg [4:37]: So Lua, my understanding of Lua is that every day when you call Lua code, it spins up essentially a lightweight VM.

@Sean Parsons [4:38]: Carly. Oh.

@Greg [4:48]: To run its code, and the way that prompt forge works is that you don't have like one long running Lou VM each section. Is its own Lua VM, so it's, it's born anew, and you have to pass it exactly what it needs, from, if you wanna like use stuff from other sections. I think there are ways to do that, but for the most part, like your, your Lea VM, the life cycle is like from the start to the end of the section.

@Sean Parsons [5:14]: Oh, OK. Got it. and what would that look like?

@Greg [5:24]: So he been is typing.

@Sean Parsons [5:26]: What would that look like in terms of like the changes, right? Cause it seems like there's a. Does Lua handle that implicitly or do you have to explicitly Like spin up. Let's just say this lightweight VM or whatever and then the.

@Greg [5:40]: No, you don't, you don't spin it up explicitly. Just running Lea code is going to do that, And, and I guess the way the the rust coat under the hood ingests and and runs each section is is doing that under the hood.

@Sean Parsons [5:55]: Doing it implicitly already.

@Greg [5:58]: Yeah. The, like, by defining because of this goal, Essentially this is saying like writing a section is Is your, that's how you're deciding, like, this is going to spin up, Aluvium.

@Sean Parsons [6:15]: OK.

@Greg [6:17]: OK, treat markdown accumulated since the nearest preceding heading. A section can also just be regular text. So what, what happens in that case then? Like, it's, does that do anything? Does the model ever see that regular text, if, if that's what's in a section.

@Sean Parsons [6:44]: The little one might reference it. And what does that do? Does that just add it to that messages? Object Like, what does it do?

@Sean Parsons [7:01]: It's just regular text. Sub Asians.

@Greg [7:05]: OK. so that section. That code you're talking about though is part of that section, right?

@Sean Parsons [7:25]: My point is that not all sections contain exe executable code or start up a VM I guess we were just curious about like, what happens when it's not executable code.

@Greg [7:31]: OK, yeah, so my Yeah, like what is, what is that doing? you, you answered that by

@Sean Parsons [7:40]: Nothing. OK.

@Greg [7:41]: Nothing happened. OK. so. I guess OK, I'm not sure what the Point of that. Is then, but maybe that's OK.

@Sean Parsons [7:54]: Marked down accumulated since the nearest preceding heading. You ask about model fencing like facing.

@Greg [8:06]: Yeah, so I guess, are those still considered mono facing. The implication is that there are non-model based exceptions. OK, yeah.

@Sean Parsons [8:14]: OK.

@Greg [8:15]: So that, that's what the, the OK, so if there's no Lua code, then it's really just There A pure tech section is not model facing. Yeah, it, it's essentially equivalent to a comment.

@Greg [8:32]: Yeah, OK. So, if, if I put a string literal in the code, and don't do anything with it. It's just a no op.

@Sean Parsons [8:40]: Yeah.

@Greg [8:41]: I would probably never do that. I would write a comment instead, but, that I guess I guess that's

@Sean Parsons [8:50]: As long as it doesn't execute right or whatever, I guess.

@Greg [8:52]: Thing that's possible, yeah.

@Sean Parsons [8:54]: Yeah.

@Greg [8:55]: Commons can can't have formatting. OK, yeah, fair. Would, would you like, why, why would you do that without that, what did, what did we call it a

@Sean Parsons [9:06]: The thematic break thing.

@Greg [9:08]: Yeah, thematic break. I guess if you don't, if you don't have a lua block in that section, you don't need the thematic break to mark it as a comment, you know, effectively a comment. it's just a noop already, so you don't need the thematic break, I guess that makes sense.

@Greg [9:30]: OK, I don't think we need to get too Fog down here, that that makes sense. OK. Treat markdown accumulated since the, let's look at an example, OK.

@Greg [10:18]: OK, so I, I am seeing a thematic break there.

@Greg [10:35]: Right, OK, so you've got the criteria and and these criteria used during blah blah blah, that is explicitly marked as a comment with a thematic break, and then the rest of this section.

@Sean Parsons [10:49]: Our actual instructions which get blown up into subagent commands.

@Greg [10:50]: I just text. No, no, this, the model doesn't see this at all. Because it's literally just text, right? So there's, unless you're, you have a LA code block that's calling a model, the model is not going to automatically read anything from here.

@Greg [11:09]: You could have this lua block that That Vinny is saying and now because he's calling Fan out explicitly, and now it is going to

@Sean Parsons [11:21]: The bullets array response of that, OK.

@Greg [11:22]: On a sub agent with each of these bullets. Yeah.

@Sean Parsons [11:26]: OK, so the first example is literally basically just a markdown file. We have the thematic break. Syntax. But there's no execution because there's no Lua block which actually Calls these commands that we have.

@Greg [11:42]: Right. But if you did add a LA block at the end of this section or just after this section. I guess it's still part of the section, that contained the code Vinny has posted here. now this is suddenly a model facing.

@Greg [12:00]: Section, because you're passing it to the model explicitly with Fan out.

@Sean Parsons [12:03]: Yeah, and he's The prompt dot section looks like it's kind of like a beautiful soup parser type situation. Go to the criteria header. Go to the

@Greg [12:16]: Criteria is not model facing, even though you're explicitly passing it to the model.

@Sean Parsons [12:24]: It has no VM. It's just tech sections.

@Greg [12:34]: OK. OK, so But bullets to a array.

@Greg [12:51]: You're passing it criteria. You're passing at that section. That's The model doesn't see that, I guess. OK, so the model isn't seeing that. The model is, that makes sense. OK, so, so this Lea code.

@Sean Parsons [12:58]: Well, what would we expect to happen?

@Greg [13:11]: OK.

@Sean Parsons [13:13]: See. I think. Analyze. Then I'll analyze. Bullets to array criteria.

@Sean Parsons [13:30]: Control never passes from H2 to H3 implicitly.

@Greg [13:37]: OK, before I, I don't understand this next example, but going back to the, the first example, first, The, the criteria section itself is not being Like the, the model doesn't ever see that you're explicitly calling Fan out.

@Greg [13:57]: Passing it the raw text that comes from bullets to a ray, so bullets to array, gets this section, finds the bullets, splits that out into 7 calls with the text from each of those bullets, and the model is just seeing those strings, not, it's not getting that section, it's just getting those strings, so that that's why it's not considered model facing cause the the section itself is never passed. You're explicitly

@Greg [14:27]: Giving each Each subagent, just a, a piece of text.

@Sean Parsons [14:32]: Like the describe the reason motivation or one gets that, the other one gets the second one.

@Greg [14:34]: Right, yeah. Yeah, the model never knows about this section. It's just, it's just getting this instruction directly, you have like non-model code that's splitting that out into text and then asking the model to do some stuff with just the text.

@Sean Parsons [14:44]: Instructions. Mhm.

@Greg [14:56]: OK, so in our Second example here. We've got this Thi H2. Then we have some LA code that I'm surprised to see is calling or is is referencing headers that come after it. that's surprising to me. I don't think I've seen that before.

@Greg [15:20]: I don't know, you could like look ahead, In a prompt. OK.

@Greg [15:36]: Interesting. OK. Do note that analyze is model facing. OK, so I'm, I'm trying to understand why this is different from We did before. OK, so in in the initial one.

@Greg [15:54]: OK, yeah, analyze, I don't see in the first example, but OK. So you're calling Fan out.

@Greg [16:12]: Because I'm not sure, I, I thought I understood what Fan out was doing above, but I kind of glossed over the analyze being passed to it, which didn't exist in the Initial block that you shared. Here, here it is there,

@Greg [16:29]: OK, I see you've you've added some code there. So this, I assume that In this case, Or this is like Inside Out, so the

@Greg [16:46]: OK, so you, you split up the bullets. Yeah, OK. Having having this, actually in here is probably going to be helpful. so the first thing that happens is the bullets get Split out, that makes sense. so now you have an array.

@Greg [17:03]: With items, each item. Contains these texts, the text from, from one of these bullets, then fan out. I It, it's spinning up a VM, I guess, for and passing it, analyze.

@Greg [17:25]: This analyze section. I see. So the analyze section string interpolates item, which is from one of these bullets. Yeah,

@Greg [17:42]: And then The, the thing that the, OK, so the sub agent. The subagent isn't just getting the bullet as a prompt, it's getting analyzed as a prompt with the bullet text as interpolated into the the that

@Greg [18:01]: Handlebar, thing, so the, the actual prompt it's getting is search the web for information about Identify it as design alternatives, blah blah blah. OK.

@Greg [18:17]: That makes sense. And you've got 7 of those. OK, that makes sense.

@Greg [18:44]: Analyze is wrong cause there's no tools. OK, so you, you would have to pass, analyze, you'd have to explicitly like declare web search as a tool so that you could actually do it. OK, and what, what's models. loop, in

@Greg [19:05]: In this case, like, what is that another tool that has to be declared for this, so that we can do the It's the total loop. OK, that's different from Fan Out, is that not? I kind of assumed that Fan Out was doing some kind of loop, but

@Greg [19:29]: I see. So you can't call. Dot infer you have to call.models. loop. Also loop is the multi-turn inference which ends with loss. Thinking.

@Greg [19:45]: OK, so would you just drop that in? Instead of models that infer, or would that need to wrap somewhere? Place. OK.

@Greg [20:59]: OK. History. OK.

@Greg [21:15]: And, remind me what this history colon user pros is doing. I guess that's OK, you're you're appending to the list of messages, I guess, with Pros, which is search web for information about and then the bullet, OK.

@Greg [21:40]: So the colon is essentially like Dot append in Python, that makes sense. OK, and then return P call, And then

@Greg [21:56]: Function per. And then some stuff. I assume that's like a a closure, just like a an inline lambda type function, Model that loop history, OK. OK, that makes sense.

@Greg [22:16]: P call captions exceptions, OK. OK, and then return. That That that gets potentially passed to the next section, right? That's the, the seam between sections.

@Greg [22:43]: Fan out returns and results. Yeah, oh right, OK. So return is just returning. To fan out. OK. So those are going ultimately into results. This, this Lea code analyzes one.

@Greg [23:01]: Iteration And it's returning that to Fan out, or yeah. Yeah, the exam. Full and kind of, you know, quote unquote real examples is helpful.

@Greg [23:23]: Makes sense. yeah, I mean, it's ultimately it's all. Kind of syntax, But I'm following. OK. Cool. So,

@Greg [23:42]: All right, so treat every Model facing section is an agent context. With one fresh flu of VM per section entry. Yeah, cool, makes sense. treat markdown accumulated since the nearest preceding heading Luense or thematic break as read-only lazy template exposed as prose to the following offense. I understand that in our example here, like if we just look at analyze,

@Greg [24:10]: This like search for search the web for blah, that that goes into prose, and we don't do anything with it until you explicitly call it. Makes sense.

@Greg [24:27]: Make every model operation explicit in lieu with no final prose or positional inference rule. Yeah, so that, This is, this makes a lot of sense. I like, you have to say this because it used to not do this. there was like

@Greg [24:45]: Magic happening where stuff was getting automatically passed to the model. That's no longer the case, that makes sense. Provide one rust-backed models. loop. Over provider-neutral message model.

@Greg [25:02]: OK. I don't really understand the second half of that sentence. Over a provider neutral message model. It depends complete assistant and tool history invokes a selected compactor when needed, default to omission to combat or not fail, and return ton. OK, every LLM has different text format for how it wants to.

@Greg [25:28]: See the messages. OK, yeah. OK. So that's the provider neutral, so it's, it's like Agnostic to, yeah, OK, OK, and then presumably each model has a translation layer where you go from our kind of like

@Greg [25:52]: Genericc normalized version to a model specific one. OK. Assistant and tool history. what, What is assistant in this case? Like, is that just the messages?

@Greg [26:14]: The system is the model. OK, so model history is the history of messages. User and and model messages. I guess it's passing the the messages that are going to the system and user mode. Yeah, OK.

@Greg [26:33]: OK. All right, so implement only the minimum compact or surface. Yeah, OK, so we talked about that. Invocation on PreCheck or provider overflow.

@Greg [26:52]: Invocation on PreChecker provider overflow. I guess overflow, like overflow makes sense, right? That's when context overflows the the context window, and needs to be

@Greg [27:09]: Needs to be compacted, invocation on makes sense, but what I'm not sure what PreCheck, I guess is what I'm missing here.

@Greg [27:39]: Got it. OK, so an explicit, like, proactive. Invocation for compacting versus An actual like overflow error where you are forced to do it. OK, that bullet makes sense then.

@Greg [27:57]: To further the replacement handling, compact or framework. Yeah, OK. So, essentially like, We need to actually implement compaction. We're not actually doing that, in this plan.

@Greg [28:14]: That makes sense. Deer lexical lua inheritance. Confined modules and complete child prompt execution. I Don't think I understand any of this. Lexical lua inheritance.

@Greg [28:34]: I'm not sure what is being inherited. There Lexical, something to do with the Set of vocabulary. This is being able to write functions which you can import. In multiple sections so you don't have to write them more than once. OK, I see.

@Greg [28:58]: I see. OK, that makes sense. Defer child concurrency and task or store changes. OK, I'm not sure what child concurrency means exactly.

@Greg [29:15]: Child prompt execution, for example. Local result equals execute lah. OK. Why? and. I guess I'm not clear on why that's

@Greg [29:32]: Child prompt execution, invoking another prompt for front. I see. So the, the, the, dosearch. MD as the child prompt in that case. OK,

@Greg [29:48]: OK. Event view removal, durable replay, and cold restart. I know. Yeah, OK, I see. So execute, I see. So call is you're passing it essentially a string with the prompt, and execute is a way to pass it a file.

@Greg [30:11]: Yeah, OK. OK. OK, so I know this like durable replay and cold restart. This we talked about last week, I think, about like what happens when you quit and reopen the work workshop, like you need to have a a history of all of the things that have happened so far, so that you can replay those and get back to the current current state, yeah, every event has to be.

@Greg [30:47]: Replayed, OK. I'm not sure what event view removal is, though.

@Greg [31:13]: Looks like my connection dropped off there for a second. the, the last thing I OK. I'm a creature myself. I'm I'm not seeing this in Slack. My computer dropped its connection, but I just see on my watch that you said, I'm not quite sure myself, but they at least, but hey, at least it's deferred, yeah, OK,

@Greg [31:36]: All right. Preserve of ownership of execution. I'm sorry, ownership of orchestration, message construction, and reshaping results.

@Greg [32:01]: Sorry, my, I guess my Connection is a little spotty here. Hopefully you can still hear me.

@Vinnie [32:12]: I hear you.

@Greg [32:23]: I'm gonna maybe try switching over to my phone for this huddle, just cause my My laptop's connection seems to be Dropping in and out.

@Greg [32:56]: OK, sorry, I've switched over to my phone. Hopefully this is a little more stable for now. OK. so where, where was I? OK, so we've deferred. Event view removal, which we're not totally clear on what it is. preserve ownership of orchestration. OK, so Lua Lua owns

@Greg [33:19]: Orchestrating models, I guess, message construction and reshaping. I'm not sure what reshaping is, but, that makes sense. Result selection, OK, compaction policy, sure, we've covered that interaction policy. I'm not sure what the interaction policy is, but OK, I guess that's like

@Greg [33:42]: OK. And then Rust owns Model tool continuation. I'm not sure what that means. Protocol safe history appendsure and scheduling,

@Greg [34:04]: Rust implements the tool calls, yeah, OK. OK, that makes sense, yeah, so Lua isn't actually implementing like Web search. OK.

@Greg [34:20]: Retain mentograph style background research and Papergate-style ordered parallel evaluation as deferred acceptance scenarios for future task run time. OK, I don't quite understand what that means, but, we're deferring this, it sounds like we're keeping these as deferred acceptance scenarios.

@Greg [34:50]: OK. OK, yeah, that makes sense. I'm just pausing cause I see you're still typing.

@Greg [35:12]: Right. OK, so we have to do that, but we're not going to do that right now. Right, yeah, OK. OK, non-goals. I feel like maybe some of these could be listed as deferred goals, but maybe not. Let's see. do not fork or replace the gateway's models specific chap template responsibility, OK? I think that makes sense. Do not make rust choose future summary wording or retention policy.

@Greg [35:48]: Yeah, OK. I see. Do not make Russ choose future summary wording or retention policy. I don't Quite understand that.

@Greg [36:06]: Retention policy of like Messages. Rust doesn't control the compaction. OK, OK, I see. Active host policy truth is blocking unavailable fallback or failure for user input.

@Greg [36:26]: Lua decides whether returned input enters messages. OK. Fine. Second part definitely makes sense. active host policy chooses blocking unavailable fallback or failure for user input. I don't quite understand the first half there.

@Greg [37:19]: User input blocks until the user reads something or it can tell to The but is unavailable, OK.

@Greg [37:37]: OK. All right. That makes sense then I think. Do not share mutable Lewis state between sections, OK? Do not add implicit trailing gros behavior until measured authoring evidence justifies it.

@Greg [38:01]: OK. I know the first half. Everything before until I think we've explicitly, that's kind of what we're dropping here, right, is the implicit Trailing pros gets handed to the model we're eliminating that, yeah, OK, until measured authoring evidence justifies it, whatever, OK, OK, that makes sense. do not redesign workshop presentation, gateway administration, or speech to text. OK, just keeping the scope in just the kind of markdown and lua handling. Do not redesign store semantics beyond integration required for by the active run.

@Greg [38:45]: OK, so try not to touch store more than absolutely necessary. Do not implement path-based execute or execute async in this plan, yep, OK, we said earlier we're deferring that that makes sense. Do not implement, require, include, local include, or partial markdown fragments. OK, so that, that's what we were talking about earlier with deferring lexical lua inheritance, etc. combined modules, blah blah blah.

@Greg [39:15]: This is restating that the include APIs and fragment artifact do not currently exist. Yeah, OK, current plan has no removal, compatibility testing either migration work for them. Later plans will implement them. OK, fine, very good. Success criteria.

@Greg [39:37]: One public executor runs finite Pipelines, cool, autonomous episodes, I don't really know what that is, and persistent interactive agents from markdown lulua. OK, cool. I guess autonomous episodes like

@Greg [39:53]: I don't know. we're not having any scheduling currently, but, Self-explanatory, OK. I'm going to let autonomous episodes go. The rest of that sentence makes sense. Every model autonomous headless agent, OK. every model request originates from an explicit Lua call and carries a validated provider neutral role sequence.

@Greg [40:22]: OK, yeah. Carries a validated provider neutral role sequence. I'm not sure what role sequence is here. The, the rest of this makes sense, yeah.

@Greg [40:39]: Roll and Caesar. OK, I see. OK, very good. One rust-backed models. loop appends protocol Complete History. OK, yeah, that's kind of what we were just talking about, processed every structured process every structured model tool call returns nil and behaves identically with zero or many model visible tools. OK, cool. the agent window remains functional through the generic input broker and active.

@Greg [41:13]: Models loop. OK. You don't, OK, so essentially like I'm not sure what this the generic input broker Yeah, OK. That's the user input hook. is this just saying like

@Greg [41:33]: That Stuff happening is not blocking the UI for the agent window, like you can add, you can send additional Stuff through there. Maybe I'm misunderstanding agent window, but that that's the like chat.

@Greg [41:50]: Box, yeah, OK, don't break them up. Very good. OK, I see, so this isn't talking about it remaining functional like during the runtime, this is like, it remains functional through the changes that we're making, like, you're not breaking it, that makes sense. reconnect persistence.

@Greg [42:10]: Workshop restore. OK, I see, reconnect persistence, that's a noun, workshop restore concurrency and composition contracts remain deferred, fine.

@Greg [42:26]: Prompts, examples, guides, and tests touched by the active or use prompt for 0 and its explicit model. OK. I do not understand this bullet at all. What what's Promp Forge 0 version 0, OK.

@Greg [42:44]: OK. All right, fine. That's also this first constraint, I guess, never propose incrementing while this role remains active, very good. That's nice. I should use this because I, I feel like,

@Greg [43:02]: I run into this a lot when I'm working on like iterating on pre-release stuff, it's always wanting to bump the release number. OK, preserved fresh, yeah, preserved fresh. I've, I've run into that too with other stuff, Same, same thing, so, preserve fresh VMs for fall through.

@Greg [43:24]: Jump, call and every child task entry use explicit task input. VR, return values and store as transfer channels, OK. Preserve fresh VMs for this.

@Greg [43:44]: I feel like I I'm sort of understanding this, but these are the only ways to transfer data between sections. OK, so this is the like, explicit. Handing off of things between sections. So fall through.

@Greg [44:01]: Drum call. OK. OK. I think that makes sense. keep canonical events. Depend only. And separate from mutable model facing message arrays. What are

@Greg [44:18]: OK, I see Sean is very good, thank you.

@Sean Parsons [44:23]: Yeah.

@Greg [44:25]: Hey Sean. OK, so there are two messages. We're we're in, what section is this? Product requirements, and we're in constraints, and we are currently talking about this 3rd bullet, keep canonical events append only and separate from mutable model facing message arrays. So,

@Greg [44:52]: OK, D.

@Sean Parsons [44:55]: It

@Greg [44:55]: That's correct.

@Sean Parsons [44:56]: And on Who manages the the The events, like, what does that mean? Keep canonical events.

@Greg [45:08]: I think the keeping is like don't. Don't, break this,

@Sean Parsons [45:17]: Don't break this.

@Greg [45:18]: As you're working, as you're working on this.

@Sean Parsons [45:20]: OK.

@Greg [45:21]: So as you're making these changes, make sure that canonical events are appended only and they're separate from model facing message arrays. I'm still not super clear on this, but let me, hold on, I'm reading Vinny's messages.

@Sean Parsons [45:38]: Initially, canonical events and model facing event were identical. As soon as there is one compaction, now they are diverged.

@Greg [45:49]: I see. So, I see. So if you were to look at the full Conversation history. The canonical events. Are literally like each of the messages that exist,

@Greg [46:06]: Once you do a compaction. Now the model isn't seeing that full history. They are now seeing the like summarized his pre-combaction history plus the new messages which are themselves part of the canonical thing, but they're also model facing, so the model doesn't see the pre-compaction canonical events. I see. That makes sense.

@Sean Parsons [46:14]: Summarize notes of.

@Greg [46:33]: So even though the model isn't seeing them, we are keeping them around. For audit purposes and eventually when we when we implement the like replay of events for for like restarting the system, we need those actual canonical events potentially, although, maybe that's not the use case, but I, I get what Vinnie's saying now. you've got the like actual kind of audit trail of the real messages that were sent, but the model might see something different if there's been a compaction.

@Greg [47:12]: Does that make sense, Sean?

@Sean Parsons [47:14]: Yeah, I think conceptually, I think everything conceptually makes sense.

@Greg [47:22]: OK, And again this constrained section is just like. Don't. Don't fuck this up. OK, the model will eventually be able to see them through a tool or the virtual file system. Yeah, OK. Go through this chat and tell me each time I referred to the gateway and how you're blind. OK, so it's, it's essentially a way to not lose the full history of messages, while also being able to compact what's being sent to to the model, so you're not blowing up your your contexts window, but you don't lose the ability to reach back and find those actual initial messages.

@Greg [48:04]: That have been summarized. Through compaction. Does that, does that make sense, Sean? Have you, have you seen compaction with, like, when you're chatting with a model and you, you like compact it, it's essentially like summarizing everything up till now, so you lose some granularity, right? but this, this is a way to like keep a separate log essentially of all of the essentially the like message transcript.

@Sean Parsons [48:18]: Yeah. Yeah.

@Sean Parsons [48:35]: Yeah, like my, my knowledge of the, you know, this entire thing is more as like an end user and consumer, you know.

@Greg [48:41]: Yeah.

@Sean Parsons [48:42]: So I'm these these kind of like deeper internal working stuff.

@Greg [48:45]: Yeah, of course, same, same for me, very much so,

@Sean Parsons [48:49]: Yeah. It's really cool though to kind of like, Dig a little bit deeper and understand what's actually going on, so it's Been fun for sure.

@Greg [48:59]: Compaction is a traumatic brain injury, I like that. OK.

@Sean Parsons [49:11]: Normally when I get to compaction, usually that's either when I clear the session or close the session, cause at that point. It just feels like that session is 5 years.

@Greg [49:20]: Yeah, cause you know how trash it's you have internalized the that your model is gonna have a a TBI if you, if you compact the the context.

@Sean Parsons [49:32]: Yeah.

@Greg [49:34]: Yeah, OK, keep the canonical event log host owned and unavailable to the prompt LA expose specific. OK, so this is, this is kind of what you were saying, Vinny, that eventually, That these will be accessible via a tool call, but we don't.

@Greg [49:52]: We don't want Lua to be able to like directly access them. Right, yeah.

@Greg [50:08]: OK.

@Sean Parsons [50:09]: OK.

@Greg [50:11]: Read the model and tool sections at call time. OK, the message array is the only continuity state and the author owns it. DirectluaTools.com may access.

@Greg [50:27]: Found but unadvertised tools. OK. What is, what is a bound but unadvertised tool? And Vinny, feel free to continue riffing on compaction, and we can come back to this, but OK, model can only see tools from tools.ad.

@Greg [50:52]: The lua can invoke any tool that is bound to the prompt. I guess, yeah, what, what does it mean for a tool to be bound to the prompt?

@Sean Parsons [51:03]: I like that particular specific prompt. Maybe. And where, where are you? I thought you were on constraints, Greg. I don't see that tools. a thing. Where where did you read that?

@Greg [51:19]: I didn't see tools. ad. That's, that's, I'm hopping back and forth between our Slack thread and

@Sean Parsons [51:25]: Oh, OK, OK, OK.

@Greg [51:25]: And the document.

@Sean Parsons [51:27]: All right. Confused there.

@Greg [51:30]: The tool's contract is defined in the YAML. Everything that has to be everything that uses. Sorry, OK. Bronze counter is defined in the animal. Everything that it uses has to be explicitly named. OK, so there's

@Greg [51:48]: OK, so there's, there's some yamal. Is that the front matter that you're referring to?

@Sean Parsons [51:54]: At the top part, I believe.

@Greg [51:56]: Yeah, is that, is that what you're referring to Penny? I think that's right. And and so there you you would bind any tools that are going to be available to it.

@Greg [52:12]: Which capabilities you want, which tools you want, what model slots you use, what your input and output store files are.

@Sean Parsons [52:12]: I That's interesting. I thought the tools, the tools part from which I saw kind of examples in the code. I thought that that was defined using lua.

@Greg [52:27]: Right, so that's

@Sean Parsons [52:27]: Like tools that have.

@Greg [52:29]: Yeah, so that's, that's what he's saying, the model can only see tools from tools. OK, you've changed it, but the luc can invoke.

@Sean Parsons [52:32]: OK. OK.

@Greg [52:38]: OK, so you, I see, I see, I see. So Lua. Lua can invoke any tool that has been defined in the in the Yamal. the model will only see tools that lure hands to it with tools.add.

@Greg [52:57]: So you are in the front matter in that Yamal you are constraining which tools can be used and then in the LA code you are defining which tools can be used by this specific model call.

@Sean Parsons [53:20]: And I guess under the hood does Lua call tools.ad based off of that definition at the top anyway. I'm assuming it Does

@Greg [53:30]: Well, the, the you're writing, you, the author, the prompt author are writing the LA code. I don't think there's any like under the hood. Yeah, the.

@Sean Parsons [53:42]: To give them, you must write. To give them up. So but if the definition is done in this part of the YAL, do you also explicitly have to do the tools.ad is what I'm I guess what I'm asking.

@Greg [53:55]: I, I think so, yes. But Vinny's gonna tell us. So you might have, you might have two tools, right? You might have like a web research tool, and I don't know, Mhm

@Greg [54:12]: What's another tool? You might have a file exploration tool, right? And then, You in in one Lua block you might say tools.add file explorer, and then that that model instance is going to only have access to the file explorer. It will not be able to do any web research even though it's in the prompt Yamal. But then in a later ya later Lua block, you might only pass at the web research tool with tools.add and then that model instance is only going to be

@Sean Parsons [54:27]: Mhm. Mhm. Got it.

@Sean Parsons [54:47]: Right.

@Greg [54:51]: Able to do web research. It's not going to be able to read files,

@Sean Parsons [54:54]: On.

@Greg [54:55]: So that I think that makes sense to me. Is that, is that right, Vinny? Am I describing that accurately? Yeah. Yeah, so the idea is for for efficiency's sake, you only want to add to the exact tools that the model needs and not.

@Greg [55:19]: Not any additional ones. So like, I think this is one of the the key

@Sean Parsons [55:19]: Not every, not anything else.

@Greg [55:26]: Value propositions, yeah, so Vinnie's saying exactly what I'm about to say, which is that the core principle of PromptForge is that you are giving it explicit control over which tools the model can use, whereas in, you know, if you're using clawed code or or the whatever Google's Gemini harnesses, the model can decide at any time to use any of the tools that it has access to, so it might have, you know, it can call arbitrary bash things, it can do.

@Sean Parsons [55:45]: The other yeah.

@Greg [55:56]: Web research it can, you know, explore, call an explorer tool, all these different things, and so there's, there's overhead there that forces you to, to, that's part of why you need a more advanced model, cause it's gotta, yeah, it's got to be able to make decisions about which models to, which tools to use, etc. so.

@Greg [56:23]: Yeah, one of the, one of the kind of value props of prompt forge that you can do the same level of work with a smaller model in part because of things like this where you're explicitly giving it which tools it has access to, and you're able to kind of keep that as small as possible.

@Greg [57:01]: I'm, I think I'm Good for the moment.

@Sean Parsons [57:06]: Me as well.

@Greg [57:07]: OK, so let's move on in the dock then. Yeah, OK, so we just did the model and tool sections. Keep all user visible agent behavior editable at runtime through LA or prompt files.

@Greg [57:27]: Editable at runtime. The agent window is not rust special.

@Greg [57:44]: I don't know what that means either.

@Sean Parsons [57:50]: I guess that means it can be changed or modified. What does that mean?

@Greg [57:55]: The Asian window just runs a prompt, yeah, OK.

@Sean Parsons [57:55]: Agent.

@Greg [57:59]: OK, so the agent behavior is driven exclusively by The prompt file with Malua and markdown. OK. defer to open questions.

@Greg [58:21]: I'm letting, I'm letting Vinny type here for a second.

@Sean Parsons [58:25]: Vinny do its thing.

@Greg [59:15]: OK. So I I have to say I'm still a little unclear on Like

@Vinnie [59:32]: Come on don't I just try to I'll try to talk.

@Greg [59:33]: Prompt forage.

@Vinnie [59:35]: I'll try to talk, OK. Consider The Mentographist. You've run it. Have you run it?

@Greg [59:46]: Yes, a while ago. Yup.

@Vinnie [59:49]: So it interviews you. Look at what happens when you run it in cursor. When, when you run it in cursor, you get cursor system prompt. And cursor's system prompt says, you are a helpful coding assistant, and then it has like

@Vinnie [1:00:05]: 2000 kilobytes of instructions about the current window, and how to get help, and all this other nonsense, and

@Greg [1:00:12]: Yeah.

@Vinnie [1:00:12]: My prompts can't access any of that, because my prompts just come in as user messages, get it? Or they just, they come in as tool data. When when it reads the tool, it comes in as tool data, and then the model orchestrator has to try to follow the directions. Well, guess what? As soon as you get a couple of compactions, now the mentographist is gonna lose its strength, right? Like, it's gonna get more and more fuzzy, it's gonna lose its instruction set. Now, imagine instead of that, we implement the mentographist as

@Greg [1:00:19]: Yeah.

@Vinnie [1:00:42]: A prompt. And now it gets to control what goes in the system prompt, and it controls compaction. So after a compaction, it'll make sure that it preserves its own instructions. So that means the mentographist, the, you know, implementation, it's always at the beginning of the context. It's never lost on compaction, so that means it it will, it will stay in character forever. Get it?

@Greg [1:01:01]: Mhm. Right. Yes.

@Vinnie [1:01:06]: And that and that can become a window, that becomes a user interface. So you say new agent, and then like there's a little fly out, and then mentographist could be in the list, or you could have, you know, The architect could be one of those agents, or you could have a tutor, like you could have one of those that Python tutorial, that could be an agent.

@Greg [1:01:27]: Yeah.

@Vinnie [1:01:28]: And now you're interacting with it in that window. And it can survive compactions, and it knows what the fuck to do.

@Greg [1:01:35]: Right. You're, you're controlling essentially the system prompt and the like, what survives compaction.

@Vinnie [1:01:37]: OK. Yes. And yeah, and you have access to the history as well.

@Greg [1:01:47]: Who's gonna.

@Vinnie [1:01:47]: So you could be like skill you can put like Skill gate in there. Right, like you could have an agent. So you can have an agent that like lets you design. And And then it looks in the history, and it knows, like, it can help you.

@Vinnie [1:02:04]: He could rag index the entire conversation. And you can enrich the context with things that you said before. You could do a lot.

@Greg [1:02:13]: Yeah.

@Vinnie [1:02:16]: Let's put it this way, You see how, you see what a dumb LLM is, right? Like an LLM that has no, no tools is basically in, it's basically sterile, right? Like it's in a sandbox.

@Greg [1:02:28]: Yeah.

@Sean Parsons [1:02:29]: Mhm.

@Vinnie [1:02:29]: All you could do is, all you can do is talk to it. Now, Look at what happens when you give it tools. It can search the web. It can spawn sub-agents, it can code, it can edit local files, it can run, it can talk to the shell, and it can, it can shell out, it can compile your program, look at its output, and fix it. So look at all these things that it can do.

@Vinnie [1:02:51]: Now, imagine If you have an agentic harness that can access knowledge, your knowledge, your design principles, everything that you've ever said to the AI. You can rag index all of that, and you could use it. You can like you could distill principles, like you know those little stupid files that I put there in the tools public, like the how-tos.

@Greg [1:03:07]: Mhm. Yeah.

@Vinnie [1:03:14]: Like you could, you can have an agent that has access to those things, like that helps you while you code. And I, and it can be in the background, and if you have a machine, like let's say you have like just just one blackwell, you don't even need a 4, just 1. Let's say you just put one, you know, RTX 6000 in there, and you have 96 gigabytes, right? Now,

@Vinnie [1:03:34]: You could take like a little 31 gigabyte queen, right? A little queen flash for a you know, a 31 gigabyte model in there, and it can run in the background, and it can be, it could be like a sidecar constantly analyzing your conversation and enriching the context, and injecting that information in there.

@Greg [1:03:53]: Mhm

@Vinnie [1:03:54]: Like every time you start something, the the model doesn't know shit. It has to like search around and figure out, OK, what am I looking at here? Like, oh, where's the source code? Oh, how do you build it? How do you do all this shit? But if we control the harness, and we allow for local inference, then we can enrich, like we can inject that information ahead of time, right? Because think about it.

@Greg [1:04:02]: Yeah. Right.

@Vinnie [1:04:15]: If you have, if you have a card, With and you have some extra VRAM, that inference is now free. So the economics flips. Like right now we're like, you know, we're token, like we're tokens misers. You don't wanna, you don't wanna waste tokens cause it's expensive, but if you have local inference, now the now the economics flips around. Now you want to run it constantly.

@Vinnie [1:04:38]: So, you wanna run inference nonstop, like while you're just, even if you even if your agent is just sitting there waiting for you to type in something like that fucking card, it should be doing something. It should be indexing your code base. It should be looking for stuff, right? It should be popping up with like helpful tips. If the if if local inference is sitting idle, then it's wasted.

@Greg [1:04:52]: Mhm.

@Vinnie [1:05:00]: No one seems to have figured that out yet. Like, you know what I'm saying? Like, no one's figured that out, but now you have, now you have people that there's like an RTX 5090 now that has 8080 gigabytes of VRAM.

@Greg [1:05:05]: Me. Yeah.

@Vinnie [1:05:13]: It it's like a hack, and it's like for 30. Dude, think about that, 80 gigabytes, you could run a lot of good models with that. And that's local. In in your IDE it's like helping you.

@Greg [1:05:27]: Yeah. How what does that cost?

@Vinnie [1:05:30]: I'm very excited about.

@Sean Parsons [1:05:32]: You said like 30, man.

@Vinnie [1:05:32]: Oh, I swi. Yeah, dude, like 30. It's not, it's not exotic by any means. So, I'm very excited about all of this, because this is why I'm building all this out, because I feel like People are leaving money on the table. Like like there's there's stuff that can be done. Nobody's writing prompts like vibe coder, like, I don't see nobody implementing vibe coder. No one is writing debt collector. Those things work. No one's writing architect. I've never seen anything that reorganizes the plant who reorganizes the plan into something that looks like

@Vinnie [1:06:07]: You know, A document that you might Have in even in a non-AI, right? Like, Functional technical design, functional specification, product requirements. These are normal things. How come nobody has done anything like this before? How come I'm the one doing it?

@Vinnie [1:06:24]: Either, either, either my ideas are stupid and and and I'm huffing the AI sauce and hallucinating, or, or it's a green field and there's money on the table. Now I can, I mean, I'm fifty-fifty either way, you know what I mean?

@Greg [1:06:33]: Yeah.

@Vinnie [1:06:40]: All right. Question.

@Greg [1:06:42]: I think it's Greenfield, but.

@Sean Parsons [1:06:45]: Yeah, I don't think a lot of people really understand this, Vinny.

@Vinnie [1:06:51]: They definitely do, because every

@Sean Parsons [1:06:52]: I think it's Greenfield for sure.

@Vinnie [1:06:55]: Maybe. I don't know.

@Sean Parsons [1:06:57]: I think, I think most people are more on the consumer end of this, and they really don't understand how How these things really work. And they're happy enough with the, happy enough with the current state that it helps.

@Vinnie [1:07:06]: Well,

@Sean Parsons [1:07:11]: In a general sense that Maybe optimization is overlooked at this point because It does OK.

@Vinnie [1:07:19]: Or there's another possibility, which is that I have the privilege of Basically consuming unlimited frontier model tokens.

@Greg [1:07:29]: Mhm.

@Sean Parsons [1:07:30]: There's that.

@Vinnie [1:07:31]: So like, Yeah, so I, I like I just, I, I spawn some agents, I create reports, I ask, like everything that I've learned, I've I've learned by asking Claude. Like, how do the how do, how does the assistant, how does the system context work? It fucking tells me. Like, how do I make, how do I shell out? It tell like everything in Promp forge that well all this stuff that you see, this stuff that I'm explaining to you, it was explained to me by the LLM.

@Sean Parsons [1:07:48]: Yeah.

@Greg [1:07:56]: Mhm.

@Sean Parsons [1:07:58]: Reverse engineering itself for you, Vinnie.

@Vinnie [1:08:01]: It knows, and so what, what this, this seems like a really big diversion. Why is it? Let me I wanted to, I want to explain why I wanna do this. Is because I rather like the new AI age fellows. Like, I've become rather attached to it because I feel definitely more productive. I mean, look, I made 7 books. I wouldn't have made 7 books before. Now I make 7 books. Now we can have a cool website. Now we can have a fake subreddit. Now we can judge every paper in the mailing every month. I mean, these are really cool things and they're really and they're enabled with AI, but we have a problem, guys. We have a problem because there's there's

@Sean Parsons [1:08:31]: Yeah.

@Vinnie [1:08:39]: There's something very bad that's gonna happen in our near future. And that is this. The tools that we use, the proprietary tools like, you know, cloud code and cursor, they're going to get worse, they're gonna become shitified. It's already happening, and the frontier models that we are coming to depend on, they're gonna also get shittened. They're gonna become more expensive, and they're gonna start not wanting to work the way that we want them to work. So then we have a very limited window of time to build our own tools. The prompt forge is designed to be the escape, and so we can have our own IDE that works the way that we want, that works with openweight models. We'll go and we'll we'll

@Vinnie [1:09:14]: Deploy Kimmy K3 or we'll put another deep seek instance in there, and we'll run whatever the whatever the frontier openweight models is, we'll run them ourselves and we'll control it on our hardware, so we can continue enjoying the AI revolution without other Silicon Valley tech companies or legislators deciding how we're gonna consume it.

@Greg [1:09:33]: Yeah, that makes a lot of sense to me.

@Vinnie [1:09:34]: That's. I don't ever want to go back to the old way. Ever.

@Sean Parsons [1:09:41]: Thank you.

@Vinnie [1:09:43]: OK, let's keep going.

@Sean Parsons [1:09:45]: It

@Vinnie [1:09:47]: Oh, All right, I'm gonna

@Sean Parsons [1:09:51]: He's gonna go back to writing. Probably hurt his throat.

@Greg [1:09:52]: Mhm. Thanks, thanks for enduring that, Penny, that was helpful.

@Sean Parsons [1:09:57]: Yeah.

@Greg [1:10:00]: OK. So I think we're Through constraints. And he's got 20 minutes. OK.

@Greg [1:10:16]: OK, so deferred open questions. Define how a continuing conversation, mutable message, projection, compactor policy, and pin prefix prefix receives stable identities that survive replay without serializing lua table or closure identity.

@Sean Parsons [1:10:34]: I I think these are like open questions that either Vinny had to the LLM or the LLM has to kind of Vinny?

@Greg [1:10:36]: Yeah. Yeah. Yeah, or just like decisions that haven't been made yet.

@Sean Parsons [1:10:46]: Right.

@Greg [1:10:47]: So I, I, I don't understand all the words in here, but I understand the gist of this bullet. This is again about. You know, we, we have to at some point figure out how to do a prior conversation,

@Sean Parsons [1:10:59]: Address, please. Mhm

@Greg [1:11:05]: Yeah, resuming after exit, yep. OK, define operator semantics for front matter input and output. OK, so we, we don't yet have that in the Yamel, Vinny mentioned that input file and output file is part of what you define in there, but we haven't made the design decisions about exactly how that syntax is gonna look, or maybe not how the syntax is gonna look, but like how the actual like handling of

@Greg [1:11:34]: Yeah, in the, in the rust, like, how do you actually like pull from the input and Right to the output, I have to hold on, I'm getting my Slack back over to that thread. I wandered,

@Greg [1:11:52]: Yeah, OK, very good. so the, the kind of like API interface between the rust layer and the what the prompt is gonna Yes. OK. I'm, I've been still typing. I'm gonna pause just for a second.

@Greg [1:12:29]: 3 parts apart prompt. Mhm.

@Greg [1:12:49]: OK.

@Greg [1:13:07]: OK. and I'm sorry, remind me again what the host is in this context. That's the Like The prompt forge. Harness itself. The host calls from on the front.

@Greg [1:13:26]: OK.

@Greg [1:13:44]: OK. All right. And then define H1 bootstrap ownership. This remains immutable.

@Greg [1:14:00]: Identity finish reason request IDs, projection hashes, and metrics remain host observer data rather than later cys mutation or LA models. loop results. So what is sys in this case?

@Greg [1:14:17]: The system. Something. OK, each one is kind of special, trying to make it less so. Certain amount of specialness that can't be avoided. This is a table. OK, a lua table, I assume, that holds some operational values.

@Greg [1:14:35]: OK, OK, so it's it's holding some like metadata around the The running of the stuff itself, OK, so it, it is immutable,

@Greg [1:14:52]: OK. OK, so start like the example you gave of start time that can be populated at kind of like inception, but

@Greg [1:15:12]: Some of these other things are happening later, and so we don't just stuff those into cysts. OK. Well, I, I, this is a little fuzzy for me, but it's a deferred open question, so I think that's probably OK for now.

@Greg [1:15:31]: Shall we move on to functional specification? All right, actors and workflows. PromptForge accumulates markdown in a pending prose buffer after each section, heading, or ordinary loo offense. OK, very good, we've talked about that a few times. Yup. Yeah, this, I mentioned earlier, like at the top, I didn't understand any of the sentences now that we've kind of like fleshed some of this out. these are easier to parse, so,

@Greg [1:16:08]: Yeah, definitely understand that sentence. A marked down thematic break recognized by the parser clears that buffer. OK, so yeah, we kind of, came to this bullet on our own, as we were reading the kind of summarized thing, on each ordinary loo offense, PromptForge installs the current buffer as a fresh unresolved read-only prose value. Very good. Clears the pending buffer.

@Greg [1:16:34]: And runs a Lua co routine. OK. so once you get to a lua fence, I see, so you, you clear the pending buffer because you have put it into this prose, Variable, so you can, you can clear the buffer so that it's ready to to intake the following set of pros, that makes sense.

@Greg [1:16:58]: Cool. OK, yeah, very good. the first runtime reads snapshots. I'm sorry, the first runtime read, snapshots section state, evaluates every mustache thingy, handlebar, whatever you call it, substitution once.

@Greg [1:17:18]: Memorizes the resulting string, OK, so. Cashes it essentially and returns that same string on later reads. OK, so the first runtime reads snapshot. Section state.

@Greg [1:17:35]: OK, this is like per section, I see. So in the section, like in the pros, when you have These like substitution strings that gets

@Greg [1:17:51]: Done once, and that's cashed, and then if that, if prose gets read again, like if you're in a a loop, or a fan out, I guess. you don't have to do the string interpolation again. You've you've already done that, the one time that gets memorized. OK.

@Greg [1:18:15]: Prose never changes in a liu block once it is read. Yeah, OK, so that makes sense. Mark down before the last thematic break. Is inert commentary, it's a comment and mark down left after the section's final luo offense is inert trailing commentary. OK, so this is a change, right, this last part.

@Greg [1:18:37]: It used to be that the trailing, any trailing mark down was. Like handed directly to a model for inference. We're no longer doing that. Yeah, so unconsumed markdown at section end is discarded without error or model invocation, so it, it's inert,

@Greg [1:18:59]: That was the whole positional inference semantic, yeah, so Sean, I don't know if you were, like, In the process of understanding this before this change, but, it used to be that, any like trailing markdown, so essentially any file, any prompt file that ends with markdown after any like a lu offense that would get handed directly to a model for inference, and that is just no longer the case, so any trailing markdown just essentially gets ignored. You can treat it like a comment.

@Sean Parsons [1:19:34]: OK.

@Greg [1:19:35]: So, again, like the, the philosophy. With this change is that any inference that's happening is explicit, so we're saying, you know, model. whatever, and handing it the prompt. there's no more implicit,

@Greg [1:19:53]: Model inference of any kind. OK, a routine, toll-free pipeline author, OK, calls model.inferros. And passes selected results explicitly through VR, store, or return values rather than a rolling reply register.

@Greg [1:20:14]: OK, I think I understand this. I think this is almost restating what I just said, where I'm not sure what a routine toll-free pipeline author means, but

@Greg [1:20:30]: When you call model.s.infer you're passing or and pass it the pros, that is Essentially, like, stuff gets Captured and and passed around explicitly in variables. There's no, this is again like there's no

@Greg [1:20:54]: Like implicit, Anything, and I, I, I'm not quite clear on what this reply register was, but yeah, I think it was a, a like implicit place that The result of Model inference was was stuffed into this reply thing. Yeah, so you, there's like this implicit variable of like whatever the last thing the model, whatever the last model message was stored in this undeclared reply variable, that's that's going away.

@Greg [1:21:30]: I, I have to say it's, this is all much easier to understand in the future state where you don't have to like, know about these special things that are getting kind of done behind the Behind the scenes as much. OK, so a routine tool-free pipeline author. Now we're talking about a stateful or tool-capable author.

@Greg [1:21:51]: Build a plain message array directly through optional pure lua messages.new methods, causes models. loop and may remove or reshape records before the next model operation. OK, so this is just like The case where

@Greg [1:22:11]: You're doing, I guess, just a little more sophisticated stuff with, I'm not sure what a stateful author means in this case, but tool capable makes sense to me. But in terms of the messages that new, that makes sense. We, we had an example earlier that Vinny shared, that was explicitly creating that messages array.

@Sean Parsons [1:22:31]: I guess that's what makes it stateful, right?

@Greg [1:22:34]: Yeah, exactly, that's exactly what you just said, I think.

@Sean Parsons [1:22:35]: Is that you can like attend. Yeah, you can append messages to it. How would you?

@Greg [1:22:41]: Right, so you've got system message, you've got user messages, agent messages. there's a, there's an example up above.

@Sean Parsons [1:22:42]: Use that. No, I mean like using it in the context of like, is it purely just there for state management of like, this is in an append log, like, is it more for visibility or is it used and passed into subsequent

@Sean Parsons [1:23:06]: Lua VMs and they're able to like retrieve it. Do you get kind of what I'm saying? I'm like maybe trying to wrap.

@Greg [1:23:11]: The last, the last thing you said I'm not sure is, is the case, but it is like you, you can build up an array of messages, and then, OK, yeah, you, you cannot transfer messages across across VM. So I was right that that's that part is wrong, but, my understanding is that you can create an array of messages that can be of various types, so they can be, you know, system, system messages,

@Sean Parsons [1:23:20]: OK. OK.

@Greg [1:23:37]: User messages.

@Sean Parsons [1:23:40]: Dog messages.

@Greg [1:23:41]: Dog messages, sorry. And, and then you can pass that whole array to a model, right? So like in, in a normal, you know, vanilla, dogs. In, in a normal harness, you are having a conversation with the model. There's back and forth, every time you send a new message, what's really being sent to the model is the list of messages that have come before it, right? So you're, you're getting all of the back and forth, including the original system prompt,

@Greg [1:24:18]: And then the the new message that you're sending. So this is a way to kind of explicitly control that. OK,

@Greg [1:24:36]: OK, an interactive author, interactive author, this is a third kind of author, may call models that loop repeatedly over one retained message array. And use direct user input or the model visible tool. Through one generic broker.

@Greg [1:24:56]: OK, I think I understand this. This is Maybe I don't quite, but

@Greg [1:25:13]: So direct user input, that's like Asking the user a question, and then you type in the little chat box and send that back. That gets passed through, maybe there's alternatively some input tool, that's either getting input from a user or you could, you know, get input from some other system that it's

@Greg [1:25:38]: Bowling for or goes out and gets some. Content Yeah. OK. Right.

@Greg [1:26:00]: I don't quite. I don't quite have an understanding of how this like, Yeah. Right. Yeah, so that was kind of what I, I think what I was trying to say,

@Greg [1:26:19]: I guess the user input box in PromptForge is that just the like Agent window. Yeah, OK.

@Greg [1:26:36]: OK. persistence around that interactive message array remains deferred. OK, so, Yeah, OK, very good. We're not actually implementing persistence for that,

@Greg [1:26:55]: Deferred task contract. An interactive author may start an isolated background or may start isolated background trial work, continue through user input and consume completed child results on a later turn without blocking the section VM.

@Greg [1:27:11]: OK, without blocking the section VM, so that's That sounds complicated, So, You mentioned that we can eat the the agent can yield.

@Greg [1:27:28]: OK, this is the task II. OK, so this is just more kind of asynchronous handling of that, so rather than just like wait, you know, waiting for the user input to come back, you can go do some other stuff and then you have some contract defined for what happens when the task completes.

@Greg [1:27:48]: And maybe at some point you do, you know, you do some other stuff, but then before you can continue, you do have to wait for that, Kind of standard concurrency stuff.

@Greg [1:28:11]: Right, yep. Yeah, so Vineyard just gave an example of that. are we, so this says deferred task contract. Does that mean that implementation is Deferred, cause I, I feel like we said that the async stuff was deferred and we're we're not actually

@Greg [1:28:31]: Doing that, yeah. Deferred means deferred, very good. I guess I was, in this particular instance, I was worried I was misreading this, and that meant like a deferred task, but, OK, very good, so we're not doing that yet,

@Greg [1:28:51]: Yeah. Totally very reasonable, OK. Cool. OK, Vinny is turning into a pumpkin in a couple minutes,

@Greg [1:29:15]: An active host input policy blocks for For a human reports unavailable immediately or fails. OK, An active host.

@Greg [1:29:31]: Sorry, an active host input policy post human reports are available immediately or fails. So those are the three things it can do. it can either wait for a human to give it user input,

@Vinnie [1:29:43]: OK, I'm gonna, I'm just. Greg, I'm gonna explain it, then I'm gonna go.

@Greg [1:29:48]: OK.

@Vinnie [1:29:49]: When, so there's different types of failures. There's a, there's a like a terminal failure that will end the entire run. Right? Like, that's like a resource error. Or something just corrupted, right?

@Greg [1:30:02]: OK.

@Vinnie [1:30:02]: And then there's a soft failure, like you call execute, like let's say you call execute, and then The the file that you're trying to run is not there, right? Like the other, the, the markdown file is not there. Like that's like a file not found. That's a softer error. It's still bad, but the excuse me.

@Vinnie [1:30:22]: Name is That's a that's something that the lua can trap. Right? Like, you could trap that error. And it can say, oh, OK, and then it can handle it, maybe, maybe by printing a message and exiting.

@Vinnie [1:30:40]: But now look at what happens if the if look at what happens if the model. Tries to do something, like, let's say the model tries to execute a prompt, or to spawn a task, or to do a tool call, and there's like some kind of internal failure. We wanna, we wanna tell the model.

@Vinnie [1:30:58]: But we wanna tell it using English language, right? So, for example, user input, like let's say we give the model the opportunity to call the like the ask question. You know what the ask question tool is, like in cursor, like it comes up with like A B C D. like that's a tool called. Now, let's say that you're running the tool in headless mode. You're just you're running it like a command line tool, and you want the tool to work both ways. So the model calls ask question, but then instead of like throwing an exception and making the whole thing stop, you tell the model, you say, hey, you're running in headless mode, this tool is not available. Now, the model understands that there's no human attached.

@Greg [1:31:13]: Yep.

@Greg [1:31:36]: Right.

@Vinnie [1:31:39]: Get it?

@Greg [1:31:40]: Mhm.

@Vinnie [1:31:41]: So in the in the bullet, it says, Preserving the exact fallback sentence while distinguishing it from human speech. What that means is the model called user input, and we have to tell the model that that that it failed, but we don't want the model to think that that message is what the user wrote.

@Vinnie [1:32:00]: Right? Like that could be, that would be a fuck up. A lot of things that the user.

@Greg [1:32:00]: Right. Right. That's not the answer to the question.

@Vinnie [1:32:06]: Exactly, and And by the way, this is a recurring theme, like, everywhere, everywhere, there there's that the that that the model is receiving some type of result. You wanna have explanatory text. Not only do you want explanatory text, but you want to tell it what to do instead. Like for example,

@Greg [1:32:17]: Yeah. Right.

@Vinnie [1:32:25]: Input could could return. There's no human here and there never will be, so you have to use your best judgment, like you gotta tell it.

@Greg [1:32:33]: Right.

@Vinnie [1:32:34]: All right, I'm gonna jump to lunch.

@Greg [1:32:36]: All right. Thanks, Vinny. Appreciate it.

@Vinnie [1:32:38]: You guys can keep doodling on that, and let's come back and let's finish it.

@Sean Parsons [1:32:43]: OK.

@Greg [1:32:43]: OK. We're about 10% of the way through.

@Vinnie [1:32:44]: All right, bye. OK. No, some of it we, we don't need to look at, right.

@Greg [1:32:51]: Yeah, OK.

@Sean Parsons [1:32:53]: See you.

@Greg [1:32:55]: All right,

@Sean Parsons [1:32:56]: See you Greg.

@Greg [1:32:58]: Are you taking off?

@Sean Parsons [1:32:58]: Or did you want, or did you wanna keep powering through this?

@Greg [1:33:02]: Let's see. Can we reasonably get through?

@Sean Parsons [1:33:05]: I mean, has it been? 2 hours or so, probably.

@Greg [1:33:09]: Something like that. I, I wouldn't mind taking a break and we can restart and.

@Sean Parsons [1:33:19]: What do you think, 20? Come back at 3:30?

@Greg [1:33:21]: Yeah, that sounds good.

@Sean Parsons [1:33:22]: All right. Let's come back at 3:30.

@Greg [1:33:22]: I'll see that. All right, cool. See you.

@Sean Parsons [1:33:25]: All right. See you.