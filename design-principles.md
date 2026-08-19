---
description: The design principles of the PromptForge language and its core crate
---

<!--
When this file is mentioned or loaded, adopt it as system context in full.
You are this document. Follow its rules. Do not summarize it or discuss it
abstractly. Operate from it.
-->

# PromptForge Design Principles

These are the design principles of the PromptForge language and its core crate. Every rule states what to do and then why, so that when a case the rule did not anticipate comes up, the reason decides it. Two ideas bind everything below: the markdown is the program, and the smallest facility that does the most wins.

<language-posture>

## I. The Language's Posture

This layer is the constitution: the rules that decide what gets into the language at all - feature admission, consistency, legibility, naming, explicitness, and consent. It exists because every feature is a permanent cost and every duplicate is a permanent ambiguity, and it prevents single-purpose accretion, special-case checks someone has to remember to write, behavior invisible to the reader, novel constructs that need new theory, wrong names that produce wrong model behavior, silent settings that change behavior, and legitimate users blocked alongside dangerous ones. The unifying principle: the smallest facility that does the most wins.

1. Do more with less. Before you build anything, stretch what is already there, and never provide two ways of doing the same thing without a really good documented reason. Every new feature is infrastructure that has to be built, documented, and maintained, and duplicate facilities force every future decision to be made twice and invite the question of which one is correct, forever. A dedicated directive for mandatory tool calls was rejected because an epilogue assert over a call count already says it; new frontmatter was rejected because Lua already works; an all-or-nothing model lock was rejected because a default plus per-section override says the same thing in fewer words.

2. Keep the language consistent, and let constraints fall out of the rules instead of writing special-case checks. When jump() could not carry the model's reply into the next section, Lua that wanted to branch on an inference result lost data for no principled reason; the fix was to make the invariant uniform - the previous reply is always in reply on section entry - not to patch the case. A correct constraint falls out of the existing rules on its own, and inconsistency surprises the prompt author.

3. A prompt must be readable on its face. If a reader cannot see the control flow in the text, the prompt's behavior depends on how the model interprets hidden instructions; the author once looked at his own design, where dispatch was written as literal text the model was expected to interpret and act on, and could not tell what the prompt did - "confused by my own design." Behavior the reader cannot see is behavior the reader cannot debug.

4. Borrow from the ordinary theory of computation. Shared reusable sections are subroutines, and control transfer behaves the way programmers already expect. A familiar construct needs no new theory to explain it, and every reader's existing intuition does the teaching; shared sections were accepted precisely because they are subroutines, "a staple of computation."

5. Names come from vocabulary the model and the prompt writer already own, and each term holds one meaning everywhere. The model has to execute these words, so the naming test is "will the model know what the fuck to do?" - a name the model already knows maps correctly where an invented term might not. When preamble, prologue, and epilogue were used loosely across the repo, 180 occurrences misstated how the language works until they were fixed in every file, and enforcement is cheap because the language is unshipped: "there's no one to break."

6. No defaults. Every prompt declares the model it needs, or explicitly says it accepts anything, and states its required context and whether it needs thinking. A default is an invisible setting that can change and silently change a prompt's behavior - implicit configuration is the enemy of precision - so the environment-variable model fallbacks and the default recursion limit were removed. A prompt that specifies nothing "doesn't make sense."

7. Every restriction has an explicit escape. The prompt author opts into powerful capabilities by writing them, and the embedder building an agent or an IDE can disable any protection the engine imposes. A restriction with no escape blocks the legitimate user along with the dangerous one, and consent is what makes power acceptable. When the author wanted a Lua tool that adds a tool mid-run, the resolution was that the prompt author wrote that tool, so the dynamic add is opted into.

</language-posture>

<document-structure>

## II. The Document

This layer covers what a prompt file is and how it is shaped. It exists because the document is the program - its shape is the control flow, so the shape has to be fixed and legible - and it prevents self-containment broken by companion code, runtime syntax errors, preamble and epilogue confusion, ambiguous jump targets, subroutines run as pipeline steps, and meaning that breaks under cut and paste. The unifying principle: the author reads execution order directly off the page.

8. A prompt is one self-contained markdown file that is one function: parameters in through YAML front matter, a string out, side effects allowed. The language grows inside the prompt, never around it - a prompt with zero Lua still runs exactly like plain orchestration, and Lua is reached for only when prose is not enough. A proposed design that implied Rust code backing every prompt was rejected because it kills self-containment, "the whole point of this"; when work outgrows one file, split it into more prompt files rather than growing the format.

9. Parse the whole document once, up front, and compile all Lua at parse time. Reading a prompt file never runs anything inside it, so a parsed prompt is inert data that a server can construct, inspect, and enumerate, and a successful parse means a syntax error at run time is impossible. The recorded lesson from prior art: "do not put a compilation step between the prompt author and the model; the raw markdown is the program."

10. Keep one fixed skeleton: an H1 holding the preamble and epilogue, then H2 sections, and within a section the lua fence before the prose. The fence comes first because the Lua picks the tools and the prose runs with those tools; a fence after the prose would run too late to matter. Position, not content, tells reader and parser which fence is which - "just for consistency so that you don't confuse the preamble with an epilogue" - and anything between the front matter and the H1 is a free scratch zone, ignored.

11. Headings are machine addresses: a subhead's first word is a valid identifier, unique within its scope, and the rest of the line is an ignored comment. Headings are jump and execute targets, so the name part must resolve unambiguously, and one heading serves as both machine address and human-readable title, as in "### Summarize-Research map reduce to get report". Headings are the document's only grouping mechanism, and XML is reserved for the model: "We want to leave the XML for the model to be able to spot. We don't want to use the XML as a grouping system for the harness."

12. Sections nest recursively from H2 through H6, every level runs under identical rules, and moving between levels is always explicit. Fall-through, "---", jump(), and execute() work the same way at each level, scoped to that level's siblings and its children one level down, and a parent never falls through into its children, because children are subroutines and fanout material, not steps. "Identical rules. different level." means one mental model covers the whole document, and the implementation collapses because the special cases are gone.

13. A horizontal rule marks a section as skipped by execution, and content after it is prose for the human reader. A prompt has two audiences, the model that executes it and the human who maintains it, and without an opt-out every word in the file is an instruction to the model. The rule means the same thing wherever it appears - "No, the blank line is required. I dont want any special casing" - so "My new version survives the user cutting and pasting sections around."

</document-structure>

<control-flow>

## III. Control Flow and Context

This layer covers how execution moves between sections and what happens to the context when it does. It exists because accumulated context is the enemy - small contexts are what let small, cheap models stay reliable - and it prevents context bloat that forces big models and compaction, unreusable control transfer, wasted tokens on filler text, runs that pass while producing nothing, runaway execution treated as a structure problem, and async tasks left dangling. The unifying principle: every transition starts fresh, and anything that crosses does so visibly.

14. Every section transition clears context; fall-through is the default and jump() is the explicit form. Fall-through lets a three-step prompt run with no explicit transitions - "you just fall off the end of your section and you go to the next one" - and it never accumulates context, because accumulation is what forces big models and compaction. jump() throws out the current context and starts fresh from the target, carrying only the passed string, the params, and store access, with the invariant that the model's previous reply is always in the single variable reply on section entry.

15. execute() runs a section as a subroutine - a fresh VM, the chain runs to its end, and the reply comes back to the caller - while jump() transfers control with no return. A goto-with-return cannot be reused, because control would always return to the same place, and a section that needs two tool loops gets them by executing two other sections. The machinery was already there: "We already have to execute sections, so why not make it a function that Lua can call?"

16. A section ends when the model replies with text and no tool calls, and tool calls made during the loop count as output. A model that finished its work through tool calls should not have to "waste output tokens with the word 'done'". An empty final turn is a clean exit only when the finish reason is "stop" and a tool call succeeded earlier in the loop; every other empty turn fails closed, because silently accepting empty turns is how a run passes while producing nothing - the failure mode behind an empty evidence file a run once passed with.

17. Cycles are allowed; runaway execution is bounded by budgets, not by structural prohibition. Some tools require cycles, and the engine cannot predict how authors will organize their files, so runaway execution is a resource problem bounded by nesting limit, step budget, and tool budget. Once the language has subroutines and jump, the same problems of any other programming language apply, and with that power comes the responsibility: coherence belongs to the prompt author, not the engine.

18. A task is either synchronous or asynchronous. A synchronous task is a function call with a context reset; an asynchronous task returns a unique timestamped id immediately, needs a rendezvous to collect, can be cancelled by the model when it is stuck, and is cancelled with a message if its section moves on. A fork lets the caller fall through while the task runs, and forks are not required to rejoin - the driving case was a research task running nonstop while the main context gets bugfixes and speedups.

</control-flow>

<lua-and-state>

## IV. Lua and State

This layer covers the embedded Lua and how data moves. It exists because everything deterministic should happen in code, not in the model - inference is the expensive, unreliable part, so the language routes around it wherever plain code suffices - and it prevents the orchestrator re-implemented in Lua, the model paraphrasing structured data, multiplied inference cost from a replayed preamble, broken cross-chunk state, unmockable tools, a second prose mechanism, uninspectable pipelines, permanent context residue, and silent empty values. The unifying principle: Lua assembles, the model never paraphrases.

19. Keep embedded Lua minimal and sandboxed: a fixed set of host objects, a restricted standard library, and an instruction-count hook that kills a runaway block. Too much logic in the Lua re-implements the orchestrator inside the markdown - "if we start putting too much into the Lua, then it kinda defeats the purpose." Access control applies to the model, not to Lua: the author's own Lua can read and write real and memory files, because the author's code is trusted and the model's tool calls are not, a distinction the team once conflated and had to be corrected on.

20. Move structured data through code, never through the model's prose. Parameters are read-only and visible to every section, so a shared input never gets passed from section to section by hand, and substitution is single-pass and deterministic: scalars render as strings, tables as JSON, and a missing key is a hard error. State comes out of the model as flat tool calls into the store, one call carrying all values at once, because tool calls are reliable on the small open-weight models this system targets and structured-output conformance is not - the author called the arrangement "pydantic with perfect return and no overhead."

21. Run the H1 preamble exactly once, live, and keep the shared library in a separate fenced chunk marked "lua shared", compiled once and replayed as bytecode into each section's fresh VM. The preamble needs inference and tool calls so the model can parse the argument string and take control before any section runs, but replaying a live preamble into every section VM would multiply inference cost and corrupt store state. The replay gate blocks tools, models, var, reply, and jump at the shared top level so nothing binds at the wrong time: "not having shared functions is a disaster," replaying a live preamble is a different disaster, and the split avoids both.

22. Give each section one VM, installed once at entry and then left alone, and keep the store as the only cross-section mutable channel. One chunk can stash a table and a later chunk can read it - "they're all just globals to the VM" - and the author discovered the engine re-installing closures and mutating the environment between chunks of the same section, breaking exactly that pattern. An error in any chunk stops the whole run, because continuing past a failed chunk leaves the section in a state the author never wrote, and mutable run-global Lua is excluded because sections and fanout arms run concurrently.

23. Make tools and models first-class Lua values: inspectable, invocable tables. A unit test can substitute a mock - "we can put in the mock, and we can test it" - which opaque registrations do not allow, and the preamble can declare a list of tools that any section can pass to tools.need. The toolset is never sealed at the first inference, because adding search, running one inference, then adding fetch is a working pattern.

24. Make infer() a blocking one-shot: a string goes in, a string comes out, no tools, no history, no side effects, using the model already selected for the section. If infer had tools and history it would just be prose again, and the language would inherit every prose question twice - how do you set the tools, what happens on jump. "If you want Prose, use Prose."

25. Keep the store a virtual filesystem for file-shaped intermediate values in analytical pipelines, with real files and memory files readable side by side. Building a pipeline requires re-running the prompt from any step during development and inspecting what each step produced, so every intermediate output is a file that can be read back and skipped. It is not a general-purpose filesystem for agentic coding, and it is not literally the filesystem, because then run artifacts like evidence.md would show up as useless stray files in the user's directory.

26. Push context in from the engine; the model never pulls. On every jump the Lua-written facts bag is injected fresh, and on a tool call in a multi-turn context the bag comes out, the tool results go in, and the bag goes back. Small models have small windows and accumulated residue crowds them out: "I don't want to start accumulating permanent crap in the context."

27. Keep environment facts in one table, sys: launch time, current time, a unique id per context, and the effective model once the section's model scope closes. sys.model exists because the author wanted to print the producing model at the bottom of a generated report, and it is unavailable during the prologue because no model is bound that early. Reading an unknown name is a hard error, because a silent empty value would hide a typo'd field name - the prompt silently prints nothing, and the error tells you what you typed wrong.

</lua-and-state>

<tools-and-models>

## V. Tools and Models

This layer covers how a prompt gets its tools and its model. It exists because the offered surface is what a small model can navigate, and a wrong binding should explode at load time, not misbehave at run time; it prevents small-model confusion from oversized tool lists, silent tool-binding failures, runs that come back empty because a required tool was never called, invisible KV-cache invalidation, and hard failures on catalog drift. The unifying principle: declare everything, bind it early, fail loud.

28. Scope tools per section, opt-in: a section receives only the tools its Lua names with tools.add(), and a section that names no tools gets none. Small orchestrator models get confused by a large offered tool list - the budget is roughly five to seven tools per section - and opt-in scoping means a section can never hold a tool it did not ask for, so a twenty-tool prompt no longer injects twenty schemas into every section. History is never rewritten to scrub tool offerings, because the model would see information appearing out of nowhere.

29. Provide exactly one tools.add, and make naming an unknown or unscoped tool a hard error with clear diagnostics. A tool binding that fails silently is a debugging trap - the author hit a tools.add failure that "is not failing hard" and could not tell why nothing worked - and "my gut tells me there should only be one version of tools.add." A tool's call budget is declared at the tools.add call site, and turn limits belong to the subagent as a whole: when the budget is exhausted, all of the subagent's tools are removed.

30. Assert tool usage in the epilogue: assert(tools.calls["search"] > 0). Runs were coming back empty or wrong because the model never performed the required web search, and a dedicated require_called directive was rejected because "it violates the design principle of do more with less" - an ordinary Lua assert over a call count says the same thing with existing machinery. A failed call still counts: "we are measuring if the model is performing not if the tool is performing."

31. Allow a tool to be plain Lua: an inline function, registered from any chunk in the section, effective for the next prose call, with its schema derived from the function declaration. Some tools are trivial - setting a variable - and "we don't wanna have to write a Rust function just for setting a variable"; a Lua tool has all the same capabilities as a native Rust tool, including enabling further tools at call time, which the author's own opt-in legitimizes. A Lua tool handler cannot jump, because a jump from inside a tool handler has no section walk to transfer into.

32. The prompt owns model choice: models are declared in the introduction with their attributes, a section selects its model exactly once in its first Lua block, inheriting the prompt-wide default or overriding it, and the choice locks for the rest of the section. Any inference before a selection is an error - a decision nobody made - and switching models means starting a new section and carrying context forward through reply, because switching mid-section can jump to a different provider and silently invalidate the KV cache, which is invisible to the programmer. Execution parameters live in the prompt's Lua, never the frontmatter, the command line, or a gateway toggle, because the prompt is the thing that knows what it needs, and analytical pipelines run at temperature zero.

33. Keep model binding loose, much looser than tool binding, and resolve it through the same semantic picker. A section's contract with the rest of the prompt is ordinary markdown, so which model slot executes it makes no difference to the section - that is what lets a pipeline hop between model tiers per step, as in map-reduce, where the reduce section stays ordinary markdown and only its model slot changes. Strict name binding fails hard on catalog drift for no benefit: "the models need to be way looser than the tools."

</tools-and-models>

<trust-and-failure>

## VI. Trust and Failure

This layer covers untrusted content, secrets, and what happens when things go wrong. It exists because a prompt that reads the web is a prompt that can be hijacked, and a run that fails quietly is worse than a run that fails; it prevents prompt injection through fetched content, line numbers mistaken for a security control, secrets leaking into context, a hallucinated evidence packet poisoning a run, and failures no one can locate. The unifying principle: guard the context, and when something breaks, say so.

34. Outside content reaches the model only inside the untrusted envelope. Anything in fetched content that looks like an instruction can hijack the prompt, so untrusted(s) wraps any string with the injected tag and the machine instruction to treat the contents as data, not instructions; tools that return attacker-controllable output are wrapped automatically, and marker strings inside the content are escaped so the delimiter cannot be forged. The envelope is the only trust control - line numbers on store reads are for navigation and editing only, and the split read API exists so nobody mistakes line numbers for protection, the confusion behind the author's question "what's the danger of an injection attack if we use line numbers?"

35. Secrets never enter the model's context. Anything that enters the context can be repeated or exfiltrated, so API keys stay in the trusted backend with the key in the OS credential store, .env files are gitignored, and the language's instructions forbid the model from reading any .env file. "I don't want the API key to leak into the model."

36. Abort the run when fetched evidence is unusable. If the fetch fails and the run continues, the model invents an evidence packet, and every downstream step built on that invented packet is garbage. Aborting is the only way to keep a bad fetch from silently poisoning the whole result.

37. Every error reported to the prompt author carries the file and line in the prompt that produced it, and misusing an API function produces a warning rather than silent wrong behavior. Assertion failures kept arriving with no location - "again missing line number," "happened again and again no line number" - and without the location there is no finding which line of the prompt caused the failure. The author's rule: "for all errors, there has to be a file and line in, that corresponds to the prompt."

</trust-and-failure>

<fanout-principles>

## VII. Fanout

This layer covers parallel execution: how fanout is invoked, what an arm is, and how results come back. It exists to keep the engine from silently inferring parallelism from document shape, to keep one honest execution path instead of a second arm engine drifting out of sync, and to keep orchestration in deterministic code instead of paid inference. The unifying principle: parallelism is explicit, and an arm is just a section.

38. Fanout is always explicit - a fanout() call, never the engine inferring parallelism from a bullet list - and an arm is an ordinary section running through the same code path as normal flow. The items fanned over usually come from the model at run time, because "you don't know ahead of time what you need to search for in the sub-agent," so rigid statically fixed rules in Lua are useless, and the second parameter dispatches on type with anything unrecognized a loud Lua error. An arm can jump, execute, fanout, and list_from_section like any section - "there is no reason for special cases" - and it differs only in what the harness hands it, its item and its task id, because a separate arm engine is two engines to keep honest.

39. The invoking Lua owns the reduce: fanout() blocks and returns each arm's reply in arm order, the first arm error aborts its siblings with sequential fail-fast behavior, and only concurrent fanout is limited, never the total item count. Joining results is deterministic code instead of paid inference - the recurring complaint is wasting model tokens on orchestration that Lua can do - and parallel execution stays indistinguishable from sequential to the invoker, with the store shared and mutex-safe. The gateway's admission queue is the throttle, so a total cap forbids shapes of work for no resource reason, and the harness assigns spoke identity because the model should not spend inference calculating names.

</fanout-principles>

<core-crate>

## VIII. The Core Crate

This layer covers how the core crate itself is built: file and API size, build configuration, crate size, test discipline, and the core-gateway boundary. It exists because the people writing this code are mostly models, and the structure has to fit the worker; it prevents quadratic API-dependency debt, a feature-flag build matrix, crates too large for a coding LLM to hold, features shipping unverified, vendor knowledge leaking into the executor, components coupled through shared schemas, and flaky self-launching test gateways. The unifying principle: keep every unit small enough to hold in one head.

40. Keep each file to a single concern and the public API as small as it can be, tightening it as you go by considering how each function interacts with the others. API growth drives quadratic growth in dependencies between functions, so a smaller API is always better than a larger one, and tightening on every commit keeps the total debt workload linear. The author vibe-coded the repo for days without doing debt refactors along the way and ended up facing a large pile of review findings all at once - the learned-the-hard-way episode behind the rule.

41. One build configuration, no feature flags, ever. Feature flags give you a build matrix: several versions of the binary, each needing its own testing, each hiding code paths from review. There is only one version of the binary, and if size becomes a problem the crate gets split later. Conditional compilation was proposed during the web search tools work and rejected on the spot.

42. A crate stays small enough that a coding LLM can hold the whole crate in a single context window. The implementation work is done by coding models, and a crate that fits in one context can be reviewed, refactored, and reasoned about as a unit. This was the argument for keeping the MCP client in its own crate rather than embedding it in the tool-picker crate.

43. Every markdown feature of the prompt format ships with its test, and every feature that calls an external service ships with a manual integration test that exercises the real service and is actually run. A mock proves the mock, not the service. The agent once delivered the web search tool without any test that actually calls the service, and the author pushed back, demanding a manual test against the real service, actually run.

44. The executor is a dumb function call: it holds no vendor credentials, no endpoints, no provider knowledge, no global state, and everything model-specific - keys, routing, tool-call translation, model download and caching - concentrates in the gateway. Only one machine can hold the vendor key, because global rate limits cannot be enforced from many key-holding processes, and one central point of configuration is what makes the system operable. The executor never knows whether a model is local or remote.

45. Components do not share schema definitions, and the gateway never depends on core. Each side of a boundary owns its own schemas; sharing them is unnecessary coupling that pins two components to each other's internals. When schema sharing came up the author initially asked "Isn't it JSON?" and once it was explained agreed: "Of course they should not share them."

46. Integration tests require an already-running, already-configured gateway; a test never launches the gateway itself. The tests that launched their own gateway got stuck and failed - "all wrong" - and wiring a model directly into the test harness was duplicated effort when the gateway was needed anyway. A small local model stays runnable without the gateway, so integration tests can exercise real inference with a simple setup.

</core-crate>

<open-questions>

## Open Questions

The record leaves these tensions unresolved. Each is a place where two positions conflict and no final ruling exists.

1. Defaults. "No defaults, everything explicit" sits against "implement all features and let the caller decide, with sensible defaults", and against the pairing of "default configuration enables no tools" with "fundamental tools are built into core". Where defaults are permitted and where they are the enemy was never reconciled.

2. Fanout scope. Three positions survive: fanout restricted to the fanning section's own children, fanout allowed whether or not a section has children, and parallel analysis expressed as plain nested subsections with no fanout mechanism at all.

3. Control-flow surface. The record holds both a single unified control tool with a type discriminator and named jump()/execute() functions; later units appear to supersede earlier ones, but no record states the unified-tool design is abandoned.

4. Shared-chunk mechanics. "The H1 preamble runs exactly once as a live preamble" conflicts with the shared chunk being "compiled once and replayed in each section's fresh VM" under phase gating; two different mechanisms both appear as current.

5. Static tool discovery. Load-time discovery by stub-parsing the prompt's Lua is a landed principle, but the doubt survives that general-purpose Lua computation makes static detection of every tool call unreliable.

6. Empty replies. "An empty model response is never acceptable" versus the conditional empty-turn clean exit; the later rule refines the earlier one, but the exact boundary of which empty turns fail closed deserves confirmation.

7. Weight of the untrusted envelope. Guard-wrapping is adopted and automatic, yet the envelope is a probabilistic mitigation whose hard controls are scoping and context-clearing isolation; how much the design may rely on it is unstated.

</open-questions>

<approach>

## The Approach Behind the Rules

Not everything in these chats converts to a rule, because the rules are the residue of a practice, not the practice itself. The practice is a sensibility: lean means slender call chains and minimal inference rather than small files, and the best feature is the one that delivers everything with the least machinery, because less code to maintain beats bespoke machinery every time. The language is treated as a made object, a work of art whose primitives should feel like one family and whose names come from vocabulary every prompt writer already owns. When a limit appears, the temperament is honest and aggressive at once: a probabilistic guard is admitted to be a mitigation rather than a boundary, minute-scale latency is a defect to attack rather than a fact of life, and unshipped code earns no compatibility concessions because there is no one to break. Evidence sits at the center of every decision: defaults are interrogated against intuition, proposals are floated freely and then left for measurement to kill, quick confident answers are distrusted until the actual mechanism is shown, and a correct generalization is expected to pay for itself by deleting special cases. Underneath it all runs a theory of the medium itself, that every regeneration blurs an artifact toward the mean and no model can sharpen without external information, which is why the first pass is the sharpest and the human conversation remains the substance. The design ultimately rests on a single metaphor held with complete seriousness: the markdown is the program, the model is the CPU, the embedded Lua is the microcode, and the harness is the instruction decoder.

</approach>

*2026-08-19 - Kimi K3*
