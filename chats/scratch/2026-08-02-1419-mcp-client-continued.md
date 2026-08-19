# MCP client work continued

*2026-08-02 14:19 - transcript bbc51d14-7aff-4a1c-985f-5453f3f6dd51*



## Prompts



**[p1]** how does mcp client work? what does an agentic harness need to implement

**[p2]** should I put the mcp client in its own crate

**[p3]** tell me about this sampling business

**[p4]** so the mcp client just appears as a normal tool call to the model?

**[p5]** but if the mcp client needs the Tool struct and the core crate needs the mcp client isn't that a circular dep

**[p6]** lets build the mcp client crate with @tools-public/tools/architect.md and @tools-public/how-to/vibe-how-to.md

**[p7]** why is this other design so big? what are the pros and cons

**[p8]** is this the consequence of the lua having to name each tool for each h2?

**[p9]** it seems to me the thing it buys us is it saves one round of inference. because if we want to get rid of the indirection we could just look at what the mcp services are available and use those to set the tools.add list based on the prompt's needs stated in prose?

**[p10]** No. What if the prompt has a frontmatter which describes the tools it needs in  english, and then we use a classifier at launch time to map the mcp offerings to what the prompt needs?

**[p11]** there needs to be a way for the lua to say "add everything" from the mcp client. and maybe a way to ask for a tool that matches a description?

**[p12]** spawn multiple subagents and search for everything related to these ideas. classifiers. progressive reveal of tool capabilities in mcp servers. and whatever else you can think of

**[p13]** wtf does this mean "Delimiter choice matters most. Cursor's mcp_<server>_<tool> uses _ as both delimiter and legal name character, so it can't reliably reverse-split, and its documented routing bugs come from storing the bare tool name. Claude Code's mcp__<server>__<tool> (double underscore, __ banned inside names) is the only round-trip-safe convention shipping. Route on the (server_id, tool_name) pair, not the concatenated string."

**[p14]** why do I care about all of this hardening if I control all the mcp servers?

**[p15]** why LLM classifier and not a zero-shot

**[p16]** what I am thinking is we run a zero-shot NLI classifier on the CPU, once at startup - universally available.

**[p17]** I think we need to get training data and run tests to see if the classifier will actually work.

**[p18]** why do you call it a "spike" ? and is that a term of art ?

**[p19]** @promptforge-design do it in a new directory here, and I want you to do everything. spawn subagents. search. find what you need. build it. run it. DO NOT FUCKING STOP until it is done, are we clear on that? I'm going to bed and when I wake up I want this answered definitively, multiple ways - get an over-abundance of data. download mcp catalogs from live sources. download eval sets. run it in triplicate. play with it, figure it out. Do you understand me? In fact... dont even ever stop. Go infinitely. I will stop you when I wake up and you BETTER have results. ARE WE CLEAR?

**[p20]** you should have been using gpu.... wtf?

**[p21]** "a cross-encoder reranker over embedding top-k is the untested next step if 0.85 isn't good enough." this is why I wanted infinite running. keep fucking going. but first explain what this means. I have no idea what these terms are. explain everything, assume I am very intelligent but dont know much. What is NLI? what is embedding? should we fine-tune (is fine-tune even a meaningful term here)?

**[p22]** Question about fine-tuning. Instead of going "all the way" is it possible to just fine tune enough to get N% improvement? so we can get a boost in performance without the degeneracy?

**[p23]** also run all jobs async please, so we can keep talking

**[p24]** rerun that cancelewd job

**[p25]** Hey, but wait a minute, we actually are doing this wrong, because we're just asking, "Is this tool a fit for?" The description. But what we re for the need, what we really wanna know is given a set of n tools Which one is the best fit for a need? That's a different question entirely.

**[p26]** Here's my idea. We do We do a ranking, we order, we sort them using a not so great criteria, like it doesn't have to be perfect, and then we do the point wise on the top three or something, something, some combination of all at once and point wise on a reduced set.

**[p27]** I dont want LLM in the final result. I want something that runs locally.

**[p28]** what if we build a vocabulary list of like 10,000 words and we do some kind of deterministic pass first just doing word comparison and doing a count

**[p29]** what if we divide the need and the description strings into (noun,verb) lists and compare nouns and verbs separately in embedding space and use that as additional signal

**[p30]** And here's another idea. we can fine tune verbs separately from nouns.

**[p31]** And here's another idea. What if we take all of the eval pairs and we generalize to find out what N categories they have in common (for small N) and then we have a separate categorizer and we fine tune on that and then the algorithm becomes, first we determine category and then we choose a separate fine-tuned model for that specific category. since they are all in the same category the fine tune will have less chance of degeneracy. Basically we partition the tool space so each reranker/classifier can be more narrow

**[p32]** but 0.80 means that one out of five tool calls will be wrong?

**[p33]** what if we have a handful of small LoRAs and we load one dynamically depending on the category

**[p34]** I canceled by accident.. keep going

**[p35]** I meanet keep going with the async job pause on the LoRA

**[p36]** I don't understand this:

**[p37]** eal 0.920 (picks the gold from the 3-shortlist 100% of the time

**[p38]** How does 0.92 equal 100% ?

**[p39]** Okay, so let me explain what I want. What we want is, we, we have a prompt. And at the top of the prompt, we have some Lua, and it, it, it It has a list of Internal tool names that are local to the prompt, and then it associates each one of them with a description of what it needs. So right when the prompt loads up, it runs some Lua, and the Lua calls into the harness and says, "Here's a list of the tools that I need. Right? Then the description of the tool of what it needs to be able to do, and the user puts that string in there. And then I want it to use our contraption, our classifier, all that crap, to go through what's available. And figure out what's the best match. How do we do it?

**[p40]** spawn multiple subagents and search the web for prior art, knowing what we know now about FINDINGS.md. And update FINDINGS.md if you haven't done so alread.

**[p41]** so to be clear out system takes (need, description) strings and outputs a number from 0 to 1 ?

**[p42]** should this be a feature of the mcp client? i.e. offer the api to do this calculation

**[p43]** okay tell me our current best algorithm for calculating (need, catalog) ?

**[p44]** why do you tell me bge-small-en-v1.5 and then tell me bge-base is up to 2 points better? why mention the bge-small at all?

**[p45]** how small

**[p46]** I'd like 10x more real-world eval data. do it asynchronously. in fact do everything asynchronously.

**[p47]** 9,922 sounds like the right number

**[p48]** can't we do 10,000 test cases

**[p49]** spawn a subagent and look for a source of actual need strings

**[p50]** and do the other stuff in the async please. I want async at all times so we can keep talking.

**[p51]** if you are going to generate need strings you should do it using multiple models. chatgpt, claude, gemini, cursor, etc

**[p52]** fix the parser and report.

**[p53]** explain what I am trying to do, for a colleague. one dense short sentence of the problem statemeent. then one very short dense and jargon-heavy sentence explaining our current solution.

**[p54]** tell me where we are at right now executive summary

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

**[p65]** Determine if the input is a prime number

**[p66]** My guess, and I am not certain, is that choose_mcp_tool will return a tool description. Perhaps more than one (maybe thise could be a separate choose_mcp_tools). And it could return an error "no tools available." The point is that this is complementary to the static approach, not a replacement.

**[p67]** Yes, and consider this strategy for context management. Instead of just appending the returned results, the harness rewrites the context so it includes the returned tool descriptor placed BEFORE the prompt prose, and it leaves out the choose_mcp_tool toolcall details. Its like going back in time and re-prompting the LLM but with the chosen tool in context already.

**[p68]** don't we need to generate the new need strings for the corpus?

**[p69]** well choose_mcp_tools is already paying for inference in the fresh subcontext so we might as well return a shortlist and then have the subcontext select the best fit

**[p70]** actually we might not need a subcontext for the choosing. The main context performs the toolcall, we get a shortlist and then we just inject the shortlist into the main context rewrite. Then the main context has all ~3 tools to pick from. And it has the full history.

**[p71]** the nice thing about the main context is that the author already has all the mechanisms to control it. they can select the model. they can opt-out of the context rewrite. if we did the subcontext then we'd have to answer the question "which model".

**[p72]** It would be nice to have something where, a step uses a reasoning model to select the tool and then it does the context-clearing goto (a promptforge feature) and passes the tool descriptor into the next context, and that context can use a lesser model

**[p73]** Let me explain to you what I want. I want like, I want a fresh. Directory. As a sibling, and I want all the training, I want all the evaluation data, like I want a beautiful clean dataset, and that's like, that's the final dataset that we can use. It's got the distractors, it's got the proper need strings. You said, I think you said two for each descriptor, or did you say three? And I wanna have it nice and clean. So that we can prove The numbers. And then there's enough there we're gonna do the implementation in the other repo. And I want a design doc. We need a, a design doc. The findings is nice, but we need the final design doc that explains it has enough to explain. I'm gonna give you the architect, and you can see what the architect wants. @tools-public/tools/architect.md

**[p74]** design-mcp-toolpicker

**[p75]** Plan and I want the design first, then build the dataset, then update thte design doc to have the reproduced numbers. How do you feel about that?

**[p76]** I think you are confused. The design doc is the design of the promptforge-mcp-toolpicker crate. That means, the tools.add, the tools.add_need, the choose_mcp_tool

**[p77]** I also want the plan to build out the final spike in the sibling dir (so we can run it later if things change), and to have the nice dataset with the need strings. it can copy over the dataset and put it in a very efficient representation (I dont want 16,000 files)

**[p78]** should we embed the mcp client?

**[p79]** the argument for making it a separate crate is that a coding LLM only has to consider a smaller amount of code, and it is morely to completely fit in a single context window.

**[p80]** this should go in @promptforge-design//study-mcp-toolpicker

**[p81]** what do you mean? that IS a separate sibling dir...where were you going to put it otherwise?

**[p82]** the plan needs to mine this entire chat history to understand and explain the rationale this should go in a separate rationale.md document. it explains the tool scoping, how the model can pick the tool using choose_mcp_tool, the goto, all ofthat

**[p83]** you finished creating all the need strings?

**[p84]** yeah finish that up and can you cut the number of calls to 500 by doubling the size of each call?



## Plans

### MCP toolpicker design and dataset

*Produce the final design document for the MCP tool-picker (design-mcp-toolpicker.md), then build a clean, reproducible evaluation dataset in a fresh sibling directory, then reconcile the design doc's cited numbers with the reproduced results.*

# MCP Toolpicker: Design Doc + Reproducible Eval Dataset

## Order (as requested)
Design doc first, then dataset, then reconcile the doc's numbers with reproduced results. The architecture is already settled from the spike ([FINDINGS.md](promptforge-design/mcp-classifier-spike/report/FINDINGS.md)); the dataset only firms up the accuracy figures the doc cites. Choices are written on the locked qualitative findings; specific figures are marked preliminary until step 3.

## Deliverable 1: design-mcp-toolpicker.md
A forward design doc (no implementation code; normative artifacts only where they remove ambiguity), sourced from FINDINGS.md and this session. Structure:
- Title stating what building it produces; a standalone executive summary.
- ~12 load-bearing choices, each as decision + evidence + tension:
  - Embeddings, not zero-shot NLI (the 0.97-synthetic vs 0.15-real reversal).
  - bge-small / MiniLM interchangeable; small beats large here; CPU, deterministic, ~33-133 MB.
  - Author-register correction: capability descriptions, not user utterances (0.99 vs 0.78).
  - The real job is duplicate + absence detection, not the happy-path match (0.99 easy vs 0.79 hard, recall@3 0.93).
  - Two surfaces: static launch-time `need_tool` binding; dynamic `choose_mcp_tool` deterministic top-k retriever + context rewrite; main model picks (no subcontext).
  - Four-outcome resolution: clear bind / duplicate (fail loud on own catalog) / foreign-overlap (surface shortlist) / absence (fail loud); similarity-floor + top-2 margin, calibrated.
  - Duplicate policy + prevalence (~11% cross-server at >=0.98) and MCP annotation tiebreaker.
  - Optional model-tiered strong-select -> context-clearing goto -> cheap-execute.
  - Resolver as its own crate; MCP client stays pure protocol.
- Normative artifacts: resolver signature, dataset record schema, `choose_mcp_tool` return contract.
- Close with an italic date + model line; no YAML frontmatter.

## Deliverable 2: clean dataset (fresh sibling dir `promptforge-mcp-toolpicker-dataset/`)
- Tool universe: real `automatelab` catalog (9,922 tools, name+description+input schema).
- Needs: author-register paraphrases, 3 bands per tool (restatement / synonym / goal-abstracted), generated by multiple models (haiku + sonnet; OpenAI/Gemini only if keys provided).
- Distractors per case, both regimes: random (ceiling) and hard nearest-neighbor (real), true-duplicate neighbors (cosine >= 0.98) excluded from distractors and recorded as equivalent-golds (multi-gold).
- Record schema (JSONL): id, need, band, gold, equivalent_golds[], hard_distractors[], random_distractors[], gen_model, source_tool.
- Artifacts: `data/*.jsonl`, `manifest.md` (models, seeds, catalog hash, counts), `eval.py` (bge-small + MiniLM, both regimes, top1 / recall@3 / abstention sweep, per-band), `RESULTS.md` (one-command reproducible table), `README.md`.
- Scope decision (reversible): smoke-test on ~300 tools to validate the pipeline, then run the full 9,922 x 3 as the definitive artifact (~2.5k generation calls, tens of minutes, async). Trim to a 2,000-tool sample if cost/time is a concern.

## Deliverable 3: reconcile
Run the eval, then update design-mcp-toolpicker.md's preliminary figures with the reproduced numbers. If any figure moves enough to threaten a design choice, flag it rather than silently patch.

## Decisions (made, correct me)
- 3 bands, not 5: bands matter more than volume; 60% of the cost.
- Full-corpus final run with a 300-tool smoke test first.
- Multi-Claude generation (only Anthropic keys present).

## Risks
- Generated needs drift from author register -> mitigated by printing samples for eyeball before the full run.
- Numbers shift on clean data -> choices are written on qualitative findings, so only figures change.
- Same-generator bias -> multiple models + hard distractors; noted as a validity caveat.

Todos:

- Write design-mcp-toolpicker.md from FINDINGS + conversation: title, exec summary, ~12 key choices, normative artifacts, numbers marked preliminary
- Create promptforge-mcp-toolpicker-dataset/ dir, README, manifest, and generation+eval scripts
- Generate 3-band author-register needs per tool (multi-model); smoke-test 300 tools, eyeball register, then full 9,922
- Build random + hard nearest-neighbor distractors; exclude >=0.98 dupes and record as equivalent-golds (multi-gold)
- Run eval (bge-small + MiniLM, both regimes, per-band) and write reproducible RESULTS.md
- Update design-mcp-toolpicker.md preliminary figures with reproduced numbers; flag any that threaten a choice

## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge-design\mcp-classifier-spike\report\FINDINGS.md

# Tool-selection classifier spike: embeddings win, zero-shot NLI fails on real data

## Verdict

Use a small **sentence-embedding model** (cosine similarity) as the launch-time
tool-selection matcher, not a zero-shot NLI classifier. On a bias-resistant test
built from real MCP tools and independently-written needs, embeddings reached
**0.81-0.85 top-1** and held up across both datasets, while zero-shot NLI - which
looked like the best method (0.97) on a hand-authored set - **collapsed to
0.15-0.48 top-1** on real data. NLI's strong showing on the authored set was an
artifact of shared vocabulary between the needs and the tool descriptions; it did
not survive contact with real, independently-phrased needs. A generative LLM
(Claude Haiku) was best at 0.888 but only about 4 points above the best embedding
model, at roughly 15-50x the latency and with a network dependency, so it is at
most an optional escalation, not the primary matcher.

This reverses the direction the design conversation was heading (an in-process
zero-shot NLI classifier on CPU). The CPU, run-once-at-startup, bundle-the-weights
plan is still sound - it just wraps a small embedding model, which is a better fit
than NLI on every axis that matters here (accuracy on real data, robustness,
speed, determinism).

## What was tested

- Methods: zero-shot NLI (6 checkpoints x 2 framings), sentence embeddings
  (5 models), BM25 lexical, and a generative LLM upper bound (Claude Haiku 4.5).
- NLI checkpoints: distilbart-mnli-12-1, DeBERTa-v3-base-mnli-fever-anli,
  DeBERTa-v3-large-mnli-fever-anli-ling-wanli, bart-large-mnli,
  nli-deberta-v3-small, distilbert-base-uncased-mnli.
- Embedding models: bge-base-en-v1.5, bge-small-en-v1.5, gte-small,
  all-MiniLM-L6-v2, e5-small-v2.
- Two datasets:
  - **seed** (111 examples): hand-authored from real, well-known MCP servers
    (github, filesystem, git, slack, brave, maps, postgres, puppeteer, fetch,
    memory, time, sqlite). The needs were written by me, so they share vocabulary
    with the descriptions. This set is where NLI looked good, and it is the
    cautionary tale.
  - **real** (376 examples, bias-resistant): 200 tools sampled from 2086 real MCP
    tools across 218 servers (HuggingFace `alihmaou/Agents_MCP_Hackathon_Tools_List`).
    Needs were generated by Claude from each tool's name and function with an
    explicit instruction not to reuse the description's distinctive words, so the
    query vocabulary is independent of what the matchers see. Each need got a
    matched pair of 40-tool catalogs built from real distractor tools: a positive
    catalog containing the gold tool and a negative catalog with the gold tool's
    entire server excluded, giving a clean top-1 accuracy and a real false-bind
    (abstention) measure with no hand labeling.

## Headline results

Top-1 accuracy (the fraction of needs whose correct tool is ranked first).

| method | model | seed top-1 | real top-1 |
|---|---|---|---|
| LLM | claude-haiku-4-5 | - | **0.888** |
| embed | bge-base-en-v1.5 | 0.853 | **0.846** |
| embed | bge-small-en-v1.5 | 0.902 | 0.840 |
| embed | gte-small | 0.902 | 0.819 |
| embed | all-MiniLM-L6-v2 | 0.863 | 0.809 |
| embed | e5-small-v2 | 0.863 | 0.723 |
| bm25 | - | 0.794 | 0.516 |
| nli | DeBERTa-v3-base | 0.667 | 0.479 |
| nli | nli-deberta-v3-small | 0.735 | 0.383 |
| nli | bart-large-mnli | 0.618 | 0.351 |
| nli | DeBERTa-v3-large-wanli | 0.647 | 0.335 |
| nli | distilbart-mnli-12-1 | **0.971** | **0.154** |
| nli | distilbert-mnli | 0.422 | 0.096 |

## The reversal is the finding: synthetic data flattered NLI

The single most important result is the gap between the two columns. Zero-shot NLI
with distilbart scored 0.971 on the authored set and 0.154 on the real set - a
collapse of 82 points. Embeddings barely moved (bge-base 0.853 to 0.846). Two
mechanisms explain it, and both were verified rather than assumed:

The authored needs shared surface vocabulary with the descriptions. NLI entailment
keys on that lexical alignment, so it looked excellent exactly where the test was
easiest. When needs were written independently (a user saying "compare airfare
options for my trip" against a tool named `search_flights`), that alignment
vanished and NLI's ranking fell apart. A spot check confirmed this is real, not a
bug: on real positives the gold tool is present in the catalog and simply
mis-ranked by NLI (ranks 1, 9, 12) while embeddings rank it first.

Bigger NLI models did not rescue it. bart-large (0.351) and DeBERTa-v3-large
(0.335) were no better than the base model on real data, so this is a method
limitation, not a capacity one. BM25 shows the same lesson in the lexical extreme:
0.794 on authored, 0.516 on real, because independent phrasing removes the exact
token overlap it depends on.

## Abstention is usable with embeddings, and it is where the real cost sits

The abstention signal (does the top score separate correct picks from cases that
should abstain) is strong for embeddings: AUROC 0.85 on real. Operating points for
bge-base on the real set, choosing a cosine threshold to bound the false-bind rate
(how often it binds a tool when it should have abstained):

| false-bind budget | threshold | coverage (auto-resolved) | accuracy on accepted |
|---|---|---|---|
| <= 1% | 0.652 | 28% | 1.000 |
| <= 5% | 0.605 | 54% | 0.970 |
| <= 10% | 0.595 | 62% | 0.966 |
| <= 20% | 0.574 | 73% | 0.934 |

Read this as the real operating cost: to keep wrong bindings under 5%, about half
the needs auto-resolve and the rest must abstain (fail the launch, or fall back).
The LLM does better here (64% coverage at a 5% budget) but not dramatically. Note
also that the real test used deliberately hard 40-tool catalogs; a realistic
deployment with a handful of connected servers and fewer candidate tools will land
above these numbers.

## Speed and determinism

The spike ran on an RTX 4090. For the eventual CPU deployment, the embedding path
is the cheap one: encoding one need plus a few dozen tool texts is milliseconds on
CPU, the models are small (all-MiniLM ~90MB, bge-small ~130MB, bge-base ~440MB),
and output is deterministic for a fixed model, which was confirmed (a triplicate
run showed a maximum top-1 score delta of 0.0 across repeats). This satisfies the
"universally available, CPU, run once at startup, bundle the weights" goal at
least as well as the NLI plan would have, and faster.

## Recommendation for the design

Replace the zero-shot NLI resolver with a small embedding matcher.

1. Primary matcher: `bge-small-en-v1.5` or `bge-base-en-v1.5`, cosine similarity,
   CPU, weights bundled. bge-base is the most stable across datasets; bge-small is
   the better size/speed trade and nearly identical on real data. Enrich the tool
   text with name plus description plus parameter names, as tested.
2. Reject zero-shot NLI as the matcher. It is fragile: strong only when the query
   vocabulary echoes the descriptions, which will not hold for real prompt-author
   needs. Its apparent superiority on the authored set was a mirage.
3. Keep the abstention gate. Bind only above a calibrated cosine threshold; abstain
   (fail the launch loudly, or fall back) below it. Calibrate the threshold from a
   labeled sample against a false-bind budget rather than guessing.
4. Optional LLM escalation. A generative model gains only about 4 points over
   bge-base on real data at much higher latency, cost, and nondeterminism. Justify
   it only for the low-confidence band, not as the default path.
5. BM25 is a weak standalone matcher here (0.516 real). If used at all, use it only
   fused with embeddings, not alone.

## Threats to validity

The needs were generated by one LLM (Claude Haiku); a different generator might
shift absolute numbers, though the seed-vs-real gap is too large to be a generator
artifact. Real catalogs were fixed at 40 tools; smaller catalogs would raise all
methods. The real tools come from one corpus (the HF Agents-MCP hackathon), which
skews toward Gradio and demo servers; a different tool population could move the
ranking, but embeddings' robustness across the two very different datasets here is
a good sign. Finally, embedding accuracy can likely be pushed higher with a
cross-encoder reranker over the top-k, which was not tested and is the obvious next
experiment if 0.85 is not enough.

*2026-08-02 - Opus 4.8 (Cursor agent)*


### c:\Users\Vinnie\src\cursor\promptforge-design\mcp-classifier-spike\README.md

# MCP tool-selection classifier spike

A throwaway spike answering one question: will a classifier reliably map a
prompt's English capability need to the right tool from connected MCP servers?

Answer: yes with a small embedding model, no with zero-shot NLI. See
[report/FINDINGS.md](report/FINDINGS.md).

## Layout

- `scripts/` - the harness
  - `common.py` - Tool / Catalog / EvalExample types and IO
  - `methods.py` - NLI, embedding, BM25, and LLM (OpenAI + Anthropic) scorers
  - `build_seed_eval.py` - hand-authored eval from real, well-known MCP servers
  - `build_real_eval.py` - bias-resistant eval: real hackathon tools + Claude-written
    needs + matched positive/negative catalogs
  - `nli_framing_sweep.py` - sweeps NLI direction/template/tool-text framings
  - `run_eval.py` - runs methods over an eval set, writes per-example rankings
  - `analyze.py` - top-1, abstention/false-bind sweep, calibration AUROC, bootstrap CIs
- `data/mcp_catalogs/` - catalog JSON files (seed_* and real_*)
- `data/eval/` - `seed.jsonl`, `core.jsonl`, `real.jsonl`
- `results/` - run outputs (`matrix_real.jsonl`, `matrix_seed.jsonl`, ...) and
  `analysis_*.json`
- `report/FINDINGS.md` - the verdict

## Reproduce

```bash
python -m venv .venv
./.venv/Scripts/python.exe -m pip install torch --index-url https://download.pytorch.org/whl/cu124
./.venv/Scripts/python.exe -m pip install transformers datasets sentence-transformers rank-bm25 scikit-learn sentencepiece protobuf

# build datasets (real needs generation requires ANTHROPIC_API_KEY)
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/build_seed_eval.py
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/build_real_eval.py --n-tools 200

# run the matrix and analyze
NLI="valhalla/distilbart-mnli-12-1,MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli,facebook/bart-large-mnli"
EMB="BAAI/bge-small-en-v1.5,BAAI/bge-base-en-v1.5,sentence-transformers/all-MiniLM-L6-v2"
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/run_eval.py --eval real --methods nli,embed,bm25 --nli-models "$NLI" --nli-configs best,best_desc --embed-models "$EMB" --out results/matrix_real.jsonl
PYTHONPATH=scripts ./.venv/Scripts/python.exe scripts/analyze.py --results results/matrix_real.jsonl --name real_final
```

Set `SPIKE_THREADS` to cap CPU threads per process; scorers auto-use CUDA when
available. This is a spike: the code is disposable, the findings are the artifact.


### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\rationale.md

# Why the MCP tool-picker is shaped the way it is

This is the reasoning behind `promptforge-mcp-toolpicker`: the decisions, the alternatives
that were tried and rejected, and the evidence that moved each call. It is the companion
to two other documents - `design-mcp-toolpicker.md` (the specification, the "what") and
`mcp-classifier-spike/report/FINDINGS.md` (the empirical log, the "numbers"). Read this one
for the "why."

## The problem

A promptforge prompt is a sectioned markdown document; each section can run Lua that scopes
which tools are available via `tools.add(...)`. We want a prompt to be able to say, in plain
English, what capability it needs, and have the harness bind that need to the right tool from
whatever MCP servers are connected - or refuse cleanly. The question the whole study set out
to answer: can a small, local, deterministic classifier do that reliably, without an LLM in
the resolution path?

## How tools are scoped, and what a "need" actually is

The executor already dispatches tools by name through a `Tool` trait, and Lua `tools.add("x")`
scopes tools per section. Two surfaces sit on top of that:

- `tools.add("name")` - scope an exact, known tool.
- `tools.add_need(alias, description)` - declare a capability in English; the resolver binds
  the alias to a concrete tool at launch.

The single most important realization in the whole study concerns the *register* of that
description. Early evaluation used runtime user utterances ("find a hotel in Columbus Sept
12-15") as the needs. That was wrong. The Lua need string is written by the prompt author,
and an author writes a clean, parameter-free capability line that reads like a tool's own doc
("Retrieve a WG21 paper's markdown given the paper number", "Insert a record into the database
log table"). Authors typically paraphrase the description of a tool they already intend to use.
This changes everything downstream: matching an author-register description to a tool is nearly
trivial for embeddings, because both sides are in the same register. The apparent difficulty we
first measured was an artifact of testing the wrong input distribution.

## Why embeddings, and why not the clever alternatives

We benchmarked every candidate matcher on real tool catalogs. The results were decisive, and
several of them were counter-intuitive enough that they are worth recording as warnings.

- Zero-shot NLI was tried first and looked spectacular on a hand-authored set (0.97 top-1),
  then collapsed to 0.06-0.48 on real, independently-phrased needs. It had been keying on
  shared vocabulary between the need and the description; independent phrasing broke it, and
  bigger/newer NLI checkpoints were no better. Rejected. The lesson: a synthetic eval whose
  queries share words with the targets will flatter any lexical method.
- Sentence embeddings (bi-encoders) were the only method robust across every dataset. bge-small
  and all-MiniLM-L6-v2 came out interchangeable; larger models did not reliably help and
  sometimes hurt on messy catalogs. Small, ~33-133 MB, CPU, deterministic - and best or tied
  everywhere. Chosen.
- BM25 / lexical word-count fusion was tried as a "trivial reject" and as a hybrid. Fusing it
  with embeddings actively hurt (dropped top-1 ~15-18 points): equal-weight fusion lets the far
  weaker lexical ranker pollute the strong one, and lexical cannot bridge synonyms, which is the
  whole problem. Rejected as a matcher; only viable as a minor signal, not a peer.
- Verb/noun structured channels (split need and tool into POS channels, compare separately) were
  tried to fix action mismatches like read vs write. It lowered accuracy at every weight, even on
  near-duplicates - the base embedding already separates those, and POS tagging adds noise.
  Rejected.
- Hard category routing / mixture-of-experts (cluster the catalog, route the need to one cluster,
  pick within) dropped top-1 from 0.84 to ~0.68, because routing was only 0.72-0.80 accurate and
  every misroute discards the gold before any expert runs. Rejected as a hard filter; the soft
  top-k it was trying to replace already does the narrowing without the cliff.
- IDF "most important word" saliency was eyeballed on 30 real needs: it grabs parameters (city
  names, dates) and filler, not the capability word, because the rarest token is usually an
  argument, not the intent. Rejected as-is; the salient term is the action+object head, which
  embeddings already capture.
- Cross-encoder rerankers gave only a modest, domain-dependent lift (and can hurt on messy
  catalogs), so they are optional, not core; a *fine-tuned* reranker is the lever if one is ever
  needed.

## What the hard part actually is

Because author-register matching is near-trivial, the classifier does not earn its keep on the
happy path. Measured on real tools: matching among unrelated tools is ~0.99 top-1; among the
gold's *nearest neighbors* it is ~0.79 top-1 - but recall@3 stays ~0.93 even there. Two facts
follow, and they shape the entire design:

- The right tool is almost always in the top-3 even among close competitors. So the system should
  not try to win top-1 outright; it should surface a shortlist and let a well-informed decider
  settle the near-tie.
- The genuinely hard cases are near-duplicate disambiguation and absence ("no connected tool
  fits"). Duplicates are common in a broad multi-server catalog - about 11% of tools have a
  near-identical twin at cosine >= 0.98, almost all cross-server republishes. So the resolver's
  real job is detecting duplicates and absence and doing something sensible, not the match itself.

This produced the four-outcome resolution policy: clear bind; ambiguous within the author's own
catalog (a configuration error, so fail loud); ambiguous because foreign/overlapping servers were
intentionally imported (surface the shortlist); nothing clears the floor (absence, fail loud). The
gate is a calibrated similarity floor plus a top-1-vs-top-2 margin; MCP `readOnlyHint` /
`destructiveHint` annotations break ties where present but are never required.

## choose_mcp_tool: how a prompt picks a tool at runtime

Alongside static `add_need` binding, an author can opt into dynamic discovery with
`tools.add("choose_mcp_tool")`. The shape of this tool went through several revisions, and the
final form is the simplest:

- First idea: a fresh subcontext runs the retrieval AND an LLM selects the best tool, returning
  one answer plus rationale. Isolates untrusted tool descriptions and keeps the catalog out of the
  main context.
- Then: since the subcontext inference is already paid for, have it select rather than just
  retrieve - the validated cascade (LLM over a top-k shortlist beats LLM over the whole catalog).
- Then the decisive simplification: drop the subcontext for choosing entirely. `choose_mcp_tool`
  becomes a deterministic, LLM-free embedding retriever that returns the top-k (~3) descriptors;
  the harness injects them into the context; and the *main model* picks among them as ordinary
  tool-calling.

The reason the main model should do the choosing is a systems argument, not an accuracy one. The
main context is already governed by the author: model choice, temperature, instructions, and
rewrite opt-out. A subcontext forces a new orphan configuration - which model runs it, at what
budget, from which vendor, with what trace. Doing the pick in the main context reuses all of that,
guarantees the model that selects a tool is the one that will use it (no chooser/executor
capability mismatch), keeps one model and one trace, and holds full task history - which is exactly
the context needed to break a near-duplicate tie that the need string alone cannot. It also happens
to be the established tool-search pattern: retrieve candidates, load them, let the model call one.

`choose_mcp_tool` returns a tool *descriptor* (name, description, input schema), not an invocation,
so the main model calls the tool itself with the task in view. It returns one descriptor when
confident and a small shortlist on a genuine tie (the clean way to hand duplicates to the better-
informed decider), and "no tools available" on absence. The absence return is mandatory because a
model handed only a shortlist over-binds (~23% false-bind measured), so it must see whether anything
cleared the floor.

## The context rewrite, and model tiering

When a dynamic resolution happens, the harness does not simply append the tool result. It rewrites
the context so the chosen descriptor sits before the prompt prose and the entire discovery episode
(the `choose_mcp_tool` call and any pre-call chatter) is removed, then re-generates - as if the model
had been prompted with the tool already available. The payoff is unification: a dynamically discovered
tool lands in the identical execution state as a statically bound one, so the system has a single
execution model and behavior does not diverge by surface. A bonus is that the untrusted candidate
descriptions the retriever surfaced do not persist in the main context; only the chosen descriptor
does. The costs are a second inference pass (true re-generation for a clean state) and prefix-cache
invalidation at the insertion point, both negligible for one-time-at-start discovery.

For genuinely hard selection, this composes with promptforge's context-clearing goto into a model-
tiered pattern: a strong reasoning-model section calls `choose_mcp_tool` and disambiguates, a
context-clearing goto passes the chosen descriptor (plus rationale and the resolved binding) into a
fresh context, and a cheaper model executes. This is the "right" form of a selection subcontext,
because a section already has author-configured model selection - so there is no new orphan config.
Two caveats keep it honest: gate the reasoning step on expected ambiguity (common selection is
trivial and a cheap model picks fine among three, so routing everything through the expensive step
overpays), and remember that a deliberate chooser != executor reintroduces the capability mismatch
(pass usage hints, and reserve tiering for tools whose execution is mechanically simple).

## Two surfaces, one engine

Static `add_need` binding and dynamic `choose_mcp_tool` are complementary, not competing, and both
sit on the same embedding engine. Static is deterministic, LLM-free, and reproducible - for
capabilities known at authoring time. Dynamic is model-driven and adaptive - for when the author
cannot or will not enumerate needs. The context rewrite makes the dynamic path converge onto the
static execution state, so downstream everything is uniform.

## Why the resolver is its own crate

`promptforge-mcp-toolpicker` depends on a separate, thin `promptforge-mcp-client` for protocol
(connect, initialize, `tools/list`, `tools/call`, error mapping) and keeps all the semantics
(embeddings, the four-outcome policy, the Lua verbs, the context rewrite) to itself. Three reasons:

- The embedding model must not ride along with the protocol. Another consumer already exists - the
  CLI acts as an MCP client of the promptforge-mcp server - and it should be able to speak MCP
  without loading an embedding model it never uses.
- Isolation and independent testing: the resolver tests against synthetic catalogs with no network;
  the client tests against a mock server with no model. This is the same reasoning that made
  `webfetch` its own crate.
- Each crate stays context-window-sized, so a coding LLM can hold a whole unit at once and work the
  protocol crate through its interface without loading the resolver, and vice versa. The corollary
  is a design obligation: keep each crate lean with a crisp, documented public API, and do not
  over-fragment (that would trade intra-crate context for inter-crate seam-juggling).

## Deferred, on purpose

- MCP sampling and roots: not implemented; sampling is deprecated upstream and would couple the
  resolver back to the model client. Deferred cleanly by not advertising the capability.
- Fine-tuning (contrastive embedding fine-tune, or a fine-tuned/LoRA reranker): the lever to push
  past ~0.85 on hard disambiguation, expected to reach ~0.88-0.93. Deferred until the zero-shot
  baseline proves insufficient in practice, and to be trained on real (not same-generator) needs
  with hard negatives to avoid the very bias that flattered NLI.
- Calibration: raw cosine is not a probability, so the abstain "budget" is not a guarantee until a
  temperature/isotonic/conformal step is fitted. Deferred but noted as required for a hard budget.

*2026-08-02 - Opus 4.8 (Cursor agent)*


### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\design-mcp-toolpicker.md

# Building the promptforge-mcp-toolpicker crate

Building this crate gives a promptforge prompt two ways to obtain an MCP tool for a capability
described in plain English: a static, launch-time binding declared in Lua, and a dynamic,
runtime discovery tool the model can call. Both are backed by one local, deterministic
sentence-embedding engine over the connected servers' tool catalog, and both resolve through a
single four-outcome policy (bind / duplicate / foreign-ambiguous / absent). The crate holds the
resolution semantics and the Lua-facing API; it depends on a separate thin `promptforge-mcp-client`
for protocol.

## Executive summary

A prompt author declares needs as capability descriptions - `tools.add_need("db", "run a read-only
SQL query against the log database")` - and at launch the crate embeds every connected tool's
text, matches each need by cosine similarity, and binds the alias to a concrete tool when one wins
clearly, or fails loud when the match is ambiguous within the author's own catalog or absent. For
capabilities not known at authoring time, the author opts into `tools.add("choose_mcp_tool")`; at
runtime the model calls `choose_mcp_tool(need)`, a deterministic top-k retriever returns candidate
descriptors, the harness rewrites the context so the chosen tool appears as if it were available
from the start, and the main model calls it. Matching in the author register is near-trivial
(preliminary top-1 ~0.99), so the engine's real work is duplicate and absence detection; the right
tool is in the top-3 ~0.93 of the time even among close competitors, which is why the design
surfaces a shortlist rather than forcing a single guess. The matcher is a small model
(bge-small-en-v1.5 or all-MiniLM-L6-v2, ~33-133 MB, CPU, deterministic); no LLM runs in the crate's
own machinery.

## Key design choices

1. Local sentence embeddings are the matcher, not zero-shot NLI or lexical methods. Embeddings were
   the only approach robust across every real dataset; NLI looked strong on synthetic data and
   collapsed on real needs, and lexical fusion degraded the strong ranker. Tension: embeddings need
   a bundled model file, but it is small and deterministic.
2. bge-small-en-v1.5 and all-MiniLM-L6-v2 are interchangeable; the crate treats the model as
   configurable and defaults to bge-small. Larger models did not reliably help. Reversing this later
   is a config change, not a code change.
3. Needs are author-register capability descriptions, not user utterances. This is what a Lua author
   writes, and it makes matching near-trivial. The contract for `add_need`'s description field is "a
   clean, parameter-free statement of what the tool does."
4. The real job is duplicate and absence detection, not the happy-path match. The engine is built
   around a four-outcome decision, and the abstain path (fail loud) is first-class, not an afterthought.
5. Resolution is a similarity floor plus a top-1-vs-top-2 margin. A clear winner binds; a thin margin
   means ambiguity; nothing above the floor means absence. Raw cosine is not a probability, so a
   calibration step is required before the floor can be a guaranteed error budget (deferred).
6. Duplicates within the author's own catalog are treated as configuration errors and fail loud;
   duplicates arising from intentionally imported foreign/overlapping servers surface a shortlist for
   disambiguation. MCP `readOnlyHint`/`destructiveHint`/`idempotentHint` annotations break ties where
   present but are never required.
7. `tools.add_need` is the static, launch-time, LLM-free surface; `choose_mcp_tool` is the dynamic,
   runtime surface. They are complementary and share the engine.
8. `choose_mcp_tool` is a deterministic embedding retriever, not an LLM. It returns descriptors; the
   main model does the choosing. This keeps the crate's machinery LLM-free and puts selection where
   the full task context and the author's model configuration already are.
9. On dynamic resolution the harness rewrites the context (chosen descriptor before the prose,
   discovery episode excised) so the dynamic path converges onto the static execution state. One
   execution model, regardless of surface.
10. The crate depends on a separate thin `promptforge-mcp-client` for protocol and owns only the
    semantics. Protocol consumers (such as the CLI) must not pull the embedding model, and each crate
    stays small enough for a coding LLM to hold whole.
11. An optional model-tiered configuration (strong-model select -> context-clearing goto ->
    cheap-model execute) exists for genuinely hard selection, gated on expected ambiguity.
12. MCP sampling and roots are not implemented (sampling is deprecated upstream); the crate does not
    advertise those capabilities.

## Public API (Lua-facing), normative

The crate contributes these verbs to the section Lua environment. Signatures are contracts, not
implementations.

- `tools.add(name: string)` - scope an exact, already-known tool (existing mechanism; includes
  `"choose_mcp_tool"` to opt into dynamic discovery).
- `tools.add_need(alias: string, description: string)` - declare a capability need. At launch the
  resolver binds `alias` to a concrete `(server, tool)` per the four-outcome policy; the bound alias
  is then usable exactly like a local tool name in `tools.add`. `description` is an author-register
  capability line (parameter-free). Errors at launch on ambiguity-in-own-catalog or absence.

## choose_mcp_tool return contract, normative

`choose_mcp_tool(need: string)` runs deterministic embed -> top-k over the connected catalog and
returns one of:

- a single tool descriptor `{ server, name, description, input_schema }` when one candidate clearly
  wins;
- a shortlist `[descriptor, ...]` (2-3) when the top candidates are a genuine near-tie (duplicates),
  for the main model to disambiguate with full task context;
- `{ error: "no tools available" }` when nothing clears the similarity floor.

The harness then rewrites the context to place the returned descriptor(s) before the prompt prose,
excising the call, and the main model calls the tool. The retriever result is cacheable by
`(need, catalog_hash)`.

## Resolution engine

- At startup: connect configured servers, snapshot each `tools/list` into a catalog of
  `(server, name, description, input_schema, annotations)`, and embed each tool's enriched text
  (name + description + parameter names). Cache embeddings by catalog hash.
- Per need or per `choose_mcp_tool` call: embed the need, cosine-rank the catalog, take top-k, apply
  the floor and margin, and emit one of the four outcomes. Near-identical tools (cosine >= a
  duplicate threshold, roughly 0.98) are recorded as equivalent-golds so an equivalent pick is not
  treated as wrong.

## Configuration, normative shape

- Connected MCP servers: list of `{ name, url|command, auth }` (delegated to `promptforge-mcp-client`).
- Embedding model id (default `bge-small-en-v1.5`), bundled weights path.
- Resolution thresholds: similarity floor, margin, duplicate threshold, top-k.
- Context-rewrite opt-out (per prompt/section).

## Crate boundaries

- Depends on `promptforge-core` for the `Tool` trait and on `promptforge-mcp-client` for protocol.
- Owns: the embedding engine, the four-outcome policy, the Lua verbs, and the context-rewrite hook.
- Does not own: MCP transport/JSON-RPC (that is `promptforge-mcp-client`), the model that does dynamic
  selection (that is the author's main-context model).

## Evidence (preliminary, to be reconciled from study-mcp-toolpicker/RESULTS.md)

- Author-register match, random distractors: top-1 ~0.99, recall@3 ~1.0.
- Hard near-neighbor distractors: top-1 ~0.79, recall@3 ~0.93.
- Duplicate prevalence: ~11% of a broad catalog has a >= 0.98 twin, overwhelmingly cross-server.
- Model choice: bge-small ~ MiniLM at scale; larger models not reliably better.
These figures are from the spike and will be replaced by the reproduced dataset numbers.

*2026-08-02 - Opus 4.8 (Cursor agent) - numbers preliminary, pending dataset reconciliation*


### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\README.md

# study-mcp-toolpicker

The design and reproducible evidence for the `promptforge-mcp-toolpicker` crate: mapping a
prompt's English capability need to the right MCP tool, locally and deterministically.

## Documents
- `rationale.md` - the why: the reasoning journey and the alternatives rejected.
- `design-mcp-toolpicker.md` - the what: the crate's API, contracts, engine, config, boundaries.
- `RESULTS.md` - the numbers, regenerated by the spike below.
- `../mcp-classifier-spike/report/FINDINGS.md` - the fuller empirical log this study distills.

## Dataset (compact, id-referenced - no per-case files)
- `data/catalog.jsonl` - 9,922 real MCP tools (automatelab), one line each with a stable `id`.
- `data/needs_raw.jsonl` - author-register need strings, 3 bands per sampled tool, multi-model.
- `data/needs.jsonl` - eval cases referencing tools by id: gold, equivalent-golds, hard and
  random distractor id lists, band, generator model.
- `embeddings/catalog_<model>_<hash>.npy` - cached catalog vectors.

## Reproduce
```
bash reproduce.sh 1500       # sample; use 9922 for the full corpus
```
Requires `ANTHROPIC_API_KEY` for need generation. Uses the sibling spike's venv
(`../mcp-classifier-spike/.venv`, torch + sentence-transformers, CUDA if present).

## What the numbers mean
Needs are author-register capability descriptions (what a Lua author writes), not user
utterances. `random` distractors measure matching among unrelated tools (the easy ceiling);
`hard` distractors are the gold's nearest neighbors (real disambiguation). Bands vary paraphrase
distance (restatement / synonym / goal). The abstention sweep reports coverage vs accuracy at a
false-bind budget on the hard regime.


### c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\manifest.md

# Dataset manifest

Provenance for the reproducible artifacts in this directory.

- Catalog source: `automatelab/mcp-servers-tool-catalog` (real MCP `tools/list` dumps), copied from `../mcp-classifier-spike/data/automatelab_tools.parquet`.
- Catalog: 9,922 usable tools (name + description + input-schema params); `data/catalog.jsonl`, id-indexed.
- Catalog embedding hash: `1f1f51fe403b452c` (see `embeddings/catalog_*_1f1f51fe403b452c.npy`).
- Needs: 29,226 across 9,742 tools x 3 bands (restatement / synonym / goal). ~180 tools dropped from ~9 generation chunks that failed JSON parse (~2%).
- Need generators: `claude-haiku-4-5` and `claude-sonnet-4-6`, alternating per chunk (20 tools/chunk, `max_tokens` scaled to chunk size).
- Eval models: `BAAI/bge-small-en-v1.5`, `sentence-transformers/all-MiniLM-L6-v2` (CUDA).
- Distractors per case: 39; duplicate threshold 0.98 (equivalent-golds excluded from distractors); seed 0.
- Regenerate: `bash reproduce.sh 9922` (needs `ANTHROPIC_API_KEY`).

*2026-08-02 - Opus 4.8 (Cursor agent)*


StrReplace-edited design docs (path only): `c:\Users\Vinnie\src\cursor\promptforge-design\mcp-classifier-spike\report\FINDINGS.md`, `c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\design-mcp-toolpicker.md`, `c:\Users\Vinnie\src\cursor\promptforge-design\study-mcp-toolpicker\rationale.md`
