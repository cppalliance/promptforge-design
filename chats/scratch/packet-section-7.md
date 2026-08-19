# Packet Section VII - Fanout (Principles 38-39)

Facts only. No prose.

## Principle 38: Fanout is always explicit; an arm is an ordinary section

**Rule:** Fanout is always explicit - a `fanout()` call, never the engine inferring parallelism from a bullet list - and an arm is an ordinary section running through the same code path as normal flow.

**Purpose facts:**
- Parallelism is a deliberate act by the prompt author; a bullet list sitting in a section must never silently trigger a fanout.
- The items fanned over usually come from the model at run time: a list section the model just wrote, or a Lua array built from tool results. You do not know ahead of time what the arms need to work on, so rigid statically fixed rules in Lua are useless - the hard part is the model's decision.
- `fanout()`'s second parameter dispatches on type: a string names a list section, an array table is the collection, anything else is a loud Lua error. Loud errors keep author mistakes visible instead of silently iterating something unintended.
- `list_from_section(name)`/`items()` returns a section's parsed bullet items as an array of strings; it can access only sibling sections at the same nesting level and child sections.
- An arm runs through the same engine code path and the same functions as normal flow; it can jump, execute, fanout, and list_from_section like any section. It differs only in what the harness hands it: its item and its task id.
- Work splits between a pure-data list section (no Lua) and a template section (shared leading-Lua preamble, prose with the per-arm item, shared trailing-Lua epilog): one section supplies items, the other supplies everything else.
- Each arm runs in a fresh VM built from the shared template; per-arm values (item text, task id) arrive through a sealed `sys`, not by overloading the section identity variable.
- Fanout is allowed whether or not a section has child headings.

**Rejected alternatives and stated costs:**
- Inferring fanout from bullets without an explicit call - listed as a non-goal in the plan; "This explicit fanout is in-contract; inferred fanout remains a non-goal."
- Silently iterating a hash-keyed table in unstable order - mistakes become invisible.
- Rigid, statically fixed fan-out rules in Lua - useless when the hard part is the model's run-time decision about what to work on.
- Colocating the arm's Lua with the bullet list - rejected in favor of the list-section/template-section split ("the H3 with the bullets can't have Lua. Instead, another H3 carries the Lua").
- Overloading the section identity variable with per-arm data - rejected in favor of sealed `sys` with item and taskid.
- Stubbed control globals in arms - rejected; arms get the real functions.
- A separate arm-execution path with its own functions - two engines to keep honest.
- Restricting fanout() to sections with child headings - a special case with no reason.

**Concrete incidents / author-verbatim phrases:**
- Reviewing the plan to collapse the duplicated arm engine: "an arm must be treated the same way as normal flow, preferably with the same functions... Why should arms be different?" (2026-08-19-0447-collapse-fanout-arm-review.md [p2])
- On the child-heading restriction: "I dont see a point to restricting things like fanout() just beause a section has no child headings. this is try-hard. its pointless." (2026-08-18-1126-promptforge-md-aug18-morning.md [p138])
- On arm capabilities: "arms can jump" ... "and execute, fanout, list_from_section, etc there is no reason for special cases" (2026-08-19-0048-promptforge-md-aug19.md [p78], [p79])
- On run-time item sources: "You don't know ahead of time what you need to search for in the sub-agent... if you're calling it from the Lua and you just have some rigid rules... really the hard part is in the model" (2026-07-30-0534-promptforge-design-context.md [p50])
- "Make this a general principle of the design, always explicit" (2026-08-08-0029-promptforge-context-planning.md [p35])
- "the most fundamental operation of FanOut... executing a set of operations in parallel... we have to allow that second parameter to be an array" (2026-08-18-1126-promptforge-md-aug18-morning.md [p45])
- "remember the preamble is shared. each subagent VM gets item and sys.taskid" (2026-08-08-0029-promptforge-context-planning.md [p47])

**Merge/derivation notes:**
- Merged from grouped-draft Fanout records 1 ("Fanout is always invoked explicitly through a fanout() call...", endorsement: affirmed (ai-proposed legs); source: ai-proposed (affirmed); user-stated) and 2 ("The subagent section is the arm template...", endorsement: n/a; source: user-stated; user-corrective).
- Purpose-pass merge suggestion: records 1 and 2 share one root purpose - fanout is an explicit, author-invoked mechanism built out of ordinary sections, with no engine inference from document shape and no special-cased arm execution.

## Principle 39: The invoking Lua owns the reduce

**Rule:** The invoking Lua owns the reduce - `fanout()` blocks and returns each arm's reply in arm order, the first arm error aborts its siblings with sequential fail-fast behavior, and only concurrent fanout is limited, never the total item count.

**Purpose facts:**
- The reduce is ordinary Lua written by the prompt author in the same chunk that called `fanout()`, so joining results is deterministic code instead of paid inference. Recurring author complaint: wasting model tokens on orchestration that Lua can do.
- `fanout()` is a blocking call returning each arm's final reply ordered by arm index.
- The first arm error aborts its siblings with the same invoker-visible behavior as sequential fail-fast - parallel execution stays indistinguishable from sequential to the invoker.
- The store stays shared and mutex-safe; authors must not assume arm N sees arm N-1 writes; store writes from arm epilogs stay visible to the reducer.
- Concurrency is throttled by the gateway's admission queue (core fires all arms at once, the gateway queue is the throttle), so a total item cap is unnecessary; only concurrent fanout needs a limit.
- Spoke identity (taskid, unique file names) is assigned by the harness because the model should not spend inference calculating names.

**Rejected alternatives and stated costs:**
- A total item cap (`max_fanout_items`) - forbids shapes of work for no resource reason; the gateway queue already throttles.
- The model computing each spoke's unique name or index - wastes inference on naming.
- A wait-for-all barrier before the reduce step runs - rejected in favor of fail-fast sibling abort.

**Concrete incidents / author-verbatim phrases:**
- "my thinking is this, the invoking lua deals with the reduce step" (2026-08-08-0029-promptforge-context-planning.md [p33])
- "max_fanout_items there should be no limit on the total, just a limit on concurrent fanout" (2026-08-19-0048-promptforge-md-aug19.md [p80])
- "I don't want the model to have to calculate the final name, we want to minimize the amount of inference" (2026-07-28-0925-orchestrator-design-document.md [p67])
- "why should we waste inference having to figure that out?" (2026-07-28-0925-orchestrator-design-document.md [p69])
- Plan language, repeated across two core plans: "core fires all arms at once, the gateway queue is the throttle; replies stay ordered by arm index; fail-fast aborts siblings... same invoker-visible behavior as sequential; the store stays shared and mutex-safe" (2026-08-14-1613-promptforge-core-largest-part5.md and 2026-08-09-1058-promptforge-core-large-part5.md, plans sections)

**Merge/derivation notes:**
- Derives from grouped-draft Fanout record 3 ("The invoking Lua owns the reduce step...", endorsement: unaddressed (ai-proposed legs); source: user-stated; user-corrective; ai-proposed).
- Purpose pass: record 3 stands apart from records 1-2 - its purpose is reduce semantics and concurrency (deterministic reduce in Lua, gateway-throttled concurrency, harness-assigned identity), not how fanout is invoked or how arms execute. Kept separate per the merge suggestion.

## Stanza facts (Section VII)

- Covers: parallel execution - how fanout is invoked (explicit `fanout()` call, type-dispatched second parameter), what an arm is (an ordinary section, same code path, fresh VM, sealed sys), and how results come back (blocking call, ordered replies, fail-fast abort, Lua-owned reduce, gateway-throttled concurrency, harness-assigned spoke identity).
- Failure modes prevented: engine silently inferring parallelism from document shape; silent iteration of unintended collections; a second arm-execution engine drifting out of honesty with the main engine; special-cased arm capabilities; paying model inference for orchestration (reduce, naming) that deterministic code can do; total item caps forbidding valid work shapes; parallel runs behaving observably differently from sequential runs.
- Unifying principle (one sentence): Parallelism is explicit, and an arm is just a section.
