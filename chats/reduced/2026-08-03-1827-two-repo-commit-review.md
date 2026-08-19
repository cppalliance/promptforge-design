# Two-repo commit review step

*2026-08-03 18:27 - transcript 41d84ee8-4cea-4d1b-b29c-7231d2f973b9*



## Prompts



**[p1]** You are reviewing one commit in each of two repositories, which together are one step: HEAD in c:\Users\Vinnie\src\cursor\promptforge-design (the rename, retitle, and cross-reference repointing) and HEAD in c:\Users\Vinnie\src\cursor\promptforge (a STATUS pointer).

**[p2]** Read these sources of checks:
1. c:\Users\Vinnie\src\cursor\tools-public\how-to\vibe-how-to.md - grep it for `code-review` and apply the block those tag lines delimit.
2. c:\Users\Vinnie\.cursor\plans\promptforge_mcp_server_correction_97dfaec0.plan.md - grep it for `mcp-review`; check 15 is written for exactly this commit. Read the three-commit shape in section 5 and the entry covering steps 14, 15 and 16.

**[p3]** Read both diffs with `git show HEAD --find-renames` in each repository.

**[p4]** Judge these things. Does the residue say plainly at its top that it is forward design, name what exists today, and point at the crate's document? Is anything it asserts about the built world wrong, including its lists of what is unbuilt and what is partly built - check each against c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core, since claiming something unbuilt that ships is as wrong as the reverse. Did the commit touch seven files to repoint references - verify each repointing is correct and that none changed meaning beyond the pointer. Search both repositories for any surviving reference to the design repository's old `design-core.md`, remembering the crate now has a file of that name. Was anything deleted as redundant that was not? Did it touch anything steps 17 through 19 own?

**[p5]** Write your findings to c:\Users\Vinnie\src\cursor\promptforge\vibe-review.md, overwriting whatever is there. For every failure write one entry: the repository, the file and line, the problem in one sentence, and the single change that fixes it. Write nothing for a check that passes. If everything passes, write a single line saying so.

**[p6]** Do not fix anything yourself and do not commit. Report back in under 80 words: how many findings, and the most serious one.



## Design Documents Written

### c:\Users\Vinnie\src\cursor\promptforge\vibe-review.md

# Review - step 16, `design-core.md` finish

- **promptforge-design, `agentic-harness-ide-report.md` line 183.** The source list still cites `promptforge-design/design/design-core.md`, a path that no longer exists and whose bare name now denotes the crate's as-built document instead. Change the path to `promptforge-design/design/design-core-residue.md`.

- **promptforge-design, `agentic-harness-ide-report.md` line 43.** The parenthetical source citation still names `design-core.md`, so it points at the moved-and-renamed document by a name that now belongs to the crate's file. Change `design-core.md` to `design-core-residue.md` in that citation.

- **promptforge-design, `agentic-harness-ide-report.md` line 62.** The sentence quotes "design-core.md is unambiguous" for the context-destruction passage, which is residue content and no longer lives under that name in this repository. Change `design-core.md` to `design-core-residue.md` in that sentence.

- **promptforge-design, `design/design-core-residue.md` line 849.** The rewrite of the completion paragraph dropped the rationale sentence "That is the ordinary termination of any tool-call loop and needs no signal from the prompt: the model has nothing left to do, so it says so in prose and the executor moves on," which the transfer did not make redundant and which appears nowhere else in the file. Restore that sentence after the paragraph's first sentence.

*2026-08-03 18:35 - Opus 5 (Cursor agent)*


StrReplace-edited design docs (path only): `c:\Users\Vinnie\src\cursor\promptforge\vibe-review.md`
