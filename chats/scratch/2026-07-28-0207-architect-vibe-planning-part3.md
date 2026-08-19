# Architect and vibe-coding planning session

*2026-07-28 02:07 - transcript 02e2ab27-db37-4548-80f8-f0b3046ddb71*



*Prompts p117-p171 of 223. Part 3 of 4. The Plans and Design Documents sections are in part 4.*



## Prompts



**[p117]** who needs the extractive (that's the token dropper?)

**[p118]** >100 tools. I can see where token dropping is useful though. But for my prompts, I want them to read beautifully. And.. this technique could also shrink wg21 papers

**[p119]** My question though So I can train it on Peter Dimov, I can train it on Villa, I can train it on like technical papers, I can find good compressed human prose, but here's the problem though: every human has their own style. Is this gonna be, is this gonna sound like the person? If I train it on multiple people, is it, are they gonna compete with each other? Like, am I, is the model gonna get pulled in a bunch of different directions? How's this gonna work?

**[p120]** But what if my goal is to compress plans and prompts? Then I'm using committee output on. That.

**[p121]** But that's not right, because my tools have evolved. Like my earlier tools were just raw output, my later tools have been refined by the use of other prompts that voice the tool in a way that holds alignment with the LLM. Let me show you. @tools-public/how-to/how-to-write-prompts.md

**[p122]** But here's the problem. The rulebook itself is the result of blurring.

**[p123]** is this a problem though? a blurred rulebook still produces sharp outputs

**[p124]** Here's my question: If we want to produce, if we want to take sharp input and then blur it. To create our training dataset, what do we use to blur? Do we use like a seven billion parameter model? And then, how do we set that up? Do we just like set the temperature? What do we do?

**[p125]** Can we do, can we do 10 sentences at a time?

**[p126]** Wait a minute, I don't know about this. I disagree. You're saying expand any points that could benefit from additional context or justification? No, we don't want that. Like, that's hallucination. Why do we wanna We don't want hallucination. We want natural expansion.

**[p127]** Here's my question. And then how do we prepare the training data? Do we separate, do we. Do we chop it back up into sentences, or do we train on the larger dataset? Like, do we train on paragraphs?

**[p128]** 200 tokens is small though, like a 7 billion parameter model has what, 8K token context window? And you're only doing 200? Why?

**[p129]** create a rust program to generate the training dataset. For now only work on @promptforge/study/make-dataset/peter.md as input. we just want to validate that we can blur at multiple levels, and get the data set generation harness in place. give me some choices for the model. I have a 24GB video car

**[p130]** Blur Dataset Generator

**[p131]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p132]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p133]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p134]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p135]** apply @tools-public/how-to/how-to-write-prompts.md to @promptforge/study/make-dataset/peter-v2.md rewriting it in place

**[p136]** @promptforge/study/make-dataset/papergate.md lets use this instead of peter.md

**[p137]** This is a problem because I was hoping to be able to use the human outputs. papergate.md is AI output. So now I have to go through all my prompts and figure out which ones are first generation

**[p138]** yes do this now. the prompts are in @tools-public/tools @tools-public/tools-wg21 @tools-public/how-to @staff-private/tools @umbra/tools @profiles-coalition/campaign/tools and note that they have been renamed, moved to different directories in the same repo, and also moved across repos in this workspace.

**[p139]** First-Gen Extractor

**[p140]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p141]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p142]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p143]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p144]** Let me explain. There was a point in time when I develoepd "how-to-write-promptss" which is actually the renamed version of some prompting lessons file (forgot the name). And thats when I started applying the how-to and this made my existing prompts smaller. So when you see a big v1 and then a smaller v2, check the date, and also look at the style of the change and I bet you will see fingerprints of how-to-write-prompts.md

**[p145]** forget the voice/pen files those were manually trimmed when I was building the "novelist" system. how many revisions did The German get?

**[p146]** "tighten" doesn't mean reduce the size in the context of prompts. it means make the prompt aligned and unambiguous. compare the diff

**[p147]** Yes, that sounds reasonable. Perform the analysis, but here's a, we have a problem, which is that, remember, I was expecting to be able to use ordinary English as my source material, but now we can't do that. So now we need a source, now we need to be able to have like a source of prompts, and I don't have enough data here. Like, I want like five thousand to ten thousand files that we can blur. I wanna have a big dataset, 'cause this is high value, this is high stakes. So where are we gonna get that?

**[p148]** what if we take the bloated prompts from the web and run how-to-write-prompts.md on them to produce the sharp set, and then you can go through each one with a frontier model and extract the parts we need.

**[p149]** I'm worried that @tools-public/how-to/how-to-write-prompts.md has acquired some slop

**[p150]** the thing is that the prompt rulebook got an update from an Anthropic blog post about context engineering so it might have more valuable information than the german

**[p151]** What's next?

**[p152]** Okay, you added a whole bunch of Fucking rust shit, and now it's going into git. Don't you think you should make some git ignore to ignore the intermediate outputs? Duh.

**[p153]** Let's validate the sharpening. Are you gonna do this from Rust? If you're gonna do it from Rust, I would like you to use Opus 4.8 with maximum thinking.

**[p154]** I dont want Cursor's harness shit and their prompt engineering and their system context.

**[p155]** I'm not sure what you mean about hand-tightened. What is hand-tightened? None of my prompts were authored by hand.

**[p156]** Let me explain how I write prompts. I go into plan mode and I tell the model what I want. During this conversation at some point I say "apply @tools-public/how-to/how-to-write-prompts.md " then keep refining, then at some point I say "review the plan" and it tightens. Then I say run

**[p157]** you aren't understanding. look closely at @tools-public/how-to/how-to-write-prompts.md . When applied it not only tightens the plan, it tightens the tool that the plan would produce, and if the produced tool is itself a tool-producer, it propagates the applicable prompt-tightening rules.

**[p158]** before you do that you should test your own prior. see if a sharpening of a tool that was produced sharp actually strips the thing you said it would strip.

**[p159]** sounds like this @promptforge/study/make-dataset/sharpen-instrument.md is a fucking rock star

**[p160]** the problem is now we are faced with a tough decision. for each prompt do we sharpen it first to make sure its already sharp? I mean, for my prompts... tutor.md clearly had some bloat. maybe you should compare line by line the original vs. the sharpened version I mean really make sure because this is a high-value high-leverage audit

**[p161]** No. The em-dash is in a workspace rule. And your Rust program does not import the always.mdc. You're still a rock star.

**[p162]** is it possible with careful mechanical processing of the dataset we could train the model to convert em-dash to regular dash?

**[p163]** @tools-public/how-to/how-to-write-prose.md which of these would be easy to piggyback in

**[p164]** question: would we add the safe rules into the @promptforge/study/make-dataset/sharpen-instrument.md  ?

**[p165]** I dont see how the prose rules can be mechanical. not all of them anyway. this is becoming more trouble than it is worth.

**[p166]** yep the em-dash is it. what's next?

**[p167]** Pair Pipeline Validation

**[p168]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p169]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p170]** Pair Pipeline Validation

**[p171]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.
