# PromptForge: What the Field Does and What to Steal

Report type: evaluation / review. It judges PromptForge against 4 popular codebases sharing its Rust agent-infrastructure technique, and prescribes idioms to adopt, in payoff order.

## Executive summary

PromptForge's crate discipline already matches the field; its public API shape does not. All four references converge on a narrow, deny-missing-docs facade over wide internals with CI guards behind the layering rules - exactly the machinery PromptForge lacks at its gateway and Lua seams, where re-export shims and a `#[doc(hidden)]` contract do the work a published surface should. The top finding pays by converting convention-only layering into enforced layering with a documented facade, which also frames the 4,608-line `gateway/src/lib.rs` split. For the agentic-IDE mission, the field offers five steals PromptForge has no equivalent of: fail-closed execution budgets, a sans-I/O turn planner for durable agents, a reconnecting SSE state machine, per-session git worktrees, and offline LLM simulation.

### Key findings

1. **Adopt a single facade crate with `#![deny(missing_docs)]` and publish the wire protocol as its own crate** - converged on by everruns, yolop, and the everruns SDK. PromptForge's documented API (`Prompt`, `run`, `LuaProgram`) sits over a wide undocumented seam; the field's answer is a small facade plus a versioned protocol crate with a drift guard. Confidence: high.
2. **Give the layering rules CI teeth: dependency pins, a public-api snapshot, and re-export bans** - everruns enforces its crate graph with shell scripts over `cargo metadata`; PromptForge's family-prefix rules are convention-only and already leaking through shims. Confidence: high.
3. **Aggregate integration tests into one binary, with an enumeration guard and a no-`#[ignore]` tripwire** - converged on by bashkit, everruns, and yolop; directly retires the 1,500-3,150-line inline test modules. Confidence: high.
4. **Publish a stable narrow projection over unstable internals for host-facing gating** - bashkit's `analysis.rs` is the strongest human-provenance idiom in the field and the model for shrinking the Lua-host seam. Confidence: high.
5. **Adopt the decision-comment convention backed by a CI-enforced knowledge bundle** - bashkit and yolop both keep architecture prose in a maintained `knowledge/` tree instead of an accreting AGENTS.md. Confidence: medium.
6. **Add a fail-closed execution budget and a runtime progress guard** - bashkit and yolop enforce at runtime what PromptForge only reports; the natural extension of its cancellation substrate to long-running agents. Confidence: medium.
7. **Steal the sans-I/O turn planner with a serializable `TurnState`** - everruns' pure planner is the bridge from PromptForge's single-owner scheduler to durable, resumable coding agents. Confidence: medium.
8. **Steal the reconnecting SSE state machine with a poll-level idle timeout** - the SDK's stream layer catches half-open connections that `read_timeout` never fires on; directly transferable to the gateway's SSE/WS relays. Confidence: medium.
9. **Adopt per-session git worktrees with canonicalized ownership checks** - yolop's isolation primitive for parallel coding agents, including restore-safety checks. Confidence: medium.
10. **Build a deterministic offline LLM simulation driver** - everruns' `llmsim` (also shipped as a yolop provider) runs the whole agent loop in tests without credentials. Confidence: medium.

## Method

The subject was profiled first through nine lenses (module decomposition, state ownership, boundaries, errors, lifecycle, testing, comments, build, messes). The operator supplied the four-reference shortlist directly, replacing the field survey; all four references were dived in parallel at pinned commits, every cited idiom walked for AI-marker provenance with a pre-AI rewind where markers appeared, and synthesis clustered idioms by convergence and mapped them onto the profiled deficits. Per the operator's focus, findings 1-5 rank deficit-mapped idioms (crate structure and public API shape); findings 6-10 are feature steals mapped to the agentic-IDE mission rather than to a profiler deficit, and are labeled as such. Citations were checked against the pinned clones: 36 of 41 passed, 5 were corrected (one wrong file, one missing path prefix, three stale line counts); none were unverifiable.

## Reference projects and provenance

| Reference | Popularity | Why chosen | License | Provenance of cited idioms |
|---|---|---|---|---|
| [everruns/bashkit](https://github.com/everruns/bashkit) | 269 stars | Operator-selected; sandboxed tool execution for agents | MIT | 1 strong human signal (`analysis.rs`), remainder explicit AI marker, several AI-originated; the decision-comment principle held up against its pre-AI form |
| [everruns/everruns](https://github.com/everruns/everruns) | 47 stars | Operator-selected; durable agentic harness engine | MIT | 5 strong human signal (all guard scripts, `machine.rs`, `work.rs`), 3 explicit AI marker (facade, turn planner, llmsim all present in pre-AI form) |
| [everruns/yolop](https://github.com/everruns/yolop) | 15 stars | Operator-selected; terminal coding agent, closest mission overlap | MIT | 1 unknown (AI attribution disabled repo-wide), remainder explicit AI marker; 4 held up or tightened against pre-AI forms, 1 AI-originated |
| [everruns/sdk](https://github.com/everruns/sdk) | 0 stars (new) | Operator-selected; multi-language SDK public API shape | MIT | 2 explicit AI marker: sub-client facade present pre-AI; SSE machinery AI-introduced over a thin pre-AI wrapper |

## Baseline: where the subject stands

PromptForge is a 34-crate Rust workspace (~557 `.rs` files, ~85% Rust, plus two esbuild TypeScript SPAs) delivering two cooperating programs: `promptforge-gateway`, a headless OpenAI-compatible server and sole credential holder, and `promptforge-workshop`, a Tauri desktop hosting its own server in-process, talking over loopback HTTP/SSE/WS with Jupyter-style discovery. Build is cargo (edition 2024, MSRV 1.89) with rust-embed for the SPAs and cargo-dist plus Tauri bundling for release.

Strengths the findings build on: enforced family-prefixed workspace layering with stated cross-product dependency rules; a typed coroutine `Request`/`Answer` protocol as a one-read audit surface; structural cancellation and progress (CancellationToken, VM instruction-hook abort, `shared-progress`); error discipline with typed `non_exhaustive` public errors and workspace-denied `unwrap`/`expect`; and multi-process attach done right (discovery file with liveness proof, launch-election lock, process-lifetime lease).

Deficits the findings map to: (1) `gateway/src/lib.rs` at 4,608 lines mixing router, ~25 handlers, app state, and inline tests; (2) inline test modules of 1,500-3,150 lines inside source files; (3) a wide `#[doc(hidden)]` cross-crate Lua seam (~20 items) imported by `promptforge-agent`; (4) re-export shims (`gateway::wire/upstream/queue`, `core::untrusted`) keeping pre-split aliases alive; (5) a thin documented public API over a wide undocumented seam surface; (6) tray/sidecar platform code concentrated in the gateway crate; (7) two hand-rolled-DOM SPAs sharing only a small `shared-ui` package.

## Detailed findings, ranked by payoff

### Finding 1: Facade crate with `deny(missing_docs)` plus a published wire-protocol crate

Three references independently ship the same shape. everruns makes `crates/everruns` the only application-facing crate, with `#![deny(missing_docs)]`, a value-first API, and an offline-by-default simulated model ([lib.rs:L1-L90](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/everruns/src/lib.rs#L1-L90)). yolop publishes its wire protocol as its own crate, `yolop-yep`, with types plus a minimal server SDK and a CI schema drift guard ([lib.rs:L1-L27](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/crates/yolop-yep/src/lib.rs#L1-L27)). The SDK hands out short-lived per-resource sub-clients from one immutable `Clone` client, so the public surface is a facade over generated internals ([client.rs:L160-L216](https://github.com/everruns/sdk/blob/46979f8801b666c8c6f2d41970e44e844079a688/rust/src/client.rs#L160-L216)).

This replaces PromptForge's current arrangement: a thin documented API (`Prompt`, `run`, `LuaProgram`) over the wide `#[doc(hidden)]` `promptforge-lua` seam that `promptforge-agent` imports ~20 items from, and the implicit gateway HTTP contract that lives only in handler code. The fix: create a `promptforge` facade crate re-exporting the documented API with `deny(missing_docs)`, and extract the gateway/workshop wire types into a published `promptforge-proto` crate with a schema snapshot test. Confidence: high - three-reference convergence on the same shape.

### Finding 2: CI architecture guards - dependency pins, public API snapshot, re-export bans

everruns keeps ~15 bash scripts that pin exact crate dependency sets via `cargo metadata` + jq diff ([check-core-kernel-dependencies.sh](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/scripts/lib/check-core-kernel-dependencies.sh)) and snapshot the public API in a checked-in file while grep-banning forbidden re-exports ([check-core-public-api.sh](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/scripts/lib/check-core-public-api.sh), `crates/core/public-api.txt`). bashkit ties its knowledge-contract check into the standard lint entry point ([justfile:L78](https://github.com/everruns/bashkit/blob/8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a/justfile#L78)).

This replaces PromptForge's convention-only family-prefix rules (stated in AGENTS.md, enforced nowhere), under which the `gateway::wire/upstream/queue` and `core::untrusted` re-export shims survive unmolested. The fix: three scripts - a dependency-set pin per crate family, a `public-api.txt` snapshot for the new facade crate, and a grep-ban on the shim paths once deprecated - wired into the existing CI lint stage. Confidence: high - strong human signal on both everruns scripts, and the mechanism directly names PromptForge's deficit 4.

### Finding 3: Aggregated integration-test binary plus enumeration guard and no-`#[ignore]` tripwire

bashkit consolidates integration tests into one binary declaring ~80 modules, with written criteria for exceptions ([main.rs:L1-L12](https://github.com/everruns/bashkit/blob/8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a/crates/bashkit/tests/integration/main.rs#L1-L12), `knowledge/operations/testing.md`). everruns runs a script verifying every test target is named in a CI workflow or allowlisted with a reason ([check-test-enumeration.sh](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/scripts/lib/check-test-enumeration.sh)). yolop bans `#[ignore]`: environment-dependent tests skip at runtime, and `YOLOP_REQUIRE_LIVE_TESTS=1` upgrades the skip to a hard failure in CI ([integration.rs:L1-L20](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/tests/integration.rs#L1-L20)).

This replaces PromptForge's 1,500-3,150-line `#[cfg(test)]` modules embedded in source files (deficit 2), which blur file roles and inflate the files the other findings need to split. The fix: move integration-scale tests into `tests/` binaries per crate (one aggregated binary where module count is high), adopt the enumeration guard so no test file silently never runs, and adopt the env-var tripwire for live-provider gateway tests. Confidence: high - three-reference convergence, small cost, and it unblocks findings 1 and 4.

### Finding 4: Stable narrow projection over unstable internals

bashkit's `analysis.rs` publishes a literal-or-null AST projection with bounded output (`MAX_ANALYSIS_NODES`) and `COMMAND_WRAPPERS` expressed as data, so embedders gate permissions on a stable narrow surface instead of drifting against interpreter internals ([analysis.rs:L1-L60](https://github.com/everruns/bashkit/blob/8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a/crates/bashkit/src/analysis.rs#L1-L60)).

This is the model for shrinking PromptForge's `promptforge-lua` seam (deficit 3): instead of `promptforge-agent` importing ~20 `#[doc(hidden)]` items, the Lua host publishes one versioned projection type - what a script may request, what the host will answer - and internals move freely behind it. PromptForge's `Request`/`Answer` coroutine protocol is already the right substrate; this finding is about making its surface narrow, bounded, and documented rather than wide and hidden. Confidence: high - the only strong-human-signal idiom at a seam boundary, and it maps to two named deficits.

### Finding 5: Decision-comment convention backed by an enforced knowledge bundle

bashkit pairs a decision-comment convention - comments record the non-obvious why at seams - with a canonical `knowledge/` bundle governed by a written maintenance contract ([AGENTS.md:L14](https://github.com/everruns/bashkit/blob/8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a/AGENTS.md#L14), `knowledge/knowledge-contract.md`). yolop runs the same play with progressive disclosure and a single-owner-per-instruction rule, validated in CI ([agent-context.md:L20-L41](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/knowledge/specs/agent-context.md#L20-L41), `knowledge/index.md`, `scripts/validate_okf.py`).

This addresses deficit 4's root cause: the re-export shims survive because nothing records why each seam exists or who owns it. The fix: adopt the decision-comment convention at every shim and seam, and move growing architecture prose out of AGENTS.md into a `knowledge/` tree with one owner per rule and a CI validation step. Confidence: medium - two-reference convergence, but the enforcement tooling is partly AI-originated with no pre-AI form.

### Finding 6 (feature steal): Fail-closed execution budget plus runtime progress guard

bashkit scopes one non-resettable, `Arc`-shared `ExecutionBudget` per request - work units, bytes, deadline, cancel flag - cloned to every descendant, and any breach poisons the whole request ([limits.rs:L754-L830](https://github.com/everruns/bashkit/blob/8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a/crates/bashkit/src/limits.rs#L754-L830)). yolop enforces progress at runtime via pre/post-tool hooks that intervene when an agent loop stalls, rather than relying on prompt-only guidance ([progress_guard.rs:L1-L5](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/src/capabilities/progress_guard.rs#L1-L5), thresholds at [L29-L44](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/src/capabilities/progress_guard.rs#L29-L44)).

Maps to no profiler deficit; it extends strength 3 for the agentic-IDE mission. PromptForge's `shared-progress` hub reports progress but never acts on it, and its CancellationToken cancels but does not budget. The fix: add a request-scoped budget type cloned into every Lua task and agent run spawned by a turn, and add a hook that flags a run making no forward progress across N tool calls. Confidence: medium - two-reference convergence; both mechanisms verified at HEAD, one tightened since its pre-AI form.

### Finding 7 (feature steal): Sans-I/O turn planner with serializable `TurnState`

everruns' engine is a pure synchronous planner: facts and `now` go in, a `TurnPlan` plus ordered `TurnLifecycleEffect`s come out, and one serializable `TurnState` drives both the in-process and durable hosts ([turn.rs:L1-L10](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/engine/src/turn.rs#L1-L10), [machine.rs:L23-L58](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/engine/src/machine.rs#L23-L58)).

Maps to no profiler deficit; it is the bridge from PromptForge's single-owner scheduler to durable, resumable long-running coding agents - the difference between an agent that dies with the workshop process and one that survives restarts. The fix: introduce a pure turn-planning core for the agent loop that emits effects for a host to execute, with the loop's state serializable at every boundary; adopt incrementally behind the existing scheduler. Confidence: medium - single-source and large cost, but the mechanism was fully present in its pre-AI form and unchanged at HEAD.

### Finding 8 (feature steal): Reconnecting SSE state machine with poll-level idle timeout

The SDK's stream layer distinguishes graceful from unexpected disconnects: server `disconnecting` events carry a `retry_ms` hint and never consume retry budget, unexpected drops back off 1s-30s, a `connected` event resets backoff, and resume uses a `since_id` cursor ([sse.rs:L366-L493](https://github.com/everruns/sdk/blob/46979f8801b666c8c6f2d41970e44e844079a688/rust/src/sse.rs#L366-L493)). A poll-level idle timeout is raced against the inner stream because `read_timeout` never fires on streaming SSE bodies and heartbeats are parser-invisible ([sse.rs:L31-L35](https://github.com/everruns/sdk/blob/46979f8801b666c8c6f2d41970e44e844079a688/rust/src/sse.rs#L31-L35), [L400-L418](https://github.com/everruns/sdk/blob/46979f8801b666c8c6f2d41970e44e844079a688/rust/src/sse.rs#L400-L418)).

Maps to no profiler deficit; it hardens the loopback HTTP/SSE/WS channel between workshop and gateway for sessions that run for hours, where a half-open TCP connection currently reads as a stuck agent. The fix: port the state machine (graceful-vs-unexpected, hint-driven retry, cursor resume, idle race) into the workshop's gateway client. Confidence: medium - single-source, AI-introduced with no comparable pre-AI form, but the behavior is pinned by a normative spec and test checklist.

### Finding 9 (feature steal): Per-session git worktrees with canonicalized ownership checks

yolop gives each agent session its own git worktree branched from `origin/main`, carries ignored local files along via `.worktreeinclude`, and runs a canonicalized ownership check before any restore touches the tree ([worktree.rs:L1-L26](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/src/exec/worktree.rs#L1-L26), [L94-L100](https://github.com/everruns/yolop/blob/a2b94a794827dce860b640b2948f75d8b27836a0/src/exec/worktree.rs#L94-L100)).

Maps to no profiler deficit; it is the core isolation primitive for an IDE running multiple coding agents against one repository - each agent edits its own worktree, and the IDE merges. The fix: add a session-scoped worktree manager to the workshop's agent runner, with the ownership check gating any checkpoint/restore of workspace state. Confidence: medium - single-source; mechanism held up against its pre-AI form.

### Finding 10 (feature steal): Deterministic offline LLM simulation

everruns ships `llmsim`, an offline scripted LLM driver with failure injection, paired with a leased at-least-once session `WorkQueue` for recovery testing ([lib.rs:L1-L20](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/drivers/llmsim/src/lib.rs#L1-L20), [work.rs:L1-L20](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/everruns/src/work.rs#L1-L20)); yolop exposes the same simulator as a first-class provider (`--provider llmsim`), so the whole agent loop runs with no API key.

Maps to no profiler deficit; it is the test substrate an agentic IDE needs - long-running agent behavior, cancellation, and resume exercised deterministically in CI without credentials. The fix: add a scripted-provider mode to the gateway's upstream abstraction, scriptable per test, with failure-injection hooks. Confidence: medium - two-reference presence; the everruns driver was fully present in its pre-AI form.

## Provenance

All four references carry heavy AI-marked history: bashkit 533 of 1,756 commits since 2022, everruns 1,074 of 3,381, yolop 187 of 659, the SDK 57 of 157. yolop disabled AI attribution on day two, so its one clean cited file (`agent-context.md`) is tagged `unknown` - the named-maintainer signal carries no weight there. The load-bearing architecture idioms skew human or pre-AI: everruns' guard scripts, `machine.rs`, and `work.rs` are single-maintainer strong human signal; bashkit's `analysis.rs` has zero AI-marked touches; and the everruns facade, sans-I/O planner, llmsim driver, yolop-yep protocol crate, progress guard, worktree manager, and test tripwire were all verified present in their pre-AI forms - none degraded, and the progress guard was tightened (file-read gating added). The AI-originated idioms - bashkit's `ExecutionBudget`, aggregated test binary, and knowledge-contract tooling, plus the SDK's entire reconnection machine - have no pre-AI form to compare against; the SDK's pre-AI stream layer was a thin `reqwest-eventsource` wrapper carrying a "could implement reconnection logic here" comment, so the AI-era version is strictly richer there. bashkit's AGENTS.md mandates human-only commit attribution while 533 commits carry Claude trailers - read its policy text as aspiration, not evidence. A sample of four repos from one org cannot carry any general conclusion about AI-authored code.

## Where the subject already matches or beats the references

- Error discipline: typed `non_exhaustive` public errors with workspace-denied `unwrap`/`expect` beats all four references; everruns classifies errors only at the provider boundary, and none of the others show an equivalent lint floor.
- Multi-process attach: the discovery file with liveness proof, launch-election lock, and process-lifetime lease (`shared-sidecar`) has no equivalent in any reference; yolop's stdio control plane is simpler but strictly single-purpose.
- Typed coroutine audit surface: the `Request`/`Answer` protocol is richer than bashkit's one-way literal-only analysis projection; finding 4 narrows its surface but keeps the mechanism.
- Cancellation substrate: CancellationToken plus a VM instruction-hook abort matches bashkit's budget cancel flag and exceeds yolop, which can only intervene at tool boundaries.
- File-size discipline: PromptForge's worst file (4,608 lines) is smaller than the worst file in every reference (12,874 / 5,708 / 10,540 / 1,795 lines) - but the field's messes show exactly where an unsplit `gateway/src/lib.rs` is heading.

## Messes we should explicitly not copy

- bashkit: `crates/bashkit/src/interpreter/mod.rs` at 12,874 lines - the entire execution engine in one file, contradicting the repo's own incremental-change principle; `crates/bashkit/src/builtins/rg/mod.rs` is a 528 KB single file; agent-tooling config (`.agents/`, `.claude/`, `.deepsec/`) and a stray `out file.txt` debris file are checked in.
- everruns: 4,000-plus-line leaf files despite the CI guards - `openresponses_protocol.rs` 5,708 lines, `sessions/service.rs` 5,304, `events.rs` 5,105, `capabilities/mod.rs` 5,009; plugin registration happens by linker side effect via forced `extern crate` linkage ([lib.rs:L13-L26](https://github.com/everruns/everruns/blob/e3d715542568dc682f004aac0d79fa1bd9c35917/crates/server/src/lib.rs#L13-L26)); a 64 KB `domains/common.rs` grab-bag sits beside 40+ tidy domain directories.
- yolop: `src/runtime/mod.rs` is a ~10,540-line god-module wiring every capability into `BuiltRuntime`; `src/tui/mod.rs` is 483 KB; `tests/integration.rs` is a 132 KB single file - the aggregation idiom of finding 3 taken too far.
- everruns-sdk: `rust/src/client.rs` holds the core client plus all 12 sub-clients in 1,795 lines; `specs/error-handling.md` specifies a 4-variant error enum while the implementation has 9 - the normative spec is stale against the code it governs; a placeholder-looking `DEFAULT_BASE_URL` ships in released code ([client.rs:L9](https://github.com/everruns/sdk/blob/46979f8801b666c8c6f2d41970e44e844079a688/rust/src/client.rs#L9)).

## Recommended execution order

1. Finding 2 - CI guards first: pin the current crate graph and ban new shim use before moving any code, so every later step is checked.
2. Finding 3 - test aggregation: move inline test modules into `tests/` binaries; the test suite is the invariant for everything after, so consolidate and enumerate it before the splits.
3. Finding 1 - facade plus protocol crate: split `gateway/src/lib.rs` handlers behind the facade; extract wire types into `promptforge-proto`.
4. Finding 4 - narrow projection: shrink the `promptforge-lua` seam to a versioned projection; delete the shims the guards now ban.
5. Finding 5 - decision comments and knowledge bundle: record the why at each new seam while they are fresh.
6. Finding 6 - execution budget and progress guard: first behavior change, layered on the cancellation substrate.
7. Finding 8 - SSE reconnection: hardens the workshop-gateway channel that long-running agents depend on.
8. Finding 9 - per-session worktrees: isolation primitive for parallel agents.
9. Finding 10 - offline LLM simulation: test substrate that findings 6-9 then use.
10. Finding 7 - sans-I/O turn planner: largest and last, adopted incrementally once budgets, worktrees, and simulation exist to test it.

## Refactor notes

Findings 2, 3, and 5 are pure structure and tooling - no behavior change. Findings 1 and 4 change the public surface but not runtime behavior if the old paths are kept as deprecated re-exports for one release - the finding-2 guards should ban *new* uses immediately and grandfather existing ones until deleted. Findings 6-10 add capabilities and change behavior; each lands behind its own tests. The test suite is the invariant: consolidate it (finding 3) before the splits, and never move tests and code in the same commit. Do-not-touch boundaries: the `Request`/`Answer` coroutine protocol and the `shared-sidecar` attach machinery are confirmed strengths - findings narrow and build on them but do not restructure them. Verify and commit per step; two consecutive failures on one step stops the run for a re-plan.

## Sources

- https://github.com/everruns/bashkit - HEAD `8e1a2e5ae06f3db1d55cb3e49e6d4bfd808f4b4a` - MIT - analyzed 2026-09-11 - rewinds: `AGENTS.md` pre-AI `e4bfd901bc996af679076cf17a36c0523c2b487c`, `testing.rs` pre-AI `b2a66ac931029db9311f91936f451528cbb4a72b`
- https://github.com/everruns/everruns - HEAD `e3d715542568dc682f004aac0d79fa1bd9c35917` - MIT - analyzed 2026-09-11 - rewinds: `turn.rs` pre-AI `a71eaf339bf192b53108eff0ed5e2c2b34602dc2`, facade `lib.rs` pre-AI `871bd56fa517b4cad01c619c4d1fa088653fe211`, `llmsim` pre-AI `66c20400b0bcd4e14cb6552bf477f1a21d437250`
- https://github.com/everruns/yolop - HEAD `a2b94a794827dce860b640b2948f75d8b27836a0` - MIT - analyzed 2026-09-11 - rewinds: `progress_guard.rs` pre-AI `8576858cfa505dde613cdd6fb31ec6fa773e701d`, `yolop-yep` pre-AI `c32e644beecbe34e251a8cec4a07f15ee4fc12cb`, `worktree.rs` pre-AI `bbac2b7421453927bb871b7273543ad6681bb7c0`, `tests/integration.rs` pre-AI `f1638c75726bb4f7aea1340d3937e630963d58c1`
- https://github.com/everruns/sdk - HEAD `46979f8801b666c8c6f2d41970e44e844079a688` - MIT - analyzed 2026-09-11 - rewinds: `sse.rs` and `client.rs` pre-AI `5ee763a9`
- Field survey replaced by an operator-supplied shortlist, 2026-09-11; subject profile produced 2026-09-11.

*2026-09-11 08:55 - kimi-k3*
