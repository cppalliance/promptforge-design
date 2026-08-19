# Purpose pass - Cluster 4: Lua environment and state

## 1. "Embedded Lua is kept minimal..."

Purpose: If too much logic goes into the Lua, the author ends up re-implementing the orchestrator inside the markdown file, which defeats the point of the system ("if we start putting too much into the Lua, then it kinda defeats the purpose"). The sandbox exists because prompts are runnable artifacts with a fixed host surface, and a runaway Lua block (an infinite loop) must not hang the run - hence the instruction-count hook. The file-access leg is a correction: the team had confused the model's file tools with the author's Lua API and sandboxed Lua away from files; the fix is that access control applies to the model through per-section tool injection, while the author's own Lua code can read and write both real and memory files.

Citations: 2026-07-28-0925-orchestrator-design-document.md [p68]; 2026-07-30-1046-compaction-algorithm-large-part2.md [p71], [p92]; 2026-08-02-1134-mcp-client-large-part5.md [p349]; 2026-08-09-1058-promptforge-core-large-part4.md [p368]; 2026-08-14-1613-promptforge-core-largest-part4.md [p368]

Merge: stands alone.

## 2. "A prompt's key-value parameters are read-only and visible to every section..."

Purpose: When every section works on the same input (e.g. a file path), the author does not want to pass that value from section to section by hand, so the parameters sit in a read-only table any Lua anywhere can see. Substitution exists to make prompt assembly deterministic: the Lua assembles the value, the executor splices it in, and the model never paraphrases it. The JSON leg has the same driver - Lua assembles the JSON and the model returns it through macro substitution, which the author called "pydantic with perfect return and no overhead": structured return values without the conformance burden or injected system-prompt cost of Pydantic.

Citations: 2026-07-30-1046-compaction-algorithm-large-part2.md [p74]; 2026-08-02-1134-mcp-client-large-part2.md [p66], [p78], [p79]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p364-p365]; 2026-07-28-2238-orchestrator-design-continued.md [p66], [p78]

Merge: stands alone. Shares a "the engine pushes values in, the model does not pull" motif with records 10 and 11, but the pain here is specifically passing inputs around and paying for structured output.

## 3. "A single ```lua shared chunk per prompt is compiled once and replayed..."  +  4. "The H1 preamble runs exactly once as a live preamble..."

These two records are one decision and share one purpose; they should merge.

Purpose: The preamble needs to run inference and tool calls (to parse the argument string and take control before any section runs), and replaying such a preamble into every section VM would multiply inference cost and corrupt store state - so the H1 runs exactly once, live. But sections still need the author's helper functions ("not having shared functions is a disaster"), and generic VM serialization/cloning was rejected as fragile, so the solution is a separate ```lua shared chunk: pure code, compiled once so syntax errors surface before anything runs, then replayed as bytecode into each section's fresh VM. The replay gate (blocking tools/models/var/reply/jump at the shared top level) exists because replaying with the full environment leaves footguns - a shared chunk that calls tools.add at top level would bind at the wrong time. The empty-chunk substitution exists so the section-startup code path is unconditional instead of branching on whether the author wrote a shared chunk.

Citations: 2026-08-19-0048-promptforge-md-aug19.md [p6], [p7], [p9], [plans: untrusted global and VM reorder]; 2026-08-14-1613-promptforge-core-largest-part5.md [p446], [p450], [p453], [p461], [p462], [p470], [p474], [plans: H1 once no replay]; 2026-08-09-1058-promptforge-core-large-part5.md [p397], [p448-p450]

Merge: merge records 3 and 4 into one principle (live-once preamble plus pure replayable shared library).

## 5. "All Lua chunks in one H2 section share a single VM..."

Purpose: The author discovered the engine was re-installing closures and mutating the environment between Lua chunks of the same section, which broke the natural pattern of one chunk stashing a table and a later chunk reading it - plain globals in one VM is simply how Lua is supposed to work ("they're all just globals to the VM"). Installing the environment once and leaving it alone also removes a whole class of scope open/close machinery the author called "tryhard." The cross-section half is about fanout: sections and fanout arms run concurrently, so mutable run-global Lua is excluded and the store is the only intentional mutable channel - otherwise arms would share mutable state. An error in any chunk stops the run because continuing past a failed chunk leaves the section in a state the author never wrote.

Citations: 2026-08-18-1126-promptforge-md-aug18-morning.md [p102], [p103], [p124], [p125], [p127], [p149], [p154]; 2026-08-02-1134-mcp-client-large-part4.md [p234], [p235]; 2026-08-09-1058-promptforge-core-large-part1.md [p15-p21]; 2026-08-14-1613-promptforge-core-largest-part5.md [plans: section-lua-lifecycle]

Merge: stands alone.

## 6. "Tools and models are first-class Lua objects..."

Purpose: Two concrete drivers. First, testability: with a Tool or Model as an inspectable, invocable table, a unit test can substitute a mock - "we can put in the mock, and we can test it" - which opaque registrations do not allow. Second, the preamble needs to declare globals such as a list of tools that any section can pass to tools.need, which only works if a tool is a value. The unsealed-toolset leg exists because sealing at first infer breaks the working pattern of adding search, running one inference, then adding fetch.

Citations: 2026-08-14-1613-promptforge-core-largest-part5.md [p398], [p400], [p401], [p409]; 2026-08-09-1058-promptforge-core-large-part5.md [p398-p401], [p409]

Merge: stands alone.

## 7. "infer() is a blocking call with a fresh context..."

Purpose: The language rule is no two ways to do the same thing: if infer had tools and conversation history it would just be prose again, with all the same questions (how do you set the tools, what happens on jump). infer exists for a quick one-shot inference inline inside a calculation - string in, string out - when prose would be overkill; "if you want Prose, use Prose." The two-argument form that picked a model per call was dropped so infer always uses the model already selected for the H2.

Citations: 2026-08-18-1126-promptforge-md-aug18-morning.md [p164], [p165], [p182]

Merge: stands alone.

## 8. "State is built through flat tool calls into a persistent store..."

Purpose: This was the founding substitution for Pydantic: routing every model call through a structured-output layer is expensive and conformance is unreliable on the small open-weight models the system targets, while flat-argument tool calls are reliable - so the model builds state by calling tools and persistence becomes a side effect. The single-call leg is a cost measure: propagating state as one tool call carrying all values exists because otherwise "you end up making 2 tool calls instead of 1."

Citations: 2026-07-28-0925-orchestrator-design-document.md [p13]; 2026-07-28-2238-orchestrator-design-continued.md [p13], [plans]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p228], [p265]

Merge: stands alone. Related to record 9 (same store) but a different pain - this one is about reliable state extraction from the model, record 9 is about debugging and resume.

## 9. "The store is a virtual filesystem for file-shaped intermediate values..."

Purpose: Building an analytical pipeline requires re-running the prompt from any step during development and inspecting what each step produced after the run, so intermediate values must exist as files that can be read back in and skipped via store.exists. It is deliberately not a general-purpose filesystem - string replacement and delta application for agentic coding are a different, future class - and it must not be literally the filesystem, because then intermediate artifacts like evidence.md would show up as useless stray files in the user's directory. Real and virtual files must be readable at the same time because prompts need to read author-supplied input files alongside run-produced memory files.

Citations: 2026-08-14-1613-promptforge-core-largest-part5.md [p377], [p504], [p505]; 2026-08-14-1613-promptforge-core-largest-part4.md [p367]; 2026-08-09-1058-promptforge-core-large-part3.md [p162]

Merge: stands alone (see record 8 note).

## 10. "State is carried as a key/value block written by Lua..."

Purpose: A jump clears the context, so the facts the next section needs have to be injected fresh on every transfer - the Lua writes the block, the executor picks the tag. On multi-turn horizons the same facts bag must not become permanent transcript residue: on a tool call it is removed, the tool results go in, and the bag is added back, because small models have tiny context windows and accumulated residue crowds them out ("I don't want to start accumulating permanent crap in the context"). The push direction is deliberate: the prompt's Lua declares what the model needs and the engine injects it, rather than the model pulling context items itself.

Citations: 2026-08-02-1134-mcp-client-large-part4.md [p254]-[p260], [p287], [p288], [p290]; 2026-07-30-1046-compaction-algorithm-large-part4.md [p257], [p288], [p290]

Merge: stands alone.

## 11. "The engine exposes system facts to prompts through a sys object..."

Purpose: Prompts need facts only the engine knows: the launch time as a fixed constant, the current time so a model can detect time passing and compute elapsed time, and a unique incrementing id per context so Lua can compute unique filenames in the store. sys.model exists because the author wanted to print the producing model at the bottom of a generated report; it is unavailable during the prologue because no model is bound until the section's model scope closes. Unknown sys names fail loud because a silent empty value would hide a typo'd field name from the prompt author.

Citations: 2026-08-02-1134-mcp-client-large-part4.md [p284], [p285], [p286]; 2026-08-02-1134-mcp-client-large-part5.md [p419], [p420]; 2026-08-08-0029-promptforge-context-planning.md [p14], [p15]; 2026-08-08-1223-gateway-local-inference.md [p54], [p55]

Merge: stands alone. Shares the fail-loud-on-unknown-name posture with other records but the purpose (engine-known facts) is its own.
