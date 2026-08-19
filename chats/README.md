# Chat Corpus and Design-Principle Pipeline

This directory holds the corpus and intermediates for mining PromptForge design principles from chat transcripts. A fresh context that reads only this file can rerun the extraction from any point. Everything here is regenerable; the final document is `promptforge-design/design-principles.md`.

## Directory map

- `source/` - the immutable originals. One file per chat, named by date and topic slug. Each file holds the user's prompts in order, then the plans created during the chat, then the design documents written during the chat. Never modified by any pipeline stage.
- `scratch/` - working copies and pipeline tooling. Cleaned units (one per source file, or several `-partN` files for the five largest, split at topical boundaries), with harness boilerplate and content-free acknowledgments removed and every surviving paragraph carrying a stable `[pN]` marker. Also holds the cleaning script (`clean.py`), the task-block file (`extractor.md`), the dedupe chunks and halves, the grouped draft, the approach paragraph, and the audit findings.
- `reduced/` - the recall-first compressed units. Pasted papers, code dumps, and debugging blow-by-blow are compressed to one-line notes; principle-bearing paragraphs survive verbatim with their `[pN]` markers. Extraction reads only these.
- `cabinet/_research/` (outside this directory) - the candidate files, one per unit, each holding principle records in yaml form plus a "Not converted" list; also the consolidated packet and the cross-check results.

## Pipeline stages

1. **Clean** - deterministic script. Reads `source/`, removes known noise, numbers paragraphs, splits large files at hardcoded topical cuts. Produces `scratch/`.
2. **Reduce** - one subagent per unit over 30KB. Recall-first: cut only what cannot carry a principle. Produces `reduced/`.
3. **Pilot** - extract from 3 known-content units and check the pass criteria before spending on the fan-out.
4. **Extract** - one subagent per reduced unit, dispatched by reference against `extractor.md`. Produces one candidate file per unit in `cabinet/_research/`.
5. **Consolidate** - shell concatenation of the candidate files into one packet. The main context never reads the records.
6. **Dedupe** - if the packet exceeds 400 records, slice it into batches at file boundaries and run one dedupe subagent per batch, then again on halves if needed. Duplicates assert the same constraint on the same scope; citations merge under the sharpest wording.
7. **Group** - one strong subagent dedupes across the whole packet, trims to the strongest 100, assigns scope layers, clusters into themes, writes stanzas, and preserves the merged Not-converted list.
8. **Cross-check** - one subagent compares the mined set against the AI-written design docs and sorts everything into attested, undocumented, and suspected-confabulation buckets.
9. **Approach** - one subagent compresses the merged Not-converted list into the closing prose section.
10. **Assemble the writing packet** - one assembler subagent per output section. Each fact sheet carries the rule, the purpose facts, the rejected alternative and its cost, the concrete incidents, and author-verbatim phrases worth keeping. Produces `scratch/packet-section-N.md`, concatenated by shell into `scratch/writing-packet.md`. The packet is structured like the final document but holds facts, not prose.
11. **Write** - a fresh writer subagent in a teacher register ("You are a writer tasked with explaining design principles as a teacher would teach a student. Write in simple, clear terms.") reads only the writing packet and writes the final document. The orchestrating context never writes the document: a context that planned the work covers its gaps from memory, so the writer starts cold. The writer's task block lives in `scratch/writer-task.md`.
12. **Audit** - a fresh subagent checks grounding, purpose, plain words, provenance, numbering, structure, and scope against the writing packet; the main context applies the fixes.

## Derivation rules

- **Altitude test.** If a statement says which technology to use, it is an implementation preference: exclude it. If it says how the language or engine behaves, it is a candidate: extract it. The test applies to user prompts and to AI-written plans alike.
- **Purpose test.** Every principle must answer two questions from the record: what does this let the author do, and what breaks without it? A statement that can only describe how the mechanism works is a specification, not a principle; it belongs to the user guide. Take the purpose only from the record: the discussion before the decision, the pain being fixed, or the stated cost of the rejected alternative. When two candidates share one purpose, merge them into the principle that purpose supports. Never invent a motive; a candidate with no purpose in the record is dropped, not rationalized.
- **Plain words.** No invented metaphors, no abstractions where a concrete reason exists. When the reason is mechanical, state the mechanism as the reason. The test: every sentence is something the author would say out loud.
- **Source types.** User-stated and user-corrective records are strong evidence. Ai-proposed records (mined from plans and design documents) carry an endorsement - affirmed, corrected, rejected, unaddressed - and an unaddressed one is weak evidence.
- **Write-once.** No intermediate is ever edited in place. Every stage writes fresh files; iterations and reruns write versioned paths. The full trail stays auditable.
- **Dispatch by reference.** Subagent tasks live in `extractor.md` under unique tags. A dispatch carries only the file path, the tag name, and the run's paths, so the orchestrator holds nothing large enough to paraphrase.

## How to rerun

- **From the top:** run `clean.py` in `scratch/`, then follow the stages in order. Every stage is idempotent against fresh outputs.
- **From any middle point:** each stage needs only its named inputs. Extraction needs `reduced/` and `extractor.md`. Grouping needs the packet. Packet assembly needs the grouped draft, the purpose notes, and the current document's structure. Writing needs only the writing packet and `writer-task.md`.
- **After a compaction:** this file, the plan, and the artifact map are sufficient. The main context holds no state that disk does not.
- **With different rules:** edit the task blocks in a fresh versioned copy of `extractor.md`, rerun from the extract stage, and write outputs to versioned paths. The reduced corpus is reusable; reduction does not need to run again.
