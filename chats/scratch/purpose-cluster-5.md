# Purpose pass - Cluster 5: Tools and models

## Record 1: "Per-section tool scoping is opt-in..."

Purpose: Small orchestrator models get confused when the offered tool list is large, so each section should advertise only the handful of tools it actually needs - the author set a budget of roughly five to seven tools for 7B-14B models. Scoping is opt-in (a section gets only what it names) so that a section can never hold a tool it did not ask for, and a 20-tool prompt no longer injects 20 schemas into every section. History is never scrubbed of tool offerings because the model would see information appearing out of nowhere, and constraining the toolset must not otherwise change the section's behavior.

Citations used: 2026-07-28-2238-orchestrator-design-continued.md [p17] ("keeps the tool list small so the model doesn't get confused"), [p85] ("each subhead only needs a few of them"), [p119] (tool count 5-7 for small orchestrator models); 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: per-section tool scoping] (opt-in chosen "for isolation - a section can never hold a tool it did not ask for"); 2026-08-02-1134-mcp-client-large-part5.md [plans: per-section tool scoping] (same decision, hard error on unknown names); 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p61] (scrubbing history: "the model would see information appearing out of nowhere"), [p63] (search/fetch turn-scoped availability), [p64] ("I want the behavior to be the same as the traditional way, except that the toolset is constrained"); 2026-07-30-1046-compaction-algorithm-large-part3.md [p163], [p164], [p222] (fewer tools in context; no control-flow tool for fall-through sections; restricting call kinds "reduces pressure because the model doesnt have to pick"); 2026-08-09-1058-promptforge-core-large-part4.md [p372] (only web_search on the first turn, "this locks the model to calling just one tool").

Merge suggestion: adjacent to Record 2 (both govern tools.add), but the purposes differ - this one is small-model context pressure and isolation, Record 2 is loud failure and a single entry point. Keep separate.

## Record 2: "There is exactly one tools.add entry point..."

Purpose: The author hit tool-binding failures that did not fail hard and found them confusing to debug, so unknown or unscoped tool names must be hard errors with clear diagnostics instead of being silently dropped. His gut rule was that there should be only one version of tools.add - no overloaded variants - consistent with the "do more with less" principle. Call budgets live at the tools.add call site and turn limits belong to the subagent (config.max_turns), because a limit is a property of the agent, not of any single tool; when the budget is exhausted all of the subagent's tools are removed.

Citations used: 2026-08-14-1613-promptforge-core-largest-part2.md [p89] (a tools.add failure case that "is not failing hard"), [p90] ("my gut tells me there should only be one version of tools.add"), [p170] ("we need to bake the limit into the tools.add call"), [p175] ("max_turns is not really on the tools its on the subagent itself"), [p176] ("this means we take ALL the tools away on exhaustion"); 2026-08-09-1058-promptforge-core-large-part4.md [p271] ("unknown aliases are hard errors with clear diagnostics"), [p272] ("'registered' is wrong - it has to be scoped"), [p273] ("naming an unscoped yet global tool should hard-error").

Merge suggestion: none. See Record 1 note.

## Record 3: "A prompt can assert postconditions on tool usage in its epilogue..."

Purpose: The author had runs where the model never performed a required web search and the output came back empty or wrong, so the prompt needs a way to require that a tool was actually called - "if it doesn't perform at least one web search, that's a problem." A dedicated require_called directive was rejected because it violates "do more with less"; an ordinary Lua assert over a call count says the same thing with existing machinery. A failed tool call still counts because the assertion measures whether the model is performing, not whether the tool is performing.

Citations used: 2026-08-09-1058-promptforge-core-large-part4.md [p265] ("The prompt needs to have a way to say that a tool has to be called"), [p266] (the assert syntax), [p267] ("no to require_called, it violates the design principle of do more with less"), [p268] ("that count would be per-vm"), [p271] ("failed tool call counts as a call, we are measuring if the model is performing not if the tool is performing"); 2026-08-14-1613-promptforge-core-largest-part3.md [p265]-[p271] (same discussion, duplicate capture).

Merge suggestion: none.

## Record 4: "A tool can be implemented as an inline Lua function..."

Purpose: Some tools are trivial - the author's example is setting a variable - and writing a Rust function for each one is unjustified, so a Lua function can stand in as the tool. A Lua tool can also act as a front end to a real tool, e.g. a search tool that adds fetch when called, and the author's own opt-in is what legitimizes a tool enabling further tools at call time. The schema is derived from the function declaration because "we can't do no schema," and Lua handlers cannot jump because a jump from inside a tool handler makes no sense - ordinary section Lua still can.

Citations used: 2026-08-09-1058-promptforge-core-large-part4.md [p373] ("we don't wanna have to write a Rust function just for setting a variable... a front end to the real search tool... when the tool is called, it does a tools.add for fetch"), [p374] ("the user is opting in to the behavior, so that makes it ok"); 2026-08-18-1126-promptforge-md-aug18-morning.md [p99] (plan the Lua-backed tool feature), [p117] ("We can't, we can't do no schema. We have to pick the parameter types out of the function declaration"), [p144] ("invocable from any lua chunk in an H2 and it should just add the tool for the next prose call"), [p160] ("a Lua tool should have all the same capabilities as a regular tool, a native Rust tool"), [p162], [p163] ("Lua needs to jump local tool handlers cannot").

Merge suggestion: none.

## Record 5: "Models are declared in the prompt's introduction via models.add..."

Purpose: Model choice and execution parameters belong to the prompt because the prompt is the thing that knows what it needs - the author objected to thinking toggles at the gateway, to model settings in the frontmatter, and to context_max_tokens and no_think on the command line: "The prompt has to specify what the minimum context size is." Analytical pipelines run at temperature zero. The model locks per section because switching models mid-section can jump to a different provider and silently invalidate the KV cache, which is invisible to the programmer - to switch models you start a new H2 and carry context forward through reply. models.only was rejected because an all-or-nothing lock forecloses per-section overrides; a default plus per-section override is briefer when there are only one or two exceptions.

Citations used: 2026-08-09-1058-promptforge-core-large-part2.md [p105] ("temperature is supposed to be zero for analytical pipelines"), [p107] ("the prompt should control if thinking is on or off, not at the gateway"), [p108]-[p112] (models.add in the introduction, model("fast") in the H2), [p142] ("H3 should inherit the H2's model unless it specifies otherwise"); 2026-08-14-1613-promptforge-core-largest-part2.md [p154] ("the H1 lua needs controls to set the caps. it should not go in the frontmatter"), [p205] ("Context_max_tokens and no_think, those should be properties of the prompt, not the command line"); 2026-08-08-0029-promptforge-context-planning.md [p80]-[p83], [plans: models.always] (prompt-wide default binding); 2026-08-18-1126-promptforge-md-aug18-morning.md [p66]-[p67] (models.always "permanently foreclosed" per-section choice; no model selected before first prose is an error), [p168] (replace models.only with models.default), [p175], [p177] (models.use only in the first Lua block, then locked), [p179] ("switching a model in the middle of a block has consequences for the KV cache... that's not visible to the programmer").

Merge suggestion: none. Adjacent to Record 6 (both about model binding), but this record is about who owns the choice and when it locks; Record 6 is about how loosely the name resolves.

## Record 6: "Model binding is much looser than tool binding..."

Purpose: The author hit a hard "model binding failed" error and rejected strict binding: "the models need to be way looser than the tools" and should resolve through the same semantic picker used for tools. A section's contract with the rest of the prompt is ordinary markdown, so which model slot executes the section makes no difference to the section - the map-reduce design note puts it as "the reduce section stays ordinary markdown; only its model slot changes," which is what lets a pipeline hop between model tiers per step.

Citations used: 2026-08-14-1613-promptforge-core-largest-part2.md [p132] ("model binding failed"), [p133] ("this makes no sense. the models need to be way looser than the tools. Shouldn't this use the tool-picker?"); 2026-07-30-0654-map-reduce-synthesis.md [design documents section] ("The reduce section stays ordinary markdown; only its model slot and a staircase-streaming aggregator change"; tiered model slots per section).

Merge suggestion: none.
