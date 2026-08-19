# Agentic IDE research session (reduced)

*2026-07-31 15:16 - transcript 55139d32-0ef4-41d3-9429-6752b4796749*



## Prompts



**[p2]** I am leaning Tauri but before I do that how popular is it, and what software stack does VSCode/Cursor use

**[p7]** Listen up, here's the problem. Every time I hear React, I think about bloated UIs that are clumsy, they're over-engineered, they're not lean. Am I wrong?

**[p8]** I dont mean file size lean, I mean API-lean, call-chain-lean, etc

**[p10]** Here's what I need: Menubar, project treeview, editor tabs, terminal panel, chat tabs, everything that VSCode has high level interface components (what did I miss?)

**[p11]** shell plus global search and is this going to be able to open and edit files? and add folders to the workspace?

**[p12]** I am building this in a separate repo from @promptforge but eventually I want to put all the crates together will that be a problem?

**[p17]** since we are merging later should we use promptforge- as the prefix here?

**[p18]** I dont understand Browser panel. Is this for the editor? or is this for a full-blown browser experience connecting to the internet and surfing?

**[p20]** promptforge-core already exists in the other repo

**[p21]** I need the full browser and eventually the LLM will need to be able to drive it

**[p22]** Rename it to vibbi

**[p25]** del,ete the dup. NO _trash. DELETE

**[p30]** [troubleshooting: new window showed black then "can't reach this page", with an extra tied window; later resolved]

**[p32]** Question, what about the chat window? What about the panel that has the window where I can talk to the agent, where it's got the little chat box at the bottom? What happened to that?

**[p33]** You can just use a gateway, I'll just point you at it, like you just have the URL and the API keys in the environment for Anthropic, and then, but this panel, it's gonna be Rich Text, is it gonna format Markdown? I want it to look, I want the whole app to look just like cursor. Sponsor sub-agents, sponsor sub-agents search the web for people that have configured this tawdry to, to look like cursor, to like, define the style sheet, get, find out what fonts they use, get everything.

**[p35]** no stay in plan mode

**[p36]** I did not say run the plan I said apply the vibe file to the plan and contextr

**[p37]** api key is in environment, and hardcode the url from here @wg21-paperflow/SERVICES.toml

**[p40]** spawn subagents search the web for other projects or libraries that have the components we need. specifically displaying streaming markdown, initeracting with the model, etc

**[p42]** can we make control+ and control- work to adjust the zoom of the entire UI?

**[p43]** spawn subagents search the web 1 or 2 subagents for best practices for plan items, 3 to 4 subagents searching for missing features from vscode and if there are already existing components or solutions we can use

**[p44]** work it all into the plan, spawn 8 subagents find more toos, libraries, guidance to make this great

**[p45]** [bug: browser had no UI entry except the command palette, and when opened the window was disconnected from its tab]

**[p46]** Okay, that's working better, but the, the browser panel isn't affected by the zoom. Like, when I zoom, the, the UI around it gets bigger and smaller, but the brows the content of the browser doesn't. I don't know if that was intended. That's number one. Number two, the panel, the, like the tree panel. It's not, you can't move the divider. Like, n Is that, there's no divider there. And then the chat, like I wanted three panels. I want three vertical panels. I want the tree on the left, like normal, and then I want, in the middle, I want a frame that can hold my documents, multi-tab, and then on the right, I wanna have the chat panel that holds my chats, but I wanna be able to have more than one chat. I want it to be like cursor. You know what I mean? I want it to be like cursor. Let me give you a screenshot. I want it to be like cursor. Spawn some agents, go on the internet, and look to see if you can find like a description of cursors ui or v s codes ui. Just, let's, let's put together like a document that explains all the UI features. I'm gonna show you, I'm gonna paste.

**[p49]** For now, until further notice, the overriding prime directive, all caps prime directive, is copy cursor. When in doubt, look at the UI of cursor, and that's what I want. And you can look at Visual Studio Code as a secondary backup, but I want it to look and feel like cursor. I want the fonts to be like cursor. I want every little UI element to be like cursor. I want the icons to look like cursor. I want the layouts to look like cursor. Every time you're gonna do a commit, every time you're gonna do a feature Do a first look at, figure out how Cursor does it, and, and of course, Cursor's based on VS Code, so ninety-nine percent of it's gonna be looking at VS Code. But I want it to s it's gonna sub-agents, do all that research if you need to, and I want you to put together a master report, like a master document that explains The rules, like everything needs to be all dividers need to be movable, all the windows need to be dockable, right? And I want this code I want you to make sure you refactor the code at every step to be nice and organized, single concern in a file. I don't want any drift, I don't want to accumulate any technical debt.

**[p57]** Can we add a couple of slices which refactor particular subsets of the existing code to be compliant? including redteam/coreview

**[p60]** It looks pretety good but this vertical button strip with the treee,search,debug,etc... shouldn't that be on top of the tree horizontally not a panel on the side?

**[p63]** parity polish then phase 1 editor

**[p64]** [bugs: dragging any window tab gives a no-can-do icon; there is no "New Agent" button]

**[p66]** yes match the wording

**[p67]** [bugs: launch opens a phantom "prompt-compression-research.md" tab with no contents; shrinking the project panel pushes button-bar buttons offscreen; opening a file from the tree view put the tab in the treeview's panel and broke the layout; File menu missing Close, app window-locked]

**[p68]** [bug: no keyboard shortcuts for opening menus (opening, not selecting menu items)]

**[p72]** [bugs: New File appeared to do nothing (only a message); right-click delete made the file disappear from the tree]

**[p73]** [bug: right-clicking the last file in the list pops the menu partially offscreen, delete button inaccessible]

**[p77]** [bug: all terminals failed to acquire a shell; later fixed]

**[p79]** [bug: a browser tab button in the treeview toolbar replaced the treeview with the browser; controls gone, softlocked]

**[p80]** is there a menu and key for opening the browser?

**[p81]** ctrl+SHIFT+B works in cursor

**[p83]** is markdown preview on the todo list?

**[p84]** I was thinking it could be a toggle on the file

**[p87]** Keep going and dont stop unless you actually need me, or if something turned out significantly differenet than it should have.

**[p95]** [bug: clicking a .rs file popped an ugly window and an error]

**[p96]** [bug: markdown preview doesn't show images]

**[p97]** the image is local. also, I thought the preview was just an html? the markdown preview is just converting markdown to html or no? the image is not scaling to the width of the window, instead it is causing the horizontal scrollbar to show

**[p99]** do we want XML tags in markdown to render?

**[p100]** github doesn't show xml tags

**[p102]** lets keep the xml visible

**[p103]** but lets hide HTML comments:

**[p104]** This has YAML at the top:

**[p105]** that was github

**[p106]** do we need a more robust YAML parser that handles escapes, and is proven robust/secure?

**[p107]** we can worry about it later. keep executing on whats left

**[p109]** you should not have stopped

**[p113]** I want to defer all the AI/MCP related stuff and I want to finish everything needed to bring it in parity with VS Code. adjust the roadmap.

## Plans

### Rust Tauri Editor Substrate

*Build a polished, Windows-first desktop editor substrate in Rust using Tauri v2, with a CodeMirror 6 code editor, a Dockview-based IDE windowing/docking shell, and an embedded browser panel. No agent layer.*

This is a substrate to build polished UI on, not an agent product.

Decisions and rationale:
- Frontend framework defaulted to React for the best-documented Dockview integration; swappable for Svelte/Solid/vanilla in step 1 before code accretes.
- Browser panel: ship an `<iframe>` web panel first (simple, in-DOM); escalate to a native WebView2 child webview only if needed, because iframes are blocked by some sites (X-Frame-Options/CSP) while the native webview avoids that.
- Windows-only for now by choice; the architecture keeps cross-platform additive (macOS/Linux deferred until the Windows substrate is solid).

### Vibbi Chat Panel

*Add the missing chat panel to vibbi: a dockable chat pane (transcript + bottom input) wired to a Rust-side LLM provider client with streaming over Tauri events, the API key held in the OS credential store, conversational now with agentic tool-use deferred.*

Defaults chosen (decision rationale):
- Provider abstracted over Anthropic (Claude) and OpenAI, selectable in settings; default Anthropic; model configurable.
- The LLM call happens in Rust, never the webview - the API key stays out of the frontend and streaming is delivered via Tauri events, matching the existing architecture.
- The API key is stored in the OS credential store (Windows Credential Manager via `keyring`), not in plaintext settings JSON; include a clear error path if the keyring is unavailable rather than falling back to plaintext.
- Scope now is conversational streaming chat; agentic tool-use (the model calling vibbi's fs/terminal/browser commands) is the next milestone, not this one.
- The chat panel runs in the trusted `main` webview with full IPC access - it is app UI, unlike the isolated `browser:*` webviews.

Rejected alternative: merging the chat onto the `promptforge` agent engine (not chosen now).

### Vibbi Chat Best-Practices Upgrade

*Upgrade the vibbi chat panel to the researched best practices: Shiki (VS Code engine) code highlighting in the Anysphere theme, live incremental streaming-Markdown rendering via streaming-markdown (smd) with partial-syntax buffering, stick-to-bottom scrolling with user-scroll override, and security hardening (DOMPurify pin + a real Tauri CSP).*

Motivation (grounded in current code): Lezer themes do not reproduce the VS Code/Cursor look; the in-flight assistant turn rendered as escaped plain text and only became Markdown on complete; `security.csp` was `null`.

Decisions (each with a falsifier):
- Use `streaming-markdown` (smd) as the incremental renderer, not `solid-streamdown` or a markdown-it+remend rewrite. The panel is imperative Dockview DOM, so smd's framework-agnostic, append-only DOM renderer fits directly and avoids the re-`innerHTML` mXSS class (it builds nodes, never re-injects HTML strings). Falsifier: the chat panel is rewritten as a Solid component.
- Shiki for code highlighting, replacing CodeMirror/Lezer in the transcript: it uses VS Code's TextMate engine, so an Anysphere theme matches Cursor exactly; bundled offline (fine-grained core + JS engine + only-needed langs/theme), no CDN. Falsifier: the fine-grained bundle still bloats unacceptably.
- Keep DOMPurify as a safety net even under smd's append-only DOM, and keep `html: false` semantics (raw HTML in model output stays inert text). Falsifier: smd is proven to emit only a fixed safe node set.

Review principles (from the plan's vibe-review block):
- Model output stays sanitized: no raw HTML/script, links hardened (target=_blank, rel=noopener); a `<script>`/`onerror`/`javascript:` payload produces no live element or handler, asserted by tests including mid-stream.
- Incremental rendering never flashes broken markup: partial bold/italic/fences/links buffer until disambiguated; the finalized DOM equals an atomic render of the same text.
- Append-only DOM: no re-`innerHTML` of a growing sanitized string during streaming.
- A code block is highlighted once on fence close, not per token.
- Scroll: streaming follows the bottom only when the user is already there; a user scroll-up detaches and is not yanked back; the scroll-decision logic is pure and tested.
- The Tauri CSP blocks inline scripts and the app still boots; no capability/isolation change (browser:* webviews unaffected).
- Listeners/observers dispose race-safely on panel dispose; no leaks; no dead code; no secrets.

Process principles: build each slice in a subagent, commit, review in a fresh subagent, fix in a third; never run a git-mutating command concurrently with a file-writing subagent; stage before amend so a fix lands in its own commit; fix an old bug in its own commit.

Risk decision: CSP is the sharpest risk - start permissive-but-safe (block inline script; allow self + asset origin; allow inline style) and tighten later.

Deferred (out of scope): message virtualization for very long transcripts; branching for edit/regenerate; tool-call/"thinking" rendering for the deferred agentic step.

### Vibbi Roadmap

*A phased roadmap folding all research into buildable, vibe-run phases: Phase 0 = the chat best-practices upgrade + UI zoom; Phases 1-3 add editor/terminal/workbench parity, language intelligence + git, and the AI-native differentiators, on cross-cutting tracks for architecture, performance, accessibility, testing/CI, distribution, and theming.*

Principles and decision rationale:
- Performance first (gates everything else in Phase 1).
- MCP + LSP are the extensibility surface, not a bespoke plugin API (Lapce and Zed converge here). Falsifier: a required UI-extension use case neither covers. WASM plugins (Wasmtime + WIT, Zed's model) only after MCP/LSP prove insufficient.
- Agentic loop: tool-calling with human-in-the-loop (`interrupt -> approve/edit/reject -> resume`), edit checkpoints/rollback, sandbox-first (the shell boundary is not checkpointable).
- `git2` now, behind a trait; `gitoxide` read-paths later. Falsifier: the C toolchain breaks the Windows-first build badly enough to force pure-Rust now.
- Shiki for theme fidelity + Lezer for interactivity (run both). Falsifier: the dual-highlighter cost is too high.
- `nucleo` (Rust) for large fuzzy sets; `fuzzysort` in-UI for tiny lists. Falsifier: IPC latency makes the Rust path feel slow for the palette.
- Theming: import VS Code/TextMate themes via Shiki and map the theme's `colors` onto the design-token CSS variables ("bring your own theme" reskins the whole app); keep Lezer for interactive features.

Cross-cutting architecture principles (verbatim):
- One typed error seam (`thiserror` + serde-tagged) across the Rust IPC boundary; never leak a dependency's error type; per-variant `#[non_exhaustive]`.
- Pin `tauri-specta` with `=` and isolate it plus the community `smd`/`dockview`/`solid-dockview` deps behind thin modules.
- signals vs `createStore`/`reconcile` discipline; feature folders; a service/command-registry layer; keep imperative Dockview panels coherent with reactive state via shared stores + `onDidVisibilityChange`.
- Treat the IPC bridge like a network call: minimize payloads; stream or use a custom protocol for bytes.

Rejected scope (honest out-of-scope): VS Code extension-API compatibility; a full multi-language debugger matching VS Code's breadth; full remote/SSH dev; a general notebook platform with kernel management.

Sequencing rationale: the AI-native items (MCP tool loop, inline diff/apply, checkpoints/HITL, browser-as-tool) are the highest-leverage differentiators and can be pulled forward if AI is the priority over parity.

### Vibbi Cursor-like Workbench

*Rework vibbi's shell into a Cursor-like workbench: Explorer, editor, and chat become resizable Dockview regions (real sashes), the right pane holds multiple chat tabs, and the embedded browser page zooms with the UI.*

Target layout: the Activity Bar stays as chrome to the left of the dock; the sidebar, editor, and chat are all Dockview panels separated by draggable sashes; the chat group holds one tab per conversation.

Key design decisions:
- Each chat panel derives `conversationId` from its panel id, so tabs are independent conversations (the Rust chat commands already take a `conversationId`, so the backend supports many). The selected model stays global (shared) for now.
- Keep the Activity Bar; its buttons set `activeView` and reveal/toggle the side bar dock panel; `Ctrl+B` toggles the side bar panel's presence, behaving like VS Code, with width remembered across toggles.
- Bump a layout schema version; ignore legacy/mismatched persisted layouts and rebuild defaults once (old layouts reference removed panels) - the version gate must reject legacy layouts rather than crash on them.
- Browser: mirror the UI zoom onto the child webview (`webview.set_zoom`) so page content scales with the chrome.
- Dockview remains the single layout owner; the new panels serialize with the existing debounced layout persistence.
- Chat transcripts are still not persisted (only the panel/layout); restored chat tabs start empty. Noted as a follow-up, not in scope.
