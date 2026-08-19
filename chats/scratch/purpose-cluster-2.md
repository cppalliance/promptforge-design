# Purpose pass - Cluster 2: The prompt as a program and document structure

## 1. "A prompt is a single markdown file that is one function..."

Purpose: The author decided the basic unit of the system is the function - parameters in, string out, side effects allowed - and his existing workflow was already one markdown file per prompt, so the file and the function are the same thing. When work outgrows one file, you split it into more prompt files (separate functions) rather than growing the format; a prompt has a natural size limit as a linear pipeline. Requiring anything beyond the one file (a companion Rust file, extra structure) would break self-containment, which he called "the whole point."

Citations used: 2026-07-30-1046-compaction-algorithm-large-part2.md [p65]; 2026-08-02-1134-mcp-client-large-part2.md [p86], [p117]; 2026-07-28-2238-orchestrator-design-continued.md [p65], [p117]; 2026-08-02-1134-mcp-client-large-part5.md [p409], [p410]; 2026-08-12-1534-dokuman-each-crate.md [guide/src/introduction.md]

Merge: shares the self-containment motive with record 2 ("The design starts from the prompt...") - both rest on [p86] "the whole point of this was that it was self-contained." They can merge into one principle: a prompt is one self-contained file that is one function, and the language grows inside the prompt rather than around it.

## 2. "The design starts from the prompt and adds structured programming into it..."

Purpose: Other frameworks start with a host language (Python, Go) and bolt prompts on; the author owns a body of markdown prompts and wants programming added into them, so a prompt with zero Lua still runs exactly like a plain Cursor/Claude Code orchestration (the whole file passed to the model). The pain was concrete: a proposed tool design implied Rust code backing every prompt, and he objected that this kills self-containment. Lua is additive - you only reach for it when plain prose is not enough.

Citations used: 2026-08-02-1134-mcp-client-large-part2.md [p86], [p118]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p86], [p118]; 2026-07-28-2238-orchestrator-design-continued.md [p118]; 2026-08-02-1134-mcp-client-large-part5.md [p402]-[p406]

Merge: see record 1 - same self-containment motive, merge candidate.

## 3. "No compilation step sits between the prompt author and the model..."

Purpose: Three concrete drivers. (a) Prior art: Playbooks compiled prompts to an intermediate representation and the recorded lesson was "do not put a compilation step between the prompt author and the model; the raw markdown is the program." (b) Parsing must happen once up front so a syntax error is impossible at run time - he rejected runtime markdown parsing inside fanout helpers for exactly this reason. (c) A parsed prompt must be inert data so a server can list, inspect, and enumerate prompts without executing any prompt code - reading a file never runs anything inside it.

Citations used: 2026-07-28-0925-orchestrator-design-document.md [design documents: promptforge.md, Playbooks lesson]; 2026-08-08-0029-promptforge-context-planning.md [p62]; 2026-08-03-2040-plan-the-mcp-server.md [p74]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans: section-lua-lifecycle - "all Lua compiled at parse so a successful Prompt is fully syntax-validated"]

Merge: none.

## 4. "A prompt file is an H1 section containing a lua preamble fence..."

Purpose: The author caught the parser missing the trailing epilog fence and dictated the section shape by example: lua fence, prose, lua fence. He then asked to require the lua before the prose in the H1 too, "just for consistency so that you don't confuse the preamble with an epilogue," and required the H1 with anything between the YAML and the H1 ignored. The rule exists so that position, not content, tells reader and parser which fence is which - a fixed layout with no ambiguity and a free scratch zone between front matter and the H1.

Citations used: 2026-08-09-1058-promptforge-core-large-part1.md [p6]-[p12], [p22], [p23]; 2026-08-14-1613-promptforge-core-largest-part1.md [p7], [p22], [p23]

Merge: none. Related to record 5 (both fix the document grammar) but the motive differs: this one is positional disambiguation of fences, record 5 is machine-addressable names.

## 5. "H2 is a subhead and H1 is not; every subhead's first word must be a valid identifier..."

Purpose: Section headings are jump/execute targets, so the name part must be a valid identifier and unique within its scope (H2s across the file, H3s within their parent) or control-flow calls cannot resolve unambiguously. Making the first word the identifier and the rest of the line an ignored comment lets one heading serve as both machine address and human-readable title ("### Summarize-Research map reduce to get report"). The H1 is excluded because it is the prompt itself, not a callable section.

Citations used: 2026-08-02-1134-mcp-client-large-part5.md [p381], [p391]-[p394]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p381], [p391]-[p395]

Merge: none.

## 6. "Prompt documents support nested sections recursively from H2 through H6..."

Purpose: Subroutines and fanout arms need to live inside their parent section ("H3 as well of course.. fully recursive to H6"), and the author wanted one set of execution rules at every level instead of per-level special cases - "identical rules. different level." He explicitly expected this to simplify the implementation: "this should result in a simplification because we've eliminated the special cases." Without recursion, shared subroutines and fanout templates would have to be top-level sections, polluting the flat walk.

Citations used: 2026-08-02-1134-mcp-client-large-part3.md [p137]-[p144]; 2026-08-19-0048-promptforge-md-aug19.md [p39], [p40], [p60], [p79]; 2026-08-02-1134-mcp-client-large-part5.md [p411]

Merge: shares one discussion and one motive with record 8 (aug19 [p39]-[p41]): uniform recursive rules plus explicit level transfer are two halves of the same decision. Merge into one principle: sections nest H2-H6, every level runs under identical rules, and moving between levels is always explicit.

## 7. "A horizontal rule marks a section to be skipped by execution..."

Purpose: The author needed reusable subroutine sections to sit in the file without the default sequential walk running them, and wanted space for prose aimed at the reader that does not affect execution. He rejected the first design (one "---" below which nothing executes) because its meaning depends on position: "My new version survives the user cutting and pasting sections around." He also refused special casing ("No, the blank line is required. I dont want any special casing") and demanded the rule apply uniformly, even to a section reached through a chain.

Citations used: 2026-08-02-1134-mcp-client-large-part5.md [p382], [p383], [p387]-[p390]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p382]-[p390]; 2026-08-19-0048-promptforge-md-aug19.md [p26], [p30], [p32], [p35], [p65]

Merge: none.

## 8. "Fall-through never crosses heading levels..."

Purpose: A section's children are subroutines and fanout material, not steps, so the default walk must never silently descend into them - "H2 never falls through to H3. The transfer from HN to H(N+1) must be explicit." Once a jump or execute lands at the deeper level, the ordinary sibling walk takes over. Without this, running a parent section would execute its arm templates and subroutines as if they were pipeline steps.

Citations used: 2026-08-19-0048-promptforge-md-aug19.md [p41]; 2026-08-02-1134-mcp-client-large-part5.md [p400], [p401]

Merge: merge with record 6 - same conversation, same decision, two halves of one rule.

## 9. "XML blocks may appear anywhere in the document..."

Purpose: XML is model-facing markup - models are trained on it and spot it easily - so the author reserved it for the model and refused to let the harness use it as a grouping system: "We want to leave the XML for the model to be able to spot. We don't want to use the XML as a grouping system for the harness." The harness already has section headings for grouping, and no heading level is special. Extracting XML into a table keeps reusable material (e.g. shared rule lists) available as data without counting it as prompt text.

Citations used: 2026-07-30-0534-promptforge-design-context.md [p40], [p41], [p53], [p54]

Merge: none.

---

*2026-08-19 07:34 - kimi-k3*
