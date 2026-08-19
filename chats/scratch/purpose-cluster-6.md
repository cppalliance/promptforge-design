# Purpose pass - Cluster 6: Trust, errors, observability

## Record 1: "Content arriving from external sources is untrusted and injection-prone..."

Purpose: Web fetches and other outside content go straight into the model's context, and anything in that content that looks like an instruction can hijack the prompt. The author hit this concretely while wiring the briefer tool: the `reply` being injected was "the joining of web fetches" and "definitely untrusted," and he needed a way to inject it while telling the model it is data, not commands. He also wanted the wrap to work on any string, not just store content, which is why `store.inject` was removed in favor of a global `untrusted(s)`.

Citations: 2026-08-19-0048-promptforge-md-aug19.md [p3], [p4], plans section; 2026-08-08-0029-promptforge-context-planning.md [p17]; 2026-07-30-1046-compaction-algorithm-large-part5.md [p333]-[p335]; 2026-08-14-1613-promptforge-core-largest-part2.md [p159], [p161]; 2026-08-18-1126-promptforge-md-aug18-morning.md [p110]

Merge: shares its purpose with Record 2 - both exist so outside content reaches the model only inside the untrusted envelope. Candidate to merge into one principle about untrusted content handling.

## Record 2: "The store's read API is split by trust and presentation..."

Purpose: The author worried that numbered lines might look like protection they do not provide - he asked outright "what's the danger of an injection attack if we use line numbers?" The split keeps the three uses separate so nobody mistakes line numbers for a security control: numbering is only for editing and navigation, verbatim read is for trusted handoff, and anything going to the model must go through the untrusted envelope. Without the split, a caller could inject numbered store content raw and believe it was safe.

Citations: 2026-08-08-0029-promptforge-context-planning.md [p17], [p20], [p22]; 2026-08-19-0048-promptforge-md-aug19.md [p12], [p16], [p17], [p18]

Merge: same purpose as Record 1 (the envelope is the only trust mechanism). Merge candidate.

## Record 3: "When fetched evidence is unusable, the run aborts..."

Purpose: The author asked what happens if all the fetched content is a bunch of 404s, and decided the run must stop: if the fetch fails and the run continues, the model invents an evidence packet, and every downstream step built on that invented packet is garbage. Aborting is the only way to keep a bad fetch from silently poisoning the whole result.

Citations: 2026-08-14-1613-promptforge-core-largest-part2.md [p173], [p174]; 2026-08-09-1058-promptforge-core-large-part3.md [p173], [p174]

Merge: none.

## Record 4: "Every error reported to the prompt author carries the source file and line number..."

Purpose: This rule came out of repeated debugging failures: assertion errors kept arriving with no file and line ("assertion failed and we aren't getting the file and line numbers again," "happened again and again no line number," "again missing line number"), and without the location the author could not find which line of the prompt caused the failure. He also got bitten by calling the wrong API function with no warning at all - "this is kind of a trap." His stated rule: "for all errors, there has to be a file and line in, that corresponds to the prompt."

Citations: 2026-08-18-1126-promptforge-md-aug18-morning.md [p54]; 2026-08-14-1613-promptforge-core-largest-part3.md [p279], [p280], [p313]; 2026-08-14-1613-promptforge-core-largest-part2.md [p164]; 2026-08-09-1058-promptforge-core-large-part2.md [p86]

Merge: related to Records 5 and 6 (all three serve debugging a run) but distinct: this one is about locating the failing prompt line, not observing engine behavior. Keep separate.

## Record 5: "Every harness operation reports its activity to an optional caller-installed observer..."

Purpose: The author could not debug runs or tests because he could not see what the engine did - "the logs are kind of useless for debugging. I can't see what went into evidence.md" - and he wanted tests to be able to tell whether code reached a certain point. He asked for the observer as a cross-cutting facility and cut the typed event taxonomy down to two strings (Section, Detail) because the richer events "seem kind of pointless." Concurrency-safety and per-execution ids exist because fanout runs arms in parallel and their log lines would interleave.

Citations: 2026-08-09-1058-promptforge-core-large-part1.md [p39], [p40], [p53]-[p56]; 2026-08-14-1613-promptforge-core-largest-part1.md [p39], [p40], [p55], [p56]; 2026-08-19-0048-promptforge-md-aug19.md [p6]; 2026-08-09-1058-promptforge-core-large-part2.md [p97], [p105]

Merge: shares the run-debugging purpose with Record 6. Candidate to merge into one observability principle.

## Record 6: "Run artifacts are written incrementally as turns complete..."

Purpose: Buffering everything until the end of the run blocked debugging - "this is stupid how it waits to write all the json turn files" - so turns and files are written as they arrive, and stale traces are deleted on launch so old output is never confused with the current run. The deeper driver is the analytical pipeline: "it is absolutely essential for development and debugging, to be able to re-run the prompt from any step," which requires every intermediate output to exist as a file that can be read back in.

Citations: 2026-08-14-1613-promptforge-core-largest-part3.md [p290], [p298], [p299]; 2026-08-14-1613-promptforge-core-largest-part2.md [p128], [p165]; 2026-07-28-0207-architect-vibe-planning-part1.md [p3]; 2026-08-14-1613-promptforge-core-largest-part5.md [p377]

Merge: shares the run-debugging purpose with Record 5. Candidate to merge.

## Record 7: "Secrets and privileged calls live only in the trusted backend..."

Purpose: The author did not want his API key anywhere the model could see it - "you're gonna be handling my API key, which is no good. I don't want the API key to leak into the model" - because anything that enters the model's context can be repeated or exfiltrated. The same rule keeps keys out of the frontend webview (the LLM call happens in the Rust backend with the key in the OS credential store) and out of git (gitignored .env), and the prompt's instructions forbid the model from reading any .env file into context.

Citations: 2026-08-15-2006-promptforge-md-aug15.md [p6], [p18], [p19], [p22]; 2026-07-31-1516-agentic-ide-research.md [plans section: Vibbi Chat Panel]

Merge: none. Related to Record 1 (both keep dangerous things out of the model's context) but the direction is opposite - Record 1 guards the context from content coming in, this one keeps secrets from getting in at all. Keep separate.

## Merge summary

- Records 1 + 2: one purpose (outside content reaches the model only through the untrusted envelope; nothing else is a trust control). Merge.
- Records 5 + 6: one purpose (a run must be observable and debuggable while it runs and after). Merge.
- Result: 7 records, 2 merges, 5 principles. No records with "no purpose found."
