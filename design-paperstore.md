<!-- STATUS: crate doc - promptforge-ext-paperstore - behind Cargo feature `paperstore` - the transactional reference case - see design.md for the system -->

# `promptforge-ext-paperstore`: WG21 storage as a transactional extension

## Scope

This crate is where WG21 domain knowledge enters the system, and it is the only place it enters. It holds the paper schema, the table names, the paper id format, the revision convention, the mailing year index, and the two database backends those tables live in. Nothing above it knows any of that: `promptforge` declares no storage concept at all, `promptforge-gateway` routes LLM traffic, and `promptforge-mcp` binds a canonical tool name to the string `"paperstore"` without knowing what a paper is.

A deployment that does not link this crate is a working deployment. That is the load-bearing test of the domain boundary from [design.md](design.md), and this crate is the thing the test is about: with the `paperstore` feature off there is no schema, no connection, no `sqlx` in the dependency graph, no WG21 vocabulary anywhere in the binary, and every prompt that names no `paper_*` word runs unchanged. A prompt that does name one fails startup validation with an unbound canonical name, which is the correct failure and the only one.

This crate is also the second half of the assumption `design.md` recorded as its riskiest: that one `Extension` trait carries both a stateless extension and a transactional database one without acquiring a special case for either. [design-search.md](design-search.md) is the stateless half and the reference case for it, with [design-classify.md](design-classify.md) a second stateless example; in both, `on_section` is a no-op because neither holds anything whose lifetime is a section. This crate is the half that holds a write transaction for exactly the length of a section, so `## The Extension impl` below is the heart of the document and its verdict on the trait is the most valuable thing in it.

The verdict was that the trait was close and not sufficient, and `## Verdict on the trait` names the four changes it needed. All four have since landed in [design-core.md](design-core.md): `on_section`, `validate`, and `shutdown` are async, `SectionEvent` gained `RunEnded` and a `TaskId` on the nested variants plus `NestedFailed`, `RunError` gained an `Extension` variant, and the trait gained `row_count` and `holds_section_state`. The signatures quoted below are the current ones. The assumption is retired as substantially correct: one trait carries both shapes, and no special case for either extension was required.

What this crate does not do, and cannot be made to do without a change to this document:

- Write the Django site's tables. It writes paperstore and lets the site mirror. The site resolves author organizations against an `Organization` table it owns, and its evaluation rows are append-only history whose ordering it depends on; neither is reachable from here.
- Run the ingestion pipeline. Scraping open-std.org, downloading sources, and converting PDF to markdown stay in Python. This crate reads what that pipeline produced and writes what a prompt produced.
- Own the artifact files. `paper.md`, the staged PDF, the extracted figures, and the agora JSON are written by the Python side. This crate reads markdown through a windowed accessor and writes rows.
- Convert anything. No PDF, no HTML, no OCR, no markdown generation.
- Hold run state. `state` and `store` are the core's run state store and are unrelated to this crate despite the name collision, which `design-core.md` flags for the same reason.
- Call an LLM, a classifier, or a search provider. It has no HTTP client at all.
- Migrate a production Postgres database at boot without being told to. See `## The Postgres backend`.
- Construct a filesystem path from prompt-supplied text. Every path is derived from a validated `PaperId` under a configured root.
- Decide what a paper means. `disposition`, `intent`, and `target_group` are strings this crate stores and never interprets.

The test of the boundary: removing this crate from the workspace leaves every other crate compiling untouched, and no crate outside it mentions `sqlx`, SQLite, Postgres, a table name, or a paper.

## What the Python implementation actually is

Everything in this section was read out of `wg21-paperflow/packages/paperstore` rather than inferred, and three of the claims correct documents in that repository. The Rust trait below covers the call sites that exist rather than the ones the README describes.

### Shape

- `backend.py` holds `StorageBackend`, a Python `abc.ABC` with **89 `@abstractmethod` declarations**, plus the `PaperRow` and `ClearedSet` frozen dataclasses and the `parse_authors_raw` helper.
- `sqlite_backend.py` holds `SqliteBackend`, the only implementation, at roughly 1,840 lines. Files are the source of truth and the database is an index: each writer lands the artifact through a `.partial` rename and then commits the matching row in a `with self._conn:` block.
- `factory.py` holds `from_uri`, which resolves `None`, `""`, and `file://` to a `SqliteBackend` and raises `InvalidPaperstoreUriError` on every other scheme. `postgres://` is a comment, not a branch.
- `extract_rows.py` holds 21 frozen dataclasses returned by read methods. Write methods are duck-typed and import no domain types.
- `tools.py` holds `PaperstoreTools`, the agent-facing read-only surface: `paper_meta`, `paper_meta_latest`, `read_file`, each returning a JSON string for `agent.tool_plain` registration. This is the closest existing thing to a model-facing tool surface and it is what the read half of the canonical vocabulary below is derived from.
- `stages.py` holds the status integers: `download = 0`, `convert = 1`, `agora = 4`, `herald = 5`, `ready = 6`, with a failed status of `-(stage + 1)`.

### The real schema

Twenty-eight tables, created by one `_SCHEMA` string executed with `executescript`, followed by a hand-written `_migrate` that runs `ALTER TABLE` for later columns and then executes `_SCHEMA` a second time. Every column is `TEXT`, `INTEGER`, `REAL`, or `BOOLEAN`, every timestamp is an ISO-8601 string written by `datetime.now(timezone.utc).isoformat()`, and every JSON value is a `TEXT` column holding `json.dumps` output.

`papers` is the spine and is worth quoting in full, because the Rust row type has to match it column for column:

```sql
CREATE TABLE IF NOT EXISTS papers (
    paper_id         TEXT PRIMARY KEY,
    year             TEXT DEFAULT '',
    title            TEXT DEFAULT '',
    authors          TEXT DEFAULT '',
    target_group     TEXT DEFAULT '',
    intent           TEXT DEFAULT '',
    url              TEXT DEFAULT '',
    document_date    TEXT DEFAULT '',
    mailing_date     TEXT DEFAULT '',
    disposition      TEXT DEFAULT '',
    previous_version TEXT DEFAULT '',
    source_file      TEXT DEFAULT '',
    markdown_path    TEXT DEFAULT '',
    dissect_path     TEXT DEFAULT '',
    advocatus_path   TEXT DEFAULT '',
    agora_path             TEXT DEFAULT '',
    citations_extracted_at TEXT DEFAULT '',
    line_count             INTEGER DEFAULT 0,
    status                 INTEGER NOT NULL DEFAULT 0,
    error                  TEXT DEFAULT '',
    updated_at             TEXT DEFAULT ''
);
```

`assay_path TEXT DEFAULT ''` is a twenty-second column that exists on every database and appears in no `CREATE TABLE`: it is added by `_migrate` alone. `dissect_path` and `advocatus_path` are marked deprecated in the source and kept for migration safety. `PaperRow` exposes 20 of the 22 columns, omitting `advocatus_path` and `updated_at`.

The other twenty-seven:

| Table | Columns | Primary key |
|---|---|---|
| `settings` | `key TEXT`, `value TEXT NOT NULL` | `key` |
| `years` | `year TEXT`, `added TEXT` | `year` |
| `mailings` | `mailing_id TEXT`, `label TEXT`, `added TEXT` | `mailing_id` |
| `claims` | `paper_id TEXT NOT NULL`, `uid INTEGER NOT NULL`, `loc_line INTEGER NOT NULL`, `loc_start INTEGER NOT NULL`, `loc_end INTEGER NOT NULL`, `text TEXT NOT NULL`, `section TEXT`, `question TEXT`, `kind TEXT DEFAULT 'normative'`, `merged_into INTEGER` | `(paper_id, uid)` |
| `evidence` | as `claims` plus `supports TEXT DEFAULT '[]'`, `quantitative INTEGER`, `cited INTEGER`, `verifiable INTEGER`, `normative INTEGER`, minus `question` and `kind` | `(paper_id, uid)` |
| `paper_citations` | `paper_id TEXT NOT NULL`, `cited_paper_id TEXT NOT NULL`, `count INTEGER DEFAULT 1` | `(paper_id, cited_paper_id)` |
| `external_citations` | `id INTEGER PRIMARY KEY AUTOINCREMENT`, `paper_id TEXT NOT NULL`, `source_url TEXT`, `source_title TEXT`, `text TEXT`, `finding TEXT`, `stance TEXT` | `id` |
| `questions` | `paper_id`, `uid`, `loc_line`, `loc_start`, `loc_end`, `claim_text TEXT NOT NULL`, `section`, `question TEXT NOT NULL`, `kind` | `(paper_id, uid)` |
| `rhetoric` | `paper_id`, `uid`, `loc_line`, `loc_start`, `loc_end`, `text TEXT NOT NULL`, `section`, `marker_type`, `target`, `intensity TEXT DEFAULT 'medium'` | `(paper_id, uid)` |
| `caput_causae` | `paper_id TEXT`, `thesis TEXT NOT NULL` | `paper_id` |
| `citation_audit` | `paper_id`, `cited_paper_id`, `resolution_method TEXT NOT NULL`, `resolved INTEGER NOT NULL`, `source_url`, `quote_match TEXT DEFAULT 'not_checked'`, `discrepancy` | `(paper_id, cited_paper_id)` |
| `candidates` | `paper_id TEXT NOT NULL`, `rule TEXT NOT NULL`, `label TEXT NOT NULL`, `detail TEXT`, `data TEXT DEFAULT '{}'` | **none** |
| `findings` | `paper_id`, `id TEXT NOT NULL`, `lens`, `severity`, `title`, `quoted_text`, `source_line INTEGER`, `explanation` | `(paper_id, id)` |
| `signals` | `paper_id`, `section_idx INTEGER NOT NULL`, `heading`, `loc_line INTEGER NOT NULL`, `loc_start`, `loc_end`, `signal_type TEXT NOT NULL`, `quote`, `observation` | **none** |
| `assay_claims` | `paper_id`, `uid`, `loc_line`, `quote TEXT NOT NULL`, `section`, `kind`, `load_bearing INTEGER` | `(paper_id, uid)` |
| `assay_evidence` | `paper_id`, `uid`, `loc_line`, `quote`, `section`, `subtype`, `quality_tier`, `supports TEXT DEFAULT '[]'`, `source_pid` | `(paper_id, uid)` |
| `assay_concessions` | `paper_id`, `uid`, `loc_line`, `quote`, `section`, `subtype` | `(paper_id, uid)` |
| `assay_gaps` | `paper_id`, `uid`, `chunk_index INTEGER NOT NULL`, `loc_line`, `gap TEXT NOT NULL`, `why_important`, `primary_lens`, `secondary_lens`, `severity TEXT DEFAULT 'minor'`, `closed_by TEXT` | `(paper_id, uid)` |
| `assay_thesis` | `paper_id`, `central_claim TEXT NOT NULL`, `problem_statement`, `scope_boundary`, `ask_calibration` | `paper_id` |
| `assay_findings` | `paper_id`, `uid`, `title`, `lens`, `severity`, `quote`, `loc_line`, `explanation`, `test`, `survived INTEGER DEFAULT 1`, `major INTEGER`, `challenge`, `reasoning`, `from_gap_ids TEXT` | `(paper_id, uid)` |
| `assay_asks` | `paper_id`, `uid`, `target TEXT NOT NULL`, `quote TEXT NOT NULL`, `type TEXT NOT NULL` | `(paper_id, uid)` |
| `assay_pids` | `paper_id`, `uid`, `raw_pid TEXT NOT NULL`, `resolved_pid`, `url`, `mention_count INTEGER`, `in_paperstore BOOLEAN DEFAULT 0`, `stale BOOLEAN DEFAULT 0`, `author_overlap REAL DEFAULT 0.0` | `(paper_id, uid)` |
| `assay_urls` | `paper_id`, `uid`, `url TEXT NOT NULL`, `line INTEGER` | `(paper_id, uid)` |
| `assay_strengths` | `paper_id`, `uid`, `title TEXT NOT NULL`, `quote`, `loc_line`, `explanation` | `(paper_id, uid)` |
| `assay_checklist` | `paper_id`, `item_id TEXT NOT NULL`, `name TEXT NOT NULL`, `passed INTEGER`, `location`, `note` | `(paper_id, item_id)` |
| `assay_compounds` | `paper_id`, `uid`, `name TEXT NOT NULL`, `constituents TEXT DEFAULT '[]'`, `mechanism`, `cross_lens INTEGER`, `emergent_risk` | `(paper_id, uid)` |
| `assay_synthesis` | `paper_id`, `verdict TEXT NOT NULL`, `verdict_confidence TEXT DEFAULT 'Medium'`, `thesis_statement`, `thesis_survives INTEGER`, `central_thesis`, `dominant_dynamic`, `critical_count INTEGER`, `significant_count INTEGER`, `skip_reason`, `paper_stats TEXT DEFAULT '{}'` | `paper_id` |

**There are no indexes.** Not one `CREATE INDEX` statement exists in the package. Every lookup is served by an implicit primary-key index or by a full table scan, and the four queries that scan are `WHERE year = ?`, `WHERE mailing_date >= ?`, `WHERE cited_paper_id = ?`, and `WHERE paper_id LIKE ?`. At the archive scale `wg21-paperflow/DESIGN.md` names, roughly ten thousand papers, a scan of `papers` is cheap enough that this has never hurt, and it is a scan nonetheless.

Nine tables use a `paper_id` prefix with no index on it, so every `DELETE FROM t WHERE paper_id = ?` in a replace-all write is a full scan of that table. Two tables, `candidates` and `signals`, have no primary key at all, which makes delete-and-insert the only safe write shape for them and rules out an upsert.

### The abstract interface, by group

Eighty-nine abstract methods, in the source's own order. Every one takes a `paper_id: str` unless noted.

- Workspace: `workspace_dir`, a property returning `Path`.
- Year index: `has_year(year)`, `upsert_year(year, papers)` returning `list[PaperRow]`, `list_papers_for_year(year)`, `list_all_paper_ids()`, `resolve_year_for_paper(pid)` returning a year and row pair or `None`.
- Mailing metadata: `upsert_mailing_label(mailing_id, label)`, `get_mailing_label(mailing_id)`.
- Artifact writes: `put_source(pid, content, *, suffix)`, `write_paper_md(pid, markdown)`, `write_agora_json(pid, payload)`, `read_agora_json(pid)`, `clear_agora(pid)`, `write_intermediate(pid, name, payload)`, `record_source(pid, path)`, `record_markdown(pid, path, *, intent, line_count)`, `reconcile()`.
- Images and invalidation: `get_paper_image_path(pid, page, index, ext)`, `write_paper_image(pid, page, index, ext, data)`, `iter_paper_image_paths(pid)`, `delete_paper_images(pid)`, `get_html_images_manifest_path(pid)`, `clear_downstream_outputs(pid)` returning a `ClearedSet`.
- Artifact reads: `get_meta(pid)`, `get_source_path(pid)`, `get_paper_md(pid)`, `try_read_paper_md(pid)`, `get_paper_md_path(pid)`, `get_agora_path(pid)`, `get_debug_md_path(pid, tool)`, `get_trace_md_path(pid, tool)`, `list_years()`, `list_papers_since(month)`.
- Status and settings: `advance_status(pid, from_status, to_status)`, `fail_paper(pid, stage, error)`, `get_setting(key)`, `set_setting(key, value)`.
- Assay: thirteen `store_assay_*` writes and thirteen `get_assay_*` reads, plus `write_assay_md(pid, markdown)` and `clear_assay(pid)`.
- Extract: `store_claims`, `store_evidence`, `store_paper_citations`, `store_external_citations`, `store_questions(pid, claims, verdicts)`, `store_rhetoric`, `store_caput_causae(pid, thesis)`, `store_citation_audit`, the matching `get_*` reads, and `get_incoming_citations(cited_pid)`.

`advance_status` is the one interesting method in the set: it is a compare-and-swap, `UPDATE papers SET status = ?, error = '', updated_at = ? WHERE paper_id = ? AND status = ?`, returning `rowcount == 1`. `wg21-paperflow/ARCHITECTURE.md` states this works on both SQLite and Postgres, and it does, because both report affected rows and both serialize the update.

Eight public methods exist on `SqliteBackend` and not on the ABC: `find_latest_revision`, `store_candidates`, `get_candidates`, `store_findings`, `get_findings`, `store_signals`, `get_signals`, and `close` with its context-manager pair. Seven of the eight have no caller anywhere in the workspace. `find_latest_revision` is dead in a more interesting way: `PaperstoreTools.paper_meta_latest` needs exactly that behaviour and reimplements it in Python over `list_all_paper_ids()`, because it is written against the ABC and the ABC does not have it. That is the abstraction leak the ABC exists to prevent, visible in the one place a second backend would have broken.

### The SqliteBackend connection settings

Four lines, and they are the whole story:

```python
self._conn = sqlite3.connect(str(db_path), check_same_thread=False)
self._conn.execute("PRAGMA busy_timeout = 5000")
self._conn.row_factory = sqlite3.Row
self._conn.executescript(_SCHEMA)
```

**No WAL.** No `journal_mode` at all, so the database runs in the default rollback journal, where a writer excludes every reader for the length of its transaction. `busy_timeout` is 5000 milliseconds. `synchronous` is left at its default. `foreign_keys` is off, which is harmless only because the schema declares none.

`design.md` records this accurately: the current Python backend sets only a busy timeout and its comment asserts a single-process assumption. The comment is at the top of the module, and it is worth quoting because it is the assumption this crate breaks: `Designed for single-threaded access from the main coroutine in jobs.py. No WAL or connection pool is needed because workers never touch the DB.` A second comment at the connection explains `check_same_thread=False` as a concession to the preview server handing the backend to Werkzeug worker threads, and asserts that concurrent reads are safe because Python's `sqlite3` is built SERIALIZED while writes stay inside one process.

Both comments are true of the Python deployment and both stop being true the moment `promptforge-mcp` is a second process on the same file. WAL is therefore not an optimization here; it is a correctness precondition, and it is `## The SQLite backend`.

### Is there a Postgres backend

**No, and there is no evidence of one in either repository.** What exists is four documents describing one and one function reserving its URI scheme:

- `paperstore/src/paperstore/CLAUDE.md` states it as a fact under `## Invariants`: `A Postgres backend exists in wg21-website (private).`
- `wg21-paperflow/DESIGN.md` specifies it in detail at section 5: Postgres for structured metadata, S3 for blobs, `get_source_path` materializing from S3 to a temp file, `Implemented in wg21-website (private), not in this repo`.
- `wg21-paperflow/DESIGN.md` section 8 shows a call site: `storage=PostgresBackend(db)`.
- `factory.py` reserves the scheme in a docstring and then raises on it: `Any other scheme is reserved for future backends (e.g. postgres://)`.

Against that: no file in `wg21-paperflow` defines a `PostgresBackend`, imports `psycopg`, or references a Postgres connection outside prose. `from_uri` has exactly two branches and both return `SqliteBackend`. And `wg21-website` in this workspace is an empty directory with no git metadata, so nothing in it can be read, imported, or verified.

So `design.md`'s assertion holds, with one correction that matters. `design.md` says no Postgres backend exists despite the Python design document describing one. That understates it: `CLAUDE.md` does not describe a plan, it asserts existence as a standing invariant that agents are told to preserve. An agent reading that file will believe a second backend is already in the field and will write code to keep it working. It should be corrected to say the backend is specified and unbuilt. Building it is in scope for this crate, and this crate's Postgres backend is not that one: it is Postgres for rows with no S3 and no blob store, because the artifact files stay on the Python side of the boundary.

### Paper id case

`design.md` says paperstore ids are uppercase while every Django-side paper-keyed model is lowercase. The paperstore half is verified and the Django half is not checkable here, since `wg21-website` is empty. What the code actually does is more mixed than one rule:

- Every `papers` write and read folds with `paper_id.strip().upper()`. `upsert_year` skips any entry whose uppercased id is empty. `list_all_paper_ids` returns uppercase. `CLAUDE.md`'s invariant, filesystem stems lowercase and `list_paper_ids` uppercase, is correct.
- Filesystem stems are lowercase: `put_source` writes `{pid.lower()}{suffix}`, `write_paper_md` writes `{pid.lower()}.md`, and `_IMAGE_FILENAME_RE` matches `^[a-z]\d+(?:r\d+)?-fig\d+-\d+\.[a-z0-9]+$`, so the regex will not match an uppercase filename at all.
- The extract-era writes fold: `store_claims`, `store_evidence`, `store_paper_citations`, `store_external_citations`, `store_questions`, `store_rhetoric`, `store_caput_causae`, `store_citation_audit`, `store_candidates`, `store_findings`, and `store_signals` all begin with `pid = paper_id.strip().upper()`.
- **Every one of the twenty-six `assay_*` reads and writes passes `paper_id` through unfolded.** `store_assay_claims` deletes and inserts on the raw argument. So does `clear_assay`. `write_assay_md` is the worst of them: it computes `pid = paper_id.strip().upper().lower()` for the filename and then writes the raw argument into the `papers` row, including `INSERT OR IGNORE INTO papers (paper_id) VALUES (?)`. A lowercase call there inserts a second `papers` row for the same paper that no uppercase reader will ever find, and `clear_downstream_outputs` will not clear it because that method does fold.
- `get_debug_md_path` and `get_trace_md_path` contain `paper_id.strip().upper().lower()`, which is `.lower()` with two extra steps.

So the case convention is uppercase in the database and lowercase on disk, held up by a fold repeated at sixty-odd call sites, with a twenty-six-method hole in the assay path. That is the argument for `## Paper id case` below: the fold belongs in a type, once.

### How writes behave on re-run

Replace-all, and the system's discard-and-rerun recovery model rests on it correctly. Every structured write is delete-then-insert inside one transaction:

```sql
DELETE FROM claims WHERE paper_id = ?;
INSERT INTO claims (paper_id, uid, loc_line, loc_start, loc_end, text, section, question, kind, merged_into)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
```

The `with self._conn:` block makes the pair atomic, so a reader sees the old set or the new set and never a partial one. Three writes use `INSERT OR REPLACE` instead, on the three single-row-per-paper tables: `caput_causae`, `assay_thesis`, `assay_synthesis`. `set_setting` is the fourth. `upsert_year` uses `ON CONFLICT(paper_id) DO UPDATE`, overwriting the metadata fields while preserving `source_file` and `markdown_path`, and preserving `intent` only when the stored value is empty. Rows present for a year but absent from the incoming list are retained rather than deleted.

`store_paper_citations` is the one write with a subtlety worth copying: it deletes, inserts, and stamps `citations_extracted_at` **even when the incoming list is empty**, because row presence alone cannot distinguish a paper with zero citations from a paper never processed. The stamp is the authoritative signal. Any replace-all design needs one of those per table whose empty state is meaningful.

The class docstring states the recovery model in the same words `design.md` uses: files land first through an atomic `.partial` rename, the row commits second, and a crash between them leaves a complete file with a stale or absent row, `Recovery is simply to re-run the operation; the pipeline is idempotent and the next call rewrites both file and row cleanly.` That is verified, and it is what makes `## Idempotent replace-all writes` true.

### Three corrections to the Python repository's own documents

Not this crate's problem to fix, and worth recording because the next reader of those files will otherwise carry the errors forward.

- `paperstore/README.md` lists backend methods that do not exist: `upsert_mailing_index`, `list_mailing`, `list_paper_ids`. The real names are `upsert_year`, `list_papers_for_year`, `list_all_paper_ids`.
- `CLAUDE.md` says `Six tables in paperstore.db store structured extraction results` and names `rhetorical_markers` with a loc-triple primary key. The table is `rhetoric` with a `(paper_id, uid)` key, and `_migrate` explicitly drops `rhetorical_markers` when it finds it. It also gives `questions` a `paper_id + claim_text` key, which is `(paper_id, uid)`, and says `all 12 assay_* tables` where `_ASSAY_TABLES` has thirteen entries.
- `CLAUDE.md` gives the debug artifact name as `<pid>.<tool>.debug.md`. The code produces `<pid>.debug.<tool>.md`, and the ABC docstring agrees with the code.

## Dependencies and pins

```toml
[dependencies]
promptforge = { path = "../promptforge" }
sqlx = { version = "=0.9.0", default-features = false, features = [
    "runtime-tokio",
    "tls-rustls-ring-webpki",
    "sqlite",
    "postgres",
    "macros",
    "migrate",
] }
async-trait = "0.1"
mlua = { workspace = true }
serde = { workspace = true }
serde_json = { workspace = true }
schemars = { workspace = true }
thiserror = { workspace = true }
tokio = { workspace = true }
tracing = { workspace = true }
```

`sqlx` is the whole decision and the rest follows from it.

- Version checked on **2026-07-25** against crates.io. Latest is **0.9.0**, published 2026-05-21, MSRV 1.94.0. The last 0.8 release is 0.8.6 from 2025-05-19. The repository moved from `launchbadge/sqlx` to `transact-rs/sqlx` at the 0.9.0 release, which is an ownership formalization rather than a fork.
- Pinned at exactly `=0.9.0`, and this is the only exact pin in the crate. The reason is not the release-candidate risk that makes `design-classify.md` pin everything: `sqlx` is a stable release with a nine-figure download count. It is that 0.9.0 removed `Cargo.lock` from the upstream repository and made three signature-level breaking changes, so a caret range across a project that owns its own lockfile buys nothing while a minor bump lands in the two backend files at a time nobody chose.
- `sqlite` and `postgres` in one crate rather than two crates. This is the decision the storage trait's cost depends on, and one crate wins on every axis that matters: one connection model, one `Executor` trait so a statement is written once and run against either, one `Transaction` type so `## The Extension impl` has one code path instead of a `cfg`-shaped fork, one type-mapping table, and one pool implementation. The two-crate alternative is `rusqlite` plus `tokio-postgres` or `deadpool-postgres`, and it is worse than merely more code: `rusqlite` is synchronous, so every read and every write would need `spawn_blocking` and the transaction would have to live on a thread rather than in a task, which is a second concurrency model inside one extension. Diesel is synchronous for SQLite too, and `diesel-async` does not cover it. An ORM was rejected for the opposite reason: `sea-orm` and Diesel both abstract the dialect difference away, and `## Behavioral parity` is a list of divergences this crate needs to see rather than hide.
- `default-features = false` because the default set pulls both `tls-native-tls` and a runtime selection this crate does not choose. `runtime-tokio` because the host is already a Tokio runtime. `tls-rustls-ring-webpki` so a Postgres URL with `sslmode=require` works without a rebuild; the intranet is firewalled and TLS there is not required today, but a rebuild to add it later would be a rebuild of the whole binary to change a connection string.
- The `sqlite` feature bundles SQLite through `libsqlite3-sys` and compiles it from source, which is exactly right for a single-binary goal: no system SQLite version to match on either target host. It costs a C compiler on the build machine, which CI already has. `sqlite-unbundled` exists and is not used. 0.9.0 made SQLite extension loading `unsafe`; this crate loads no extensions, so the change is invisible here.
- `macros` is enabled for `#[derive(sqlx::FromRow)]` and for nothing else. `migrate` is enabled for `sqlx::migrate!`, which embeds the SQL migration files in the binary so a deployment carries its schema.

**Compile-time query checking is not worth its cost here, and the reason is structural rather than a build-time complaint.** `sqlx::query!` typechecks a statement against a live database named by `DATABASE_URL` at compile time, or against a committed `.sqlx` directory in offline mode. It resolves to exactly one database. This crate runs most of its statements against two, so a checked statement could be verified against SQLite or against Postgres but not both, and the half that went unchecked is precisely the half where the divergences in `## Behavioral parity` live. Making the check work would mean two macro invocations per statement behind `cfg`, which doubles the SQL and defeats the single-statement design. The `sqlx.toml` support added in 0.9.0 lets a crate rename its `DATABASE_URL` for multi-database workspaces, which solves a different problem: several databases each with one dialect, not one statement against two dialects.

The replacement is stronger than what was given up: `query_as::<_, Row>` with a `FromRow` derive, and the shared backend test suite in `## Tests` running every statement against a real SQLite file and a real Postgres server. A compile-time check proves a statement parses against one schema; the suite proves both backends produce the same rows, which is the property this crate actually needs. Tension: a typo in a column name is a test failure rather than a compile error, so it is found in seconds rather than instantly, and only if a test covers that statement.

One more consequence of 0.9.0 to design around. The `query*` functions now take `SqlSafeStr`, which accepts `&'static str` and requires `AssertSqlSafe` for anything built at runtime. Every statement in this crate is a static literal except the ones that interpolate a table name for a declared `Rows` output, and those are gated behind an allowlist lookup before `AssertSqlSafe` is reached. The new bound makes that gate visible in the type system instead of a convention, which is a genuine improvement and is why `## Declared row outputs` names the allowlist as the mechanism rather than the habit.

## The storage trait

The trait lives here. `promptforge` declares no storage concept at all, so nothing in the core imports it, nothing in the core names a table, and an extension backed by a REST API, a file tree, or nothing persistent is equally valid.

```rust
/// A paper id in paperstore's canonical form. Constructed only through
/// `parse`, which trims, folds to uppercase, and validates the shape, so no
/// other code in this crate performs a case fold.
#[derive(Clone, PartialEq, Eq, PartialOrd, Ord, Hash, Debug)]
pub struct PaperId(String);

impl PaperId {
    pub fn parse(raw: &str) -> Result<Self, StoreError>;
    /// Uppercase. What every database column holds.
    pub fn as_str(&self) -> &str;
    /// Lowercase. What every artifact filename stem is.
    pub fn stem(&self) -> String;
    /// The number without its revision suffix: `P4003R2` gives `P4003`.
    pub fn base(&self) -> &str;
    /// The revision, if the id carries one.
    pub fn revision(&self) -> Option<u32>;
}

/// A table this extension will accept rows for. Constructed only from the
/// configured allowlist, so a table name can never arrive from prompt text.
#[derive(Clone, PartialEq, Eq, Debug)]
pub struct TableName(&'static str);

#[async_trait]
pub trait Store: Send + Sync + 'static {
    /// Which backend this is, for diagnostics and for the two places where
    /// behaviour legitimately differs. Never branched on inside a statement.
    fn kind(&self) -> Backend;

    /// Reachability plus a schema check. Runs inside `Extension::validate`.
    async fn ping(&self) -> Result<(), StoreError>;

    /// Apply embedded migrations. Called only when configuration asks.
    async fn migrate(&self) -> Result<(), StoreError>;

    /// Open a write transaction. On SQLite this is `BEGIN IMMEDIATE` and it
    /// takes the single database-wide writer slot.
    async fn begin(&self) -> Result<Box<dyn Tx>, StoreError>;

    // Reads outside any transaction. A read inside one goes through `Tx`.
    async fn meta(&self, id: &PaperId) -> Result<PaperRow, StoreError>;
    async fn latest_revision(&self, base: &str) -> Result<Option<PaperId>, StoreError>;
    async fn markdown(&self, id: &PaperId, from: u32, lines: u32) -> Result<MdWindow, StoreError>;
    async fn outgoing_citations(&self, id: &PaperId) -> Result<Vec<CitationRow>, StoreError>;
    async fn incoming_citations(&self, id: &PaperId) -> Result<Vec<CitationRow>, StoreError>;
    async fn papers_for_year(&self, year: &str) -> Result<Vec<PaperRow>, StoreError>;
    async fn papers_since(&self, month: &str) -> Result<Vec<PaperRow>, StoreError>;
    async fn all_paper_ids(&self) -> Result<Vec<PaperId>, StoreError>;
    async fn setting(&self, key: &str) -> Result<Option<String>, StoreError>;

    /// Release every connection. Idempotent.
    async fn close(&self);
}

/// One write transaction, owned by one run for the length of one section.
/// Dropping without `commit` rolls back, which is the safety net under the
/// missing run-terminal event described in `## Verdict on the trait`.
#[async_trait]
pub trait Tx: Send + Sync {
    /// Replace every row for `id` in `table` with `rows`. An empty `rows` is a
    /// delete, and is how a prompt clears a table.
    async fn replace_rows(
        &mut self,
        table: &TableName,
        id: &PaperId,
        rows: &[serde_json::Value],
    ) -> Result<u64, StoreError>;

    /// Insert or update one paper's metadata, preserving the artifact-path
    /// columns the Python pipeline owns. Mirrors `upsert_year` for one paper.
    async fn upsert_paper(&mut self, paper: &PaperUpsert) -> Result<(), StoreError>;

    /// Reads inside the transaction, so a section sees its own writes.
    async fn meta(&mut self, id: &PaperId) -> Result<PaperRow, StoreError>;
    async fn count_rows(&mut self, table: &TableName, id: &PaperId) -> Result<u64, StoreError>;

    async fn savepoint(&mut self, name: &str) -> Result<(), StoreError>;
    async fn release(&mut self, name: &str) -> Result<(), StoreError>;
    async fn rollback_to(&mut self, name: &str) -> Result<(), StoreError>;

    async fn commit(self: Box<Self>) -> Result<(), StoreError>;
    async fn rollback(self: Box<Self>) -> Result<(), StoreError>;
}

pub enum Backend { Sqlite, Postgres }
```

Four notes on the shape.

`Store` and `Tx` are separate traits because a transaction owns a connection and a store owns a pool, and collapsing them would mean either a `&mut self` on `Store`, which forbids the concurrent reads WAL exists to allow, or a transaction handle threaded through every read signature. Splitting them also puts `commit` and `rollback` on a `Box<Self>` receiver, so the type system enforces that a transaction is consumed exactly once.

`replace_rows` takes `serde_json::Value` rather than 21 typed row structs. This is the single largest departure from the Python interface, which has 89 methods because it has one method per table. The rows in question arrive from the core's run state store as JSON, having been filed by the model one validated tool call at a time, and they leave as `INSERT` parameters; typing them here would mean 21 Rust structs, 21 `FromRow` impls, and 21 trait methods to carry values that were JSON on both sides of the trait. The typing that matters is done instead by the per-table column specification in `## Declared row outputs`, which is data rather than types: a table name resolves to an ordered column list with a type per column, and a row that does not match fails with the column named. Tension: a schema mistake is a runtime error naming a column rather than a compile error naming a field, and the 21 typed row structs the Python side has are traded for one validation table.

`markdown` is a windowed read returning `MdWindow { text, start_line, end_line, total_lines }` rather than a whole-document `String`. The Python `get_paper_md` returns the entire markdown, and its two agent-facing wrappers, `PaperstoreTools.read_file` and `cli.paper_tools.make_read_paper_tool`, both immediately window it and clamp at 200 and 500 lines. The window is the real interface and the full read is an implementation detail of it, so the trait exposes the interface. A paper is up to several thousand lines of untrusted text and an unwindowed read is a way to fill a context in one tool call.

Tension: a second storage-shaped extension duplicates this trait rather than sharing it. This is a real cost and it is accepted deliberately. `promptforge` declares no storage concept, so there is no shared place for `Store` to live; a second extension that wanted a database would write its own `Store` and its own `Tx`, and the two would be structurally similar and formally unrelated. The alternative is a `promptforge-storage` crate that both depend on, and it is worse in a specific way rather than merely unnecessary: a shared trait acquires the union of two domains' needs, so paperstore's `PaperId` and the other extension's key type both end up in it, or it becomes generic over a key and stops being readable. The cost of duplication is one file of roughly sixty lines of trait declarations. The cost of premature sharing is a fourth crate in the workspace whose changes break two extensions at once. Duplicate.

## The SQLite backend

For a developer machine, and it is the backend a first release runs on.

### Pragmas

Every one of these is set on every connection as it is established, through `SqliteConnectOptions`, because a pragma is per-connection and a pool creates connections lazily.

```rust
fn sqlite_options(path: &Path, busy_timeout: Duration) -> SqliteConnectOptions {
    SqliteConnectOptions::new()
        .filename(path)
        .create_if_missing(true)
        .journal_mode(SqliteJournalMode::Wal)
        .synchronous(SqliteSynchronous::Normal)
        .busy_timeout(busy_timeout)
        .foreign_keys(true)
        .pragma("temp_store", "MEMORY")
        .pragma("cache_size", "-32000")
        .pragma("wal_autocheckpoint", "1000")
}
```

- `journal_mode = WAL` is **required**, not tuned. The Python backend runs in the default rollback journal, where a writer takes an exclusive lock over the whole database and every reader blocks for the length of the write. `promptforge-mcp` is a second process on the same file, alongside the Python CLI, the preview server, and any Django-side reader, so without WAL a single section-long write transaction stops the entire Python pipeline. WAL gives one writer concurrent with many readers, and each reader sees a stable snapshot from the moment its transaction began. `journal_mode` is persistent in the database header rather than per-connection, so the first connection this crate opens converts the file and every later process inherits it, including the Python one, which is a silent improvement to the existing stack and the reason this change is safe to make from here.
- `synchronous = NORMAL` is the correct pairing with WAL. `FULL` fsyncs on every commit and buys durability across a power failure; `NORMAL` fsyncs at checkpoint and can lose the most recent commits in a power loss while never corrupting the database. Discard-and-rerun makes lost recent commits a re-run rather than a data loss, so the fsync is spent for nothing. Not `OFF`, which can corrupt.
- `busy_timeout` defaults to **30000 milliseconds**, configurable, against the Python backend's 5000. See `## The single-writer constraint` for why even thirty seconds is the wrong shape for the real problem.
- `foreign_keys = ON` even though the current schema declares none, so that the first foreign key anyone adds is enforced from the day it lands rather than from the day someone remembers this pragma.
- `temp_store = MEMORY` because the four queries with an `ORDER BY` or `GROUP BY` would otherwise be able to spill to a temp file next to the database.
- `cache_size = -32000` is thirty-two mebibytes, negative meaning kibibytes rather than pages. The whole `papers` table at archive scale fits, which turns the four unindexed scans into memory scans.
- `wal_autocheckpoint = 1000` is the default, restated because it is load-bearing: a long-lived reader holding a snapshot prevents checkpointing, so the WAL grows for as long as that reader lives. Every read in this crate is a short statement outside any transaction for exactly this reason.

The one thing not expressed above is the transaction start mode. **A write transaction must open with `BEGIN IMMEDIATE`, not the default `BEGIN DEFERRED`.** A deferred transaction takes no lock until its first write and then tries to promote a read snapshot to a write lock; if another writer committed in between, SQLite returns `SQLITE_BUSY_SNAPSHOT` and `busy_timeout` does not retry it, because retrying could not help. `BEGIN IMMEDIATE` takes the write lock at the start, which is a wait that `busy_timeout` does cover. For a transaction that spans a whole section this is the difference between waiting at the start and failing at the end, after the model turns have already been spent. `Store::begin` therefore issues `BEGIN IMMEDIATE` explicitly rather than taking sqlx's default; the exact API for that in 0.9.0 is in `## Open`.

### Pools

Two pools on SQLite, which is unusual and is a direct expression of what WAL provides.

- A read pool, `max_connections = 4`, serving every `Store` read method with a bare statement and no transaction.
- A write pool of exactly **one** connection, from which `begin` acquires. One connection rather than a semaphore over a larger pool, because WAL permits exactly one writer database-wide, and a pool of one makes that fact a property of the type rather than a rule someone has to remember. A second concurrent `begin` waits on pool acquisition, which is the same wait it would have taken on the lock, but it waits in Rust with a timeout this crate chose instead of inside SQLite with a timeout that is also every reader's timeout.

Postgres uses one pool, because its writers do not exclude each other.

A read issued while its own run holds a transaction does not use the read pool. `PaperstoreExt` looks the run up in its transaction map first and routes the read through `Tx::meta` or `Tx::count_rows`, so a section sees its own uncommitted writes. Without that routing, a prompt that wrote rows in one section and read them back in the next would work while a prompt that did both in one section would silently see stale data, which is the kind of difference nobody debugs on the first day.

### The single-writer constraint

The consequence of the section-as-transaction-boundary on SQLite, stated plainly because it is the largest operational fact in this document: **a run holding a section-long write transaction blocks every other writer for the length of that section.** A section is a model turn plus tool calls, so tens of seconds to minutes. With the write pool at one connection and a thirty-second acquisition timeout, two concurrent runs that both write means the second one fails to begin.

Three responses, and the choice is deliberate.

- On SQLite, cap concurrent writing runs at one and let the second wait. This is what the write pool of one does, with `acquire_timeout` set to the run deadline rather than thirty seconds, so a second run queues instead of failing. Correct for a developer machine, which is what SQLite is for.
- On Postgres, the constraint does not exist, because two transactions writing different papers touch different rows.
- The escape hatch, recorded and not built: buffer a run's writes in memory and apply them in one short transaction at `Complete`, which turns a minutes-long write into a milliseconds-long one at the cost of routing reads through the buffer. It is in `## Open` because it is a change to the mapping `design.md` specifies, not a change to this crate alone.

Tension: the section-as-transaction-boundary is right for correctness under retry and wrong for concurrency on SQLite, and the resolution is that concurrent writing runs are a production profile and production is Postgres.

### Backups

WAL adds two sidecar files, `paperstore.db-wal` and `paperstore.db-shm`, and **a copy-based backup that copies only `paperstore.db` is a backup of a database missing every committed transaction since the last checkpoint.** That is a silent data loss discovered at restore time. Two supported answers:

- Preferred: `VACUUM INTO 'backup.db'`, which writes one consistent file with no sidecars while the database stays open and in use.
- Acceptable: copy all three files together with the database quiesced, the main database file first.

The Python side's existing backup story, whatever it is, was written against a rollback-journal database with no sidecars. Converting the file to WAL from this crate changes that story for every process sharing the file, which makes this the one change here with a consequence outside the workspace. Tension: a correctness fix to the concurrency model silently invalidates a backup procedure nobody in this repository owns.

## The Postgres backend

It does not exist in either repository and building it is in scope. It is the production backend, it stores rows and nothing else, and it has no S3 half: the artifact files stay under the Python side's workspace directory, so `wg21-paperflow/DESIGN.md`'s Postgres-plus-S3 design is a superset of what this crate builds.

### Connection pooling

```rust
fn pg_pool(cfg: &PgConfig) -> PgPoolOptions {
    PgPoolOptions::new()
        .max_connections(cfg.max_connections)
        .min_connections(1)
        .acquire_timeout(Duration::from_secs(30))
        .idle_timeout(Duration::from_secs(600))
        .max_lifetime(Duration::from_secs(1800))
        .test_before_acquire(true)
}
```

- `max_connections` defaults to **16**, matching the gateway's global in-flight ceiling. A run holds at most one write transaction at a time, so sixteen is the number of runs that can be in a section concurrently, and sixteen is already the number of runs that can have a model turn in flight. Deriving it from a number `design.md` settled is better than picking one, and it means one dial moves both.
- `acquire_timeout` is thirty seconds, matching the gateway's admission timeout, so a client waiting on a database connection and a client waiting on a GPU permit wait the same length of time and a caller sees one timeout shape rather than two.
- `min_connections(1)` keeps one connection warm so `validate` at boot and the first run do not both pay a connect.
- `max_lifetime` at thirty minutes so a rolling Postgres restart or a failover drains rather than pinning dead sockets, and `test_before_acquire` so a connection killed server-side surfaces as a retry rather than as a failed run.

Two session settings are set on every connection through `PgConnectOptions::options`, and one of them is a mitigation rather than a tuning knob:

- `application_name = promptforge` so `pg_stat_activity` attributes a long transaction to this service rather than to an anonymous client. Note that 0.9.0 changed `PgConnectOptions::options()` to escape its input automatically, so a value with a space no longer needs hand-quoting.
- `idle_in_transaction_session_timeout` set above the longest expected section and below the run deadline. **This is what reaps the transaction that a dead run left open**, and it exists because the `Extension` trait has no run-terminal event. It is a server-side backstop for a client-side gap, it is the reason the gap is survivable in production, and SQLite has no equivalent, which is why the same gap is worse on a developer machine. See `## Verdict on the trait`.

### Schema ownership and migrations

Migrations are SQL files under `migrations/`, embedded by `sqlx::migrate!` so the binary carries its own schema. They run on `Store::migrate`, which is called from `PaperstoreExt::new` only when configuration asks:

```toml
[extensions.paperstore]
backend = "postgres"
url = "postgres://promptforge@10.0.0.11/paperstore"
migrate = false
max_connections = 16
busy_timeout = "30s"
```

`migrate` defaults to `false` on Postgres and `true` on SQLite, and that asymmetry is a decision rather than caution. A service that migrates a shared production database at boot means every restart is a schema event, two service instances starting together race the same `ALTER TABLE`, and the Django deploy that also owns tables in that database has no say. SQLite is the opposite case: the file belongs to one developer, is created if missing, and a manual migration step there is friction with no payoff. Tension: a production schema change is a deploy step someone has to remember, and forgetting it produces a `SchemaMismatch` at boot rather than a broken run, which is the failure this arrangement is choosing.

`ping` is not a `SELECT 1`. It checks that every table in the allowlist exists and that its columns match the expected names and types, reading `information_schema.columns` on Postgres and `pragma_table_info` on SQLite. That check is why a forgotten migration is a boot failure with the missing column named.

### How the Django site's mirror code stays unchanged

The site mirrors from paperstore into its own tables and the swap is invisible to it, because three things are held fixed.

- **Column names and types are byte-identical to the SQLite schema.** Timestamps stay `text` holding ISO-8601 rather than becoming `timestamptz`, JSON stays `text` holding `json.dumps` output rather than becoming `jsonb`, and the zero-or-one integer flags keep their names. The site's `SELECT` list, its `WHERE` clauses, and the Python types it gets back are unchanged. A `timestamptz` column would be more correct in isolation and would break the mirror's string comparisons on `mailing_date >= '2026-03'`, which is real code in `list_papers_since`.
- **Paper ids stay uppercase.** Whatever fold the site performs between its lowercase paper-keyed models and paperstore's uppercase ids stays exactly where it is and keeps working.
- **Nothing writes the site's tables.** The site owns its write path, its `Organization` resolution, and its append-only evaluation history. This crate writes paperstore tables, the site mirrors on its own schedule, and the two diverge until it does.

Tension: holding the column types fixed for the mirror's benefit means importing SQLite's type poverty into Postgres, so a Postgres deployment has text timestamps and integer booleans it did not need, and the day the mirror is rewritten is the day that becomes technical debt with no owner.

## Behavioral parity

Two backends must be indistinguishable through the `Store` trait. Nine things differ underneath, and every one of them is either normalized in the schema, normalized in Rust, or accepted and documented.

| Divergence | What bites | Resolution |
|---|---|---|
| No boolean in SQLite | Eleven columns are zero-or-one `INTEGER` in SQLite and want `boolean` in Postgres. `BOOLEAN DEFAULT 0` in `assay_pids` is NUMERIC affinity in SQLite and a type error in Postgres, where the literal must be `false`. | Declare `integer` in both and keep the Rust type `i64`, because the Django mirror reads these columns. The alternative, `boolean` in Postgres with sqlx converting to `bool`, is cleaner Rust and changes what the mirror sees. |
| `INTEGER PRIMARY KEY AUTOINCREMENT` | `external_citations` uses SQLite-only syntax. | `bigint GENERATED BY DEFAULT AS IDENTITY` in the Postgres migration. The column is never read by id and is written only by replace-all, so nothing depends on the values matching. |
| `TEXT DEFAULT ''` is nullable | SQLite lets `NULL` into every one of those columns, which is why `parse_authors_raw` handles `None`. In Rust that is `Option<String>` everywhere or a panic somewhere. | `text NOT NULL DEFAULT ''` in both migrations, with a SQLite backfill of existing `NULL` to the empty string. One Rust type, `String`, and the empty string keeps its existing meaning of absent. |
| `INSERT OR REPLACE` semantics | SQLite's `INSERT OR REPLACE` **deletes the row and inserts a new one**, so columns absent from the statement revert to their defaults and delete triggers fire. Postgres has no such statement, and `ON CONFLICT DO UPDATE` updates in place. Four existing writes use it. | Use `ON CONFLICT (pk) DO UPDATE SET` everywhere, which is valid on both and is what SQLite's own upsert grammar was copied from. The in-place semantics are also the intended ones: `upsert_paper` must preserve `source_file` and `markdown_path`, which a delete-and-insert would clear. |
| `LIKE` case sensitivity | SQLite's `LIKE` is case-insensitive for ASCII by default; Postgres's is case-sensitive. `find_latest_revision` uses `WHERE paper_id LIKE 'P4003R%'` and would silently return fewer rows on Postgres. | No `LIKE` anywhere. `latest_revision` selects a half-open range over the primary-key index and filters the revision number in Rust, which is index-friendly on both and depends on no collation. |
| Text ordering and collation | `=` on text is byte-exact on both, but `ORDER BY paper_id` follows the database collation, which is `BINARY` on SQLite and locale-dependent on Postgres. Two backends return the same rows in different orders. | Every ordering a caller can observe is applied in Rust after the fetch. `ORDER BY` survives in SQL only where the sort key is numeric, as in `get_paper_citations`'s `count DESC`. |
| Integer width | SQLite `INTEGER` is 64-bit; Postgres `integer` is 32-bit. A `line_count` on a large paper is safe either way, and the mismatch is silent until it is not. | `bigint` in Postgres wherever the Rust type is `i64`, `integer` only where a 32-bit range is part of the meaning. `REAL` becomes `double precision`. |
| Transaction isolation | SQLite in WAL gives a transaction a stable snapshot for its whole life. Postgres defaults to READ COMMITTED, where each statement sees newly committed rows. A section-long transaction therefore sees different things on the two backends. | Accept READ COMMITTED and forbid the dependency rather than raise the isolation level. REPEATABLE READ would match SQLite and introduce serialization failures, and a serialization failure on a section-long transaction cannot be retried, because retrying would mean re-running the model turns that produced the rows. |
| Concurrent writers | One writer database-wide on SQLite; row-level locks on Postgres. | Structural, and the pools express it: one write connection on SQLite, sixteen on Postgres. This is the divergence that is not normalized, and `## The single-writer constraint` is where it is documented instead. |

### The shared suite

One test module, one list of cases, parameterized over a `Vec<Arc<dyn Store>>`.

```rust
async fn backends() -> Vec<(Backend, Arc<dyn Store>)> {
    let mut v = vec![(Backend::Sqlite, sqlite_temp().await)];
    if let Ok(url) = std::env::var("PAPERSTORE_TEST_PG_URL") {
        v.push((Backend::Postgres, postgres(&url).await));
    }
    v
}
```

Every case runs against every backend and asserts identical observable behaviour: the same rows, the same order, the same counts, the same `StoreError` variant. SQLite runs against a temporary file rather than an in-memory database, because an in-memory database cannot exercise WAL, cannot be opened by a second connection, and is therefore unable to test the two things most likely to be wrong.

Postgres is skipped when `PAPERSTORE_TEST_PG_URL` is unset, so a developer with no server runs the SQLite half, and **CI sets it, so a skip is impossible where it matters.** The suite asserts at its start that at least one Postgres backend is present when `CI` is set, because a silently skipped parity suite is worse than no parity suite. A CI service container rather than testcontainers, since the runner already has Docker and a service container is four lines of YAML.

## The `Extension` impl

This is the transactional reference case, and the section `design.md`'s build path points at to retire its riskiest assumption.

```rust
pub struct PaperstoreExt {
    inner: Arc<Inner>,
    names: Vec<ToolName>,
}

struct Inner {
    store: Arc<dyn Store>,
    /// Tables this deployment will accept rows for, from configuration,
    /// each with its ordered column specification.
    tables: BTreeMap<String, TableSpec>,
    /// One open write transaction per run, plus its savepoint stack and the
    /// row counts a declared `Rows` output will report.
    runs: Mutex<BTreeMap<RunId, RunState>>,
    /// Committed row counts, surviving the transaction that produced them.
    counts: Mutex<BTreeMap<RunId, BTreeMap<String, u64>>>,
}

struct RunState {
    tx: Option<Box<dyn Tx>>,
    /// Savepoint names in acquisition order, so a `NestedComplete` releases
    /// the one a `NestedEnter` took.
    savepoints: Vec<String>,
    /// Table to the row count of the most recent replace-all write.
    /// Not a running sum, because a second write to one table supersedes
    /// the first rather than adding to it.
    rows: BTreeMap<String, u64>,
    /// The section the transaction was opened for, so an out-of-order
    /// `Complete` is a detected bug rather than a wrong commit.
    section: usize,
}

impl PaperstoreExt {
    /// Connects, pools, and migrates if configured. The host calls this while
    /// loading configuration, so an unreachable database fails before any
    /// prompt is registered.
    pub async fn new(cfg: &PaperstoreConfig) -> Result<Self, StoreError>;
}
```

The state sits in a separate `Inner` behind an `Arc` for the same reason `design-classify.md` gives: `tools` receives `&self` and cannot hand itself to a closure. Both maps are `tokio::sync::Mutex` rather than `std` mutexes, because a section boundary awaits inside the critical region while it commits.

```rust
#[async_trait]
impl Extension for PaperstoreExt {
    fn name(&self) -> &str {
        "paperstore"
    }

    fn provides(&self) -> &[ToolName] {
        &self.names
    }

    fn tools(&self) -> Vec<ToolDef> {
        vec![
            meta_def(self.inner.clone()),
            latest_def(self.inner.clone()),
            md_def(self.inner.clone()),
            cites_def(self.inner.clone()),
            upsert_def(self.inner.clone()),
            rows_def(self.inner.clone()),
        ]
    }

    fn bind_lua(&self, lua: &Lua) -> Result<Vec<(String, Value)>, ExtError> {
        let t = lua.create_table()?;
        t.set("meta", lua.create_async_function(bind(self.inner.clone(), Op::Meta))?)?;
        t.set("latest", lua.create_async_function(bind(self.inner.clone(), Op::Latest))?)?;
        t.set("cites", lua.create_async_function(bind(self.inner.clone(), Op::Cites))?)?;
        t.set("upsert", lua.create_async_function(bind(self.inner.clone(), Op::Upsert))?)?;
        t.set("rows", lua.create_async_function(bind(self.inner.clone(), Op::Rows))?)?;
        Ok(vec![("paper".to_string(), Value::Table(t))])
    }

    fn validate(&self) -> Result<(), ExtError> {
        block_on(self.inner.store.ping())?;
        for (name, spec) in &self.inner.tables {
            block_on(self.inner.store.check_table(name, spec))?;
        }
        Ok(())
    }

    async fn on_section(&self, ev: &SectionEvent) -> Result<(), ExtError> {
        let mut runs = self.inner.runs.lock().await;
        match *ev {
            SectionEvent::Enter { run, section } => {
                let tx = self.inner.store.begin().await?;
                let prior = runs.insert(run, RunState::new(tx, section));
                debug_assert!(prior.is_none(), "Enter without a matching Complete");
            }

            SectionEvent::Complete { run, section } => {
                let Some(st) = runs.remove(&run) else { return Ok(()) };
                if st.section != section {
                    return Err(StoreError::LifecycleOrder { want: st.section, got: section }.into());
                }
                if let Some(tx) = st.tx {
                    tx.commit().await?;
                }
                self.inner.counts.lock().await.insert(run, st.rows);
            }

            SectionEvent::Retry { run, section, .. } => {
                if let Some(st) = runs.remove(&run) {
                    if let Some(tx) = st.tx {
                        tx.rollback().await?;
                    }
                }
                let tx = self.inner.store.begin().await?;
                runs.insert(run, RunState::new(tx, section));
            }

            SectionEvent::NestedEnter { run, depth, .. } => {
                let Some(st) = runs.get_mut(&run) else { return Ok(()) };
                let name = format!("sp_{depth}_{}", st.savepoints.len());
                st.tx.as_mut().ok_or(StoreError::NoTransaction)?.savepoint(&name).await?;
                st.savepoints.push(name);
            }

            SectionEvent::NestedComplete { run, .. } => {
                let Some(st) = runs.get_mut(&run) else { return Ok(()) };
                let Some(name) = st.savepoints.pop() else { return Ok(()) };
                st.tx.as_mut().ok_or(StoreError::NoTransaction)?.release(&name).await?;
            }
        }
        Ok(())
    }

    async fn shutdown(&self) -> Result<(), ExtError> {
        let mut runs = self.inner.runs.lock().await;
        for st in runs.values_mut() {
            if let Some(tx) = st.tx.take() {
                tx.rollback().await?;
            }
        }
        runs.clear();
        self.inner.store.close().await;
        Ok(())
    }
}
```

`name` returns `"paperstore"` and not `"sqlite"` or `"postgres"`. This is a departure from `design-classify.md`, where `ClassifyExt::name` returns `"onnx"` on the argument that the extension name is the backing implementation. The argument does not transfer: a configuration line binding `paper_upsert` must not change when a deployment moves from SQLite to Postgres, because `design.md`'s whole point about tool binding is that a prompt must not know whether the store is SQLite or Postgres. The backend is a field inside `[extensions.paperstore]`, one extension serves both, and `Backend` is a diagnostic. Tension: two crate docs now give opposite answers to what `name` means, and the rule that reconciles them is that the name is whatever a binding must keep stable across a swap.

`provides` returns six canonical names, so landing this crate adds six words to the core's canonical set. That is the one core change this extension requires beyond the trait changes below, and it is an edit to a list.

`validate` is synchronous because the trait says so, and it does async work, so it blocks. That is the smallest of the four problems below and the least defensible code in this file: `block_on` inside a runtime worker panics on a current-thread runtime, and it works here only because boot is single-threaded and nothing else is scheduled. It should be `async fn validate`.

`bind_lua` binds five of the six operations under one table named `paper`, matching the canonical prefix. `paper_md` is absent from Lua and the reason is in `## Surfaces`.

## Verdict on the trait

**The `Extension` trait as originally designed was not sufficient for a transactional extension, and all four changes below have since landed in `design-core.md`.** The finding is kept rather than deleted, because the reasoning is what a future extension author needs when they hit a fifth gap. It was close: `&self` with interior mutability is fine, the registration ordering is right, and the five-variant `SectionEvent` mapped onto begin, commit, rollback, and savepoints with no contortion. Four things were missing, two of them blocking. This is the answer to the question `design.md` said was worth a day to find out, and the day was worth it.

### One: `on_section` must be async

The trait declares `fn on_section(&self, _ev: &SectionEvent) -> Result<(), ExtError>`. A transaction boundary is network or disk I/O: `BEGIN IMMEDIATE`, `COMMIT`, `ROLLBACK`, `SAVEPOINT`. A synchronous hook cannot await any of them. The three ways out are all bad. `block_in_place` plus `Handle::block_on` panics on a current-thread runtime and is forbidden inside an existing `block_on`. Spawning the commit and returning `Ok(())` discards the result, so a failed commit becomes a successful run. A dedicated writer task with a channel and a blocking receive on the reply reintroduces the same block on the reply.

Required: `async fn on_section(&self, ev: &SectionEvent) -> Result<(), ExtError>`, with `#[async_trait]` on the trait, which the trait already needs for `ToolFn`. `validate` and `shutdown` need the same for the same reason. This is a small, mechanical change to `design-core.md` and it is not optional.

### Two: there is no run-terminal event, and the leak is a pooled connection

`SectionEvent` has `Enter`, `Complete`, `Retry`, `NestedEnter`, and `NestedComplete`. Nothing fires when a run ends. Every failure path in `RunError` therefore leaves an open transaction: `PostconditionExhausted`, `MissingRequiredOutput`, `Deadline`, `JumpLimit`, `TaskDepth`, `TaskBudget`, `Unimplemented`, a Lua error, a gateway error, a tool error. `shutdown` is process shutdown, not run scope. So `Inner::runs` accumulates one entry per failed run, each holding a connection out of the pool and a write lock on the database.

On SQLite that is total: the write pool has one connection, so **the first failed run wedges every subsequent write until the process restarts.** On Postgres it is pool exhaustion after sixteen failed runs. `idle_in_transaction_session_timeout` reaps it server-side, which is why production survives, and there is no SQLite equivalent, which is why a developer machine does not.

This is the difference between recovery being to run it again, which is the system's stated model, and recovery being to restart the service. It is the trait's real insufficiency.

Required: a run-terminal signal. Either a sixth variant, which is the smaller change:

```rust
pub enum SectionEvent {
    Enter { run: RunId, section: usize },
    Complete { run: RunId, section: usize },
    Retry { run: RunId, section: usize, attempt: u32 },
    NestedEnter { run: RunId, section: usize, depth: u32 },
    NestedComplete { run: RunId, section: usize, depth: u32 },
    /// Emitted exactly once per run, on every path out of `Executor::run`,
    /// including every error path and the deadline. `ok` is false when the
    /// run did not complete.
    RunEnded { run: RunId, ok: bool },
}
```

or a separate `async fn on_run_end(&self, run: RunId, ok: bool)`. The variant is preferable because it inherits the existing delivery and ordering guarantees rather than adding a second hook with its own. Either way the contract has to be that it fires on **every** path out of `run`, which means the core emits it from a guard rather than from the happy path, or the guarantee is worthless.

`Tx::commit` and `Tx::rollback` taking `Box<Self>`, and a sqlx transaction rolling back when dropped, are the partial safety net that makes the gap survivable rather than corrupting: the rows are never wrong, only the connection is stuck. That is why this is a blocker on availability and not on correctness.

### Three: the nested events cannot express concurrent fan-out

`NestedEnter { run, section, depth }` and `NestedComplete { run, section, depth }` identify a nesting level and not a task. `fanout` runs up to `max_fanout_concurrency` subagent tasks at once, all in one run, all at the same depth. Savepoints on one connection are strictly last-in-first-out, so three concurrent tasks at depth two produce three interleaved `SAVEPOINT` and `RELEASE` pairs against one transaction, and a `RELEASE` from the task that finished first releases the savepoint the task that started last is holding. The result is not an error; it is silently released nesting.

There is also no `NestedRetry` and no nested failure variant, so a subagent task that failed has no way to say `ROLLBACK TO SAVEPOINT`, which is the entire reason a savepoint was taken.

Required, in preference order: a task identity on both nested variants, `task: TaskId`, plus a `NestedFailed { run, task }`; or, if that is too large a change, an explicit statement in `design-core.md` that fan-out is serialized when any registered extension declares that it holds section-scoped state, which is a capability declaration the trait also does not have. The workaround available today without any core change is for this crate to take a savepoint only at depth transitions it can observe as ordered, which in practice means ignoring `NestedEnter` during a fan-out and accepting that a failed subagent's writes are rolled back with the whole section rather than alone. That is a correctness-preserving degradation and it is what the implementation should do until the trait carries a task identity.

### Four: two smaller gaps in the plumbing

- **`RunError` has no variant for an extension lifecycle failure.** A failed `COMMIT` on `Complete` has to fail the run, and `RunError` offers `Tool(ToolError)`, which is a lie, or nothing. `ValidateError::Extension(ExtError)` exists for boot. Add `RunError::Extension(ExtError)`.
- **There is no way to report a row count for a declared `Rows` output.** See `## Declared row outputs`. One method with a default satisfies it.

### What is sufficient

Everything else about the trait holds up, and this is worth saying because three of the four problems are additions rather than redesigns.

- `&self` with interior mutability is right. A `&mut self` hook would forbid the concurrent reads that make the extension usable.
- Delivering every event to every extension, whether or not it participated in the section, is exactly what a transaction holder needs. A section that called no `paper_*` tool still has to commit its empty transaction.
- Registration order for `Enter` and reverse order for `Complete` gives correct nesting when a future extension holds a resource that depends on this one.
- `Retry` meaning rollback-and-begin rather than rollback-only is unambiguous from `design-core.md`'s execution flowchart, where `Retry` leads back to the Lua block and no second `Enter` is emitted. It is now stated in the core doc's `SectionEvent` comment so the next implementer does not have to derive it from a diagram.

So: **one trait carries both shapes.** All four changes have landed in `design-core.md`, including `holds_section_state` as the declared-serialization escape hatch for the fan-out interleaving case, so this crate no longer needs the degradation described under point three and can take a savepoint per `TaskId`. The assumption is retired as substantially correct rather than as either confirmed or refuted, every change was additive, no special case for either extension was required, and `design.md`'s confidence on `Extension trait shape` has moved to `high`.

## Canonical tool names

One canonical name is exactly one function. Six names share the `paper` prefix, which makes them a family, and the family reaches Lua as one table named `paper`. Every name is derived from a call site that exists in `wg21-paperflow` rather than from a guess about what a prompt might want.

| Canonical name | Function | Derived from |
|---|---|---|
| `paper_meta` | Metadata for one exact paper id. | `PaperstoreTools.paper_meta`, `StorageBackend.get_meta` |
| `paper_latest` | Metadata for the highest revision of a bare paper number. | `PaperstoreTools.paper_meta_latest`, `SqliteBackend.find_latest_revision` |
| `paper_md` | A line window of one paper's converted markdown. | `cli.paper_tools.make_read_paper_tool`, `PaperstoreTools.read_file`, `get_paper_md` |
| `paper_cites` | Citations out of and into one paper. | `get_paper_citations`, `get_incoming_citations` |
| `paper_upsert` | Insert or update one paper's metadata row. | `upsert_year` narrowed to one paper. The name `design.md` fixes. |
| `paper_rows` | Replace every row for one paper in one target table. | The eleven `store_*` and thirteen `store_assay_*` replace-all writes, collapsed into one function over a table name. |

Six rather than twenty-four. The Python interface has one method per table because each one takes a differently shaped domain object; the rows here arrive as JSON from the run state store and leave as `INSERT` parameters, so the table name is a parameter rather than a method name. That is the collapse that keeps the canonical vocabulary at six words instead of twenty-four, and it is only safe because the table name is validated against an allowlist rather than trusted.

Not included, and each for a reason:

- The whole ingestion surface: `put_source`, `write_paper_md`, `write_agora_json`, `write_paper_image`, `reconcile`, `advance_status`, `fail_paper`. Python owns the pipeline, and a prompt that could advance a pipeline stage would be a second scheduler.
- `paper_clear`. Replace-all makes it redundant: `paper_rows` with an empty array is the clear, which is one function fewer and one fewer way for a clear and a write to disagree.
- `paper_search`. Search is `promptforge-ext-search`, and a full-text search over paper bodies here would be a second search provider under a different name.
- Every path accessor. `get_paper_md_path`, `get_debug_md_path`, `get_source_path`: a prompt emits to a declared output name and never sees a path, so an extension handing one out is handing a prompt something `design.md` spent a non-goal removing.

## Surfaces

`Surfaces` is this crate's declaration and the core enforces it: a `LuaOnly` function is absent from the schema list the model sees, a `ToolOnly` function is absent from the Lua environment.

| Function | Surfaces | Why |
|---|---|---|
| `paper_meta` | `Both` | A model mid-run asking for a paper's title, audience, or line count is a legitimate choice, and a Lua precondition asserting `paper.meta{id}.line_count > 0` before a section runs is the same call. Cheap, read-only, and no untrusted text in the result beyond fields the Python pipeline already extracted. |
| `paper_latest` | `Both` | Same reasoning. Resolving `P4003` to `P4003R3` is a step either caller legitimately takes, and the Python side already exposes it as a model tool. |
| `paper_cites` | `Both` | A read a model uses to follow a citation graph and a prompt author uses to assert that citations were extracted before a section that analyses them. |
| `paper_md` | `ToolOnly` | Browsing a paper incrementally is exactly a model decision, which is why the Python side exposes it as a model tool and nothing else. It is off the Lua surface because of what the text is: a paper body is untrusted content, and a Lua block that pulled five hundred lines into `state` would have that text substituted into the section body by `{{ state.x }}` with no guard, because the core's substitution wraps nothing. As a tool the return is wrapped in guard delimiters, which is what `pipeline.tools.inject_untrusted` does on the Python path. Lua has no need for the body: `paper_meta` gives it `line_count`. |
| `paper_upsert` | `LuaOnly` | A write, and a write of metadata: title, authors, year, url, disposition. A model must not invent a paper's authors, and there is no prompt where it should. A prompt author setting up a metadata row before a section is deterministic setup, which is what the Lua layer is for. |
| `paper_rows` | `LuaOnly` | The care the write case wants, and the more interesting of the two. The model files findings into the core run state store one validated tool call at a time, so every field crossed a boundary and the aggregate is well-formed by construction. A model-callable bulk row writer would undo that: one malformed call could write an arbitrary batch, and the table name would enter the model's vocabulary, where a hallucinated one is a plausible failure. The prompt author calls `paper.rows{ table = "assay_finding", id = pid, rows = store.get("findings") }` at the section boundary over state the model filed. This is the same argument `design-core.md` makes for `Task` returning a serialized store rather than a composed JSON object. |

Two reads are `Both` and one is `ToolOnly`, so the model surface is three names and the Lua surface is five. Tension: a prompt author who wants the model to decide when to write has no way to express it, and that is this crate's declaration rather than something the core enforces on writes generally.

A `Both` read is safe during an open transaction only because it routes through it. `Inner::runs` is consulted on every read, keyed by `CallCtx::run`, so a read inside a section that has written sees its own uncommitted rows. Without that routing the two surfaces would disagree with each other depending on whether a write had happened yet in the same section.

## Declared row outputs

A prompt declares an output and never a destination:

```yaml
outputs:
  - name: findings
    kind: rows
    table: assay_finding
    required: true
```

Resolution, end to end:

1. `prompts.toml` maps the output name to this extension with `[outputs] findings = { extension = "paperstore" }`. The core turns that into `Root::Extension("paperstore")` and the frontmatter's `kind: rows` into `OutputKind::Rows { table: "assay_finding" }`.
2. At boot, `promptforge-mcp` resolves `OutputRoots` and checks that an extension named `paperstore` is linked. That check exists today. **The check that the extension accepts `assay_finding` does not**, and `design.md` requires it: startup rejects a prompt whose declared output names a missing output root or target table. Only the extension knows its own tables.
3. During the run, `paper_rows` writes the rows inside the section's transaction and records the count in `RunState::rows` keyed by table. The count is the row count of the most recent replace-all write for that table, not a running sum, because a second write to one table supersedes the first.
4. On `Complete` the counts move from `RunState` into `Inner::counts`, which outlives the transaction, so the count is available after the commit that made it true.
5. At run end the core asks this extension for the count and builds `Destination::Rows { table, count }`. `promptforge-mcp` maps that to `OutputRef { kind: rows, table, rows }` and the text block reads `findings: 7 rows in assay_finding`.

Step 5 has no method to call. Two additions to `Extension`, both defaulted so no other extension notices:

```rust
/// Rows this extension holds for `table` after `run`. Called once per
/// declared `OutputKind::Rows` output when a run finishes.
fn output_rows(&self, run: RunId, table: &str) -> Result<u64, ExtError> { Ok(0) }

/// Whether this extension will accept rows for `table`. Checked at boot,
/// for every declared rows output whose root resolves to this extension.
fn accepts_table(&self, _table: &str) -> bool { false }
```

`accepts_table` could be avoided by having the host pass its `[outputs]` table names into `PaperstoreExt::new` and letting `validate` check them, which needs no core change at all. It is a trait method anyway, because the core is the thing that resolved `Root::Extension` and the core is where the error belongs; pushing it into configuration means the same check written once per host binary. `output_rows` cannot be avoided: the core owns `Destination` and nothing else can produce the number.

The alternative considered and rejected was for the core to sum a `rows` field out of tool results whose extension matches the output root. It needs no trait change and it requires the core to know that a JSON result field named `rows` means something, which is a domain convention in a crate that declares no domain.

The table allowlist is configuration and the specification is data:

```toml
[extensions.paperstore.tables.assay_finding]
table = "assay_findings"
key = ["paper_id", "uid"]
columns = [
    { name = "uid",         type = "int",  required = true },
    { name = "title",       type = "text", required = true },
    { name = "lens",        type = "text", required = true },
    { name = "severity",    type = "text", required = true },
    { name = "quote",       type = "text", default = "" },
    { name = "loc_line",    type = "int",  default = 0 },
    { name = "explanation", type = "text", default = "" },
    { name = "survived",    type = "flag", default = 1 },
    { name = "major",       type = "flag", default = 0 },
]
```

The declared name and the physical table are separate, so `assay_finding` in a prompt binds to `assay_findings` on disk and a prompt does not carry the Python schema's pluralization. A row that omits a required column, carries an unknown key, or has the wrong JSON type fails with the column named. `TableName` is constructed only from this map, which is what makes the interpolated table name in the `DELETE` and the `INSERT` safe enough to reach `AssertSqlSafe`.

## Paper id case

Uppercase in every database column, lowercase in every filename stem, and **the fold happens in exactly one place: `PaperId::parse`.**

```rust
impl PaperId {
    pub fn parse(raw: &str) -> Result<Self, StoreError> {
        let s = raw.trim().to_ascii_uppercase();
        if !PID.is_match(&s) {
            return Err(StoreError::BadPaperId(raw.to_string()));
        }
        Ok(PaperId(s))
    }
}
```

`PaperId` is the only way to name a paper anywhere in this crate. No statement takes a `&str` id, no path is built from a `&str`, and no method calls `to_ascii_uppercase` or `to_ascii_lowercase` outside `parse` and `stem`. Every entry point parses: a tool argument struct deserializes into `PaperId` through a `Deserialize` impl that calls `parse`, so a malformed id fails at argument validation with the offending string in the message rather than as a missing row later.

The shape is one or more ASCII letters, one or more digits, and an optional `R` plus digits: `P4003R2`, `N4950`, `D1234R0`. Derived from what the Python actually matches, which is a single leading letter in `_IMAGE_FILENAME_RE` and `P` plus digits in `paper_meta_latest`, widened to letters because `CWG` and `LWG` ids exist in the corpus and a narrower rule would reject them at the boundary rather than at the query.

`stem()` is the lowercase form and is used only where a filename is constructed. That is one method, so the `paper_id.strip().upper().lower()` construction in the Python `get_debug_md_path`, `get_trace_md_path`, and `write_assay_md` has no analogue here.

This closes the twenty-six-method hole in the Python assay path by construction rather than by discipline: there is no unfolded id to pass, because there is no `String` id.

Tension: every cross-boundary lookup still needs a fold, and this only guarantees that the fold is this crate's problem and happens once. The Django site's lowercase paper keys are folded on the site's side, where they already are, and nothing here changes that.

## Idempotent replace-all writes

Every write this crate performs is a replace-all write from deterministic content, and that is what makes discard-and-rerun safe with no cleanup.

```sql
DELETE FROM assay_findings WHERE paper_id = $1;
INSERT INTO assay_findings (paper_id, uid, title, lens, severity, quote, loc_line, explanation, survived, major)
VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);
```

The pair is inside the section's transaction, so a reader sees the old set or the new set and never a partial one. `paper_upsert` is the same idea in upsert form: `ON CONFLICT (paper_id) DO UPDATE SET` over the metadata columns, preserving `source_file`, `markdown_path`, `agora_path`, `assay_path`, and `status`, which the Python pipeline owns and this crate must not clear.

What follows, and it is the whole recovery model:

- A run that dies at section five having committed sections one through four needs no cleanup. The rerun writes sections one through four again, and each write replaces rather than appends, so the end state is the same as if the first run had never happened.
- There is no partial state to detect, so there is no repair step, no forcing flag, and no reconcile pass for prompt-written rows.
- A prompt that produced zero rows still writes: `paper_rows` with an empty array deletes and inserts nothing, so a paper whose findings were retracted ends with zero rows rather than with the previous run's findings.
- The empty-state ambiguity that `store_paper_citations` solves with `citations_extracted_at` is solved the same way where it matters: a table whose empty state is meaningful carries a stamp column in its specification, written on every replace-all write including the empty one.

The precondition is that content is deterministic from the same source, which is a property of the prompt rather than of this crate. A prompt whose model output varies run to run still rewrites cleanly; it just rewrites something different. That is the same guarantee `wg21-paperflow/ARCHITECTURE.md` already claims for file writes: duplicate work is harmless because writes are atomic and content is deterministic from the same source.

Tension: replace-all forecloses append-only history inside these tables, so a prompt that wanted to accumulate across runs cannot, and the Django site's append-only evaluation rows are exactly that shape and are exactly why the site owns them.

## Errors

```rust
#[derive(Debug, thiserror::Error)]
pub enum StoreError {
    // Configuration and boot.
    #[error("paperstore url is not a supported backend: {0}")]
    BadUrl(String),
    #[error("cannot reach the paperstore database: {0}")]
    Unreachable(String),
    #[error("table `{table}` is missing column `{column}`; a migration has not been applied")]
    SchemaMismatch { table: String, column: String },
    #[error("table `{0}` is not in this deployment's allowlist")]
    UnknownTable(String),
    #[error("column `{column}` of `{table}` declares type `{ty}`, which is not int, text, flag, or real")]
    BadColumnType { table: String, column: String, ty: String },
    #[error("migrations are disabled for this backend; apply them and restart")]
    MigrationsDisabled,

    // Retryable at the statement level.
    #[error("the database is locked by another writer")]
    Busy,
    #[error("the transaction lost a race and must be retried")]
    Serialization,
    #[error("no connection available within {0:?}")]
    PoolTimeout(Duration),
    #[error("connection lost mid-statement: {0}")]
    Disconnected(String),

    // Terminal at the call level.
    #[error("`{0}` is not a paper id")]
    BadPaperId(String),
    #[error("paper `{0}` is not in the store")]
    NoPaper(PaperId),
    #[error("paper `{0}` has no converted markdown")]
    NoMarkdown(PaperId),
    #[error("row {index} for `{table}` is missing required column `{column}`")]
    MissingColumn { table: String, index: usize, column: String },
    #[error("row {index} for `{table}` has an unknown column `{column}`")]
    UnknownColumn { table: String, index: usize, column: String },
    #[error("row {index} for `{table}`: column `{column}` wanted {want} and got {got}")]
    ColumnType { table: String, index: usize, column: String, want: &'static str, got: &'static str },
    #[error("constraint violated writing `{table}`: {detail}")]
    Constraint { table: String, detail: String },

    // Lifecycle, all of them bugs rather than conditions.
    #[error("no write transaction is open for this run")]
    NoTransaction,
    #[error("a write transaction is already open for this run")]
    TxAlreadyOpen,
    #[error("section lifecycle out of order: opened at {want}, completed at {got}")]
    LifecycleOrder { want: usize, got: usize },
    #[error("paperstore was shut down")]
    ShutDown,
}

impl StoreError {
    /// True for the four variants a retry can fix.
    pub fn retryable(&self) -> bool {
        matches!(
            self,
            Self::Busy | Self::Serialization | Self::PoolTimeout(_) | Self::Disconnected(_)
        )
    }
}

impl From<StoreError> for ExtError { /* boot and lifecycle surface */ }
impl From<StoreError> for ToolError { /* call surface */ }
```

The split is between what a retry can fix and what it cannot, because that is the only distinction that changes behaviour. **Retryable errors are retried inside this crate and never reach the model.** `Busy`, `Serialization`, `PoolTimeout`, and `Disconnected` get bounded retries with jittered backoff at the statement level, because the model has no useful response to `SQLITE_BUSY` and burning a turn on one is worse than waiting forty milliseconds. If the retries are exhausted the error surfaces as a failed tool call and the run is discarded and rerun, which is the system's recovery model rather than this crate's.

What the model sees is the `Display` text and nothing else. Concretely, from a `paper_meta` call on a paper that is not in the store, the tool result is `paper P4003R2 is not in the store`. That is a complete instruction to a model: it knows what it asked for, that the answer is absence rather than failure, and that a retry with the same argument will not help.

Three rules on what never reaches the model:

- No SQL. A statement in a tool result teaches the model that SQL is a thing it can influence.
- No connection string, no host, no file path. An `Unreachable` at call time surfaces as `the paperstore database is unavailable`, with the detail in the log.
- No row dumps in an error. `Constraint` carries the table and the database's own detail string, which names a column and a value, and that is the one place a value can leak. It is accepted because a constraint violation with no value named is unactionable, and the values in question are rows the model itself just filed.

Boot-time variants have a different audience and get the opposite treatment: `SchemaMismatch` names the table and the column, because the reader is an operator who has to decide whether to run a migration.

`thiserror` throughout, and `anyhow` appears nowhere in this crate's public surface.

## Tests

Every test below runs without a database server except the Postgres half of the shared suite, which runs against a CI service container.

- **Shared backend suite**, every case against SQLite on a temporary file and against Postgres: `meta` hit and miss, `latest_revision` across `P4003R0` through `P4003R11` asserting `R11` rather than `R9` so the comparison is not lexical, `markdown` windows at the start, across the end, and past the end, `outgoing_citations` and `incoming_citations` ordering, `papers_for_year` on a year with no papers, `papers_since` with a string month comparison, `replace_rows` on a table with a composite key and on `signals` which has no key at all, `upsert_paper` preserving `source_file` and `markdown_path` while overwriting `title`, and `setting` round-tripping. Each case asserts the same rows in the same order and the same `StoreError` variant from both backends.
- **Parity of the divergences** in `## Behavioral parity`, one test each, because a list of known divergences with no test is a list of future bugs: a zero-or-one flag read back as the same integer, an upsert preserving unmentioned columns rather than defaulting them, `latest_revision` finding a lowercase-inserted row on both backends, an ordering applied in Rust producing identical order, and a `NULL` in a legacy `TEXT` column reading back as an empty string after the migration.
- **Schema check**: `ping` passes against a migrated database and fails with `SchemaMismatch` naming the column against a database with one column dropped. Run on both backends, because the introspection is the one piece of SQL that is deliberately different.
- **Transaction and savepoint under the section lifecycle**, against a recording harness that drives `on_section` directly: `Enter` then a write then `Complete` commits and the row is visible outside the transaction; `Enter` then a write then `Retry` rolls back, and a following `Complete` commits only what the second attempt wrote; a read inside the section after a write sees the uncommitted row and a read from a second run does not; `Enter` then `NestedEnter` then a write then `NestedComplete` then `Complete` commits everything; `NestedEnter` then a write then a rollback to that savepoint keeps the outer section's earlier write; a `Complete` with no `Enter` is a no-op rather than a panic; an out-of-order `Complete` returns `LifecycleOrder`; a failed commit propagates as an error rather than a silent success.
- **The missing run-terminal event, as a failing test that documents the gap**: `Enter`, a write, and then no further event, followed by a second run's `Enter`. On SQLite the second `begin` blocks on the one write connection and times out. The test asserts that timeout and is named for the gap, so it becomes the test that starts passing when `RunEnded` lands. Asserting the bug is how a known gap stays known.
- **Concurrent writers against WAL**: two `Store` instances on one file, one holding a write transaction while the other reads, asserting the read succeeds and sees pre-transaction data, which is the property WAL buys and the rollback journal does not. Then a second writer asserting it waits and then succeeds after the first commits, with a busy timeout shorter than the test's patience so a regression to the rollback journal fails rather than hangs. Then a direct assertion that `journal_mode` reads back as `wal` after `new`, since a silent fallback to `delete` mode on a filesystem that does not support WAL is exactly the kind of thing that only shows up under load.
- **Idempotence of a re-run**: write eight rows, read them, write a different six rows for the same paper, and assert the table holds exactly six. Then write zero rows and assert the table holds zero and the stamp column is still updated. Then the multi-section case: drive `Enter`, a write, and `Complete` for three sections, abandon the fourth, and replay all four from the start, asserting the final table state is byte-identical to a clean four-section run. That is the discard-and-rerun claim as an assertion rather than a paragraph.
- **The case-fold boundary**: `PaperId::parse` on `p4003r2`, ` P4003R2 `, `P4003r2`, and `p4003R2` all producing the same value; `as_str` uppercase and `stem` lowercase; `parse` rejecting the empty string, `4003`, `P`, `PR2`, `P4003R`, and a string with an interior space. Then the cross-method test the Python side would fail: write rows with a lowercase id, read them back with an uppercase id, and assert they are found, on both backends. Then a deserialization test asserting a lowercase id in a tool argument payload arrives as an uppercase `PaperId`.
- **Surface separation**: build a `ToolMap` with `PaperstoreExt` registered and assert the model's schema list contains exactly `paper_meta`, `paper_latest`, `paper_md`, and `paper_cites`, and neither `paper_upsert` nor `paper_rows`. Then the converse: the Lua environment has a `paper` table with exactly `meta`, `latest`, `cites`, `upsert`, and `rows`, and no `md`. This is the test that fails if someone later changes a `Surfaces` value.
- **Table allowlist**: `paper_rows` against a table not in the allowlist fails with `UnknownTable` and issues no statement; a row missing a required column fails with `MissingColumn` naming it; an unknown column fails with `UnknownColumn`; a string where an int is declared fails with `ColumnType` naming both types. Plus a test that a table name containing a quote or a semicolon cannot be constructed, since the allowlist is what stands between an interpolated identifier and an injection.
- **Declared rows resolution**: a prompt declaring `kind: rows` with `table: assay_finding` and a root resolving to this extension passes boot validation; the same prompt with `table: not_a_table` fails boot with the table named; after a run that wrote seven rows, `output_rows` returns seven, and after a second write of three it returns three rather than ten.
- **Feature off**: a compile test that the host binary builds with the `paperstore` feature disabled, that no `sqlx` symbol is in the dependency graph, and a runtime test that a prompt naming `paper_meta` fails startup validation with an unbound canonical name.

## Open

- The exact sqlx 0.9.0 API for opening a transaction with `BEGIN IMMEDIATE` rather than the default deferred begin. `## The SQLite backend` requires it and the requirement does not depend on the API: if no suitable entry point exists in the pinned version, `Store::begin` checks out a pooled connection, executes the statement directly, and drives `COMMIT` and `ROLLBACK` by hand, which is more code and the same semantics. This is the one place in this document where an implementation detail is unverified rather than undecided.
- Whether the write-buffering escape hatch replaces the section-long transaction on SQLite. Buffering a run's writes in memory and applying them in one short transaction at `Complete` would dissolve the single-writer constraint, the pooled-connection leak, and the fan-out savepoint problem at once, and it would cost read-your-writes routing through the buffer and unbounded memory on a large section. It is not proposed here because `design.md` specifies the transaction mapping and a change to it is a change to that document rather than to this one. It is the strongest argument available if concurrent writing runs on SQLite turn out to be needed.
- Whether the eleven zero-or-one integer flag columns should become real booleans in Postgres. Keeping them integers preserves what the Django mirror reads and imports SQLite's type poverty into a database that has a boolean type. The answer depends on the mirror code, which is in `wg21-website` and unreadable from here.
- Whether `paper_md` should also be reachable from Lua through a guarded accessor that returns a handle rather than text. It would let a prompt author window a paper deterministically without putting untrusted text where `{{ state.x }}` substitution can reach it, and it would add a fourth thing to the language for one use case.
- Whether the twenty-eight tables should be reduced before the Postgres migration is written. Seven of them, `claims`, `evidence`, `external_citations`, `questions`, `rhetoric`, `caput_causae`, and `citation_audit`, are documented in `CLAUDE.md` as no longer written by any production pipeline, and two more, `candidates` and `signals`, have no primary key and no caller. Migrating nine dead tables to Postgres to keep parity with a SQLite schema nobody writes is work with no reader, and deleting them is a decision about the Python side that this crate does not own.
- Whether the indexes the Python schema lacks should be added here. Nine `paper_id` prefixes with no index mean every replace-all `DELETE` is a full table scan, which is invisible at ten thousand papers and is not free. Adding them changes the SQLite schema for the Python side too, which is the same kind of cross-boundary change as the WAL conversion and wants the same deliberateness.
- The feature name and the type name, which two crate docs already disagree about. This document uses feature `paperstore` and type `PaperstoreExt`, matching `design-classify.md`'s `classify` and `ClassifyExt`. `design-mcp.md` uses feature `ext-paperstore` and type `Paperstore`, and also `ext-classify` and `Classify` against `design-classify.md`. One convention has to win and the choice is cosmetic, which is why it is unresolved rather than argued.
- What `design-mcp.md`'s `[tools] store = "paperstore"` binding is meant to be. It is a single canonical word bound to this extension, which contradicts `design.md`'s settled rule that one canonical name is exactly one function, and it collides with `store`, which `design-core.md` reserves as the core's run state store host object and warns is easily confused with a persistent database. The six `paper_*` names in `## Canonical tool names` are what this document proposes instead, and that line in `design-mcp.md` needs to change to match. The same line binds `classify = "classify"` against `design-classify.md`'s four `classify_*` words, so it is one stale example rather than a disagreement about the rule.

*2026-07-25 - design-paperstore*
