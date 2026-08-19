# Map-reduce synthesis report plan

*2026-07-30 06:54 - transcript f237b662-c0ec-4546-98f0-95963820937c*



## Prompts



**[p1]** spawn subagents and search the web for agentic techniques for taking separate web fetch researtch results and combining them into a single document. this is essentially map-reduce. I am wondering, can a model be fine-tuned to perform this? maybe in a streaming way? a fast way? find out search broad and deep

**[p2]** create a beautiful report in @promptforge-design ( use @tools-public/how-to/how-to-write-reports.md ) keep inline hyperlinks, inverted pyramid

**[p3]** Map-Reduce Synthesis Research Report

**[p4]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p5]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p6]** Implement the plan as specified, it is attached for your reference. Do NOT edit the plan file itself.

**[p7]** To-do's from the plan have already been created. Do not create them again. Mark them as in_progress as you work, starting with the first one. Don't stop until you have completed all the to-dos.

**[p8]** how can such a small model handle everything though? what if the inputs have code fences. C++. Javascript. etc



## Plans

### Map-reduce synthesis report

*Write a research/analytical report in `promptforge-design/` synthesizing the three research files on map-reduce document synthesis, fine-tuning for the reduce step, and streaming/fast approaches. The report follows the how-to-write-reports rulebook, uses inverted pyramid structure, and preserves inline hyperlinks from all sources.*

# Map-Reduce Synthesis Research Report

## Target File

`promptforge-design/design/design-map-reduce-synthesis.md`

This sits alongside the existing `chatlight-fine-tuning-small-models.md` in `design/` since it directly informs PromptForge's reduce-step architecture.

## Report Type

**Type 3: Research / scientific** crossed with **Type 2: Analytical / recommendation** - the report presents research findings on techniques and recommends an architecture for PromptForge's reduce step.

## Structure (Inverted Pyramid)

1. **Executive summary** - Bottom line up front: yes, a model can be fine-tuned for the reduce step; staircase streaming eliminates the wait-for-all bottleneck; the optimal stack is a 1-3B QLoRA model with speculative decoding.
2. **Key findings** - The three headline discoveries, each in one paragraph with inline citations.
3. **Techniques catalog** - The 11 patterns from the map-reduce research, compressed to their essentials with decision criteria.
4. **Fine-tuning feasibility** - Evidence that small models match frontier, distillation pipeline, QLoRA benchmarks. Concrete model names and ROUGE scores.
5. **Streaming and speed** - Staircase streaming, Parallel-Synthesis, BRIEF-PRO compression, prompt caching economics. Production system architectures (Perplexity, Tavily).
6. **Recommended architecture for PromptForge** - How this maps to PromptForge's fan-out/reduce model. The reduce section as a fine-tuned model behind a vLLM endpoint, staircase streaming from fan-out workers.
7. **Risks and open questions** - Training data quality, context-window expansion making reduce unnecessary for small corpora, LED/Longformer QLoRA NaN issue.
8. **Sources** - Full reference list with inline URLs preserved throughout.

## Key Style Rules (from how-to-write-reports.md)

- Answer-first (rule 3.1) - recommendation in first paragraph
- Headings state points, not topics (rule 3.2)
- Active voice, 15-25 word sentences (rule 3.3)
- Evidence before value words (rule 3.5)
- Prose for reasoning, not bullets for arguments (rule 3.7)
- All claims cited with inline hyperlinks
- No YAML frontmatter (cabinet output rule)
- Date/model at bottom in italics

## Sources to Synthesize

- `cabinet/_research/2026-07-30-conduct-research-llm-map-reduce-synthesis.md`
- `cabinet/_research/2026-07-30-llm-fine-tuning-document-synthesis-reduce.md`
- `cabinet/_research/2026-07-30-streaming-document-synthesis-techniques.md`


Todos:

- Write the full report to promptforge-design/design/design-map-reduce-synthesis.md following inverted pyramid, report rulebook, preserving all inline hyperlinks from the three research files

## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge-design\design\design-map-reduce-synthesis.md

# Fine-tune the reduce step: map-reduce synthesis for agentic research

## Executive summary

A model can be fine-tuned to combine separate web-fetch results into a single document, this is feasible today, and a purpose-built model already exists on HuggingFace ([pszemraj/flan-t5-xl-summary-map-reduce-1024](https://huggingface.co/pszemraj/flan-t5-xl-summary-map-reduce-1024)). The task the question describes - map many sources, reduce them to one coherent document - is the standard map-reduce summarization pattern, and its reduce step is a well-studied, trainable target. The recommendation is to fine-tune a 1-3B model with QLoRA on synthesis pairs generated by a frontier teacher, deploy it behind vLLM, and feed it with staircase streaming so the reduce begins before every fetch has returned. Confidence: high on feasibility, medium on the exact latency numbers until benchmarked on the specific hardware.

Three findings drive that recommendation. First, fine-tuned small models match frontier models on well-defined synthesis tasks: [FLAN-T5-Large at 780M parameters matches GPT-3.5 and PaLM-2 on meeting summarization](https://arxiv.org/pdf/2402.00841), and a [TACL 2024 study](https://doi.org/10.1162/tacl_a_00632) attributes summarization ability to instruction tuning, not scale. Second, streaming is free because every autoregressive model streams by default; the real lever is latency, and [staircase streaming](https://arxiv.org/html/2510.05059v1) cuts time-to-first-token by up to 93% by reducing on partial results. Third, speed stacks across three layers - architecture (pipelined reduce), inference (speculative decoding adds 2-3x), and preprocessing ([BRIEF-PRO](https://aclanthology.org/2026.findings-acl.696.pdf) compresses sources 32x before the reduce ever runs).

This report serves a decision about PromptForge's reduce step: whether to keep prompting a general driver model to combine fan-out results, or to train a dedicated synthesis model. The evidence favors training one, and the closing section maps the choice onto PromptForge's existing fan-out and virtual-file machinery.

## The reduce step is a trainable target, not a prompting trick

The core question - can a model be fine-tuned to combine research results in a fast, streaming way - resolves to yes on all three counts, and the strongest evidence is that the exact model already ships. [pszemraj/flan-t5-xl-summary-map-reduce-1024](https://huggingface.co/pszemraj/flan-t5-xl-summary-map-reduce-1024) is a FLAN-T5-XL fine-tuned explicitly for the reduce/consolidation step of map-reduce summarization, trained on a dedicated `summary-map-reduce-v1` dataset. For multi-document synthesis specifically, [PRIMERA](https://aclanthology.org/2022.acl-long.360.pdf) is the research reference point: an encoder-decoder pre-trained for the task, using `<doc-sep>` tokens to share information across document boundaries.

Streaming needs no special work. All autoregressive models emit tokens sequentially, and streaming is the default output mode in production inference frameworks ([ClickHouse inference-latency guide](https://clickhouse.com/resources/engineering/llm-inference-latency)). A fine-tuned model streams identically to its base. The architectural concern is not whether output streams but how quickly the first token arrives, which is a prefill-latency question addressed in the speed section below.

## Small fine-tuned models match large prompted models on synthesis

The evidence that a small dedicated model can replace a large general one on this narrow task is consistent across studies. [FLAN-T5-Large (780M) matches LLaMA-2-7B through 70B, GPT-3.5, and PaLM-2 on meeting summarization](https://arxiv.org/pdf/2402.00841), and does it at 4.2 seconds per transcript on one L4 GPU against 15 seconds for LLaMA-2-7B on the same hardware. [Phi3-Mini and Llama3.2-3B match 70B models on news summarization](https://aclanthology.org/2025.naacl-long.253.pdf). A [568M model, INFOSUMM](https://arxiv.org/html/2403.13780), competes with ChatGPT on controllable summarization without ever using ChatGPT to train. The [TACL 2024 benchmarking study](https://doi.org/10.1162/tacl_a_00632) states the mechanism plainly: "We identify instruction tuning, instead of model scale, as the key to LLMs' summarization capability."

Distillation is the route to that quality. Task-specific distillation retains 85-90% of a teacher's performance while cutting latency 3-6x: an [8B model distilled from a 70B teacher](https://doi.org/10.1109/slaai-icai68534.2025.11318480) dropped response time from 12 seconds to 3 while holding 90% of quality. The practical pipeline, per [Distil Labs' benchmarks of 12 small models](https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/), is to generate roughly 10,000 training examples with a teacher model, then fine-tune a student with QLoRA; their best student, Qwen3-4B, matched a 120B-parameter teacher, and Llama-3.2-1B and 3B gained the most from tuning.

QLoRA is the standard training method, and the numbers are concrete. On CNN/DailyMail with Mistral-7B on a single A100, [LoRA lifts ROUGE-L from 0.139 to 0.201](https://github.com/achi9629/efficient-llm-finetuning), and the optimal production path - QLoRA train, merge to FP16, then AWQ INT4 quantize - holds that 0.201 ROUGE-L at 368 tokens/second in 4.9 GB of VRAM. The one architecture caveat: [QLoRA breaks LED/Longformer models like PRIMERA with NaN gradients](https://huggingface.co/mehdielg/primera-billsum-arxiv-pubmed), so PRIMERA needs standard LoRA in bf16 while decoder models take QLoRA cleanly.

## Speed comes from pipelining the reduce, not from a faster model alone

The largest latency win is structural: begin reducing before every map finishes. [Staircase streaming](https://arxiv.org/html/2510.05059v1) formalizes this - the aggregator starts generating as soon as the first proposer produces a chunk, updates its prompt as later chunks arrive, and reaches up to 93% TTFT reduction while holding quality on Arena-Hard and AlpacaEval. This is exactly the pipelined map-reduce the question asks about, and it is proven to work rather than speculative.

A more aggressive research technique skips text entirely. [Parallel-Synthesis](https://arxiv.org/html/2606.14672) has the synthesizer consume the KV caches of parallel workers directly through a cache mapper and a synthesizer LoRA, rather than re-encoding their text summaries, for a 2.5x-11x TTFT reduction that matches or beats text synthesis on 7 of 9 benchmarks. It requires post-training and a shared model family across workers and synthesizer, so it is not yet API-accessible, but it sets the ceiling for what a co-trained fan-out-plus-reduce system can reach.

Two cheaper levers stack on top. Compressing sources before synthesis shrinks the reduce token budget: [BRIEF-PRO](https://aclanthology.org/2026.findings-acl.696.pdf) achieves 32x compression while improving QA quality 4.67% over less aggressive compressors, at 23% of their compute. And [speculative decoding](https://aclanthology.org/2026.findings-acl.2153.pdf) accelerates summarization directly and losslessly - SpecExtend reaches 2.84x on 16K-token long-document summarization, and [Medusa heads](https://arxiv.org/abs/2401.10774) add 2-2.8x with no separate draft model and compose with an already fine-tuned model via self-distillation.

Prompt caching sets the economic floor and constrains the design. Keeping every pipeline stage on one model family matters because [switching families invalidates the cache](https://www.digitalapplied.com/blog/prompt-caching-economics-cache-first-agent-architecture-2026), turning a 90%-off cache read into a 125%-of-base cold write; placing static instructions first and dynamic source content last preserves the cacheable prefix. Measured savings run to 88-89% of input cost. The rule for PromptForge is direct: the reduce model and the fan-out workers should share a family, and the reduce section's preamble should be byte-stable.

Production systems confirm the pattern holds at scale. [Perplexity](https://research.perplexity.ai/articles/architecting-and-evaluating-an-ai-first-search-api) budgets roughly 100ms for hybrid retrieval and generates on Cerebras at 1,200 tokens/second for a 358ms median end-to-end latency; [Tavily](https://www.tavily.com/blog/how-we-built-the-fastest-web-search-in-the-world) returns pre-shaped citation-rich JSON to minimize downstream processing. The closest published template to the target use case is a [five-pass research pipeline](http://mikeosswatch.com/topics/459) - query expand, parallel search fan-out, triage, parallel extract, stream synthesize - with hard caps of 25 LLM calls and 45 seconds and graceful degradation that emits partial synthesis when a cap hits.

## Choosing a synthesis pattern

The reduce step is one of a family of patterns, and the right one depends on corpus size and whether source order matters. The map-reduce research catalogs eleven; the four that matter for an agentic web-fetch pipeline are these.

**Stuff** concatenates all sources into one call. It gives the highest coherence and lowest latency when the content fits, and with 1M-token windows it now fits far more than it used to - a [2026 RAG survey](https://futureagi.com/blog/rag-summarization/) notes that "passing the whole document tends to beat multi-stage approaches on long-context QA." The caveat is recall: models do not use all context positions equally, so "it fits" is not "it is used well."

**Map-reduce** summarizes each source in parallel, then combines. It parallelizes cleanly and scales to any corpus size, at the cost of losing cross-document context at the map step and stacking lossy compression if the reduce overflows and must collapse recursively. It is the workhorse for large corpora and the pattern the fine-tuned reduce model targets.

**Refine** walks sources sequentially, updating a running summary. It preserves narrative order and coherence best, but it cannot parallelize, so its latency is the worst of the four - though it can stream a progressively improving answer. **Tree-summarize / RAPTOR** merges bottom-up, clustering sources by embedding and recursing to a root; it beats flat map-reduce on large corpora and adds a [20-point accuracy gain on QuALITY](https://futureagi.com/blog/rag-summarization/), at the cost of more total calls and harder pipelining.

The trade-off between flat and hierarchical reduce is the operative choice. Flat reduce is faster, more token-efficient, and easy to pipeline with staircase streaming; hierarchical trees give better local coherence and multi-granularity retrieval but need full clusters before each level and so resist pipelining. For a speed-first research tool, flat reduce with a fine-tuned model wins; for a quality-first tool over a large corpus, the tree is worth its cost.

## Recommended architecture for PromptForge

This maps directly onto PromptForge's existing machinery. The [fan-out primitive](design-promptforge.md) already dispatches parallel `Task` subagents over web fetches, each in a fresh context, and merges their stores. The reduce step becomes one more section whose Lua block selects a dedicated model slot pointing at a fine-tuned synthesis model behind vLLM, exactly as the current design tiers `gemma-27b` for mechanical work and a large driver for orchestration.

Three design choices follow from the research. Fine-tune a 1-3B model (Qwen3-4B or Llama-3.2-3B) with QLoRA on synthesis pairs a frontier teacher generates, then merge and AWQ-quantize for deployment; this is the same distillation route the [chatlight fine-tuning note](chatlight-fine-tuning-small-models.md) recommends for progress-summary models, applied to a heavier task. Keep the reduce model in the same family as the fan-out workers so prompt caching survives across stages. And feed the reduce section with staircase streaming, so it begins synthesizing as the first fetch returns rather than blocking on the slowest one - the pipelined reduce that PromptForge's fan-out aggregation does not yet exploit.

The payoff is consistent with PromptForge's model-sovereignty goal: a self-hosted 3B reduce model with AWQ and Medusa runs an estimated 10-20x faster than a frontier API at 85-95% of quality, per the [fine-tuning research](https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/), and streams by default. The reduce section stays ordinary markdown; only its model slot and a staircase-streaming aggregator change.

## Risks and open questions

Training-data quality is the dominant risk, not architecture. Poor synthesis examples will drag a fine-tuned model below a zero-shot frontier model, and the mitigation is to generate high-quality reduce examples with a frontier teacher and distill from them rather than hand-labeling. [Low-quality few-shot examples actively hurt](https://arxiv.org/html/2501.18128v1), which is a warning that applies equally to training pairs.

Expanding context windows narrow the reduce step's value for small corpora. When all fetched sources fit a 1M-token window, the stuff pattern beats a trained reduce on coherence, so the fine-tuned model earns its place only when the corpus is large or when cost and latency at scale rule out stuffing frontier context. The open question is where the crossover sits for the specific workloads PromptForge runs; it should be benchmarked before committing training effort.

Two narrower caveats: the LED/Longformer QLoRA NaN issue rules PRIMERA out of the QLoRA path and forces bf16 LoRA if that architecture is chosen, and the most aggressive speed technique, direct KV-cache synthesis, remains research-stage and unavailable via API, so its 2.5-11x ceiling is a target rather than a shippable option today.

## Sources

The three research files behind this report, each with full source lists:

- Map-reduce and multi-document synthesis techniques - `cabinet/_research/2026-07-30-conduct-research-llm-map-reduce-synthesis.md`
- Fine-tuning LLMs for the reduce step - `cabinet/_research/2026-07-30-llm-fine-tuning-document-synthesis-reduce.md`
- Streaming and fast document synthesis - `cabinet/_research/2026-07-30-streaming-document-synthesis-techniques.md`

Primary external sources cited above:

- [pszemraj/flan-t5-xl-summary-map-reduce-1024](https://huggingface.co/pszemraj/flan-t5-xl-summary-map-reduce-1024) - purpose-built reduce model
- [PRIMERA (ACL 2022)](https://aclanthology.org/2022.acl-long.360.pdf) - multi-document summarization pre-training
- [Tiny Titans (arXiv 2402.00841)](https://arxiv.org/pdf/2402.00841) - small models matching large on meeting summarization
- [TACL 2024 summarization benchmark](https://doi.org/10.1162/tacl_a_00632) - instruction tuning over scale
- [INFOSUMM (arXiv 2403.13780)](https://arxiv.org/html/2403.13780) - 568M model competing with ChatGPT
- [Distil Labs 12-model benchmark](https://www.distillabs.ai/blog/we-benchmarked-12-small-language-models-across-8-tasks-to-find-the-best-base-model-for-fine-tuning/) - distillation pipeline
- [Efficient LLM fine-tuning benchmarks](https://github.com/achi9629/efficient-llm-finetuning) - QLoRA and AWQ ROUGE numbers
- [Staircase Streaming (arXiv 2510.05059)](https://arxiv.org/html/2510.05059v1) - pipelined reduce
- [Parallel-Synthesis (arXiv 2606.14672)](https://arxiv.org/html/2606.14672) - direct KV-cache synthesis
- [BRIEF-PRO (ACL Findings 2026)](https://aclanthology.org/2026.findings-acl.696.pdf) - 32x context compression
- [SpecExtend (ACL Findings 2026)](https://aclanthology.org/2026.findings-acl.2153.pdf) - speculative decoding for long-document summarization
- [Medusa (arXiv 2401.10774)](https://arxiv.org/abs/2401.10774) - multi-head decoding
- [Prompt caching economics](https://www.digitalapplied.com/blog/prompt-caching-economics-cache-first-agent-architecture-2026) - cache-first design
- [Perplexity architecture](https://research.perplexity.ai/articles/architecting-and-evaluating-an-ai-first-search-api) and [Tavily architecture](https://www.tavily.com/blog/how-we-built-the-fastest-web-search-in-the-world) - production speed
- [RAG summarization survey 2026](https://futureagi.com/blog/rag-summarization/) - pattern landscape and RAPTOR

---

*2026-07-30 06:00 - claude-4.8-opus (Cursor agent)*
