# Packet Section VI - Trust and Failure (principles 34-37)

Facts only. No prose. Writer subagent turns this into exposition.

## Principle 34 - Untrusted envelope

- Rule: Outside content reaches the model only inside the untrusted envelope.
- Purpose facts:
  - Web fetches and other outside content go straight into the model's context; anything in that content that looks like an instruction can hijack the prompt.
  - Lets the author wrap any string, not just store content - this is why `store.inject` was removed in favor of a global `untrusted(s)`.
  - `untrusted(s)` wraps any string with the injected tag and the machine instruction to treat the contents as data, not instructions.
  - Tools that return attacker-controllable output are wrapped automatically when the tool declares an untrusted-output property.
  - Marker strings inside the content are escaped so the delimiter cannot be forged; content that forges the envelope's open or close tags is defanged before injection.
  - The envelope is the only trust control. Line numbers on store reads are for navigation and editing only; the split read API (`read_lines` numbered for editing, `read` verbatim for trusted handoff, injection via the envelope) exists so nobody mistakes line numbers for protection.
  - What breaks without it: a caller could inject numbered store content raw and believe it was safe.
- Rejected alternatives and stated costs:
  - An inject method on the store (`store.inject` is removed, not kept as sugar).
  - Injecting stored content into the context raw.
  - A separate safe-fetch tool chosen per call.
  - A single read call with a trusted/untrusted flag.
  - Treating numbered output as safe for model consumption.
  - A (startLine, lineCount) range form.
  - A global `numbered()` function composing strings in memory.
- Concrete incidents:
  - Hit while wiring the briefer tool: the `reply` being injected was "the joining of web fetches" and "definitely untrusted"; the author needed to inject it while telling the model it is data, not commands.
  - Author-verbatim: "what's the danger of an injection attack if we use line numbers?" - the question that motivated the split read API.
- Merge/derivation notes:
  - Merged from purpose-cluster-6 Record 1 ("Content arriving from external sources is untrusted and injection-prone...") and Record 2 ("The store's read API is split by trust and presentation..."). Both share one purpose: outside content reaches the model only through the untrusted envelope; nothing else is a trust control.
  - Grouped-draft endorsements: envelope record `corrected (ai-proposed leg)`; split-read record `affirmed (ai-proposed leg)`.
  - Scope: core. Sources: user-corrective; user-stated; ai-proposed.

## Principle 35 - Secrets never enter context

- Rule: Secrets never enter the model's context.
- Purpose facts:
  - Anything that enters the model's context can be repeated or exfiltrated.
  - API keys stay in the trusted backend; the LLM call happens in the Rust backend with the key in the OS credential store.
  - .env files are gitignored so secrets never enter version control.
  - The language's instructions explicitly forbid the model from reading any .env file into context.
  - App UI runs in the trusted context while third-party web content runs isolated.
- Rejected alternatives and stated costs:
  - Passing the API key through the prompt or the core instruction file.
  - Making LLM calls from the frontend with the key present in the webview.
- Concrete incidents:
  - Author-verbatim: "you're gonna be handling my API key, which is no good. I don't want the API key to leak into the model."
- Merge/derivation notes:
  - From purpose-cluster-6 Record 7 ("Secrets and privileged calls live only in the trusted backend..."). No merge.
  - Relation to Principle 34: both keep dangerous things out of the model's context, but the direction is opposite - 34 guards the context from content coming in, 35 keeps secrets from getting in at all. Kept separate for that reason.
  - Grouped-draft endorsement: `affirmed (ai-proposed leg)`. Scope: boundary gateway<->model; app<->web. Source: user-stated; ai-proposed (affirmed).

## Principle 36 - Abort on unusable evidence

- Rule: A run aborts when fetched evidence is unusable.
- Purpose facts:
  - If the fetch fails and the run continues, the model invents an evidence packet, and every downstream step built on that invented packet is garbage.
  - Aborting is the only way to keep a bad fetch from silently poisoning the whole result.
  - What breaks without it: a hallucinated evidence packet taints the entire downstream result.
- Rejected alternative and stated cost:
  - Soft-returning fetch failures and letting the prompt hallucinate past them.
- Concrete incidents:
  - The author asked what happens if all the fetched content is a bunch of 404s, and decided the run must stop.
- Merge/derivation notes:
  - From purpose-cluster-6 Record 3 ("When fetched evidence is unusable, the run aborts..."). No merge.
  - Grouped-draft endorsement: n/a. Scope: core. Source: user-stated.

## Principle 37 - Errors carry file and line

- Rule: Every error reported to the prompt author carries the file and line in the prompt that produced it, and misusing an API function produces a warning rather than silent wrong behavior.
- Purpose facts:
  - Without the location there is no finding which line of the prompt caused the failure.
  - Includes assertion failures.
  - What breaks without it: the author cannot locate the failing prompt line.
- Rejected alternatives and stated costs:
  - Errors that lack the prompt's file and line location.
  - Silently accepting the wrong function with no warning.
- Concrete incidents:
  - Assertion failures kept arriving with no location, repeatedly.
  - Author-verbatim: "assertion failed and we aren't getting the file and line numbers again"; "happened again and again no line number"; "again missing line number."
  - The author got bitten by calling the wrong API function with no warning at all - "this is kind of a trap."
  - Author's stated rule, verbatim: "for all errors, there has to be a file and line in, that corresponds to the prompt."
- Merge/derivation notes:
  - From purpose-cluster-6 Record 4 ("Every error reported to the prompt author carries the source file and line number..."). No merge.
  - Related to the observability records (observer/trace events, incremental run artifacts) - all three serve debugging a run - but kept separate: this one is about locating the failing prompt line, not observing engine behavior. Those observability records landed elsewhere (not in this section).
  - Grouped-draft endorsement: n/a. Scope: core. Sources: user-corrective; user-stated.

## Stanza facts - Section VI "Trust and Failure"

- What the section covers: untrusted content, secrets, and what happens when things go wrong.
- Why the layer exists: a prompt that reads the web is a prompt that can be hijacked, and a run that fails quietly is worse than a run that fails.
- Failure modes it prevents:
  - Prompt injection via fetched or tool-returned content (34).
  - Mistaking line numbers for a security control (34).
  - Secret leakage or exfiltration through the model's context, the frontend webview, or version control (35).
  - Silent poisoning of a run by a hallucinated evidence packet after a failed fetch (36).
  - Undiagnosable failures: errors with no prompt file/line, and silent wrong behavior from misused API functions (37).
- Unifying principle (one sentence): guard the context, and when something breaks, say so.
- Principle count: 4 (34, 35, 36, 37).
