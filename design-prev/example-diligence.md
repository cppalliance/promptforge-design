<!--
Simplified Diligence, written in PromptForge, as a teaching example.
Not the real 30-test tool. Every idiom of the language appears at least once,
labelled in an HTML comment so you can find it. Reading this top to bottom
should teach the whole language.

Idiom index:
  - frontmatter: name/description/version/args/tools/default_return
  - {{ args.x }} substitution in prose
  - ## Main entry point
  - fall-through between H2 sections (no explicit exit)
  - Lua block: model(), tools.add()
  - virtual files: create_file / append_file / read_file
  - counters: increment / get_count
  - state collection: add_breadcrumb (declared as a tool, filed by the model)
  - store queries in Lua: store.count, store.filter, store.group_by
  - fan-out over ### children: sections.children + call("fanout", ...)
  - subagent dispatch: call("task", "## Section", {...})
  - the return fence: call("return", ...) ends the run
  - task-target sections sit BELOW the fence, unreachable by fall-through
  - preconditions: top-level assert
  - postconditions: function check()
  - json.encode for a structured return value
-->

---
name: diligence
description: Assess whether a firm should be hired for an engagement. Returns a verdict.
version: 1
args:
  type: object
  properties:
    firm: { type: string }
    engagement: { type: string }
  required: [firm]
tools:
  - web_search        # canonical, bound to a search extension
  - web_fetch         # canonical
  - create_file       # core, virtual filesystem
  - append_file       # core
  - read_file         # core
  - increment         # core, counter bag
  - get_count         # core
  - add_breadcrumb    # state collection, declared by this prompt
default_return: "Diligence complete. See the report file."
---

## Main

<!-- idiom: ## Main is the entry point. args are global and read-only. -->
<!-- idiom: a section can be pure orchestration. This Lua block fans out the
     three research passes and does no model work itself. The fanout blocks
     until all three subagents finish, each writing its own file. -->

```lua
-- idiom: call("fanout", ...) over named task-target sections (below the fence).
-- Each runs in a fresh context on the fast tier and writes one research file.
call("fanout", {
  { section = "## Company" },
  { section = "## Leadership" },
  { section = "## Reputation" },
})
```

<!-- idiom: {{ args.firm }} is substituted by the runtime before the model sees it. -->

Research on **{{ args.firm }}** for the engagement "{{ args.engagement }}" is
complete: `company.md`, `leadership.md`, and `reputation.md` now exist. This
section only dispatched that work; fall through to the industry synthesis.

<!-- idiom: no call() at top level, so the section FALLS THROUGH to the next H2,
     ## Industry. Context is cleared on the way. ## Industry cannot see this
     section's turns; it reads the files. -->

## Industry

```lua
model("fast")                          -- cheaper model, mechanical synthesis
tools.add("web_search", "read_file", "create_file")

-- idiom: precondition. Runs before the model. If it fails, the section is
-- skipped (and fall-through still happens). Here it guards against an empty gather.
assert(#read_file("company.md") > 0, "company.md is empty")
```

Read `company.md`, `leadership.md`, and `reputation.md`. Identify the firm's
industry, its five closest competitors, and the pricing and engagement norms of
this market. Write it all to `industry.md`, then stop.

## Diagnose

<!-- idiom: fan-out over ### children. Each ### under ## Test Battery becomes a
     parallel subagent with its own fresh context, running on a small model.
     Each files breadcrumbs into the shared state collection. -->

```lua
model("fast")
tools.add("read_file")                 -- the parent only needs to read evidence

-- idiom: sections.children returns the H3 sections under a heading.
local tests = sections.children("## Test Battery")

-- idiom: call("fanout", ...) dispatches them all concurrently and waits.
-- ordered=true is irrelevant here because each test files into the store by id.
call("fanout", tests, { firm = args.firm })
```

Every test in the battery has now run and filed its breadcrumbs. Nothing else to
do here; fall through to the challenge.

## Challenge

<!-- idiom: store queries in Lua. The breadcrumbs are a real collection, filtered
     by field. This is the operation files cannot do reliably at 30+ records. -->

```lua
model("driver")
tools.add("read_file")                 -- reads breadcrumbs via context.inject below

-- pull every breadcrumb the battery filed, inject them for the model to judge
context.inject(json.encode(store.get_all("breadcrumbs")))
```

Cross-examine each breadcrumb against the five appeal grounds: already handled,
not claimed, historical counter-example, survivorship bias, insufficient
evidence. For each one that fails, call add_breadcrumb again with the same id and
`status = "killed"` and a one-line reason. Leave survivors untouched. When every
breadcrumb has a status, stop.

```lua
-- idiom: postcondition. Runs when the section ends. Fails -> the section retries.
-- store.count with a filter is the structured query that justifies the store.
function check()
  local total = store.count("breadcrumbs")
  local judged = store.count("breadcrumbs", { has = "status" })
  assert(judged == total, "judged " .. judged .. " of " .. total)
  -- idiom: counter for the audit trail
  increment("findings_killed", store.count("breadcrumbs", { status = "killed" }))
end
```

## Couple

<!-- idiom: store.group_by on the cluster field. This is the group-by that files
     cannot do reliably: 20+ surviving breadcrumbs bucketed into six clusters. -->

```lua
model("driver")
tools.add("create_file")

-- only surviving breadcrumbs, grouped by cluster, injected as JSON
local surviving = store.filter("breadcrumbs", { status = nil })   -- no kill status
context.inject(json.encode(store.group_by(surviving, "cluster")))
```

For each cluster holding two or more surviving breadcrumbs, name the compound
dynamic: how one finding amplifies or enables another. Write the coupling map to
`coupling.md`, one named compound per block, then stop.

## Synthesize

```lua
model("driver")
tools.add("read_file", "create_file")
```

Read `coupling.md`, `industry.md`, and the surviving breadcrumbs. Decide the
verdict: hire, hire_with_conditions, or avoid. Write the full report to
`report.md` following the firm's evidence, and set the verdict in one line at the
top. Then stop.

## Report

<!-- idiom: the return fence. call("return", ...) ends the run and hands one
     string to the caller. Everything below this section in file order is
     unreachable by fall-through. -->

```lua
model("fast")
tools.add("read_file")

function check()
  assert(#read_file("report.md") > 0, "no report written")
end
```

Read `report.md`. Extract the verdict line. Then return a structured summary.

```lua
-- idiom: json.encode assembles a structured return from validated state.
-- The model never produced this JSON; the store did, one breadcrumb at a time.
call("return", json.encode({
  firm       = args.firm,
  verdict    = store.get("verdict"),
  findings   = store.count("breadcrumbs", { status = nil }),
  killed     = get_count("findings_killed"),
  report     = "report.md"
}))
```

<!-- ============================================================
     BELOW THE FENCE: task targets. Reachable only by call("task"/"fanout").
     Never reached by fall-through, because ## Report returned above.
     ============================================================ -->

## Test Battery

<!-- idiom: ### children are individually addressable and fannable-out.
     Each is a tiny focused task: read the evidence, apply ONE test, file a
     breadcrumb if it fires. A 14B handles one test in isolation easily.
     add_breadcrumb is the state collection tool declared in frontmatter. -->

### Credential Depth

```lua
model("fast")
tools.add("read_file", "add_breadcrumb")
```

Read `leadership.md`. Are the firm's credentials substantive or purchasable
(pay-to-play awards, revenue-tier partnerships)? If purchasable, call
add_breadcrumb with cluster="capability", a one-sentence finding, and the gap
"cannot tell if the client can distinguish real credentials." Otherwise file
nothing.

### Staffing Model

```lua
model("fast")
tools.add("read_file", "add_breadcrumb")
```

Read `company.md` and `reputation.md`. Do the senior people who sell the work
also deliver it, or is there a bait-and-switch to juniors? If bait-and-switch,
call add_breadcrumb with cluster="delivery", the finding, and the gap. Otherwise
file nothing.

### Financial Viability

```lua
model("fast")
tools.add("read_file", "add_breadcrumb")
```

Read `company.md`. Can the firm survive a slow quarter, or are there layoffs,
office closures, or single-client dependence? If fragile, call add_breadcrumb
with cluster="reputation", the finding, and the gap. Otherwise file nothing.

## Company

<!-- idiom: a task target dispatched by ## Main's fanout. Fresh context, fast
     tier, writes one file. Reached only by call("fanout"/"task"), never by
     fall-through, because ## Report returned above the fence. -->

```lua
model("fast")
tools.add("web_search", "web_fetch", "create_file")
```

Research {{ args.firm }}: founding, size, revenue signals, named clients,
headcount trend, financial signals. Write it to `company.md`, then stop.

## Leadership

```lua
model("fast")
tools.add("web_search", "web_fetch", "create_file")
```

Research the leaders and senior delivery staff at {{ args.firm }}: backgrounds,
prior firms, publications, and any credentials that look inflated relative to
verifiable output. Write it to `leadership.md`, then stop.

## Reputation

```lua
model("fast")
tools.add("web_search", "web_fetch", "create_file")
```

Research the reputation record of {{ args.firm }}: employee sentiment, client
reviews versus self-published case studies, litigation, and controversies. Weight
specific structural complaints over vague ones. Write it to `reputation.md`, then
stop.
