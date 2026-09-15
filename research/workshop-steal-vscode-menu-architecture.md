# Workshop UI: How the VS Code Family Builds Menus, Keybindings, Quick Open, and SPA Messaging

Report type: evaluation / review. It judges the PromptForge Workshop UI against 7 open-source codebases in the VS Code family (the upstream, four forks, two from-scratch reimplementations), and prescribes the naming, file organization, registry mechanics, and messaging shape to adopt for the menu overhaul, in payoff order.

## Executive summary

The field has converged, and the Workshop should stop inventing: every project examined that builds a workbench menu system, whether by forking VS Code or rewriting it from zero, lands on the same six primitives with the same names. A command registry keyed by id. A menu model where a menu is a string id, a menu item names a command, and a submenu is a menu item whose payload is another menu id (so the title-bar buttons are just the children of a root `menubar` menu, generated, never hard-coded). A keybinding registry whose rules carry a `when` clause and whose displayed labels are looked up from the registry, never typed into the menu row. A context-key service with a small `when` expression language, where `when` hides, `precondition` disables, and `toggled` checks. A chord resolver that is a pure function returning "no match / more chords needed / found", with the shell owning the pending state and a status-bar message. And a quick-access registry keyed by prefix, where the command palette is nothing but the `>` provider. The two from-scratch reimplementations (Theia, OpenSumi) adopted VS Code's names and shapes deliberately; OpenSumi copied Theia's quick-open and VS Code's `MenuId` outright rather than design its own. That is the strongest convergence signal available.

The Workshop already matches the field on its foundations - `Emitter`/`Event`, `Disposable`/`DisposableStore`, a `CommandRegistry` of descriptors, per-feature `register()` functions returning disposables, upsert-safe registrations, and dynamic menus resolved at open time - so the adoption is a reshaping of three files, not a rewrite. The top finding, the one-declaration action (`registerAction2`'s shape: id, title, keybinding, menu placements, precondition in one object), removes three of the seven deficits at once and is what every fork uses to add its own menu rows without touching upstream files.

### Key findings

1. **One declaration registers command, menu placement, keybinding, and palette entry (VS Code `registerAction2`, used verbatim by Void, Positron, code-server, openvscode-server).** A single object fans out into all four registries and returns one disposable; features never touch a central menu file. Confidence: high.
2. **A submenu is a menu item whose payload is a menu id, and the menubar is the root menu's submenu list (VS Code `MenuId.MenubarMainMenu`, OpenSumi `registerMenubarItem`, Theia `MAIN_MENU_BAR` path).** Title-bar buttons are generated from the model; the popover renderer branches on "command item or submenu item" and recurses. Confidence: high.
3. **Shortcut hints are looked up from the keybinding registry at render time (`lookupKeybinding(id)?.getLabel()` in VS Code and Positron, `acceleratorFor` in Theia and OpenSumi).** The command descriptor carries no shortcut string. Confidence: high.
4. **Chords are a pure resolver returning `NoMatchingKb | MoreChordsNeeded | KbFound`; the shell keeps the pressed chords and posts a status message (VS Code, Theia, OpenSumi).** Keybindings are written as space-separated keystroke strings (`ctrl+m ctrl+o`) in Theia, OpenSumi, and VS Code's own extension manifest format. Confidence: high.
5. **Enablement and visibility are context keys evaluated by a `when` expression (`RawContextKey`, `ContextKeyExpr`, `ContextKeyService`) in all seven references.** Menus collect the keys their rows reference and re-evaluate only when one of those keys changes. Confidence: high.
6. **Quick access is a registry of providers keyed by prefix; the palette is the `>` provider listing enabled commands with their keybinding labels; `?` lists the prefixes (VS Code, Theia, OpenSumi).** The title-bar pill does nothing but `quickAccess.show()` (Positron, VS Code command center). Confidence: high.
7. **Registries are DOM-free and live below the widgets; widgets live in the UI layer and are lint-forbidden from being imported upward (VS Code `common`/`browser` split, Theia `common`/`browser` folders, OpenSumi `core-common`/`core-browser`).** Confidence: high.
8. **SPA-to-server messaging converges on one socket carrying multiplexed named channels, numeric request ids, a JS `Proxy` that turns a TypeScript service interface into RPC by method-name convention, and events as ref-counted subscriptions (VS Code IPC, Theia `RpcProxy`, OpenSumi `SumiConnection`, Void's request-id streaming).** Wire formats diverge; the shape does not. Noted, not scheduled for the menu plan. Confidence: medium.

## Method

Light run of the what-to-steal procedure. The subject was profiled from the working session rather than by a separate profiler (its menu, command, shortcut, and socket files had just been read in full). A surveyor verified 30+ candidates against source via the GitHub API and confirmed the shortlist covers the field's four organizational patterns (prefixed contrib fork, quilt patch series, upstream-tracking fork, DI reimplementation); one reimplementation (OpenSumi) was added as a convergence check. Seven divers read source through GitHub's web and raw endpoints at a pinned commit each, no clones, and wrote per-lens analyses with permalinks. Provenance dating and the independent citation check were skipped; every citation below is a permalink at the pinned commit as reported by its diver, not re-verified by a second pass.

## Reference projects

| Reference | Kind | Popularity | Why chosen | License |
|---|---|---|---|---|
| microsoft/vscode | upstream | 192.6k stars | The canonical naming and mechanics every fork inherits | MIT |
| eclipse-theia/theia | from-scratch reimplementation, browser SPA over WebSocket | 21.7k stars | Closest architectural match to the subject; shows which VS Code names a clean-room team chose to keep | EPL-2.0 / GPL-2.0 w/ CPE |
| opensumi/core | from-scratch reimplementation | 3.7k stars | Third implementation, used as a convergence check | MIT |
| voideditor/void | fork adding AI agent panel (archived 2026-06) | 28.8k stars | Cursor-alternative; shows how a fork adds `Ctrl+L`-style AI menu rows | Apache-2.0 |
| posit-dev/positron | large active fork adding workbench parts | 4.3k stars | Adds a new title-bar part with a command-center pill; fence-comment fork discipline | Elastic-2.0 |
| gitpod-io/openvscode-server | browser-served fork | 6.2k stars | Clean pinned copy of the server-to-browser IPC stack and the web menubar path | MIT |
| coder/code-server | quilt patch series over vendored VS Code | 79.3k stars | Shows the minimal shape a downstream uses to add one menu row and one RPC service | MIT |

## Baseline: where the subject stands

The Workshop UI is a plain-DOM TypeScript SPA bundled by esbuild, served by a Rust crate, shown in WebView2 or a browser. Layers run `base/` (Event, Disposable) -> `services/` (token registry, WebSocket client, model and workbench state) -> `ui/` feature directories, with `main.ts` as composition root. Its menu system is three files in `ui/menu/`: a `CommandRegistry` (Map of `{label, shortcut, run, enabled}`), a `MenuRegistry` (placements per menu id, plus dynamic providers), and a `MenuRenderer` that builds popovers under five buttons hard-coded in `index.html`. `ui/layout/shortcuts.ts` matches single-stroke Ctrl chords and dispatches by command id.

Strengths confirmed by the field: the `Emitter`/`Event`/`Disposable`/`DisposableStore` vocabulary is identical to VS Code's and Theia's; the command registry has the right name and shape; features already register through `register()` functions that return disposables; registrations upsert so re-running a setup never duplicates (VS Code has no equivalent and relies on module load order); dynamic menus already rebuild at open time, which is what every reference does for every menu.

Deficits the findings map to:

1. No submenu support in the renderer.
2. No multi-stroke chords and no pending-chord status.
3. No quick open or command palette.
4. Enablement is a per-command `enabled()` callback; no context keys or `when` clauses.
5. Shortcut hints are hand-typed strings in the command descriptor.
6. All menus are declared in one composition file; command, placement, and keybinding are three separate registrations.
7. Title-bar buttons are hard-coded HTML.
8. The WebSocket protocol is an ad-hoc frame union with no correlation, channels, or typed proxies.

## The naming convergence table

Three independent implementations, one column each; forks inherit the VS Code column. "Same" means the reimplementation chose VS Code's name or a trivial variant.

| Concept | VS Code | Theia | OpenSumi | Adopt |
|---|---|---|---|---|
| Command registry | `CommandsRegistry`, `ICommandService` | `CommandRegistry`, `CommandService` (same) | `CommandRegistry`, `CommandService` (same) | keep `CommandRegistry` |
| Menu identity | `MenuId` (static instances, `MenuId.for(id)`) | `MenuPath = string[]` (diverges) | `MenuId` enum of `'editor/context'` strings (same as VS Code) | `MenuId` as string constants |
| Menu item | `IMenuItem {command, when, group, order}` | `MenuAction {commandId, order, label, when}` (close) | `IMenuItem` (same) | `IMenuItem` |
| Submenu | `ISubmenuItem {submenu: MenuId, title, group, order, when}` | `registerSubmenu(path, label)` (same idea) | `ISubmenuItem` (same) | `ISubmenuItem` |
| Menu registry | `MenuRegistry.appendMenuItem(menuId, item)` | `MenuModelRegistry.registerMenuAction` (diverges) | `IMenuRegistry.registerMenuItem(menuId, item)` (same) | `MenuRegistry.appendMenuItem` |
| Root of the menubar | `MenuId.MenubarMainMenu`, top menus are `ISubmenuItem`s of it | `MAIN_MENU_BAR = ['menubar']` (same idea) | `registerMenubarItem` (same idea) | `MenuId.MenubarMainMenu` |
| Group ordering | `group` string, `navigation` first, then lexical (`1_open`), then `order` | `navigation` sorts first (same) | `group`/`order` (same) | same |
| One-shot declaration | `Action2` / `registerAction2` | `AbstractViewContribution` options object (same idea) | `CommandContribution` + `MenuContribution` (Theia's) | `registerAction(descriptor)` |
| Keybinding registry | `KeybindingsRegistry.registerKeybindingRule {id, primary, when, weight}` | `KeybindingRegistry {command, keybinding, when}` (same) | `KeybindingRegistry` (same) | `KeybindingsRegistry` |
| Chord notation | `KeyChord(a, b)` in code; `"ctrl+k ctrl+o"` in manifests | `"ctrlcmd+k ctrlcmd+o"` whitespace-split (same as manifest form) | `KeySequence.parse` splits on whitespace (same) | `"ctrl+m ctrl+o"` strings |
| Chord resolution | `KeybindingResolver.resolve -> NoMatchingKb / MoreChordsNeeded / KbFound` | `CompareResult {NONE, PARTIAL, SHADOW, FULL}` (same idea) | partial/full (Theia's) | VS Code's three-way result |
| Pending-chord message | "({0}) was pressed. Waiting for second key of chord..." via status | "{0} was pressed, waiting for more keys" status entry `keybinding-status` (same) | identical to Theia | status-bar entry |
| Shortcut label | `keybindingService.lookupKeybinding(id)?.getLabel()` | `acceleratorFor(binding, '+')` (same idea) | `getKeybindingsForCommand` + `acceleratorFor` (Theia's) | `lookupKeybinding(id)?.getLabel()` |
| Context keys | `RawContextKey.bindTo`, `ContextKeyExpr`, `IContextKeyService` | `ContextKeyService`, wraps VS Code's `ContextKeyExpr` (same) | `RawContextKey`, vendored monaco engine (same) | same names |
| Enablement semantics | `when` hides, `precondition` disables, `toggled` checks | `isVisible`, `isEnabled`, `isToggled` handler predicates + `when` | VS Code's | VS Code's |
| Quick input | `IQuickInputService`, `IQuickPick`, `IInputBox` | `QuickInputService`, `QuickPickService` (same) | `IQuickInputService`, `QuickOpenService` (same) | `QuickInputService` |
| Quick access | `IQuickAccessProviderDescriptor {prefix, placeholder, helpEntries}` in `QuickAccessRegistry` | `QuickAccessProviderDescriptor {prefix, helpEntries}` (same) | `QuickOpenHandler.prefix` (Theia 1.14 copy, diverges in name) | `QuickAccessRegistry` |
| Palette | prefix `>`, id `workbench.action.showCommands`; quick open `workbench.action.quickOpen` | `QuickCommandService.PREFIX = '>'`, same command id | `>` (same) | same ids |
| Prefixes | `''` files, `>` commands, `@` symbols, `:` line, `%` text, `#` workspace symbols, `?` help | same set minus `%` located | `>` `@` `:` | same set |
| Events / ownership | `Emitter`, `Event`, `Disposable`, `DisposableStore` | `Emitter`, `Event`, `Disposable`, `DisposableCollection` (same) | Theia's | already matched |
| Feature registration | `<feature>.contribution.ts` side-effect module, flat import list in `workbench.common.main.ts` | `CommandContribution` / `MenuContribution` / `KeybindingContribution` bound via DI (diverges) | `@Domain(...Contribution)` (Theia's) | `register()` per feature (already) plus `*.contribution.ts` naming |
| Layering | `common` (no DOM) / `browser` / `electron-*`; ESLint forbids upward imports | `common` / `browser` / `node` / `electron-*` (same) | `core-common` / `core-browser` (same) | registries to `services/`, widgets stay in `ui/` |
| RPC | `IPCClient`, `IChannel`, `ProxyChannel.toService<T>`, numeric request ids, `EventListen`/`EventDispose` | `RpcProxy`, `RpcConnectionHandler {path}`, `ChannelMultiplexer` (diverges in name, same shape) | `SumiConnection`, `RPCServiceStub.getProxy()`, `WSChannel` (own) | shape only, later |

Twenty-two concepts; the reimplementations match VS Code on eighteen by name or by shape. The four divergences are Theia's `MenuPath` arrays (OpenSumi rejected them for `MenuId`), the DI-interface contribution style (a consequence of InversifyJS, not a design preference), and RPC naming.

## Detailed findings, ranked by payoff

### Finding 1: One declaration registers command, placements, keybinding, and palette entry

VS Code's `registerAction2` takes one descriptor `{id, title, category, f1, precondition, toggled, keybinding: {primary, when, weight}, menu: [{id, group, order, when}]}` and fans it into `CommandsRegistry`, `MenuRegistry` (one item per `menu` entry plus a `MenuId.CommandPalette` item when `f1` is true), and `KeybindingsRegistry` (the `precondition` ANDed into the keybinding's `when`), returning one composite disposable ([actions.ts#L723-L781](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/actions/common/actions.ts#L723-L781)). Void uses exactly this shape for its AI sidebar actions ([sidebarActions.ts#L146-L160](https://github.com/voideditor/void/blob/b3166e7ef2aefbdfeb139445fdf248a561b85d4d/src/vs/workbench/contrib/void/browser/sidebarActions.ts#L146-L160)); Positron's console actions are 1,600 lines of them; code-server's one added menu row is the two-call unrolled form, `registerCommand` then `appendMenuItem` per menu ([logout.diff#L87-L105](https://github.com/coder/code-server/blob/20a260f7488ea5508d9216a2629a1beccf5e8954/patches/logout.diff#L87-L105)).

What it replaces: `window-menu.ts` lines 292-357, where 19 descriptors are registered, then 25 `item()`/`separator()` placements are made separately, then `shortcuts.ts` binds the same ids a third time with hand-matched key predicates.

The fix: add `registerAction(descriptor)` to the services layer that writes to the three registries and returns one disposable; each feature directory's `register()` calls it for its own actions. Addresses deficits 4, 5, 6. Cost medium. Confidence: high - five references use the identical shape.

### Finding 2: Submenus are menu items whose payload is a menu id; the menubar is the root menu's children

In VS Code, `ISubmenuItem` is `{submenu: MenuId, title, group, order, when}` ([actions.ts#L30-L36](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/actions/common/actions.ts#L30-L36)); the File, Edit, Selection... menus are eight such items appended to `MenuId.MenubarMainMenu` ([menubar.contribution.ts#L10-L18](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/workbench/browser/parts/titlebar/menubar.contribution.ts#L10-L18)); `CustomMenubarControl` generates the bar's buttons by walking that root, drops empty submenus, and splices the dynamic Open Recent list in by id at conversion time ([menubarControl.ts#L632-L665](https://github.com/gitpod-io/openvscode-server/blob/2bfb814c5215c51a10e80c2cb1b58ed91068ad8b/src/vs/workbench/browser/parts/titlebar/menubarControl.ts#L632-L665)). The popover widget branches on `instanceof SubmenuAction` and shares one `{parent, submenu}` slot per open menu ([menu.ts#L895-L963](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/base/browser/ui/menu/menu.ts#L895-L963)). Theia reaches the same rendering by recursion: a labelled compound node becomes a `{type: 'submenu'}` with its own recursive menu, an unlabelled one becomes an inline group wrapped in de-duplicated separators, and items are rebuilt on every open ([browser-menu-plugin.ts#L315-L349](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/browser/menu/browser-menu-plugin.ts#L315-L349)). OpenSumi's `MenubarServiceImpl` does the same walk ([menubar-service.ts#L152-L182](https://github.com/opensumi/core/blob/9fee6aa38f96f85ac686f25c2522910067324c1d/packages/core-browser/src/menu/next/menubar-service.ts#L152-L182)).

What it replaces: `index.html` lines 14-18 (five hard-coded buttons), `menu-registry.ts`'s `registerMenu(id, label, order)` (a separate concept for top-level menus), and the `MenuItemSpec` union that knows only `command` and `separator`.

The fix: `MenuItemSpec` gains `{kind: "submenu", submenu: MenuId, title}`; `registerMenu` goes away, replaced by appending submenu items to `MenuId.MenubarMainMenu`; the renderer generates the `nav` buttons from that root and opens a child popover when a row is a submenu. Separators come from group boundaries, not explicit rows. Addresses deficits 1, 7. Cost medium. Confidence: high - three implementations, identical structure.

### Finding 3: Shortcut labels are looked up from the keybinding registry at render time

VS Code's `Menu` widget receives `getKeyBinding: (action) => keybindingService.lookupKeybinding(action.id)` and renders `?.getLabel()` beside each row, re-rendering on `onDidUpdateKeybindings` ([menu.ts#L417-L425](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/base/browser/ui/menu/menu.ts#L417-L425), [menubarControl.ts#L674-L681](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/workbench/browser/parts/titlebar/menubarControl.ts#L674-L681)). Positron's `ActionBarCommandButton` takes only a command id and derives its tooltip the same way ([actionBarCommandButton.tsx#L42-L101](https://github.com/posit-dev/positron/blob/f7d370069a03f7c940d5c77579f4af4f3fc6ede0/src/vs/platform/positronActionBar/browser/components/actionBarCommandButton.tsx#L42-L101)). Theia's `ActionMenuNode` calls `getKeybindingsForCommand(id)` and `acceleratorFor(binding, '+')`, the same function that feeds the palette and native menus ([action-menu-node.ts#L83-L93](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/browser/menu/action-menu-node.ts#L83-L93)).

What it replaces: the `shortcut?: string` field on `CommandDescriptor` and every hand-typed `"Ctrl+Z"` in `window-menu.ts`.

The fix: remove `shortcut` from the descriptor; the renderer asks `KeybindingsRegistry.lookupKeybinding(id)?.getLabel()`. The same label formatter serves the palette. Addresses deficit 5. Cost small. Confidence: high - four references.

### Finding 4: Chords are a pure resolver plus shell-owned pending state and a status message

`KeybindingResolver.resolve(context, currentChords, keypress)` indexes rules by first chord, prefix-filters against the pressed sequence, lets the last `when`-matching rule win, and returns `MoreChordsNeeded` when a longer rule still matches ([keybindingResolver.ts#L320-L378](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/keybinding/common/keybindingResolver.ts#L320-L378)). The service keeps `_currentChords`, posts "({0}) was pressed. Waiting for second key of chord..." through the status service, and leaves chord mode after 5 s idle or on window blur ([abstractKeybindingService.ts#L175-L224](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/keybinding/common/abstractKeybindingService.ts#L175-L224)). Theia parses `"ctrlcmd+k ctrlcmd+o"` by whitespace into a `KeySequence`, returns `PARTIAL`/`FULL`, swallows the partial event, and sets status entry `keybinding-status` to "{0} was pressed, waiting for more keys" ([keybinding.ts#L650-L684](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/browser/keybinding.ts#L650-L684)); OpenSumi's is the same code ([keybinding.ts#L842-L873](https://github.com/opensumi/core/blob/9fee6aa38f96f85ac686f25c2522910067324c1d/packages/core-browser/src/keybinding/keybinding.ts#L842-L873)).

What it replaces: `shortcuts.ts`'s list of `{command, matches(event)}` predicates and its plain-Ctrl gate.

The fix: rules are `{id, keybinding: "ctrl+m ctrl+o", when, weight}` strings parsed once; a DOM-free resolver returns the three-way result; the dispatcher in `ui/layout/` keeps the pending chords, shows the status message, and clears on timeout or blur. Addresses deficit 2. Cost small to medium. Confidence: high - three implementations, one message text.

### Finding 5: Context keys with `when` (hide), `precondition` (disable), `toggled` (check)

`RawContextKey<T>.bindTo(service)` yields a typed setter; `ContextKeyExpr.and/or/not/equals/has/deserialize` build expressions from strings; `IContextKeyService.contextMatchesRules` evaluates them ([contextkey.ts#L580-L637](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/contextkey/common/contextkey.ts#L580-L637)). `MenuService` collects every key its items reference and refires only when `affectsSome(keys)` ([menuService.ts#L278-L312](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/actions/common/menuService.ts#L278-L312)). Void flips two actions in one menu slot by a context key set during async work ([voidSCMService.ts#L185-L230](https://github.com/voideditor/void/blob/b3166e7ef2aefbdfeb139445fdf248a561b85d4d/src/vs/workbench/contrib/void/browser/voidSCMService.ts#L185-L230)); code-server pipes a server flag into a context key once at boot and gates menu rows with `when: ContextKeyExpr.and(...)` ([external-file-actions.diff#L172-L206](https://github.com/coder/code-server/blob/20a260f7488ea5508d9216a2629a1beccf5e8954/patches/external-file-actions.diff#L172-L206)). Theia and OpenSumi wrap VS Code's engine rather than write one.

What it replaces: `enabled?: () => boolean` on the descriptor and the `hasEditTarget` closure in `window-menu.ts`.

The fix: a `ContextKeyService` in `services/` with `createKey(name, default)` and `onDidChangeContext`; a `ContextKeyExpr` supporting the subset we need now (key, `!key`, `key == 'v'`, `&&`, `||`, `true`/`false`); menu rows and keybinding rules carry `when`/`precondition` strings. Initial keys: `editorFocus`, `activeEditorExists`, `editTargetFocus`, `isDesktop`, `treeVisible`, `chordPending`. Stubs use `precondition: false`. Addresses deficit 4. Cost medium. Confidence: high - all seven references.

### Finding 6: Quick access is a prefix registry; the palette is the `>` provider; the pill only calls `show()`

`QuickAccessRegistry` holds descriptors `{ctor, prefix, placeholder, helpEntries, when}` sorted by prefix length; `QuickAccessController.show(value)` picks the longest matching prefix, lazily instantiates the provider, and re-routes in place as the value changes ([quickAccess.ts#L233-L266](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/quickinput/common/quickAccess.ts#L233-L266), [quickAccess.ts#L210-L250](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/quickinput/browser/quickAccess.ts#L210-L250)). The palette's picks are `getMenuActions(MenuId.CommandPalette)` with `lookupKeybinding` per row ([commandsQuickAccess.ts#L226-L232](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/workbench/contrib/quickaccess/browser/commandsQuickAccess.ts#L226-L232)). Theia's `QuickCommandService` is the `>` provider filtering labelled, visible, enabled commands, recent first, with the first keybinding attached, and `?` lists the other prefixes from `helpEntries` ([quick-command-service.ts#L67-L142](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/browser/quick-input/quick-command-service.ts#L67-L142)). Positron's centered title-bar pill is a button whose click handler is `quickInputService.quickAccess.show()` and nothing else ([topActionBarCommandCenter.tsx#L39-L60](https://github.com/posit-dev/positron/blob/f7d370069a03f7c940d5c77579f4af4f3fc6ede0/src/vs/workbench/browser/parts/positronTopActionBar/components/topActionBarCommandCenter.tsx#L39-L60)).

What it replaces: nothing yet; this is the greenfield piece of the plan.

The fix: `services/quick-access.ts` registry plus a `ui/quickinput/` widget; providers for `''` (files from the tree cache), `>` (commands with `f1` from the registry, labels from the keybinding registry), `:` (go to line on the active editor), `?` (help); `@` and `%` registered with a "not available" placeholder. Command ids `workbench.action.quickOpen` and `workbench.action.showCommands`. Addresses deficit 3. Cost large for the widget, small for the registry. Confidence: high - three implementations and one pinned pill.

### Finding 7: Registries are DOM-free and live below the widgets

VS Code keeps `CommandsRegistry`, `MenuRegistry`, `KeybindingsRegistry`, `KeybindingResolver`, `ContextKeyExpr`, and `QuickAccessRegistry` in `platform/*/common/` and the `Menu`, `MenuBar`, and quick-input widgets in `base/browser/ui/` and `platform/quickinput/browser/`; ESLint forbids `common` from touching the DOM and forbids core from importing `contrib` ([eslint.config.js#L1810-L1825](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/eslint.config.js#L1810-L1825)). Theia mirrors this with `common/` and `browser/` folders, and its own mess is the place where it broke the rule ([common/menu/index.ts#L17-L20](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/common/menu/index.ts#L17-L20) re-exports browser modules).

What it replaces: `ui/menu/` holding both the registries and the renderer.

The fix: move `command-registry.ts` and `menu-registry.ts` to `services/commands.ts` and `services/menus.ts`, add `services/keybindings.ts`, `services/context-keys.ts`, `services/actions.ts`, `services/quick-access.ts`; leave `menu-renderer.ts` and the new menubar and quick-input widgets in `ui/`. Registries get jsdom-free tests. Addresses deficit 6 structurally. Cost small. Confidence: high - the subject's own `base -> services -> ui` rule already says this.

### Finding 8 (noted, not scheduled): one socket, named channels, request ids, Proxy-based typed services

VS Code's `ChannelClient` correlates by `lastRequestId++` over typed request/response enums with wire-level cancel and `{name, message, stack}` errors, treats events as ref-counted subscriptions (`EventListen` on first listener, `EventDispose` on last), and `ProxyChannel.toService<T>` turns a TypeScript interface into RPC by classifying `onX` members as events and the rest as calls ([ipc.ts#L571-L652](https://github.com/gitpod-io/openvscode-server/blob/2bfb814c5215c51a10e80c2cb1b58ed91068ad8b/src/vs/base/parts/ipc/common/ipc.ts#L571-L652), [ipc.ts#L654-L693](https://github.com/gitpod-io/openvscode-server/blob/2bfb814c5215c51a10e80c2cb1b58ed91068ad8b/src/vs/base/parts/ipc/common/ipc.ts#L654-L693), [ipc.ts#L1187-L1246](https://github.com/gitpod-io/openvscode-server/blob/2bfb814c5215c51a10e80c2cb1b58ed91068ad8b/src/vs/base/parts/ipc/common/ipc.ts#L1187-L1246)). Theia's contract is a path constant, a Symbol, and an interface in `common/`; the browser gets a `Proxy` that queues calls until connected and re-arms on close; many services multiplex over one socket by channel id ([proxy-factory.ts#L220-L279](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/common/messaging/proxy-factory.ts#L220-L279), [service-connection-provider.ts#L73-L86](https://github.com/eclipse-theia/theia/blob/0b5a5f27164581ca47b8d7c08eaf690ac23d932f/packages/core/src/browser/messaging/service-connection-provider.ts#L73-L86)). OpenSumi's `SumiConnection` has the same `_requestId` counter and `_callbacks` map under a different wire format ([multiplexer.ts#L8-L66](https://github.com/opensumi/core/blob/9fee6aa38f96f85ac686f25c2522910067324c1d/packages/connection/src/common/rpc/multiplexer.ts#L8-L66)); Void multiplexes streaming LLM responses by `requestId` over one channel ([sendLLMMessageService.ts#L103-L146](https://github.com/voideditor/void/blob/b3166e7ef2aefbdfeb139445fdf248a561b85d4d/src/vs/workbench/contrib/void/common/sendLLMMessageService.ts#L103-L146)).

This maps to deficit 8 in `workshop-socket.ts` and the Rust `/ws` handler, which are outside the menu plan. When that work is scheduled, the shape to adopt is: JSON frames `{type: request|response|error|event, id, channel, method, args}`, a `ChannelClient` with numeric ids and a pending map, a `Proxy` over a service interface, and a Rust `match (channel, method)` dispatcher. Cost medium. Confidence: medium - shapes converge, wire formats do not, and the Rust side was not examined.

## Where the subject already matches or beats the references

- `Emitter`/`Event`/`Disposable`/`DisposableStore` match VS Code and Theia by name and semantics.
- `CommandRegistry` as a Map of descriptors with `register`/`lookup`/`execute` is the same shape as all three implementations.
- Upsert-by-id registrations that never duplicate on re-run beat VS Code, which depends on module load order and has no such guard.
- Dynamic menus rebuilt at open time is what every reference does for every menu; the subject only needs to make it the default rather than the provider-only path.
- Per-feature `register()` functions returning a disposable are the `*.contribution.ts` pattern under a different file name.
- The subject has no 2,600-line contribution file (Theia's `common-frontend-contribution.ts`), no React bridge inside the workbench (Void, Positron), and no `base` importing `workbench` (Positron's `positronReactServices.tsx`). Keep it that way: stubs go in a table, not a class.

## Messes we should explicitly not copy

- VS Code: 260 feature-specific `MenuId` statics in the platform layer ([actions.ts#L70-L337](https://github.com/microsoft/vscode/blob/925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e/src/vs/platform/actions/common/actions.ts#L70-L337)); a 1,460-line `menu.ts` with ~430 lines of CSS in a string for shadow DOM; `CustomMenubarControl` re-wrapping resolved actions into base actions to satisfy layering. Our `MenuId` constants stay in the feature that owns them, our CSS stays in `.css` files.
- Theia: `common-frontend-contribution.ts` at 2,609 lines with `registerKeybindings` alone spanning 460 lines - the exact file `window-menu.ts` would become if every stub landed in it; `common/menu/index.ts` re-exporting browser modules; overriding Lumino's private `_openChildMenu` from the constructor.
- OpenSumi: not a mess but a caution - the quick-open package is a licensed copy of Theia 1.14 with EPL headers inside an MIT repo.
- Void: a 104 KB single React component, duplicate action-id constants both registered, a 6-second timer rewriting a CSS file as a "hack to refresh styles".
- Positron: fence-comment syntax drift with no verifier; `src/vs/base/browser/positronReactServices.tsx` importing ~40 workbench services into `base`.
- code-server: patches without header comments despite the written rule; a 347-line patch carrying seven concerns.
- openvscode-server: `= true || ...` and `false &&` patches instead of clean deltas; a stale "header is 9 bytes" comment beside `HeaderLength = 13`.

## Recommended execution order

1. Finding 7 first, since everything else lands in the new files: move the two registries to `services/`, add `context-keys.ts`, `keybindings.ts` (registry, resolver, label formatter), `actions.ts` (`registerAction`), `quick-access.ts` (registry only). Pure TypeScript, jsdom-free tests.
2. Findings 2 and 3 together, since they change the same renderer: submenu item kind, root `MenubarMainMenu`, generated `nav` buttons, group-boundary separators, labels from `lookupKeybinding`.
3. Finding 4: replace `shortcuts.ts` with the chord dispatcher over the resolver; status message; 5 s timeout and blur exit.
4. Finding 5: wire the context keys the features need; menus and keybindings evaluate `when`/`precondition`.
5. Finding 1 applied: each feature's `register()` declares its actions; `menubar.contribution.ts` declares the eight root submenus and their groups; `stubs.contribution.ts` is a table of `{id, title, menu, group, order, keybinding}` rows with `precondition: false`.
6. Finding 6: quick-input widget, the four live providers and two placeholders, the title-bar pill.
7. Tests last: the existing suite pins behavior through `setupWindowMenus`; keep that entry point until the new registrations pass, then rewrite the menu tests against the registries.

## Refactor notes

- Findings 7, 3, and 1 are pure structure: no user-visible change except that shortcut labels come from one table. Findings 2, 4, 5, 6 change behavior (flyouts, chords, disabled-by-context rows, quick open).
- The test suite is the invariant. `titlebar-style.mjs`, `window-menu.mjs`, `zoom.mjs`, `gateway-config-menu.mjs` pin labels and button counts; they move last and are rewritten against the registries, not against DOM built by hand.
- Do not touch `workshop-socket.ts`, the agent panel's socket, or the Rust server in this plan; Finding 8 is a separate effort.
- Keep `MenuId` constants beside the feature that owns the menu; only `MenubarMainMenu`, the eight menubar submenus, and `CommandPalette` live in the menu service.
- Verify and commit per step. Two consecutive failures on one step stops the run for a re-plan.

## Sources

- microsoft/vscode - https://github.com/microsoft/vscode - HEAD 925a0ffbf3e488061e4c01ae9d9ac88ae6907a7e - MIT - analyzed 2026-09-14
- eclipse-theia/theia - https://github.com/eclipse-theia/theia - HEAD 0b5a5f27164581ca47b8d7c08eaf690ac23d932f - EPL-2.0 OR GPL-2.0-only WITH Classpath-exception-2.0 - analyzed 2026-09-14
- opensumi/core - https://github.com/opensumi/core - HEAD 9fee6aa38f96f85ac686f25c2522910067324c1d - MIT - analyzed 2026-09-14
- voideditor/void - https://github.com/voideditor/void - HEAD b3166e7ef2aefbdfeb139445fdf248a561b85d4d - Apache-2.0 (archived 2026-06-02) - analyzed 2026-09-14
- posit-dev/positron - https://github.com/posit-dev/positron - HEAD f7d370069a03f7c940d5c77579f4af4f3fc6ede0 - Elastic License 2.0 - analyzed 2026-09-14
- gitpod-io/openvscode-server - https://github.com/gitpod-io/openvscode-server - HEAD 2bfb814c5215c51a10e80c2cb1b58ed91068ad8b - MIT - analyzed 2026-09-14
- coder/code-server - https://github.com/coder/code-server - HEAD 20a260f7488ea5508d9216a2629a1beccf5e8954 (vscode submodule 645f29cc3176500b4b5762ba887cf2a7f0ffdf2c) - MIT - analyzed 2026-09-14
- Field survey of 30+ candidates and subject profile: 2026-09-14

*2026-09-14 20:30 - Claude Fable 5.1*

