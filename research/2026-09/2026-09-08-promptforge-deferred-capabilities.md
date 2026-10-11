# PromptForge Deferred Capability Assessment

## Executive verdict

The highest-value deferred work is not additional prompting syntax. The active core already covers explicit finite pipelines, autonomous model-tool episodes, mutable provider-neutral histories, custom compactor callbacks, capability sealing, and synchronous section composition. The largest remaining gaps are:

1. **Generic `user_input()` and host input brokerage - 10/10.** This turns a retained message array and repeated `model_loop` calls into a real interactive or unattended workflow. Without it, Lua can describe a conversation loop but cannot obtain the next turn through the unified runtime.
2. **Asynchronous section tasks through `call_async` - 10/10.** This enables useful work to proceed while the parent continues, waits for input, or starts other children. Synchronous `call` cannot express that overlap.
3. **Cold restore backed by journals, snapshots, incarnation checks, and replay - 10/10 as a bundle.** This enables long-running sessions and suspended workflows to survive process loss or planned restart without repeating completed effects.
4. **Complete-document `execute(path, input?)` - 9/10.** This enables prompts to compose separately owned, separately bound PromptForge programs instead of copying them into one document or wrapping them as external tools.
5. **Task handles plus `tasks.await_all` - 9/10.** This enables dynamic parallel batches, ordered aggregation, all-settled collection, fail-fast cancellation, and explicit child-failure policy.
6. **Asynchronous complete-document `execute_async` - 9/10.** This combines reusable prompt programs with concurrent execution, enabling heterogeneous prompt graphs rather than only same-document worker sections.
7. **Model-visible subagent adapters - 8/10.** This lets a model delegate bounded work to PromptForge sections while preserving the same task lifecycle and correlated tool protocol.
8. **Task-aware store semantics - 7/10.** This makes shared-file collaboration between concurrent children safe enough to use for workflows that cannot be reduced to return-value aggregation.
9. **Sandboxed `require(path)` - 7/10.** This enables reusable Lua libraries with per-VM module state and source-relative identity. Today the reasonable substitute is duplication.
10. **`lua inherit` - 6/10.** This enables reusable lexical initialization across isolated section entries. It is significant for authoring larger prompt programs, but most workflows remain expressible through duplication.

Recommendation: implement the generic input boundary, the common task runtime, and durable replay as the next strategic capability layers. Confidence: high - each creates workflow classes that the active core cannot emulate through message reshaping or synchronous calls.

## Scoring method

Scores measure user workflows newly expressible relative to the stated active core, not engineering value:

- **10:** Creates a major workflow category that has no reasonable active-core substitute.
- **8 to 9:** Enables a broad class of workflows or removes a fundamental execution boundary.
- **6 to 7:** Materially expands what larger prompt programs can do, but a constrained or laborious substitute exists.
- **4 to 5:** Useful authoring or control capability with practical substitutes.
- **2 to 3:** Mostly safety, observability, ergonomics, or an enabling contract.
- **1:** No direct new user workflow, although implementation quality may still depend on it.

Scores for overlapping items are baseline scores, not additive business value. For example, `fanout` scores highly relative to the active baseline because the baseline has no concurrency, but its marginal capability after `call_async` and `tasks.await_all` exist is low because it is thin Lua sugar.

## Dependency spine

### Interactive and durable sessions

1. Generic host input broker with blocking, unavailable-fallback, and failing policies.
2. Direct `user_input() -> text, available` plus provenance-safe event recording.
3. Continuation-capable waits and section suspension.
4. Stable operation identities and journaling for every control-flow-relevant host observation.
5. Incarnation identity, task-graph snapshots, and deterministic replay.
6. Cold restore and Workshop migration.

### Concurrent child work

1. Common task scheduler, stable task and frame identities, lifecycle states, quotas, and structured parent closure.
2. `call_async` with deeply copied structured input.
3. Immutable handles, Outcomes, TaskErrors, `result`, `await`, and `cancel`.
4. `tasks.await_all` with ordered all-settled and atomic fail-fast modes.
5. Thin `fanout` and `pfanout`, model-visible subagent adapters, and task-aware store behavior.
6. Task journaling and persistence for restart-safe concurrency.

### Reusable composition

1. Source-relative confined resolver, frozen bytes, trust rules, limits, cycle detection, and source-aware diagnostics.
2. `require` for cached Lua module values.
3. Common task runtime plus complete child-prompt isolation for `execute`.
4. `execute_async` after asynchronous task semantics exist.
5. Explicit parsing, scope, lifecycle, persistence, and return semantics before `include`, `local_include`, or partial fragments.

### Long-context operation

1. The active compactor callback, validation, progress checks, and in-place replacement.
2. Pinned-prefix conventions and a shipped summarizing factory.
3. Stable conversation, projection, compactor-policy, and pin identities.
4. Compaction events and persistence integrated with replay.

## Full deferred inventory

### Interaction and host integration

1. **Generic input broker with blocking, immediate fallback, and failure policies - 10/10.**
   - Unlocks: One prompt can run as an interactive agent when a human is present and as an unattended agent when input is unavailable.
   - Dependencies: Host wait registry abstraction, cancellation behavior, trust and provenance recording.
   - Important detail: The exact fallback sentence plus `available == false` prevents fallback text from being mistaken for human speech.

2. **Direct `user_input()` - 10/10.**
   - Unlocks: Multi-turn chat, approval gates, clarification loops, interviews, iterative drafting, and runtime branching on whether a human actually answered.
   - Dependencies: Generic broker. Durable use also depends on operation journaling and restore.

2a. **Model-visible user-input tool adapter - 8/10.**
   - Unlocks: A model can decide that it needs clarification and request a human turn through the same correlated tool protocol used by other model-visible tools.
   - Dependencies: Generic broker, provenance-safe result recording, correlated tool dispatch, and continuation-capable waits.

3. **Continuation-capable waits - 9/10.**
   - Unlocks: Suspending only the current Lua fence while preserving the section VM and allowing other work to continue.
   - Dependencies: Coroutine suspension, host broker, scheduler, cancellation, and eventual journaling.

4. **Broader Workshop migration to the unified Markdown runtime - 8/10.**
   - Unlocks: The language-level interaction model becomes available in the primary interactive host instead of remaining a contract with no general UI path.
   - Dependencies: Input broker, unified messages, removal of Workshop's dependency on `runtime.events()`, and restored-session surfaces.

5. **Markdown-agent discovery - 4/10.**
   - Unlocks: Hosts can find and present prompt-defined agents without hard-coded registration.
   - Dependencies: Stable prompt metadata and host integration.
   - This improves deployability and discoverability more than expressiveness.

6. **Generic `ui()` host snapshot changes - 3/10.**
   - Unlocks: Optional adaptation to selected model or workspace presentation context.
   - Dependencies: Narrow non-authoritative host snapshot contract.
   - Correct workflows cannot depend on these fields, so the capability ceiling is intentionally low.

7. **Additional Workshop visual features - 2/10.**
   - Unlocks: Better visibility into compaction and restored sessions.
   - Dependencies: Compaction events and restore state.
   - This changes presentation, not what a prompt can express.

### Tasks, concurrency, and child execution

8. **Common asynchronous task runtime and scheduler - 10/10.**
   - Unlocks: Overlapping child work, background work during parent waits, dynamic work graphs, and nonblocking orchestration.
   - Dependencies: Task identity, state machine, run-wide scheduling, structured scope closure, quotas, and cancellation.

9. **`call_async(heading, input?)` - 10/10.**
   - Unlocks: A section can start isolated same-document work and continue before that child finishes.
   - Dependencies: Common task runtime, visible-heading resolution, fresh child VMs, structured input, and task handles.

10. **Deeply copied read-only JSON child input through `args` - 7/10.**
    - Unlocks: Structured section-worker and child-document requests, indexed batch inputs, and safe records crossing VM boundaries.
    - Dependencies: Canonical JSON conversion and child creation.
    - String input alone is an unreasonable substitute for larger worker protocols.

11. **Opaque task handles with stable `id` - 8/10.**
    - Unlocks: Retaining, polling, awaiting, cancelling, and correlating independently running children.
    - Dependencies: Stable task identity and host-owned userdata.

12. **Nonblocking idempotent `task:result()` - 8/10.**
    - Unlocks: Opportunistic consumption of background results without forcing the parent to wait.
    - Dependencies: Handles, immutable terminal Outcomes, and journaled nil probes for replay.

13. **Suspending `task:await()` - 8/10.**
    - Unlocks: Join points anywhere in Lua control flow while other tasks continue.
    - Dependencies: Handles, coroutine suspension, scheduler, and terminal outcomes.

14. **Durable `task:cancel(reason?)` - 7/10.**
    - Unlocks: User-defined timeout, abandonment, supersession, and sibling-cancellation policies.
    - Dependencies: Cancellation state, descendant propagation, provider or tool cooperation where available, and replay.

15. **Immutable Outcomes and stable TaskErrors - 7/10.**
    - Unlocks: Explicit best-effort collection, retry decisions, selective propagation, and programmatic handling of failure versus cancellation.
    - Dependencies: Terminal task state and stable error taxonomy.

16. **`tasks.await_all` in all-settled mode - 9/10.**
    - Unlocks: Parallel evaluation where every result matters even when some workers fail, with input-order aggregation.
    - Dependencies: Task handles, common scheduler, immutable Outcomes, and dense ordered input validation.

17. **`tasks.await_all` in atomic fail-fast mode - 9/10.**
    - Unlocks: Parallel work whose first canonical failure should cancel and drain unfinished siblings before propagating.
    - Dependencies: Atomic terminal selection, structured cancellation, descendant drain, and deterministic ordering.

18. **Thin `fanout(section, inputs)` - 8/10 from the active baseline, 3/10 after task primitives.**
    - Unlocks: Concise ordered parallel map with fail-fast behavior.
    - Dependencies: `call_async`, structured indexed input, and fail-fast `tasks.await_all`.

19. **Thin protected `pfanout(section, inputs)` - 8/10 from the active baseline, 3/10 after task primitives.**
    - Unlocks: Concise ordered parallel map that returns all Outcomes and does not cancel siblings on worker failure.
    - Dependencies: `call_async`, structured indexed input, and all-settled `tasks.await_all`.

19a. **Removal of legacy core `fanout`, `item`, `sys.index`, fanout result records, and fanout-specific store behavior - 1/10.**
    - Unlocks: No new workflow. The future generic task primitives retain the useful parallel behavior.
    - Dependencies: `call_async`, structured `args`, `tasks.await_all`, and migration of existing consumers.

20. **`tasks.await_any` - 6/10.**
    - Unlocks: First-result races, speculative alternatives, and latency hedging.
    - Dependencies: Deterministic candidate and cancellation semantics.
    - The contract deliberately defers this until there is a concrete race use case, so its score is lower than `await_all`.

21. **Model-visible subagent adapters - 8/10.**
    - Unlocks: A model can delegate bounded work to fixed PromptForge section workers through normal correlated tool calls.
    - Dependencies: Task runtime, fixed-target adapter, await-and-unwrap behavior, serialization, and recursion limits.

22. **Structured parent closure and descendant drain - 6/10.**
    - Unlocks: Safe background work without detached or orphan tasks, making early parent return and cancellation usable.
    - Dependencies: Child-creation gate, terminal intent, downward cancellation, and lifecycle ordering.
    - This mostly makes concurrency dependable, rather than adding a separate workflow category.

23. **Running-task, live-task, depth, time, wait, and recursion limits - 2/10.**
    - Unlocks: Safe admission of untrusted or accidentally explosive task graphs.
    - Dependencies: Scheduler and host policy.
    - These are operational guardrails, not new orchestration forms.

24. **Task-runtime tests, migrations, benchmarks, and adversarial matrices - 1/10.**
    - Unlocks: No direct workflow.
    - Dependencies: The owning task features.
    - They are required evidence for shipping but should not be ranked as user capability.

### Composition and control flow

25. **Sandboxed source-relative `require(path)` - 7/10.**
    - Unlocks: Shared Lua helpers, policy libraries, schemas, message constructors, and common compactor code without source duplication.
    - Dependencies: Resolver, confinement, frozen source identity, per-VM cache, cycle handling, and module errors.

26. **Frozen source-relative resolver and confinement contract - 3/10.**
    - Unlocks: Safe availability of `require` and external prompt execution from trusted roots, including embedded prompts with virtual roots.
    - Dependencies: Canonicalization, symlink and reparse-point checks, limits, source anchors, diagnostics, and trust classification.
    - This is an enabling security boundary, not a user-facing workflow by itself.

27. **Per-VM module cache and module return semantics - 5/10.**
    - Unlocks: Modules with stable local state and one-time initialization during a section entry.
    - Dependencies: `require`, frozen module identity, and cycle detection.

28. **Synchronous complete-document `execute(path, input?)` - 9/10.**
    - Unlocks: Reusable child prompt programs with their own frontmatter, bindings, section graph, and isolated prompt state.
    - Dependencies: Confined resolver, formal parser and executor entry, child isolation, shared run services, typed execution errors, and common task runtime for await-and-unwrap semantics.

29. **Asynchronous complete-document `execute_async(path, input?)` - 9/10.**
    - Unlocks: Concurrent heterogeneous prompt programs, including batches where each worker has a different document, bindings, and section structure.
    - Dependencies: `execute`, task runtime, handles, cancellation, confinement, and restoration.

30. **`include` - 6/10.**
    - Unlocks: Reuse of partial Markdown prompt material without turning it into a cached Lua module or a complete child prompt.
    - Dependencies: Still-unspecified parsing, lifecycle, scope, persistence, trust, and return semantics.
    - The score is provisional because the contract intentionally does not yet define enough behavior to identify the exact workflow boundary.

31. **`local_include` - 6/10.**
    - Unlocks: Locally scoped partial Markdown composition when a global include would leak or collide.
    - Dependencies: The same unresolved fragment contract plus explicit locality semantics.

32. **Partial Markdown fragment artifact - 6/10.**
    - Unlocks: A reusable unit between Lua modules and complete prompt documents, such as shared policy prose or section fragments.
    - Dependencies: Artifact grammar, source identity, trust, VM scope, persistence, and result behavior.

33. **`lua inherit` lexical initialization - 6/10.**
    - Unlocks: Shared declarations, constants, helper functions, and setup across fresh section VMs in a hierarchy.
    - Dependencies: Prefix grammar, deterministic root-to-leaf replay, declaring-file source anchors, and guidance against repeated host effects.

34. **`list_from_section(heading)` - 4/10.**
    - Unlocks: Treating a visible Markdown list as ordered structured input without duplicating it in Lua.
    - Dependencies: Heading visibility and strict list parsing.
    - Authors can currently encode the list in Lua, so this is literate-authoring convenience rather than a new execution class.

35. **`jump(heading)` as an inert contract - 5/10 if it is truly unavailable.**
    - Unlocks: Nonreturning dynamic transfer into another fresh section chain while carrying `var`.
    - Dependencies: Heading resolution, fresh VM entry, and inherited initialization when available.
    - `call` plus explicit return can approximate many cases. The sources conflict on status: the contract explicitly labels `jump` deferred, while the plan discusses it as an existing path affected by active `reply` removal.

36. **Operational frontmatter `input` and `output` semantics - 6/10.**
    - Unlocks: Machine-checkable prompt interfaces, composition validation, and host tooling that can connect prompts safely.
    - Dependencies: A decision on whether declarations validate files, `args`, returns, or external artifacts.
    - The syntax is described, but the plan explicitly leaves operational meaning open.

37. **Broader H1 bootstrap ownership - 3/10.**
    - Unlocks: Potentially more reusable or explicit top-level setup, depending on the eventual decision.
    - Dependencies: A concrete ownership contract.
    - No definite workflow can be credited while the behavior remains an open question.

38. **Nested prompt and module cycle limits, source diagnostics, and causal errors - 2/10.**
    - Unlocks: Safe diagnosis and bounded use of recursive composition.
    - Dependencies: `require` and `execute`.
    - These make composition shippable but do not independently add a workflow.

### Compaction

39. **`compactors.summarize(options)` - 6/10.**
    - Unlocks: Practical long conversations for authors who cannot safely implement protocol-aware summarization and retention themselves.
    - Dependencies: Active callback framework, tool-free inference, pinned-prefix policy, exchange-safe slicing, and progress validation.
    - The score is not higher because the active callback can already call `models.infer` or `handle:infer`, so expert authors can express custom summarization now.

40. **Pinning helpers - 4/10.**
    - Unlocks: Reliable retention of policy and selected records without hand-written index logic.
    - Dependencies: Stable prefix or record identity and compactor validation.

41. **Other shipped compaction strategies - 4/10.**
    - Unlocks: Turn dropping, extraction, hybrid summarization, or domain-specific retention with less author code.
    - Dependencies: Active callback and replacement contract.
    - No particular new workflow can score higher until a strategy is specified.

42. **Stable compactor-policy and pinned-record identity - 3/10 directly, 7/10 as a restore enabler.**
    - Unlocks: Reliable recognition of the same retention policy and immutable prefix after replay.
    - Dependencies: Stable conversation and projection identities.
    - The plan says compactor identity remains deferred, but the language contract also says a continuing array seals compactor identity. That status needs reconciliation.

43. **Rich compaction events - 3/10.**
    - Unlocks: Auditing when and why context changed, with hashes, spans, policy identity, estimates, and counts.
    - Dependencies: Stable policy identity and canonical host events.
    - Events intentionally omit replacement content, so they support operations and audit rather than model behavior.

43a. **Content-free compaction records - 2/10.**
    - Unlocks: Privacy-preserving replay correlation and audit without persisting replacement prompt content, injected files, framing, or schemas in the event record.
    - Dependencies: Projection hashes, source spans, policy identity, reason, estimates, and record counts.

44. **Compaction persistence - 7/10.**
    - Unlocks: Long-running conversations that retain their compacted projection coherently through suspension and restart.
    - Dependencies: Projection identity, content-free compaction records, snapshots, incarnation, and replay.

45. **Compactor attempt and context-reserve limits - 2/10.**
    - Unlocks: Bounded failure instead of runaway compaction.
    - Dependencies: Host limits and active callback invocation.

### Persistence, events, and concurrent state

46. **Journaled host operations - 8/10.**
    - Unlocks: Suspend and replay without repeating completed effects or changing prior control-flow observations.
    - Dependencies: Stable operation IDs, canonical argument digests, result schemas, and policy identity.

47. **Journaling nil result probes, wait candidate sets, cancellation races, reads, clocks, input, and UI snapshots - 6/10.**
    - Unlocks: Deterministic continuation of workflows whose branching depends on absence, timing, or race outcomes.
    - Dependencies: General operation journal and stable identities.
    - This is a critical completeness requirement for replay, not a separate surface API.

48. **Atomic task-graph and store snapshots - 8/10.**
    - Unlocks: Fast durable checkpoints for sessions with active frames, waits, children, message projections, and shared files.
    - Dependencies: Journals, event offsets, task state, replay cursors, store versions, and durable boundaries.

49. **Section incarnation identity and drift checks - 7/10.**
    - Unlocks: Safe resume only when prompt source, policy, limits, runtime, and continuing conversations still mean the same thing.
    - Dependencies: Stable hashes and identities for every sealed capability and deferred source artifact.

50. **Deterministic VM reconstruction and replay - 9/10.**
    - Unlocks: Resuming sections without serializing Lua stacks, closures, globals, or userdata and without repeating recorded effects.
    - Dependencies: Journals, snapshots, incarnation checks, fresh VM entry, and replay verification.

51. **Cold restore under an exclusive ownership epoch - 10/10 as the completed stack, 4/10 for epoch handling alone.**
    - Unlocks: Long-lived interactive and concurrent PromptForge sessions that survive host restarts and process failure.
    - Dependencies: Incarnation, snapshots, journals, replay, task persistence, store atomicity, and exclusive ownership.

52. **Task, wait, outcome, and cancellation persistence - 9/10.**
    - Unlocks: Background children and suspended interactions that remain valid across restart.
    - Dependencies: Stable task IDs, lifecycle events, snapshots, and replay.

53. **Stable conversation, mutable projection, policy, and pinned-prefix identities - 4/10 directly, 8/10 as a persistence prerequisite.**
    - Unlocks: Durable continuation without serializing Lua table or closure identity.
    - Dependencies: An unresolved identity model.

54. **Stable task and frame IDs derived from run and operation identity - 3/10 directly.**
    - Unlocks: Durable handle correlation and unambiguous host observation.
    - Dependencies: Run identity, incarnation, frame activation, and asynchronous-call operation identity.

55. **External-operation reattachment, deduplication, and fail-closed `indeterminate_operation` - 7/10.**
    - Unlocks: Safe recovery around model or tool calls that may have been dispatched when the host failed.
    - Dependencies: Stable remote operation IDs or provider deduplication support.
    - This cannot guarantee provider-independent exactly-once effects, but it enables honest recovery instead of blind retry.

56. **Canonical task, wait, compaction, model-attempt, and lifecycle events - 3/10.**
    - Unlocks: Host-side audit, diagnostics, and restored-session presentation.
    - Dependencies: Gap-free event sequencing and stable identifiers.
    - Prompt Lua intentionally cannot consume these events, limiting direct workflow impact.

57. **Removal of `runtime.events()` from Lua - 1/10.**
    - Unlocks: No positive user workflow. It removes a broad observation path in favor of narrow APIs.
    - Dependencies: Workshop migration and replacement of legitimate consumers with operation results, counters, metrics, store state, or dedicated APIs.

58. **Event sandbox tests and broader event migration - 1/10.**
    - Unlocks: No direct workflow.
    - Dependencies: Event-view removal and host observation.

59. **Task-aware linearizable and journaled store operations - 7/10.**
    - Unlocks: Concurrent children can collaborate through shared virtual files with defined read-your-writes and replay behavior.
    - Dependencies: Task and operation IDs, commit sequencing, snapshots, and replay.

60. **Conflict detection for causally unordered destructive mutations - 6/10.**
    - Unlocks: Safe shared-file workflows that fail visibly instead of silently losing concurrent changes.
    - Dependencies: Causal ordering and atomic store commits.

61. **Atomic concurrent append with replay-stable commit order - 6/10.**
    - Unlocks: Many workers can contribute independent notes, evidence, or log fragments to one path without corruption.
    - Dependencies: Linearizable append, persisted commit sequence, and conflict rules against destructive operations.

62. **Atomic store mutation plus operation-result commit - 5/10.**
    - Unlocks: Restore cannot duplicate a completed append or expose a mutation without its recorded completion.
    - Dependencies: Journaled store and snapshots.

63. **Store race, cancellation, replay, and restore tests - 1/10.**
    - Unlocks: No direct workflow.
    - Dependencies: Concurrent store and persistence features.

### Deferred ergonomics, optimization, and host scope

64. **Implicit trailing-prose or other prose sugar - 2/10.**
    - Unlocks: Shorter routine prompts.
    - Dependencies: Measured authoring evidence and an unambiguous rule.
    - The active explicit `models.infer(prose)` path already expresses the workflow.

65. **Shared-VM optimization - 2/10.**
    - Unlocks: At most implicit state sharing across entries.
    - Dependencies: A serializable isolation model that avoids path-dependent hidden globals.
    - This is both low-value and contrary to the current fresh-VM semantic guarantee.

66. **VM pooling - 1/10.**
    - Unlocks: No new workflow.
    - Dependencies: Benchmarks and proof that isolation semantics remain unchanged.

67. **Gateway provider redesign beyond tokenizer or budget support - 1/10.**
    - Unlocks: No defined PromptForge workflow.
    - Dependencies: A concrete provider limitation.

68. **Deferred inheritance, summarization, task, module, restore, platform, and Workshop benchmarks or matrices - 1/10.**
    - Unlocks: No direct workflow.
    - Dependencies: Their owning features.

## Use-case evidence

- **Mentograph evidence:** A user can continue an interview while domain research runs in the background, wait for one or more user turns, then consume a late result. This demonstrates the combined need for `user_input`, `call_async`, nonblocking task observation, live children during parent waits, and eventually task persistence. It does not by itself justify a separate Mentograph-specific primitive.
- **Papergate evidence:** A user can dispatch multiple evaluators concurrently, aggregate in input order, choose fail-fast or all-settled behavior, and transfer results explicitly. This demonstrates `call_async`, structured task input, `tasks.await_all`, Outcomes, `fanout`, and `pfanout`. It does not justify fanout-specific store semantics.

## Contract inconsistencies that affect prioritization

1. **Model-visible subagent status:** The plan consistently defers model-visible subagent adapters with the task runtime. The language contract's task section says they use the same runtime "in the current implementation scope." Given the explicit active-scope paragraph and deferred work list, this assessment treats them as deferred.
2. **`jump` status:** The language contract explicitly marks `jump` deferred and inert. The plan also treats jump as an existing execution path when discussing fresh VMs and active `reply` removal. Confirm whether only new jump semantics are deferred or whether the API itself is unavailable.
3. **Compactor identity status:** The plan says compactor identity remains deferred, while the language contract says each continuing message array seals its compactor identity. The active baseline clearly includes model and tool sealing, but not durable compactor identity. This assessment treats durable compactor identity as deferred.
4. **Frontmatter I/O status:** Frontmatter permits `input` and `output` declarations, but their operational semantics remain an explicit open question. Syntax should not be counted as the capability.

## Priority interpretation

The best next feature depends on the product goal:

- For an interactive agent product, implement `user_input` and the generic broker first. Confidence: high - it is the smallest boundary that converts the existing retained-history loop into a genuine conversation.
- For batch and research orchestration, implement the common task runtime, `call_async`, handles, and `tasks.await_all` as one coherent slice. Confidence: high - partial task APIs do not deliver safe concurrency.
- For reusable prompt packages, implement confined `require` before partial Markdown includes, then implement complete-document `execute` on the common task runtime. Confidence: high - `require` has a settled contract, while fragment semantics remain unresolved.
- For reliable long-running sessions, treat journal, snapshot, incarnation, replay, and cold restore as one system rather than isolated features. Confidence: high - omitting any one of them breaks replay safety or usable recovery.
- Do not prioritize built-in summarization ahead of interaction, tasks, composition, or restore. Confidence: high - the active compactor callback already lets expert authors implement summary policy, so the incremental workflow unlock is smaller.

*2026-09-08 16:12 - GPT-5.6 Sol*



