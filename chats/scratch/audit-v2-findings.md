# Audit v2 findings - design-principles.md

Purpose (check 2) - Principle 10 (line 47): the rationale "the Lua picks the tools, and the prose runs with those tools; a fence after the prose would run too late to matter" states a motive not found in the purpose notes - fix: use the recorded motive, that position rather than content tells reader and parser which fence is which, so a preamble can never be confused with an epilogue.

Purpose (check 2) - Principle 41 (line 157): "Conditional compilation multiplies the configurations that must be tested and hides code paths from review" is a motive not found in the purpose notes, which record only one stated reason - fix: say there is only one version of the binary, and if size becomes a problem the crate gets split later.

Purpose (check 2) - Principle 46 (line 167): "a test that launches services is testing its own launch code" is a motive not found in the purpose notes - fix: state the recorded motive, that tests launching the gateway themselves got stuck and failed, and that wiring a model directly into the harness was duplicated effort.

Purpose (check 2) - Principle 37 (line 133): "The author learns the rule from the failure" is a motive not found in the purpose notes - fix: delete the sentence, since the recorded motive (failures arrived with no file and line and could not be located; silent API misuse was a trap) is already stated.

Plain words (check 3) - Principle 2 (line 23): "A hand-coded guard is a confession that the rules are underpowered, and it drifts out of sync with them" is an invented metaphor where the record is concrete - fix: say a correct constraint should fall out of the existing rules on its own, not be a separate check someone has to remember to write.

Plain words (check 3) - Principle 14 (line 63): "context the author cannot see, bound, or afford" is an abstraction where the record is concrete - fix: say accumulated context bloats the window, and small contexts are what keep small, cheap models reliable.

Plain words (check 3) - Principle 46 (line 167): "a test that launches services is testing its own launch code" is an aphorism where the record has a concrete reason - fix: say plainly that the self-launched gateway got stuck and failed.

Plain words (check 3) - Principle 37 (line 133): "The author learns the rule from the failure" is an aphorism the author never said - fix: delete it (same fix as the Purpose flag above).

Scope (check 7) - Principle 40 (line 155): "Pay down debt on every commit" is a commit-ritual and process rule, not a rule about the language or the core crate's structure - fix: remove it from this document.

Scope (check 7) - Principle 45 (line 165): "the gateway never depends on core" and cross-component schema ownership are rules about the gateway service boundary, not the core crate's own structure - fix: remove or move to a boundary/architecture document.

Scope (check 7) - Principle 46 (line 167): requiring an already-running, already-configured gateway is a rule about the gateway service and test-launch workflow - fix: remove or move to a boundary/architecture document.
