# Packet Section 3 - Control Flow and Context (Principles 14-18)

Facts only. Sources: purpose-cluster-3.md (Records 1-6), grouped-draft.md "Control flow" YAML block.

## Principle 14: Every section transition clears context

**Rule:** Every section transition clears context; fall-through is the default and jump() is the explicit form.

**Purpose facts:**
- Lets the author write a simple linear pipeline with no explicit transitions: "you just fall off the end of your section and you go to the next one, and then you don't have to name the next section."
- A three-step prompt that processes a file needs no explicit transitions; running off the last section ends the run with a well-defined message (default completion message, overridable in YAML front matter).
- Context-clearing exists because accumulated context is the enemy: "I do NOT want sequential fall-through to accumulate context." Clearing on every transition keeps contexts small so smaller, cheaper models stay reliable.
- Fall-through lives in the executor, not Lua: "the default control flow, falling through, doesn't happen in Lua and making it happen there would be clumsy."
- jump() throws out the current context and starts fresh from the target section, which "eliminates context bloat" and lets each step run in a small window.
- The value carried across a jump must be visible in the prompt source: "we said we're gonna make it visible so that if you can actually read the code."
- The model's previous reply always rides along in the single variable `reply`; the invariant is "when you enter a section, the model's previous reply is always in the reply variable."
- jump carries only the passed string, the params, and store access.
- Renamed from goto to jump because goto is a reserved word in Lua.
- Without it: context that accumulates across sections bloats the window; accumulation is what forces big models and compaction.

**Rejected alternatives and stated costs:**
- Requiring an explicit exit or transition from every section.
- Implementing fall-through inside the Lua block - rejected as "clumsy."
- Fall-through that appends each section into a growing shared context - rejected because accumulation bloats the window and forces big models and compaction.
- Compacting the transcript to make room in a continuing context (for jump).
- jump() dropping the reply.
- Three separate variables incoming_reply, reply, and last_reply - rejected in favor of the single variable reply.
- Endorsement: n/a (both constituent records).

**Concrete incidents:**
- The author hit the case where Lua wanted to jump based on an inference result and had no way to pass that reply along; this broke his invariant that the model's previous reply is always in `reply` on section entry. This incident also appears under principle 2 as the motivating case for uniform constraints.

**Merge/derivation notes:**
- Merged from purpose-cluster-3 Record 1 (fall-through, default advance, termination) and Record 2 (jump, explicit transfer, reply rule). Both records state the same root rule: every section transition starts a fresh context, because accumulation is what forces big models and compaction. Record 1 is the default form; Record 2 is the explicit form.
- Record 1 citations: 2026-07-28-2238-orchestrator-design-continued.md [p75], [p121]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p75], [p121]; 2026-08-02-1134-mcp-client-large-part5.md [p363], [p414], [p415]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10].
- Record 2 citations: 2026-07-28-0925-orchestrator-design-document.md [p14], [p74], [p75]; 2026-07-28-2238-orchestrator-design-continued.md [p14], [p75], [p120]; 2026-07-30-0534-promptforge-design-context.md [p12]-[p18]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20], [p21], [p22]; 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481].

## Principle 15: execute() runs a section as a subroutine; jump() transfers without returning

**Rule:** execute() runs a section as a subroutine - a fresh VM, the chain runs to its end, and the reply comes back to the caller - while jump() transfers control with no return.

**Purpose facts:**
- Lets the author reuse a section from more than one call site; a goto-with-return cannot be reused: "'return goto(...)' can't be a reusable function called from more than one place, because control always transfers to the same place after the Research is done."
- Lets one section get two tool loops: a section can only have one tool loop (its last prose block), so "if we really want two loops in one section, we can have the Lua... execute, and it can mention two different H2s... that's like a subroutine."
- Reuses the existing section-execution code deliberately: "We already have to execute sections, so why not make it a function that Lua can call?"
- Refined so execute starts a new chain that runs to its end and returns its reply, recursively: "it's like calling a different prompt whose pieces just happen to be in the same file."
- Return versus transfer is the author's choice; one section-execution machinery serves both.

**Rejected alternatives and stated costs:**
- An asymmetric model where an execute-entered subroutine may not jump.
- Treating goto-with-return as a reusable multi-call-site function - rejected because control would always return to the same place, so it cannot be reused.
- Endorsement: n/a.

**Concrete incidents:**
- The two stated gaps are themselves the incidents: the unreusable return-goto, and the one-tool-loop-per-section limit forcing the subroutine form.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 3); no merge. Distinct purpose from jump: subroutine with return vs transfer without return.
- Citations: 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]; 2026-08-09-1058-promptforge-core-large-part5.md [p430], [p432], [p433]; 2026-08-19-0048-promptforge-md-aug19.md [p55], [p58], [p60]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p242].

## Principle 16: A section ends when the model replies with text and no tool calls

**Rule:** A section ends when the model replies with text and no tool calls; tool calls made during the loop count as output; an empty final turn is a clean exit only when finish_reason is "stop" and a tool call succeeded earlier in the loop, and every other empty turn fails closed as EmptyModelReply.

**Purpose facts:**
- Token economy: a model that finished its work through tool calls should not have to "waste output tokens with the word 'done'"; tool calls already count as output.
- The empty-turn clean exit binds reply to the empty string.
- Every other empty turn fails closed, because silently accepting empty turns is how a run passes while producing nothing.

**Rejected alternatives and stated costs:**
- An explicit termination call required to end a section.
- Requiring a non-empty text reply to validate a turn.
- Accepting any empty turn once a tool call has occurred - rejected because silently accepting empties is how runs pass while producing nothing.
- Endorsement: affirmed.

**Concrete incidents:**
- A real papergate run failed: the prompt said "Do not output any text," the model recorded everything via tool calls and legally exited with empty content, and the engine hard-failed it as EmptyModelReply.
- The briefer's empty evidence.md: a run passed while producing nothing, the failure mode the fail-closed rule exists to prevent.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 4); no merge. Source tagged ai-proposed; user-stated.
- Open question 6 in the principles file notes the tension: "An empty model response is never acceptable" versus the conditional empty-turn clean exit; the later rule refines the earlier one, but the exact boundary of which empty turns fail closed deserves confirmation.
- Citations: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p3], [p6], [plans section]; 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions]; 2026-08-09-1058-promptforge-core-large-part5.md [p429]; grouped-draft also lists 2026-08-03-1827-two-repo-commit-review.md [design documents section].

## Principle 17: Cycles are allowed

**Rule:** Cyclic section calls are permitted; runaway execution is bounded by budgets (nesting limit, step budget, tool budget), not by structural prohibition.

**Purpose facts:**
- Some tools require cycles: "There are obviously tools which require cycles."
- The engine cannot predict how authors will organize their files: "we can't predict all the organizations, and we know that we can have cycles."
- Runaway execution is a resource problem, not a structure problem, so it is bounded by "nesting limit, step budget, tool budget" instead of prohibition.
- Once the language has subroutines, jump, and goto, "the same problems of any other computer programming language apply... with that power comes the responsibility" - coherence belongs to the prompt author, not the engine.

**Rejected alternatives and stated costs:**
- Restricting calls to an acyclic graph (the proposed restriction was: H3 can only call H3 and down, acyclic call graph) - rejected because some tools require cycles.
- Engine-enforced guardrails on control flow.
- Endorsement: n/a.

**Concrete incidents:**
- No specific debugging incident recorded; the rejected acyclic-graph proposal is the originating event.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 5); no merge. Source tagged user-corrective; user-stated.
- Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [p369]-[p372]; 2026-08-02-1134-mcp-client-large-part5.md [p369], [p371], [p372]; 2026-08-19-0048-promptforge-md-aug19.md [p60]; 2026-07-28-0925-orchestrator-design-document.md [p18]; 2026-07-30-0534-promptforge-design-context.md [p4].

## Principle 18: A task is either synchronous or asynchronous

**Rule:** A synchronous task is a function call with a context reset; an asynchronous task returns a unique timestamped id immediately, needs a rendezvous to collect, can be cancelled by the model when stuck, and is cancelled with a message if its section moves on; a fork lets the caller fall through while the task runs, and forks are not required to rejoin.

**Purpose facts:**
- The driving case was a long-running research task: "this is how you have a 'research task' going nonstop, while the main context is getting bugfixes and speedups."
- The unique timestamped ID returned at launch exists for one reason: "we have to give the harness the ability to cancel... we need to let the model cancel the task, like, if it's stuck."
- Cancellation on section exit exists because the author asked what happens "if the main section tries to move on or tries to return" with a pending task - the pending task must be cancelled and the section told.
- Forks are not required to rejoin because the author could "see forking a section that calls itself over and over again until some condition is met... and then it never comes back."

**Rejected alternatives and stated costs:**
- Requiring forks to always come together.
- Endorsement: n/a.

**Concrete incidents:**
- The research-task-running-nonstop scenario is the case that forced the design; no separate debugging incident recorded.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 6); no merge.
- Citations: 2026-07-30-0534-promptforge-design-context.md [p22], [p23], [p25], [p26], [p27], [p28], [p34], [p35]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]; 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247].

## Stanza facts (Section III header)

- What the section covers: how execution moves between sections and what happens to the context when it does.
- Why the layer exists: accumulated context is the enemy; small contexts are what let small, cheap models stay reliable.
- Failure modes it prevents: context bloat across sections (which forces big models and compaction); unreusable control transfer; wasted tokens on filler text like "done"; runs that pass while producing nothing (empty evidence.md); runaway execution treated as a structure problem instead of a resource problem; async tasks left dangling when a section moves on.
- Unifying principle, one sentence: every transition starts fresh, and anything that crosses does so visibly.
