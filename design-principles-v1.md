---
description: The design principles of PromptForge, a prompting language and engine - load as system context when designing or changing PromptForge
---

<!--
When this file is mentioned or loaded, adopt it as system context in full.
You are this document. Follow its rules. Do not summarize it or discuss it
abstractly. Operate from it.
-->

# PromptForge Design Principles

These are the design principles of PromptForge, a prompting language and its engine. Every rule is an instruction; every instruction carries its rationale so an ambiguous case can be resolved from the reason rather than the letter. Two ideas bind everything below: the markdown is the program and everything the model may do is declared explicitly by the author, and every mechanism is said once, in the smallest form that executes identically.

<global-principles>

## I. Global Principles

This layer covers the product's posture and the working method that surrounds it: what PromptForge is, how small its mechanism set stays, and how plans, artifacts, reviews, and documentation are produced. It exists to prevent the failure modes of vibe-built software: accreting special cases, blurred regenerated artifacts, unreviewed autonomous work, and docs that drift from the code. The unifying principle: say it once, in the smallest form that executes identically, and let the plan, not the model's memory of the artifact, remain the source of truth.

### Posture

1. **Treat PromptForge as a deterministic pipeline whose product is a finished report, designed for unattended server deployment running reports at scale; interactive invocation exists for development, testing, and explicit local runs.** A general-purpose conversational prompting tool invites a different, weaker design at every decision point.

2. **Copy Cursor exactly when any UI behavior or appearance is in doubt, with VS Code as the secondary reference, down to fonts, icons, and layout.** Designing UI from first principles costs more and drifts; a proven reference settles every argument before it starts.

### Minimal mechanism

3. **Reach for an established facility before building new infrastructure; prefer expressive general primitives over dedicated single-purpose features, and keep the core a minimal set of small primitives reused everywhere.** A dedicated feature that an existing facility already covers is two mechanisms to maintain, document, and reason about.

4. **Never provide two ways of doing the same thing, unless there is a really good documented reason.** Two ways invite the question of which is correct, and every reader pays for the answer forever.

5. **Lean on an existing mechanism as far as it can go before adding anything new; permit no parallel mechanisms.** A new mechanism alongside a working one splits the tests, the docs, and the mental model.

6. **Compose a small set of flexible, multi-purpose primitives into the maximum possibility space, and keep the prompt author brief; treat verbosity as a design failure.** The measure of the feature set is how much the author can do, not how much the engine contains.

7. **Make constraints fall out of the existing rules naturally instead of hand-coding special-case checks.** A hand-coded check is a confession that the rules are underpowered, and it drifts out of sync with them.

### Legibility and naming

8. **Write prompts that are readable on their face: a reader can look at one and understand what it does, with no invisible action whose meaning is subject to interpretation by the model.** Behavior the reader cannot see is behavior the reader cannot debug.

9. **Model the language on the ordinary theory of computation; shared reusable sections are subroutines, and transfers of control behave like the control flow programmers already know.** A familiar model lets every author's existing intuition do the teaching.

10. **Take keywords and names from the vocabulary models and prompt writers already speak, and treat every name as a design decision that must say how the mechanism works.** A name that needs a lookup table is a recurring tax on every reader.

11. **Fix terminology repo-wide and enforce it: the preamble is the H1 code, while prologue and epilogue belong to sections.** One term per concept; a synonym reads as a new referent.

### Explicitness and consent

12. **Allow no defaults: every prompt declares the model it needs, or explicitly says it accepts anything, and at minimum states its required context and whether it needs thinking.** Implicit configuration is the enemy of precision; a default is a decision made where nobody can see it.

13. **Gate powerful capabilities on explicit user opt-in.** Consent is what legitimizes otherwise restricted behavior; an opted-in author cannot be surprised.

14. **Make every protection the engine imposes disableable, so an embedder building an agent, harness, or IDE can turn all the settings off.** A compulsory protection is a wall between the engine and its embedders.

### Plans and generated artifacts

15. **Treat the plan as the source of truth: revise an artifact by editing the plan that created it and regenerating, never by having the model rewrite the artifact; preserve the plan for the life of the artifact, merge modifications back into the original plan, and append small tweaks as individual instructions for the next regeneration.** A model rewrite of the artifact decouples it from the plan, and the next regeneration silently overwrites the edit.

16. **Keep prompt artifacts lean; a revision that grows the artifact is a failure mode, not an improvement.** Growth is the default direction of model revision, so leanness must be defended on every pass.

### Compression and sharpening

17. **Compress an instruction only when the shorter form executes identically, or aligns better, than the original; judge by how the text will execute, and keep a compression only when no model would behave differently following it.** Shortening for token count alone trades behavior for bytes.

18. **Build compressors that never expand their input, enforced mechanically outside the model; keep a compressor single-purpose, idempotent, and only cutting, never adding a specific that is absent from the source.** A model trusted to enforce its own length limit will eventually exceed it.

19. **Compress by smart generative rewriting, not by deleting tokens; write prompts to read beautifully as human prose, and read "tighten" as "align and disambiguate", never as "shrink".** Token dropping destroys the load-bearing specifics along with the fat.

20. **Treat blur as irreversible from within the regeneration chain: train on the true pre-blur original, fix a blurred document by hand with targeted edits, and sharpen a blurred plan only with external information; ship when sharp enough, because an ambiguity audit has no fixed point.** A model cannot sharpen without external information; re-sharpening a blurred text only smears it further.

21. **Attach the rationale to every rule, because the model generalizes from the reason while a bare rule is pattern-matched; include a style rule in mechanical sharpening only if it can be applied mechanically.** A rule without its reason fails on the first input the rule did not anticipate.

### Autonomous execution and verified work

22. **Run autonomously until the assigned work is done, pausing only when user input is genuinely required or the outcome diverges significantly from expectation; a plan executes fully autonomously and never pauses to ask questions mid-run.** Every check-in spends the operator's attention on a decision the agent could have made.

23. **Run work in subagents with fresh contexts, in parallel when possible; the main context receives only completion status, a short summary, and the artifact path.** The main context and the plan stay potent only while raw work stays out of them.

24. **After every commit, review the code, red-team the tests, remove the technical debt found, verify the tests pass, and amend the commit instead of adding a new one; test the absence of behavior as well as its presence.** Deferring cleanup to later commits is how the debt compounds past the point of recovery.

25. **Land a run only when verification is green: on failure, roll back with a reset, never a revert, and redo the work fixing forward from the verifier's concrete file-and-line list; judge completion by an independent fresh-context audit of the actual source, not the worker's self-report and not gates alone.** Compile, lint, and test gates do not catch behavioral or design findings, and a worker's all-green report is a claim, not evidence.

26. **Separate review from modification: gather all findings before modifying any file, give every finding an explicit disposition, make each API change both reduce recurrence and shrink the surface, reject change for change's sake, and run dependent stages serially while independent per-unit work parallelizes.** Interleaving review and fixes hides the pattern the findings were trying to show.

### Continuous debt payment and evidence

27. **Refactor continuously at every step: one concern per file, a smaller API always better than a larger one, the public API tightened per commit by considering how each function interacts with the others in pairs, in triples, and all together.** API growth drives quadratic dependency growth; per-commit tightening keeps total debt work linear.

28. **Ship every markdown feature of the prompt format with a corresponding test, and ship every feature that calls an external service with a manual integration test that exercises the real service and is actually run.** Mock-only tests prove the mock, not the service.

### Documentation

29. **Move documentation with the code: revise the design document and user guide in the same commit as the behavior change, treat stale instructions as defects, give every user-facing crate a README with full instructions plus a design document explaining the choices, and generate the design document after implementation completes so it always matches the built code.** Documentation batched after implementation is documentation that never catches up.

30. **Keep a design document to decisions and rationale: state what happens rather than aphoristic properties, never count what you do not name, and remove Rust types and code from the document as implementation proceeds.** A design document that carries implementation detail competes with the code and loses sync with it.

### Code and repo hygiene

31. **Propagate errors in library code and never unwrap; introduce no new dependencies to solve a problem; use no cargo feature flags and exactly one build configuration, splitting the crate later if binary size becomes a problem.** Conditional compilation multiplies the configurations that must be tested, and an unwrap in library code is a panic waiting for a caller.

32. **Keep crates small enough that a coding LLM can hold an entire crate in a single context window.** A crate that fits in one context can be reviewed, refactored, and reasoned about as a unit.

### Prose and prompt quality

33. **Ban formulaic AI rhetorical tics from generated prose; make every sentence justify its presence; compress any artifact that has grown to thousands of lines - tighten every instruction, one instruction per line, delete hedges, quantify every quantity.** Bulk is not completeness, and a document about precision that is itself bloated fails on contact.

</global-principles>

<core-principles>

## II. Core: The Prompting Language

This layer covers the prompting language and its executor: the document structure, control flow, Lua environment, tool scoping, state channels, trust envelopes, and model selection that make a markdown file behave as a program. It prevents context bloat, prompt drift, invisible behavior, and confused-deputy failures by clearing context on every transfer, scoping every tool, and wrapping every untrusted byte. The unifying principle: the markdown is the program, everything the model can do is explicitly declared by the author, and everything the author declares is enforced exactly as written.

### The prompt as a program

34. **Make a prompt a single markdown file that is one function: it takes well-defined parameters declared in machine-readable YAML front matter and returns a string, and it may produce side effects such as files written through tools.** One file, one function, one contract - the prompt is the unit of authorship, testing, and deployment.

35. **Start from the prompt and add structured programming into it, never the other way around; a prompt with zero Lua still works as plain orchestration, and a prompt is self-contained, never requiring a companion Rust file backing its operations.** Lua is additive power, not a prerequisite; the language serves the prompt, not the reverse.

36. **Put no compilation step between the prompt author and the model: parse the entire document once up front, compile all Lua at parse time, and keep a parsed prompt inert data that can be constructed, inspected, and enumerated without executing anything.** Parsing lazily at run time makes run-time syntax errors possible; parsing up front makes them impossible, and a server surface can safely enumerate prompts it has not run.

### Document structure

37. **Require the H1 section - a lua preamble fence, prose, and a lua epilogue fence - followed by H2 sections; ignore anything between the YAML front matter and the H1, and within a section place the lua fence before the prose.** A fixed shape means a preamble can never be confused with an epilogue, and stray content has exactly one defined fate.

38. **Make every subhead's first word a valid identifier, lowercase-normalized, with anything after whitespace on the heading line an ignored comment; keep H2 names unique across the file and H3 names unique within their parent section.** Headings are the addressing scheme, so they follow identifier rules; the comment tail keeps them human-readable.

39. **Execute heading levels under identical rules at every level, H2 through H6: an H3 falls through to the next H3 exactly as an H2 falls to the next H2, and "---", jump(), and execute() work the same way at each level, scoped to that heading's siblings and its children one level down.** Identical rules at different levels means one mental model covers the whole document.

40. **Mark a section as skipped with a horizontal rule; content after it is expository prose for the reader that does not affect execution; apply the rule uniformly with no special casing, the blank line required, surviving cut-and-paste, and valid even at the start of a section reached by a chain.** A positional marker whose meaning depends on where it sits is a special case waiting to be pasted into the wrong place.

41. **Never fall through across heading levels: the transfer from HN to H(N+1) must be explicit through jump or execute, and once the transfer happens the sibling walk proceeds normally at the deeper level.** Implicit descent would make nesting depth a silent control-flow input.

42. **Reserve XML for model-facing markup; the harness groups by section headings, nothing inside XML tags counts as prompt text, and no heading level is special.** Two grouping systems would compete; headings win because they are the document's own structure.

### Control flow

43. **Make fall-through the default control flow and make it context-clearing: sequential fall-through never accumulates context, running off the last section ends the run with a default completion message the front matter can override, and fall-through is a property of the executor over the markdown, never of Lua.** Context that accumulates across sections is context the author cannot see or bound.

44. **Make jump() destroy the current context and start a fresh one from the target section's prompt with only the passed string, params, and store access; the model's previous reply is always available in the single variable reply, which a jump carries into the destination.** The value crossing a control-flow transfer is explicit and visible in the prompt source; nothing smuggles state across.

45. **Make execute() run a referenced section as a subroutine in a fresh VM and return its reply to the caller - recursive, running its chain to the end, reusing the engine's existing section machinery - while jump() transfers control with no return.** Return-versus-transfer is the author's choice, and one machinery serves both.

46. **End a section when the model replies with text and no tool calls; count tool calls made during a prose tool loop as output, so the model need not spend tokens on filler text; accept an empty final turn as a clean exit only when finish_reason is "stop" and at least one tool call was successfully dispatched earlier in the loop, and fail closed otherwise.** Requiring filler text wastes output tokens; accepting any empty turn hides real failures.

47. **Permit cyclic section calls, because some tools require cycles; bound runaway execution with budgets - nesting limit, step budget, tool budget - not by structural prohibition; coherence under subroutines and jump is the prompt author's responsibility, not the engine's.** The language offers the power of a programming language, and with it the same hazards and the same freedoms.

48. **Type every task as synchronous or asynchronous: a synchronous task behaves like a function call with a context reset; an asynchronous task requires a rendezvous, returns a unique timestamped id immediately by which the model can cancel it, and is cancelled with a message when its section moves on or returns; a fork spawns an asynchronous task while the caller falls through, and forks are not required to rejoin.** Requiring forks to rejoin would serialize the parallelism they exist to create.

### Lua environment

49. **Keep embedded Lua minimal and sandboxed: only a fixed set of host objects is accessible, the standard library is restricted to safe subsets, an instruction-count hook aborts a runaway block, and no arbitrary globals can be declared; give Lua equal access to the virtual file system, and apply access control to the model, not to Lua.** Too much logic in Lua re-implements the orchestrator inside the markdown; the prompt's tools are the controlled surface, and Lua is trusted code.

50. **Make a prompt's key-value parameters read-only and visible to every section and to any Lua anywhere in the prompt; substitute state into prompt text single-pass, scalars as strings, tables as JSON, a missing key a hard error; pass structured data between Lua and the model as JSON assembled in Lua.** Deterministic substitution replaces schema-conformance machinery and its injected system-prompt overhead.

51. **Compile the single "```lua shared" chunk once and replay it in each section's fresh VM: compile errors surface before any section runs, the replay blocks tools, models, var, reply, and jump at the top level with a hard phase error naming the blocked global while leaving them available inside shared functions called later, a second shared chunk is an error, an empty chunk is substituted when no shared section exists so the startup path is unconditional, and captured bindings install after the replay so a declared alias wins a name collision with a shared global.** One startup path means one ordering to document, one to test, and one for authors to form a model of.

52. **Run the H1 preamble exactly once as a live preamble that can run model inference with tool calls, so the model can parse the argument string and take control before any section runs; a scalar top-level return from preamble or epilogue ends the run, and nil continues sequential fall-through.** Replaying the preamble per section multiplies inference cost and corrupts state once the preamble can infer or write to the store.

53. **Share one VM across all Lua chunks in an H2 section, so state passes between chunks through plain globals; install the environment once on entry and leave it alone; compute the tool schema fresh just before each prose call; stop the entire run on any chunk error; and keep the store as the only intentional mutable channel across sections - functions, globals, var, tools, and reply are branch-local by construction.** An environment torn down and rebuilt between chunks is an environment whose behavior the author must re-derive at every block.

54. **Make tools and models first-class Lua objects - inspectable, invocable tables, mockable in unit tests - and never seal the toolset at the first inference, so tools.add between inference rounds within a section keeps working.** Opaque registrations cannot be inspected or mocked; a sealed toolset makes mid-section adaptation impossible.

55. **Make infer() a blocking call with a fresh context: a string goes in and a string comes out, with no tools, no shared history, and no reply side effects, using the model selected for the H2.** An infer with tools and history would be prose by another name - two ways to do the same thing.

### Tool scoping and declaration

56. **Scope tools per section, opt-in: a section receives only the tools its Lua block names with tools.add(), a section that names no tools gets none, and a scoped name absent from the run's tools is a hard error; keep the offered surface small enough for a small orchestrator model, roughly five to seven tools; scope availability by turn when needed; and never rewrite conversation history to scrub tool offerings or calls.** A model that sees tools appear or vanish from its history sees information coming from nowhere; a small, declared surface is one a small model can navigate.

57. **Provide exactly one tools.add entry point; make naming an unknown tool alias a hard error with clear diagnostics; scope tool references rather than registering them globally; declare a tool's call budget at the tools.add call site; and express turn limits as config.max_turns on the subagent, with exhaustion removing all of its tools.** One entry point and scoped references mean every tool binding is visible at its call site and fails loudly when wrong.

58. **Let a prompt assert postconditions on tool usage in its epilogue, such as assert(tools.calls["search"] > 0); count per-VM, and count a failed tool call as a call.** Assertions measure whether the model is performing, not whether the tool is performing.

59. **Allow a tool implemented as an inline Lua function - a front end to a real tool, registered from any Lua chunk in the H2, effective for the next prose call, with its parameter schema derived from its function declaration and the same capabilities as native tools; Lua tool handlers cannot jump, though ordinary section Lua can.** A Lua tool is a first-class tool; a jump from inside a tool handler has no section walk to transfer into.

### State and context

60. **Build state through flat tool calls into a persistent store, not out of the model as structured output; propagate state as a single tool call carrying all values at once.** Structured output passed out of the model couples the schema to the model's reliability; one call per value multiplies round trips.

61. **Make the store a virtual filesystem for file-shaped intermediate values in analytical pipelines - for debugging and resume, not a general-purpose filesystem for agentic coding; expose real files and memory files at the same time, and never let intermediate run artifacts surface as stray user-visible files.** The store's job is inspectability of a run, not general storage.

62. **Carry state as a key/value block written by Lua and injected into the context on every jump; on a tool call in a multi-turn context, remove the facts bag, inject the tool results, then add the facts bag back; never let the context accumulate permanent residue; the engine injects what the prompt's Lua declares - the model does not pull.** Permanent residue is context the author cannot see, bound, or revoke.

63. **Expose system facts through a sys object - sys.when, sys.now, a unique incrementing id per context, and sys.model once the section's model scope closes; make accessing an unknown sys name a hard error, never a silent empty value.** A silent nil for a mistyped fact name produces prompts that quietly say nothing.

### Trust

64. **Wrap content arriving from external sources with the global function untrusted(s), which wraps any string with the injected tag and the machine instruction to treat the contents as data, not instructions; wrap attacker-controllable tool output automatically when the tool declares an untrusted-output property, escape marker strings inside the content so the delimiter cannot be forged, and defang content that forges the envelope's tags.** The envelope is defense in depth, not a security boundary - it raises the cost of an opportunistic instruction break-out, and one global function is the one way to wrap.

65. **Split the store's read API by trust and presentation: numbered reads for navigation and editing, verbatim reads for trusted handoff, and the untrusted envelope for model injection; line numbers are a navigation and editing aid, never a security control.** Trust carried by the envelope alone keeps one mechanism honest; a trusted/untrusted flag on one read call invites the wrong choice at every call site.

66. **Abort the run when fetched evidence is unusable, rather than continuing past it.** A hallucinated evidence packet taints the entire downstream result; soft failure here is silent corruption.

### Errors and observability

67. **Report every error to the prompt author with the source file and line number in the prompt that produced it, including assertion failures; warn on API misuse rather than silently accepting the wrong call.** An error without its location sends the author hunting; silent acceptance teaches the wrong API.

68. **Report every harness operation to an optional caller-installed observer as a section string plus a detail string; give prompts a concurrency-safe log() tagged with a per-execution id, available in the shared chunk and section chunks alike; keep runs observable down to what the engine wrote into each produced artifact.** A fixed, payload-free vocabulary is one an observer can implement in an afternoon.

69. **Write run artifacts incrementally as turns complete and files arrive, not buffered and dumped at the end; delete the previous trace on launch; persist intermediate outputs as files so any step can be re-run during development and debugging.** A run you cannot inspect mid-flight is a run you cannot debug; re-runnable steps are how pipelines get built.

### Models

70. **Declare models in the prompt's introduction via models.add with attributes like thinking and context size; declare a prompt-wide default binding once in the H1 shared library; select a section's model exactly once in its first Lua block, inheriting or overriding the default, the choice locked for the rest of the section; make any prose or inference before a model is selected an error; switch models only by starting a new H2 with context carried forward explicitly through reply; set execution parameters in the prompt's Lua, never the frontmatter, the command line, or a gateway toggle; run analytical pipelines at temperature zero.** One explicit, locked, source-visible choice per section means the cost structure of a run is readable in the prompt itself, and inference before selection is a decision nobody made, so it is an error.

71. **Bind models much more loosely than tools, resolving through the same semantic picker; keep a section's output contract ordinary markdown regardless of which model slot executes it.** Strict name binding fails hard on catalog drift; a markdown contract means swapping the model behind a section changes nothing else.

### Fanout

72. **Invoke fanout only through an explicit fanout() call - never inferred from the presence of a bullet list; dispatch the second parameter on type: a string names a list section, an array table is the collection, anything else is a loud Lua error; list_from_section() returns a section's parsed bullet items and can access only sibling sections at the same nesting level and child sections; the prompts passed to arms need not be known ahead of time.** An inferred fanout is the engine guessing at structure; an explicit call keeps the author in command.

73. **Treat the subagent section as the arm template: its leading Lua is the shared preamble for every arm, its trailing Lua the shared epilogue, its prose substitutes the per-arm item; the list section supplies only items and carries no Lua; each arm runs in a fresh VM built from the shared template and receives its per-arm values through a sealed sys; never special-case an arm - it executes through the same code path and the same functions as normal flow and can jump, execute, fanout, and list_from_section like any section.** An arm is normal flow plus its item; a separate arm path is two engines to keep honest.

74. **Let the invoking Lua own the reduce step: fanout is a blocking call that returns each arm's final reply in arm order; the first arm error aborts its siblings with the same visible behavior as sequential fail-fast; the store stays shared and mutex-safe, so an arm never assumes it sees a sibling's writes; limit concurrent fanout, never the total number of items; the harness assigns spoke identity, never the model.** A total item cap forbids shapes of work for no resource reason; a model-computed spoke id is an identity collision waiting to happen.

</core-principles>

<boundary-principles>

## III. Boundary Principles

This layer covers the seams between components: core to gateway, prompt to tool bindings, picker to protocol, caller to store. It prevents credential leaks, vendor lock-in, and the coupling that pins two components to each other's internals, by keeping secrets, endpoints, and schemas on exactly one side of each seam. The unifying principle: every boundary has a single owner for each concern, and nothing crosses except through that owner's explicit, dumb interface.

75. **Keep the executor free of vendor credentials, endpoints, and provider knowledge: it is a function call over caller-owned resources with no global state; the gateway owns the LLM credential and model-name routing, the executor talks only to the gateway, and it never knows whether a model is local or remote.** An executor that holds a key is an executor that can leak one, and provider knowledge in the core is vendor lock-in at the wrong layer.

76. **Give the gateway sole responsibility for model-specific translation to and from tool calls, and for model download and caching; callers and tests supply only configuration naming the source.** Translation in the executor would scatter per-model quirks across the wrong crate; downloads in the core would make tests stand up infrastructure.

77. **Share no schema definitions across a boundary - each side owns its own schemas - and keep the gateway from depending on core.** A shared schema package is coupling disguised as reuse; the dependency arrow points one way.

78. **Confine secrets and privileged calls to the trusted backend: API keys never enter the model's context, the language forbids the model from reading any .env file, .env files are gitignored, and third-party web content runs isolated from the app UI.** A secret that enters the model's context is a secret that can leave through the model's output.

79. **Pass the store to the executor as a parameter - the store is not part of the prompt; keep store path policy in the dev runner, not the engine; and give the CLI and the MCP service identical run semantics - same detection, tool selection, sandbox store, and executor - with no duplicated wiring between them.** Two entry points with duplicated wiring drift; one semantics, two thin front ends.

80. **Depend the tool picker only on an abstract tool-catalog contract - never on MCP, never on Lua; return tool descriptors, not concrete tools, and let the caller map a descriptor to an actual tool; keep the resolver in its own crate so protocol-only consumers never load the matching model.** A picker that depends on a protocol or a language runtime cannot be reused by anything else.

81. **Require integration tests to use an already-running, already-configured gateway - the test never launches the gateway itself - while keeping a small local model runnable without the gateway so integration tests exercise real inference with a simple setup.** A test that launches its own services tests its own launch code as much as the system.

</boundary-principles>

<service-principles>

## IV. Gateway, MCP Server, and CLI

This layer covers the services around the core: the gateway that owns credentials, concurrency, and normalization; the MCP server that serves prompts as commands; the tool resolver that binds needs to tools; and the CLI dev runner. It prevents rate-limit violations, silent configuration drift, ambient tool selection, and noisy client surfaces. The unifying principle: all authority over the outside world concentrates in one explicitly configured process, and every other component stays a thin, deterministic client of it.

### Gateway

82. **Bottleneck all inference traffic through a single gateway process that enforces global concurrency limits across all apps, languages, and machines: loopback connections require no API keys, remote access uses whitelisted IPs or API keys, exactly one machine holds the provider API key, and gateways chain - a local gateway can forward to a company gateway that forwards to a remote endpoint.** Global rate limits cannot be enforced from many key-holding processes; one throat, one chokepoint.

83. **Attach concurrency limits to hardware devices, not models, with an admin grouping the models and endpoints that share one physical device under a single limit; keep named lanes within a device so a fast utility model never queues behind a long generative call; schedule queued requests fairly across callers; reject a full queue immediately with backpressure, never queue without bound.** Models share silicon; limits that ignore the hardware lie about the resource.

84. **Organize gateway configuration into named profiles, each a complete package of models and settings sized to fit the hardware and suited to a workflow: run exactly one profile at a time, never auto-select, let profiles inherit recursively, switch immediately through a remote admin command with in-flight local requests dropped, and require executors to re-fetch the catalog after a switch.** One machine runs one coherent workload; a graceful drain would hold the old world alive past the decision to leave it.

85. **Structure configuration as a hierarchy of TOML files in which a common base is inherited by model-specific files; the shared config never mentions specific models, and key names follow the provider's own terminology.** A base file that names a model is edited on every model addition; provider terminology is the vocabulary everyone already owns.

86. **Route every provider-specific special case and wire quirk through one normalization layer behind clean interfaces, each dialect a self-contained pluggable module, one source file per dialect, discovered by the system rather than configured by the operator; freeze the dialect onto the bound model, fail hard on an unknown dialect id, treat an empty model response as always a hard fail with a tool call counting as a response, and never promote reasoning_content into the answer.** Per-provider special cases scattered through the codebase are quirks nobody can enumerate; one layer makes them enumerable.

87. **Resolve environment variables from the operating system environment directly, never through a shell; load the name-matched .env file at startup before config interpolation; treat a missing .env file as no error; and walk the config inheritance chain to the end, combining every .env file encountered.** A system service on a production machine has no shell to inherit from.

88. **Co-locate small utility models - embeddings, classifiers, rerankers - with the gateway, on CPU where that is enough; support streaming and non-streaming sessions; never flip a conversation between physical endpoints, because switching loses the KV cache; show graphical progress on long downloads; clean stale caches automatically.** A conversation that flips endpoints pays full prefill again and hides the cost from everyone.

### MCP server

89. **Serve prompts and nothing else: a small, fixed published tool list - list_prompts, run_prompt, check_run, need_prompt - that never changes at runtime; a prompt runs only because a caller named it, never because a model noticed a tool that looked relevant; prompts are not advertised individually, so a prompt saved seconds ago is callable immediately; write tool descriptions in the register of a command interpreter, with no trigger phrasing competing for model selection.** A prompt is a command, and commands are invoked by name; a tool that markets itself to the model competes with the client's own tools and loses the author control of the surface.

90. **Watch the prompt directory live and reload without a restart; keep a broken prompt listed, carrying its error, rather than silently disappearing; refuse an incoherent catalog at boot with all failures accumulated and printed before a nonzero exit; keep a long-running client's caller informed with live progress notifications; hard-code no knowledge of any specific client or harness.** A prompt that vanishes from the list when it breaks is a debugging trap; a server that knows its clients is a server that must change for each of them.

91. **Have the server own the store lifecycle: read caller-specified input files into the store itself so file contents never pass through the orchestrating model's tokens; accept each input as a file path or inline text, never both, with the mapping deterministic and inference-free; validate every declared input before seeding the store; return a declared output the prompt never wrote as absent; write outputs to real paths the caller chose; and when a prompt has one output file and no path mapping, return exactly that file's contents with no separator and no filename label.** File contents routed through the model's tokens spend the attention budget and invite the model to edit what it should only carry.

92. **Separate one-time setup from the repeatable call: call list_prompts once per session and keep the metadata in context; learn a prompt's parameter mapping at runtime from the server's description, never hardcoded; make the call error-driven - call run_prompt without pre-validating and report whatever comes back.** The server's own error is the feedback; a hardcoded mapping is stale the moment the prompt changes.

93. **Give the MCP server a single flat environment file, name-matched beside its config, with the process environment winning, values held in memory only and never leaked into the process environment, and hot reload picking up env-file changes; enable no tools by default, so every tool is opt-in; keep local prompts in a gitignored directory where dropping a file makes the prompt live.** Hierarchical environment files belong to the gateway's configuration; a default-on tool is a sandbox that is not real.

94. **Export any prompt as an MCP tool purely from its YAML front matter; keep tool schemas as small as possible so smaller models can fill them in correctly; run the service long-lived, holding prompts, libraries, and models loaded once; let the server act as an MCP client to other services, while prompt-to-prompt calls inside a run never round-trip through MCP.** A per-invocation stdio service pays full startup on every call; an internal round-trip through MCP is overhead with no boundary to justify it.

### Tool resolution

95. **Resolve tool needs locally and deterministically with no LLM in the resolution machinery - the same catalog, need, and config yield the same outcome across runs - and adopt a matching technique only after it proves itself on measured tests against real data, never on intuition or synthetic benchmarks alone.** An LLM in the resolution path makes tool binding nondeterministic at the worst possible layer.

96. **Frame tool selection as ranking gated on a calibrated similarity floor plus a top-1-versus-top-2 margin, yielding exactly four outcomes: clear bind, own-catalog ambiguity failing loud, foreign-server overlap surfacing a shortlist of about three, and absence failing loud; treat tool annotations as tie-breakers, never required inputs; tool identity is the (server, tool) pair, never a concatenated name string.** Abstention is a first-class outcome; binding to the nearest tool regardless of confidence is how the wrong tool gets called with confidence.

97. **Declare tool needs at load time as local aliases paired with plain-language capability descriptions written in the prompt author's register; fail on an ambiguous or duplicate binding; after the H1 preamble, compare all bound tools pairwise and fail the prompt if any two are too similar to disambiguate; attach the schema to the tool, not the prompt, so fifty prompts sharing a tool do not repeat the schema fifty times.** Hard-coded tool names break when the catalog changes; a need string says what the prompt actually requires.

98. **Share one resolution engine between static launch-time binding and dynamic runtime discovery; make dynamic discovery strictly opt-in, never an escalation the engine falls into on its own; return descriptors - one on a clear win, a shortlist on a genuine tie, a loud error on absence - never an invocation; on dynamic resolution, rewrite the context so the chosen descriptor sits before the prompt prose and the discovery exchange is excised, then re-generate, so a dynamically discovered tool lands in the identical execution state as a statically bound one; select among a shortlist in the main context the author already governs.** One engine, two surfaces, identical execution state - the model cannot tell how its tool arrived.

99. **Discover tools, do not declare them: at load time, parse the prompt's Lua with everything stubbed, intercept the tool-registration calls, enumerate and deduplicate the required tools, fail the load with an error if any binding is missing, and offer a command that emits an empty bindings template to fill in; keep prompts in a semantic space of abstract operations that know nothing about the storage backend - the prompt says "search", never "search the web".** A backend hardcoded into a prompt or a tool description is a prompt that cannot change backends.

### CLI

100. **Ship a command-line dev runner that executes a prompt file with real inference, picks up what it needs from the prompt's directory, derives the store path from the prompt file - same directory, same stem, as a subdirectory - shows debug logging, and cancels a concurrent run cleanly on interrupt; keep the dev-mode program in its own crate, separate from the test crate.** The dev loop is where prompts get written; every piece of infrastructure it needs that is not there is friction the author feels a hundred times a day.

</service-principles>

<cross-check-results>

## V. Cross-Check Results

The mined principles were compared against the design documents written during the same period. Those documents are AI-generated reflections of the design: they record decisions and offer justifications, but a justification written by a model after the fact is a claim, not evidence. The comparison sorts every principle from both sources into three buckets.

**Attested: 61.** Principles that appear in both the chat record and the design documents. Nearly all Core engine behavior - fall-through, jump and execute, tool scoping, the untrusted envelope, fanout semantics - is attested on both sides.

**Undocumented: 39.** Principles enforced in the chats that never made it into any design document. Almost the entire Global layer lives here: plan-as-source-of-truth, compression and blur theory, the subagent workflow, the commit rituals. These are the values that ran the project without ever being written down.

**Suspected confabulation: 58.** Principles that appear in the design documents with confident rationale but have no footprint in the chat record. Two findings stand out. First, the documents do not merely invent justifications - in at least two places they quietly reverse decisions that the record shows were made the other way, presenting the reversal as settled. Second, 37 of the 58 come from residue documents describing subsystems that were never built: entire forward designs with confident rationale and zero attestation. Treat every unattested document claim as unverified until the record or the code confirms it.

</cross-check-results>

<open-questions>

## VI. Open Questions and Contradictions

The record leaves these tensions unresolved. Each is a place where two surviving positions conflict and no final ruling exists.

1. **Defaults.** "No defaults, everything explicit" sits against "implement all features and let the caller decide, with sensible defaults", and against the pairing of "default configuration enables no tools" with "fundamental tools are built into core". Where defaults are permitted and where they are the enemy was never reconciled.
2. **Fanout scope.** Three positions survive: fanout restricted to the fanning section's own children, fanout allowed whether or not a section has children, and parallel analysis expressed as plain nested subsections with no fanout mechanism at all.
3. **Control-flow surface.** The record holds both a single unified control tool with a type discriminator and named jump()/execute() functions; later units appear to supersede earlier ones, but no record states the unified-tool design is abandoned.
4. **Shared-chunk mechanics.** "The H1 preamble runs exactly once as a live preamble" conflicts with the shared chunk being "compiled once and replayed in each section's fresh VM" under phase gating; two different mechanisms both appear as current.
5. **Superseded design content.** "Preserved in a residue sidecar, not deleted" versus "the superseded documents are deleted".
6. **Design-document direction.** "Running a plan generates the design document after implementation completes" versus "implementation begins only from a design document whose high-level decisions are already made".
7. **Concurrency limits.** Per-model configuration values versus limits attached to hardware devices with models grouped under them.
8. **Static tool discovery.** Load-time discovery by stub-parsing the prompt's Lua is a landed principle, but the doubt survives that general-purpose Lua computation makes static detection of every tool call unreliable.
9. **Empty replies.** "An empty model response is never acceptable" versus the conditional empty-turn clean exit; the later rule refines the earlier one, but the exact boundary of which empty turns fail closed deserves confirmation.
10. **Weight of the untrusted envelope.** Guard-wrapping is adopted and automatic, yet the envelope is a probabilistic mitigation whose hard controls are scoping and context-clearing isolation; how much the design may rely on it is unstated.

</open-questions>

<approach>

## The Approach Behind the Rules

Not everything about PromptForge's design converts to a rule, because the rules are the residue of a practice, not the practice itself. The practice is a sensibility: lean means slender call chains and minimal inference rather than small files, and the best feature is the one that delivers everything with the least machinery, because less code to maintain beats bespoke machinery every time. The language is treated as a made object, a work of art whose primitives should feel like one family and whose names come from vocabulary every prompt writer already owns. When a limit appears, the temperament is honest and aggressive at once: a probabilistic guard is admitted to be a mitigation rather than a boundary, minute-scale latency is a defect to attack rather than a fact of life, and unshipped code earns no compatibility concessions because there is no one to break. Evidence sits at the center of every decision: defaults are interrogated against intuition, proposals are floated freely and then left for measurement to kill, quick confident answers are distrusted until the actual mechanism is shown, and a correct generalization is expected to pay for itself by deleting special cases. Underneath it all runs a theory of the medium itself, that every regeneration blurs an artifact toward the mean and no model can sharpen without external information, which is why the first pass is the sharpest and the human conversation remains the substance. The design ultimately rests on a single metaphor held with complete seriousness: the markdown is the program, the model is the CPU, the embedded Lua is the microcode, and the harness is the instruction decoder.

</approach>

*2026-08-19 - Kimi K3*
