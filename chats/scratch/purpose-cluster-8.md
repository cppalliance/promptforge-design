# Cluster 8 purposes - Core crate structure and boundaries

## 1. "Refactoring happens continuously at every step..."

The author vibe-coded the repo for days without doing debt refactors along the way and ended up facing a large pile of review findings all at once. His stated reasoning: public API growth causes quadratic growth in dependency between functions, so tightening the API on every commit keeps the total debt workload linear even though each commit costs more. He also wanted the one-off cleanup he was doing by hand generalized into a reusable prompt that runs against recent commits, so the debt gets paid as he goes instead of in one large effort at the end.

Citations used: 2026-08-10-0856-repo-review-top-to-bottom.md [p30]-[p32], [p36], [p52], [p53]; 2026-07-31-1516-agentic-ide-research.md [p57]

## 2. "Every markdown feature of the prompt format ships with a corresponding test..."

Two pains. First, while planning the executor he instructed that every markdown feature must come with its test, so format features never ship unverified. Second, the agent delivered the Brave web search tool without any test that actually calls Brave, and he pushed back: he wants a manual test that exercises the real service, and he wants to see it run and work. A mock proves nothing about the real service.

Citations used: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]; 2026-08-02-1134-mcp-client-large-part3.md [p173]; 2026-07-29-0937-brave-web-search-tools.md [p26], [p27]

## 3. "Library code propagates errors and never unwraps; new dependencies are not introduced..."

The cited units give an explicit reason only for the feature-flag leg: when conditional compilation was proposed, he refused, saying he never wants "features," there is only one version of the binary, and if binary size becomes a problem the crate gets split later. The no-unwrap and no-new-deps legs appear in the cited material only as standing binding rules restated in a plan prompt, with no stated motivation. No purpose found for those two legs in the record.

Citations used: 2026-07-29-0937-brave-web-search-tools.md [p16], [p19]; 2026-08-14-1612-file-backed-store-execution.md [p3]

## 4. "Crates are kept small enough that a coding LLM can hold an entire crate..."

Stated directly: when deciding whether to embed the MCP client in the tool-picker crate, the argument for a separate crate was that a coding LLM only has to consider a smaller amount of code and is more likely to fit the whole crate in a single context window. His workflow has coding LLMs doing the implementation, so crate size is bounded by what the LLM can hold at once.

Citations used: 2026-08-02-1034-mcp-client-harness.md [p78], [p79]; 2026-08-02-1419-mcp-client-continued.md [p79]

## 5. "The executor holds no vendor credentials, endpoints, or provider knowledge..."

He works through an AI-driven workflow with many layers of software between him and the running system, and found configuration a pain; he wanted one central point of configuration, and the gateway is it. Only one machine can hold the vendor key, because global rate limits cannot be enforced otherwise (OpenAI and vLLM do not queue well), so the key had to move out of the executor into the gateway. His summary: "the executor is just a function call" - it talks only to the gateway and never knows whether a model is local or remote.

Citations used: 2026-07-30-1046-compaction-algorithm-large-part3.md [p189], [p211], [p215]; 2026-08-08-1223-gateway-local-inference.md [p16], [p18]; 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: gateway v0]

## 6. "Model-specific translation to and from tool calls is the gateway's responsibility..."

He asked directly which layer should handle translating to and from each model's tool-call format, and the answer he confirmed was the gateway, keeping the executor free of per-model differences. Later, when wiring local inference, he rejected core tests standing up llama-server and fetching GGUF weights themselves: downloading and caching models is the gateway's job, and callers and tests should supply only configuration naming the source URL and pin.

Citations used: 2026-07-30-1046-compaction-algorithm-large-part3.md [p185]-[p187]; 2026-08-08-1223-gateway-local-inference.md [p41], [p42]

## 7. "Components do not share schema definitions... the gateway must not depend on core."

When schema sharing came up he initially asked why not share them ("Isn't it JSON?"), and once it was explained he agreed: "Of course they should not share them. that's unnecessary coupling." The gateway-not-depending-on-core leg was his own gut call from the first gateway discussion. The purpose is to keep the two components from being pinned to each other's internals.

Citations used: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190]-[p192]; 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]; 2026-07-29-0937-brave-web-search-tools.md [p11]

## 8. "Integration tests require an already-running, already-configured gateway..."

The tests were launching the gateway themselves and it was going wrong (stuck, failing), and he called it "all wrong": a test should require that the gateway already exists and already has its configuration. Earlier he had also regretted wiring the 9B model directly into core-tests when the gateway was needed anyway for web search - bespoke direct wiring in the harness was duplicated effort. At the same time he wanted a small 0.6B model kept runnable without the gateway, because that is a simple setup that lets integration tests exercise real inference and expands the testing surface without the bulk of spawning the gateway.

Citations used: 2026-08-14-1613-promptforge-core-largest-part2.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part3.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part2.md [p140]

## Merge suggestions

- Records 5 and 6 share one purpose: the executor stays a dumb, vendor-neutral function call and everything model-specific (credentials, endpoints, tool-call translation, model download and caching) concentrates in the gateway. They can merge into one principle.
- Record 7 is adjacent to 5/6 (same core<->gateway seam) but its purpose is distinct: it is about not coupling the two components through shared schemas, not about where vendor knowledge lives. Keep separate, or merge as a second leg of a broader "the gateway and core stay decoupled" principle.
- Record 8's second leg (tests supply only config, never wire models directly) is the test-side consequence of record 6's purpose; the two could merge, with record 8's first leg (tests never launch the gateway) standing as the testing corollary.
- Records 3 and 4 both serve the LLM-driven workflow (one build configuration, crates small enough to fit in a context window) but the mechanisms differ; no merge recommended.
