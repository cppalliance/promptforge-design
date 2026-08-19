# Writing packet - PromptForge design principles



Facts only. The writer turns each fact sheet into prose. Section order and principle order are fixed.



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

# Packet Section II - The Document (Principles 8-13)

Facts only. Sources: purpose-cluster-2.md (motivations), grouped-draft.md (records: statement, rejected-alternative, endorsement).

---

## Principle 8

- Rule: A prompt is one self-contained markdown file that is one function: parameters in through YAML front matter, a string out, side effects allowed.
- Purpose facts:
  - The basic unit of the system is the function: parameters in, string out, side effects allowed. The author's existing workflow was already one markdown file per prompt, so the file and the function are the same thing.
  - A prompt with zero Lua still runs exactly like a plain Cursor/Claude Code orchestration (the whole file passed to the model). Lua is additive - reached for only when plain prose is not enough.
  - The language grows inside the prompt, never around it.
  - When work outgrows one file, split it into more prompt files (separate functions) rather than growing the format. A prompt has a natural size limit as a linear pipeline.
  - What breaks without it: requiring anything beyond the one file (a companion Rust file, extra structure) breaks self-containment, which the author called "the whole point."
- Rejected alternative: starting with an interpreted host language (Python, Go) and bolting prompts onto it; every prompt backed by its own Rust code. Stated cost: kills self-containment; other frameworks start with the host language, but the author owns a body of markdown prompts and wants programming added into them, never the other way around.
- Concrete incidents:
  - A proposed tool design implied Rust code backing every prompt; the author objected that this kills self-containment.
  - Author-verbatim: "the whole point of this was that it was self-contained." [mcp-client-large-part2 p86]
- Merge/derivation notes: merged from two grouped-draft records - "A prompt is a single markdown file that is one function..." (rejected-alternative: none; endorsement: n/a) and "The design starts from the prompt and adds structured programming into it..." (source: user-stated; user-corrective). Both rest on the same self-containment motive and the same [p86] citation.

## Principle 9

- Rule: Parse the whole document once, up front, and compile all Lua at parse time.
- Purpose facts:
  - Reading a prompt file never runs anything inside it: a parsed prompt is inert data that can be constructed, inspected, and enumerated on a server surface without executing prompt code.
  - A syntax error at run time is impossible (or nearly so): a successful parse means the prompt is fully syntax-validated.
  - No markdown parsing happens at run time.
- Rejected alternative: compiling markdown to an intermediate representation before execution (the Playbooks lesson); parsing markdown lazily at run time. Stated cost: a compilation step between the prompt author and the model breaks the rule that the raw markdown is the program; lazy runtime parsing makes runtime syntax errors possible.
- Concrete incidents:
  - Prior art: Playbooks compiled prompts to an intermediate representation. Recorded lesson, author-verbatim: "do not put a compilation step between the prompt author and the model; the raw markdown is the program."
  - The author rejected runtime markdown parsing inside fanout helpers for exactly the runtime-syntax-error reason.
- Merge/derivation notes: single grouped-draft record ("No compilation step sits between the prompt author and the model..."). Source: ai-proposed; user-stated. Endorsement: corrected (one ai-proposed leg); unaddressed (other ai-proposed leg). No merge.

## Principle 10

- Rule: Keep one fixed skeleton: an H1 holding the preamble and epilogue, then H2 sections, and within a section the lua fence before the prose.
- Purpose facts:
  - The fence comes first because the Lua picks the tools, and the prose runs with those tools; a fence after the prose would run too late to matter.
  - Position, not content, tells reader and parser which fence is which: a preamble can never be confused with an epilogue.
  - The H1 is required; anything between the YAML front matter and the H1 is a free scratch zone, ignored.
- Rejected alternative: a trailing lua code fence after the section body; meaningful content between front matter and H1. Stated cost: a trailing fence runs too late to matter (tools must be picked before the prose runs), and position-dependent fence identity reintroduces ambiguity.
- Concrete incidents:
  - The author caught the parser missing the trailing epilog fence and dictated the section shape by example: lua fence, prose, lua fence.
  - Author-verbatim, on requiring lua before prose in the H1: "just for consistency so that you don't confuse the preamble with an epilogue."
- Merge/derivation notes: single grouped-draft record ("A prompt file is an H1 section containing a lua preamble fence..."). Source: user-stated. Endorsement: n/a. No merge. Related to the heading-identifier record (both fix the document grammar) but motives differ: this one is positional disambiguation of fences, that one is machine-addressable names.

## Principle 11

- Rule: Headings are machine addresses: a subhead's first word is a valid identifier, unique within its scope, the rest of the line an ignored comment; XML is reserved for the model.
- Purpose facts:
  - Section headings are jump/execute targets, so the name part must be a valid identifier and unique within its scope (H2s across the file, H3s within their parent) or control-flow calls cannot resolve unambiguously.
  - First word is the identifier (lowercase-normalized); everything after whitespace on the heading line is an ignored comment, so one heading serves as both machine address and human-readable title.
  - The H1 is excluded: it is the prompt itself, not a callable section.
  - Headings are the document's only grouping mechanism; no heading level is special.
  - XML is model-facing markup: models are trained on it and spot it easily. The harness extracts XML blocks into a table; nothing inside XML tags counts as prompt text, so reusable material (e.g. shared rule lists) stays available as data without counting as prompt text.
- Rejected alternative: XML tags as the harness's grouping and batching system; restricting references to one designated heading level. Stated cost: the harness already has headings for grouping, and consuming XML would take it away from the model that is trained to spot it. (Identifier record: rejected-alternative none.)
- Concrete incidents:
  - Author-verbatim: "We want to leave the XML for the model to be able to spot. We don't want to use the XML as a grouping system for the harness."
  - Worked example of the dual-purpose heading, author-verbatim: "### Summarize-Research map reduce to get report".
- Merge/derivation notes: merged from two grouped-draft records - "H2 is a subhead and H1 is not; every subhead's first word must be a valid identifier..." (source: user-stated) and "XML blocks may appear anywhere in the document..." (source: user-stated; user-corrective). Both endorsements n/a.

## Principle 12

- Rule: Sections nest recursively from H2 through H6; every level runs under identical rules, and moving between levels is always explicit.
- Purpose facts:
  - Subroutines and fanout arms need to live inside their parent section.
  - Fall-through, "---", jump(), and execute() work the same way at each level, scoped to that level's siblings and its children one level down.
  - A section's children are subroutines and fanout material, not steps, so the default walk must never silently descend into them; once a jump or execute lands at the deeper level, the ordinary sibling walk takes over.
  - What breaks without it: running a parent section would execute its arm templates and subroutines as if they were pipeline steps; without recursion, shared subroutines and fanout templates would have to be top-level sections, polluting the flat walk.
  - Identical rules at every level means one mental model covers the whole document, and the implementation collapses because the special cases are gone.
- Rejected alternative: per-level execution semantics; implicit fall-through from a parent level into its children. Stated cost: per-level semantics multiply special cases; implicit descent runs subroutines and fanout templates as pipeline steps.
- Concrete incidents:
  - Author-verbatim: "H3 as well of course.. fully recursive to H6"
  - Author-verbatim: "identical rules. different level."
  - Author-verbatim, on the implementation payoff: "this should result in a simplification because we've eliminated the special cases."
  - Author-verbatim: "H2 never falls through to H3. The transfer from HN to H(N+1) must be explicit."
- Merge/derivation notes: merged from two grouped-draft records - "Prompt documents support nested sections recursively from H2 through H6..." and "Fall-through never crosses heading levels..." (both user-stated, endorsements n/a). Same conversation, same decision, two halves of one rule: uniform recursive rules plus explicit level transfer.

## Principle 13

- Rule: A horizontal rule marks a section as skipped by execution, and content after it is prose for the human reader.
- Purpose facts:
  - A prompt has two audiences: the model that executes it and the human who maintains it. Without an opt-out, every word in the file is an instruction to the model.
  - Reusable subroutine sections can sit in the file without the default sequential walk running them.
  - The rule means the same thing wherever it appears, so sections survive being cut and pasted; it applies uniformly with no special casing (the blank line is required), even to a section reached through a chain.
- Rejected alternative: special-cased parsing of horizontal-rule placement; positional control-flow markers whose meaning depends on where they sit in the file. Stated cost: position-dependent meaning breaks when the user cuts and pastes sections around.
- Concrete incidents:
  - The author rejected the first design (one "---" below which nothing executes) because its meaning depends on position.
  - Author-verbatim: "My new version survives the user cutting and pasting sections around."
  - Author-verbatim, refusing special casing: "No, the blank line is required. I dont want any special casing"
- Merge/derivation notes: single grouped-draft record ("A horizontal rule '---' marks a section to be skipped by execution..."). Source: user-corrective. Endorsement: n/a. No merge.

---

## Stanza facts - Section II "The Document"

- What the section covers: what a prompt file is and how it is shaped - self-containment, parse-once compilation, the fixed H1/H2 skeleton, headings as addresses, recursive nesting with explicit level transfer, and the horizontal-rule opt-out.
- Why the layer exists: the document is the program; its shape is the control flow, so the shape has to be fixed and legible.
- Failure modes it prevents:
  - Self-containment broken by companion code files (principle 8).
  - Runtime syntax errors and prompts that execute on read (principle 9).
  - Preamble/epilogue confusion and fences that run too late (principle 10).
  - Ambiguous jump targets and harness markup colliding with model-facing markup (principle 11).
  - Subroutines and fanout templates executed as pipeline steps; per-level special cases (principle 12).
  - Every word in the file forced to be an instruction to the model; position-dependent meaning that breaks under cut and paste (principle 13).
- Unifying principle, one sentence: the author reads execution order directly off the page.

# Packet Section 3 - Control Flow and Context (Principles 14-18)

Facts only. Sources: purpose-cluster-3.md (Records 1-6), grouped-draft.md "Control flow" YAML block.

## Principle 14: Every section transition clears context

**Rule:** Every section transition clears context; fall-through is the default and jump() is the explicit form.

**Purpose facts:**
- Lets the author write a simple linear pipeline with no explicit transitions: "you just fall off the end of your section and you go to the next one, and then you don't have to name the next section."
- A three-step prompt that processes a file needs no explicit transitions; running off the last section ends the run with a well-defined message (default completion message, overridable in YAML front matter).
- Context-clearing exists because accumulated context is the enemy: "I do NOT want sequential fall-through to accumulate context." Clearing on every transition keeps contexts small so smaller, cheaper models stay reliable.
- Fall-through lives in the executor, not Lua: "the default control flow, falling through, doesn't happen in Lua and making it happen there would be clumsy."
- jump() throws out the current context and starts fresh from the target section, which "eliminates context bloat" and lets each step run in a small window.
- The value carried across a jump must be visible in the prompt source: "we said we're gonna make it visible so that if you can actually read the code."
- The model's previous reply always rides along in the single variable `reply`; the invariant is "when you enter a section, the model's previous reply is always in the reply variable."
- jump carries only the passed string, the params, and store access.
- Renamed from goto to jump because goto is a reserved word in Lua.
- Without it: context that accumulates across sections bloats the window; accumulation is what forces big models and compaction.

**Rejected alternatives and stated costs:**
- Requiring an explicit exit or transition from every section.
- Implementing fall-through inside the Lua block - rejected as "clumsy."
- Fall-through that appends each section into a growing shared context - rejected because accumulation bloats the window and forces big models and compaction.
- Compacting the transcript to make room in a continuing context (for jump).
- jump() dropping the reply.
- Three separate variables incoming_reply, reply, and last_reply - rejected in favor of the single variable reply.
- Endorsement: n/a (both constituent records).

**Concrete incidents:**
- The author hit the case where Lua wanted to jump based on an inference result and had no way to pass that reply along; this broke his invariant that the model's previous reply is always in `reply` on section entry. This incident also appears under principle 2 as the motivating case for uniform constraints.

**Merge/derivation notes:**
- Merged from purpose-cluster-3 Record 1 (fall-through, default advance, termination) and Record 2 (jump, explicit transfer, reply rule). Both records state the same root rule: every section transition starts a fresh context, because accumulation is what forces big models and compaction. Record 1 is the default form; Record 2 is the explicit form.
- Record 1 citations: 2026-07-28-2238-orchestrator-design-continued.md [p75], [p121]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p75], [p121]; 2026-08-02-1134-mcp-client-large-part5.md [p363], [p414], [p415]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10].
- Record 2 citations: 2026-07-28-0925-orchestrator-design-document.md [p14], [p74], [p75]; 2026-07-28-2238-orchestrator-design-continued.md [p14], [p75], [p120]; 2026-07-30-0534-promptforge-design-context.md [p12]-[p18]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20], [p21], [p22]; 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481].

## Principle 15: execute() runs a section as a subroutine; jump() transfers without returning

**Rule:** execute() runs a section as a subroutine - a fresh VM, the chain runs to its end, and the reply comes back to the caller - while jump() transfers control with no return.

**Purpose facts:**
- Lets the author reuse a section from more than one call site; a goto-with-return cannot be reused: "'return goto(...)' can't be a reusable function called from more than one place, because control always transfers to the same place after the Research is done."
- Lets one section get two tool loops: a section can only have one tool loop (its last prose block), so "if we really want two loops in one section, we can have the Lua... execute, and it can mention two different H2s... that's like a subroutine."
- Reuses the existing section-execution code deliberately: "We already have to execute sections, so why not make it a function that Lua can call?"
- Refined so execute starts a new chain that runs to its end and returns its reply, recursively: "it's like calling a different prompt whose pieces just happen to be in the same file."
- Return versus transfer is the author's choice; one section-execution machinery serves both.

**Rejected alternatives and stated costs:**
- An asymmetric model where an execute-entered subroutine may not jump.
- Treating goto-with-return as a reusable multi-call-site function - rejected because control would always return to the same place, so it cannot be reused.
- Endorsement: n/a.

**Concrete incidents:**
- The two stated gaps are themselves the incidents: the unreusable return-goto, and the one-tool-loop-per-section limit forcing the subroutine form.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 3); no merge. Distinct purpose from jump: subroutine with return vs transfer without return.
- Citations: 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]; 2026-08-09-1058-promptforge-core-large-part5.md [p430], [p432], [p433]; 2026-08-19-0048-promptforge-md-aug19.md [p55], [p58], [p60]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p242].

## Principle 16: A section ends when the model replies with text and no tool calls

**Rule:** A section ends when the model replies with text and no tool calls; tool calls made during the loop count as output; an empty final turn is a clean exit only when finish_reason is "stop" and a tool call succeeded earlier in the loop, and every other empty turn fails closed as EmptyModelReply.

**Purpose facts:**
- Token economy: a model that finished its work through tool calls should not have to "waste output tokens with the word 'done'"; tool calls already count as output.
- The empty-turn clean exit binds reply to the empty string.
- Every other empty turn fails closed, because silently accepting empty turns is how a run passes while producing nothing.

**Rejected alternatives and stated costs:**
- An explicit termination call required to end a section.
- Requiring a non-empty text reply to validate a turn.
- Accepting any empty turn once a tool call has occurred - rejected because silently accepting empties is how runs pass while producing nothing.
- Endorsement: affirmed.

**Concrete incidents:**
- A real papergate run failed: the prompt said "Do not output any text," the model recorded everything via tool calls and legally exited with empty content, and the engine hard-failed it as EmptyModelReply.
- The briefer's empty evidence.md: a run passed while producing nothing, the failure mode the fail-closed rule exists to prevent.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 4); no merge. Source tagged ai-proposed; user-stated.
- Open question 6 in the principles file notes the tension: "An empty model response is never acceptable" versus the conditional empty-turn clean exit; the later rule refines the earlier one, but the exact boundary of which empty turns fail closed deserves confirmation.
- Citations: 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p3], [p6], [plans section]; 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions]; 2026-08-09-1058-promptforge-core-large-part5.md [p429]; grouped-draft also lists 2026-08-03-1827-two-repo-commit-review.md [design documents section].

## Principle 17: Cycles are allowed

**Rule:** Cyclic section calls are permitted; runaway execution is bounded by budgets (nesting limit, step budget, tool budget), not by structural prohibition.

**Purpose facts:**
- Some tools require cycles: "There are obviously tools which require cycles."
- The engine cannot predict how authors will organize their files: "we can't predict all the organizations, and we know that we can have cycles."
- Runaway execution is a resource problem, not a structure problem, so it is bounded by "nesting limit, step budget, tool budget" instead of prohibition.
- Once the language has subroutines, jump, and goto, "the same problems of any other computer programming language apply... with that power comes the responsibility" - coherence belongs to the prompt author, not the engine.

**Rejected alternatives and stated costs:**
- Restricting calls to an acyclic graph (the proposed restriction was: H3 can only call H3 and down, acyclic call graph) - rejected because some tools require cycles.
- Engine-enforced guardrails on control flow.
- Endorsement: n/a.

**Concrete incidents:**
- No specific debugging incident recorded; the rejected acyclic-graph proposal is the originating event.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 5); no merge. Source tagged user-corrective; user-stated.
- Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [p369]-[p372]; 2026-08-02-1134-mcp-client-large-part5.md [p369], [p371], [p372]; 2026-08-19-0048-promptforge-md-aug19.md [p60]; 2026-07-28-0925-orchestrator-design-document.md [p18]; 2026-07-30-0534-promptforge-design-context.md [p4].

## Principle 18: A task is either synchronous or asynchronous

**Rule:** A synchronous task is a function call with a context reset; an asynchronous task returns a unique timestamped id immediately, needs a rendezvous to collect, can be cancelled by the model when stuck, and is cancelled with a message if its section moves on; a fork lets the caller fall through while the task runs, and forks are not required to rejoin.

**Purpose facts:**
- The driving case was a long-running research task: "this is how you have a 'research task' going nonstop, while the main context is getting bugfixes and speedups."
- The unique timestamped ID returned at launch exists for one reason: "we have to give the harness the ability to cancel... we need to let the model cancel the task, like, if it's stuck."
- Cancellation on section exit exists because the author asked what happens "if the main section tries to move on or tries to return" with a pending task - the pending task must be cancelled and the section told.
- Forks are not required to rejoin because the author could "see forking a section that calls itself over and over again until some condition is met... and then it never comes back."

**Rejected alternatives and stated costs:**
- Requiring forks to always come together.
- Endorsement: n/a.

**Concrete incidents:**
- The research-task-running-nonstop scenario is the case that forced the design; no separate debugging incident recorded.

**Merge/derivation notes:**
- Single record (purpose-cluster-3 Record 6); no merge.
- Citations: 2026-07-30-0534-promptforge-design-context.md [p22], [p23], [p25], [p26], [p27], [p28], [p34], [p35]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]; 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247].

## Stanza facts (Section III header)

- What the section covers: how execution moves between sections and what happens to the context when it does.
- Why the layer exists: accumulated context is the enemy; small contexts are what let small, cheap models stay reliable.
- Failure modes it prevents: context bloat across sections (which forces big models and compaction); unreusable control transfer; wasted tokens on filler text like "done"; runs that pass while producing nothing (empty evidence.md); runaway execution treated as a structure problem instead of a resource problem; async tasks left dangling when a section moves on.
- Unifying principle, one sentence: every transition starts fresh, and anything that crosses does so visibly.

# Packet Section IV - Lua and State (principles 19-27)

Facts only. No prose.

## Principle 19 - Keep embedded Lua minimal and sandboxed

- Rule: Keep embedded Lua minimal and sandboxed: a fixed set of host objects, a restricted standard library, an instruction-count hook that kills a runaway block.
- Purpose facts:
  - Too much logic in the Lua re-implements the orchestrator inside the markdown, which defeats the point of the system.
  - The sandbox exists because prompts are runnable artifacts with a fixed host surface.
  - A runaway Lua block (infinite loop) must not hang the run; the instruction-count hook aborts it.
  - Access control applies to the model, not to Lua: the author's own Lua can read and write real and memory files, because the author's code is trusted and the model's tool calls are not. Per-section tool injection is what restricts the model.
- Rejected alternatives and stated costs:
  - An orchestrator written in Lua embedded in the markdown file - defeats the purpose of the system.
  - Arbitrary user-declared globals.
  - Protecting the machine by restricting the Lua API instead of the prompt's tools - this was the team's actual confusion; they had conflated the model's file tools with the author's Lua API and sandboxed Lua away from files.
  - Sandboxing Lua so it cannot write files.
- Concrete incidents / verbatim:
  - "if we start putting too much into the Lua, then it kinda defeats the purpose"
  - The file-access leg is a recorded correction: the team had confused the model's file tools with the author's Lua API.
- Endorsement: unaddressed (ai-proposed leg).
- Merge/derivation: stands alone (purpose-cluster record 1; grouped-draft "Lua environment" record 1).

## Principle 20 - Move structured data through code, never through the model's prose

- Rule: Move structured data through code, never through the model's prose.
- Purpose facts:
  - Parameters are read-only and visible to every section and any Lua anywhere, so a shared input (e.g. a file path) never gets passed from section to section by hand.
  - Substitution makes prompt assembly deterministic: the Lua assembles the value, the executor splices it in, the model never paraphrases it. Substitution is single-pass; scalars render as strings, tables as JSON; a missing key is a hard error.
  - State comes out of the model as flat tool calls into the store because tool calls are reliable on the small open-weight models this system targets and structured-output conformance is not. Persistence becomes a side effect of tool calls.
  - Propagating state is a single tool call carrying all values at once, not one call per value.
- Rejected alternatives and stated costs:
  - Pydantic-style schema conformance with injected system-prompt overhead - expensive, and conformance is unreliable on small open-weight models.
  - Model-conformant JSON produced under constrained decoding.
  - One set call per value - "you end up making 2 tool calls instead of 1."
- Concrete incidents / verbatim:
  - The author called the JSON-via-macro-substitution arrangement "pydantic with perfect return and no overhead": structured return values without the conformance burden or injected system-prompt cost of Pydantic.
  - This was the founding substitution for Pydantic in the orchestrator design.
- Endorsement: affirmed (ai-proposed leg) on the substitution record; n/a on the flat-tool-call record.
- Merge/derivation: merges purpose-cluster records 2 (parameters and substitution) and 8 (flat tool calls into the store). Record 8 shares the store with record 9 but is a different pain: reliable state extraction from the model, not debugging/resume.

## Principle 21 - Live-once preamble plus pure replayable shared library

- Rule: The H1 preamble runs exactly once, live, and can infer and call tools; the shared library is a separate "```lua shared" chunk, compiled once and replayed as bytecode into each section's fresh VM.
- Purpose facts:
  - The preamble needs inference and tool calls so the model can parse the argument string and take control before any section runs.
  - Replaying a live preamble into every section VM would multiply inference cost and corrupt store state.
  - Sections still need the author's helper functions; generic VM serialization/cloning was rejected as fragile, so the shared chunk is pure code.
  - Compiling the shared chunk once surfaces syntax errors before anything runs.
  - The replay gate blocks tools, models, var, reply, and jump at the shared top level (a hard phase error naming the blocked global) while leaving them available inside shared functions called later; a shared chunk calling tools.add at top level would bind at the wrong time.
  - A second shared chunk, or one after the H1, is an error.
  - An empty compiled chunk is substituted when no shared section exists, so the section-startup code path is unconditional instead of branching on whether the author wrote a shared chunk.
  - Captured bindings install after the replay, so a tool or model alias wins a name collision with a shared global.
  - A scalar top-level return from preamble or epilog ends the run; nil continues sequential fall-through.
- Rejected alternatives and stated costs:
  - Two-phase preamble treatment and shared-bytecode re-execution in section VMs.
  - Replaying with the full environment and tightening later - leaves footguns (bindings at the wrong time).
  - Branching section-startup logic on whether a shared section was specified.
  - Generic VM serialization and cloning - fragile.
- Concrete incidents / verbatim:
  - "not having shared functions is a disaster"; replaying a live preamble is a different disaster. The split avoids both.
- Endorsement: affirmed (ai-proposed leg) on both records.
- Merge/derivation: merges purpose-cluster records 3 (shared chunk) and 4 (live-once preamble) into one principle; two grouped-draft records ("Lua environment" records 3 and 4).

## Principle 22 - One VM per section; the store is the only cross-section mutable channel

- Rule: All Lua chunks in one section share a single VM, installed once at entry and then left alone; an error in any chunk stops the whole run; across sections and fanout arms there is no shared mutable Lua state - the store is the only mutable channel.
- Purpose facts:
  - One chunk can stash a table and a later chunk can read it - plain globals, the way Lua is supposed to work.
  - Installing the environment once and leaving it alone removes a whole class of scope open/close machinery.
  - The tool schema is computed fresh just before each prose call.
  - An error in any chunk stops the run because continuing past a failed chunk leaves the section in a state the author never wrote.
  - Lua chunks return values with Lua's native return semantics.
  - Sections and fanout arms run concurrently, so mutable run-global Lua is excluded; functions, closures, globals, var, tools, and reply are branch-local by construction.
  - After the H1 preamble runs, the prompt-global Lua state becomes read-only; each fanout arm receives its own copy of shared functions.
- Rejected alternatives and stated costs:
  - Per-chunk environments with closures re-installed between blocks - this was the actual engine behavior the author discovered and it broke the stash-a-table pattern.
  - A tool loop that mutates the environment between blocks.
  - Continuing the run past a chunk error - leaves the section in a state the author never wrote.
  - A declared identifier or descriptor inspected by the Rust side.
  - Mutable run-global Lua state; shared mutable global state across fanout arms - arms run concurrently.
- Concrete incidents / verbatim:
  - The author discovered the engine was re-installing closures and mutating the environment between Lua chunks of the same section, breaking the natural pattern of one chunk stashing a table and a later chunk reading it.
  - "they're all just globals to the VM"
  - The removed scope open/close machinery was called "tryhard."
- Endorsement: corrected (one leg affirmed).
- Merge/derivation: stands alone (purpose-cluster record 5; grouped-draft "Lua environment" record 5).

## Principle 23 - Tools and models are first-class Lua values

- Rule: Tools and models are first-class Lua values: inspectable, invocable tables.
- Purpose facts:
  - Testability: with a Tool or Model as an inspectable, invocable table, a unit test can substitute a mock - put in the mock and test the section - which opaque registrations do not allow.
  - The preamble can declare globals such as a list of tools that any section can pass to tools.need, which only works if a tool is a value.
  - A model exposes infer()/turn().
  - The toolset is never sealed at the first inference, so tools.add between inference rounds within a section keeps working.
- Rejected alternatives and stated costs:
  - Treating tools and models as opaque registrations - blocks mock substitution in unit tests.
  - Sealing the toolset when infer begins - breaks the working pattern of adding search, running one inference, then adding fetch.
- Concrete incidents / verbatim:
  - "we can put in the mock, and we can test it"
  - The unsealed-toolset leg exists because the add-search, infer, add-fetch pattern is a working pattern.
- Endorsement: n/a.
- Merge/derivation: stands alone (purpose-cluster record 6; grouped-draft "Lua environment" record 6).

## Principle 24 - infer() is a blocking one-shot

- Rule: infer() is a blocking one-shot: a string goes in, a string comes out, no tools, no history, no side effects, using the model already selected for the section.
- Purpose facts:
  - infer exists for a quick one-shot inference inline inside a calculation, when prose would be overkill.
  - No two ways to do the same thing: if infer had tools and conversation history it would just be prose again, and the language would inherit every prose question twice (how do you set the tools, what happens on jump).
  - Uses the model already selected for the H2; the two-argument form that picked a model per call was dropped.
- Rejected alternatives and stated costs:
  - infer with tools and history - just prose again, with all the same questions.
  - A two-argument infer that picks a model per call.
- Concrete incidents / verbatim:
  - "if you want Prose, use Prose."
- Endorsement: n/a.
- Merge/derivation: stands alone (purpose-cluster record 7; grouped-draft "Lua environment" record 7).

## Principle 25 - The store is a virtual filesystem for file-shaped intermediate values

- Rule: The store is a virtual filesystem for file-shaped intermediate values in analytical pipelines, for debugging and resume; real files and memory files are readable side by side.
- Purpose facts:
  - Building an analytical pipeline requires re-running the prompt from any step during development and inspecting what each step produced after the run, so every intermediate output is a file that can be read back and skipped via store.exists.
  - It is not a general-purpose filesystem for agentic coding: string replacement and delta application are a different, future class.
  - It is not literally the filesystem, because then run artifacts like evidence.md would show up as useless stray files in the user's directory.
  - Real and virtual files must be readable at the same time because a prompt needs its author-supplied input files alongside its run-produced memory files.
- Rejected alternatives and stated costs:
  - A general-purpose filesystem supporting string replacement and delta application.
  - A store model that supports only one kind of file at a time.
  - A store that is literally the file system - run artifacts surface as stray user-visible files.
- Concrete incidents / verbatim:
  - The named stray-file hazard: intermediate artifacts like evidence.md showing up in the user's directory.
- Endorsement: n/a.
- Merge/derivation: stands alone (purpose-cluster record 9; grouped-draft "State and context" record 2). Related to record 8 (same store) but a different pain: debugging and resume, not reliable state extraction.

## Principle 26 - The engine pushes context in; the model never pulls

- Rule: The engine pushes context in; the model never pulls. On every jump the Lua-written facts bag is injected fresh; on a tool call in a multi-turn context the bag comes out, the tool results go in, and the bag goes back.
- Purpose facts:
  - A jump clears the context, so the facts the next section needs have to be injected fresh on every transfer; the Lua writes the block, the executor picks the enclosing tag.
  - On multi-turn horizons the facts bag must not become permanent transcript residue: on a tool call it is removed, the tool results go in, and the bag is added back.
  - Small models have small windows and accumulated residue crowds them out.
  - The push direction is deliberate: the prompt's Lua declares what the model needs and the engine injects it, rather than the model pulling context items itself.
- Rejected alternatives and stated costs:
  - Leaving the facts bag permanently in the transcript.
  - Accumulating permanent entries in the context - residue crowds out small models' windows.
  - The model requesting context items itself.
- Concrete incidents / verbatim:
  - "I don't want to start accumulating permanent crap in the context"
- Endorsement: n/a.
- Merge/derivation: stands alone (purpose-cluster record 10; grouped-draft "State and context" record 3).

## Principle 27 - Environment facts live in one table, sys

- Rule: Environment facts live in one table, sys: launch time, current time, a unique id per context, and the effective model once the section's model scope closes; reading an unknown name is a hard error.
- Purpose facts:
  - Prompts need facts only the engine knows: launch time as a fixed constant (sys.when), current time (sys.now) so a model can detect time passing and compute elapsed time, and a unique incrementing id per context so Lua can compute unique filenames in the store.
  - sys.model exists because the author wanted to print the producing model at the bottom of a generated report; it is usable in prose substitution and in Lua.
  - sys.model is unavailable during the prologue because no model is bound until the section's model scope closes.
  - Unknown sys names fail loud because a silent empty value would hide a typo'd field name - an empty value means the prompt silently prints nothing, and the error tells you what you typed wrong.
- Rejected alternatives and stated costs:
  - Silently returning nil for unknown sys fields - hides a typo'd field name from the prompt author.
  - Putting model in the initial pre-preamble sys object - no model is bound that early.
- Concrete incidents / verbatim:
  - The motivating use for sys.model: printing the producing model at the bottom of a generated report.
- Endorsement: n/a.
- Merge/derivation: stands alone (purpose-cluster record 11; grouped-draft "State and context" record 4). Shares the fail-loud-on-unknown-name posture with other records but the purpose (engine-known facts) is its own.

## Stanza facts - Section IV "Lua and State"

- What the section covers: the embedded Lua and how data moves - the sandbox and its limits, parameters and substitution, the preamble/shared-chunk split, per-section VM lifetime, tools and models as values, infer(), the store, context injection, and system facts.
- Why the layer exists: everything deterministic should happen in code, not in the model; inference is the expensive, unreliable part, so the language routes around it wherever plain code suffices.
- Failure modes it prevents:
  - The orchestrator re-implemented in Lua inside the markdown (19).
  - The model paraphrasing or failing to conform structured output (20).
  - Multiplied inference cost and corrupted store state from replaying a live preamble; missing shared helper functions (21).
  - Broken cross-chunk state from per-chunk environments; runs continuing past failed chunks into unwritten states; shared mutable state across concurrent fanout arms (22).
  - Unmockable, opaque tool/model registrations; toolsets sealed too early (23).
  - A second prose mechanism with all prose's questions asked twice (24).
  - Uninspectable, non-resumable pipelines; run artifacts polluting the user's directory (25).
  - Permanent context residue crowding out small models' windows (26).
  - Silent empty values hiding typo'd field names (27).
- Unifying principle (one sentence): Lua assembles, the model never paraphrases.

# Section V: Tools and Models - Fact Sheet

## Principle 28: Scope tools per section, opt-in

**Rule:** A section receives only the tools its Lua names with tools.add(); a section that names no tools gets none.

**Purpose facts:**
- Small orchestrator models (7B-14B) get confused by a large offered tool list; the author's budget is roughly five to seven tools per section.
- Opt-in scoping means a section can never hold a tool it did not ask for (isolation).
- A 20-tool prompt no longer injects 20 schemas into every section.
- Constraining a section's toolset must not otherwise change the section's behavior.
- History is never rewritten to scrub tool offerings, because the model would see information appearing out of nowhere.
- Tool availability can be scoped by turn within a section (e.g. only web_search on the first turn).
- A section that always falls through gets no control-flow tool injected at all.

**Rejected alternatives and stated costs:**
- Opt-out scoping where a section starts with all frontmatter tools (loses isolation; a section could hold a tool it never asked for).
- A constrained-toolset formulation that alters section behavior (author: "I want the behavior to be the same as the traditional way, except that the toolset is constrained").
- Scrubbing the tool offering and tool call from history ("the model would see information appearing out of nowhere").
- Making all of a section's tools available on every turn.

**Concrete incidents / author-verbatim phrases:**
- "keeps the tool list small so the model doesn't get confused" (2026-07-28-2238-orchestrator-design-continued.md p17)
- "each subhead only needs a few of them" (p85); tool count 5-7 for small orchestrator models (p119)
- Opt-in chosen "for isolation - a section can never hold a tool it did not ask for" (2026-07-30-1046-compaction-algorithm-large-part5.md plans)
- Restricting call kinds "reduces pressure because the model doesnt have to pick" (2026-07-30-1046-compaction-algorithm-large-part3.md p222)
- Only web_search on the first turn: "this locks the model to calling just one tool" (2026-08-09-1058-promptforge-core-large-part4.md p372)

**Merge/derivation notes:**
- Grouped-draft record (line 460) merged from ai-proposed (affirmed), user-stated, and user-corrective sources across 7 chat units; endorsement: affirmed.
- Purpose pass kept this record separate from the single-tools.add record (Record 2): this one is small-model context pressure and isolation; Record 2 is loud failure and a single entry point. The design doc preserves that split as principles 28 and 29.

## Principle 29: Exactly one tools.add; unknown or unscoped tool names are hard errors

**Rule:** There is exactly one tools.add, and naming an unknown or unscoped tool is a hard error with clear diagnostics.

**Purpose facts:**
- A tool binding that fails silently is a debugging trap; unknown or unscoped tool names must be hard errors, never silently dropped.
- One version of tools.add, no overloaded variants - consistent with "do more with less."
- Tool references are scoped, not globally "registered"; naming an unscoped yet global tool hard-errors.
- A tool's call budget is declared at the tools.add call site.
- Turn limits belong to the subagent as a whole (config.max_turns), not to any single tool; when the budget is exhausted all of the subagent's tools are removed.

**Rejected alternatives and stated costs:**
- Multiple overloaded versions of tools.add (violates the author's gut rule and "do more with less").
- Silently ignoring unknown aliases (the debugging trap that motivated the rule).
- A global tool registry where any name resolves ("'registered' is wrong - it has to be scoped").
- Attaching max_turns to individual tools ("max_turns is not really on the tools its on the subagent itself").

**Concrete incidents / author-verbatim phrases:**
- The author hit tool-binding failures that did not fail hard and could not tell why nothing worked: a tools.add failure case that "is not failing hard" (2026-08-14-1613-promptforge-core-largest-part2.md p89).
- "my gut tells me there should only be one version of tools.add" (p90)
- "we need to bake the limit into the tools.add call" (p170)
- "this means we take ALL the tools away on exhaustion" (p176)
- "unknown aliases are hard errors with clear diagnostics" (2026-08-09-1058-promptforge-core-large-part4.md p271)
- "naming an unscoped yet global tool should hard-error" (p273)

**Merge/derivation notes:**
- Grouped-draft record (line 467) from user-stated and user-corrective sources across 3 chat units; endorsement: n/a.
- Purpose pass Record 2; merge suggestion: none (kept separate from Record 1 as noted above).

## Principle 30: Assert tool usage in the epilogue

**Rule:** A prompt can assert in its epilogue that a tool was actually called - assert(tools.calls["search"] > 0).

**Purpose facts:**
- Runs were coming back empty or wrong because the model never performed the required web search.
- The count is per-VM.
- A failed tool call still counts: the assertion measures whether the model is performing, not whether the tool is performing.

**Rejected alternatives and stated costs:**
- A dedicated require_called directive - rejected because "it violates the design principle of do more with less"; an ordinary Lua assert over a call count says the same thing with existing machinery.
- Counting only successful tool calls (wrong target: the assertion measures the model, not the tool).

**Concrete incidents / author-verbatim phrases:**
- "The prompt needs to have a way to say that a tool has to be called" (2026-08-09-1058-promptforge-core-large-part4.md p265)
- "if it doesn't perform at least one web search, that's a problem" (purpose pass Record 3)
- "no to require_called, it violates the design principle of do more with less" (p267)
- "failed tool call counts as a call, we are measuring if the model is performing not if the tool is performing" (p271)

**Merge/derivation notes:**
- Grouped-draft record (line 474) from user-stated and user-corrective sources; the same discussion was captured twice (2026-08-09 part4 and 2026-08-14 part3, duplicate capture) and consolidated; endorsement: n/a.
- Purpose pass Record 3; merge suggestion: none.

## Principle 31: A tool can be plain Lua

**Rule:** A tool can be an inline Lua function, registered from any chunk in the section, effective for the next prose call, with its schema derived from the function declaration.

**Purpose facts:**
- Some tools are trivial - the author's example is setting a variable - and writing a Rust function for each is unjustified.
- A Lua tool has the same capabilities as a native Rust tool, including enabling further tools at call time (e.g. a search front end that does a tools.add for fetch when called); the author's own opt-in legitimizes this.
- The schema is derived from the function declaration because "we can't do no schema."
- A Lua tool handler cannot jump: a jump from inside a tool handler has no section walk to transfer into. Ordinary section Lua still can jump.

**Rejected alternatives and stated costs:**
- Requiring a Rust function for every tool (unjustified for trivial tools like setting a variable).
- Schema-less local tools presenting only name and description ("We can't, we can't do no schema. We have to pick the parameter types out of the function declaration").
- Allowing jump() from tool handlers (makes no sense - no section walk to transfer into).

**Concrete incidents / author-verbatim phrases:**
- "we don't wanna have to write a Rust function just for setting a variable... a front end to the real search tool... when the tool is called, it does a tools.add for fetch" (2026-08-09-1058-promptforge-core-large-part4.md p373)
- "the user is opting in to the behavior, so that makes it ok" (p374)
- "invocable from any lua chunk in an H2 and it should just add the tool for the next prose call" (2026-08-18-1126-promptforge-md-aug18-morning.md p144)
- "a Lua tool should have all the same capabilities as a regular tool, a native Rust tool" (p160)
- "Lua needs to jump local tool handlers cannot" (p162-163)

**Merge/derivation notes:**
- Grouped-draft record (line 481) from user-stated and user-corrective sources across 3 chat units; endorsement: n/a.
- Purpose pass Record 4; merge suggestion: none.

## Principle 32: The prompt owns model choice

**Rule:** Models are declared in the introduction with their attributes; a section selects its model exactly once in its first Lua block, inheriting the prompt-wide default or overriding it, and the choice locks for the rest of the section.

**Purpose facts:**
- The prompt owns model choice and execution parameters because the prompt is the thing that knows what it needs.
- Any inference before a selection is an error - a decision nobody made.
- Switching models means starting a new section and carrying context forward through reply, because switching mid-section can jump to a different provider and silently invalidate the KV cache, which is invisible to the programmer.
- A subsection inherits its parent section's model unless it specifies otherwise.
- Execution parameters (context size, thinking, resource caps) live in the prompt's Lua, never the frontmatter, the command line, or a gateway toggle.
- Analytical pipelines run at temperature zero.

**Rejected alternatives and stated costs:**
- Declaring model settings in the frontmatter ("the H1 lua needs controls to set the caps. it should not go in the frontmatter").
- models.only, an all-or-nothing lock - rejected because it "permanently foreclosed" per-section choice; a default plus per-section override is briefer when there are only one or two exceptions. Replaced with models.default.
- Non-inheriting model resolution.
- Frontmatter keys or command-line flags for context_max_tokens and no_think ("those should be properties of the prompt, not the command line").
- A gateway-level thinking toggle ("the prompt should control if thinking is on or off, not at the gateway").
- Nonzero temperature for analytical work ("temperature is supposed to be zero for analytical pipelines").

**Concrete incidents / author-verbatim phrases:**
- "The prompt has to specify what the minimum context size is" (purpose pass Record 5).
- "switching a model in the middle of a block has consequences for the KV cache... that's not visible to the programmer" (2026-08-18-1126-promptforge-md-aug18-morning.md p179)
- No model selected before first prose is an error (p66-67).
- "H3 should inherit the H2's model unless it specifies otherwise" (2026-08-09-1058-promptforge-core-large-part2.md p142)
- models.use only in the first Lua block, then locked (p175, p177).

**Merge/derivation notes:**
- Grouped-draft record (line 574) merged from user-stated, user-corrective, and ai-proposed (affirmed) sources across 5 chat units; endorsement: affirmed (ai-proposed leg).
- Purpose pass Record 5; merge suggestion: none. Adjacent to Record 6 (both about model binding) but kept separate: Record 5 is about who owns the choice and when it locks; Record 6 is about how loosely the name resolves. The design doc preserves that split as principles 32 and 33.

## Principle 33: Model binding is loose

**Rule:** Model binding is loose, much looser than tool binding, and resolves through the same semantic picker.

**Purpose facts:**
- A section's contract with the rest of the prompt is ordinary markdown, so which model slot executes it makes no difference to the section.
- This is what lets a pipeline hop between model tiers per step (map-reduce: the reduce section stays ordinary markdown; only its model slot changes).

**Rejected alternatives and stated costs:**
- Strict model-name binding that fails hard on mismatch - fails hard on catalog drift for no benefit.

**Concrete incidents / author-verbatim phrases:**
- The author hit a hard "model binding failed" error and rejected strict binding: "this makes no sense. the models need to be way looser than the tools. Shouldn't this use the tool-picker?" (2026-08-14-1613-promptforge-core-largest-part2.md p132-133)
- "The reduce section stays ordinary markdown; only its model slot and a staircase-streaming aggregator change" (2026-07-30-0654-map-reduce-synthesis.md design documents section)

**Merge/derivation notes:**
- Grouped-draft record (line 581) from user-corrective and ai-proposed sources across 2 chat units; endorsement: unaddressed (ai-proposed leg).
- Purpose pass Record 6; merge suggestion: none.

## Stanza facts

**What the section covers:** How a prompt gets its tools and its model: per-section opt-in tool scoping, a single loud tools.add entry point, epilogue assertions on tool usage, Lua-implemented tools, prompt-owned model selection with per-section locking, and loose model binding.

**Why the layer exists:** The offered surface is what a small model can navigate, and a wrong binding should explode at load time, not misbehave at run time.

**Failure modes it prevents:**
- Small-model confusion from oversized tool lists (context pressure).
- Silent tool-binding failures that are debugging traps.
- Runs that come back empty because a required tool was never called.
- Invisible KV-cache invalidation from mid-section model switches.
- Hard failures on model catalog drift for no benefit.

**Unifying principle (one sentence):** Declare everything, bind it early, fail loud.

# Packet Section VI - Trust and Failure (principles 34-37)

Facts only. No prose. Writer subagent turns this into exposition.

## Principle 34 - Untrusted envelope

- Rule: Outside content reaches the model only inside the untrusted envelope.
- Purpose facts:
  - Web fetches and other outside content go straight into the model's context; anything in that content that looks like an instruction can hijack the prompt.
  - Lets the author wrap any string, not just store content - this is why `store.inject` was removed in favor of a global `untrusted(s)`.
  - `untrusted(s)` wraps any string with the injected tag and the machine instruction to treat the contents as data, not instructions.
  - Tools that return attacker-controllable output are wrapped automatically when the tool declares an untrusted-output property.
  - Marker strings inside the content are escaped so the delimiter cannot be forged; content that forges the envelope's open or close tags is defanged before injection.
  - The envelope is the only trust control. Line numbers on store reads are for navigation and editing only; the split read API (`read_lines` numbered for editing, `read` verbatim for trusted handoff, injection via the envelope) exists so nobody mistakes line numbers for protection.
  - What breaks without it: a caller could inject numbered store content raw and believe it was safe.
- Rejected alternatives and stated costs:
  - An inject method on the store (`store.inject` is removed, not kept as sugar).
  - Injecting stored content into the context raw.
  - A separate safe-fetch tool chosen per call.
  - A single read call with a trusted/untrusted flag.
  - Treating numbered output as safe for model consumption.
  - A (startLine, lineCount) range form.
  - A global `numbered()` function composing strings in memory.
- Concrete incidents:
  - Hit while wiring the briefer tool: the `reply` being injected was "the joining of web fetches" and "definitely untrusted"; the author needed to inject it while telling the model it is data, not commands.
  - Author-verbatim: "what's the danger of an injection attack if we use line numbers?" - the question that motivated the split read API.
- Merge/derivation notes:
  - Merged from purpose-cluster-6 Record 1 ("Content arriving from external sources is untrusted and injection-prone...") and Record 2 ("The store's read API is split by trust and presentation..."). Both share one purpose: outside content reaches the model only through the untrusted envelope; nothing else is a trust control.
  - Grouped-draft endorsements: envelope record `corrected (ai-proposed leg)`; split-read record `affirmed (ai-proposed leg)`.
  - Scope: core. Sources: user-corrective; user-stated; ai-proposed.

## Principle 35 - Secrets never enter context

- Rule: Secrets never enter the model's context.
- Purpose facts:
  - Anything that enters the model's context can be repeated or exfiltrated.
  - API keys stay in the trusted backend; the LLM call happens in the Rust backend with the key in the OS credential store.
  - .env files are gitignored so secrets never enter version control.
  - The language's instructions explicitly forbid the model from reading any .env file into context.
  - App UI runs in the trusted context while third-party web content runs isolated.
- Rejected alternatives and stated costs:
  - Passing the API key through the prompt or the core instruction file.
  - Making LLM calls from the frontend with the key present in the webview.
- Concrete incidents:
  - Author-verbatim: "you're gonna be handling my API key, which is no good. I don't want the API key to leak into the model."
- Merge/derivation notes:
  - From purpose-cluster-6 Record 7 ("Secrets and privileged calls live only in the trusted backend..."). No merge.
  - Relation to Principle 34: both keep dangerous things out of the model's context, but the direction is opposite - 34 guards the context from content coming in, 35 keeps secrets from getting in at all. Kept separate for that reason.
  - Grouped-draft endorsement: `affirmed (ai-proposed leg)`. Scope: boundary gateway<->model; app<->web. Source: user-stated; ai-proposed (affirmed).

## Principle 36 - Abort on unusable evidence

- Rule: A run aborts when fetched evidence is unusable.
- Purpose facts:
  - If the fetch fails and the run continues, the model invents an evidence packet, and every downstream step built on that invented packet is garbage.
  - Aborting is the only way to keep a bad fetch from silently poisoning the whole result.
  - What breaks without it: a hallucinated evidence packet taints the entire downstream result.
- Rejected alternative and stated cost:
  - Soft-returning fetch failures and letting the prompt hallucinate past them.
- Concrete incidents:
  - The author asked what happens if all the fetched content is a bunch of 404s, and decided the run must stop.
- Merge/derivation notes:
  - From purpose-cluster-6 Record 3 ("When fetched evidence is unusable, the run aborts..."). No merge.
  - Grouped-draft endorsement: n/a. Scope: core. Source: user-stated.

## Principle 37 - Errors carry file and line

- Rule: Every error reported to the prompt author carries the file and line in the prompt that produced it, and misusing an API function produces a warning rather than silent wrong behavior.
- Purpose facts:
  - Without the location there is no finding which line of the prompt caused the failure.
  - Includes assertion failures.
  - What breaks without it: the author cannot locate the failing prompt line.
- Rejected alternatives and stated costs:
  - Errors that lack the prompt's file and line location.
  - Silently accepting the wrong function with no warning.
- Concrete incidents:
  - Assertion failures kept arriving with no location, repeatedly.
  - Author-verbatim: "assertion failed and we aren't getting the file and line numbers again"; "happened again and again no line number"; "again missing line number."
  - The author got bitten by calling the wrong API function with no warning at all - "this is kind of a trap."
  - Author's stated rule, verbatim: "for all errors, there has to be a file and line in, that corresponds to the prompt."
- Merge/derivation notes:
  - From purpose-cluster-6 Record 4 ("Every error reported to the prompt author carries the source file and line number..."). No merge.
  - Related to the observability records (observer/trace events, incremental run artifacts) - all three serve debugging a run - but kept separate: this one is about locating the failing prompt line, not observing engine behavior. Those observability records landed elsewhere (not in this section).
  - Grouped-draft endorsement: n/a. Scope: core. Sources: user-corrective; user-stated.

## Stanza facts - Section VI "Trust and Failure"

- What the section covers: untrusted content, secrets, and what happens when things go wrong.
- Why the layer exists: a prompt that reads the web is a prompt that can be hijacked, and a run that fails quietly is worse than a run that fails.
- Failure modes it prevents:
  - Prompt injection via fetched or tool-returned content (34).
  - Mistaking line numbers for a security control (34).
  - Secret leakage or exfiltration through the model's context, the frontend webview, or version control (35).
  - Silent poisoning of a run by a hallucinated evidence packet after a failed fetch (36).
  - Undiagnosable failures: errors with no prompt file/line, and silent wrong behavior from misused API functions (37).
- Unifying principle (one sentence): guard the context, and when something breaks, say so.
- Principle count: 4 (34, 35, 36, 37).

# Packet Section VII - Fanout (Principles 38-39)

Facts only. No prose.

## Principle 38: Fanout is always explicit; an arm is an ordinary section

**Rule:** Fanout is always explicit - a `fanout()` call, never the engine inferring parallelism from a bullet list - and an arm is an ordinary section running through the same code path as normal flow.

**Purpose facts:**
- Parallelism is a deliberate act by the prompt author; a bullet list sitting in a section must never silently trigger a fanout.
- The items fanned over usually come from the model at run time: a list section the model just wrote, or a Lua array built from tool results. You do not know ahead of time what the arms need to work on, so rigid statically fixed rules in Lua are useless - the hard part is the model's decision.
- `fanout()`'s second parameter dispatches on type: a string names a list section, an array table is the collection, anything else is a loud Lua error. Loud errors keep author mistakes visible instead of silently iterating something unintended.
- `list_from_section(name)`/`items()` returns a section's parsed bullet items as an array of strings; it can access only sibling sections at the same nesting level and child sections.
- An arm runs through the same engine code path and the same functions as normal flow; it can jump, execute, fanout, and list_from_section like any section. It differs only in what the harness hands it: its item and its task id.
- Work splits between a pure-data list section (no Lua) and a template section (shared leading-Lua preamble, prose with the per-arm item, shared trailing-Lua epilog): one section supplies items, the other supplies everything else.
- Each arm runs in a fresh VM built from the shared template; per-arm values (item text, task id) arrive through a sealed `sys`, not by overloading the section identity variable.
- Fanout is allowed whether or not a section has child headings.

**Rejected alternatives and stated costs:**
- Inferring fanout from bullets without an explicit call - listed as a non-goal in the plan; "This explicit fanout is in-contract; inferred fanout remains a non-goal."
- Silently iterating a hash-keyed table in unstable order - mistakes become invisible.
- Rigid, statically fixed fan-out rules in Lua - useless when the hard part is the model's run-time decision about what to work on.
- Colocating the arm's Lua with the bullet list - rejected in favor of the list-section/template-section split ("the H3 with the bullets can't have Lua. Instead, another H3 carries the Lua").
- Overloading the section identity variable with per-arm data - rejected in favor of sealed `sys` with item and taskid.
- Stubbed control globals in arms - rejected; arms get the real functions.
- A separate arm-execution path with its own functions - two engines to keep honest.
- Restricting fanout() to sections with child headings - a special case with no reason.

**Concrete incidents / author-verbatim phrases:**
- Reviewing the plan to collapse the duplicated arm engine: "an arm must be treated the same way as normal flow, preferably with the same functions... Why should arms be different?" (2026-08-19-0447-collapse-fanout-arm-review.md [p2])
- On the child-heading restriction: "I dont see a point to restricting things like fanout() just beause a section has no child headings. this is try-hard. its pointless." (2026-08-18-1126-promptforge-md-aug18-morning.md [p138])
- On arm capabilities: "arms can jump" ... "and execute, fanout, list_from_section, etc there is no reason for special cases" (2026-08-19-0048-promptforge-md-aug19.md [p78], [p79])
- On run-time item sources: "You don't know ahead of time what you need to search for in the sub-agent... if you're calling it from the Lua and you just have some rigid rules... really the hard part is in the model" (2026-07-30-0534-promptforge-design-context.md [p50])
- "Make this a general principle of the design, always explicit" (2026-08-08-0029-promptforge-context-planning.md [p35])
- "the most fundamental operation of FanOut... executing a set of operations in parallel... we have to allow that second parameter to be an array" (2026-08-18-1126-promptforge-md-aug18-morning.md [p45])
- "remember the preamble is shared. each subagent VM gets item and sys.taskid" (2026-08-08-0029-promptforge-context-planning.md [p47])

**Merge/derivation notes:**
- Merged from grouped-draft Fanout records 1 ("Fanout is always invoked explicitly through a fanout() call...", endorsement: affirmed (ai-proposed legs); source: ai-proposed (affirmed); user-stated) and 2 ("The subagent section is the arm template...", endorsement: n/a; source: user-stated; user-corrective).
- Purpose-pass merge suggestion: records 1 and 2 share one root purpose - fanout is an explicit, author-invoked mechanism built out of ordinary sections, with no engine inference from document shape and no special-cased arm execution.

## Principle 39: The invoking Lua owns the reduce

**Rule:** The invoking Lua owns the reduce - `fanout()` blocks and returns each arm's reply in arm order, the first arm error aborts its siblings with sequential fail-fast behavior, and only concurrent fanout is limited, never the total item count.

**Purpose facts:**
- The reduce is ordinary Lua written by the prompt author in the same chunk that called `fanout()`, so joining results is deterministic code instead of paid inference. Recurring author complaint: wasting model tokens on orchestration that Lua can do.
- `fanout()` is a blocking call returning each arm's final reply ordered by arm index.
- The first arm error aborts its siblings with the same invoker-visible behavior as sequential fail-fast - parallel execution stays indistinguishable from sequential to the invoker.
- The store stays shared and mutex-safe; authors must not assume arm N sees arm N-1 writes; store writes from arm epilogs stay visible to the reducer.
- Concurrency is throttled by the gateway's admission queue (core fires all arms at once, the gateway queue is the throttle), so a total item cap is unnecessary; only concurrent fanout needs a limit.
- Spoke identity (taskid, unique file names) is assigned by the harness because the model should not spend inference calculating names.

**Rejected alternatives and stated costs:**
- A total item cap (`max_fanout_items`) - forbids shapes of work for no resource reason; the gateway queue already throttles.
- The model computing each spoke's unique name or index - wastes inference on naming.
- A wait-for-all barrier before the reduce step runs - rejected in favor of fail-fast sibling abort.

**Concrete incidents / author-verbatim phrases:**
- "my thinking is this, the invoking lua deals with the reduce step" (2026-08-08-0029-promptforge-context-planning.md [p33])
- "max_fanout_items there should be no limit on the total, just a limit on concurrent fanout" (2026-08-19-0048-promptforge-md-aug19.md [p80])
- "I don't want the model to have to calculate the final name, we want to minimize the amount of inference" (2026-07-28-0925-orchestrator-design-document.md [p67])
- "why should we waste inference having to figure that out?" (2026-07-28-0925-orchestrator-design-document.md [p69])
- Plan language, repeated across two core plans: "core fires all arms at once, the gateway queue is the throttle; replies stay ordered by arm index; fail-fast aborts siblings... same invoker-visible behavior as sequential; the store stays shared and mutex-safe" (2026-08-14-1613-promptforge-core-largest-part5.md and 2026-08-09-1058-promptforge-core-large-part5.md, plans sections)

**Merge/derivation notes:**
- Derives from grouped-draft Fanout record 3 ("The invoking Lua owns the reduce step...", endorsement: unaddressed (ai-proposed legs); source: user-stated; user-corrective; ai-proposed).
- Purpose pass: record 3 stands apart from records 1-2 - its purpose is reduce semantics and concurrency (deterministic reduce in Lua, gateway-throttled concurrency, harness-assigned identity), not how fanout is invoked or how arms execute. Kept separate per the merge suggestion.

## Stanza facts (Section VII)

- Covers: parallel execution - how fanout is invoked (explicit `fanout()` call, type-dispatched second parameter), what an arm is (an ordinary section, same code path, fresh VM, sealed sys), and how results come back (blocking call, ordered replies, fail-fast abort, Lua-owned reduce, gateway-throttled concurrency, harness-assigned spoke identity).
- Failure modes prevented: engine silently inferring parallelism from document shape; silent iteration of unintended collections; a second arm-execution engine drifting out of honesty with the main engine; special-cased arm capabilities; paying model inference for orchestration (reduce, naming) that deterministic code can do; total item caps forbidding valid work shapes; parallel runs behaving observably differently from sequential runs.
- Unifying principle (one sentence): Parallelism is explicit, and an arm is just a section.

# Packet Section VIII - The Core Crate (principles 40-46)

Facts only. Sources: purpose-cluster-8.md (motivations), grouped-draft.md (full records with rejected alternatives and endorsements).

## Principle 40 - Single concern per file, minimal public API, tightened continuously

- Rule: Keep each file to a single concern and the public API as small as it can be, tightening it as you go by considering how each function interacts with the others.
- Purpose facts:
  - API growth drives quadratic growth in dependencies between functions, so a smaller API is always better than a larger one.
  - Tightening the API on every commit keeps the total debt workload linear, even though each commit costs more.
  - API design considers how each function interacts with the others in pairs, in triples, and all together - not each function in isolation.
  - One-off cleanup efforts done by hand get generalized into a reusable prompt that runs against recent commits, so debt is paid as he goes instead of in one large effort at the end.
- Rejected alternative (grouped draft): deferring cleanup to a later dedicated phase or one large effort at the end; evaluating each API function in isolation. Stated cost: facing a pile of review findings all at once.
- Concrete incident: The author vibe-coded the repo for days without doing debt refactors along the way and ended up facing a large pile of review findings all at once. This is the "learned the hard way" episode behind the principle.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Derives from the grouped-draft record "Refactoring happens continuously at every step..." (Continuous debt payment and evidence group). Citations: 2026-08-10-0856-repo-review-top-to-bottom.md [p30]-[p32], [p36], [p52], [p53]; 2026-07-31-1516-agentic-ide-research.md [p49], [p57].

## Principle 41 - One build configuration, no feature flags

- Rule: One build configuration. No feature flags, ever - there is only one version of the binary, and if size becomes a problem the crate gets split later.
- Purpose facts:
  - When conditional compilation was proposed, he refused: he never wants "features," there is only one version of the binary.
  - The escape hatch for binary size is splitting the crate later, not gating code behind flags.
- Rejected alternative (grouped draft): conditional compilation via feature gates. Stated cost: none recorded beyond the refusal itself; the record gives an explicit reason only for this leg.
- Concrete incident: Feature flags were proposed during the Brave web search tools work and rejected on the spot.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Derives from the feature-flag leg of the grouped-draft record "Library code propagates errors and never unwraps; new dependencies are not introduced...; there are no cargo feature flags and exactly one build configuration." The no-unwrap and no-new-deps legs of that record appear only as standing binding rules restated in a plan prompt with no stated motivation, and did not carry into this principle. Citations: 2026-07-29-0937-brave-web-search-tools.md [p16], [p19]; 2026-08-14-1612-file-backed-store-execution.md [p3].

## Principle 42 - A crate fits in one coding-LLM context window

- Rule: A crate stays small enough that a coding LLM can hold the whole crate in a single context window.
- Purpose facts:
  - The implementation work is done by coding models; crate size is bounded by what the LLM can hold at once.
  - A crate that fits in one context can be reviewed, refactored, and reasoned about as a unit.
  - Stated directly during the MCP client work: a separate crate means a coding LLM only has to consider a smaller amount of code and is more likely to fit the whole crate in a single context window.
- Rejected alternative (grouped draft): none recorded.
- Concrete incident: Arose when deciding whether to embed the MCP client in the tool-picker crate; the argument for a separate crate was the context-window bound.
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Stands alone. Purpose notes record that this principle and principle 41 both serve the LLM-driven workflow, but the mechanisms differ and no merge was recommended. Citations: 2026-08-02-1034-mcp-client-harness.md [p78], [p79]; 2026-08-02-1419-mcp-client-continued.md [p79].

## Principle 43 - Every feature ships with its test; external services get real manual integration tests

- Rule: Every markdown feature of the prompt format ships with its test, and every feature that calls an external service ships with a manual integration test that exercises the real service and is actually run.
- Purpose facts:
  - Format features never ship unverified: while planning the executor he instructed that every markdown feature must come with its test.
  - For external services he wants a manual test that exercises the real service, and he wants to see it run and work.
  - A mock proves the mock, not the service.
- Rejected alternative (grouped draft): mock-only tests. Stated cost: a mock proves nothing about the real service.
- Concrete incident: The agent delivered the Brave web search tool without any test that actually calls Brave, and he pushed back, demanding a manual test against the real service, actually run.
- Endorsement: n/a (user-stated; user-corrective).
- Merge/derivation notes: Single grouped-draft record "Every markdown feature of the prompt format ships with a corresponding test..." (Continuous debt payment and evidence group). Citations: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]; 2026-08-02-1134-mcp-client-large-part3.md [p173]; 2026-07-29-0937-brave-web-search-tools.md [p26], [p27].

## Principle 44 - The executor is a dumb function call; the gateway owns everything model-specific

- Rule: The executor holds no vendor credentials, no endpoints, no provider knowledge, no global state; everything model-specific - keys, routing, tool-call translation, model download and caching - concentrates in the gateway. The executor never knows whether a model is local or remote.
- Purpose facts:
  - He works through an AI-driven workflow with many layers of software between him and the running system, and found configuration a pain; he wanted one central point of configuration, and the gateway is it.
  - Only one machine can hold the vendor key, because global rate limits cannot be enforced from many key-holding processes (OpenAI and vLLM do not queue well), so the key had to move out of the executor into the gateway.
  - One central point of configuration is what makes the system operable.
  - He asked directly which layer should handle translating to and from each model's tool-call format, and confirmed the gateway, keeping the executor free of per-model differences.
  - Downloading and caching models is the gateway's job; callers and tests supply only configuration naming the source URL and pin.
- Rejected alternatives (grouped draft, both merged records): the executor reading the vendor API key directly; an executor-level base_url setting; engine-owned global state shared across runs; the executor handling per-model tool-call translation; core tests standing up llama-server and fetching GGUF weights themselves.
- Concrete incidents and author-verbatim phrases:
  - His summary, verbatim: "the executor is just a function call" - it talks only to the gateway and never knows whether a model is local or remote.
  - When wiring local inference, he rejected core tests standing up llama-server and fetching GGUF weights themselves.
- Endorsement: the executor-as-function-call record is marked ai-proposed legs unaddressed; the tool-call-translation record is user-stated/user-corrective, endorsement n/a.
- Merge/derivation notes: Two grouped-draft records merged into this principle, per the purpose notes' merge suggestion (records 5 and 6 share one purpose): "The executor holds no vendor credentials, endpoints, or provider knowledge of its own..." and "Model-specific translation to and from tool calls is the gateway's responsibility...; model download and caching live in the gateway, never in the core or the test harness." Citations: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: gateway v0]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p185]-[p187], [p189], [p211], [p215]; 2026-08-08-1223-gateway-local-inference.md [p16], [p18], [p41], [p42]; 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md].

## Principle 45 - No shared schemas; the gateway never depends on core

- Rule: Components do not share schema definitions, and the gateway never depends on core. Each side of a boundary owns its own schemas.
- Purpose facts:
  - Sharing schemas is unnecessary coupling that pins two components to each other's internals.
  - The gateway-not-depending-on-core leg was his own gut call from the first gateway discussion.
- Rejected alternative (grouped draft): a shared schema package used by both executor and gateway; the gateway linking against core.
- Concrete incidents and author-verbatim phrases:
  - When schema sharing came up he initially asked why not share them - verbatim: "Isn't it JSON?" - and once it was explained he agreed, verbatim: "Of course they should not share them. that's unnecessary coupling."
- Endorsement: n/a (user-stated).
- Merge/derivation notes: Single grouped-draft record "Components do not share schema definitions... the gateway must not depend on core." The purpose notes mark it adjacent to principle 44's records (same core<->gateway seam) but with a distinct purpose - decoupling, not vendor-knowledge placement - so it stays separate. Citations: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190]-[p192]; 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]; 2026-07-29-0937-brave-web-search-tools.md [p11].

## Principle 46 - Integration tests require an already-running gateway

- Rule: Integration tests require an already-running, already-configured gateway - a test never launches the gateway itself. A small local model stays runnable without the gateway, so integration tests can exercise real inference with a simple setup.
- Purpose facts:
  - A test should require that the gateway already exists and already has its configuration.
  - Models are reached through the gateway rather than through bespoke direct wiring in the test harness; direct wiring is duplicated effort when the gateway is needed anyway.
  - A small (0.6B) model kept runnable without the gateway is a simple setup that lets integration tests exercise real inference and expands the testing surface without the bulk of spawning the gateway.
- Rejected alternative (grouped draft): tests spawning their own gateway instance; wiring a local model directly into core-tests, bypassing the gateway.
- Concrete incidents and author-verbatim phrases:
  - The tests were launching the gateway themselves and it was going wrong - stuck, failing - and he called it, verbatim, "all wrong."
  - Earlier he had regretted wiring the 9B model directly into core-tests when the gateway was needed anyway for web search.
- Endorsement: n/a (user-corrective; user-stated).
- Merge/derivation notes: Single grouped-draft record "Integration tests require an already-running, already-configured gateway..." The purpose notes observe that its second leg (tests supply only config, never wire models directly) is the test-side consequence of principle 44's model-download record, and its first leg (tests never launch the gateway) stands as the testing corollary. Citations: 2026-08-14-1613-promptforge-core-largest-part2.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part3.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part2.md [p140].

## Stanza facts - Section VIII as a whole

- What the section covers: how the core crate itself is built - file and API size, build configuration, crate size, test discipline, and the core<->gateway boundary (credentials, translation, schemas, test setup).
- Why the layer exists: the people writing this code are mostly models, and the structure has to fit the worker.
- Failure modes it prevents:
  - Quadratic API-dependency debt surfacing as one large pile of review findings (40).
  - A feature-flag build matrix and multiple versions of the binary (41).
  - Crates too large for a coding LLM to review, refactor, or reason about as a unit (42).
  - Format features shipping unverified and external-service features proven only against mocks (43).
  - Vendor credentials, endpoints, provider knowledge, and global state leaking into the executor; unenforceable global rate limits; scattered configuration (44).
  - Two components pinned to each other's internals through shared schemas or a gateway-to-core dependency (45).
  - Flaky self-launching test gateways and bespoke model wiring duplicated in the test harness (46).
- Unifying principle, one sentence: keep every unit small enough to hold in one head.

# Open questions facts



Render these as the Open Questions section, one short paragraph each, plain language.



## Open Questions

The record leaves these tensions unresolved. Each is a place where two positions conflict and no final ruling exists.

1. Defaults. "No defaults, everything explicit" sits against "implement all features and let the caller decide, with sensible defaults", and against the pairing of "default configuration enables no tools" with "fundamental tools are built into core". Where defaults are permitted and where they are the enemy was never reconciled.
2. Fanout scope. Three positions survive: fanout restricted to the fanning section's own children, fanout allowed whether or not a section has children, and parallel analysis expressed as plain nested subsections with no fanout mechanism at all.
3. Control-flow surface. The record holds both a single unified control tool with a type discriminator and named jump()/execute() functions; later units appear to supersede earlier ones, but no record states the unified-tool design is abandoned.
4. Shared-chunk mechanics. "The H1 preamble runs exactly once as a live preamble" conflicts with the shared chunk being "compiled once and replayed in each section's fresh VM" under phase gating; two different mechanisms both appear as current.
5. Static tool discovery. Load-time discovery by stub-parsing the prompt's Lua is a landed principle, but the doubt survives that general-purpose Lua computation makes static detection of every tool call unreliable.
6. Empty replies. "An empty model response is never acceptable" versus the conditional empty-turn clean exit; the later rule refines the earlier one, but the exact boundary of which empty turns fail closed deserves confirmation.
7. Weight of the untrusted envelope. Guard-wrapping is adopted and automatic, yet the envelope is a probabilistic mitigation whose hard controls are scoping and context-clearing isolation; how much the design may rely on it is unstated.

# Approach section source



The closing section The Approach Behind the Rules. This text is already final prose; carry it unchanged.



## The Approach Behind the Rules

Not everything in these chats converts to a rule, because the rules are the residue of a practice, not the practice itself. The practice is a sensibility: lean means slender call chains and minimal inference rather than small files, and the best feature is the one that delivers everything with the least machinery, because less code to maintain beats bespoke machinery every time. The language is treated as a made object, a work of art whose primitives should feel like one family and whose names come from vocabulary every prompt writer already owns. When a limit appears, the temperament is honest and aggressive at once: a probabilistic guard is admitted to be a mitigation rather than a boundary, minute-scale latency is a defect to attack rather than a fact of life, and unshipped code earns no compatibility concessions because there is no one to break. Evidence sits at the center of every decision: defaults are interrogated against intuition, proposals are floated freely and then left for measurement to kill, quick confident answers are distrusted until the actual mechanism is shown, and a correct generalization is expected to pay for itself by deleting special cases. Underneath it all runs a theory of the medium itself, that every regeneration blurs an artifact toward the mean and no model can sharpen without external information, which is why the first pass is the sharpest and the human conversation remains the substance. The design ultimately rests on a single metaphor held with complete seriousness: the markdown is the program, the model is the CPU, the embedded Lua is the microcode, and the harness is the instruction decoder.
