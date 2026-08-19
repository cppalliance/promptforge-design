# Shortlist v2 - in-scope candidates for the purpose pass

Scope: the PromptForge language, plus the high-level rules for how the core crate is structured. Out: process/workflow principles, the gateway/MCP/CLI service layer, UI posture.

Records are identified by their location in `grouped-draft.md` (same directory): layer, theme heading, and the opening words of the statement. The purpose subagent reads the full record there, then reads the cited reduced units (in `chats/reduced/`, one level up from this file's directory) around the cited `[pN]` markers to find the motivation.

## Cluster 1: Language philosophy

From layer Global, themes "Minimal mechanism", "Legibility and naming", "Explicitness and consent":

- "Do more with less: if an established facility can implement a feature..."
- "Never provide two ways of doing the same thing..."
- "No parallel mechanisms; a single, small, well-designed set of primitives..."
- "A small set of flexible, multi-purpose primitives should compose into maximum possibility..."
- "Everything in the language behaves as consistently as possible, and constraints fall out of the existing rules..."
- "A prompt must be readable on its face..."
- "An overarching design theme of the language is that it closely resembles the ordinary theory of computation..."
- "Language keywords and names come from the vocabulary models and prompt writers already speak..."
- "Terminology is fixed and enforced repo-wide..."
- "No defaults, everything explicit..."
- "Explicit user opt-in legitimizes otherwise restricted behavior..."
- "Every protection the engine imposes can be disabled..."

## Cluster 2: The prompt as a program and document structure

From layer Core, themes "The prompt as a program" and "Document structure":

- "A prompt is a single markdown file that is one function..."
- "The design starts from the prompt and adds structured programming into it..."
- "No compilation step sits between the prompt author and the model..."
- "A prompt file is an H1 section containing a lua preamble fence..."
- "H2 is a subhead and H1 is not; every subhead's first word must be a valid identifier..."
- "Prompt documents support nested sections recursively from H2 through H6..."
- "A horizontal rule marks a section to be skipped by execution..."
- "Fall-through never crosses heading levels..."
- "XML blocks may appear anywhere in the document..."

## Cluster 3: Control flow

From layer Core, theme "Control flow":

- "Falling through to the next section is the default control flow and is context-clearing..."
- "jump() (formerly goto) destroys the current context..."
- "execute() runs a referenced section as a subroutine in a fresh VM..."
- "A section ends when the model replies with text and no tool calls..."
- "Cyclic section calls are permitted because some tools require cycles..."
- "A task is either synchronous or asynchronous..."

## Cluster 4: Lua environment and state

From layer Core, themes "Lua environment" and "State and context":

- "Embedded Lua is kept minimal..."
- "A prompt's key-value parameters are read-only and visible to every section..."
- "A single ```lua shared chunk per prompt is compiled once and replayed..."
- "The H1 preamble runs exactly once as a live preamble..."
- "All Lua chunks in one H2 section share a single VM..."
- "Tools and models are first-class Lua objects..."
- "infer() is a blocking call with a fresh context..."
- "State is built through flat tool calls into a persistent store..."
- "The store is a virtual filesystem for file-shaped intermediate values..."
- "State is carried as a key/value block written by Lua..."
- "The engine exposes system facts to prompts through a sys object..."

## Cluster 5: Tools and models

From layer Core, themes "Tool scoping and declaration" and "Models":

- "Per-section tool scoping is opt-in..."
- "There is exactly one tools.add entry point..."
- "A prompt can assert postconditions on tool usage in its epilogue..."
- "A tool can be implemented as an inline Lua function..."
- "Models are declared in the prompt's introduction via models.add..."
- "Model binding is much looser than tool binding..."

## Cluster 6: Trust, errors, observability

From layer Core, themes "Trust" and "Errors and observability", plus layer Boundary record "Secrets and privileged calls live only in the trusted backend...":

- "Content arriving from external sources is untrusted and injection-prone..."
- "The store's read API is split by trust and presentation..."
- "When fetched evidence is unusable, the run aborts..."
- "Every error reported to the prompt author carries the source file and line number..."
- "Every harness operation reports its activity to an optional caller-installed observer..."
- "Run artifacts are written incrementally as turns complete..."
- "Secrets and privileged calls live only in the trusted backend..."

## Cluster 7: Fanout

From layer Core, theme "Fanout":

- "Fanout is always invoked explicitly through a fanout() call..."
- "The subagent section is the arm template..."
- "The invoking Lua owns the reduce step..."

## Cluster 8: Core crate structure and boundaries

From layer Global, themes "Continuous debt payment and evidence" and "Code and repo hygiene", and layer Boundary:

- "Refactoring happens continuously at every step: each file holds a single concern, a smaller API is always better..."
- "Every markdown feature of the prompt format ships with a corresponding test..."
- "Library code propagates errors and never unwraps; new dependencies are not introduced..."
- "Crates are kept small enough that a coding LLM can hold an entire crate..."
- "The executor holds no vendor credentials, endpoints, or provider knowledge..."
- "Model-specific translation to and from tool calls is the gateway's responsibility..."
- "Components do not share schema definitions... the gateway must not depend on core."
- "Integration tests require an already-running, already-configured gateway..."
