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

**promptforge-mcp-server** (binary)
- config loader (`prompts.toml`) + prompt catalog, watcher and per-prompt reload
- a fixed published tool list: `list_prompts`, `run_prompt`, `check_run`, and `need_prompt` under the `picker` feature. No prompt is published as a tool of its own; `run_prompt` is the only invocation path and the caller names the prompt
- `serve_stdio()` and `serve_http()`

**promptforge-tool-picker** (library)
- the resolution engine behind `need_prompt`: a described prompt resolved to a catalog name

`promptforge-host` is the only entry above that is not built; its two functions live in the CLI and the MCP server.