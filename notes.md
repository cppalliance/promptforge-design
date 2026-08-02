**promptforge-core** (library)
- parser: frontmatter, `promptforge_version` detection, H2-H6 section tree, Lua-fence split
- execute: section fall-through executor + tool-call loop + version gate
- client: `GatewayClient` (OpenAI-shaped calls to the gateway)
- lua: sandboxed mlua VM (`run_chunk`)
- subst: `{{ }}` substitution
- store: VFS (`FileStore`, `MemVfs`, `Store` handle)
- tools: `Tool` trait + `web_search`
- error: `Error`/`Result`

**promptforge-webfetch** (library)
- `web_fetch` tool: fetch URL -> markdown
- SSRF hardening: URL policy, CIDR blocklist, guarded DNS resolver, redirect policy
- content extraction (readability + HTML->markdown)

**promptforge-gateway** (binary)
- inference gateway; holds vendor + Brave keys
- `gateway.toml` config, model routing, OpenAI passthrough
- bearer auth; `/v1/chat/completions`, `/health`, `/v1/tools/web_search`

**promptforge-cli** (binary)
- the `promptforge` command; `run <file> [input]`
- tool selection (`select_tools`)

**promptforge-host** (library, *planned*)
- `select_tools` (names -> concrete tools)
- `run_prompt_file` (read -> gate -> parse -> sandbox -> execute)
- `HostError`

**promptforge-mcp** (library, *planned*)
- config loader + prompt registry (installed prompts)
- two MCP tools: `list_prompts`, `run_prompt`
- `serve()` (streamable-HTTP daemon)

First four are built; the last two are proposed in the MCP plan.