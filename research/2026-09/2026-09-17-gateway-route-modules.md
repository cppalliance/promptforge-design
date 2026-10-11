# Gateway App: How to Structure API Route Code That Grows

Report type: evaluation / review. It judges the PromptForge gateway app crate against 5 popular codebases sharing the Rust + axum HTTP API service technique, and prescribes idioms to adopt, in payoff order.

## Executive summary

The gateway's routing discipline is field-grade but its crate root is a junk drawer: every reference surveyed keeps handlers out of the crate root, and the gateway is the only one still editing a 4,371-line lib.rs to add an endpoint. The subject already matches the field on trust layering, boundary purity, and router composition; it loses on handler placement, test placement, and surface enumerability. The top finding - a thin crate root whose route table names handlers by module path - is exactly the decomposition already planned, and five independent references confirm it is the right shape.

### Key findings

1. **Make lib.rs a thin assembly seam whose route table names handlers by full module path** - confirmed by tensorzero, crates.io, svix-webhooks, openobserve, and clean-axum-demo. Every reference keeps the whole table in one handler-free file; none lets handlers live beside it. Confidence: high.
2. **Write down a handler-placement rule: route area decides the module** - crates.io, svix, openobserve, clean-axum-demo, and tensorzero all make handler location derivable from the route path. The gateway's stranded `admin_*` handlers are the gap. Confidence: high.
3. **Mirror the route surface 1:1 in test files over one shared fixture module** - crates.io, svix, and clean-axum-demo all do this; the gateway's inline tests are 60% of lib.rs and redefine the same fixtures per block. Confidence: high.
4. **Make the mounted surface enumerable and drift-guarded** - routes-as-data (tensorzero) or a generated OpenAPI spec pinned by snapshot/assertion tests (crates.io, svix, openobserve). The gateway's only full route list is a prose doc header that can drift. Confidence: high on the need, medium on mechanism choice.
5. **Register routes in all builds and gate the feature inside the handler** - openobserve's rule kills the `#[cfg]`-fragmented mounting that makes the gateway's surface unenumerable. Confidence: medium.
6. **Review-gate the route table file with CODEOWNERS** - tensorzero forces review friction on any change to the API surface. Confidence: low.

## Method

The subject crate was profiled first through nine lenses (module decomposition, state ownership, boundaries, errors, lifecycle, testing, comment policy, build, messes). The field was surveyed for popular Rust/axum HTTP API services and each candidate verified against its actual dependency manifest and source. Five references were dived in parallel at pinned commits, each idiom then examined for provenance - AI-marked commit history - with a pre-AI rewind comparison where markers appeared. Findings were synthesized by cross-reference convergence and mapped onto the subject's named deficits, and every citation was checked against the pinned clones (40 of 50 passed as written; 10 corrected, none dropped).

## Reference projects and provenance

| Reference | Popularity | Why chosen | License | Provenance of cited idioms |
|---|---|---|---|---|
| [tensorzero](https://github.com/tensorzero/tensorzero) | 11.7k stars | LLM gateway on axum 0.8; closest technique match | Apache-2.0 | 5 explicit AI marker (1 AI-originated; 3 held up or extended against pre-AI forms), 1 unknown |
| [crates.io](https://github.com/rust-lang/crates.io) | 3.7k stars | Production axum service; router separate from controllers | MIT OR Apache-2.0 | 9 strong human signal; zero AI-marked commits since 2022 |
| [svix-webhooks](https://github.com/svix/svix-webhooks) | 3.4k stars | Versioned per-resource endpoint modules on axum | MIT | 6 unknown (2022 code drop hides earlier history), 1 strong human signal |
| [openobserve](https://github.com/openobserve/openobserve) | 22k stars | Grown-codebase-scale axum handler tree, 535 routes | AGPL-3.0 | 3 explicit AI marker (2 held up or extended; 1 has no pre-AI form), 1 strong human signal |
| [clean-axum-demo](https://github.com/sukjaelee/clean_axum_demo) | 203 stars | Read-whole slot; per-domain router template | MIT | 7 strong human signal (single maintainer, zero AI markers) |

## Baseline: where the subject stands

The gateway app crate is ~100% Rust on axum, tokio, tower, and reqwest, delivered as one `promptforge-gateway` binary with additive cargo features and a headless `--no-default-features` build. Its routing seam is genuinely good: a single `build_router(state, bound) -> Router` testable in-process via tower, an admin surface isolated as a separate `Router` under one `route_layer(require_loopback)`, transport-pure wire types in `gateway-protocol` with table-driven error mapping, and feature crates that contribute merged routers. Its deficits are all about growth: a 4,371-line lib.rs holding the route table, `AppState`, ~15 handlers, and ~60% of its bulk in inline tests; no rule deciding where a new handler goes (`admin_config`/`admin_status` sit in lib.rs while sibling routes live in `config_write.rs`/`config_pending.rs`); a route table that names private same-file functions; `#[cfg]`-gated imperative mounting that makes the mounted surface unenumerable from code; and test fixtures redefined in nearly every inline test block despite a shared `test_support.rs`.

## Detailed findings, ranked by payoff

### Finding 1: Thin crate root; the route table is an index that names handlers by full module path

All five references keep the entire route table in one handler-free place and banish handlers to modules. openobserve centralizes all 535 mounts in one file, each naming its handler by full module path (`get(organization::org::org_summary)`) - [router/mod.rs:801-953](https://github.com/openobserve/openobserve/blob/b85030e7d909090ba1bd330c6d2b24c7369c704c/src/api/http/src/handler/http/router/mod.rs#L801-L953). crates.io's [src/router.rs:17-112](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/router.rs#L17-L112) is a flat list of handler function paths and its [src/lib.rs:1-66](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/lib.rs#L1-L66) is 66 lines where `build_handler` (lines 61-65) is the only assembly seam. svix's [v1/mod.rs:17-26](https://github.com/svix/svix-webhooks/blob/c608e3717cff250527fd82b35f4b6ef36f3f26b7/server/svix-server/src/v1/mod.rs#L17-L26) is a flat `.merge(endpoints::<resource>::router())` list whose crate root names no handlers. tensorzero quarantines handler-free tables under [crates/gateway/src/routes/](https://github.com/tensorzero/tensorzero/blob/62eb8f63e8ec62018d70420dbf1a8c5d1c026315/crates/gateway/src/routes/external.rs#L1-L5), and clean-axum-demo mounts per-domain factories with `.nest("/user", user_routes())` at [src/app.rs:81-84](https://github.com/sukjaelee/clean_axum_demo/blob/428cec16821a2ef8334636ced57db341dd7448a4/src/app.rs#L81-L84).

This replaces the gateway's `build_router` (lib.rs:486-602), which names private same-file handlers and so cannot split or move without moving them. The fix is the planned decomposition itself: extract handlers to feature modules, keep the route table whole in lib.rs, and mount by module path (`get(models::list_models)`). Confidence: high - five independent references converge on the same shape.

### Finding 2: Written handler-placement rule: route area decides the module

Every reference makes handler location derivable from the route path, and three of them write the rule down. crates.io uses one controllers directory per resource with one file per operation group and shared extractors in the domain mod.rs - [src/controllers/krate/follow.rs](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/controllers/krate/follow.rs) beside [src/controllers/krate.rs](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/controllers/krate.rs). svix promotes sub-surfaces to submodules with the router at the resource root naming `crud::create_endpoint` - [endpoints/endpoint/mod.rs:893-960](https://github.com/svix/svix-webhooks/blob/c608e3717cff250527fd82b35f4b6ef36f3f26b7/server/svix-server/src/v1/endpoints/endpoint/mod.rs#L893-L960). openobserve states the placement and aggregation rule in [src/api/http/README.md](https://github.com/openobserve/openobserve/blob/b85030e7d909090ba1bd330c6d2b24c7369c704c/src/api/http/README.md). clean-axum-demo fixes a per-domain directory template with a facade re-exporting only the routes function - [src/domains/user.rs:1-22](https://github.com/sukjaelee/clean_axum_demo/blob/428cec16821a2ef8334636ced57db341dd7448a4/src/domains/user.rs#L1-L22). tensorzero keeps handlers in a core crate under `endpoints/<area>`, one module per API area.

This replaces the gateway's ambiguity where `admin_*` handlers sit in lib.rs while sibling routes live in `config_write.rs`/`config_pending.rs`/`config_apply.rs`. The fix: state the rule once in the crate docs - a route area gets a module; at 3+ files it earns a directory - and let the planned `admin/` tree be its first application. Confidence: high - the rule is cheap, written down by three references, and directly names the subject's deficit.

### Finding 3: Tests mirror the route surface 1:1 in their own files over one shared fixture module

crates.io roots one integration crate at `src/tests/mod.rs` with a tree mirroring the route surface ([src/tests/routes/crates/following.rs](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/tests/routes/crates/following.rs)) and shared fixtures in `src/tests/util/` plus a builders crate. svix keeps DTO-validation tests inline but puts all HTTP behavior in `tests/it/e2e_<resource>.rs` mirroring module names 1:1 over one shared `TestClient` - [tests/it/utils/mod.rs:311-350](https://github.com/svix/svix-webhooks/blob/c608e3717cff250527fd82b35f4b6ef36f3f26b7/server/svix-server/tests/it/utils/mod.rs#L311-L350) and [tests/it/main.rs:3-17](https://github.com/svix/svix-webhooks/blob/c608e3717cff250527fd82b35f4b6ef36f3f26b7/server/svix-server/tests/it/main.rs#L3-L17). clean-axum-demo uses surface-per-file `tests/test_<feature>_routes.rs` over one shared helper module, driving the real router via tower oneshot - [tests/test_helpers.rs:66-72](https://github.com/sukjaelee/clean_axum_demo/blob/428cec16821a2ef8334636ced57db341dd7448a4/tests/test_helpers.rs#L66-L72).

This replaces the gateway's inline tests (~60% of lib.rs) and the per-block redefinition of `state()`, `wait_until()`, `fake_chat_backend()`, and `parking_executor()`. The subject's kebab `-tests.rs` sibling convention is the compatible local form of the same rule; the steal is naming test siblings after the route surface 1:1 and consolidating the four duplicated fixtures into `test_support.rs`. Confidence: high - three references converge and the subject already has the fixture module to consolidate into.

### Finding 4: Make the mounted surface enumerable and drift-guarded

Four references make the API surface machine-checkable. tensorzero keeps route groups as data - a `Vec<(&str, MethodRouter)>` folded into a `Router`, with the tracing layer's route-name list derived from the same vector so they cannot drift - [routes/external.rs:24-53](https://github.com/tensorzero/tensorzero/blob/62eb8f63e8ec62018d70420dbf1a8c5d1c026315/crates/gateway/src/routes/external.rs#L24-L53) and [endpoints/mod.rs:39-44](https://github.com/tensorzero/tensorzero/blob/62eb8f63e8ec62018d70420dbf1a8c5d1c026315/crates/tensorzero-core/src/endpoints/mod.rs#L39-L44). crates.io generates OpenAPI from handler-carried `#[utoipa::path]` attributes ([controllers/krate/follow.rs:34-50](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/controllers/krate/follow.rs#L34-L50)) and insta-snapshots the entire spec so any endpoint add/move/reshape fails CI until accepted - [src/tests/openapi.rs:5-19](https://github.com/rust-lang/crates.io/blob/b5adf6a201abb45bd473ba96f133ad75a1cc1b4b/src/tests/openapi.rs#L5-L19). svix generates the spec from the route table via aide and seals it after mounting - [src/lib.rs:196-214](https://github.com/svix/svix-webhooks/blob/c608e3717cff250527fd82b35f4b6ef36f3f26b7/server/svix-server/src/lib.rs#L196-L214). openobserve builds the doc in tests and asserts its properties - [router/openapi.rs:730-772](https://github.com/openobserve/openobserve/blob/b85030e7d909090ba1bd330c6d2b24c7369c704c/src/api/http/src/handler/http/router/openapi.rs#L730-L772).

This replaces the gateway's prose doc header - the only full route list - and the `#[cfg]`-gated imperative mounting at lib.rs:506-592. The cheap form is tensorzero's: build the route table as data and derive any secondary list from the same value. The full form is a generated spec with a snapshot test; it pays more and costs more. Confidence: high that the surface must become enumerable, medium on which mechanism - the data form fits the subject's no-new-dependencies posture, the spec form fits if OpenAPI is already on the roadmap.

### Finding 5: Register routes in all builds; gate the feature inside the handler

openobserve registers routes in all builds and has the handler return 403 when the feature is unlicensed, so "not licensed" differs from "no such endpoint" and the table stays free of `#[cfg]` fragments - [router/mod.rs:886-899](https://github.com/openobserve/openobserve/blob/b85030e7d909090ba1bd330c6d2b24c7369c704c/src/api/http/src/handler/http/router/mod.rs#L886-L899). The same house shows the cost of the alternative: `service_routes()` is one ~1,150-line function with 18 interleaved `#[cfg(feature = "enterprise")]` blocks - [router/mod.rs:775-1940](https://github.com/openobserve/openobserve/blob/b85030e7d909090ba1bd330c6d2b24c7369c704c/src/api/http/src/handler/http/router/mod.rs#L775-L1940) - the gateway's imperative-fragmentation disease at 10x scale.

This replaces the gateway's `#[cfg]`-gated `let router = router.route(...)` blocks at lib.rs:506-592. The fix: mount unconditionally, and let a thin shim handler return 404/501 when the feature is compiled out. Confidence: medium - single-source, but the counter-evidence comes from the same reference's own mess.

### Finding 6: Review-gate the route table file

tensorzero's handler-free route tables are gated by CODEOWNERS review - [routes/external.rs:1-5](https://github.com/tensorzero/tensorzero/blob/62eb8f63e8ec62018d70420dbf1a8c5d1c026315/crates/gateway/src/routes/external.rs#L1-L5) plus `.github/CODEOWNERS` - so every change to the API surface gets forced review friction. For the gateway, adding the route table file (or its future `routes.rs`) to CODEOWNERS makes the surface change-visible in every PR. Confidence: low - single-source, and the mechanism is process rather than code.

## Provenance

tensorzero's cited routing idioms carry explicit AI markers, and the rewinds are reassuring about the specific mechanisms. The external route table is AI-originated (its introducing commit carries Copilot trailers) and has no pre-AI form. The internal table and the `build_api_routes` plus OTel route-name list were already present at the pre-AI commit (`gateway/src/routes/internal.rs` and `gateway/src/routes/mod.rs` at 6c1fec7a) and are the same mechanism at HEAD, only grown. The `RouteHandlers` route-groups-as-data idiom was AI-introduced in late 2025. The root-state quarantine was added by unmarked commits even though its file carries AI markers elsewhere, and the black-box test scaffolding predates AI touches and held up. openobserve's axum route-table-as-index has no pre-AI form - the pre-AI file is a 693-line actix router - and its OpenAPI assembly predates AI marks while the cited spec-assertion tests were added after. crates.io and clean-axum-demo show zero AI markers; svix's server tree entered its repo as a single 2022 code drop, so its idioms tag `unknown` despite clean marker scans. A sample this small supports no conclusion about AI-authored code in general.

## Where the subject already matches or beats the references

- Trust grouping by router composition - one `route_layer(require_loopback)` over a merged admin router - matches tensorzero's external/internal split and clean-axum-demo's layered nest groups; svix's typed permission extractors are an alternative, not a superior.
- A single router seam testable in-process via tower matches clean-axum-demo's oneshot tests on the real router and openobserve's composition-root ordering tests.
- Transport-pure boundary types in `gateway-protocol` with table-driven error mapping match crates.io's boundary-extractor discipline.
- The surface-organized integration suite with ephemeral listeners, rendezvous shutdown, and no sleeps beats clean-axum-demo, whose tests need a live Postgres with credentialed `.env` files checked into git.

## Messes we should explicitly not copy

- tensorzero: `endpoints/inference.rs` at 3,591 lines - module-per-area with no size bound recreates the monolith one level down; `crates/gateway/src/main.rs` at 1,148 lines; `routes/internal.rs` is a single 60-route chain with drifting indentation and a feature-flagged tail.
- crates.io: `controllers/krate/publish.rs` at 1,130 lines; test files that dwarf the code under test (`tests/routes/crates/list.rs` at 1,479 lines); dual registration styles - utoipa `routes!()` plus raw `.route()` after `split_for_parts()` - so the full surface requires reading both blocks.
- svix-webhooks: `src/v1/endpoints/attempt.rs` at 1,199 lines and `endpoints/endpoint/mod.rs` at 1,114 lines mixing DTOs, handlers, router, and tests; a hardcoded checked-in `openapi.json` served while the generated spec sits unused with a TODO; a 955-line `v1/utils/mod.rs` shared-utils monolith.
- openobserve: the ~1,150-line `service_routes()` with 18 interleaved cfg blocks; handler god-files of 168-190 KB (`oncall/mod.rs`, `alerts/mod.rs`); an OpenAPI `paths()` list that manually duplicates the route table.
- clean-axum-demo: an identical ~14-line OpenAPI security-scheme impl copy-pasted into all four domain routes files; route paths declared twice (utoipa attributes vs route table strings) with silent drift risk; credentialed `.env` files in git.

## Recommended execution order

1. Findings 1 + 2 as one step: extract handlers into feature modules under a written placement rule, keep the route table whole in lib.rs naming module paths. This is the existing decomposition plan, confirmed.
2. Finding 3: move tests to surface-mirroring kebab siblings and consolidate the four duplicated fixtures into `test_support.rs`. Same files as step 1's extractions, sequenced after each module lands.
3. Finding 5: mount unconditionally, gate features inside shim handlers. Small, independent, removes the cfg fragmentation.
4. Finding 4: convert the route table to data (or adopt a spec snapshot if OpenAPI is planned) so the surface is enumerable in diffs.
5. Finding 6: add the route table file to CODEOWNERS.

## Refactor notes

Findings 1, 2, 3, and 6 are pure structure - code motion and process. Finding 5 changes behavior at the edges: a feature-compiled-out endpoint shifts from connection-level absence to a 404/501 response, so clients and the headless-gate CI job must be checked before it lands. Finding 4 is additive (data reshaping plus tests) but touches the same route table as step 1, so it must follow it. The test suite is the invariant: test counts before and after each extraction must match, and tests move last within each module's extraction. Do not touch `runner.rs`, `commands.rs`, `dialect.rs`, or `config_apply.rs` - they are over 500 lines but are not route code and are out of scope. Verify and commit per step: `cargo test -p gateway`, `cargo check -p gateway --no-default-features`, clippy, fmt, doc. Stop condition: two consecutive failures on one step stops the run for a re-plan.

## Sources

- https://github.com/tensorzero/tensorzero - HEAD 62eb8f63e8ec62018d70420dbf1a8c5d1c026315 - Apache-2.0 - analyzed 2026-09-17 - PRE_AI 6c1fec7aecf17bdf9a7540fff7b4c74011bbd3cc (routes), 1b3cbadb8530596a4c923bdb3217f670f753530e (endpoints/mod.rs), 075971eff4084dab5541f2af0145230493af4eb5 (utils/gateway.rs), 65c7c395b889cc03af6b870c06a36fb53a62ebee (tests/common)
- https://github.com/rust-lang/crates.io - HEAD b5adf6a201abb45bd473ba96f133ad75a1cc1b4b - MIT OR Apache-2.0 - analyzed 2026-09-17
- https://github.com/svix/svix-webhooks - HEAD c608e3717cff250527fd82b35f4b6ef36f3f26b7 - MIT - analyzed 2026-09-17
- https://github.com/openobserve/openobserve - HEAD b85030e7d909090ba1bd330c6d2b24c7369c704c - AGPL-3.0 - analyzed 2026-09-17 - PRE_AI b9483617694fdfab09c5e39837c1c3dfc79f1b3f (management module tree; pre-AI form at src/handler/http/request/alerts/mod.rs), ca1ca8e169c95892e4680800d7cc836e4187bfa9 (router/mod.rs), 0ebaf21f33e8bfdd3b8ab0a7e9eba62bb5ec32b0 (openapi.rs)
- https://github.com/sukjaelee/clean_axum_demo - HEAD 428cec16821a2ef8334636ced57db341dd7448a4 - MIT - analyzed 2026-09-17
- Field survey and subject profile produced 2026-09-17.

*2026-09-17 09:50 - kimi-k3*
