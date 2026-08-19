# Promptforge.md session, Aug 16 afternoon

*2026-08-16 14:31 - transcript 94084ecb-026e-49b7-ab8d-bbc344ac238a*



## Prompts



**[p1]** @promptforge/promptforge.md

**[p2]** promptforge echo this is it

**[p3]** add a model binding for "any model"

**[p4]** you butchered that because you didn't use a 4-tick fence

**[p5]** why did echo move to @promptforge/prompts/echo.md when it should have been used @promptforge/local/prompts/echo.md

**[p6]** who uses @promptforge/prompts

**[p7]** prompts/valid is not at the root that's a different prompts dir. I asked about /prompts

**[p8]** so is the mcp server running?

**[p9]** I want @promptforge/promptforge.md to run the MCP server and I want the prompts to be executed as MCP Tool calls

**[p10]** the root toml should not even be used

**[p11]** is there a way to invoke an mcp service from JSON injected in the context rather than in mcp.json ?

**[p12]** promptforge echo Now is the time for all good men

**[p13]** I wanna make it so that you don't need an H2, like if the H1. If there's no Section after the H1, and the model doesn't end, doesn't end in a tool call, then I think we should just end right there. Then the model's output becomes the output. What do you think about that?

**[p14]** I don't understand what you're saying. What is this, what's default return? What the fuck is default return? What does that mean, def beat the model's reply? Is default return a lua command that we ended? That we invented?

**[p15]** To be honest, I don't like that yamal. I don't like that default return in the YAML. Why do we have that? Is there any rationale? I think we should just get rid of it, or should we? Because if they want a default return, isn't it easy enough to just, like, do like a goto and then a section? Like, if you wanna have a default return so that multiple areas all end the same way, just do a goto, an H2, that returns a constant string. And one of the, one of the design principles of PromptForge is we never create a feature that does something that can be implemented by the user using other fe-more general features already, right?

**[p16]** yes fold it in and also, how do you set last_reply with jump() ?

**[p17]** you keep using triple backticks when you output fenced blocks with interior backticks

**[p18]** What exactly is last reply? Is that the Lua variable?

**[p19]** why didn't we call it `reply` in rust

**[p20]** So, so here's, here's my thinking. Let's say we have a block, we do some Lua, we have, we have the prologue. Then we run the prose, and the prose generates some text, so we have a reply. Now we go back into Lua. Now, if that Lua wants to make a decision and it wants to jump, it has no way of trans it ha it doesn't even have the option of transferring the reply to, with it, into the next block. And I think it should, because what if you wanna implement a decision? Like, what if you wanna do some inference? Okay, now you've done some inference, and now you wanna jump based on some decision that has to do with something else. You can't, you can't pass the reply through. This is an inconsistency. So one of the design principles of PromptForge is that everything behaves as consistently as possible, unless there's a really good reason. And so one of the invariants is that when you, when you enter, when you enter a section, the model's previous reply is always in the reply variable. And this would break that.

**[p21]** Yes, I, I think, I think the right thing to do is to Pulled it in and If the If the user doesn't want, if the user doesn't need the reply, they can just clear it themselves. They can just set last_reply equals nil before they perform the jump. Also. And then in the destination, like if the destination section doesn't really need it, if it doesn't care, then it just won't mention it. And I also want to know, so when, when, when, when prose creates a reply, the only way for pro for the, for the next block of prose to use it is through the substitution, isn't that correct?

**[p22]** Question: can we fold incoming_reply, reply, last_reply into just `reply` ?

**[p23]** include this rename

**[p24]** I'm going to need you to fix ALL the documentation in the repo to reflect these changes.

**[p25]** Also, can lua terminate the prompt early and return `reply` ?

**[p26]** you did the backtick fuckup again

**[p27]** Fix the plan and repeat that last output

**[p28]** stay in plan mode and are we introducing any new behavior or change in behavior that needs examples in the docs?

**[p29]** I have a question. Explore how {{ reply }} can be used to inject information, versus injecting instructions. Because it seems kind of ambiguous. The prose is passed to the model, and it includes substitutions

**[p30]** the user can always fix it

**[p31]** reply = wrap(reply)

**[p32]** apply @cabinet/_output/vibe-coding-rust-guide.md

**[p33]** is there anyting in @cabinet/_output/vibe-coding-rust-guide.md which is missing from @tools-public/rulebooks/vibe-rulebook.md

**[p34]** is there anyting in @cabinet/_output/vibe-coding-rust-guide.md which is missing from @tools-public/rulebooks/rust-rulebook.md

**[p35]** throw @tools-public/rulebooks/rust-rulebook.md into the mix

**[p36]** Did you decompose the plan into testable steps that each commit?

**[p37]** does @cabinet/_output/vibe-coding-rust-guide.md tell you to decompose?

**[p38]** I want you to fix @cabinet/_output/vibe-coding-rust-guide.md and @tools-public/rulebooks/vibe-rulebook.md to use crystal clear, unambiguous, imperative language to make absolutely certain the rules are followed. See @tools-public/rulebooks/prompts-rulebook.md . Do this now. And only do this now. Then switch back to plan mode.

**[p39]** move @cabinet/_output/vibe-coding-rust-guide.md to @tools-public/rulebooks//vibe-rust-rulebook.md and update the title inside the file

**[p40]** apply @tools-public/rulebooks/vibe-rulebook.md and @tools-public/rulebooks/rust-rulebook.md to the plan @c:\Users\Vinnie\.cursor\plans\h1-only_prompt_support_902d35fc.plan.md

**[p41]** review the plan then run it

**[p42]** why are the command lines exporting the keys and shit when we just did the env feature?

**[p43]** does promptforge.md need update?

**[p44]** would it be better to just let the model discover the MCP api by querying it once? and then it is in context

**[p45]** @promptforge/local/papergate.md:5 why is this in the YAML? shouldn't it be in the lua ?

**[p46]** my point is that it belongs in the H1 as

**[p47]** tools.max_use(24)

**[p48]** dont fucking manage my schedule

**[p49]** So I'm thinking like we definitely need to move it out of the YAML, like it has to go My thinking is this, there should be like a default. I think that's global. Is that global? Global doesn't really make sense. Global, the global doesn't make sense at all. Other than Like setting it to a really large number, like a thousand, right? Like, because otherwise every time you, every time you change something, you have to think about, oh, did I, you know, did I, did I surpass the global? Like, if you start adding sections, then you run into the limit, it doesn't make sense. The real limits need to be per section. Analyze that.

**[p50]** tools.at_most ?

**[p51]** tools.call_limit ?

**[p52]** I would go with call_limit. Now analyze how this plays out for fanout

**[p53]** you fucked up the fence. use 4-tick outer

**[p54]** ```
### Web Research

**[p55]** ```lua
tools.add("search")
tools.call_limit(1)
```

**[p56]** Search for {{ item }}

**[p57]** ```lua
tools.remove("search")
tools.add("fetch")
tools.call_limit(3)
```

**[p58]** Check pages for {{ args }} and report a summary of matches

**[p59]** I dont think it exists. Check the code. There's a problem though, wouldn't the old tool call still be in the context? the model could infer that the tool is stil available. how does the tool info work

**[p60]** could we go through the history and scrub the tool offering and the tool call?

**[p61]** this could have side effects. the model would see information appearing out of nowhere

**[p62]** is reply populated from the tool call like that? check the code

**[p63]** That's not necessarily a good thing. I want promptforge to be able to express the search/fetch pattern used universally, and just add the behavior that the search is available only in the 1st turn, and the fetch is only available in 2nd and later turns

**[p64]** no I'm not saying that either. I'm ok with going to the next section but the way you wrote it, it could change behavior. I want the behavior to be the same as the traditional way, except that the toolset is constrained'

**[p65]** no, migrating the whole conversation is a design non-goal

**[p66]** I don't know if I even wanna have the, I don't, we shouldn't have a default limit. You're thinking twenty-four is a default limit, but defaults are kind of toxic because it's like, it's like an invisible setting that can change and then it can change the behavior of prompts. And the whole point of prompt forge is to be as deterministic as possible while still having the capability of inference. So like, that twenty-four goes against the philosophy.

**[p67]** Not sure that there should be a limit though. I mean, won't we eventually overflow the context? A large, a large model is gonna naturally come to a conclusion, and with the big context, it'll be fine. A small model with the smaller context, the context will fill up, and then we'll get an error.

**[p68]** The Make them count prompts is, that's just, that's just text that goes in the, to the model. How does tool calls do anything?

**[p69]** did we ever make these changes



## Plans

### H1-only prompt support

*Allow prompts with no H2 sections. When a prompt has only an H1, run its blocks (Lua and prose) and use the model's reply as the prompt output.*

# H1-Only Prompt Support

Allow prompts with no `##` sections. The H1 runs its Lua and prose blocks, and the model's last reply becomes the prompt output.

## What changes

### 1. Parser: remove the "no sections" rejection

In [`crates/promptforge-core/src/parser.rs`](crates/promptforge-core/src/parser.rs) around line 413, delete the check:

```rust
if section_headings.is_empty() {
    return Err(Error::Parse("prompt has no ## sections".into()));
}
```

Allow `prompt.sections` to be an empty `Vec<Section>`.

### 2. Fix `Prompt::entry()` 

In [`crates/promptforge-core/src/parser.rs`](crates/promptforge-core/src/parser.rs) around line 436, `entry()` assumes sections is non-empty. Either make it return `Option<&Section>` or guard callers. Check all call sites.

### 3. Executor: carry H1 reply out

In [`crates/promptforge-core/src/execute/h1.rs`](crates/promptforge-core/src/execute/h1.rs), `LiveH1State` tracks `returned` (from Lua `return`) but not the model's prose reply. Add a `reply: Option<String>` field so the caller can use it.

### 4. Executor: handle empty sections

In [`crates/promptforge-core/src/execute.rs`](crates/promptforge-core/src/execute.rs) around line 238, after `execute_live_h1`, if `prompt.sections.is_empty()`:

```rust
if prompt.sections.is_empty() {
    return Ok(h1.reply.unwrap_or_else(|| "done".to_string()));
}
```

This skips `run_sections` entirely. The priority is: H1 Lua `return` (already handled above this), then H1 model reply, then `"done"`.

### 5. Tests

- Update or remove the existing `no_sections_errors` test in `parser/tests.rs:187`
- Add a parse test: H1-only prompt parses successfully with empty `sections`
- Add an execution test: H1-only prompt with prose returns the model's reply
- Add an execution test: H1-only prompt with only Lua returns via `return` or falls through to `"done"`

### Example prompt this enables

```markdown
---
name: summarize
description: Summarize the input
promptforge: 1
---

# Summarize

` ` `lua
models.always("m", "A model suited for careful analysis")
` ` `

Summarize this text in one paragraph.

{{ args }}
```

No `## Section` needed.


Todos:

- Remove 'no ## sections' rejection in parser.rs
- Fix Prompt::entry() to handle empty sections
- Add reply field to LiveH1State in h1.rs
- Handle empty sections case in execute.rs
- Update/add parser and execution tests

## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge\local\prompts\echo.md

---
name: echo
description: Return the input argument unchanged
promptforge: 1
---

# Echo

```lua
models.always("m", "any model")
```

## Main

```lua
return args
```


StrReplace-edited design docs (path only): `c:\Users\Vinnie\src\cursor\promptforge\promptforge.md`, `c:\Users\Vinnie\src\cursor\promptforge\prompts\echo.md`
