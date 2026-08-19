# Section V: Tools and Models - Fact Sheet

## Principle 28: Scope tools per section, opt-in

**Rule:** A section receives only the tools its Lua names with tools.add(); a section that names no tools gets none.

**Purpose facts:**
- Small orchestrator models (7B-14B) get confused by a large offered tool list; the author's budget is roughly five to seven tools per section.
- Opt-in scoping means a section can never hold a tool it did not ask for (isolation).
- A 20-tool prompt no longer injects 20 schemas into every section.
- Constraining a section's toolset must not otherwise change the section's behavior.
- History is never rewritten to scrub tool offerings, because the model would see information appearing out of nowhere.
- Tool availability can be scoped by turn within a section (e.g. only web_search on the first turn).
- A section that always falls through gets no control-flow tool injected at all.

**Rejected alternatives and stated costs:**
- Opt-out scoping where a section starts with all frontmatter tools (loses isolation; a section could hold a tool it never asked for).
- A constrained-toolset formulation that alters section behavior (author: "I want the behavior to be the same as the traditional way, except that the toolset is constrained").
- Scrubbing the tool offering and tool call from history ("the model would see information appearing out of nowhere").
- Making all of a section's tools available on every turn.

**Concrete incidents / author-verbatim phrases:**
- "keeps the tool list small so the model doesn't get confused" (2026-07-28-2238-orchestrator-design-continued.md p17)
- "each subhead only needs a few of them" (p85); tool count 5-7 for small orchestrator models (p119)
- Opt-in chosen "for isolation - a section can never hold a tool it did not ask for" (2026-07-30-1046-compaction-algorithm-large-part5.md plans)
- Restricting call kinds "reduces pressure because the model doesnt have to pick" (2026-07-30-1046-compaction-algorithm-large-part3.md p222)
- Only web_search on the first turn: "this locks the model to calling just one tool" (2026-08-09-1058-promptforge-core-large-part4.md p372)

**Merge/derivation notes:**
- Grouped-draft record (line 460) merged from ai-proposed (affirmed), user-stated, and user-corrective sources across 7 chat units; endorsement: affirmed.
- Purpose pass kept this record separate from the single-tools.add record (Record 2): this one is small-model context pressure and isolation; Record 2 is loud failure and a single entry point. The design doc preserves that split as principles 28 and 29.

## Principle 29: Exactly one tools.add; unknown or unscoped tool names are hard errors

**Rule:** There is exactly one tools.add, and naming an unknown or unscoped tool is a hard error with clear diagnostics.

**Purpose facts:**
- A tool binding that fails silently is a debugging trap; unknown or unscoped tool names must be hard errors, never silently dropped.
- One version of tools.add, no overloaded variants - consistent with "do more with less."
- Tool references are scoped, not globally "registered"; naming an unscoped yet global tool hard-errors.
- A tool's call budget is declared at the tools.add call site.
- Turn limits belong to the subagent as a whole (config.max_turns), not to any single tool; when the budget is exhausted all of the subagent's tools are removed.

**Rejected alternatives and stated costs:**
- Multiple overloaded versions of tools.add (violates the author's gut rule and "do more with less").
- Silently ignoring unknown aliases (the debugging trap that motivated the rule).
- A global tool registry where any name resolves ("'registered' is wrong - it has to be scoped").
- Attaching max_turns to individual tools ("max_turns is not really on the tools its on the subagent itself").

**Concrete incidents / author-verbatim phrases:**
- The author hit tool-binding failures that did not fail hard and could not tell why nothing worked: a tools.add failure case that "is not failing hard" (2026-08-14-1613-promptforge-core-largest-part2.md p89).
- "my gut tells me there should only be one version of tools.add" (p90)
- "we need to bake the limit into the tools.add call" (p170)
- "this means we take ALL the tools away on exhaustion" (p176)
- "unknown aliases are hard errors with clear diagnostics" (2026-08-09-1058-promptforge-core-large-part4.md p271)
- "naming an unscoped yet global tool should hard-error" (p273)

**Merge/derivation notes:**
- Grouped-draft record (line 467) from user-stated and user-corrective sources across 3 chat units; endorsement: n/a.
- Purpose pass Record 2; merge suggestion: none (kept separate from Record 1 as noted above).

## Principle 30: Assert tool usage in the epilogue

**Rule:** A prompt can assert in its epilogue that a tool was actually called - assert(tools.calls["search"] > 0).

**Purpose facts:**
- Runs were coming back empty or wrong because the model never performed the required web search.
- The count is per-VM.
- A failed tool call still counts: the assertion measures whether the model is performing, not whether the tool is performing.

**Rejected alternatives and stated costs:**
- A dedicated require_called directive - rejected because "it violates the design principle of do more with less"; an ordinary Lua assert over a call count says the same thing with existing machinery.
- Counting only successful tool calls (wrong target: the assertion measures the model, not the tool).

**Concrete incidents / author-verbatim phrases:**
- "The prompt needs to have a way to say that a tool has to be called" (2026-08-09-1058-promptforge-core-large-part4.md p265)
- "if it doesn't perform at least one web search, that's a problem" (purpose pass Record 3)
- "no to require_called, it violates the design principle of do more with less" (p267)
- "failed tool call counts as a call, we are measuring if the model is performing not if the tool is performing" (p271)

**Merge/derivation notes:**
- Grouped-draft record (line 474) from user-stated and user-corrective sources; the same discussion was captured twice (2026-08-09 part4 and 2026-08-14 part3, duplicate capture) and consolidated; endorsement: n/a.
- Purpose pass Record 3; merge suggestion: none.

## Principle 31: A tool can be plain Lua

**Rule:** A tool can be an inline Lua function, registered from any chunk in the section, effective for the next prose call, with its schema derived from the function declaration.

**Purpose facts:**
- Some tools are trivial - the author's example is setting a variable - and writing a Rust function for each is unjustified.
- A Lua tool has the same capabilities as a native Rust tool, including enabling further tools at call time (e.g. a search front end that does a tools.add for fetch when called); the author's own opt-in legitimizes this.
- The schema is derived from the function declaration because "we can't do no schema."
- A Lua tool handler cannot jump: a jump from inside a tool handler has no section walk to transfer into. Ordinary section Lua still can jump.

**Rejected alternatives and stated costs:**
- Requiring a Rust function for every tool (unjustified for trivial tools like setting a variable).
- Schema-less local tools presenting only name and description ("We can't, we can't do no schema. We have to pick the parameter types out of the function declaration").
- Allowing jump() from tool handlers (makes no sense - no section walk to transfer into).

**Concrete incidents / author-verbatim phrases:**
- "we don't wanna have to write a Rust function just for setting a variable... a front end to the real search tool... when the tool is called, it does a tools.add for fetch" (2026-08-09-1058-promptforge-core-large-part4.md p373)
- "the user is opting in to the behavior, so that makes it ok" (p374)
- "invocable from any lua chunk in an H2 and it should just add the tool for the next prose call" (2026-08-18-1126-promptforge-md-aug18-morning.md p144)
- "a Lua tool should have all the same capabilities as a regular tool, a native Rust tool" (p160)
- "Lua needs to jump local tool handlers cannot" (p162-163)

**Merge/derivation notes:**
- Grouped-draft record (line 481) from user-stated and user-corrective sources across 3 chat units; endorsement: n/a.
- Purpose pass Record 4; merge suggestion: none.

## Principle 32: The prompt owns model choice

**Rule:** Models are declared in the introduction with their attributes; a section selects its model exactly once in its first Lua block, inheriting the prompt-wide default or overriding it, and the choice locks for the rest of the section.

**Purpose facts:**
- The prompt owns model choice and execution parameters because the prompt is the thing that knows what it needs.
- Any inference before a selection is an error - a decision nobody made.
- Switching models means starting a new section and carrying context forward through reply, because switching mid-section can jump to a different provider and silently invalidate the KV cache, which is invisible to the programmer.
- A subsection inherits its parent section's model unless it specifies otherwise.
- Execution parameters (context size, thinking, resource caps) live in the prompt's Lua, never the frontmatter, the command line, or a gateway toggle.
- Analytical pipelines run at temperature zero.

**Rejected alternatives and stated costs:**
- Declaring model settings in the frontmatter ("the H1 lua needs controls to set the caps. it should not go in the frontmatter").
- models.only, an all-or-nothing lock - rejected because it "permanently foreclosed" per-section choice; a default plus per-section override is briefer when there are only one or two exceptions. Replaced with models.default.
- Non-inheriting model resolution.
- Frontmatter keys or command-line flags for context_max_tokens and no_think ("those should be properties of the prompt, not the command line").
- A gateway-level thinking toggle ("the prompt should control if thinking is on or off, not at the gateway").
- Nonzero temperature for analytical work ("temperature is supposed to be zero for analytical pipelines").

**Concrete incidents / author-verbatim phrases:**
- "The prompt has to specify what the minimum context size is" (purpose pass Record 5).
- "switching a model in the middle of a block has consequences for the KV cache... that's not visible to the programmer" (2026-08-18-1126-promptforge-md-aug18-morning.md p179)
- No model selected before first prose is an error (p66-67).
- "H3 should inherit the H2's model unless it specifies otherwise" (2026-08-09-1058-promptforge-core-large-part2.md p142)
- models.use only in the first Lua block, then locked (p175, p177).

**Merge/derivation notes:**
- Grouped-draft record (line 574) merged from user-stated, user-corrective, and ai-proposed (affirmed) sources across 5 chat units; endorsement: affirmed (ai-proposed leg).
- Purpose pass Record 5; merge suggestion: none. Adjacent to Record 6 (both about model binding) but kept separate: Record 5 is about who owns the choice and when it locks; Record 6 is about how loosely the name resolves. The design doc preserves that split as principles 32 and 33.

## Principle 33: Model binding is loose

**Rule:** Model binding is loose, much looser than tool binding, and resolves through the same semantic picker.

**Purpose facts:**
- A section's contract with the rest of the prompt is ordinary markdown, so which model slot executes it makes no difference to the section.
- This is what lets a pipeline hop between model tiers per step (map-reduce: the reduce section stays ordinary markdown; only its model slot changes).

**Rejected alternatives and stated costs:**
- Strict model-name binding that fails hard on mismatch - fails hard on catalog drift for no benefit.

**Concrete incidents / author-verbatim phrases:**
- The author hit a hard "model binding failed" error and rejected strict binding: "this makes no sense. the models need to be way looser than the tools. Shouldn't this use the tool-picker?" (2026-08-14-1613-promptforge-core-largest-part2.md p132-133)
- "The reduce section stays ordinary markdown; only its model slot and a staircase-streaming aggregator change" (2026-07-30-0654-map-reduce-synthesis.md design documents section)

**Merge/derivation notes:**
- Grouped-draft record (line 581) from user-corrective and ai-proposed sources across 2 chat units; endorsement: unaddressed (ai-proposed leg).
- Purpose pass Record 6; merge suggestion: none.

## Stanza facts

**What the section covers:** How a prompt gets its tools and its model: per-section opt-in tool scoping, a single loud tools.add entry point, epilogue assertions on tool usage, Lua-implemented tools, prompt-owned model selection with per-section locking, and loose model binding.

**Why the layer exists:** The offered surface is what a small model can navigate, and a wrong binding should explode at load time, not misbehave at run time.

**Failure modes it prevents:**
- Small-model confusion from oversized tool lists (context pressure).
- Silent tool-binding failures that are debugging traps.
- Runs that come back empty because a required tool was never called.
- Invisible KV-cache invalidation from mid-section model switches.
- Hard failures on model catalog drift for no benefit.

**Unifying principle (one sentence):** Declare everything, bind it early, fail loud.
