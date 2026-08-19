# Packet Section 1: The Language's Posture (Principles 1-7)

Facts only. Sources: purpose-cluster-1.md (purpose notes, merge map), grouped-draft.md "Global" layer (full records: statement, rejected-alternative, endorsement), design-principles.md Section I (final wording and order).

## Principle 1: Do more with less

- Rule: Do more with less. Before you build anything, stretch what is already there. Never provide two ways of doing the same thing without a really good documented reason.
- Purpose facts:
  - Every new feature adds infrastructure that has to be built, documented, and maintained; the first question is always whether something already in the language can do the job.
  - Without this rule the core accumulates dedicated single-purpose features instead of staying a small set of reusable primitives.
  - Duplicate facilities force every future decision to be made twice and create ambiguity about which one to use; two ways invite the question of which one is correct, forever.
  - Two ways of doing one thing is where stale, redundant code comes from.
  - A second mechanism alongside a working one means two implementations to keep correct and two things for the prompt author to learn.
  - Brevity clause (borderline record): prompt authors should write less; verbosity is a design failure.
- Rejected alternatives and stated costs:
  - A dedicated `require_called` directive for mandatory tool calls - rejected because an epilogue Lua assert over a call count already expresses it.
  - New frontmatter - rejected because Lua already works.
  - A YAML `default return` - rejected because a jump to a constant-return section already expresses it.
  - Duplicate facilities for the same capability - cost: every future decision made twice, permanent ambiguity about which is correct.
  - A new mechanism alongside an existing one that already covers the need (case: file access control for sections, covered by stretching tool scoping) - cost: two implementations to keep correct, two things to learn.
  - `models.only` (all-or-nothing model lock) - rejected because a prompt with one or two exceptions was forced to restate the whole model list; a default plus per-section override says the same in fewer words.
- Concrete incidents:
  - The author removed tool frontmatter because the H1 block already declared tools.
  - `infer()` was kept strictly different from prose: if infer were "just another version of Prose" the language would inherit all the same questions (how do you set the tools, what happens if you jump) for both.
  - During the store redesign, "no parallel mechanisms" was stated verbatim as "a general principle."
  - Author-verbatim: in 2026-08-09-1058-promptforge-core-large-part1.md [p26] the author states "design rule number one" (smallest facility, don't invent a new facility when an existing one handles it) and "design rule number two" (never two ways of doing the same thing) in one breath.
- Merge/derivation notes:
  - Merged from purpose-cluster records 1 ("Do more with less"), 2 ("Never provide two ways of doing the same thing"), and 3 ("No parallel mechanisms") - one shared purpose: keep the core minimal by reusing existing facilities.
  - Record 4 ("A small set of flexible, multi-purpose primitives compose into maximum possibility while keeping the prompt author brief") is a borderline candidate for the group; it adds the distinct brevity purpose.
  - Grouped-draft sources: "Minimal mechanism" group, four records; all endorsements n/a; sources user-stated and user-corrective.

## Principle 2: Keep the language consistent; constraints fall out of the rules

- Rule: Keep the language consistent, and let constraints fall out of the rules instead of writing special-case checks.
- Purpose facts:
  - Inconsistency surprises the prompt author.
  - A correct constraint should fall out of the existing rules on its own, not be a separate check someone has to remember to write.
  - The fix for an inconsistency is to make the invariant uniform, not to patch the case.
- Rejected alternative and stated cost:
  - Hand-coded guard checks for each constraint - cost: a separate check someone has to remember to write; exceptions need a really good reason.
- Concrete incidents:
  - `jump()` could not carry the model's reply into the next section, so Lua code that wanted to branch on an inference result lost data for no principled reason. The fix was to make the invariant uniform: the previous reply is always in `reply` on section entry.
  - Example of a constraint that should fall out on its own: "model locked after first Lua block."
- Merge/derivation notes:
  - Single record (purpose-cluster record 5; grouped-draft "Minimal mechanism" group, fifth record). Kept separate from the minimal-mechanism group because its purpose is predictability of behavior, not minimality of features.
  - Citations: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20-p21]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p176-p178]. Endorsement n/a; source user-stated.

## Principle 3: A prompt must be readable on its face

- Rule: A prompt must be readable on its face.
- Purpose facts:
  - If a reader cannot see the control flow in the text, the prompt's behavior depends on how the model interprets hidden instructions.
  - Readability on the face is what keeps a prompt's meaning fixed instead of model-dependent.
  - Behavior the reader cannot see is behavior the reader cannot debug.
- Rejected alternative and stated cost:
  - Dispatch expressed as literal text the model is expected to interpret and act on - cost: the prompt's behavior becomes subject to the model's interpretation of invisible action.
- Concrete incidents:
  - The author looked at his own design, where dispatch was written as literal text the model was expected to interpret and act on, and could not tell what the prompt did.
  - Author-verbatim: he called this being "confused by my own design."
- Merge/derivation notes:
  - Single record (purpose-cluster record 6; grouped-draft "Legibility and naming" group, first record). Kept separate.
  - Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [p360-p362]; 2026-08-02-1134-mcp-client-large-part5.md [p362]. Endorsement n/a; source user-corrective.

## Principle 4: Borrow from the ordinary theory of computation

- Rule: Borrow from the ordinary theory of computation. Shared reusable sections are subroutines; control transfer behaves the way programmers already expect.
- Purpose facts:
  - When a new construct is needed, take it from established computation rather than inventing a novel one.
  - A familiar construct needs no new theory to explain it, and every reader's existing intuition does the teaching.
- Rejected alternative and stated cost:
  - None recorded (rejected-alternative: none).
- Concrete incidents:
  - Shared top-level reusable sections were accepted precisely because they are subroutines - author-verbatim: "a staple of computation."
- Merge/derivation notes:
  - Single record (purpose-cluster record 7; grouped-draft "Legibility and naming" group, second record). Kept separate.
  - Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [p385]; 2026-08-02-1134-mcp-client-large-part5.md [p385]. Endorsement n/a; source user-stated.

## Principle 5: Names come from vocabulary already owned; one meaning per term

- Rule: Names come from vocabulary the model and the prompt writer already own, and each term holds one meaning everywhere.
- Purpose facts:
  - The model has to execute these words, so a name the model already knows maps correctly where an invented term might not.
  - A name is also documentation: a design decision that must say how the mechanism works, so there is no confusion.
  - Wrong names produce wrong model behavior and confused readers.
  - One fixed meaning per term, enforced in every file, keeps docs, code, and plans saying the same thing.
  - Repo-wide enforcement is cheap because the language is unshipped.
- Rejected alternative and stated cost:
  - None recorded for either underlying record (rejected-alternative: none, both).
- Concrete incidents:
  - The author's naming test, verbatim: "will the model know what the fuck to do?" (example of a passing name: "spawn three asynchronous sub-agents").
  - `Prompt.replay` was approved because, verbatim, "it tells you how it works so there is no confusion."
  - The words preamble, prologue, and epilogue were being used loosely across the repo - 180 occurrences to fix - and the preamble is meaningfully different from the prologue, so mixing the terms misstated how the language works until they were fixed in every file. Fixed terminology: the preamble is the H1 code, while prologue and epilogue belong to sections.
  - Author-verbatim on why enforcement is cheap: "there's no one to break."
- Merge/derivation notes:
  - Merged from two records deliberately kept distinct in the purpose pass: record 8 (choosing names the model and reader understand) and record 9 (using one term consistently everywhere, enforced repo-wide). The final principle joins them: names come from owned vocabulary AND each term holds one meaning everywhere.
  - Grouped-draft sources: "Legibility and naming" group, third and fourth records; endorsements n/a; sources user-stated.
  - Citations: 2026-07-30-0534-promptforge-design-context.md [p30-p31]; 2026-08-14-1613-promptforge-core-largest-part5.md [p473], [p393], [p395]; 2026-08-02-2331-mcp-client-evening.md [plans section]; 2026-08-09-1058-promptforge-core-large-part5.md [p393].

## Principle 6: No defaults

- Rule: No defaults. Every prompt declares the model it needs, or explicitly says it accepts anything, and states its required context and whether it needs thinking.
- Purpose facts:
  - A default is an invisible setting that can change and silently change a prompt's behavior.
  - The point of the system is to be as deterministic as possible while still doing inference.
  - A prompt always knows its minimum context and whether it needs thinking, so it can always say what it needs.
  - Grouped-draft framing, verbatim: "implicit configuration is the enemy of precision."
- Rejected alternatives and stated costs:
  - `DEFAULT_MODEL` and `PROMPTFORGE_MODEL` environment-variable fallbacks - removed; cost: invisible settings that silently change behavior.
  - A default recursion limit of 24 - rejected for the same reason.
- Concrete incidents:
  - The author removed the `DEFAULT_MODEL` and `PROMPTFORGE_MODEL` environment fallbacks.
  - Author-verbatim: a prompt that specifies nothing "doesn't make sense."
- Merge/derivation notes:
  - Single record (purpose-cluster record 10; grouped-draft "Explicitness and consent" group, first record). Kept separate.
  - Citations: 2026-08-08-1223-gateway-local-inference.md [p58], [p60], [p62]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p66]. Endorsement n/a; source user-corrective.
  - Open-questions note: the design document's Open Questions list records an unresolved tension between "No defaults, everything explicit" and "implement all features and let the caller decide, with sensible defaults."

## Principle 7: Every restriction has an explicit escape

- Rule: Every restriction has an explicit escape. The prompt author opts into powerful capabilities by writing them; the embedder building an agent or an IDE can disable any protection the engine imposes.
- Purpose facts:
  - Consent is the gate for powerful capabilities; consent is what makes power acceptable.
  - A restriction with no escape blocks the legitimate user along with the dangerous one.
  - Protections exist to shield the machine from untrusted prompts, but the engine is also embedded by people building agents, harnesses, and IDEs who need real file access and full control.
  - If a protection cannot be turned off, legitimate embedders are blocked by a guard meant for someone else. So every setting must have a way to be disabled.
- Rejected alternatives and stated costs:
  - Restricting the behavior outright regardless of user consent - cost: powerful capabilities cannot exist at all.
  - Compulsory protections with no opt-out - cost: legitimate embedders blocked by guards meant for untrusted prompts.
- Concrete incidents:
  - The toolset is closed after the preamble, but the author wanted a Lua tool that adds a tool mid-run (a Lua search front end that calls `tools.add` for fetch when invoked). His resolution: the prompt author wrote that Lua tool, so the dynamic add is opted into, and consent is what makes an otherwise restricted behavior acceptable.
- Merge/derivation notes:
  - Merged from two records deliberately kept distinct in the purpose pass: record 11 (the prompt author consenting to a capability by writing it) and record 12 (the embedder needing an off-switch for every protection). The final principle joins both directions of escape.
  - Grouped-draft sources: "Explicitness and consent" group, second and third records; endorsements n/a; sources user-stated.
  - Citations: 2026-08-14-1613-promptforge-core-largest-part4.md [p372-p374]; 2026-08-02-1134-mcp-client-large-part5.md [p353-p354]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p354].

## Stanza facts (Section I as a whole)

- What the section covers: the constitution layer - the rules that decide what gets into the language at all (feature admission, consistency, legibility, naming, explicitness, and consent).
- Why the layer exists, verbatim from the stanza: "every feature is a permanent cost and every duplicate is a permanent ambiguity."
- Failure modes it prevents:
  - Accretion of dedicated single-purpose features and parallel mechanisms (principles 1-2).
  - Special-case checks someone has to remember to write (principle 2).
  - Behavior invisible to the reader and therefore undebuggable; meaning that drifts with model interpretation (principle 3).
  - Novel constructs that need new theory to explain (principle 4).
  - Wrong model behavior from invented names; docs, code, and plans that say different things (principle 5).
  - Silent behavior changes from invisible settings; nondeterminism (principle 6).
  - Legitimate users blocked alongside dangerous ones (principle 7).
- The one-sentence unifying principle, verbatim: "the smallest facility that does the most wins."
- Record counts: 7 principles derived from 10 purpose-cluster records (records 1-3 merged into principle 1 with record 4 borderline; records 8-9 merged into principle 5; records 11-12 merged into principle 7; records 5, 6, 7, 10 stand alone).

