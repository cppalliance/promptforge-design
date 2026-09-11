Transcript of huddle in Greg on Sep 11 from 6:20 AM to 8:03 AM Pacific Time (US and Canada).

This transcript is auto-generated, so some information may be inaccurate. It won’t be surfaced in search results.
@Vinnie [1:01]: I I, I think Sean, you saw the design repo, right?

@Sean Parsons [1:12]: The design the

@Vinnie [1:14]: Pump forge design.

@Greg [1:17]: OK

@Sean Parsons [1:18]: No, just prompt forge itself, not the des, is there a design repo?

@Vinnie [1:18]: Too. Oh. Yeah, so I, oh, I think maybe I did I show that to you, Greg?

@Greg [1:26]: No, I, first time hearing of it, I think.

@Vinnie [1:31]: Here.

@Sean Parsons [1:32]: It's a separate repo.

@Vinnie [1:34]: Yeah, I made a separate repo to just dump the stuff in here, look. See this? Cause when you're waiting for a vibe, you need something to do, so I would start a new plan, and I would start a new document, and then you can outpace, you can outpace the AI's ability to to implement.

@Greg [1:52]: I can't see this. I get a 404.

@Vinnie [1:52]: And so I dumped, I dumped all my ideas into this repo, so I just I mine it for ideas.

@Greg [1:57]: Oh

@Vinnie [1:58]: But it's not all valid, so just be aware. Don't, don't like take think this is some kind of gospel. There's something that I'm sure.

@Greg [2:05]: I don't have access to this many.

@Sean Parsons [2:07]: It, Greg, maybe.

@Greg [2:08]: Yeah, it's private.

@Vinnie [2:10]: Geez, what a mess. OK.

@Sean Parsons [2:12]: I am added to it, but I don't think Greg is. Let me see the settings.

@Vinnie [2:12]: All right. Well, there's no reason for it to be private, so.

@Sean Parsons [2:20]: OK.

@Vinnie [2:21]: It's good to know, I guess, that it's private. Change that visibility. Oh my god.

@Vinnie [2:37]: I I need my 2 factor. And I just switched phones, so I don't have all my passwords. OK, here we go. Now it's public.

@Greg [2:49]: All right. Got it.

@Vinnie [2:53]: I guess I'll add the everyone, I'll add the everyone team. Right? OK. Shaw has maintenance, and everyone has bright access.

@Greg [3:13]: Right.

@Vinnie [3:13]: OK. So, I just put, so here's what I would like though. From now on,

@Sean Parsons [3:19]: Yeah.

@Vinnie [3:20]: Every time we have a huddle, I, I'll make a transcript. We'll have a transcript, and then I want you to add the, put the transcript in the repo.

@Greg [3:29]: OK.

@Sean Parsons [3:30]: OK.

@Vinnie [3:31]: With a very with a very specific, I'm gonna write it, I'm gonna write in the in the public in our 21 WG 21 channel.

@Sean Parsons [3:40]: Like a format.

@Vinnie [3:41]: How'd you know?

@Sean Parsons [3:44]: Well, I mean, for ordering, so like we can.

@Vinnie [3:59]: There. That's usually how I do it. OK, right. OK. So then, so we have a cha we just said we can have that.

@Sean Parsons [4:12]: Mhm.

@Vinnie [4:13]: Transcripts. And then, Also, Scooping up the Slack conversations. Public and private, if it has to do with prompt forage and just

@Vinnie [4:29]: Putting that in another directory, you know, Slack. And then we just Well, Will can help with that actually. So Will can help. And then, I wanna try to build We need to build design documents, but real ones, not just the ones that the AI shits out.

@Vinnie [4:50]: Cause that's not helpful. That's just folding slop into slop.

@Greg [4:55]: Mhm.

@Sean Parsons [4:55]: Mhm.

@Vinnie [4:56]: Try my hand at that today. Now I got a, I have some bad news. I tried these skills, you know, the bash kit, I, I looked at their skills a little more closely. Beautiful idea.

@Greg [5:03]: Yeah.

@Vinnie [5:07]: But Unfortunately, 50% of it is hopes and dreams. it's, it's, it's like, it's bullshit. And let me see if I can find it. Skills evaluation. Look, see this? What's well written and what's hopes and dreams? Well,

@Vinnie [5:25]: Some of it's good, but then hopes it this is taste wearing a procedure's clothes. Take time to find better abstractions, has no success condition. The model being asked to find the shortcut is the model that just wrote the code. In the same context, fresh off justifying every choice it made, it will look at its own work and find it good every time.

@Vinnie [5:47]: Oh Same disease. The same model self-review as a rain dance. Oh God, you know what? Jimmy Kimmy is surprisingly good at writing. I gotta say, it's pretty darn good.

@Vinnie [6:08]: Yeah, Yeah. Well organized expression of hope. So, oh my god, OK. Anyway, and then there's another problem. Which is

@Vinnie [6:24]: That the the way that I work is I, I have what's called a mono repo. See this?

@Greg [6:29]: Yeah.

@Vinnie [6:29]: Yeah. Like I just have I have one directory, and then in there I have all these folders. This is I I have one folder with all this stuff in it.

@Sean Parsons [6:35]: Mm-hmm.

@Vinnie [6:41]: And Unfortunately, cursor doesn't see that, it only sees the cursor directory at the root. So it'll it'll this skill. But like, it won't see the ones in here.

@Sean Parsons [6:53]: All the sub skills or whatever.

@Vinnie [6:55]: Exactly, and this this happens every single time I look at skills, I'm like, oh, we gotta make this work. No, there's no way to do it. I mean, I guess you could copy the skills. Yeah, if you're willing to just maintain a copy of the skills, then yeah, you can make it work.

@Greg [7:08]: Yes so.

@Vinnie [7:12]: But

@Sean Parsons [7:12]: I think you can set them globally too, right?

@Vinnie [7:16]: Yeah, but you know, again, dude, now you have this stuff that's in your in your user account, and it's like, oh well the repository just updated. I gotta copy them over. Oh, I forgot. Oh, I, I just did 150.

@Sean Parsons [7:22]: Yeah, for sure.

@Vinnie [7:29]: I did a 150 commit vibe run where I forgot to apply the skill. Oops.

@Sean Parsons [7:33]: Right.

@Vinnie [7:34]: But, you know, you know.

@Greg [7:35]: I, I think you need a script that scans the sibling directories and sim links to any skills in the dark cursor skills thing.

@Vinnie [7:43]: Yeah. Yeah. That, well,

@Greg [7:45]: Like that.

@Vinnie [7:47]: Then we have the next problem, which is, yeah, once you try to do that, then you realize, but wait a minute, what if you have two different repositories? How do you combine all their skills? Oh, now you gotta make a script. So, This is just another reason why we need the prompt forged workshop.

@Vinnie [8:04]: Right? This is why we need our own harness. We need a programmable harness that lets us work the way that we want, not the way the cursor thinks that we should work. And there there's a very real risk because now that Elon Musk owns Cursor, now Cursor gonna care more about satisfying Elon Musk than us.

@Vinnie [8:25]: And we're already seeing it, by the way. so, And I, and I'm rather attached to my new AI powers. I don't wanna lose them.

@Sean Parsons [8:35]: Excuse me.

@Vinnie [8:35]: So, and the, the prospect of having to go to another harness bothers me greatly. Cause I've looked at them, and they all, there's something, you know, they, they all have their little agenda. Cloud code is good, but cloud, I, I can't work cloud code doesn't work the way that I work. I need my tree and I need rag indexing over all my files. Like I depend on those features because of the type of work that I do, like when I do my papers, like quad code is not as good at writing WG 21 papers as cursor.

@Vinnie [9:03]: It's great for code, but, you know, well, I guess maybe, maybe I should be using it more for the code, but It doesn't handle things like finding minutes. You know, finding conversations. Putting together a

@Vinnie [9:19]: An argument, right?

@Sean Parsons [9:21]: Mhm.

@Vinnie [9:21]: Mhm I mean, the the model handles the reasoning, but I don't know if you, do you guys understand how what a harness does?

@Sean Parsons [9:29]: No.

@Vinnie [9:31]: OK, let me explain it to you. You're gonna love it. The large language model can only do one thing. It has exactly one fucking function. It takes a prompt, Well, it, it takes a giant, it, it takes a stack of messages, really. And

@Vinnie [9:48]: Then it gives you a reply. That's it. So, you're in the input to the model is is a structured object. You could there's the system message, right? It's all the text. Then you have the user messages. And then you have the assistant messages, though that was the previous conversation.

@Vinnie [10:11]: So, OK, so users, what you put in, right? It's the shit that goes in this box down here, that's a user message. And it can be multimodal, you can paste an image, right?

@Sean Parsons [10:22]: Right.

@Vinnie [10:23]: Hold on, I gotta school this guy, man. Right, so that's the user message, and then when the AI responds, that's the assistant message, and that can that can have like thinking blocks, right? You've seen, you know what thinking blocks are.

@Vinnie [10:40]: See that? That's not a thinking block, that's a tool call, that's a thinking block. That's a tool call.

@Sean Parsons [10:47]: Mhm.

@Vinnie [10:48]: And that's And that's another thinking block.

@Sean Parsons [10:51]: Right.

@Vinnie [10:53]: So like, If you If you use PromptForge, and you use the the right model, you'll see like, you'll see all this shit appearing like all these little Jason lines, and they're like, what the hell is this? That's what the model is returning, but an an IDE like cursor, like what it'll do is, it'll take all those little consecutive thinking blocks and reports, and it consolidates them, right? Like you see this, this is a consolidated, because you don't want to flood the user with a bunch of spam, right? So the, the IDE consolidates this for you, but this is an assistant message that has a hierarchy. There's like an array in there, and then there's a tool tool call results and all this other shit. So,

@Sean Parsons [11:22]: Mhm.

@Vinnie [11:35]: That's the, that's, that's the conversation, and this agent window here, every time, every time you submit a prompt like that conversation grows. Every time you submit. A prompt to the model, the harness sends everything that came before, plus your message. That's why this thing over here, see this in context, that's why this just grows. It grows, and it keeps growing, and eventually it it the the harness submits the, the, the messages and it gets an error. It says, no, context overflow, and that's when you get a compaction. Are we clear?

@Vinnie [12:13]: Did you know that's how it all worked?

@Sean Parsons [12:13]: Yep. Maybe not at that level.

@Vinnie [12:19]: She kind of had an intuition, right? Like you could see your context filling up. And you know it's coming that compaction's coming, right?

@Sean Parsons [12:23]: Yeah. Yeah.

@Vinnie [12:29]: So, So, do you understand what a tool call is?

@Sean Parsons [12:35]: Well, based off of like the prompt forge, the prompt forge stuff in this conversation, it seems like it's a dedicated.

@Vinnie [12:35]: Oh, this is great.

@Sean Parsons [12:42]: A process or task that's really good at doing. Some specific thing.

@Vinnie [12:47]: Oh man, you don't know what a tool call is. You're gonna love this. This is gonna be the best, this is gonna be the best huddle you've ever had, cause you're now you're gonna understand how these things actually work. So,

@Sean Parsons [12:50]: Apparently not.

@Vinnie [12:59]: A tool call is when the model makes a request. It asks you to do something. How does that work? Well, every model is trained in tool calls, basically, except for very specialized models. A toolol is a block of jason. That that has the tool call structure.

@Vinnie [13:16]: And a and a special marking that says, here's a tool call, it's basically it's just part of the text that the model sends back, and the tool call is a model's request for the harness to do something. So for example, the model may decide, hey, I want to see what's in this directory, and then it'll do a tool call to the shell and and with the command to do like LS, right?

@Sean Parsons [13:38]: Yeah.

@Vinnie [13:39]: And then you, and then you know what happens after that?

@Sean Parsons [13:42]: I'm assuming it responds and then it thinks.

@Vinnie [13:45]: Nothing happens, because the model doesn't actually do anything. It just asks for the harness to do something, and then it waits patiently, doing nothing. Why? Because it's not running. The inference is over. So now it's the harnesses's responsibility to say, oh shit, he wants to do a tool call and then to actually do the thing that was asked for, collect the results, and then that goes into the, that goes, gets submitted as a, as a message. It's a tool, it's a tool called result message, and then it gets submitted back to the model.

@Sean Parsons [13:47]: So.

@Vinnie [14:15]: For inference, and then the model thinks it says, oh, hey, he did the tool, he did the thing, here's the result, and then it continues thinking. Get it?

@Sean Parsons [14:25]: Yup.

@Vinnie [14:26]: But how does it know what tools you have? Well, You can only get a tool call if you offer the model a set of tools to begin with. So, for example, in in in cursor, in the agent harness, they offer a very big set of tools. There's like

@Vinnie [14:43]: String replace, reed file, you can see them in here. Look, there's a tool called explored, right? That's a call to read file. Used ship. That means it looked at this skill. You can go over here, here, let's go, let's look at my

@Sean Parsons [15:03]: So is that why you were suggesting creating a files package to be able to. Provide the harness with the ability to like read the users' file system. And do things like that.

@Vinnie [15:16]: Yes, we only The only way for the model to interact with the outside world is with tools. What? Oh my God. Their reed. You see that? That's the reed tool.

@Sean Parsons [15:29]: Yeah.

@Vinnie [15:30]: This this little box is a tool called. And They have cursor has like a little, a very fast and very dumb model. That will, it looks at It it it it can look at a tool call, and it can give you a string telling you what it's doing.

@Vinnie [15:51]: Right? Like,

@Sean Parsons [15:51]: Mhm.

@Vinnie [15:54]: Like, you know how It goes, you see planning next move, and then it says thinking, and then under that you could see like these little strings that tell you like what it's doing.

@Sean Parsons [16:04]: Yes.

@Vinnie [16:05]: Those strings are not hard-coded. They're they're the result of a little tiny model, like a, like a 1 billion parameter model, whose only job it is to look at a a block of text and calculate that string, like it it's it describes what like the, you know, it gives you that little message.

@Sean Parsons [16:25]: Mhm.

@Vinnie [16:25]: So that's how it comes up with these things. Now, here's of course the fucking, here's the classic problem. I'm on Windows, and it always gets this wrong because on Windows we have PowerShell instead of a fucking normal shell like Bass. We've got the power shell, like, like Power Rangers, except you're the pink one.

@Vinnie [16:47]: And it always gets a mistake every fucking time because Per shell has to be a special snowflake, and it uses different syntax. Now, what does the model do about that? Well, the model is very good when it sees an error. It's, then he knows how to fix it. So this is, by the way, this is like a really good general principle of when you're of writing tools. If your tool fails,

@Vinnie [17:10]: Explain why in very clear terms that don't require a lot of context, you know, a lot of contextual information, but also give you, explain what to do instead. If you do that, By the way, you know those stupid ass benchmarks, you know how every time like there's a model that comes out, everyone like puts those benchmarks.

@Sean Parsons [17:29]: Yeah.

@Vinnie [17:30]: The harness is as equally as important to the benchmarks as the model itself, because a good harness will explain what to do instead. A bad harness will just give you an error, like it'll say error code 3, and that doesn't help the model. And so the result is if you have like a long horizon task that involves like, you know, thousands of tool calls, your yield, your, your, your success rate will go up if you have good res good errors, because you have to help the model.

@Sean Parsons [17:44]: Right. Right.

@Vinnie [18:00]: And then another example like, OK, like let's say you're implementing the LS tool, a naive implementation of LS right, would be to just call the shell and run the, you know, list the directory. Why is that naive? Well, because what if there's like 10,000 files in the directory, OK. Here's what's gonna happen. The model, the model is gonna go in there, it's gonna say, hey, what's in this directory? Cause you know, they love to look around before they do things. That's smart.

@Sean Parsons [18:24]: Yeah.

@Vinnie [18:25]: And that's, you want that. You don't want to ever want to model to just blindly make assumptions. So it doesn't LS and now, now look at what happens, you have 10,000 files in this giant string, and you've just flooded your context, right? Like that's no good, that's a bad harness, that's, that's crap. Instead, what you want is you want to limit it. You want to say, OK, instead of running the real LS, you're going to run your own synthetic version, it's going to limit its output, and it's gonna say at the bottom, it's gonna say, results are truncated.

@Sean Parsons [18:40]: Yeah.

@Vinnie [18:55]: And, and then give you, give it the command to give, get the full results, or even better, it'll give the the it'll give the model like a paginator. It'll say, here's how you page through the results, or it'll give the model a way to grip, like, you know, look for specific files, and that makes a better harness.

@Sean Parsons [19:12]: Mhm.

@Vinnie [19:13]: The better the harness. The better it's gonna be at tasks.

@Sean Parsons [19:18]: Mhm.

@Vinnie [19:18]: Right? So let me explain. Let me explain why, if you, if all you have is just a bunch of tools, You're not going to get a good result. The cursor Like every other good harness, injects information into the system prompt, and into the user messages. It injects information that helps the model figure out what's going on. For example,

@Sean Parsons [19:41]: In

@Vinnie [19:43]: It says what files you have open, it tells you what's in the terminal that you're looking at. It knows what you have selected here. And all of that is injected, and you can see it. Look at that. See that? System prompt, 1.3K. That's quite a lot.

@Sean Parsons [19:57]: OK.

@Vinnie [19:59]: Tool definitions, rules, skills, All that crap, all of this is additional context that cursor injects in there for you, that helps the model.

@Sean Parsons [20:10]: Mhm.

@Vinnie [20:11]: So, So, OK, back to the tools. So, When, when every, every, every API for like every API endpoint for interacting with the model, they all have a separate jason to represent the tools. The tools is just a big adjacent array.

@Vinnie [20:28]: Each tool has adjacent, and the tool has like a description. Let me show you what that looks like. Show me the exact Jason. For the For the tool description. Or stirr place.

@Vinnie [20:46]: This is in the model has this in its context there, see it? String replace that edits files.

@Sean Parsons [20:51]: Yeah.

@Vinnie [20:54]: See that?

@Sean Parsons [20:56]: Yeah.

@Vinnie [20:57]: So the model sees this, like it sees this description, and then it knows. So like if you tell it to edit a file, it sees this string replace and it thinks, oh, this looks handy, shit, let me use that. And then and then it's like, how do I call that? Well, here's the name. Oh, what are the parameters? Oh, here we go. There's there's the there's a new string parameter, the old string parameter. Oh, what is that? Oh, the text to replace. Oh, OK, and then it knows how to call it.

@Sean Parsons [21:10]: Mhm.

@Vinnie [21:24]: It's just words, dude.

@Sean Parsons [21:24]: It's like an oak. It's like an open API spec definition.

@Vinnie [21:28]: Yes. It's just, but notice, it's like it's just words, right? It's like you just tell it, you say what to put where, and then the and then the the LLM figures it out. This is all because of training.

@Sean Parsons [21:33]: Yeah. Right.

@Vinnie [21:43]: And one thing that models know really well is paths. Like they know how they know paths. They know about replacing, they know about gripping. That's like any model that's tool capable, that's the first thing that they get trained on.

@Sean Parsons [21:58]: Right.

@Vinnie [21:59]: And then look, if you want to create a new file, use the right tool instead. See alternatives. So this is like a package. This is a package of editing tools that cursor provides. OK, so when you do, when you, when you invoke the model, You offer it a set of tools.

@Vinnie [22:18]: And that's why in PromptForge, you notice that like, It you're, it's it's being offered tools. See that?

@Vinnie [22:35]: Wait, what is this? Paper gate. I really do need to fix that.

@Greg [22:40]: Hm

@Vinnie [22:43]: OK. See that tools. add local.

@Sean Parsons [22:47]: Tools not that local in that section.

@Vinnie [22:48]: Yes. That tool is being

@Sean Parsons [22:51]: So you're building your goals, like, OK. That's in Lia, right?

@Vinnie [22:57]: Yes.

@Sean Parsons [22:57]: The tools add local to the start string function. Oh, and that's a callback to Rx table.insert. So table.

@Vinnie [22:59]: But I mean, Yeah. The

@Sean Parsons [23:08]: Table is the, I remember you mentioning Lua uses tables for kind of like. Executing underlying functions.

@Vinnie [23:19]: Everything's Everything in lu is a scalar or a table.

@Sean Parsons [23:22]: Mhm Mhm.

@Vinnie [23:25]: No.

@Greg [23:26]: Sorry, a, a what or a table?

@Vinnie [23:26]: This thing this this variable, this variable.

@Sean Parsons [23:29]: Or

@Vinnie [23:31]: This variable is the table module.

@Sean Parsons [23:34]: Right.

@Vinnie [23:35]: Like

@Sean Parsons [23:35]: Whereas.

@Vinnie [23:37]: Prompt Forge, when it creates a VM, it imports some of Lua's default modules. It imports the system module, which gives you like, the time.

@Sean Parsons [23:42]: Yeah. Mhm.

@Vinnie [23:46]: And not random numbers, not much else. The math module, and it imports the The blew up basics like the table module. So table.insert is basically a global function. Yeah, it's a lure function that inserts into the table.

@Sean Parsons [23:59]: Right, that's built in a lua, right?

@Vinnie [24:02]: Yes.

@Sean Parsons [24:03]: Right.

@Vinnie [24:03]: Now, If you don't need tables, you don't have to load that module. Now we need tables, of course, but you know.

@Sean Parsons [24:10]: Insert section.

@Vinnie [24:10]: Blue is designed to be very lean. So, The goal of this is to build a table of Line number ranges of all the sections of markdown, get it? That for each section, record its name and line number range.

@Vinnie [24:27]: And the model figures out, it's like, oh, it says record its name and line number, and then it sees the tool. And the tool says add a section with its line range, and the model says, huh. If I, I'm being asked to record the line number ranges of each section, and I'm being offered a tool called add section, which adds a section with this line range. Oh, I know, I should call that tool for each section, and it does it. Isn't that amazing? Isn't that fucking cool?

@Sean Parsons [24:58]: Yeah.

@Vinnie [25:00]: Now, I know what you're thinking. You're thinking, but Vinny, why are we wasting inference on something deterministic that we could achieve with a markdown parser, and you're right, we could do that. But if we do that, now we're adding something that's Papergate specific to the executor, so that means we need to figure out how do we add like plug-ins, right? Like, if we want to do like a little custom parser in rust or lua. Now, how do we add, you know, stuff that that can be linked in at runtime, and so I have a design for that.

@Vinnie [25:32]: From add-ons like shared libraries, but you know, that's that has to wait. So we're doing it this way for now. So, the more tools you offer a model, the more you're asking it to think. If you offer 1000 tools to the model, you're, it's not gonna work. No, no model can handle 1000 tools. The frontier models can handle like 30 to 50.

@Vinnie [25:56]: The really tiny models can handle like 5 to 9. The less, the fewer the tools that you offer, the better the chances it'll pick the right one. If you offer only one tool, well, guess what? It's like every, every nail every nail is gonna want the hammer.

@Vinnie [26:12]: Right? So, One of the principles of prompt forge is to give the prompt author very tight control over the tools that are offered. Instead of just offering everything all at once, You have to opt in to every tool that the model gets.

@Vinnie [26:29]: And that allows you to use smaller and smaller models. Right? Because the smaller models can only handle a fewer number of tools. And then being able to Write these little tiny bespoke tools lets you do things like Like, OK, look at the pedantic way, right, here's what pedantic would do. Greg, you, you know this, pedantic would have the model build adjacent object that has an entry for every section.

@Greg [26:56]: Mhm.

@Vinnie [26:58]: Right? So the bigger the paper, the more complex you're asking the model to build adjacent object, and the bigger the jason, the better the, the more is the chance that it's going to screw it up, like it's going to miss a comma, or it's gonna forget to quote something, right? Like, there's risk, and then pedantic requires that the server have support for it. Like you have to put some shit in the server to like filter the logics, whatever that means, but it costs, it can tax the model up to 30% performance.

@Greg [27:12]: Yeah.

@Vinnie [27:27]: So instead, Of doing all that bullshit, instead of having to return this giant adjacent object. Instead we have little individual tool calls that accumulate the results into a table. Isn't that better?

@Sean Parsons [27:41]: Yes sir.

@Vinnie [27:43]: And then when it's done, And then we go to the next section. Guess what? Now we have Whatever it is, the ranges. See that? ranges.

@Sean Parsons [27:55]: So flipping over the sections, right?

@Vinnie [27:58]: That's right. So now we fan out and each, each, each arm of the fan gets one of the ranges. See, that item is each is item becomes the element from ranges. All right, so now, What were we talking about?

@Vinnie [28:17]: We were talking about the model. So every time you do, every time you submit a chat, It's that's called a model turn. And the event, the messages that it receives gets bigger and bigger. And You can't change the tools.

@Vinnie [28:36]: Like once you offer a set of tools, you have to leave it that way, because if you change it, like if you remove tools, the model is going to get confused because it sees the history, like it's like, wait a minute, I was able to use that. I was using that tool like, you know, for like 5 times, and when and then you take it away and then now I can't use it. Now it's gonna get errors. It's not, it's gonna, things are gonna get weird.

@Vinnie [28:59]: Get what I'm saying? Like if it uses the same tool 5 times in a row, Then the chances are very good it's gonna keep using that tool because it's built up priors, right? It's like. It's gonna be very reluctant to wanna switch tools, so

@Vinnie [29:16]: Generally speaking, the tool tool insertions have to happen early. And they, you can't remove them from the From the context.

@Sean Parsons [29:25]: And Vinny Do you add? All of the tools at once, or as like you understand the problem, like the separation between the harness and the LLM like. Do you define all the tools at once?

@Vinnie [29:39]: Great question. So, In the H1 section is where you have to import all the tools that you could possibly use. So, it has to know what tools it can possibly use. And then in each H2, then you then you add the tools that you want to allow the model to use.

@Vinnie [29:58]: Which could be nothing. Right, like over here. There's no tools allowed here that like this evaluate has no tools. It's pure inference. Right, this is the cool part. This is what, this is why we like prompt forge cause this gets rendered as markdown.

@Vinnie [30:19]: The whole, the whole payload, the whole payoff of PromptForge is that instead of looking at like a giant file that consists of lua and a bunch of shitty looking embedded strings. Here you get this beautiful markdown with bullets and right? Headings, and that looks a lot nicer. I mean, this is what we're used to, right? Is markdown.

@Sean Parsons [30:38]: Yeah, for sure.

@Vinnie [30:41]: So, in theory, you could add tools, like, for example, You could offer, like we could offer the Add section tool. We can run some inference, and then We could add another tool to it, but you would, you can't take away the ad section one in that context. Now, when you in in prompt forge, when you go to a new section, like when when control flows.

@Vinnie [31:04]: To hear, to analyze. Now everything is reset, it's a fresh VM. All the messages are gone, by the way, like when you, every time you transfer sections, that's it. The whole context is cleared. Get it?

@Sean Parsons [31:18]: So you would need to redefine any, any new things that are required for that next step.

@Vinnie [31:25]: That's right. If you wanna have tools, you gotta put them back in.

@Sean Parsons [31:26]: OK

@Vinnie [31:27]: If you want to have a system prompt, you need that as well.

@Sean Parsons [31:28]: Next. Understood.

@Vinnie [31:33]: Do you know what the difference is between a system prompt and the just the user and the assistant messages.

@Greg [31:39]: I mean, the system, well, the system prompt.

@Vinnie [31:42]: Model. Yeah, go on.

@Greg [31:45]: I mean, I feel like to the model, there's not necessarily a difference, but the system prompt is what the the harness is kind of preceding the conversation with. Of like

@Vinnie [31:59]: There's a huge difference. Let me explain the difference. The difference is pretty much that every model respects is, number one, the system prompt is a secret.

@Greg [32:01]: OK. Yeah.

@Vinnie [32:09]: The very first thing that the model is trained with is never to reveal its system prompt. And #2, Instructions in the system prompt are given priority over everything else.

@Greg [32:19]: Yeah.

@Vinnie [32:21]: That's why when you, when in, that's why when you're in plan mode. Right? the system prompt says, do not modify anything other than markdown files, and that command is strong, like it'll never get, it'll, it never gets weak. Even after compaction, that instruction remains.

@Vinnie [32:39]: That's how effective it is, is that you can't jailbreak the plan mode.

@Sean Parsons [32:43]: And how, how do you define like a system prompt versus just regular? Text.

@Vinnie [32:49]: You mean like on the wire?

@Sean Parsons [32:51]: No, like say in this. I guess I'm naively asking the question because I don't understand, but I'm understanding a little bit more. In this paper gate. MD. You know, you're defining tools and you're telling the, the model what to do, but how do you seed it with, let's say, a system prompt?

@Vinnie [33:04]: Oh. Now that's a really great question. So here you can't. Models infer prose. Is a one-shot inference.

@Vinnie [33:22]: And it's But in order to, what you need to use, you need to use this thing called model turn. And which I don't really actually know how to use.

@Sean Parsons [33:39]: Yeah, cause I would imagine you want to do something similar with Prompt Forge. So I was just kind of curious.

@Vinnie [34:09]: This is a really great question which dovetails right into one of my objectives. The Tolkien is glowing. The fuck? So, We, I wanted, I do want to set up some skills or con context files or something.

@Vinnie [34:31]: Hand-authored by humans. That Informs the model of what the fuck prompt forge is and how it works so that it doesn't have to do this every time, because right now it's like discovering, right? So these are tools, these are tool calls.

@Greg [34:43]: Right. Explore, yeah, and thinking.

@Vinnie [34:48]: Yeah.

@Greg [34:50]: Thinking is not a tool, but

@Vinnie [34:51]: Ma'am. No, it's not. I'm, I'm very excited because I'm My next set of changes, I'm gonna enable this loop. Now, now we have the model loop, that was my last bunch of commits. And then promptForge will be able to do this. OK. There's no heading level syntax.

@Vinnie [35:10]: OK. The way to give a section a system prompt is message is new. OK, so we create messages new. And then we do, we appendis, this is a sugar for a pending assistance. Well,

@Greg [35:24]: Pretty, pretty explicit.

@Vinnie [35:35]: There we go. That's it. Pretty nice. That's pretty good. That's that's pretty awesome.

@Greg [35:51]: OK, so you do it explicitly in liea then.

@Vinnie [35:54]: Yeah.

@Sean Parsons [35:55]: And his, his messages built into lure or is that something, how, how does messages get Injected into the.

@Vinnie [36:03]: That's something Great question. And Messages is one of the lua globals that the run time, by the way, we are the run time.

@Vinnie [36:23]: Prompt forge runtime seeds into every section sandbox. It's a builder factory for chat message lists. Oh shit, there's a guide? What? Whoa.

@Sean Parsons [36:39]: So you have a guide for this already. You didn't know that, did you?

@Vinnie [36:42]: Apparently. The building message list connective.

@Sean Parsons [36:47]: And. It looks like you add a type to it, like an enum or something, system user assistant tool.

@Vinnie [36:53]: Oh look, Oh my God. There. So this is the open API interface, right? Like you're in your Jason that you submit to the endpoint.

@Vinnie [37:10]: You, you tag the message with role equals user. Or role equals assistant or system, right?

@Greg [37:17]: I see. So then the, the message is colon user is sugar for for this.

@Sean Parsons [37:17]: Yeah.

@Vinnie [37:23]: Yeah. That was my idea, by the way, that the AI didn't just hallucinate that.

@Greg [37:32]: Uh-huh

@Sean Parsons [37:35]: Did Cursor did cursor take a look at that markdown file and basically

@Vinnie [37:35]: The erased.

@Sean Parsons [37:42]: Give you a response based of that markdown, or is it actually thinking outside of the context of this markdown file.

@Vinnie [37:42]: Yes. No, no, no, I, you, you can see what it did. Look. It you can, you can check its work, thought briefly. The user is asking what messages is, and then, oh, now see that, you see this from 06 models MD.

@Sean Parsons [37:58]: OK. Yeah.

@Vinnie [38:02]: Now, Let me explain. This There's a lot going on here. This is why I use cursor and not clogged code. Why? Because cursor builds a rag index of all the files in here.

@Vinnie [38:19]: And it, when you, when you type something in, Cursor, when you, when you submit your prompt, it doesn't go to Kimmi, it goes to cursor's server, where they have their own endpoint, and they proxy the call to kimmi for you. That's why when you look in their models, like you, you can see there's only a certain list. That's why they can't, that's why you can't use astra. So cursor's server takes takes what what you wrote here, and it adds additional context, like it'll look up the rag index, and it puts little pointers. It says,

@Vinnie [38:53]: It like, it knows it, it like it'll, like before it submits this to Kimmy, it'll say, Here's a list of all the files that mention prompt forge and messages. It adds that. And that's why it knows right away. It's like from 06 models MD. Like, how the fuck did it know that? There was no tool call here. Where's the tool call?

@Vinnie [39:16]: What's the tool called? Where is it? There's no tool call. It never did a grip. How'd you get that file name? There's only one way, came from the rag index. Well, then why don't we see it? Because it didn't happen on Kimmy, it happens on their server, and they don't reveal it.

@Vinnie [39:33]: But we can see the effect, get it?

@Greg [39:38]: Yeah, interesting.

@Vinnie [39:38]: So the the the prompt goes from here to the cursor server, they enrich the prompt with additional context, they send it to Kimmy. And then it comes back. They make sure they edit the message to not reveal any trade secrets, and then it comes back to you.

@Vinnie [39:56]: That's why if you change the model, if you put your own model, like if you put Deep seek, or you put, you know, our own or a local model, you're gonna cripple cursor, because they will not allow. They will not allow their enriched prompt to go to your local model, but then you could see everything that they're doing. Then you would, we could just extract all their techniques.

@Vinnie [40:17]: So, I have to reverse engineer what cursor is doing by looking at its behavior.

@Sean Parsons [40:23]: Gotcha.

@Vinnie [40:25]: So, Now, it knows, oh, OK. Oh, let me check if there's more detail maybe, and oh wow, fuck you, that's good. Let me tell you, man. Without I'm, I'm, I'm, I'm gonna be in for a sobering awakening, because the first version of my harness that is tool enabled.

@Vinnie [40:46]: It's gonna, it's gonna be in theory, it's gonna be able to do these things, but the results are not going to be anywhere near it because it's not gonna, it's not gonna see models MD. It's not gonna see that. It's gonna be gripping like forever. It's gonna, it's going to be looking through it, it's going to fill the context up, it's going to be very inefficient.

@Vinnie [41:02]: Right? And then, We're gonna have, then we're gonna enter the phase of optimizing our harness. That's where we're gonna like, could be like, Vinny, how can I optimize the harness? There's no logs. Oh, we gotta add logging. OK, now let's look at the log. Oh, why did it do this? Why did it do this? Why did it call Grepp 200 times, blah blah blah. Let's fix this and formify hypothesis. How can we make it better, right? That's harness, that's called harness engineering.

@Vinnie [41:27]: So, Look, there he did the grip. Look, you could see the result. You see that little pop-up? That's actually pretty nice. See the UI

@Greg [41:40]: Mhm.

@Vinnie [41:43]: So, one of the rules of the UI, one of the invariants of the UI is that we have to make sure that the user can see everything. Now, they did it with the pop-up, and I, I, I, I don't, I don't know that that's wrong. Another an alternative would have been it to give it like a little carrot, right, to unroll.

@Vinnie [42:01]: Mhm But if you do that, then The JavaScript starts getting, the JavaScript and the HTML starts getting pretty big, right? Cause that's what this control is. It's an HTML control. And it's the same in PromptForge. It's HTML. It's served the promptForge interface is served by an HTTP server, and then it's shown in a browser panel.

@Vinnie [42:26]: Thought briefly.

@Sean Parsons [42:28]: Is it, is it like an electron application or something?

@Vinnie [42:31]: No, it's Atari app.

@Sean Parsons [42:34]: Oh, Atari, OK.

@Vinnie [42:34]: What. Yeah. All right, so, So now you're getting it, right?

@Sean Parsons [42:43]: Well, certainly a lot more than I was, yeah.

@Vinnie [42:45]: Yeah, that's how this shit works. OK, questions.

@Sean Parsons [42:53]: Not necessarily right now. I've got a lot more context though. I feel. A lot better about it.

@Vinnie [43:01]: Good. It's ambitious, but the AI is helping me. And what was this? Oh, OK, all right. So,

@Greg [43:05]: Mhm

@Vinnie [43:09]: Yeah, so on the skill side, it's kind of a mess. I don't know what to do, but one thing is that we could do is we could just have a file in here. That has all the rules, that has, that explains how prompt forge works and just loaded into a context, right? Like, like how I've got like the reports rulebook.

@Vinnie [43:30]: You know, just load it in. OK, so I was gonna show you how I was gonna fix the Talktron updates. Fuck. Oh,

@Vinnie [43:50]: Yeah. Skills on. Always is.

@Vinnie [44:06]: Why is my why is this thing so oh there we go. Pretty much garbage. OK, commit compliance, yes. So I just so I discovered

@Vinnie [44:23]: So I realized I forgot Rush's rulebook. So, the purpose of this huddle. Is to show you my process. For what I'm, how, what I'm going to do about it. And you can compare it with how you work. I'm not saying this is the only way to do it. I'm just saying this is how I did it. So I realized I'm like, oh shit, I forgot the rust rulebook. OK, what's the damage? All right, well, let's look at the top 150 commits.

@Vinnie [44:51]: Oh, it did it. 78 deviations. 43 compliant, well, that's good. So, Recurring deviations, Notable one-offs. OK, so the next thing I did is, should we really fix them all?

@Vinnie [45:08]: And thankfully, Kimmy K3 is pretty sensible. No. All right, so tier one fixed these for sure. Tier 2 fixed opportunistically, but I figured let me just do that as well. Tier threes or don't fixes.

@Vinnie [45:24]: Tier fours or defers. So like we have a lot, we have a file that's at almost 5000 lines. We're gonna have to deal with that. So I said, let's fix everything in tiers 1 and 2. Nice, and I went to plan mode. Ding ding ding ding ding. Oh, here, now we got a plan. We know we love these plans.

@Vinnie [45:44]: So, Then I want, since I'm gonna commit the plan into the Repo I want to make sure that we we capture the deferred work. So I said, add a deferred work stream item.

@Vinnie [46:04]: Deferred. Oh well. That needs to be better, that could be better. Not happy with that.

@Vinnie [46:21]: OK. You should see it. Edit, come on, edit. All right, so, I'm not so happy with the format of this plan.

@Vinnie [46:39]: So then I asked, I said, can we do a very light adoption of architect? Oh, there we go. Wait, no, no, we didn't. Execution instructions projects are in regular testing technically, OK. Oh,

@Vinnie [46:58]: I don't see it. What's Happening here.

@Vinnie [47:23]: Hm There we go, OK. OK, so now we, that's, these are, cause we need to come back to this. And then

@Vinnie [47:42]: So, I did a light adoption of architect. So he said, Adopt a self-containment. Add a decision record. In-place consolidation instead of appendon edits.

@Vinnie [48:01]: Good bounded evidence readers. Oh, we already did it, OK. Don't do the contract tags. Actually, I like the contract tags. Oh, it didn't want the whole template. OK.

@Vinnie [48:20]: OK. All right. Can we add the mandated sections, but make their contents expository instead of bullets. Well, it did what I asked. Look at that. There's your expects position, but this, can we agree that this sucks? Like, nobody wants to read this.

@Vinnie [48:42]: It it it did add product requirements. Let's see what it did here. 150 commit audit. Found 78. 0, this is very good, actually. That's a very good, this is a good explanation. If, if, if I wasn't around and you read this, would this be helpful?

@Greg [48:59]: The first sentence, yeah.

@Vinnie [49:02]: OK. So, Now we're gonna, so I'm gonna go into ask mode. And I'm gonna say, All right, listen, I, I, I asked for exposition, but you just put, you just did an entire paragraph, and one enormous paragraph per section. You need more structure than that full.

@Vinnie [49:25]: Break up those enormous paragraphs. Into Into smaller paragraphs and consider whether or not you should use bullets in some places. What do you think? Go over each level 2 section, and tell me how you would soften it up so that it's easier to read by a human.

@Vinnie [49:44]: Motherfucker. There. Is this how you work?

@Greg [50:01]: I don't usually say motherfucker at the end, but

@Vinnie [50:06]: Fair. One wall of text it defeats the point. Currently, I'd keep a short prose paragraph. Then break the rest into bullets. Oh, I love, I love it. Functional spec, keep the actor workflow. Oh yeah, hey, that sounds all nice.

@Vinnie [50:26]: OK. Hey, that's pretty reasonable. But you see, I got the model to pre-commit what it's gonna do, and then I can audit it, right? See, I went into asthma, oh, wait. I went into ask mode.

@Vinnie [50:44]: So ask mode forces it to Explain what it's about to do. I flip back and forth in the mode a lot.

@Vinnie [51:01]: Oh, Hey, hi, is this better? Did this get better? What do you think?

@Sean Parsons [51:07]: Let's take a look.

@Greg [51:09]: Better. It's about 1 quarter of the Length

@Vinnie [51:14]: So the first paragraph is good for you.

@Greg [51:18]: Yeah. At first glance, it looks good.

@Vinnie [51:23]: OK, what about functional spec? The actor is a maintainer. Yeah, it's not wrong. Oh, accepting.

@Sean Parsons [51:36]: The content still breeds pretty AI but

@Vinnie [51:41]: It is what it is, man. Should I try to fix it?

@Sean Parsons [51:48]: Well, it's still an improvement over the previous one.

@Vinnie [51:52]: I think as long as we can read it, like, If, if, as long as someone can look at this code and figure out, oh yeah, and see if it makes any sense. Cause like the purpose here is that is we need to look through it. And make sure that the AI is not doing anything stupid.

@Sean Parsons [52:18]: But I think that requires also understanding.

@Vinnie [52:24]: Sorry, you got cut out. What?

@Sean Parsons [52:28]: But like for us to be able to evaluate whether it's doing anything stupid or not. I think we need to understand the The code base a little bit better also, right?

@Vinnie [52:40]: Yeah, well, OK, so let's go through it. You understand that?

@Sean Parsons [52:51]: No, that, that entire sentence. It's nice that it points to a specific file, but

@Vinnie [53:01]: And.

@Vinnie [53:17]: Motherfucker. Yeah, look, I have to be honest. I don't understand half the shit either.

@Greg [53:28]: Hm.

@Vinnie [53:28]: It is that this is an ongoing problem is that the AI will say the unused def dependency is gone, and I'm stroking my chin thinking, well, that sounds good. Now, what's a depth dependency? Oh, OK, does this help?

@Sean Parsons [53:46]: Which part, the part on the right?

@Vinnie [53:47]: Yeah, this thing, plain English. So we're trying to understand, no, we're trying to understand. I guess no drop.

@Sean Parsons [53:57]: No drop.

@Vinnie [53:59]: Is it? What did we What what was the highlighted text? Was it the no drop? No, no, here, yeah, this, this thing.

@Vinnie [54:18]: Blocking drops are replaced with explicit fallible shutdowns and non-blocking drops. Well, I know, I know blocking is probably bad. If we're doing network.

@Greg [54:29]: Mhm.

@Vinnie [54:34]: Oh, One of them makes a network request. Yes, I'm familiar with this anti-pattern.

@Sean Parsons [54:58]: So it looks like the the destructors.

@Vinnie [55:00]: OK.

@Sean Parsons [55:02]: Or going from a blocking to a signal-based approach, kind of like can go with like. A channel I mean, I think that makes sense.

@Vinnie [55:10]: Actually, no. What it's doing is it's adding an explicit shutdown method, and the requirement is that you have to call that before letting it destroy.

@Greg [55:21]: So it doesn't get to decide on its own.

@Vinnie [55:24]: The drop bodies are reduced to signal and detach. Oh, doc comments state that the explicit method is the blocking path. Oh, that's good. So that means that when it writes new code, it will know.

@Sean Parsons [55:42]: I mean, overall, conceptually it sounds good, but You don't have to go through this with A fine tooth comb to Make sure it all makes sense.

@Sean Parsons [56:09]: Oh, so the shutdown method would get passed into something and then it owns calling shutdown or what?

@Vinnie [56:09]: Well.

@Sean Parsons [56:17]: I'd have to take a look at the photo.

@Vinnie [56:17]: What who whoever owns, whoever owns the object, like wherever that object is used, shutdown would have to be calm.

@Sean Parsons [56:24]: OK.

@Vinnie [56:30]: Oh.

@Vinnie [56:54]: Oh boy.

@Vinnie [57:17]: I mean, I'm just gonna have to do it, trust me, bro. So my thinking is we're going to hire 2 more people that know Rust really well. And we're going to set them to the task cleaning up the slop.

@Greg [57:30]: OK.

@Vinnie [57:35]: So that's number one. 2, I'm going to try to learn. I'm gonna, I'm gonna find the boundaries of these crates. And I'm going to identify what's important. Like we know the executive interface is important, right?

@Sean Parsons [57:51]: Yeah, is that, is that part of the harness?

@Vinnie [57:51]: They're called the. That's what we call the runtime. That executive run. There's no harness there at all. That's that that executes the prompt. It's up to the harness.

@Greg [58:01]: Yes. Yeah, it's, it's just like interpreting and running the, the prompt itself.

@Vinnie [58:10]: Exactly. Run, run, run to here, let's look at it.

@Greg [58:26]: And execute that. RS, yeah.

@Vinnie [58:29]: OK. Like this is the function.

@Greg [58:37]: I have no idea what the 1st 216 lines are doing, by the way. I don't know if I should.

@Vinnie [58:37]: This is it. Comments Oh, you mean this stuff?

@Greg [58:43]: Well, that's, yeah, it's just like

@Vinnie [58:47]: There's like imports and exports.

@Greg [58:49]: OK. OK.

@Vinnie [58:52]: And like This identifies. It's a bunch of bullshit.

@Greg [58:58]: OK.

@Vinnie [58:58]: I let the AI figure that shit out.

@Greg [59:01]: OK.

@Vinnie [59:01]: But they're like imports and exports. But this is the main function. So this is how you execute a prompt. You pass the prompt.

@Greg [59:04]: Yeah, yeah.

@Vinnie [59:09]: Right? You pass the arguments, the the one string that you're allowed to pass in. Resolution context is where it gets all the tools and the models. And then the store Which has like that virtual file system in it, and then the run config, which has everything else.

@Vinnie [59:30]: Context for the run. And then this runs it.

@Greg [59:34]: The run config has things like what model?

@Vinnie [59:35]: And it's

@Greg [59:37]: To do inference with and

@Vinnie [59:41]: It's a great question.

@Sean Parsons [59:56]: I think you could do a jump to on that run config right to go to the file.

@Vinnie [1:00:03]: There. So,

@Greg [1:00:10]: I feel like I've looked at this before, but

@Vinnie [1:00:12]: Oh yeah, yeah, yeah, right. So, We, you set the, you can set the observer. So the observer is an object that the caller creates. And The while while the prompt is executing, the observer gets called a lot with everything.

@Vinnie [1:00:32]: Every little thing that happens, the observer gets to see. The observer is how we show the streaming result. Like when you see like the, so, to the lua. The the the model's response arrives as a single complete message, but to the user in the workshop, you could see the words like at the tokens as they're generated, right?

@Vinnie [1:00:53]: That's the observer. The observer can see the the data as it's streaming in. The observer can see like when there's a tool call, the model can't see the tool calls. It knows that they happened, but it can't observe them as they're happening. The observer is how we're gonna implement, you know, all this bullshit that happens in the chat, like when it makes a mock, when it does a tool call and

@Vinnie [1:01:17]: That's what the observer's for. And then the observers also for like recording, making, making a keeping a log of everything that ever happened during the run of that prompt. So when we implement debugging, Like what, like when we implement the ability to like, to put a prompt in the prompt forge debugger, it's gonna be a custom observer that sees all the events.

@Vinnie [1:01:38]: And then the debugger will have like a little window with a lot with the list that you could click on and you could say, oh, I wrote this file, oh, what's in it? And then you can expand it and say, oh, there, there it is, and you could like see it, you could see what happened in the run. You see why that would be useful, right?

@Greg [1:01:52]: Yeah, for sure.

@Vinnie [1:01:55]: Well that's the observer. And then So then there's then you have to choose the gateway client, like the the the the runtime needs a gateway. Or else they can't really do much. Then there's a cancellation handle.

@Vinnie [1:02:14]: So, like, if you press stop, Right, you know, we need to stop it. There's we could set resource limits. Oh, the host policy behind user input. Oh, that's interesting. So, the user input to command, the user input function in lia.

@Vinnie [1:02:35]: It it will it calls this object. Because prompt forge executor can't depend on workshop. So the way the workshop works is when it installs a handler. The when so and then it knows when it knows when the When the prompt calls user input, so now the prompt is suspended. It's an asynchronous object, it's suspended, and then the workshop gets the message, and then it, now it unfreezes the edit box.

@Vinnie [1:03:03]: Right? Hm. Like when you submit, when you submit the prompt, Like the The voice input box gets disabled and it gets replaced with like a stop button. See the stop button?

@Sean Parsons [1:03:18]: Mhm.

@Vinnie [1:03:18]: And then, and then when user input gets called. The UI changes again. The stop button goes away, this comes back, this thing, you could put it, you could put the cursor back in here or whatever. The UI So,

@Vinnie [1:03:35]: This is a hack. Yeah, that's a little hack. So there's a UI I'm injecting this thing into the lua called UI. And it only has one member, the currently selected model. So that's how the chat can synchronize the model that it uses with what you're choosing from the dropdown.

@Vinnie [1:03:55]: But this could have other things too, like it could say like what what what's the list of windows that you have open and what are the folders on the side, and how many terminals do you have? Like that that object can hold all those things. So then you could write an agent that exposes that. To the

@Vinnie [1:04:14]: To the prompt, right? Like that's that's what cursor does. Like cursor. Injects into the into your prompt without you seeing it, it injects this list of what terminals you have, and it gives it tells the model, it says, the user has 6 terminals, and here's how you can find out their contents, and it gives like a pointer.

@Vinnie [1:04:33]: To, and then if the model wants to, it can read it. For example, See that LS Kaka? Now I can say, why did my Terminal get an heir. Huh, why did my terminal get an error?

@Vinnie [1:04:51]: Oh, what's that? Oh, shit. List recent terminal state files. Oh, Hm, very interesting. Oh, Kaka, how the fuck did it know? How did it know? How did it know? There's only one way. Cursor injected information that that tells the model about what its environment looks like.

@Vinnie [1:05:13]: Right?

@Greg [1:05:14]: Mhm

@Vinnie [1:05:14]: See how that works.

@Sean Parsons [1:05:17]: For sure.

@Vinnie [1:05:20]: Get Oh, interesting. So look, it, it issued a powershell command. I should check the terminals folder for recent terminal output. So there's a, so now, so now we're reverse engineering the cursor harness, right?

@Vinnie [1:05:37]: Your most recent, so it decided to use fucking, by the way, this is PowerShell. Like think, look how, look what in I, I fucking hate whoever did this. Get child item? What the hell is that? Get child item? Are you serious? That's the command in PowerShell.

@Vinnie [1:05:55]: Thank you. So, Is there any coffee by any chance? Yeah, oh, we ordered them. I think it's here. OK, so, That's why I'm using bash kit, by the way, so that no matter what system you're on,

@Vinnie [1:06:12]: The harness always thinks that it has access to a bass shell.

@Greg [1:06:13]: Mhm

@Vinnie [1:06:17]: And then, oh, what's this? What the fuck is this? cursors Vinny, so the terminal terminals are all actual files on the file system. And it just appends to it. So that's how, so, it uses the physical file system as the place where it echoes the terminal.

@Vinnie [1:06:41]: Now you know what I'm gonna do. I'm gonna use a virtual file system. And So, and then I'm gonna put, I'm gonna inject the harness my harness will inject into the prompt. It'll say, the terminals are here, and then we'll have like

@Vinnie [1:06:59]: Backslash Slash prompt forge, terminals. You know, like, some number. And then output. MD or TXT, right? So that'll be like, you know what that is, but that file won't exist, it'll just be in the database.

@Vinnie [1:07:17]: And then, now and then we're using bash kit, right? The it's a like a ver it's a sandbox shell, and Bashkit lets you map virtual files, so I can give bash kit and a configuration that routes everything that's in that starts with prompt forge, route it to my own handler, and then my handler.

@Vinnie [1:07:38]: It like parses the path, and it knows that with its terminals, that this is the terminal ID and that this stem means the terminal output, and I can map it, and I can return it. So, the model thinks it's exploring a real file system, and it'll do exactly this, but using bash commands, and it'll all this will work, and I get that all for free by just mapping it.

@Vinnie [1:07:59]: Into the file system that's in Bashkit, and then there's no actual files on disk, so it's all clean. And the user can't fuck with it, like they can't go and delete it, which would mess it up. What do you think of that?

@Greg [1:08:17]: Sounds like a reasonable approach. I I've never really worked with Virtual file systems like this, but

@Vinnie [1:08:26]: Well, it's, it's not.

@Greg [1:08:26]: I think it gives us the control we need for like the having our canonical chat. MD and

@Vinnie [1:08:36]: So to be clear,

@Greg [1:08:36]: Something the user can

@Vinnie [1:08:38]: The virtual file system is, is just a, it's a design pattern, right?

@Greg [1:08:43]: Yeah.

@Vinnie [1:08:44]: Creating a file system. But it doesn't map to the real file system. And In our file system, There's gonna be an extra field, like in addition to file name, size, last modification, creation date.

@Vinnie [1:09:02]: Read only versus write only permissions. We're going to have one more field, we're going to have. Description So, we're gonna be able to attach a description of what the file is. So then with the model, when the model does like LS like when it does like, you know, like Ellis prompt forge.

@Vinnie [1:09:21]: It's gonna see It's gonna see, oh, you know, like, For Or terminal, and then this will be like

@Greg [1:09:29]: We like give, give everything front matter for free.

@Vinnie [1:09:31]: Yeah. The model will see that.

@Greg [1:09:41]: Yeah, interesting.

@Vinnie [1:09:41]: And then, and then it'll know, like it'll know, oh, that's where the terminals are, and then it'll do an LS in here, and then it'll see all the little numbers, and it'll, and those, and it'll say this is a terminal session, and then it might say, this is the terminal session that the user has opened and that they're looking at, so it knows to look there first.

@Greg [1:10:06]: That's cool.

@Vinnie [1:10:06]: This is all I just made all this shit up, by the way, like I, I.

@Greg [1:10:10]: I like it.

@Vinnie [1:10:11]: It's a good idea. I don't know if it's gonna work. It's all speculative, could backfire. Could like not work.

@Greg [1:10:18]: It's, it's Seems like it would be pretty helpful for an agent trying to like explore a code base. We're like in this case we're not exploring a code base, but just like understanding what what is where without actually having to read into the file.

@Vinnie [1:10:36]: Sean thoughts

@Sean Parsons [1:10:39]: Yeah, I'm still trying to understand the virtual file system in general, Cause if it's not stored in the system, I, I saw like using SQL Light DB or Taurus or whatever, so I'm still kind of just trying to understand.

@Vinnie [1:10:54]: OK. You know what a regular file system is?

@Sean Parsons [1:10:57]: Yes.

@Vinnie [1:10:58]: So imagine you create an an abstract interface, right? Like one of those ABC's.

@Sean Parsons [1:11:04]: Yeah.

@Vinnie [1:11:05]: And you say, I'm gonna write a program that that accesses files in the file system, but instead of using Python standard library, I'm gonna go through this API for everything. So if I want to open a file, I go through this API. If I want to show the contents of a directory, I go through this API get it?

@Sean Parsons [1:11:24]: Got it.

@Vinnie [1:11:24]: So now you implement Now you can implement the real file system underneath that, you just map. Every function to its corresponding standard equivalent, right?

@Sean Parsons [1:11:34]: Got it.

@Vinnie [1:11:36]: So, but now you say, now I want to overlay. Now I want to make a directory called_promptForge. And I wanna, and I wanna map that. So that any time any commands are run that have this at the beginning of the path, instead of going to the real file system. I want to just call my functions and I want to put some art, I want to synthesize, I wanna put artificial stuff there.

@Sean Parsons [1:12:02]: That is actually Not stored anywhere, whereas Where's that information?

@Vinnie [1:12:10]: It's however I want, I can make it up however I want. For example, let's say I make a directory called prompt for slash help. And then I can have a catalog of of files, like, you know, like using prompt forge.

@Sean Parsons [1:12:19]: Mhm.

@Vinnie [1:12:25]: But that file doesn't actually exist anywhere. Maybe it's like, it's embedded, it's an embedded string in the executable.

@Sean Parsons [1:12:25]: Mhm.

@Vinnie [1:12:31]: Right? So then,

@Sean Parsons [1:12:32]: Yep.

@Vinnie [1:12:33]: In my in my overlay, when I see that the path matches this text, then instead of going to the real file system, I deliver my hard-coded string.

@Sean Parsons [1:12:43]: OK. That makes sense.

@Vinnie [1:12:47]: And but the model, the model doesn't know. It thinks that it's, it's like it just thinks it's a file. And what's great about this is it can use grip, like it can be like, oh, the help is here. Let me grab through all the files in this directory recursively, and it'll work because Bashkit implements all of its tools in terms of the virtual file system, we get all that for free.

@Vinnie [1:13:13]: Bash kit comes with grip. Hm.

@Sean Parsons [1:13:19]: But it would work even if it's embedded into the PromptForge application.

@Vinnie [1:13:26]: Yes, because we've implemented the virtual interface. So from Bashkit's perspective, Bashkit doesn't care where the data is, it calls your API to find it. So, if your API passes it through to the regular file system. Normally, or it when if it matches the overlay, then it then it calls your other function, then Bashkit doesn't care. You've abstracted access to the file system. In other words, you've made it virtual.

@Vinnie [1:13:56]: This is really good to know because I thought that this was just like obvious. I didn't realize that this was a non-obvious approach. I guess it's because of C++. Like in C++, abstraction is the norm. Like you create these virtual interfaces, and then the implementation can change.

@Vinnie [1:14:13]: And so you don't know. So all that you're, so when you write your code, you write it against an abstract interface. You know, open this file, close this file, read these contents, and then then you don't care where the actual data lives, right?

@Vinnie [1:14:29]: Greg, do you get it?

@Sean Parsons [1:14:29]: Yeah, they Yeah.

@Greg [1:14:31]: Python does some of the same stuff, but it's, I don't know, like, it's rare that, I guess for like, I don't want to speak for Sean, but I, I think this is probably true for Sean too, like, we're generally, like, using abstractions without really understanding what's going on under the hood as much. I've, I, I've written plenty of abstractions, but not at the like, I don't know, just the file system munging stuff like I, I, I don't.

@Sean Parsons [1:14:51]: Yeah.

@Greg [1:15:01]: With that usually just take something off the shelf.

@Sean Parsons [1:15:03]: Yeah.

@Vinnie [1:15:05]: And to be fair, like, having a Having a virtual file system abstraction implies that you have written a large set of tools that use it, right? Like, because just having the abstraction is not enough. Now you have to, you have to implement like every little tool. You get what I'm saying? Like you need LS, you need cat, you need rep, you need RG, you need the shell when you do like when you pipe and you go to X. TXT like that has to work. Everything has to work, so this, you know, this is not something that you would encounter in your day to day.

@Greg [1:15:17]: Right. Yes.

@Sean Parsons [1:15:26]: Yeah.

@Greg [1:15:28]: Yeah.

@Sean Parsons [1:15:38]: Right.

@Vinnie [1:15:39]: Because But however, but look at look, Bashkit did the work for us.

@Greg [1:15:44]: Right.

@Vinnie [1:15:46]: Bashkit did it. And it's beautiful, and he had his last commit was 14 hours ago. And like this guy's working for us. He's doing the work. Let's see what they've got.

@Vinnie [1:16:02]: Secure by default, no process spawning. No file system access, I love it. Dude, look at that number. 167 commands.

@Greg [1:16:19]: Yeah.

@Vinnie [1:16:21]: Look at that. In memory file system, that's the store, overlay file system, that's the prompt forge, mountable file system. You can mount network drives, you can, you can mount a a local directory anywhere into the virtual file system. It comes with the real FS back end.

@Vinnie [1:16:40]: Resource limits. Remember what I was telling you about like if you do it, if you show the contents of a directory and it has, there's 10,000 items in it, you don't want to just dump all that into the context. It has, it has resource limits for every one of those 166 7 commands built in. And look, you see that parser fuel? That means that when a limit is reached, it outputs useful text to the model. It says, sorry, I truncated. If you want more, here's how you do it.

@Greg [1:16:49]: Mhm.

@Vinnie [1:17:11]: Look at that. LLM tool contract. The whole, the thing was like, it's like, it's what I, it's what the, it's what Kimmy said. It said it is unusually suited for grumpforge. I don't know what's going on here, but that's fucking annoying.

@Greg [1:17:17]: Yeah, it's like it was designed for us.

@Vinnie [1:17:27]: Sean, do you understand everything that's being said here? You need to understand this. To read it and.

@Sean Parsons [1:17:33]: I understand. I understand most of the conversation that we had, I think this has been a helpful. Introductory call. I understand PromptForge and AI in general more across the board. I'm taking a look at Bashkit.

@Vinnie [1:17:48]: I.

@Sean Parsons [1:17:51]: The GitHub repository now and trying to take a look at. Like what it offers and things of that nature. The file system things I kind of understand, but not in the context of how Not in the context of AI, so I understand virtual file systems and things of that nature.

@Sean Parsons [1:18:10]: But like how we plan on using it and how it could be useful in the prompt forage context, I think is maybe where I'm. Maybe lacking or missing a little bit.

@Vinnie [1:18:22]: Let me come at it from a different direction. When you invoke a model, like when you call into an AI. Like, it's just text in, text out.

@Sean Parsons [1:18:38]: Mhm.

@Vinnie [1:18:40]: Even if you paste an image, The image is converted into base 64. And then the and then the image is tokenized, and it's presented as text. It's basically a one-trick pony. Somebody wrote that paper, attention is all you need, and then that one construct is powering the entire AI revolution. A string goes in, a string comes out. Even the audio is turned into is turned into tokens, like they're like little, they're like little like 15 millisecond Fourier transform tokens.

@Vinnie [1:19:13]: But they're tokens, just like text. You know, the fact that they're encoded from audio data, the model doesn't really give a shit. It's the same operation being performed over and over again. The training exactly the same for everything, it's all the same. So,

@Vinnie [1:19:30]: If you wanna create the illusion of something. Then you have to give the model that something. Right? So, you're creating a world for the model. Now, you could model the real world, you could sample stuff that's happening in the real world. Like, you could measure the temperature, you can measure the wind direction, you can take screenshots, you know, from a camera, you could take all that and then you could feed it into the model.

@Vinnie [1:19:57]: Now, But that's it's that's curated. The model is not really interacting with the world, it's just being presented with some sample data.

@Sean Parsons [1:20:04]: Mhm.

@Vinnie [1:20:04]: Well, it's the same, it's the same for the file system. The model can't doesn't really know what's there, you know, it doesn't know what the files are. Everything that you want the model to see, you have to give it. So what does that mean? That means you could give the model, you could say, hey, here's your directory. Like I can give the model, I could say,

@Sean Parsons [1:20:16]: Mhm.

@Vinnie [1:20:24]: Let's say I've got users Vinny. You know, my stuff, right?

@Sean Parsons [1:20:28]: Mhm.

@Vinnie [1:20:29]: Down here. What I can do is I can map that to the root, you know, about CH root, you know, that shit, right? You know what I'm talking about.

@Sean Parsons [1:20:37]: Yeah.

@Vinnie [1:20:39]: I can I can map this directory to the root, and then I can give it to the model with a set of tools, and now it can explore everything that's in here. But it can't escape. It can't go up a directory, because the tools simply don't allow it. So from the model's perspective, its entire universe consists of a file system that's rooted in the what in the actual contents of what's here.

@Sean Parsons [1:20:48]: Mhm. Right. Mhm.

@Vinnie [1:21:02]: So I've created a sandbox, right?

@Sean Parsons [1:21:05]: Right.

@Vinnie [1:21:07]: Well, you could take it one step further. With Bash kit, you don't even need a real directory, you could construct a synthetic directory. And you can give it at least a little tiny set of files, and you can say, this is all you get.

@Sean Parsons [1:21:22]: And you can add on to that. Sandbox as the conversation. Expands or grows, but you can keep it isolated.

@Vinnie [1:21:32]: Yeah, well, it's better it's Changing the sandbox is usually not a good idea because If it's, if it, if it does a model turn and it sees like something's available, and then it's gonna expect that thing to stay available cause it pattern matches. So if it later becomes unavailable, then you can, the model can get confused. It can be like, wait a minute, that shit worked, and now it doesn't work, and I'm not and and it's not explained to me why.

@Sean Parsons [1:21:44]: Mhm. Right. I meant more adding to it. So like,

@Vinnie [1:21:58]: Yep.

@Sean Parsons [1:22:00]: Like, If they want to reference a file, so you know how you can reference like a file. When you're having a conversation.

@Vinnie [1:22:09]: Yeah.

@Sean Parsons [1:22:10]: Would that, would this sandbox.

@Vinnie [1:22:11]: OK, you in here like that thing.

@Sean Parsons [1:22:13]: Yeah. Like, would you add?

@Vinnie [1:22:16]: Like that.

@Sean Parsons [1:22:17]: That file like using this kind of virtual file system thing, would you add that file into that sandbox layer? And maintain that sandbox layer with only the files that are necessary for the for the model to do what it needs. Is that the overall objective?

@Vinnie [1:22:28]: Yes So that's a great question. Now, obviously, what you're describing would be very safe. So what you're describing is opt-in permissioning, right? and then it's contextual, so the it's the, so with the harness, what you're proposing is the harness gives the model the minimum permissions at all times, and then everything that it needs to access, it has to come from a grant.

@Sean Parsons [1:22:55]: Mhm.

@Vinnie [1:23:00]: Like some user action or some configuration where it's expressly allowed. Now, everyone remembers when they first started using their favorite IDE how it keeps asking, do I have permission for this? Do I have permission for this? And, you know what I'm talking about. And then, how long did it take for you, how long did it take before you finally said, you know what, I'm, I'm over this shit. Allow all.

@Sean Parsons [1:23:04]: Mhm. I. Yeah.

@Sean Parsons [1:23:21]: Yeah, pretty quickly.

@Vinnie [1:23:23]: Right? So that's what you're describing.

@Greg [1:23:25]: Pretty quickly.

@Vinnie [1:23:27]: So, So, I trust The frontier models pretty, pretty well. Like, I'm pretty trusting of the frontier models. I've had, I've had allow all on, and they haven't done me wrong yet.

@Vinnie [1:23:43]: Here's where I would have some caution. Smaller models. Those, maybe we don't allow all of those.

@Sean Parsons [1:23:48]: Mhm.

@Vinnie [1:23:54]: We gotta be very careful when we use a small model. Because, you know, It's grasp of the English language is not as nuanced.

@Sean Parsons [1:24:03]: Mhm.

@Vinnie [1:24:05]: Like you wanna say, I want to erase these bugs. Well, it'll go it might do something you don't like. The frontier model will have no problem with that, right?

@Sean Parsons [1:24:14]: Yeah.

@Vinnie [1:24:17]: OK

@Sean Parsons [1:24:17]: Mhm.

@Vinnie [1:24:20]: OK, so, Dude, this is getting me pretty excited. Look at that. Asink first, built on Tokyo. By the way, Tokyo is the async framework that's a de facto rust system.

@Sean Parsons [1:24:30]: Yes. Tokyo.

@Vinnie [1:24:36]: Built as sync first, built from the ground up on Tokyo, I love it. Experimental git support. Oh shit. Virtual get on the virtual file system. wow, dude, that's amazing. Hm.

@Greg [1:24:51]: That's crazy.

@Vinnie [1:24:53]: Do you know what that means? That means if we wanted to do like the event system, That means we could use its virtual git to create a little virtual repository attached to your agent window, and we could just, we can make everything like commits. And then your your history in the agent window would be the commit log. That's, that's what this would allow. Look, Python support, embedded Python interpreter. Dude, the, the if the model, like the, you, this will allow the model to write a little quick Python program.

@Vinnie [1:25:24]: And run it. You ever see it, you ever see a model like write a Python program real quick to solve?

@Greg [1:25:32]: Yes.

@Sean Parsons [1:25:35]: Did we lose you, Vinny?

@Greg [1:25:39]: Hm, I think we did.

@Vinnie [1:25:41]: Sorry, like you're writing, you've you've seen, you've seen a model write Python on the fly, right?

@Greg [1:25:46]: Yes. Yeah.

@Vinnie [1:25:47]: This this would enable that, and it would be safe. Cause it runs in their sandbox.

@Greg [1:25:51]: Yeah

@Vinnie [1:25:53]: Look, type script. Oh my God, this is amazing, dude, I love this. We should buy them.

@Greg [1:25:58]: See polite.

@Vinnie [1:26:04]: Should hire these people. Who's this guy? I like him. I like how he thinks. He's Russian, he'll fit right in.

@Sean Parsons [1:26:29]: Oh, it's from, he's Ukrainian.

@Vinnie [1:26:35]: To check his politics.

@Sean Parsons [1:26:37]: Michela.

@Greg [1:26:41]: He's vaccinated. That's good to know.

@Sean Parsons [1:26:44]: It's good to know, right? Working remotely.

@Vinnie [1:26:45]: I Uh-huh.

@Greg [1:26:48]: Hm.

@Sean Parsons [1:26:49]: Wanna make sure if he sneezes on the other end. Am I right, Greg?

@Greg [1:26:53]: Yeah. Come right through the slack cuddle.

@Vinnie [1:27:02]: I think he would be good for us. What do you think?

@Greg [1:27:06]: I mean, sure. This project is pretty

@Vinnie [1:27:12]: Wait a minute, headless, durable agentic harness. Sorry, what?

@Greg [1:27:17]: Did he already build Prompforge?

@Vinnie [1:27:18]: OK. Fucking hell, 6 hours ago. Dude,

@Sean Parsons [1:27:25]: I mean, the guy does have like 18,000 commits, so.

@Vinnie [1:27:25]: No. But, oh.

@Sean Parsons [1:27:33]: Well, not that, like this past year, he has 18,000 commits, so.

@Greg [1:27:35]: Yeah.

@Vinnie [1:27:38]: Well, you know, he's using AI. I

@Sean Parsons [1:27:41]: And

@Vinnie [1:27:47]: Wow. Oh man, what is this ancient ancient builder?

@Vinnie [1:28:05]: Dude,

@Sean Parsons [1:28:08]: Like a

@Vinnie [1:28:08]: Describe an agent.

@Sean Parsons [1:28:11]: Website for it or like a, is there like a Some images.

@Vinnie [1:28:21]: I mean, this is basically The little, this is just another, this is a normal thing, man. This is not, there's nothing special here. It's just implementation, but I'll tell you what is special is if if he wrote this by hand, if it was human authored, then we could take the design patterns and we could add them.

@Vinnie [1:28:38]: Like I, I should run what to steal on this. Look, he's got the knowledge again. Harnesses. What is this? Harness types. What is this?

@Vinnie [1:28:56]: Oh, users can create custom harnesses via the API which means it's in rust. So if you want to build your own harness, you have to build it in rust, which means you need to compile. That means if you want to distribute it, you have to distribute an executable. Whereas in prompt forage you distribute a markdown file. See the difference?

@Vinnie [1:29:19]: Based system prompt. Oh, yeah. Oh, cool, an icon. Well, that's neat. That's like my, that's how I put an image in my, in my tools. He has an icon. I like that.

@Vinnie [1:29:38]: That's just like the work, the the the workshop thing. Where's that little stupid ass workshop, this thing, right? Like, Fuck. Oh yeah, see, see the little icons? These are add-ons.

@Vinnie [1:29:55]: Skin have an icon. He did the same thing. Oh, look, you the, the harnesses are can be delivered through an API. I love it.

@Vinnie [1:30:16]: Hey, What's coding Daytona? Is that a, is that a coating harness? Oh, Daytona Cloud sandbox. What the fuck is this? Do you have any idea what this is?

@Greg [1:30:36]: No.

@Sean Parsons [1:30:38]: No, it's

@Vinnie [1:30:38]: Oh, Daytona San real file system, real processes, real network for actual coding, get cloned builds tests, oh. Whoa. Follows patterns from state of the art coding agents. In other words, he reverse engineered their system prompts, like what I'm doing.

@Vinnie [1:31:02]: Dude. But of course, Bashkit, obviously. By the way, these are the rules. Infinity context, long conversation support, that means compaction. Skills, 8 skill discovery.

@Vinnie [1:31:33]: This guy is on top of it, man. We need him. Oh, fuck. This guy's on top of it. Where's this thing?

@Vinnie [1:31:53]: Well, I can tell you this. I'll be looking at I'll be looking at his code.

@Vinnie [1:32:18]: OK. That's a lot. I'm exhausted. Questions Oh, let me finish this. I have to finish this. I, I, I made a promise. OK.

@Sean Parsons [1:32:26]: No.

@Vinnie [1:32:34]: OK, you fixed it all, so this looks all right. Oh my God. OK.

@Greg [1:32:42]: So nothing has happened here yet, right? Other than creating the plan.

@Vinnie [1:32:46]: To OK, I want the vibe coder, but I don't want 30 or 40 steps. I want to keep these consolidated work stream items. I want to keep the number of steps low. I don't know, maybe what, 5 steps? How many do you think?

@Vinnie [1:33:02]: Man, I want a light execution though. I don't want to be building. I don't want to have to like do the full verify at every step.

@Vinnie [1:33:19]: The user is asking to apply the tool. I will read the tool. Now I understand. The vibe coder is a multi-agent workshop that uses sub-agent isolation. To implement the to do list. The user has asked for a light work stream. I will consolidate several of the items into see there it is the user wants to.

@Vinnie [1:33:44]: My opinion, 7 is the sweet spot. Let me think about that. My recommendation 6 steps. I like it.

@Vinnie [1:34:07]: Oh, it wants to, it wants to go beyond 5. OK, I'll I'll take its advice. Oh, contract tags, ooh. The XML tags are now mandatory, but did you know that, do you know about the XML tag technique, by the way?

@Greg [1:34:25]: Is that related to bread crumbs, or is that Something else.

@Vinnie [1:34:29]: So when When the, when the, when the LLM is orchestrating. The way here here's how you make an LLM orchestrate, you offer a subagent tool. Right? That's it. So if you offer a tool that will allow the model to spawn a sub-agent. Now you've just turned the model into an orchestrator, and it'll use it if you ask for it, and it'll, and if it's a frontier model, it'll use it.

@Vinnie [1:34:55]: Frontier models are trained in planning, right? Like, have you ever noticed that they're really good at planning like a large task, it's because they're trained. So if you offer a sub agent tool, it'll use it when it thinks that it's necessary. Well, so what do you think the parameters to the sub-agent tool are, Sean, pop quiz.

@Sean Parsons [1:35:13]: The parameters to the sub-agent tool.

@Vinnie [1:35:14]: I. Yes.

@Sean Parsons [1:35:17]: 00, come on, Vinny. I, I

@Vinnie [1:35:19]: OK.

@Sean Parsons [1:35:21]: I don't know of any. XML I'm assuming.

@Vinnie [1:35:23]: This is What? What?

@Sean Parsons [1:35:26]: XML I'm assuming.

@Vinnie [1:35:29]: No, like what, like what if, if you were, if, if you, if you, if a model had to spawn a sub agent, what would be, what would it pass to the sub agent? What information?

@Sean Parsons [1:35:40]: The specific task it wants to execute. Just enough context for it to know what to do.

@Vinnie [1:35:43]: Yes, in other words. Right, in other words, the prompt.

@Sean Parsons [1:35:48]: Yes.

@Vinnie [1:35:50]: You, you have to give it the prompt. Well, here's the problem. The prompt could be paraphrased. Right? Because it's the, the model can just put whatever the fuck it wants there. So if, if you have a, if you, if, if, if you have a rule, like for example, like vibe coder.

@Sean Parsons [1:36:02]: Yeah.

@Vinnie [1:36:09]: Right? Vibe coder has very specific, like, see this? This is this is the sub-agent prompt that it wants for when it does a code review. This is the prompt that it wants. It's a pretty big prompt, right? Well, guess what?

@Sean Parsons [1:36:22]: Yeah.

@Vinnie [1:36:24]: If If if the main context is under context pressure, Right? In other words, if it has like a huge list of instructions, then it can paraphrase this. Like, it can make it shorter, or it can make it general, like it like in the worst case, it'll say, you know, do a code review.

@Vinnie [1:36:42]: Like 5 words, cause it thinks that that's the equivalent of this detailed plan, because it's under context pressure. So, now the question becomes, if you're using the LLM as an orchestrator, how the hell do you make sure that the subagent gets exactly the right text.

@Vinnie [1:36:58]: Well, so what I do is I

@Sean Parsons [1:37:00]: And delineated with XML.

@Vinnie [1:37:02]: I, I put, I put the instructions in XML and the sub agent gets a much simpler instruction. The sub agent is told grip for this pattern and execute the contents that are in between. And that keeps the main context clean, because if the main context had to spawn like, you know, 50 sub-agents and each one of them has like these big instructions. Now you're filling up the main context with a bunch of garbage.

@Vinnie [1:37:30]: And it can get confused cause it's has to look at these instructions, has to think about them. And if the main context like looks at this line, like line 305, if the main context looks at that line too many times, it's going to start to think that it's the reviewer, and then it's gonna say, oh, I know, I don't need a sub-agent. I'll just do it right now.

@Vinnie [1:37:51]: You've, have you ever seen that happen?

@Sean Parsons [1:37:54]: Yeah, I think so.

@Vinnie [1:37:55]: Yeah Yeah. Because, again, models are are good at planning, and the models are trained to be efficient, like, they're trained to be token efficient. And, you know, always to do the easier thing that that doesn't require as much work. Well, that cuts both ways.

@Vinnie [1:38:14]: If, if it's under context pressure, it's gonna start looking for shortcuts. And the shortcut will be, I'll just do it myself. Right? So, That's what we have. By the way, this, you say what's, why do we, why are we doing prompt forge? This is why.

@Vinnie [1:38:32]: Is because the model cannot be trusted to orchestrate, because we need determinism. Like, can you imagine if we're reviewing a paper and it takes a fucking shortcut, like, and then this is what I said yesterday, in our WG 21 work, we cannot afford a single mistake, because all it takes is, cause we're criticizing other people. Think about what we're doing. We're criticizing the institution, we're using AI to generate papers and work outputs that critique other people's work. If there is so much as one mistake, then that's gonna be the

@Vinnie [1:39:02]: Excuse that everybody uses to say, oh, these guys, they're, they're just using AI it's no good. Get it?

@Greg [1:39:11]: Yeah.

@Vinnie [1:39:14]: All right, let's see what the hell this thing did. Contract tags, inventories move. Testing plan rewritten to the light cadence, I like it. Five-step decomposition. Oh,

@Vinnie [1:39:31]: Oh, they wanted.

@Vinnie [1:39:48]: And see what happens when we give the model some freedom. The user is offering The user asks, let me think honestly. Considerations. Option 6, option 7. My honest judgment, 6 steps. Split C at the natural seam, cause C C is kind of big.

@Vinnie [1:40:07]: Why not 7? Oh, Fucking Kimmy, dude. Kimmy is really smart. I, I'm, I, I mean, unless they're routing the loud. I think you think they're running?

@Vinnie [1:40:24]: Maybe, maybe that's why they're so smart. Oh fuck. My judgment, 6, not 5, not 7. I love this. This is amazing. This is amazing.

@Vinnie [1:40:40]: Done. OK. Well, I mean, it sounds like we're ready to kick the tires and light the fires. Agents,

@Vinnie [1:40:57]: Bye-bye. Oh, I'm sorry, I'm in, I'm in PowerShell, we need to remove dash object. Fucking power shell.

@Sean Parsons [1:41:13]: So Vinny, with, with this kind of intro.

@Vinnie [1:41:15]: Oh hold on, hold on, hold on, I gotta, I gotta delete this stupid thing. Dot agents, OK, bye-bye. All right, now we're back here. OK, sorry, what now?

@Sean Parsons [1:41:27]: I was saying with this, with this intro and getting a little bit more familiar with prompt forge and things of that nature. Like what do you, what do you think the next steps? Greg and I could do. To maybe help you or like what are some areas that you feel.

@Sean Parsons [1:41:44]: Need some.

@Vinnie [1:41:44]: That's a great question.

@Sean Parsons [1:41:46]: Yeah.

@Vinnie [1:41:46]: Let me think about that. Ready for the vibe coder. Oh. Let's not forget the Rust rulebook. I. That's the thing that caused all this.

@Vinnie [1:42:03]: Oh, Given that we're in plant mode, Apply the rulebook means load it into context and check the plan against it, make the plan conform. Yes, that's right.

@Vinnie [1:42:21]: Plan mode. Review the plan, report fixed gaps. SMRT. Oh. I mean, there's already gaps. The plan came from the rule book.

@Vinnie [1:42:44]: Oh boy. You The rule book is already in my context. Apply it means two things. No, I don't want to bind the rulebook into the plan. Fixed. I don't want the plan to reference the rule book. I want you to inline the smallest amount of material that will ensure that the plan conforms when it runs.

@Vinnie [1:43:10]: Oh The user is asking, Remove the constraint, I inline the minimal rules.

@Vinnie [1:43:34]: The plan already inlines nearly everything. The remaining gap is small, that's what I like to hear. What's actually missing. Smallest sufficient material, one compact paragraph. Oh, I like that. Remove the constraint bullet referencing the rule book, add a single paragraph, nice edits. Oh yeah, very good, very good.

@Vinnie [1:43:55]: Oh, look at that little tiny edit. Beautiful. Very good, very good. OK, so now this thing's ready to rock. Go to go to Max Thinking. Actually, let's leave it on high. Sometimes, sometimes max, well, let's try Max, let's see what happens. OK. Ready? Here we go.

@Sean Parsons [1:44:18]: I've never had a good experience with Macs.

@Vinnie [1:44:22]: Oh Really? What happens?

@Sean Parsons [1:44:24]: Yeah, I think it just marinates on things forever and it actually tries to make things more complicated than they actually are.

@Vinnie [1:44:33]: Damn it, maybe that's when the routes declawed. OK. Here's what's gonna happen. I'm gonna leave, everybody leaves the huddle, and then I'm gonna recreate the huddle. You ready?

@Greg [1:44:47]: OK.

@Sean Parsons [1:44:48]: Ready.