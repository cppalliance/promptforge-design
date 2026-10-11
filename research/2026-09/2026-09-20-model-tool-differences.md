---
produced: 2026-09-20
title: Per-model tool differences for PromptForge - apply_patch versus old_string/new_string edit tool by model family, harness tool conventions (Codex CLI, OpenCode, Cline, Cursor, Aider), edit format benchmarks, reasoning replay and tool-call id rules in the gateway, mid-conversation model switching
---

# Per-model tool differences: what varies, how much it matters, and what PromptForge must accommodate

Report type: analytical / recommendation. Written for the PromptForge owner. The decision it serves: how the static `tools:` contract in prompt frontmatter, the capability-provided schemas, and the gateway's pass-through relay should accommodate models that were trained on different tool shapes, and whether mid-conversation model switching stays allowed.

Sources: nine research collections produced 2026-09-20 (harness tool inventories; vendor tool conventions; open-weight tool templates; measured evidence; harness code branches; edit-tool schemas; history replay rules; llama.cpp gateway duties; non-edit tool semantics). Each claim below cites its primary source; the collections hold the verbatim quotes.

## Summary

Only one core tool changes its contract by model family: the file editor. Every other per-model difference in shipped harnesses is a rename, a description change, an instruction, or a protocol rule that lives below the prompt in the transport layer. PromptForge should therefore ship one string-replacement edit capability for every family now, design the `tools:` slot fill so that a family-specific edit can be substituted later as a policy change, and move the real per-model work into the gateway and model client, where reasoning replay, tool-call ids, and result grouping already differ by provider.

Five independent harnesses (Codex CLI, OpenCode, Kilo Code, Roo Code, Cline) converged on the same rule: GPT-5-era OpenAI models get a V4A `apply_patch` tool, and Anthropic, Gemini, Grok, and open models get an `old_string`/`new_string` replacement tool. Cursor, Copilot Chat, and Aider encode the same split. The measured payoff is asymmetric. Giving a non-OpenAI model the patch format is costly: Grok Code Fast 1 scores 6.7% with `apply_patch` and 68.3% with a line-addressed alternative, and GLM-4.7 and Grok 4 Fast fail 46% to 51% of patches (Bölük, Feb 2026). Giving an OpenAI model string replacement is nearly free: GPT-5.2 Codex moves under 5 points across patch, replace, and hashline formats on the same benchmark, and OpenAI's own GPT-4.1 launch table shows the whole-file versus diff penalty closed to 1.3 points (51.6% versus 52.9%). String replacement is the format every family handles acceptably. Confidence: high that the edit tool is the only contract-changing per-model core tool (three inventories, six models captured byte-exact, five harness codebases read); medium that a single string-replacement tool costs OpenAI models under 5 points (one 180-task benchmark and one partial replication).

Below the edit tool, the differences that break requests are protocol rules, and they differ by provider, not by prompt. Anthropic rejects a request if a signed thinking block is altered; Gemini 3 returns 400 if the first function call of a turn lacks its `thought_signature`; DeepSeek returns 400 if `reasoning_content` is missing from any assistant message once tools are present; Mistral rejects tool-call ids that are not exactly nine alphanumerics; Kimi expects ids of the form `functions.name:idx`. PromptForge's Lua history layer today normalizes each assistant message to `{role, content, tool_call_id, tool_calls}` and discards reasoning, which is correct for Anthropic and OpenAI over the OpenAI-compatible shape and wrong for DeepSeek, Kimi, gpt-oss, GLM-4.7+, and Qwen3 in thinking mode. That is a gateway and model-client fix, not a prompt contract fix.

For local inference the picture simplified in March 2026. llama.cpp PR #18675 replaced per-family tool-call parsers with a template-driven autoparser, so the GGUF's Jinja template now drives format detection. The gateway's residual duties are to forward `reasoning_content` and `chat_template_kwargs` untouched, preserve tool-call ids and order, refuse `tools` for templates that cannot render them (llama.cpp ignores them silently), and translate the named-function `tool_choice` form, which llama-server silently downgrades to `auto`.

Recommendation, in order: (1) ship one `str_replace`-style edit capability with exact-match-once semantics and a `replace_all` flag, for all families; (2) keep the `tools:` slot as alias-to-identity but make `fill_tool_bindings` able to resolve a role (`want:`) by model family when a second edit capability exists; (3) add a provider-aware replay policy to the model client for `reasoning_content` and ids; (4) leave mid-conversation model switching enabled while there is one edit format, and pin the model per session on the day a second format ships. Owner: PromptForge owner. First step: a design note for the edit capability's schema and error strings, drawn from Appendix A.

## Contents

1. The question is whether a static tool contract can serve every model, judged on three criteria
2. What differs per model
3. Only edit format and the serialization path move frontier models by double digits
4. One string-replacement edit for all families beats the three alternatives on every criterion
5. Ship one edit format now, build the fill seam, and fix replay in the client
6. Limitations
- Appendix A: edit tool contracts side by side
- Appendix B: history replay rules by provider
- Appendix C: gateway duties for llama-server
- Appendix D: open-weight tool-call formats
- References

## 1. The question is whether a static tool contract can serve every model, judged on three criteria

PromptForge prompts declare their tool contract statically in YAML: each `tools:` slot maps a prompt-local alias to a capability id, the capability supplies the JSON schema and description, and the model sees the alias as `function.name`. Cursor and other multi-model harnesses instead present different tool sets to different model families, and Cursor's engineering blog states the reason plainly: "OpenAI's models are trained to edit files using a patch-based format, while Anthropic's models are trained on string replacement ... So in our harness, we provision each model with the tool format it had during training" (Cursor, "Continually improving our agent harness", 2026-04-30). The question is whether a static contract can serve every model PromptForge routes to, and what has to give if it cannot.

Three criteria decide it. First, does a difference change the tool's contract (parameters or runtime semantics), or only its name, description, or surrounding instructions? A rename or instruction fits inside the alias and Lua override mechanisms PromptForge already has; a contract change does not. Second, how large is the measured effect on the same model when the choice is wrong? Third, where in PromptForge's stack does the difference belong: prompt contract, harness fill, model client, or gateway relay?

## 2. What differs per model

### 2.1 The edit tool is the one core tool whose contract changes by family

Every multi-model harness with readable source or a byte-exact capture routes OpenAI GPT-5-era models to a patch tool and everyone else to a replacement tool. Table 1 lists the convergence. The independent arrival of five codebases at the same rule is the evidence; the stated rationale is uniformly empirical ("more reliable edits") and traces to OpenAI's training statement: "we highly recommend using `apply_patch` for file edits to match the training distribution" (OpenAI GPT-5 prompting guide).

Table 1. Edit-tool routing by model family in shipped harnesses. Source: harness code branches and inventories collections.

| Harness | OpenAI GPT-5 era | Anthropic | Gemini | Grok / open models | Where the rule lives |
|---|---|---|---|---|---|
| Cursor (2026 capture) | `ApplyPatch` | `StrReplace` + `Write` | not captured | `StrReplace` + `Write` (Grok 4.5) | server-side harness per model |
| Codex CLI | `apply_patch` freeform grammar | n/a | n/a | JSON `apply_patch` for gpt-oss | `models.json` `apply_patch_tool_type` |
| OpenCode | `apply_patch` replaces `edit`+`write` | `edit` | `edit` | `edit` | `usePatch = id.includes("gpt-") && !oss && !gpt-4` |
| Kilo Code | same as OpenCode, keeps `write` | `edit` | `edit` | `edit` | catalog `family` field |
| Roo Code | `apply_patch`; excludes `apply_diff`, `write_to_file` | `apply_diff` | `apply_diff` (Gemini aliases later reverted) | `apply_diff` | `ModelInfo.includedTools` |
| Cline | "Apply Patch tool for GPT-5+ models" (3.46.0) | `replace_in_file` | `replace_in_file` | `replace_in_file` | `ModelFamily` variants |
| Copilot Chat | `apply_patch` | `multi_replace_string_in_file` | `replace_string_in_file` | `replace_string_in_file` (grok-code, MiniMax) | `chatModelCapabilities.ts` |
| Aider | SEARCH/REPLACE (`diff`) for gpt-5 too | `diff` | `diff-fenced` | `whole` for grok-3-mini | `model-settings.yml` `edit_format` |

Aider is the holdout, keeping SEARCH/REPLACE for GPT-5 on its own benchmark evidence, and Aider is also the only harness in the table that publishes numbers. Gemini special cases are the most volatile: Zed's `DiffFenced` format for Google (eval 0.77 to 0.98) and Roo's Gemini aliases were both later reverted.

The two contracts differ in more than syntax. Anthropic's `str_replace_based_edit_tool` performs one operation per call, requires `old_str` to match exactly once, and addresses inserts by line number. OpenAI's V4A patch is multi-hunk and multi-file, locates hunks by three lines of context and optional `@@` scope anchors, forbids line numbers, and folds create, update, delete, and move into one grammar. A V4A hunk can be lowered to `old_string` = context plus removed lines and `new_string` = context plus added lines, but the `@@ class Foo` narrowing is lost; the reverse requires synthesizing context the model never emitted. `replace_all`, `insert_line`, `Move to`, Gemini's required `instruction` field, and Anthropic's `undo_edit` have no counterpart across families. Appendix A gives the full comparison.

What every family shares is a postcondition: the designated region is replaced with the model's text, or nothing is written and the model receives an error. That shared postcondition is the only thing a prompt can legitimately depend on, and it is enough for a prompt to say "use `edit` to change files" and stop.

### 2.2 Non-edit core tools differ by harness, not by model

Shell, read, search, todo, and subagent tools vary enormously across harnesses and barely at all across models within a harness. The non-edit semantics collection classified every difference it found as contract-changing, rename-only, or instruction-only. The contract-changing ones are almost all harness-versus-harness: Codex's shell went from an argv array to a string to a `exec_command` plus `write_stdin` session model, and PR #39772 (2026-08-20) then standardized every model on the last of these; Cursor splits background execution into `Shell(block_until_ms)` and `AwaitShell`, Claude Code uses a boolean `run_in_background`, Gemini CLI uses `is_background` plus `delay_ms`. None of those choices is keyed on the model.

The per-model non-edit differences that exist in shipped code are few. Cursor's GPT dialect renames `Read` to `ReadFile`, `Grep` to `rg`, `Task` to `Subagent`, namespaces everything under `functions.`, and adds the `multi_tool_use.parallel` wrapper; the names differ, the observable schemas do not (pi-cursor-sdk capture, 2026-08-02; the GPT schemas were not exportable and are unverified). Gemini CLI keeps two tool manifests selected by `isGemini3Model`, and a diff shows identical names and parameters with only description text changed. Claude Code removed its todo and task tools entirely for Opus 4.8, Sonnet 5, Fable 5, and Mythos 5 (v2.1.233) because those models "keep track of multi-step work without a written checklist". Codex's read tool is absent for every model; the prompt says to use `cat`, `sed -n`, and `rg` through the shell. Copilot Chat's fourteen per-model capability flags include nine about edit tools and none about shell, read, or search.

Two non-edit differences are protocol-level rather than tool-level and do matter. OpenAI models trained in the ChatML era emit `multi_tool_use.parallel` as a real extra function whose argument is a list of calls; Anthropic and Gemini emit several tool-use blocks in one message. A harness on the OpenAI Chat Completions shape gets a native `tool_calls` array from every provider and does not need the wrapper. And the read tool's line-number format varies (`cat -n` tabs in Claude Code, `LINE|` in Cursor, none in Codex and Gemini, `N#HASH` in hashline harnesses), which matters only because it feeds the edit tool's `old_string`.

### 2.3 The differences that break requests are transport rules, and they differ by provider

Below the tool schemas sit rules about what a replayed conversation must contain. These are enforced with 400 errors, they differ by provider, and they are invisible to the prompt. Table 2 summarizes; Appendix B holds the full matrix.

Table 2. Hard replay requirements by provider. Source: history replay collection, vendor docs.

| Provider | Reasoning replay | Tool-call id rule | Failure text if wrong |
|---|---|---|---|
| Anthropic | Last assistant turn's `thinking` blocks must go back byte-identical inside a tool loop; Fable 5.1 also binds blocks to an unchanged `system`/`tools`/prior-messages prefix | `tool_result.tool_use_id` must match a prior `tool_use`; all results in one user message immediately after | "`thinking` or `redacted_thinking` blocks in the latest assistant message cannot be modified"; "The block is bound to a different conversation" |
| OpenAI Responses | Replay `reasoning` items with `encrypted_content`; omission degrades, foreign blobs fail | `call_id` pairing | `invalid_encrypted_content` for cross-org or cross-provider blobs; missing reasoning is silent degradation |
| Gemini 3 | `thought_signature` on the first `functionCall` of each step in the current turn | ids optional | "Function call `FC1` in the `1.` content block is missing a `thought_signature`" |
| DeepSeek | `reasoning_content` on every historical assistant message once `tools` is present | keep | "The `reasoning_content` in the thinking mode must be passed back to the API." |
| Kimi K3 / k2.7-code | `reasoning_content` always | ids must be `functions.name:idx` | documented as required; K2.x degrades silently |
| Mistral | none documented | exactly nine alphanumerics | error code 3280 |
| Qwen / GLM | `preserve_thinking` / `clear_thinking: false` retain; otherwise degrade | keep | none (quality loss) |

Over an OpenAI-compatible endpoint the rules soften but do not vanish. Anthropic's compatibility layer hoists all system messages and has no thinking replay path; Gemini's exposes signatures through `extra_content`; DeepSeek's and Kimi's still require `reasoning_content` on replayed assistant messages because the field is native to their Chat Completions dialect.

PromptForge's history layer normalizes each assistant message to `{role, content, tool_call_id, tool_calls: [{id, name, arguments}]}` and discards reasoning (the answer parser's diagnostic reads "empty model reply: reasoning content was present but ignored"). That design is correct for Anthropic and OpenAI through the OpenAI-compatible shape, where the provider handles or ignores reasoning server-side. It is wrong for DeepSeek with tools, which returns 400, and it silently degrades gpt-oss, Kimi, GLM-4.7+, and Qwen3 in thinking mode, whose templates render `reasoning_content` between tool calls. The fix belongs in the model client or gateway, which knows the provider, not in the prompt, which does not.

### 2.4 Open-weight families are template-driven, and the gateway's duties shrank in March 2026

Before March 2026 llama.cpp carried a hand-written parser per family (`HERMES_2_PRO`, `LLAMA_3_X`, `DEEPSEEK_R1`, `GLM_4_5`, `KIMI_K2`, and so on). PR #18675, merged 2026-03-06, replaced them with a differential autoparser that renders the GGUF's Jinja template with and without reasoning, with one and two tool calls, and with two different call ids, diffs the outputs to find the markers, and generates a PEG parser and grammar at runtime. The `common_chat_format` enum collapsed to `CONTENT_ONLY`, `PEG_SIMPLE`, `PEG_NATIVE`, `PEG_GEMMA4`, `PEG_MINIMAX_M3`. Hand-written handlers survive only where the diff cannot reconstruct the format: gpt-oss, Gemma 4, Kimi K2/K3, Qwen3-Coder, Ministral 3, Cohere2, MiniMax M3, Functionary, LFM2, GigaChat.

The consequence for a gateway that forwards OpenAI-shaped JSON to llama-server is that format knowledge is no longer its job, but five residual duties are. When `tools` reach a template with no tool support (Gemma 3, Phi-4, Mixtral v0.1), llama.cpp ignores them silently: prose answer, `finish_reason: "stop"`, no error. `reasoning_content` on assistant history has been forwarded to the template unconditionally since PR #18994, so stripping it upstream loses chain-of-thought between calls for gpt-oss, Kimi, Qwen3, GLM-4.7+, Gemma 4, DeepSeek V3.2+, and MiniMax. Tool-call ids are passed through untouched, so Mistral Nemo's template raises on any id that is not nine characters, Kimi K2 and Gemma 4 match results positionally, and DeepSeek V4 sorts results by id. The named-function `tool_choice` object is silently downgraded to `auto`, and `required` can run to `max_tokens` without a call (issue #27217, open). Llama 3.1 and 3.3 raise "This model only supports single tool-calls at once!" if a replayed turn holds two calls. Appendix C lists the duties with sources; Appendix D lists the per-family formats.

Four tool-result carriers exist across families: user-turn text (Qwen, Granite 4, Nemotron), a dedicated role token (Llama `ipython`, GLM `<|observation|>`, DeepSeek, Mistral `[TOOL_RESULTS]`), a named pseudo-role (gpt-oss `functions.n to=assistant`), and inside the assistant's own turn (Gemma 4 `tool_responses`, Cohere). The last class forces OpenAI `tool` messages to be folded back into the preceding assistant message before rendering; llama.cpp does this for Gemma 4 (PR #21418). The gateway need only emit one `tool` message per call, string content, in call order, immediately after the assistant turn.

## 3. Only edit format and the serialization path move frontier models by double digits

The measured-evidence collection gathered roughly 200 same-model comparisons across eight axes and ranked them by the largest credible isolated delta. Table 3 gives the ranking with the load-bearing numbers. Provenance matters: vendor self-reports (V) and harness-author benchmarks (H) dominate; independent measurements (I) exist for edit format, tool naming, tool count, and whole-harness swaps.

Table 3. Same-model effect of each tool-design axis, largest credible delta first. Source: measured evidence collection.

| Axis | Largest same-model delta | Frontier-model delta | Direction flips by family? | Best provenance |
|---|---|---|---|---|
| Edit format | Grok Code Fast 1 6.7% to 68.3% (patch to hashline); GPT-4 Turbo 20% to 61% (search/replace to udiff) | Sonnet 4.5 +14.4 over patch, +3.3 over replace; Claude 4 Sonnet +0.3% (Cline); GPT-5.2 Codex within 4.6 points, +26% tokens on hashline | Yes: DeepSeek V3.2 loses 5 to 8 points on hashline; GPT-4.1-nano gains on apply but collapses on generation | H (Aider, Bölük), I (Diff-XYZ, edit-bench) |
| Text protocol vs native function calling | Llama-3.1-70B 50.4 prompt to 20.8 FC (BFCL) | GPT-4o-mini +6, GPT-4-turbo +9.5 in FC; o1 59.1 to 52.8 | Yes, sign flips | I (BFCL) |
| Reasoning continuity | GPT-5-Codex -30% on Cursor Bench without reasoning traces | GPT-5 -3% on SWE-bench; Tau-bench 73.9 to 78.2 with `previous_response_id` | Yes, family-specific | V only |
| Whole-harness swap | 29.8 points observational spread for claude-3-5-sonnet across nine SWE-bench scaffolds | 0 to 8 points controlled (KDD Scaffold Effect); tokens per solve vary 40x | n/a | I |
| Tool count | roughly -10 points from 10 to 100 tools, near-identical across GPT-4o-mini, Haiku 3.5, Gemini 2.0 Flash | Opus 4 49 to 74 with Tool Search; Cursor -46.9% tokens with dynamic MCP loading | Slope family-independent, floor family-dependent | I, V |
| Tool naming and description | GPT-4 tool selection 80.0 to 58.1 under name noise (RoTBench); 0/20 to 19/20 from unifying two tool names (edit-bench) | +2% SWE-bench for tools in API field vs prompt (GPT-4.1); +5 to +17 for 3B to 8B models | Large for small models, small for frontier | I, V |
| Parallel calling | Claude 3.5 Sonnet 3.5% in FC mode vs 70.5% prompted; o1 0% FC; Llama-3.1-70B 12.5% vs 94.5% | GPT-4o and Gemini 2.0 Flash unaffected | Binary per model and mode | I (BFCL) |
| Schema strictness | OpenAI 93 to 100 schema adherence with strict mode | Zero task-level gain (Aider); no nesting or enum ablation exists anywhere | Unmeasured | V |

Three readings follow. First, edit format is the only axis that both changes the contract and moves frontier models by double digits when wrong, and the damage is asymmetric: non-OpenAI models given the patch format collapse (Grok 4 Fast and GLM-4.7 fail 46% to 51% of patches), while OpenAI models given string replacement barely move (GPT-5.2 Codex -0.4 versus replace). Cline's production telemetry shows the ceiling: on one identical `replace_in_file` tool, Claude 4 Sonnet, Claude 4.5 Sonnet, and GLM-4.6 succeed at 95.8%, 96.2%, and 94.9% of edits.

Second, the two axes with sign flips that are not about the edit tool, text-versus-native protocol and parallel calling, are properties of the serialization path, not the prompt. BFCL's numbers say that the same Claude 3.5 Sonnet weights almost never issue parallel calls through native function calling and do so 70% of the time when prompted, and that Llama 3.1 loses 30 points in native mode. A harness chooses the path once per provider; the prompt never sees it.

Third, Cursor's own numbers do not isolate its per-model customization. Cursor has published one quantitative result tied to a model-specific harness variable, the 30% Codex reasoning-trace figure, and it concerns API plumbing. The patch-versus-replace claim, the shell-style renames, and the provider-specific prompt text are asserted without measurement. Cursor's Composer 2 tech report (Table 1, March 2026) compares its harness against each lab's native harness on the same weights and scores lower in most pairs, for example GPT-5.3 Codex at 64.8 on Terminal-Bench in Cursor's harness against 77.3 self-reported. Confidence: high that per-model prompt text is the least-evidenced customization (no ablation exists from any vendor or independent source).

## 4. One string-replacement edit for all families beats the three alternatives on every criterion

The criteria are the three from section 1: does the option handle contract changes, what does it cost when the choice is wrong for a model, and does it put each difference at the layer that knows enough to make it. Four options, including the do-nothing.

Option A, do nothing: each `tools:` slot names an exact capability id, and the author picks. Today PromptForge has no built-in edit capability, so the question is deferred until one exists. When one does, this option bakes its format into every prompt that binds it, and a prompt that binds `promptforge/fs/apply_patch` would break on Grok and GLM. Cheap now, wrong later.

Option B, one string-replacement edit capability for every family. Exact-match-once on `old_string`, `replace_all` flag, create via a separate `write`, line-numbered `read` output that the description tells the model to treat as metadata. This is the format Anthropic trained on, that Cursor gives Claude and Grok, that Copilot gives Gemini, grok-code, and MiniMax, and that costs OpenAI's GPT-5.2 Codex under 5 points relative to its trained format. It changes nothing in the YAML contract or the gateway. The cost is a few points on OpenAI models and possibly more on future OpenAI models trained harder on patches.

Option C, an `edit` role satisfied at fill time. The slot declares a requirement rather than an identity (`edit: { want: promptforge/fs/edit }`), and `fill_tool_bindings` resolves it to `promptforge/fs/str_replace` or `promptforge/fs/apply_patch` from the bound model's family, in the same prepare step that fills `models:` roles. The model still sees `edit`; the schema and description follow the chosen capability; dispatch keys on the alias unchanged. Two prerequisites: `ModelDescriptor` carries `id`, `description`, `context`, and `thinking` and no family, so the catalog must expose one; and the prompt's prose must stay format-neutral, with format-specific guidance ("re-read before patching", "keep hunks small") shipped by the capability as a prompt fragment. The 2026-09-13 design already names fuzzy `want` and capability prompt fragments as deferred; this is the concrete reason to un-defer both. The cost is the second edit capability, the family field, and a correctness dependency on model pinning: once `edit` can carry two schemas under one name, a mid-conversation switch replays patch-shaped calls to a model whose `edit` expects `old_string`.

Option D, full per-model dialects as Cursor does: per-family tool names, descriptions, and prompt text. Section 3 shows this is the least-evidenced customization, and section 2.2 shows the renames are cosmetic. The alias mechanism already lets an author pick shell-flavored names. Not worth its maintenance cost.

Table 4 scores the options.

Table 4. Options against the three criteria.

| Option | Handles the edit contract change | Cost when wrong for a model | Puts each difference at the right layer | Verdict |
|---|---|---|---|---|
| A. Do nothing | No; format baked per prompt | High for non-OpenAI models if patch chosen | No | Reject |
| B. One str_replace edit for all | Yes, by choosing the robust format | Under 5 points on OpenAI (medium confidence) | Yes for the prompt; gateway untouched | Adopt now |
| C. `edit` role filled per family | Yes, structurally | Near zero once families are correct | Yes; requires family field and pinning | Design for, ship when a second format is justified |
| D. Full per-model dialects | Yes, plus renames and prompt text | Near zero | No; least-evidenced work at the most expensive layer | Reject |

The transport-layer duties from sections 2.3 and 2.4 are orthogonal to these options and apply under all of them: a provider-aware replay policy for `reasoning_content` and ids in the model client, and the llama-server duties in Appendix C for the gateway.

## 5. Ship one edit format now, build the fill seam, and fix replay in the client

Adopt Option B now and design the fill seam for Option C. Confidence: high on B being safe for Anthropic, Gemini, Grok, and open models (it is their trained format); medium on B costing OpenAI models under 5 points (one 180-task benchmark and one partial replication, no Cursor Bench-scale data).

The steps, each with an owner and a first action:

1. Edit capability (PromptForge owner). Write the design note for `promptforge/fs/str_replace` and `promptforge/fs/write`: exact-match-once, `replace_all`, absolute paths, the error strings from Appendix A, and a `read` whose description marks line-number prefixes as metadata. Claude Code's three-check rule (read before edit, exact match, uniqueness) is the reference behavior.

2. Fill seam (PromptForge owner). Amend the 2026-09-13 capability design to un-defer `want:` on tool slots and capability-contributed prompt fragments, and add a `family` field to the gateway catalog entry and `ModelDescriptor`. No second edit capability ships until a model shows a measured need; the seam is the deliverable.

3. Replay policy (PromptForge owner, model client). Stop discarding `reasoning_content` in the Lua history layer; store it on the assistant record and let the model client decide per provider whether to send it. DeepSeek with tools is a hard failure today; gpt-oss, Kimi, GLM-4.7+, and Qwen3 thinking are silent degradations. Add id preservation and, for Mistral endpoints, nine-character id minting at the `Upstream` seam.

4. Gateway duties (PromptForge owner, gateway). Implement the Appendix C list for the local path: check `/props` `supports_tool_calls` before forwarding `tools`, forward `chat_template_kwargs` and top-level `reasoning_effort`, translate the named-function `tool_choice` object, never forward `grammar` with `tools`, and detect leaked tool markup in `content` as a parse failure rather than final text.

5. Model switching (PromptForge owner). Leave the current behavior (selection read at launch, effective next run) while Option B is the only edit format; the replayed history is provider-neutral and the cost of a switch is one cache miss plus Cursor's unmeasured out-of-distribution concern. Pin the model per session in the same change that ships a second edit capability, because that is the day the same alias can carry two schemas in one history.

## 6. Limitations

The evidence has four weak points. Cursor's 2026 GPT-dialect schemas were never captured byte-exact; the tool names are verified, the parameters are self-reported. The claim that string replacement costs OpenAI models under 5 points rests on Bölük's 180-task benchmark and nwyin's partial replication, and the replication reversed Bölük's hashline-versus-replace finding for some models, so treat hashline-specific numbers as contested while the patch-on-non-OpenAI failure rates are consistent across both. No vendor or independent source has ablated per-model system prompt text; the absence of evidence is not evidence of no effect. And the out-of-distribution cost of replaying one model's transcript to another has never been measured by anyone, including Cursor, whose recommendation to stay on one model is a judgment, not a result.

One source was rejected: the "clawRxiv 2604.00687" tool-renaming paper is agent-generated with no human authors or code and is not cited here. Several Terminal-Bench per-harness rows disagree between secondary compilations and are not relied on.

## Appendix A: edit tool contracts side by side

Table A1. Production edit tools by family. Condensed from the edit-tool schemas collection; "UNVERIFIED" marks schemas not captured byte-exact.

| Tool | Family | Granularity | Match rule | Create / delete in same tool | Replace-all | Line numbers in payload |
|---|---|---|---|---|---|---|
| `str_replace_based_edit_tool` (`text_editor_20250728`) | Anthropic API | one op per call (`view`, `create`, `str_replace`, `insert`) | exact once | create yes, delete no | no | `insert_line`, `view_range` only; `view` returns `cat -n` style |
| `apply_patch` V4A (GPT-4.1 guide) | OpenAI | multi-hunk, multi-file | three context lines plus optional `@@` anchor, first match | Add / Update / Delete (Codex adds Move) | n/a | forbidden |
| `{type: "apply_patch"}` Responses built-in | OpenAI | one file op per `apply_patch_call` | context anchors; the harness applies | `create_file` / `update_file` / `delete_file` | n/a | forbidden |
| Codex `apply_patch` (Lark grammar) | OpenAI | multi-hunk, multi-file | exact, then rstrip, trim, Unicode punctuation normalization | Add / Update / Delete / Move | n/a | forbidden |
| Cursor `StrReplace` (2026, Claude and Grok) | Cursor | single hunk | exact once unless `replace_all` | no (`Write`, `Delete` separate) | yes | no; `Read` shows `LINE|` as metadata |
| Cursor `ApplyPatch` (2026, GPT-5.6) | Cursor | multi-hunk | V4A-style (UNVERIFIED) | UNVERIFIED | n/a | no |
| Claude Code `Edit` | Anthropic CLI | single hunk | exact once unless `replace_all`; read-before-edit enforced | no (`Write`) | yes | no |
| Gemini CLI `replace` | Google | single hunk | exact, then whitespace-flexible, regex, fuzzy, LLM fixer; once unless `allow_multiple` | create via empty `old_string` on a missing file | yes | no; required `instruction` field |
| Copilot `replace_string_in_file` / `multi_replace_string_in_file` | Microsoft | single hunk / multi-hunk multi-file sequential | exact, whitespace-flexible, fuzzy regex, similarity 0.95 | no (`create_file`) | no | no |
| Copilot `apply_patch` | Microsoft | multi-hunk, multi-file | six-pass canonicalized match ending in Levenshtein | Add / Update / Delete | n/a | forbidden |
| Aider editblock (`diff`) | Aider | multi-block per message | exact, leading-whitespace tolerant, `...` elision | create via empty SEARCH | no | no |
| hashline v2 (Bölük) | third-party | multi-hunk, multi-file, `PUT` / `CUT` / `REM` / `MV` | per-file snapshot tag plus original line numbers | `REM`, `MV`; create via `write` | n/a | yes, tag-validated |

The shared postcondition: the designated region is replaced with the model's text and nothing else changes, or nothing is written and an error string returns. Appliers differ on line-ending normalization (Codex, Gemini), re-indentation (Gemini, Copilot, Aider), and atomicity across hunks (only Claude Code `MultiEdit` and hashline are atomic per file; Codex, Copilot multi-replace, and Aider leave earlier hunks applied on later failure).

Parameters with no cross-family mapping: `@@` scope anchors; `replace_all` / `allow_multiple`; `insert_line` and any line-addressed op; `Move to`; Gemini's `instruction`; Anthropic's `undo_edit` (20250124 only); Cursor `edit_file` and Copilot `insert_edit_into_file` sketches, whose postcondition a second model decides; path convention (relative-only in OpenAI's instructions, absolute-only in Claude Code and Copilot).

Reference error strings for a string-replacement capability: Anthropic's reference implementation returns "No replacement was performed, old_str ... did not appear verbatim" on no match and reports the count on multiple matches; Claude Code refuses an edit on a file not yet read in the session; before v2.1.208 it also refused any file changed on disk since the read, and since v2.1.208 it allows that edit when `old_string` still matches exactly once and notes the other changes in the result so the model re-reads before dependent edits.

## Appendix B: history replay rules by provider

Table B1. What must be done to provider A's history before sending it to provider B over native APIs. HARD = documented 400; SOFT = server drops, request succeeds, reasoning lost; QUAL = no error, quality degrades. Condensed from the history replay collection.

| From / To | Anthropic | OpenAI Responses | Gemini 3 | DeepSeek, Kimi, GLM, Qwen | Mistral |
|---|---|---|---|---|---|
| Anthropic | same model: keep thinking verbatim; newer Claude reads older blocks, older drops newer (SOFT) | strip `thinking`; map `tool_use` to `function_call`, `tool_result` to `function_call_output`; QUAL | strip signatures; dummy-sign current-turn calls or omit (3.1+); QUAL | drop thinking; DeepSeek then requires `reasoning_content` on every later turn; Kimi needs `functions.name:idx` ids | remint ids to nine alphanumerics or HARD 3280 |
| OpenAI Responses | strip `reasoning` items (unsigned thinking rejected); regroup results into one user message; QUAL | same org and family: replay `encrypted_content`; cross-org or provider HARD `invalid_encrypted_content` | strip reasoning; dummy-sign | drop reasoning | remint ids |
| Gemini 3 | strip signatures; synthesize ids; group results | strip signatures; synthesize `call_id` | same endpoint only; AI Studio to Vertex is HARD | drop signatures; synthesize ids | synthesize ids |
| DeepSeek, Kimi, GLM, Qwen | drop `reasoning_content` (do not render as text; Claude mimics it) | drop | convert; dummy-sign | field name shared, content model-specific; DeepSeek still requires the field once tools exist | remint ids |

Rules that break in every direction: Anthropic requires all `tool_result` blocks in one user message immediately after the `tool_use` message; OpenAI Chat Completions requires one `tool` message per `tool_call_id` immediately following; Gemini requires all parallel `functionCall`s before their `functionResponse`s. Dangling calls are 400 on Anthropic and OpenAI. Every switch is a prompt-cache miss, and on Fable 5.1 the same prefix edits that miss cache also invalidate thinking blocks.

Harness behavior on switch, for reference: Cursor swaps in the new model's harness, injects "taking over mid-chat" instructions, accepts the cache miss, and recommends one model per conversation; OpenCode's `differentModel` guard strips signatures; Codex replays `encrypted_content` verbatim and fails on switch; Zed stored OpenAI reasoning as `RedactedThinking` and broke GPT-to-Claude switches until fixed.

## Appendix C: gateway duties for llama-server

Table C1. Residual per-family duties for an OpenAI-shaped gateway forwarding to llama-server after PR #18675. Condensed from the llama.cpp duties collection, which cites file and line for each.

| Duty | Families affected | What breaks if skipped |
|---|---|---|
| Check `/props` `chat_template_caps.supports_tool_calls`; refuse or self-handle `tools` when false | Gemma 3, Phi-4, Mixtral v0.1, any template without tool rendering | tools silently ignored: prose answer, `finish_reason: "stop"`, no `tool_calls`, no error |
| Forward `reasoning_content` on assistant history verbatim | gpt-oss, Kimi K2/K2.5, Qwen3.x, GLM-4.7+, Gemma 4, DeepSeek V3.2+, MiniMax | lost chain-of-thought between calls; correlated with Qwen3.6 long-session loops (#26781) |
| Preserve `tool_calls[i].id` to `tool_call_id` pairs and order; mint nine-character ids for Mistral Nemo templates | Mistral Nemo (raises), Kimi K2 and Gemma 4 (positional), DeepSeek V4 (sorts by id) | Jinja `raise_exception` becomes a 500; results attach to the wrong call |
| One `tool` message per call, string content, in call order, immediately after the assistant turn | Gemma 4, Cohere2, DeepSeek V4, Qwen3-Coder | merged-turn name mismatch or lost responses |
| Set `parallel_tool_calls: true` only when the template supports it; split multi-call history for single-call templates | Llama 3.1 / 3.2 / 3.3 | "This model only supports single tool-calls at once!" on replay |
| Translate the named-function `tool_choice` object; never rely on `required` without `max_tokens` | all | named form silently becomes `auto`; `required` runs to `max_tokens` with no call (#27217) |
| Never forward client `grammar` with `tools` | all | 400 "Cannot use custom grammar constraints with tools." |
| Pass `chat_template_kwargs` and top-level `reasoning_effort` through; coerce `enable_thinking` to boolean | Qwen3.x, gpt-oss, GLM, Gemma 4 | thinking cannot be toggled per request; string `"false"` is a 400 |
| Ship `--chat-template-file` overrides for known-bad GGUF templates | GLM-5.x (`m.content.0.type`), Gemma 4 interleaved, DeepSeek R1 distills, Phi-4-mini | template load failure or tools ignored |
| Treat leaked tool markup in `content` (`<tool_call>`, `[TOOL_CALLS]`, `<|DSML|`, `<|channel|>commentary`) as a parse failure | GLM, Qwen3-Coder, any autoparser family when the lazy trigger misses | raw markup shown and the turn ends (Cursor forum topic 165182; llama.cpp #26530) |
| Do not use `chat_format` to identify a family | all | post-#18675 nearly everything reports `peg-native` |

## Appendix D: open-weight tool-call formats

Table D1. Native tool-call envelope, id ownership, parallel support, reasoning replay, and result carrier per family. Condensed from the open-weight templates collection.

| Family | Call envelope | Id owner | Parallel | Reasoning replay rule | Result carrier |
|---|---|---|---|---|---|
| Qwen 2.5 / 3 | `<tool_call>{json}</tool_call>` | server | yes | keep only after last real user turn | user turn, `<tool_response>` |
| Qwen3-Coder | `<function=n><parameter=k>v</parameter></function>` | server | yes | none in Instruct | user turn |
| Llama 3.1 / 3.3 | `<|python_tag|>{json}<|eom_id|>` | server | no (single call) | none | `ipython` role |
| Llama 3.2 small / Llama 4 | pythonic `[f(a=1), g(b='x')]` | server | yes | none | `ipython` role (Llama 4 UNVERIFIED) |
| Gemma 3 | none native; ` ```tool_code` ` fence by convention | server | prompt-dependent | none | user text |
| Gemma 4 | `<|tool_call>call:n{k:<|"|>v<|"|>}<tool_call|>` | server | yes | keep between calls within a turn (interleaved template) | inside the model turn (`tool_responses`) |
| gpt-oss | `<|channel|>commentary to=functions.n ... <|call|>` | server | yes | required on tool turns, dropped after `final`; no `content` plus `thinking` on one tool message | `functions.n to=assistant` pseudo-role |
| DeepSeek V3 / V3.1 / R1 | `<｜tool▁calls▁begin｜>...` block tokens | server | yes | `<think>`; history thinking stripped | `<｜tool▁output▁begin｜>` |
| DeepSeek V3.2 | DSML `<｜DSML｜invoke name=".."><｜DSML｜parameter ...>` | server | yes | dropped before last user message | `<function_results>` |
| GLM-4.5 to 5.x | `<tool_call>n<arg_key>k</arg_key><arg_value>v</arg_value></tool_call>` | server | yes | `clear_thinking=false` keeps all | `<|observation|>` role |
| Kimi K2 / K2.5 | `<|tool_call_begin|>functions.n:0<|tool_call_argument_begin|>{json}` | model (`functions.n:idx`, load-bearing) | yes | K2.5 keeps for whole tool loop; calls may occur inside `<think>` | `<|im_system|>tool` |
| Mistral v3 / v11 | `[TOOL_CALLS][{..., "id": "XXXXXXXXX"}]` | model, nine characters required | yes | `[THINK]` on Magistral | `[TOOL_RESULTS]` |
| Mistral v13 (Devstral 2, Ministral 3) | `[TOOL_CALLS]n[ARGS]{json}` | server (no id) | yes | `[THINK]` on reasoning variants | `[TOOL_RESULTS]` |
| Phi-4-mini | `<|tool_call|>[{json}]<|/tool_call|>` | server | array form | UNVERIFIED | UNVERIFIED (not in official template) |
| MiniMax M2 / M2.5 | `<minimax:tool_call><invoke name="n">...` | server | yes | kept after last user message | `]~b]tool` role |
| Command A / R7B | `<|START_ACTION|>[{"tool_call_id": "0", ...}]` | model (positional) | yes | `<|START_THINKING|>` | inside the chatbot turn |
| Granite 4.x | `<tool_call>{json}</tool_call>` | server | yes | none | user turn |

## References

Primary sources cited in the body, by section. The nine research collections hold the full list of roughly 150 sources with verbatim quotes.

Cursor: "Continually improving our agent harness" (cursor.com/blog/continually-improving-agent-harness, 2026-04-30); "Improving Cursor's agent for OpenAI Codex models" (cursor.com/blog/codex-model-harness, 2025-12-04); "Composer 2 technical report" (arxiv.org/html/2603.24477v2, Table 1); pi-cursor-sdk hash-verified system-prompt capture (github.com/fitchmultz/pi-cursor-sdk, docs/evidence/cursor-system-prompts-2026-08-02); Cursor forum topic 165182 "GLM 5.2: Tool calls terminate chats".

Vendors: OpenAI GPT-4.1 prompting guide and GPT-5 prompting guide (cookbook.openai.com); OpenAI "Introducing GPT-4.1 in the API" (2025-04-14); OpenAI Responses `apply_patch` and `shell` tool guides (platform.openai.com); Anthropic text editor tool, extended thinking, and tool use documentation (docs.anthropic.com); Anthropic "Raising the bar on SWE-bench Verified" and "Writing tools for agents"; Google Gemini function calling and thought-signature documentation (ai.google.dev); DeepSeek, Moonshot, Mistral, Zhipu, Alibaba API documentation.

Harness code: openai/codex (`codex-rs`, `models.json`, PR #39772); anomalyco/opencode (`usePatch`, `session/system.ts`); Kilo-Org/kilocode; RooCodeInc/Roo-Code PR #10170; cline/cline changelog 3.17.9 to 3.46.0; microsoft/vscode-copilot-chat `chatModelCapabilities.ts`; google-gemini/gemini-cli `model-family-sets`; Aider-AI/aider `model-settings.yml`; All-Hands-AI/OpenHands `fn_call_converter.py`; zed-industries/zed PRs #32737 and #52083; code.claude.com tool documentation (v2.1.142, v2.1.208, v2.1.233).

Measurements: Aider edit-format leaderboard and blog posts (aider.chat, 2023-12 to 2025-04); JetBrains Diff-XYZ (arxiv.org/html/2510.12487); Bölük "The Harness Problem" (blog.can.ac, 2026-02-12); nwyin/edit-bench issues #8, #13, #14 (2026-03); yaoyi1222/edit-tool-bench; Cline "Improving Diff Edits by 10%" (2025-06-24), v3.18 and GLM-4.6 posts; SWE-agent (arxiv.org/abs/2405.15793, Table 3); Berkeley Function Calling Leaderboard `data_overall.csv`; RoTBench (arxiv.org/abs/2401.08326); PA-Tool (arxiv.org/pdf/2510.07248v1); "The Scaffold Effect" (KDD 2026 agentic AI evaluation workshop); Anthropic Tool Search announcement; HumanMCP tool-count study.

llama.cpp: PR #18675 (autoparser, 2026-03-06), PR #18994 (`reasoning_content` forwarding), PR #21418 and #21704 (Gemma 4), issues #19701, #19703, #26530, #26781, #27217; `common/chat.cpp`, `common/chat-auto-parser*.cpp`, `common/parsers/`, `tools/server/server-common.cpp`; model templates under `models/templates/` and the Hugging Face model cards for each family.

---

*2026-09-20 - Claude Fable 5.1 (Cursor agent). Synthesized from nine research collections produced the same day; the rulebook audit (sections 3, 4.2, 6) was run on the finished draft.*
