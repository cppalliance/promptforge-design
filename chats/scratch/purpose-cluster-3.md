# Purpose pass - Cluster 3 (Control flow)

## Record 1: "Falling through to the next section is the default control flow and is context-clearing..."

**Purpose:** The author was designing for simple linear pipelines: "you just fall off the end of your section and you go to the next one, and then you don't have to name the next section." A three-step prompt that processes a file should need no explicit transitions, and running off the last section must still end the run with a well-defined message. The context-clearing half exists because accumulated context is the enemy: "I do NOT want sequential fall-through to accumulate context" - clearing on every transition keeps contexts small so smaller, cheaper models stay reliable. Fall-through lives in the executor, not Lua, because "the default control flow, falling through, doesn't happen in Lua and making it happen there would be clumsy."

**Citations used:** 2026-07-28-2238-orchestrator-design-continued.md [p75], [p121]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p75], [p121]; 2026-08-02-1134-mcp-client-large-part5.md [p363], [p414], [p415]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10]

**Merge:** Shares its context-clearing motivation with Record 2 (jump). The mechanisms differ (default advance vs explicit transfer) but both exist to keep context from accumulating. See merge note on Record 2.

## Record 2: "jump() (formerly goto) destroys the current context..."

**Purpose:** Same root as Record 1: a transition throws out the current context and starts fresh from the target section, which "eliminates context bloat" and lets each step run in a small window. On top of that, the value carried across the transfer must be visible in the prompt source ("we said we're gonna make it visible so that if you can actually read the code"), and the model's previous reply must always ride along in `reply` - the author hit the case where Lua wanted to jump based on an inference result and had no way to pass that reply along, which broke his invariant that "when you enter a section, the model's previous reply is always in the reply variable." Renamed from goto to jump because goto is a reserved word in Lua.

**Citations used:** 2026-07-28-0925-orchestrator-design-document.md [p14], [p74], [p75]; 2026-07-28-2238-orchestrator-design-continued.md [p14], [p75], [p120]; 2026-07-30-0534-promptforge-design-context.md [p12]-[p18]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20], [p21], [p22]; 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481]

**Merge:** Candidate merge with Record 1. Both say: every section transition starts a fresh context, because accumulation is what forces big models and compaction. Record 1 adds the default-and-termination rules; Record 2 adds the explicit-value and reply rules. If the principle is stated as "transitions clear context," these two records are its default and explicit forms.

## Record 3: "execute() runs a referenced section as a subroutine in a fresh VM..."

**Purpose:** Two concrete gaps drove it. First, goto-with-return cannot be reused: "'return goto(...)' can't be a reusable function called from more than one place, because control always transfers to the same place after the Research is done." Second, a section can only have one tool loop (its last prose block), so "if we really want two loops in one section, we can have the Lua... execute, and it can mention two different H2s... that's like a subroutine." It reuses the existing section-execution code deliberately: "We already have to execute sections, so why not make it a function that Lua can call?" Later refined so execute starts a new chain that runs to its end and returns its reply, recursively - "it's like calling a different prompt whose pieces just happen to be in the same file."

**Citations used:** 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]; 2026-08-09-1058-promptforge-core-large-part5.md [p430], [p432], [p433]; 2026-08-19-0048-promptforge-md-aug19.md [p55], [p58], [p60]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p242]

**Merge:** None. Distinct purpose (subroutine with return vs transfer without return).

## Record 4: "A section ends when the model replies with text and no tool calls..."

**Purpose:** Token economy and an observed failure. The author asked why a model that finished its work through tool calls should "waste output tokens with the word 'done'" - tool calls already count as output. Then a real papergate run failed: the prompt said "Do not output any text," the model recorded everything via tool calls and legally exited with empty content, and the engine hard-failed it as EmptyModelReply. So an empty stop-turn after a successful tool call is a clean exit, but every other empty turn still fails closed, because silently accepting empties is how runs like briefer's empty evidence.md pass while producing nothing.

**Citations used:** 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p3], [p6], [plans section]; 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions]; 2026-08-09-1058-promptforge-core-large-part5.md [p429]

**Merge:** None.

## Record 5: "Cyclic section calls are permitted because some tools require cycles..."

**Purpose:** A proposed structural restriction (H3 can only call H3 and down, acyclic call graph) was rejected on concrete grounds: "There are obviously tools which require cycles." The author also wants the prompt author free to organize the file however they want - "we can't predict all the organizations, and we know that we can have cycles." Runaway execution is a resource problem, not a structure problem, so it is bounded by "nesting limit, step budget, tool budget" instead of prohibition. Once subroutines, jump, and goto exist, "the same problems of any other computer programming language apply... with that power comes the responsibility" - coherence belongs to the prompt author, not the engine.

**Citations used:** 2026-07-30-1046-compaction-algorithm-large-part5.md [p369]-[p372]; 2026-08-02-1134-mcp-client-large-part5.md [p369], [p371], [p372]; 2026-08-19-0048-promptforge-md-aug19.md [p60]; 2026-07-28-0925-orchestrator-design-document.md [p18]; 2026-07-30-0534-promptforge-design-context.md [p4]

**Merge:** None.

## Record 6: "A task is either synchronous or asynchronous..."

**Purpose:** The driving case was a long-running research task: "this is how you have a 'research task' going nonstop, while the main context is getting bugfixes and speedups." That forces the sync/async split - a synchronous task is just "a function call with context reset," while an asynchronous one needs a rendezvous. The unique timestamped ID returned at launch exists for one reason: "we have to give the harness the ability to cancel... we need to let the model cancel the task, like, if it's stuck." Cancellation on section exit exists because the author asked what happens "if the main section tries to move on or tries to return" with a pending task - the pending task must be cancelled and the section told. Forks are not required to rejoin because the author could "see forking a section that calls itself over and over again until some condition is met... and then it never comes back."

**Citations used:** 2026-07-30-0534-promptforge-design-context.md [p22], [p23], [p25], [p26], [p27], [p28], [p34], [p35]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]; 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247]

**Merge:** None.
