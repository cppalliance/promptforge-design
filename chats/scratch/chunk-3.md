---
produced: 2026-08-19
title: PromptForge design principles mined from architect-vibe-planning part 2 (vibe methodology, prompt compression)
---

# 2026-07-28-0207-architect-vibe-planning-part2.md

```yaml
- statement: Everything the executor does runs in subagents, in parallel when possible, so the main context and the plan stay potent; attention to recent content degrades as old material fills the context.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60] [p84]
  rejected-alternative: doing work in the main context
  endorsement: n/a

- statement: Every step of an implementation plan ends with working code, real non-trivial tests, and a checkpoint of finished functionality.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: none
  endorsement: n/a

- statement: After every commit the AI reviews its own code, red-teams the tests, removes the technical debt it finds, verifies the tests pass, and amends the commit instead of adding a new one.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: committing first and cleaning up in later commits
  endorsement: n/a

- statement: Before implementing anything, the executor spawns subagents to search the web for current information about what it is about to do, unless it is certain it already knows.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: relying on the model's prior knowledge
  endorsement: n/a

- statement: Plans are refined hierarchically: a high-level ordered plan, then a finer-grained plan per component, decomposed until each step is the smallest unit of functionality that leads to a testable thing.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: none
  endorsement: n/a

- statement: Implementation begins only from a design document whose high-level decisions are already made, so the model's only job is to implement.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: letting the model make high-level decisions during implementation
  endorsement: n/a

- statement: Design decisions the AI makes during implementation are recorded in a per-crate design.md, with a top-level design document holding the cross-package decisions.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: none
  endorsement: n/a

- statement: Comments appear only where something is surprising or non-standard; code is never annotated with restatements of the obvious.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: narrating code line by line
  endorsement: n/a

- statement: Code hygiene rules are language-independent, general principles (DRY, single responsibility) expressed as unambiguous tests that can be applied to AI-written code.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p60]
  rejected-alternative: language-specific style rules
  endorsement: n/a

- statement: A compressor must never expand its input; when it cannot find a shortening, it emits the input verbatim.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p62] [p82]
  rejected-alternative: none
  endorsement: n/a

- statement: Compression is idempotent: a second compression pass over the output changes nothing.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p71] [p82]
  rejected-alternative: none
  endorsement: n/a

- statement: Compression must be smart generative rewriting, not the deletion of tokens.
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p81]
  rejected-alternative: LLMLingua-style subtractive token dropping
  endorsement: n/a

- statement: The compressor is single-purpose: it compresses and does nothing else, with no tool calls and no thinking.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p70]
  rejected-alternative: a general-purpose model that also compresses
  endorsement: n/a

- statement: Generated prose must not contain formulaic AI rhetorical tics such as "This is not merely an observation" or "deserves emphasis rather than apology".
  scope: global
  source: user-corrective
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p99] [p108] [p110]
  rejected-alternative: a length pass that leaves the rhetorical patterns in place
  endorsement: n/a

- statement: Every sentence in a written artifact must justify its presence; anything not needed is cut.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p113]
  rejected-alternative: none
  endorsement: n/a

- statement: During plan implementation the plan file itself is never edited.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p103] [p105]
  rejected-alternative: none
  endorsement: n/a

- statement: Plan execution runs until every to-do is complete, without stopping partway.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p104] [p106]
  rejected-alternative: none
  endorsement: n/a

- statement: The plan file is preserved and evolved across the session and kept compressed so it stays potent.
  scope: global
  source: user-stated
  citation: 2026-07-28-0207-architect-vibe-planning-part2.md [p95]
  rejected-alternative: none
  endorsement: n/a
```

## Not converted

- Compression is the most valuable substance in the AI universe; the antislab. [p67]
- Start from the most compressed version of the idea, the highest-frequency signals; the chat itself is the substance and the human supplies the decision-making. [p68]
- Distrust quick confident answers; demand to see the actual mechanism, not a simulation of one. [p85]
- A report should open experientially and take the reader on the same journey the author took. [p94]
- An illustrative example may be approximate if it is close enough to reality to teach the reader. [p98]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from compaction-algorithm session part 4 (goto args, Lua return, fork rendezvous, context prefix inheritance, sys constants)
---

# 2026-07-30-1046-compaction-algorithm-large-part4

```yaml
- statement: goto resolves its argument string at the call site and injects it directly into the new context, acting as a minimal argument list for section transfer.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p229], [p231]
  rejected-alternative: a formal parameter-declaration mechanism for sections
  endorsement: n/a

- statement: A goto transfer is permanent; because control always lands in the same target, a goto expression cannot serve as a reusable subroutine called from multiple sites.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p242]
  rejected-alternative: treating goto-with-return as a reusable function callable from many places
  endorsement: n/a

- statement: Lua chunks return values to the engine through Lua's native return statement, not through any added identifier or descriptor convention.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p235]
  rejected-alternative: returning values via a declared identifier
  endorsement: n/a

- statement: A rendezvous section that is data-dependent on multiple fork arms waits until every arm it depends on has completed before it executes.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p247]
  rejected-alternative: none
  endorsement: n/a

- statement: A tool takes args as one string; the prompt's own first step deduces the individual values from that string rather than requiring the caller to supply pre-structured fields.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p251]
  rejected-alternative: structured args fields (args.name, args.mission) that push inference onto the caller
  endorsement: n/a

- statement: Propagating state is a single tool call carrying all values at once, not one tool call per value.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p228], [p265]
  rejected-alternative: one set call per value, requiring multiple tool calls to move state
  endorsement: n/a

- statement: Every heading's context is structured as prefix, body, and suffix: the prefix is inherited cumulatively by child headings, the body is throwaway, and the suffix floats.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p269], [p270], [p271]
  rejected-alternative: none
  endorsement: n/a

- statement: On a tool call within a multi-turn context, the engine removes the injected facts block from the transcript, injects the tool results, then adds the facts block back.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p257]
  rejected-alternative: none
  endorsement: n/a

- statement: Contexts must not accumulate permanent entries across turns.
  scope: core
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p288]
  rejected-alternative: accumulating persistent context entries turn over turn
  endorsement: n/a

- statement: The engine exposes substitution constants such as sys.when (the time the prompt launched), sys.now (the current time), and a unique id per context starting from 1.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p284], [p285], [p286]
  rejected-alternative: none
  endorsement: n/a

- statement: The Lua declares which dynamic values a model needs and the engine supplies them automatically; the model does not pull them by request.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p290]
  rejected-alternative: model-initiated requests for dynamic values such as the current time
  endorsement: n/a

- statement: The tool surface is restricted per section; the engine does not inject every tool declared in the front matter into every context.
  scope: core
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p328], [p329]
  rejected-alternative: defaulting each context to all declared tools
  endorsement: n/a

- statement: The master plan tracks only unbuilt design; for anything already implemented, the Rust code itself is the design reference.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p280]
  rejected-alternative: keeping implemented design described in the plan alongside unbuilt work
  endorsement: n/a

- statement: A design document records decisions and rationale only; as the plan implements, the corresponding Rust types and code are removed from the document so what remains is the why.
  scope: global
  source: user-stated
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p310]
  rejected-alternative: design documents that carry Rust types and declarations
  endorsement: n/a

- statement: Running a plan generates the design document after implementation completes, so the document is always in sync with the built code.
  scope: global
  source: user-corrective
  citation: 2026-07-30-1046-compaction-algorithm-large-part4.md [p318], [p319]
  rejected-alternative: generating the design document before or separately from the implementation
  endorsement: n/a
```

## Not converted

- "The best engineers are lazy" - the best feature gives everything for the minimal implementation (p231).
- design-promptforge.md is overengineered bloatslop; mine it for ideas only (p232, p233).
- Build in the smallest testable increments: Lua plus args plus substitution first, "echo" as the first commit, fall-through as one testable thing (p250, p276, p293).
- Args without Lua is too little; Lua is needed to return values (p277, p278).
- Prefix caching is irrelevant at 3B; a 3B model has a tiny context window (p258, p259).
- The consolidated single tool call existed because small-model sections were assumed to need many call kinds at once; large models may not need it (p224, p225).
- Each commit must have tests, code review, docs, and user docs, and each commit must make self-sufficient progress rather than needing a later commit to retroactively realize it (p292, p312).
- Wants a lightweight vibe-coding how-to, roughly one fifth of how-to-vibe-code, injected into context periodically (p297-p302); loading how-to-write-prompts.md into plans "works like a miracle" (p299).
- Implement all features and let the caller decide, with sensible defaults (p316).

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from MCP client and agentic harness session (tool needs, choose_mcp_tool, context rewrite, resolver crate)
---

# 2026-08-02-1034-mcp-client-harness

```yaml
- statement: A prompt declares its tool needs at load time as a list of local aliases, each paired with a plain-language description of the capability it needs, and the harness binds each alias to the best-matching available tool.
  scope: core
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p39]
  rejected-alternative: none
  endorsement: n/a

- statement: The Lua API offers both a way to add every tool the MCP client offers and a way to ask for a tool matching a description.
  scope: core
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p11]
  rejected-alternative: none
  endorsement: n/a

- statement: Need strings are written in the prompt author's register as clean, parameter-free capability descriptions that read like a tool's own documentation, not as runtime user utterances; authors typically paraphrase the description of the tool they already intend to use.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p58], [p60]
  rejected-alternative: using runtime user utterances as the need-string distribution
  endorsement: n/a

- statement: Tool resolution runs locally with no LLM in the resolution machinery.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p27]
  rejected-alternative: an LLM-based matcher in the resolution path
  endorsement: n/a

- statement: Static launch-time binding (add_need) and dynamic runtime discovery (choose_mcp_tool) are complementary surfaces that share one resolution engine; neither replaces the other.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: Dynamic tool discovery is an opt-in surface the prompt author selects explicitly; it is the only path when chosen, not an escalation path the engine falls into on its own.
  scope: mcp
  source: user-corrective
  citation: 2026-08-02-1034-mcp-client-harness.md [p63], [p64]
  rejected-alternative: dynamic selection as an escalation path entered automatically
  endorsement: n/a

- statement: Dynamic tool selection returns a tool descriptor (name, description, input schema), never an invocation: one descriptor on a clear win, a shortlist on a genuine tie, and a "no tools available" error on absence.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p66]
  rejected-alternative: none
  endorsement: n/a

- statement: On dynamic resolution the harness rewrites the context so the chosen tool descriptor sits before the prompt prose and the discovery exchange is excised, then re-generates; a dynamically discovered tool lands in the identical execution state as a statically bound one.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p67]
  rejected-alternative: appending the discovery results to the context
  endorsement: n/a

- statement: Selection among a returned shortlist happens in the main context, which the author already governs (model choice, rewrite opt-out, instructions), rather than in a separate subcontext that would need its own model and configuration answers.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p70], [p71]
  rejected-alternative: a dedicated selection subcontext with its own model configuration
  endorsement: n/a

- statement: A prompt can use a strong reasoning model to select a tool, then a context-clearing goto to pass the tool descriptor into a fresh context where a cheaper model executes.
  scope: core
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p72]
  rejected-alternative: none
  endorsement: n/a

- statement: Duplicate tools within the author's own catalog are a configuration error and fail loud; duplicates arising from intentionally imported foreign servers must have an explicit disambiguation path.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p61]
  rejected-alternative: silently picking one of the duplicates
  endorsement: n/a

- statement: Absence of a matching tool fails loud; abstention is a first-class resolution outcome, not an afterthought.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p61], [p66]
  rejected-alternative: binding to the nearest tool regardless of confidence
  endorsement: n/a

- statement: Tool annotations (such as readOnlyHint or destructiveHint) may improve resolution confidence or break ties, but resolution must work without them; they are never required.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p56]
  rejected-alternative: depending on annotations as a necessary input
  endorsement: n/a

- statement: Tool identity is the (server, tool) pair; routing keys on the pair, not on a concatenated name string.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p13]
  rejected-alternative: routing on a concatenated server-plus-tool name string
  endorsement: n/a

- statement: Crates are kept small enough that a coding LLM can hold an entire crate in a single context window.
  scope: global
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p79]
  rejected-alternative: none
  endorsement: n/a

- statement: The tool resolver lives in its own crate, separate from the MCP protocol client, so protocol-only consumers (such as the CLI) do not carry the matching model.
  scope: mcp
  source: user-stated
  citation: 2026-08-02-1034-mcp-client-harness.md [p78], [p79]
  rejected-alternative: embedding the resolver in the MCP client crate
  endorsement: n/a

- statement: Resolution is gated on a similarity floor plus a top-1-vs-top-2 margin, yielding four outcomes: clear bind, own-catalog ambiguity (fail loud), foreign-server ambiguity (surface a shortlist), and absence (fail loud).
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1034-mcp-client-harness.md [design-mcp-toolpicker.md section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Because the right tool is almost always in the top few candidates, resolution surfaces a shortlist for a well-informed decider to settle near-ties rather than forcing a single top-1 answer.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-02-1034-mcp-client-harness.md [rationale.md section], [p25], [p26], [p69]
  rejected-alternative: forcing a single top-1 binding in all cases
  endorsement: affirmed
```

## Not converted

- Skepticism about hardening when the operator controls all MCP servers: "why do I care about all of this hardening if I control all the mcp servers?" [p14]
- Preference for partial fine-tuning that buys a bounded improvement without degeneracy, rather than going "all the way" [p22]
- Eval data should be generated by multiple models (ChatGPT, Claude, Gemini, Cursor) to avoid same-generator bias [p51]
- Working style: run all jobs asynchronously so the conversation can continue [p23], [p46]
- Inspect raw data samples together before committing to a theory ("pick 30 descriptions at random... let's look at it together") [p57]
- Plans should ship with a separate rationale document that mines the chat history and explains the why behind the design [p82]
- A fast, high-confidence "trivial reject" stage may drop clearly mismatched tools before finer matching, tolerating false negatives but never false positives [p55]

---

---
produced: 2026-08-19
title: PromptForge design principles mined from modify-the-store (store input files, MCP gateway file mapping, sandboxed file IO)
---

# 2026-08-15-1851-modify-the-store

```yaml
- statement: The executor receives a store instance as a parameter; the store is not part of the prompt.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p2]
  rejected-alternative: none
  endorsement: n/a

- statement: File-in/file-out prompt execution runs against an in-memory store so a run performs no disk IO.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p1]
  rejected-alternative: reading and writing real disk files during the run
  endorsement: n/a

- statement: A prompt is agnostic to how its inputs arrive; the executor exposes only a store, and the gateway translates between the calling environment and the executor.
  scope: boundary: mcp<->core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p12]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway owns the store lifecycle: it seeds inputs, hands control to the prompt, then regains control and decides the disposition of outputs.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p4]
  rejected-alternative: none
  endorsement: n/a

- statement: The gateway reads caller-specified input files into the store itself; file contents never pass through the orchestrating model's tokens.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p6]
  rejected-alternative: the orchestrator inlining existing file contents into the tool call
  endorsement: n/a

- statement: A caller supplies each input as either a file path or inline text; the gateway normalizes both into the store and the prompt never knows which.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p14]
  rejected-alternative: none
  endorsement: n/a

- statement: Supplying both an input file and input text for one input is a validation error at the gateway.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p23]
  rejected-alternative: silently accepting both
  endorsement: n/a

- statement: Output files are written to real filesystem paths chosen by the caller; permissions and authorization are the orchestrator's responsibility, not the gateway's.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p5]
  rejected-alternative: the gateway managing output permissions itself
  endorsement: n/a

- statement: The gateway has the option to inline an output file in its response instead of writing it to disk.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p21]
  rejected-alternative: none
  endorsement: n/a

- statement: The MCP server maps caller inputs to the store deterministically, without using inference.
  scope: mcp
  source: user-corrective
  citation: 2026-08-15-1851-modify-the-store.md [p18]
  rejected-alternative: an inference-based mapping of caller inputs to store entries
  endorsement: n/a

- statement: MCP tool schemas are kept as small as possible so smaller models can fill them in correctly.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p13]
  rejected-alternative: none
  endorsement: n/a

- statement: Textual args remain separate from file inputs so a caller can attach additional commands alongside a file input.
  scope: core
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p19]
  rejected-alternative: merging file inputs into args
  endorsement: n/a

- statement: Prompts declare expected input and output files in frontmatter as store-relative paths, with descriptions used for documentation and MCP schema generation.
  scope: core
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: When a prompt declares input files, the server validates that every declared input has a supplied value, rejects the call if any are missing, and seeds the store before execution.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Output extraction is best-effort: a declared output the prompt never wrote is returned as absent rather than failing the run.
  scope: mcp
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [plans section]
  rejected-alternative: failing the run when a declared output is missing
  endorsement: affirmed

- statement: Default configuration enables no tools; every tool is opt-in so the sandbox is real.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p47]
  rejected-alternative: registering WebFetch and WebSearch by default
  endorsement: n/a

- statement: The gateway is started first; the MCP server and the dev runner both call through it.
  scope: global
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p38]
  rejected-alternative: none
  endorsement: n/a

- statement: Local MCP prompts live in a gitignored directory; dropping a prompt file into it makes the prompt live.
  scope: mcp
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p40]
  rejected-alternative: none
  endorsement: n/a

- statement: A prompt containing only Lua, with no prose outside code fences, runs without a gateway.
  scope: core
  source: ai-proposed
  citation: 2026-08-15-1851-modify-the-store.md [design docs section]
  rejected-alternative: none
  endorsement: unaddressed

- statement: LLM-facing quickref documentation is compressed to minimal tokens, and references other repo files rather than restating their contents.
  scope: global
  source: user-stated
  citation: 2026-08-15-1851-modify-the-store.md [p36]
  rejected-alternative: duplicating YAML format and prompt structure documentation inside the quickref
  endorsement: n/a
```

## Not converted

- [p13] Hesitation about gateway-side URL fetching: if the model might do the fetching itself, gateway fetching becomes ambiguous. Unresolved preference, no directive landed.
- [p19] Open question whether the common one-file-in/one-file-out case deserves its own special syntax. Floated, never decided.
- [p27] Documentation workflow preference: integrate new design into the existing per-crate design docs instead of generating a new document. Process directive, not engine behavior.
- [p34] Rule-authoring philosophy: loosen a workspace rule with an "unless" clause and tighten rulebooks into standalone imperatives. About rule governance, not PromptForge.
- [p56] Temperament about verified work: every commit must have tests that were actually run, confirmed commit by commit. Process demand, not a design principle.
- [p58] Session-reuse goal for the quickref: services launched once should be remembered and reused across repeated prompt runs in the same chat. A doc purpose statement, not a directive on the engine.

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core large session part 2 (prompts p79-p155)
---

# Design principle candidates: 2026-08-09-1058-promptforge-core-large-part2.md

```yaml
- statement: A failed tool.need fails the prompt immediately with an error.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p95]
  rejected-alternative: continuing prompt execution after a failed tool.need
  endorsement: n/a

- statement: Misusing an API function produces a warning rather than silent wrong behavior.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p86]
  rejected-alternative: silently accepting the wrong function with no warning
  endorsement: n/a

- statement: Prompt code fences carry the bare lua tag with no extra annotation word.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p87]
  rejected-alternative: a "lua prompt" fence tag
  endorsement: n/a

- statement: There is exactly one tools.add entry point for adding tools.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p90]
  rejected-alternative: multiple tools.add variants
  endorsement: n/a

- statement: Whether model thinking is on or off is controlled by the prompt, not by the gateway.
  scope: boundary: core<->gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p107]
  rejected-alternative: gateway-level thinking control
  endorsement: n/a

- statement: Prompt configuration is written as Lua calls in the prompt body, never in frontmatter.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p108], [p154]
  rejected-alternative: frontmatter configuration
  endorsement: n/a

- statement: Models are declared in the introduction via models.add with per-model parameters such as thinking and context, and a section selects its model with model(name).
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p109]-[p112]
  rejected-alternative: frontmatter model declarations
  endorsement: n/a

- statement: A subsection inherits its parent section's model unless it specifies its own.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p142]
  rejected-alternative: non-inheriting model resolution
  endorsement: n/a

- statement: Analytical pipelines run at temperature zero.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p105]
  rejected-alternative: nonzero temperature for analytical work
  endorsement: n/a

- statement: An empty model response is always a hard failure.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p124]
  rejected-alternative: treating an empty response as acceptable or recoverable
  endorsement: n/a

- statement: A tool call counts as a model response.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p126]
  rejected-alternative: treating a tool-call-only turn as an empty response
  endorsement: n/a

- statement: Provider and model quirks are normalized behind one lean layer so the rest of the system can speak universally.
  scope: gateway
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p122]
  rejected-alternative: scattering per-provider special cases across the codebase
  endorsement: n/a

- statement: Each run starts with a fresh trace; preserving a trace across runs is the developer's own job.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p128]
  rejected-alternative: appending to the previous run's trace
  endorsement: n/a

- statement: Model binding is looser than tool binding and resolves through the same picker mechanism as tools.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p133]
  rejected-alternative: strict model binding on a path separate from the tool picker
  endorsement: n/a

- statement: Recoverable web_fetch failures soft-return instead of hard-failing.
  scope: core
  source: user-stated
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p146]
  rejected-alternative: hard-failing the prompt on a recoverable fetch error
  endorsement: n/a

- statement: Missing gateway credentials produce a clear diagnostic at bind time, not an opaque tool-bind failure.
  scope: gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p99]
  rejected-alternative: an unexplained tool-bind failure when the token is missing
  endorsement: n/a

- statement: Runs are observable: logs expose what the engine wrote into each produced artifact.
  scope: core
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p97], [p105]
  rejected-alternative: logs that omit what went into run artifacts
  endorsement: n/a

- statement: Models are reached through the gateway rather than through bespoke direct wiring in the test harness.
  scope: boundary: core<->gateway
  source: user-corrective
  citation: 2026-08-09-1058-promptforge-core-large-part2.md [p140]
  rejected-alternative: wiring a local model directly into core-tests, bypassing the gateway
  endorsement: n/a
```

## Not converted

- Minute-scale per-prompt latency is treated as a defect worth attacking, not a fact of life [p81], [p91].
- Heavyweight process rulebooks get lightened when they slow the development loop [p116].
- Review loops stop after one round of amend; more rounds only surface noise [p117].
- Architecture should be lean and slender; scope creep that later proves necessary is accepted by definition, because that is what normalizing means [p122], [p124].
- Abstraction risks such as trait cosplay are discounted when removal is trivially easy [p124].
- Defaults are interrogated against intuition before acceptance, as with the skepticism that turning off thinking could help analysis [p106].

---

---
produced: 2026-08-19
title: PromptForge design principles mined from promptforge-core largest session part 4 (p327-p375)
---

# 2026-08-14-1613-promptforge-core-largest-part4.md

```yaml
- statement: The store exposes real files and virtual (memory) files at the same time; both are available concurrently, not as mutually exclusive modes.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p367]
  rejected-alternative: a store model that supports only one kind of file at a time
  endorsement: n/a

- statement: Sandboxing applies to the prompt-facing tool surface, not to the Lua API; Lua code can read and write both real files and memory files.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p368]
  rejected-alternative: sandboxing Lua so it cannot write files
  endorsement: n/a

- statement: Tool injection is scoped per section; when tools are injected into an H2 section, the set of files that section may access is injected with them.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p368]
  rejected-alternative: none
  endorsement: n/a

- statement: No parallel mechanisms; a single, small, well-designed set of primitives services all needs, and an existing mechanism such as tool scoping is leaned on as far as it can go before anything new is added.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p371]
  rejected-alternative: adding a new mechanism alongside an existing one that already covers the need
  endorsement: n/a

- statement: Tool availability can be conditioned on turn number within a section, so a prompt can lock the model to one tool on the first turn and widen the set on later turns.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p372]
  rejected-alternative: a static tool set that is identical on every turn
  endorsement: n/a

- statement: A Lua function can be exposed as a tool, acting as a front end to an existing tool, so new tool behavior is added inline without writing a Rust function.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p373]
  rejected-alternative: requiring a Rust function for every new tool
  endorsement: n/a

- statement: A tool front end can grant further capability when invoked, for example a Lua search tool that performs a tools.add for fetch when called.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p373]
  rejected-alternative: none
  endorsement: n/a

- statement: Tools support multi-turn interaction, because tools that do coding work such as refactoring a source file need sustained access across turns.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p370]
  rejected-alternative: single-turn tool calls only
  endorsement: n/a

- statement: Explicit user opt-in legitimizes otherwise restricted behavior; consent is the gate for powerful capabilities.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part4.md [p374]
  rejected-alternative: restricting the behavior outright regardless of user consent
  endorsement: n/a
```

## Not converted

- Empirical tuning temperament: A/B test model features (thinking on/off) and adjust parameters until no axis shows further improvement. [p346]
- Autonomous execution working style: run the plan without stopping until no reliable progress remains, keeping code clean with a review every three commits. [p348]
- Deliberation before action: discuss a plan from all angles with pros and cons before editing it. [p369]
- Cost-of-change as a decision input: before adopting a design, ask how much churn it would cause in the source. [p374]

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from promptforge-core largest session part 5 (first-class tools/models, section lifecycle, lua shared, H1-once, file-backed store)
---

# 2026-08-14-1613-promptforge-core-largest-part5

```yaml
- statement: An analytical pipeline persists intermediate outputs as files so that any step can be re-run during development and debugging.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p377]
  rejected-alternative: none
  endorsement: n/a

- statement: The overlay store is integrated into the core engine, not packaged as a separately loadable tool, because it affects the Lua mount.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p380]
  rejected-alternative: overlay as a tool loaded separately from core
  endorsement: n/a

- statement: Prompts are written agnostic of the tool backend; the prompt says "search", never "search the web", and the tool's name and description are established by tool.need and can be rewritten when the tool is injected.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p383], [p386]
  rejected-alternative: hardcoding the backend into prompt text and tool descriptions
  endorsement: n/a

- statement: Behavioral variation of a prompt comes from ahead-of-time configuration; the orchestrating model cannot reshape the Lua at runtime the way an agentic host reshapes instructions.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p392]
  rejected-alternative: runtime reinterpretation of the pipeline by the model
  endorsement: n/a

- statement: Terminology is fixed and enforced repo-wide: the preamble is the H1 code, while prologue and epilogue belong to sections.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p393], [p395]
  rejected-alternative: none
  endorsement: n/a

- statement: Tool and Model are first-class Lua objects (tables) that can be inspected and invoked, which also makes them mockable in unit tests; the preamble can declare globals such as lists of tools usable in any section.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p398], [p400], [p401]
  rejected-alternative: none
  endorsement: n/a

- statement: The toolset is not sealed at the first inference; tools.add between inference rounds within a section must keep working.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p409]
  rejected-alternative: sealing the toolset when infer begins
  endorsement: n/a

- statement: Prose lives in markdown sections where it can be richly formatted, never as string literals embedded in Lua code.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p427]
  rejected-alternative: passing prose as strings to model:infer()
  endorsement: n/a

- statement: A section is a sequence of alternating lua and prose blocks; non-final prose blocks are single-shot and always fall through, the final prose block runs the full tool loop until a reply with no tool call, and one conversation grows across all blocks of a section and is cleared between sections.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p479]-[p487]
  rejected-alternative: none
  endorsement: affirmed

- statement: Sections are subroutines: execute("## Name") runs a section in a fresh VM and returns its reply, while jump("## Name") transfers control with a context-clearing, no-return goto; the default remains running sections in order.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p430], [p431], [p488], [p489]
  rejected-alternative: none
  endorsement: n/a

- statement: The control-transfer function is named jump() because goto is reserved in Lua, and the rename is swept across the entire repo as the first step of the work.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p442], [p481]
  rejected-alternative: exposing sections through _G, or keeping the name goto()
  endorsement: n/a

- statement: The H1 preamble runs exactly once as a live preamble; per-section replay is abandoned because replay multiplies inference cost and corrupts state once the preamble can infer or write to the store.
  scope: core
  source: user-corrective
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p446], [p470]
  rejected-alternative: two-phase preamble treatment and shared-bytecode re-execution in section VMs
  endorsement: n/a

- statement: A single "```lua shared" chunk per prompt is parsed into bytecode but not executed during the preamble; a second one, or one appearing after the H1 ends, is an error.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p461], [p462], [p474]
  rejected-alternative: generic VM serialization and cloning to share functions
  endorsement: n/a

- statement: Every commit that changes the prompting language also updates the user guide in the same commit, adding or deleting sections so the guide is correct for each commit.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p478]
  rejected-alternative: none
  endorsement: n/a

- statement: A name is a design decision and must say how the mechanism works, so there is no confusion.
  scope: global
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p473]
  rejected-alternative: none
  endorsement: n/a

- statement: The store is a virtual filesystem for file-shaped intermediate values in analytical pipelines; it is strictly for debugging and resume, not a general-purpose filesystem for agentic coding, which is a different class entirely.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p504], [p505]
  rejected-alternative: a general-purpose filesystem supporting string replacement and delta application
  endorsement: n/a

- statement: The engine has no defaults and no self-chosen behavior; the caller provides every path explicitly, because the whole system is designed to make things explicit.
  scope: core
  source: user-stated
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [p506]
  rejected-alternative: engine-provided default paths
  endorsement: n/a

- statement: All Lua is compiled at parse time so a successfully parsed Prompt is fully syntax-validated; there is one VM per whole section; the store is the only intentional mutable channel across sections, with functions, closures, globals, var, tools, and reply branch-local by construction; mutable run-global Lua is explicitly excluded.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: section-lua-lifecycle]
  rejected-alternative: none
  endorsement: corrected

- statement: Wire quirks (field synonyms, empty content, null-content tool calls) enter through one normalizer door so hosts stay dumb; a final turn with no tool calls and empty content is a hard error even when reasoning is present; reasoning_content is never promoted into the answer.
  scope: core
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: completion normalize layer]
  rejected-alternative: adopting an external crate (genai, rig) instead of an in-core seam
  endorsement: unaddressed

- statement: Fanout fires all arms at once with the gateway queue as the throttle; replies stay ordered by arm index; fail-fast aborts sibling arms and propagates the first error; the store stays shared and mutex-safe, so authors must not assume arm N sees arm N-1 writes.
  scope: boundary: core<->gateway
  source: ai-proposed
  citation: 2026-08-14-1613-promptforge-core-largest-part5.md [plans section: Fanout and gateway concurrency]
  rejected-alternative: none
  endorsement: unaddressed
```

## Not converted

- [p384], [p388] Open question on tool-naming training bias (snake_case vs single word vs WebSearch); no directive reached.
- [p401] Temperament: "you always encapsulate, you always model" as general programming hygiene.
- [p412] Observation that the only point of the phase transition is to protect the epilog; analytical, not a directive.
- [p448]-[p451] Exploration of generic VM serialization and cloning (with an ID-table scheme for Rust userdata); abandoned in favor of "lua shared".
- [p500], [p501] Housekeeping preference: trim loose design/status files that create noise.
- [p508] Feature spec for a promptforge-dev option to create a same-named directory next to a tool; implementation detail, not a behavior principle.

---

---
produced: 2026-08-19
title: PromptForge design-principle candidates mined from repo review continued session (fresh contexts, findings-driven API redesign, independent source audit, fix-forward retry, de-inlined rulebooks, lean prompts)
---

# 2026-08-11-1510-repo-review-continued

```yaml
- statement: Each unit of work in a pipeline runs in a fresh agent context; no context is reused across files or stages.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p1], [plans section]
  rejected-alternative: carrying one rolling context through the whole pipeline
  endorsement: n/a

- statement: Review and modification are separate phases: all findings for a crate are gathered before any file is modified, and the complete findings set is what drives the changes.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p1]
  rejected-alternative: interleaving review and fixes file by file
  endorsement: n/a

- statement: A redesign is derived from the complete findings set: each API change must both reduce the chance of a finding recurring and make the surface smaller and more robust; change for change's sake is rejected.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p1], [plans section]
  rejected-alternative: fixing findings one by one in place without rethinking the API
  endorsement: n/a

- statement: Subagent returns are capped: the main context receives only completion status, a short summary, and the artifact path; raw source and full findings stay out of the main context.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: none
  endorsement: affirmed

- statement: Stages that consume a previous stage's output run serially; only independent per-unit work runs in parallel.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: parallelizing stages that depend on each other's artifacts
  endorsement: affirmed

- statement: Every finding receives an explicit disposition: fixed, or rejected with specific contrary evidence.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: letting findings drop silently
  endorsement: affirmed

- statement: Completion is judged by an independent fresh-context audit of the actual source, not by the worker's self-report and not by gates alone; compile, lint, and test gates do not catch behavioral or design findings.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p24], [plans section], [design documents section]
  rejected-alternative: trusting the fix agent's own all-green report
  endorsement: affirmed

- statement: On verification failure, fix forward: the verifier's concrete file:line NOT-FIXED list goes back into a fixer on the same candidate, and discard-and-restart happens only when progress stalls or the round budget is spent.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p54], [plans section]
  rejected-alternative: discarding a mostly-correct candidate and restarting blind from the original head
  endorsement: affirmed

- statement: The intended public API is machine-checked against the actual public API; drift between them fails verification.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [p31], [p32], [plans section]
  rejected-alternative: hand-maintained API inventories
  endorsement: affirmed

- statement: A prompt whose subagents share its run and filesystem references shared rulebooks by path instead of inlining them; inlining shared rules into each prompt is the anti-pattern, and only artifacts read by a non-sharing reader inline their rules.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p53], [plans section]
  rejected-alternative: inlining rulebook blocks into the tool prompt
  endorsement: n/a

- statement: A prompt artifact that has grown to thousands of lines is defective and gets compressed: tighten every instruction, one instruction per line, delete hedges, quantify every quantity.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p52], [p53], [plans section]
  rejected-alternative: accepting bulk as the natural cost of completeness
  endorsement: n/a

- statement: When a design changes, the new design is written as one fresh document, the residue goes into a separate document, and the superseded documents are deleted.
  scope: global
  source: user-stated
  citation: 2026-08-11-1510-repo-review-continued.md [p6]
  rejected-alternative: accumulating overlapping design documents
  endorsement: n/a

- statement: An artifact shaped by a style rulebook never cites that rulebook.
  scope: global
  source: ai-proposed
  citation: 2026-08-11-1510-repo-review-continued.md [plans section]
  rejected-alternative: none
  endorsement: affirmed
```

## Not converted

- Trust the frontier model's competence instead of enumerating hygiene basics: "I dont have to tell you what those are I hope, you are a frontier model." [p1]
- The quality bar for the result: code getting smaller, clearer, bounded API surface, crisp, understandable, without the smell of AI slop smearing and bloating everything. [p39], [p44]
- Vibe-coding for days without interim technical-debt refactors is why so many findings accumulated. [p30]
- Much time is wasted because correction subagents keep making mistakes. [p40]
- Autonomous-execution preference: run the plan without stopping for confirmation; on failure roll back and redo, so the user returns to a clean result. [p20]
- Reset, do not revert; force-pushing is fine on a solo repo. (Git mechanics, a technology choice.) [p15], [p19], [p20]
- wip commits pushed to the remote are a cheap backup; keep them. [p26], [p27]
- Use cargo public-api as the ground truth for the workflow. (Excluded as a technology choice; the technology-agnostic form was converted above.) [p31], [p32]
- The improvised review process was preferred over the pre-written refactor-rust tool: faster and more grounded in reality. [p49], [p50], [p51]
