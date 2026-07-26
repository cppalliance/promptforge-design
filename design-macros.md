<!-- STATUS: crate doc - promptforge-macros (proc-macro) - see design.md for the system -->

# `promptforge-macros`: the tool attribute macro

## Scope

One procedural macro crate exporting one attribute, `#[tool]`. It goes on an ordinary async Rust function and emits everything the runtime needs to call that function from two places: the JSON Schema the model sees, the `mlua` binding a prompt author calls, and the `ToolDef` registry entry that carries both.

A proc-macro crate is a compiler plugin. It is compiled for the host, loaded into `rustc`, and run at compile time on the token stream of the item it is attached to, emitting replacement tokens. That is why it must be its own crate with `proc-macro = true` in its manifest: the compilation model gives it no choice.

What this crate does not do:

- Run at runtime. Everything here happens during `cargo build` and nothing ships in the binary except the code it generated.
- Depend on `promptforge`. A proc-macro crate cannot depend on the crate whose types it names without a cycle, so it emits absolute paths like `::promptforge::ToolDef` and never imports them. `promptforge` re-exports the attribute so that `use promptforge::tool;` is the only import an extension author writes, exactly as `serde` re-exports `serde_derive`.
- Register anything. Registration is the explicit central `register_all`, because dead code elimination silently drops `inventory`-style registrations and startup validation must be able to reject an unknown name.
- Generate MCP tool definitions. Our tools never reach an MCP surface; prompts do. This is not `rmcp`'s `#[tool]` and the two are unrelated.
- Parse or validate a prompt. That is `promptforge`.

## Why a macro at all

The honest case against it: an AI writing this codebase can produce a schema literal, an `mlua` binding, and a registry entry by hand for each function, and hand-written code has better compile errors than any macro. If the macro's only benefit were less typing, plain code would win and this crate would not exist.

The benefit is not typing. It is that three artifacts have to agree with a fourth, and hand-writing them makes disagreement possible. A tool's argument struct, its JSON Schema, its Lua argument marshalling, and its registry entry are four statements of one fact. Written by hand they can drift: a field renamed in the struct and not in the schema produces a model that supplies `query` to a function reading `q`, and nothing catches it until a tool call fails at runtime with an argument the model was told to send. Generated from the signature, drift is not a bug that can be introduced, because there is one source and three derivations.

That argument holds regardless of who or what writes the code. An AI adding a field to the struct and correctly updating the other three places has done the work correctly; an AI doing it ninety-nine times out of a hundred has introduced a defect class that only appears under a live model. Tension: the macro makes a whole class of drift impossible and pays for it in error messages that read worse than the equivalent hand-written code, which is a real cost the span handling below exists to hold down.

## Dependencies and pins

Versions confirmed against crates.io on 2026-07-25.

- `syn` at `2.0.119`, pinned to the 2.x line rather than tracking latest
- `quote` at `1.0.47`
- `proc-macro2` at `1.0.107`
- `darling` at `0.23.0`, for attribute argument parsing
- `schemars` at `1.2.1`, a dependency of the generated code rather than of this crate
- `trybuild` at `1.0.118`, dev-dependency only

`syn` 3.0.2 exists and is not used. The 3.0 line landed on 2026-07-18, one week before this document, and `darling` 0.23.0 declares `syn ^2.0.15`, so adopting `syn` 3 today means dropping `darling` and hand-parsing attribute arguments. That trade is not worth taking for a one-attribute surface whose error quality is the thing `darling` is carrying. The pin is therefore `syn` 2.0.119, the last 2.x release, and the migration to `syn` 3 is gated on `darling` rather than chosen. Tension: a dependency the project cannot upgrade on its own schedule sits under the whole extension mechanism, which is the same shape of risk `ort` carries in the classifier extension.

## The attribute

```rust
use promptforge::tool;

/// Search the web and return ranked results.
#[tool(name = "web_search", surfaces = both, rate_limit = 4)]
pub async fn web_search(args: WebSearchArgs, ctx: &CallCtx) -> Result<WebSearchOut, ToolError> {
    // ordinary Rust; the body is emitted unchanged
}

#[derive(serde::Deserialize, schemars::JsonSchema)]
pub struct WebSearchArgs {
    /// The query string.
    pub query: String,
    /// Maximum results to return.
    #[serde(default = "default_count")]
    pub count: u32,
}

#[derive(serde::Serialize)]
pub struct WebSearchOut { pub results: Vec<Hit> }
```

Arguments to the attribute:

- `name` - the canonical tool name. Required, and a string literal rather than an expression, because startup validation and configuration both need it readable without running code. Checked at expansion time against the canonical-set naming rule below.
- `surfaces` - `tool_only`, `lua_only`, or `both`. Required, with no default, because a silent default would decide whether a model can see a function and that decision should be visible at the call site. Maps to `promptforge::Surfaces`.
- `rate_limit` - optional permit count for a metered upstream. Absent means unlimited, and the registry stores `None`.
- `description` - optional string literal. Absent means the function's own doc comment is used, which is the normal case; the override exists for a function whose doc comment addresses a Rust caller rather than a model.

The function must be `async`, must take exactly `(args: T, ctx: &CallCtx)`, and must return `Result<U, ToolError>` where `T: serde::Deserialize + schemars::JsonSchema` and `U: serde::Serialize`. Every one of those is checked at expansion time with a span pointing at the offending token rather than deferred to a trait-resolution failure inside generated code.

## Expansion

For the function above the macro emits four things and leaves the original function untouched.

```rust
// 1. The function, byte for byte as written. A caller with a typed handle can
//    still call it directly, and it is unit-testable without the runtime.
pub async fn web_search(args: WebSearchArgs, ctx: &CallCtx) -> Result<WebSearchOut, ToolError> { .. }

// 2. A unit struct carrying the erased implementation.
#[doc(hidden)]
#[allow(non_camel_case_types)]
pub struct __pf_tool_web_search;

// 3. The erased entry point. JSON in, JSON out, which is the single interchange
//    form both surfaces are built on.
#[::async_trait::async_trait]
impl ::promptforge::ToolFn for __pf_tool_web_search {
    async fn call(
        &self,
        args: ::serde_json::Value,
        ctx: &::promptforge::CallCtx,
    ) -> ::core::result::Result<::serde_json::Value, ::promptforge::ToolError> {
        let parsed: WebSearchArgs = ::serde_json::from_value(args)
            .map_err(|e| ::promptforge::ToolError::BadArguments {
                tool: "web_search",
                detail: e.to_string(),
            })?;
        let out = web_search(parsed, ctx).await?;
        ::serde_json::to_value(out)
            .map_err(|e| ::promptforge::ToolError::BadResult {
                tool: "web_search",
                detail: e.to_string(),
            })
    }
}

// 4. The registry entry constructor, called from the extension's `tools()`.
impl __pf_tool_web_search {
    pub fn def() -> ::promptforge::ToolDef {
        ::promptforge::ToolDef {
            name: ::promptforge::ToolName::canonical("web_search"),
            description: "Search the web and return ranked results.",
            schema: ::schemars::schema_for!(WebSearchArgs),
            surfaces: ::promptforge::Surfaces::Both,
            rate_limit: ::core::option::Option::Some(4u32),
            call: ::std::sync::Arc::new(__pf_tool_web_search),
        }
    }
}
```

The extension then writes:

```rust
fn tools(&self) -> Vec<ToolDef> {
    vec![__pf_tool_web_search::def(), __pf_tool_web_fetch::def()]
}
```

A `tools!` helper macro that collects the entries by name is deliberately not provided. The list is short, an explicit `vec!` is greppable, and a macro hiding it would recreate the implicit-registration problem the design already rejected.

### The Lua binding is derived, not written

`Surfaces` decides which surfaces exist; the binding itself is generated from the same signature by the core rather than by this macro. The macro's contribution is that `ToolDef` carries an erased `ToolFn` plus the schema, which together are sufficient for `promptforge` to build an `mlua` function that converts a Lua table to `serde_json::Value`, calls `ToolFn::call`, and converts the result back. That conversion is one generic function in the core, not generated code, because it is identical for every tool.

This is why `serde_json::Value` is the interchange form rather than two typed entry points. Tension: a Lua call pays a table-to-JSON-to-struct round trip it does not strictly need, which matters only if a classifier call in a tight ranking loop is ever measured as the bottleneck, and the classifier extension's batch-shaped signatures are what keep that call count low.

## Name checking at expansion time

`name` must be lowercase ASCII with underscores, must not start or end with an underscore, and must not be one of the reserved core names: `state`, `store`, `tools`, `params`, `context`, `sections`, `progress`, `done`, `create_file`, `append_file`, `read_file`, `delete_file`. A collision with a reserved name is a compile error rather than a startup error, because the reserved set is fixed at compile time and there is no reason to defer a decidable check to runtime.

The macro cannot check that a name is in the canonical set, because the canonical set is a list in `promptforge` and this crate does not depend on it. `ToolName::canonical` is therefore a const-checked constructor in the core that panics at startup on an unknown name, and startup validation reaches it before any run. Tension: adding an extension means editing a list in the core, which is the one core change a new extension requires, and the error for getting it wrong is a startup panic rather than a compile error.

## Error messages

The failure mode a macro is judged on is what a reader sees when they get it wrong. Three rules:

- Every diagnostic is emitted with `syn::Error::new_spanned` against the narrowest token that is wrong. A bad `surfaces` value underlines the value, not the attribute, and not the function.
- Emit the original function even when the attribute is invalid. A macro that returns only an error deletes the item, so the reader gets one error about the attribute plus a cascade of "cannot find function" errors from every call site. Emitting the function and the error together keeps the output to the one real problem.
- Trait bound failures get a `#[doc(hidden)]` assertion function with a span on the argument type, so a struct missing `JsonSchema` reports at the struct rather than inside generated code the reader cannot see.

Tension: none of this makes a macro error as good as a plain-code error, and the mitigation is a budget of care rather than a mechanism.

## Tests

`trybuild` is the harness, since the thing under test is compiler output.

- Pass cases in `tests/expand/`: each `surfaces` value, `rate_limit` present and absent, `description` present and absent falling back to the doc comment, a generic argument struct, a function returning `()`.
- Fail cases in `tests/fail/`, each with a committed `.stderr` golden file: missing `name`, missing `surfaces`, a `name` that is not a literal, an uppercase `name`, a reserved `name`, a non-async function, a wrong argument count, a wrong return type, an argument struct without `JsonSchema`.
- Every fail case additionally asserts that the "cannot find function" cascade is absent, which is the regression test for the emit-anyway rule.
- One integration test in the workspace links a generated `ToolDef` into a `ToolMap`, calls it through `ToolFn` with a JSON value, and calls it again through the Lua binding, asserting both produce the same result. This is the test that catches the schema and the binding disagreeing, which is the entire reason the crate exists.

Golden `.stderr` files are version-sensitive: a `rustc` upgrade can reword a diagnostic and fail these tests without any change here. They are regenerated with `TRYBUILD=overwrite` and the diff is read rather than trusted. Tension: a compiler upgrade produces test churn that looks like breakage.

## Open

- Whether a `#[tool]` on an inherent method, rather than a free function, is worth supporting. An extension holding a connection pool currently writes free functions that reach it through the `CallCtx` or a captured `Arc`, and the paperstore extension is the case that will settle whether that is comfortable.
- Whether `surfaces` should permit a per-deployment override in configuration. Today it is compile-time and a deployment cannot hide a tool from the model without a rebuild.
- Whether the description should be checked for length. A model reads it, and a two-paragraph doc comment on forty tools is a context cost nothing currently bounds.

*2026-07-25 - design-macros*
