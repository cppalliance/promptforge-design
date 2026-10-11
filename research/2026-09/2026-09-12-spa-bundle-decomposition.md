# Workshop SPA: How to Decompose an SPA Bundle

Report type: evaluation / review. It judges Workshop SPA against 6 popular
codebases sharing vanilla TypeScript SPA architecture, and prescribes idioms to adopt, in payoff order.

## Executive summary

The subject ships every feature in one monolithic bundle and styles it with unscoped CSS - the two deficits that every reference solves and the subject does not. Its strengths - the cross-language wire contract, the DisposableStore lifecycle tree, and the server-owned state discipline - match or beat the field. Adopting lazy panel loading and CSS colocation alone would retire the two highest-severity deficits at medium-to-small cost.

### Key findings

1. **Dynamic import registry for lazy panel loading (Home Assistant, corroborated by VS Code, Theia, JupyterLab).** Map panel names to `() => import(...)` thunks; load each chunk on first route activation. Retires the monolithic bundle without requiring a DI framework. Confidence: high.
2. **CSS colocation with project-prefix namespace (VS Code, Theia, JupyterLab, vanilla-typescript-spa).** Place each component's CSS beside its TypeScript, import it as a side-effect, and prefix all classes with `ws-`. Eliminates collision risk without CSS modules. Confidence: high.
3. **Phased contribution lifecycle for deferred instantiation (VS Code, JupyterLab).** Gate heavy features behind a post-restore phase so they parse but do not execute until the shell is interactive. Runtime code splitting without bundle splitting. Confidence: high.
4. **Workshop directory decomposition by concern subdirectory (Theia, JupyterLab, Home Assistant).** Split the flat 15-file workshop/ into editor/, agent/, tree/, and layout/ subdirectories. Pure file-move refactor; no code changes. Confidence: high.
5. **Part/Widget base class for panel lifecycle (VS Code, Theia, vanilla-typescript-spa).** Define a base Panel class with create/layout/dispose contract that all dockview panels extend, standardizing the imperative construction pattern. Confidence: high.
6. **HTML template files with build-time string import (vanilla-typescript-spa, ft_transcendence).** Move DOM structure into .html files imported as strings at build time, separating markup from TypeScript. Confidence: medium.
7. **Content-hashed asset filenames (Home Assistant).** Use esbuild's `[name]-[hash]` output naming and serve hashed assets with long-lived cache headers. Confidence: high.
8. **Centralized store replacing module-scope state (vanilla-typescript-spa).** Move scattered module-level Maps/Sets into a single observable store built on the existing Emitter pattern. Confidence: medium.
9. **CSS design tokens via custom properties (JupyterLab, Home Assistant).** Extract all color/size values into `--ws-` custom properties, making themes swappable and visual values greppable. Confidence: medium.
10. **Result<T> monad for typed error propagation (ft_transcendence).** Replace stringly-typed errors with a Result type plus an ErrorCatalog, making error handling explicit and composable. Confidence: medium.

## Method

Workshop SPA was profiled through nine architectural lenses (module decomposition, state ownership, boundaries, error shape, resource lifecycle, testing, comment policy, build/delivery, messes) to produce a fingerprint with 8 named deficits and 5 strengths. A field survey searched for open-source projects sharing the subject's vanilla TypeScript SPA stack and verified each candidate's technique against its source. Six references were shortlisted and dived in parallel at pinned commits. Each dive applied the same nine lenses and extracted idioms with citations. A provenance examination walked each cited file's commit history for AI markers and, where found, compared the HEAD form against the last pre-AI commit to determine whether the cited mechanism held up, tightened, or degraded. Idioms were clustered by convergence, mapped to deficits, and ranked by payoff. Citations were verified against the pinned clones.

## Reference projects and provenance

| Reference | Popularity | Why chosen | License | Provenance of cited idioms |
|---|---|---|---|---|
| VS Code Workbench | 190k stars | Closest architecture match; subject's Disposable/Emitter ancestor | MIT | 8 strong human signal, 1 explicit AI marker (CSS file; colocation mechanism held up against pre-AI form) |
| Eclipse Theia | 21.6k stars | InversifyJS DI + Lumino widgets; ContributionProvider extension model | EPL-2.0 / GPL-2.0 w/ Classpath | 5 strong human signal, 0 AI markers |
| JupyterLab | 15.3k stars | Token-based DI; library/extension package split; CSS design tokens | BSD-3-Clause | 3 strong human signal, 4 explicit AI marker (all held up against pre-AI forms), 1 AI-originated (dockpanel.ts) |
| Home Assistant Frontend | 5.5k stars | Lit SPA with dynamic import code splitting and Shadow DOM scoping | Apache-2.0 | 4 strong human signal, 5 explicit AI marker (4 held up, 1 AI-originated: stale build recovery) |
| vanilla-typescript-spa | 4 stars | Small vanilla TS + Custom Elements + Shadow DOM; readable whole | MIT | 6 strong human signal, 0 AI markers |
| ft_transcendence | No proxy | Vanilla TS SPA + DDD backend; Result<T> error pattern | unknown | 13 strong human signal, 0 AI markers |

## Baseline: where the subject stands

Workshop SPA is a server-delivered single-page application - one `index.html` loads a single esbuild-bundled `app.js` plus `app.css`, served by a Rust backend via rust-embed. The codebase is ~69 TypeScript and CSS source files (~399 KB) organized into three clean layers: `base/` (lifecycle primitives), `services/` (DOM-free state and wire), and `ui/` (views). Two WebSocket connections carry server state; a typed `protocol.ts` cross-cited with `protocol.rs` pins the wire format from both sides with a shared JSON fixture.

The subject's strengths are genuine: the cross-language contract test catches wire drift before it ships, the DisposableStore lifecycle tree provides deterministic cleanup with a test-time leak checker, server-owned state discipline means the SPA never derives readiness or selection locally, the comment policy is the densest and most architectural of any reference surveyed, and services are cleanly separated from views with no DOM imports crossing the boundary.

The deficits are structural. The single bundle (deficit 2) loads CodeMirror, Shiki, Tiptap, and speech capture at boot whether or not the user opens those panels. CSS (deficit 4) relies on BEM-ish naming convention with no scoping mechanism. The `workshop/` directory (deficit 3) mixes 15 files spanning editor, agent, tree, layout, and widget concerns in one flat folder. `window-menu.ts` (deficit 1) is a 25 KB god-object building five HTML menus imperatively. Views construct DOM via createElement chains (deficit 5). Module-level Maps and Sets in `zones.ts` and `workshop-panel.ts` (deficit 6) survive panel re-creation but are invisible to services. Errors surface as strings (deficit 7). Every asset is served with `no-cache` (deficit 8).

## Detailed findings, ranked by payoff

### Finding 1: Dynamic import registry for lazy panel loading

Four of six references solve the monolithic-bundle problem. Home Assistant's [`partial-panel-resolver.ts`](https://github.com/home-assistant/frontend/blob/6dcca891855c95af3889cc6a6cfe9dd4c617b83e/src/layouts/partial-panel-resolver.ts#L23-L81) maintains a typed record mapping panel names to `() => import(...)` thunks. Route changes trigger the import; the panel element is created only after its chunk loads. A `waitForReady` flag plus per-panel timeout defers the loading-screen removal for data-dependent panels. VS Code achieves a similar effect through [`WorkbenchPhase`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/workbench/common/contributions.ts) gating. Theia uses per-package [`ContainerModule`](https://github.com/eclipse-theia/theia/blob/69805e3299deb477431e6d1e527bd7ebada5726a/packages/navigator/src/browser/navigator-frontend-module.ts) exports as the splitting unit. JupyterLab splits features into library/extension package pairs.

In the subject, CodeMirror, Shiki, Tiptap, and speech capture all pay their parse and init cost at boot. Wrapping each heavy panel in a dynamic import thunk and loading it on first activation would cut initial bundle size to the shell and services. esbuild supports `import()` splitting natively when `splitting: true` and `format: 'esm'` are set.

The Home Assistant form is the most adoptable: it requires no DI framework, just a typed record and dynamic imports. The subject's dockview panel creation already has a natural hook point. Provenance: Home Assistant's lazy-load mechanism held up against its pre-AI form; VS Code's phased lifecycle is strong human signal. Confidence: high - 4/6 references converge; the dynamic import form requires only build config and a panel registry.

### Finding 2: CSS colocation with project-prefix namespace

Four references solve CSS isolation without CSS modules. VS Code places each widget's CSS alongside its TypeScript - [`list.css`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/base/browser/ui/list/list.css) sits beside `listWidget.ts`, imported as a side-effect. Theia reinforces this with a `.theia-` class prefix on all components and aggregates package CSS through a single [`index.css`](https://github.com/eclipse-theia/theia/blob/69805e3299deb477431e6d1e527bd7ebada5726a/packages/core/src/browser/style/index.css) using `@import`, with [explicit CSS ordering](https://github.com/eclipse-theia/theia/blob/69805e3299deb477431e6d1e527bd7ebada5726a/packages/core/src/browser/frontend-application-module.ts#L18-L25) in the module file. JupyterLab uses `--jp-` design tokens. vanilla-typescript-spa uses Shadow DOM via a decorator.

The subject's CSS files use BEM-ish class names with no enforcement. Adopting a `.ws-` prefix on all classes and moving each component's CSS beside its TypeScript file (one `.css` per component, imported by the `.ts`) provides namespace isolation and makes ownership visible in the file tree. Combined with finding 9 (design tokens), this retires deficit 4.

Provenance: VS Code's `sidebarpart.css` carries an AI marker (Copilot added visual polish), but the colocation mechanism is unchanged from its pre-AI form at `12f4872e2dd3`. All other cited files are strong human signal. Confidence: high - 4/6 references solve this the same way; the change is file reorganization and class renaming.

### Finding 3: Phased contribution lifecycle for deferred instantiation

VS Code's [`WorkbenchPhase`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/workbench/common/contributions.ts) enum gates when contributions instantiate: `BlockStartup`, `BlockRestore`, `AfterRestored`, `Eventually`. Features not needed at boot register as `Eventually` (2-5 seconds after restore). Combined with [`InstantiationType.Delayed`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/platform/instantiation/common/extensions.ts) on service registrations, heavy features do not execute until their phase fires - runtime code splitting without bundle splitting.

Even if the subject adopts dynamic imports (finding 1), a phased lifecycle complements it: the bundle can carry everything, but speech capture, the take registry, and the editor surface defer their wiring until the shell is interactive. The subject's `main.ts` already sequences service construction - adding phase gates formalizes what is currently implicit ordering.

Provenance: both cited files are strong human signal (maintained by named contributors since 2016-2020). Confidence: high - VS Code's own bundle is monolithic yet boots fast using this pattern.

### Finding 4: Workshop directory decomposition by concern subdirectory

Theia's [`core/src/browser/`](https://github.com/eclipse-theia/theia/tree/69805e3299deb477431e6d1e527bd7ebada5726a/packages/core/src/browser) splits into 23 subdirectories by concern: `shell/`, `widgets/`, `tree/`, `menu/`, `keyboard/`, `preferences/`, `style/`, `dialogs/`. Home Assistant's [`panels/`](https://github.com/home-assistant/frontend/tree/6dcca891855c95af3889cc6a6cfe9dd4c617b83e/src/panels) uses one directory per route. JupyterLab uses separate npm packages per feature.

The subject's flat `workshop/` directory mixes 15 files spanning editor concerns (editor-surface, editor-panel, editor-dialog), agent concerns (agent-panel), tree concerns (workshop-panel), layout (zones, layout-persistence, panel-types, shortcuts), and shared widgets (typeahead-popup, mention-chip, icons). Splitting into `workshop/editor/`, `workshop/agent/`, `workshop/tree/`, `workshop/layout/` groups files by the concern they serve and makes role decidable from path.

Provenance: all cited directories are strong human signal. Confidence: high - pure file-move refactor with no code changes; every reference with 10+ features groups by concern.

### Finding 5: Part/Widget base class for panel lifecycle

VS Code's [`Part`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/workbench/browser/part.ts) abstract class provides a standard lifecycle for workbench regions: `create(parent)` builds the DOM, `layout(dimension)` sizes it, and the class owns title, content, and footer areas. [`Composite`](https://github.com/microsoft/vscode/blob/3addbda66f9e80c3ed1b943822ab823bb6747b02/src/vs/workbench/browser/composite.ts) adds focus tracking and action bars. Theia's [`BaseWidget`](https://github.com/eclipse-theia/theia/blob/69805e3299deb477431e6d1e527bd7ebada5726a/packages/core/src/browser/widgets/widget.ts#L100-L160) adds a message protocol with per-phase DisposableCollections.

The subject already has DisposableStore. Adding a base Panel class that every dockview panel extends would standardize how panels build their DOM: `createContent(container)` for structure, `layoutContent(dimension)` for sizing, `dispose()` for cleanup. The ad-hoc createElement chains in agent-panel, editor-panel, and workshop-panel would follow a uniform contract. vanilla-typescript-spa's `@CustomElement` decorator shows the same idea at smaller scale.

Provenance: all cited files are strong human signal (VS Code part.ts, composite.ts, component.ts from 2018-2019; Theia widget.ts from 2017). Confidence: high - the subject already has the disposable infrastructure; the base class is an incremental step.

### Finding 6: HTML template files with build-time string import

vanilla-typescript-spa imports `.html` and `.css` files as strings via Vite's `?raw` suffix at [`src/pages/home/index.ts:2-3`](https://github.com/flaviodelgrosso/vanilla-typescript-spa/blob/bdffb75becb16d51f813e31abd8b32d6a8b37676/src/pages/home/index.ts#L2-L3), then injects them into a Custom Element's shadow root. ft_transcendence fetches HTML templates at runtime via a 7-line mustache replacer at [`frontend/src/core/view.ts:3-9`](https://github.com/bonissanti/42SP_15_ft_transcendence/blob/e5a311a2381458352f9b204e3bf2f88c6cd89e6a/frontend/src/core/view.ts#L3-L9).

For the subject's menus, templates would separate the static structure of each menu's HTML from the dynamic row-building logic, cutting `window-menu.ts` from 660 lines of interleaved createElement and event-handler code into a template + a focused wiring module. esbuild supports text imports via the `loader` option (`{ '.html': 'text' }`).

Provenance: both cited files are strong human signal. Confidence: medium - the pattern is sound for static structure, but the subject's menus have significant dynamic content (model catalog rebuilds, profile list updates) that may resist pure template approaches.

### Finding 7: Content-hashed asset filenames

Home Assistant uses rspack's content-hashing pipeline to produce filenames like `app-[contenthash].js`, served with long-lived cache headers. The manifest maps entrypoint names to hashed URLs.

The subject serves every asset with `Cache-Control: no-cache`, forcing revalidation on every page load even when the bundle has not changed between server restarts. esbuild supports content hashing natively via `entryNames: '[name]-[hash]'`. The Rust server needs only a manifest reader (a small JSON file mapping logical names to hashed filenames) to resolve the correct asset URL in `index.html`.

Provenance: Home Assistant build pipeline is strong human signal (rspack config). Confidence: high - esbuild supports this out of the box; the server-side change is a manifest lookup.

### Finding 8: Centralized store replacing module-scope state

vanilla-typescript-spa wraps a plain object in a `Proxy` whose `set` trap dispatches named `CustomEvent`s on `window` - the entire reactive layer is [30 lines](https://github.com/flaviodelgrosso/vanilla-typescript-spa/blob/bdffb75becb16d51f813e31abd8b32d6a8b37676/src/store/index.ts).

The subject's `zones.ts` and `workshop-panel.ts` hold `Map`s and `Set`s at module scope - `zoneGroups`, `zoneOverrides`, `expandedPaths`, `listingCache`. These survive panel re-creation but are invisible to the service layer and untestable without importing the module. Moving this state into a service-layer store (using the existing Emitter pattern rather than Proxy) makes it observable, injectable, and testable. The store need not be a single atom - one per concern (zone state, tree state) is sufficient.

Provenance: strong human signal. Confidence: medium - one reference only; the subject's existing Emitter pattern could absorb this without introducing Proxy, making adoption even cheaper.

### Finding 9: CSS design tokens via custom properties

JupyterLab defines ~273 `--jp-` CSS custom properties in a central [`variables.css`](https://github.com/jupyterlab/jupyterlab/blob/cd7f6133a5809c83ebbede50673b06aa2fd0c311/packages/theme-light-extension/style/variables.css#L1-L50): elevation, border colors, font sizes, content fonts, UI fonts, code fonts. All component CSS references these tokens exclusively. Home Assistant does the same with `--ha-` and `--primary-*` properties across Shadow DOM boundaries.

The subject has no design token system. Colors and sizes are scattered across CSS files. A `--ws-` variable set would centralize visual values, make themes swappable, and make every visual decision greppable. Combined with finding 2 (CSS colocation), this completes the subject's CSS architecture.

Provenance: JupyterLab variables.css is strong human signal. Home Assistant Lit static styles are strong human signal. Confidence: medium - two references confirm the approach; extraction is mechanical but touches every CSS file.

### Finding 10: Result<T> monad for typed error propagation

ft_transcendence's backend uses [`Result<T>`](https://github.com/bonissanti/42SP_15_ft_transcendence/blob/e5a311a2381458352f9b204e3bf2f88c6cd89e6a/game-service/src/Shared/Utils/Result.ts) instead of throwing. `Result.Success(msg)`, `Result.SuccessWithData<T>(msg, data)`, `Result.Failure(msg, errorType)`. Combined with [`ErrorCatalog`](https://github.com/bonissanti/42SP_15_ft_transcendence/blob/e5a311a2381458352f9b204e3bf2f88c6cd89e6a/game-service/src/Shared/Errors/ErrorCatalog.ts) (a static catalog of all domain errors with codes and messages), this eliminates stringly-typed errors.

The subject surfaces errors as strings or HTTP status codes. A `Result<T, E>` type on the TS side would make error handling explicit: services return `Result.ok(value)` or `Result.err(catalogEntry)`, and views pattern-match on the result. Adoptable incrementally - start with the workspace-api boundary where fetch errors currently throw.

Provenance: all cited files are strong human signal (single maintainer, Bruno Onissanti, throughout). Confidence: medium - one reference only; the pattern is well-established in functional programming but requires buy-in across the service layer.

## Provenance

AI markers appear in three of six references. In VS Code, two Copilot-authored commits touched `sidebarpart.css` (border-radius scoping and activity bar indicator styling). The colocation mechanism - a `.css` file beside its `.ts` owner, imported as a side-effect - is present unchanged at the pre-AI commit `12f4872e2dd3`; the Copilot commits added visual polish only. In JupyterLab, AI-marked commits touched `filebrowser/src/tokens.ts`, `filebrowser-extension/src/index.ts`, `filebrowser/style/base.css`, and `application/src/shell.ts`; in every case the cited mechanism (Token DI, plugin wiring, CSS token consumption, named-area layout) is present and unchanged at the pre-AI form. One JupyterLab file - `dockpanel.ts` (optimized resize with freeze/unfreeze) - is AI-originated with no pre-AI form; this idiom was noted-not-scheduled as it maps to no listed deficit. In Home Assistant, the lazy-load registry, state atom, and panel visibility suspension all held up against their pre-AI forms. One Home Assistant idiom - stale build recovery (`recover-stale-build.ts`) - is AI-originated; it maps to no subject deficit and was noted-not-scheduled.

## Where the subject already matches or beats the references

The subject's cross-language wire contract (protocol.ts + protocol.rs + shared JSON fixture) is more rigorous than any reference; Home Assistant has no shared protocol file, ft_transcendence has diverging type definitions between frontend and backend, and Theia uses RPC proxying without a cross-language fixture. The DisposableStore lifecycle tree matches VS Code (its direct ancestor) and Theia; ft_transcendence and vanilla-typescript-spa have no cleanup pattern, and Home Assistant has only ad-hoc cleanup. Server-owned state discipline - the SPA never derives readiness, selection, or profile state locally - matches Home Assistant and exceeds ft_transcendence and vanilla-typescript-spa. The comment policy (file-level block comments explaining role, boundary, and invariants; inline why-comments cross-citing the Rust side) exceeds every reference surveyed. The clean service/view separation matches VS Code's platform/workbench split and Theia's common/browser split.

## Messes we should explicitly not copy

**VS Code:** `layout.ts` (2,663 lines) - god-object layout engine mixing grid management, zen mode, fullscreen, panel alignment, title bar, and editor layout. `workbench.common.main.ts` - 376-line import manifest with no feature flags. `contrib/chat/` (1,385 files) - single feature larger than most applications.

**Theia:** `common-frontend-contribution.ts` (134 KB) - registers commands, menus, keybindings, preferences, and colors for the entire core frontend in one file. `application-shell.ts` (97 KB) - shell layout manager with area management, widget tracking, drag-and-drop, and layout save/restore all in one class.

**JupyterLab:** `notebook-extension/src/index.ts` (169 KB) - dozens of plugin definitions packed into one file. `shell.ts` (87 KB) - layout manager with all areas in one class.

**Home Assistant:** HassElement mixin tower - 17 mixins composed via `reduceRight` with implicit ordering dependencies. 22 `createRenderRoot` overrides breaking Shadow DOM encapsulation.

**ft_transcendence:** `websockets.ts` (477 lines) - WebSocket server, lobby management, tournament bracket, and game history all in one file. Duplicated `Paddle`/`Ball` type definitions between frontend and backend with diverging shapes.

## Recommended execution order

1. **Split workshop/ into concern subdirectories** (finding 4). Pure file moves - editor/, agent/, tree/, layout/. Update import paths. Verify tests pass. This clears the ground for later per-concern work.
2. **CSS colocation + project prefix** (finding 2). Move each component's CSS beside its TypeScript, rename classes to `.ws-*`, update imports to side-effect imports. Verify visual correctness.
3. **Dynamic import registry for lazy panels** (finding 1). Enable esbuild splitting. Create a panel registry mapping panel IDs to dynamic import thunks. Update dockview panel creation to load chunks on demand. Verify each panel loads correctly.
4. **Phased contribution lifecycle** (finding 3). Add lifecycle phases to main.ts. Defer speech capture, take registry, and editor surface to post-restore. Verify boot time improvement.
5. **Part base class for panels** (finding 5). Define a base WorkshopPanel class with create/layout/dispose contract. Migrate panels one at a time, starting with the simplest (agent-panel). Verify each migration preserves behavior.
6. **HTML templates for menus** (finding 6). Extract window-menu.ts static structure into HTML template files. Wire dynamic content separately. Verify all five menus function correctly.
7. **Content-hashed asset filenames** (finding 7). Configure esbuild `entryNames: '[name]-[hash]'`. Add a manifest file. Update the Rust server to read the manifest and inject hashed URLs into index.html.
8. **Centralized store for zone/tree state** (finding 8). Create a ZoneStateService and TreeStateService using the Emitter pattern. Move module-scope Maps/Sets from zones.ts and workshop-panel.ts into these services. Wire views to subscribe.
9. **CSS design tokens** (finding 9). Extract all color/size literals into `--ws-*` custom properties in a central variables.css. Update all CSS files to reference tokens.
10. **Result<T> error type** (finding 10). Define Result<T, E> and an ErrorCatalog. Adopt in workspace-api.ts first, then propagate to other service boundaries.

## Refactor notes

Findings 1, 2, 3, 4, and 7 are pure structure changes - they do not alter runtime behavior. The test suite is the invariant: every step must pass `node --test` before commit. Finding 5 (base class) changes the class hierarchy but not behavior; each panel migration is a separate commit. Finding 6 (templates) changes how DOM is constructed but not what is constructed - visual diff is the verify step. Findings 8 and 10 change how state flows and errors propagate - these carry the highest regression risk and should be adopted incrementally, one module at a time.

Do-not-touch boundaries: `protocol.ts` and its Rust counterpart `protocol.rs` are load-bearing and correct. The shared JSON fixture `agent-frames.json` must not change. The DisposableStore lifecycle tree is correct and complete - findings build on it, not around it.

Per-step verify and commit: each numbered step above is one commit. Run the full test suite after each. Visual-verify CSS changes in the browser.

Stop condition: two consecutive test failures on one step stops the run for a re-plan.

## Sources

- VS Code Workbench: https://github.com/microsoft/vscode at `3addbda66f9e80c3ed1b943822ab823bb6747b02`, MIT, analyzed 2026-09-12. PRE_AI_SHA for sidebarpart.css: `12f4872e2dd3778ddba829f05fcf1b195ac7f21e`.
- Eclipse Theia: https://github.com/eclipse-theia/theia at `69805e3299deb477431e6d1e527bd7ebada5726a`, EPL-2.0 / GPL-2.0 w/ Classpath, analyzed 2026-09-12.
- JupyterLab: https://github.com/jupyterlab/jupyterlab at `cd7f6133a5809c83ebbede50673b06aa2fd0c311`, BSD-3-Clause, analyzed 2026-09-12. PRE_AI_SHAs: tokens.ts `b5b497bacb11c735aadf8ffc02d64e6696fe344f`, filebrowser-extension index.ts `6c10f87dec04b897e96c73b02a8699be8408bf0d`, base.css `9a8078600ee39710bc6bbad7ae37312d565bb974`, shell.ts `63e50d485c3e1bb3983312834e36a61b6441ac66`.
- Home Assistant Frontend: https://github.com/home-assistant/frontend at `6dcca891855c95af3889cc6a6cfe9dd4c617b83e`, Apache-2.0, analyzed 2026-09-12. PRE_AI_SHAs: partial-panel-resolver.ts `d3182da587c20ae372636c2433aacaa906305a4a`, hass-base-mixin.ts `e703750136cc6ebdd50e94258e46023f51bfe661`, connection-mixin.ts `9e7ddb3e5e1d3e9c23f8f2dedd71221f7068a61a`, home-assistant.ts `b72b6c77bf734f237cc89ee327f85dd45535e8a2`.
- vanilla-typescript-spa: https://github.com/flaviodelgrosso/vanilla-typescript-spa at `bdffb75becb16d51f813e31abd8b32d6a8b37676`, MIT, analyzed 2026-09-12.
- ft_transcendence: https://github.com/bonissanti/42SP_15_ft_transcendence at `e5a311a2381458352f9b204e3bf2f88c6cd89e6a`, unknown license, analyzed 2026-09-12.
- Subject profile: 2026-09-12. Field survey: 2026-09-12.

*2026-09-12 11:28 - claude-4.6-opus*
