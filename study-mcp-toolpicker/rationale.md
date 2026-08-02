# Why the MCP tool-picker is shaped the way it is

This is the reasoning behind `promptforge-mcp-toolpicker`: the decisions, the alternatives
that were tried and rejected, and the evidence that moved each call. It is the companion
to two other documents - `design-mcp-toolpicker.md` (the specification, the "what") and
`mcp-classifier-spike/report/FINDINGS.md` (the empirical log, the "numbers"). Read this one
for the "why."

## The problem

A promptforge prompt is a sectioned markdown document; each section can run Lua that scopes
which tools are available via `tools.add(...)`. We want a prompt to be able to say, in plain
English, what capability it needs, and have the harness bind that need to the right tool from
whatever MCP servers are connected - or refuse cleanly. The question the whole study set out
to answer: can a small, local, deterministic classifier do that reliably, without an LLM in
the resolution path?

## How tools are scoped, and what a "need" actually is

The executor already dispatches tools by name through a `Tool` trait, and Lua `tools.add("x")`
scopes tools per section. Two surfaces sit on top of that:

- `tools.add("name")` - scope an exact, known tool.
- `tools.add_need(alias, description)` - declare a capability in English; the resolver binds
  the alias to a concrete tool at launch.

The single most important realization in the whole study concerns the *register* of that
description. Early evaluation used runtime user utterances ("find a hotel in Columbus Sept
12-15") as the needs. That was wrong. The Lua need string is written by the prompt author,
and an author writes a clean, parameter-free capability line that reads like a tool's own doc
("Retrieve a WG21 paper's markdown given the paper number", "Insert a record into the database
log table"). Authors typically paraphrase the description of a tool they already intend to use.
This changes everything downstream: matching an author-register description to a tool is nearly
trivial for embeddings, because both sides are in the same register. The apparent difficulty we
first measured was an artifact of testing the wrong input distribution.

## Why embeddings, and why not the clever alternatives

We benchmarked every candidate matcher on real tool catalogs. The results were decisive, and
several of them were counter-intuitive enough that they are worth recording as warnings.

- Zero-shot NLI was tried first and looked spectacular on a hand-authored set (0.97 top-1),
  then collapsed to 0.06-0.48 on real, independently-phrased needs. It had been keying on
  shared vocabulary between the need and the description; independent phrasing broke it, and
  bigger/newer NLI checkpoints were no better. Rejected. The lesson: a synthetic eval whose
  queries share words with the targets will flatter any lexical method.
- Sentence embeddings (bi-encoders) were the only method robust across every dataset. bge-small
  and all-MiniLM-L6-v2 came out interchangeable; larger models did not reliably help and
  sometimes hurt on messy catalogs. Small, ~33-133 MB, CPU, deterministic - and best or tied
  everywhere. Chosen.
- BM25 / lexical word-count fusion was tried as a "trivial reject" and as a hybrid. Fusing it
  with embeddings actively hurt (dropped top-1 ~15-18 points): equal-weight fusion lets the far
  weaker lexical ranker pollute the strong one, and lexical cannot bridge synonyms, which is the
  whole problem. Rejected as a matcher; only viable as a minor signal, not a peer.
- Verb/noun structured channels (split need and tool into POS channels, compare separately) were
  tried to fix action mismatches like read vs write. It lowered accuracy at every weight, even on
  near-duplicates - the base embedding already separates those, and POS tagging adds noise.
  Rejected.
- Hard category routing / mixture-of-experts (cluster the catalog, route the need to one cluster,
  pick within) dropped top-1 from 0.84 to ~0.68, because routing was only 0.72-0.80 accurate and
  every misroute discards the gold before any expert runs. Rejected as a hard filter; the soft
  top-k it was trying to replace already does the narrowing without the cliff.
- IDF "most important word" saliency was eyeballed on 30 real needs: it grabs parameters (city
  names, dates) and filler, not the capability word, because the rarest token is usually an
  argument, not the intent. Rejected as-is; the salient term is the action+object head, which
  embeddings already capture.
- Cross-encoder rerankers gave only a modest, domain-dependent lift (and can hurt on messy
  catalogs), so they are optional, not core; a *fine-tuned* reranker is the lever if one is ever
  needed.

## What the hard part actually is

Because author-register matching is easy in the common case, the classifier does not earn its keep
on the happy path. Reconciled on 4,440 real cases, the numbers depend on how close the need is to
the tool's doc: for restatement-style needs (the common case) top-1 is 0.98 among unrelated tools
and 0.75 among the gold's nearest neighbors, with recall@3 0.90 on that hard band; for goal-
abstracted needs it falls to 0.34 hard top-1. Blended across bands, hard top-1 is 0.53 and hard
recall@3 0.74. Two facts follow, and they shape the entire design:

- The right tool is almost always in the top-3 even among close competitors. So the system should
  not try to win top-1 outright; it should surface a shortlist and let a well-informed decider
  settle the near-tie.
- The genuinely hard cases are near-duplicate disambiguation and absence ("no connected tool
  fits"). Duplicates are common in a broad multi-server catalog - about 11% of tools have a
  near-identical twin at cosine >= 0.98, almost all cross-server republishes. So the resolver's
  real job is detecting duplicates and absence and doing something sensible, not the match itself.

This produced the four-outcome resolution policy: clear bind; ambiguous within the author's own
catalog (a configuration error, so fail loud); ambiguous because foreign/overlapping servers were
intentionally imported (surface the shortlist); nothing clears the floor (absence, fail loud). The
gate is a calibrated similarity floor plus a top-1-vs-top-2 margin; MCP `readOnlyHint` /
`destructiveHint` annotations break ties where present but are never required.

## choose_mcp_tool: how a prompt picks a tool at runtime

Alongside static `add_need` binding, an author can opt into dynamic discovery with
`tools.add("choose_mcp_tool")`. The shape of this tool went through several revisions, and the
final form is the simplest:

- First idea: a fresh subcontext runs the retrieval AND an LLM selects the best tool, returning
  one answer plus rationale. Isolates untrusted tool descriptions and keeps the catalog out of the
  main context.
- Then: since the subcontext inference is already paid for, have it select rather than just
  retrieve - the validated cascade (LLM over a top-k shortlist beats LLM over the whole catalog).
- Then the decisive simplification: drop the subcontext for choosing entirely. `choose_mcp_tool`
  becomes a deterministic, LLM-free embedding retriever that returns the top-k (~3) descriptors;
  the harness injects them into the context; and the *main model* picks among them as ordinary
  tool-calling.

The reason the main model should do the choosing is a systems argument, not an accuracy one. The
main context is already governed by the author: model choice, temperature, instructions, and
rewrite opt-out. A subcontext forces a new orphan configuration - which model runs it, at what
budget, from which vendor, with what trace. Doing the pick in the main context reuses all of that,
guarantees the model that selects a tool is the one that will use it (no chooser/executor
capability mismatch), keeps one model and one trace, and holds full task history - which is exactly
the context needed to break a near-duplicate tie that the need string alone cannot. It also happens
to be the established tool-search pattern: retrieve candidates, load them, let the model call one.

`choose_mcp_tool` returns a tool *descriptor* (name, description, input schema), not an invocation,
so the main model calls the tool itself with the task in view. It returns one descriptor when
confident and a small shortlist on a genuine tie (the clean way to hand duplicates to the better-
informed decider), and "no tools available" on absence. The absence return is mandatory because a
model handed only a shortlist over-binds (~23% false-bind measured), so it must see whether anything
cleared the floor.

## The context rewrite, and model tiering

When a dynamic resolution happens, the harness does not simply append the tool result. It rewrites
the context so the chosen descriptor sits before the prompt prose and the entire discovery episode
(the `choose_mcp_tool` call and any pre-call chatter) is removed, then re-generates - as if the model
had been prompted with the tool already available. The payoff is unification: a dynamically discovered
tool lands in the identical execution state as a statically bound one, so the system has a single
execution model and behavior does not diverge by surface. A bonus is that the untrusted candidate
descriptions the retriever surfaced do not persist in the main context; only the chosen descriptor
does. The costs are a second inference pass (true re-generation for a clean state) and prefix-cache
invalidation at the insertion point, both negligible for one-time-at-start discovery.

For genuinely hard selection, this composes with promptforge's context-clearing goto into a model-
tiered pattern: a strong reasoning-model section calls `choose_mcp_tool` and disambiguates, a
context-clearing goto passes the chosen descriptor (plus rationale and the resolved binding) into a
fresh context, and a cheaper model executes. This is the "right" form of a selection subcontext,
because a section already has author-configured model selection - so there is no new orphan config.
Two caveats keep it honest: gate the reasoning step on expected ambiguity (common selection is
trivial and a cheap model picks fine among three, so routing everything through the expensive step
overpays), and remember that a deliberate chooser != executor reintroduces the capability mismatch
(pass usage hints, and reserve tiering for tools whose execution is mechanically simple).

## Two surfaces, one engine

Static `add_need` binding and dynamic `choose_mcp_tool` are complementary, not competing, and both
sit on the same embedding engine. Static is deterministic, LLM-free, and reproducible - for
capabilities known at authoring time. Dynamic is model-driven and adaptive - for when the author
cannot or will not enumerate needs. The context rewrite makes the dynamic path converge onto the
static execution state, so downstream everything is uniform.

## Why the resolver is its own crate

`promptforge-mcp-toolpicker` depends on a separate, thin `promptforge-mcp-client` for protocol
(connect, initialize, `tools/list`, `tools/call`, error mapping) and keeps all the semantics
(embeddings, the four-outcome policy, the Lua verbs, the context rewrite) to itself. Three reasons:

- The embedding model must not ride along with the protocol. Another consumer already exists - the
  CLI acts as an MCP client of the promptforge-mcp server - and it should be able to speak MCP
  without loading an embedding model it never uses.
- Isolation and independent testing: the resolver tests against synthetic catalogs with no network;
  the client tests against a mock server with no model. This is the same reasoning that made
  `webfetch` its own crate.
- Each crate stays context-window-sized, so a coding LLM can hold a whole unit at once and work the
  protocol crate through its interface without loading the resolver, and vice versa. The corollary
  is a design obligation: keep each crate lean with a crisp, documented public API, and do not
  over-fragment (that would trade intra-crate context for inter-crate seam-juggling).

## Deferred, on purpose

- MCP sampling and roots: not implemented; sampling is deprecated upstream and would couple the
  resolver back to the model client. Deferred cleanly by not advertising the capability.
- Fine-tuning (contrastive embedding fine-tune, or a fine-tuned/LoRA reranker): the lever to push
  past ~0.85 on hard disambiguation, expected to reach ~0.88-0.93. Deferred until the zero-shot
  baseline proves insufficient in practice, and to be trained on real (not same-generator) needs
  with hard negatives to avoid the very bias that flattered NLI.
- Calibration: raw cosine is not a probability, so the abstain "budget" is not a guarantee until a
  temperature/isotonic/conformal step is fitted. Deferred but noted as required for a hard budget.

*2026-08-02 - Opus 4.8 (Cursor agent)*
