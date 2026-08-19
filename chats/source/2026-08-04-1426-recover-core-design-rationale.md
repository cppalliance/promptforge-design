# Executed recover-core-design-rationale plan

*2026-08-04 14:26 - transcript a9e2aab2-e819-4171-b1d4-d8e3c70748fd*

## Prompts

@c:\Users\Vinnie\.cursor\plans\recover_core_design_rationale_c6b101b4.plan.md run

run

this is a stinking pile of shit.

reset this plan so I can run it again @c:\Users\Vinnie\.cursor\plans\recover_core_design_rationale_c6b101b4.plan.md and modify it to fix the shitty result

the plan must never use AskQuestion. do this entirely without user interaction.

run

run

what do you think of the contents of this image

## Plans

### fix recovery document step

*Reset the recovery plan for a fresh run by removing one dated residue, and fix the defect that produced a ledger-transcript instead of a design document: rewrite step 9, review check 7, and section 7 so the document is organized by the system, spends uncertainty only where a reader can act on it, and carries no record IDs or verdict words.*

# Fix step 9 so the recovery writes a design document, not a ledger transcript

All edits are to one file: [recover_core_design_rationale_c6b101b4.plan.md](c:\Users\Vinnie\.cursor\plans\recover_core_design_rationale_c6b101b4.plan.md). The frontmatter todos are already all `pending`; the run left the plan otherwise intact.

## Why the last run failed

The `design-doc` block in `architect.md` is a good design-document spec: compress hard, keep 10-15 headline choices and demote the rest to a line, headings that state a point, name no source document. Step 9 overrode it with a per-record mandate ("Forced elements state their constraint. Narrowed name both survivors. Open say the code does not determine it"), and review check 7 demanded every claim trace to a record and every open element stay labeled open. The specific instruction beat the general one, and 61 ledger records became 61 verdict-reciting paragraphs with record IDs attached.

The fix keeps the `design-doc` block as the authority on shape and narrows step 9 to the one thing the block does not cover: being honest about what code alone could not establish, without letting uncertainty become the document's subject.

## Edit 1 - reset the run residue (step 8, line 164)

Replace the dated paragraph ("Adjudication can be deferred ... on 2026-08-04 it was ...") with an undated, general statement: adjudication may be deferred; if a batch goes unanswered, steps 9 and 10 proceed on the settled ledger with no proposal applied and no verdict moved; deferral is a clean measurement of what code and archive recover without a human. Add the tightened rule that flows from the two decisions just made: the document states a reason only where code forced it or the author confirmed it, and an unconfirmed archive proposal never becomes rationale in the document.

## Edit 2 - rewrite step 9 (line 166)

Replace the per-record mandate with:

- The document is organized by the system, not by the ledger. Follow the `design-doc` block as the authority on shape. The ledger is the evidence behind the document, consulted, never transcribed; a document a reader could rebuild by rewording the ledger row by row has failed.
- Stay blind to `design-core.md` - do not read it - so the recovered document is independent and the two can be compared; leave it untouched.
- The one addition the block does not cover, the uncertainty-to-prose rule:
  - Code forced the reason: state it as fact (the block's own "why").
  - Reason unsettled but a reader cannot act on not knowing it: state what the code does, omit the reason silently, no verdict word.
  - Reason unsettled and a reader could build on a decision nobody made: one sentence of explicit warning. The linear section walk is the archetype - do not present file order as a settled control-flow design.
- No record identifiers and no verdict vocabulary in the body. The ratio is step 10's job; the ledger is the committed audit trail.

## Edit 3 - rewrite review check 7 (line 191)

Replace the single check 7 with document-level checks: (7) could a reader who never saw the ledger learn how the crate works from this; (7a) does any paragraph exist mainly to report a verdict or cite a record, or does any record ID or verdict word appear in the body - the transcript failure; (7b) is uncertainty spent only where a reader can act on it and omitted silently elsewhere; (7c) is every claim supported by a settled record with nothing beyond what survived and nothing from an unconfirmed proposal, while not requiring every record to appear; (7d) does the document obey the `design-doc` block's shape.

## Edit 4 - section 7 governing rule (lines 170-179)

Retitle "How the prose must read" to "How the document must read". Strengthen the opening to name both past failures - the accurate-and-unreadable one, and the ledger-transcript one - and add a governing rule above the two existing sentence-level rules: the document is organized by the system, the ledger is evidence, and a document rebuildable by rewording the ledger has failed however clean its sentences. Keep the two existing rules (state what happens; never count what you do not name).

## Edit 5 - generalize a baked-in count (step 7, line 160)

Change "Pass 1 left 48 records narrowed or open" to a run-independent phrasing (on the order of four dozen), so the three-agents-over-thirds structure does not depend on the last run's exact count.

## Edit 6 - frontmatter todo

Update the step-9 todo content to "write design-core-recovered.md as a design document organized by the system, not a ledger transcript".

## Left as-is

The ledger filename date (`2026-08-03`) stays; step 1 recreates the file under that name and the date is cosmetic. Genuine mid-run fixes from the last pass - section 0 paths, the parallel extraction structure, the E-002 worked example, the unfalsifiable rule, the scoped-grep guard - are correct and stay.

Todos:

- Reset step 8 deferral note to undated general form, add unconfirmed-proposal-never-rationale rule
- Rewrite step 9: system-organized, blind to design-core.md, uncertainty-to-prose rule, no record IDs or verdict words
- Rewrite review check 7 into document-level checks 7-7d
- Retitle and add governing structure rule to section 7
- Generalize the baked-in '48 records' count in step 7
- Update step-9 frontmatter todo content
