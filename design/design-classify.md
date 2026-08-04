<!-- STATUS: crate doc - promptforge-ext-classify - behind Cargo feature `classify` - see design.md for the system -->

# `promptforge-ext-classify`: in-process classifiers as Lua host objects

## Scope

This crate is the first real `Extension` implementation and the reference other extension authors copy. It runs text classifiers and embedders in-process on the GPU through ONNX Runtime and exposes them to prompt authors as Lua host objects. It contributes four functions, three ONNX-backed model kinds, and one startup self-check. That is the whole crate.

It is not part of the core library. `promptforge` knows no domain, and a classifier is a domain: it has a label vocabulary, a hypothesis template, a checkpoint, and a device. All of that lives here, behind the `classify` Cargo feature. Built without the feature the binary is self-contained, no CUDA shared library is loaded, and no prompt may name a `classify` function. Built with it, CUDA shared libraries become a deployment dependency, which costs nothing because both target environments already have CUDA installed and a shared library is ordinary native practice rather than the interpreter-and-package-tree dependency the single-binary goal exists to avoid.

What this crate does not do, and cannot be made to do without a change to this document:

- Appear on the model's tool surface. Every function declares `Surfaces::LuaOnly`.
- Serve anything over HTTP, or call anything over HTTP. There is no client and no server here.
- Download weights. Every artifact is a local export named by a manifest, and the runtime never reaches the network for a model.
- Export a model. Export is an offline Python procedure that runs before deployment and is gated separately.
- Train, fine-tune, or evaluate. A checkpoint arrives already fine-tuned.
- Hold run state. It keeps no per-run and no per-section data, which is why `on_section` is a no-op.
- Decide what a label means. `TARGET` and `SKIP` are strings a prompt passes in; this crate scores them and returns one.
- Run a generative model. Large models are reached through the gateway; only embedders and text classifiers execute locally.
- Quantize. FP32 is the only precision.
- Batch across callers. A call's batch is exactly what that call passed, because determinism requires fixed batch composition.

The test of the boundary: removing this crate from the workspace leaves every other crate compiling untouched, and no crate outside it mentions `ort`, `fastembed`, `tokenizers`, ONNX, or CUDA.

## Dependencies and pins

- `ort` at exactly `=2.0.0-rc.12`, with the `cuda` feature, binding ONNX Runtime for the NLI cross-encoder path.
- `fastembed` at exactly `=5.17.2`, for text embedding and cross-encoder rerank. It re-exports `ort`, which is why the `ort` pin is not independently chosen.
- `tokenizers` at exactly `=0.23.1`, HuggingFace's own Rust implementation, for preprocessing. No Python enters the runtime.
- `promptforge`, `serde`, `serde_json`, `schemars`, `thiserror`, and `tokio` from the workspace, at whatever the workspace pins. Notably not `mlua`: the core owns every Lua binding.

Every version is an exact `=` pin rather than a caret range. The reason is in `## Carrying the ort release-candidate risk` below and it is not a general workspace habit.

## The `Extension` impl

The trait is `promptforge::Extension`, reproduced from the core doc without modification. `ClassifyExt` implements all eight methods, including all four the trait defaults, because a reader of this file should see every decision made rather than inherited. Two of those defaults are restated here rather than inherited and both are the empty answer: `holds_section_state` returns false, because a classification is a call and a result with nothing held past it, so this extension has no savepoint a nested section could interleave with and never costs a deployment its fan-out concurrency; `summarize` returns `None`, because this crate commits nothing and a run summary reporting how many times a classifier was called would be noise rather than information.

```rust
pub struct ClassifyExt {
    /// Shared with every `ToolFn` this extension hands to the registry.
    inner: Arc<Inner>,
    /// Owned storage so `provides` can return a slice.
    names: Vec<ToolName>,
}

struct Inner {
    /// Every classifier the deployment configured, keyed by classifier name.
    scorers: BTreeMap<String, Arc<dyn PairScorer>>,
    embedders: BTreeMap<String, Arc<dyn Embedder>>,
    /// Selector slot to classifier name. Resolved by the host, not read from a file here.
    slots: ClassifierSlots,
    limits: SelfCheckLimits,
}

impl ClassifyExt {
    /// Builds every session eagerly. The host calls this while loading configuration.
    pub fn new(cfg: ClassifyConfig) -> Result<Self, ClassifyError>;
}
```

Sessions are built in `new`, not lazily in `validate`. The trait gives `validate` only `&self`, so a `validate` that built sessions would need interior mutability to keep them, and a lazily built session would first appear mid-run on whichever section happened to call it first. Eager construction in a fallible constructor is both simpler and stricter: an unreadable weights file, a missing CUDA provider, or a manifest mismatch fails while the host is still reading configuration, before any prompt is registered.

```rust
impl Extension for ClassifyExt {
    fn name(&self) -> &str {
        "onnx"
    }

    fn provides(&self) -> &[ToolName] {
        &self.names
    }

    fn tools(&self) -> Vec<ToolDef> {
        vec![
            label_def(self.inner.clone()),
            entail_def(self.inner.clone()),
            embed_def(self.inner.clone()),
            rank_def(self.inner.clone()),
        ]
    }

    // No bind_lua. The core builds the `classify` table with its four fields
    // from the four canonical names, all declaring Surfaces::LuaOnly. This
    // crate does not depend on mlua and constructs no Lua value.

    async fn validate(&self) -> Result<(), ExtError> {
        for (name, s) in &self.inner.scorers {
            self.check_discriminates(name, s.as_ref())?;
            self.check_on_device(name, s.as_ref())?;
            self.check_golden(name, s.as_ref())?;
        }
        for (name, e) in &self.inner.embedders {
            self.check_discriminates_embed(name, e.as_ref())?;
            self.check_on_device_embed(name, e.as_ref())?;
            self.check_golden_embed(name, e.as_ref())?;
        }
        self.inner.slots.validate()?;
        Ok(())
    }

    /// Stateless. Nothing to begin, commit, or roll back.
    async fn on_section(&self, _ev: &SectionEvent) -> Result<(), ExtError> {
        Ok(())
    }

    async fn shutdown(&self) -> Result<(), ExtError> {
        for s in self.inner.scorers.values() {
            s.shutdown();
        }
        for e in self.inner.embedders.values() {
            e.shutdown();
        }
        Ok(())
    }
}
```

`validate`, `on_section`, and `shutdown` are all `async` on the landed trait, and this extension awaits nothing inside any of the three. That is worth stating rather than leaving to the reader, because the `std::sync::Mutex` guarding each session is a blocking lock. It is sound here exactly because no guard ever crosses an await point, and an extension that did await while holding one would park a runtime worker rather than the caller. The rule an extension author should take: a blocking lock inside an async hook is fine while the hook is straight-line code, and stops being fine the moment an await appears between the lock and its release.

`name` returns `"onnx"` rather than `"classify"`. The extension name is the backing implementation, because that is what a configuration line binds a canonical word to, and a second classifier extension over a different runtime would be a different name backing the same words. It appears in `ResolvedTool::extension` for diagnostics and dispatch never branches on it.

`provides` returns the four canonical names in the `classify` family: `classify_label`, `classify_entail`, `classify_embed`, `classify_rank`. Four rather than one `classify` word carrying an operation field, and the deciding reason is the Lua surface rather than the typing. `design-core-residue.md` derives Lua tables from a `family_operation` split on the first underscore, which is how `web_search` becomes `web.search`. A bare `classify` has no underscore, therefore no family, therefore no Lua table, and Lua is the only surface this extension has, because all four operations declare `Surfaces::LuaOnly`. One word would break the surface the extension exists for. The typing follows for free: `ToolDef` carries exactly one `ToolName`, so four functions keep four schemas and per-operation validation instead of one union type dispatched on a string. `ToolName` parses only from the core's canonical set, so landing this extension adds four words to that set. Tension: a central vocabulary gains four words instead of one, against `design.md`'s concern about the size of that list, and that edit to a list in the core is the only core change this extension requires.

`tools` builds four `ToolDef` values, each cloning `Arc<Inner>` into its `ToolFn`. This is the pattern every extension needs and it is why the state sits in a separate `Inner` behind an `Arc`: `tools` receives `&self`, not `Arc<Self>`, so it cannot hand itself to a closure. Each def sets `surfaces: Surfaces::LuaOnly` and `rate_limit: None`. `description` is still written and still accurate even though no model ever reads it, because it is what an author sees in generated documentation. `schema` is derived from the argument struct by `register_capability` and is not wasted on a `LuaOnly` tool: it is what validates the Lua argument table, so a misspelled field name fails with a message naming the field instead of being silently ignored.

Lua reaches these as one table, `classify`, with four fields, and this crate writes none of that. The core groups the four canonical names by their shared `classify_` prefix and installs the table once per run, naming each field from the suffix. The functions are created with `create_async_function` because `ToolFn::call` is async; this requires the core's Lua driver to execute a section block with `call_async`, which is a property of the core rather than of this crate and the same requirement every other extension places on it.

`validate` runs three checks per configured model and is the most important method in the crate. It is specified in `## The two silent-failure invariants` below.

`on_section` is a no-op, and the reason is instructive rather than incidental. The section lifecycle exists so that an extension holding a resource across a section can begin, commit, and roll it back: a database-backed extension opens a write on `Enter`, commits on `Complete`, rolls back on `Retry`, and takes a savepoint on `NestedEnter`. This extension holds nothing across a call. A classification is a pure function of its arguments and the loaded weights, it writes nothing, and a retried section that classifies the same text gets the same answer with no cleanup in between. There is nothing to roll back, so the override is `Ok(())` and the method is written out explicitly rather than left to the trait default, because a reader of this file should see that the decision was made rather than inherited. An extension author reading this should take the general rule: implement `on_section` if and only if you hold something whose lifetime is a section. Tension: the crate therefore cannot enforce the per-section call cap itself, which is why the cap is the core's counter and not this crate's.

`shutdown` drops every session and releases its CUDA arena. It receives `&self`, so a session that must be released has to sit behind interior mutability; the same `Mutex` that serializes runs holds an `Option` and `shutdown` takes the session out of it. A call arriving after shutdown returns `ClassifyError::ShutDown` rather than panicking. The ONNX Runtime environment itself is process-lifetime and is not released, which is correct because the only caller of `shutdown` is a process that is exiting.

## The four Lua operations

Prompt authors see one global, `classify`, with four fields. Two conventions hold across all four.

- Every operation takes a single table argument, so a call reads as named fields and a new optional field is not a breaking change.
- Every operation returns its primary value first and a detail table second, so the common case is one expression and the numbers stay reachable.

| Operation | Primary return | Detail table |
|---|---|---|
| `classify.label` | the winning label, a string | `label`, `score`, `scores`, `classifier`, `ms` |
| `classify.entail` | the entailment probability, a number | `score`, `scores`, `classifier`, `ms` |
| `classify.embed` | a vector, or an array of vectors | `dim`, `count`, `normalized`, `classifier`, `ms` |
| `classify.rank` | an array of results, best first | `count`, `returned`, `classifier`, `ms` |

### `classify.label`

Zero-shot classification over a caller-supplied label set, implemented as NLI entailment against a hypothesis template. Returns the label with the highest entailment probability.

```lua
model("fast")
break_section()

local label, detail = classify.label{
  text = state.paragraph,
  labels = { "TARGET", "SKIP" },
}
state.set("tag", label)
state.set("tag_score", detail.score)
assert(label == "TARGET", "paragraph is not on target")
```

A precondition is a top-level `assert`, so a classifier call that decides whether a section runs at all sits at the top of the block and the failing assertion's message is what the observer reports.

The declared exit is taken whether or not that assertion holds, which is what makes this shape usable: a paragraph classified `SKIP` skips this section's model turn and the run continues at the next one, rather than the whole run stopping because one paragraph was off target. A classifier can also choose the exit outright, which is the cheapest branch in the language because no model turn is spent on it:

```lua
if classify.label{ text = state.paragraph, labels = { "TARGET", "SKIP" } } == "TARGET" then
  goto("## Analyze")
else
  break_section()
end
```

`text` and `labels` are required. `selector` names a classifier slot and defaults to `selector`. `template` overrides the classifier's configured hypothesis template and must contain one `{}` placeholder. The template belongs in configuration or in the prompt rather than in Rust, because the wording of a hypothesis is a measured domain choice: the cross-validated `TARGET` hypothesis on the Python path is what took `nli-small` to 96 percent target recall at one eighty-fifth the cost of `zeroshot-large`.

### `classify.entail`

A single cross-encoder pair, returning the entailment probability directly. This is the operation that reads well inside a postcondition.

```lua
function check()
  local score = classify.entail{
    premise = state.verdict,
    hypothesis = "The verdict cites at least one primary source.",
  }
  assert(score > 0.8, "verdict does not appear to cite a primary source")
end
```

`premise` and `hypothesis` are required, `selector` is optional. The second return carries the full three-way distribution as `scores.entailment`, `scores.neutral`, and `scores.contradiction`. Requires a classifier whose head is three-way NLI; a selector resolving to a single-logit reranker fails at boot, not at the call.

### `classify.embed`

```lua
local vec, detail = classify.embed{ text = state.get("summary") }
local vecs = classify.embed{ texts = state.get("paragraphs") }
```

Exactly one of `text` or `texts` is set; setting both or neither is `InvalidArgs`. The return shape follows the argument: a flat array of numbers for `text`, an array of arrays for `texts`. `normalize` overrides the classifier's configured normalization. `selector` defaults to the `embedder` slot. The batch form is one call rather than a Lua loop, which matters twice: it costs one unit of the per-section cap regardless of length, and its batch composition is exactly the array the caller passed, which is what determinism requires.

A vector crosses into Lua as a table of numbers, which is what the examples above return, and not as an opaque handle. The recorded cost is 384 conversions plus a Lua table allocation per call, which is free next to a 1 ms forward pass and is not free inside a loop over 200 paragraphs. A userdata handle carrying a cosine method is the named upgrade if a ranking loop is ever measured as the bottleneck rather than assumed to be one; it would also have prevented a prompt from doing arithmetic on a vector, which may be a feature and is not enough of one to pay for the opacity now.

Normalization is configuration rather than a default, because `all-MiniLM-L6-v2` uses MEAN pooling plus L2 normalization per its `1_Pooling/config.json` while a raw graph gives whatever the export baked in. A pooling or normalization mismatch produces valid-looking vectors that do not match the ones an existing index was built with, which is a silent failure of the same family as the two named below and is caught by the same golden fixture.

### `classify.rank`

Ranks a candidate set against a query with a cross-encoder and returns ordered results.

```lua
local ranked = classify.rank{
  query = params.entity .. " position on contracts",
  candidates = state.get("candidate_texts"),
  top_k = 10,
}

local keep = {}
for _, hit in ipairs(ranked) do
  if hit.score > 0.5 then
    keep[#keep + 1] = hit.index
  end
end
state.set("shortlist", keep)
```

`query` and `candidates` are required, `candidates` must be non-empty. `top_k` truncates the returned array and defaults to all of it. `return_text` defaults to false so the candidate strings are not copied back across the boundary; each result carries `index` and `score`, plus `text` when asked. `index` is 1-based, because it indexes the Lua table the caller passed and an off-by-one here would be a silent wrong answer. Results are sorted by score descending, with ties broken by ascending `index` so the order is total and reproducible.

One call scores every candidate as one batch, for the same two reasons as `embed`: one unit against the cap, and a batch composition the caller fixed.

### Argument structs

`register_capability` derives the schema and the registry entry from these. `deny_unknown_fields` is what converts a Lua typo into a diagnostic.

```rust
#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct LabelArgs {
    pub text: String,
    pub labels: Vec<String>,
    #[serde(default)]
    pub selector: Option<String>,
    #[serde(default)]
    pub template: Option<String>,
}

#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct EntailArgs {
    pub premise: String,
    pub hypothesis: String,
    #[serde(default)]
    pub selector: Option<String>,
}

#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct EmbedArgs {
    #[serde(default)]
    pub text: Option<String>,
    #[serde(default)]
    pub texts: Option<Vec<String>>,
    #[serde(default)]
    pub normalize: Option<bool>,
    #[serde(default)]
    pub selector: Option<String>,
}

#[derive(Deserialize, JsonSchema)]
#[serde(deny_unknown_fields)]
pub struct RankArgs {
    pub query: String,
    pub candidates: Vec<String>,
    #[serde(default)]
    pub top_k: Option<usize>,
    #[serde(default)]
    pub return_text: bool,
    #[serde(default)]
    pub selector: Option<String>,
}
```

Each `ToolFn` returns one JSON object; the Lua binding lifts one declared field out of it as the primary return and passes the whole object as the detail table. That keeps one function behind both surfaces, which is the point of `ToolDef`.

Underneath, the four operations reduce to two model primitives, which is why the trait boundary has exactly two shapes.

```rust
/// Cross-encoder scoring. Backs label, entail, and rank.
pub trait PairScorer: Send + Sync {
    fn score_pairs(&self, pairs: &[(&str, &str)]) -> Result<Vec<Vec<f32>>, ClassifyError>;
    fn head(&self) -> &Head;
    fn shutdown(&self);
}

/// Text embedding. Backs embed.
pub trait Embedder: Send + Sync {
    fn embed(&self, texts: &[&str]) -> Result<Vec<Vec<f32>>, ClassifyError>;
    fn dim(&self) -> usize;
    fn shutdown(&self);
}

pub enum Head {
    /// Three-way NLI head. Indices into the logit vector, read from the checkpoint.
    Nli { entail: usize, neutral: usize, contra: usize },
    /// A single relevance logit, as a cross-encoder reranker emits.
    Relevance,
}
```

`Head::Nli` carries indices rather than assuming an order, because the entailment dimension is not at the same position in every NLI checkpoint and a wrong index silently inverts every score. The indices are read from the checkpoint's `id2label` at export time and recorded in the manifest, so the runtime reads a number rather than guessing.

## Classifier slots

Three layers, identical in shape to model slots, reusing the `classifier_defaults` convention that already exists on the Python path rather than inventing a mechanism.

- Layer one, the prompt: names a logical selector, or names nothing and takes the default.
- Layer two, `prompts.toml`: maps each selector slot to a classifier name, globally with per-prompt overrides.
- Layer three, `prompts.toml` again: maps each classifier name to weights, a device, and its preprocessing.

Layer three sits in `prompts.toml` rather than `gateway.toml` because the gateway owns LLM endpoints and credentials and has no reason to see a local model file. A classifier is not LLM traffic and never reaches the gateway.

```toml
[tools]
web_search = "brave"
web_fetch = "brave"
paper_upsert = "paperstore"
classify_label = "onnx"
classify_entail = "onnx"
classify_embed = "onnx"
classify_rank = "onnx"

[extensions.onnx]
model_root = "/srv/promptforge/models"
verify = "hash"
self_check_max_ms = 20

[classifiers.nli-small]
backend = "nli_cross_encoder"
model = "nli-deberta-v3-small/onnx-fp32-opset17-v1"
device = "cuda:0"
max_length = 192
hypothesis_template = "This text is about {}."

[classifiers.zeroshot-base]
backend = "nli_cross_encoder"
model = "deberta-v3-base-zeroshot-v2/onnx-fp32-opset17-v1"
device = "cuda:0"
max_length = 192
hypothesis_template = "This text is about {}."

[classifiers.minilm-embed]
backend = "fastembed_text"
model = "all-MiniLM-L6-v2/onnx-fp32-opset17-v1"
device = "cuda:0"
max_length = 256
normalize = true

[classifiers.minilm-rerank]
backend = "fastembed_rerank"
model = "ms-marco-MiniLM-L-6-v2/onnx-fp32-opset17-v1"
device = "cuda:0"
max_length = 256

[classifier_defaults]
selector = "nli-small"
embedder = "minilm-embed"
ranker = "minilm-rerank"

[prompts.staker.classifiers]
selector = "zeroshot-base"
```

The block key is `extensions.onnx` and not `extensions.classify`, because an extension table is keyed by whatever `Extension::name` returns, which is the backing implementation rather than the Cargo feature. The feature is `classify`, the name is `"onnx"`, and that same string is what each `[tools]` line above binds the four canonical words to. `design-mcp.md` owns `prompts.toml` and states the rule generally; this fragment is written to drop into it.

Three keys sit in the block and this document is where each is decided. `model_root` is the root the per-classifier `model` paths resolve against, so moving the artifact tree is one line. `verify` selects how an artifact is checked before a session is built, and `hash` is the sha256 comparison `## Invariant three` runs ahead of the golden fixture. `self_check_max_ms` is the off-device ceiling of `## The two silent-failure invariants`. There is no block-level `device`: a device is a property of one classifier, it is already set in each `[classifiers.NAME]` table, and the off-device check reads it there to decide whether to skip, so a second device key one level up would only be a way for the two to disagree. There is no block-level call cap either, because the cap is the core's `Limits::max_lua_calls_per_section` and this crate keeps no counter of its own, which is what `## The per-section call cap` settles. Tension: `design-mcp.md`'s illustrative block writes `device`, `weights`, and `max_calls_per_section`, so reconciling the two files means renaming `weights` to `model_root`, dropping the other two keys, and adding `verify` and `self_check_max_ms` there.

Three slot names rather than one, because the three roles are three different models and one name cannot resolve to all of them. Slots are typed: `selector` and `ranker` must resolve to a `PairScorer`, `embedder` to an `Embedder`, and `entail` additionally requires `Head::Nli`. A selector pointing at an embedder is a boot failure with both names in the message.

There is no `dtype` field, unlike the `transformer_providers` tables this convention comes from. FP32 is the only value, so offering the field would only offer a way to be wrong. `device` is a device string rather than a provider mode, because auto-detection is what makes a CPU fallback look like success.

## Session management

One session per configured classifier, built once in `ClassifyExt::new` and shared by every run for the life of the process. Nothing is per-run and nothing is per-section.

```rust
fn build(spec: &ClassifierSpec) -> Result<Session, ClassifyError> {
    Session::builder()?
        .with_execution_providers([
            CUDAExecutionProvider::default()
                .with_device_id(spec.device_id)
                .with_memory_limit(spec.memory_limit_bytes)
                .with_arena_extend_strategy(ArenaExtendStrategy::SameAsRequested)
                .build()
                .error_on_failure(),
        ])?
        .with_optimization_level(GraphOptimizationLevel::Level3)?
        .with_intra_threads(1)?
        .commit_from_file(spec.weights_path())
        .map_err(ClassifyError::from)
}
```

- `error_on_failure` is the first silent-failure invariant and is not optional. See below.
- `ArenaExtendStrategy::SameAsRequested` keeps the allocation static instead of doubling under the default next-power-of-two strategy, which is what makes a static GPU budget a budget.
- `with_intra_threads(1)` because the work is on the device and the batch is one; more intra-op threads would only contend with the rest of the runtime for CPU.
- `commit_from_file` reads a local path from the manifest. There is no path that fetches a model.

Threading and sharing. ONNX Runtime documents `Run` as thread-safe on a single session, so sharing is sound. This design nonetheless serializes calls per session behind a `std::sync::Mutex<Option<Session>>` and does so deliberately: a mutex makes batch composition exactly what the caller passed, keeps one batch on the device at a time so a run's timing does not depend on what another run is doing, and gives `shutdown` somewhere to take the session from. The mutex is a determinism decision, not a soundness requirement.

Blocking. `Session::run` is synchronous and blocks for the duration of the forward pass. `ToolFn::call` is async. Every session run therefore happens inside `tokio::task::spawn_blocking`, with the mutex acquired inside the blocking task, so an 8 ms device call never stalls a runtime worker thread. Tokenization runs in the same blocking task, since `tokenizers` is synchronous too.

```rust
async fn score(inner: Arc<Inner>, name: String, pairs: Vec<(String, String)>)
    -> Result<Vec<Vec<f32>>, ClassifyError>
{
    let scorer = inner.scorer(&name)?;
    tokio::task::spawn_blocking(move || {
        let refs: Vec<(&str, &str)> = pairs.iter().map(|(a, b)| (a.as_str(), b.as_str())).collect();
        scorer.score_pairs(&refs)
    })
    .await
    .map_err(ClassifyError::Blocking)?
}
```

Tension: two concurrent runs each making a hundred classifier calls serialize against each other, so the second run's classifier time is added rather than overlapped. At 8 ms a call this is 1.6 seconds of queueing in the worst case, which is accepted in exchange for reproducible batches, and the per-section cap is what keeps the worst case bounded.

## The two silent-failure invariants

Both of these produce a session that builds, a call that returns, and an answer that is wrong. Any smoke test asserting that the call succeeded passes. `design.md` records them as build-time invariants that no ordinary runtime assertion catches, which is true of every assertion made on a single call: a single call cannot tell a baked-in constant from a confident prediction, and cannot tell 44 ms on CPU from 8 ms on CUDA without something to compare against. This crate closes both at `validate` time with differential checks, which need two observations rather than one.

### Invariant one: export at ONNX opset 15 or higher

Below opset 15 the XSoftmax tracer bakes constants into the graph and the model returns an identical answer for every input. The export pipeline pins opset 17 and its gate asserts the opset read back from the emitted graph is 15 or higher. The runtime does not trust that, because the file it loads is not necessarily the file the gate ran on.

The check that catches it, `check_discriminates`, runs at `validate` time against the session that will actually serve requests:

```rust
/// Two deliberately different inputs must produce different outputs.
fn check_discriminates(&self, name: &str, s: &dyn PairScorer) -> Result<(), ExtError> {
    const HIGH: (&str, &str) = ("A cat sat on the mat.", "There is a cat.");
    const LOW: (&str, &str) = ("A cat sat on the mat.", "The stock market closed lower.");

    let out = s.score_pairs(&[HIGH, LOW])?;
    let (a, b) = (&out[0], &out[1]);

    // Degenerate graph: every input yields the same logits.
    if a.iter().zip(b).all(|(x, y)| (x - y).abs() < 1e-6) {
        return Err(ClassifyError::Degenerate { classifier: name.into() }.into());
    }
    // Ordering must also be the right way round, which catches a wrong entail index.
    let (pa, pb) = (entail_prob(s.head(), a)?, entail_prob(s.head(), b)?);
    if !(pa > 0.5 && pb < 0.5 && pa - pb > 0.25) {
        return Err(ClassifyError::Ordering { classifier: name.into(), high: pa, low: pb }.into());
    }
    Ok(())
}
```

Near-bitwise equality across two unrelated inputs is the exact signature of the constant-baking failure, so the first assertion is precise rather than heuristic. The second assertion costs nothing extra and catches the neighbouring silent failure of a wrong entailment index, which inverts every score without changing any shape. The embedder form is the same check with cosine similarity: two unrelated sentences must not produce vectors that are equal to within 1e-6.

### Invariant two: `error_on_failure` on the session builder

Without it, a driver mismatch makes ONNX Runtime fall back silently to CPU and every call costs 44 ms instead of 7.98 ms while returning the right answer. `error_on_failure` on the CUDA provider dispatch converts that into a build error, and it is the primary guard.

It is not sufficient, which is why there is a second check. `error_on_failure` fails a build when the provider cannot be registered at all; it does not fail a build in which the provider registers and then individual unsupported nodes are partitioned onto CPU. That partial fallback is slow in exactly the same way and reports success in exactly the same way.

```rust
/// After warmup, the median batch-one call must be fast enough to be on the device.
fn check_on_device(&self, name: &str, s: &dyn PairScorer) -> Result<(), ExtError> {
    const PAIR: (&str, &str) = ("A cat sat on the mat.", "There is a cat.");
    for _ in 0..5 {
        s.score_pairs(&[PAIR])?;               // warm kernels and the arena
    }
    let mut ms = Vec::with_capacity(9);
    for _ in 0..9 {
        let t = Instant::now();
        s.score_pairs(&[PAIR])?;
        ms.push(t.elapsed().as_secs_f64() * 1000.0);
    }
    ms.sort_by(f64::total_cmp);
    let median = ms[4];
    if median > self.inner.limits.max_ms {
        return Err(ClassifyError::OffDevice {
            classifier: name.into(),
            median_ms: median,
            limit_ms: self.inner.limits.max_ms,
        }
        .into());
    }
    Ok(())
}
```

The default ceiling is 20 ms, configured as `self_check_max_ms`. It is chosen to sit more than a factor of two from both measured outcomes: 7.98 ms on CUDA FP32 and 44 ms on the CPU fallback, so neither a slow device nor a fast host moves the verdict. A median over nine samples after five warmup calls, rather than one sample, because the first call carries kernel autotuning and arena growth. The check is skipped when the configured device is `cpu`, since a deliberate CPU deployment is a valid configuration and only an accidental one is a bug.

### Invariant three, by construction: the artifact is the one that passed parity

`check_golden` reloads the fixture recorded at export time and asserts the live session reproduces it to three decimals. This is a re-run of the parity gate against the deployed file, so a swapped, truncated, or re-exported artifact fails at boot rather than at the first call that matters. With `verify = "hash"` the manifest's sha256 is checked first, which is cheaper than a forward pass and catches corruption before any GPU work.

Tension: three checks per model at every boot cost a few hundred milliseconds of startup and require the weights to be present before the service accepts a connection, which is the intended trade and is the same posture as every other extension's `validate`.

## FP32 is the only precision

There is no dtype option because every alternative measured worse on both axes.

- INT8 collapses the model. Entailment scores fall from 0.99 to 0.49, and macro-F1 drops between 21 and 38 points depending on the corpus. A 0.49 entailment score is not a wrong answer that looks wrong; it is a coin flip wearing a probability.
- INT8 on CUDA is slower anyway, at 27.37 ms against FP32's 7.98 ms, so the usual quantization bargain is not on offer here.
- FP32 ONNX matches PyTorch probabilities to three decimals. That is what makes the offline parity gate a gate rather than an approximation, and it is what retires the bf16 and fp16 `CrossEncoder` instability recorded for the Python cross-encoder path in `wg21-paperflow/SERVICES.toml`, where bf16 on older CUDA produced NaN logits and fp16 was the documented workaround.

Tension: FP32 weights cost four times the memory of INT8, spent to keep the numbers trustworthy, and that is the largest single line in the crate's two-gigabyte budget.

## Measured latency

At batch size one on an RTX 4070 Laptop, measured 2026-07-25:

- DeBERTa-v3-base, ONNX FP32 on CUDA: 7.98 ms at sequence length 64.
- The same model through PyTorch: 14.47 ms.
- The same model as INT8 on CUDA: 27.37 ms.
- The same model on a silent CPU fallback: 44 ms.
- MiniLM: 0.4 to 1.5 ms per call.

At batch 32 the advantage vanishes: 209 sentences per second through ONNX against 207 through PyTorch. So what ONNX wins is launch overhead and kernel fusion, not arithmetic. That is precisely the regime the Lua layer produces, because a section's pre- and postconditions call a classifier once with a short input and then do it again on the next paragraph, tens to hundreds of times per run, with no opportunity for anything to batch across calls. A runtime whose classifier calls arrived in batches of 32 would have no reason to prefer ONNX; this one does.

The production card is an RTX PRO 6000 Blackwell 96GB, which is faster than the laptop part these numbers came from, so they are a ceiling rather than a forecast. The self-check ceiling of 20 ms is set against the laptop numbers for that reason.

## Why there is no HTTP escape hatch

Serving these models over HTTP is impossible rather than inconvenient, and the finding is about model support rather than latency.

- vLLM v0.26.0 carries zero DeBERTa entries in its model registry. Confirmed three ways on 2026-07-25: no case-insensitive match for `deberta` in `registry.py`, none in `supported_models.md`, and no DeBERTa row in the classification or scoring tables.
- PR 42094 is the live attempt to add `DebertaV2ForSequenceClassification` and has sat open since May with no activity since 2026-06-10. An earlier attempt, PR 20215, closed unmerged after roughly ten months.
- The cause is architectural. Disentangled attention splits queries and keys into content and position components and buckets relative positions, which vLLM's standard attention layer cannot express. It is a roughly 630-line new model file, not a configuration flag.
- The transformers fallback is closed too. `--model-impl transformers` requires the model to route attention through `ALL_ATTENTION_FUNCTIONS` and to set `_supports_attention_backend = True`; HuggingFace's `modeling_deberta_v2.py` has zero occurrences of either and computes attention directly in `DisentangledSelfAttention`.
- SGLang v0.5.16 is a strict subset here, registering only `BertModel`, Contriever, `BertForSequenceClassification`, `XLMRobertaModel`, and `XLMRobertaForSequenceClassification`. There is no `deberta.py` in its model directory.

Both engines are the wrong tool for encoder work regardless of which checkpoint is loaded. The one credible measurement, vLLM issue 41390 with a published reproduction, puts vLLM at 907 queries per second against plain HuggingFace Transformers at 1671 on the same bidirectional encoder, which is 1.8x slower per query excluding startup, with startup itself three times longer at 13.654 seconds against 4.457. Continuous batching, paged attention, and prefix caching are the entire reason to accept an engine's overhead, and none of them apply: chunked prefill conflicts with a non-causal attention mask on both engines, and a radix cache is not reusable for encoders at all. Add JSON encode, a localhost round trip, tokenization in a separate process, a ZMQ hop, and a scheduler step per call, and the comparison at batch one is a contest between fixed overheads that the in-process path does not have.

Tension: the classifier path has no HTTP escape hatch, so a deployment that cannot run in-process CUDA cannot run classifiers at all, and a fallback would be a model change rather than a configuration change.

## GPU memory

About two gigabytes in-process, covering FP32 weights for the configured classifiers, the CUDA context, cuBLAS and cuDNN workspace, and the ONNX Runtime arena. `with_memory_limit` caps the arena per session and `ArenaExtendStrategy::SameAsRequested` stops it doubling, so the number is a budget rather than a hope.

The budget is static, and the co-hosting mechanism is MPS rather than MIG. MIG is supported on the production RTX PRO 6000 Blackwell 96GB, but its smallest partition is 24 gigabytes and one quarter of the SMs, in fixed steps, so a large generative model plus classifiers plus a speech stack cannot be expressed: it would have to be four 24-gigabyte slices, capping the generative model at 24 while handing the classifiers 24 they cannot use. Enabling MIG additionally requires switching the card from graphics to compute display mode, which disables physical display output on a workstation where that card is the primary adapter. MPS leaves the display intact, allows uneven budgets, and lets kernels from different processes overlap instead of time-slicing.

Startup order on a single card is a hard requirement rather than a nicety, because vLLM computes its reservation as a fraction of free memory at profiling time and holds it for the process lifetime:

1. vLLM first, with explicit headroom, budgeted in absolute bytes via `kv_cache_memory_bytes` so the reservation does not depend on a denominator that moves with launch order.
2. Then the runtime process, whose classifier sessions are built eagerly in `ClassifyExt::new` and whose two gigabytes are allocated by the time `validate` returns.
3. Then any speech stack.

Set `CUDA_MPS_ACTIVE_THREAD_PERCENTAGE` per client so a generative decode loop does not head-of-line block a short classifier pass, and `CUDA_MPS_PINNED_DEVICE_MEM_LIMIT` as a backstop, understanding that both are API-level checks rather than hardware isolation and that neither partitions memory bandwidth. Verify the SM cap with `nvidia-cuda-mps-control` rather than `nvidia-smi`, whose `utilization.gpu` reports the fraction of time any kernel was running and therefore reads near 100 percent for a client capped at 1 percent of SMs.

Two honest notes. These two gigabytes sit outside the gateway's request budget: the gateway owns LLM concurrency and knows nothing about a classifier call, so a section that ranks 200 candidates consumes GPU time no admission control accounted for. And the alternative was worse rather than merely different: an HTTP-served classifier would be a second engine process, a second CUDA context, a second reservation never returned while running, a second MPS client, and a second entry in the startup ordering, all to serve an 86M-parameter encoder.

## The per-section call cap

Classifier calls are capped per section, for the same reason tool calls are: ranking hundreds of candidates inside a loop is easy to write by accident, and a prompt author debugging a precondition will not notice that a nested loop turned 40 calls into 1,600.

The cap is the core's existing `Limits::max_lua_calls_per_section`, counted by the core at the dispatch boundary and configured in `prompts.toml` under run limits. This crate adds no counter of its own, which is what keeps it stateless and lets `on_section` stay a no-op. The batch-shaped signatures are what make one number sufficient: `classify.rank` over 200 candidates and `classify.embed` over 200 paragraphs each cost one call, so the cap constrains how many times a section reaches for a model rather than how much text it scores.

Tension: the budget is shared with every other Lua host call, so a section that ranks heavily and writes heavily competes for one number, and a legitimately large ranking job raises the cap in configuration for every host object at once.

## The offline export pipeline

Export is a documented, reproducible procedure that runs before deployment and never inside the runtime. Its output is an artifact directory plus a manifest, and it must reach numerics parity with PyTorch to three decimals before any prompt calls the model.

Where the tooling lives:

- `tools/export-onnx/` in the workspace, a Python project with its own `pyproject.toml` and a lockfile, run under `uv`. It is not a workspace crate and nothing links it.
- Primary route is `optimum-cli export onnx` with the opset pinned to 17. Fallback is `torch.onnx.export` on the TorchScript tracer path, which is the path the opset floor is about.
- Exporter, torch, transformers, and optimum versions are pinned in the lockfile and copied into the manifest, because an export is reproducible only against the toolchain that produced it.

Where the weights live:

- Under the configured `model_root`, one directory per `<checkpoint-slug>/<export-id>`, where `export-id` is `onnx-fp32-opset<N>-v<K>`. `prompts.toml` names that relative path, so moving the root is a configuration change and the identity of an export is immutable.
- Tensors are never in git. The directory holds `model.onnx`, `tokenizer.json`, `config.json`, `export.toml`, and `golden.json`.
- Git holds `export.toml` and `golden.json` only. They are small, they are the reviewable part, and they are what the runtime checks against, so a change to an export shows up as a diff in a pull request even though the weights do not.
- Versioning is by new directory, never by overwrite. `v2` sits beside `v1` until every configuration has moved, so a rollback is a configuration line rather than a re-export.

What `export.toml` records, all of it read by the runtime or by a reviewer:

- source checkpoint identifier and its resolved revision hash
- opset, precision, and the exporter and framework versions
- sha256 of `model.onnx`, `tokenizer.json`, and `config.json`
- input and output names and shapes, and `max_length`
- the head kind, and for an NLI head the `id2label` mapping and the resolved entailment, neutral, and contradiction indices
- for an embedder, the pooling mode, the normalization flag, and the dimension
- the parity gate's result, including the corpus size and the worst observed absolute difference

What the parity gate asserts, in the export script, before it will write the manifest:

1. The opset read back from the emitted graph is 15 or higher.
2. Over a fixed corpus of at least 32 inputs spanning short and long sequences up to `max_length`, and for an NLI model at least four hypothesis templates, ONNX FP32 on CUDA and PyTorch FP32 agree on every output probability to within 1e-3.
3. Argmax agrees on every input. A three-decimal match with a flipped argmax on one borderline input is a failure, because argmax is what `classify.label` returns.
4. Two unrelated inputs produce outputs that differ by more than 1e-6, which is the degeneracy check run offline as well as at boot.
5. For an embedder, cosine similarity against sentence-transformers output on the same corpus is within 1e-3, which is what catches a pooling or normalization mismatch that produces valid-looking vectors.
6. Latency at batch one on the export machine is recorded, not asserted, so a regression across export versions is visible.

`golden.json` is written from the same corpus: a handful of inputs and their expected outputs, which is what `check_golden` reloads at every boot. One artifact therefore drives the offline gate and two of the three runtime self-checks.

Tension: an export step stands between a published model and a usable one, and a new checkpoint is a procedure rather than a configuration line.

## Carrying the `ort` release-candidate risk

`ort` has been a release candidate since February 2024, across thirteen releases, with breaking API churn between them. `fastembed` 5.17.2 depends on one exact release candidate, so the `ort` version is not independently chosen: upgrading `ort` means upgrading `fastembed`, and upgrading `fastembed` means taking whichever `ort` it pins. Upgrades are gated externally.

That risk is carried rather than solved, with two mitigations.

- Exact pins. `=2.0.0-rc.12`, `=5.17.2`, `=0.23.1`, plus a committed lockfile. A release candidate can be yanked or republished, and a caret range on a pre-release dependency is an unplanned upgrade waiting for a clean build.
- A trait boundary. `PairScorer` and `Embedder` are the only surfaces the rest of the crate uses, and `ort` and `fastembed` types appear only inside their implementations and inside `new`. This is the same containment used for storage in the paperstore extension. An API break lands in two files, and a replacement runtime is a third implementation of two traits rather than a rewrite.

Tension: a dependency the project cannot upgrade on its own schedule sits under a load-bearing feature, and the trait boundary bounds the cost of that without removing it.

## Determinism

The dtype half of the problem is closed. FP32 is pinned in both environments, matches PyTorch to three decimals, and is asserted at boot against a golden fixture, so the bf16 NaN behaviour and its fp16 workaround recorded on the Python cross-encoder path do not arise here.

What remains is batch composition. A differently batched rerun can score differently, because the reduction order inside a batched matmul depends on the batch, and floating-point addition is not associative. The crate therefore makes batch composition a property of the call rather than of the schedule:

- Every operation batches exactly what one call passed. Nothing is coalesced across calls, across runs, or across sections.
- The per-session mutex means no second caller's work is ever in the same batch.
- `classify.rank` and the `texts` form of `classify.embed` take the whole set in one call, so the batch is the array the author wrote and is stable across reruns of the same prompt with the same inputs.
- Result ordering is total. `rank` breaks score ties by ascending index rather than leaving equal scores in whatever order the sort produced.

Under the system's rerun-everything principle this is enough for a rerun of the same prompt over the same inputs to reproduce. It is not enough for a rerun over a differently sized candidate set to reproduce the scores of the overlapping candidates, and that is a real limit rather than a rounding remark. Tension: a prompt that filters its candidate set before ranking will score the survivors differently than it did when they were ranked alongside the rejects.

## Feature gating and the dependency tree

In the two host binaries, `promptforge-mcp` and `promptforge-cli`:

```toml
[features]
default = []
classify = ["dep:promptforge-ext-classify"]

[dependencies]
promptforge-ext-classify = { path = "../promptforge-ext-classify", optional = true }
```

Registration is explicit, in the central `register_all`, gated by the same feature:

```rust
pub fn register_all(cfg: &Config) -> Result<Extensions, ConfigError> {
    let mut exts = Extensions::new();
    exts.add(Arc::new(SearchExt::new(&cfg.search)?));
    exts.add(Arc::new(PaperstoreExt::new(&cfg.store)?));
    #[cfg(feature = "classify")]
    exts.add(Arc::new(ClassifyExt::new(cfg.classify()?)?));
    Ok(exts)
}
```

In this crate:

```toml
[dependencies]
promptforge = { path = "../promptforge" }
ort = { version = "=2.0.0-rc.12", default-features = false, features = ["cuda", "load-dynamic"] }
fastembed = { version = "=5.17.2", default-features = false }
tokenizers = { version = "=0.23.1", default-features = false, features = ["onig"] }
serde = { workspace = true }
serde_json = { workspace = true }
schemars = { workspace = true }
thiserror = { workspace = true }
tokio = { workspace = true }
sha2 = { workspace = true }
```

`fastembed` takes `default-features = false` because its default set includes the online model download path, and this runtime must never reach the network for weights: every artifact is a local export the manifest names. `ort` takes `load-dynamic`, so the ONNX Runtime shared library is located at runtime through `ORT_DYLIB_PATH` rather than downloaded at build time; the CUDA provider has to match the host driver and toolkit, so which build is loaded is a deployment decision and not a build-machine decision.

With the feature off, the dependency graph gains nothing. No `ort`, no `fastembed`, no `tokenizers`, no `ndarray`, no ONNX Runtime shared library, no CUDA. The binary runs on a host with no GPU and no NVIDIA driver, every prompt that names no `classify_*` word runs unchanged, and any prompt that names one fails startup validation with an unbound canonical name. With the feature on, those crates and the ONNX Runtime and CUDA shared libraries are added, and nothing else in the workspace is affected, because no other crate depends on this one.

Tension: two build configurations to test and ship, and CI has to build both while only the GPU runner can test one of them.

## Errors

```rust
#[derive(Debug, thiserror::Error)]
pub enum ClassifyError {
    // Configuration and resolution, all boot-time.
    #[error("classifier slot `{0}` is not mapped")]
    UnknownSlot(String),
    #[error("classifier `{0}` is not configured")]
    UnknownClassifier(String),
    #[error("slot `{slot}` resolves to `{classifier}`, which is a {found} and not a {want}")]
    SlotKind { slot: String, classifier: String, want: &'static str, found: &'static str },
    #[error("classifier `{classifier}` has a {head} head; entailment needs a three-way NLI head")]
    HeadKind { classifier: String, head: &'static str },
    #[error("weights not found for `{classifier}` at {path}")]
    MissingWeights { classifier: String, path: PathBuf },
    #[error("manifest for `{classifier}` is unreadable or incomplete: {reason}")]
    BadManifest { classifier: String, reason: String },
    #[error("sha256 mismatch for {path}: manifest {want}, file {got}")]
    ArtifactMismatch { path: PathBuf, want: String, got: String },
    #[error("`{classifier}` was exported at opset {got}; 15 is the floor")]
    OpsetTooLow { classifier: String, got: i64 },
    #[error("CUDA execution provider unavailable for `{classifier}`: {source}")]
    ProviderUnavailable { classifier: String, source: ort::Error },
    #[error("session build failed for `{classifier}`: {source}")]
    SessionBuild { classifier: String, source: ort::Error },

    // Self-checks, all boot-time.
    #[error("`{classifier}` returns the same output for unrelated inputs; check the export opset")]
    Degenerate { classifier: String },
    #[error("`{classifier}` scored the unrelated pair at {low} and the entailing pair at {high}; check the label indices")]
    Ordering { classifier: String, high: f32, low: f32 },
    #[error("`{classifier}` median batch-one latency {median_ms:.1} ms exceeds {limit_ms:.1} ms; the session is probably on CPU")]
    OffDevice { classifier: String, median_ms: f64, limit_ms: f64 },
    #[error("`{classifier}` diverged from its golden fixture by {worst:.5} at {field}")]
    ParityDrift { classifier: String, field: String, worst: f64 },

    // Call-time.
    #[error("{0}")]
    InvalidArgs(String),
    #[error("`candidates` is empty")]
    EmptyCandidates,
    #[error("input of {got} tokens exceeds max_length {limit} for `{classifier}`")]
    TooLong { classifier: String, got: usize, limit: usize },
    #[error("hypothesis template for `{classifier}` has no `{{}}` placeholder")]
    BadTemplate { classifier: String },
    #[error("tokenization failed for `{classifier}`: {source}")]
    Tokenize { classifier: String, source: tokenizers::Error },
    #[error("inference failed for `{classifier}`: {source}")]
    Inference { classifier: String, source: ort::Error },
    #[error("`{classifier}` returned shape {got:?}, expected {want:?}")]
    Shape { classifier: String, got: Vec<usize>, want: Vec<usize> },
    #[error("classifier `{0}` was shut down")]
    ShutDown(String),
    #[error("classifier task failed to join")]
    Blocking(#[from] tokio::task::JoinError),
}

impl From<ClassifyError> for ExtError { /* boot-time surface */ }
impl From<ClassifyError> for ToolError { /* call-time surface */ }
```

The taxonomy splits on when a variant can occur, because that is what a reader needs. Everything above `InvalidArgs` is reachable only from `new` or `validate` and therefore only at boot; everything below is reachable from a call. Two conversions exist because the trait speaks `ExtError` and `ToolFn` speaks `ToolError`, and both are provided here so no call site writes a map. `thiserror` throughout, and `anyhow` appears nowhere in this crate's public surface.

Every message names the classifier, because a deployment configures several and a message that does not say which one is a message that starts an investigation instead of ending it.

## Tests

Nothing in this list needs a GPU except the parity gate and the two device checks, which are gated behind a `gpu` test feature and run on the GPU runner. Everything else runs against stub implementations of `PairScorer` and `Embedder`, which is the payoff of the two-trait boundary.

- Parity gate, on the GPU runner: load each configured export, run the full export corpus, and assert the three-decimal agreement, argmax agreement, and embedder cosine agreement that the export script asserted. This is the gate that stands between a checkpoint and a prompt, so it runs in CI rather than only in the export script.
- Golden fixture, on the GPU runner: `check_golden` against the deployed artifact, plus a negative case where a manifest sha256 is edited and `validate` fails with `ArtifactMismatch`.
- Degeneracy self-check, no GPU: a hand-built ONNX graph of a few kilobytes whose output is a `Constant` independent of its input, committed as a fixture. `check_discriminates` must reject it with `Degenerate`. The check is what is under test, so the fixture reproduces the symptom directly rather than reproducing the tracer bug. A real opset-13 export is the manual reproduction, recorded in the export tooling and not in CI.
- Wrong-index self-check, no GPU: a stub scorer with the entailment and contradiction indices transposed. `check_discriminates` must reject it with `Ordering`.
- Off-device self-check, no GPU: a stub scorer that sleeps 44 ms per call, which is the measured CPU-fallback figure. `check_on_device` must reject it with `OffDevice`. A second stub sleeping 8 ms must pass. A third asserts the check is skipped when the configured device is `cpu`.
- Lua level, no GPU: a Luau script exercising all four operations against stubs, asserting the primary-then-detail return shape of each, 1-based and descending order from `rank`, `top_k` truncation, `return_text` on and off, the flat versus nested return from `embed` under `text` versus `texts`, and that setting both or neither is `InvalidArgs`. A typo'd argument key must fail with a message naming the key, which is what `deny_unknown_fields` buys.
- Surface separation, no GPU: build a `ToolMap` with `ClassifyExt` registered, assert that the schema list sent to the model contains none of `classify_label`, `classify_entail`, `classify_embed`, `classify_rank`, and that the list is exactly what it was without the extension registered. Then assert the converse: the Lua environment has a `classify` table with four callable fields. This is the test that encodes the `LuaOnly` decision, and it is the test that fails if someone later changes a `Surfaces` value.
- Section scoping, no GPU: a section that calls no `tools.add` at all can still call `classify`, because the core installs capability families once per run and `ToolMap::scoped` filters only what the model sees. This is surprising enough to be worth a test that documents it.
- Cap, no GPU: a section looping past `max_lua_calls_per_section` fails, and a single `rank` over 200 candidates costs one call against it.
- Lifecycle, no GPU: a recording harness asserting that `on_section` is called for every event and does nothing observable, that `validate` runs every check on every configured model, and that `shutdown` releases each session and a subsequent call returns `ShutDown`.
- Slot resolution, no GPU: default resolution, per-prompt override, an unknown selector failing at boot with `UnknownSlot`, a `selector` slot pointing at an embedder failing with `SlotKind`, and `entail` against a `Relevance` head failing with `HeadKind`.
- Determinism, no GPU for the shape and on the GPU runner for the numbers: the same call twice is bitwise equal, and a 200-candidate `rank` compared against the same 200 candidates ranked in two batches of 100 is asserted only to the documented tolerance, which is the test that records the remaining limit rather than pretending it is closed.
- Feature off: a compile test that the host binary builds with `--no-default-features`, and a runtime test that a prompt naming `classify_label` fails startup validation with an unbound canonical name.

## Open

- Whether `ort` 2.0.0-rc.12 exposes `Session::run` as `&self` or `&mut self`. It decides only whether the per-session mutex is also a borrow requirement, since the mutex is there for determinism either way, but it decides that in the type system rather than in prose.
- The self-check latency ceiling on the production card under MPS with a generative model resident. Twenty milliseconds is derived from an idle RTX 4070 Laptop, and memory bandwidth is partitioned by neither MPS control, so a loaded card may push a genuinely on-device median past the ceiling and turn the check into a boot failure. The likely answer is a higher ceiling in production configuration; the honest answer is that it has not been measured.
- Whether `classify.rank` should cap its candidate count in the extension. The per-section cap bounds the number of calls but not the size of one, so a single call can rank ten thousand candidates and hold the session mutex for a minute.
- Whether the export corpus should be shared across checkpoints or per checkpoint. Shared makes two exports comparable; per checkpoint lets an NLI corpus carry hypothesis templates an embedder has no use for.

*2026-07-25 - design-classify*
