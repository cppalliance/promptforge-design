---
produced: 2026-08-19
title: PromptForge design principles mined from architect-vibe-planning part 4 (semantic blur, sharpen instrument, dataset gates)
---

# 2026-07-28-0207-architect-vibe-planning-part4.md

```yaml
- statement: An agent handed a bounded research task plans the work, forms hypotheses, runs the experiments, and returns clean results without checking in.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p175]
  rejected-alternative: none
  endorsement: n/a

- statement: A plan must be standalone: a fresh context can load it and resume the work with no prior state.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p176]
  rejected-alternative: none
  endorsement: n/a

- statement: An experiment log is append-only; each experiment records hypothesis, method, results, finding, and commit hash, with a git commit at every checkpoint, so the log is the reload point for a fresh context.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p176]
  rejected-alternative: none
  endorsement: n/a

- statement: Build training pairs by degrading a known-sharp target, never by sharpening a raw bloated input; raw bloat carries off-topic content that would teach the model relevance judgments.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p197]
  rejected-alternative: (raw bloated plan, sharpened plan) pairs
  endorsement: n/a

- statement: Blur is produced by the model's natural resampling; never steer the model toward bloat.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p198]
  rejected-alternative: steering the model into bloating
  endorsement: n/a

- statement: Crisp instructions survive blur because a reword converges back to execution semantics; descriptive prose drifts because its language is interpretive.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p200]
  rejected-alternative: none
  endorsement: n/a

- statement: Attach the rationale to every rule; the model generalizes from the reason, while a bare rule is pattern-matched and leaves the model hallucinating when the input does not perfectly match.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p204], [p214]
  rejected-alternative: reasonless rules, and the "escape hatch" framing in place of a rationale
  endorsement: n/a

- statement: Each concept is referred to by one name, not more.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p205]
  rejected-alternative: the ambiguous phrasing "One term names each concept"
  endorsement: n/a

- statement: A sharpening instrument aligns the model generally; it does not prescribe task-specific diagnostic algorithms.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p216]
  rejected-alternative: including the analytical-framework cluster in the sharpener
  endorsement: n/a

- statement: Datasets built from different sources are kept distinct from each other, each with its own experiment log.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p188]
  rejected-alternative: none
  endorsement: n/a
```
```yaml
- statement: The plan is the source of truth; a design that changes is regenerated from an updated plan, never patched in place.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: patching the generated document in place
  endorsement: affirmed

- statement: The non-expansion guarantee is enforced mechanically outside the model; the guardrail's worst case is returning the input verbatim.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: trusting the model to enforce its own length limit
  endorsement: affirmed

- statement: A compression pair is kept only when no model would behave differently following the compressed text instead of the original (execution-equivalence).
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: A quality gate is validated with negative controls; a gate that cannot fail is worthless, the same trap as a test that cannot fail.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: The meaning gate is directional, blurred input to sharp target, because a specific dropped by the blur would otherwise train the compressor to hallucinate.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: A compressor only cuts; it never adds a specific that is absent from the source.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: bundling add-rigor rules (quantify every quantity, define the empty case) into a compressor
  endorsement: affirmed

- statement: Blur is irreversible from within the regeneration chain; the training target must be the true pre-blur original, never a re-sharpened blur.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: re-sharpening a blurred text to recover the original
  endorsement: affirmed

- statement: A blurred document is fixed by hand with targeted, non-regenerative edits; regeneration is the blur.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p223]
  rejected-alternative: fixing blur by regenerating or rebuilding the document
  endorsement: n/a

- statement: Ship the sharp-enough and stop regenerating; an ambiguity audit has no fixed point, and chasing perfection is the blur trap applied to process.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: one more tightening pass
  endorsement: affirmed

- statement: A gate that catches nothing beyond another gate is redundant cost; keep the one gate that discriminates.
  scope: global
  source: ai-proposed
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [design documents section]
  rejected-alternative: running both Gate 1 and Gate 2
  endorsement: affirmed
```

## Not converted

- Small models carry a narrow vocabulary; vocabulary lives in pretraining, not in the fine-tune set. [p184]
- Before trusting the model's judgment, the user asks it to rate its own confidence. [p187]
- Early hypothesis that blur is near-lossless; measurement disproved it, a single pass drops or alters a specific in 43-54% of cases. [p199]
- The user interrogates every phrase of the rulebook; no wording survives unexamined. [p208], [p209], [p211], [p219]
- The endeavor keeps living out its own thesis: every tightening pass regenerates the disease it studies. [p220], [p221]
- A report about bloat that is itself bloated fails on contact. [plans section]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from dokuman each-crate session (execution model, Lua sandbox, fanout, SSRF boundary)
---

# 2026-08-12-1534-dokuman-each-crate

```yaml
- statement: Execution is a free function over caller-owned resources; the engine holds no global state.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: engine-owned global state shared across runs
  endorsement: unaddressed

- statement: The H1 section resolves first, then H2 sections execute top to bottom.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: A prompt is a single Markdown file: YAML frontmatter for metadata, embedded Lua for logic, and prose blocks for model instructions.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The embedded Lua environment is a sandboxed VM with memory and instruction limits.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: an unsandboxed scripting environment with full host access
  endorsement: unaddressed

- statement: Fanout maps a worker section over a list section, running the arms in parallel with isolated state per arm.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: fanout arms that share mutable state
  endorsement: unaddressed

- statement: The result of a run is a string.
  scope: core
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md]
  rejected-alternative: none
  endorsement: unaddressed

- statement: The web fetch tool enforces an SSRF boundary on the pages it retrieves.
  scope: boundary: webfetch<->web
  source: ai-proposed
  citation: 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md, CHANGELOG.md]
  rejected-alternative: unrestricted outbound fetching
  endorsement: unaddressed
```

## Not converted

- Assembling the combined user guide should be a program that does one thing, not a prompt. (Excluded as a technology choice for repo tooling, not a language or engine behavior.) [p5]
- Stating a fact is not a request: the user stopped the agent for making unrequested changes after being told only that cppa uses Jekyll. [p23], [p24], [p25]
- Generated documentation belongs in the crate it documents, overriding default output routing. [p1], [p2]
- Git history should be kept clean: rewrite out a revert commit and the commit it reverts rather than layering corrections. [p29], [p30]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from gateway local-inference session (gateway centrality, profiles, devices, queuing, no-defaults, sys.model)
---

# 2026-08-08-1223-gateway-local-inference

```yaml
- statement: All PromptForge inference goes through the gateway, no matter what; the gateway is the single, central point of configuration for models, keys, and endpoints.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p16]
  rejected-alternative: clients talking directly to Ollama, llama.cpp, OpenAI, or Anthropic
  endorsement: n/a

- statement: The executor never knows whether a model is local or remote; it just talks to the gateway.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p16], [p18]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway is configured from one centralized file that lists every model, and a model entry may carry the URL where its weights are downloaded on demand.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p16]
  rejected-alternative: none
  endorsement: n/a

- statement: Model download and caching live in the gateway, never in the core or the test harness; callers and tests supply only configuration naming the source URL and pin.
  scope: boundary: core<->gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p41], [p42]
  rejected-alternative: core tests standing up llama-server and fetching GGUF weights themselves
  endorsement: n/a

- statement: The gateway multiplexes many competing callers onto shared inference hardware and owns the queue and the concurrency limits, so a prompt can fan out fifty wide and the gateway interleaves the callers.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p18]
  rejected-alternative: building concurrency limits into the prompt executor
  endorsement: n/a

- statement: Concurrency limits attach to hardware devices, not to models; the configuration lets an admin group the models and endpoints that share one physical device (a local card, a specific run pod) under a single limit.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p25]
  rejected-alternative: per-model limits
  endorsement: n/a

- statement: Gateway configuration is organized into named profiles, each a complete package of models and settings sized to fit the hardware and suited to a specific workflow; the gateway runs exactly one profile at a time.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p35]
  rejected-alternative: one general-purpose configuration holding every model at once
  endorsement: n/a

- statement: Profiles can be switched at runtime through a remote admin command, so a batch script can reconfigure the gateway for a workload before running its prompts.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p35]
  rejected-alternative: none
  endorsement: n/a

- statement: Profile switching is immediate, not graceful: in-flight local requests are dropped, because the local machine has a single operator who knows what they are doing.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: graceful drain of in-flight requests before switching
  endorsement: n/a

- statement: A profile can inherit another profile recursively, like include files.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway never auto-selects a profile; the operator names the profile explicitly.
  scope: gateway
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p36]
  rejected-alternative: auto-selecting a profile
  endorsement: n/a

- statement: Small utility models (embeddings, classifiers, rerankers) are co-located with the gateway rather than called over a network, and they may run on CPU where that is enough.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p19], [p20], [p21]
  rejected-alternative: serving utility models from a remote endpoint
  endorsement: n/a

- statement: No defaults, everything explicit: every prompt declares the model it needs, or explicitly says it accepts anything, and at minimum states its required context and whether it needs thinking; implicit configuration is the enemy of precision.
  scope: global
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p58], [p60], [p62]
  rejected-alternative: DEFAULT_MODEL and PROMPTFORGE_MODEL environment-variable fallbacks
  endorsement: n/a

- statement: The effective model name is exposed to the prompt as sys.model, usable in prose substitution and in Lua, so a report can footer itself with the model that produced it without hardcoding.
  scope: core
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p54]
  rejected-alternative: none
  endorsement: n/a

- statement: sys.model is unavailable during the prologue (the H1 Lua block); it exists only after the section's model scope closes, so the epilog is its intended consumer.
  scope: core
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p55]
  rejected-alternative: putting model in the initial pre-preamble sys object, which would miss section-local models.use
  endorsement: n/a

- statement: Within a local device, concurrency is divided into named lanes so a fast utility model is never queued behind a long generative call, while two generative calls still cannot run simultaneously.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: one flat concurrency limit per local device
  endorsement: unaddressed

- statement: Queued requests are scheduled fairly across callers, round-robin, so no single caller starves the others.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: When the gateway queue is full, it rejects requests immediately with backpressure (HTTP 503) rather than queueing without bound; the executor retries or reports failure.
  scope: gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: unbounded queueing
  endorsement: unaddressed

- statement: When the active profile changes, the model catalog changes with it, and any bindings cached in an executor are stale; the executor must re-fetch the catalog on its next run.
  scope: boundary: core<->gateway
  source: ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [plans section]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- The gateway executable may be as big as it needs to be; operational simplicity beats binary size [p16].
- The author works through an AI-driven workflow and feels layers of software between operator and machine; the design should collapse those layers [p16].
- Quantization quality bar: "Q4 sounds terrible" - skepticism toward heavy quantization for serious work [p4].
- GPU support must not be forced on anyone; a machine without CUDA still gets a working gateway [p46] - excluded as a build/technology choice, kept as a sensibility note.
- Build order preference: easiest and most useful first, hardest and most risky last [p38].
- Review process preference: exactly one round of review, edits made in the review context, because further rounds keep finding things forever [p45].
- Deadline temperament: "you will get it done in 2 hours" [p40].

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client large session part 3 (prompt file format, call syntax, per-section tool restriction, gateway proxy, logical model routing)
---

# 2026-08-02-1134-mcp-client-large-part3

```yaml
- statement: A prompt file is markdown with YAML frontmatter, an H1 title, human-readable text, and headed sections that nest recursively from H2 through H6.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p137]-[p144]
  rejected-alternative: none
  endorsement: n/a

- statement: The call directive uses natural-language syntax ("Call return with x") because prompts are written for humans to read.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p155]-[p158]
  rejected-alternative: function-call notation call("return", "x")
  endorsement: n/a

- statement: A prompt hands the model a handful of well-described tools plus a prose prompt and lets the model figure out the task on its own.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p158]
  rejected-alternative: none
  endorsement: n/a

- statement: Operations funnel through a single call() tool so the model is not loaded with too many tools in context.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p163]
  rejected-alternative: exposing each operation as its own tool
  endorsement: n/a

- statement: call() is not injected into a section that always falls through; a section is offered only the tools it needs.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p164]
  rejected-alternative: injecting call() into every section unconditionally
  endorsement: n/a

- statement: Model sessions come in both streaming and non-streaming forms, because downstream consumers (talktron) need a streaming session.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p170]
  rejected-alternative: none
  endorsement: n/a

- statement: Every markdown feature of the prompt format has a corresponding test.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p173]
  rejected-alternative: none
  endorsement: n/a

- statement: The executor and the gateway do not share schema definitions; each keeps its own copy because sharing them is unnecessary coupling.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]
  rejected-alternative: a shared schema crate used by both sides
  endorsement: n/a

- statement: A conversation never flips between physical endpoints, because switching endpoints loses the KV cache.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p210]
  rejected-alternative: flipping one conversation across multiple endpoints
  endorsement: n/a

- statement: Global inference limits are enforced by funneling all model traffic through the single gateway that holds the provider key.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p211]
  rejected-alternative: distributing the provider key across multiple machines
  endorsement: n/a

- statement: An executor run is not tied to one base URL; each H2 step can use a different logical model, and each logical model can point to a different physical model.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p212]
  rejected-alternative: binding a whole run to a single base URL
  endorsement: n/a

- statement: The executor carries no base_url; endpoint configuration lives in the model config.
  scope: core
  source: user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p213]
  rejected-alternative: an executor-level base_url setting
  endorsement: n/a

- statement: Each prompt carries a per-prompt file that maps prompt-level model ids to gateway model ids.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p214]
  rejected-alternative: none
  endorsement: n/a

- statement: The executor is just a function call, not a long-running service.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p215]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway is a proxy to an upstream OpenAI-compatible endpoint, and gateways chain: a local gateway can forward to a company gateway that forwards to a remote endpoint guarded by a whitelist.
  scope: gateway
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p216]-[p218]
  rejected-alternative: none
  endorsement: n/a

- statement: The tools offered to the model are restricted per section; a section that only does goto-with-clear is offered a mode-less goto() so the model never has to pick a call kind.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p222]
  rejected-alternative: offering the full call() surface to every section
  endorsement: n/a

- statement: The language offers both a dramatically simple single-concern call and a swiss-army call with every mode; simple sections and small models use the former, and complex sections can use a frontier model with the latter.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p223]
  rejected-alternative: a single call shape for all sections
  endorsement: n/a
```

## Not converted

- Make a little progress on a lot of things instead of a lot of progress on a few; build the known quantity (the gateway) first while the control flow is still uncertain. (Work-sequencing philosophy.) [p189]
- The user wrote Beast and knows SSE cold; the irritation is at being lectured, not at the technology. (Temperament.) [p183]
- Open question, unresolved in this unit: should skipping a heading level be an error? [p145]
- Open question, unresolved in this unit: AGENTS.md or CLAUDE.md? [p146]
- AGENTS.md should carry a command that keeps the docs up to date on every commit. (Repo-process directive, not language or engine behavior.) [p168]
- Hard-code the Anthropic base URL for now and point the HTTP layer at the gateway later. (Excluded as a technology/scaffolding choice, not a behavior.) [p149], [p169]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP server planning session (explicit invocation, fixed tool list, live reload, minimal core, plain-prose design docs, hypothesis collapse)
---

# 2026-08-03-2040-plan-the-mcp-server

```yaml
- statement: The MCP server has exactly one job, serving PromptForge prompts to a calling harness; anything beyond that is out of scope.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p2]
  rejected-alternative: a broader server surface beyond prompt-serving
  endorsement: n/a

- statement: A PromptForge prompt is a command; it runs only because a caller named it, never because a model noticed a tool that looked relevant.
  scope: mcp
  source: user-corrective
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p58], [p59]
  rejected-alternative: publishing each prompt as its own tool so a model can select it ambiently
  endorsement: n/a

- statement: PromptForge is a deterministic pipeline whose product is a finished report, designed for unattended server deployment running reports at scale; interactive invocation exists for development, testing, and explicit local runs.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p58], [p59]
  rejected-alternative: a general-purpose prompting language invoked conversationally
  endorsement: n/a

- statement: The server's published tool list is small and fixed (list_prompts, run_prompt, check_run, need_prompt) and never changes at runtime, so a prompt saved seconds ago is callable immediately with no reconnect and no list-changed machinery.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section]
  rejected-alternative: dynamic per-prompt tools with notifications/tools/list_changed
  endorsement: affirmed

- statement: need_prompt resolves an inexact name for an intent the user already stated; it never discovers a capability the user did not ask for.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p60]
  rejected-alternative: a classifier-backed chooser that recommends prompts for a task
  endorsement: affirmed

- statement: Tool descriptions are written in the register of a command interpreter; no trigger phrasing, no "use this when", nothing that competes with a client's own tools for selection.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p15], [p58]
  rejected-alternative: tool descriptions optimized to win model selection
  endorsement: affirmed

- statement: The server hard-codes no knowledge of any specific client or harness; it behaves the way conventional MCP servers behave.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p25], [p26]
  rejected-alternative: client-specific special cases such as Cursor-aware behavior
  endorsement: n/a

- statement: The prompt directory is watched live and prompts reload without a server restart; a prompt that breaks stays listed, carrying its error, rather than silently disappearing.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p6], [plans section]
  rejected-alternative: requiring a restart or a new chat to pick up prompt edits
  endorsement: n/a

- statement: The prompt catalog is configured with both individual prompt files and whole directories via wildcard, with exceptions.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p4], [p5]
  rejected-alternative: none
  endorsement: n/a

- statement: A long-running run keeps the calling client informed with live progress notifications, so the client sees work happening instead of waiting on a silent timer.
  scope: mcp
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p32]
  rejected-alternative: a bare admission timer with no progress signal
  endorsement: n/a

- statement: Boot validation refuses an incoherent catalog; all failures accumulate and print before a nonzero exit, so a client never sees a silently missing tool.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section]
  rejected-alternative: starting the service with only the valid subset of prompts
  endorsement: unaddressed

- statement: Design work separates fact-finding from prose; one agent states plain facts and a separate fresh agent composes the prose in a given register, because writing under context pressure is what produces riddling language.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p77], [p78]
  rejected-alternative: writing the prose in the same commit and context that did the design work
  endorsement: n/a

- statement: A prompt declares what it needs (a need string bound to an internal ID in its Lua block), never which tool to call; binding needs to concrete tools is the engine's indirection, not the prompt's.
  scope: core
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p60]
  rejected-alternative: prompts naming specific tools
  endorsement: n/a

- statement: Do more with less; if an established facility can implement a feature, use it instead of building new infrastructure, and keep the core a minimal set of small primitives reused everywhere.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p61]
  rejected-alternative: inventing new frontmatter when Lua already works
  endorsement: n/a

- statement: Reading a prompt file never runs anything inside it; a parsed prompt is inert data that can be constructed, inspected, and enumerated on a server surface without executing prompt code.
  scope: core
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p74]
  rejected-alternative: none
  endorsement: n/a

- statement: The design document is revised in the same commit as the step that changes the design, so the document is accurate per commit.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p17], [plans section]
  rejected-alternative: batching documentation updates after implementation
  endorsement: n/a

- statement: Design documents state what happens, not what property a thing has.
  scope: global
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p68], [p73]
  rejected-alternative: aphoristic property statements such as "parsing is total and produces no side effects"
  endorsement: affirmed

- statement: Never count what you do not name; a sentence like "two of those five are refuted" must name the two.
  scope: global
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p68], [p76]
  rejected-alternative: unnamed counts that send the reader hunting
  endorsement: affirmed

- statement: Superseded or rejected design content is preserved in a residue sidecar alongside the design document, not deleted.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p64], [p65]
  rejected-alternative: deleting leftover design material during a reorganization
  endorsement: n/a

- statement: Recovered design rationale is hypothesis collapse; generate competing explanations for each design element, kill them with structural evidence (plausibility kills nothing), state survivors confidently, leave what cannot be collapsed openly unresolved, and never apply an archive-proposed collapse without human approval.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p80], [p81]
  rejected-alternative: fluent single-explanation rationale written without evidence
  endorsement: n/a
```

## Not converted

- A design document is mostly why; code contains what, and where nothing forces a choice, that fact is worth stating rather than papering over. [plans section]
- The bet behind rationale recovery: most design choices are forced by constraints that are themselves visible in the code, so the why is largely recoverable. [plans section]
- Contingency is unrecoverable from code; numbers chosen inside a range, facts learned outside the repository, and deleted alternatives leave no trace, so a high open count is honest archaeology, not failure of effort. [plans section]
- "What lost and why" is the most valuable line a design document has. [plans section]
- The user wants prompts to be first-class citizens in the harness and research output delivered into the chat, not into side boxes. [p24]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core-large part 5 (first-class tools/models, section lifecycle, store, dialects, fanout)
---

# 2026-08-09-1058-promptforge-core-large-part5.md

```yaml
- statement: A pipeline must be re-runnable from any step, with every intermediate output persisted as a file that can be read back in, because development and debugging of an analytical pipeline depend on it.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p377]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompts are written agnostic of the tool backend - a prompt says "search", never "search the web" - and a tool's exposed description can be rewritten when it is injected so it fits what the model expects, leaving the prompt valid whether the backing tool is web search, workspace search, MCP, or a RAG index.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p383]
  rejected-alternative: exposing the tool to the model under its backend-specific description
  endorsement: n/a

- statement: The tool.need call establishes a tool's name and the prompt owns that name from then on; rebinding happens in the preamble.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p386]
  rejected-alternative: none
  endorsement: n/a

- statement: Because the engine's pipeline is rigid and the orchestrating model cannot reshape the Lua at runtime, behavioral variation (such as which sources a prompt may consult) must be supplied through ahead-of-time configuration.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p392]
  rejected-alternative: relying on an orchestrator to reinterpret and reshape the prompt's instructions at runtime
  endorsement: n/a

- statement: The language has exactly three named Lua phases - the preamble (the H1 code) and the per-section prologue and epilogue - and this terminology is enforced consistently across the entire repo.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p393]
  rejected-alternative: none
  endorsement: n/a

- statement: The preamble can run model inference with tool calls, so the model can parse the argument string and take control before any section runs.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p397]
  rejected-alternative: none
  endorsement: n/a

- statement: Tools and models are first-class Lua objects: a tool is an inspectable, invocable table, a model exposes infer()/turn(), and the preamble can declare globals such as tool lists that any section can use - encapsulation that also makes both mockable and unit-testable.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p398-p401]
  rejected-alternative: treating tools and models as opaque registrations rather than encapsulated objects
  endorsement: n/a

- statement: Tool registration stays open between inference calls within a phase, so the add-search, infer, add-fetch pattern keeps working; the toolset must not be sealed at the first infer().
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p409]
  rejected-alternative: sealing the toolset on the first inference call
  endorsement: n/a

- statement: Prose lives in markdown sections, never inside Lua code; prose in code is rejected because markdown is where bold, italics, bullets, paragraphs, block quotes, and URLs can be properly formatted.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p427]
  rejected-alternative: passing prose as string arguments to model.infer()
  endorsement: n/a

- statement: Non-final prose sections are single-shot and always fall through; the last prose section is the tool loop and proceeds to the epilogue only when the reply contains no tool call.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p429]
  rejected-alternative: none
  endorsement: n/a

- statement: Lua can invoke another H2 section as a subroutine through execute(), reusing the engine's existing section-execution machinery.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p430, p432, p433]
  rejected-alternative: none
  endorsement: n/a

- statement: Any Lua can call goto to transfer control to another section, and goto is context-clearing.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p431, p432, p433]
  rejected-alternative: none
  endorsement: n/a

- statement: The shared preamble program is never re-executed for each section; its objects are serialized out of the preamble VM and into each section VM, because replaying would re-run any inference the preamble performed.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [p448-p450]
  rejected-alternative: replaying the shared H1 program inside every section VM
  endorsement: n/a

- statement: The store is the only intentional cross-section mutable channel; Lua functions, closures, globals, var, tools, and reply are branch-local by construction.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: mutable run-global Lua state
  endorsement: affirmed

- statement: A scalar top-level return from either preamble or epilog ends the run; a preamble return skips prose, model, and epilog; nil continues sequential fall-through.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: none
  endorsement: affirmed

- statement: The shared library is compiled once and its bytecode executed independently in every section VM, so each section receives isolated functions, closures, and mutable globals.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: none
  endorsement: corrected

- statement: All wire quirks - field synonyms, empty content, tool-call-with-null-content - are normalized in one module, and execute, clients, and hosts stay dumb; a final turn with no tool calls and empty content is a hard error even when reasoning is present, reasoning is never promoted into the answer, and breaking prompts that silently succeeded with empty replies is the intended effect.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: completion normalize layer]
  rejected-alternative: scattering wire-quirk handling across execute, client, and hosts
  endorsement: unaddressed

- statement: Recoverable tool target failures (HTTP errors, unsupported content type, timeout, too large, undecodable charset, DNS) return Ok with model-readable text naming status, final URL, and a next move, so the tool loop continues; admission and policy failures (invalid URL, blocked scheme/port/userinfo/IP literal, redirect refused) remain hard errors, and the untrusted HTTP error body is never placed in the tool result.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: webfetch soft errors]
  rejected-alternative: aborting the tool call on recoverable target failures
  endorsement: unaddressed

- statement: Prompts stay dialect-agnostic: the operator declares each model's tool dialect on the gateway, the gateway advertises it, core freezes it onto the bound model, and the tool loop selects the normalization plugin without ever asking the prompt what format to use; an unknown dialect id is a hard error with no silent fallback.
  scope: boundary: gateway<->core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Tool dialect plugins]
  rejected-alternative: sniffing completion text in the prompt surface or hardcoding model names inside prompts
  endorsement: unaddressed

- statement: Fanout fires all arms at once while the gateway admits up to its lane concurrency and queues the rest fairly; replies stay ordered by arm index, the first arm error aborts its siblings with the same visible behavior as sequential fail-fast, and authors must not assume one arm sees another arm's store writes.
  scope: core
  source: ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Fanout and gateway concurrency]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- [p376] After first-class tools arrive, the VM can no longer be assumed fixed once the preamble has run; it can change after each completion.
- [p395] Unshipped code earns no compatibility concessions: "there's no one to break."
- [p401] Encapsulation is plain programming hygiene; an abstraction earns its keep by being mockable and testable.
- [p411] Big changes get a deep, subagent-driven evaluation before adoption; thoroughness scales with blast radius.
- [p412] The phase transition's only real point is to protect the epilogue.
- [p432] The conversation is preeminent: design documents must be rewritten to match what was settled in discussion.
- [p436] Documentation teaches progressively: one new concept per section, no forward references, every example a complete runnable prompt.
- [p440] Front-page documentation is crisp, bottom-line-up-front, dense and scannable - it says what the thing is rather than performing cool.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge.md session, Aug 16 afternoon (H1-only prompts, reply variable, tool call limits)
---

# 2026-08-16-1431-promptforge-md-aug16-afternoon.md

```yaml
- statement: Never create a feature that does something the user can already implement using more general existing features.
  scope: global
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p15]
  rejected-alternative: a default_return key in the YAML frontmatter (use a goto to a section that returns a constant string instead)
  endorsement: n/a

- statement: Everything in the language behaves as consistently as possible, unless there is a really good reason for an exception.
  scope: global
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20]
  rejected-alternative: none
  endorsement: n/a

- statement: When execution enters a section, the model's previous reply is always available in the reply variable; a jump carries the reply into the destination section.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20]
  rejected-alternative: jump() dropping the reply so Lua cannot transfer it into the next block
  endorsement: n/a

- statement: State is carried forward by default; a user who does not need the reply clears it themselves before jumping, and a destination section that does not care simply never mentions it.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p21]
  rejected-alternative: not transferring the reply on jump
  endorsement: n/a

- statement: There is a single reply variable; incoming_reply, reply, and last_reply are folded into one name, reply.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p22]
  rejected-alternative: three separate variables incoming_reply, reply, and last_reply
  endorsement: n/a

- statement: Lua can terminate the prompt early and return the reply.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p25]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt with no H2 sections is valid: the H1 runs its Lua and prose blocks, and when the model does not end in a tool call, execution ends and the model's reply becomes the prompt output.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p13]
  rejected-alternative: requiring at least one H2 section per prompt
  endorsement: n/a

- statement: For an H1-only prompt, the output priority is: the H1 Lua return value, then the H1 model reply, then a "done" fallback.
  scope: core
  source: ai-proposed
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Prompts are executed as MCP tool calls, and promptforge.md itself runs the MCP server.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p9]
  rejected-alternative: none
  endorsement: n/a

- statement: The root toml is not used at all.
  scope: global
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p10]
  rejected-alternative: configuration through a root toml file
  endorsement: n/a

- statement: The model discovers the MCP API by querying it once, keeping the API in context, rather than having the API documentation embedded up front.
  scope: mcp
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p44]
  rejected-alternative: embedding the MCP API documentation in the context
  endorsement: n/a

- statement: Tool configuration belongs in the H1 as Lua, not in the YAML frontmatter.
  scope: core
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p45]
  rejected-alternative: tool configuration keys in the YAML frontmatter
  endorsement: n/a

- statement: Tool call limits are per-section; a global limit makes no sense other than being set to a very large number, because a global limit forces the author to re-check it every time sections are added.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p49]
  rejected-alternative: a meaningful global tool call limit
  endorsement: n/a

- statement: There are no hidden defaults that can change prompt behavior; PromptForge is as deterministic as possible while still having the capability of inference.
  scope: global
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p66]
  rejected-alternative: an invisible default tool call limit of 24
  endorsement: n/a

- statement: The language can express the universal search/fetch pattern with per-turn tool availability, where search is available only on the first turn and fetch only on the second and later turns.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p63]
  rejected-alternative: none
  endorsement: n/a

- statement: Constraining a section's toolset must not otherwise change its behavior; the section behaves the same as the traditional unconstrained form, only with a restricted toolset.
  scope: core
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p64]
  rejected-alternative: a constrained-toolset formulation that alters section behavior
  endorsement: n/a

- statement: The conversation history is not rewritten to scrub tool offerings or tool calls, because the model would see information appearing out of nowhere.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p61]
  rejected-alternative: scrubbing the tool offering and tool call from history
  endorsement: n/a

- statement: Migrating the whole conversation is a design non-goal.
  scope: core
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p65]
  rejected-alternative: whole-conversation migration
  endorsement: n/a

- statement: A fenced block whose contents contain backticks is written with a 4-tick outer fence.
  scope: global
  source: user-corrective
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p4]
  rejected-alternative: triple-backtick fences around blocks with interior backticks
  endorsement: n/a
```

## Not converted

- [p29] Whether {{ reply }} substitution injects information versus instructions is ambiguous and was raised as an open question, never resolved into a rule.
- [p30] Imperfect model output is acceptable because the user can always fix it.
- [p67] Tool call limits may be unnecessary at all; a large model concludes before overflow and a small model's context fills up and errors, which is a natural bound.

---

# 2026-08-05-2249-section-lua-lifecycle.md

## Candidates

(none - the unit is a single plan-execution dispatch prompt; it directs workflow, not language or engine behavior, so nothing passes the altitude test)

## Not converted

- When executing a plan, do not pause for reversible choices: make the plan's stated decision, record any necessary falsifier in design-core.md, and continue. [p1]
- Preserve the original design document (design-core-orig.md) byte-for-byte as the historical record. [p1]
- Fix every failure you introduce; run targeted tests as you proceed, then the full verification commands. [p1]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from the two-repo commit review step (2026-08-03 18:27)
---

# 2026-08-03-1827-two-repo-commit-review.md

```yaml
- statement: A tool-call loop terminates ordinarily with no signal from the prompt; when the model has nothing left to do it says so in prose, and the executor moves on.
  scope: core
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [design documents section]
  rejected-alternative: an explicit termination signal emitted by the prompt
  endorsement: n/a

- statement: A forward-design residue states plainly at its top that it is forward design, names what exists today, and points at the crate's as-built document.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: residue that reads as if it describes the built world
  endorsement: n/a

- statement: Documentation of the built world must be accurate in both directions; claiming something unbuilt that ships is as wrong as claiming built what is not.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: checking only for claims of built features that do not exist
  endorsement: n/a

- statement: A repointing commit changes only the pointer; any change of meaning beyond the pointer is a defect.
  scope: global
  source: user-stated
  citation: 2026-08-03-1827-two-repo-commit-review.md [p4]
  rejected-alternative: folding content edits into a rename or repointing commit
  endorsement: n/a

- statement: When a rename makes a bare filename ambiguous, every surviving reference must be found and updated, including citations and quoted sentences, not just links.
  scope: global
  source: user-corrective
  citation: 2026-08-03-1827-two-repo-commit-review.md [design documents section]
  rejected-alternative: updating only formal path references and leaving prose mentions
  endorsement: n/a
```

## Not converted

- Review is read-only: the reviewer reports findings and never fixes or commits anything itself. A work-discipline rule for the review step, not a rule of the language or engine.
- Report back in under 80 words with the finding count and the most serious finding. A terse-reporting preference, bookkeeping.
- Write nothing for a check that passes. A signal-to-noise preference for review output, subsumed by the review discipline.
