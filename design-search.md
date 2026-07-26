<!-- STATUS: crate doc - promptforge-ext-search - the stateless reference case - see design.md for the system -->

# `promptforge-ext-search`: web search and fetch as compiled-in tools

## Scope

This crate contributes two functions, `web_search` and `web_fetch`, one search provider abstraction, one URL policy, and two HTTP connection pools. That is the whole crate.

It is the first extension to build, and it has a second job beyond specifying itself. `design.md` records the riskiest remaining assumption in the design as the claim that the `Extension` trait carries both a stateless HTTP-backed extension and a transactional database-backed one without acquiring a special case for either. This crate is the stateless half of that experiment and `promptforge-ext-paperstore` is the transactional half. So this document says explicitly which parts of the trait a stateless extension leaves empty and why, because that is the finding the experiment is for, and an extension author reading two documents should be able to see the same trait doing two different jobs.

`web_search` and `web_fetch` are compiled-in Rust functions called directly from the tool registry. They are never federated over MCP. MCP exists to cross a process boundary and these cross none, so wrapping them in a protocol would buy a hop, a serialization, and a second failure mode, and nothing else. They also never appear on our own MCP surface: a connecting client sees prompts and never tools, and Cursor already has web search and must not be offered a second one.

What this crate does not do, and cannot be made to do without a change to this document:

- Appear on `promptforge-mcp`'s MCP surface. The tool registry calls these functions in process. Nothing publishes them.
- Speak MCP in either direction. There is no MCP client and no MCP server here. A genuinely remote search service is a different extension wrapping a remote MCP endpoint, which `design-mcp.md` specifies as an `[[mcp_clients]]` entry, and it is not this crate.
- Hold run state or section state. It keeps no per-run and no per-section data, which is why `on_section` is a no-op.
- Cache. A repeated identical search inside one run reaches the network again. See `## Caching`.
- Render a document. `web_fetch` returns text. It does not return HTML, a DOM, a screenshot, or a PDF.
- Read a PDF. An `application/pdf` response is refused with a message the model can act on.
- Execute JavaScript. There is no browser engine, so a page whose content arrives by client-side rendering returns whatever its server-side HTML contained, which is often nothing.
- Log in, hold a cookie, or present a credential to a fetched host. The fetch client has no cookie store and no default authorization header.
- Write anything. No file, no row, no declared output. Fetched text reaches durable storage only if a prompt files it through some other extension.
- Crawl. One call is one URL. There is no link following beyond redirects and no recursion.
- Rank, deduplicate, or summarise results. The provider's order is preserved verbatim, and reranking is `promptforge-ext-classify`'s four operations acting on what this crate returned.
- Decide which pages are trustworthy. Everything `web_fetch` returns is untrusted text, and this crate says so rather than filtering it.

The test of the boundary: removing this crate from the workspace leaves every other crate compiling untouched, and no crate outside it mentions `reqwest`, `dom_smoothie`, `html2text`, or a search provider.

## The stateless reference case

The `Extension` trait has eight methods. A stateless extension implements four of them with real content and four with almost none, and which four are almost empty is the entire finding.

| Method | Here | In `promptforge-ext-paperstore` |
|---|---|---|
| `name` | The `[extensions.NAME]` block key, which also selects the provider. | The store's identity. |
| `provides` | Two canonical words, `web_search` and `web_fetch`. | The `paper_` family. |
| `tools` | Two `ToolDef` values, both `Surfaces::Both`, both rate limited. | Several, and a write is not on the model surface for free. |
| Lua bindings | None written here. The core derives `web.search` and `web.fetch` from the canonical names. | Nothing; no extension writes Lua bindings. |
| `holds_section_state` | `false`. A search is a request and a response, so nothing survives the tool call for a nested section to interleave with. | `true`, which serializes `fanout` for every run in the deployment. |
| `validate` | Offline. Credential present, endpoint parses, policy compiles. Never touches the network. | Connects, checks the schema, checks migrations. |
| `on_section` | `Ok(())`. Nothing here has a section-shaped lifetime. | Begin, commit, rollback, savepoint. The whole point of the hook. |
| `row_count` | Zero. This crate writes no rows anywhere, so no declared `rows` output can resolve to it and there is nothing to report. | A real per-run count for the table named, read from the writes it made. |
| `shutdown` | Drops two connection pools. | Closes a pool after rolling back anything open. |

`on_section` is the load-bearing difference and it is worth being precise about why it is empty rather than merely convenient. The section lifecycle exists so an extension holding a resource whose lifetime is a section can open it on `Enter`, commit it on `Complete`, discard it on `Retry`, and nest it on `NestedEnter`. A search is a request and a response. It completes before the tool call returns, it holds nothing afterwards, and it wrote nothing that a rollback could remove. The HTTP connection pool is the only long-lived resource in the crate and its lifetime is the process, not the section: pooling a socket across sections is the point of pooling it. So there is nothing to begin, nothing to commit, and nothing to roll back, and the override is `Ok(())`.

The method is written out explicitly rather than left to the trait default, exactly as `promptforge-ext-classify` writes it out, because a reader of this file should see that the decision was made rather than inherited. The general rule an extension author should take from both files: implement `on_section` if and only if you hold something whose lifetime is a section.

There is one honest asymmetry, and it is the most interesting thing this crate learns about the trait. A rollback restores our side and cannot restore the upstream's. A section that retries three times, each attempt running the same two searches, has spent six requests against a metered monthly quota, and `Retry` gives this crate no way to make that untrue because the requests already happened at a third party. A transactional extension can undo its writes; an extension whose side effect is somebody else's billing meter cannot. Tension: the section lifecycle is a rollback mechanism for local state only, so a retried section is free for the database and costs money at the search provider, and the only control on that is `Limits::max_retries_per_section`.

`shutdown` is the other near-empty method, and it does exactly one thing: it drops the two `reqwest::Client` values, which closes their idle keep-alive sockets. That is the whole method. It exists because a service that is exiting should close its connections rather than leave the peer and the local TCP stack to discover the process is gone. `reqwest::Client` is a cheap handle over shared internals, so dropping one clone releases nothing while the registry still holds others through `Arc<Inner>`; the clients therefore sit in a `RwLock<Option<Client>>` and `shutdown` takes them out. A call arriving after that returns `SearchError::ShutDown` rather than panicking.

`validate`, `on_section`, and `shutdown` are all `async` on the landed trait and this crate awaits nothing inside any of the three, which is the same shape `promptforge-ext-classify` reports and for the same reason: the hooks are straight-line code, so no lock guard ever crosses an await point.

The read lock on every call is the visible cost of that arrangement, and it is free next to a network round trip. This is worth contrasting with `promptforge-ext-classify`, where the per-session mutex is a determinism decision that happens to also give `shutdown` somewhere to take a session from. Here the lock is only about shutdown, because there is no determinism to protect: two concurrent searches may proceed in parallel and there is no batch composition to fix.

The two methods with real content are ordinary. `tools` is two calls to `register_capability`, each capturing `Arc<Inner>`, which is why the state sits in a separate `Inner` behind an `Arc` in the first place: `tools` receives `&self` and cannot hand `self` to a closure. `validate` is a pure function of configuration.

## Dependencies and pins

Every version below was checked against crates.io on 2026-07-25.

- `reqwest` at `0.13.4`, published 2026-05-25. The HTTP client. Chosen over `hyper` directly because redirect policy, transparent decompression, charset decoding, connection pooling, and a pluggable DNS resolver are all load-bearing here and all things `hyper` would leave to us. The version floor matters concretely: 0.13.4's changelog records "Fix redirect handling to strip sensitive headers when the scheme changes", which is precisely the failure mode a fetcher that follows arbitrary redirects has to be right about.
- `url` at `2.5.8`, published 2026-01-05. WHATWG URL parsing. The URL policy is a set of assertions about a parsed URL, and a hand-rolled parser is how a policy gets talked into disagreeing with the client that eventually makes the request. `reqwest` already parses with this crate, so using it directly means the policy inspects the same parse the connector will use.
- `ipnet` at `2.12.0`, published 2026-03-03. CIDR containment for the blocked address ranges. `std::net` has stable `is_loopback`, `is_private`, and `is_link_local` on `Ipv4Addr`, but `is_global`, `Ipv6Addr::is_unique_local`, and `Ipv6Addr::is_unicast_link_local` are not stable, and the ranges that matter here are wider than the stable predicates cover. An explicit CIDR table is also testable one range at a time, which is what `## Tests` requires.
- `mime` at `0.3.17`, published 2023-03-20. Content-type parsing. Old and unchanged because media types are. Matching on `type_()` and `subtype()` is what makes the content-type decision table a match expression rather than a pile of string comparisons.
- `dom_smoothie` at exactly `=0.18.0`, published 2026-06-07. Boilerplate removal, closely following Mozilla's `readability.js`. Chosen over `readability-rs` because that crate is a fork of an unmaintained one, and over writing selectors by hand because "which part of this page is the article" is a scoring heuristic with fifteen years of tuning behind it and no interesting local variant.
- `html2text` at exactly `=0.17.1`, published 2026-04-19. Renders HTML to wrapped plain text. It is not redundant with `dom_smoothie`: `Article::text_content` is concatenated text with every list, table, and heading boundary collapsed, which reads badly and is exactly what a model needs preserved. `html2text` renders the cleaned HTML in `Article::content` into text that keeps list structure, table cells, and heading levels. Its MSRV of 1.85 sets the crate's Rust floor.
- `encoding_rs` at `0.8.35`, published 2024-10-24. Decoding a declared non-UTF-8 charset. It is already in the dependency graph because `reqwest`'s `charset` feature uses it, so naming it directly adds a line to `Cargo.toml` and nothing to the build.
- `promptforge`, `serde`, `serde_json`, `schemars`, `thiserror`, `tokio`, `tracing`, and `humantime_serde` from the workspace, at whatever the workspace pins. Notably not `mlua`: the core owns every Lua binding.

Two crates take exact `=` pins and the rest take caret requirements, which is the opposite habit from `promptforge-ext-classify` and for a different reason. `dom_smoothie` and `html2text` are both pre-1.0 with a long history of breaking releases, and both are compared against golden files: their output *is* the crate's observable behaviour on the fetch path. A caret bump that improves extraction is indistinguishable at build time from one that regresses it, and either way it rewrites every golden file in the test suite. Pinning them exactly makes an extraction change a deliberate commit with a diff to review. Everything else is stable, semver-respecting, and pinned by the committed workspace `Cargo.lock` rather than by the manifest.

```toml
[dependencies]
promptforge = { path = "../promptforge" }
reqwest = { version = "0.13.4", default-features = false, features = ["rustls-tls", "gzip", "brotli", "json", "charset", "stream"] }
url = "2.5.8"
ipnet = "2.12.0"
mime = "0.3.17"
dom_smoothie = { version = "=0.18.0", default-features = false }
html2text = { version = "=0.17.1", default-features = false }
encoding_rs = "0.8.35"
serde = { workspace = true }
serde_json = { workspace = true }
schemars = { workspace = true }
thiserror = { workspace = true }
tokio = { workspace = true }
tracing = { workspace = true }
humantime_serde = { workspace = true }
```

`default-features = false` on `reqwest` and then an explicit feature list, because every feature here is a decision and two of the defaults are wrong:

- `rustls-tls` rather than `native-tls`, so the build needs no OpenSSL and the binary carries its own TLS. Single-binary distribution is the reason the project is in Rust at all.
- `gzip` and `brotli` for transparent decompression. Brave's own documentation asks for `Accept-Encoding: gzip`, and on the fetch path compression is most of the wire cost of a large page. This interacts with the size cap and the interaction is not incidental: the cap counts decompressed bytes, so a decompression bomb is caught. See `## web_fetch`.
- `json` for the provider response.
- `charset` so `encoding_rs` is present and a declared charset can be honoured.
- `stream` for `bytes_stream`, which is what makes the size cap enforceable before the body is fully in memory rather than after.
- No `cookies`. The fetch client holds no cookie store, so no fetch carries ambient credentials and no fetched host can set state that a later fetch replays. This is a security decision, not an omission.
- No `hickory-dns`. The resolver is ours. See `## URL policy and SSRF defence`.
- No `http3`.

## The `Extension` impl

The trait is `promptforge::Extension`, reproduced from `design-core.md` without modification. `SearchExt` implements all eight methods, including all four the trait defaults.

```rust
pub struct SearchExt {
    /// Shared with every `ToolFn` this extension hands to the registry.
    inner: Arc<Inner>,
    /// Owned storage so `provides` can return a slice.
    names: Vec<ToolName>,
}

struct Inner {
    /// From the `[extensions.NAME]` block key. This is what `Extension::name` returns
    /// and what a `[tools]` binding names.
    name: String,
    /// The search backend, selected by that same block key.
    provider: Arc<dyn SearchProvider>,
    /// Talks only to the provider endpoint. Carries the API key. Follows no redirect.
    search_http: RwLock<Option<reqwest::Client>>,
    /// Talks to arbitrary hosts. Carries no credential and no cookie store.
    fetch_http: RwLock<Option<reqwest::Client>>,
    /// Serialises provider requests to at most one per `min_interval`.
    throttle: Mutex<Option<Instant>>,
    policy: Arc<UrlPolicy>,
    fetch: FetchPolicy,
    search: SearchDefaults,
}

impl SearchExt {
    /// Builds both clients eagerly. The host calls this while loading configuration.
    pub fn new(cfg: &SearchConfig) -> Result<Self, SearchError>;
}
```

Both clients install the guarded resolver of `## URL policy and SSRF defence`, so no request either of them makes can reach a blocked address. Two clients rather than one, and the reason is a credential-containment reason rather than a tidiness one. The provider client sets `X-Subscription-Token` and must never follow a redirect off the provider host, because a default credential header on a client that follows arbitrary redirects is how an API key ends up in somebody else's access log. The fetch client must send no credential at all, must hold no cookie, and must follow up to five redirects with the URL policy re-checked at every hop. Those two configurations are not merely different, they are incompatible, and the cost of collapsing them is a leaked key. Tension: two pools instead of one, which is two sets of idle sockets and the reason `shutdown` has two things to drop.

Clients are built in `new`, not lazily on first call, for the same reason `promptforge-ext-classify` builds sessions in `new`: the trait gives `validate` only `&self`, and a client built on first use first fails on whichever section happened to search first.

```rust
impl Extension for SearchExt {
    fn name(&self) -> &str {
        &self.inner.name
    }

    fn provides(&self) -> &[ToolName] {
        &self.names
    }

    fn tools(&self) -> Vec<ToolDef> {
        vec![
            search_def(self.inner.clone()),
            fetch_def(self.inner.clone()),
        ]
    }

    // No bind_lua. The core builds `web.search` and `web.fetch` from the two
    // canonical names above, because both declare Surfaces::Both. This crate
    // does not depend on mlua and constructs no Lua value.

    async fn validate(&self) -> Result<(), ExtError> {
        self.inner.provider.validate_credential()?;
        self.inner.policy.compile_check()?;
        self.inner.policy.check_endpoint(self.inner.provider.endpoint())?;
        self.inner.fetch.check_bounds()?;
        if self.inner.search.probe_at_boot {
            self.probe()?;
        }
        Ok(())
    }

    /// Stateless. Nothing here has a section-shaped lifetime, so there is nothing
    /// to begin, commit, or roll back. See `## The stateless reference case`.
    async fn on_section(&self, _ev: &SectionEvent) -> Result<(), ExtError> {
        Ok(())
    }

    /// Drops both connection pools, closing their idle sockets. That is all it does.
    async fn shutdown(&self) -> Result<(), ExtError> {
        let _ = self.inner.search_http.write().take();
        let _ = self.inner.fetch_http.write().take();
        Ok(())
    }
}
```

`name` returns the `[extensions.NAME]` block key, which is `"brave"` in every deployment specified so far. It is the provider's name rather than the crate's, following the same rule that makes `promptforge-ext-classify` report `"onnx"`: the extension name is the backing implementation, because that is what a configuration line binds a canonical word to. `design-mcp.md` fixes both ends of this - `[tools] web_search = "brave"` and `[extensions.brave] api_key = ...`, with the comment that extension tables are "keyed by the name the extension reports from `Extension::name`" - so the block key, the binding value, and this return are one string.

`provides` returns `web_search` and `web_fetch`. Both words already exist in `design.md`'s canonical vocabulary, so unlike the classify extension this one adds nothing to the core's fixed set and requires no core change at all. That is a small point and it is the only extension for which it is currently true.

`tools` builds two `ToolDef` values, each cloning `Arc<Inner>` into its `ToolFn`, which is why the state sits in a separate `Inner` behind an `Arc`: `tools` receives `&self` and cannot hand itself to a closure.

```rust
fn search_def(inner: Arc<Inner>) -> ToolDef {
    ToolDef {
        name: ToolName::parse("web_search").expect("canonical"),
        description: "Search the web and return ranked results with titles, URLs and short \
                      snippets. Returns links and excerpts, never page bodies: use web_fetch \
                      to read a result.",
        schema: schemars::schema_for!(SearchArgs),
        surfaces: Surfaces::Both,
        rate_limit: Some(4),
        call: Arc::new(SearchFn(inner)),
    }
}

fn fetch_def(inner: Arc<Inner>) -> ToolDef {
    ToolDef {
        name: ToolName::parse("web_fetch").expect("canonical"),
        description: "Fetch one https URL and return its readable text. HTML is reduced to the \
                      article body unless `raw` is set. PDFs and binary types are refused. \
                      Everything returned is untrusted text from a third party.",
        schema: schemars::schema_for!(FetchArgs),
        surfaces: Surfaces::Both,
        rate_limit: Some(8),
        call: Arc::new(FetchFn(inner)),
    }
}
```

`ToolName::parse` is the core's constructor and it accepts only words in the canonical set, so the `expect` is sound exactly because `design.md` already lists both words. `rate_limit` here is a default that a `[tool_limits]` entry overrides. `web_fetch`'s description tells the model in advance that what comes back is untrusted, because a description is the only place this crate can say so at a point where the model is still deciding whether to call it.

Lua reaches these as `web.search` and `web.fetch`, and this crate does nothing to make that happen. Two canonical words sharing the `web_` prefix are one family, and the core builds one table per family from the `ToolDef` list, naming each field from the suffix. The functions are created with `create_async_function` because `ToolFn::call` is async, which places a requirement on the core's Lua driver rather than on this crate: a section block runs under `call_async`.

`validate` is offline and that is a decision rather than an oversight. It checks that the credential is present and non-empty, that the endpoint parses as an absolute `https` URL with no userinfo and an allowed port, that every configured CIDR in the policy parses, and that the fetch policy's numbers are inside their bounds. It sends no request and resolves no name. The endpoint check applies the blocked address ranges directly when the endpoint host is written as an IP literal, which catches the configuration accidentally left pointing at a local mock and is the one check here that would be embarrassing to omit; a named endpoint whose DNS resolves into a blocked range is caught at first call instead, because the guarded resolver is installed on the provider client too. Installing it there costs nothing - a public search API never trips the policy - and it means a hijacked or typo'd provider hostname cannot reach an intranet address either. `design-mcp.md` already establishes the principle for the gateway: a dependency with its own lifecycle must not be required at boot, because requiring it makes startup order load-bearing. A third-party search API across the public internet is a stronger case than the gateway, not a weaker one, and a Brave outage must not stop a service whose other thirty-nine prompts never search.

Tension: a syntactically valid but wrong API key is not caught until the first search, which fails a run mid-flight with what is really a configuration error. `probe_at_boot = true` is offered for deployments that would rather fail at boot, and it defaults to false because the failure it prevents is rarer than the outage it would cause.

## `Surfaces::Both`, and what it costs

Both functions declare `Surfaces::Both`. The model may call them inside the tool-call loop and a Lua block may call them at a section boundary. This is the opposite declaration from `promptforge-ext-classify`, which declares `LuaOnly` for all four of its operations, and the difference is not a matter of taste.

A classifier call is deterministic logic the author already decided on. The runtime makes it during section configuration or in a postcondition, the answer follows from the arguments, and putting it on the model surface would spend instruction budget on a choice nobody is choosing. A search is the other thing entirely. Which query to run next, given what the last one returned, is a judgement call with no script that captures it, and a tool-call loop is the mechanism that exists for judgement calls. Forcing search into Lua would mean the prompt author writing the search strategy in advance, which is exactly the case where a model beats a script.

The Lua side is equally real and is not a convenience. A section that needs a candidate list before its model turn begins should build that list itself and hand it over:

```lua
model("fast")
tools.add("web_search", "web_fetch", "add_statement", "done")

-- Assemble the candidate set before the model turn, so the model starts with
-- the list instead of spending three turns discovering it.
local hits = web.search{ query = params.entity .. " P2300 sender receiver", count = 20, freshness = "year" }

local lines = {}
for _, hit in ipairs(hits.results) do
  if hit.site == "lists.isocpp.org" or hit.site == "open-std.org" then
    lines[#lines + 1] = string.format("%s  %s", hit.url, hit.title)
  end
end

assert(#lines > 0, "no committee-hosted sources found for this entity")
context.inject("Candidate sources:\n" .. table.concat(lines, "\n"))
```

That block filters by host and refuses the section when nothing survives, which is a precondition a model cannot express and should not have to. The model in the same section still holds `web_search` and `web_fetch`, so it can follow a thread the author did not anticipate. Both surfaces, both used, in one section.

`Both` costs four things and they should be named.

- Two schemas in the model's context in every section that adds them. `web_fetch`'s schema is small; `web_search`'s carries six optional fields. That is the price of the model being able to choose freshness and result count rather than living with a default.
- Two callers with different failure expectations, which is the tension `design.md` names for the dual-surface mechanism generally. A Lua caller wants an error that fails or skips a section; a model caller wants prose it can act on. One `SearchError` serves both because the Lua binding raises it and the core renders it into tool-result text, which is why every message in `## Errors` is written to be actionable in the second person.
- A section's tool-call budget is spendable on searching. A section capped at twenty tool calls that spends fifteen searching has five left to file what it found. That is the author's problem and `tools.add` is where it is solved.
- The security cost, which is the real one. `web_fetch` on the model surface means the URL comes from a model that may have just read an attacker-controlled page. Every control in the next section exists because of this one declaration. Were `web_fetch` declared `LuaOnly`, its URLs would come from a prompt author's script and the URL policy would be defence in depth. It is `Both`, so the URL policy is the primary control and has to be written as one.

## `web_search`

```rust
#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct SearchArgs {
    /// The query. One to four hundred characters and at most fifty words.
    pub query: String,
    /// Results to return, 1 to 20. Defaults to the configured `default_count`.
    #[serde(default)]
    pub count: Option<u8>,
    /// Zero-based page offset, 0 to 9.
    #[serde(default)]
    pub offset: Option<u8>,
    /// Restrict results by age.
    #[serde(default)]
    pub freshness: Option<Freshness>,
    /// Restrict results to one registrable domain, "open-std.org".
    #[serde(default)]
    pub site: Option<String>,
    /// Two-letter language code. Defaults to the configured `search_lang`.
    #[serde(default)]
    pub lang: Option<String>,
}

#[derive(Deserialize, JsonSchema)]
#[serde(rename_all = "lowercase")]
pub enum Freshness { Day, Week, Month, Year }
```

`deny_unknown_fields` is what converts a hallucinated argument name into a diagnostic that names the field, on both surfaces: a model inventing `num_results` and a Lua author typo'ing `frehsness` both get told which key was wrong instead of being silently ignored.

`register_capability` derives this schema through `schemars`, and it is worth showing what the model actually receives, because the doc comments above are the descriptions the model reads:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "SearchArgs",
  "type": "object",
  "additionalProperties": false,
  "required": ["query"],
  "properties": {
    "query": {
      "description": "The query. One to four hundred characters and at most fifty words.",
      "type": "string"
    },
    "count": {
      "description": "Results to return, 1 to 20. Defaults to the configured `default_count`.",
      "type": ["integer", "null"],
      "format": "uint8",
      "minimum": 0,
      "maximum": 255
    },
    "offset": {
      "description": "Zero-based page offset, 0 to 9.",
      "type": ["integer", "null"],
      "format": "uint8",
      "minimum": 0,
      "maximum": 255
    },
    "freshness": {
      "description": "Restrict results by age.",
      "anyOf": [
        { "type": "string", "enum": ["day", "week", "month", "year"] },
        { "type": "null" }
      ]
    },
    "site": {
      "description": "Restrict results to one registrable domain, \"open-std.org\".",
      "type": ["string", "null"]
    },
    "lang": {
      "description": "Two-letter language code. Defaults to the configured `search_lang`.",
      "type": ["string", "null"]
    }
  }
}
```

Note what the derived schema does not carry: `count`'s real range is 1 to 20 and the schema says 0 to 255, because `u8` is what `schemars` sees. Ranges are enforced in Rust and stated in the description, and the description is the part the model reads. Adding `schemars` range attributes would tighten the schema and would still not be the enforcement point, because the Lua surface does not validate against the schema's numeric bounds. One enforcement point in Rust, one advisory statement in prose. Tension: a model that ignores the description sends `count = 50` and gets a terminal argument error instead of a clamp, which is deliberate - silently clamping teaches the model nothing and makes the result shape a surprise.

### Result shape

```rust
#[derive(Serialize, JsonSchema)]
pub struct SearchResult {
    /// The query as sent upstream, after `site` folding. Not the model's raw input.
    pub query: String,
    /// The provider that answered, which is `Extension::name`.
    pub provider: String,
    pub count: usize,
    pub results: Vec<Hit>,
}

#[derive(Serialize, JsonSchema)]
pub struct Hit {
    /// One-based, in the provider's order. Never reordered here.
    pub rank: u32,
    pub title: String,
    pub url: String,
    /// The provider's snippet, plain text, tags stripped.
    pub snippet: String,
    /// Registrable host, so Lua can filter by source without parsing a URL.
    pub site: String,
    /// The page's own date as an RFC 3339 date, when the provider supplied one
    /// that parses. Absent otherwise.
    pub age: Option<String>,
}
```

Four decisions in that shape.

`rank` is one-based and preserves the provider's order without reordering. A reranked set is `classify.rank` applied to these hits, which is a separate call the author makes deliberately, and silently reordering here would make that call impossible to reason about.

`site` is precomputed because the Lua filtering above is the common case and `string.match` over a URL in a Luau sandbox is how a prompt author writes a subtly wrong host check.

`age` is normalised or absent, never passed through. Brave's `page_age` is a mix of formats and free text. A model reasoning about freshness from an inconsistent string is worse off than one reasoning from a missing field, because the missing field is obviously missing.

`snippet` has provider markup stripped. Brave returns `<strong>` around matched terms, and highlight markup inside a field a model treats as prose is noise at best and an injection surface at worst.

### The provider abstraction

```rust
#[async_trait]
pub trait SearchProvider: Send + Sync {
    /// Provider identity, matching the `[extensions.NAME]` block that selected it.
    fn id(&self) -> &'static str;

    /// Absolute base URL, checked against the URL policy at `validate` time.
    fn endpoint(&self) -> &Url;

    /// The provider's own ceiling on results per request. Brave is 20.
    fn max_count(&self) -> u8;

    /// The provider's own ceiling on paging. Brave is 9.
    fn max_offset(&self) -> u8;

    /// Longest query the provider accepts, in characters. Brave is 400.
    fn max_query_chars(&self) -> usize;

    /// Boot-time credential check. No network.
    fn validate_credential(&self) -> Result<(), SearchError>;

    /// One request. The client is supplied so there is one pool and one place
    /// the credential header is attached.
    async fn search(&self, q: &Query, http: &reqwest::Client) -> Result<Vec<Hit>, SearchError>;
}

/// The crate's own query vocabulary, which is what the trait insulates.
pub struct Query {
    pub text: String,
    pub count: u8,
    pub offset: u8,
    pub freshness: Option<Freshness>,
    pub site: Option<String>,
    pub lang: String,
    pub country: String,
}
```

`BraveProvider` is the one implementation. It issues `GET {endpoint}/web/search` with `q`, `count`, `offset`, `country`, `search_lang`, `result_filter=web`, and `freshness` mapped from our vocabulary to Brave's `pd`, `pw`, `pm`, `py`. The credential goes on the request as `X-Subscription-Token` rather than as a client default header, for the containment reason above. `site` folds into the query text as `site:example.org` because Brave has no separate parameter for it, and that folding is exactly the kind of provider-specific translation the trait exists to hide. Only `web.results` is read; `mixed`, `news`, `videos`, `infobox`, and `discussions` are ignored, and `result_filter=web` asks the provider not to compute them.

Response parsing is deliberately loose in one direction and strict in the other. Unknown fields in the provider's JSON are ignored, because a provider adds fields without notice and a build that broke on the addition would break on a Tuesday for no reason. A missing or renamed field this crate depends on is `SearchError::ProviderShape` with the field named, because that is a real incompatibility and a silently empty result set is worse than a loud failure. A `200` whose body is HTML rather than JSON - a captive portal, a proxy error page - is `ProviderShape` too, and not a panic.

Adding a provider is a rebuild, and `design.md` records that as the accepted cost of not federating search over MCP. Concretely, adding Google costs: one `impl SearchProvider`, one match arm mapping a block key to it, one `[extensions.google]` block, one recorded response fixture, a rebuild, and a release. The trait bounds that work to two files; it does not turn it into a configuration line. Tension: a deployment that wants a different search engine on Friday waits for a release, and the only in-configuration alternative is `design-mcp.md`'s `[[mcp_clients]]` path, which reaches a remote provider through an entirely different extension and pays a process hop to do it.

The trait has one known weak joint, named here rather than discovered later. `offset` assumes page-number paging. Brave pages that way and caps at nine. Google's Custom Search pages by a one-based `start` index, which maps cleanly enough, and a provider that pages by an opaque cursor does not map at all: it would need `Query` to carry a cursor and `SearchResult` to return the next one, which is a trait change. The trait is honest about the providers it was designed against and no more.

## `web_fetch`

```rust
#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct FetchArgs {
    /// Absolute https URL of a page to read as text.
    pub url: String,
    /// Cap on returned characters. Defaults to the configured `max_chars`.
    #[serde(default)]
    pub max_chars: Option<usize>,
    /// Skip article extraction and render the whole document. Use for pages that
    /// are mostly tables or lists, where extraction discards the content.
    #[serde(default)]
    pub raw: bool,
}
```

```rust
#[derive(Serialize, JsonSchema)]
pub struct FetchResult {
    /// The URL that actually answered, after redirects.
    pub url: String,
    /// The URL as requested, present only when it differs from `url`.
    pub requested: Option<String>,
    pub status: u16,
    pub content_type: String,
    pub title: Option<String>,
    pub byline: Option<String>,
    /// The document's own publication date, from its metadata, when it parses.
    pub published: Option<String>,
    pub text: String,
    pub chars: usize,
    /// Set when `max_chars` cut the text short. The text is a prefix.
    pub truncated: bool,
    /// How `text` was produced.
    pub extraction: Extraction,
    /// Every hop, in order, when there were redirects.
    pub redirects: Vec<String>,
}

#[derive(Serialize, JsonSchema)]
#[serde(rename_all = "snake_case")]
pub enum Extraction {
    /// `dom_smoothie` found an article and `html2text` rendered it.
    Readability,
    /// `html2text` rendered the whole document, either because `raw` was set or
    /// because extraction found nothing.
    RawHtml,
    /// The response was already text and was decoded, not extracted.
    Plain,
}
```

`url` is the final URL and `requested` records the original only when they differ, because the provenance of a quotation is where the bytes came from and not where the model aimed. `extraction` is on the result because "this text is what readability kept" and "this text is the whole page" are different claims about completeness, and a model asked to confirm something absent should be able to tell which one it got.

### Content type

The `Content-Type` header decides everything, and it is trusted for routing while being trusted for nothing else.

| Content type | Handling |
|---|---|
| `text/html`, `application/xhtml+xml` | Extract with `dom_smoothie`, render with `html2text`. `Extraction::Readability`. |
| `text/plain`, `text/markdown`, `text/csv`, any other `text/*` | Decode, no extraction. `Extraction::Plain`. |
| `application/json`, `application/xml`, `text/xml`, any `+json` or `+xml` suffix | Decode verbatim. `Extraction::Plain`. Feeds RSS, Atom, and JSON APIs, all of which a research prompt legitimately reads. |
| `application/pdf` | `SearchError::UnsupportedContentType`. |
| anything else, including `application/octet-stream`, `image/*`, `audio/*`, `video/*`, archives | `SearchError::UnsupportedContentType`. |
| absent | `SearchError::NoContentType`. |

An absent `Content-Type` is refused rather than sniffed. Content sniffing is how a fetcher gets talked into treating a binary as text, and refusing produces a message the model can act on. Practically every HTTP server sends the header, so the cost is near zero.

**A PDF is refused.** No PDF text extraction is compiled in. The message names the content type and tells the model to look for an HTML version. Three reasons, and the domain one is the strongest: WG21 papers are the PDFs this system cares about, and paper text enters through the ingestion pipeline into `promptforge-ext-paperstore`, which is where paper content belongs and where it arrives already parsed, chunked, and addressable. A second, worse PDF path through `web_fetch` would produce text of unknown quality that no prompt should be reasoning over when the good copy is one `paper_` call away. Beyond that, PDF text extraction is a large dependency with output quality that varies from clean to unusable depending on how the file was produced, and a model cannot tell which it got. Tension: a document published only as a PDF and not in paperstore cannot be read by a prompt at all, which is a real gap for anything outside the committee corpus, and closing it means either a PDF crate here or an ingestion step there.

Charset comes from the `charset` parameter. UTF-8 or absent decodes as UTF-8, replacing invalid sequences rather than failing, because one bad byte in a long document should not lose the document. A declared non-UTF-8 charset goes through `encoding_rs`; an unrecognised charset label is `SearchError::Undecodable` with the label named. An HTML `<meta charset>` that disagrees with the header is ignored: the header wins, and the disagreement is logged.

### HTML to text

Three steps, and the middle one is why two crates are in the dependency list.

1. `dom_smoothie`'s `Readability` scores the DOM and returns an `Article`, whose `title`, `byline`, and `published_time` become the corresponding result fields and whose `content` is cleaned HTML with navigation, sidebars, and footers removed.
2. `html2text` renders that cleaned HTML into plain text wrapped at 100 columns, preserving heading levels, list markers, and table cells. `Article::text_content` is not used, because it is concatenated text with every structural boundary collapsed, and a standards document whose meaning is carried by a table becomes an unreadable run of cell values.
3. Link targets are appended as bracketed footnotes rather than inlined, so a model can follow a reference with `web_fetch` without the prose being cut apart by URLs.

`raw = true` skips step one and renders the original document. This exists because readability is tuned for articles and is wrong for exactly the pages this project reads most: the WG21 papers index is a large table with almost no prose, and article extraction discards the table and keeps a heading. A model has no way to know which mode a page needs before fetching it, which makes `raw` an argument rather than a heuristic, and makes the two-call pattern - fetch, see that the text is a heading and nothing else, fetch again with `raw` - the honest way to handle an unfamiliar page. When extraction returns nothing usable, the crate falls back to the raw rendering by itself and reports `Extraction::RawHtml`, so the two-call pattern is the exception rather than the rule. Tension: the fallback makes the failure invisible unless the caller reads `extraction`, and a genuinely empty page and a page that defeated the extractor produce the same field value.

### Size caps

Three caps, at three different points, because they defend against three different things.

- `Content-Length`, when present and larger than `max_bytes`, refuses before a body byte is read. This is the cheap case and it saves the bandwidth.
- The body stream is counted as it arrives and aborted at `max_bytes`, default 8 MiB. The count is of decompressed bytes, because `reqwest` decompresses in the stream, which means a gzip bomb declaring one kilobyte on the wire and expanding to a gigabyte is caught by the same counter as an honestly large page. Counting wire bytes instead would have left that hole open.
- `max_chars`, default 40,000, caps the extracted text after extraction.

**A 40 MB page fails.** It does not return truncated. `SearchError::TooLarge` names the URL and the cap. The reason is specific to HTML: a document cut off at 8 MiB stops mid-tag, and readability on a truncated tree produces confident, well-formed text from whichever fragment happened to parse, which a model cannot distinguish from a complete page. An incomplete document that looks complete is worse than no document.

Plain text is different and is treated differently: a prefix of a plain text file is a legitimate prefix, so `text/*` and the JSON and XML types truncate at `max_bytes` and return with `truncated: true`. So the rule is that structured formats are all-or-nothing and flat formats truncate, and the distinction is whether a prefix is still valid in the format.

`max_chars` truncation is always a success with `truncated: true`, since by then the document has been parsed as a whole and the text being cut is text. Truncation is on a character boundary and, where one exists within the last 200 characters, on a paragraph boundary. 40,000 characters is roughly ten thousand tokens, which is a large but not run-destroying share of a section's context, and the model is told it was cut so it can narrow its next fetch.

### Redirects and timeouts

`reqwest::redirect::Policy::custom` runs the URL policy on every hop. A hop that fails the policy stops the request with `SearchError::RedirectRefused`, naming both ends and the reason, and no body is read. Refused specifically: a scheme change from `https` to `http`, a host that fails the policy, a port outside the allowed set, and a hop to an address in a blocked range. The last of those is the important one, because a public host redirecting to `http://127.0.0.1:8080/admin` is the shortest SSRF payload there is and a naive fetcher that checked only the URL it was handed follows it happily.

**A redirect loop fails at five hops** with `SearchError::TooManyRedirects`, and the error carries the chain so a reader sees the loop rather than inferring it. `max_redirects` defaults to 5. There is no cycle detection, deliberately: a legitimate chain can revisit a URL - a bounce to a canonical form after a locale redirect does exactly that - so cycle detection would need an exception list to be correct, while a hop count is both simpler and sufficient. Five is enough for every legitimate chain observed in this domain and the failure mode of being one hop short is a clear error rather than a wrong answer.

Timeouts are two numbers and one bound taken from the core:

- `connect_timeout`, default 5 seconds, which covers DNS plus TCP plus TLS.
- `timeout`, default 20 seconds, total including the body read, which is what catches a server dribbling bytes indefinitely.
- `CallCtx::deadline`, which the core supplies. The effective per-request timeout is the smaller of the configured value and the time remaining until that deadline. A tool that ignores `deadline` can outlive the run that called it, and a run that has fourteen seconds left must not start a twenty-second fetch. When the remaining budget is under one second the call returns `SearchError::NoTimeBudget` without opening a socket, because spending a permit and a connection on a request that cannot finish is worse than failing immediately.

## URL policy and SSRF defence

This is the crate's most security-sensitive surface, and the reason is the `Surfaces::Both` declaration: `web_fetch` takes a URL chosen by a model that may have just read a page an attacker wrote. The URL policy is therefore the primary control and not defence in depth, and it is written in Rust where neither a prompt author nor a model can weaken it.

### The URL itself

Checked before anything is resolved, on the `url::Url` parse that the client will also use.

- **Scheme allowlist**, not a blocklist. `https` always; `http` only when `allow_http = true`, which a production deployment leaves false. Everything else is refused by not being on the list, which covers `file`, `ftp`, `gopher`, `data`, `blob`, `javascript`, `ws`, `wss`, `chrome`, `about`, and whatever the next one is. A blocklist here is a promise to have thought of every scheme, and nobody has.
- **No userinfo.** `https://user:pass@host/` is refused outright. It is the classic parser-confusion vector, since the parts before and after the `@` are read differently by different parsers, and no legitimate document fetch needs it.
- **Port allowlist**, default `[80, 443]`. Widened by configuration, never by an argument. This removes internal port scanning as a capability even in the event that an address check is somehow satisfied.
- **No bare IP literals**, default. Every public document has a name, and a bare address is the shape of a probe rather than of a citation. This also removes the whole family of literal-encoding tricks - octal `0177.0.0.1`, decimal `2130706433`, IPv4-mapped `[::ffff:127.0.0.1]` - in one rule, without depending on the parser normalising each of them the way we assumed.
- **No fragment, and query strings passed through unchanged.** The fragment is dropped because it never reaches the server. The query is untouched, which is the honest limit noted below.

### The blocked address ranges

Checked against every resolved address, IPv4 and IPv6, as CIDR containment.

IPv4:

- `0.0.0.0/8` - this network, and the unspecified address
- `10.0.0.0/8` - RFC 1918 private
- `100.64.0.0/10` - RFC 6598 carrier-grade NAT
- `127.0.0.0/8` - loopback, the whole block and not just `127.0.0.1`
- `169.254.0.0/16` - link-local, which is where cloud instance metadata lives at `169.254.169.254`
- `172.16.0.0/12` - RFC 1918 private
- `192.0.0.0/24` - IETF protocol assignments
- `192.0.2.0/24` - TEST-NET-1
- `192.88.99.0/24` - 6to4 relay anycast
- `192.168.0.0/16` - RFC 1918 private
- `198.18.0.0/15` - benchmarking
- `198.51.100.0/24` - TEST-NET-2
- `203.0.113.0/24` - TEST-NET-3
- `224.0.0.0/4` - multicast
- `240.0.0.0/4` - reserved
- `255.255.255.255/32` - broadcast

IPv6:

- `::/128` - unspecified
- `::1/128` - loopback
- `::ffff:0:0/96` - IPv4-mapped, which is loopback and RFC 1918 wearing a v6 hat and is the range most often forgotten
- `64:ff9b::/96` and `64:ff9b:1::/48` - NAT64, which translates to a v4 address the v6 check would otherwise never see
- `100::/64` - discard-only
- `2001:db8::/32` - documentation
- `2002::/16` - 6to4
- `fc00::/7` - unique local
- `fe80::/10` - link-local
- `ff00::/8` - multicast

`deny_extra` adds deployment-specific CIDRs, for a firewalled intranet that owns public address space. `allow_exact` is the escape hatch and takes a host plus an exact address, never a range, so a deliberate hole cannot accidentally become a subnet. It defaults to empty and an entry in it is the only supported way to fetch an intranet document. Tension: `allow_exact` is a hole in the control that matters most, and its existence is justified only by the alternative being a deployment that disables the policy wholesale.

For this system the ranges above already cover the interesting targets without any `deny_extra` entry, which is worth stating: `design-mcp.md`'s own configuration puts the paperstore Postgres at `10.0.0.11` and a peer MCP service at `10.0.0.30`, both inside RFC 1918, and the gateway, the MCP server's own bind address, and the Django site are all on the same intranet or on loopback. The default policy is not abstract hygiene here; it is what stops `web_fetch` from reading this system's own configuration surfaces.

### DNS rebinding

The naive arrangement is to parse the URL, resolve the host, check the addresses, and then hand the URL to the client. That has a time-of-check to time-of-use window: the client resolves again when it connects, and a name whose record has a one-second TTL can answer publicly for the check and privately for the connection. Closing that window by checking harder does not work, because the check and the connection are two different resolutions no matter how close together they happen.

The fix is to make them one resolution. The check moves *inside* the resolver, so the only addresses the connector can ever receive are addresses that passed.

```rust
pub struct GuardedResolver {
    policy: Arc<UrlPolicy>,
}

impl Resolve for GuardedResolver {
    fn resolve(&self, name: Name) -> Resolving {
        let policy = self.policy.clone();
        let host = name.as_str().to_owned();
        Box::pin(async move {
            let answered: Vec<SocketAddr> = tokio::net::lookup_host((host.as_str(), 0))
                .await
                .map_err(|e| Box::new(SearchError::Dns { host: host.clone(), reason: e.to_string() }) as _)?
                .collect();

            // Filter rather than reject: a name answering with one public and one
            // private address yields only the public one, so a connector retry
            // cannot fall through to the private answer.
            let kept: Vec<SocketAddr> = answered
                .iter()
                .copied()
                .filter(|a| policy.addr_allowed(a.ip()))
                .collect();

            if kept.is_empty() {
                let first = answered.first().map(|a| a.ip());
                return Err(Box::new(match first {
                    Some(ip) => SearchError::BlockedAddress {
                        host,
                        addr: ip,
                        range: policy.matching_range(ip).to_string(),
                    },
                    None => SearchError::NoAllowedAddress { host },
                }) as _);
            }
            Ok(Box::new(kept.into_iter()) as Addrs)
        })
    }
}
```

Three properties follow, and they are the whole defence.

- **There is no cached verdict to rebind against.** The policy is applied at the moment of resolution, and resolution happens per connection attempt. A name that was public a second ago is re-evaluated, not remembered.
- **Filtering beats checking.** A host answering with a mix of public and private addresses is the multi-answer variant of the same attack: a policy that checks the first answer and then hands the name onward lets the connector try the second. Returning only the addresses that passed means the connector has nothing else to try.
- **An all-blocked answer is a hard error naming the host**, not an empty address list that the client would report as an ordinary connection failure. The distinction matters because the two produce different messages to the model and only one of them is honest.

`tokio::net::lookup_host` rather than `hickory-resolver`: it uses the platform resolver, so `/etc/hosts`, Windows name resolution, and the intranet's own search domains behave as the rest of the host does, and there is no second DNS implementation with its own cache to reason about. `reqwest`'s `hickory-dns` feature is therefore off.

One residual gap, stated rather than glossed. `reqwest`'s connection pool reuses an established connection for a later request to the same host without re-resolving. A second `web_fetch` to a host fetched moments ago may therefore ride a socket to an address that was legal when the socket opened. That is not a bypass - the address passed the policy at connect time and a peer does not become a different machine - but it does mean the *freshest* possible verdict is not applied to every request. `pool_idle_timeout` is set to 10 seconds on the fetch client to bound how stale a reused socket can be. Tension: a shorter idle timeout means more TLS handshakes on a prompt that fetches ten pages from one host, which is the cost paid for that bound.

### Untrusted content and exfiltration

`design-core.md` specifies virtual files as the sandbox: a section reading untrusted text while holding only virtual-file tools has no real path to traverse and no exfiltration channel, which removes two legs of the private-data-plus-untrusted-content-plus-exfiltration problem at once. Its stated tension is that the guarantee holds only if such a section is also denied any tool that shells out.

`web_fetch` is that tool. Not because it shells out, but because a URL is an outbound channel with an attacker-controlled host, path, and query string, and a model that has read a poisoned page can be induced to put run data into one. Everything `web_fetch` returns is untrusted, and the model choosing the next URL from what it just read is precisely the loop the virtual-files sandbox was closing.

What this crate does about it:

- **No credential leaves on a fetch.** No cookie store, no `Authorization` header, no bearer token, no API key, no configured secret of any kind on the fetch client. There is nothing worth stealing riding on the request itself, which removes the cheapest version of the attack.
- **The URL policy caps reach.** A fabricated URL cannot name a scheme that reads a local file, a port that reaches an internal service, or an address inside the intranet.
- **The redirect policy re-checks every hop**, so a public host cannot launder a request to an internal one.
- **The query string is not sanitised.** This is the honest limit and it should not be dressed up. A model that has read a poisoned page can put run data in a query string and this crate will send it to a legal public host, because a query string is indistinguishable from a legitimate search URL. No amount of URL policy fixes this, since the destination is genuinely public and the payload is genuinely a query.

The control that does work is a prompt-author control and belongs restated here because this is the crate that makes it necessary: a section that reads untrusted text should not hold `web_fetch` in the same section that holds private data. Per-section tool scoping is the mechanism - `goto` to a section whose Lua block calls `tools.add` without `web_fetch`, and the context is cleared on the way in as well. Tension: neither the core nor this crate can check that an author did it, `Surfaces::Both` is what makes `web_fetch` reachable by the model at all, and so the full cost of that declaration lands on a convention rather than on a mechanism.

One thing deliberately not added: a per-run fetch budget. It would need a run-scoped counter, which would make this extension stateful and give `on_section` real work, which is exactly the property this crate exists to demonstrate is optional. `Limits::max_tool_calls_per_section` already bounds a section. Tension: a run that jumps between four fetching sections can therefore spend four times that cap, and nothing here notices.

## Rate limiting

`ToolDef.rate_limit` is a permit count, and both functions set one: `web_search` defaults to 4 and `web_fetch` to 8. `design-mcp.md` resolves it as `limit.or(def.rate_limit)`, so a `[tool_limits]` entry wins and the value here is the fallback when configuration says nothing.

A metered upstream needs this because the alternative is a self-inflicted denial of service that costs money. Brave enforces a one-second sliding window, returns `X-RateLimit-Remaining` on every response, and sells a monthly request quota. With `max_concurrent_runs = 4` and no per-tool limit, four runs each searching in a loop generate as many concurrent requests as the executor can dispatch, collect `429`s, surface them to the models as tool errors, and burn turns retrying. The permit count makes the tool the bottleneck instead of the provider.

A semaphore alone is the wrong shape for a sliding window and it is worth being clear about why. Four permits against a provider answering in 50 milliseconds is eighty requests per second, which blows a one-per-second window immediately. A permit count bounds *concurrency*; a sliding window bounds *rate*. The crate closes the gap with a second mechanism: `min_interval`, default 1100 milliseconds, enforced by the last-request `Instant` in `Inner` behind a mutex, so provider requests are serialised to at most one per interval regardless of how many permits are free. With `min_interval` set, the permit count mostly determines how many callers wait rather than how many run, which is still worth having because it bounds the queue.

That `Instant` is state, and it is worth saying exactly what kind, because this crate's whole claim is statelessness. It is process-lifetime state, like the connection pool. It is not run state and it is not section state, and nothing about it has a section-shaped lifetime, which is why `on_section` stays empty. "Stateless" here means stateless with respect to the run and the section, which is the only sense the `Extension` trait cares about.

A `429` from the provider is retried with backoff honouring `Retry-After`, up to `retries` times, default 2, and then surfaced as retryable. The retry happens inside the tool call, which means it holds its permit while it waits, which is why the retry count is small and why the effective timeout is still bounded by `CallCtx::deadline`.

**The limit is process-local**, and this is one of the concrete reasons `design.md` makes the CLI a client rather than a second execution engine. A second process running prompts holds a second set of permits and a second `min_interval` clock, so the provider sees twice the configured rate and the monthly quota drains twice as fast. For the GPU budget the equivalent mistake shows up as latency; here it shows up as a bill and, eventually, as a hard quota wall mid-run. `design-mcp.md` states the general form of this; this crate is the case where it costs money.

## Caching

**There is no cache.** A repeated identical search inside one run reaches the network again. No response cache, no ETag store, no conditional requests, and no honouring of `Cache-Control` on either path.

The system's rerun-everything principle is what settles this, though not in the direction it might first appear. A cache does not make a rerun reproduce. Search results are non-deterministic across time no matter what this crate does: the index changes hourly, so two runs a day apart differ whether or not anything was cached. What a cache with a TTL would actually produce is a rerun that reproduces inside the TTL and diverges outside it, which converts an honest property - results reflect the index at the moment of the run - into an unpredictable one, results reflect the index at some point within the last N minutes unless they do not. Non-determinism that is uniform and understood is better than non-determinism with a hidden time-dependent boundary in it.

So determinism on this path is: none, and the document says so plainly rather than implying a cache buys some. What makes a run's *conclusions* auditable is not retrieval stability, it is that what the run retrieved gets filed - into the run state store during the run, and into paperstore when it is worth keeping - so the record a report rests on is reproducible even though the search that found it is not.

Two further arguments point the same way. A repeated identical search inside one section is almost always a symptom rather than an intention: instruction decay past roughly fifteen tool calls produces exactly this, and a cache would hide it while the network call plus its `ToolCalled` observer event make it visible in the log. And the cost of not caching is bounded and small: a section that retries three times pays for three identical searches, bounded by `max_retries_per_section`.

The cost is named rather than mitigated: money and latency on retried sections, and no protection at all against a prompt that searches the same thing in two sections. If caching ever becomes necessary, the right place for it is a forward proxy in front of both clients, configured as `proxy` in the fetch block, so the cache has its own TTL, its own operational visibility, and its own owner, rather than being a hidden behaviour of a tool call. Tension: that pushes a real cost onto deployment configuration, and a deployment that skips it pays the provider for duplicate work.

## Configuration

Everything this extension reads lives under `[extensions.brave]` in `prompts.toml`, plus its two entries in the global `[tools]` and `[tool_limits]` tables. `design-mcp.md` owns that file and this fragment is written to drop into it.

The API key is here and not in `gateway.toml`. The gateway holds LLM endpoint credentials and owns the GPU concurrency budget, and it has no reason whatever to see a search key: a search request never passes through it, and putting the key there would widen the blast radius of the one file in the system that already holds every model credential. `design.md` states the rule generally - non-LLM credentials live beside the prompt catalog - and this is the credential it was stated for.

```toml
# ---------------------------------------------------------------------------
# promptforge-ext-search. Two canonical words, one extension, one block.
# The block key is what `Extension::name` returns, what a `[tools]` binding
# names, and what selects the provider: `brave` builds the Brave backend. A
# second provider is a second block plus a rebuild, not a rename.
# ---------------------------------------------------------------------------

[tools]                          # both words bound to the one linked instance
web_search = "brave"
web_fetch  = "brave"

[tool_limits]                    # process-local permits; wins over ToolDef.rate_limit
web_search = 4
web_fetch  = 8

[extensions.brave]
api_key = "BSA_9f2Ld0QpXv"       # a non-LLM credential: the gateway has no reason to see it
endpoint = "https://api.search.brave.com/res/v1"
country = "us"
search_lang = "en"
default_count = 10               # what `web_search` returns when the caller says nothing
min_interval = "1100ms"          # the provider's window is one second; a semaphore alone cannot hold a rate
retries = 2                      # on 429 and on 5xx, honouring Retry-After, inside the tool call
probe_at_boot = false            # true trades a boot failure on a bad key for a boot dependency on Brave

[extensions.brave.fetch]
user_agent = "promptforge/0.1 (+https://cppalliance.org)"
timeout = "20s"                  # total, including body read; also bounded by the run deadline
connect_timeout = "5s"           # DNS plus TCP plus TLS
pool_idle_timeout = "10s"        # bounds how stale a reused socket can be
max_bytes = 8_388_608            # counted after decompression, so a gzip bomb hits the same cap
max_chars = 40_000               # cap on returned text, roughly ten thousand tokens
max_redirects = 5
allow_http = false               # https only; true is a development convenience
allow_ip_literals = false        # a bare address is the shape of a probe, not of a citation
allow_ports = [80, 443]

[extensions.brave.fetch.url_policy]
deny_extra = []                  # deployment CIDRs beyond the built-in set; RFC1918 is already covered
allow_exact = []                 # deliberate holes: host plus exact address, never a range
```

Durations are strings parsed by `humantime_serde`, matching the rest of the file. Byte and character counts are integers whose key names the unit, because a byte-size string would need a parser this crate does not otherwise want and `max_bytes` is not ambiguous about what it counts.

A prompt reaches both words through frontmatter and then scopes them per section:

```markdown
---
name: staker
description: Build a stakeholder position report for one entity
version: 1
keywords: [governance, stakeholder]
params:
  type: object
  properties:
    entity: { type: string }
  required: [entity]
tools: [web_search, web_fetch]
state:
  - name: add_statement
    description: File one public statement by the entity, with its source.
    collection: statements
    params:
      type: object
      properties:
        quote: { type: string }
        source_url: { type: string }
        stance: { type: string, enum: [supports, opposes, mixed, unclear] }
      required: [quote, source_url, stance]
outputs:
  - name: report
    kind: file
    format: markdown
    required: true
progress:
  gather: Gathering source material
---
```

`tools:` holds canonical names only, so it holds exactly two. `add_statement` is not a canonical name and never becomes one: it is a state-filing tool this prompt declares for itself, generated as `Surfaces::ToolOnly` so the model files statements and Lua reads them back through `store.count("statements")`. `done` is absent for the opposite reason, that it is a core tool present in every prompt and naming it in `tools:` would be naming something the runtime already supplied. All three sources still scope by name, which is why the Lua block above writes `tools.add("web_search", "web_fetch", "add_statement", "done")` in one call without caring which source each name came from.

One reconciliation note for a reader comparing crate documents. One extension is one linked crate, `design-mcp.md` owns `prompts.toml` and keys extension tables by `Extension::name`, and a single Brave-backed instance provides both canonical words. So both bindings name it: `web_search = "brave"` and `web_fetch = "brave"`. Tension: the binding for the fetcher is named after the search provider even though Brave has nothing to do with fetching, and swapping to a different search engine therefore edits two `[tools]` lines rather than one.

## Errors

```rust
#[derive(Debug, thiserror::Error)]
pub enum SearchError {
    // Configuration and boot. Reachable only from `new` and `validate`.
    #[error("`[extensions.{ext}]` has no `api_key`, which `web_search` requires")]
    MissingCredential { ext: String },
    #[error("provider `{0}` is not compiled into this build")]
    UnknownProvider(String),
    #[error("endpoint `{got}` is not an absolute https URL")]
    BadEndpoint { got: String },
    #[error("endpoint host `{host}` resolves into blocked range {range}, so it cannot be a search provider")]
    EndpointBlocked { host: String, range: String },
    #[error("`{field}` is {got}, which is outside {lo} to {hi}")]
    BadLimit { field: &'static str, got: String, lo: String, hi: String },
    #[error("`{key}` entry `{got}` is not a CIDR block: {reason}")]
    BadCidr { key: &'static str, got: String, reason: String },
    #[error("boot probe of `{host}` failed: {reason}")]
    ProbeFailed { host: String, reason: String },

    // Arguments. Terminal: the caller must change the call.
    #[error("{0}")]
    InvalidArgs(String),
    #[error("`query` is empty")]
    EmptyQuery,
    #[error("`query` is {got} characters; the provider accepts at most {limit}")]
    QueryTooLong { got: usize, limit: usize },
    #[error("`count` is {got}; the provider returns at most {limit} results per request")]
    CountTooHigh { got: u8, limit: u8 },
    #[error("`offset` is {got}; the provider pages to at most {limit}")]
    OffsetTooHigh { got: u8, limit: u8 },
    #[error("`url` is not a valid absolute URL: {reason}")]
    BadUrl { reason: String },

    // URL policy. Terminal: no retry of this URL will ever succeed.
    #[error("scheme `{scheme}` is not fetchable; only {allowed} is allowed")]
    BlockedScheme { scheme: String, allowed: &'static str },
    #[error("a URL with an embedded username or password is not fetchable")]
    UrlUserinfo,
    #[error("port {port} is not fetchable; allowed ports are {allowed}")]
    BlockedPort { port: u16, allowed: String },
    #[error("`{host}` is a bare IP address; fetch a named host instead")]
    IpLiteral { host: String },
    #[error("`{host}` resolves to {addr}, which is in blocked range {range}")]
    BlockedAddress { host: String, addr: IpAddr, range: String },
    #[error("`{host}` has no address outside the blocked ranges")]
    NoAllowedAddress { host: String },
    #[error("redirect from `{from}` to `{to}` was refused: {reason}")]
    RedirectRefused { from: String, to: String, reason: String },

    // Transport. Retryable except where noted.
    #[error("`{host}` did not resolve: {reason}")]
    Dns { host: String, reason: String },
    #[error("could not connect to `{host}`: {reason}")]
    Connect { host: String, reason: String },
    #[error("TLS handshake with `{host}` failed: {reason}")]
    Tls { host: String, reason: String },
    #[error("`{url}` did not respond within {timeout:?}")]
    Timeout { url: String, timeout: Duration },
    #[error("more than {limit} redirects starting from `{url}`; chain was {chain}")]
    TooManyRedirects { url: String, limit: u32, chain: String },

    // Provider responses.
    #[error("the search provider rejected the credential (HTTP 401)")]
    Unauthorized,
    #[error("the search provider is out of quota or over its rate limit (HTTP 429)")]
    RateLimited { retry_after: Option<Duration> },
    #[error("the search provider returned HTTP {status}")]
    ProviderStatus { status: u16 },
    #[error("the search provider returned a body this build cannot parse: {reason}")]
    ProviderShape { reason: String },

    // Fetched responses.
    #[error("`{url}` returned HTTP {status}")]
    HttpStatus { url: String, status: u16 },
    #[error("`{url}` is {content_type}, which cannot be read as text")]
    UnsupportedContentType { url: String, content_type: String },
    #[error("`{url}` sent no Content-Type, so it cannot be read as text")]
    NoContentType { url: String },
    #[error("`{url}` is larger than the {limit} byte cap")]
    TooLarge { url: String, limit: usize },
    #[error("`{url}` declares charset `{charset}`, which this build cannot decode")]
    Undecodable { url: String, charset: String },
    #[error("no readable text was extracted from `{url}`")]
    NoContent { url: String },

    // Lifecycle.
    #[error("the search extension was shut down")]
    ShutDown,
    #[error("the run deadline leaves no time for this call")]
    NoTimeBudget,
}

impl From<SearchError> for ExtError { /* boot-time surface */ }
impl From<SearchError> for ToolError { /* call-time surface, via `model_facing` */ }
```

The taxonomy splits on when a variant can occur and then on what a caller should do about it, because those are the two things a reader needs. `thiserror` throughout, and `anyhow` appears nowhere in this crate's public surface.

| Class | Variants | What the caller should do |
|---|---|---|
| Boot | `MissingCredential` through `ProbeFailed` | Nothing at call time. These reach `ExtError` and stop the service starting. |
| Terminal, argument | `InvalidArgs`, `EmptyQuery`, `QueryTooLong`, `CountTooHigh`, `OffsetTooHigh`, `BadUrl` | Change the argument. Retrying identically fails identically. |
| Terminal, policy | `BlockedScheme`, `UrlUserinfo`, `BlockedPort`, `IpLiteral`, `BlockedAddress`, `NoAllowedAddress`, `RedirectRefused` | Use a different source. No retry of this URL will ever succeed. |
| Terminal, content | `UnsupportedContentType`, `NoContentType`, `Undecodable`, `NoContent`, `TooLarge` | Use a different URL, or set `raw` for `NoContent`. The resource is not readable as text. |
| Terminal, upstream | `Unauthorized`, `ProviderShape`, `HttpStatus` for 4xx other than 408 and 429 | Give up on this call. A misconfigured key and a 404 are both settled facts. |
| Retryable | `Dns`, `Connect`, `Tls`, `Timeout`, `RateLimited`, `ProviderStatus` for 5xx, `HttpStatus` for 408 and 429 | The crate already retried up to `retries` with backoff. A later attempt may succeed. |
| Structural | `TooManyRedirects`, `ShutDown`, `NoTimeBudget` | Not retryable in this call. A redirect loop is a property of the URL; the other two are properties of the process and the run. |

### What the model actually sees

A `ToolError` is rendered by the core into text in the tool result, so the `Display` string is the model's entire view of what went wrong, and that makes the wording part of the interface rather than a diagnostic afterthought. Three rules follow.

- **Every terminal message names the offending argument and implies the next move.** "`https://x/y.pdf` is application/pdf, which cannot be read as text" tells a model to look for an HTML version. "fetch failed" tells it to try again, which wastes a tool call and then fails again.
- **No retryable message suggests changing the arguments,** and no terminal message suggests waiting. A model told to retry a `BlockedAddress` will retry it, because that is what the text said.
- **The model-facing rendering is not the log rendering.** `BlockedAddress` carries the resolved address and the matched range, which is what an operator needs and is more than a model should be told about a network it cannot see. `SearchError::model_facing` omits the address and says only that the host is not fetchable; `tracing` logs the full `Display`. The `ToolError` conversion uses `model_facing` and the log line uses `Display`, so one error has two renderings and the security-relevant detail goes only to the log.

Every message names the URL or the host it concerns, because a section makes many of these calls and a message that does not say which one starts an investigation rather than ending it.

## Tests

Everything here runs against a local `axum` test server on an ephemeral loopback port and a stub resolver, with no live network call anywhere in the suite. Nothing needs a GPU and nothing needs a credential.

The test server binds loopback, which the URL policy blocks, so the fetch tests construct their client with an `allow_exact` entry for the test host and address. That is deliberate: it exercises `allow_exact` as a first-class path rather than leaving the escape hatch untested, and it means a bug that made `allow_exact` ineffective would fail the whole fetch suite loudly.

- **URL policy, every blocked range.** Table-driven, one case per CIDR named in `## URL policy and SSRF defence`, both families. Explicitly including `::ffff:127.0.0.1` and `::ffff:10.0.0.1`, since IPv4-mapped is the range most often missed; `64:ff9b::7f00:1` for NAT64; `169.254.169.254` by name, because it is the metadata address; and one address just inside and one just outside each boundary, since an off-by-one in a prefix length is the failure this table exists to catch.
- **Literal encodings.** `0177.0.0.1`, `2130706433`, `0x7f.1`, `[::1]`, and `127.1` are each asserted to be refused, and the test asserts *which* error: with `allow_ip_literals = false` they are all `IpLiteral`, and the test additionally records what `url` normalised each one to, so a change in the parser's normalisation shows up as a test needing an update rather than as a hole.
- **Scheme allowlist.** `file:`, `ftp:`, `data:`, `javascript:`, `gopher:`, `ws:`, `blob:`, `about:`, and a made-up scheme are each `BlockedScheme`. `http:` is `BlockedScheme` with `allow_http = false` and accepted with it true. `HTTPS://` uppercase is accepted, because the parser lowercases and a policy that compared raw strings would not.
- **Userinfo and ports.** `https://u:p@example.org/` is `UrlUserinfo`. Ports 22, 3306, 5432, 6379, 8080, and 9310 are each `BlockedPort`, with 9310 there because it is this system's own MCP bind port.
- **Guarded resolver.** A stub returning one public and one private address yields exactly the public one. A stub returning only private addresses fails with `BlockedAddress` naming the range. A stub returning nothing fails with `NoAllowedAddress`. And the rebinding case: a stub that answers publicly on its first call and with loopback on its second must succeed then fail, which is the test that proves no verdict is cached and is the single most important test in the file.
- **Provider parsing against recorded fixtures.** Real Brave response bodies, recorded once with the recording date in a header comment and committed, served by the test server. Cases: a full twenty-result body; a body with `web` absent, which is a query that matched nothing and must return zero hits rather than an error; `web.results` present and empty; a result missing `description`; a `page_age` that does not parse, which must drop `age` and keep the hit; an unrecognised extra top-level field, which must be ignored; a renamed field this crate depends on, which must be `ProviderShape` naming the field; a 401; a 429 with `Retry-After`; and a 200 whose body is an HTML captive-portal page, which must be `ProviderShape` and not a panic. Recording the fixtures rather than hand-writing them is the point: a provider schema change then surfaces as a fixture needing re-recording.
- **HTML extraction against golden files.** Committed HTML inputs and expected text outputs, one pair per case: an article page where readability keeps the body and drops navigation; a WG21-shaped index page that is mostly a table, asserted both ways, so the golden file records that readability discards it and `raw` keeps it; a page with no readable content, which must fall back to `RawHtml` and not `NoContent`; a page that is entirely boilerplate, which must be `NoContent`; a Latin-1 page with a declared charset; a UTF-8 page with invalid bytes, which must decode lossily rather than fail; and a page whose only metadata is `<title>`. These golden files are why `dom_smoothie` and `html2text` are exactly pinned.
- **Size caps.** 40 MB of `text/html` fails with `TooLarge`. The same response with an honest `Content-Length` fails before the first body byte, asserted on the server's sent-byte counter rather than on timing. 40 MB of `text/plain` succeeds with `truncated: true` and exactly `max_bytes` of input consumed. A gzip response declaring one kilobyte on the wire and expanding past the cap fails with `TooLarge`, which is the test that proves the counter counts decompressed bytes. A body one byte under the cap succeeds untruncated.
- **`max_chars`.** A document producing more than the cap returns exactly the cap, `truncated: true`, and a prefix that ends on a character boundary; a multi-byte character straddling the cap is not split.
- **Redirect caps.** Five hops succeed and `redirects` records all five in order. Six fail with `TooManyRedirects` and the chain in the message. An A to B to A loop fails by count. `https` to `http` fails with `RedirectRefused`. A public host redirecting to `127.0.0.1` fails with `RedirectRefused` and the test asserts the final server received no request at all.
- **Timeouts.** A server that accepts and never responds fails with `Timeout` at the configured value plus a tolerance. A server dribbling one byte per second past the total timeout fails, which is the slow-loris case the total rather than the connect timeout catches. A `CallCtx::deadline` half a second out returns `NoTimeBudget` with no socket opened, asserted on the server's connection counter.
- **Rate limiting.** Eight concurrent `web_search` calls through a four-permit `ResolvedTool` never put more than four in flight, asserted by a counting handler on the test server. `min_interval` of 1100 milliseconds serialises two calls to at least that gap. A 429 with `Retry-After: 2` is retried after roughly two seconds and then surfaced once `retries` is exhausted.
- **No cache.** Two identical `web_search` calls in one run produce two requests at the test server, and two identical `web_fetch` calls produce two. This is the test that encodes the caching decision, and it fails if someone later adds a cache without amending this document.
- **Surface presence.** The converse of the classify document's test. Build a `ToolMap` with `SearchExt` registered and assert the schema list sent to the model contains exactly `web_search` and `web_fetch`, with their derived schemas matching a committed snapshot so a change to an argument struct shows up as a diff. Then assert the Lua environment has a `web` table with two callable fields. Then assert scoping: a section calling `tools.add("web_search")` alone sends one schema and not two, while Lua can still reach `web.fetch`, because the core installs capability families once per run and `ToolMap::scoped` filters only what the model sees.
- **Credential containment.** The fetch client's default headers contain no `X-Subscription-Token` and no `Authorization`. A fetch against the test server asserts the received request carries no credential and no cookie. A provider response that redirects to the test server asserts the token was not forwarded, which is the test that justifies two clients.
- **Lifecycle.** A recording harness asserts `on_section` is called for every event and does nothing observable. `validate` passes with no network reachable at all, which is the test that encodes the offline decision. `validate` fails with `MissingCredential` on an empty key, `EndpointBlocked` on an endpoint pointed at loopback, and `BadCidr` on a malformed `deny_extra`. `shutdown` drops both pools and a subsequent call of each function returns `ShutDown`.
- **Argument validation on both surfaces.** A model-shaped JSON call and a Lua table call with the same defect produce the same error: a misspelled key named in the message, `count = 50` as `CountTooHigh`, an empty query as `EmptyQuery`. Same function, two callers, one error taxonomy.
- **Error rendering.** `BlockedAddress::model_facing` does not contain the address or the range, while its `Display` contains both. This is a one-line test guarding a decision that is otherwise easy to undo by accident.

There is deliberately no test asserting that a search returns the same results twice, because it does not and this document says so.

## Open

- Whether `web_fetch` should carry a per-run fetch budget. The per-section tool cap bounds a section, so a run jumping between four fetching sections spends four times it. Adding a run-scoped counter would make this extension stateful and give `on_section` real work, which is exactly the property the crate exists to show is optional, so the trade is between a real limit and the cleanest available demonstration that the trait needs no special case.
- Whether the readability-or-raw choice belongs to the caller or to the crate. It is the caller's today, and a caller cannot know which mode a page needs before fetching it. `dom_smoothie::Readability::is_probably_readable` would let the crate decide, but it must be called before `parse` because `parse` mutates the document, and whether its verdict is right on committee pages that are largely tables is unmeasured.
- Whether the provider trait's `offset` survives a second provider. It fits Brave's page offset and Google's `start` index and does not fit cursor-based paging at all, and which of those the second provider turns out to be is unknown.
- Whether the monthly quota should be visible to a prompt. `X-RateLimit-Remaining` arrives on every response and is currently logged and discarded. Surfacing it on `SearchResult` would let a Lua block refuse to start an expensive section, at the cost of putting a billing number into a value the model reads.
- Whether 40,000 characters is the right default. It is derived from a token estimate, not from measurement of how much of a fetched page a section actually uses, and the two plausible failures - truncating a document a section needed whole, and spending a third of a context window on boilerplate - point in opposite directions.
- Whether `allow_exact` should exist. It is a hole in the control that matters most, its only justification is that the alternative is a deployment disabling the policy wholesale, and the test suite's dependence on it means the hole is now load-bearing for the tests as well.

*2026-07-25 - design-search*
