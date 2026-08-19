# MCP client / agentic harness work (reduced)

*2026-08-02 10:34 - transcript 068d3001-b330-4843-93e6-0fbe10f9985e*



## Prompts



**[p2]** should I put the mcp client in its own crate

**[p5]** but if the mcp client needs the Tool struct and the core crate needs the mcp client isn't that a circular dep

**[p9]** it seems to me the thing it buys us is it saves one round of inference. because if we want to get rid of the indirection we could just look at what the mcp services are available and use those to set the tools.add list based on the prompt's needs stated in prose?

**[p10]** No. What if the prompt has a frontmatter which describes the tools it needs in  english, and then we use a classifier at launch time to map the mcp offerings to what the prompt needs?

**[p11]** there needs to be a way for the lua to say "add everything" from the mcp client. and maybe a way to ask for a tool that matches a description?

**[p13]** [pasted: tool-naming research - Cursor's mcp_<server>_<tool> can't reliably reverse-split (_ is both delimiter and legal name character); Claude Code's mcp__<server>__<tool> is round-trip-safe; route on the (server_id, tool_name) pair, not the concatenated string]

**[p14]** why do I care about all of this hardening if I control all the mcp servers?

**[p16]** what I am thinking is we run a zero-shot NLI classifier on the CPU, once at startup - universally available.

**[p17]** I think we need to get training data and run tests to see if the classifier will actually work.

**[p19]** [directive: build the classifier spike autonomously to definitive results - download MCP catalogs from live sources, download eval sets, run in triplicate, get an over-abundance of data]

**[p22]** Question about fine-tuning. Instead of going "all the way" is it possible to just fine tune enough to get N% improvement? so we can get a boost in performance without the degeneracy?

**[p23]** also run all jobs async please, so we can keep talking

**[p25]** Hey, but wait a minute, we actually are doing this wrong, because we're just asking, "Is this tool a fit for?" The description. But what we re for the need, what we really wanna know is given a set of n tools Which one is the best fit for a need? That's a different question entirely.

**[p26]** Here's my idea. We do We do a ranking, we order, we sort them using a not so great criteria, like it doesn't have to be perfect, and then we do the point wise on the top three or something, something, some combination of all at once and point wise on a reduced set.

**[p27]** I dont want LLM in the final result. I want something that runs locally.

**[p28]** what if we build a vocabulary list of like 10,000 words and we do some kind of deterministic pass first just doing word comparison and doing a count

**[p29]** what if we divide the need and the description strings into (noun,verb) lists and compare nouns and verbs separately in embedding space and use that as additional signal

**[p30]** And here's another idea. we can fine tune verbs separately from nouns.

**[p31]** And here's another idea. What if we take all of the eval pairs and we generalize to find out what N categories they have in common (for small N) and then we have a separate categorizer and we fine tune on that and then the algorithm becomes, first we determine category and then we choose a separate fine-tuned model for that specific category. since they are all in the same category the fine tune will have less chance of degeneracy. Basically we partition the tool space so each reranker/classifier can be more narrow

**[p33]** what if we have a handful of small LoRAs and we load one dynamically depending on the category

**[p39]** Okay, so let me explain what I want. What we want is, we, we have a prompt. And at the top of the prompt, we have some Lua, and it, it, it It has a list of Internal tool names that are local to the prompt, and then it associates each one of them with a description of what it needs. So right when the prompt loads up, it runs some Lua, and the Lua calls into the harness and says, "Here's a list of the tools that I need. Right? Then the description of the tool of what it needs to be able to do, and the user puts that string in there. And then I want it to use our contraption, our classifier, all that crap, to go through what's available. And figure out what's the best match. How do we do it?

**[p42]** should this be a feature of the mcp client? i.e. offer the api to do this calculation

**[p46]** I'd like 10x more real-world eval data. do it asynchronously. in fact do everything asynchronously.

**[p51]** if you are going to generate need strings you should do it using multiple models. chatgpt, claude, gemini, cursor, etc

**[p55]** Oh, I think there's still room to do a trivial reject. Okay, look at what we have. We have a description, and then we have a catalog, and I wanna have a trivial reject. In other words, I wanna find a way, a fast way, for each description to quickly say no. What if we pair everything? Like, what if we take a catalog, we have twenty items, and we pair them, and we do a comparison, which one's better, which one's a better match for the description, and we toss the one that's worse? Like. When, and when we compute the pairs, we have, we, we calculate how similar they are. Like two tools, we, we have like, we calculate their axes, like. What do they do? And we pair tools together that are like, I think if we can categorize like some tools re-some tools return data, some tools talk to the database, some tools update state. Like if we could compare, if we could say the need is to update state, but then we have a tool that, for example, does a-that returns data, like it grabs a report, like we can trivially reject that. And the, and the trivial reject doesn't have to be that accurate as long as there's no false positives, right? So we can de we can develop a very high confidence categorization, and then if the category's not correct, just toss it. We have like eight thousand samples, surely we can come up with some categories for that eight thousand samples.

**[p56]** We should definitely use the, the annotation, but it has to work without the annotation. So the annotation can be seen only as improving the confidence, it can't be seen as necessary, but you knew that. Next, okay. So, okay, let's refine this idea. What if we do, what if we have a classifier, or what if we train a very small network, and so given, given a description and given, or given a need, calculate the word that matters the most. Like for example, the word "OpenAuth" or the word "database," like those words mean a lot.

**[p57]** Do me a favor, just do me a favor. Forget about all this complex stuff. I want you to go into our data, go into our dataset, go into our query set, pick 30 descriptions at random, and then for each description, you pick the most important word, the most relevant word, and then show me a bulleted list of the word and then the, and then the description. Let's look at it together.

**[p58]** We just discovered something. The need strings are all wrong. Those look like prompts. That is NOT what goes in the Lua. The Lua need strings are very much general and aligned. For example
lua.need_tool( "get_paper", "Retrieve WG21 paper's markdown given the paper number" )
lua.need_tool( "insert", "Insert a record into the database log table" )

**[p59]** I think a good way to make need strings is to take the entire catalog corpus, and for each tool description, restate the description in various ways. you could get 5 need strings out of one description.

**[p60]** think about it - when the author goes to write the lua need strings, they will likely just copy or paraphrase the description from the tool they already have which they want to use

**[p61]** We should optimize for identifying when there are duplicates in the catalog, and fail loud there. Having two of the same tool in my opinion is a configuration error, except when the user intentionally imports foreign mcp servers. and even in that case there has to be a way to disambiguate. For example we could *require* in that case that the user has to use the LLM to do the tool select, not the lua.

**[p62]** What do you think of this: the promptgate executor can have a built-in tool choose_mcp_tool and this takes the need string and launches a fresh subcontext to make the decision, and it can also return the rationale

**[p63]** ha.. no you dont quite get it. it is not "an escalation path" it is the ONLY path, the author opts-in:

**[p64]** ```lua
tools.add( "choose_mcp_tool" ) <-- the only choice
```

**[p66]** My guess, and I am not certain, is that choose_mcp_tool will return a tool description. Perhaps more than one (maybe thise could be a separate choose_mcp_tools). And it could return an error "no tools available." The point is that this is complementary to the static approach, not a replacement.

**[p67]** Yes, and consider this strategy for context management. Instead of just appending the returned results, the harness rewrites the context so it includes the returned tool descriptor placed BEFORE the prompt prose, and it leaves out the choose_mcp_tool toolcall details. Its like going back in time and re-prompting the LLM but with the chosen tool in context already.

**[p69]** well choose_mcp_tools is already paying for inference in the fresh subcontext so we might as well return a shortlist and then have the subcontext select the best fit

**[p70]** actually we might not need a subcontext for the choosing. The main context performs the toolcall, we get a shortlist and then we just inject the shortlist into the main context rewrite. Then the main context has all ~3 tools to pick from. And it has the full history.

**[p71]** the nice thing about the main context is that the author already has all the mechanisms to control it. they can select the model. they can opt-out of the context rewrite. if we did the subcontext then we'd have to answer the question "which model".

**[p72]** It would be nice to have something where, a step uses a reasoning model to select the tool and then it does the context-clearing goto (a promptforge feature) and passes the tool descriptor into the next context, and that context can use a lesser model

**[p73]** [directive: fresh sibling directory holding the clean final dataset (distractors, proper need strings, 2-3 per descriptor) plus the final design doc, produced with the architect tool]

**[p76]** I think you are confused. The design doc is the design of the promptforge-mcp-toolpicker crate. That means, the tools.add, the tools.add_need, the choose_mcp_tool

**[p77]** I also want the plan to build out the final spike in the sibling dir (so we can run it later if things change), and to have the nice dataset with the need strings. it can copy over the dataset and put it in a very efficient representation (I dont want 16,000 files)

**[p78]** should we embed the mcp client?

**[p79]** the argument for making it a separate crate is that a coding LLM only has to consider a smaller amount of code, and it is morely to completely fit in a single context window.

**[p82]** the plan needs to mine this entire chat history to understand and explain the rationale this should go in a separate rationale.md document. it explains the tool scoping, how the model can pick the tool using choose_mcp_tool, the goto, all ofthat



## Plans

### MCP toolpicker design and dataset

*Produce the final design document for the MCP tool-picker (design-mcp-toolpicker.md), then build a clean, reproducible evaluation dataset in a fresh sibling directory, then reconcile the design doc's cited numbers with the reproduced results.*

Order (as requested): design doc first, then dataset, then reconcile. Choices are written on the spike's locked qualitative findings; figures marked preliminary until reproduction.

The design doc must carry ~12 load-bearing choices, each as decision + evidence + tension: embeddings not zero-shot NLI (the 0.97-synthetic vs 0.15-real reversal); small interchangeable models; the author-register correction; duplicate + absence detection as the real job; two surfaces (static need_tool, dynamic choose_mcp_tool with main-model pick); four-outcome resolution; duplicate policy with MCP annotation tiebreaker; optional model tiering; resolver as its own crate. (Stated in full in the design-mcp-toolpicker.md section below.)

Dataset design decisions: author-register needs in 3 bands per tool (restatement / synonym / goal-abstracted), generated by multiple models; distractors in two regimes (random = ceiling, hard nearest-neighbor = real); near-duplicates (cosine >= 0.98) excluded from distractors and recorded as equivalent-golds (multi-gold). 3 bands, not 5: bands matter more than volume. Smoke-test ~300 tools and eyeball register before the full 9,922-tool run.

Reconcile principle: after the eval, update the doc's preliminary figures with the reproduced numbers; if any figure moves enough to threaten a design choice, flag it rather than silently patch.

Validity caveats carried: author-register drift in generated needs (eyeball samples before the full run); same-generator bias (multi-model generation + hard distractors).

[Step lists, file-path inventories, and todos dropped.]

## Design Documents Written

### FINDINGS.md (mcp-classifier-spike report) - verdict and unique evidence kept; results tables, dataset build detail, and reproduce commands dropped

Verdict: small sentence-embedding model (cosine), not zero-shot NLI, as the launch-time matcher. NLI looked best (0.97) on a hand-authored set and collapsed to 0.15-0.48 on real, independently-phrased needs; embeddings held at 0.81-0.85 across both. The reversal mechanism: authored needs shared surface vocabulary with the descriptions and NLI keyed on it; bigger checkpoints did not rescue it - a method limitation, not capacity. BM25 same lesson (0.794 authored, 0.516 real). Lesson: a synthetic eval whose queries share words with the targets flatters any lexical method. The CPU, run-once-at-startup, bundle-the-weights plan survives; it just wraps an embedding model.

Evidence unique to this document: a generative LLM was best (0.888) but only ~4 points over the best embedding model at 15-50x latency plus a network dependency - optional escalation at most. Abstention is usable (AUROC 0.85 real) and is where the real cost sits: at a 5% false-bind budget about half the needs auto-resolve and the rest must abstain; the test's hard 40-tool catalogs are harder than realistic deployments. Embedding scoring is milliseconds on CPU, models ~90-440 MB, deterministic (triplicate delta 0.0). Threats to validity: needs generated by one LLM; one tool corpus skewed toward demo servers; cross-encoder reranker over top-k untested - the next experiment if 0.85 is not enough. (Its five recommendations are carried in the design doc choices below.)

### mcp-classifier-spike README - dropped (harness layout, reproduce commands). One line retained: "This is a spike: the code is disposable, the findings are the artifact."

### study-mcp-toolpicker/rationale.md - rejected alternatives and decision rationale kept in substance; prose compressed

The register realization (the single most important one in the study): the Lua need string is written by the prompt author as a clean, parameter-free capability line that reads like a tool's own doc, and authors typically paraphrase the description of the tool they already intend to use. Early evaluation used runtime user utterances as needs - the wrong input distribution. Author-register matching is near-trivial for embeddings because both sides share a register; the difficulty first measured was an artifact of testing the wrong distribution.

Rejected alternatives (each tried and measured):
- Zero-shot NLI: 0.97 hand-authored, 0.06-0.48 real; keyed on shared vocabulary; bigger checkpoints no better. Rejected.
- BM25 / lexical fusion: fusing with embeddings dropped top-1 ~15-18 points - the weaker lexical ranker pollutes the strong one and cannot bridge synonyms, which is the whole problem. Rejected as a matcher; viable only as a minor signal, not a peer.
- Verb/noun POS channels: lowered accuracy at every weight - the base embedding already separates read vs write; POS tagging adds noise. Rejected.
- Hard category routing / mixture-of-experts: dropped top-1 from 0.84 to ~0.68; routing was only 0.72-0.80 accurate and every misroute discards the gold before any expert runs. Rejected as a hard filter; soft top-k narrows without the cliff.
- IDF "most important word" saliency: grabs parameters and filler, not the capability word - the rarest token is usually an argument, not the intent. Rejected; the salient term is the action+object head, which embeddings already capture.
- Cross-encoder rerankers: modest, domain-dependent lift; optional, not core; a fine-tuned reranker is the lever if ever needed.

What the hard part actually is: matching among unrelated tools is ~0.99 top-1; among nearest neighbors ~0.79, but recall@3 stays ~0.93. Two design-shaping facts: (1) the right tool is almost always in the top-3, so surface a shortlist and let a well-informed decider settle near-ties rather than forcing top-1; (2) the genuinely hard cases are near-duplicate disambiguation and absence (~11% of a broad catalog has a >=0.98 twin, mostly cross-server republishes). Hence the four-outcome policy: clear bind; ambiguous within own catalog = configuration error, fail loud; ambiguous from intentionally imported foreign servers = surface shortlist; nothing clears the floor = absence, fail loud. Gate = calibrated similarity floor + top-1-vs-top-2 margin; MCP readOnlyHint/destructiveHint annotations break ties but are never required.

choose_mcp_tool evolution: (1) fresh subcontext retrieves AND an LLM selects, returning one answer plus rationale; (2) since the subcontext inference is already paid for, have it select over a top-k shortlist; (3) decisive simplification - drop the subcontext: choose_mcp_tool is a deterministic, LLM-free embedding retriever returning top-k (~3) descriptors and the main model picks as ordinary tool-calling. The reason is systems, not accuracy: the main context is already author-governed (model choice, temperature, instructions, rewrite opt-out); a subcontext is an orphan configuration (which model, budget, vendor, trace). Main-context selection guarantees chooser = executor (no capability mismatch), keeps one model and one trace, and holds full task history - exactly what breaks a near-duplicate tie the need string alone cannot.

Return contract: a tool descriptor (name, description, input schema), not an invocation; one on confidence, a shortlist on a genuine tie, "no tools available" on absence - mandatory because a model handed only a shortlist over-binds (~23% false-bind measured).

Context rewrite: on dynamic resolution the harness rewrites context so the chosen descriptor sits before the prompt prose and the discovery episode is excised, then re-generates - a dynamically discovered tool lands in the identical execution state as a statically bound one (single execution model). Bonus: untrusted candidate descriptions do not persist. Costs: a second inference pass and prefix-cache invalidation, negligible for one-time discovery.

Model tiering: strong-model section selects, context-clearing goto passes the descriptor into a fresh context, cheaper model executes - the "right" form of a selection subcontext because a section already has author-configured model selection. Caveats: gate on expected ambiguity (common selection is trivial); deliberate chooser != executor reintroduces capability mismatch - pass usage hints, reserve tiering for mechanically simple tools.

Two surfaces, one engine: static add_need (deterministic, LLM-free, reproducible) and dynamic choose_mcp_tool (model-driven, adaptive) are complementary; the context rewrite converges the dynamic path onto the static execution state, so downstream everything is uniform.

Why the resolver is its own crate: (1) the embedding model must not ride along with the protocol - the CLI already consumes MCP without it; (2) isolation and independent testing - resolver tests against synthetic catalogs, client against a mock server; (3) each crate stays context-window-sized so a coding LLM can hold a whole unit at once. Corollary obligation: keep each crate lean with a crisp public API, and do not over-fragment.

Deferred on purpose: MCP sampling and roots (deprecated upstream); fine-tuning (the lever past ~0.85, expected ~0.88-0.93, trained on real - not same-generator - needs with hard negatives); calibration (raw cosine is not a probability; a temperature/isotonic/conformal step is required for a hard error budget).

### study-mcp-toolpicker/design-mcp-toolpicker.md - the 12 key choices and normative contracts kept; configuration shape and crate file inventories dropped

Executive summary: the author declares needs as author-register capability descriptions - tools.add_need("db", "run a read-only SQL query against the log database") - and at launch the crate embeds the connected catalog, cosine-matches each need, and binds the alias on a clear win, or fails loud on own-catalog ambiguity or absence. For capabilities not known at authoring time, tools.add("choose_mcp_tool") opts into runtime discovery: a deterministic top-k retriever returns descriptors, the harness rewrites context so the tool appears available from the start, and the main model calls it. Author-register matching is near-trivial (top-1 ~0.99), so the engine's real work is duplicate and absence detection; the right tool is in the top-3 ~0.93 of the time even among close competitors, hence shortlist over single guess. No LLM runs in the crate's own machinery.

Key design choices:
1. Local sentence embeddings are the matcher, not zero-shot NLI or lexical methods. Tension: a bundled model file, but small and deterministic.
2. bge-small-en-v1.5 and all-MiniLM-L6-v2 are interchangeable; the model is configurable and defaults to bge-small; larger models did not reliably help. Reversing later is a config change, not a code change.
3. Needs are author-register capability descriptions, not user utterances; the add_need description contract is "a clean, parameter-free statement of what the tool does."
4. The real job is duplicate and absence detection, not the happy-path match; the abstain path (fail loud) is first-class, not an afterthought.
5. Resolution is a similarity floor plus a top-1-vs-top-2 margin; raw cosine is not a probability, so calibration is required before the floor can be a guaranteed error budget (deferred).
6. Duplicates within the author's own catalog are configuration errors and fail loud; duplicates from intentionally imported foreign servers surface a shortlist. MCP readOnlyHint/destructiveHint/idempotentHint annotations break ties where present but are never required.
7. tools.add_need (static, launch-time, LLM-free) and choose_mcp_tool (dynamic, runtime) are complementary and share the engine.
8. choose_mcp_tool is a deterministic embedding retriever, not an LLM; the main model does the choosing - the crate stays LLM-free and selection sits where full task context and author model configuration already are.
9. On dynamic resolution the harness rewrites the context (descriptor before the prose, discovery episode excised); dynamic converges onto the static execution state - one execution model regardless of surface.
10. The crate depends on a thin promptforge-mcp-client for protocol and owns only the semantics; protocol consumers (the CLI) must not pull the embedding model; each crate stays small enough for a coding LLM to hold whole.
11. An optional model-tiered configuration (strong-model select -> context-clearing goto -> cheap-model execute) exists for genuinely hard selection, gated on expected ambiguity.
12. MCP sampling and roots are not implemented (sampling is deprecated upstream); the crate does not advertise those capabilities.

choose_mcp_tool return contract (normative): a single descriptor {server, name, description, input_schema} on a clear win; a 2-3 shortlist on a genuine near-tie (duplicates), for the main model to disambiguate with full task context; {error: "no tools available"} when nothing clears the floor. Cacheable by (need, catalog_hash).

Resolution engine: at startup, snapshot each server's tools/list and embed enriched tool text (name + description + parameter names), cached by catalog hash; per need, cosine-rank, take top-k, apply floor and margin, emit one of the four outcomes; near-identical tools (cosine >= ~0.98) are recorded as equivalent-golds so an equivalent pick is not wrong.

Evidence (preliminary): top-1 ~0.99 random distractors / ~0.79 hard near-neighbor, recall@3 ~0.93 hard; duplicates ~11% of a broad catalog at >=0.98, overwhelmingly cross-server; bge-small ~ MiniLM, larger models not reliably better.

### study-mcp-toolpicker README - reduced to dataset definitions: random distractors = matching among unrelated tools (easy ceiling); hard distractors = the gold's nearest neighbors (real disambiguation); bands vary paraphrase distance (restatement / synonym / goal); dataset stored compact, id-referenced (no per-case files).

