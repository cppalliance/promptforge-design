# Packet Section VIII - The Core Crate (principles 40-46)

Facts only. Sources: purpose-cluster-8.md (motivations), grouped-draft.md (full records with rejected alternatives and endorsements).

## Principle 40 - Single concern per file, minimal public API, tightened continuously

- Rule: Keep each file to a single concern and the public API as small as it can be, tightening it as you go by considering how each function interacts with the others.
- Purpose facts:
  - API growth drives quadratic growth in dependencies between functions, so a smaller API is always better than a larger one.
  - Tightening the API on every commit keeps the total debt workload linear, even though each commit costs more.
  - API design considers how each function interacts with the others in pairs, in triples, and all together - not each function in isolation.
  - One-off cleanup efforts done by hand get generalized into a reusable prompt that runs against recent commits, so debt is paid as he goes instead of in one large effort at the end.
- Rejected alternative (grouped draft): deferring cleanup to a later dedicated phase or one large effort at the end; evaluating each API function in isolation. Stated cost: facing a pile of review findings all at once.
- Concrete incident: The author vibe-coded the repo for days without doing debt refactors along the way and ended up facing a large pile of review findings all at once. This is the "learned the hard way" episode behind the principle.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Derives from the grouped-draft record "Refactoring happens continuously at every step..." (Continuous debt payment and evidence group). Citations: 2026-08-10-0856-repo-review-top-to-bottom.md [p30]-[p32], [p36], [p52], [p53]; 2026-07-31-1516-agentic-ide-research.md [p49], [p57].

## Principle 41 - One build configuration, no feature flags

- Rule: One build configuration. No feature flags, ever - there is only one version of the binary, and if size becomes a problem the crate gets split later.
- Purpose facts:
  - When conditional compilation was proposed, he refused: he never wants "features," there is only one version of the binary.
  - The escape hatch for binary size is splitting the crate later, not gating code behind flags.
- Rejected alternative (grouped draft): conditional compilation via feature gates. Stated cost: none recorded beyond the refusal itself; the record gives an explicit reason only for this leg.
- Concrete incident: Feature flags were proposed during the Brave web search tools work and rejected on the spot.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Derives from the feature-flag leg of the grouped-draft record "Library code propagates errors and never unwraps; new dependencies are not introduced...; there are no cargo feature flags and exactly one build configuration." The no-unwrap and no-new-deps legs of that record appear only as standing binding rules restated in a plan prompt with no stated motivation, and did not carry into this principle. Citations: 2026-07-29-0937-brave-web-search-tools.md [p16], [p19]; 2026-08-14-1612-file-backed-store-execution.md [p3].

## Principle 42 - A crate fits in one coding-LLM context window

- Rule: A crate stays small enough that a coding LLM can hold the whole crate in a single context window.
- Purpose facts:
  - The implementation work is done by coding models; crate size is bounded by what the LLM can hold at once.
  - A crate that fits in one context can be reviewed, refactored, and reasoned about as a unit.
  - Stated directly during the MCP client work: a separate crate means a coding LLM only has to consider a smaller amount of code and is more likely to fit the whole crate in a single context window.
- Rejected alternative (grouped draft): none recorded.
- Concrete incident: Arose when deciding whether to embed the MCP client in the tool-picker crate; the argument for a separate crate was the context-window bound.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Stands alone. Purpose notes record that this principle and principle 41 both serve the LLM-driven workflow, but the mechanisms differ and no merge was recommended. Citations: 2026-08-02-1034-mcp-client-harness.md [p78], [p79]; 2026-08-02-1419-mcp-client-continued.md [p79].

## Principle 43 - Every feature ships with its test; external services get real manual integration tests

- Rule: Every markdown feature of the prompt format ships with its test, and every feature that calls an external service ships with a manual integration test that exercises the real service and is actually run.
- Purpose facts:
  - Format features never ship unverified: while planning the executor he instructed that every markdown feature must come with its test.
  - For external services he wants a manual test that exercises the real service, and he wants to see it run and work.
  - A mock proves the mock, not the service.
- Rejected alternative (grouped draft): mock-only tests. Stated cost: a mock proves nothing about the real service.
- Concrete incident: The agent delivered the Brave web search tool without any test that actually calls Brave, and he pushed back, demanding a manual test against the real service, actually run.
- Endorsement: n/a (user-stated; user-corrective).
- Merge/derivation notes: Single grouped-draft record "Every markdown feature of the prompt format ships with a corresponding test..." (Continuous debt payment and evidence group). Citations: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]; 2026-08-02-1134-mcp-client-large-part3.md [p173]; 2026-07-29-0937-brave-web-search-tools.md [p26], [p27].

## Principle 44 - The executor is a dumb function call; the gateway owns everything model-specific

- Rule: The executor holds no vendor credentials, no endpoints, no provider knowledge, no global state; everything model-specific - keys, routing, tool-call translation, model download and caching - concentrates in the gateway. The executor never knows whether a model is local or remote.
- Purpose facts:
  - He works through an AI-driven workflow with many layers of software between him and the running system, and found configuration a pain; he wanted one central point of configuration, and the gateway is it.
  - Only one machine can hold the vendor key, because global rate limits cannot be enforced from many key-holding processes (OpenAI and vLLM do not queue well), so the key had to move out of the executor into the gateway.
  - One central point of configuration is what makes the system operable.
  - He asked directly which layer should handle translating to and from each model's tool-call format, and confirmed the gateway, keeping the executor free of per-model differences.
  - Downloading and caching models is the gateway's job; callers and tests supply only configuration naming the source URL and pin.
- Rejected alternatives (grouped draft, both merged records): the executor reading the vendor API key directly; an executor-level base_url setting; engine-owned global state shared across runs; the executor handling per-model tool-call translation; core tests standing up llama-server and fetching GGUF weights themselves.
- Concrete incidents and author-verbatim phrases:
  - His summary, verbatim: "the executor is just a function call" - it talks only to the gateway and never knows whether a model is local or remote.
  - When wiring local inference, he rejected core tests standing up llama-server and fetching GGUF weights themselves.
- Endorsement: the executor-as-function-call record is marked ai-proposed legs unaddressed; the tool-call-translation record is user-stated/user-corrective, endorsement n/a.
- Merge/derivation notes: Two grouped-draft records merged into this principle, per the purpose notes' merge suggestion (records 5 and 6 share one purpose): "The executor holds no vendor credentials, endpoints, or provider knowledge of its own..." and "Model-specific translation to and from tool calls is the gateway's responsibility...; model download and caching live in the gateway, never in the core or the test harness." Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: gateway v0]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p185]-[p187], [p189], [p211], [p215]; 2026-08-08-1223-gateway-local-inference.md [p16], [p18], [p41], [p42]; 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md].

## Principle 45 - No shared schemas; the gateway never depends on core

- Rule: Components do not share schema definitions, and the gateway never depends on core. Each side of a boundary owns its own schemas.
- Purpose facts:
  - Sharing schemas is unnecessary coupling that pins two components to each other's internals.
  - The gateway-not-depending-on-core leg was his own gut call from the first gateway discussion.
- Rejected alternative (grouped draft): a shared schema package used by both executor and gateway; the gateway linking against core.
- Concrete incidents and author-verbatim phrases:
  - When schema sharing came up he initially asked why not share them - verbatim: "Isn't it JSON?" - and once it was explained he agreed, verbatim: "Of course they should not share them. that's unnecessary coupling."
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Single grouped-draft record "Components do not share schema definitions... the gateway must not depend on core." The purpose notes mark it adjacent to principle 44's records (same core<->gateway seam) but with a distinct purpose - decoupling, not vendor-knowledge placement - so it stays separate. Citations: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190]-[p192]; 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]; 2026-07-29-0937-brave-web-search-tools.md [p11].

## Principle 46 - Integration tests require an already-running gateway

- Rule: Integration tests require an already-running, already-configured gateway - a test never launches the gateway itself. A small local model stays runnable without the gateway, so integration tests can exercise real inference with a simple setup.
- Purpose facts:
  - A test should require that the gateway already exists and already has its configuration.
  - Models are reached through the gateway rather than through bespoke direct wiring in the test harness; direct wiring is duplicated effort when the gateway is needed anyway.
  - A small (0.6B) model kept runnable without the gateway is a simple setup that lets integration tests exercise real inference and expands the testing surface without the bulk of spawning the gateway.
- Rejected alternative (grouped draft): tests spawning their own gateway instance; wiring a local model directly into core-tests, bypassing the gateway.
- Concrete incidents and author-verbatim phrases:
  - The tests were launching the gateway themselves and it was going wrong - stuck, failing - and he called it, verbatim, "all wrong."
  - Earlier he had regretted wiring the 9B model directly into core-tests when the gateway was needed anyway for web search.
- Endorsement: n/a (user-corrective; user-stated).
- Merge/derivation notes: Single grouped-draft record "Integration tests require an already-running, already-configured gateway..." The purpose notes observe that its second leg (tests supply only config, never wire models directly) is the test-side consequence of principle 44's model-download record, and its first leg (tests never launch the gateway) stands as the testing corollary. Citations: 2026-08-14-1613-promptforge-core-largest-part2.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part3.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part2.md [p140].

## Stanza facts - Section VIII as a whole

- What the section covers: how the core crate itself is built - file and API size, build configuration, crate size, test discipline, and the core<->gateway boundary (credentials, translation, schemas, test setup).
- Why the layer exists: the people writing this code are mostly models, and the structure has to fit the worker.
- Failure modes it prevents:
  - Quadratic API-dependency debt surfacing as one large pile of review findings (40).
  - A feature-flag build matrix and multiple versions of the binary (41).
  - Crates too large for a coding LLM to review, refactor, or reason about as a unit (42).
  - Format features shipping unverified and external-service features proven only against mocks (43).
  - Vendor credentials, endpoints, provider knowledge, and global state leaking into the executor; unenforceable global rate limits; scattered configuration (44).
  - Two components pinned to each other's internals through shared schemas or a gateway-to-core dependency (45).
  - Flaky self-launching test gateways and bespoke model wiring duplicated in the test harness (46).
- Unifying principle, one sentence: keep every unit small enough to hold in one head.
