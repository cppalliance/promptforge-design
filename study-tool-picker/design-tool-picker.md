# Building the promptforge-tool-picker crate

Building this crate gives a promptforge prompt two ways to obtain an MCP tool for a capability
described in plain English: a static, launch-time binding declared in Lua, and a dynamic,
runtime discovery tool the model can call. Both are backed by one local, deterministic
sentence-embedding engine over the connected servers' tool catalog, and both resolve through a
single four-outcome policy (bind / duplicate / foreign-ambiguous / absent). The crate holds the
resolution semantics and the Lua-facing API; it depends on a separate thin `promptforge-mcp-client`
for protocol.

## Executive summary

A prompt author declares needs as capability descriptions - `tools.add_need("db", "run a read-only
SQL query against the log database")` - and at launch the crate embeds every connected tool's
text, matches each need by cosine similarity, and binds the alias to a concrete tool when one wins
clearly, or fails loud when the match is ambiguous within the author's own catalog or absent. For
capabilities not known at authoring time, the author opts into `tools.add("choose_mcp_tool")`; at
runtime the model calls `choose_mcp_tool(need)`, a deterministic top-k retriever returns candidate
descriptors, the harness rewrites the context so the chosen tool appears as if it were available
from the start, and the main model calls it. Matching in the author register is easy when the
need restates the tool's doc (top-1 0.98 among unrelated tools, 0.75 among near-neighbors) and
degrades as the need abstracts toward a goal; either way the right tool is in the top-3 about
0.90 of the time on the realistic band, which is why the design surfaces a shortlist rather than
forcing a single guess. The engine's real work is duplicate and absence detection, not the match. The matcher is a small model
(bge-small-en-v1.5 or all-MiniLM-L6-v2, ~33-133 MB, CPU, deterministic); no LLM runs in the crate's
own machinery.

## Key design choices

1. Local sentence embeddings are the matcher, not zero-shot NLI or lexical methods. Embeddings were
   the only approach robust across every real dataset; NLI looked strong on synthetic data and
   collapsed on real needs, and lexical fusion degraded the strong ranker. Tension: embeddings need
   a bundled model file, but it is small and deterministic.
2. bge-small-en-v1.5 and all-MiniLM-L6-v2 are interchangeable; the crate treats the model as
   configurable and defaults to bge-small. Larger models did not reliably help. Reversing this later
   is a config change, not a code change.
3. Needs are author-register capability descriptions, not user utterances. This is what a Lua author
   writes, and it makes matching near-trivial. The contract for `add_need`'s description field is "a
   clean, parameter-free statement of what the tool does."
4. The real job is duplicate and absence detection, not the happy-path match. The engine is built
   around a four-outcome decision, and the abstain path (fail loud) is first-class, not an afterthought.
5. Resolution is a similarity floor plus a top-1-vs-top-2 margin. A clear winner binds; a thin margin
   means ambiguity; nothing above the floor means absence. Raw cosine is not a probability, so a
   calibration step is required before the floor can be a guaranteed error budget (deferred).
6. Duplicates within the author's own catalog are treated as configuration errors and fail loud;
   duplicates arising from intentionally imported foreign/overlapping servers surface a shortlist for
   disambiguation. MCP `readOnlyHint`/`destructiveHint`/`idempotentHint` annotations break ties where
   present but are never required.
7. `tools.add_need` is the static, launch-time, LLM-free surface; `choose_mcp_tool` is the dynamic,
   runtime surface. They are complementary and share the engine.
8. `choose_mcp_tool` is a deterministic embedding retriever, not an LLM. It returns descriptors; the
   main model does the choosing. This keeps the crate's machinery LLM-free and puts selection where
   the full task context and the author's model configuration already are.
9. On dynamic resolution the harness rewrites the context (chosen descriptor before the prose,
   discovery episode excised) so the dynamic path converges onto the static execution state. One
   execution model, regardless of surface.
10. The crate depends on a separate thin `promptforge-mcp-client` for protocol and owns only the
    semantics. Protocol consumers (such as the CLI) must not pull the embedding model, and each crate
    stays small enough for a coding LLM to hold whole.
11. An optional model-tiered configuration (strong-model select -> context-clearing goto ->
    cheap-model execute) exists for genuinely hard selection, gated on expected ambiguity.
12. MCP sampling and roots are not implemented (sampling is deprecated upstream); the crate does not
    advertise those capabilities.

## Public API (Lua-facing), normative

The crate contributes these verbs to the section Lua environment. Signatures are contracts, not
implementations.

- `tools.add(name: string)` - scope an exact, already-known tool (existing mechanism; includes
  `"choose_mcp_tool"` to opt into dynamic discovery).
- `tools.add_need(alias: string, description: string)` - declare a capability need. At launch the
  resolver binds `alias` to a concrete `(server, tool)` per the four-outcome policy; the bound alias
  is then usable exactly like a local tool name in `tools.add`. `description` is an author-register
  capability line (parameter-free). Errors at launch on ambiguity-in-own-catalog or absence.

## choose_mcp_tool return contract, normative

`choose_mcp_tool(need: string)` runs deterministic embed -> top-k over the connected catalog and
returns one of:

- a single tool descriptor `{ server, name, description, input_schema }` when one candidate clearly
  wins;
- a shortlist `[descriptor, ...]` (2-3) when the top candidates are a genuine near-tie (duplicates),
  for the main model to disambiguate with full task context;
- `{ error: "no tools available" }` when nothing clears the similarity floor.

The harness then rewrites the context to place the returned descriptor(s) before the prompt prose,
excising the call, and the main model calls the tool. The retriever result is cacheable by
`(need, catalog_hash)`.

## Resolution engine

- At startup: connect configured servers, snapshot each `tools/list` into a catalog of
  `(server, name, description, input_schema, annotations)`, and embed each tool's enriched text
  (name + description + parameter names). Cache embeddings by catalog hash.
- Per need or per `choose_mcp_tool` call: embed the need, cosine-rank the catalog, take top-k, apply
  the floor and margin, and emit one of the four outcomes. Near-identical tools (cosine >= a
  duplicate threshold, roughly 0.98) are recorded as equivalent-golds so an equivalent pick is not
  treated as wrong.

## Configuration, normative shape

- Connected MCP servers: list of `{ name, url|command, auth }` (delegated to `promptforge-mcp-client`).
- Embedding model id (default `bge-small-en-v1.5`), bundled weights path.
- Resolution thresholds: similarity floor, margin, duplicate threshold, top-k.
- Context-rewrite opt-out (per prompt/section).

## Crate boundaries

- Depends on `promptforge-core` for the `Tool` trait and on `promptforge-mcp-client` for protocol.
- Owns: the embedding engine, the four-outcome policy, the Lua verbs, and the context-rewrite hook.
- Does not own: MCP transport/JSON-RPC (that is `promptforge-mcp-client`), the model that does dynamic
  selection (that is the author's main-context model).

## Evidence (reconciled from RESULTS.md; 29,226 cases over the full 9,922-tool catalog, bge-small)

Accuracy depends strongly on how close the author's need is to the tool's own doc, so the numbers
are reported per band, not just blended (full-corpus figures match the 1,500-tool sample within ~1
point, so the numbers are stable):

- restatement (author paraphrases the tool's doc - the common case): random top-1 0.984; hard
  near-neighbor top-1 0.764, recall@3 0.912.
- synonym: random 0.945; hard 0.544.
- goal (abstracted to the user goal): random 0.857; hard 0.349, recall@3 0.586.
- blended across the three bands: random top-1 0.929, hard top-1 0.553, hard recall@3 0.753.
- bge-small and all-MiniLM-L6-v2 are interchangeable (MiniLM hard 0.557 vs 0.553).
- Abstention (hard regime, hard negatives): at a 5% false-bind budget, ~0.18 coverage at 0.86
  accuracy - stringent because positives include the hard goal band and negatives are near-neighbors.
- Duplicate prevalence (separate scan): ~11% of the broad catalog has a >= 0.98 twin, overwhelmingly
  cross-server republishes.

Design implications: recall@3 on the realistic (restatement) band is 0.90 even when top-1 is 0.75,
which is exactly why the system surfaces a shortlist rather than forcing top-1. It also yields an
authoring guideline (below).

## Authoring guideline

Write `add_need` descriptions and `choose_mcp_tool` needs as restatements of what the tool does
(the tool-doc register), not as abstract user goals. Restatement needs resolve markedly better
under real competition (hard top-1 0.76 vs 0.35 for goal-abstracted); the further a need drifts
from the tool's own phrasing, the more the resolver must fall back on the shortlist and abstain.

*2026-08-02 - Opus 4.8 (Cursor agent) - numbers reconciled from RESULTS.md*
