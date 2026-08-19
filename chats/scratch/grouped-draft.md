# PromptForge design principles - grouped draft

Deduplicated, trimmed, and grouped from the merged research packet (635 records across 51 chat units). Survivors: 100 principles in four layers. Near-duplicates were merged with citations consolidated under the sharpest wording; weaker records were cut by coverage, derivation weight, and generality. Each survivor keeps its full record: statement, scope, source, citation, rejected-alternative, endorsement.

## Global

*This layer covers the product's posture and the working method that surrounds it: what PromptForge is, how small its mechanism set stays, and how plans, artifacts, reviews, and documentation are produced. It exists to prevent the failure modes of vibe-built software: accreting special cases, blurred regenerated artifacts, unreviewed autonomous work, and docs that drift from the code. Compressed to one sentence: say it once, in the smallest form that executes identically, and let the plan - not the model's memory of the artifact - remain the source of truth.*

### Posture and reference fidelity

```yaml
- statement: When any UI behavior or appearance is in doubt, the implementation copies Cursor exactly, with VS Code as the secondary reference, down to fonts, icons, and layout.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p46], [p49], [p81]
  rejected-alternative: designing UI elements from first principles or original designs
  endorsement: n/a

- statement: PromptForge is a deterministic pipeline whose product is a finished report, designed for unattended server deployment running reports at scale; interactive invocation exists for development, testing, and explicit local runs.
  scope: global
  source: user-stated
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p58], [p59]
  rejected-alternative: a general-purpose prompting language invoked conversationally
  endorsement: n/a
```

### Minimal mechanism

```yaml
- statement: Do more with less: if an established facility can implement a feature, use it instead of building new infrastructure; expressive general primitives are preferred over dedicated single-purpose features, and the core stays a minimal set of small primitives reused everywhere.
  scope: global
  source: user-stated; user-corrective
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p61]; 2026-08-09-1058-promptforge-core-large-part4.md [p267]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p15]; 2026-08-09-1058-promptforge-core-large-part1.md [p26]; 2026-08-14-1613-promptforge-core-largest-part3.md [p267]
  rejected-alternative: inventing new frontmatter when Lua already works; a dedicated require_called directive for mandatory tool calls
  endorsement: n/a

- statement: Never provide two ways of doing the same thing, unless there is a really good documented reason.
  scope: global
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p26]; 2026-08-14-1613-promptforge-core-largest-part1.md [p26]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p165]
  rejected-alternative: duplicate facilities for the same capability
  endorsement: n/a

- statement: No parallel mechanisms; a single, small, well-designed set of primitives services all needs, and an existing mechanism such as tool scoping is leaned on as far as it can go before anything new is added.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p371]; 2026-08-09-1058-promptforge-core-large-part4.md [p371]
  rejected-alternative: adding a new mechanism alongside an existing one that already covers the need
  endorsement: n/a

- statement: A small set of flexible, multi-purpose primitives should compose into maximum possibility while keeping the prompt author brief; verbosity is a design failure.
  scope: global
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p168]
  rejected-alternative: none
  endorsement: n/a

- statement: Everything in the language behaves as consistently as possible, and constraints fall out of the existing rules naturally rather than as hand-coded special-case checks, unless there is a really good reason for an exception.
  scope: global
  source: user-stated
  citation: 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p176], [p177], [p178]
  rejected-alternative: hand-coded guard checks for each constraint
  endorsement: n/a

```

### Legibility and naming

```yaml
- statement: A prompt must be readable on its face: a reader can look at it and understand what it does, with no invisible action whose meaning is subject to interpretation by the model.
  scope: global
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p360-p362]; 2026-08-02-1134-mcp-client-large-part5.md [p362]
  rejected-alternative: dispatch expressed as literal text the model is expected to interpret and act on
  endorsement: n/a

- statement: An overarching design theme of the language is that it closely resembles the ordinary theory of computation; shared top-level reusable sections are subroutines, a staple of computation.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p385]; 2026-08-02-1134-mcp-client-large-part5.md [p385]
  rejected-alternative: none
  endorsement: n/a
- statement: Language keywords and names come from the vocabulary models and prompt writers already speak, and a name is a design decision that must say how the mechanism works, so there is no confusion.
  scope: global
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p30], [p31]; 2026-08-14-1613-promptforge-core-largest-part5.md [p473]; 2026-08-02-2331-mcp-client-evening.md [plans section]
  rejected-alternative: none
  endorsement: n/a

- statement: Terminology is fixed and enforced repo-wide: the preamble is the H1 code, while prologue and epilogue belong to sections.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p393], [p395]; 2026-08-09-1058-promptforge-core-large-part5.md [p393]
  rejected-alternative: none
  endorsement: n/a
```

### Explicitness and consent

```yaml
- statement: No defaults, everything explicit: every prompt declares the model it needs, or explicitly says it accepts anything, and at minimum states its required context and whether it needs thinking; implicit configuration is the enemy of precision.
  scope: global
  source: user-corrective
  citation: 2026-08-08-1223-gateway-local-inference.md [p58], [p60], [p62]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p66]
  rejected-alternative: DEFAULT_MODEL and PROMPTFORGE_MODEL environment-variable fallbacks
  endorsement: n/a

- statement: Explicit user opt-in legitimizes otherwise restricted behavior; consent is the gate for powerful capabilities.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p374]
  rejected-alternative: restricting the behavior outright regardless of user consent
  endorsement: n/a

- statement: Every protection the engine imposes can be disabled; an embedder building an agent, harness, or IDE must have a way to turn all the settings off.
  scope: global
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part5.md [p354]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p354]
  rejected-alternative: compulsory protections with no opt-out
  endorsement: n/a
```

### Plans and generated artifacts

```yaml
- statement: The plan is the source of truth: an artifact is revised by editing the plan that created it and regenerating, never by having the model rewrite the artifact; the plan is preserved for the life of the artifact; a modification is merged back into the original plan rather than planned against the generated artifact; and small tweaks are appended to the plan as individual instructions for the next regeneration.
  scope: global
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p6], [p24], [p33], [p42], [p57]; 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: bringing the artifact into a new revision pass and letting the model rewrite it; chaining a modification plan whose input is the previous plan's output
  endorsement: affirmed (ai-proposed leg)
- statement: Prompt artifacts must stay lean; a revision that grows the artifact is a failure mode, not an improvement.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p1], [p49], [p50]
  rejected-alternative: accepting growth as the natural cost of revision
  endorsement: n/a
```

### Compression and sharpening

```yaml
- statement: Compressing a prompt sentence is valid only when the shorter sentence means the same thing in execution, or is even more aligned than the original; the judgment is objective - how the instruction will execute, comparable by a frontier model - and a compression pair is kept only when no model would behave differently following the compressed text.
  scope: global
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-07-28-0207-architect-vibe-planning-part1.md [p56], [p58]; 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: shortening for token count alone; training the compressor on the author's personal style
  endorsement: affirmed (ai-proposed leg)

- statement: A compressor never expands its input - the non-expansion guarantee is enforced mechanically outside the model, whose worst case is returning the input verbatim - and it is single-purpose (no tool calls, no thinking), idempotent, and only cuts: it never adds a specific that is absent from the source.
  scope: global
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p62], [p70], [p71], [p82]; 2026-07-28-0207-architect-vibe-planning-part1.md [p57]; 2026-07-28-0207-architect-vibe-planning-part4.md [plans section]
  rejected-alternative: trusting the model to enforce its own length limit; a general-purpose model that also compresses; bundling add-rigor rules into a compressor
  endorsement: affirmed (ai-proposed legs)

- statement: Compression is smart generative rewriting, not the deletion of tokens; prompts are written to read beautifully as human prose, readability outranks token-count reduction, and tightening a prompt means making it aligned and unambiguous, not making it shorter.
  scope: global
  source: user-corrective; user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p81]; 2026-07-28-0207-architect-vibe-planning-part3.md [p118], [p146]
  rejected-alternative: LLMLingua-style subtractive token dropping applied to the author's prompts; reading "tighten" as size reduction
  endorsement: n/a

- statement: Blur is irreversible from within the regeneration chain: the training target must be the true pre-blur original, a blurred document is fixed by hand with targeted non-regenerative edits, sharpening a blurred plan requires external information (the previous revision plus the author's stable repertoire of techniques), and the work ships when sharp enough - an ambiguity audit has no fixed point, and chasing perfection is the blur trap applied to process.
  scope: global
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p223], [design documents section]; 2026-07-28-0207-architect-vibe-planning-part1.md [p55]
  rejected-alternative: re-sharpening a blurred text to recover the original; fixing blur by regenerating; one more tightening pass
  endorsement: affirmed (ai-proposed legs)
- statement: Attach the rationale to every rule, because the model generalizes from the reason while a bare rule is pattern-matched; a sharpening instrument aligns the model generally rather than prescribing task-specific diagnostic algorithms, and a style rule belongs in mechanical sharpening only if it can be applied mechanically.
  scope: global
  source: user-corrective; user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part4.md [p204], [p214], [p216]; 2026-07-28-0207-architect-vibe-planning-part3.md [p165]
  rejected-alternative: reasonless rules with an escape-hatch framing; including the analytical-framework cluster in the sharpener; encoding judgment-requiring prose rules
  endorsement: n/a
```

### Autonomous execution and verified work

```yaml
- statement: Autonomous execution continues without stopping until the assigned work is done, pausing only when user input is genuinely required or the outcome diverges significantly from expectation; a plan executes fully autonomously and never uses AskQuestion or otherwise pauses for user interaction.
  scope: global
  source: user-corrective
  citation: 2026-07-31-1516-agentic-ide-research.md [p87], [p109]; 2026-07-28-0207-architect-vibe-planning-part2.md [p104], [p106]; 2026-08-04-1426-recover-core-design-rationale.md [p4]
  rejected-alternative: stopping to check in at intermediate milestones; interactive plans that stop to ask the user questions mid-run
  endorsement: n/a

- statement: Work runs in subagents, in parallel when possible: every unit of work gets a fresh context that is never reused, and the main context receives only completion status, a short summary, and the artifact path, so the main context and the plan stay potent.
  scope: global
  source: user-stated
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p1], [plans section]; 2026-08-11-1510-repo-review-continued.md [p1], [plans section]; 2026-07-28-0207-architect-vibe-planning-part2.md [p60], [p84]
  rejected-alternative: reusing agents, pulling full findings into the main conversation, or doing the work in the main context
  endorsement: n/a

- statement: After every commit the AI reviews its own code, red-teams the tests, removes the technical debt it finds, verifies the tests pass, and amends the commit instead of adding a new one; every commit pays down technical debt, and tests cover the absence of behavior (removed names erroring, blocked actions failing, invalid inputs rejected) and not only the presence of new behavior.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]; 2026-08-19-0048-promptforge-md-aug19.md [p21], [p74], [plans section]
  rejected-alternative: committing first and cleaning up in later commits; testing only what was added
  endorsement: n/a

- statement: A run lands its result only when verification is green: on failure it rolls back with a reset (never a revert) and redoes the work, fixing forward from the verifier's concrete file:line NOT-FIXED list, and completion is judged by an independent fresh-context audit of the actual source - not the worker's self-report and not gates alone, because compile, lint, and test gates do not catch behavioral or design findings.
  scope: global
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-10-0856-repo-review-top-to-bottom.md [p20], [plans section]; 2026-08-11-1510-repo-review-continued.md [p24], [p54], [plans section]
  rejected-alternative: landing red; undoing failure with a revert commit; discarding a mostly-correct candidate and restarting blind; trusting the fix agent's own all-green report
  endorsement: affirmed (ai-proposed legs)

- statement: Review and modification are separate phases driven by the complete findings set: all findings for a crate are gathered before any file is modified, every finding receives an explicit disposition (fixed, or rejected with specific contrary evidence), each API change must both reduce the chance of recurrence and shrink the surface, change for change's sake is rejected, and stages that consume a previous stage's output run serially while only independent per-unit work parallelizes.
  scope: global
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-11-1510-repo-review-continued.md [p1], [plans section]; 2026-08-10-0856-repo-review-top-to-bottom.md [p1]
  rejected-alternative: interleaving review and fixes file by file; fixing findings one by one without rethinking the API; letting findings drop silently; parallelizing dependent stages
  endorsement: affirmed (ai-proposed legs)
```

### Continuous debt payment and evidence

```yaml
- statement: Refactoring happens continuously at every step: each file holds a single concern, a smaller API is always better than a larger one, and the public API is tightened per commit - designed by considering how each function interacts with the others in pairs, in triples, and all together - because API growth drives quadratic dependency growth and per-commit tightening keeps total debt work linear; one-off cleanup efforts are generalized into reusable prompts that run against recent changes.
  scope: global
  source: user-stated
  citation: 2026-07-31-1516-agentic-ide-research.md [p49], [p57]; 2026-08-10-0856-repo-review-top-to-bottom.md [p31], [p32], [p36], [p52], [p53]
  rejected-alternative: deferring cleanup to a later dedicated phase or one large effort at the end; evaluating each API function in isolation
  endorsement: n/a
- statement: Every markdown feature of the prompt format ships with a corresponding test, and a feature that calls an external service ships with a manual integration test that exercises the real service and is actually run to prove it works.
  scope: global
  source: user-stated; user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p173]; 2026-08-02-1134-mcp-client-large-part3.md [p173]; 2026-07-29-0937-brave-web-search-tools.md [p26], [p27]
  rejected-alternative: mock-only tests
  endorsement: n/a
```

### Documentation

```yaml
- statement: Documentation moves with the code: the design document and user guide are revised in the same commit as the change that alters the behavior, stale instructions are treated as defects, every user-facing crate carries a README.md with full friendly instructions plus a design.md explaining the design choices, and running a plan generates the design document after implementation completes so it is always in sync with the built code.
  scope: global
  source: user-stated; user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p204]; 2026-08-14-1613-promptforge-core-largest-part5.md [p478]; 2026-08-03-2040-plan-the-mcp-server.md [p17], [plans section]; 2026-08-15-2006-promptforge-md-aug15.md [p21]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p318], [p319]
  rejected-alternative: batching documentation updates after implementation; leaving outdated instructions in place; generating the design document before or separately from the implementation
  endorsement: n/a

- statement: A design document holds only decisions and rationale: it states what happens rather than aphoristic properties, never counts what it does not name, and Rust types and code are removed from it as implementation proceeds while the master plan tracks only unbuilt design.
  scope: global
  source: user-corrective; ai-proposed (affirmed)
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p280], [p310]; 2026-08-03-2040-plan-the-mcp-server.md [plans section], [p68], [p73], [p76]
  rejected-alternative: design documents carrying Rust types and declarations; aphoristic property statements; unnamed counts that send the reader hunting
  endorsement: affirmed (ai-proposed legs)
```

### Code and repo hygiene

```yaml
- statement: Library code propagates errors and never unwraps; new dependencies are not introduced to solve a problem; there are no cargo feature flags and exactly one build configuration - if binary size becomes a problem, the crate is split later.
  scope: global
  source: user-stated
  citation: 2026-08-14-1612-file-backed-store-execution.md [p3]; 2026-07-29-0937-brave-web-search-tools.md [p19]
  rejected-alternative: unwrap/expect in library code; pulling in a new crate; conditional compilation via feature gates
  endorsement: n/a

- statement: Crates are kept small enough that a coding LLM can hold an entire crate in a single context window.
  scope: global
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p79]; 2026-08-02-1419-mcp-client-continued.md [p79]
  rejected-alternative: none
  endorsement: n/a
```

### Prose and prompt quality

```yaml
- statement: Generated prose contains no formulaic AI rhetorical tics; every sentence in a written artifact justifies its presence; and an artifact that has grown to thousands of lines is defective and gets compressed - tighten every instruction, one instruction per line, delete hedges, quantify every quantity.
  scope: global
  source: user-corrective; user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p99], [p108], [p110], [p113]; 2026-08-11-1510-repo-review-continued.md [p52], [p53], [plans section]
  rejected-alternative: a length pass that leaves the rhetorical patterns in place; accepting bulk as the natural cost of completeness
  endorsement: n/a
```

## Core

*This layer covers the prompting language and its executor: the document structure, control flow, Lua environment, tool scoping, state channels, trust envelopes, and model selection that make a markdown file behave as a program. It prevents context bloat, prompt drift, invisible behavior, and confused-deputy failures by clearing context on every transfer, scoping every tool, and wrapping every untrusted byte. Compressed to one sentence: the markdown is the program, everything the model can do is explicitly declared by the author, and everything the author declares is enforced exactly as written.*

### The prompt as a program

```yaml
- statement: A prompt is a single markdown file that is one function - it takes well-defined parameters declared in machine-readable YAML front matter and returns a string, and it may also produce side effects such as files written through tools.
  scope: core
  source: user-stated; ai-proposed
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p117]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p65, p117]; 2026-07-28-2238-orchestrator-design-continued.md [p65, p117, p74]; 2026-08-12-1534-dokuman-each-crate.md [design documents: introduction.md]
  rejected-alternative: none
  endorsement: n/a

- statement: The design starts from the prompt and adds structured programming into it, never the other way around; a prompt with zero Lua still works like a plain orchestration, so Lua is additive, not required, and a prompt is self-contained - running it never requires a companion Rust file backing its operations.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part2.md [p86], [p118]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p86], [p118]; 2026-07-28-2238-orchestrator-design-continued.md [p118]
  rejected-alternative: starting with an interpreted host language and bolting prompts onto it; every prompt backed by its own Rust code
  endorsement: n/a

- statement: No compilation step sits between the prompt author and the model - the raw markdown is the program: the entire document is parsed once up front and all Lua is compiled at parse time, so no markdown parsing happens at run time and a run-time syntax error is impossible or nearly so; and reading a prompt file never runs anything inside it - a parsed prompt is inert data that can be constructed, inspected, and enumerated on a server surface without executing prompt code.
  scope: core
  source: ai-proposed; user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [design documents section]; 2026-08-03-2040-plan-the-mcp-server.md [p74]; 2026-08-08-0029-promptforge-context-planning.md [p62]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: compiling markdown to an intermediate representation before execution (Playbooks lesson); parsing markdown lazily at run time
  endorsement: corrected (one ai-proposed leg); unaddressed (other ai-proposed leg)
```

### Document structure

```yaml
- statement: A prompt file is an H1 section containing a lua preamble fence, prose, and a lua epilogue fence, followed by H2 sections; the H1 is required, and anything between the YAML front matter and the H1 is ignored; within a section the lua fence comes before the prose, so a preamble can never be confused with an epilogue.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p6-p12], [p23]; 2026-08-14-1613-promptforge-core-largest-part1.md [p7], [p22], [p23]
  rejected-alternative: a trailing lua code fence after the section body; meaningful content between front matter and H1
  endorsement: n/a

- statement: H2 is a subhead and H1 is not; every subhead's first word must be a valid identifier, lowercase-normalized, with anything after whitespace on the heading line an ignored comment; H2 names are unique across the file and H3 names unique within their parent section.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p381], [p391-p395]; 2026-08-02-1134-mcp-client-large-part5.md [p381], [p391], [p392], [p393], [p394]
  rejected-alternative: none
  endorsement: n/a

- statement: Prompt documents support nested sections recursively from H2 through H6, and heading levels execute under identical rules at every level: an H3 falls through to the next H3 exactly as an H2 falls to the next H2, and "---", jump(), and execute() work the same way at each level, scoped to that heading's siblings and its children one level down.
  scope: core
  source: user-stated
  citation: 2026-08-02-1134-mcp-client-large-part3.md [p137]-[p144]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p144]; 2026-08-19-0048-promptforge-md-aug19.md [p39], [p40]
  rejected-alternative: per-level execution semantics
  endorsement: n/a

- statement: A horizontal rule "---" marks a section to be skipped by execution and fall-through, and content after it is expository prose for the reader that does not affect execution; the rule is uniform with no special casing (the blank line is required), survives the user cutting and pasting sections around, and applies even when the rule appears at the start of a section reached by a chain.
  scope: core
  source: user-corrective
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p26], [p30], [p32], [p35], [p65]; 2026-08-02-1134-mcp-client-large-part5.md [p382], [p383], [p387], [p388], [p389], [p390]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p382-p389], [p390]
  rejected-alternative: special-cased parsing of horizontal-rule placement; positional control-flow markers whose meaning depends on where they sit in the file
  endorsement: n/a

- statement: Fall-through never crosses heading levels; the transfer from HN to H(N+1) must be explicit (jump or execute), and once the transfer happens the sibling walk proceeds normally at the deeper level.
  scope: core
  source: user-stated
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p41]; 2026-08-02-1134-mcp-client-large-part5.md [p400], [p401]
  rejected-alternative: implicit fall-through from a parent level into its children
  endorsement: n/a

- statement: XML blocks may appear anywhere in the document; the harness extracts them into a table, nothing inside XML tags counts as prompt text, and XML is reserved for model-facing markup, not for the harness's grouping - section headings are the grouping mechanism, and no heading level is special.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-07-30-0534-promptforge-design-context.md [p41], [p53], [p54]
  rejected-alternative: XML tags as the harness's grouping and batching system; restricting references to one designated heading level
  endorsement: n/a

```

### Control flow

```yaml
- statement: Falling through to the next section is the default control flow and is context-clearing - sequential fall-through never accumulates context - and running off the last section ends the run with a default completion message the YAML front matter can override, so termination is always well-defined; fall-through is a property of the executor over the markdown, never of Lua.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-07-28-2238-orchestrator-design-continued.md [p75, p121]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p75, p121]; 2026-08-02-1134-mcp-client-large-part2.md [p75], [p121]; 2026-08-02-1134-mcp-client-large-part5.md [p363], [p414], [p415]; 2026-07-30-0534-promptforge-design-context.md [p9], [p10]
  rejected-alternative: requiring an explicit exit or transition from every section; implementing fall-through inside the Lua block; fall-through that appends each section into a growing shared context
  endorsement: n/a

- statement: jump() (formerly goto) destroys the current context and starts a fresh context from the target section's prompt with only the passed string, params, and state-store access; the value passed on a control-flow transfer is explicit and visible in the prompt source, and the model's previous reply is always available in the single variable reply, which a jump carries into the destination section.
  scope: core
  source: user-stated
  citation: 2026-07-28-0925-orchestrator-design-document.md [p14, p74, p75]; 2026-07-28-2238-orchestrator-design-continued.md [p14, p75, p120]; 2026-07-30-0534-promptforge-design-context.md [p12]-[p18]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20], [p21], [p22]; 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481]
  rejected-alternative: compacting the transcript to make room in a continuing context; jump() dropping the reply; three separate variables incoming_reply, reply, and last_reply
  endorsement: n/a

- statement: execute() runs a referenced section as a subroutine in a fresh VM and returns its reply to the caller; it starts a new chain that runs to its end, is recursive, and reuses the engine's existing section-execution machinery, while jump() transfers control with no return.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]; 2026-08-09-1058-promptforge-core-large-part5.md [p430, p432, p433]; 2026-08-19-0048-promptforge-md-aug19.md [p55], [p58], [p60]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p242]
  rejected-alternative: an asymmetric model where an execute-entered subroutine may not jump; treating goto-with-return as a reusable multi-call-site function
  endorsement: n/a

- statement: A section ends when the model replies with text and no tool calls, and that text becomes the run result; tool calls made during a prose tool loop count as output, so the model is not required to spend tokens on filler text; the empty-turn clean exit applies only when finish_reason is "stop" and at least one tool call was successfully dispatched earlier in the loop, binding reply to the empty string, and otherwise an empty turn fails closed as EmptyModelReply.
  scope: core
  source: ai-proposed; user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [STATUS.md decisions]; 2026-08-03-1827-two-repo-commit-review.md [design documents section]; 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p3], [p6], [plans section]
  rejected-alternative: an explicit termination call required to end a section; requiring a non-empty text reply to validate a turn; accepting any empty turn once a tool call has occurred
  endorsement: affirmed

- statement: Cyclic section calls are permitted because some tools require cycles; runaway execution is bounded by budgets (nesting limit, step budget, tool budget), not by structural prohibition, and with subroutines, jump, and goto allowed, the same hazards as any programming language apply - coherence is the prompt author's responsibility, not the engine's.
  scope: core
  source: user-corrective; user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [p369-p372]; 2026-08-02-1134-mcp-client-large-part5.md [p369], [p371], [p372]; 2026-08-19-0048-promptforge-md-aug19.md [p60]; 2026-07-28-0925-orchestrator-design-document.md [p18]
  rejected-alternative: restricting calls to an acyclic graph; engine-enforced guardrails on control flow
  endorsement: n/a

- statement: A task is either synchronous or asynchronous: a synchronous task behaves like a function call with a context reset, an asynchronous task requires a rendezvous, launching one immediately returns a unique timestamped ID by which the model can cancel it, and when a section with a pending async task moves on or returns, the pending task is cancelled and the section receives a cancellation message; a fork spawns an asynchronous task while the caller falls through, and forks are not required to rejoin.
  scope: core
  source: user-stated
  citation: 2026-07-30-0534-promptforge-design-context.md [p22], [p23], [p26], [p27], [p28], [p34], [p35]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]; 2026-08-02-1134-mcp-client-large-part4.md [p245], [p246], [p247]
  rejected-alternative: requiring forks to always come together
  endorsement: n/a
```

### Lua environment

```yaml
- statement: Embedded Lua is kept minimal - putting too much logic in Lua re-implements the orchestrator inside the markdown and defeats the purpose - and a section's Lua block runs in a sandbox: the user cannot declare arbitrary globals, only a fixed set of host objects is accessible from prompt code, the standard library is restricted to safe subsets (no io/os/require/load/package/debug), and an instruction-count hook aborts a runaway block; Lua has equal access to the virtual file system and is not a second-class citizen; access control applies to the model, not to Lua - every H2 section that injects tools also injects which files those tools may access, while Lua code itself can read and write both real files and memory files.
  scope: core
  source: user-stated; user-corrective; ai-proposed
  citation: 2026-07-28-0925-orchestrator-design-document.md [p68]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p71]; 2026-08-02-1134-mcp-client-large-part5.md [plans: lua args substitution], [p349]; 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p349]; 2026-08-09-1058-promptforge-core-large-part4.md [p368]; 2026-08-14-1613-promptforge-core-largest-part4.md [p368]
  rejected-alternative: an orchestrator written in Lua embedded in the markdown file; arbitrary user-declared globals; protecting the machine by restricting the Lua API instead of the prompt's tools; sandboxing Lua so it cannot write files
  endorsement: unaddressed (ai-proposed leg)

- statement: A prompt's key-value parameters are read-only and visible to every section and to any Lua anywhere in the prompt, so values never have to be passed from section to section; Lua state is substituted into prompt text through a substitution syntax that makes prompt assembly deterministic: substitution is single-pass, scalars render as strings, tables as JSON, and a missing key is a hard error; structured data passes between Lua and the model as JSON assembled in Lua and returned by the model via macro substitution, so structured return values are assembled deterministically rather than emitted by the model.
  scope: core
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p74]; 2026-08-02-1134-mcp-client-large-part2.md [p66], [p74], [p78], [p79]; 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: Lua args substitution], [p364-p365]; 2026-07-28-2238-orchestrator-design-continued.md [p66, p78]
  rejected-alternative: pydantic-style schema conformance with injected system-prompt overhead; model-conformant JSON produced under constrained decoding
  endorsement: affirmed (ai-proposed leg)

- statement: A single "```lua shared" chunk per prompt is compiled once and replayed in each section's fresh VM: compile errors surface before any section runs, the replay blocks tools, models, var, reply, and jump at the top level (a hard phase error naming the blocked global) while leaving them available inside shared functions called later, a second shared chunk or one after the H1 is an error, and an empty compiled chunk is substituted when no shared section exists so the startup path is unconditional; captured bindings install after the replay, so a tool or model alias wins a name collision with a shared global.
  scope: core
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p6], [p7], [p9], [plans section]; 2026-08-14-1613-promptforge-core-largest-part5.md [p461], [p462], [p474]
  rejected-alternative: replaying with the full environment and tightening later; branching section-startup logic on whether a shared section was specified; generic VM serialization and cloning
  endorsement: affirmed (ai-proposed leg)

- statement: The H1 preamble runs exactly once as a live preamble and can run model inference with tool calls, so the model can parse the argument string and take control before any section runs; per-section replay is abandoned because replay multiplies inference cost and corrupts state once the preamble can infer or write to the store; a scalar top-level return from either preamble or epilog ends the run, and nil continues sequential fall-through.
  scope: core
  source: user-corrective; user-stated; ai-proposed (affirmed)
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p446], [p470]; 2026-08-09-1058-promptforge-core-large-part5.md [p397], [p448-p450], [plans section: section-lua-lifecycle]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p25]
  rejected-alternative: two-phase preamble treatment and shared-bytecode re-execution in section VMs
  endorsement: affirmed (ai-proposed leg)

- statement: All Lua chunks in one H2 section share a single VM, so state passes between chunks through plain globals; the Lua environment is installed once on entry to an H2 and then left alone, with the tool schema computed fresh just before each prose call; an error in any Lua chunk stops the entire prompt run; Lua chunks return values with Lua's native return semantics; and the store is the only intentional mutable channel across sections - functions, closures, globals, var, tools, and reply are branch-local by construction, mutable run-global Lua is explicitly excluded, and after the H1 preamble runs the prompt-global Lua state becomes read-only, with each fanout arm receiving its own copy of shared functions.
  scope: core
  source: user-corrective; user-stated; ai-proposed
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p103], [p124], [p125], [p127], [p149], [p154]; 2026-08-02-1134-mcp-client-large-part4.md [p234], [p235]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: section-lua-lifecycle]; 2026-08-09-1058-promptforge-core-large-part5.md [plans section: section-lua-lifecycle]; 2026-08-09-1058-promptforge-core-large-part1.md [p15-p21]
  rejected-alternative: per-chunk environments with closures re-installed between blocks; a tool loop that mutates the environment between blocks; continuing the run past a chunk error; a declared identifier or descriptor inspected by the Rust side; mutable run-global Lua state; shared mutable global state across fanout arms
  endorsement: corrected (one leg affirmed)

- statement: Tools and models are first-class Lua objects - inspectable, invocable tables, a model exposes infer()/turn() - which makes them mockable in unit tests, and the preamble can declare globals such as lists of tools usable in any section; the toolset is not sealed at the first inference, so tools.add between inference rounds within a section keeps working.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p398], [p400], [p401], [p409]; 2026-08-09-1058-promptforge-core-large-part5.md [p398-p401], [p409]
  rejected-alternative: treating tools and models as opaque registrations; sealing the toolset when infer begins
  endorsement: n/a

- statement: infer() is a blocking call with a fresh context: a string goes in and a string comes out, with no tools, no shared conversation history, and no reply side effects, using the model selected for the H2.
  scope: core
  source: user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p165], [p182]
  rejected-alternative: infer with tools and history, and a two-argument infer that picks a model per call
  endorsement: n/a

```

### Tool scoping and declaration

```yaml
- statement: Per-section tool scoping is opt-in: a section receives only the tools its Lua block names with tools.add(), a section that names no tools gets none, and a scoped name absent from the run's tools is a hard error never silently dropped; the offered surface stays small enough for a small orchestrator model (roughly five to seven tools) and is specialized per section - a section that always falls through gets no control-flow tool injected at all - and tool availability can be scoped by turn within a section, e.g. only web_search on the first turn; constraining a section's toolset must not otherwise change its behavior, and the conversation history is never rewritten to scrub tool offerings or calls, because the model would see information appearing out of nowhere.
  scope: core
  source: ai-proposed (affirmed); user-stated; user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: per-section tool scoping]; 2026-08-02-1134-mcp-client-large-part5.md [plans: per-section tool scoping]; 2026-07-28-2238-orchestrator-design-continued.md [p17, p85, p119]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p61], [p63], [p64]; 2026-08-02-1134-mcp-client-large-part2.md [p85], [p119], [p120]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p163], [p164], [p222]; 2026-08-09-1058-promptforge-core-large-part4.md [p372]
  rejected-alternative: opt-out scoping where a section starts with all frontmatter tools; a constrained-toolset formulation that alters section behavior; scrubbing the tool offering and tool call from history; making all of a section's tools available on every turn
  endorsement: affirmed

- statement: There is exactly one tools.add entry point; naming an unknown tool alias is a hard error with clear diagnostics; tool references are scoped, not globally "registered", so naming an unscoped yet global tool is a hard error; a tool's call budget is declared at the tools.add call site; and turn limits are a property of the subagent expressed as config.max_turns, with exhausting the budget removing all of the subagent's tools.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p90], [p170], [p175], [p176]; 2026-08-09-1058-promptforge-core-large-part4.md [p271], [p272], [p273]; 2026-08-09-1058-promptforge-core-large-part3.md [p175], [p176]
  rejected-alternative: multiple overloaded versions of tools.add; silently ignoring unknown aliases; a global tool registry where any name resolves; attaching max_turns to individual tools
  endorsement: n/a

- statement: A prompt can assert postconditions on tool usage in its epilogue, e.g. assert(tools.calls["search"] > 0); the count is per-VM, a failed tool call still counts as a call because assertions measure whether the model is performing, not whether the tool is performing.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p265], [p266], [p268], [p271]; 2026-08-14-1613-promptforge-core-largest-part3.md [p265], [p266], [p268], [p271]
  rejected-alternative: counting only successful tool calls; a dedicated require_called directive
  endorsement: n/a

- statement: A tool can be implemented as an inline Lua function acting as a front end to a real tool, registered from any Lua chunk in the H2 and effective for the next prose call, with a parameter schema derived from its function declaration and the same capabilities as native tools - including enabling further tools at call time, which the prompt author's opt-in legitimizes; Lua tool handlers cannot jump, though ordinary section Lua can.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p99], [p117], [p120], [p144], [p160], [p162], [p163]; 2026-08-09-1058-promptforge-core-large-part4.md [p373], [p374]; 2026-08-14-1613-promptforge-core-largest-part4.md [p373]
  rejected-alternative: requiring a Rust function for every tool; schema-less local tools presenting only name and description; allowing jump() from tool handlers
  endorsement: n/a

```

### State and context

```yaml
- statement: State is built through flat tool calls into a persistent store, not returned out of the model as structured output; propagating state is a single tool call carrying all values at once, not one tool call per value.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-07-28-0925-orchestrator-design-document.md [p13]; 2026-07-28-2238-orchestrator-design-continued.md [p13, plans section]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p228], [p265]
  rejected-alternative: Pydantic structured output passed out of the model orchestrator; one set call per value
  endorsement: n/a

- statement: The store is a virtual filesystem for file-shaped intermediate values in analytical pipelines - strictly for debugging and resume, not a general-purpose filesystem for agentic coding; it exposes real files and virtual (memory) files at the same time, and intermediate run artifacts must not surface as stray user-visible files.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p504], [p505]; 2026-08-14-1613-promptforge-core-largest-part4.md [p367]; 2026-08-09-1058-promptforge-core-large-part3.md [p162]
  rejected-alternative: a general-purpose filesystem supporting string replacement and delta application; a store model that supports only one kind of file at a time; a store that is literally the file system
  endorsement: n/a

- statement: State is carried as a key/value block written by Lua and injected into the context on every jump, with the executor choosing the enclosing tag; on a tool call in a multi-turn context, the facts bag is removed from the transcript, the tool results are injected, and then the facts bag is added back; the context must not accumulate permanent residue across turns; context needs are declared by the prompt's Lua and injected by the engine - the model does not pull them.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p254]-[p260], [p287], [p288], [p290]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p257], [p288], [p290]
  rejected-alternative: leaving the facts bag permanently in the transcript; accumulating permanent entries in the context; the model requesting context items itself
  endorsement: n/a
- statement: The engine exposes system facts to prompts through a sys object - sys.when for launch time, sys.now for the current time, and a unique incrementing id per context; accessing a name that is not in the sys table is a hard error, never a silent empty value; the effective model name is exposed as sys.model, usable in prose substitution and in Lua, and is unavailable during the prologue because it exists only after the section's model scope closes.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-02-1134-mcp-client-large-part4.md [p284], [p285], [p286]; 2026-08-08-0029-promptforge-context-planning.md [p15]; 2026-08-08-1223-gateway-local-inference.md [p54], [p55]; 2026-08-02-1134-mcp-client-large-part5.md [p419], [p420]
  rejected-alternative: silently returning nil for unknown sys fields; putting model in the initial pre-preamble sys object
  endorsement: n/a
```

### Trust

```yaml
- statement: Content arriving from external sources is untrusted and injection-prone: wrapping is done by a global function untrusted(s) that takes any string and wraps it with the injected tag and the machine instruction to treat the contents as data, not instructions; attacker-controllable tool output is automatically wrapped when the tool declares an untrusted-output property, with marker strings inside the content escaped so the delimiter cannot be forged, and content that forges the envelope's open or close tags is defanged before injection.
  scope: core
  source: user-corrective; user-stated; ai-proposed
  citation: 2026-08-19-0048-promptforge-md-aug19.md [p3], [p4], [plans section]; 2026-08-08-0029-promptforge-context-planning.md [p17], [plans section]; 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: guard-wrap untrusted tool output], [p333-p335]; 2026-08-14-1613-promptforge-core-largest-part2.md [p159], [p161]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p110]
  rejected-alternative: an inject method on the store (store.inject is removed, not kept as sugar); injecting stored content into the context raw; a separate safe-fetch tool chosen per call
  endorsement: corrected (ai-proposed leg)

- statement: The store's read API is split by trust and presentation: read_lines returns numbered lines for editing, read returns verbatim contents for trusted handoff, and injection to the model goes through the untrusted envelope; line numbers are a navigation and editing aid, not a security control - trust is carried by the envelope alone.
  scope: core
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-08-0029-promptforge-context-planning.md [p22], [plans section]; 2026-08-19-0048-promptforge-md-aug19.md [p12], [p16], [p17], [p18]
  rejected-alternative: a single read call with a trusted/untrusted flag; treating numbered output as safe for model consumption; a (startLine, lineCount) range form; a global numbered() function composing strings in memory
  endorsement: affirmed (ai-proposed leg)

- statement: When fetched evidence is unusable, the run aborts rather than continues, because a hallucinated evidence packet taints the entire downstream result.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p174]; 2026-08-09-1058-promptforge-core-large-part3.md [p173], [p174]
  rejected-alternative: soft-returning fetch failures and letting the prompt hallucinate past them
  endorsement: n/a
```

### Errors and observability

```yaml
- statement: Every error reported to the prompt author carries the source file and line number in the prompt that produced it, including assertion failures; misusing an API function produces a warning rather than silent wrong behavior.
  scope: core
  source: user-corrective; user-stated
  citation: 2026-08-18-1126-promptforge-md-aug18-morning.md [p54]; 2026-08-14-1613-promptforge-core-largest-part3.md [p279], [p280], [p313]; 2026-08-09-1058-promptforge-core-large-part4.md [p279], [p280], [p313]; 2026-08-14-1613-promptforge-core-largest-part2.md [p164]; 2026-08-09-1058-promptforge-core-large-part2.md [p86]
  rejected-alternative: errors that lack the prompt's file and line location; silently accepting the wrong function with no warning
  endorsement: n/a

- statement: Every harness operation reports its activity to an optional caller-installed observer, with trace events reduced to a Section string and a Detail string; prompts have a log() facility whose output is concurrency-safe and tagged with a per-execution id, available in both the shared chunk and the section chunks, with print disabled or remapped to it; runs are observable - logs expose what the engine wrote into each produced artifact; and fanout arm boundaries are logged as fixed, payload-free detail lines.
  scope: core
  source: user-corrective; user-stated; ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p39-p40], [p53-p56]; 2026-08-14-1613-promptforge-core-largest-part1.md [p39], [p40], [p55], [p56]; 2026-08-19-0048-promptforge-md-aug19.md [p6]; 2026-08-09-1058-promptforge-core-large-part2.md [p97], [p105]; 2026-08-08-0029-promptforge-context-planning.md [plans section]
  rejected-alternative: a taxonomy of typed trace event structures; logs that omit what went into run artifacts
  endorsement: unaddressed (ai-proposed leg)

- statement: Run artifacts are written incrementally as turns complete and files arrive, not buffered and dumped at the end of the run; each run deletes the previous trace on launch (a developer who wants to keep a trace backs it up himself); intermediate values produced during a run are examinable, because inspecting them is how runs get debugged, and an analytical pipeline persists intermediate outputs as files so any step can be re-run during development and debugging.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p290], [p298], [p299]; 2026-08-14-1613-promptforge-core-largest-part3.md [p290], [p298], [p299]; 2026-08-14-1613-promptforge-core-largest-part2.md [p128], [p165]; 2026-07-28-0207-architect-vibe-planning-part1.md [p3]; 2026-08-14-1613-promptforge-core-largest-part5.md [p377]; 2026-08-09-1058-promptforge-core-large-part5.md [p377]
  rejected-alternative: waiting to write all JSON turn files at the end; accumulating trace files across runs
  endorsement: n/a
```

### Models

```yaml
- statement: Models are declared in the prompt's introduction via models.add with attributes like thinking and context size; a prompt can declare a prompt-wide default model binding once in the H1 shared library; a section selects its model with model("name") exactly once in its first Lua block, inherits the prompt-wide default if it omits the call, may override the default for itself, and the choice locks for the rest of the section - any prose or inference before a model has been selected is an error, switching models means starting a new H2 with context carried forward explicitly through reply, and a subsection inherits its parent section's model; execution parameters such as context size, thinking, and resource caps are likewise properties of the prompt set in its Lua, never the frontmatter, the command line, or a gateway-level toggle, and analytical pipelines run at temperature zero.
  scope: core
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p107], [p108], [p154], [p205]; 2026-08-09-1058-promptforge-core-large-part2.md [p105], [p107], [p109]-[p112], [p142]; 2026-08-08-0029-promptforge-context-planning.md [p83], [plans section]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p62], [p67], [p168], [p175], [p177], [p179]; 2026-08-09-1058-promptforge-core-large-part3.md [p205, p206]
  rejected-alternative: declaring model settings in the frontmatter; models.only, an all-or-nothing lock that forecloses per-section overrides; non-inheriting model resolution; frontmatter keys or command-line flags for context_max_tokens and no_think; a gateway-level thinking toggle; nonzero temperature for analytical work
  endorsement: affirmed (ai-proposed leg)

- statement: Model binding is much looser than tool binding and resolves through the same semantic picker used for tools; a section's output contract is ordinary markdown regardless of which model slot executes it, so swapping the model behind a section does not change the section.
  scope: core
  source: user-corrective; ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p133]; 2026-07-30-0654-map-reduce-synthesis.md [design documents section]
  rejected-alternative: strict model-name binding that fails hard on mismatch
  endorsement: unaddressed (ai-proposed leg)
```

### Fanout

```yaml
- statement: Fanout is always invoked explicitly through a fanout() call - the engine never infers a fanout from the presence of a bullet list - and fanout's second parameter dispatches on type: a string names a list section, an array table is the collection, and anything else is a loud Lua error; list_from_section(name)/items() returns a section's parsed bullet items as an array of strings and can access only sibling sections at the same nesting level and child sections; the prompts passed to fan-out arms need not be known ahead of time.
  scope: core
  source: ai-proposed (affirmed); user-stated
  citation: 2026-08-08-0029-promptforge-context-planning.md [p35], [plans section]; 2026-08-19-0048-promptforge-md-aug19.md [p22], [p23], [p24], [plans section]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p45], [p108], [p109]; 2026-07-30-0534-promptforge-design-context.md [p50]
  rejected-alternative: inferring fanout from bullets without an explicit call; silently iterating a hash-keyed table in unstable order; rigid, statically fixed fan-out rules in Lua
  endorsement: affirmed (ai-proposed legs)

- statement: The subagent section is the arm template: its leading Lua is the shared preamble for every arm, its trailing Lua the shared epilog, and its prose substitutes the per-arm item; in a fanout the list section supplies only items and carries no Lua; each arm runs in a fresh VM built from the shared template and receives its per-arm values (the item text and a task id) through a sealed sys; arms are not special-cased - an arm executes through the same code path and the same functions as normal flow and can jump, execute, fanout, and list_from_section like any section; fanout is allowed whether or not a section has child headings.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-08-0029-promptforge-context-planning.md [p35], [p47]; 2026-08-19-0048-promptforge-md-aug19.md [p78], [p79]; 2026-08-19-0447-collapse-fanout-arm-review.md [p2]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p138]
  rejected-alternative: colocating the arm's Lua with the bullet list; overloading the section identity variable with per-arm data; stubbed control globals in arms; a separate arm-execution path with its own functions; restricting fanout() to sections with child headings
  endorsement: n/a

- statement: The invoking Lua owns the reduce step: fanout is a blocking call that returns each arm's final reply in order, replies stay ordered by arm index, the first arm error aborts its siblings with the same visible behavior as sequential fail-fast, the store stays shared and mutex-safe so authors must not assume arm N sees arm N-1 writes, and store writes from arm epilogs stay visible to the reducer; there is no limit on the total number of fanout items, only a limit on concurrent fanout; spoke identity is assigned by the harness, never calculated by the model.
  scope: core
  source: user-stated; user-corrective; ai-proposed
  citation: 2026-08-08-0029-promptforge-context-planning.md [p33]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: Fanout and gateway concurrency]; 2026-08-09-1058-promptforge-core-large-part5.md [plans section: Fanout and gateway concurrency]; 2026-08-19-0048-promptforge-md-aug19.md [p80]; 2026-07-28-0925-orchestrator-design-document.md [p67]
  rejected-alternative: a total item cap (max_fanout_items); the model computing each spoke's unique name or index; a wait-for-all barrier before the reduce step runs
  endorsement: unaddressed (ai-proposed legs)
```

## Boundary

*This layer covers the seams between components: core to gateway, prompt to tool bindings, picker to protocol, app to web content, caller to store. It prevents credential leaks, vendor lock-in, and the coupling that pins two components to each other's internals, by keeping secrets, endpoints, and schemas on exactly one side of each seam. Compressed to one sentence: every boundary has a single owner for each concern, and nothing crosses except through that owner's explicit, dumb interface.*

```yaml
- statement: The executor holds no vendor credentials, endpoints, or provider knowledge of its own - it is just a function call over caller-owned resources with no global state; a gateway owns the LLM credential and model-name routing, the executor talks only to the gateway, and it never knows whether a model is local or remote.
  scope: boundary: core<->gateway
  source: ai-proposed; user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part5.md [plans: gateway v0]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p215]; 2026-08-08-1223-gateway-local-inference.md [p16], [p18]; 2026-08-12-1534-dokuman-each-crate.md [design documents: report-template.md]
  rejected-alternative: the executor reading the vendor API key directly; an executor-level base_url setting; engine-owned global state shared across runs
  endorsement: unaddressed (ai-proposed legs)

- statement: Model-specific translation to and from tool calls is the gateway's responsibility, not the executor's; model download and caching live in the gateway, never in the core or the test harness - callers and tests supply only configuration naming the source URL and pin.
  scope: boundary: core<->gateway
  source: user-stated; user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p185], [p186], [p187]; 2026-08-08-1223-gateway-local-inference.md [p41], [p42]
  rejected-alternative: the executor handling per-model tool-call translation; core tests standing up llama-server and fetching GGUF weights themselves
  endorsement: n/a

- statement: Components do not share schema definitions - each side of a boundary owns its own schemas, because sharing them is unnecessary coupling - and the gateway must not depend on core.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part3.md [p190], [p191], [p192]; 2026-08-02-1134-mcp-client-large-part3.md [p190]-[p192]; 2026-07-29-0937-brave-web-search-tools.md [p11]
  rejected-alternative: a shared schema package used by both executor and gateway; the gateway linking against core
  endorsement: n/a
- statement: Secrets and privileged calls live only in the trusted backend and never reach an untrusted context: API keys never enter the model's context, the language's instructions explicitly forbid the model from reading any .env file, .env files are gitignored so secrets never enter version control, and app UI runs in the trusted context while third-party web content runs isolated.
  scope: boundary: gateway<->model; app<->web
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p6], [p18], [p19], [p22], [plans section]; 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Panel]
  rejected-alternative: passing the API key through the prompt or the core instruction file; making LLM calls from the frontend with the key present in the webview
  endorsement: affirmed (ai-proposed leg)

- statement: The executor receives a store instance as a parameter - the store is not part of the prompt; a prompt is agnostic to how its inputs arrive, and the gateway translates between the calling environment and the executor; store path derivation is the dev runner's policy, not the engine's; and the CLI and the MCP service share identical run semantics - same detection, tool selection, sandbox store, and executor - with no duplicated virtual file system or tool wiring between them.
  scope: boundary: mcp<->core; cli<->core; cli<->mcp
  source: user-stated; user-corrective
  citation: 2026-08-15-1851-modify-the-store.md [p2], [p12]; 2026-08-14-1612-file-backed-store-execution.md [p3]; 2026-08-02-1134-mcp-client-large-part5.md [p437]
  rejected-alternative: the engine owning store path policy; duplicating the vfs inside the MCP service
  endorsement: n/a

- statement: The tool picker depends only on an abstract tool-catalog type defined as its input contract - never on MCP, and never on Lua; the resolver returns tool descriptors, not concrete tools, and the caller maps a chosen descriptor to an actual tool; the resolver lives in its own crate, separate from the pure-protocol MCP client crate, so protocol-only consumers such as the CLI never load the matching model; and the Lua interface can add every tool from an MCP client in one call and ask for a tool that matches a description.
  scope: boundary: tool-picker<->mcp; tool-picker<->lua; tool-picker<->core
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-02-2331-mcp-client-evening.md [p11], [p20], [p21], [plans section]; 2026-08-02-1034-mcp-client-harness.md [p11], [p78], [p79]; 2026-08-02-1419-mcp-client-continued.md [design documents section]
  rejected-alternative: a direct MCP dependency inside the picker; a Lua dependency inside the picker crate; returning dyn Tool and taking a dependency on the core crate; embedding the resolver in the MCP client crate; requiring each tool to be named individually
  endorsement: affirmed (ai-proposed legs)

- statement: Integration tests require an already-running, already-configured gateway - the test never launches the gateway itself - while a small local model is kept runnable without the gateway so integration tests can exercise real inference with a simple setup; models are reached through the gateway rather than through bespoke direct wiring in the test harness.
  scope: boundary: tests<->gateway; core<->gateway
  source: user-corrective; user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part2.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part3.md [p201], [p202]; 2026-08-09-1058-promptforge-core-large-part2.md [p140]
  rejected-alternative: tests spawning their own gateway instance; wiring a local model directly into core-tests, bypassing the gateway
  endorsement: n/a

```

## Gateway / MCP / CLI

*This layer covers the services around the core: the gateway that owns credentials, concurrency, and normalization; the MCP server that serves prompts as commands; the tool resolver that binds needs to tools; and the CLI dev runner. It prevents rate-limit violations, silent configuration drift, ambient tool selection, and noisy client surfaces. Compressed to one sentence: all authority over the outside world concentrates in one explicitly configured process, and every other component stays a thin, deterministic client of it.*

### Gateway

```yaml
- statement: All inference traffic bottlenecks through a single gateway process that enforces global concurrency limits across all apps, languages, and machines: loopback connections require no API keys while remote access uses whitelisted IPs or API keys, exactly one machine holds the provider API key because global rate limits cannot otherwise be enforced, and gateways chain - a local gateway can forward to a company gateway that forwards to a remote endpoint.
  scope: gateway
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p116]; 2026-07-28-2238-orchestrator-design-continued.md [p116]; 2026-08-08-1223-gateway-local-inference.md [p16]; 2026-07-30-1046-compaction-algorithm-large-part3.md [p211]; 2026-08-02-1134-mcp-client-large-part3.md [p211], [p216]-[p218]
  rejected-alternative: each application managing its own inference concurrency; distributing provider keys across multiple machines
  endorsement: n/a

- statement: The gateway multiplexes many competing callers onto shared inference hardware and owns the queue and the concurrency limits: concurrency limits attach to hardware devices, not models, with an admin grouping the models and endpoints that share one physical device under a single limit; within a device, named lanes keep a fast utility model from queueing behind a long generative call; queued requests are scheduled fairly across callers, round-robin; and a full queue rejects requests immediately with backpressure (HTTP 503) rather than queueing without bound.
  scope: gateway
  source: user-stated; ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [p18], [p25], [plans section]; 2026-08-09-1058-promptforge-core-large-part4.md [p305], [p307]; 2026-08-14-1613-promptforge-core-largest-part3.md [p305], [p306], [p307]
  rejected-alternative: building concurrency limits into the prompt executor; per-model limits; one flat concurrency limit per local device; unbounded queueing
  endorsement: affirmed (fairness leg); unaddressed (lanes and backpressure legs)

- statement: Gateway configuration is organized into named profiles, each a complete package of models and settings sized to fit the hardware and suited to a specific workflow: the gateway runs exactly one profile at a time, never auto-selects, profiles can inherit other profiles recursively, profile switching is available through a remote admin command and is immediate rather than graceful (in-flight local requests are dropped), and when the active profile changes the model catalog changes with it, so executors must re-fetch the catalog on their next run.
  scope: gateway
  source: user-stated; user-corrective; ai-proposed
  citation: 2026-08-08-1223-gateway-local-inference.md [p35], [p36], [plans section]
  rejected-alternative: one general-purpose configuration holding every model at once; auto-selecting a profile; graceful drain of in-flight requests before switching
  endorsement: unaddressed (ai-proposed leg)

- statement: Configuration is a hierarchy of TOML files in which a common base file is inherited by model-specific files; the shared config never mentions specific models - anything naming a model lives in that model's own config file, including its concurrency value - and configuration key names follow the provider's own terminology.
  scope: gateway
  source: user-stated; user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part3.md [p220], [p221], [p222]; 2026-08-14-1613-promptforge-core-largest-part3.md [p220], [p221], [p222], [p309], [p310]; 2026-08-16-1229-promptforge-md-aug16-midday.md [p24], [p28]
  rejected-alternative: naming qwen or gemma inside common.toml; inconsistent or invented key names across the repo
  endorsement: n/a

- statement: All provider-specific special cases and wire quirks - field synonyms, empty content, tool-call-with-null-content - enter through one normalization layer behind clean interfaces with no hardcoding, so hosts stay dumb; each dialect is a self-contained pluggable module, one source file per dialect; adding a model never requires the operator to set its dialect because the system discovers it; prompts stay dialect-agnostic - the operator declares each model's tool dialect on the gateway, the gateway advertises it, core freezes it onto the bound model, and an unknown dialect id is a hard error with no silent fallback; an empty model response is always a hard fail (a tool call counts as a model response); reasoning_content is never promoted into the answer; and missing gateway credentials produce a clear, specific error rather than an opaque tool-bind failure.
  scope: gateway
  source: user-stated; ai-proposed
  citation: 2026-08-09-1058-promptforge-core-large-part4.md [p250], [p253], [p254]; 2026-08-14-1613-promptforge-core-largest-part3.md [p250], [p253], [p254]; 2026-08-14-1613-promptforge-core-largest-part2.md [p99], [p124], [p126]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: completion normalize layer]; 2026-08-09-1058-promptforge-core-large-part5.md [plans section: completion normalize layer], [plans section: Tool dialect plugins]
  rejected-alternative: scattering per-provider special cases throughout the codebase; hardcoded per-model handling; operator-configured dialect per model; sniffing completion text in the prompt surface or hardcoding model names inside prompts; treating an empty response as a valid result; failing the tool bind with no explanation when the token is absent
  endorsement: unaddressed (ai-proposed legs)

- statement: The gateway resolves environment variables from the operating system environment directly, never through a shell, because it runs as a system service on production machines where no shell inheritance exists; every user-facing binary loads its .env file at startup before config interpolation resolves ${VAR} references; a missing .env file is not an error; and env-file resolution walks the config inheritance chain from the specified TOML all the way to the end, combining every .env file encountered along the way.
  scope: gateway
  source: user-corrective; ai-proposed (affirmed)
  citation: 2026-08-15-2006-promptforge-md-aug15.md [p4], [p5], [p11], [p12], [p13], [plans section]; 2026-07-31-1516-agentic-ide-research.md [p33], [p37]
  rejected-alternative: resolving variables through shell inheritance; failing startup when no .env file is present; stopping at the first encountered .env file
  endorsement: affirmed (ai-proposed leg); unaddressed (missing-.env leg)

- statement: Small utility models (embeddings, classifiers, rerankers) are co-located with the gateway rather than called over a network, and may run on CPU where that is enough; model sessions come in both streaming and non-streaming forms; a conversation never flips between physical endpoints, because switching endpoints loses the KV cache; long-running operations such as multi-gigabyte model downloads display graphical progress; and stale cache files are cleaned up automatically.
  scope: gateway
  source: user-stated
  citation: 2026-08-08-1223-gateway-local-inference.md [p19], [p20], [p21]; 2026-08-02-1134-mcp-client-large-part3.md [p170], [p210]; 2026-08-09-1058-promptforge-core-large-part3.md [p233], [p235]; 2026-08-14-1613-promptforge-core-largest-part3.md [p223], [p233], [p235]
  rejected-alternative: serving utility models from a remote endpoint; flipping one conversation across multiple endpoints; silent downloads with no progress indication
  endorsement: n/a
```

### MCP server

```yaml
- statement: The MCP server's sole role is serving PromptForge prompts: its published tool list is small and fixed (list_prompts, run_prompt, check_run, need_prompt) and never changes at runtime, a PromptForge prompt is a command that runs only because a caller named it - never because a model noticed a tool that looked relevant - and prompts are not advertised individually, so a prompt saved seconds ago is callable immediately with no reconnect and no list-changed machinery; tool descriptions are written in the register of a command interpreter, with no trigger phrasing that competes with a client's own tools for selection.
  scope: mcp
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p2], [p15], [p58], [p59], [plans section]; 2026-08-16-1229-promptforge-md-aug16-midday.md [p8], [p27]; 2026-08-02-1134-mcp-client-large-part5.md [p435], [p441]
  rejected-alternative: a broader server surface beyond prompt-serving; dynamic per-prompt tools with notifications/tools/list_changed; publishing each prompt as its own tool; tool descriptions optimized to win model selection; per-prompt advertisement
  endorsement: affirmed (ai-proposed legs)

- statement: The prompt directory is watched live and prompts reload without a server restart, and a prompt that breaks stays listed, carrying its error, rather than silently disappearing; boot validation refuses an incoherent catalog, with all failures accumulated and printed before a nonzero exit; a long-running run keeps the calling client informed with live progress notifications; and the server hard-codes no knowledge of any specific client or harness.
  scope: mcp
  source: user-stated; ai-proposed
  citation: 2026-08-03-2040-plan-the-mcp-server.md [p6], [p25], [p26], [p32], [plans section]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p122]
  rejected-alternative: requiring a restart or a new chat to pick up prompt edits; starting the service with only the valid subset of prompts; a bare admission timer with no progress signal; client-specific special cases such as Cursor-aware behavior
  endorsement: unaddressed (boot-validation leg)

- statement: The gateway owns the store lifecycle: it reads caller-specified input files into the store itself so file contents never pass through the orchestrating model's tokens, a caller supplies each input as either a file path or inline text (supplying both is a validation error) with the mapping deterministic and inference-free, the server validates that every declared input has a supplied value before seeding the store and executing, output extraction is best-effort (a declared output the prompt never wrote is returned as absent), output files go to real paths chosen by the caller with permissions the orchestrator's responsibility, and when a prompt has one output file and no path mapping, the server returns exactly that file's contents with no separator line and no filename label.
  scope: mcp
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-15-1851-modify-the-store.md [p4], [p5], [p6], [p14], [p18], [p21], [p23], [plans section]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p29], [p30], [p31], [p39]
  rejected-alternative: the orchestrator inlining existing file contents into the tool call; an inference-based mapping of caller inputs; failing the run when a declared output is missing; the gateway managing output permissions itself; appending a decorated copy of the output after the chat reply
  endorsement: affirmed (ai-proposed legs)

- statement: Running a prompt separates one-time setup (gateway, MCP server, metadata discovery) from the repeatable call: list_prompts is called once per session and the metadata stays in context, a prompt's parameter mapping is learned at runtime from the server's description of the prompt's metadata and never hardcoded into the skill, and a prompt call is error-driven - the agent calls run_prompt without pre-validating and reports whatever comes back, letting the server's error be the feedback.
  scope: mcp
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p5], [p7], [p9], [plans section]
  rejected-alternative: repeating the full setup procedure on every invocation; re-querying prompt metadata on subsequent invocations; hardcoding an understanding of args into the procedure; pre-validating the prompt's existence before calling
  endorsement: affirmed (ai-proposed legs)

- statement: The MCP server has a single flat environment file - hierarchical environment files belong to the gateway's configuration alone - loaded name-matched beside its config just like the gateway, with the process environment winning over the file, env-file values held in memory only and never leaked into the process environment, and hot-reloading the config also picking up env-file changes; default configuration enables no tools, so every tool is opt-in and the sandbox is real; and local MCP prompts live in a gitignored directory where dropping a prompt file makes the prompt live.
  scope: mcp
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-16-1229-promptforge-md-aug16-midday.md [p17], [p18], [p24]; 2026-08-18-1639-promptforge-md-aug18-afternoon.md [p7], [plans section]; 2026-08-15-1851-modify-the-store.md [p40], [p47]
  rejected-alternative: attaching the hierarchical env-file scheme to the MCP service; requiring manual env sourcing at startup; mutating the process environment; registering WebFetch and WebSearch by default
  endorsement: affirmed (ai-proposed legs)

- statement: Any prompt can be exported as an MCP tool purely from its YAML front matter (parameters plus description, with frontmatter-declared input and output files used for documentation and MCP schema generation); the MCP tool schemas are kept as small as possible so smaller models can fill them in correctly; the service is long-running rather than launched per invocation, holding its prompts, libraries, and models loaded once; and the server can itself act as an MCP client to other services, while prompt-to-prompt calls inside a run never round-trip through MCP.
  scope: mcp
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p122]; 2026-07-28-2238-orchestrator-design-continued.md [p122]; 2026-08-02-1134-mcp-client-large-part5.md [p440]; 2026-08-15-1851-modify-the-store.md [p13], [plans section]
  rejected-alternative: a stdio service the editor launches and tears down on every call; exposing one tool per prompt to the editor
  endorsement: affirmed (frontmatter-files leg)
```

### Tool resolution

```yaml
- statement: Tool-need resolution runs locally and deterministically with no LLM in the resolution machinery - the same catalog, need, and config yield the same outcome across runs - and a matching technique is adopted only after it proves itself on measured tests against real data, never on intuition or synthetic benchmarks alone.
  scope: mcp
  source: user-stated; ai-proposed (affirmed)
  citation: 2026-08-02-1034-mcp-client-harness.md [p17], [p27]; 2026-08-02-1419-mcp-client-continued.md [p17], [p27]; 2026-08-02-2331-mcp-client-evening.md [p16], [p17], [plans section]
  rejected-alternative: an LLM-based matcher in the resolution path; adopting a classifier without empirical validation
  endorsement: affirmed (ai-proposed leg)

- statement: Tool selection is framed as ranking - given the catalog, which tool best fits the need - gated on a calibrated similarity floor plus a top-1-vs-top-2 margin, yielding exactly four outcomes: clear bind, own-catalog ambiguity (fail loud), foreign-server overlap (surface a shortlist of about three for a well-informed decider), and absence (fail loud, because abstention is a first-class resolution outcome); tool annotations such as readOnlyHint may improve confidence or break ties but are never required, and tool identity is the (server, tool) pair, never a concatenated name string.
  scope: mcp
  source: user-stated; user-corrective; ai-proposed (affirmed)
  citation: 2026-08-02-1034-mcp-client-harness.md [p13], [p56], [p61], [p66], [p69], [design-mcp-toolpicker.md section], [rationale.md section]; 2026-08-02-1419-mcp-client-continued.md [p25], [p56], [p61], [p66], [p69], [plans section]
  rejected-alternative: asking of each tool separately "is this a fit"; forcing a single top-1 answer in all cases; binding to the nearest tool regardless of confidence; depending on annotations as a necessary input; routing on a concatenated server-plus-tool name string; silently picking among duplicates
  endorsement: affirmed (ai-proposed legs)

- statement: A prompt declares its tool needs at load time as a list of local aliases, each paired with a plain-language description of the capability it needs - need strings written in the prompt author's register as clean, parameter-free capability descriptions that read like a tool's own documentation - and the harness binds each alias to the best-matching available tool; an ambiguous or duplicate binding is an error, and after the H1 preamble runs the harness compares all bound tools pairwise and fails the prompt if any two are too similar to disambiguate; the schema attaches to the tool, not to the prompt, so fifty prompts sharing a tool do not repeat the schema fifty times.
  scope: core
  source: user-stated; user-corrective
  citation: 2026-08-02-1034-mcp-client-harness.md [p39], [p58], [p60]; 2026-08-02-1419-mcp-client-continued.md [p39], [p58]; 2026-08-09-1058-promptforge-core-large-part1.md [p27-p31], [p35], [p36-p37]; 2026-08-02-1134-mcp-client-large-part2.md [p90]
  rejected-alternative: hard-coded tool names in prompts; need strings phrased like runtime user utterances; silently allowing duplicate tool bindings; declaring the schema in each prompt's front matter
  endorsement: n/a

- statement: Static launch-time binding (add_need) and dynamic runtime discovery (choose_mcp_tool) are complementary surfaces that share one resolution engine: dynamic discovery is strictly opt-in - the only dynamic path, never an escalation the engine falls into on its own - and returns descriptors (one on a clear win, a shortlist on a genuine tie, a "no tools available" error on absence), never an invocation; on dynamic resolution the harness rewrites the context so the chosen descriptor sits before the prompt prose and the discovery exchange is excised, then re-generates, so a dynamically discovered tool lands in the identical execution state as a statically bound one; selection among a shortlist happens in the main context the author already governs, and for genuinely hard selection a strong reasoning model can select the tool and pass the descriptor through a context-clearing jump into a fresh context where a cheaper model executes.
  scope: mcp
  source: user-stated; user-corrective
  citation: 2026-08-02-1034-mcp-client-harness.md [p63], [p64], [p66], [p67], [p70], [p71], [p72]; 2026-08-02-1419-mcp-client-continued.md [p63], [p66], [p67], [p71], [p72], [design documents section]
  rejected-alternative: dynamic selection as an automatic escalation path; appending the discovery results to the context; a dedicated selection subcontext with its own model configuration
  endorsement: n/a

- statement: Tools are discovered, not declared: at load time the harness parses the prompt's Lua with everything stubbed, intercepts tool-registration calls, enumerates and deduplicates the required tools, fails to load with an error if any binding is missing, and offers a command that emits an empty bindings template for the user to fill in; prompts operate in a semantic space of abstract operations that know nothing about the storage backend, with a per-prompt configuration file binding each abstract tool to a concrete implementation, so the prompt says "search", never "search the web", and backends are never hardcoded into tools.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part2.md [p88], [p89], [p91], [p95]; 2026-08-02-1134-mcp-client-large-part2.md [p88], [p89], [p91]; 2026-07-28-2238-orchestrator-design-continued.md [p71, p88, p90, p91, p95]; 2026-08-14-1613-promptforge-core-largest-part5.md [p383], [p386]
  rejected-alternative: listing required tools in the YAML front matter; hardcoding the database backend into the tool; hardcoding the backend into prompt text and tool descriptions
  endorsement: n/a

```

### CLI

```yaml
- statement: There is a command-line dev runner that executes a prompt file with real inference, picks up what it needs from the prompt's directory, derives the store path from the prompt file (same directory, same stem, no extension, as a subdirectory), and shows debug logging, so prompts can be iterated quickly without extra infrastructure; interrupting with Ctrl+C cancels a concurrent run cleanly; and the program that puts a prompt into dev mode lives in its own crate, separate from the simplified test crate.
  scope: cli
  source: user-stated; user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part1.md [p76-p77]; 2026-08-14-1613-promptforge-core-largest-part1.md [p76], [p77]; 2026-08-14-1612-file-backed-store-execution.md [p3]; 2026-08-14-1613-promptforge-core-largest-part3.md [p317], [p318]; 2026-08-09-1058-promptforge-core-large-part4.md [p317]; 2026-08-09-1058-promptforge-core-large-part3.md [p203, p204]
  rejected-alternative: folding dev mode into the test crate
  endorsement: n/a
```

## Open questions

1. **Defaults.** "No defaults, everything explicit" (gateway-local-inference [p58]-[p62]) sits against "the engine implements all features and lets the caller decide among them, with sensible defaults" (mcp-client-large-part4 [p316]) and against "default configuration enables no tools" (modify-the-store [p47]) versus "fundamental tools are built into core" (brave-web-search-tools [p14], [p17]). The record never reconciles where defaults are permitted and where they are the enemy.
2. **Fanout scope.** Three positions survive: fan-out restricted to the fanning section's own children (promptforge-design-context [p39]), fanout allowed whether or not a section has child headings (promptforge-md-aug18-morning [p138]), and parallel analysis expressed as plain nested subsections with no explicit fanout mechanism (mcp-client-large-part4 [p272]-[p274]). The final rule is not pinned.
3. **Control-flow surface.** The record holds both a single unified control tool with a type discriminator (compaction-algorithm-large-part5 STATUS decisions; mcp-client-large-part1 [p65]) and named jump()/execute() functions (promptforge-core-largest-part5 [p442]; promptforge-md-aug19 [p55]). Later units appear to supersede earlier ones, but the merged record does not state that the unified-tool design is abandoned.
4. **Shared-chunk mechanics.** "The H1 preamble runs exactly once as a live preamble" with per-section replay abandoned (promptforge-core-largest-part5 [p446], [p470]) conflicts with the shared chunk being "compiled once and replayed in each section's fresh VM" under phase gating (promptforge-md-aug19 [p7], [p9]). Two different mechanisms both appear as current.
5. **Superseded design content.** "Preserved in a residue sidecar, not deleted" (plan-the-mcp-server [p64], [p65]) versus "the superseded documents are deleted" (repo-review-continued [p6]).
6. **Design-document direction.** "Running a plan generates the design document after implementation completes" (compaction-algorithm-large-part4 [p318]) versus "implementation begins only from a design document whose high-level decisions are already made" (architect-vibe-planning-part2 [p60]).
7. **Concurrency limits.** Per-model configuration values (promptforge-core-large-part4 [p305]-[p307]) versus limits attached to hardware devices with models grouped under them (gateway-local-inference [p25]).
8. **Static tool discovery.** Load-time discovery by stub-parsing the prompt's Lua is a landed principle, but the record also carries the unresolved doubt that Lua will be used for general-purpose computation, so static detection of every tool call may never be reliable (compaction-algorithm-large-part2 [p94]).
9. **Empty replies.** "An empty model response is never acceptable" (promptforge-core-largest-part2 [p124]) versus the conditional empty-turn clean exit (promptforge-md-aug18-afternoon [p3], [plans]). The later rule refines the earlier one, but the exact boundary - which empty turns fail closed - should be confirmed as fully specified.
10. **Weight of the untrusted envelope.** Guard-wrapping untrusted content is adopted and automatic, yet the record also notes the envelope is a probabilistic mitigation whose hard controls are scoping and context-clearing isolation (mcp-client-large-part5). How much the design may rely on the envelope is unstated.

## Not converted

The merged "Not converted" lists from all 51 packet units, deduplicated across units with citations combined. Items that graduated into surviving candidates during grouping are omitted; items that were convertible but dropped only at a per-unit candidate cap are marked (cap).

### Design philosophy and temperament

- API-lean and call-chain-lean matter to the author, not file-size lean; "bloated" means over-engineered call chains, not bundle size. [2026-07-31-1516-agentic-ide-research.md p7, p8]
- Technology choices are validated against ecosystem popularity and prior art before adoption. [agentic-ide-research p2, p40, p43, p44]
- Non-blocking robustness concerns are deferred explicitly ("we can worry about it later") rather than fixed on the spot. [agentic-ide-research p106, p107]
- Components are named and organized so separately developed repos can merge into one workspace later. [agentic-ide-research p12, p17, p20, p22]
- Model sovereignty: every design decision should make mid-size open-weight models reliable at roughly 1/100th of frontier API cost; self-hosted small models are preferred over frontier APIs for cost and speed independence. [orchestrator-design-document BLUF; map-reduce-synthesis design documents; mcp-client-large-part5]
- "Minimize the amount of inference" as a general instinct behind several rulings. [orchestrator-design-document p67, p69]
- The best engineers are lazy; the best kind of feature delivers everything with the minimal implementation. [mcp-client-large-part4 p231; compaction-algorithm-large-part4 p231]
- Earlier design documents are bloat to be mined for ideas, not followed; design-promptforge.md was called overengineered bloatslop. [mcp-client-large-part4 p232, p233; compaction-algorithm-large-part4 p232, p233]
- Architecture should be lean, slender, and good; scope creep that later proves necessary is accepted by definition, because that is what normalizing means. [promptforge-core-largest-part2 p122; promptforge-core-large-part2 p122, p124]
- Abstraction risks such as trait cosplay are discounted when removal is trivially easy. [promptforge-core-large-part2 p124]
- Defaults are interrogated against intuition before acceptance. [promptforge-core-large-part2 p106]
- Cost-of-change as a decision input: before adopting a design, ask how much churn it would cause in the source. [promptforge-core-largest-part4 p374]
- Deliberation before action: discuss a plan from all angles with pros and cons before editing it. [promptforge-core-largest-part4 p369]
- Prefer shipping the permissive, simpler design now and tightening later with evidence; noted in tension with the replay gate that was ultimately adopted. [promptforge-md-aug19 p11]
- A correct generalization should simplify the implementation by eliminating special cases. [promptforge-md-aug19 p43, p60]
- Ask for evidence before choosing an API shape, then answer from first principles when the evidence is already in hand. [promptforge-md-aug19 p17, p18]
- Efficiency instinct: an API that forces reading 5,000 lines to extract 400 is wasteful. [promptforge-md-aug19 p15]
- Delight in elegant synthesis wherever it comes from; the jump-into-child-walk solution was found by the AI and credited as luck. [promptforge-md-aug19 p66-p72]
- Less code to maintain beats bespoke machinery; prefer nil-ing out a table over building a dedicated error path. [promptforge-md-aug18-morning p53, p54]
- When a feature is removed, leave a short comment explaining why, written for a fresh-context reader. [promptforge-md-aug18-morning p162]
- A Lua tool that combines deterministic data with a one-shot inference is the most powerful operation available: determinism plus model judgment. [promptforge-md-aug18-morning p162]
- A silent no-op (tools.add between prose blocks) is taken as evidence of insufficient test coverage. [promptforge-md-aug18-morning p145]
- The primitives should feel like one family: fanout is like infer. [promptforge-md-aug18-morning p87]
- Instinct against duplicating data: pass store paths rather than copying section strings. [promptforge-md-aug18-morning p105, p106]
- An itch for a general cleanup pass that finds stale, redundant, or tightened code across the codebase. [promptforge-md-aug18-morning p134, p158]
- "Hell no to shellout" - no shelling out to subprocesses. [brave-web-search-tools p15]
- "I don't want a bunch of junk" - temperament about keeping dependencies lean. [brave-web-search-tools p21]
- Aversion to code paths that can theoretically fail but never actually do, because they produce code that appears to ignore errors. [promptforge-core-largest-part1 p20]
- Unshipped code earns no compatibility concessions: "there's no one to break"; nothing has shipped, so backward breakage is not a concern. [promptforge-core-large-part5 p395; promptforge-core-largest-part1 p24; promptforge-core-large-part1 p24]
- Encapsulation is plain programming hygiene; an abstraction earns its keep by being mockable and testable. [promptforge-core-largest-part5 p401; promptforge-core-large-part5 p401]
- Big changes get a deep, subagent-driven evaluation before adoption; thoroughness scales with blast radius. [promptforge-core-large-part5 p411]
- Minute-scale per-prompt latency is treated as a defect worth attacking, not a fact of life. [promptforge-core-large-part2 p81, p91]
- Heavyweight process rulebooks get lightened when they slow the development loop. [promptforge-core-large-part2 p116]
- Security mechanisms must justify themselves: asked whether the data-not-instructions preface actually makes a difference. [promptforge-context-planning p26]
- Names should come from vocabulary every prompt writer already owns: "reply" is right because everyone understands "the model's reply". [promptforge-context-planning p58]
- Ship the static form first and add the dynamic feature later. [promptforge-context-planning p63]
- A prompt is a work of art; the single-prompt format is loved for its own sake. [promptforge-design-context p4]
- The defining metaphor of the whole design: the markdown is the program, the model is the CPU, embedded Lua is the microcode, and the harness is the instruction decoder. [mcp-client-large-part5]
- Honest-limits temperament on guard-wrapping untrusted tool output: a probabilistic mitigation, not a boundary; the hard controls are scoping and context-clearing isolation. [mcp-client-large-part5]
- Sequencing preference: structure the work as the shortest line to a working Cursor integration and push all later complexity much later. [mcp-client-large-part5]
- Make a little progress on a lot of things instead of a lot of progress on a few; build the known quantity (the gateway) first while the control flow is still uncertain. [mcp-client-large-part3 p189; compaction-algorithm-large-part3 p189]
- Build order preference: easiest and most useful first, hardest and most risky last. [gateway-local-inference p38]
- Aesthetic conviction: there is something powerful about a small tool set plus prose with the model left to figure it out. [compaction-algorithm-large-part3 p158]
- The author works through an AI-driven workflow and feels layers of software between operator and machine; the design should collapse those layers. [gateway-local-inference p16]
- The gateway executable may be as big as it needs to be; operational simplicity beats binary size. [gateway-local-inference p16]
- Quantization quality bar: "Q4 sounds terrible" - skepticism toward heavy quantization for serious work. [gateway-local-inference p4]
- GPU support must not be forced on anyone; a machine without CUDA still gets a working gateway. [gateway-local-inference p46]
- Evaluate every design choice by whether it relieves context-window pressure so smaller models suffice - recorded both as a design heuristic and (in another unit) as a converted candidate. [orchestrator-design-continued; mcp-client-large-part2 p119]

### Process and workflow

- Hard-delete preference: when the user says delete, there is no trash staging step. [agentic-ide-research p25]
- Commit uncommitted WIP before starting plan work. [promptforge-core-large-part4 p259, p291]
- Preference for cribbing other people's code from the internet to make things work. [promptforge-core-large-part4 p253]
- A/B test thinking on/off across models and iterate until no axis improves; review code every 3 commits; stage quality targets against a baseline, log what works, roll back anything that regresses, minimize agent turns, and stop after three rounds without improvement. [promptforge-core-large-part4 p346, p348; promptforge-core-largest-part4 p346; promptforge-core-largest-part3 p319-p321]
- Staged definition of "beautiful" output: parity with local qwen, then surpass it, then three rounds of no improvement before switching subjects. [promptforge-core-large-part4 p320]
- Optimize web-search agents for as few turns as possible. [promptforge-core-large-part4 p321]
- Tranche-based plan implementation: put everything in one plan, implement a working subset, subtract it, and iterate across the executor, gateway, and MCP service. [mcp-client-large-part2 p123, p129; compaction-algorithm-large-part2 p123; orchestrator-design-continued]
- Repo bookkeeping: keep a cumulative status file (AGENTS.md at the root, not .mdc) that all changes must update so a fresh context knows the project state; AGENTS.md should carry a command that keeps the docs up to date on every commit. [mcp-client-large-part2 p130-p132; compaction-algorithm-large-part2 p130-p132; mcp-client-large-part3 p168]
- Review loops stop after one round of amend; more rounds only surface noise; exactly one round of review, edits made in the review context, because further rounds keep finding things forever. [promptforge-core-large-part2 p117; gateway-local-inference p45]
- One adversarial review per commit with fixes amended in, design doc and user docs kept current as work proceeds. [promptforge-context-planning p74]
- Plans are organized into discrete steps, each with tests, commit, review, fix, amend; each plan step includes a debt-reduction pass over every modified file; fix iterations are unlimited but review iterations are capped; tests are expected to pass at every commit. [collapse-fanout-arm-review]
- When a run goes sideways, stop and interrogate the state before touching anything: is the top commit better than before, and how much would a reset lose. [repo-review-top-to-bottom p10-p12]
- Wip commits pushed to the remote are a cheap backup and are kept. [repo-review-top-to-bottom p26, p27; repo-review-continued p26, p27]
- Reset, do not revert; force-pushing is fine on a solo repo. [repo-review-continued p15, p19, p20]
- Git history should be kept clean: rewrite out a revert commit and the commit it reverts rather than layering corrections. [dokuman-each-crate p29, p30]
- The improvised review process was preferred over the pre-written refactor-rust tool: faster and more grounded in reality. [repo-review-continued p49-p51]
- Trust the frontier model's competence instead of enumerating hygiene basics. [repo-review-continued p1]
- Much time is wasted because correction subagents keep making mistakes. [repo-review-continued p40]
- Run all jobs asynchronously so the conversation can continue; preference for asynchronous background research while prompting continues. [mcp-client-harness p23, p46; mcp-client-continued p46; promptforge-core-largest-part3 p255]
- Inspect raw data samples together before committing to a theory ("pick 30 descriptions at random... let's look at it together"). [mcp-client-harness p57; mcp-client-continued p57]
- Plans should ship with a separate rationale document that mines the chat history and explains the why behind the design; design doc first, then dataset, then reconcile the cited numbers; preliminary figures must be replaced by reproduced numbers, and any figure that moves enough to threaten a design choice gets flagged rather than silently patched. [mcp-client-harness p82; mcp-client-continued p75, p82, plans section]
- Working-style preference: do not commit, leave changes in the worktree, and return a terse status (done or blocked, files touched, test command) under a tight token budget. [file-backed-store-execution]
- Review is read-only: the reviewer reports findings and never fixes or commits anything itself; report back in under 80 words with the finding count and the most serious finding; write nothing for a check that passes. [two-repo-commit-review]
- When executing a plan, do not pause for reversible choices: make the plan's stated decision, record any necessary falsifier in design-core.md, and continue; preserve the original design document byte-for-byte as the historical record; fix every failure you introduce, running targeted tests as you proceed, then the full verification commands. [section-lua-lifecycle p1]
- Stating a fact is not a request: the user stopped the agent for making unrequested changes after being told only that cppa uses Jekyll. [dokuman-each-crate p23-p25]
- Demands complete test coverage for every change; "make fucking sure" is the temperament, not a rule. [promptforge-md-aug15 p14]
- Applies the standing rulebooks (rust, vibe) to all implementation work. [promptforge-md-aug15 p15]
- Clutter at the repository root is a defect. [promptforge-md-aug15 p24]
- Wary of dot-prefixed directory names confusing the IDE. [promptforge-md-aug15 p28]
- Everything should "just work" from a mention; impatience with manual steps. [promptforge-md-aug15 p5]
- Deadline temperament: "you will get it done in 2 hours". [gateway-local-inference p40]
- The user reasons that the tool-indirection layer only buys one saved round of inference, and that needs stated in prose could drive the tools.add list directly. [mcp-client-evening p9]
- The user weighs model tiers for subagent work, then declines to change anything and orders the run. [mcp-client-evening p31-33]
- Turnaround time on changes is painfully slow. [promptforge-core-largest-part2 p91]
- Preference for partial fine-tuning that buys a bounded improvement without degeneracy, rather than going "all the way". [mcp-client-harness p22]
- Eval data should be generated by multiple models (ChatGPT, Claude, Gemini, Cursor) to avoid same-generator bias; need strings derived by paraphrasing the descriptions of tools the author already intends to use. [mcp-client-harness p51; mcp-client-continued p51, p59, p60]
- A stream of clever matcher variants (vocabulary word-counts, noun/verb embedding channels, category routing, dynamic LoRA pools), all later measured and rejected: propose freely, then let measurement kill. [mcp-client-continued p28-p33]
- A fast, high-confidence "trivial reject" stage that tolerates false negatives but never false positives - proposed, later rejected as hard category routing. [mcp-client-harness p55; mcp-client-continued p55]
- The user interrogates every phrase of the rulebook; no wording survives unexamined. [architect-vibe-planning-part4 p208, p209, p211, p219]
- Before trusting the model's judgment, the user asks it to rate its own confidence. [architect-vibe-planning-part4 p187]
- Distrust quick confident answers; demand to see the actual mechanism, not a simulation of one. [architect-vibe-planning-part2 p85]
- Test your own prior before acting on it: verify that sharpening a sharply produced tool actually strips what you predicted it would strip. [architect-vibe-planning-part3 p158]
- A high-value, high-leverage audit warrants line-by-line comparison of original against sharpened output. [architect-vibe-planning-part3 p160]
- Wants the assistant to push back on weak designs and approve good ones, with more dialogue. [promptforge-context-planning p48]
- Prefers direct answers without hedging: "Don't fence answers". [promptforge-context-planning p51]
- Floats naming ideas as questions, expecting discussion rather than immediate execution. [promptforge-context-planning p45]
- Prefers compact tests, ideally plain markdown files and logging over Lua test harnesses. [promptforge-context-planning p70, p71]
- "This is a stinking pile of shit" - the user delivers blunt quality verdicts without criteria; the defect and fix direction must be inferred from the artifact. [recover-core-design-rationale p2]
- Vibe-coding for days without interim technical-debt refactors is what produced the findings pileup; the mess is self-diagnosed. [repo-review-top-to-bottom p30; repo-review-continued p30]
- The quality bar for the result: code getting smaller, clearer, bounded API surface, crisp, understandable, without the smell of AI slop smearing and bloating everything. [repo-review-continued p39, p44]
- The finished result must be chefs-kiss; the recurring worry is whether the work is making the code cleaner or just bloating and smearing it around. [repo-review-top-to-bottom p22, p23, p59]
- Flavor text must be genuine, lightly adapted Gibson fragments with every sentence reviewed for sense; nonsense imagery is called out by name. [repo-review-top-to-bottom p54-p57]
- Housekeeping preference: trim loose design/status files that create noise. [promptforge-core-largest-part5 p500, p501]
- Cuts to the design documents happen as they come up in conversation; no speculative purge. [promptforge-design-context plans section]
- Design documents are provisional and lower priority than the conversation, always; conversation decisions override anything written in them; the conversation is preeminent. [promptforge-design-context p5, p6, plans section; promptforge-core-large-part5 p432]
- Documentation workflow preference: integrate new design into the existing per-crate design docs instead of generating a new document. [modify-the-store p27]
- Rule-authoring philosophy: loosen a workspace rule with an "unless" clause and tighten rulebooks into standalone imperatives. [modify-the-store p34]
- Temperament about verified work: every commit must have tests that were actually run, confirmed commit by commit. [modify-the-store p56]
- Session-reuse goal for the quickref: services launched once should be remembered and reused across repeated prompt runs in the same chat. [modify-the-store p58]
- Plans should stand alone. [promptforge-md-aug19 p81]
- Build in the smallest testable increments: Lua first, then args, then substitution, with an echo tool as the first commit; fall-through as one testable thing. [mcp-client-large-part4 p250, p276, p293; compaction-algorithm-large-part4 p250, p276, p293]
- Every commit carries tests, code review, and docs, and each commit makes self-sufficient progress rather than needing a later commit to retroactively realize it. [mcp-client-large-part4 p292, p312; compaction-algorithm-large-part4 p292, p312]
- Keep a lightweight vibe-coding addendum (roughly one fifth of how-to-vibe-code) and inject it into the context periodically; loading how-to-write-prompts.md into plans "works like a miracle". [mcp-client-large-part4 p297-p302, p299; compaction-algorithm-large-part4 p297-p302, p299]
- Deeply nested task chains stay debuggable when each subtask is well tested and well defined - an engineering practice. [compaction-algorithm-large-part1 p19; mcp-client-large-part1 p19]

### Documentation and reporting craft

- Design documents should explain rationale and features, not just instructions. [promptforge-core-large-part1 p13; promptforge-core-largest-part1 p13]
- A design document should be richly detailed enough for any frontier model to produce working code including tests. [mcp-client-large-part1 p37]
- A design document is mostly why; code contains what, and where nothing forces a choice, that fact is worth stating rather than papering over. [plan-the-mcp-server plans section]
- The bet behind rationale recovery: most design choices are forced by constraints that are themselves visible in the code, so the why is largely recoverable. [plan-the-mcp-server plans section]
- Contingency is unrecoverable from code; numbers chosen inside a range, facts learned outside the repository, and deleted alternatives leave no trace, so a high open count is honest archaeology, not failure of effort. [plan-the-mcp-server plans section]
- "What lost and why" is the most valuable line a design document has. [plan-the-mcp-server plans section]
- The user wants prompts to be first-class citizens in the harness and research output delivered into the chat, not into side boxes. [plan-the-mcp-server p24]
- Documentation teaches progressively: one new concept per section, no forward references, every example a complete runnable prompt. [promptforge-core-large-part5 p436]
- Front-page documentation is crisp, bottom-line-up-front, dense and scannable - it says what the thing is rather than performing cool. [promptforge-core-large-part5 p440]
- A report should open experientially and take the reader on the same journey the author took. [architect-vibe-planning-part2 p94]
- An illustrative example may be approximate if it is close enough to reality to teach the reader. [architect-vibe-planning-part2 p98]
- Report-craft preferences (inverted pyramid, inline hyperlinks, answer-first headings) govern the design documents PromptForge produces, not the language or engine itself. [map-reduce-synthesis p2]
- Reports should put date and model on their own italic paragraph at the bottom - a per-prompt output formatting choice. [promptforge-core-largest-part2 p207]
- A report about bloat that is itself bloated fails on contact. [architect-vibe-planning-part4 plans section]
- Generated documentation belongs in the crate it documents, overriding default output routing. [dokuman-each-crate p1, p2]
- Assembling the combined user guide should be a program that does one thing, not a prompt. [dokuman-each-crate p5]
- The recovery plan's document-shape principles were never explicitly endorsed in that unit; the only user correction targeted its use of AskQuestion. [recover-core-design-rationale p4]

### Compression and blur theory

- Every time a model rewrites an artifact it resamples toward the mean of the distribution (top-k) and away from argmax, like gaussian blur in semantic space; only a significant correction counteracts it. [architect-vibe-planning-part1 p1, p3]
- First-pass generation is the sharpest pass: one pass, one prompt. [architect-vibe-planning-part1 p3, p4]
- The blur of a regenerated artifact is proportional to how many tokens of the input came from the model. [architect-vibe-planning-part1 p38]
- The output of a blurred plan can still be as sharp as the original, because the plan's design choices survive even when its rationale is sanded down. [architect-vibe-planning-part1 p47]
- No comparison algorithm, however good, prevents slow bloat over repeated regenerate-and-repair cycles; blurred content smears and takes up more space. [architect-vibe-planning-part1 p48, p49]
- Cropping a blurred plan makes it smaller but loses information each time, so over many cycles the plan returns to the same size with its instructions sanded down. [architect-vibe-planning-part1 p54]
- A model cannot sharpen without external information. [architect-vibe-planning-part1 p55]
- Open question the user kept circling: what operation shrinks a plan without blurring it, and how can a model compress without smoothing? [architect-vibe-planning-part1 p51, p53]
- Cursor plan files are machine-local and not portable via git; skills are the better portable mechanism today. [architect-vibe-planning-part1 p12, p22]
- Compression is the most valuable substance in the AI universe; the antislab. [architect-vibe-planning-part2 p67]
- Start from the most compressed version of the idea, the highest-frequency signals; the chat itself is the substance and the human supplies the decision-making. [architect-vibe-planning-part2 p68]
- A rulebook that is itself the product of blurring can still produce sharp outputs. [architect-vibe-planning-part3 p122-p123]
- Token dropping has legitimate uses (tool catalogs over 100 tools, shrinking WG21 papers) even though it is wrong for the author's own prompts. [architect-vibe-planning-part3 p117-p118]
- The author's prompt-writing practice: enter plan mode, state the goal, apply how-to-write-prompts.md, keep refining, ask for a review pass that tightens, then run. [architect-vibe-planning-part3 p156]
- The prompt rulebook absorbs external influence (an Anthropic context-engineering blog post) and may drift ahead of older exemplars. [architect-vibe-planning-part3 p150]
- Small models carry a narrow vocabulary; vocabulary lives in pretraining, not in the fine-tune set. [architect-vibe-planning-part4 p184]
- Early hypothesis that blur is near-lossless; measurement disproved it - a single pass drops or alters a specific in 43-54% of cases. [architect-vibe-planning-part4 p199]
- The endeavor keeps living out its own thesis: every tightening pass regenerates the disease it studies. [architect-vibe-planning-part4 p220, p221]

### Models and infrastructure

- Skepticism about Gemma's reliability at tool calling ("that's its one fucking job") - a model-quality grievance. [promptforge-core-large-part4 p249, p303; promptforge-core-largest-part3 p249, p250]
- An untrustworthy model is useless no matter its size; trust in the model's output is the whole point. [promptforge-core-large-part3 p244; promptforge-core-largest-part3 p244]
- Empirical observation that the smaller model outperformed the larger one on the briefer task. [promptforge-core-large-part3 p243]
- Curiosity about load times for trillion-parameter models on a Blackwell B300 rack. [promptforge-core-large-part3 p186]
- Adding temperature floated as a tuning lever for search behavior. [promptforge-core-large-part3 p179]
- Open question of how to close the output-quality gap with the current model. [promptforge-core-large-part3 p190]
- Temperature should be zero for analytical pipelines - a usage preference, not an engine directive. [promptforge-core-largest-part2 p105]
- The Observer API could grow a side channel for verbose debug logging - a floated question, never confirmed as a directive. [promptforge-core-largest-part2 p105]
- Puzzlement that turning off thinking could ever be good - a teaching moment about model behavior. [promptforge-core-largest-part2 p106]
- Model thinking-level selection (Kimi K3 Low vs High vs Max) - operational tuning question. [promptforge-md-aug18-afternoon p10, p12]
- Open-weight hardware and latency discussion (model sizes, gaming cards, STT/TTS budget) - capability scouting, no behavioral directive. [orchestrator-design-document p4-p10, p38]
- Open-weight model tier economics and "this runs at scale, not on macbooks" - deployment posture, not language design. [orchestrator-design-continued]
- Prefix caching is irrelevant at 3B model scale; tiny context windows are what drive the context engineering. [mcp-client-large-part4 p258, p259; compaction-algorithm-large-part4 p258, p259]
- The consolidated single tool call existed because small-model sections were assumed to need many call kinds at once; large models may not need it. [compaction-algorithm-large-part4 p224, p225]
- The user worried whether a small fine-tuned reduce model can robustly handle inputs containing code fences and mixed languages (C++, JavaScript); raised as a question, never resolved into a directive. [map-reduce-synthesis p8]
- Idea of a fine-tuned small open-weight model that summarizes a prompt into a short label - undecided whether to use it. [promptforge-core-large-part1 p41; promptforge-core-largest-part1 p41]
- Whether an OpenAI-shaped llama-server endpoint duplicates promptforge-gateway - unresolved question. [promptforge-core-large-part1 p65-p68]
- Hard-code the Anthropic base URL for now and point the HTTP layer at the gateway later - a scaffolding choice, not a behavior. [mcp-client-large-part3 p149, p169]
- Skepticism about hardening when the operator controls all the MCP servers: "why do I care about all of this hardening if I control all the mcp servers?" - a threat-model posture, never resolved into a directive. [mcp-client-harness p14; mcp-client-evening p14; mcp-client-continued p14]
- Accuracy is felt as a per-call error rate ("0.80 means one out of five tool calls will be wrong") - the stakes framing behind the abstention design. [mcp-client-continued p32]
- Use cargo public-api as the ground truth for the workflow - a technology choice; the technology-agnostic form was converted. [repo-review-continued p31, p32]
- The transcript compaction algorithm (recursive halving, fidelity gradient, prompt reinjection, pre-compaction at 90%, full transcript persisted) belongs to Mentographist, explicitly declared not part of the orchestrator. [orchestrator-design-document p2, p15, p31, plans appendix; mcp-client-large-part1 p15, p31; orchestrator-design-continued]
- Chat-format preferences ("dont code fence me", blockquote user text) - transcript formatting, not PromptForge design. [orchestrator-design-document p12, p26, p59; compaction-algorithm-large-part1 p12; orchestrator-design-continued]

### Language and engine open questions, worries, and cap-dropped items

- "Should we do files or should we do state?" - an open musing on the state model, no directive landed. [compaction-algorithm-large-part5 p341]
- Line-offset table versus character ranges for edit tools - a question about established practice, not a position. [compaction-algorithm-large-part5 p343-p344]
- Sharded-mutex lock contention idea - a performance implementation note the user explicitly deferred. [compaction-algorithm-large-part5 p350-p351]
- Sub-agent doing web search then web fetch into a virtual file - a usage scenario probing capability, not a directive. [compaction-algorithm-large-part5 p355]
- The web_fetch SSRF security surface (CIDR tables, redirect re-checks, size caps, content-type routing) - tool implementation spec, not language or engine behavior. [compaction-algorithm-large-part5 plans: webfetch crate extraction]
- (cap) Model tiering per section - a convertible principle dropped only because the 20-candidate cap favored more general records. [compaction-algorithm-large-part5 plans: Orchestrator Design Document]
- (cap) Lua sandbox contents (empty globals, safe stdlib only, instruction-count hook) - convertible but dropped at the cap; the module allowlist is also partly a technology choice. [compaction-algorithm-large-part5 plans: Lua args substitution]
- (cap) State tiering (files primary, counters for audit, store for the rest) - convertible but dropped at the cap. [compaction-algorithm-large-part5 plans: PromptForge Executor Tranche 1]
- Naming preference: "args" over "params" for prompt parameters. [mcp-client-large-part2 p76]
- Anxiety that twenty large per-tool schemas recreate the pydantic burden, just shifted into Lua. [mcp-client-large-part2 p84; compaction-algorithm-large-part2 p84]
- Open sandboxing worries: infinite loops in prompt Lua, and tools gaining file read/write through the Lua library. [mcp-client-large-part2 p92, p93; compaction-algorithm-large-part2 p92, p93]
- Belief that people will use prompt Lua for general-purpose computation, so static tool detection may never be complete - in tension with the load-time tool-discovery principle. [mcp-client-large-part2 p94; compaction-algorithm-large-part2 p94]
- Open exploration of making the file the unit of state, tempered by the corrective that structured data like breadcrumbs still exists. [mcp-client-large-part2 p96, p100]
- Lua spawning sub-agents and blocking to collect their results into variables or a map was explored as a scenario, not decided. [promptforge-design-context p32]
- Dividing the problem space into synchronous and asynchronous halves is the way to make progress. [promptforge-design-context p36]
- Manual per-item fan-out markup that turns thirty lines into a hundred is not worth it; the ergonomics were left unresolved. [promptforge-design-context p46]
- Putting the prompt itself in Lua as individual sections means the tool can write itself - an intriguing consequence, not a directive. [compaction-algorithm-large-part1 p45; mcp-client-large-part1 p45]
- Open question: how the tool-call approach to structured output recognizes failure modes the way Pydantic does. [mcp-client-large-part1 p24]
- The detour on running an unmodified prompt by passing it whole to one model was explicitly excluded from the plan. [mcp-client-large-part1 p51, p54]
- Whether the "version" key should be required and how it differs from "promptforge" - unresolved questions. [promptforge-core-large-part1 p48-p50]
- Whether Lua print should be disabled or remapped - unresolved question. [promptforge-core-large-part1 p54]
- Should skipping a heading level be an error? - open question, never resolved. [mcp-client-large-part3 p145; compaction-algorithm-large-part3 p145]
- AGENTS.md or CLAUDE.md? - open question, unresolved. [mcp-client-large-part3 p146]
- If the store is a real filesystem, intermediate artifacts like evidence.md become useless files - a stated worry, no directive issued. [promptforge-core-largest-part2 p162]
- Open question the user left unresolved: how does a PromptForge prompt call an MCP service that is not a PromptForge prompt - an MCP proxy in the gateway was floated, not decided. [promptforge-md-aug16-midday p27, p29, p30]
- Curiosity about the difference between an API key and a bearer token; a terminology question that informed the rename but carries no directive. [promptforge-md-aug16-midday p26]
- Musing on whether more thinking would have prevented the skipped commits; a temperament question. [promptforge-md-aug16-midday p38]
- promptforge.md names local/prompts.toml as the prompt registry - a config-location fact, not a behavior. [promptforge-md-aug16-midday p4]
- The gateway should read gateway.toml from promptforge/local - a config-location decision, not a behavior. [promptforge-md-aug16-midday p13, p14]
- Hesitation about gateway-side URL fetching: if the model might do the fetching itself, gateway fetching becomes ambiguous. Unresolved preference, no directive landed. [modify-the-store p13]
- Open question whether the common one-file-in/one-file-out case deserves its own special syntax. Floated, never decided. [modify-the-store p19]
- Naming-symmetry instinct: config.toml pairs with config.env; superseded by the inheritance-chain resolution rule. [promptforge-md-aug15 p10]
- Whether {{ reply }} substitution injects information versus instructions is ambiguous - raised as an open question, never resolved into a rule. [promptforge-md-aug16-afternoon p29]
- Imperfect model output is acceptable because the user can always fix it. [promptforge-md-aug16-afternoon p30]
- Tool call limits may be unnecessary at all; a large model concludes before overflow and a small model's context fills up and errors, which is a natural bound. [promptforge-md-aug16-afternoon p67]
- A prose section whose last turn emits a tool call loops back into inference - the user's surprise at discovering existing loop behavior, not a directive. [promptforge-md-aug18-afternoon p5]
- Outbound history serializes assistant tool turns as "content": ""; left as-is through the gateway until it actually breaks - a deferred fix. [promptforge-md-aug18-afternoon plans section]
- After first-class tools arrive, the VM can no longer be assumed fixed once the preamble has run; it can change after each completion. [promptforge-core-large-part5 p376]
- The only point of the phase transition is to protect the epilog - an observation, not a directive. [promptforge-core-large-part5 p412; promptforge-core-largest-part5 p412]
- Exploration of generic VM serialization and cloning (with an ID-table scheme for Rust userdata) - abandoned in favor of "lua shared". [promptforge-core-largest-part5 p448-p451]
- Open question on tool-naming training bias (snake_case vs single word vs WebSearch); no directive reached. [promptforge-core-largest-part5 p384, p388]
- Feature spec for a promptforge-dev option to create a same-named directory next to a tool - implementation detail, not a behavior principle. [promptforge-core-largest-part5 p508]
- Terminology question about "spike" as a term of art; teaching exchange only. [mcp-client-evening p18]
- Pasted research finding that tool routing should key on the (server_id, tool_name) pair rather than a concatenated string; the user asked what it meant but never adopted it in that unit (a later unit converted it). [mcp-client-evening p13]
- Args without Lua is too little; Lua is needed to return values. [compaction-algorithm-large-part4 p277, p278]
- Development ergonomics: the service picks up config and directory changes without a restart, and invoking an uninstalled prompt simply errors. [mcp-client-large-part5]
- Integrity stance: subagent prompts are shipped verbatim from named sections rather than paraphrased by the model; what you test is what runs. [mcp-client-large-part5]
- Unit of testing equals unit of composition; each section is testable in isolation with known inputs. [mcp-client-large-part5]
- "Implement all features and let the caller decide, with sensible defaults" - recorded here as temperament; see Open questions for the unresolved tension with no-defaults. [compaction-algorithm-large-part4 p316]

*Grouped draft assembled from the 635-record deduplicated packet; 100 surviving principles (Global 33, Core 41, Boundary 7, Gateway/MCP/CLI 19), 10 open questions, and the merged Not converted list above.*





