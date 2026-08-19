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
