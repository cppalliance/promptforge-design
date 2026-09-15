<!-- source: Huddle, Sep 15 2026, 10:30 AM to 12:02 PM Pacific, Greg Kaleka, Sean Parsons, Vinnie Falco. Walkthrough of the PromptForge prompting-language design document: goals, non-goals, success criteria, constraints, deferred open questions, functional specification. -->

# PromptForge, Taught From the Ground Up

This tutorial is built from a working session in which two engineers read the PromptForge design document aloud, stopped at every sentence they did not understand, and had the designer explain it. That is a gift for a teacher, because it shows exactly where the confusion lives. Every idea below is one that tripped somebody up, and every explanation is the one that finally made it click.

The ideas are ordered so that nothing is used before it is introduced. If you read it top to bottom you will never hit a term you have not already met. If you skip ahead, the glossary at the end will catch you.

---

## Part 1: What a harness is, and why you should want to own one

### 1.1 A raw model does nothing

Start with the simplest possible picture. A large language model, by itself, is a function: text goes in, text comes out. That is all. It cannot search the web, read a file, remember yesterday, or ask you a question. If you have never "talked to a raw LLM," picture a toy that turns ordinary sentences into pirate speak. You type, it answers, and nothing else in the world changes.

Everything you think of as "the AI doing things" is done by something wrapped around the model. That wrapper is called the **harness**, or in PromptForge's vocabulary, the **host**. One of the engineers summed it up during the session: the host is what connects the model to the outside world. It integrates the model with the person chatting, with tools, with files, with other models. That is why the design document calls it a **host integrator**.

Hold onto this: **run does nothing on its own.** Whenever you feel lost later, come back to the question "who is actually doing this, the model or the host?" The answer is almost always the host.

### 1.2 The problem with somebody else's harness

When you use a commercial coding assistant, you are using somebody else's harness. Their system prompt goes first, and it may be enormous: instructions about the current window, how to get help, house rules, all of it. Your own instructions arrive later, as user messages or as tool results. The model is asked to follow your directions while somebody else's directions sit at the top of its attention.

That works until the conversation gets long. Then the harness compacts the history (we will study compaction carefully in Part 9), and each compaction blurs your instructions a little more. An agent you carefully designed drifts out of character because it never controlled what survives.

PromptForge exists so that **you** control the harness: what goes in the system prompt, which tools the model can see, when and how history is compacted, and what happens when something fails. The rest of this tutorial is the mechanics of that control.

### 1.3 The one design philosophy you need

If you remember one sentence, make it this one: **every model operation is explicit.** Nothing is ever sent to a model because of where it sits in the file. Nothing is stored in a hidden variable because the model happened to say it. If the model is being called, you will see the call in your code. This philosophy replaced an earlier design in which "magic" happened, and the engineers in the session agreed the new version is far easier to reason about precisely because there are no special things being done behind the scenes.

---

## Part 2: Anatomy of a prompt file

### 2.1 Three ingredients

A PromptForge prompt is a single Markdown file containing three kinds of material:

- **YAML frontmatter** at the very top. This declares the contract: which tools the prompt is allowed to use, which model slots it uses, what its input and output store files are. Anything the prompt uses has to be named here. Think of it as the manifest.
- **Markdown**: headings and ordinary text. Headings divide the file into sections. Text is either commentary for humans or material you will hand to a model.
- **Lua fences**: fenced code blocks marked as Lua. This is where all the work happens. Every model call, every tool call, every decision is written in Lua.

The frontmatter contains a version line, `promptforge: 0`. One of the constraints in the design document is that this number must never be incremented while the current design work is active. The engineers laughed in recognition here: AI assistants love to bump version numbers on pre-release software, and this rule exists to stop them.

### 2.2 Sections

A **section** is a heading plus everything under it until the next heading. Sections are the fundamental unit of execution, and Part 4 will show you why. For now, just notice that the design talks about "section entry" as a distinct event, like calling a function.

### 2.3 Two ways to read the same file

You can read a prompt file two ways, and both are valid:

1. As a document. It has headings, paragraphs, and code blocks. A human can read it top to bottom and understand what it does.
2. As a program. Each Lua fence executes. The Markdown around it is data the Lua can pick up and use.

The design goes to some lengths to make sure the second reading never surprises someone doing the first. That is what the next part is about.

---

## Part 3: How Markdown becomes data

This part is where the first engineer said "I didn't understand any of these sentences" at the start of the session and "these are easier to parse now" at the end. Go slowly.

### 3.1 The pending prose buffer

As PromptForge reads your file from top to bottom, it keeps a running buffer of Markdown text. Call it the **pending prose buffer**. Three things reset it:

- A **heading** starts a new section and a fresh buffer.
- A **Lua fence** consumes the buffer (details next) and leaves it empty.
- A **thematic break** (a horizontal rule, `---` in Markdown) clears the buffer and throws the text away.

So at any moment, the buffer holds "the Markdown accumulated since the nearest preceding heading, Lua fence, or thematic break." That phrase from the design document is exactly a description of this buffer.

### 3.2 The thematic break makes a comment

Suppose you want to write a paragraph explaining what a section does, for the benefit of a human reader, and you do not want any model to see it. Write the paragraph, then put a thematic break under it. The break clears the buffer, so the paragraph is gone before any Lua fence can pick it up.

This is how you write a comment with formatting. Lua comments cannot have bullets or bold text; Markdown followed by a thematic break can.

A subtle consequence the engineers worked out on their own: if a section has no Lua fence at all, you do not need a thematic break. A section of pure text does nothing. Nobody reads it, nothing executes. It is already, in effect, a comment.

### 3.3 The Lua fence receives `prose`

When PromptForge reaches a Lua fence, it takes whatever is in the pending buffer and installs it as a value called **`prose`**, visible inside that fence. Then it clears the buffer so the next stretch of Markdown accumulates cleanly. Then it runs the Lua.

Three properties of `prose` matter:

- **Read-only.** You cannot assign to it. It is the text above the fence, period.
- **Lazy.** Nothing is done with the text until your Lua actually reads `prose`. If your fence never mentions it, the text was never processed.
- **Evaluated once and memoized.** The first time your Lua reads `prose`, PromptForge takes a snapshot of the section's current state, fills in every `{{ }}` substitution once, and remembers the resulting string. Every later read in that same fence returns the identical string, even if state has changed. This matters inside loops: you pay for the substitution once, and the text cannot shift under you mid-fence.

### 3.4 Substitutions

Inside your Markdown you can write placeholders like `{{ item }}` or `{{ var.draft }}`. When `prose` is first read, those are filled in with live values. The engineer in the session called them "mustache thingies" and "handlebars," which is fine; the design just calls them substitutions. Each Lua fence receives its own captured prose with its own substitution pass.

### 3.5 Trailing Markdown is inert

Here is the change that most affected the veteran in the room. In the old design, if a section ended with Markdown after its last Lua fence, that trailing text was automatically handed to a model for inference. Positional. Implicit. Magic.

That is gone. **Markdown left after a section's final Lua fence is inert trailing commentary.** It is discarded at section end, with no error and no model call. Likewise, Markdown before the last thematic break is inert. If you want a model to see text, a Lua fence must read `prose` and hand it to a model call.

This is the philosophy from Part 1.3 made concrete: no positional inference rule, no final-prose rule. Only explicit calls.

---

## Part 4: Sections as isolated programs

### 4.1 One fresh Lua VM per section entry

Now the payoff of defining sections. **Every time execution enters a section, PromptForge spins up a brand-new Lua virtual machine for it.** When the section ends, that VM is gone.

There is no long-running Lua process holding state across the whole file. You do not start the VM yourself; writing a section is how you declare "this gets its own VM." The Rust runtime underneath handles the spin-up and tear-down when it ingests and runs each section.

The lifecycle of a VM is the lifecycle of the section: born at entry, dead at exit.

### 4.2 The consequence: nothing is shared by accident

Because each section starts fresh, a variable you set in one section does not exist in the next. The design states this as a non-goal: **do not share mutable Lua state between sections.** If you want data to travel from one section to another, you have to send it deliberately through one of a small number of channels. Part 8 covers those channels. For now, just absorb the rule: sections are isolated, and isolation is on purpose.

### 4.3 Model-facing sections

The design's first goal reads: "Treat every model-facing section as an agent context with one fresh Lua VM per section entry." You now know what the second half means. What is a **model-facing section**?

The engineers worked this out with an example and got it exactly right. A section is model-facing when its Lua explicitly sends something to a model. A section that is pure text is not model-facing; it is a comment. A section whose Lua does non-model work (splitting text, reading a file) is not model-facing either.

The instructive case: imagine a section called **Criteria** that contains seven bullet points, and a separate section whose Lua reads the Criteria section, splits it into an array of bullets, and sends each bullet to a sub-agent. Is Criteria model-facing? **No.** The model never receives the Criteria section. It receives seven strings that happened to be extracted from it. Criteria has no VM; it is just text that other code parsed. The section doing the sending is the model-facing one.

The rule of thumb: a section is model-facing if and only if its own Lua fence is the thing calling a model.

---

## Part 5: Talking to a model

### 5.1 The simplest call: `models.infer`

The most basic way to invoke a model is:

```lua
return models.infer(prose)
```

This performs one fresh, tool-free text inference. You hand it a string (here, the prose above the fence), and you get the completed text back. It does not read or modify any message history. It is a pure request-response. For a great many pipeline steps, this is all you need.

### 5.2 Messages and roles

Anything more sophisticated than a single request needs a **message array**. Every conversation with a model is, under the hood, a list of messages, each tagged with a **role**:

- **system**: instructions that frame the whole conversation.
- **user**: what the human (or the calling code) says.
- **assistant**: what the model said.
- **tool**: the result of a tool the model asked to run.

When you chat with any assistant, every time you send a new message, what actually gets transmitted is the entire list that came before plus your new one. The model has no memory; the message array **is** the memory. PromptForge lets you build that array yourself instead of letting the harness build it for you.

### 5.3 Provider-neutral

Every model vendor wants messages in a slightly different wire format. PromptForge keeps one **provider-neutral** representation of the array, and a translation layer (owned by the gateway, not by your prompt) projects it into whatever format the chosen model wants. You write against one message model; the gateway handles the rest. The design explicitly refuses to fork or replace the gateway's model-specific chat-template responsibility.

The success criteria phrase this as: every model request "carries a validated provider-neutral role sequence." Role sequence just means the ordered list of system, user, assistant, and tool messages.

### 5.4 Building an array: `messages.new()`

You can build a message array as an ordinary Lua table, or use the optional builder:

```lua
local history = messages.new():system(prose):user("Search the web for " .. item)
```

The builder methods are chainable and pure: they append a record and return the same list. They do not call any model, dispatch any tool, or retain anything hidden. One of the engineers noticed that Lua's `:` method syntax here acts like `.append()` in Python, and that is a good way to read it.

### 5.5 What went away: the `reply` register

In the old design there was an implicit variable, `reply`, that always held whatever the model last said. You never declared it; it was just there. It is gone. If you want a result, capture it in a variable, put it in `var`, write it to the store, or return it. Explicit, always.

---

## Part 6: Tools, and why explicit tool scoping is the whole point

### 6.1 Two layers of tool access

This took the engineers a while and is worth getting exactly right. There are **two separate decisions** about tools:

1. **Binding** (frontmatter, YAML). The frontmatter names every tool this prompt is allowed to use at all. If it is not bound here, nobody in this prompt can touch it.
2. **Advertising** (Lua, `tools.add`). Inside a section, `tools.add("search")` puts a bound tool into the **model-visible scope**. The model can only see, and only call, tools that have been added this way.

Binding is the outer fence. Advertising is the inner one. A tool that is bound but not advertised is invisible to the model.

### 6.2 `tools.call`: Lua uses tools the model cannot see

Your Lua code can directly dispatch **any bound tool**, advertised or not:

```lua
local result = tools.call("search", { query = "C++" })
```

This is deterministic, author-directed dispatch. The model is not involved. The design phrase for this is that direct Lua dispatch "may access bound but unadvertised tools."

### 6.3 The example that made it click

Suppose your frontmatter binds two tools: a web search tool and a file explorer. In one Lua fence you write `tools.add("file_explorer")` and call the model. That model instance can read files and cannot search the web, even though search is bound. In a later fence you write `tools.add("search")` instead. Now that model instance can search and cannot read files.

Same prompt, same bound tools, two different model calls with two different views of the world.

### 6.4 Why this is the value proposition

In a general-purpose harness, the model can call any tool it has access to at any moment: shell out, search, explore files, spawn agents. Every turn, the model has to decide which of many tools to use. That decision-making load is part of why those harnesses need frontier-class models to work well.

PromptForge's bet is that if **you** give each model call exactly the tools it needs and nothing more, the model has less to decide and a smaller, cheaper model can do the same work. The designer stated it plainly: you want to add exactly the tools the model needs and not one more. This is not a convenience feature. It is one of the core reasons the project exists.

---

## Part 7: `models.loop`, the multi-turn engine

### 7.1 Why `models.infer` is not enough

`models.infer` is tool-free by design. If the model responds with a tool call instead of text, `models.infer` raises an error. So the moment you advertise tools, you need something that can run the loop: model speaks, model asks for a tool, tool runs, result goes back, model speaks again, until the model stops.

That something is **`models.loop`**.

### 7.2 What it does

```lua
tools.add("search")
local history = messages.new():system(prose):user(question)
models.loop(history)
```

`models.loop` takes a message array and drives multi-turn inference on it. When the model requests a tool, `models.loop` dispatches the tool (in Rust), appends the tool result to the array, and calls the model again. It keeps going until the model produces a final answer with no further tool calls. When it returns, the array contains **every** assistant and tool record from the exchange. The design calls this "protocol-complete history."

Two properties worth memorizing:

- **It returns nil.** The result is not a return value; the result is the mutated message array. The array is the only continuity state, and you own it.
- **It behaves identically with zero or many tools.** No tools advertised? It still runs a loop, which happens to end after one turn. The code path is the same.

`models.loop` reads the section's current model selection and current advertised tool scope **at call time**. So `tools.add` before the call affects it; `tools.add` after the call affects the next one.

### 7.3 The Lua/Rust ownership split

The design is careful about who does what. Learn the boundary:

**Lua (you, the author) owns:**
- Orchestration: which models to call, in what order.
- Message construction: what goes in the array.
- Reshaping results: pulling records out, rearranging, selecting what to keep.
- Compaction policy: when and how to shrink history (Part 9).
- Interaction policy: whether user input enters the messages.

**Rust (the runtime) owns:**
- Model-tool continuation: the actual loop of dispatch, append, re-call.
- Protocol-safe history appends: making sure the array stays valid for the provider.
- Scheduling.
- Implementing the tools themselves. Lua does not implement web search; Rust does. Lua decides whether to advertise it.

The point of the split: everything that is **policy** stays in Lua where you can read and change it. Everything that is **mechanism** lives in Rust where it is fast and correct.

### 7.4 Wrapping a model call in `pcall`

A model call can fail: provider error, context overflow, a tool blowing up. Lua's `pcall` runs a function and catches errors instead of propagating them:

```lua
return pcall(function()
  models.loop(history)
  return history
end)
```

You will see this pattern in the worked example in Part 8. Read `pcall` as "try this and tell me whether it worked."

---

## Part 8: Moving data between sections

### 8.1 The transfer channels

Part 4 established that sections are isolated. So how does anything get from one to the next? The design names exactly four channels and forbids everything else:

- **Task input.** When you invoke a section, you pass it an argument explicitly. The section receives it as `args`.
- **`var`.** A JSON clipboard that travels with control flow. It is carried by fall-through and jump, cloned into `call` children, and isolated from child writes (a child can read the parent's `var` but its writes do not come back).
- **Return values.** A section can `return` a value to whoever invoked it.
- **The store.** A virtual file system shared across the run. Write a file in one section, read it in another.

If you find yourself wanting to share something and it does not fit one of these four, you are fighting the design.

### 8.2 Ways control moves

- **Fall-through.** Execution reaches the end of one section and continues into the next at the same heading level. The clipboard `var` comes along. Note that control never passes from an H2 into an H3 implicitly; sub-sections are invoked, not fallen into.
- **Jump.** Transfer control to another section by name. `var` comes along.
- **`call(heading, input?)`.** Synchronously invoke a section as a child. It gets a fresh VM, a clone of `var`, and optionally a new `args`. It runs to completion and returns its final text to the caller. Recursion is allowed up to depth eight.

Every one of these creates a fresh VM at the target. The constraint in the design reads: "Preserve fresh VMs for fall-through, jump, call, and every child task entry; use explicit task input, `var`, return values, and store as transfer channels." You now understand every word of that sentence.

### 8.3 Sections that look ahead

One thing that surprised the engineers: a Lua fence can reference a section heading that appears **after** it in the file. A controller section near the top can invoke a worker section defined below. This is normal; sections are named entry points, not lines to be reached in order.

### 8.4 `execute(path, input?)`: invoking another file

`call` invokes a section in the same file. **`execute`** invokes a whole other prompt file as a child. The child gets fresh prompt state, its own model and tool bindings, and shares the parent's store. Parent globals and `var` do not cross the file boundary.

`execute` by path is **deferred** in the current plan. It is documented so you know the shape, but it is not being built yet.

### 8.5 The worked example: fanout

This is the example the session spent the most time on, and it ties together everything from Parts 3 through 8. `fanout(section, inputs)` is itself deferred, but it is the clearest illustration of the model, so learn it.

The file has a **Criteria** section: seven bullet points, each naming something to investigate. It has an **Analyze** section that looks like this:

````markdown
### Analyze

Search the web for information about {{ item }}. Identify design alternatives...

```lua
tools.add("search")
local history = messages.new():user(prose)
return pcall(function()
  models.loop(history)
  return history
end)
```
````

And it has a controller section whose Lua does the orchestration:

```lua
local items = bullets_to_array(prompt.section("Criteria"))
local results = fanout("### Analyze", items)
```

Walk through what happens, step by step:

1. `prompt.section("Criteria")` fetches the Criteria section as text. The engineers compared this to a Beautiful Soup parser: go to the heading, grab the contents. No model, no VM, just parsing.
2. `bullets_to_array` splits that text into an array of seven strings, one per bullet.
3. `fanout` invokes the Analyze section once per string. Each invocation gets its **own fresh VM** and its string as `item`.
4. Inside each Analyze VM, reading `prose` snapshots the section, substitutes `{{ item }}` with that bullet's text, and memoizes the result. The model does not get the raw bullet; it gets "Search the web for information about [bullet text]. Identify design alternatives..."
5. `tools.add("search")` advertises the search tool to this model call. Without it, the instruction "search the web" would be impossible to follow; the engineers caught this exact bug in an earlier draft.
6. `models.loop(history)` runs the multi-turn exchange, appending every assistant and tool record.
7. `pcall` catches any failure so one bad bullet does not kill the other six.
8. Each Analyze VM `return`s to `fanout`, which collects all seven results into `results` in the controller.

Now ask the Part 4.3 question: which sections are model-facing? **Analyze** is, because its Lua calls `models.loop`. **Criteria** is not; it is parsed, never sent. The **controller** is not; it orchestrates but never calls a model itself.

---

## Part 9: Compaction, or how to give a model a brain injury carefully

### 9.1 The problem

Every model has a context window: a maximum number of tokens it can attend to at once. A long conversation eventually exceeds it. The standard remedy is **compaction**: summarize the older history into a shorter form and continue with the summary plus recent messages.

The designer's phrase for this was that compaction is "a traumatic brain injury." The model loses granularity. One engineer admitted he treats the compaction prompt in commercial tools as the signal to just close the session, because he has learned the model will be noticeably dumber afterward.

PromptForge does not eliminate compaction. It makes the injury controllable and keeps a full medical record.

### 9.2 Two histories, not one

This is the central concept. There are **two** records of a conversation:

- **Canonical events.** The complete, append-only log of everything that actually happened: every message sent, every tool called, every compaction performed. This is the audit trail. It is owned by the host.
- **Model-facing message array.** The array you built in Part 5 and pass to `models.loop`. This is what the model actually sees on the next call.

At the start of a conversation these two are identical. **The moment you compact once, they diverge.** The model-facing array now contains a summary where the canonical log contains the real messages. From that point forward, new messages are appended to both, but the model never again sees the pre-compaction originals through its normal context.

One engineer's restatement was exactly right: the canonical log is the real transcript; the model might be seeing something different if there has been a compaction.

### 9.3 Why keep the canonical log

Three reasons:

- **Audit.** You can always answer "what was actually said?"
- **Replay.** When cold restart and durable replay are eventually implemented (deferred, see Part 15), the canonical log is what gets replayed to reconstruct state.
- **Retrieval.** The model cannot see the canonical log directly, but it will eventually be able to reach it through a tool or the virtual file system. Imagine asking "go through this chat and tell me every time I referred to the gateway." The summary lost that detail; the canonical log still has it.

So you get both: a small context for the model, and no loss of history for you.

### 9.4 The constraints, decoded

Two constraints in the design document now read clearly:

- "Keep canonical events append-only and separate from mutable model-facing message arrays." The word "keep" means: as you implement things, do not break this separation.
- "Keep the canonical event log host-owned and unavailable to prompt Lua." Your Lua cannot reach into the canonical log and edit it. It can only shape the model-facing array. The log is the host's.

### 9.5 When compaction triggers

Two triggers:

- **Precheck.** Before sending, the runtime estimates the token count and sees it will not fit. Proactive.
- **Provider overflow.** The request was sent and the model's provider reported that the context was too large. Reactive.

`models.loop` invokes the selected **compactor** when either fires.

### 9.6 Who decides what the summary says

Rust does not. The design lists as a non-goal: "Do not make Rust choose future summary wording or retention policy." The compactor is a policy you supply from Lua. It can call tool-free `models.infer` to produce its summary, and it can decide what to keep and what to drop.

Only the minimum compactor surface is being built right now: the hook that invokes a compactor, and one built-in policy, `compactors.fail`, which refuses to compact and raises a context-exhaustion error instead. Real summarizing compactors are deferred. In other words, the plan builds the seam and leaves the hard part for later.

### 9.7 The payoff

Come back to Part 1.2. The reason a carefully designed agent drifts in someone else's harness is that it does not control compaction. In PromptForge, the compactor is yours. After every compaction, it can put your agent's instructions right back at the top of the array. The agent stays in character forever, no matter how long the conversation runs.

---

## Part 10: Talking to humans, and telling the model the truth

### 10.1 `user_input()` and the input broker

Sometimes a prompt needs something from a person. The call is:

```lua
local text, available = user_input()
```

This goes through one **generic input broker** in the host. The same broker serves two callers: your Lua directly, and a model-visible tool that lets the model itself ask a question (like the multiple-choice question tool in commercial assistants). One broker, two entry points.

### 10.2 The three host policies

The host decides what `user_input()` does, and the policy is one of three:

- **Block.** Wait for a human to type something. This is what the agent window does.
- **Unavailable.** Report immediately that there is no human. This is what a headless command-line run does.
- **Fail.** Raise an error.

Your Lua then decides whether the returned text enters the message array. That decision is yours (interaction policy is Lua-owned, per Part 7.3), not the host's.

### 10.3 The exact fallback sentence

When the policy is "unavailable," `user_input()` returns `available == false` and `text` set to exactly:

> User input is unavailable, use your best judgement.

Now the subtle part, which the designer explained just before leaving. Suppose the **model** called the ask-question tool and no human is attached. Something has to come back to the model. If you simply return that sentence as the tool result, the model might read it as the human's answer. That would be a serious mistake: the model would proceed as if a person had said "use your best judgement" when in fact nobody said anything.

So the design requires "preserving the exact fallback sentence while distinguishing it from human speech." The model must be told, unambiguously, that this is a system condition and not a reply.

### 10.4 The general principle: explain and redirect

The designer flagged this as a recurring theme across the whole system. Whenever the model receives a result, especially a failure, two things must be true:

1. **Explanatory text.** Tell the model in plain English what happened. "You are running in headless mode; this tool is not available."
2. **Tell it what to do instead.** "There is no human here and there never will be, so use your best judgment."

A model that gets a bare error code stalls or hallucinates. A model that gets an explanation and a redirection keeps working. Design every result the model sees with this in mind.

### 10.5 Three kinds of failure

While on the subject, the designer laid out a taxonomy of failures that clarifies who handles what:

- **Terminal failure.** A resource error, corruption, something that ends the entire run. Nobody recovers from this; the run stops.
- **Soft failure.** Something bad but recoverable, like `execute` being asked to run a file that does not exist. Lua can trap this with `pcall`, print a message, and decide how to proceed.
- **Model-facing failure.** The **model** tried to do something (call a tool, spawn a task, ask a question) and it did not work. This does not become an exception. It becomes a message to the model, in English, per Part 10.4.

The distinction is who is the audience for the error: the runtime, the author's Lua, or the model.

---

## Part 11: Three kinds of author

The functional specification describes three archetypes. They are cumulative: each uses everything the previous one uses, plus more. Where you sit tells you which parts of this tutorial you need daily.

### 11.1 The routine tool-free pipeline author

You write sections that each read `prose`, call `models.infer`, and pass results forward through `var`, the store, or return values. No tools, no message arrays, no loops. This is most batch work: classify these documents, summarize these papers, draft this section. Parts 3, 4, 5.1, and 8 are your world.

### 11.2 The stateful or tool-capable author

You build a message array (with `messages.new()` or a raw table), advertise tools with `tools.add`, and call `models.loop`. Between model operations you may remove or reshape records in the array. "Stateful" here just means you hold onto a message array and keep working on it. Parts 5 through 7 are added to your toolkit.

### 11.3 The interactive author

You call `models.loop` repeatedly over **one retained message array**, feeding in user input through the generic broker between turns. This is a chat agent. Part 10 joins the set. Persistence of that retained array across restarts is deferred, so for now an interactive session lives as long as the process does.

The deferred task contract extends this: an interactive author will eventually be able to start isolated background work, keep talking to the user, and consume the finished results on a later turn without blocking the section VM. Standard concurrency, not yet built.

---

## Part 12: Runtime metadata and the H1

### 12.1 The `sys` table

Every section has access to a small, **immutable** table called `sys`, sealed at section entry. It holds operational metadata: the time, an identifier, the section name, the execution, the section count. Read it; you cannot write it.

One of the deferred open questions asks what belongs in `sys` and what does not. The design's answer so far: things fixed at section entry (like start time) go in `sys`. Things that only become known later (model identity, finish reason, request IDs, projection hashes, metrics) are **host-observer data**. They are recorded by the host for logging and inspection, but they do not get stuffed into `sys` and they are not returned to Lua from `models.loop`. This is the "one way to do things" instinct applied to metadata.

### 12.2 The H1

The top-level heading of a prompt file is somewhat special. It is the bootstrap: where the file's identity is established. The design's stated goal is to make it as un-special as possible, while acknowledging there is a certain amount of specialness that cannot be avoided. How much is still an open question.

---

## Part 13: The agent window is just a prompt

### 13.1 Nothing about the chat UI is hard-coded

The chat window in the Workshop (PromptForge's IDE) is not implemented in Rust as a special case. It runs a prompt, `chat.md`, written in the same Markdown and Lua you have been learning. The constraint reads: "Keep all user-visible agent behavior editable at runtime through Lua or prompt files. The agent window is not Rust-special."

If you want the chat agent to behave differently, you edit a prompt file. No recompile.

### 13.2 The Mentographist example

The designer illustrated why this matters with an existing prompt called the Mentographist, an agent that interviews you. Today it runs inside a commercial IDE. The IDE's system prompt goes first; the Mentographist's instructions arrive as user messages or tool data; after a couple of compactions the agent loses its grip on its own instructions and gets fuzzy.

Reimplement the Mentographist as a PromptForge prompt and it controls the system prompt and the compactor. After every compaction it puts its own instructions back at the top. It stays in character indefinitely.

Now generalize. "New agent" in the Workshop can open a list: Mentographist, Architect, a Python tutor, a debt collector, anything. Each is just a prompt file. Each survives compaction. Each can look back through the canonical history (Part 9.3), index the whole conversation, and enrich its own context with things you said an hour ago.

---

## Part 14: Why any of this matters

This section is the designer's argument for the project, given in the middle of the session when the engineers admitted they were still fuzzy on the purpose. It is not part of the specification, but it is the reason the specification exists.

### 14.1 Tools are what make a model useful

A model with no tools is sterile: a sandbox you can only talk to. Give it tools and it can search, code, edit files, shell out, compile, read its own output, and fix it. Give it a harness that also has access to **your** knowledge (your design principles, everything you have ever told an AI, indexed and retrievable) and it becomes something else again: an assistant that already knows your project before you type the first word.

### 14.2 The economics flip with local inference

Today everyone is a token miser. Frontier inference is billed per token, so you send as little as possible and let the card sit idle. But if you own a GPU with spare VRAM, running a model on it costs nothing extra. Now the incentive inverts: you want inference running **constantly**. While you type, a local model should be indexing your codebase, analyzing the conversation, pre-loading context, surfacing tips. An idle local card is wasted capital. Consumer cards with very large VRAM are already available at non-exotic prices, and nobody has built the harness that exploits them.

PromptForge, with a gateway that can route to local models, is meant to be that harness.

### 14.3 The escape hatch

The designer's closing argument was blunt. The proprietary tools people rely on are going to get worse: more expensive, more restricted, less willing to do what you ask. The frontier models will follow. There is a limited window to build your own tools before that happens. PromptForge is designed as the escape: an IDE that works the way you want, running open-weight models on your own hardware, so the productivity of the current moment survives whatever the vendors decide.

Whether the ideas are, in his words, "green field with money on the table" or "huffing the AI sauce," he put at fifty-fifty. The engineers voted green field.

---

## Part 15: What is deliberately not being built yet

A good specification says what it is not doing. The design does this in two lists, and it is worth knowing them so you do not go looking for features that are not there.

### Deferred (will be built later)

- **Lexical Lua inheritance.** Writing a function once and reusing it across sections without copy-paste.
- **Confined modules, `require`, `include`, `local_include`, partial Markdown fragments.** The include APIs do not exist yet; the current plan has no removal, compatibility, or migration work for them.
- **Child concurrency and the task contract.** `call_async`, `execute_async`, `tasks.await_all`, background work that does not block the section VM.
- **Path-based `execute`.** Invoking another prompt file as a child.
- **`fanout` and `pfanout`.** The helpers from Part 8.5, built on the task runtime.
- **Durable replay and cold restart.** Replaying the canonical event log to reconstruct a session after quitting and reopening the Workshop.
- **Event view removal.** Even the engineers in the room were not sure what this one was; it is deferred, so it does not matter yet.
- **Persistence of the interactive message array.** Chat sessions do not survive a restart.
- **Full compactor framework.** Summarizing compactors; only `compactors.fail` ships.
- **Stable identities across replay.** How a continuing conversation, its message projection, its compactor policy, and its pinned prefix keep stable identities through replay without serializing Lua tables or closures.
- **Operator semantics for frontmatter `input` and `output`.** The fields exist; exactly how Rust reads from the input and writes to the output is undecided.
- **Mentographist-style background research and PaperGate-style ordered parallel evaluation.** Kept as acceptance scenarios for the future task runtime.

### Non-goals (out of scope by design)

- Forking or replacing the gateway's model-specific chat-template responsibility.
- Making Rust choose summary wording or retention policy.
- Sharing mutable Lua state between sections.
- Adding implicit trailing-prose behavior back, unless measured authoring evidence justifies it.
- Redesigning the Workshop presentation, gateway administration, or speech-to-text.
- Redesigning store semantics beyond what the active run requires.

### Success criteria (what "done" looks like)

- One public executor runs finite pipelines, autonomous episodes, and persistent interactive agents from Markdown plus Lua.
- Every model request originates from an explicit Lua call and carries a validated provider-neutral role sequence.
- One Rust-backed `models.loop` appends protocol-complete history, processes every structured model tool call, returns nil, and behaves identically with zero or many model-visible tools.
- The agent window keeps working through the generic input broker and the active `models.loop`. This means "do not break it while making the changes," not "it never blocks."
- Prompts, examples, guides, and tests touched by the active work use `promptforge: 0` and its explicit model.
- Reconnect persistence, Workshop restore, concurrency, and composition contracts remain deferred.

---

## Glossary

- **Advertise**: make a bound tool visible to the model via `tools.add`.
- **Bind**: declare a tool in frontmatter so the prompt may use it at all.
- **Canonical events**: the complete append-only host-owned record of everything that happened in a run.
- **Compaction**: shrinking the model-facing history to fit the context window. The canonical log is untouched.
- **Compactor**: a Lua-supplied policy that `models.loop` invokes on precheck or provider overflow.
- **Fall-through**: control continuing from one section to the next at the same heading level, carrying `var`.
- **Frontmatter**: the YAML block at the top of a prompt file declaring tools, models, version, input, and output.
- **Host / host integrator / harness**: the runtime that connects the model to the world. In PromptForge, the Rust runtime plus gateway.
- **Host-observer data**: metadata recorded by the host (model identity, request IDs, metrics) that is not exposed to Lua.
- **Inert**: Markdown that no Lua fence reads. Equivalent to a comment.
- **Model-facing section**: a section whose own Lua fence calls a model.
- **Message array**: the ordered list of role-tagged messages that is a model's entire memory.
- **Pending prose buffer**: Markdown accumulated since the last heading, Lua fence, or thematic break.
- **`prose`**: the read-only, lazy, memoized value a Lua fence receives holding the buffer above it.
- **Provider-neutral**: one message format for all model vendors; the gateway translates.
- **Section**: a heading and everything under it. The unit of VM lifetime.
- **Store**: the run's virtual file system, shared across sections and child prompts.
- **`sys`**: immutable per-section metadata sealed at entry.
- **Thematic break**: a Markdown horizontal rule. Clears the pending prose buffer, turning the text above it into a comment.
- **`var`**: the JSON clipboard carried across fall-through, jump, and cloned into `call`.

---

*2026-09-15 12:45 - claude-fable-5.1*
