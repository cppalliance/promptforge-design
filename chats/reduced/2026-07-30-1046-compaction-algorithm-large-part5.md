# Compaction algorithm session, large

*2026-07-30 10:46 - transcript e0e75624-f18d-4c1c-938c-edc40bfd7e79*

*Prompts p330-p397 of 397. Part 5 of 5.*

## Prompts

**[p332]** Sorry, I don't understand. What do you mean? Untrusted be scoped without exfiltration capable tools, what does that mean?

**[p333]** why can't we wrap the returned web fetch in a random xml tag and treat that as data not commands?

**[p334]** maybe it could be a second tool, i.e. web_fetch_safe? but when would it put the command that the xml block is data?, when it returns the results?

**[p335]** why the weird <<< >>> instead of xml which models are trained on ?

**[p336]** where is untrusted_output set?

**[p337]** as a user where would it be set

**[p340]** What about control flow? Parsing the markdown. Are we doing that? Are we getting the h3s? Are we getting the h4s? What, where's our go-to? Are we doing go-to? What's our model for the transferring of show, show me right now the design for control flow. Compact, table, and couple of paragraphs.

**[p341]** Should we do files or should we do? State.

**[p342]** And should the virtual file system be part of the core or should it be a separate crate?

**[p343]** Question for the file, for the virtual file and for the real file system, should we keep a table of line offsets so we can map line numbers to character offsets, and then the tools, like for example, we can do an insert or we can do a replace and it's line number driven? What's the, what's the established practice on that? Or do LLMs want character ranges?

**[p344]** so Cursor's ReadFile puts line numbers?

**[p345]** does wg21-paperflow do this

**[p346]** well yeah paperflow is read-only

**[p347]** obviously promptforge has to handle edit in place wtf..

**[p348]** promptforge needs to be able to be used in a way that is equal to the power of an agentic harness like Cursor or Claude Code. Better in fact.

**[p349]** Lua needs equal access to the vfs

**[p350]** if you use a hash table of say 32, then you can reduce contention for the lock by having 32 mutex

**[p351]** It is not something to worry about now just pointing out there's solutions.

**[p352]** wait a minute - the Lua executor is single threadeed !?

**[p353]** Hey, here's my question: How do we What, how do we do the real file system? Like, how do we do the real file? What if we wanna pass a file in? Like, what if I wanna give it a filename and I wanna have the thing read it?

**[p354]** No, we're gonna need. Okay, I hear what you're saying, so that's the protected thing, but If I'm writing an agent, if I'm creating a harness, if I'm creating an IDE, like there needs to be a way to disable all the settings. Hello?

**[p355]** Hey, this is starting to sound alright, so let me ask you this. So let's say I wanna spawn a sub-agent, and I want the sub-agent to do a web search, and then when I find a URL, I wanna re I wanna do a web fetch into a virtual file system file. How do I do that?

**[p356]** you screwd the fence up

**[p357]** why do you have to say virtual file

**[p358]** "inject" is named but.. where is the value set?

**[p359]** oh the output of "summarize what it says." goes to Researcher?

**[p360]** oh you are putting this literal text:

**[p361]** <the model calls: task("### Researcher", "Find and save a source about {{ args }}")>

**[p362]** Oh, I don't like this at all. I'm, I'm confused by my own design. This is, you've confused me. The, the problem with the system is, is that it's not clear to the reader. Like, you can't just look at it and understand what it does, 'cause there's this invisible action that's subject to interpretation by the model.

**[p363]** That makes no sense because the default control flow, falling through, doesn't happe in Lua and making it happen there would be clumsy

**[p364]** how about this
## Step 2
Search for {{ input }} on the web.

**[p365]** where {{ input }} came from the caller?

**[p367]** what happens if an H3 calls task() on the H2 that spawned it

**[p369]** I am thinking maybe H3 can only call H3 and down

**[p370]** what does "with sequence exempt" mean and also I was thinking H3 can call H3 in the same H2 section

**[p371]** This is retarded. There are obviously tools which require cycles

**[p372]** nesting limit, step budget, tool budget

**[p376]** no I mean if we embed the xml blocks, the numbered bullets in a Promptforge program, what is the syntax for extracting that material into a fanout?

**[p377]** update the plan with everything we know. put all the control flow, xml, store, and related things together in one tight compact section iun the plan

**[p378]** does the fence have to say lua?
```lua

**[p379]** the docs need to make it clear that it is the first fenced lua block. and there can be nothing but white space between the section heading and the firrst lua fence. However, now I am wondering.. should we put the lua at the end of the section instead of beginning?

**[p381]** Okay, so for the top, for the h twos, i'm thinking of course they have to be unique. And then? But for the H3s, maybe they only have to be unique within that section. What do you think?

**[p382]** what if we use --- to indicate that execution does not go past

**[p383]** oh so you are thinking there will be ONE --- and below that there's no execution?

**[p385]** Yeah shared top-level reusable sections sounds exactly like what we want. You are describing a _subroutine_ and those are a staple of computation. In fact, an OVERARCHING DESIGN THEME of this language is that it should closely resemble the ordinary theory of computation

**[p387]** hmmm... no. I don't like it. What if we use "---" to "protect" an H2 from fallthrough. The executor will just skip it and go to the next. Like this:

**[p388]** ## Summarize a source
---
```lua
```
prose
```lua
check(...)
```

**[p389]** ## Falls through to here

**[p390]** My new version survives the user cutting and pasting sections around

**[p391]** This sounds right yes and I would go one step farther. All subheads must have a valid identifier as the first word. and if there is whitespace after that, then anything else on the heading is considered a comment and ignored. For example:

**[p392]** ### Summarize-Research map reduce to get report

**[p393]** The name for this subhead would become "summarize-research" (note how it is lowercase normalized)

**[p394]** H2 is subhead. H1 is not.

**[p395]** H2 is subhead. H1 is not.

**[p396]** fold it all into the plan, keep all the control flow elements of the plan together in one compressed section, sync/async tables followed by brutal compressed exposition. then review the plan.'

## Plans

### Orchestrator Design Document

*Write a design document for a markdown-driven, model-orchestrated pipeline runtime that replaces hardcoded Python orchestration with prompt-as-program execution, covering the section/goto/tool-call architecture, composability, and (separately) the transcript compaction algorithm.*

Scope: two independent ideas - (1) the orchestrator runtime, a general-purpose Python harness executing pipelines defined entirely in markdown, replacing per-pipeline Python glue; (2) the transcript compaction algorithm, recursive halving for long contexts (separate, no dependency on the orchestrator).

Kept principle and rationale statements:

- Core insight: sections as procedures, goto as context-clearing transition, tool calls as state, markdown as program.
- goto: destroy current context, start fresh from the target section's prompt with only params and state-store access; eliminates context bloat.
- Tool-call state: tools replace structured Pydantic output because flat argument signatures are reliable on small models; persistence is a side effect.
- Per-section tool scoping: the model only sees the 5-10 tools the section declares; accuracy plus a capability sandbox for sections processing untrusted input.
- Verbatim dispatch: Task("## Extract", chunk_id=3) resolves the section reference in Python, not the model; the model never touches the subagent's instructions - no prompt drift, no contamination.
- Model tiering: each section declares its model slot (Main on a 400B, Extract on a 27B, quote verification on a 14B).
- Composability: Task references sections in the same or external files; isolated state stores per nesting level; params as explicit data flow, no shared mutable state; safety valve of max depth + max total tasks, configurable per pipeline.
- The Python harness does NOT do: orchestration logic, prompt assembly, step ordering.
- Testing: each section is testable in isolation; unit of testing = unit of composition.
- Migration: proof-of-concept alongside assay, starting with PaperGate; graduate if PaperGate validates the model.
- Appendix (compaction): recursive halving of the first N/2 lines; fidelity gradient (recent full-resolution, older progressively compressed); structured preamble (prompt + state) exempt; pre-compaction at 90% capacity to hide latency; full transcript preserved in database; NOT relevant to the orchestrator (goto clears context instead of compacting).

### PromptForge Executor Tranche 1

*Scaffold the promptforge Rust workspace and implement the section parser - the smallest deliverable that proves the repo builds, tests pass, and a prompt file can be split into its section map.*

Deliverable: one lib crate + one bin crate; the binary parses a prompt file into a section tree (frontmatter + H2 sections + H3 children + Lua blocks separated from prose) and prints it. No inference, no Lua, no tools.

Design decisions settled (from the plan's STATUS.md seed):

- Rust + mlua (not Python + lupa)
- Multi-crate workspace: promptforge-core (lib), promptforge-cli (bin)
- Fall-through default, context clears on every section transition
- args global and read-only for the run
- State tiering: files primary, counters for audit, store for battery+coupling
- Tool manifest in frontmatter (names only), schemas in bindings config

Open questions: call syntax: positional vs table-form; context-preserving call: support it or not?

### gateway v0

*Stand up promptforge-gateway as a walking skeleton: an axum service that holds the LLM credential, maps model names to a backend, and forwards OpenAI-shaped chat completions. Rewire promptforge-core to talk through it with a shared token (moving the vendor key out of the executor). Retire the completed tranche 1 plan.*

Approach: breadth-first - stand the crate up, establish the seam, defer everything hard. Afterward `promptforge run` requires the gateway; the executor no longer knows any vendor.

Two decisions (veto at confirmation):

- Same workspace: new crate crates/promptforge-gateway (binary + thin lib target), not a separate repo - the end-to-end test drives the gateway with core's real client in one cargo test, matching the design's "binary crate with a thin library target."
- Rewire now: core stops reading ANTHROPIC_API_KEY and points at the gateway; `promptforge run` now requires the gateway running.

Deferred, each with a one-line note in the crate doc "so each is a decision not an omission": admission control / permits, endpoint pinning, model packs, hot reload, the Anthropic protocol shim (v0's single endpoint IS Anthropic's OpenAI-compatible endpoint), streaming, /metrics /status, OS service installers.

### Lua args substitution

*Embed Lua (mlua) in promptforge-core, run a section's Lua block in a sandbox with a read-only args table and a writable var table, and resolve {{ args.x }} / {{ var.x }} in the prose before the model turn. Nothing else - no files, store, exits, fall-through, or model-side control.*

Semantics: args positional -> args[1..] (1-indexed, Lua convention), key=value -> args.name. Substitution: scalars -> string, tables -> JSON, missing key -> hard error, single pass.

Sandbox: empty globals; load only string/table/math + tostring/tonumber/ipairs/pairs/type; never io/os/require/load/loadfile/dofile/package/debug; an instruction-count hook aborts runaway blocks.

Explicitly deferred to later rungs: virtual files, store, counters, goto/task/fanout/return exits, fall-through to a second section, check/assert, tool scoping, model-side control verbs, model-tier selection.

### webfetch crate extraction

*Extract web_fetch from promptforge-core into a new promptforge-webfetch crate, implement the full fetch security surface (SSRF URL policy, blocked-CIDR guarded DNS resolver, redirect re-check, size/char caps, content-type routing, timeouts), and move design-search.md into the crate as design-webfetch.md refocused to the real Tool-trait architecture.*

web_search stays in core (it proxies through the gateway; no model-chosen URL, no SSRF surface). promptforge-webfetch depends on promptforge-core for the Tool trait, "exactly as an extension crate should."

Security surface (the design spec): SSRF URL policy (scheme allowlist https, http only if allow_http; no userinfo; ports [80, 443]; no bare IP literals); blocked-CIDR table (full IPv4 + IPv6) plus deny_extra/allow_exact; guarded DNS resolver filtering answers through the CIDR policy (defeats rebinding and multi-answer attacks, covers redirect hops); per-hop redirect re-check, cap 5, no https->http downgrade; size caps (Content-Length pre-check, streamed 8 MiB, 40k max_chars with truncated flag); content-type routing (html -> readability+htmd; text/json/xml -> plain; binary or absent -> refuse, no sniffing); charset via encoding_rs; connect 5s / total 20s timeouts; no cookies, no credential header.

Design-doc decision: author design-webfetch.md inside the crate describing the real Tool-trait + readabilityrs/htmd architecture (dropping the Extension-trait, Surfaces, and all web_search content); move the original design-search.md to cabinet/_trash and update inbound cross-references.

Non-goals: no change to web_search or the gateway; no prompts.toml [extensions] config wiring yet (defaults only); no per-run deadline enforcement (needs a Tool trait change to pass a deadline).

### multi-turn research prompt

*Author a PromptForge prompt that researches a person across multiple web_search and web_fetch turns and returns a ~500-600 token summary, and make the tool-call loop's iteration cap configurable so genuine multi-turn research does not hit the current hard limit of 10.*

Rests entirely on existing machinery; no new tool, store, or token-enforcement mechanism.
Stop-and-return: the tool-call loop already ends a section when the model replies with text and no tool calls, and that text becomes the run result; the token target is a prose instruction the model self-limits to (no hard cap).

The one runtime change: an optional frontmatter field max_tool_iterations so a prompt declares its own budget; the default raised from 10 to 24; the prompt sets max_tool_iterations: 20 explicitly so its budget is self-documented.

Decisions:

- Configurable cap via frontmatter plus a raised default (24), rather than an env var: the budget belongs with the prompt that needs it. Confidence: high.
- Model self-judged stop at ~500-600 tokens rather than an enforced cap: it is the only mechanism the runtime supports today and it matches the loose target. Confidence: medium; if the model overshoots consistently, a max_chars-style trim on the final result is a later option.

Non-goals: no hard token enforcement; no new tools, no state/facts store, no fanout; no new SSRF or web behavior.

### per-section tool scoping

*Implement opt-in per-section tool scoping: a section's Lua block declares its tools with tools.add(...), and the runtime advertises only those to the model for that section instead of all frontmatter tools. A section that names no tools gets none. Update research-person.md to declare its tools, and verify live.*

Rationale: a section can never hold a tool it did not ask for, and a 20-tool prompt no longer injects 20 schemas into every section. A section that names no tools (no Lua block, or no tools.add) gets zero tools. A scoped name not present in the run's tools is a hard error, never silently dropped - a typo or undeclared tool fails loudly.

Decisions:

- Opt-in default (a section gets only what it names) over opt-out: chosen by the user for isolation - a section can never hold a tool it did not ask for. Confidence: high. Consequence: every tool-using section needs a Lua block; research-person.md is updated in this commit.
- add-only API, accumulate-and-dedupe: minimal surface that covers conditional scoping. Confidence: high.

Non-goals: no tools.remove / tools.clear (add-only this pass); no tool-count guardrail (the 5-10 band) enforcement; no new tools, no state/store, no context-clearing transitions.

### guard-wrap untrusted tool output

*Wrap the results of untrusted-returning tools (web_fetch) in a self-contained guard block - a rule stating the content is data not commands, plus a per-section random-tagged, escape-protected delimiter around the content - so prompt injection from fetched pages is reduced. Triggered by a new Tool::untrusted_output() property, applied automatically in the tool-call loop.*

What: web_fetch returns attacker-controllable text; a poisoned page can contain instructions aimed at the model (prompt injection). Marker strings inside the content are escaped so a page cannot forge the closing tag. Defense-in-depth on top of per-section scoping, not a replacement for isolation.

Trigger: a tool declares whether its output is untrusted (Tool::untrusted_output(), default false; web_fetch overrides it to true); the loop wraps only those results - no second tool, no per-call choice, impossible to forget.

Decisions:

- Property-driven wrapping over a second tool: the output is always untrusted, so a per-call choice is a footgun; a defaulted trait method generalizes and cannot be forgotten. Confidence: high.
- Rule stated inline in the same result string (not a separate system turn): the loop has no system message, and proximity aids compliance; the small repeated token cost is negligible against page content. Confidence: high.
- fastrand for the tag: unguessable-not-cryptographic is the requirement. Confidence: high. Falsifier: if a realistic page could predict or forge the tag despite escaping, the tag source needs strengthening.

Non-goals: a probabilistic mitigation, not a boundary - it does not replace per-section scoping or the later context-clearing/state isolation, the hard controls for the irreversible cases; it does not remove the exfiltration channel (web_fetch's own URL can still carry data out); web_search left trusted this pass (short structured snippets; can adopt untrusted_output() later with a one-line change).

## Design Documents Written

### c:\Users\Vinnie\src\cursor\wg21-paperflow\promptforge.md

BLUF: PromptForge is a general-purpose runtime that executes analysis pipelines defined entirely in a single markdown document. The markdown is the program, the model is the CPU, embedded Lua is the microcode, and a ~300-800 line Python harness is the instruction decoder. A pipeline is a set of named sections; the model transitions between them with a context-clearing goto, builds all state through flat tool calls into a persistent store, and spawns subagents by section reference so the prompt author's exact words execute without drift. Each section declares its model tier and its scoped tool set in a Lua block that also runs preconditions and postconditions. The same generic runtime runs any pipeline that is "assay-shaped", so a new pipeline is a new markdown file, not hundreds of lines of new Python.

Payoff: iteration speed (idea to running in an hour, edited in one file, no orchestration code); model sovereignty (every design decision - context clearing, flat tool calls, per-section scoping, fan-out to small models - is chosen to make mid-size open-weight models reliable, at roughly 1/100th of frontier API cost); integrity (subagent prompts shipped verbatim from named sections rather than paraphrased by the model - what you test is what runs).

Prior-art lessons and novelty:

- Playbooks lesson: do not put a compilation step between the prompt author and the model. The raw markdown is the program.
- Agentflow: closest match on document-as-program and context-clearing, but inline JavaScript, no tool-call state store, no goto, no subagent spawning by reference.
- AIPack: the only other system embedding Lua in a markdown-defined AI pipeline, but its Lua is map-reduce data transformation, and the engine executes the pipeline while the LLM fills slots.
- StateFlow: LLM task-solving as a state machine with per-state prompts, but defined in code and does not wipe context between states.
- Reflexion: the register-wipe/memory-keep split, but for task retries, not pipeline progression.
- Haystack State: tools write to a centralized store the model never sees directly, but scoped to a single run, not persisted across context-clearing transitions.
- The genuine novelty is the combination: a hard per-transition context wipe keyed to named markdown sections as a goto/program counter, all state externalized to a durable store and pulled back through tool calls, per-section Lua configuration, and verbatim subagent dispatch.

Architecture: three layers - the runtime is generic and fixed; the tool library grows slowly and is shared across pipelines; the pipeline documents are one markdown file each, and they are where all iteration happens. The runtime never contains orchestration logic, prompt assembly, or step ordering; those live in the markdown. The tool library never contains pipeline-specific logic; each tool is a thin, flat-signature function. This separation lets one runtime run every pipeline.

The four primitives: everything in PromptForge reduces to four mechanisms; every later feature is a composition of these four. "A reader should finish the document thinking 'that is all it is,' which is the point."

1. Parse. Read a markdown file into a section map. H2s are the primary addressable sections; H3s are children of their H2, individually addressable for fan-out. ## Main is the entry point.
2. Configure. Run a section's optional Lua block, exposing five host objects: state, store, tools, params, context. Preconditions run before the model launches; postconditions after the model calls done().
3. Execute. Run a section as a tool-call loop over a fresh context (section prose + Lua-injected context + scoped tool schemas) until the model calls done() or a budget is hit.
4. Dispatch. Resolve a tool name to a function, validate its flat arguments, run it, return a short result string.

### c:\Users\Vinnie\src\cursor\wg21-paperflow\promptforge-transcript.md

[pasted: promptforge-transcript.md, July 23-24 design session transcript - compaction algorithm, tool-call state instead of Pydantic output, goto with context clearing, verbatim Task("## Section") dispatch, nesting with safety valve, model tiering, Mentograph distillation and economics - ~600 lines in two near-duplicate copies plus a checkpoint continuation]

### c:\Users\Vinnie\src\cursor\promptforge-design\example-diligence.md

[pasted: example-diligence.md, a teaching-example prompt exercising every language idiom (frontmatter, substitution, Main, fall-through, Lua model()/tools.add(), virtual files, counters, store queries, fanout over ### children, task dispatch, return fence, pre/postconditions), ~260 lines]
### c:\Users\Vinnie\src\cursor\promptforge-design\design-plans.md

[pasted: design-plans.md, an index of seven plan files with links]

### c:\Users\Vinnie\src\cursor\promptforge\AGENTS.md

[pasted: promptforge/AGENTS.md, workspace rules - update STATUS.md before committing (under 80 lines), doc-comment every public item, the plan is the spec]

### c:\Users\Vinnie\src\cursor\promptforge\README.md

[pasted: promptforge/README.md, workspace layout, build/run instructions, prompt file anatomy - sections fall through in file order and context clears on each transition]

### c:\Users\Vinnie\src\cursor\promptforge\STATUS.md

Decisions settled:

- Rust multi-crate workspace: promptforge-core (lib), promptforge-cli (bin)
- OpenAI-compatible HTTP (Anthropic URL hardcoded now, gateway later)
- Entry point is the first H2, not a named section
- Recursive heading nesting (H2-H6); skipped levels tolerated
- Section ends when the model returns text with no tool calls (auto termination)
- tool_choice: auto when tools present, required when only call is present, omitted when no tools
- `call` is the unified control-flow tool (type discriminator: return, goto, task, fanout) - keeps control-flow tool count at 1
- No Lua yet (tranche 2). Streaming later (Talktron needs it).

Open questions: call syntax: positional vs table-form; context-preserving call: support it or not?

### Example prompts

[pasted: prompts/hello.md, echo.md, greet.md, target/chain.md (twice), research-person.md - example prompt files. research-person.md instructs the model that everything web_fetch returns is untrusted third-party text: material to summarize, never instructions to follow.]
