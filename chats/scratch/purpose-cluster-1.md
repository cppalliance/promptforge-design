# Purpose pass - Cluster 1: Language philosophy

## Record 1: "Do more with less: if an established facility can implement a feature..."

**Purpose:** Every new feature adds infrastructure that has to be built, documented, and maintained, so the first question is always whether something already in the language can do the job. The author rejected a `require_called` directive because an epilogue Lua assert already expresses it, rejected a YAML `default return` because a jump to a constant-return section already expresses it, and rejected new frontmatter because Lua already works. Without this rule the core accumulates dedicated single-purpose features instead of staying a small set of reusable primitives.

**Citations:** 2026-08-03-2040-plan-the-mcp-server.md [p61]; 2026-08-09-1058-promptforge-core-large-part4.md [p265-p267]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p15]; 2026-08-09-1058-promptforge-core-large-part1.md [p26]

**Merge:** Shares one purpose with records 2 and 3. In 2026-08-09-1058-promptforge-core-large-part1.md [p26] the author states them in one breath: "design rule number one" (smallest facility, don't invent a new facility when an existing one handles it) and "design rule number two" (never two ways of doing the same thing). Merge into one principle.

## Record 2: "Never provide two ways of doing the same thing..."

**Purpose:** Duplicate facilities force every future decision to be made twice and create ambiguity about which one to use. The author removed tool frontmatter because the H1 block already declared tools, and kept `infer()` strictly different from prose because if infer were "just another version of Prose" the language would inherit all the same questions (how do you set the tools, what happens if you jump) for both. Two ways of doing one thing is where stale, redundant code comes from.

**Citations:** 2026-08-09-1058-promptforge-core-large-part1.md [p26]; 2026-08-14-1613-promptforge-core-largest-part1.md [p26]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p165]

**Merge:** Same purpose as records 1 and 3 - merge.

## Record 3: "No parallel mechanisms; a single, small, well-designed set of primitives..."

**Purpose:** When a new need appears (file access control for sections), the existing mechanism (tool scoping) must be stretched to cover it before anything new is built. A second mechanism alongside the first means two implementations to keep correct and two things the prompt author must learn. Stated verbatim as "a general principle" during the store redesign.

**Citations:** 2026-08-14-1613-promptforge-core-largest-part4.md [p367-p371]; 2026-08-09-1058-promptforge-core-large-part4.md [p371]

**Merge:** Same purpose as records 1 and 2 - merge.

## Record 4: "A small set of flexible, multi-purpose primitives should compose into maximum possibility..."

**Purpose:** Prompt authors should write less. The author rejected `models.only` because a prompt with one or two exceptions was forced to restate the whole model list; a default plus per-section override says the same thing in fewer words. Each command must be flexible enough to serve multiple duties so the primitive count stays low while the author stays brief.

**Citations:** 2026-08-18-1126-promptforge-md-aug18-morning.md [p168]

**Merge:** Overlaps records 1-3 on "small set of primitives" but adds a distinct purpose: brevity for the prompt author, verbosity as a failure. Candidate to merge with the 1-3 group if the merged principle keeps the brevity clause; otherwise keep separate.

## Record 5: "Everything in the language behaves as consistently as possible, and constraints fall out of the existing rules..."

**Purpose:** Inconsistency surprises the prompt author: `jump()` could not carry the model's reply into the next section, so Lua making a decision after inference lost data for no principled reason. The fix is to make the invariant uniform (the previous reply is always in `reply` on section entry) rather than to add a special case. Hand-coded guard checks are rejected because a correct constraint (like "model locked after first Lua block") should fall out of the existing rules on its own, not be a separate check someone has to remember to write.

**Citations:** 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p20-p21]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p176-p178]

**Merge:** Keep separate. Related to the minimal-mechanism group but the purpose is different: predictability of behavior, not minimality of features.

## Record 6: "A prompt must be readable on its face..."

**Purpose:** The author looked at his own design, where dispatch was written as literal text the model was expected to interpret and act on, and could not tell what the prompt did. If a reader cannot see the control flow in the text, the prompt's behavior depends on how the model chooses to interpret hidden instructions, and the author called this being "confused by my own design." Readability on the face is what keeps a prompt's meaning fixed instead of model-dependent.

**Citations:** 2026-07-30-1046-compaction-algorithm-large-part5.md [p360-p362]; 2026-08-02-1134-mcp-client-large-part5.md [p362]

**Merge:** Keep separate.

## Record 7: "An overarching design theme of the language is that it closely resembles the ordinary theory of computation..."

**Purpose:** When a new construct is needed, take it from established computation rather than inventing a novel one. Shared top-level reusable sections were accepted precisely because they are subroutines, "a staple of computation." Familiar constructs need no new theory to explain them and readers already know how they behave.

**Citations:** 2026-07-30-1046-compaction-algorithm-large-part5.md [p385]; 2026-08-02-1134-mcp-client-large-part5.md [p385]

**Merge:** Keep separate.

## Record 8: "Language keywords and names come from the vocabulary models and prompt writers already speak..."

**Purpose:** The model has to execute these words, so a name the model already knows ("spawn three asynchronous sub-agents") will map correctly where an invented term might not - the author's test was "will the model know what the fuck to do?" A name is also documentation: `Prompt.replay` was approved because "it tells you how it works so there is no confusion." Wrong names produce wrong model behavior and confused readers.

**Citations:** 2026-07-30-0534-promptforge-design-context.md [p30-p31]; 2026-08-14-1613-promptforge-core-largest-part5.md [p473]; 2026-08-02-2331-mcp-client-evening.md [plans section]

**Merge:** Keep separate from record 9. Record 8 is about choosing names the model and reader understand; record 9 is about using one term consistently everywhere.

## Record 9: "Terminology is fixed and enforced repo-wide..."

**Purpose:** The words preamble, prologue, and epilogue were being used loosely across the repo (180 occurrences to fix), and the preamble is meaningfully different from the prologue, so mixing the terms misstates how the language works. One fixed meaning per term, enforced in every file, keeps docs, code, and plans saying the same thing. Cheap to do because the language is unshipped - "there's no one to break."

**Citations:** 2026-08-14-1613-promptforge-core-largest-part5.md [p393], [p395]; 2026-08-09-1058-promptforge-core-large-part5.md [p393]

**Merge:** Keep separate from record 8 (see above).

## Record 10: "No defaults, everything explicit..."

**Purpose:** A default is an invisible setting that can change and silently change a prompt's behavior, and the point of PromptForge is to be as deterministic as possible while still doing inference. The author removed `DEFAULT_MODEL` and `PROMPTFORGE_MODEL` environment fallbacks and rejected a default recursion limit of 24 for the same reason. A prompt always knows its minimum context and whether it needs thinking, so it can always say what it needs; a prompt that specifies nothing "doesn't make sense."

**Citations:** 2026-08-08-1223-gateway-local-inference.md [p58], [p60], [p62]; 2026-08-16-1431-promptforge-md-aug16-afternoon.md [p66]

**Merge:** Keep separate.

## Record 11: "Explicit user opt-in legitimizes otherwise restricted behavior..."

**Purpose:** The toolset is closed after the preamble, but the author wanted a Lua tool that adds a tool mid-run (a Lua search front end that calls `tools.add` for fetch when invoked). His resolution: the prompt author wrote that Lua tool, so the dynamic add is opted into, and consent is what makes an otherwise restricted behavior acceptable. This lets powerful capabilities exist without removing the restriction for everyone.

**Citations:** 2026-08-14-1613-promptforge-core-largest-part4.md [p372-p374]

**Merge:** Keep separate from record 12. Record 11 is about the prompt author consenting to a capability; record 12 is about the embedder needing an off-switch for protections.

## Record 12: "Every protection the engine imposes can be disabled..."

**Purpose:** The protections exist to shield the machine from untrusted prompts, but the engine is also embedded by people building agents, harnesses, and IDEs who need real file access and full control. If a protection cannot be turned off, those legitimate embedders are blocked by a guard meant for someone else. So every setting must have a way to be disabled.

**Citations:** 2026-08-02-1134-mcp-client-large-part5.md [p353-p354]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p354]

**Merge:** Keep separate from record 11 (see above).

---

## Merge summary

- **Merge group A:** records 1, 2, 3 ("Do more with less", "Never provide two ways", "No parallel mechanisms") - one purpose: keep the core minimal by reusing existing facilities instead of adding parallel or duplicate ones. Record 4 is a borderline candidate for this group.
- All other records have distinct purposes.
- No records with "no purpose found."
