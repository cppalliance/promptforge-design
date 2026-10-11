<!-- sources: cabinet/_research/2026-09-13-conduct-research-tool-naming-namespaces.md, 2026-09-13-conduct-research-global-naming-systems.md, 2026-09-13-conduct-research-plugin-ecosystem-naming-versioning.md, plus decentralized naming systems survey of same date -->

# Global Tool Naming for PromptForge Tool Packs: Survey and Recommendation

Four parallel surveys covered agent/LLM tool wire naming, classic package namespaces, decentralized protocol naming, and plugin ecosystems. This report synthesizes them into a recommendation for promptforge's tool-pack naming: packs installed as a unit, globally unique tool names, prompts binding global names to prompt-local aliases in frontmatter.

## The constraint that shapes everything: the wire alphabet

Every major provider converges on the same tool-name rule: `^[a-zA-Z0-9_-]{1,64}$`, starting with a letter or underscore. OpenAI, Anthropic, Gemini (in its strict proto path), and Mistral all land there. MCP is more permissive (1-128 chars, dots allowed, unique per server only) and explicitly warns that `serverInfo.name` must not be used for disambiguation - so MCP-sourced names always need sanitization before they hit a provider, and that sanitization creates a second collision domain.

Consequence: the global name can never go on the wire. The prompt-local alias is not just namespacing hygiene - it is the wire-legal name the model sees. This validates the binding design: global name for identity and resolution, local alias for the model. Two namespaces, syntactically distinct, never mixed.

A second wire lesson: never recover routing by parsing the wire name. Prefix schemes like `mcp__server__tool` are provably not injective (`mcp/read_file` vs `mcp_read/file` collide), and every framework that relied on them has documented silent-collision or truncation bugs. Routing must key on the global name internally; the alias is display-only.

## The authority question: who may mint a pack name

The surveys converged unanimously: when there is no central registry, every successful ecosystem roots global uniqueness in **DNS ownership**. Java did it by pure convention (the JLS says explicitly "instead of having to create a separate registry"), Go by making import paths domain-anchored fetch URLs, Kubernetes by reserving API groups as DNS subdomains, AT Protocol by reverse-DNS NSIDs with DNS TXT proof of authority, and the official MCP registry by reverse-DNS namespaces verified through GitHub OAuth (`io.github.user/*`) or DNS TXT records (`com.example/*`).

The MCP registry model is the strongest fit for promptforge: globally unique, human-readable, no allocation bottleneck, and a future promptforge registry can add Maven-style DNS verification later without renaming anything. The alternative - a central registry assigning names (VS Code's `publisher.name`, Obsidian's PR-gated flat namespace) - works only if promptforge runs the only registry, which contradicts the DLL/no-registry-first distribution model.

The cautionary poles: Neovim (no registry, no namespacing - attribution and collision avoidance both failed, and the ecosystem is now retrofitting exactly the pack-identity concept) and WordPress (no runtime isolation - the ecosystem pays forever in prefix conventions and still collides). The lesson from both: qualify every tool name with its pack, always, and let the runtime enforce the boundary rather than convention.

## The local-alias archetype

XML namespaces are the classic proof of the user's model: global URI identity, document-local prefix alias, comparison always on the (URI, localname) pair, never on the prefix. JSON-LD's `@context` is the same idea as a shareable binding map. WIT's `use wasi:http/types@0.2.0 as http-types;` is the same idea in a modern grammar. The documented failures of these systems are all ergonomic (opacity, copy-paste ritual, silent typos) - not structural. The structure is right.

Two alias lessons worth importing:

- **Bind once at manifest level, not per use site.** Cargo's `foo = { package = "bar" }` and npm's alias installs are the best-regarded designs; Go and Python's per-file import aliasing produce recurring confusion. Promptforge frontmatter is the manifest - one binding block, whole-prompt scope.
- **Never let the compact and global forms be lexically ambiguous.** The CURIE lesson from RDF: if a short string could parse as either an alias or a global name, tooling and humans both eventually misread it. Aliases should be wire-legal (`[a-zA-Z0-9_-]`), global names should contain characters aliases can't (dots/slashes), making the distinction self-evident at a glance.

## Versioning: beside the name, with a qualified escape hatch

Unanimous for installable units: the version is metadata beside the name (VS Code, JetBrains, MCP, Cargo, npm), identity is frozen at first publish, and published versions are immutable (MCP's rule - pinning is only trustworthy if versions can't mutate). A pack rename is operationally a new pack (JetBrains freezes IDs precisely because everything keys off them).

The escape hatch for incompatible majors is version-qualified references, WIT-style: `wasi:http/types@0.2.0` vs `@1.0.0` bound to two different aliases lets one consumer use both without a flag-day upgrade. Kubernetes' deprecation policy is the gold standard for renames/removals: old and new served simultaneously, deprecation announced with a deadline, migration tooling shipped. One caution: WIT's `@version` placement (after the package in declarations, after the interface in references) confuses even its own designers - fix the version position in the grammar once and never move it.

Also: persisted references outlive code. Names get stored in configs, event logs, and session history. No surveyed ecosystem handles this well; a `renamed-from` alias field in the pack manifest so the host can diagnose or repair broken bindings is a gap worth filling rather than copying.

## Recommendation

```yaml
# prompt frontmatter
packs:
  - io.github.corp/bashkit@1        # global pack id, DNS-anchored, major-qualified
tools:
  shell: io.github.corp/bashkit/shell      # local alias: global name
  grep:  io.github.corp/bashkit/grep
calls:
  term-worker: ./agents/terminal.md        # called prompts bound the same way
```

- **Pack id:** `namespace/pack` where namespace is reverse-DNS (`io.github.corp`, `com.example`) or a reserved first-party prefix (`promptforge/...`, reserved now, before anyone else squats it). Slash form over dotted form: it matches the MCP registry convention promptforge will interoperate with, and it reads as a path, which it conceptually is.
- **Global tool name:** `namespace/pack/tool` - always pack-qualified, never bare. Three segments, no more.
- **Local alias:** wire-legal (`^[a-zA-Z0-9_-]{1,64}$`), chosen by the prompt author, the only name the model ever sees. Aliases and global names are lexically disjoint by construction.
- **Version:** beside the pack id (`@1` major pin in frontmatter; exact resolution recorded in the run's event log), with WIT-style major-qualified references as the designed-in escape hatch for coexistence.
- **Registry later, not now:** when a promptforge registry exists, model it on the DID method registry / MCP registry - a PR-based directory with DNS-proof namespace verification, not a root of trust. Names work without it from day one.
- **Normalization fixed at launch:** comparison is case-sensitive on the exact string (OpenAPI's lesson: uniqueness must survive lowercasing and separator removal, so forbid pack names that collide under normalization at registration/publish time).

## What this means for the picker

The picker leaves the binding path entirely. Its surviving roles: optional prose discovery for exploratory sessions, and `near_duplicates` as a registration-time lint - when two installed packs offer tools whose descriptions are near-identical, that is a pack-authoring smell worth failing loudly on, which is exactly what the picker's duplicate detection already computes.

*2026-09-13 06:40 - kimi-k3*
