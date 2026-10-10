---
produced: 2026-10-10
title: Naming and behavior of model-facing subagent tools across coding harnesses, agent frameworks, and model training (Claude Code Agent/Task, Cursor Task, Codex spawn_agent and wait_agent, Copilot CLI task and read_agent, Qwen agent, Kimi Agent, DeepSeek subagent, TaskOutput, TaskStop, completion notices, timeout units, task_id) - recommendation for PromptForge subagents_run, subagents_join, subagents_cancel
---

# PromptForge: Naming the Subagents Plugin's Model Tools So Models Call Them Without Coaching

Report type: analytical / recommendation. It asks what tool names, parameter names, and behaviors PromptForge's planned `subagents` Plugin should give its three model-facing tools, so that frontier and open-weight models call them correctly with what they saw in training. It judges five options, from shipping the plan unchanged to per-model dialects, against five criteria, and ends with owned recommendations. It builds on the behavioral survey "How Agent Harnesses Let a Model Spawn, Watch, and Stop Subagents" (2026-10-10) and does not repeat it.

## Executive summary

Keep the three wire names the owner chose, `subagents_run`, `subagents_join`, and `subagents_cancel`, and put the effort where the evidence says models look: the parameters and the descriptions. The plan's spawn parameters, `description`, `prompt`, `subagent_type`, and `run_in_background`, already match the shape most models have seen. That shape is Claude Code's `Agent` tool, which Moonshot, Alibaba, and Z.ai also ship in their own harnesses. Three small changes are worth making before Part 4 starts. Name the join timeout's unit (`timeout_seconds`). Call the id parameters `task_id` and `task_ids`, so they match the `Task id=N` text the model reads. And tell the model plainly to join a background subagent before it replies, because PromptForge stops the subagent when the section ends.

No vendor documents training a model on a subagent tool name that PromptForge's id rule can produce. Frontier vendors state training only for edit, shell, and a few other client tools, none of them a delegation tool. The two closest signals are OpenAI's API reserving `collaboration.spawn_agent` with a `{task_name, message, fork_turns}` schema for GPT-5.6 models, and Moonshot's Kimi K2.5 report printing `create_subagent` and `assign_task`. Across harnesses the spawn names scatter: `Agent`, `Task`, and `task` lead among closed harnesses, `task` and `agent` among open ones, and no surveyed harness, framework, or protocol has a tool called "join".

When tool names are removed in a controlled study, parameter names alone keep GPT-5 at 0.82 accuracy against 0.95 with full documentation. A rename to a trained name would reopen the owner's choice of `subagents` and need a new naming rule. Hidden aliases would cut against the Engine's new wire-name-only lookup. Neither has a measured payoff. A cheaper guard sits outside this plan: today a model's call to an unoffered tool name ends the round, while Anthropic's docs and several harnesses answer it with an error the model can act on.

The plan's behaviors mostly match the field, and the owner's choices hold up. Blocking by default is the majority among harnesses with a background switch, though Claude Code and Qwen Code moved to background by default in July 2026. Pointer-only notices are a minority pattern: 3 closed harnesses use them, while 6 closed and 11 open harnesses put the result in the notice. GitHub Copilot CLI ships pointer notices across more than 20 models, so they work. The plan's stated reason is wrong, though: "this is how Cursor notifies about a background agent". Cursor's notice includes the subagent's full final message.

The largest risk is a habit, not a name. Claude Code, Cursor, Copilot CLI, opencode, Qwen Code, and Hermes Agent all tell the model to end its turn after a background spawn, because those harnesses wake it when the child finishes. In PromptForge a text reply ends `models.loop`, and the section's end then stops the subagent, so the model must hear the opposite rule.

### Key judgments

1. **Parameters hold the trained signal, and the plan already matches them.** For Claude and for the open-weight families trained in Claude Code, it is very likely that a spawn tool reads best with `description` as a 3-5 word label, `prompt` as the instructions, and `subagent_type` as the selector. Confidence: high, because `prompt` names the task text in 26 of the surveyed harnesses, the full three-name set appears in 14, and a Deep Agents issue shows Claude Sonnet 5 inventing a `prompt` key when it was missing.
2. **The spawn name matters less than its parameters and description.** It is unlikely that the wire name `subagents_run` by itself makes a frontier model fail to call the tool, given Claude Code's parameters and description text. Confidence: medium, because no study tests subagent tool names, and the inference rests on general tool-naming studies and vendor guidance.
3. **No trained name fits the id rule.** Only a Plugin named after a verb (a Plugin `spawn` with a tool `agent`, giving `spawn_agent`) could produce a trained name, and the join and cancel tools could not follow it. This is a fact about the rule, not a forecast.
4. **Background spawns meet a harmful habit.** It is likely that a model which starts a background subagent and has nothing else to do will reply without calling `subagents_join`, unless the tool text tells it not to. Confidence: medium, because the "end your turn" instruction is documented in six widely used harnesses, but PromptForge has no measurement.
5. **A bare `timeout` invites unit errors.** It is likely that some models will at least occasionally pass milliseconds to a `timeout` meant as seconds. Confidence: medium, because bare `timeout` means milliseconds in four harnesses including Claude Code's former `TaskOutput`, and a public dataset shows Claude models sending `"timeout": 120000` there.
6. **Pointer-only notices work at a cost.** It is likely that models follow a pointer notice that names the collecting tool, at the price of one extra call per background subagent. Confidence: medium, because Copilot CLI ships the pattern but publishes no failure rate.
7. **One surface cannot match every family.** GPT-5.6 and later were very likely trained on `collaboration.spawn_agent {task_name, message, fork_turns}`, which no Claude-Code-shaped surface can match at the same time. Confidence: medium, because the evidence is an API reservation error, not an OpenAI statement.
8. **Hidden aliases are unlikely to pay.** It is unlikely that accepting `Task`, `Agent`, or `spawn_agent` as aliases would rescue many calls. Confidence: medium, because no case shows a model calling another harness's subagent name in place of a differently named offered tool, and vLLM drops such calls before a harness sees them.

### Recommendations at a glance

Each is detailed, with owner and next step, in the recommendations section.

1. Keep `subagents_run`, `subagents_join`, and `subagents_cancel`; add no aliases and no bare-name exception. Confidence: medium, because names are untested but every measured signal favors parameters and descriptions.
2. Write the `subagents_run` description and its parameter descriptions in the Claude Code phrases the field reuses. Confidence: high, because the phrases recur verbatim across more than 15 harnesses and cost only text.
3. Keep the four spawn parameters, `subagent_type` required as an enum, and blocking by default. Confidence: high, because this is the converged shape in vendor-built harnesses.
4. Tell the model, in the background ack and the `run_in_background` description, to join before it replies. Confidence: medium, because the habit is documented but its rate in PromptForge is unmeasured.
5. Rename `timeout` to `timeout_seconds` and cap it with a required-versus-actual error. Confidence: medium, because the field splits on the unit of a bare `timeout`.
6. Rename `id` and `ids` to `task_id` and `task_ids`, typed as strings passed verbatim. Confidence: medium, because it is the majority spelling and matches the ack, though no failure with `id` is recorded.
7. Keep `join`, the `any` boolean, the wait-for-all default, and the sleep, and describe them in four sentences. Confidence: medium, because these are owner decisions and no evidence shows `join` hurts.
8. Keep pointer-only notices, but correct the Decision Record's reason to cite Copilot CLI, not Cursor. Confidence: medium, because the pattern ships in production while most of the field inlines results.
9. Keep `subagents_cancel` under the verb cancel. Confidence: medium, because half the field offers no cancel and "cancel" is the protocol verb.
10. Ship one surface for every model family, and add delegation guidance for GPT-family runs to the author docs. Confidence: low, because the GPT guidance is inferred from vendor prompts and untested in PromptForge.
11. Outside Part 4, answer a model's call to an unoffered tool name with a failed tool result listing the valid names, instead of ending the round as the Engine does today. Confidence: medium, because Anthropic's docs and three harnesses do this, but no PromptForge failure of this kind is recorded.

## Contents

1. Scope: three tools, one notice, and a naming rule that forbids bare names
2. Five criteria judge the options, with training fit first
3. Five options for the whole surface, and why Option B wins
4. Finding 1: Keep `subagents_run`, because no trained name fits and the name matters least
5. Finding 2: The plan's spawn parameters are the trained shape
6. Finding 3: Background spawns meet an "end your turn" habit that section lifetime punishes
7. Finding 4: Keep `join`, `any`, and the sleep, but name the timeout's unit
8. Finding 5: Pointer-only notices work, but the plan cites the wrong precedent
9. Finding 6: Keep "cancel", and call the id `task_id`
10. Finding 7: One surface serves Claude and the open-weight families best, GPT least
11. Finding 8: The old task tools had an in-distribution name and out-of-distribution parameters
12. Eleven recommendations, each with an owner, a next step, and a confidence
13. Six kinds of evidence would change these judgments
14. The new notes correct the earlier survey in four places and disagree with each other in four
15. Method and limitations
16. Appendix A: Spawn tools
17. Appendix B: Wait, read, and join tools
18. Appendix C: Cancel tools
19. Appendix D: Launch acks and completion notices
20. Appendix E: Training statements and usage data
21. Sources

## Scope: three tools, one notice, and a naming rule that forbids bare names

**The surface under review.** Part 4 of the plan "Plugin registry, parallel tool calls, and the tasks and subagents Plugins" gives the model three tools and one notice:

- `subagents_run { description, prompt, subagent_type, run_in_background? }` blocks by default and answers with the worker's final text, verbatim; in the background it answers `Task id=N started`.
- `subagents_join { ids?, timeout?, any? }` takes a timeout in seconds and collects every subagent the section started and has not joined, finished or running. It waits for all by default, or for the first with `any: true`, and sleeps when there is nothing to wait on.
- `subagents_cancel { id }` stops one of the section's subagents.
- A completion notice is one line ahead of the model's next round: `Task id=0.3 (researcher) finished. Call subagents_join to collect its result.`

A subagent lives only as long as the section whose model started it. The surface replaces four bare-name built-ins, `task`, `task_cancel`, `task_status`, and `await_tasks`, which `tools.allow_tasks` switched on.

**The naming rule.** Every PromptForge tool belongs to a Plugin and has the id `<plugin>/<tool>`. The model sees only the wire name, the id with `/` and `.` replaced by `_`, so `subagents/run` becomes `subagents_run`. Every provider surveyed rejects `/` in tool names, and OpenAI, Anthropic, and Bedrock also reject `.`, so some mangling is unavoidable (provider docs, gathered 2026-10-10). A bare name such as `Agent` cannot come out of this rule. Since the plan "Author API debt removal" (2026-10-10), the Engine also resolves a model's tool call by wire name only, never by canonical id or alias. A model's call to any name the round did not advertise is a hard error that ends the round.

**Terms.** A *harness* is the program that runs a model and gives it tools; *closed* and *open* refer to whether its source is public. A *push notice* is a message the harness injects when a background child finishes. An *inline* notice includes the child's result, while a *pointer* notice names the tool that collects it. An *ack* is the immediate answer to a background spawn. *Subagent* and *child* name the same thing: the agent a parent model starts; the report says child mostly when describing other harnesses' mechanics.

**Evidence classes.** Each finding separates three kinds of evidence. *Stated* means a vendor or model builder said it in a doc, model card, tech report, or blog. *Observed* means it was read in code at a pinned commit, in a shipped bundle, in a captured session, or in a dataset. *Inferred* is my judgment from the first two. Source quality is named where a claim depends on it; the strongest sources are official docs and source code, and the weakest are third-party captures and forum reports.

**Calibration.** Likelihood uses one ladder: very unlikely, unlikely, roughly even chance, likely, very likely, almost certain. Confidence in the evidence is low, medium, or high, and always sits in its own sentence. Counts of harnesses measure how many products use a name, not how often models saw it in training.

**Owner decisions.** The plan's Decision Record separates choices the owner made, with his words, from defaults chosen in planning. Where a recommendation touches an owner decision, the report quotes it and says so.

## Five criteria judge the options, with training fit first

The options are judged against five criteria, in priority order.

1. **In distribution.** The names, parameters, and texts should match what the target models saw in harnesses they were trained or tuned in. This criterion counts most, because it is the question the report serves.
2. **Unambiguous on a cold read.** A model reading the schema for the first time should not be able to misread a unit, an id, or a verb.
3. **Fits PromptForge's rules.** The surface should keep `<plugin>/<tool>` ids and wire-name-only resolution, and should not bring back bare names that shadow other tools, a defect the plan exists partly to remove.
4. **Respects owner decisions.** A change that reopens an owner decision needs strong evidence, and the report names each such reopening.
5. **Cheap to adopt.** Changes to strings and tests in Part 4 beat new Engine rules.

## Five options for the whole surface, and why Option B wins

Five options cover the credible space, doing nothing included. Table 1 scores each against the criteria; the prose after it gives the trade-offs. Option B is the recommendation.

- **Option A, do nothing.** Ship the plan as written: the three names, `id`, `ids`, and a bare `timeout`, the ack `Task id=N started`, an unspecified base description, and pointer notices justified by Cursor.
- **Option B, keep the names and fix the words.** Keep the three names and the owner's behaviors. Write the descriptions in the Claude Code phrases the field reuses, rename three parameters (`timeout_seconds`, `task_id`, `task_ids`), add a join-before-reply rule to the ack and the background flag, and correct the notice rationale.
- **Option C, a trained bare name.** Add a rule that lets a native Plugin advertise a bare wire name, so `subagents/run` reaches the model as `Agent` (Claude Code's current name) or `Task` (its former name and Cursor's).
- **Option D, hidden aliases.** Keep the names, but route calls named `Task`, `Agent`, `task`, `agent`, or `spawn_agent` to `subagents_run`, as Roo Code's `TOOL_ALIASES` and Kilo Code's `resolveToolAlias` do for other tools.
- **Option E, per-family dialects.** Advertise a different name and schema per model family, for example `Agent` with `prompt` to Claude and `spawn_agent` with `message` to GPT, as Cursor provisions each model "with the tool format it had during training".

*Table 1. The five options scored against the criteria. "Yes" means the option meets the criterion, "partly" that it meets it for some models or with a caveat, and "no" that it fails it.*

| Option | In distribution | Unambiguous | Fits PromptForge's rules | Respects owner decisions | Cheap |
|---|---|---|---|---|---|
| A. Do nothing | partly: parameters yes, name neutral | no: bare `timeout`, bare `id` | yes | yes | yes |
| B. Keep names, fix words | partly: parameters and text yes, name neutral | yes | yes | yes, except three parameter spellings | yes |
| C. Trained bare name | partly: Claude yes, GPT no | yes | no: new rule, shadowing returns | no | no |
| D. Hidden aliases | partly: only when a model calls an unoffered name | yes | no: cuts against wire-name-only lookup | yes | partly |
| E. Per-family dialects | yes for the mapped families | yes | no: new rule per family | no | no |

**Option A** costs nothing and is defensible on names, because the parameters already match the trained shape (Finding 2). It leaves two ambiguities a model can trip on, a `timeout` whose unit the field splits on (Finding 4) and an `id` that does not echo the `Task id=N` text (Finding 6). It also leaves the base description to the implementer, and it ships an ack that says nothing against the field's "end your turn" habit (Finding 3).

**Option B** keeps everything the owner chose and changes only what the model reads. Its three parameter renames edit the spelling inside an owner-approved decision line, quoted in Finding 6, but not the tools or behaviors that decision chose. Its cost is string and test changes in Part 4.

**Option C** would match Claude Code's current name, which an opt-in usage tracker counts at 47,304 calls from 210 developers. It reopens the owner's naming decision: 'User chose "subagents, with tools subagents/run, subagents/join, subagents/cancel"', with `agents/run` and `agents/spawn` rejected and marked "No revisit". It needs a rule that breaks the `<plugin>_<tool>` form, and a bare `Agent` could shadow a local tool of the same name, the problem the plan's first bullet lists against today's built-ins. It also helps only Claude-family models: GPT's trained name is `spawn_agent`, and join and cancel would still have no trained counterpart.

**Option D** would help only when a model calls a name that was not offered. No case in the evidence shows a model calling `Task` or `Agent` in place of a differently named offered subagent tool. It would cut against the Engine's wire-name-only lookup, and under vLLM such a call never reaches the harness anyway. A cheaper guard keeps exact lookup: answer an unoffered name with a failed tool result that lists the valid names, instead of ending the round as the Engine does today (Finding 1, recommendation 11).

**Option E** fits each family best on paper, but it multiplies schemas and tests, needs a rule that maps models to families, and invites a specific failure: a trained name pulls in its trained arguments. Deep Agents shows that pull (Finding 2), and a `spawn_agent` that takes `prompt` instead of `message` would invite it on GPT models.

A sixth idea is to name Plugins after verbs, so that a Plugin `spawn` with a tool `agent` gives `spawn_agent`. It is set aside, because the join and cancel tools would need their own Plugins to get matching names, which would undo the two-Plugin design the owner chose.

## Finding 1: Keep `subagents_run`, because no trained name fits and the name matters least

`subagents_run` should stay. No name PromptForge's rule can produce is one a model is documented as trained on, the field's spawn names scatter widely, and the measured evidence says a tool's parameters and description do more work than its name.

**What vendors stated.** No frontier vendor names a subagent tool it trained on. OpenAI's Codex prompting guide names `apply_patch`, `shell`, and `update_plan` as trained tools, and Anthropic's tool-use docs name `memory`, `bash`, `text_editor`, `computer`, and `browser`, saying "these schemas are trained-in" (both official docs, fetched 2026-10-10). Neither list holds a delegation tool. The closest statements are three:

- OpenAI wrote "We trained GPT-5.6 end-to-end with three complementary architectural interventions [...] 2. Parallel decomposition where appropriate: using native multi-agent orchestration" ([official blog, 2026-08-13](https://openai.com/index/builders-guide-to-gpt-5-6/)). Its API rejects a mismatched schema with "Function 'collaboration.spawn_agent' is reserved for use by this model and must match the configured schema" ([Codex issue 31864](https://github.com/openai/codex/issues/31864), opened 2026-07-09, a vendor error string reproduced by several reporters and re-read for this report). The reserved schema exposes "only `task_name`, `message`, and `fork_turns`" ([Codex issue 32705](https://github.com/openai/codex/issues/32705), forum, confirmed against source).
- Moonshot's Kimi K2.5 report says the orchestrator "is equipped with interfaces for sub-agent creation and task delegation", RL-trained, and prints `create_subagent {name, system_prompt}` and `assign_task {agent, prompt}` in its evaluation appendix ([tech report, 2026-02-02](https://arxiv.org/abs/2602.02276)). The report does not say those are the exact training interfaces.
- Anthropic says "Claude's latest models orchestrate subagents natively" when subagent tools are "available and described in tool definitions" ([official doc](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), undated, fetched 2026-10-10). Anthropic itself runs two unrelated delegation surfaces: Claude Code's `Agent` tool and Managed Agents' `create_agent`, `send_to_agent`, `wait_for_agents`, and `list_agents` ([official cookbook, 2026-07-02](https://platform.claude.com/cookbook/managed-agents-cma-plan-big-execute-small)).

On naming in general, OpenAI advises, for tools a model was not post-trained on, "Making the tool names and arguments as semantically "correct" as possible" ([official cookbook](https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide)). Anthropic reports that prefix versus suffix namespacing has "non-trivial effects on our tool-use evaluations. Effects vary by LLM" ([vendor blog, 2025-09-11](https://www.anthropic.com/engineering/writing-tools-for-agents)). Anthropic renamed Claude Code's `Task` tool to `Agent` in version 2.1.63 (2026-02-28) and kept `Task` as an alias "in settings and agent definitions", with no stated reason ([official doc](https://code.claude.com/docs/en/sub-agents), re-read 2026-10-10). Table 7 in Appendix E collects these statements together with the usage data and studies cited below.

**What was observed.** The spawn names scatter, and the noun names lead. Table 3 in Appendix A lists every harness; the counts are these:

- Among 20 closed coding-harness spawn schemas, 9 use a bare noun: `Agent` in 4 (Claude Code, Z.ai ZCode, Qoder, CodeBuddy), `Task` in 3 (Cursor, Amp, Factory), and `task` in 2 (Copilot CLI, Grok Build). Six contain "subagent" (Devin `run_subagent`, Antigravity `invoke_subagent`, Muse `subagent_spawn`, and three Kiro and Augment forms), and 2 use `spawn_agent`, both from OpenAI. None uses a Plugin-style prefix.
- Among about 30 open harnesses at pinned commits, `task` leads with 6 (plus `Task` in Kode), then `agent` or `Agent` with 4, then `spawn_agent`, `subagent`, and `delegate` with 3 each. Three of the four `agent` holders renamed to it in 2026: Qwen Code on 2026-03-19, Kimi CLI on 2026-03-23, and Letta Code on 2026-04-24.
- Among agent frameworks, Microsoft Agent Framework's `background_agents_start_task` and Strands' `strands_manage_background_task` use the same `<namespace>_<verb>` shape as `subagents_run`.

Renames in the field cite terminology or parity, never a measurement. Qwen Code's rename PR says "for clearer semantics and better alignment with industry terminology" ([PR 2489](https://github.com/QwenLM/qwen-code/pull/2489)). Letta Code's code comment says "Align subagent-spawning tool with Claude Code". Zed's says "with some back and forth verification + market research, we both agreed spawn_agent was a better name for what this tool is doing. It still calls the right tool if you ask for a subagent" ([PR 49741](https://github.com/zed-industries/zed/pull/49741)). Gemini CLI's back-and-forth was about schema shape: a single `delegate_to_agent` with one `anyOf` branch per agent caused "schema squashing" and `MALFORMED_FUNCTION_CALL` errors on Gemini 3 Pro ([PR 17346](https://github.com/google-gemini/gemini-cli/pull/17346)).

Usage data favors Claude Code's names. An opt-in tracker of real sessions counts `Agent` at 47,304 calls from 210 developers and `Task` at 19,264 from 9 developers. `spawn_agent` is absent from its top 25, although Codex's `wait_agent` has 54,266 calls ([whoburnedmore](https://whoburnedmore.com/research/ai-agent-tool-usage), data 2026-10-10, opt-in and "not a representative survey").

Controlled studies say names matter, but parameter names matter more. With function names replaced by `function_1` and so on, GPT-5 scores 0.82 when parameter names remain, 0.00 when only descriptions remain, and 0.95 with full documentation ([OpaqueToolsBench, preprint, Feb 2026](https://arxiv.org/html/2602.15197v1)). Noisy names cut GPT-4 from 80.00 to 58.10 ([RoTBench, EMNLP 2024](https://arxiv.org/abs/2401.08326)), and renaming tools to pretraining-aligned names gave "improvements of up to 17%" ([PA-Tool, ACL 2026](https://arxiv.org/abs/2510.07248)). None of these studies tests a subagent tool, and `subagents_run` is a meaningful name, not noise.

Trained-name gravity is real but unproven for subagent tools. gpt-oss called an undefined `apply_patch` 860 times in one study ([preprint, Apr 2026](https://arxiv.org/abs/2604.00362)), and Qwen3-Coder emitted Claude Code's `TodoWrite` inside opencode (forum). For subagent tools the evidence is thin: opencode issue 9379 shows a model calling `task` after it was disabled, but `task` was that harness's own name, and Codex issue 37113 concerns a wait tool. No case shows a model calling `Task` or `Agent` in place of a differently named offered subagent tool.

Most `Agent` and `Task` aliases in vendor docs serve configuration, not model calls. Codex's hook docs say "`spawn_agent` also matches `Agent`", Copilot's hooks reference maps `task` to "`Agent` (the literal `Task` is also accepted)", and Claude Code keeps `Task(...)` working "in settings and agent definitions" (official docs). A few harnesses do resolve model calls through aliases: Roo Code's `TOOL_ALIASES` ([PR 9989](https://github.com/RooCodeInc/Roo-Code/pull/9989)), Kilo Code's `resolveToolAlias`, and ZCode's inactive `Task` alias tool. Xiaomi's MiMo-Code went the other way: "Tool name resolution is exact-only... Silent case-fold produced unwinnable schema errors" ([vendor design doc, 2026-09-15](https://raw.githubusercontent.com/XiaomiMiMo/MiMo-Code/f98dcd1cf7e70e7eb42f721fdf72bc4a6b87914f/docs/compose/spec/tool-name-case-hint.md)). And under vLLM, "the server's tool parser drops a call to any tool name missing from the request", so an alias never sees the call ([strands-agents issue 4987](https://github.com/strands-agents/harness-sdk/issues/4987), forum, 2026-10-07).

**What I infer.** `subagents_run` passes OpenAI's "semantically correct" test: "subagents" names the thing, and "run" is the verb in Devin's `run_subagent`, VS Code's `runSubagent`, Warp's `run_agents`, and Anthropic's research prompt's `run_blocking_subagent`. It collides with no trained name, so it cannot pull in a foreign schema. Anthropic's framing, and its own use of unrelated names in Managed Agents, suggest that Claude's delegation behavior attaches to a described tool rather than to one string.

**A habitual name costs PromptForge more than most harnesses.** In PromptForge today, a model's call to a tool name the round did not advertise is a hard `OutOfScopeToolCall` error that ends the round; the Engine's tests `model_calling_pure_unknown_tool_is_a_hard_error` and `model_calling_an_offered_but_unscoped_tool_is_a_hard_error` pin it, and the error reaches the author, not the model. The field mostly does the opposite. opencode, OpenHands, and Qwen Code answer the model with an error naming the valid tools, and OpenHands' maintainers say the model "sees the list of correct tools again, and it can correct itself" (forum). Anthropic's own tool reference says: "A disabled member is removed from the tools Claude sees. If Claude still names it, return an error `tool_result`." (official doc). So a single habitual call to `Task` would cost PromptForge a failed round where other harnesses lose one retry. This does not argue for a different name, since no case shows such calls for subagent tools, but it argues for a softer failure, which recommendation 11 takes up.

The shared `subagents_` prefix is not a concern either way. Manus recommends consistent prefixes for tool groups, while one steering study found that tools sharing a first token were harder to steer between, which measures activation steering, not ordinary selection ([preprint](https://arxiv.org/html/2605.07990v2)). The evidence is weak in both directions.

**Judgment.** It is unlikely that the wire name `subagents_run`, by itself, makes a frontier model fail to call the tool or call it wrongly, once its description and parameters follow Claude Code's. Confidence: medium, because no study tests subagent names and the judgment rests on general tool-naming studies, vendor guidance, and the field's diversity. For small open-weight models the name likely matters more, since PA-Tool's gains came on Llama3.1-8B, but the parameters still hold most of the signal.

**Alternatives set aside.** A trained bare name (Option C), hidden aliases (Option D), and per-family dialects (Option E) are set aside for the reasons in the options section. `subagents_spawn` was considered, since "spawn" is OpenAI's, Zed's, and Cline's verb, but no evidence favors either verb, and the owner already rejected `agents/spawn` with the Plugin name. Recommendations 1 and 11 follow.

## Finding 2: The plan's spawn parameters are the trained shape

The plan's four spawn parameters, `description`, `prompt`, `subagent_type`, and `run_in_background`, are the shape most models have seen. Models also pull toward this shape when a tool departs from it.

**What vendors stated.** Claude Code's `AgentInput` type defines `description` as "A short (3-5 word) description of the task", `prompt` as "The task for the agent to perform", `subagent_type` as "The type of specialized agent to use for this task", and an optional `run_in_background` ([SDK type file 0.3.296](https://unpkg.com/@anthropic-ai/claude-agent-sdk@0.3.296/sdk-tools.d.ts), 2026-10-09). Several open-weight vendors say they train inside Claude Code or in harnesses that copy it:

- Moonshot RL-trained Kimi K3 across composed harness configurations that "instantiate mainstream harnesses such as Kimi Code, Claude Code, Codex, OpenClaw, and Hermes", with subagents as one module ([tech report, 2026-07-27](https://arxiv.org/abs/2607.24653)).
- Alibaba generated Qwen3-Coder-Next trajectories in "SWE-agent, Mini-SWE-agent, OpenHands, Claude-Code, Qwen-Code, and Terminus" ([tech report, 2026-02-28](https://arxiv.org/abs/2603.00729)).
- Z.ai says "ZCode has been deeply tuned and specifically optimized around GLM-5.3" (official doc), and ZCode ships Claude Code's `Agent` schema field for field.
- DeepSeek runs V4.1 RL rollouts in DeepSeek Harness, whose `subagent` tool takes `description`, `prompt`, and `run_in_background` and "waits for the result by default" ([vendor doc](https://deepseek-harness.github.io/deepseek-harness/en/reference/tool-catalog), undated developer preview).

**What was observed.** The counts point one way:

- `prompt` names the task text in 12 of 20 closed spawn schemas and 14 open harnesses; `message`, `task`, `query`, `instruction`, and `objective` trail far behind.
- `description` as a short label appears in 9 closed and 10 open harnesses, and the exact phrase "A short (3-5 word) description of the task" in 7 closed and 8 open ones.
- `subagent_type` appears in 8 closed and 8 open harnesses; `agent_type` in 2 closed and 3 open ones.
- All four of the plan's names appear together in Qwen Code, Kimi CLI, and Kode, in Letta Code until 2026-08-31, and in Claude Code, Cursor, ZCode, Qoder, CodeBuddy, Factory, and Grok Build's web `task` tool.

Open-weight models emit this shape in public data. In Z.ai's CC-Bench trajectories, Qwen3-Coder, Kimi-K2, GLM-4.5, and DeepSeek-V3.1 call Claude Code's `Task {description, prompt, ...}` 40 times across 30 trajectories ([dataset, 2025-07-28](https://huggingface.co/datasets/zai-org/CC-Bench-trajectories); counts computed by a research worker, not re-run).

A misfire in Deep Agents shows the pull directly. Its `task` tool took only `description` (as the full instructions) and `subagent_type`. Its issue 6286, opened 2026-09-13 and re-read for this report, says: "For me this is not hypothetical: Sonnet 5 keeps doing it. It leaves a short label in `description` and writes the actual instructions into an extra key, so the subagent is dispatched with the label alone." and "It is not occasional. In the run where I found this, every dispatch looked like that." ([issue 6286](https://github.com/langchain-ai/deepagents/issues/6286)). The fix rejects unknown keys and tells the model to "put all instructions for the subagent in `description`" ([PR 6299](https://github.com/langchain-ai/deepagents/pull/6299), merged 2026-09-22). A frontier model, shown a tool named `task` with Claude Code's selector, rebuilt Claude Code's `{description, prompt}` split.

Models also miss on the type selector. Claude Code 2.1.140 began accepting "case- and separator-insensitive values (e.g. `"Code Reviewer"` resolves to `code-reviewer`)" (official changelog). The plan sends `subagent_type` as an enum of registered names, which constrains the value at the schema, and its failure text for an unknown type names what was wrong.

**Required fields.** The plan requires all three of `description`, `prompt`, and `subagent_type`. Claude Code has required only `description` and `prompt` since 2.1.70, because an omitted type falls back to `general-purpose`. Factory and opencode require all three. PromptForge has no general-purpose type, since every type is an author-registered section, so requiring the selector is correct.

**Blocking versus background by default.** Blocking is the majority where a switch exists, but the trend runs the other way:

- Among 9 closed harnesses with a background flag, 7 block by default (Cursor, Factory, Devin, Copilot CLI, ZCode, Qoder, CodeBuddy) and 2 run in the background (Claude Code since 2.1.198 on 2026-07-01, and Grok Build).
- Among open harnesses with a switch, 4 entries default to the foreground (opencode v1 and v2, Kimi CLI, Kode) and 3 to the background (Qwen Code since 2026-07-18, Kilo Code, pi-subagents).
- Several moved toward always-background in mid-2026: Letta Code on 2026-08-31 and Hermes Agent on 2026-08-27, while Codex has always been asynchronous.

PromptForge has a reason to block by default that the background-first harnesses do not: a text reply ends `models.loop`, and the section's end then stops every running subagent, with the loop-hold option deferred. Blocking by default keeps the common case safe. It also fits the owner's framing, "we need full asynchrony as an option".

**Judgment.** For Claude and for the open-weight families trained in or alongside Claude Code, it is very likely that this parameter set is the one they read most reliably. Confidence: high, because the counts, the vendor-built harnesses, and the Deep Agents misfire agree. GPT models are the exception, since OpenAI's reserved schema uses `message` for the task text (Finding 7).

**Alternatives set aside.** Renaming `prompt` to `message` would match GPT but break the larger population, and an optional `subagent_type` makes sense only with a default type, which PromptForge does not have. Recommendations 2 and 3 follow.

## Finding 3: Background spawns meet an "end your turn" habit that section lifetime punishes

The tool texts models see most often teach them to end their turn after a background spawn and wait to be woken. In PromptForge that reply ends `models.loop`, and the section's end then stops the subagent, so the ack and the background flag's description must teach the opposite rule.

**What was observed.** Six widely used harnesses tell the model, in the ack or the tool text, that ending its turn is fine because a notice will wake it:

- Claude Code's ack: "You will be notified automatically when it completes. You know nothing about its results until that notification arrives - do not report, assume, or predict them; continue other work or respond to the user in the meantime." (shipped bundle 2.1.296, 2026-10-09).
- Cursor's `Task` description: "When an agent runs in the background, you will be automatically notified when it completes after you end your own turn - do NOT AwaitShell, poll, or proactively check on its progress. Continue with other work or end your turn instead." (this session's tool definition, first-hand, 2026-10-10).
- Copilot CLI's ack: "You'll be notified when it completes. Tell the user you're waiting and end your response, or continue unrelated work until notified." (shipped bundle 1.0.95, 2026-10-09).
- opencode's and Qwen Code's acks: "Work on non-overlapping tasks, or briefly tell the user what you launched and end your response." (source at pinned commits).
- Hermes Agent's description: "Background results are delivered only BETWEEN your turns: finish whatever does not depend on them, then give a one-line status and END YOUR TURN." (source at a pinned commit).

A smaller group says the reverse, and these are the precedents PromptForge needs. OpenClaw tells the model to "Wait for completion events for ALL required children before your final answer; never busy-poll." Kilo Code adds "do not give the final answer until all required background results have arrived." Microsoft Agent Framework's background-agents harness says "Important: Always wait for outstanding tasks to finish before you finish processing." Cline's team runtime injects "[SYSTEM] You still have team obligations [...] Do NOT stop until all tasks are completed." when a lead tries to stop early (all source at pinned commits).

**What the plan does.** The background ack is `Task id=N started`, and the plan does not fix the base text of the `subagents_run` description. A text reply ends the loop; the section's end then abandons its live subagents "quietly with the reason 'the section ended'" and discards their queued notices. The loop option that would hold the section open is deferred, and author code can still adopt leftovers through `tasks.pending({ origin = "model" })` when the prompt declares `tasks`. The earlier survey "How Agent Harnesses Let a Model Spawn, Watch, and Stop Subagents" recommended both the loop hold (its Finding 3) and operating rules in the ack (its Finding 5). This finding narrows the second to one sentence the new surface needs.

**What I infer.** A model that starts a background subagent and has nothing else to do will often do what its most familiar harness texts say: reply to the user and stop. That is the right move in Claude Code, Cursor, and Copilot CLI, and the wrong one in PromptForge. The fix is wording that uses the field's own phrase, "end your turn", with the opposite instruction. Keep it short and positive: Antigravity's CLI removed anti-polling text from its tool results because it "could itself nudge the model into a polling loop" (official changelog).

**Judgment.** It is likely that a model which starts a background subagent with nothing else to do will reply without calling `subagents_join`, unless the ack or the tool text tells it not to. Confidence: medium, because the "end your turn" texts are documented in six harnesses, while PromptForge's own rate is unmeasured.

**Evidence for the tracked issue.** The plan opens a GitHub issue for rounds that advertise `run_in_background` without offering `subagents_join`. The owner chose to always show the flag ('User chose "Always show run_in_background; results still reach the model only through tasks/join"'), and this report does not reopen that. The field offers precedent for the issue's discussion: Claude Code removes `run_in_background` from the schema when fork mode is on, opencode hides `background` unless an environment flag is set, and Pydantic AI's harness removes `background` unless it is configured. Recommendation 4 follows.

## Finding 4: Keep `join`, `any`, and the sleep, but name the timeout's unit

The owner's choices for collecting results hold up: no evidence shows that `join`, a boolean `any`, or the sleep confuses models. The one real ambiguity is the parameter `timeout`, whose unit the field splits on.

**The verb.** No surveyed harness, framework, or protocol names a tool "join"; the word appears only in prose, as in Hermes Agent's "join parallel children and return results in this tool call". Wait verbs lead: Codex's `wait_agent`, Grok Build's `wait_tasks`, Muse Code's `subagent_wait`, Warp's `wait_for_events`, Amp's `wait_for_threads`, pi-subagents' `bg_wait`, OpenClaw's `agents_wait`, Microsoft Agent Framework's `background_agents_wait_for_first_completion`, and Anthropic Managed Agents' `wait_for_agents`. Read verbs follow: Copilot CLI's `read_agent`, Devin's `read_subagent`, and the `TaskOutput` family in Factory, ZCode, Qoder, CodeBuddy, Kimi CLI, and Kode. Table 4 in Appendix B lists them all. In the opt-in usage tracker, Codex's `wait_agent` has 54,266 calls, more than Claude Code's `Agent`.

A bare wait verb can collide, on the vendor's own model. In Codex issue 37113, GPT-5.6 Sol, told to call `collaboration.wait_agent` after a spawn, "sometimes emits `functions.wait` instead"; one reporter "observed 133 invalid `wait` calls in about 23 minutes" (forum, opened 2026-08-05). A second reproducer saw the same with the namespace renamed, so the collision is between two visible wait tools, not one namespace.

The owner settled the verb: "Renaming the model's join tool to an `await` name. Reason: the user said they did not want join renamed to await. No revisit." The evidence does not justify reopening it. The notice and the ack name `subagents_join` explicitly, so discovery does not rest on the verb, and a distinct verb avoids the wait collision above. I infer that models know "join" from thread and promise APIs in code, though no data tests it. It is unlikely that `join` instead of `wait` causes a measurable difference in correct calls. Confidence: low, because no study or harness data bears on the verb.

**Any versus all.** No harness has a parameter named `any`, and the field's multi-id default is the opposite of PromptForge's. First-to-finish is the default in Codex V1 ("Pass multiple ids to wait for whichever finishes first"), Codex V2, pi-subagents, OpenClaw's `agents_wait` ("returns once any completes"), and Microsoft Agent Framework, whose tool is named for it. Wait-for-all is an option in pi-subagents (`all: true`), Cline (`team_await_runs` with no run id), OpenClaw's `subagents` wait, and Grok Build's `get_task_output`. Grok Build alone offers an explicit switch, the required enum `mode: "wait_any" | "wait_all"`, on a tool it marks "kept for compatibility".

The owner chose the boolean: "`subagents/join` has `any`, mirroring `tasks.join` versus `tasks.join_any`" ('User: "wait up to N seconds to see if any tasks complete in that time", then "yes add that"'). Waiting for all by default suits PromptForge, because its default join set is every unjoined subagent, so one plain call collects everything. The description just has to say which way the default runs, since a model trained on Codex expects the opposite. Keep it.

**The timeout's unit.** The field splits, and the bare name `timeout` is where it splits worst:

- Counting each harness once, 10 of the wait and read tools surveyed take milliseconds (one of them Cursor's shell wait) and 6 take seconds.
- A bare `timeout` means milliseconds in Claude Code's former `TaskOutput` (0 to 600,000, default 30,000), ZCode's and Kode's `TaskOutput`, and CodeBuddy's. It means seconds in Copilot CLI's `read_agent` ("Wait timeout in seconds (default 30, max 180)"), Devin's `read_subagent` ("Maximum number of seconds to wait when blocking. Defaults to 30, capped at 600"), and Kimi CLI's `TaskOutput` ("Maximum number of seconds to wait when block=true").
- Explicit spellings are common: `timeout_ms` (Codex, Grok Build, Muse Code, DeepSeek Harness), `timeoutMs` (pi-subagents, Mistral Vibe), `block_until_ms` (Cursor), `timeoutSeconds` (OpenClaw, Augment), and `idle_timeout_seconds` (Warp).

Claude models have emitted milliseconds under that exact name. Claude Code shipped `TaskOutput {task_id, block, timeout}` with the timeout in milliseconds from 2.0.64 (2025-12-10) until its deprecation in 2.1.83 (2026-03-24); it was removed in 2.1.277 (official changelog). A public upload of Claude Opus sessions holds 408 calls to it (names normalized to snake_case by the uploader), such as `{"task_id": "b66690d", "block": true, "timeout": 120000}` ([dataset, 2026-03-12](https://huggingface.co/datasets/TeichAI/Claude-Opus-Dataclaw-Unredacted); count computed by a research worker, not re-run).

The plan's `timeout` is in seconds, which matches the owner's words ("wait up to N seconds", "check it every 5 minutes") and the answer `slept N seconds`. A model that sends `timeout: 120000` meaning two minutes would get a join that can wait 33 hours, or a sleep that lasts that long. Two cheap changes close most of the gap. First, spell the unit, `timeout_seconds`. Second, cap the value with a required-versus-actual error such as `timeout_seconds must be between 0 and 3600, got 120000`, a cap that matches Codex's and Kimi CLI's one-hour maxima. The cap turns most millisecond mistakes into an error the model can fix; values under 3,600 meant as milliseconds would still pass.

`timeout_ms` is the credible alternative, because it is the most common explicit spelling and matches Codex's `wait_agent`. It would change the owner's unit, though, and every answer the plan reports in seconds. Either explicit spelling removes the ambiguity, so the report keeps seconds. The parameter's spelling sits inside an owner-approved decision line, quoted in Finding 6; the unit does not change.

It is likely that some models will at least occasionally pass milliseconds to a bare `timeout` meant as seconds. Confidence: medium, because the evidence is four millisecond tools, one dataset, and no PromptForge measurement.

**The sleep.** With nothing to wait on and a timeout, `subagents_join` sleeps. The plan's precedent holds: Cursor's `AwaitShell` "sleeps for the full block_until_ms duration and then returns" when given no shell id (first-hand schema). Cursor also says "NEVER USE THIS TO POLL OR WAIT VACUOUSLY FOR A SUBAGENT LAUNCHED WITH THE Task TOOL", because its subagents push results. PromptForge's join already waits for its subagents, so the sleep is only for outside jobs, as the plan's own note says. The owner chose it ('"sleep N seconds is pretty useful for example if there is a long-running terminal operation the model can check it every 5 minutes", then "yes"'), and nothing in the evidence argues against it. The description should name its purpose plainly rather than warn against polling. Recommendations 5 and 7 follow.

## Finding 5: Pointer-only notices work, but the plan cites the wrong precedent

Pointer-only notices are a minority pattern that ships in production, so the owner's choice is workable. The plan's stated reason for it is wrong, though, and the Decision Record should cite the real precedent.

**What the plan says.** The owner decided: "Completion notices stay, as pointers only. Rationale: the model can't lose finished work, results still have a single delivery path (`subagents_join`), so they can't arrive twice, and this is how Cursor notifies about a background agent." The plan also rejects "Notices carrying the full result. Reason: two delivery paths that must stay identical, and possible double delivery. No revisit."

**What was observed.** Most of the field puts the result in the notice, as Table 6 in Appendix D shows:

- Inline results: 6 of the closed harnesses (Claude Code, Cursor, Codex V2, Devin, ZCode, Grok Build) and 11 open ones (Qwen Code, Kimi CLI with an output tail, Letta Code, opencode, Kilo Code, Hermes Agent, OpenClaw, Codex V1 and V2, Mistral Vibe, Goose). Among frameworks, the Claude Agent SDK, Letta Code, Pydantic AI's harness, Strands, and Mastra push the result too.
- Pointer notices: 3 closed harnesses. Copilot CLI's reads `Agent "X" (type) has completed successfully. Use read_agent with agent_id "X" to retrieve the full results.` (shipped bundle 1.0.10). Kiro's `delegate` adds a short summary and "To read the full details of any task, ask the delegate tool." CodeBuddy's model "pulls the full result with the `TaskOutput` tool", per a translated changelog.

Claude Code tried pointers and moved off them. Version 2.0.70 pushed notices only for remote tasks, ending "Use TaskOutputTool with task_id=... to retrieve the output". Version 2.0.77 said "Read the output file to retrieve the result". Version 2.1.7 "Added inline display of agent's final response in task notifications" (shipped bundles and official changelog, 2025-12 to 2026-01-13).

**Cursor inlines.** Cursor's background notice is a `<system_notification>` whose `detail` field holds the subagent's full final message, followed by an instruction not to reiterate it. The earlier survey observed this first-hand on 2026-10-10, and exported transcripts from April and May 2026 show the same format (third-party capture). The precedent for the plan's pointer is Copilot CLI, not Cursor.

**The double-delivery concern is real, and both designs solve it.** The earlier survey records Codex V1 delivering each result twice (its issue 24225). Copilot CLI fixed the overlap from the other side: "Background agent completion notifications are not sent redundantly when read_agent is already waiting for the result" (official changelog 1.0.28). Grok Build warns that "consuming a task's output suppresses its completion notification". So inline notices need a consume-once rule, and the pointer design gets one for free.

**What I infer.** Copilot CLI runs pointer notices across "20+ frontier models across the GPT, Claude, Gemini, and MAI families" ([official blog, 2026-06-25](https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/)), and Microsoft trained MAI-Code-1-Flash "directly with GitHub Copilot harnesses used in production" (vendor blog). The pattern therefore works on the model families PromptForge targets. Its cost is one extra tool call and one extra round per background subagent. Its risk is the Finding 3 habit: a model trained on inline notices expects the result in hand, and may answer the user from the pointer line alone. The plan's notice names the tool to call, which is the right counter.

**Judgment.** It is likely that models follow a pointer notice that names the collecting tool. Confidence: medium, because Copilot CLI ships the pattern at scale but publishes no rate of skipped reads. Inline notices remain the alternative if PromptForge's own event log shows skipped joins, and choosing them would reopen the owner's decision quoted above.

**Labeling.** The earlier survey's Finding 4, a label saying a notice is engine text rather than the user's words, still applies to the one-line notice. Claude Code and ZCode open notices with "[SYSTEM NOTIFICATION - NOT USER INPUT]", while Cursor and Copilot CLI wrap them in `<system_notification>` and explain the tag in the system prompt. A pointer line holds no result, so the risk is smaller than for inline notices, but it is not zero. Recommendation 8 follows.

## Finding 6: Keep "cancel", and call the id `task_id`

The cancel tool and its verb should stay as planned. The id parameters should be spelled `task_id` and `task_ids`, the field's majority spelling and an echo of the `Task id=N` text the model reads.

**Cancel.** Half the field offers no model-facing cancel, and the rest uses three verbs. Table 5 in Appendix C lists them:

- No cancel: 8 of 20 closed schemas (Cursor, Copilot CLI, Devin, Amp, Kiro's two tools, Augment, Kimi Agent Swarm) and 14 open harnesses.
- "Stop": Claude Code's `TaskStop {task_id}`, shared by Factory, ZCode, Qoder, CodeBuddy, Kimi CLI, Kode, and Letta Code, plus Qwen Code's `task_stop`.
- "Cancel": Muse Code's `subagent_cancel`, Deep Agents' `cancel_async_task`, Cline's `team_cancel_run`, OpenClaw's `cancel` action, and Strands' `cancel` mode, plus both protocols, A2A's `CancelTask` (formerly `tasks/cancel`) and MCP's `tasks/cancel`.
- "Kill": Grok Build's `kill_task`, Antigravity's `kill` action, and DeepSeek Harness's `job_kill`. Codex separates `interrupt_agent`, which keeps the child, from V1's `close_agent`.

The trained name `TaskStop` cannot come out of PromptForge's rule, and no evidence favors "stop" over "cancel". "Cancel" is the protocol verb and the verb of PromptForge's own author API, `tasks.cancel`. The owner chose run, join, and cancel, rejecting "A separate status tool, or a join without cancel". Keep `subagents_cancel`. Confidence: medium, because the field is split and no study compares the verbs.

**Ids.** The plan uses `ids` on join and `id` on cancel, and acks with `Task id=N`, keeping that wording as a planning default ("model-facing ids keep the `Task id=N` wording"). The field mostly spells the id `task_id`:

- `task_id` is the most common id parameter across spawn, resume, message, wait, and cancel tools in open harnesses, at 7 (opencode v1, Kilo Code, Qwen Code, Kimi CLI, Kode, Letta Code, Deep Agents).
- It is also the parameter of the closed `TaskStop` and `TaskOutput` family, and Grok Build uses `task_id` and `task_ids`.
- Other spellings follow the ack text: Copilot CLI and Devin ack with `agent_id` and take `agent_id`; DeepSeek Harness uses `job_id`; Codex uses `target` and `targets`. A bare `id` appears only in pi-subagents and Codex V1's `resume_agent`.

Anthropic's tool-writing advice points the same way: "input parameters should be unambiguously named: instead of a parameter named `user`, try a parameter named `user_id`." Deep Agents describes its id as "The exact task_id string returned by start_async_task. Pass it verbatim." PromptForge's ids look like `0.3`. I infer that a loosely typed schema could let a model send that as the number 0.3, so the parameter should be a string described as copied from the `Task id=` text.

Calling the background unit a "task" while the tools say "subagents" is in distribution. Claude Code's tool is `Agent`, yet its notices include `<task-id>` and its cancel is `TaskStop {task_id}`; Qwen Code's tool is `agent`, and its ack says `task_id:`.

**The owner decision this touches.** The owner approved this decision line: "The model gets full asynchrony: `subagents/run` with optional `run_in_background`, `subagents/join { ids?, timeout?, any? }`, and `subagents/cancel { id }`, with no separate status tool because a join with `timeout: 0` covers it." His quoted words chose the tools and the asynchrony ("we need full asynchrony as an option"), not the parameter spellings. Renaming `id`, `ids`, and `timeout` edits the spelling inside an approved line, so the owner should confirm it.

**Judgment.** It is unlikely that `id` causes failures by itself; `task_id` removes a small ambiguity at no cost. Confidence: medium, because it is the majority spelling and matches the ack, but no failure with `id` is on record. Recommendations 6 and 9 follow.

## Finding 7: One surface serves Claude and the open-weight families best, GPT least

A single surface in Claude Code's shape matches what Claude, Kimi, Qwen, GLM, and DeepSeek models have seen. It cannot also match what GPT-5.6 and later were trained on, and the Gemini evidence is too thin to call. Table 2 summarizes each family.

*Table 2. What each model family has seen for delegation, and how the plan's surface lines up. "Stated" means a vendor said so; "observed" means it was read in the vendor's own harness; training on a harness's tools is inferred unless marked stated.*

| Family | Spawn shape seen | Collect and notice habit | What the plan matches | What it cannot match |
|---|---|---|---|---|
| Claude (Anthropic) | Claude Code `Agent`, formerly `Task`: `description`, `prompt`, `subagent_type`, `run_in_background`, background by default since 2026-07-01 (observed; "orchestrate subagents natively" stated) | No wait tool today; `TaskOutput {task_id, block, timeout}` in milliseconds until 2026-09; inline `<task-notification>` behind "NOT USER INPUT" | All four parameters and their phrases | The name `Agent`; the push-only "end your turn" habit; milliseconds under `timeout` |
| OpenAI GPT-5.6 and later | `collaboration.spawn_agent {task_name, message, fork_turns}`, reserved by the API per model; always asynchronous (observed) | `wait_agent {timeout_ms}` waits for any mailbox update; `FINAL_ANSWER` envelope with the payload | Spawn, wait, and interrupt semantics; an explicit timeout unit | The name, `message`, `task_name`, always-async, any-first waiting |
| Gemini (Google) | No trained delegation tool stated. Gemini CLI `invoke_agent {agent_name, prompt}`, blocking; Antigravity `invoke_subagent` with PascalCase arrays, "co-optimized" with Gemini 3.5 Flash (stated) | Antigravity resumes the model when a message arrives; Gemini CLI blocks | `prompt`; a flat schema without `anyOf` | `agent_name`; Antigravity's array form |
| Kimi (Moonshot) | K2.5 `assign_task {agent, prompt}` (stated, evaluation appendix); K3 RL across Claude Code, Codex, Kimi Code, OpenClaw, Hermes (stated); Kimi CLI `Agent` with Claude Code's parameters, blocking by default | `TaskOutput {task_id, block, timeout}` in seconds; `<task-notification>` with an output tail | Nearly everything, seconds included | The name |
| Qwen (Alibaba) | Qwen3-Coder-Next trajectories from Claude Code and Qwen Code (stated); Qwen Code `agent` with Claude Code's parameters, background by default since 2026-07-18 | Push only; `<task-notification>` with the result; `task_stop {task_id}` | All four parameters | The name; the background default |
| GLM (Z.ai) | ZCode "deeply tuned and specifically optimized around GLM-5.3" (stated), with Claude Code's `Agent` schema | `TaskOutput` in milliseconds, deprecated; `TaskStop`; "NOT USER INPUT" notices | All four parameters | The name; milliseconds under `timeout` |
| DeepSeek | V4.1 RL rollouts run in DeepSeek Harness (stated): `subagent {description, prompt, run_in_background}`, blocking by default | `job_output {job_id, wait, timeout_ms}`, `job_kill`; injected notices whose content is unverified | Three parameters, the blocking default, a blocking collect call | `job_*` names; milliseconds |
| gpt-oss (OpenAI open weights) | Trained on the harmony format and `browser` and `python` tools only (stated); no delegation tool | None | Nothing to conflict with | Small-model name sensitivity; vLLM drops calls to undeclared names |

**What the table shows.** Claude Code's parameter set is the common ground: Anthropic ships it, Moonshot, Alibaba, and Z.ai copied it into their own harnesses, and DeepSeek's harness shares three of its four names. OpenAI's shape differs in every name and in its always-asynchronous semantics, so a GPT model meets PromptForge's surface as a described custom tool, the case OpenAI's guidance covers with "semantically correct" names. Gemini's evidence is a harness shape, not a training statement; the one hard lesson is Gemini CLI's, that an `anyOf` schema broke Gemini 3 Pro's calls, and PromptForge's flat schema avoids it.

**Delegation appetite differs by family, and it is stated.** Codex "only spawns subagents when you explicitly ask it to" (official doc), and its tool text says "Only use `spawn_agent` if and only if the user explicitly asks for sub-agents, delegation, or parallel agent work". OpenAI publishes a tuning sentence for GPT-6 Astra beginning "If at any point you can parallelize work by delegating tasks to another agent" (official doc). Anthropic warns that "Claude Opus 5 delegates to subagents more readily than prior models" and suggests "explicit guidance" or "deterministic caps" (official doc). A study of an untrained base model found it "never invokes" a described delegation tool, concluding that delegation "requires explicit training" ([SearchSwarm, preprint, June 2026](https://arxiv.org/abs/2606.09730)). These differences belong in author guidance, because the author writes the prompt that frames the tool.

**What one surface cannot satisfy.** No single name serves both Claude (`Agent`) and GPT (`spawn_agent`), and no single task-text parameter serves both (`prompt` versus `message`). A per-family dialect could, at the cost Option E describes. A trained name must also come with its trained schema: Deep Agents shows a model rebuilding the schema it associates with a familiar name. A `spawn_agent` that takes `prompt` would invite GPT models to send `message` and `task_name`. Alibaba's finding that "Models trained on trajectories from one scaffold do not transfer strongly to others" cuts both ways: it argues for matching one well-known shape exactly rather than mixing several.

**Judgment.** For Claude, Kimi, Qwen, GLM, and DeepSeek models, it is very likely that the plan's surface reads as familiar once its descriptions use Claude Code's phrases. Confidence: medium, because the training of each family on Claude Code's tools is stated only for Kimi K3 and Qwen3-Coder-Next and inferred for the rest. For GPT-5.6 and later, it is roughly even chance that the models use `subagents_run` proactively without an author's delegation instruction. Confidence: low, because the evidence is vendor prompt text, not a test. Recommendation 10 follows.

## Finding 8: The old task tools had an in-distribution name and out-of-distribution parameters

The evidence supports replacing `task`, `task_cancel`, `task_status`, and `await_tasks` with the planned surface. The new surface trades a familiar name for familiar parameters, which is the better trade on the evidence of Findings 1 and 2.

- **`task`.** The bare name was in distribution: Copilot CLI, Grok Build, opencode v1, Deep Agents, OpenHands, Kilo Code, and Mistral Vibe's legacy harness all spawn with `task`. Its parameter was not. The earlier survey's reconstruction shows the model calling `task {"target": "## Research"}` with a section heading the model cannot know, a shape no harness uses.
- **`task_status`.** The field retreated from status tools: opencode's `task_status` lasted 11 days and Claude Code's `TaskOutput` was removed, as the earlier survey's Table 4 records. Folding status into `subagents_join` with `timeout: 0` matches Copilot CLI's `read_agent` with `wait: false`, Kimi CLI's non-blocking `TaskOutput`, and OpenClaw's "Use 0 for a snapshot". The owner flagged the risk: "Revisit if models struggle to discover the status use", so the join description should name that use.
- **`await_tasks`.** "Await" survives in Cline's `team_await_runs` and Cursor's `AwaitShell`; the replacement uses a distinct verb (Finding 4).
- **Bare names and `tools.allow_tasks`.** In every surveyed harness the subagent tool is an ordinary entry in the tool list. Harnesses that avoid name clashes do it with namespaces (Codex's `collaboration`, Muse's `muse.`) or prefixes (Microsoft Agent Framework's `background_agents_*`). OpenAI also tells gpt-oss users to wrap functions in a namespace "to not conflict with other tools that the model might have been trained on" (official doc). Moving to `<plugin>_<tool>` names behind `tools.offer` fits that practice.

One caution remains. opencode issue 9379 shows a model calling `task` after the tool was disabled, probably from history or prompt text. PromptForge's prompts are at language version 0 and the break is clean, so only prompt text that still names the old tools would invite such calls.

## Eleven recommendations, each with an owner, a next step, and a confidence

The owner of every recommendation is the PromptForge owner, who decides most of them through a revision of the plan's Part 4 before that part starts; the Part 4 implementer then changes the strings and the tests that pin them. Recommendations 1, 3, 7, and 9 confirm the plan as written. Recommendations 2 and 4 fill text the plan leaves open. Recommendations 5 and 6 rename parameters inside an owner-approved decision line, and recommendation 8 corrects a rationale. Recommendation 10 is author guidance, and recommendation 11 is an Engine change outside this plan.

1. **Keep `subagents_run`, `subagents_join`, and `subagents_cancel`; add no aliases and no bare-name exception (Finding 1).** This reopens nothing; it keeps 'User chose "subagents, with tools subagents/run, subagents/join, subagents/cancel"'. Next step: record in the Decision Record that this survey checked the names and found no trained name the id rule can produce. Confidence: medium, because no study tests subagent names, but every measured signal favors parameters and descriptions.
2. **Write the `subagents_run` description and parameter descriptions in Claude Code's phrases (Findings 1 and 2).** The plan builds this text in `finish_subagents_run_schema` but does not fix its base wording; the proposed strings below fill it. Next step: put the strings in the plan's Technical Design for `subagents-schemas.rs`, and pin them in the Part 4 tests. Confidence: high, because the phrases recur verbatim across more than 15 harnesses and cost only text.
3. **Keep the four spawn parameters, `subagent_type` required as an enum, and blocking by default (Finding 2).** Make the unknown-type failure list the valid types, as Deep Agents' does ("the only allowed types are ..."). Next step: none beyond that error text. Confidence: high, because this is the converged shape in the vendor-built harnesses, and the Deep Agents misfire shows models pulling toward it.
4. **Tell the model to join before it ends its turn, in the background ack and the `run_in_background` description (Finding 3).** Extend the ack after the `Task id=N` prefix, which keeps the planning default intact. Next step: adopt the ack and flag text below, update the tests that pin `Task id=N started`, and add the field precedent from Finding 3 to the GitHub issue the plan opens. Confidence: medium, because the "end your turn" habit is documented in six harnesses but its rate in PromptForge is unmeasured.
5. **Rename `timeout` to `timeout_seconds`, keep seconds, and cap it at 3,600 with a required-versus-actual error (Finding 4).** The error reads `subagents_join: timeout_seconds must be between 0 and 3600, got 120000`. This edits the spelling inside the owner-approved line quoted in Finding 6, so the owner confirms it. Next step: change the schema, the answers' wording if they echo the name, and the tests. Confidence: medium, because the field splits on the unit of a bare `timeout` and Claude models have sent milliseconds under that name.
6. **Rename `id` and `ids` to `task_id` and `task_ids`, typed as strings passed verbatim (Finding 6).** This edits the same approved line, so the owner confirms it; the `Task id=N` wording stays. Next step: change the schemas, the failure texts that name the parameter, and the tests. Confidence: medium, because it is the majority spelling and matches the ack, though no failure with `id` is recorded.
7. **Keep `join`, the `any` boolean, the wait-for-all default, and the sleep, and describe them plainly (Finding 4).** These are owner decisions, quoted in Finding 4, and the evidence does not argue for reopening them. Next step: adopt the join description below, which names the default, the status use with a zero timeout, and the sleep's purpose. Confidence: medium, because no evidence shows `join` or `any` hurts, but none tests them either.
8. **Keep pointer-only notices, and correct the Decision Record's reason (Finding 5).** Replace "this is how Cursor notifies about a background agent" with a sentence citing GitHub Copilot CLI, and note that Cursor and most of the field put the result in the notice. Next step: edit the Decision Record, and plan to count, from the event log, notices that no `subagents_join` followed before the loop ended. Confidence: medium, because Copilot CLI ships the pattern across more than 20 models, while most harnesses inline results.
9. **Keep `subagents_cancel` under the verb cancel (Finding 6).** Next step: adopt the description below. Confidence: medium, because half the field has no cancel, the rest splits between stop, cancel, and kill, and cancel matches the protocols and `tasks.cancel`.
10. **Ship one surface for every model family, and add delegation guidance to the author docs (Finding 7).** In Part 5's language-spec entry for `subagents`, note that GPT-family models delegate conservatively unless the prompt invites it, with OpenAI's published sentence as a model. Also note that Claude Opus 5 delegates readily, and that the chain's concurrency limit is the cap. Next step: one paragraph in the Part 5 docs; no per-family dialect. Confidence: low, because the guidance is inferred from vendor prompt text and is untested in PromptForge.
11. **Outside Part 4, answer a model's call to an unoffered tool name with a failed tool result that lists the in-scope wire names, instead of ending the round (Finding 1).** Today such a call is a hard `OutOfScopeToolCall` error. Anthropic's tool reference tells harnesses to "return an error `tool_result`" when Claude names a tool that was removed from its list, and opencode, OpenHands, and Qwen Code already answer unknown names this way. Exact wire-name lookup stays; only the failure changes. This is existing Engine behavior, not a decision in this plan, and it affects every tool, so it belongs in its own plan. Next step: the owner decides whether to open that plan or an issue. Confidence: medium, because vendor advice and field practice agree, but no PromptForge run has yet failed this way with a subagent tool.

**Proposed strings.** These fill the gaps the plan leaves and apply recommendations 2, 4, 5, 6, 7, and 9. The notice stays as the plan wrote it. The agent-type list is the plan's own.

```text
subagents_run
  tool description:
    Launch a new agent to handle a complex, multi-step task autonomously. The agent starts with a fresh context and sees only your prompt, so include everything it needs and say exactly what it should return. Only its final message comes back to you. Several subagents_run calls in one turn run at the same time.
    By default the call waits for the agent's result. With run_in_background: true it returns at once with a task id; call subagents_join to collect the result before you end your turn, because a subagent still running when your turn ends is stopped.
    Available agent types:
    - researcher: Finds and summarizes sources on a topic
  description:        A short (3-5 word) description of the task
  prompt:             The task for the agent to perform. Include all the context it needs; it cannot see this conversation.
  subagent_type:      The type of specialized agent to use for this task
  run_in_background:  Run the agent in the background and return a task id at once. Defaults to false, which waits for the result. Use true only for independent work you can do something else beside, and call subagents_join before you end your turn.

background ack:
  Task id=0.3 started in the background. Call subagents_join to collect its result before you end your turn; a subagent still running when your turn ends is stopped.

subagents_join
  tool description:
    Collect results from subagents you started in the background. With no task_ids it collects every one you have not collected yet, and finished ones come back at once. It waits until all of them finish, until the first finishes with any: true, or until timeout_seconds pass; timeout_seconds: 0 checks status without waiting. With task_ids: [] and timeout_seconds it only sleeps, for checking on a slow outside job.
  task_ids:         Task ids from "Task id=..." lines, as strings, passed verbatim (for example "0.3"). Omit to collect every subagent you have not collected.
  timeout_seconds:  Longest wait in seconds, from 0 to 3600. Omit to wait until done; 0 checks without waiting.
  any:              true returns as soon as one finishes; false or omitted waits for all of them.

subagents_cancel
  tool description:  Stop a subagent you started. Pass the task_id from its "Task id=..." line.
  task_id:           The task id from a "Task id=..." line, as a string, for example "0.3".

completion notice (unchanged):
  Task id=0.3 (researcher) finished. Call subagents_join to collect its result.
```

"A subagent still running when your turn ends is stopped" is true unless author code adopts it with `tasks.pending({ origin = "model" })` before the section ends, an exception the model has no use for.

## Six kinds of evidence would change these judgments

Each judgment above would move on specific evidence, most of which PromptForge can collect itself once Part 4 lands.

- **A naming test in PromptForge.** Run the same prompts with the spawn tool advertised as `subagents_run` and as `Agent`, on Claude, GPT, Qwen, and Kimi models. A clear gain for `Agent` on call validity or delegation rate would reopen recommendation 1, and with it the owner's naming decision, through Option C or E.
- **Calls to foreign names.** Rounds that fail with `OutOfScopeToolCall` naming `Task`, `Agent`, `task`, or `spawn_agent` would show trained-name gravity that this report found no case of. Any such failure makes recommendation 11 urgent; aliases would still sit badly with wire-name-only lookup.
- **Skipped joins.** Notices that no `subagents_join` followed before the loop ended, or background spawns abandoned at the section's end, would show the Finding 3 habit or a pointer-notice failure. Either would argue for the deferred loop hold, and a high rate would argue for inline notices, reopening the owner's notice decision.
- **Frequent cap errors.** Many `timeout_seconds` refusals would show models sending milliseconds even under the explicit name, and would argue for `timeout_ms`.
- **A vendor statement.** An Anthropic or OpenAI statement naming the subagent tool its models were trained on would replace the inferences in Findings 1 and 7.
- **GPT under-delegation.** GPT-family runs that never call `subagents_run` without an explicit instruction would confirm recommendation 10's guidance and might justify a default instruction in the tool text.

## The new notes correct the earlier survey in four places and disagree with each other in four

**Corrections to "How Agent Harnesses Let a Model Spawn, Watch, and Stop Subagents".** The earlier survey's behavioral conclusions stand. Re-reading the open harnesses at newer commits changes these details:

- **Goose's `peek` was a parameter, not a tool.** It was a boolean on `load`, beside a `cancel` boolean, and `async` was a boolean on `delegate`. All three were removed on 2026-10-07 with a hidden `orchestrator__*` tool family. The survey's lesson, that a bare idle figure made a model kill working children, is unaffected.
- **opencode's development branch replaced `task` on 2026-10-10.** On `dev`, the spawn tool is now `subagent {agent, description, prompt, model?, sessionID?, background?}`, a separate rewrite. Release v1.18.35 still ships `task`, and its `background` parameter is hidden from the model unless `OPENCODE_EXPERIMENTAL_BACKGROUND_SUBAGENTS` is set, so "background opt-in" holds in releases only with that flag.
- **Codex's tools live in Responses API namespaces.** V1's sit in `multi_agent_v1` and V2's in `collaboration`, and the model is told to call `to=functions.collaboration.spawn_agent`. V2's `close_agent` was renamed `interrupt_agent` on 2026-06-08, and `followup_task` was briefly `assign_task` from 2026-05-30 to 2026-06-01. The survey also did not record that OpenAI's API reserves `collaboration.spawn_agent` for GPT-5.6 models.
- **Gemini CLI's tool changed shape four times.** It went from one tool per agent (2025-10) to `delegate_to_agent` (2025-12), back to one tool per agent (2026-01, after `MALFORMED_FUNCTION_CALL` errors on Gemini 3 Pro), and then to `invoke_agent` (2026-04).
One claim is confirmed rather than corrected: Codex V2's `wait_agent` still returns no content at the newer commit. Its answer is "Wait completed.", "Wait interrupted by new input.", or "Wait timed out.", with no agent list despite the description.

Four harnesses the survey did not cover bear on naming. Qwen Code renamed `task` to `agent` and made background the default. Kimi CLI, archived on 2026-09-21, ended with `Agent` plus `TaskList`, `TaskOutput`, and `TaskStop`, and its successor keeps `Agent`. OpenClaw has a core tool literally named `subagents`, with `action: list | wait | cancel`. Letta Code shows its internal `Task` tool as `Agent` and removed `TaskOutput` on 2026-09-22. VS Code's `runSubagent` now lives in the core VS Code repository.

**Where the four notes disagree, with each flag kept.**

- **Blocking defaults.** The training note's table of vendor-built harnesses lists Claude Code and Qwen Code as blocking by default. Both are wrong today: Claude Code's docs, re-read for this report, say it "runs the subagent in the background by default", and Qwen Code's schema at the pinned commit has `run_in_background` with `default: true`. The training note read Qwen Code at a 2026-06-28 commit, before the change. Kimi CLI and DeepSeek Harness do block by default.
- **Seconds under a bare `timeout`.** The training note says no wait-style tool it checked takes seconds under a plain `timeout`, and that Kimi CLI's units are unverified. The closed note shows Copilot CLI's `read_agent` and Devin's `read_subagent` taking seconds under `timeout`, and the open note reads Kimi CLI's `TaskOutput` and `Agent` timeouts as seconds in source. This report follows the closed and open notes.
- **Anthropic Managed Agents' tool names.** The cookbook names four delegation tools (`create_agent`, `send_to_agent`, `wait_for_agents`, `list_agents`); Anthropic's skill file names two (`list_agents`, `send_to_agent`). The difference is unresolved.
- **DeepSeek Harness notices.** The training note counts them as a match for PromptForge's pointer notices. The vendor doc says completion notices are injected and results are collected with `job_output`, but whether a notice includes the result was not verified.
One clarification belongs beside these. The `Agent` and `Task` aliases often cited for Codex and Copilot CLI are hook matchers and agent-configuration aliases, not model-call aliases. Model-call aliasing is documented only for Roo Code, Kilo Code, and ZCode's inactive alias tool. Claude Code's tool definition lists `Task` as an alias, but its docs confirm only settings and agent definitions.

**Facts still unverified.** Cursor's GPT-family `functions.Subagent` tool is known only from model-reported names, so its parameters are unknown. Copilot CLI 1.0.95 assembles its `task` schema at runtime, and the required list was not recovered. Copilot's cloud agent is inferred to share the CLI's `task` tool. Amp builds its current `Task` schema on its server. The Kimi K2.5 appendix schemas may differ from the training interfaces. OpenAI never states that GPT-5.6 was trained on `collaboration.spawn_agent`; the API's reservation implies it. Dataset counts marked as worker-computed were not re-run.

## Method and limitations

**Inputs.** Four research notes, each produced on 2026-10-10 by research workers running as Cursor subagents on Claude Opus 5.5, supply the evidence:

- "Closed-source harnesses: model-facing subagent tool names, schemas, and behavior" covers 26 closed harnesses from official docs, shipped npm bundles unpacked by version, this session's own tool definitions, and extracted-prompt repositories at pinned commits. Its coordinator re-fetched seven load-bearing primary pages.
- "Open-source coding harnesses: model-facing subagent, delegation, and background-task tools" covers about 30 harnesses read at pinned commits; 25 load-bearing names and strings were re-read from the raw files, and all matched.
- "Naming survey slice: agent frameworks and SDKs that expose delegation to a model as a tool" covers 17 frameworks plus the A2A and MCP protocols at pinned commits.
- "Training-data alignment for subagent tools" covers vendor training statements, open-weight harness targeting, Hugging Face datasets queried directly, real-usage counts, and naming-sensitivity studies.

The report also draws on Part 4 of the plan "Plugin registry, parallel tool calls, and the tasks and subagents Plugins" (its Functional Specification, Technical Design, and Decision Record), on the earlier survey, and on the plan "Author API debt removal" for the wire-name-only change.

**Checks made for this report.** Where the notes disagreed or a recommendation hinged on a fact, I re-read the source on 2026-10-10. Claude Code's docs confirm the `Task` to `Agent` rename and the background default. Qwen Code's source at commit `9763580` confirms `run_in_background` defaults to true. The text of Deep Agents issue 6286 and Codex issue 31864 matches the notes. All four checks agreed with the closed and open notes; the training note's blocking-default entries did not. I also read PromptForge's Engine tests, which pin a model's call to an unoffered tool name as a hard `OutOfScopeToolCall` error.

**Limits.** No model was run, and no experiment anywhere tests subagent tool names, so the judgment on names is an inference from general studies and vendor guidance. Harness counts measure products, not how often a model saw a name in training, and closed-lab training data is invisible. Several closed schemas come from extracted prompts or third-party captures, labeled as such where cited. The usage tracker is an opt-in cohort. Harness code moves fast: opencode changed its spawn tool on the day the notes were written, and Goose removed its background mode three days earlier, so every statement holds as of its pinned commit or fetch date. Inside quotations, em dashes are rendered as " - " to follow this repository's style, and emoji are dropped.

## Appendix A: Spawn tools

*Table 3. The model-facing spawn tool in each surveyed harness and framework, with the parameter that holds the task text, the short label, the agent-type selector, and the background switch with its default. "?" marks an optional parameter. Closed harnesses come first, then open harnesses, then frameworks and vendor harnesses, then PromptForge's plan. Evidence classes and dates are in the per-harness sources listed under Sources.*

| Harness | Spawn tool | Task text | Label | Type selector | Background switch (default) |
|---|---|---|---|---|---|
| Claude Code and Agent SDK | `Agent` (alias `Task`; `Task` until 2.1.63) | `prompt` | `description` | `subagent_type?` | `run_in_background` (true since 2.1.198) |
| Cursor | `Task` (GPT dialect `Subagent`, parameters unverified) | `prompt` | `description` | `subagent_type` | `run_in_background` (false) |
| OpenAI Codex V1 | `spawn_agent` in `multi_agent_v1` | `message` or `items` | none | `agent_type?` | none; always async |
| OpenAI Codex V2, Responses API, ChatGPT Work | `spawn_agent` in `collaboration` | `message` | `task_name` | `agent_type?` (only with roles) | none; always async |
| GitHub Copilot CLI | `task` | `prompt` | `description`, `name` | `agent_type` | `mode: "sync" \| "background"` ("sync" in 1.0.95) |
| Amp | `Task` | `prompt` | `description` | none | none; blocking |
| Devin CLI and Devin Local | `run_subagent` | `task` | `title` | `profile` | `is_background` (false) |
| Kiro CLI Classic | `use_subagent` | `content.subagents[].query` | none | `agent_name?` | none; `delegate` is the async tool |
| Kiro agent service | `invoke_sub_agent` | `prompt` | `explanation` | `name` | none; blocking |
| Augment (Auggie) | `sub-agent`, `sub-agent-<name>` | `instruction` | `name` | tool-name suffix | none; separate async tool |
| Warp | `run_agents` | `prompt` per agent | `title` per agent | `name` per agent | none; always async |
| Factory Droid | `Task` | `prompt` | `description` | `subagent_type` (required) | `run_in_background` (false) |
| Google Antigravity | `invoke_subagent` | `Subagents[].Prompt` | none | `TypeName`, `Role` | none; always async |
| xAI Grok Build | `task` (accepts `Task`, `spawn_subagent`) | `prompt` | `description` | `subagent_type` | `run_in_background` (true) |
| Meta Muse Code | `muse.subagent_spawn` | `objective` | `task_name?` | `subagent_type?`, `role` | none; always async |
| Z.ai ZCode | `Agent` (alias `Task`) | `prompt` | `description` | `subagent_type?` | `run_in_background` (false, implied) |
| Qoder CLI | `Agent` | `prompt` | `description` | `subagent_type?` | `run_in_background` (false, implied) |
| Tencent CodeBuddy Code | `Agent` | `prompt` | `description?` | `subagent_type?` | `run_in_background` (false, implied) |
| Kimi Agent Swarm (K2.5 report) | `assign_task` (with `create_subagent`) | `prompt` | none | `agent` | none; blocking |
| VS Code Copilot Chat | `runSubagent` | `prompt` | `description` | `agentName?` | none; blocking |
| Gemini CLI | `invoke_agent` | `prompt` | none | `agent_name` | none; blocking |
| opencode v1 (releases) | `task` | `prompt` | `description` | `subagent_type` | `background?`, hidden unless an env flag (false) |
| opencode v2 (dev branch) | `subagent` | `prompt` | `description` | `agent` | `background?` (false) |
| Kilo Code | `task` | `prompt` | `description` | `subagent_type` | `background?` (background-first) |
| Charm Crush | `agent` | `prompt` | none | none | none; blocking |
| Cline SDK | `spawn_agent`; `subagent_<name>` | `task`; `prompt` | none | `systemPrompt` (custom) | none; blocking (team runs have `runMode`) |
| Roo Code (archived) | `new_task` | `message` | none | `mode` | none; serial |
| Continue CLI (beta) | `Subagent` | `prompt` | `description` | `subagent_name` | none; blocking |
| Qwen Code | `agent` (was `task`) | `prompt` | `description` | `subagent_type?` | `run_in_background` (true since 2026-07-18) |
| Kimi CLI (archived) | `Agent` (was `task`, `Task`) | `prompt` | `description` | `subagent_type?` (default `coder`) | `run_in_background` (false) |
| OpenHands | `task` | `prompt` | `description?` | `subagent_type?` | none; blocking |
| Goose | `delegate` | `instructions?` | none | `source?` | none since 2026-10-07 |
| Zed | `spawn_agent` (was `subagent`) | `message` | `label` | none | none; blocking |
| Deep Agents | `task`; `start_async_task` | `description` (full text) | none | `subagent_type` | separate async tool |
| OpenClaw | `sessions_spawn` | `task` | `label?` | `agentId?` | none; always async |
| Hermes Agent | `delegate_task` | `tasks[].goal` | none | none | none; always async at top level |
| Mistral Vibe (legacy harness) | `task` | `task` | none | `agent?` | none; blocking |
| Letta Code | `Agent` (internal `Task`) | `prompt` | `description` | `subagent_type` | none; always async since 2026-08-31 |
| Kode | `Task` | `prompt` | `description` | `subagent_type` | `run_in_background?` |
| pi-subagents | `subagent` | `task` | none | `agent` | `async` (true) |
| DeepSeek Harness | `subagent` (renameable) | `prompt` | `description` | none | `run_in_background` (false) |
| Microsoft Agent Framework background agents | `background_agents_start_task` | `input` | `description` | `agent_name` | none; always async |
| Pydantic AI Harness | `delegate_task` | `task` | none | `agent_name` | `background` (false) |
| Strands harness | `subagent` | `task` | none | `agent_type?` | none; always async |
| OpenAI Agents SDK `as_tool` | the agent's name | `input` | none | one tool per agent | none |
| PromptForge plan | `subagents_run` | `prompt` | `description` | `subagent_type` (required enum) | `run_in_background` (false) |

## Appendix B: Wait, read, and join tools

*Table 4. The tool a parent model calls to wait for or read a background child, with its id parameter, whether it waits for any or all of several children, its timeout parameter's name and unit, and its blocking switch. Defaults are in parentheses. Harnesses that only push results and offer no such tool (Claude Code today, opencode, Kilo Code, Qwen Code, Letta Code, Hermes Agent) are left out.*

| Harness | Tool | Id parameter | Any or all | Timeout (unit, default, limit) | Blocking switch |
|---|---|---|---|---|---|
| Claude Code (removed in 2.1.277) | `TaskOutput` | `task_id` | one child | `timeout` (ms, 30,000, max 600,000) | `block` (true) |
| OpenAI Codex V1 | `wait_agent` | `targets` | first of several | `timeout_ms` (ms, 30,000, 10,000 to 3,600,000) | always waits |
| OpenAI Codex V2 | `wait_agent` | none | any mailbox update; returns no content | `timeout_ms` (same) | always waits |
| GitHub Copilot CLI | `read_agent` | `agent_id` | one child | `timeout` (s, 30, max 180) | `wait` (false) |
| Devin | `read_subagent` | `agent_id` | one child | `timeout` (s, 30, cap 600) | `block` (false) |
| Factory Droid | `TaskOutput` | `task_id` | one child | not documented | `block` |
| xAI Grok Build | `get_task_output` | `task_ids` | all, with a positive timeout | `timeout_ms` (ms, none, max 600,000) | positive timeout waits |
| xAI Grok Build | `wait_tasks` ("kept for compatibility") | `task_ids` | `mode: "wait_any" \| "wait_all"`, required | `timeout_ms` (ms, none, max 600,000) | always waits |
| Meta Muse Code | `subagent_wait` | `subagent_id` or `agent_path` | one child | `timeout_ms` (ms, 30,000, 10,000 to 300,000) | `wait_for` enum |
| Warp | `wait_for_events` | none | any event | `idle_timeout_seconds` (s) | always waits |
| Augment | async tool, `action: "await"` | `subagentConversationId` | one child | `timeoutSeconds` (s, 60) | always waits |
| Cursor (shells only) | `AwaitShell` | `shell_id` | one shell | `block_until_ms` (ms, 30,000, max 7,140,000) | 0 is a snapshot |
| Z.ai ZCode (deprecated) | `TaskOutput` | `task_id` | one child | `timeout` (ms, 30,000, max 600,000) | `block` (true) |
| Tencent CodeBuddy Code | `TaskOutput` | `task_id` | one child | `timeout` (ms, 60,000) | `block` (true) |
| Kimi CLI | `TaskOutput` | `task_id` | one child | `timeout` (s, 30, max 3,600) | `block` (false) |
| Kode | `TaskOutput` | `task_id` | one child | `timeout` (ms, 30,000, max 600,000) | `block` (true) |
| pi-subagents | `bg_wait` | `id?` | first by default; `all: true` for all | `timeoutMs` (ms) | `nonBlocking` |
| OpenClaw | `subagents`, `action: "wait"` | `runIds` | the selected runs | `timeoutSeconds` (s, 30, 0 to 60) | 0 is a snapshot |
| OpenClaw | `agents_wait` | `ids` | first to finish | `timeoutSeconds?` (s) | always waits |
| Mistral Vibe (default harness) | `tools.subagent.wait` | `agentName` | one child | `timeoutMs` (ms) | always waits |
| Cline SDK | `team_await_runs` | `runId?` | one run, or all when omitted | set by the developer (one hour) | always waits |
| Microsoft Agent Framework | `background_agents_wait_for_first_completion` | `task_ids` (integers) | first to finish | set by the developer (300 s) | always waits |
| DeepSeek Harness | `job_output` | `job_id` | one job | `timeout_ms` (ms) | `wait` (false) |
| OpenAI async tool calling (documented pattern) | `wait_for_tasks` | `task_handles` | the selected handles | none | always waits |
| opencode (removed 2026-05-25) | `task_status` | `task_id` | one child | `timeout_ms` (ms, 60,000) | `wait` |
| PromptForge plan | `subagents_join` | `ids?` (every unjoined subagent by default) | all; first with `any: true` | `timeout` (s, none, no limit) | always waits; `timeout: 0` is a snapshot |

## Appendix C: Cancel tools

*Table 5. The tool a parent model calls to stop a running child, with its id parameter and verb. The last data row lists the harnesses with no model-facing cancel. Protocol methods are included for the verb, though no model calls them directly.*

| Harness | Tool | Id parameter | Verb | Note |
|---|---|---|---|---|
| Claude Code | `TaskStop` (aliases `KillShell`, `KillBash`) | `task_id` | stop | also stops named agents and teammates |
| Factory Droid | `TaskStop` | `task_id` | stop | SIGTERM, then SIGKILL |
| Z.ai ZCode | `TaskStop` | `task_id` | stop | |
| Qoder CLI | `TaskStop` | `task_id`, `reason?` | stop | |
| Tencent CodeBuddy Code | `TaskStop` | not captured | stop | |
| Kimi CLI | `TaskStop` | `task_id`, `reason?` | stop | "not a bash-specific kill tool" |
| Kode | `TaskStop` | `task_id` | stop | |
| Letta Code | `TaskStop` | `task_id` | stop | returns `{ killed: boolean }` |
| Qwen Code | `task_stop` | `task_id` | stop | a final notice follows |
| Hermes Agent | `delegate_task`, `action: "stop"` | `subagent_id` | stop | the partial result still returns |
| pi-subagents | `subagent`, `action: "interrupt"` or `"stop"` | `id` | interrupt, stop | |
| xAI Grok Build | `kill_task` | `task_id` | kill | |
| Google Antigravity | `manage_subagents` | `ConversationIds?` | kill, kill_all | |
| DeepSeek Harness | `job_kill` | `job_id`, `reason?` | kill | "Request cancellation of a running background job." |
| Meta Muse Code | `subagent_cancel` | `subagent_id` or `agent_path`, `reason` | cancel | |
| Deep Agents | `cancel_async_task` | `task_id` | cancel | remote async subagents only |
| Cline SDK | `team_cancel_run` | `runId`, `reason?` | cancel | updates the record without aborting the teammate (earlier survey) |
| OpenClaw | `subagents`, `action: "cancel"` | `runId` | cancel | cancels descendants too |
| Strands | `strands_manage_background_task`, `mode: "cancel"` | `task_id` | cancel | |
| OpenAI Codex V1 | `close_agent` | `target` | close | closes open descendants |
| OpenAI Codex V2 | `interrupt_agent` | `target` | interrupt | the agent survives |
| Mistral Vibe (default harness) | `tools.subagent.interrupt`, `tools.subagent.close` | `agentName` | interrupt, close | |
| A2A v1; MCP | `CancelTask`; `tasks/cancel` | task id | cancel | protocol methods |
| No model-facing cancel | Cursor (its `interrupt` flag replaces a run), Copilot CLI, Devin, Amp, Kiro, Augment, Gemini CLI, Zed, VS Code, Crush, Continue, Roo Code, OpenHands, opencode, Kilo Code, Goose, Codebuff | | | |
| PromptForge plan | `subagents_cancel` | `id` | cancel | limited to the section's own subagents |

## Appendix D: Launch acks and completion notices

*Table 6. What a parent model reads when it starts a background child and when the child finishes. The ack column quotes the phrase that sets the model's next move. "Ends turn" records whether the harness text tells the model it may end its turn or reply to the user while the child runs.*

| Harness | Ack (key phrase) | Notice includes the result | Notice wrapper | Ends turn |
|---|---|---|---|---|
| Claude Code | "Async agent launched successfully." ... "continue other work or respond to the user in the meantime" | yes | user-role `<system-reminder>`: "[SYSTEM NOTIFICATION - NOT USER INPUT]" and `<task-notification>` | yes |
| Cursor | "Subagent is running in the background." ... "either end your turn or work on something else" | yes, in `detail` | user turn `<system_notification>`, after the parent ends its turn | yes |
| OpenAI Codex V1 | `{"agent_id", "nickname"}` | yes | user-role `<subagent_notification>` JSON | no: "Call wait_agent very sparingly" |
| OpenAI Codex V2 | `{"task_name"}` | yes, payload capped at 1,000 tokens | `Message Type: FINAL_ANSWER` envelope | no |
| GitHub Copilot CLI | "Agent started in background with agent_id: ..." ... "Tell the user you're waiting and end your response" | no; points to `read_agent` | `<system_notification>` | yes |
| Devin | "Background subagent started with agent_id=..." | yes | system-role `<subagent_completion_notification>` | yes: "continue with other work or end your turn" |
| Kiro `delegate` | "Agent '{agent}' launched successfully." | a short summary; points to `delegate` status | prepended "1 Background Task Completed" block | not stated |
| Z.ai ZCode | not captured | yes | "[SYSTEM NOTIFICATION - NOT USER INPUT]" and `<task-notification>` | not captured |
| Tencent CodeBuddy Code | not captured | no; the model pulls with `TaskOutput` (translated changelog) | `<task-notification>` | not captured |
| xAI Grok Build | "Subagent started in background." ... "use {task_output_tool} with {task_ids_param}=[...] and a positive {timeout_ms_param}" (a template) | on read; wake text not found | `<subagent_result>` block | no |
| Qwen Code | "Background agent launched successfully." ... "or briefly tell the user what you launched and end your response" | yes | user-role `<task-notification>` | yes |
| Kimi CLI | `task_id: ...` lines; "next_step: You will be automatically notified when it completes." | an output tail | `<notification>` around `<task-notification>` | no |
| Letta Code | "Task running in background with task ID: ..." ... "Just continue with your current work." | yes | `<task-notification>` | no |
| opencode v1 | "The task is working in the background." ... "or briefly tell the user what you launched and end your response" | yes | `<task id state>` envelope | yes |
| opencode v2 | "The subagent is working in the background (sessionID: ...)" ... same ending | yes | `<subagent sessionID state description>` envelope | yes |
| Hermes Agent | dispatch JSON with a note: "then stop with a one-line status" | yes | "[ASYNC DELEGATION COMPLETE - id]" | yes |
| OpenClaw | receipt: "Wait for completion events for ALL required children before your final answer" | yes | "[Internal task completion event]" in runtime context | no |
| pi-subagents | "Detached. Return control now: native completion wakes you" | part of the result and a path (earlier survey) | `subagent-notify` message | yes |
| Kode | "Async agent launched successfully." then pull with `TaskOutput` | no notice | none | no |
| Deep Agents (async) | "Launched async subagent. task_id: ..." | no notice; the model polls | none | yes: report the id "and stop" |
| Microsoft Agent Framework | "Background task {id} started on agent '{name}'." | no; a per-turn status block, results by tool | status block each turn | no: "Always wait for outstanding tasks" |
| Pydantic AI Harness | "Task {id} is running in the background. This is an acceptance receipt, not a result." | yes | system-prompt part, "Automated subagent task report" | no |
| Strands | "Background task dispatched." ... "Continue without waiting or polling." | yes, as a synthetic `get` call | synthetic tool call and result | no |
| DeepSeek Harness | returns the job id | unverified | injected user message | not stated |
| PromptForge plan | `Task id=N started` | no; points to `subagents_join` | one line ahead of the next round | silent |

## Appendix E: Training statements and usage data

*Table 7. The vendor statements, API behavior, datasets, and studies this report relies on for what models were trained on and how much names matter. "Stated" is a vendor's own claim; "observed" is behavior or data read directly.*

| Source | What it shows | Class | Quality and date |
|---|---|---|---|
| OpenAI Codex prompting guide | Trained on `apply_patch`, `shell`, `update_plan`; other tools need "semantically correct" names | stated | official doc, undated |
| OpenAI GPT-5.1 prompting guide | A named built-in `apply_patch` "decreased apply_patch failure rates by 35%" | stated | official doc, undated |
| OpenAI builders' guide to GPT-5.6 | GPT-5.6 trained with "native multi-agent orchestration" | stated | official blog, 2026-08-13 |
| Codex issues 31864 and 32705 | The API reserves `collaboration.spawn_agent {task_name, message, fork_turns}` for GPT-5.6 models | observed (vendor error string) | forum, 2026-07-09 and 2026-07-13 |
| OpenAI harmony guide | gpt-oss trained on `browser` and `python`; use a `functions` namespace to avoid trained names | stated | official doc, undated |
| Anthropic tool-use docs | `memory`, `bash`, `text_editor`, `computer`, `browser` are "trained-in" | stated | official doc, undated |
| Anthropic prompting best practices | Claude "orchestrate[s] subagents natively" with described tools | stated | official doc, undated |
| Anthropic tool reference | "If Claude still names it, return an error `tool_result`", for a tool removed from Claude's list | stated | official doc, undated |
| Claude Code sub-agents doc | `Task` renamed `Agent` in 2.1.63; background by default | stated | official doc, re-read 2026-10-10 |
| Kimi K2.5 tech report | Orchestrator RL-trained with delegation tools printed as `create_subagent`, `assign_task` | stated (evaluation appendix) | tech report, 2026-02-02 |
| Kimi K3 tech report | RL across composed Kimi Code, Claude Code, Codex, OpenClaw, and Hermes harnesses | stated | tech report, 2026-07-27 |
| Qwen3-Coder-Next tech report | Trajectories from six scaffolds including Claude Code; "do not transfer strongly to others" | stated | tech report, 2026-02-28 |
| ZCode docs | ZCode tuned for GLM-5.3 | stated | official doc, undated |
| DeepSeek Harness docs and DSec paper | V4.1 RL rollouts run with DeepSeek Harness as the scaffold | stated | vendor doc and tech report, 2026-09 |
| Antigravity blog | Harness and Gemini 3.5 Flash "co-optimized" | stated | official blog, 2026-05-19 |
| Cognition SWE-1.7 post | "trained directly in the Devin harness" | stated | official blog, 2026-07-08 |
| whoburnedmore usage tracker | `Agent` 47,304 calls from 210 developers; `Task` 19,264 from 9; `wait_agent` 54,266 from 117 | observed | opt-in cohort, 2026-10-10 |
| CC-Bench trajectories | Qwen3-Coder, Kimi-K2, GLM-4.5, DeepSeek-V3.1 call `Task` inside Claude Code (40 calls) | observed | dataset, 2025-07-28 |
| Claude Opus Dataclaw upload | 408 `task_output` calls, with millisecond `timeout` values such as 120000 | observed | dataset, 2026-03-12 |
| OpaqueToolsBench | With names anonymized, parameter names alone keep GPT-5 at 0.82 against 0.95 | observed | preprint, Feb 2026 |
| RoTBench | Noisy tool names cut GPT-4 from 80.00 to 58.10 | observed | peer-reviewed, EMNLP 2024 |
| PA-Tool | Pretraining-aligned names give "improvements of up to 17%" | observed | peer-reviewed, ACL 2026 |
| Deep Agents issue 6286 | Claude Sonnet 5 invents a `prompt` key on every dispatch | observed | forum, 2026-09-13 |
| Codex issue 37113 | GPT-5.6 Sol substitutes `functions.wait` for `collaboration.wait_agent` | observed | forum, 2026-08-05 |
| strands-agents issue 4987 | vLLM drops calls to undeclared tool names before the harness sees them | observed | forum, 2026-10-07 |
| SearchSwarm | An untrained base model "never invokes" a described delegation tool | observed | preprint, June 2026 |

## Sources

Every URL cited above, grouped by owner. Quality labels: official doc or blog (the vendor's own page), source (code at the pinned commit shown), shipped bundle (a vendor package unpacked by version), extracted prompt (a leak repository at a pinned commit), third-party capture, dataset, tech report, peer-reviewed paper, preprint, and forum (GitHub issues and pull requests). Fetch dates are 2026-10-10 unless stated.

**PromptForge.** The plan "Plugin registry, parallel tool calls, and the tasks and subagents Plugins" (Part 4 and its Decision Record); the plan "Author API debt removal" (2026-10-10, step "Resolve model-supplied tool names by wire name only"); the report "How Agent Harnesses Let a Model Spawn, Watch, and Stop Subagents" (2026-10-10).

**Anthropic.**

- Claude Code sub-agents doc (official doc, re-read 2026-10-10): https://code.claude.com/docs/en/sub-agents
- Claude Agent SDK subagents doc (official doc): https://code.claude.com/docs/en/agent-sdk/subagents
- Claude Code changelog (official changelog): https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md and https://code.claude.com/docs/en/changelog
- Claude Code 2.1.296 binary (shipped bundle, 2026-10-09): https://registry.npmjs.org/@anthropic-ai/claude-code-linux-x64/-/claude-code-linux-x64-2.1.296.tgz
- Claude Agent SDK type file 0.3.296 (SDK type file, 2026-10-09): https://unpkg.com/@anthropic-ai/claude-agent-sdk@0.3.296/sdk-tools.d.ts
- How tool use works, trained-in tools (official doc): https://platform.claude.com/docs/en/agents-and-tools/tool-use/how-tool-use-works
- Tool reference, error result for an unoffered name (official doc): https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-reference
- Prompting best practices (official doc): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices
- Prompting Claude Opus 5 (official doc): https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-opus-5
- Managed Agents cookbook (official cookbook, 2026-07-02): https://platform.claude.com/cookbook/managed-agents-cma-plan-big-execute-small
- Managed Agents skill reference (vendor skill file, commit `dbd4588`): https://github.com/anthropics/skills/blob/dbd4588/skills/claude-api/shared/managed-agents-multiagent.md
- Research lead prompt with `run_blocking_subagent` (vendor cookbook prompt, 2025-07-29): https://github.com/anthropics/claude-cookbooks/blob/66ab04a/patterns/agents/prompts/research_lead_agent.md
- Writing effective tools for agents (vendor blog, 2025-09-11): https://www.anthropic.com/engineering/writing-tools-for-agents
- Tool name rules (official doc): https://platform.claude.com/docs/en/agents-and-tools/tool-use/define-tools

**OpenAI.**

- Codex source, multi-agent tool specs (source, `cc7ba33`, 2026-10-10): https://github.com/openai/codex/blob/cc7ba33601286a751477832b01de7b6f8de0dd9c/codex-rs/core/src/tools/handlers/multi_agents_spec.rs
- Codex issue 31864, reserved `collaboration.spawn_agent` (forum, 2026-07-09, re-read): https://github.com/openai/codex/issues/31864
- Codex issue 32705, reserved schema fields (forum, 2026-07-13): https://github.com/openai/codex/issues/32705
- Codex issue 37113, `functions.wait` substitution (forum, 2026-08-05): https://github.com/openai/codex/issues/37113
- Codex issue 24225, V1 double delivery (forum, via the earlier survey): https://github.com/openai/codex/issues/24225
- Codex PR 26994, `close_agent` renamed `interrupt_agent` (source, 2026-06-08): https://github.com/openai/codex/pull/26994
- Codex subagents doc (official doc): https://developers.openai.com/codex/subagents
- Codex docs dump with the hooks alias (official doc): https://developers.openai.com/codex/llms-full.txt
- Codex prompting guide (official cookbook): https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide
- GPT-5.1 prompting guide (official cookbook): https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-1_prompting_guide
- Builders' guide to GPT-5.6 (official blog, 2026-08-13): https://openai.com/index/builders-guide-to-gpt-5-6/
- Latest-model guide, GPT-6 Astra delegation sentence (official doc): https://developers.openai.com/api/docs/guides/latest-model
- Responses API multi-agent guide (official doc): https://developers.openai.com/api/docs/guides/responses-multi-agent
- Async tool calling, `wait_for_tasks` (official doc): https://developers.openai.com/api/docs/guides/async-tool-calling
- Harmony format and gpt-oss tools (official doc): https://cookbook.openai.com/articles/openai-harmony
- Tool name rules (official API reference): https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create/
- Agents SDK `as_tool` (source, `125efa0`): https://github.com/openai/openai-agents-python/blob/125efa029b4bfd84238bd2c4fd69c3406f802663/src/agents/agent.py

**Cursor.**

- Continually improving our agent harness (official blog, 2026-04-30): https://cursor.com/blog/continually-improving-agent-harness
- GPT-family `functions.Subagent` dialect (third-party capture, 2026-08-02): https://github.com/fitchmultz/pi-cursor-sdk/blob/eee1ae42d41011ff3edc3994d9b0eed8dcafd85d/docs/evidence/cursor-system-prompts-2026-08-02/README.md
- Background notice in exported transcripts (third-party capture, 2026-04-28): https://code.organicdesign.nz/organicdesign/4qx-holarchy/commit/8a2cd711a45a044b29b13461f8cb8cbbcf48801f.patch
- `Task`, `AwaitShell`, and `Shell` schemas: this session's own tool definitions (first-hand, 2026-10-10; no URL).

**GitHub and Microsoft.**

- Copilot CLI shipped bundles 1.0.10 (`@github/copilot`) and 1.0.95 (`@github/copilot-linux-x64`), unpacked from npm (shipped bundle; no URL).
- Copilot CLI issue 2595, quoting the 1.0.95 ack (forum): https://github.com/github/copilot-cli/issues/2595
- Copilot CLI changelog (official changelog): https://github.com/github/copilot-cli/blob/main/changelog.md
- Copilot hooks reference (official doc): https://docs.github.com/en/copilot/reference/hooks-reference
- Copilot harness across models (official blog, 2026-06-25): https://github.blog/ai-and-ml/github-copilot/evaluating-performance-and-efficiency-of-the-github-copilot-agentic-harness-across-models-and-tasks/
- MAI-Code-1-Flash (vendor blog, 2026-06-02): https://microsoft.ai/news/introducingmai-code-1-flash/
- VS Code `runSubagent` (source, `cc3fec8`): https://github.com/microsoft/vscode/blob/cc3fec8846d0e678357e476fa611774da26d7e24/src/vs/workbench/contrib/chat/common/tools/builtinTools/runSubagentTool.ts
- Agent Framework background agents (source, `fd52de7`): https://github.com/microsoft/agent-framework/blob/fd52de71579162a888fb2dd7510c57c6014dcdfc/python/packages/core/agent_framework/_harness/_background_agents.py and PR 6069 (2026-05-27): https://github.com/microsoft/agent-framework/pull/6069

**Google.**

- Gemini CLI `invoke_agent` (source, `9b6e026`): https://github.com/google-gemini/gemini-cli/blob/9b6e0265d16bbd29ca51e33c9e0c01dc4cec5e83/packages/core/src/agents/agent-tool.ts
- Gemini CLI PR 17346, back to per-agent tools (source): https://github.com/google-gemini/gemini-cli/pull/17346
- Antigravity hooks doc (official doc): https://www.antigravity.google/docs/hooks/
- Antigravity CLI changelog (official changelog): https://raw.githubusercontent.com/google-antigravity/antigravity-cli/main/CHANGELOG.md
- Gemini 3.5 Flash in Antigravity (official blog, 2026-05-19): https://antigravity.google/blog/gemini-3-5-flash-in-google-antigravity

**Other closed harnesses.**

- Devin CLI subagents (official doc): https://docs.devin.ai/cli/subagents.md
- Devin session receipt, v3000.11.3 (third-party capture, 2026-09-25): https://github.com/agent-next/art-discovery-repro/blob/e71b828d9886b9c04b023e9e5264691597c033dc/task-runs/20260924-myreview-s1/devin-s1-receipt.json
- Devin session exports, v3000.10.21 (third-party capture): https://github.com/KaolaBrother/Kaola-Workflow/tree/694a32e2d86bfe3302c44008ebb6464eb66ea955/kaola-workflow/archive/issue-1060/.cache/out
- Cognition SWE-1.7 (official blog, 2026-07-08): https://cognition.com/blog/swe-1-7
- Factory subagents (official doc): https://docs.factory.ai/harness/subagents
- Grok Build task tool (source, `2bdd1d6`): https://github.com/xai-org/grok-build/blob/2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8/crates/common/xai-tool-types/src/task.rs
- Grok Build web tools (extracted prompt, `181ebcd`): https://github.com/asgeirtj/system_prompts_leaks/blob/181ebcd703f377a71fd87e21ca6839b54ccfae67/xAI/grok-build.md
- Muse Code native tools (official doc): https://dev.meta.ai/docs/muse-code/extending/ and (extracted prompt) https://github.com/asgeirtj/system_prompts_leaks/blob/181ebcd703f377a71fd87e21ca6839b54ccfae67/Meta/muse-code/muse-spark-1.3-muse-code.md
- ZCode tools (extracted prompt, `a4d3da0`): https://github.com/elder-plinius/CL4R1T4S/blob/a4d3da04e63324e794a65500c3e41994fc4ab02e/ZAI/ZCode/Tools.json and ZCode docs (official doc): https://zcode.z.ai/en/docs/welcome
- Qoder CLI SDK reference (official doc): https://docs.qoder.com/cli/sdk/references-typescript
- CodeBuddy Code tools reference (official doc): https://www.codebuddy.ai/docs/cli/tools-reference
- Kiro `delegate` (source, Amazon Q Developer CLI `15cc8f3`): https://github.com/aws/amazon-q-developer-cli/blob/15cc8f3cd18c4272925ce1c7053268eedff1ea0a/crates/chat-cli/src/cli/chat/tools/delegate.rs
- Amp models and subagents (official doc): https://ampcode.com/docs/models-and-subagents
- Warp multi-agent protocol (source, `e6b8fe9`): https://github.com/warpdotdev/warp-proto-apis/blob/e6b8fe90b000e264a2849a1888fa8b522d1fa98f/apis/multi_agent/v1/task.proto

**Open harnesses (source at the pinned commit in each URL).**

- Qwen Code `agent`: https://github.com/QwenLM/qwen-code/blob/9763580b84225b4811bd05c716f1d05b37cfdf9d/packages/core/src/tools/agent/agent.ts; rename PR 2489: https://github.com/QwenLM/qwen-code/pull/2489; background-default PR 7048: https://github.com/QwenLM/qwen-code/pull/7048; unknown-tool error naming valid tools, issue 1307 (forum, 2025-12-21): https://github.com/QwenLM/qwen-code/issues/1307
- Kimi CLI `Agent` and background tools: https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/tools/agent/__init__.py and https://github.com/MoonshotAI/kimi-cli/blob/9ab1286b8fe4e6bcd116949a27ce5e0ac3389c82/src/kimi_cli/tools/background/__init__.py
- Letta Code name mapping: https://github.com/letta-ai/letta-code/blob/271f119dcf37d58649a18e6c733386b3c710a456/src/tools/tool-name-mapping.ts
- opencode v1 `task`: https://github.com/anomalyco/opencode/blob/055d95bb7e278c94baf06235a52cac79dd13ba67/packages/opencode/src/tool/task.ts; v2 `subagent`: https://github.com/anomalyco/opencode/blob/7b3d4ce3a7dbd2a6d3637722a0d5f22a7d086937/packages/core/src/tool/plugin/subagent.ts
- opencode issue 9379 (forum, 2026-01-19): https://github.com/anomalyco/opencode/issues/9379; issue 1336 (forum, 2025-07-26): https://github.com/anomalyco/opencode/issues/1336
- Kilo Code `task`: https://github.com/Kilo-Org/kilocode/blob/fb7e96eda5409517a05948b9efaf01c53997bf6e/packages/opencode/src/tool/task.ts
- Charm Crush `agent`: https://github.com/charmbracelet/crush/blob/df5b024a929d2eb88b308d0288d97130a90e0c15/internal/agent/agent_tool.go
- Cline SDK team tools: https://github.com/cline/cline/blob/c3a40572765b76873c597247941118c1778d02c8/sdk/packages/core/src/extensions/tools/team/team-tools.ts
- Roo Code `new_task`: https://github.com/RooCodeInc/Roo-Code/blob/b867ec9145750d0ae1ff7f02d35406e9bf2a0b16/src/core/prompts/tools/native-tools/new_task.ts; alias PR 9989 (2025-12-12): https://github.com/RooCodeInc/Roo-Code/pull/9989
- Continue `Subagent`: https://github.com/continuedev/continue/blob/5522c6f44ca0ac3528b37244818fbfa39b5af470/extensions/cli/src/subagent/index.ts
- OpenHands `task`: https://github.com/OpenHands/software-agent-sdk/blob/c4b93299cf2b31c8b5d0b2c5a89965ccc5ff24f9/openhands-tools/openhands/tools/task/definition.py; issue 9306 (forum, 2025-06-23): https://github.com/All-Hands-AI/OpenHands/issues/9306
- Goose `delegate`: https://github.com/aaif-goose/goose/blob/3bd852002903e016ff30947e973f76e2fcfcf90f/crates/goose/src/agents/platform_extensions/summon.rs; background removal PR 12729: https://github.com/aaif-goose/goose/pull/12729
- Zed `spawn_agent`: https://github.com/zed-industries/zed/blob/93d745668805029476e6d7fbb19652116fed51de/crates/agent/src/tools/spawn_agent_tool.rs; rename PR 49741: https://github.com/zed-industries/zed/pull/49741
- Deep Agents `task` and async tools: https://github.com/langchain-ai/deepagents/blob/9f0e39d55a5f31003b206b31b955154f2f1bc49a/libs/deepagents/deepagents/middleware/subagents.py and https://github.com/langchain-ai/deepagents/blob/9f0e39d55a5f31003b206b31b955154f2f1bc49a/libs/deepagents/deepagents/middleware/async_subagents.py
- Deep Agents issue 6286 (forum, 2026-09-13, re-read): https://github.com/langchain-ai/deepagents/issues/6286; fix PR 6299 (2026-09-22): https://github.com/langchain-ai/deepagents/pull/6299
- OpenClaw `subagents`: https://github.com/openclaw/openclaw/blob/0d4a332ea0c01e668e06ff2d87fdb0a4e6524959/src/agents/tools/subagents-tool.ts
- Hermes Agent `delegate_task`: https://github.com/NousResearch/hermes-agent/blob/6a2662a4aaad68e1b75f6e7ac789409aa653abf7/tools/delegate_tool.py
- Mistral Vibe legacy `task`: https://github.com/mistralai/mistral-vibe/blob/4ae5c5955da8e761318916bdb1a7f46f0b50c7d0/vibe/core/subagents.py
- Kode `Task`: https://github.com/shareAI-lab/Kode-CLI/blob/c7f6fccf7ec4b171a40bfe4967fc3dbbe3723d51/packages/tools/src/tools/ai/TaskTool/schema.ts
- pi-subagents: https://github.com/nicobailon/pi-subagents/blob/ca7162e72e9c7c10a50a8dfb75d012b71f330d3d/src/extension/schemas.ts
- Codebuff `spawn_agents`: https://github.com/CodebuffAI/freebuff/blob/d418a5168898a2cf9e6bdbfac7e1f1d96a3df32b/common/src/tools/params/tool/spawn-agents.ts
- DeepSeek Harness tool catalog (vendor doc, undated developer preview): https://deepseek-harness.github.io/deepseek-harness/en/reference/tool-catalog
- Xiaomi MiMo-Code exact-name design (vendor design doc, 2026-09-15): https://raw.githubusercontent.com/XiaomiMiMo/MiMo-Code/f98dcd1cf7e70e7eb42f721fdf72bc4a6b87914f/docs/compose/spec/tool-name-case-hint.md
- strands-agents harness issue 4987 (forum, 2026-10-07): https://github.com/strands-agents/harness-sdk/issues/4987

**Frameworks and protocols (source at the pinned commit in each URL).**

- Pydantic AI Harness `delegate_task`: https://github.com/pydantic/pydantic-ai/blob/69ea1e57201ed59e7d30fbe4a7590d193acecce0/src/pydantic_ai_harness/pydantic_ai_harness/subagents/_toolset.py
- Strands background tasks: https://github.com/strands-agents/sdk-python/blob/38afb968e1f40aa47546ead09a22ec031bd345de/strands-py/src/strands/background_tasks/_background_tasks.py
- Mastra sub-agent tools: https://github.com/mastra-ai/mastra/blob/3645c3d67e0c1f40005035911103deba381d246a/packages/core/src/agent/agent.ts
- A2A specification: https://github.com/a2aproject/A2A/blob/12e9d2fbb9badfe98f8ab4f660697870eeb1940b/docs/specification.md
- MCP tasks extension: https://github.com/modelcontextprotocol/modelcontextprotocol/blob/c518f7a927cff918bce35d3522fcdb046d264d7c/seps/2663-tasks-extension.md
- Manus, context engineering (blog, 2025-07-18): https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus
- Bedrock tool name rules (official doc): https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_ToolSpecification.html

**Model reports, datasets, studies, and usage data.**

- Kimi K2.5 (tech report, 2026-02-02): https://arxiv.org/abs/2602.02276
- Kimi K3 (tech report, 2026-07-27): https://arxiv.org/abs/2607.24653
- Qwen3-Coder-Next (tech report, 2026-02-28): https://arxiv.org/abs/2603.00729
- DeepSeek DSec (tech report, 2026-09-19): https://arxiv.org/abs/2609.22978
- CC-Bench trajectories (dataset, 2025-07-28): https://huggingface.co/datasets/zai-org/CC-Bench-trajectories
- Claude Opus Dataclaw upload (dataset, 2026-03-12): https://huggingface.co/datasets/TeichAI/Claude-Opus-Dataclaw-Unredacted
- whoburnedmore usage tracker (opt-in cohort, data 2026-10-10): https://whoburnedmore.com/research/ai-agent-tool-usage
- OpaqueToolsBench (preprint, Feb 2026): https://arxiv.org/html/2602.15197v1
- RoTBench (peer-reviewed, EMNLP 2024): https://arxiv.org/abs/2401.08326
- PA-Tool (peer-reviewed, ACL 2026): https://arxiv.org/abs/2510.07248
- In harmony with gpt-oss (preprint, Apr 2026): https://arxiv.org/abs/2604.00362
- Tool calling is linearly readable and steerable (preprint, May 2026): https://arxiv.org/html/2605.07990v2
- SearchSwarm (preprint, June 2026): https://arxiv.org/abs/2606.09730

**Supporting research**, each produced 2026-10-10 and holding the full verbatim schemas, permalinks, dates, and quality ratings behind this report:

- "Closed-source harnesses: model-facing subagent tool names, schemas, and behavior"
- "Open-source coding harnesses: model-facing subagent, delegation, and background-task tools"
- "Naming survey slice: agent frameworks and SDKs that expose delegation to a model as a tool"
- "Training-data alignment for subagent tools: what models were trained on, and how much names and shapes matter"

*2026-10-10 16:56 - Claude Opus 5.5 (Cursor agent).*
