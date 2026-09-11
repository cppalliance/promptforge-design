<!-- STATUS: advisory report - analytical/recommendation (feasibility variant) - what is needed to build an agentic harness IDE -->

# Building an Agentic Harness IDE: reuse vibbi's surfaces and PromptForge's plumbing, but write a new interactive agent loop

## Executive summary

Build it, and build it as a convergence of two assets you already have rather than a new system: verdict **GO, with one hard modification**. The vibbi substrate already supplies the surfaces an agent drives - a multi-root workspace, a patchable editor, a real terminal, a drivable browser, and a streaming chat panel - and its typed IPC command surface is, almost line for line, an agent tool registry. PromptForge already supplies the plumbing an agent needs behind those surfaces - a credential-custodian gateway with a shared concurrency budget, an extension-and-tool model, `register_capability`, and a hermetic Lua sandbox. The gap between them is not surfaces and not plumbing. It is the agent loop itself.

The hard modification is this: **do not run the IDE's agent inside PromptForge's `Executor`.** PromptForge is a batch pipeline runtime whose central mechanism is destroying context at every section boundary, whose control flow is written in advance by a prompt author, and whose one interactive primitive, `ask_user`, is a stub that fails the run. An interactive coding agent is the opposite on all three counts: it holds a conversation across a task, it decides its own next step, and it stops to ask and to seek approval constantly. Forcing the IDE agent into the pipeline executor fights the executor's load-bearing design. The recommendation is therefore a split: **one new interactive agent loop for human-in-the-loop coding, and PromptForge's pipeline executor kept intact and invoked as a tool from that loop** for repeatable batch analysis. Both share the gateway, the extension set, the tool registry, and `register_capability`, so the split costs no duplicated plumbing.

What must be built, in dependency order, is a surface-tool bridge exposing vibbi's commands to the agent, gateway routing for vibbi's chat, the interactive agent loop, an interactivity-and-approval channel that retires the `ask_user` stub, a patch-based edit tool with staleness detection, git-based checkpointing, the deferred LSP client for self-correction, and a verification step. Nothing in either existing design blocks this; the two were namespaced and scoped to converge. Confidence high that the convergence is sound; confidence medium on schedule until a time budget is set, which is the one open decision the plan cannot resolve for you.

## Contents

- 1. Recommendation
- 2. The two assets, and the one thing neither provides
- 3. Criteria the design is judged against
- 4. The load-bearing decision: two execution models, not one
- 5. What must be built, component by component
- 6. Options considered
- 7. Feasibility
- 8. Risks and how to retire them
- 9. Build path
- 10. Confidence
- 11. References

## 1. Recommendation

Build an agentic harness IDE by converging vibbi and PromptForge, under three rules that follow from what each system already is.

First, **reuse vibbi as the IDE shell and the surface provider.** Its command surface already reads as a tool registry: `read_file`, `write_file`, `list_dir`, `search_workspace`, the `terminal_*` family, and the browser control family are the exact tools a coding agent calls. Reversing this and re-hosting the shell would discard a working, security-audited substrate. Confidence high - the surfaces exist and are typed end to end.

Second, **reuse PromptForge's plumbing, not its execution model.** The gateway, the `Extension` trait, `register_capability`, the canonical-tool vocabulary, and the Luau sandbox are all reusable under an interactive loop without change. The `Executor` and its section model are not, because context-clearing and author-declared control flow are wrong for interactive coding. Confidence high - this follows directly from the two designs' own stated purposes.

Third, **write one new interactive agent loop, and call PromptForge pipelines as tools from it.** The loop is conversational, model-driven, and interruptible. When a task is repeatable and batch-shaped - gate a WG21 paper, run a diligence battery - the loop invokes a PromptForge pipeline as a single tool and gets back a path and a verdict. This keeps each system doing what it was designed to do. Confidence high on the architecture; confidence medium on the loop's reliability with self-hosted drivers until measured.

Each recommendation carries an owner and a next step in section 9. The do-nothing alternative - keep vibbi a plain editor and use Cursor for agent work - is a legitimate baseline and is scored in section 6.

## 2. The two assets, and the one thing neither provides

vibbi is a Tauri v2 desktop editor substrate that, by its own design document, "carries no autonomous agent; it supplies the surfaces an agent would later drive." It provides a canonicalize-then-contain filesystem boundary, a `portable-pty` terminal, a CodeMirror 6 editor across nine languages, a WebView2 browser that is drivable over the Chrome DevTools Protocol, ripgrep-style search, and a right-docked chat panel that streams from the Anthropic Messages API. Its untrusted browser webviews are isolated from every command by construction, which is the correct posture to extend to a second untrusted input source, the model. Its one deferred capability is an LSP client, so there are no real diagnostics today. (Source: design-vibbi.md.)

PromptForge is a single-binary Rust runtime that executes markdown prompts as an always-on service. It provides a gateway that holds LLM credentials, routes by model name, and owns a GPU concurrency budget shared across every process; an `Executor` that parses markdown into sections, walks them, substitutes slots, dispatches tools, and runs a Luau block per section; an MCP server that exposes each prompt as a tool; and an extension model where every domain capability is a linked Rust crate. It is explicitly built for batch, non-interactive pipelines on self-hosted mid-size models, and its design cites the evidence that fresh per-section context beats accumulated context. (Sources: design.md, design-promptforge.md, design-core-residue.md.)

Neither provides an interactive agent. vibbi's chat panel is a passthrough with no tool loop. PromptForge's executor is a pipeline engine whose interactivity primitive is stubbed: `ask_user` "is bound and it is not implemented: calling it returns `RunError::Unimplemented`," and its `Observer` is "one-way by design." The thing to build sits exactly in this gap.

## 3. Criteria the design is judged against

The reader is deciding among build approaches, so the options in section 6 are weighed against six criteria, ordered by how decisively each separates the options.

- **Interactivity.** A coding agent stops to ask, streams partial work, seeks approval before mutating, and can be interrupted. This is the criterion the pipeline executor fails.
- **Reliability on the target models.** The design must hold on self-hosted mid-size open-weight models, not only frontier APIs, because model sovereignty and roughly 1/100th frontier cost are PromptForge's stated reasons to exist.
- **Safety.** Model output is untrusted. Edits and commands must pass one auditable approval-and-checkpoint gate, mirroring vibbi's existing webview isolation.
- **Reuse.** Every component that already exists and is bought again is waste. The two assets were namespaced to converge; the design should honor that.
- **Deployment fit.** vibbi is a Windows-first desktop app; PromptForge binds a network interface and serves development-on-one-machine and production-on-an-intranet as first-class environments. The convergence must respect both.
- **Iteration speed.** A new capability should be cheap to add. PromptForge's whole value proposition is that a new pipeline is a markdown file, not new orchestration code.

## 4. The load-bearing decision: two execution models, not one

The single decision that shapes every later one is whether the IDE's agent runs inside PromptForge's `Executor` or in a new loop beside it. The recommendation is a new loop, and the reason is that the executor's three defining properties are each actively wrong for interactive coding.

The executor clears context on every transition. design-core-residue.md is unambiguous: "Model context is destroyed on every transition, `break_section` and `goto` alike," and this "is the design's central move," justified by evidence that focused context beats long context. That move is right for a batch pipeline that externalizes state to a store and pulls back only what each step needs. It is wrong for a coding session, where the user expects the agent to remember what it just did, why it chose an approach, and what the user said three turns ago. An interactive agent's continuity within a task is the feature; the executor's wipe destroys it.

The executor's control flow is written in advance. Every edge is declared by the prompt author in Lua with `break_section` or `goto`, and "there is no implicit advance." A coding agent's control flow is the opposite: the model decides the next action turn by turn from the evolving state of the code and the conversation. Encoding an open-ended coding task as a declared section graph would require the author to anticipate branches that only emerge at runtime, which is the case the executor's own design says it fits "badly."

The executor is non-interactive by construction. `ask_user` is a stub, the `Observer` is one-way, and a run "either completes or is rerun, so there is no half-answer to hand back." An IDE agent is a continuous dialogue with a human who approves edits, answers questions, and interrupts. These are not missing features of the executor; they are contrary to its discard-and-rerun model.

None of this argues against PromptForge. It argues that PromptForge is the wrong shape for the outer loop and the right shape for a called tool. The interactive loop handles the conversation, the editing, and the approvals; when the user asks for a repeatable batch job, the loop calls a PromptForge pipeline as one tool and receives a path and a one-line verdict, exactly as the design already anticipates for a Cursor caller. The two models share the gateway, the extensions, the tool registry, and `register_capability`, so the split duplicates plumbing nowhere. This is the whole recommendation in one sentence: **converge the plumbing, separate the loops.**

## 5. What must be built, component by component

Table 1 maps each component to what already exists, what is missing, and where the work lands. Prose follows for the components whose reasoning does not fit a cell.

**Table 1. Component readiness for an agentic harness IDE.**

| Component | Exists today | Missing | Lands in |
|---|---|---|---|
| Surface tools (fs, terminal, browser) | vibbi IPC command surface | Wrapping as bounded, model-facing tool schemas | vibbi + bridge |
| Model access and budget | PromptForge gateway; vibbi's direct Anthropic client | Routing vibbi chat through the gateway | vibbi chat -> gateway |
| Interactive agent loop | Neither | The loop itself: turn, tool-use, stream, stop | New crate |
| Interactivity and approval | vibbi chat panel; PromptForge one-way observer | Two-way channel; retire the `ask_user` stub | New loop + vibbi UI |
| Edit application | vibbi `write_file`, CodeMirror diff | Anchored patch tool with staleness check | vibbi + bridge |
| Checkpoint and recovery | vibbi persists layout/roots/settings | Per-action snapshot, git-based revert | New loop |
| Codebase context | vibbi search; PromptForge virtual files | LSP diagnostics; context assembler | vibbi LSP (deferred) |
| Verification | vibbi terminal | Run tests/build, read diagnostics, feed back | New loop |
| Batch pipelines as tools | PromptForge `Executor`, MCP surface | A tool wrapper the loop can call | PromptForge (as-is) |
| Safety isolation | vibbi webview isolation | Same discipline applied to model tool calls | New loop gate |

**Surface tools.** vibbi's commands are close to agent tools but are not identical to them. An agent tool must be bounded and model-legible: `read_file` should return line-numbered content and refuse or truncate very large files; the terminal tool must capture output under a timeout and a size cap rather than streaming unbounded into context; `search_workspace` already caps at 1000 matches with a `truncated` flag, which is exactly the discipline every tool needs. Bounded tool output is the single most important property, because unbounded results are the primary cause of context blowups and cost spikes. Confidence high.

**Gateway routing.** vibbi's chat panel today posts directly to `api.anthropic.com` with a key from the environment. Routing it through PromptForge's gateway instead buys the shared concurrency budget, logical model slots, and the choice between a frontier API and a self-hosted pod with no prompt change. This is a small change with a large payoff and should come early. Confidence high - the gateway "improves the existing Python stack with only a configuration change," and vibbi's chat client is already a thin, swappable transport.

**The interactive agent loop.** This is the genuinely new code. It runs the standard cycle: assemble a prompt from the conversation and the workspace state, call the model with the scoped tool schemas, stream text to the panel, validate each requested tool call, gate the risky ones, execute against vibbi's surfaces, append bounded results, and repeat until the model stops or needs the user. PromptForge's per-section tool scoping evidence applies directly here: keep the model's visible tool set small, because tool-selection accuracy is reliable at five to ten tools and cliffs past thirty. Confidence high on the loop's shape; confidence medium that a self-hosted driver follows a long coding session reliably, which is the same open risk PromptForge names for its own longest pipelines.

**Interactivity and approval.** This retires the `ask_user` stub, and it is the component that most distinguishes an IDE agent from a pipeline. The channel must carry a question or an approval request from the loop to the panel and a response back. vibbi's chat panel is the natural carrier, and MCP elicitation is the obvious protocol if the loop is reached over MCP, which design-core-residue.md already names as the likely path for a Cursor-style caller. Classify actions by risk: auto-allow reads, searches, and DOM snapshots; require approval for writes, edits, terminal commands, and cross-origin navigation; always show a diff or a command preview before it commits. This mirrors vibbi's existing rule that model output "becomes DOM at exactly one boundary" - here, model tool calls pass through exactly one validation-and-permission gate. Confidence high.

**Edit application.** `write_file` alone is a poor agent tool, because reproducing whole files is slow, costly, and error-prone. Add a patch tool: the model proposes an anchored search-and-replace or a unified diff, the handler verifies the file has not changed since the model read it, applies the edit, and renders it in CodeMirror's diff for approval. Anchored patches with staleness detection are how production coding agents avoid corrupting files. Confidence high.

**Checkpoint and recovery.** An agent that touches many files needs an undo larger than the editor's. Snapshot before each mutating action; git shadow commits or worktrees make wholesale revert cheap. Note that this is the reverse of PromptForge's discard-and-rerun model, which works only because batch pipeline writes are idempotent replace-all writes; interactive edits are not, so they need real checkpoints. Confidence medium - git-based checkpointing is simplest, but the exact granularity is a design choice to settle in build.

**Codebase context and LSP.** The agent is only as good as its prompt context. Send explicit context plus keyword search first, and defer embeddings until keyword search proves insufficient. The deferred vibbi LSP client pays off here: diagnostics let the agent see its own compile and type errors and self-correct, closing the loop. Confidence high on the value; confidence medium on effort, since the LSP client is unbuilt.

## 6. Options considered

Four options, weighed against the section 3 criteria. Table 2 summarizes; the do-nothing option is named explicitly, as a recommendation with no alternative is an assertion.

**Table 2. Options against the criteria (H high, M medium, L low fit).**

| Option | Interactivity | Reliability | Safety | Reuse | Deployment | Iteration | Verdict |
|---|---|---|---|---|---|---|---|
| A. Converge, separate loops (recommended) | H | M | H | H | H | H | Adopt |
| B. Run the IDE agent inside the `Executor` | L | M | M | M | H | L | Reject |
| C. Fork VS Code or build on Cursor | H | H | M | L | M | M | Fallback |
| D. Do nothing: plain vibbi plus Cursor | H | H | H | H | L | L | Baseline |

Option A is the recommendation of section 1: reuse both assets, share the plumbing, and write a new interactive loop that calls pipelines as tools. It scores highest on reuse and iteration and carries only the reliability uncertainty common to any self-hosted agent.

Option B forces the IDE agent into PromptForge's section model. It is rejected on the section 4 argument: context-clearing, declared control flow, and the stubbed `ask_user` are contrary to interactive coding, so this option scores L on interactivity and iteration despite reusing the most code. The reuse it appears to buy is illusory, because the executor would need interactive surgery that fights its own invariants.

Option C forks a mature editor or builds on Cursor's substrate. It scores highest on reliability and interactivity today, because that machinery is already built, but lowest on reuse, because it discards vibbi, and it forfeits the model-sovereignty and cost goals that motivate the self-hosted stack. It is the correct fallback only if the vibbi substrate proves inadequate for a demand not yet foreseen. Confidence medium - the right choice here depends on UI-control and licensing needs that are not yet specified.

Option D keeps vibbi a plain editor and uses Cursor for agent work. It is the honest baseline: zero build cost, full interactivity and reliability today, but it delivers no agentic harness IDE and forfeits every strategic reason to build one. It is the thing to beat, not the thing to ship.

## 7. Feasibility

Scored on the five standard feasibility dimensions, ending on a verdict.

**Technical: feasible.** Both assets exist and were scoped to converge. vibbi's crate namespacing (`vibbi-*`, disjoint from `promptforge-*`) and workspace layout were chosen so it "can later be moved into the separate `promptforge` workspace as a directory move rather than a rewrite." The surfaces are typed, the gateway is specified in implementable detail, and `register_capability` gives one path to add a tool. The genuinely new code is the interactive loop and its approval channel, which are well-understood patterns. Confidence high.

**Economic: favorable, and the point.** Routing through the gateway to self-hosted mid-size models targets roughly 1/100th of frontier API cost, which is PromptForge's stated economic thesis. The build cost is engineering time, not licensing or infrastructure, because the GPU stack and the editor substrate already exist. Confidence high on the direction; confidence low on absolute numbers until a time budget is set.

**Legal: low risk, one check.** The stack is Rust and web technology under permissive licenses; vibbi bundles JetBrains Mono, `@vscode/codicons`, and `material-icon-theme`, all redistributable. The one check is any model-weight license terms for self-hosted drivers, which is a procurement note rather than an architectural constraint. Confidence medium pending a license pass on the chosen models.

**Operational: two environments, both already first-class.** vibbi is a Windows desktop app; PromptForge serves development-on-one-machine and production-on-an-intranet, both binding a network interface. The IDE-plus-gateway pairing fits the development environment directly, and the same gateway serves a production intranet unchanged. The operational cost is running the gateway alongside the desktop app, which the design already assumes. Confidence high.

**Scheduling: unresolved.** design.md lists "time budget and deadline" as an open decision, and it is the one this report cannot close. The build path in section 9 is ordered so that value lands early and each phase is independently useful, which bounds schedule risk but does not set the schedule. Confidence low until a deadline exists.

**Verdict: GO, with the section 1 modification.** Build the convergence; do not fold the IDE agent into the pipeline executor.

## 8. Risks and how to retire them

The largest risk is the same one PromptForge already names: that a self-hosted mid-size driver follows a long, interactive coding session reliably enough to be useful. Retire it the way PromptForge retires its analog - measure early, on a real task, against a frontier baseline. Build the loop with a frontier model first to prove the mechanics, then swap in a self-hosted driver and measure the gap on a fixed set of coding tasks. Likelihood of a meaningful gap: roughly even. Confidence in the mitigation: high, because the measurement is cheap and decisive.

The second risk is that the two-loop split leaks: state or context the interactive loop holds becomes something a called pipeline silently depends on. Retire it by keeping the boundary exactly as PromptForge already defines a `Task` boundary - parameters in, a serialized result out, nothing else crossing. Confidence high, because the discipline already exists in the design.

The third risk is safety regression. vibbi's isolation invariant depends on browser webviews holding no capability; an agent loop that reaches those surfaces must not become a path that widens the command surface to untrusted content. Retire it by gating every mutating tool call behind the single approval choke point and keeping the loop's tools scoped per task. Confidence high.

## 9. Build path

Ordered so value lands early and each phase stands alone. Each step names an owner role and a next step, because an unactionable recommendation is a comment.

1. **Surface-tool bridge.** Owner: vibbi. Next step: wrap the existing fs, terminal, and browser commands as bounded tool schemas, reusing the 1000-match-cap pattern already in `search_workspace`.
2. **Gateway routing for chat.** Owner: gateway. Next step: point vibbi's chat client at the PromptForge gateway and replace the direct Anthropic client with a logical slot.
3. **Interactive agent loop, frontier model.** Owner: new loop crate. Next step: implement the turn-and-tool-use cycle with four read-only tools first, streaming to the existing chat panel.
4. **Approval and interactivity channel.** Owner: new loop plus vibbi UI. Next step: add the risk classifier and the diff-and-command preview, and implement the two-way channel that retires `ask_user`.
5. **Patch edit tool and checkpointing.** Owner: vibbi plus loop. Next step: add the anchored-patch tool with a staleness check and git-based per-action snapshots.
6. **LSP context and verification.** Owner: vibbi (LSP), loop (verification). Next step: build the deferred LSP client for diagnostics, then let the loop run tests and feed failures back.
7. **Pipelines as tools, self-hosted driver.** Owner: loop plus PromptForge. Next step: expose a PromptForge pipeline as one callable tool, then swap the loop's driver to a self-hosted model and measure against the phase-3 frontier baseline.

Keep every convergence invariant from the two designs while doing this: add tools only through `register_capability` so the drift test holds, keep browser webviews out of every capability, and route all filesystem work through vibbi's `Workspace` boundary.

## 10. Confidence

| Area | Level | Why |
|---|---|---|
| Convergence is sound | high | Both assets exist and were namespaced and scoped to merge |
| Two-loop split is correct | high | Follows from the executor's own stated context-clearing and control-flow design |
| Surfaces map to tools | high | vibbi's command surface already reads as a tool registry |
| Gateway routing | high | The gateway is a config-level improvement and vibbi's chat client is swappable |
| Interactive loop reliability | medium | Self-hosted driver on a long session is the same open risk PromptForge names |
| Safety model | high | Extends vibbi's existing single-boundary isolation posture |
| Edit and checkpoint | medium | Patterns are known; git-checkpoint granularity is a build-time choice |
| LSP and verification | medium | High value, but the LSP client is unbuilt in vibbi |
| Schedule | low | Time budget and deadline remain open decisions in design.md |

## 11. References

In-repo sources, referenced by identity rather than by any transient path.

- vibbi substrate design - `vibbi/design-vibbi.md`: surfaces, the IPC command contract, webview isolation, deferred LSP.
- PromptForge system design - `promptforge-design/design/design.md`: the gateway, the extension model, deployment environments, and the build path.
- PromptForge prompt-language design - `promptforge-design/design/design-promptforge.md`: the section model, context-clearing, tool-call state, per-section scoping, and the cited evidence behind each.
- PromptForge core-library design - `promptforge-design/design/design-core-residue.md`: the `Executor`, `register_capability`, `Surfaces`, the canonical vocabulary, the `ask_user` stub, and the one-way `Observer`.
- Report craft - `tools-public/how-to/reports-how-to.md`: the analytical/recommendation and feasibility rules this report is written against.

*2026-07-30 - Opus 4.8 (Cursor agent)*
