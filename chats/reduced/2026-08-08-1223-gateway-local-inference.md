# Gateway local inference, sys.model plans

*2026-08-08 12:23 - transcript 9fd78e35-10c0-494b-84b6-5cbaa0816e6e*



## Prompts



**[p1]** how much VRAM would it take to run Gemma 4

**[p2]** is there a non-MoE gemma?

**[p3]** what does Q4 mean

**[p4]** Q4 sounds terrible

**[p5]** okay so for my video card (Geforce RTX 4090) what Gemma can I run

**[p6]** How much context do I need for @tools-public/tools/briefer.md and keep in mind here's an example intermediate @cabinet/_scratch/2026-08-08-briefer-cpp-alliance/2026-08-08-briefer-cpp-alliance-evidence.md

**[p7]** I showed you briefer.md to understand what it does. I am porting briefer to promptforge, where it does not load the entire prompt into the context at once

**[p8]** only 32k context? that feels small. look at this report @umbra/campaigns/hodges-order-project/briefer-knights-of-malta.md @tools-public/output/briefer/briefer-wg21-cpp-committee.md @tools-public/output/briefer/briefer-python-software-foundation.md

**[p9]** what are some other models I can use

**[p10]** I need 64k context for the analysis stage

**[p11]** mistral is 24b why do you question its writing?

**[p12]** spawn subagents search the web for more information about mistral suitability for my use-case

**[p13]** is that Qwen dense?

**[p14]** how fast

**[p15]** lets try the Gemma 4 26B MoE in @promptforge for the tests we are doing

**[p16]** Can Question, here's the deal. The PromptForge gateway, like it's, I want the gateway, I want PromptForge to always talk to the gateway, like, no matter what. I just want that to be the central point of configuration, because I feel like it's a good separation of the concern. But the problem is that gateway has to talk to Ollama or this llama.cpp or the OpenAI or the Anthropic and whatever. So here's my question, why not build Ollama into the gateway itself so that I don't have this other stupid app? Like, why don't we just link it in? You know what I mean? And we can, the gateway can just be able to load models. I feel like that's the way to go. I wanna discuss this with you, okay? Because the configuration's a pain in the ass. You have to understand, like, I'm sitting here and I'm, I'm, I'm using an AI-driven workflow, and so it's like I'm disconnected from it. I'm not, I, I don't have my ear to the ground. I have all these layers of software in between me and the thing. And so I wanna simplify. And I don't care if the gateway executable is big. I don't, you know what I'm saying? Like let the Ollama support be like a crate, or maybe it can be a shared library, or maybe it can be a build setting, but it'd be nice to have it all built in, and so that it becomes very easy for me to swap models around. Like, okay, I can say, "Oh, go to Hugging Face and get this." In fact, I wanna have a centralized configuration file for the gateway. Like, I wanna be able to I wanna be able to have like one file The in my user directory or wherever, and then I can say, "Here's all the models, " and I can even have a URL, like the model can have the URL on Hugging Face where to download it, so then it can be, it can download what it needs on demand. What do you think about that?

**[p17]** I don't understand. You say, you say Olama handles model swapping, and I need to build Why can't I just use Olama? Just link, it's open source, just grab their fucking code!

**[p18]** This sounds very good. This sounds very good. However, however, I gotta say this, right now I'm using like Quinn nine B. I'm using a nine billion parameter one. I could easily see myself wanting to have like multiple embeddings. Like a classifier. I could, I could easily see that. You know, a re-ranker? And I feel like Someone has to manage that. And also, what if we what if I have a prompt and I want some of it to use local inference and then I want others to use remote, right? Like the gateway has to handle that. And then How do we share those resources? Who handles the queue? Who handles the concurrency limit? Because I want this gateway to also be usable on my server. So like this on our website that has like this AI workflow, like we have a cluster of machines and all the machines I want them to use this gateway, they have to share it. And so this way I can enforce the Q, because OpenAI and vLLM they don't have a very good Q. Like I wanna be able to write my Promptforge prompt where it just says fan out and it has like, like, fan out fifty, and then it just talks to the gateway. I think, or do I? We can't, we can't, we, we can build a limit into the prompt ex-executor, but even with that, we still need a way to multiplex. So if I've got five different people that are all competing for the run pod, then the gateway has to be able to like interleave all their shit.

**[p19]** To be honest, I'm not sure. I have to, we have to think, I wanna think about this some more. Let me tell you what I do know. I do know that For example, PromptForge requires the ToolPicker. And the tool picker uses, I think, embedding and reranker. You can take a, take a look, take a look at tool dash picker. And it doesn't make sense to do that over a network, right? Like even a server machine has a little bit of local VRAM, right? Or actually, i'm, i'm even thinking maybe that did we allow it to go on the cpu? We might even be running out on the CPU, have a look at it. @promptforge/crates/promptforge-tool-picker

**[p20]** I wanna think about this some more. So The tiny, the tiny utility models? I, I think though, if it's running on a CPU, there's no problem. Because there's no issues with shared memory and you don't have to link CUDA, how does that work? Does that use CANDLE?

**[p21]** The thing though, there's gonna be times when I'm gonna wanna run like Classify, I'm gonna wanna do like Classifiers that, that do twenty five predicates at a time over a large input like a, like a w g twenty one paper, and we're gonna need speed. So that's gonna need g p u, not a lot. But some @wg21-paperflow/paper-routing-classifier.md

**[p22]** what is the difference between Device::metal and Device::Cuda?

**[p23]** what if I have a rack server what kind of gpu does it have

**[p24]** no that's not what I'm saying. if I have a rack server and it is explicitly not an inference-configured server what kind of GPU can I expect? onboard?

**[p25]** I feel like if when we configure the queue, then the gateway has to have like logical groupings because we don't wanna put the queue limit on the local model and the runpod at the same time, like they each need their own limits, but we also don't want per model limits. The limit has to actually be on the hardware itself, so the configuration file for the gateway needs to be expressive enough that the admin can say, "Okay, here's all the models and embeddings that are on this device, right? Like they create a group that represents the device, the local video card. Or the, a specific run pod. Now you might have two different run pods and each of those needs its own limits because they're separate pieces of hardware. Or you might have one run pod that has multiple models on it, and we, we need to and then that's a, that's a single group. So there has to be groups. Do you agree?

**[p26]** Yes that makes sense. who is responsible for kv cache eviction? do I have to write that myself?

**[p27]** does llama run all possible open-weight models

**[p28]** When you say a novel architecture, do you mean like how the weights are arranged? So every different arrangement of parameters needs its own like code? What, but you mean, is that GPU code? Oh, so like CUDA, for example? Well, how does that work?

**[p29]** oh so its not even a problem at all. you could say that in practical terms, llama.cpp will run ALL MODELS

**[p30]** is there any downside to GGUF and why have GGUF? why not just use whatever pytorch uses

**[p31]** I dont understand. You dont NEED pytorch, anyone can just port pytorch

**[p32]** if I have a GGUF at full fidlity could I fine-tune that by converting it back to safetensors?

**[p33]** I'm just trying to understand. So the reason that GGUF "can't be fine tuned" (with the fp16 caveat) is not because of the format, it is just that in general you dont want to fine tune a quantized model. Regardless of how it is stored.

**[p34]** realistically is GGUF ever going away?

**[p35]** So here's. So if we're gonna be running locally, then We need a way to set up the card for the specific models, like the so the, the way the gateway has to work is there's a config file and it specifies, you know, what models are available, and everything has to fit in the video card, and it can also have remote models, so they can have other, other endpoints, but that's like a complete package of, of inference. But the thing is The video card has so little memory that if you wanna run basically the configuration is custom for a specific type of prompt. Like for example, all the analytical reports will probably share the same config. But then if I wanna run a different type of report, like let's say I wanna do like a threat analysis and I wanna have my own little separate embeddings, then we wanna tell the gateway, "Okay, unload everything and load this different config file." So the con a config file is like a package of models and configuration that's suited for specific workflows, because there's so little memory that we, we can't afford to have We can't load, we can't put general purpose, right? Like it's gonna be specific, like this model or that model. And so I'm thinking the gateway needs to have a command where you can, or you, or it has a directory of configs, and each config has a name, and you can tell the gateway, okay, reconfigure, load this new config file, right? And you're getting rid of all the other stuff, and now you're loading up this config file. So the gateway, when you run, you specify which config file you wanna load on the command line. And then we have a remote command that lets you change it, so you could prepare for the workload. So like you could, so the user has a batch file where they're gonna do their workload, and they tell the gateway, "Okay, now here's the config," and then they run a bunch of prompt for, for prompts. Do you understand?

**[p36]** 1. not graceful. the local machine has just one operator they are big boys who know wtf to do.
2. a profile should have a way to inherit another profile (and make that recursive). like "include" files.
3. no auto-select

**[p37]** update the plan so I can see it all. the plan is effectively the design doc. and I will decide what I like, what I dont like, what needs to change

**[p38]** Review the plan, do we have the right build order for the features? I wanna go from easiest and most useful to hardest and most risky.

**[p39]** yes. but how can things go sideways? are you saying you can't do the integration?

**[p40]** you will get it done in 2 hours

**[p41]** Question: For the Core Tests, we do all this, do we still need LlamaCPP and Llama Server, or can Core Tests just create a model profile and then tell the, and then set it in the gating Llama Server, launch the gateway, and pass it the profile so that it knows exactly what it's getting?

**[p42]** Core tests don't need the G-GoF. Those would go in the gateway. The core tests would just provide the configuration, the TAML, and then the TAML will provide the Hugging Face link and the PIN, and then the gateway will do the downloading and caching. Why would we put that in the server?

**[p43]** put that in the plan for the end

**[p44]** what do you suggest we take from  @tools-public/rulebooks/vibe-rulebook.md ?

**[p45]** Hey, yes, I like this, but the problem with the vibe rulebook is that the subagent discipline makes it take fucking forever. like, it takes a long time. So, and also for the review cycle, only one round of review. Because otherwise it just keeps finding shit. Only one round of review. And then Yeah. So yeah, use the vibe coder. Also use @tools-public/rulebooks/rust-rulebook.md

**[p46]** yeah good idea if someone doesnt need cuda it should not be forced. Yes add the execution method to the plan

**[p47]** I don't understand what this means:
Design call: local inference is a managed llama-server subprocess, not in-process FFI. Same operator story (one config, gateway owns lifecycle), stays under unsafe_code = "forbid". Revisit if IPC/lifecycle fails.

**[p48]** why does the workspace forbid "unsafe" rust?

**[p49]** you are telling me that every crate that my project uses, does not have any unsafe blocks?

**[p50]** I think you made the right call but what about this overhead of the HTTP and what port does it use and can it be accessed by other programs?

**[p51]** why didn't you use shared memory or a named pipe or something

**[p52]** so what's left

**[p53]** I ran the briefer.md how do I know it worked?

**[p54]** I want to have sys.model so I can print the model at the bottom of the report

**[p55]** the test should ensure that sys.model is unavailable during the prologue (lets call that the H1 lua block)

**[p56]** where is @promptforge/briefer.md gitigored

**[p57]** why did I have to force-add it

**[p58]** what is this DEFAULT_MODEL  ? there should be no DEFAULT_MODEL . this is the enemy of precision

**[p59]** Explain why we should keep that variable DEFAULT_MODEL

**[p60]** No about this. This doesn't This doesn't make any sense. There shouldn't, we shouldn't have a default model. Like, every prompt has to specify what it needs. If a prompt can take anything, then there should, it should say so explicitly. It should say, "Give me anything. " Ever being possible, because at a minimum, a prompt is gonna have to explain what the minimum context required is. It's gonna know if it needs thinking or not, it's gonna know if it needs to do reasoning or inference or any number of, a number of things. I mean, how can a prompt specify nothing? That doesn't make sense. The whole point of PromptForge is this precision. So I'm thinking we need to get rid of default model. What are the consequences of doing so?

**[p61]** Why should we keep PROMPTFORGE_MODEL  ?

**[p62]** yeah get rid of PROMPTFORGE_MODEL and write something in the design doc not about that specifically but the general principle: no defaults, everything explicit. This is a core principle of promptforge. implicit is the enemy of precision. What is BASE_URL is that for the gateway? It should be called PROMPTFORGE_GATEWAY_URL if so

**[p63]** also PROMPTFORGE_GATEWAY_KEY ?

**[p64]** review the plan, apply light @tools-public/rulebooks/vibe-rulebook.md steps (only one review pass, do the edits in the review context), apply @tools-public/rulebooks/rust-rulebook.md

**[p65]** review the plan, apply light @tools-public/rulebooks/vibe-rulebook.md steps (only one review pass, do the edits in the review context), apply @tools-public/rulebooks/rust-rulebook.md

**[p66]** what was I using before for the URL? a manua export each time befoer launching? how do I know the port?



## Plans

### Gateway Local Inference

*Design for embedding local model inference (llama.cpp + Candle) into the promptforge gateway, with profiles, device groups, lanes, queuing, and remote endpoint support.*

# PromptForge Gateway - Local Inference Design

## Core Concept

The gateway becomes the single point of inference for all promptforge workloads. It holds API keys for remote providers, loads local models into VRAM, manages concurrency, and exposes a unified OpenAI-compatible API. The executor (promptforge-cli, MCP server) never knows whether a model is local or remote - it just talks to the gateway.

## Profiles

A profile is a named configuration that describes everything loaded on the local GPU at a given moment. The gateway runs exactly one profile at a time. Switching profiles is immediate - kill in-flight local inferences, unload, load new config.

### Profile location

```
~/.promptforge/profiles/
├── base.toml
├── analytical.toml
├── threat.toml
└── paperflow.toml
```

### Profile inheritance

A profile can include other profiles recursively. Resolution order: depth-first, last-wins for conflicts on the same key.

```toml
# analytical.toml
include = ["base.toml"]

# threat.toml - inherits base via analytical
include = ["analytical.toml"]
```

Concrete semantics:
- Arrays (models, endpoints, devices) merge by appending. A child can override a parent's entry by declaring the same `id`/`name`.
- Scalars (server.bind, server.token) - child wins.
- `include` is resolved relative to the same directory as the including file.

### Profile switching

```bash
# At startup
promptforge-gateway serve --profile analytical

# At runtime (admin API)
POST /admin/switch-profile
{"name": "threat"}
```

Switching behavior:
- Immediate. No drain. In-flight local requests get an error response.
- Remote endpoint connections stay alive (they're not GPU-bound).
- The model catalog is re-advertised on the next `GET /v1/models` call.

## Devices

A device represents a physical compute resource with a concurrency constraint. Models reference their device. The queue enforces limits per-device.

```toml
[[device]]
id = "local-4090"
type = "local"            # local GPU managed by the gateway

[[device]]
id = "anthropic"
type = "remote"
concurrency = 10          # max concurrent requests to this provider

[[device]]
id = "runpod-a100-1"
type = "remote"
concurrency = 4
```

Local devices don't declare a top-level `concurrency` because their limits come from lanes (see below).

## Lanes

A lane is a concurrency slot within a device. Models declare which lane they use. This prevents a 5ms classifier from being blocked behind a 60-second LLM call, while still preventing two LLM calls from running simultaneously.

```toml
[[device.lane]]
device = "local-4090"
id = "generative"
concurrency = 1           # one LLM inference at a time

[[device.lane]]
device = "local-4090"
id = "utility"
concurrency = 8           # classifiers/embeddings can batch
```

Remote devices don't need lanes - their concurrency is flat (the remote server handles its own internal scheduling).

## Models

### Local generative models (llama.cpp)

```toml
[[local_model]]
name = "qwen-27b"
description = "Dense 27B model for structured analysis and long-context review"
source = "https://huggingface.co/bartowski/Qwen3.6-27B-GGUF/resolve/main/Qwen3.6-27B-Q4_K_M.gguf"
device = "local-4090"
lane = "generative"
context = 65536
thinking = "never"
cache_type_k = "q8_0"
cache_type_v = "q4_0"
flash_attention = true
gpu_layers = 99
```

The `source` field is a URL. On first use (or on `POST /admin/pull`), the gateway downloads the GGUF to a local cache directory (`~/.promptforge/models/`). If the file already exists, it's used directly. A local file path also works:

```toml
source = "~/.promptforge/models/custom-finetune.gguf"
```

### Local utility models (Candle, CPU or GPU)

```toml
[[local_model]]
name = "paper-classifier"
description = "Multi-hypothesis classifier for WG21 paper routing"
framework = "candle"
source = "~/.promptforge/models/paper-classifier-v1.safetensors"
device = "local-4090"
lane = "utility"
compute = "cuda"          # or "cpu" or "metal"
```

```toml
[[local_model]]
name = "bge-small"
description = "General-purpose sentence embeddings"
framework = "candle"
source = "compiled"       # special value: weights compiled into the binary
device = "local-4090"
lane = "utility"
compute = "cpu"
```

### Remote models

```toml
[[endpoint]]
id = "anthropic"
protocol = "openai"
base_url = "https://api.anthropic.com/v1"
api_key = "${ANTHROPIC_API_KEY}"

[[model]]
name = "claude-sonnet-4-6"
description = "Frontier model for complex analysis and coding"
context = 200000
thinking = "never"
upstream = "claude-sonnet-4-6"
endpoints = ["anthropic"]
```

Remote models have no device/lane - their concurrency is governed by the endpoint's device entry.

## Queue and Concurrency

Every request entering the gateway is routed to a device+lane. The queue enforces:

- **Per-lane semaphore** - at most N concurrent inferences per lane
- **Fair scheduling** - round-robin across callers when multiple requests are queued. No single caller starves others.
- **Backpressure** - when the queue is full (configurable depth), return HTTP 503 immediately. The executor retries or reports failure.

```toml
[queue]
max_depth = 100           # total queued requests before rejecting
fair_scheduling = true    # round-robin across client tokens
```

For remote endpoints, the device's `concurrency` is the semaphore. For local models, the lane's `concurrency` is the semaphore.

## Model Catalog and Semantic Binding

The gateway serves `GET /v1/models` with all available models (local + remote) from the active profile. The promptforge executor's semantic picker matches prompt needs (e.g. "A careful analysis model suited to structured reasoning") against model descriptions via cosine similarity, same as today.

When a profile switch occurs, the catalog changes. Any cached bindings in an executor are stale - the executor must re-fetch the catalog on its next run.

## Local Inference Engine

### Generative (llama.cpp)

The gateway links llama.cpp via Rust bindings. At profile load:
1. Download GGUF if not cached
2. Call `llama_model_load()` with configured `gpu_layers`
3. Allocate context with configured `context`, `cache_type_k`, `cache_type_v`, `flash_attention`
4. Serve completions through the same OpenAI-compatible `/v1/chat/completions` endpoint

At profile switch:
1. `llama_model_free()` - unload from VRAM
2. Load new profile's models

### Utility (Candle)

For CPU models: loaded once, stay resident across profile switches (they don't use VRAM).
For CUDA/Metal models: loaded/unloaded with the profile like generative models.

Candle models expose a different interface than chat completions (embeddings return vectors, classifiers return label scores). The gateway serves these through:
- `POST /v1/embeddings` - standard OpenAI embeddings endpoint
- `POST /v1/classify` - custom endpoint for classifier models

## Build Configuration

The gateway binary links llama.cpp and optionally CUDA/Metal via Cargo features:

```toml
[features]
default = ["local-inference"]
local-inference = ["llama-cpp-2", "candle-core"]
cuda = ["llama-cpp-2/cuda", "candle-core/cuda"]
metal = ["llama-cpp-2/metal", "candle-core/metal"]
```

A server with no GPU compiles without `cuda`/`metal` features - it still runs the gateway for remote routing and CPU-based utility models, just no local generative inference.

## Admin API

```
POST /admin/switch-profile    {"name": "analytical"}
POST /admin/pull              {"model": "qwen-27b"}       # download source URL to cache
GET  /admin/status                                         # current profile, loaded models, queue depth
GET  /admin/profiles                                       # list available profiles
```

## Example: Full Profile for Analytical Reports

```toml
# ~/.promptforge/profiles/analytical.toml
include = ["base.toml"]

[[device]]
id = "local-4090"
type = "local"

[[device.lane]]
device = "local-4090"
id = "generative"
concurrency = 1

[[device.lane]]
device = "local-4090"
id = "utility"
concurrency = 8

[[local_model]]
name = "qwen-27b"
description = "Dense 27B model for structured analysis and long-context review"
source = "https://huggingface.co/bartowski/Qwen3.6-27B-GGUF/resolve/main/Qwen3.6-27B-Q4_K_M.gguf"
device = "local-4090"
lane = "generative"
context = 65536
thinking = "never"
cache_type_k = "q8_0"
cache_type_v = "q4_0"
flash_attention = true
gpu_layers = 99
```

```toml
# ~/.promptforge/profiles/base.toml

[server]
bind = "127.0.0.1:8081"
token = "${PROMPTFORGE_TOKEN}"

[queue]
max_depth = 100
fair_scheduling = true

[[device]]
id = "anthropic"
type = "remote"
concurrency = 10

[[endpoint]]
id = "anthropic"
protocol = "openai"
base_url = "https://api.anthropic.com/v1"
api_key = "${ANTHROPIC_API_KEY}"

[[model]]
name = "claude-sonnet-4-6"
description = "Frontier model for complex analysis and coding"
context = 200000
thinking = "never"
upstream = "claude-sonnet-4-6"
endpoints = ["anthropic"]

[tools.web_search]
provider = "brave"
api_key = "${BRAVE_API_KEY}"
```

## Operator Workflow

```bash
# Prepare for analytical work
promptforge-gateway serve --profile analytical

# In another terminal (or in a script)
promptforge run briefer.md "The C++ Alliance"

# Switch to threat analysis
curl -X POST http://localhost:8081/admin/switch-profile -d '{"name":"threat"}'

# Run threat workload
promptforge run threat-briefer.md "Target Organization"
```

Or in a batch script:

```bash
#!/bin/bash
curl -s -X POST http://localhost:8081/admin/switch-profile -d '{"name":"analytical"}'
promptforge run briefer.md "Subject A"
promptforge run briefer.md "Subject B"
promptforge run briefer.md "Subject C"

curl -s -X POST http://localhost:8081/admin/switch-profile -d '{"name":"paperflow"}'
promptforge run classify-paper.md "P3456R2.md"
```

## Implementation Layers (in build order)

1. **Queue + concurrency** - add semaphores and fair scheduling to existing gateway routing. Works immediately for remote endpoints.
2. **Profile system** - config loading, inheritance resolution, `switch-profile` admin API, profile directory scanning.
3. **Local generative inference** - link llama.cpp, implement model load/unload lifecycle, serve through `/v1/chat/completions`.
4. **Model download + caching** - HTTP GET from source URL, store in `~/.promptforge/models/`, check hash/existence before re-downloading.
5. **Local utility models on GPU** - extend Candle integration from CPU-only (tool-picker) to CUDA/Metal for classifiers and embedders that need speed.


Todos:

- Add per-device/lane semaphores and fair scheduling to gateway routing
- Implement profile config loading with recursive include resolution and switch-profile admin API
- Link llama.cpp via Rust bindings, implement model load/unload lifecycle
- Serve local llama.cpp inference through /v1/chat/completions endpoint
- HTTP download from source URL with cache management in ~/.promptforge/models/
- Extend Candle from CPU-only to CUDA/Metal for utility models (classifiers, embedders)

### Add sys.model

*Expose the section's effective model name as `sys.model` for prose substitution and Lua (including epilog), then use it in briefer.md to footer the report.*

# Add `sys.model`

## Goal

Make the bound/effective model name available as `sys.model` so briefer can write a footer like `*2026-08-08 - qwen-local*` without hardcoding.

## Behavior

After a section's model scope closes, `sys.model` is the caller-facing gateway model name:

1. Bound model from `models.use` or `models.always` → `ModelBinding::id().name()` (same string sent as `CompletionOptions.model`)
2. Else host client model (`GatewayClient::model()` / `PROMPTFORGE_MODEL`)
3. Else `DEFAULT_MODEL` (`claude-sonnet-4-6`)

Available as:

- `{{ sys.model }}` in prose (post-close substitution)
- `sys.model` in Lua after close (preamble already ran; **epilog** is the intended consumer for a reliable footer)

Do not put `model` in the initial pre-preamble `sys` object - that misses section-local `models.use`.

## Code changes

### 1. Enrich + re-seal in [execute.rs](c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core\src\execute.rs)

After `close_scopes` / computing `completion_options`, before `subst::substitute`:

- Resolve `model_name` as above
- Insert `"model"` into a clone of the `sys` JSON object
- Pass enriched sys to `substitute`
- Re-inject sealed Lua `sys` so epilog sees the field (extend `SectionVm` with a small `set_sys` / `update_sys` that reuses `seal_sys`, or call existing inject path for sys only)

Mirror the same enrichment in [fanout.rs](c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core\src\fanout.rs) for arm prose + arm epilog.

Prefer a shared helper e.g. `fn enrich_sys_model(sys: &Value, scopes: &ClosedScopes, client: Option<&GatewayClient>) -> Value` in `execute.rs` (or a tiny private module) used by both paths.

### 2. Lua seal stays as-is

[lua.rs](c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core\src\lua.rs) `seal_sys` already indexes arbitrary frozen fields - no API change beyond re-sealing after enrich.

### 3. Docs

- [README.md](c:\Users\Vinnie\src\cursor\promptforge\README.md) sys table: add `sys.model`
- [design-core.md](c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core\design-core.md): note post-close enrichment

### 4. briefer.md footer

In [briefer.md](c:\Users\Vinnie\src\cursor\promptforge\briefer.md) Report epilog:

```lua
store.write("report.md", reply .. "\n\n*" .. sys.when .. " - " .. sys.model .. "*")
```

(Matches existing briefer report metadata style elsewhere: date - model.)

### 5. Tests

- Unit/integration: section with `models.always` / `models.use` → substituted prose or epilog can read `sys.model` equal to the bound catalog name
- Fanout arm: `sys.model` present when arm uses a model
- No binding: falls back to host/default model string

## Out of scope

- Alias name (`writer`) - expose gateway model id only
- Upstream/provider rewrite name inside the gateway child - caller-facing catalog name only


Todos:

- Add enrich_sys_model helper; wire execute.rs + fanout.rs; re-seal Lua sys after close
- Document sys.model; update briefer.md Report footer
- Tests for bound model, fallback, and fanout sys.model

StrReplace-edited design docs (path only): `c:\Users\Vinnie\src\cursor\promptforge\README.md`, `c:\Users\Vinnie\src\cursor\promptforge\crates\promptforge-core\design-core.md`
