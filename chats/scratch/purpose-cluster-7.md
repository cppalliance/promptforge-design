# Purpose pass - Cluster 7 (Fanout)

## Record 1: "Fanout is always invoked explicitly through a fanout() call..."

**Purpose:** The author wants parallelism to be a deliberate act by the prompt author, never something the engine guesses from document shape - a bullet list sitting in a section must not silently trigger a fanout. The items fanned out over are often produced by the model at run time (a list section the model just wrote, or a Lua array built from tool results), because you do not know ahead of time what the arms need to work on; rigid statically fixed rules in Lua are useless when the hard part is the model's decision. Dispatching on the second parameter's type, with a loud error for anything else, keeps author mistakes visible instead of silently iterating something unintended.

**Citations used:**
- 2026-08-08-0029-promptforge-context-planning.md [p35] ("Make this a general principle of the design, always explicit"), [plans section: "Inferring fanout from bullets without an explicit fanout(...) call" listed as a non-goal; "This explicit fanout is in-contract; inferred fanout remains a non-goal"]
- 2026-08-19-0048-promptforge-md-aug19.md [p22], [p23], [p24] (collection as second parameter, list_from_section factored out, scoping to siblings and children)
- 2026-08-18-1126-promptforge-md-aug18-morning.md [p45] ("the most fundamental operation of FanOut... executing a set of operations in parallel... we have to allow that second parameter to be an array"), [p108], [p109]
- 2026-07-30-0534-promptforge-design-context.md [p50] ("You don't know ahead of time what you need to search for in the sub-agent... if you're calling it from the Lua and you just have some rigid rules... really the hard part is in the model")

## Record 2: "The subagent section is the arm template..."

**Purpose:** The author wants a fanout arm to be an ordinary section running through the same engine code path as normal flow, not a special execution mode - he called restricting fanout by child headings "try-hard" and "pointless," and asked "Why should arms be different?" when reviewing the plan to collapse the duplicated arm engine. Splitting the work between a pure-data list section (no Lua) and a template section (shared preamble, prose with the per-arm item, shared epilog) keeps the mechanism clean: one section supplies items, the other supplies everything else. Per-arm values arrive through a sealed sys and item rather than overloading the section identity variable, so the arm's environment differs from a normal section only by what the harness hands it.

**Citations used:**
- 2026-08-08-0029-promptforge-context-planning.md [p35] ("the H3 with the bullets can't have Lua. Instead, another H3 carries the Lua"), [p47] ("remember the preamble is shared. each subagent VM gets item and sys.taskid")
- 2026-08-19-0048-promptforge-md-aug19.md [p78] ("arms can jump"), [p79] ("and execute, fanout, list_from_section, etc there is no reason for special cases")
- 2026-08-19-0447-collapse-fanout-arm-review.md [p2] ("an arm must be treated the same way as normal flow, preferably with the same functions... Why should arms be different?")
- 2026-08-18-1126-promptforge-md-aug18-morning.md [p138] ("I dont see a point to restricting things like fanout() just beause a section has no child headings. this is try-hard. its pointless.")

## Record 3: "The invoking Lua owns the reduce step..."

**Purpose:** The author wants the reduce to be ordinary Lua written by the prompt author in the same chunk that called fanout ("my thinking is this, the invoking lua deals with the reduce step"), so joining results is deterministic code instead of paid inference - his recurring complaint is wasting model tokens on orchestration that Lua can do. Concurrency is throttled by the gateway's admission queue, so a total item cap is unnecessary; only concurrent fanout needs a limit. Spoke identity (taskid, unique file names) is assigned by the harness because the model should not spend inference calculating names, and ordered replies plus sequential-equivalent fail-fast keep parallel execution indistinguishable from sequential to the invoker.

**Citations used:**
- 2026-08-08-0029-promptforge-context-planning.md [p33] ("my thinking is this, the invoking lua deals with the reduce step")
- 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: Fanout and gateway concurrency - "core fires all arms at once, the gateway queue is the throttle; replies stay ordered by arm index; fail-fast aborts siblings... same invoker-visible behavior as sequential; the store stays shared and mutex-safe"]
- 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Fanout and gateway concurrency - same principles]
- 2026-08-19-0048-promptforge-md-aug19.md [p80] ("max_fanout_items there should be no limit on the total, just a limit on concurrent fanout")
- 2026-07-28-0925-orchestrator-design-document.md [p67] ("I don't want the model to have to calculate the final name, we want to minimize the amount of inference"), [p69] ("why should we waste inference having to figure that out?")

## Merge suggestions

- Records 1 and 2 share one root purpose: fanout is an explicit, author-invoked mechanism built out of ordinary sections, with no engine inference from document shape and no special-cased arm execution. They could merge into a single principle of the form "fanout is explicit and arms are ordinary sections."
- Record 3 stands apart: its purpose is about reduce semantics and concurrency (deterministic reduce in Lua, gateway-throttled concurrency, harness-assigned identity), not about how fanout is invoked or how arms execute. Keep it separate.
