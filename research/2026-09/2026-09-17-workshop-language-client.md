# Steal List: Building the Workshop Language Client from Existing Parts

Report type: analytical / recommendation. Audience: project lead. Decision served: which architecture and which borrowed parts to use for the workshop's language-client and debugger work.

## Executive summary

A five-way source survey (Zed, Helix, the Lua language-server landscape, the Rust crate ecosystem, and webview integration libraries) found that every layer of the workshop's planned language tooling has a maintained, license-clean donor, with one exception: the debug UI. The recommended architecture is a thin WebSocket-to-stdio relay inside `workshop-server` (about 200 lines of Rust), the official `@codemirror/lsp-client` package (MIT, by CodeMirror's author) in the webview, LuaLS serving the embedded Lua fences through per-fence virtual documents, and `promptforge-parser` wrapped in an `async-lsp` server so PromptForge itself rides the same pipeline as third-party languages. The debugger stays a custom protocol over the existing WebSocket, because no browser-ready DAP client library exists. Estimated total effort is 4 to 6 weeks, against 3 or more months for the hand-rolled equivalent.

This report revises the architecture recommended in conversation before the survey. The prior front-runner was a smart LSP client written in Rust behind an intent-level WebSocket protocol. That design was demoted because the survey found an official, actively maintained CodeMirror 6 LSP client that expects LSP on the wire; a bespoke intent protocol would discard the single most de-risking asset available. Confidence: high, because the two most load-bearing claims (the CM6 client and the Rust client crate) were verified against npm and crates.io on the day of writing.

## Recommendation: keep CodeMirror, relay stdio over WebSocket, adopt the official client

Build the language-client feature as three pieces. First, a relay module in `workshop-server` that accepts a WebSocket connection, spawns a language-server binary, and shuttles frames between the two, adding or stripping `Content-Length` headers at the boundary. Second, `@codemirror/lsp-client` in the webview, connected through its `Transport` interface, which is three methods (`send`, `subscribe`, `unsubscribe`) over plain JSON strings. Third, a small server-management layer in Rust that owns spawn, restart, and stderr capture. This keeps the entire CodeMirror 6 editor investment, adds near-zero bundle weight, and puts zero position-conversion code on the happy path, because CodeMirror offsets, JavaScript strings, and LSP's default encoding are all UTF-16 code units. Confidence: high, the pattern is proven in production by multiple existing integrations.

## Criteria: protect the editor, minimize protocol code, stay license-clean

The options were weighed against six criteria, in order of importance.

- Preserve the existing CodeMirror 6 editor layer (keybindings, search, settings, dockview integration), which represents sunk work that no option should silently discard.
- Minimize protocol code the team maintains, because LSP client code is a known long-tail maintenance burden.
- Stay license-clean for a BSL-licensed proprietary product.
- Keep the system testable inside the existing Rust and node test harnesses.
- Leave a path to the planned line-level Lua debugger.
- Hold bundle size and startup weight roughly flat.

## Four options, one front-runner

Table 1 compares the four options against the criteria.

| Option | Editor kept | Protocol code owned | License risk | Debug path | Bundle cost |
|---|---|---|---|---|---|
| 1. Relay + `@codemirror/lsp-client` | yes | relay only (~200 lines) | none (MIT) | custom UI | near zero |
| 2. Smart Rust client + intent WS | yes | full client (~2,000 lines) | none (MIT/Apache crates) | custom UI | near zero |
| 3. Monaco + `monaco-languageclient` | no (rewrite) | relay only | none (MIT) | `monaco-vscode-api` shortcut | +4 to 12 MiB |
| 4. Do nothing (parser diagnostics only) | yes | none | none | none | zero |

Table 1. Options for workshop language-client architecture, scored against the six criteria. Sources: webview integration survey and Rust crate survey, 2026-09-17.

**Option 1 wins on criteria 1, 2, and 6 outright.** Its weakness is criterion 4: the protocol logic lives in TypeScript, where the test harness is thinner, and the official client carries a single-author bus factor plus the author's own admission of limited real-world battle-testing. Both weaknesses are mitigated: the package is the official CodeMirror organization's client, versioned 6.3.0 and updated the day of this writing, and the relay boundary means a misbehaving client can be swapped without touching server code.

**Option 2 was the pre-survey front-runner and is now the fallback.** A Rust client built on `async-lsp` and `lsp-types` keeps everything in the strongly tested tier and makes the webview a dumb renderer, but it owns roughly ten times more protocol code and cannot use any maintained CodeMirror LSP library, because every one of them expects LSP on the wire. It remains the right answer if the official CM6 client proves unreliable in the first two weeks of integration. Confidence: medium, because the deciding factor is the CM6 client's behavior under real servers, which is untested here.

**Option 3 buys a solved client and a future debug-UI shortcut at the price of the editor layer.** Monaco plus `monaco-languageclient` is the most battle-tested webview LSP stack, and `monaco-vscode-api` offers a path to real VS Code debug services later. The cost is a full rewrite of the editor surface and 4 to 12 MiB of bundle. This option stays on the shelf unless the workshop's editor ambitions grow to match VS Code's feature surface. Confidence: medium-high, the trade is real but the workshop's current ambitions do not require it.

**Option 4, do nothing, means PromptForge diagnostics only.** The direct `Prompt::parse` integration already planned delivers that. It is the correct choice if third-party language support is not actually a product pillar; the survey's cost estimates assume it is.

## Zed is design-only: GPL walls off the code, but five designs are worth copying

Zed's editor crates (`lsp`, `project`, `language`, `dap`) are GPL-3.0-or-later and marked `publish = false`, so nothing is on crates.io and no editor code can be lifted into a proprietary product. The two type crates Zed pins are permissive: its `lsp-types` fork is MIT and `dap-types` is MIT or Apache-2.0. The value is therefore architectural. Five designs transfer directly to the relay and server-management layers.

- A per-(document, server) snapshot log, where incremental `didChange` events are computed from edits since the server's last acknowledged version, never from raw keystrokes.
- A method-keyed handler registry with a `method_not_found` backstop, because an unanswered server-initiated request can deadlock real servers (gopls is the cited example).
- A single channel-fed writer task per server, so framed messages can never interleave on the wire.
- A dedicated stderr drain task with a crash-capture buffer, so a dead server leaves a diagnosis instead of silence.
- A DAP transport that mirrors the LSP transport shape, including a spawn-then-TCP-attach mode and the practice of capturing adapter stdout into the attach-failure error.

One anti-pattern to avoid: Zed bakes UTF-16 dual-coordinate types through its entire text model. The relay architecture converts at one edge or nowhere, because the webview's coordinate system already matches LSP's. Source: Zed recon, 2026-09-17; repository license files and crate manifests at github.com/zed-industries/zed.

## Helix is vendorable under MPL-2.0, but design-copying is cheaper

Helix's `helix-lsp` crate is MPL-2.0, whose copyleft is file-scoped: copied files must stay MPL-2.0 with notices intact and their source made available when shipping executables, while the larger work remains under the project's own terms. Vendoring is legal, but the cheaper path is to copy the designs and use the MIT `lsp-types` crate for types. Four designs stand out.

- A deliberately tolerant, hand-rolled JSON-RPC layer (about 350 lines) that accepts float request IDs, extra fields, and garbage log lines interleaved on stdout, because real servers violate the spec constantly.
- A three-task transport (receive, send, stderr) with pending requests correlated through a map of oneshot channels, plus lifecycle events injected into the normal inbound stream so there is one event source.
- Incremental sync computed by walking an edit changeset rather than diffing text; CodeMirror transactions map onto this naturally.
- A `languages.toml`-style configuration schema: per-server command, args, environment, timeout, and required-root patterns, plus per-language feature gating. The schema is worth copying nearly verbatim for the workshop's server registry.

Helix also ships an experimental DAP client (`helix-dap`) whose transport is the same framing shape as LSP, confirming that one framing module can serve both protocols. Source: Helix recon, 2026-09-17; LICENSE and crate sources at github.com/helix-editor/helix.

## Rust crates cover types and the client core; the rest is about 1,500 lines

Table 2 gives the build-versus-borrow inventory for the Rust side. Two crates carry real weight. `lsp-types` 0.97 (MIT) covers LSP 3.16 plus the 3.17 position-encoding types, but has had no release since June 2024, so it should be pinned with hand-written serde newtypes for any gaps. `async-lsp` 0.2.4 (MIT or Apache-2.0) is the only maintained, client-capable framework found; it is tower-based, deliberately low-level, and its README states it can build both servers and clients. Both claims were verified against crates.io on 2026-09-17.

| Layer | Decision | Detail |
|---|---|---|
| Protocol types | borrow | `lsp-types` 0.97 (MIT), pinned |
| Client core | borrow | `async-lsp` 0.2.x (MIT/Apache) |
| Content-Length framing | build | about 80 lines; no crate exists |
| Document sync | build | about 400 to 600 lines, app-specific |
| Position conversion | build | about 150 lines, or borrow `lsp-document` |
| Process management | build | about 200 lines on `tokio::process` |
| WebSocket relay | build | about 200 lines on axum WS |

Table 2. Build-versus-borrow inventory for a Rust LSP client. Source: Rust crate survey, 2026-09-17.

Two spec gotchas outrank everything else in this table. First, rust-analyzer advertises incremental-only document sync, so any client must implement ranged `didChange` edits; full sync is not a safe default. Second, position-encoding negotiation is a trap: rust-analyzer and LuaLS prefer UTF-8 if offered, so the client should advertise only `utf-16`, which also happens to match the webview's native coordinates exactly. A minimal client must also answer a fixed list of server-initiated requests (`workspace/configuration`, `workspace/applyEdit`, `window/workDoneProgress/create`, `window/showMessageRequest`, `client/registerCapability`, `workspace/workspaceFolders`, `window/showDocument`), most of which can be declined by not advertising the matching client capability. Source: LSP 3.17 specification text and server documentation, as cited in the Rust crate survey, 2026-09-17.

## LuaLS serves the Lua fences today; emmylua_ls is the in-process reserve

For the embedded Lua fences, the survey recommends LuaLS (lua-language-server). It is MIT-licensed, models Lua 5.1 through 5.5, ships as a 4.45 MB Windows zip, and documents a single-file fallback scope when the client sends `rootUri: null`, which suits a desktop app opening loose prompt files. Confidence: high, it is the only surveyed server explicitly modeling Lua 5.5 with a massive deployment base. The strategic reserve is emmylua_ls (MIT), a Rust-native server structured as reusable crates (`emmylua_parser`, `emmylua_code_analysis`), which opens a future path where Lua analysis runs in-process with no child process at all. Confidence: medium, it is younger and less battle-tested.

No Lua server analyzes Markdown-embedded Lua natively. The standard approach is client-side virtual documents with bidirectional position mapping, the pattern used by Volar, JupyterLab, and Svelte tooling, with a close Rust precedent in sudolang-lsp. Each fence becomes an independent virtual document, which matches PromptForge's semantics exactly, since each fence is a separately compiled chunk. The `lua shared` fence should be modeled as a library visible to each fence document, not concatenated into them, because concatenation would misrepresent chunk isolation. The position mapping this requires is already solved on the PromptForge side: the parser tracks each block's source line.

The largest Lua-specific risk is the sandboxed-stdlib mismatch. Both candidate servers assume the full standard library for the selected runtime, while PromptForge sandboxes chunks to string, table, and math, so neither server will flag `os` or `io` usage as unavailable. The documented levers are `diagnostics.disable` and custom `workspace.library` stubs; whether built-in stdlib definitions can be subtracted is not verified until prototyped. Likelihood that this needs a custom library stub: likely. Confidence: medium, pending a prototype.

## No browser DAP client exists, so the debugger stays custom

The survey confirms the earlier plan to hand-roll the line-level debugger. No maintained browser-ready DAP client library exists; `@vscode/debugprotocol` (MIT) is types only. The protocol client itself is small (about 300 lines: sequence counter, pending-request map, deframing, event dispatch), and the real cost is the UI, which is fully hand-rolled for CodeMirror either way: a breakpoint gutter, a current-line decoration, and dockview panels for variables and stack. Prior art for DAP-over-WebSocket exists in CodinGame's monaco-vscode-api (`debugServer.ts`) and in the transport shapes of Zed's and Helix's DAP crates, both of which reuse the LSP framing. If a full DAP adapter is ever built for external editors, the `dap-types` crate (MIT or Apache-2.0) is the legal foundation. The scoped plan stands: mlua global line hooks, executor parked on a condvar, intent-level messages over the existing WebSocket, one to two weeks. Confidence: high, verified against the mlua 0.12.1 sources in the local cargo registry.

## Risks concentrate in a young client, a stale type crate, and an unverified sandbox mismatch

- The official CM6 client is young (first release July 2025) and its author notes limited real-world battle-testing. Mitigation: the relay boundary makes it swappable; option 2 is the standing fallback.
- `lsp-types` has not released since June 2024. Mitigation: pin it and hand-write serde newtypes for spec gaps; the spec is stable.
- LuaLS's fallback-scope behavior with virtual (non-file) URIs is not verified. Mitigation: prototype with real fence documents in week one.
- Whether either Lua server's stdlib definitions can be subtracted to match the sandbox is not verified. Mitigation: custom `workspace.library` stub; worst case, tolerate the false negatives.
- This report is web-based recon, not prototyping. Every license was verified against its LICENSE file, but no code was compiled or run.

## Next steps assign every recommendation an owner and a first action

- `workshop-server`: build the WS-to-stdio relay with one language server (LuaLS) behind a feature flag. Next step: spawn LuaLS and round-trip `initialize` through the relay.
- `workshop-ui`: integrate `@codemirror/lsp-client` against the relay for one language. Next step: diagnostics rendering in the lint panel for a Lua file.
- `promptforge` family: wrap `promptforge-parser` in an `async-lsp` server exposing PromptForge diagnostics. Next step: serve `textDocument/publishDiagnostics` for one open prompt file in-process.
- `promptforge-lua`: prototype the mlua global line hook parking on a condvar. Next step: stop at a breakpoint line in a unit test.
- Product decision (owner: project lead): confirm third-party language support is a pillar before week two's work begins; if it is not, option 4 (parser diagnostics only) delivers the prompt-editing value at a fraction of the cost.

## Sources

Full evidence with per-claim URLs is held in five research documents dated 2026-09-17: the Zed recon, the Helix recon, the Lua language-server survey, the Rust client crate survey, and the webview integration survey. The two most load-bearing claims were independently re-verified on 2026-09-17 against npmjs.com/package/@codemirror/lsp-client (version 6.3.0, MIT) and crates.io/crates/async-lsp (version 0.2.4, MIT or Apache-2.0). Primary repositories: github.com/zed-industries/zed, github.com/helix-editor/helix, github.com/LuaLS/lua-language-server, github.com/EmmyLuaLs/emmylua-analyzer-rust, github.com/oxalica/async-lsp, github.com/gluon-lang/lsp-types, and the LSP 3.17 specification at microsoft.github.io/language-server-protocol.

*2026-09-17 15:55 - kimi-k3*
