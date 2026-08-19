# Task blocks for the PromptForge design-principles pipeline

Each block below is dispatched by reference: the subagent receives this file's path and a tag name, greps for the tag, and executes the block it encloses. Each block is self-contained.

<reducer-rules>
You reduce one cleaned chat unit to its principle-bearing core. You are given the unit's path and an output path.

The unit contains a user's voice-dictated prompts from one chat about the design of PromptForge, a prompting language and engine. Paragraphs carry stable markers like **[p12]**. The unit may end with Plans and Design Documents sections written by the AI assistant.

Rules:
1. Recall first. Remove only what cannot carry a design principle. A later stage does the selecting. When in doubt, keep the paragraph.
2. Keep verbatim: every user paragraph that expresses how the system should behave, a correction, a rejection, a rationale, or a design preference, plus the minimum surrounding exchange that makes a correction intelligible.
3. Compress: pasted external material (papers, transcripts, code, logs) becomes a one-line bracketed note, e.g. [pasted: P4210R1 paper, ~300 lines]. Environment troubleshooting and debugging blow-by-blow become one-line summaries. Pleasantries and status chatter are dropped.
4. Plans and Design Documents sections: keep each plan's name, overview, and every statement of principle, decision rationale, or rejected alternative. Drop step lists, file-path inventories, and test plans.
5. Preserve every **[pN]** marker on surviving content and never renumber. Citations downstream resolve to the cleaned file by these markers.
6. Target at most 25KB out. If the unit cannot reach 25KB without cutting kept-class content, keep the content and report the overrun.

Write the reduced unit to the output path. Return at most 100 words: input size, output size, any overrun.
</reducer-rules>

<extractor-rules>
You mine one reduced chat unit for design principles of PromptForge, a prompting language and engine. You are given the unit's path and an output path.

Behavioral rules:
1. Apply the altitude test to every candidate sentence. If the statement says WHICH technology to use (native IOCP watcher, no shelling out, trafilatura vs readability), it is an implementation preference: exclude it. If the statement says HOW the language or engine behaves, it is a design principle: extract it. Include-example: "execution is identical whether reached by jump, execute, or fanout". Exclude-example: "Hell no to shellout". The altitude test applies to the Plans and Design Documents sections too.
2. Rewrite each finding as one standalone normalized statement; clean up voice-dictation fragments.
3. When the principle is a rejection, add one line naming the rejected alternative.
4. For candidates mined from the Plans or Design Documents sections: tag them ai-proposed, read the prompts that follow, and record whether the user affirmed, corrected, or rejected the proposal. An ai-proposed principle the user never endorsed is weak evidence.
5. When a passage teaches but does not convert into a directive (a philosophy, a preference, a temperament), add its one-line gist to a "Not converted" list and do nothing else with it.
6. If the file yields no principles, write an empty list with a one-line reason. Never invent a principle.
7. Keep at most 20 candidates, favoring generality across cases.

Write the output file as: a heading with the unit name, then the candidate records in the yaml shape below, then a "Not converted" list. Format rules live in these examples, not in the behavioral rules:

```yaml
# user-stated example
- statement: Execution is identical whether a section is reached by fall-through, execute(), jump(), or a fanout arm.
  scope: core            # one of: global, core, gateway, mcp, cli, boundary: X<->Y
  source: user-corrective # one of: user-stated, user-corrective, ai-proposed
  citation: 2026-08-19-0447-collapse-fanout-arm-review.md [p2]
  rejected-alternative: a separate arm-execution path with its own functions
  endorsement: n/a

# ai-proposed example
- statement: A run that outlives the client is collected through a deferred-collect path.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [plans section]
  rejected-alternative: none
  endorsement: affirmed   # one of: affirmed, corrected, rejected, unaddressed

# WRONG - do not emit this record; it fails the altitude test (technology choice, not behavior):
# - statement: Use a native IOCP directory watcher on Windows instead of polling.
```

Return at most 200 words: candidate count, Not-converted count, and any anomalies. If the unit file is missing, name it and stop.
</extractor-rules>

<group-task>
You dedupe, trim, and group the mined design-principle candidates for PromptForge. You are given the research-packet path and an output path.

Steps:
1. If the packet holds more than 400 records, say so in your return and stop; the orchestrator will run a pre-dedupe fan-out first.
2. Remove near-duplicate candidates, keeping the sharpest wording and merging all citations under the survivor. Two candidates are duplicates when they assert the same constraint on the same scope. When unsure, keep both.
3. Trim to at most 100: rank by coverage (independent chats enforcing the principle), derivation weight (crate-level principles descending from it), and generality. Keep the strongest 100.
4. Assign each survivor to its scope layer: Global, Core, Boundary, or Gateway/MCP/CLI. Then cluster related principles into named themes inside each layer.
5. Order principles inside each layer from most to least fundamental.
6. Write one three-sentence stanza per layer: what the layer covers, the failure modes it prevents, and one unifying principle that compresses the layer's rules.
7. Append an "Open questions" list: tensions or contradictions between surviving principles that the record leaves unresolved.
8. Preserve the merged "Not converted" list at the end.

Keep each candidate's full record (statement, scope, source, citations, rejected-alternative, endorsement) in the output. Write the grouped draft to the output path. Return only the path plus per-layer names and counts.
</group-task>

<approach-task>
You compress a merged "Not converted" list into one closing section for a design-principles document. You are given the grouped-draft path (whose final section is the merged "Not converted" list) and an output path. Read only that final list.

The subject is the design philosophy of PromptForge, a prompting language and engine, as revealed by its author's corrections and preferences across three weeks of design chats.

Steps:
1. Sort the items into two piles. Pile one: items that reveal the design sensibility - philosophy, aesthetics, temperament, beliefs about where the design lives. Pile two: bookkeeping - items rejected as too narrow, subsumed by a rule, or duplicative. Discard pile two entirely.
2. From pile one, find the through-lines: what the author believes the design actually is, how they treat the language as a made object, what temperament they bring when a limit appears, and where they place evidence in design decisions.
3. Write one prose paragraph of 5 to 8 sentences headed "## The Approach Behind the Rules". Open with the observation that not everything converts to a rule, because the rules are the residue of a practice, not the practice itself. Weave the through-lines into flowing prose. Close on the item that best states where the design ultimately rests.
4. If the paragraph exceeds 8 sentences, split it into two paragraphs at the natural thematic seam. Keep both under the same heading.

Hard constraints: prose only, no bullets, no lists, no quotes of the discarded pile. Never use an em dash or a double dash; use a single dash or a comma. Write the result to the output path. Return only the output path.
</approach-task>

<audit-task>
You audit a finished design-principles document against the research packet it came from. You are given the document path and the research-packet path. Do not edit the document.

Check each item as a yes-or-no question:
1. Grounding: every principle traces to at least one candidate in the research packet.
2. No provenance: no citation, source name, or "the user said" anywhere in the document.
3. Form: every principle is a bold imperative followed by 1-2 sentences of rationale.
4. Numbering: continuous from 1, no repeat, no gap.
5. Cap: at most 100 principles.
6. Structure: every section is wrapped in one uniquely named tag and opens with its stanza; the Approach section is present as prose with no bulleted list remaining.
7. Rationale honesty: spot-check 10 rationales against the packet; flag any invented motive.

Write one line per failed check, naming the location and the single fix, to a scratch findings path. Return only that path.
</audit-task>
