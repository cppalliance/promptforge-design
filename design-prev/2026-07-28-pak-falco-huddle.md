Transcript of huddle in Will Pak on Jul 28 from 10:49 AM to 11:26 AM Pacific Time (US and Canada).

This transcript is auto-generated, so some information may be inaccurate. It won’t be surfaced in search results.
@Will Pak [0:14]: Hey.

@Vinnie [0:16]: Oh yeah, good idea. OK, so I think I wanna make an MCP service. That, In rust.

@Will Pak [0:28]: Oh yeah?

@Vinnie [0:29]: Yeah. And I wanna make it available to the, well, not to the public, but for us. Actually, it could be the public. We should have an MCP service so that you could request the papers marked down. Like, why not?

@Will Pak [0:45]: As part of WG21.org.

@Vinnie [0:48]: Yeah, like I could use that right now, I could, I would love an MCP service in my cursor where I can pick, I can grab the markdown for any paper, that would be amazing, that would be really good.

@Will Pak [0:59]: Yeah, it's a good idea.

@Vinnie [1:01]: Why didn't, didn't we think of this?

@Will Pak [1:04]: Well, I've been thinking of it.

@Vinnie [1:08]: Good idea.

@Will Pak [1:08]: Believe it or not. OK, so you want to write that in rust?

@Vinnie [1:10]: But, but it needs in Yeah, I'm just gonna, I was just gonna, you know, put it together in rust. so that's one thing. And then the next thing is Or for the prompt for the prompt forge.

@Will Pak [1:26]: Mhm.

@Vinnie [1:26]: I wanna have an MC I wanna have an MCP service that's facing I think internally. And we can turn any

@Will Pak [1:35]: I'm sorry, come again.

@Vinnie [1:37]: I want to have an MCP.

@Will Pak [1:37]: Internally.

@Vinnie [1:39]: Hello?

@Will Pak [1:42]: Hello.

@Vinnie [1:42]: Can you hear me? Well,

@Will Pak [1:45]: Yes, I can hear you now.

@Vinnie [1:47]: Yeah.

@Will Pak [1:49]: Connection is not very good.

@Vinnie [1:49]: So, So I want to create a gateway I want to create an a

@Will Pak [1:55]: Mhm.

@Vinnie [1:56]: An, an open AI gateway in Rust. And I wanna have all of our inference going through the gateway.

@Will Pak [2:06]: OK. Isn't that what Pipeline is already doing?

@Vinnie [2:08]: So. No. No, pipeline doesn't create a gate pipeline doesn't create a server. Pipeline does it within in process.

@Will Pak [2:22]: Oh. OK, instead of API, you want to create an API server.

@Vinnie [2:23]: Right. Yeah, I want to create an endpoint that that that all of our, all of our everything talks to, but it has to be, it has to be everything, Will, like even other computers. There we need to bottleneck all of our

@Vinnie [2:45]: A single In rust. Why? I'll tell you why, because We're gonna start, I wanna start building apps. I wanna start building AI apps.

@Vinnie [3:04]: And some of them are gonna be in rust, some of them are gonna be in Python, some of them we're gonna download, and they're all gonna be competing for the concurrency limits, and in order for us to enforce a global limit,

@Will Pak [3:04]: Mhm.

@Vinnie [3:17]: They're only 1 of our mach only 1 process in our infrastructure can talk to the remote in order for us to like have a limit, like let's say we want an 8 concurrent limit. Why is this necessary? Because VLLM does not have queuing, it doesn't have limits, it doesn't have

@Vinnie [3:36]: Proper rate limiting. Like, it doesn't give you the 503. It's kind of sucks. And so we have to do it ourselves, if we wanna be able to put limits on our In on our The way that we use the models, right?

@Vinnie [3:54]: So, so there's that.

@Will Pak [3:55]: OK, so this could be like a gateway to OpenAI, run path, everything.

@Vinnie [4:00]: Yes, let me share one.

@Will Pak [4:01]: But there's a rate limit.

@Vinnie [4:04]: Exactly, and, and we're going to need, we're gonna need, You know, we're going to need API keys because people, we're gonna need, we're, we're gonna need developers to access our RPods, and so we're gonna want to go through our gateway.

@Vinnie [4:24]: See what we got here. Anyway, Prop Forge Gateway. Expose an MCP, read a prompt, blah blah blah. Oh yeah, no, no, this is what it does not do. Create

@Vinnie [4:41]: HTTP surface, we've got the models, health metrics, status, blah blah blah.

@Will Pak [4:46]: OK.

@Vinnie [4:47]: It's very sim pretty straightforward, but why is this file so big? Oh my god, why is this big? Oh, it's pretty huge. OK. Oh, it's cause it's got some rust. D, design notes, oh my god, admission control, jeez. What is all this?

@Vinnie [5:04]: W. Protocol equals OpenAI or anthropic. Jeez. OK, well, Right, and then And then I wanna have the pro and then we have the prompt forge. So PromptForge is a library.

@Will Pak [5:19]: Yeah.

@Vinnie [5:22]: For running the prompt forts, the structured props with that have the lua, but the prompt forge doesn't do any The prompt forge has to be linked, I guess, with the library to do the, to do the calls. Right? Like prompt for us to talk to the gateway.

@Will Pak [5:41]: Yes.

@Vinnie [5:41]: OK.

@Will Pak [5:44]: With the API key.

@Vinnie [5:44]: Yeah. Yeah, well, I was thinking it would just be the local connect like anything loop back to loop back doesn't require an API key. But if we wanna have other machines in our intranet being able to access it, well then they either we need to have like a a whitelisted IP or we need the, the API key, something, we'll figure that out later,

@Vinnie [6:07]: But I want to be able to export, I want a configuration that will allow me to export. Prompt forge prompts as MC as MCP tools. Does that make sense?

@Will Pak [6:21]: Mhm. I'm trying to understand, right, Trump Forge prompts is an MCP tool. Like dynamically.

@Vinnie [6:35]: Right, like in your, in the server, you can configure it, you can say, I want the I want these prompts to also become to also be MCP tools. And the prompt has a yamel front, the prompt has a yamel front matter. Like there's yamel at the top.

@Vinnie [6:53]: So, and that's where you configure the, that's where you configure it as an MCP.

@Will Pak [6:54]: Yeah.

@Vinnie [6:58]: Every prompt forge Prompt returns a string, that's it. No, no, no pipe, no Jason, no, it's just a text, and then the, the, the prompts can declare their inputs, like in the Yamo, they can say like what what parameters they require, like a file name, or, you know, a number or a set of parameters, right? But they, they all take a, it's like a function call. Basically it's a function call.

@Vinnie [7:27]: So, once you do that, and then if you have a description, that now you have an MCP tool, right?

@Will Pak [7:34]: Yeah.

@Vinnie [7:35]: That's a tool call.

@Will Pak [7:41]: I see.

@Vinnie [7:41]: OK Right, so And like I wanna run, I wanna have this locally as well. Like I wanna, like, and this is why I'm using rust, because rust is compiled, and you can install it as a Windows service, or you can install it is a Mac, you know, cron or whatever it is that in the system, you know what I'm talking about? Like where you have it, like if the server is always there when the computer starts up.

@Will Pak [8:02]: Yeah. Like a demon.

@Vinnie [8:06]: And Yes, and I wanted to monitor the directory, so if you, if you add prompts to it, then it picks it up, and if you're doing development and you change your prompt, and then it knows it has to refresh its cache. Right? So then, so you don't have to keep restarting and restarting the server, so very convenient for development.

@Will Pak [8:20]: Mhm.

@Vinnie [8:26]: And then, And I wanna add it to cursor. Right? So like, for example, if I make a prompt like a, like a code review.

@Will Pak [8:31]: Mhm.

@Vinnie [8:34]: I wanna be able to run that. Locally, like I wanna tell cursor, I want to say, hey, do code review, but it has to go through the MCP. I don't wanna do, I don't wanna do this thing anymore, like, you know, how I call them now, like, you know, code review.

@Vinnie [8:51]: Like that, you know, like, like this thing.

@Will Pak [8:54]: So instead of doing that, you're going to be calling it via the MCP server and just mention the tool name, code review, the prompt name.

@Vinnie [9:03]: Yes, yes, yes, you get it?

@Will Pak [9:05]: Mhm. Mhm. I see.

@Vinnie [9:08]: But However, however, Some of them are gonna run locally. So I have my own MC, I have my own Basically, the prompt prompt forge is gonna be this, an executable, and when you run it, you're gonna get

@Vinnie [9:30]: An optional gateway

@Will Pak [9:34]: Mhm.

@Vinnie [9:35]: The MCP server. And it's gonna, and it's gonna be linked in with a bunch of tools, it's configurable, like the tools, cause You know, some, you need, you need to, you need to add the tools, and rust doesn't have dynamic loading of libraries, so it all has to be linked in.

@Vinnie [9:53]: So, Like web search will be LinkedIn and Trufflelaturo and all that crap, whatever you need will be like linked in there. And yeah.

@Will Pak [10:01]: Yeah.

@Vinnie [10:04]: And then you can and then you can add trumps to it. So,

@Will Pak [10:09]: Right.

@Vinnie [10:10]: OK So you have your, you have this thing running. And You can call You can do an MCP call and it'll call a prompt, but then when prompts call other prompts, we don't go through the MCP, we just do it internally because we're, we're linked in, you know what I mean?

@Will Pak [10:28]: With pumped.

@Vinnie [10:31]: Like tools, tools can call other tools.

@Will Pak [10:31]: Huh.

@Vinnie [10:37]: So, So if, if a, if a prompt forge prompt calls another prompt forged prompt, it'll go through, it'll be in process, it won't go through the MCP. There's no, why you don't need a socket for that. Right? Get what I'm saying?

@Will Pak [10:56]: Only to think about it.

@Vinnie [10:58]: Yes, it's very complicated.

@Will Pak [10:59]: The prompt goes through prompts directly, tools go through the MCP server.

@Vinnie [11:09]: But then we also want prompt forge prompts to be able to use to to be able to use other MCP services. For example, I wanna have a prompt forge prompt that runs locally that accesses Pinecone.

@Will Pak [11:22]: Mhm.

@Vinnie [11:23]: So, that promptForge MCP server has to have its own MCP service configuration where you can add multiple other MCP servers.

@Will Pak [11:34]: OK, so Let me just summarize what I heard. it's what you want. Like for example, Rust, it, it's a compiled language. Once you write the code, you execute the code, everything's LinkedIn, you can't change once it's running. But then we have this dynamic interpreter, which is like,

@Will Pak [11:53]: The prompt forge prompts are like Dynamically loaded and parsed. And exploited as a MCP server tool.

@Vinnie [12:05]: Sometimes. Wait, let me think, let me think about it.

@Will Pak [12:07]: Right.

@Vinnie [12:08]: Let me think about that. Well, Exactly, yeah, I think that's, I think that's, I think that's right.

@Will Pak [12:27]: OK.

@Vinnie [12:28]: However, But you, you also, I, I think, uh-huh. You also need to be able to run them from the command line. So there'll be like a CLI.

@Will Pak [12:38]: Yeah.

@Vinnie [12:40]: They'll be like a CR, I, I haven't figured all this out yet, by the way, I'm still trying to, that's why I'm, I'm trying to figure this all out.

@Will Pak [12:40]: Mhm. Yeah.

@Vinnie [12:46]: But I think you kind of get an idea of what I'm trying to do, right?

@Will Pak [12:47]: Right. Yes, it's a, it's a framework for, like, it, it's a, it's like a server plus MCP plus. These prompt resources and Like the dynamic.

@Will Pak [13:04]: Loading functionality exposes tools as Those prompts are dynamically changed. It sounds really complicated. I need to think about it a little.

@Vinnie [13:19]: Yes. Yes. What do you think of the prompt forged concept? Molly.

@Will Pak [13:24]: Well,

@Vinnie [13:26]: Nothing. Yeah, what do you think of the prop forge concept with the lua and all that. Have you looked at, did you look at it?

@Will Pak [13:33]: Yes, one thing.

@Vinnie [13:46]: Are you talking? oh. Oh, you, you, I lost you. Yeah, I'm, you're back.

@Will Pak [13:49]: Hello? I'm sorry, my network connection. So 1. OK, so 1 specific concern. Is that As the prompt force prompts are growing.

@Will Pak [14:08]: The prompts. It's going to be very long, right? It's basically, it's basically a program, like a software piece of software that can

@Vinnie [14:15]: Yeah, yes.

@Will Pak [14:17]: Embed LuA code, prompts, the linking dynamics, everything. So is there an option that we can break it up into multiple prompts, for example. So that it looks like a

@Vinnie [14:31]: 1.

@Will Pak [14:32]: Piece of software like

@Vinnie [14:32]: Yeah, so that's the, so that's the idea, that's the idea that you can call another prompt.

@Will Pak [14:39]: Right, when you see

@Vinnie [14:39]: Right, let me Yeah Hold on, let me show you, let me show you the design document.

@Vinnie [14:57]: So we actually have the, we actually have it. We find it in here. I have a, I have a table somewhere around here.

@Vinnie [15:18]: There's go to, there's call. And then there's Something else.

@Vinnie [15:35]: I can't find it. Well, so there's, so the idea is there's go to, is you transfer to another section.

@Will Pak [15:40]: Mhm.

@Vinnie [15:42]: And then you have call. Which means, so, but when you do the go to, you lose the context, you get a fresh context, or you could do ca call

@Will Pak [15:50]: Right.

@Vinnie [15:52]: Means you'll transfer con you, invoke another section without clearing the context, and then it returns. And then you have There's a, there's a fan out.

@Will Pak [16:04]: Mhm.

@Vinnie [16:05]: Where you multiple sub-agents, but the idea is maybe you could put like a file name, right, like you could say, call, you know. Research MD. And now that will invoke a different file, and this is why I say that in the front matter, you have

@Vinnie [16:26]: It's a function, right? Every, every prompt for prompt is 1 function. It returns a string, and it takes a set of parameters. And so now once you have that, now you have your programming language. Actually, I need, I need a minute, give me 1 minute.

@Vinnie [18:49]: Sorry about. I'll turn my video off. Right, so, so a prompt is a single markdown file and it's a function. It's 1 function. It returns the string, and it takes a set of parameters, and the parameters are, are def they're well defined in the front matter, in the yamal. They have to be well defined, and they have to be machine readable.

@Will Pak [19:13]: OK.

@Vinnie [19:13]: So However, A prompt can create outputs. It can create more outputs than the return value. So for example, you could create files. You could create a bunch of files.

@Will Pak [19:28]: Right, right to.

@Vinnie [19:30]: Yeah, so it, they need to be able to create, to do things with files, but, you know, that'll just be a tool. So, Yeah, so if you want to call another function, then you call another prompt, and I was thinking like, to see the syntax down here?

@Will Pak [19:49]: Yeah, coresearch. MD.

@Vinnie [19:51]: OK. It would be like that.

@Will Pak [19:58]: OK.

@Vinnie [20:13]: So the goal here is To be able to, we, we wanna have or so we wanna have orchestration that doesn't Require recompilation. Like with the Python, with Python, you have to, you have to write the pipeline from scratch every time, right?

@Will Pak [20:26]: Mhm.

@Vinnie [20:32]: So the idea is we have something language that's rich enough that we can express any of the type of pipeline work that we do. Without the need to write a like a whole bunch of code. And we keep it all in one file, because it's easier to work with, you could see everything.

@Will Pak [20:58]: Well, for 1 prompt, yes, but.

@Vinnie [21:00]: Yes.

@Will Pak [21:02]: As the functionality is are added. You might want to break it up to many files so that Multiple people can work on it.

@Vinnie [21:12]: Well, yes and no. So If you, these are the functions are like libraries, right? A a a prompt is like a library, it does one thing, and you can test it, you can make sure that it works, and then you're done.

@Will Pak [21:21]: Mhm.

@Vinnie [21:27]: So now if you're going to build something else, if you wanna build like another Prompt Now, but that other prompt is just one file and then the, the first prompt that you're calling into it's just like a tool. That's why I say I want to export them using MCP. But if, if it's, if it's within the same process, we don't need to go through the MCP server. We can just call it as a, you know, as a, as a rushed function to execute it, but conceptually it's just calling a tool, right?

@Vinnie [21:55]: It's just a tool call.

@Will Pak [21:59]: OK.

@Vinnie [22:00]: So, from, from the perspective of the the of the developer, they're still in the, they're still operating in the paradigm of that there's only 1 file for the prompt, right? Like this, this reflects my work flow, right? Like everything what you've seen from me has been like the one big prompt.

@Vinnie [22:20]: And so, I'm, you know, I'm taking, I'm taking, I'm taking that concept, and I'm, you know, I'm, I'm extending it now, I'm, I'm, it's the foundation of

@Will Pak [22:22]: Yeah.

@Vinnie [22:33]: So like, for example, this tool.

@Will Pak [22:36]: Yeah, and that ending.

@Vinnie [22:36]: It's 1 file. Yeah, it's just 1 file, so it's 1 file. So this is like, it does one thing. If you wanna have spread your work across multiple files, then what you do is you

@Will Pak [22:45]: Mhm.

@Vinnie [22:51]: You decompose your algorithm into individual functions, which is not, which is how you should do it.

@Will Pak [22:59]: Yeah, we could probably create like subdirectories, each directory ponds to one tool.

@Vinnie [23:05]: Whatever, yeah, you could use directories as like a name space.

@Will Pak [23:09]: Yeah.

@Vinnie [23:11]: So, OK, so, so I think now you understand, so now you understand. Any thoughts?

@Will Pak [23:30]: So MCP server. It's not technically like. Impossible to dynamically load tools, a list of tools. I think

@Will Pak [23:47]: Whenever, like a client talks to him speed server, the first thing they do is to kind of find out like what kind of tools are available. And that can be dynamically loaded, but once that's loaded into client's context, even if the server.

@Will Pak [24:04]: Dynamically reload the list of tools, it's not going to be updated for the client. So I think there's some kind of a.

@Vinnie [24:11]: Wait, I, I don't understand, so I don't understand what you're saying.

@Will Pak [24:14]: OK. Let's say you loaded like in cursive chat, you're talking to an MCP server like the Pine conserver. But let's say during the, during the execution of those chat sessions, Python server, PyCon MCP server has been updated.

@Will Pak [24:32]: So the chat session currently going on doesn't know that the list of tools has changed, right? There needs to be some kind of an API that

@Vinnie [24:40]: Oh.

@Will Pak [24:43]: Like a soy connection that tells the client, OK, the list of tools has changed, please reload, something like that.

@Vinnie [24:48]: Oh yeah, no, no, no, no. So the rea the, so the reason for monitoring the tools for the changes is for the convenience of the developer. It's not for the end, it's not for the production system.

@Will Pak [25:00]: Right, OK. So once deployed, like in usage, it's not going to be changed for the development process, however, it's going to be reloaded. OK, that makes sense.

@Vinnie [25:06]: No. Exact, yeah, that's this is exactly, this is the developer feature.

@Will Pak [25:13]: Mhm.

@Vinnie [25:15]: So, OK. Oh, good, OK, so now Let me see if I can find my, I really do have to find my notes. So I had a conversation with where I was talking about the control flow. This is kind of where I wanted your input.

@Vinnie [25:36]: Get rid of that prompt bloating. Mhm. Profile claims, boop. That's the profile poop. 4302 boop compaction algorithm, oh, there's 2 of these.

@Vinnie [25:53]: Go through this and give me another list. Here it is. Yes, this is it. This is the one. OK. So, I came up with, oh, here it is. All right, so, so here is the con, here's the control flow mechanisms. You have call,

@Vinnie [26:09]: It's a function call.

@Will Pak [26:10]: Yeah.

@Vinnie [26:12]: Then you have task.

@Will Pak [26:15]: Fresh context.

@Vinnie [26:15]: Which is

@Will Pak [26:17]: Model alua.

@Vinnie [26:18]: Fresh. Context, but it's a, it's a, basically this is a sub-agent, but it returns. The point is that it returns.

@Will Pak [26:25]: Uh-huh.

@Vinnie [26:25]: But then you have, then you have go to that does not return.

@Will Pak [26:29]: OK. Like

@Vinnie [26:30]: Like that's, that's a concept.

@Will Pak [26:31]: It gives up the control flow.

@Vinnie [26:34]: Yeah. Now, This, conceptually, this might have to change because I want, I want this to work with very small models, like, I wanna be able to have an orchestrator of a 7 billion parameter or 14 billion parameter model, and you can't have that, you cannot have too many tools, like you gotta limit yourself to 5 to 7 tools. And so, when I actually go to do my testing, I might, this might only be just become 1 control flow, like 1 function, one tool.

@Will Pak [26:56]: Yeah.

@Vinnie [27:05]: Get it. And then a practice an extra parameter.

@Will Pak [27:12]: OK.

@Vinnie [27:15]: I have, I have to experiment with the models, So, But now, if you put a file name here, then It'll, it'll do that.

@Vinnie [27:32]: But of course then we have the, then we have to pass the parameters. Like we have to know what parameters to path. And so the

@Will Pak [27:42]: 3.

@Vinnie [27:44]: Hm?

@Will Pak [27:45]: I mean, have you ever, like, taking a look at land graph, the It's like a

@Vinnie [27:53]: Yeah. Yes, I have. I've looked at every, I've looked at everything. Let me show you. What's it called?

@Will Pak [27:54]: OK. Landgraf.

@Vinnie [28:02]: Landgraf.

@Will Pak [28:04]: Yeah, Landgraf, it's, it's from Langchain. It's basically Python framework that creates like the Asian workflow. Pipelines, and it's got like similar concepts like go to,

@Vinnie [28:13]: Oh, yeah.

@Will Pak [28:19]: Not, not exactly called go to, but like a full loop until something is done, it iterates. And go to the next node, etc. it's like a, it's like a tree structure.

@Vinnie [28:40]: The thing is, so I, I, I always look at I always look at what exists on the web, and what I find is is that nothing has this particular combination of features.

@Will Pak [28:48]: OK. Right,

@Vinnie [28:54]: And if you look in the forge document, you can see there's a com there's like there's a comparison in here. Somewhere. Prior art.

@Will Pak [29:02]: I

@Vinnie [29:03]: Aent flow, AI pack, playbooks, state flow, ref

@Will Pak [29:06]: Uh-huh.

@Vinnie [29:08]: Right?

@Will Pak [29:09]: Yeah.

@Vinnie [29:10]: These are the closest ones.

@Will Pak [29:10]: Feel like So, When I read Prompt Forge, I thought, I got this feeling that you're coming up with an Asian programming language plus Interpreter, like, like the CPU for the Asian programming language.

@Will Pak [29:27]: Right, The CPU is fixed, but the program can change. Which is The prompt force prompts.

@Vinnie [29:40]: You mean the execution model, the exec the the executor?

@Will Pak [29:44]: Yes, the executor, Essentially like assembly language, you have like a multiple commands, like multiple commands, that are allowed to run on that executor. And the software is written in combination of those execution commands.

@Vinnie [30:03]: OK, I mean, I guess that, yeah, OK, and What, how does it look?

@Will Pak [30:08]: So Like there are like multiple attempts to come, to come up with Asian programming language, I guess. This prompt forge is unique in the sense that in one file it combines everything, the prompt, the lure.

@Will Pak [30:29]: And the, the, the routing metrics, like routing logic.

@Vinnie [30:36]: Yeah. It inverts usually usually people start with the interpreted language, like they start with the python or they start with the go, but in my, in my model, I start with the prompt, and then I add the, and then I add the structured programming language into that.

@Vinnie [30:53]: And be, and the reason is because it, it reflects the way that I work.

@Will Pak [30:54]: Mhm. OK.

@Vinnie [31:01]: And one of the my design, one of my design goals is that you should be able to write You should be able to write a prompt forge prompt without using any lure, and it will work just like

@Will Pak [31:11]: Hm.

@Vinnie [31:12]: A cursor orchestration. Right? Like it'll work just like that. And then you, you add the lua in order to The more lua you add, the Less The smaller the model that you need to run it, right? Like if you, if you upload your orchestration to the mop to the lua, now you don't need such a sophisticated model.

@Vinnie [31:38]: Right? And then, by getting rid of pedantic, now we can use an even smaller model because we don't have to have the con conformance to the, to the schema, and, and, and so, and also when you use pedantic, remember that library injects a system prompt in order to guide the model, and so now you don't have that overhead. So every one of those maneuvers, every one of those design choices, it, it relieves pressure on the context, and it

@Will Pak [31:48]: Right, structured of it. Right. Mhm.

@Vinnie [32:08]: Lets you run with a smaller model, right? That that's the goal.

@Will Pak [32:11]: Yeah.

@Vinnie [32:14]: Like the go to, the go the context clearing go to, that's for that avoids the accumulation of, of context. So you could run in a with again the smaller model.

@Will Pak [32:23]: Mhm.

@Vinnie [32:28]: OK, so But now, now let me ask you some design questions.

@Will Pak [32:34]: OK

@Vinnie [32:35]: So if we have, if we have like a, OK, see this, here's a prompt. Here's a prompt for each prompt, right?

@Will Pak [32:42]: OK.

@Vinnie [32:44]: So, When After the model is finished, should it go to, should it just drop to the next section?

@Will Pak [32:56]: In the parsing stage or the execution stage?

@Vinnie [32:59]: Well, execution, of course.

@Will Pak [33:05]: Yeah, that's a Like if the previous stage didn't say anything about like go to or like context clearing, like control flow. Wise, then Going to the next step is the default.

@Will Pak [33:22]: Choice, I think.

@Vinnie [33:26]: But then why, why do we care about this junk? Like we're gonna have a thinking block. We're gonna have, you know, Throat clearing, we're gonna have the nar model's narration about like what it's doing. Why do we care about that?

@Will Pak [33:40]: Every Node in that pipeline generates something, like whether it's a, whether it's inheriting context from the previous noter like for nothing, it just creates something for the next node so that it, it acts as an input.

@Will Pak [33:57]: Right.

@Vinnie [34:00]: But that wastes tokens, like, for example, Opus 5. So if you look at Opus 5, Opus 5 announces what it's doing more, so you hear more about, oh, I'm gonna read this file now, and it like it talks more, and so that wastes tokens. So shouldn't we want, shouldn't we want to trim the conversation before we go to the next

@Will Pak [34:04]: Mhm. Yeah. Uh-huh.

@Vinnie [34:21]: Step

@Will Pak [34:25]: Yes, If the whole purpose of that first blog was to read something and extract information for the next step, then yes, summarizing it for the next step would be the wise choice.

@Vinnie [34:42]: In fact, I would even go so far as to say that Maybe it's a tool call. So maybe Like Maybe the there needs to be a tool, which means go to the next section.

@Will Pak [34:56]: No.

@Vinnie [34:58]: And when you call the tool, it, you put the model puts in what the the context that it wants the next section to have. So then when we go to the next section,

@Will Pak [35:10]: Mhm.

@Vinnie [35:13]: It's we clear the context, but we include a string. From the previous section that the that the previous section chose.

@Will Pak [35:18]: Right, uh-huh.

@Vinnie [35:20]: So this is better than the go to because now you can pass, now you can pass, An instruction.

@Will Pak [35:28]: Yeah.

@Vinnie [35:34]: Because look, here.

@Will Pak [35:35]: So. Yeah.

@Vinnie [35:38]: Read the strict rationale, but how do we do that?

@Will Pak [35:43]: Evaluate At each paper called task evaluate right there. In the middle, call task, evaluate with some rationale path, right? So it's a, it's a

@Will Pak [36:01]: It's, it's, it's invoked from Maine. Or re high on the river summary. And done.

@Vinnie [36:12]: Actually, you know what, I have to go, let me go.

@Will Pak [36:13]: Well.

@Vinnie [36:15]: I gotta talk to

@Will Pak [36:16]: Sure. OK.

@Vinnie [36:18]: I gotta talk to. All right, I'll, I'll be, I'll ping you, bye.

@Will Pak [36:22]: OK, bye bye.