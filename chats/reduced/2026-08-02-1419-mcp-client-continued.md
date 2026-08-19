# MCP client work continued

*2026-08-02 14:19 - transcript bbc51d14-7aff-4a1c-985f-5453f3f6dd51*



## Prompts



**[p2]** should I put the mcp client in its own crate

**[p5]** but if the mcp client needs the Tool struct and the core crate needs the mcp client isn't that a circular dep

**[p8]** is this the consequence of the lua having to name each tool for each h2?

**[p9]** it seems to me the thing it buys us is it saves one round of inference. because if we want to get rid of the indirection we could just look at what the mcp services are available and use those to set the tools.add list based on the prompt's needs stated in prose?

**[p10]** No. What if the prompt has a frontmatter which describes the tools it needs in  english, and then we use a classifier at launch time to map the mcp offerings to what the prompt needs?

**[p11]** there needs to be a way for the lua to say "add everything" from the mcp client. and maybe a way to ask for a tool that matches a description?

**[p13]** [pasted: excerpt on MCP tool-naming delimiters; route on the (server_id, tool_name) pair, not the concatenated string] wtf does this mean

**[p14]** why do I care about all of this hardening if I control all the mcp servers?

**[p15]** why LLM classifier and not a zero-shot

**[p16]** what I am thinking is we run a zero-shot NLI classifier on the CPU, once at startup - universally available.

**[p17]** I think we need to get training data and run tests to see if the classifier will actually work.

**[p19]** [directive: build and run the classifier spike autonomously and exhaustively - live MCP catalogs, eval sets, triplicate runs, keep going until stopped]

**[p20]** [correction: the spike jobs should have been using the GPU]

**[p22]** Question about fine-tuning. Instead of going "all the way" is it possible to just fine tune enough to get N% improvement? so we can get a boost in performance without the degeneracy?

**[p25]** Hey, but wait a minute, we actually are doing this wrong, because we're just asking, "Is this tool a fit for?" The description. But what we re for the need, what we really wanna know is given a set of n tools Which one is the best fit for a need? That's a different question entirely.

**[p26]** Here's my idea. We do We do a ranking, we order, we sort them using a not so great criteria, like it doesn't have to be perfect, and then we do the point wise on the top three or something, something, some combination of all at once and point wise on a reduced set.

**[p27]** I dont want LLM in the final result. I want something that runs locally.

**[p28]** what if we build a vocabulary list of like 10,000 words and we do some kind of deterministic pass first just doing word comparison and doing a count

**[p29]** what if we divide the need and the description strings into (noun,verb) lists and compare nouns and verbs separately in embedding space and use that as additional signal

**[p30]** And here's another idea. we can fine tune verbs separately from nouns.

**[p31]** And here's another idea. What if we take all of the eval pairs and we generalize to find out what N categories they have in common (for small N) and then we have a separate categorizer and we fine tune on that and then the algorithm becomes, first we determine category and then we choose a separate fine-tuned model for that specific category. since they are all in the same category the fine tune will have less chance of degeneracy. Basically we partition the tool space so each reranker/classifier can be more narrow

**[p32]** but 0.80 means that one out of five tool calls will be wrong?

**[p33]** what if we have a handful of small LoRAs and we load one dynamically depending on the category

**[p39]** Okay, so let me explain what I want. What we want is, we, we have a prompt. And at the top of the prompt, we have some Lua, and it, it, it It has a list of Internal tool names that are local to the prompt, and then it associates each one of them with a description of what it needs. So right when the prompt loads up, it runs some Lua, and the Lua calls into the harness and says, "Here's a list of the tools that I need. Right? Then the description of the tool of what it needs to be able to do, and the user puts that string in there. And then I want it to use our contraption, our classifier, all that crap, to go through what's available. And figure out what's the best match. How do we do it?

**[p41]** so to be clear out system takes (need, description) strings and outputs a number from 0 to 1 ?

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

**[p73]** Let me explain to you what I want. I want like, I want a fresh. Directory. As a sibling, and I want all the training, I want all the evaluation data, like I want a beautiful clean dataset, and that's like, that's the final dataset that we can use. It's got the distractors, it's got the proper need strings. You said, I think you said two for each descriptor, or did you say three? And I wanna have it nice and clean. So that we can prove The numbers. And then there's enough there we're gonna do the implementation in the other repo. And I want a design doc. We need a, a design doc. The findings is nice, but we need the final design doc that explains it has enough to explain. I'm gonna give you the architect, and you can see what the architect wants. @tools-public/tools/architect.md

**[p75]** Plan and I want the design first, then build the dataset, then update thte design doc to have the reproduced numbers. How do you feel about that?

**[p76]** I think you are confused. The design doc is the design of the promptforge-mcp-toolpicker crate. That means, the tools.add, the tools.add_need, the choose_mcp_tool

**[p77]** I also want the plan to build out the final spike in the sibling dir (so we can run it later if things change), and to have the nice dataset with the need strings. it can copy over the dataset and put it in a very efficient representation (I dont want 16,000 files)

**[p78]** should we embed the mcp client?

**[p79]** the argument for making it a separate crate is that a coding LLM only has to consider a smaller amount of code, and it is morely to completely fit in a single context window.

**[p82]** the plan needs to mine this entire chat history to understand and explain the rationale this should go in a separate rationale.md document. it explains the tool scoping, how the model can pick the tool using choose_mcp_tool, the goto, all ofthat



## Plans

### MCP toolpicker design and dataset

*Produce the final design document for the MCP tool-picker (design-mcp-toolpicker.md), then build a clean, reproducible evaluation dataset in a fresh sibling directory, then reconcile the design doc's cited numbers with the reproduced results.*

Order (as requested): design doc first, then dataset, then reconcile. The architecture is already settled from the spike (FINDINGS.md); the dataset only firms up the accuracy figures the doc cites. Choices are written on the locked qualitative findings; specific figures are marked preliminary until reconciliation.

The design doc is forward-looking (no implementation code; normative artifacts only where they remove ambiguity), sourced from FINDINGS.md and this session, and built around ~12 load-bearing choices, each stated as decision + evidence + tension:

- Embeddings, not zero-shot NLI (the 0.97-synthetic vs 0.15-real reversal).
- bge-small / MiniLM interchangeable; small beats large here; CPU, deterministic, ~33-133 MB.
- Author-register correction: capability descriptions, not user utterances (0.99 vs 0.78).
- The real job is duplicate + absence detection, not the happy-path match (0.99 easy vs 0.79 hard, recall@3 0.93).
- Two surfaces: static launch-time `need_tool` binding; dynamic `choose_mcp_tool` deterministic top-k retriever + context rewrite; main model picks (no subcontext).
- Four-outcome resolution: clear bind / duplicate (fail loud on own catalog) / foreign-overlap (surface shortlist) / absence (fail loud); similarity-floor + top-2 margin, calibrated.
- Duplicate policy + prevalence (~11% cross-server at >=0.98) and MCP annotation tiebreaker.
- Optional model-tiered strong-select -> context-clearing goto -> cheap-execute.
- Resolver as its own crate; MCP client stays pure protocol.

Dataset decisions: real automatelab catalog (9,922 tools); needs are author-register paraphrases, 3 bands per tool (restatement / synonym / goal-abstracted), generated by multiple models; distractors in both regimes (random as ceiling, hard nearest-neighbor as real); true-duplicate neighbors (cosine >= 0.98) excluded from distractors and recorded as equivalent-golds (multi-gold); smoke-test ~300 tools to validate the pipeline and eyeball register, then the full 9,922 x 3 as the definitive artifact.

Decisions (made, correct me): 3 bands, not 5 - bands matter more than volume. Full-corpus final run with a 300-tool smoke test first. Multi-model generation.

Reconciliation principle: update the design doc's preliminary figures with the reproduced numbers; if any figure moves enough to threaten a design choice, flag it rather than silently patch.

Risks: generated needs drift from author register (mitigated by printing samples for eyeball before the full run); numbers shift on clean data (choices rest on qualitative findings, so only figures change); same-generator bias (multiple models + hard distractors, noted as a validity caveat).

[step list, record schema, and file-path inventory omitted]

## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge-design\mcp-classifier-spike\report\FINDINGS.md

# Tool-selection classifier spike: embeddings win, zero-shot NLI fails on real data

Verdict: use a small sentence-embedding model (cosine similarity) as the launch-time tool-selection matcher, not a zero-shot NLI classifier. On a bias-resistant test built from real MCP tools and independently-written needs, embeddings reached 0.81-0.85 top-1 and held up across both datasets, while zero-shot NLI - best (0.97) on a hand-authored set - collapsed to 0.15-0.48 top-1 on real data. NLI's authored-set showing was an artifact of shared vocabulary between needs and descriptions. A generative LLM (Claude Haiku) was best at 0.888 but only ~4 points above the best embedding model, at 15-50x the latency with a network dependency - at most an optional escalation, not the primary matcher. The CPU, run-once-at-startup, bundle-the-weights plan is still sound; it just wraps a small embedding model.

The reversal is the finding: synthetic data flattered NLI. distilbart scored 0.971 authored vs 0.154 real; embeddings barely moved (bge-base 0.853 to 0.846). NLI keyed on lexical alignment; independent phrasing broke it (spot check: the gold tool is present, simply mis-ranked by NLI while embeddings rank it first). Bigger NLI models did not rescue it (bart-large 0.351, DeBERTa-v3-large 0.335 on real) - a method limitation, not capacity. BM25 shows the same lesson in the lexical extreme: 0.794 authored, 0.516 real.

Abstention is usable with embeddings, and it is where the real cost sits: AUROC 0.85 on real; to keep wrong bindings under 5%, about half the needs auto-resolve and the rest must abstain (fail the launch, or fall back). The LLM does better (64% coverage at a 5% budget) but not dramatically. The real test used deliberately hard 40-tool catalogs; realistic deployments land above these numbers.

Speed and determinism: embedding is milliseconds on CPU; models are small (all-MiniLM ~90MB, bge-small ~130MB, bge-base ~440MB); output deterministic for a fixed model (triplicate run, max top-1 delta 0.0).

Recommendations: primary matcher bge-small-en-v1.5 or bge-base-en-v1.5 (bge-base most stable, bge-small the better size/speed trade), cosine, CPU, weights bundled, tool text enriched with name + description + parameter names; reject zero-shot NLI as the matcher (fragile: strong only when query vocabulary echoes the descriptions); keep the abstention gate (bind only above a calibrated cosine threshold, fail loud below; calibrate against a false-bind budget, not guessed); LLM escalation only for the low-confidence band, never the default; BM25 only fused with embeddings, never alone.

Threats to validity: needs generated by one LLM (Claude Haiku); catalogs fixed at 40 tools; one tool corpus skewed toward demo servers; a cross-encoder reranker over the top-k untested - the obvious next experiment if 0.85 is not enough.

[tables, checkpoint inventories, and test matrices omitted]

### c:\Users\Vinnie\src\cursor\promptforge-design\mcp-classifier-spike\README.md

A throwaway spike answering one question: will a classifier reliably map a prompt's English capability need to the right tool from connected MCP servers? Answer: yes with a small embedding model, no with zero-shot NLI. This is a spike: the code is disposable, the findings are the artifact.

[layout and reproduce-command inventory omitted]

### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\rationale.md

# Why the MCP tool-picker is shaped the way it is

The companion to design-mcp-toolpicker.md (the "what") and FINDINGS.md (the "numbers"); this document is the "why."

The problem: a promptforge prompt is a sectioned markdown document; each section can run Lua that scopes tools via `tools.add(...)`. We want a prompt to say in plain English what capability it needs, and have the harness bind that need to the right tool from whatever MCP servers are connected - or refuse cleanly. The question: can a small, local, deterministic classifier do that reliably, without an LLM in the resolution path?

Two surfaces sit on the executor's name-based `Tool` trait dispatch: `tools.add("name")` scopes an exact, known tool; `tools.add_need(alias, description)` declares a capability in English and the resolver binds the alias to a concrete tool at launch.

The single most important realization concerns the *register* of that description. Early evaluation used runtime user utterances ("find a hotel in Columbus Sept 12-15") as needs. That was wrong. The Lua need string is written by the prompt author, and an author writes a clean, parameter-free capability line that reads like a tool's own doc ("Retrieve a WG21 paper's markdown given the paper number"). Authors typically paraphrase the description of a tool they already intend to use. Matching author-register text to a tool is nearly trivial for embeddings because both sides are in the same register; the apparent difficulty first measured was an artifact of testing the wrong input distribution.

Why embeddings, and why not the clever alternatives - each tried on real tool catalogs:

- Zero-shot NLI: 0.97 top-1 on a hand-authored set, collapsed to 0.06-0.48 on real, independently-phrased needs; it keyed on shared vocabulary, and bigger/newer checkpoints were no better. Rejected. Lesson: a synthetic eval whose queries share words with the targets will flatter any lexical method.
- Sentence embeddings (bi-encoders): the only method robust across every dataset. bge-small and all-MiniLM-L6-v2 interchangeable; larger models did not reliably help and sometimes hurt on messy catalogs. Small, ~33-133 MB, CPU, deterministic. Chosen.
- BM25 / lexical word-count fusion: fusing with embeddings actively hurt (dropped top-1 ~15-18 points); equal-weight fusion lets the weaker lexical ranker pollute the strong one, and lexical cannot bridge synonyms, which is the whole problem. Rejected as a matcher; viable only as a minor signal, not a peer.
- Verb/noun structured channels (POS-split, compare separately): lowered accuracy at every weight, even on near-duplicates; the base embedding already separates read vs write, and POS tagging adds noise. Rejected.
- Hard category routing / mixture-of-experts: dropped top-1 from 0.84 to ~0.68; routing was only 0.72-0.80 accurate and every misroute discards the gold before any expert runs. Rejected as a hard filter; the soft top-k already narrows without the cliff.
- IDF "most important word" saliency (eyeballed on 30 real needs): grabs parameters (city names, dates) and filler, not the capability word - the rarest token is usually an argument, not the intent. Rejected as-is; the salient term is the action+object head, which embeddings already capture.
- Cross-encoder rerankers: modest, domain-dependent lift (can hurt on messy catalogs); optional, not core. A *fine-tuned* reranker is the lever if one is ever needed.

What the hard part actually is: matching among unrelated tools is ~0.99 top-1; among the gold's nearest neighbors ~0.79 top-1, but recall@3 stays ~0.93. Two facts shape the design: the right tool is almost always in the top-3, so surface a shortlist and let a well-informed decider settle the near-tie rather than force top-1; and the genuinely hard cases are near-duplicate disambiguation and absence - ~11% of tools in a broad multi-server catalog have a near-identical twin at cosine >= 0.98, almost all cross-server republishes. Hence the four-outcome resolution policy: clear bind; ambiguous within the author's own catalog (configuration error, fail loud); ambiguous from intentionally imported foreign/overlapping servers (surface the shortlist); nothing clears the floor (absence, fail loud). The gate is a calibrated similarity floor plus a top-1-vs-top-2 margin; MCP readOnlyHint/destructiveHint annotations break ties where present but are never required.

choose_mcp_tool's shape went through several revisions; the final form is the simplest:

- First idea: a fresh subcontext runs retrieval AND an LLM selects, returning one answer plus rationale (isolates untrusted descriptions, keeps the catalog out of the main context).
- Then: since the subcontext inference is already paid for, have it select rather than just retrieve (LLM over a top-k shortlist beats LLM over the whole catalog).
- Decisive simplification: drop the subcontext entirely. choose_mcp_tool becomes a deterministic, LLM-free embedding retriever returning the top-k (~3) descriptors; the harness injects them into the context; the *main model* picks as ordinary tool-calling.

The main model should do the choosing for systems reasons, not accuracy. The main context is already governed by the author (model choice, temperature, instructions, rewrite opt-out); a subcontext forces a new orphan configuration - which model, what budget, which vendor, what trace. Main-context selection reuses all of that, guarantees the model that selects a tool is the one that will use it (no chooser/executor capability mismatch), keeps one model and one trace, and holds full task history - exactly the context needed to break a near-duplicate tie the need string alone cannot. It is also the established tool-search pattern: retrieve candidates, load them, let the model call one.

choose_mcp_tool returns a tool *descriptor* (name, description, input schema), not an invocation, so the main model calls the tool itself with the task in view: one descriptor when confident, a small shortlist on a genuine tie (the clean way to hand duplicates to the better-informed decider), and "no tools available" on absence. The absence return is mandatory: a model handed only a shortlist over-binds (~23% false-bind measured), so it must see whether anything cleared the floor.

The context rewrite: on dynamic resolution the harness does not append the tool result; it rewrites the context so the chosen descriptor sits before the prompt prose and the entire discovery episode is removed, then re-generates - as if the model had been prompted with the tool already available. Payoff: a dynamically discovered tool lands in the identical execution state as a statically bound one - a single execution model, no divergence by surface. Bonus: untrusted candidate descriptions do not persist in the main context. Costs: a second inference pass and prefix-cache invalidation, both negligible for one-time-at-start discovery.

Model tiering: for genuinely hard selection, this composes with the context-clearing goto - a strong reasoning-model section calls choose_mcp_tool and disambiguates, a context-clearing goto passes the chosen descriptor into a fresh context, and a cheaper model executes. This is the "right" form of a selection subcontext because a section already has author-configured model selection - no new orphan config. Caveats: gate the reasoning step on expected ambiguity (common selection is trivial; routing everything through the expensive step overpays), and remember a deliberate chooser != executor reintroduces the capability mismatch (pass usage hints; reserve tiering for mechanically simple tools).

Two surfaces, one engine: static add_need and dynamic choose_mcp_tool are complementary, not competing; both sit on the same embedding engine. Static is deterministic, LLM-free, reproducible - for capabilities known at authoring time. Dynamic is model-driven and adaptive - for when the author cannot or will not enumerate needs. The context rewrite makes the dynamic path converge onto the static execution state.

Why the resolver is its own crate: promptforge-mcp-toolpicker depends on a thin promptforge-mcp-client for protocol and keeps all semantics (embeddings, four-outcome policy, Lua verbs, context rewrite) to itself. Reasons: the embedding model must not ride along with the protocol (the CLI is an MCP client of the promptforge-mcp server and should speak MCP without loading an embedding model it never uses); isolation and independent testing (resolver tests against synthetic catalogs with no network, client against a mock server with no model - the same reasoning that made webfetch its own crate); each crate stays context-window-sized so a coding LLM can hold a whole unit at once. Corollary design obligation: keep each crate lean with a crisp, documented public API, and do not over-fragment (that trades intra-crate context for inter-crate seam-juggling).

Deferred, on purpose:

- MCP sampling and roots: not implemented; sampling is deprecated upstream and would couple the resolver back to the model client. Deferred by not advertising the capability.
- Fine-tuning (contrastive embedding fine-tune, or fine-tuned/LoRA reranker): the lever to push past ~0.85 on hard disambiguation (expected ~0.88-0.93). Deferred until the zero-shot baseline proves insufficient; train on real (not same-generator) needs with hard negatives to avoid the bias that flattered NLI.
- Calibration: raw cosine is not a probability; the abstain budget is not a guarantee until a temperature/isotonic/conformal step is fitted. Deferred but noted as required for a hard budget.

### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\design-mcp-toolpicker.md

# Building the promptforge-mcp-toolpicker crate

Building this crate gives a promptforge prompt two ways to obtain an MCP tool for a capability described in plain English: a static, launch-time binding declared in Lua, and a dynamic, runtime discovery tool the model can call. Both are backed by one local, deterministic sentence-embedding engine over the connected servers' tool catalog, and both resolve through a single four-outcome policy (bind / duplicate / foreign-ambiguous / absent). The crate holds the resolution semantics and the Lua-facing API; it depends on a separate thin promptforge-mcp-client for protocol.

Executive summary: the author declares needs as capability descriptions - `tools.add_need("db", "run a read-only SQL query against the log database")`; at launch the crate embeds every connected tool's text, matches each need by cosine similarity, binds the alias when one wins clearly, and fails loud on own-catalog ambiguity or absence. For capabilities not known at authoring time, `tools.add("choose_mcp_tool")` opts into dynamic discovery: the model calls `choose_mcp_tool(need)`, a deterministic top-k retriever returns candidate descriptors, the harness rewrites the context so the chosen tool appears as if available from the start, and the main model calls it. Matching in the author register is near-trivial (preliminary top-1 ~0.99), so the engine's real work is duplicate and absence detection; the right tool is in the top-3 ~0.93 even among close competitors, so the design surfaces a shortlist rather than forcing a single guess. The matcher is small (bge-small-en-v1.5 or all-MiniLM-L6-v2, ~33-133 MB, CPU, deterministic); no LLM runs in the crate's own machinery.

Key design choices:

1. Local sentence embeddings are the matcher, not zero-shot NLI or lexical methods. Embeddings were the only approach robust across every real dataset; NLI looked strong on synthetic data and collapsed on real needs, and lexical fusion degraded the strong ranker. Tension: embeddings need a bundled model file, but it is small and deterministic.
2. bge-small-en-v1.5 and all-MiniLM-L6-v2 are interchangeable; the crate treats the model as configurable and defaults to bge-small. Larger models did not reliably help. Reversing this later is a config change, not a code change.
3. Needs are author-register capability descriptions, not user utterances. This is what a Lua author writes, and it makes matching near-trivial. The contract for add_need's description field is "a clean, parameter-free statement of what the tool does."
4. The real job is duplicate and absence detection, not the happy-path match. The engine is built around a four-outcome decision, and the abstain path (fail loud) is first-class, not an afterthought.
5. Resolution is a similarity floor plus a top-1-vs-top-2 margin. A clear winner binds; a thin margin means ambiguity; nothing above the floor means absence. Raw cosine is not a probability, so a calibration step is required before the floor can be a guaranteed error budget (deferred).
6. Duplicates within the author's own catalog are treated as configuration errors and fail loud; duplicates arising from intentionally imported foreign/overlapping servers surface a shortlist for disambiguation. MCP readOnlyHint/destructiveHint/idempotentHint annotations break ties where present but are never required.
7. tools.add_need is the static, launch-time, LLM-free surface; choose_mcp_tool is the dynamic, runtime surface. They are complementary and share the engine.
8. choose_mcp_tool is a deterministic embedding retriever, not an LLM. It returns descriptors; the main model does the choosing. This keeps the crate's machinery LLM-free and puts selection where the full task context and the author's model configuration already are.
9. On dynamic resolution the harness rewrites the context (chosen descriptor before the prose, discovery episode excised) so the dynamic path converges onto the static execution state. One execution model, regardless of surface.
10. The crate depends on a separate thin promptforge-mcp-client for protocol and owns only the semantics. Protocol consumers (such as the CLI) must not pull the embedding model, and each crate stays small enough for a coding LLM to hold whole.
11. An optional model-tiered configuration (strong-model select -> context-clearing goto -> cheap-model execute) exists for genuinely hard selection, gated on expected ambiguity.
12. MCP sampling and roots are not implemented (sampling is deprecated upstream); the crate does not advertise those capabilities.

Normative contracts:

- `tools.add_need(alias, description)` - declare a capability need. At launch the resolver binds alias to a concrete (server, tool) per the four-outcome policy; the bound alias is then usable exactly like a local tool name in tools.add. description is an author-register capability line (parameter-free). Errors at launch on ambiguity-in-own-catalog or absence.
- `choose_mcp_tool(need)` runs deterministic embed -> top-k over the connected catalog and returns one of: a single tool descriptor `{server, name, description, input_schema}` when one candidate clearly wins; a shortlist (2-3 descriptors) when the top candidates are a genuine near-tie (duplicates), for the main model to disambiguate with full task context; or `{error: "no tools available"}` when nothing clears the similarity floor. The harness then rewrites the context to place the returned descriptor(s) before the prompt prose, excising the call, and the main model calls the tool. The retriever result is cacheable by (need, catalog_hash).

Resolution engine: at startup, connect configured servers, snapshot each tools/list into a catalog of (server, name, description, input_schema, annotations), and embed each tool's enriched text (name + description + parameter names), cached by catalog hash. Per need or per choose_mcp_tool call: embed the need, cosine-rank the catalog, take top-k, apply the floor and margin, emit one of the four outcomes. Near-identical tools (cosine >= a duplicate threshold, roughly 0.98) are recorded as equivalent-golds so an equivalent pick is not treated as wrong.

Crate boundaries: depends on promptforge-core for the Tool trait and on promptforge-mcp-client for protocol. Owns: the embedding engine, the four-outcome policy, the Lua verbs, and the context-rewrite hook. Does not own: MCP transport/JSON-RPC (that is promptforge-mcp-client), or the model that does dynamic selection (that is the author's main-context model).

Evidence (preliminary, to be reconciled from the reproduced dataset): author-register match with random distractors top-1 ~0.99, recall@3 ~1.0; hard near-neighbor distractors top-1 ~0.79, recall@3 ~0.93; duplicate prevalence ~11% of a broad catalog has a >= 0.98 twin, overwhelmingly cross-server; bge-small ~ MiniLM at scale, larger models not reliably better.

[configuration shape and per-file inventories omitted]

### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\README.md + manifest.md

What the numbers mean: needs are author-register capability descriptions (what a Lua author writes), not user utterances. random distractors measure matching among unrelated tools (the easy ceiling); hard distractors are the gold's nearest neighbors (real disambiguation). Bands vary paraphrase distance (restatement / synonym / goal). The abstention sweep reports coverage vs accuracy at a false-bind budget on the hard regime.

Manifest: catalog is 9,922 real MCP tools (automatelab), id-indexed; 29,226 needs across 9,742 tools x 3 bands, generated by claude-haiku-4-5 and claude-sonnet-4-6 alternating; eval models bge-small-en-v1.5 and all-MiniLM-L6-v2; 39 distractors per case; duplicate threshold 0.98 with equivalent-golds excluded from distractors; seed 0.

[file layout, reproduce commands, and path inventories omitted]
