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
