# Deploying a Multi-User Voice Chatbot: End-to-End Component Guide (2026)

This document describes every component needed to build and deploy a cloud voice chatbot that serves many concurrent users. The flow the user described:

- Browser captures the user's speech and streams it (over a WebSocket) to the cloud
- Cloud converts speech to text (STT)
- An open-weight LLM hosted in the deployment processes the text
- The response text is converted to speech (TTS)
- Audio is streamed back to the browser and played

The controlling design fact for the whole system: **"real-time" is not one fast model, it is streaming and pipelining across every stage.** STT streams partial transcripts while the user is still talking, the LLM starts generating on that prefix, TTS starts synthesizing on the LLM's first sentence, and the browser plays sentence one while later tokens are still being generated. Run the stages sequentially and no amount of per-stage speed saves you. The target is **sub-1s** (ideally ~450-900ms) from end-of-user-speech to first-audio-out.

---

## 1. Reference Architecture

```
[Browser client]
  |  WebRTC (media) + WebSocket/DataChannel (control/signaling)
  v
[Edge / Media Ingress] -- TLS termination, auth handshake, DDoS/WAF
  v
[Connection Gateway] -- stateful session handlers, VAD, turn detection
  v
[Orchestration / Agent Session] -- the "brain": drives STT -> LLM -> TTS,
  |                                 handles barge-in, tool calls, per-user context
  |--> [STT service]  (CPU or GPU pool)
  |--> [LLM service]  (dedicated GPU pool, vLLM/SGLang)
  |--> [TTS service]  (small GPU / MIG / CPU pool)
  ^
[Streaming bus] -- audio/text frames flow bidirectionally between stages
  v
[Audio streamed back to client and played]
```

### End-to-end latency budget (the constraint that drives every decision)

| Stage | Target | Notes |
|---|---|---|
| Audio transport (one-way) | 20-50ms | WebRTC beats raw WebSocket on lossy/mobile networks |
| VAD / turn detection | 150-300ms | Prefer semantic turn detection over fixed silence timers |
| STT first partial | 100-200ms | Must be streaming; mostly hidden under user speech |
| **LLM time-to-first-token (TTFT)** | **150-400ms** | **The number to optimize.** Dominated by model size + serving stack |
| TTS time-to-first-audio (TTFB) | 100-300ms | Must be streaming synthesis |
| Buffer / orchestration overhead | 20-60ms | Client jitter buffer, sentence aggregation |
| **Total perceived** | **~450ms-1s** | >700ms feels sluggish; >2s reads as a dropped call |

Measured real-world reference: a Deepgram STT + vLLM-served Qwen2.5-7B + ElevenLabs TTS streaming cascade hit **P50 ~947ms (best case 729ms)** time-to-first-audio, with self-hosted vLLM on a single A10G comparable to cloud APIs. Native speech-to-speech models (e.g. Qwen2.5-Omni) are still far too slow to self-host (~13s TTFA); hosted S2S APIs (OpenAI Realtime, Gemini Live) can hit <500ms by collapsing the pipeline, but give up the open-weight self-hosting requirement.

### Don't hand-roll the frame graph

Two open-source frameworks dominate in 2026 and provide the streaming/interruption machinery (sentence aggregation, barge-in, reconnection) you would otherwise spend months building:

- **Pipecat** (Python, transport-agnostic) - pipeline of frame processors; interruption frames propagate upstream to cancel in-flight LLM/TTS work; 68+ service integrations; official client SDKs for JS, React, React Native, Swift, Kotlin, C++, ESP32. Best for maximal control and provider flexibility; you own scaling.
- **LiveKit Agents** (Python, built on LiveKit's WebRTC infra) - session-based; handles WebRTC transport, room management, horizontal scaling, and ships a transformer-based **semantic turn detector at sub-75ms P99**. Best when you want transport + scaling + telephony solved for you.
- Other credible bases: **Vocode**, and the HuggingFace `speech-to-speech` pipeline (exposes an OpenAI-Realtime-compatible WebSocket API with every component swappable, so the LLM slot can point at vLLM).

Recommendation: use **LiveKit Agents** (WebRTC + scaling handled) or **Pipecat** (fine-grained control). Do not build VAD, the frame graph, and interruption handling from scratch. (high confidence - this is the dominant 2026 pattern)

---

## 2. Client Layer (Browser)

The most important 2026 fact: **you almost never hand-roll all of this anymore.** WebRTC stacks (LiveKit, Pipecat, OpenAI/Gemini Realtime SDKs) ship the hard parts (echo cancellation, jitter buffer, Opus, VAD hooks) for free. Hand-built `getUserMedia` + AudioWorklet + WebSocket is the right choice for prototypes, direct-to-provider WebSocket APIs, and when you need full control.

### 2.1 Audio capture

- **Use `AudioWorklet`**, not `MediaRecorder` (forces WebM/Ogg containers, adds latency, emits encoded blobs not raw PCM) and not the deprecated `ScriptProcessorNode` (runs on the main thread, glitches under load). AudioWorklet latency at 48kHz is ~2.67ms vs 5-341ms for ScriptProcessorNode.
- **Capture at native sample rate, downsample in the worklet.** Do not trust the `sampleRate` constraint on `getUserMedia` - Firefox ignores it, Safari/iOS always returns 44.1kHz. Read `AudioContext.sampleRate` inside the worklet and downsample unconditionally to your target (16kHz for STT, or 24kHz if the provider wants it). Use `libsamplerate-js` for high-quality resampling.
- **Mono only** (speech is mono; stereo doubles bandwidth for zero STT benefit). Convert Float32 -> Int16 PCM inside the worklet.
- **Chunk cadence:** aggregate the worklet's 128-sample renders into **20ms frames** (aligns with Opus/model frame boundaries), up to ~50ms.
- iOS gotcha: `AudioContext` requires a direct, synchronous user gesture to start.

### 2.2 Encoding for transport: PCM vs Opus

- **Raw PCM16 @ 24kHz mono ~= 384 kbps.** Simple, zero encode CPU, no decode hop, but ~10-12x the bytes of Opus and no loss resilience. Base64'ing it into JSON makes it worse (~512 kbps).
- **Opus @ 16-32 kbps mono (~2-4 KB/s)** - ~1/12 the bandwidth, ~40ms combined encode/decode, adaptive bitrate, and built-in **PLC (packet loss concealment) and FEC**. Get it via the **WebCodecs `AudioEncoder`** (ships in all major browsers in 2026, hardware-accelerated, no container muxing, off the main thread).
- **Decision rule:** use PCM16 when the provider ingests it natively (OpenAI Realtime, Gemini Live) or on a private VPC link where egress is free; use Opus for any internet-facing path, especially mobile/lossy links and high concurrency. Common topology: **client <-> edge = Opus over the internet; edge <-> inference = PCM16 over private VPC.**

### 2.3 Voice Activity Detection (client-side)

- Running VAD in the browser eliminates a server round-trip for endpointing and cuts bandwidth (transmit only speech). Server-side VAD adds a full RTT.
- Standard: **`@ricky0123/vad-web`** running **Silero VAD** via ONNX Runtime Web (WASM) inside an AudioWorklet. ~1-2MB, callback API (`onSpeechStart`/`onSpeechEnd`), runs on the audio thread. Self-host the `.onnx`/`.wasm`/worklet assets to avoid the CDN default footgun.
- **Endpointing is a latency tax:** fixed 600-800ms silence timers alone can blow the budget. Tune the silence window low and/or move to **semantic turn detection**.

### 2.4 Playback of returned audio

- **Use the Web Audio API, not MediaSource Extensions** (MSE carries 2-5s first-frame latency).
- Two patterns, ascending quality:
  - **A. Scheduled `AudioBufferSourceNode`** - decode each PCM chunk, schedule at `nextStartTime` against `AudioContext.currentTime` (never `Date.now()`), chaining buffers end-to-end. Works everywhere including iOS. Clicks on underrun.
  - **B. Jitter-buffered `AudioWorkletNode` ring buffer (production-grade)** - worklet drains a sample queue on the audio thread with a configurable prebuffer "waterline"; on underrun it outputs pre-zeroed silence and re-buffers (a late chunk becomes a clean pause, not clicks).
- **Jitter buffer sizing (adaptive, don't hard-code):** ~100-150ms on wired/5G; 200-300ms on congested 4G; ~150ms for server-paced realtime audio, 400-600ms for bursty HTTP-streamed TTS. Under-buffer = stutter; over-buffer = perceived TTFB worse than measured.
- **Barge-in is a client-first state-machine problem.** When the user interrupts, three buffers hold stale agent audio (server generation queue, network, client playback). Cancelling only server-side does nothing if the client already has ~800ms queued. Order: **flush the local playback buffer AND `stop()` every scheduled `AudioBufferSourceNode` first (~0ms), then signal the server to cancel, then truncate conversation history to `played_ms`** so the LLM doesn't reference words the user never heard. Use a higher confidence threshold for barge-in than for normal turn detection (the agent's own voice is the biggest false trigger).
- **Echo cancellation is essential once barge-in exists.** Enable `echoCancellation: true, noiseSuppression: true, autoGainControl: true` at capture. Caveat: if you play TTS through a custom AudioContext/worklet, browser AEC may not "see" the reference well; keep **half-duplex ducking** (reduce output 10-20dB while agent speaks) as a fallback.

### 2.5 Transport: WebSocket vs WebRTC vs WebTransport

TCP head-of-line blocking is the fundamental WebSocket weakness: one lost segment stalls everything, and a 300ms retransmit blows the jitter buffer. Fine on stable networks, painful on mobile.

| | WebRTC | WebSocket | WebTransport |
|---|---|---|---|
| Transport | UDP (SRTP/SCTP) | TCP | QUIC/HTTP-3 (UDP) |
| Head-of-line blocking | No | **Yes** | No (across streams) |
| NAT traversal | Built-in (ICE/STUN/TURN) | Server must be reachable | None needed (client->server) |
| Media built-in (jitter, AEC, Opus, PLC) | **Yes** | No (you build it) | No |
| Typical latency | 50-150ms | 50-200ms | comparable, no HOL |
| Complexity | High (SDP/ICE) | Low | Medium |
| Browser support | Universal | Universal | Baseline as of Safari 26.4 (Mar 2026) |

Guidance: **WebSocket** for signaling, PoCs, and direct-to-provider APIs on known networks; **WebRTC** (via LiveKit/Daily) for mobile, corporate firewalls, and anything needing built-in AEC/jitter/loss handling; **WebTransport** as a control-plane upgrade (server->client captions/transcripts/TTS over datagrams), not yet a WebSocket drop-in. If you stay pure-WebSocket, send **binary** frames (not base64-in-JSON), reserve JSON for control, and build explicit backpressure.

### 2.6 Backpressure (the trap that sinks hand-built stacks)

The classic WebSocket API has no receive-side backpressure and only `bufferedAmount` polling on send. The nasty voice case: the server generates 4s of TTS in 600ms, the client plays in real time, so 3.4s piles up - and on barge-in all of it must be flushed. Mitigations: **sentence-level streaming with explicit ACKs** (one ~200-char chunk in flight at a time), **token-bucket grants** (client grants N seconds of audio credit), **bounded queues at every stage**, and client-side `bufferedAmount` throttling (alert ~256KB/connection). `WebSocketStream` gives ergonomic backpressure but is Chrome-only (progressive enhancement).

---

## 3. Speech-to-Text (STT / ASR)

### Open-weight / self-hostable models

- **NVIDIA Parakeet / Canary / Nemotron (FastConformer, NeMo)** - cache-aware streaming, extremely high throughput (~560 concurrent streams/H100 for Nemotron-class; Parakeet TDT RTFx >2000). The top pick for high-concurrency self-hosted streaming.
- **Kyutai STT** - permissively licensed streaming model with semantic VAD; ~400 streams/H100.
- **Whisper family** (OpenAI, MIT) via **faster-whisper / CTranslate2** or **whisper.cpp** - best multilingual coverage; **`faster-whisper` INT8 on ~8 CPU threads transcribes a 5s utterance in ~0.18s**, which is fast enough and **frees the GPU for the LLM**. Distil-Whisper and Whisper Large V3 Turbo are lighter/faster variants.
- **Voxtral**, **Moonshine** - newer lightweight/streaming options.

### Streaming mechanics

Feed ~100ms audio chunks, emit partial hypotheses continuously, finalize on endpointing. Use a "flush" trick to force out the tail of an utterance. Endpointing/turn detection should lean semantic, not fixed-silence.

### Serving frameworks

**NVIDIA Riva / NIM** (production streaming ASR), **Triton Inference Server**, **WhisperLive**, **faster-whisper server**, **speaches**, and the Kyutai Rust server. GPU sizing: a single H100 serves hundreds of concurrent streams for FastConformer-class models.

### Managed alternatives

Deepgram Nova-3, AssemblyAI, Google, Azure, AWS Transcribe - all offer streaming WebSocket APIs with low latency; use when you want zero ops or don't have GPUs. Deepgram STT measured ~337ms finalization in the reference cascade.

### Recommendation

For high-concurrency self-hosted: **NVIDIA cache-aware streaming FastConformer (Parakeet/Nemotron) on Riva/NIM.** Fall back to **faster-whisper (INT8 on CPU)** for MIT-license/multilingual needs and to keep the GPU free for the LLM; **Kyutai STT** for permissive streaming with semantic VAD. (high)

---

## 4. LLM Inference (Open-Weight, Self-Hosted)

**Optimize for TTFT, not benchmark score or raw throughput.** A 200-word reply takes ~10s to speak, so you deliberately keep responses to 2-3 sentences via the system prompt - you rarely need frontier-scale reasoning in the live loop.

### Model selection

Pick a **family** by license and architecture, not a single checkpoint (the leaderboard churns monthly). Licenses matter most (least reversible decision):

| Family | License | Notes |
|---|---|---|
| **Qwen** (Alibaba) | Apache 2.0 (most) | Cleanest option; verify per checkpoint |
| **Mistral / Mixtral** | Apache 2.0 | No-asterisk permissive; EU-friendly |
| **Gemma (2026 gen)** | Apache 2.0 | Now fully permissive; strong native tool-calling |
| **DeepSeek** | MIT / permissive weights | Commercial use + distillation allowed |
| **Llama 4** | Meta Community License | **700M MAU cap + EU restrictions** - avoid for a consumer product |

Prefer **Apache 2.0 / MIT** to avoid user-cap and flow-down obligations.

Size tiers for voice:
- **7-8B dense** (Qwen 3.5 7-8B, Gemma 4 E4B, Mistral Small) - lowest TTFT, cheapest, fits one GPU with huge KV headroom. **Best fit for the live voice loop.** Proven: Qwen2.5-7B on vLLM matched cloud-API latency on a single A10G.
- **~30B dense** (Gemma 4 31B, Qwen 3.5 32B) - better quality, still single-GPU with quantization. Use only if 8B quality is insufficient.
- **70B+ dense** - multi-GPU or aggressive quantization, higher TTFT; usually overkill for short spoken turns.
- **MoE** (DeepSeek V4, Mixtral, GLM) - fast inference (scales with active params) but must hold total params in VRAM.

### Serving engines

Feature surfaces have converged (all do continuous batching, paged attention, prefix caching, FP8 KV cache, OpenAI-compatible streaming); the choice is architectural:

| Engine | Strength | Best when |
|---|---|---|
| **vLLM** | Broadest hardware, easiest deploy, best throughput-per-dollar generalist | **Default.** Model swapping, autoscale, limited DevOps |
| **SGLang** | **RadixAttention** reuses shared prefixes (up to 6.4x on prefix-heavy traffic, ~29% faster than vLLM on 8B chat) | **Chatbots with a fixed shared system prompt** - directly relevant here |
| **TensorRT-LLM** | Lowest per-token latency (20-40% lower at batch=1) | One pinned model, hard latency SLA, NVIDIA-only, can absorb ~28min compile + ops |
| **TGI** | Minimal ops inside HF ecosystem | Already in HF tooling |
| **llama.cpp / Ollama** | Trivial local deploy | Dev/edge only - **not** production multi-user serving |

Because a voice chatbot has a fixed shared system prompt across all users, **SGLang's RadixAttention is directly relevant** (compute the persona/instructions prefix once, reuse it, cut TTFT). vLLM is the safe default.

### Streaming into TTS (the biggest latency lever)

Cascaded streaming pipeline with the **sentence-boundary trick**: LLM emits tokens over SSE/WebSocket -> a sentence aggregator buffers until a boundary (`.`/`!`/`?`/clause) -> each complete sentence is flushed to TTS **immediately** while the LLM keeps generating. Cuts perceived response time 60-80% for multi-sentence replies. Pipecat/LiveKit manage this plus barge-in.

### GPU sizing

VRAM = static weights + dynamic KV cache.

| Precision | Bytes/param | 8B | 70B |
|---|---|---|---|
| FP16/BF16 | 2 | 16GB | 140GB |
| **FP8** | 1 | 8GB | 70GB |
| **INT4 (AWQ/GPTQ)** | 0.5 | 4GB | 35GB |

KV cache scales linearly with context length and concurrent requests; GQA + FP8/INT4 KV cache serve ~10x more concurrent requests than 2022-era stacks. Concrete concurrency:
- **Llama-8B on one H100 80GB, 4K context:** ~124 concurrent (FP16 weights), **~248 with FP8 KV cache.** Voice replies are short, so an 8B model easily serves **100-250 live voice conversations per H100.**
- **70B at 4K:** ~10 (FP16, 2 GPUs) up to ~40 (INT4 + FP8 KV).
- Production sweet spot for high concurrency: **INT4 weights + FP8 KV cache**; `gpu-memory-utilization` 0.85-0.90.
- Prefer a model that **fits one GPU** to avoid tensor-parallelism latency; use TP only to fit a model too big for one card (keep within an NVLink node).

### Session/context handling

LLM servers are stateless - the app owns history and resends `[system prompt] + [history] + [new turn]` each turn (store in Redis keyed by session ID). Keep **one stable system prompt** (persona + "reply in 2-3 conversational sentences, no bullet lists") so prefix caching reuses it. **Route by session ID** so a user's follow-up turns hit the pod holding their KV cache. Cap history (sliding window / summarize) to keep KV small; long-context models are unnecessary here.

### Recommendation

**8B-class Apache-2.0 model (Qwen 3.5 or Gemma 4), FP8 (or AWQ/INT4 on older cards) + FP8 KV cache, served by SGLang (or vLLM), prefix caching on, session-aware routing, streaming token-by-token into TTS.** One H100 serves ~150-250 concurrent 4K voice sessions; economics land around $0.5M-$1.5/M tokens. (high)

---

## 5. Text-to-Speech (TTS)

### Open-weight / self-hostable models

- **Orpheus 3B** (Apache 2.0) - LLM-backbone, servable on vLLM with continuous batching, sub-200ms TTFA. Top self-host pick.
- **Qwen3-TTS** (Apache 2.0) - autoregressive/batchable, sub-200ms TTFA. Co-top pick.
- **Kokoro-82M** - runs real-time even on CPU (~0.5GB); cheap English fallback tier.
- **CosyVoice** - ~150ms bi-streaming.
- Others: Sesame CSM, Chatterbox, VoXtream2, Piper (fast CPU), XTTS/Coqui, StyleTTS2, Fish Speech, Parler-TTS.

### Streaming synthesis

Clause-chunk the incoming LLM tokens, synthesize the first clause immediately to minimize time-to-first-audio, and **stream raw PCM (24kHz) over the WebSocket**, scheduled via the Web Audio API (not `decodeAudioData`). Use Opus for mobile; avoid MP3. Modern TTS is only ~10-20% of the conversational budget - optimize LLM TTFT and STT first.

### Scaling

Serve LLM-backbone models (Orpheus/Qwen3-TTS) on **vLLM with FP8 + continuous batching**; budget **~16-25 concurrent real-time streams per H100** for Orpheus-class. Replicate Kokoro behind a load balancer for cheap overflow. A common pattern colocates several small TTS models on a MIG slice with GPU hot-swap (one model resident, ~60s idle eviction).

### Managed alternatives

Cartesia (leads on latency/consistency and cost-per-char), ElevenLabs (most expressive, concurrency-capped), Deepgram Aura, PlayHT, Azure, Google, AWS Polly (cheapest at scale). Note vendor latency claims are inference-only; real-world P50 is 2-4x higher.

### Recommendation

**Orpheus 3B or Qwen3-TTS (both Apache 2.0) on vLLM**, with **Kokoro-82M as a cheap CPU/English fallback tier**, streaming PCM over the WebSocket. (high)

---

## 6. Cloud Infrastructure, Orchestration & Scaling

### 6.1 WebSocket connections at scale

WebSockets are long-lived and stateful - you scale open connections, not requests/sec.
- **Every frame in a session must reach the same backend.** Round-robin breaks WebSockets. Use cookie-based stickiness (or session store); avoid NGINX `ip_hash` (thousands behind one corporate NAT all hash to one backend).
- **Envoy** with `upgrade_configs`, `LEAST_REQUEST` (connection durations vary wildly), `circuit_breakers` for per-cluster `max_connections`, cookie/ring-hash stickiness. Or **L4 (NLB / NGINX `stream`) with `least_conn`** for the simplest robust option.
- **Decouple socket ownership from conversation ownership:** thin **stateless connection gateway** terminates the socket and forwards to a **session actor** (addressed via Redis/consistent hashing) that owns the conversation - so a reconnect can reattach to the live session.
- Heartbeats (ping/pong ~30s, shorter than the tightest proxy idle timeout); client reconnect with exponential backoff + jitter; **connection draining** on deploy so restarts don't drop live calls. Track concurrent connections/node and reconnect rate/min as autoscaling signals.
- Redis pub/sub for cross-node fan-out and shared connection state (handles ~100K concurrent connections across a few servers); Kafka/NATS/Redis Streams for durable async work and KEDA queue-depth triggers.

### 6.2 Kubernetes + GPU

- **NVIDIA GPU Operator** (device plugin, GPU Feature Discovery for VRAM/product labels -> node affinity, DCGM Exporter for metrics, MIG partitioning, time-slicing).
- **MIG** carves an H100/A100 into isolated slices - ideal for co-locating small STT/TTS models. **Time-slicing** oversubscribes for bursty low-utilization services. (DRA is not yet Karpenter/EKS-Auto-Mode compatible - stick to the device plugin there.)
- Separate **tainted GPU node pools** per SKU (H100 for LLM; L40S/L4 for STT/TTS) from CPU pools (gateway, orchestration, STT-on-CPU).
- **Karpenter** (spot-first) or Cluster Autoscaler for node provisioning. **Cold start is the real GPU pain point** - pre-warmed AMIs with drivers baked in, NVMe/PVC model caching, P2P image distribution (Dragonfly), snapshot/CRIU restore (cuts vLLM cold start ~70-88%). A 7B reload is 30-60s; 70B is minutes.

### 6.3 Pod autoscaling

| Scaler | Scales on | Scale-to-zero | Best for |
|---|---|---|---|
| **HPA** | CPU/mem | No | Baseline, not GPU-aware |
| **KEDA** | any metric (Prometheus, queue depth, GPU memory %, cron) | Yes | Queue-driven pipelines, GPU-metric scaling |
| **Knative** | HTTP concurrency/RPS | Yes | User-facing HTTP inference |
| **Ray Serve** | Ray task queue | Partial | Multi-model / multi-node pipelines |

- **Autoscale on inference-specific metrics, not CPU/mem.** Use **KEDA + Prometheus** on vLLM's `num_requests_waiting` (queue depth) and `gpu_cache_usage_perc` (KV utilization); scale GPU memory % via a per-node NVML DaemonSet + ExternalScaler.
- **Scale-to-zero is a trap for latency-critical voice** - the first user eats the cold start. Keep a **warm minimum** of LLM/TTS replicas always on; use scale-to-zero only for off-hours batch/side services (cron).
- Continuous batching means one replica absorbs high concurrency before you add a second; the signal it's full is its own queue building.
- Prefix caching is per-replica, so use **prefix-aware / session-ID routing** at scale-out (route multi-turn conversations to the same pod's KV cache). The open-source **vLLM Production Stack** (Helm: serving engines + prefix-aware router + Prometheus/Grafana + LMCache) is the reference K8s pattern.

### 6.4 GPU capacity split (asymmetric placement)

- **LLM = the GPU hog** - dedicated high-VRAM GPUs (H100/H200), vLLM, always-on warm floor. This is where the money goes.
- **STT = push to CPU** - faster-whisper INT8 frees the GPU and avoids KV-cache thrash (GPU only for ultra-low-latency streaming like Parakeet TDT, pinned to a different GPU than vLLM).
- **TTS = small dedicated pool or MIG slice** - Kokoro on CPU, Orpheus-3B on L40S/L4/MIG with hot-swap.

### 6.5 2026 GPU pricing (on-demand $/GPU-hr - verify live, prices move daily)

| GPU (VRAM) | Hyperscaler | Neocloud (RunPod/Lambda/Spheron) | Spot floor |
|---|---|---|---|
| **L4 (24GB)** | $0.71-0.80 | ~$0.39 | ~$0.21 |
| **L40S (48GB)** | ~$1.86-7.5 | $0.47-0.99 | ~$0.40-0.47 |
| **A100 80GB** | $3.0-5.0 | $1.07-2.50 | ~$0.60 |
| **H100 SXM 80GB** | $6.88-12.29 | $2.00-4.19 | ~$1.03-1.73 |
| **H200 (141GB)** | ~$10-13.78 | $3.31-4.54 | ~$1.40 |

Hyperscalers run **75-86% more expensive** than neoclouds for the same silicon. Illustrative cost: an 8B model on one H100 (~$2.50/hr neocloud) serving ~150 concurrent conversations is roughly **$0.017/conversation-hour** of dedicated GPU (real per-active-user cost is lower since turns are bursty).

Cost strategy: **spot-first for stateless/retryable work** (batch, STT/TTS workers, canary; 60-90% savings), a **reserved/on-demand floor for the interactive LLM** so barge-in never waits on a preemption. At low/spiky utilization, per-token managed APIs (Together/Fireworks) can beat idle self-hosted GPUs - do the math on your utilization curve. Track spend with OpenCost.

### 6.6 Managed GPU platforms (build-vs-buy shortcut)

| Platform | Model | Cold start |
|---|---|---|
| **Modal** | Python-decorator serverless, true scale-to-zero, snapshots | 2-4s |
| **RunPod Serverless** | container + handler, FlashBoot | sub-250ms on cache hit, else 8-30s |
| **Baseten** | Truss model serving | 16-60s |
| **Cerebrium / Beam / fal** | Python-native serverless | 2-4s |
| **Together / Fireworks** | managed API, per-token billing | n/a |
| **AWS/GCP/Azure GPU** | raw instances | n/a |

Serverless wins for bursty/spiky and for STT/TTS side services; always-on self-managed/reserved wins for latency-critical, high-utilization voice at scale.

### 6.7 Serving frameworks on K8s

**vLLM** is the de-facto OSS LLM server (~30+ concurrent voice sessions/H100 on Llama-3.1-8B, ~6,200 output tok/s, KV cache the limiter). **Ray Serve + vLLM** for multi-node/multi-model; **KServe** (CNCF Incubating) for Kubernetes-native serving with built-in canary; **llm-d** for disaggregated prefill/decode at large scale.

---

## 7. Cross-Cutting Concerns

- **AuthN/AuthZ:** authenticate the WebSocket/WebRTC handshake with a short-lived JWT minted server-side after login (never a long-lived secret in the browser); validate at the edge before upgrading. **mTLS between services** via a service mesh (Istio/Linkerd/Envoy) - keep the mesh off the hot audio path, use it for the control/RPC plane. RBAC + MFA for all admin access to recordings/transcripts/logs.
- **Rate limiting & quotas:** enforce at the gateway (connections/user, concurrent sessions, minutes/day) and the LLM tier (tokens/min, requests/min) with Redis-backed token buckets keyed by user/tenant; Envoy circuit breakers protect backends.
- **Multi-tenancy:** namespace-per-tenant for logical isolation; node pools / MIG for hard GPU isolation; never share KV cache or conversation context across tenants.
- **Observability:** standardize on **OpenTelemetry GenAI semantic conventions** (`gen_ai.*`). The voice SLIs that matter: **time-to-first-token / time-to-first-audio**, inter-token latency, end-to-end round-trip, P99 per model/op, error rate by type, token cost, KV-cache hit rate. GPU metrics via **DCGM Exporter** -> Prometheus (also the KEDA signal); scrape vLLM `/metrics`. Backend: kube-prometheus-stack (Prometheus + Grafana) + Tempo/Jaeger. **Redact prompt/completion content at the collector edge.**
- **Error handling / fallbacks:** per-stage failover (saturated self-hosted LLM -> hosted API; primary TTS timeout -> lightweight Kokoro); graceful barge-in cancellation; circuit breakers + retries with jitter; connection draining on deploy.

---

## 8. Data Privacy, Security & Compliance

Voice is personal data; the moment a model identifies a speaker by voice it becomes **biometric data**. There is no "compliant model," only compliant deployments.

- **Encryption:** TLS 1.3 in transit for the whole chain (client -> gateway -> STT -> LLM -> TTS -> storage); AES-256 at rest for recordings/transcripts/inference logs. Prefer private networks over the public internet for sensitive audio.
- **GDPR / EU AI Act:** lawful basis for any voice processing; **explicit, specific consent for voiceprints/biometric ID** (a generic "by continuing you consent to recording" does not cover voiceprint creation). As of **Aug 2, 2026, AI emotion inference in workplace/education contexts is prohibited**; DPIAs required for biometric/high-risk processing.
- **HIPAA (if health-adjacent):** signed BAA with every third party touching PHI; **self-hosting open-weight models eliminates model-provider BAAs but puts the entire Security Rule burden on you** - if your gateway logs prompts in plaintext, you built the leak.
- **Controls checklist:** RBAC + MFA; immutable audit trails for prompts/outputs/consent; real-time PII/PHI redaction before storage; configurable data residency and retention/auto-deletion; caller-identity verification; DPAs with all sub-processors.
- **Self-hosting advantage:** keeping STT/LLM/TTS on your own VPC-isolated infra means voice + biometric data never crosses to external providers or jurisdictions - the strongest sovereignty posture, at the cost of owning all controls yourself.

(safety) The compliance material above is general infrastructure guidance, not legal advice; biometric/voiceprint and emotion-inference rules changed materially in 2026, so validate against counsel for your jurisdiction.

---

## 9. CI/CD, Model Deployment & Canary Rollouts

- **GitOps with ArgoCD** (infra via Terraform, platform components in waves) - reproducible and PR-reviewable.
- **Model serving + versioning:** **KServe** (CNCF Incubating) is the K8s-native standard (`InferenceService` / `LLMInferenceService` CRDs). `RawDeployment` mode is preferable to Knative for most production serving; set explicit node affinity for GPU models.
- **Canary rollouts:** deploy the canary at **`weight: 1`, not `0`** (a zero-weight dark deploy leaves the backend unwarmed and causes transient failures on ramp); promote via **Argo Rollouts** with `setWeight` steps (10 -> 25 -> 50 -> 75 -> 100), `pause` + **Prometheus analysis templates** (latency, error rate) for auto-rollback. **Shadow deployment** (mirror traffic, log-only, 48-72h) for high-stakes swaps.
- **Voice-specific gate:** canary analysis must include **TTFA/TTFT and interruption-handling**, not just error rate - a model that is "correct" but 300ms slower ruins the conversation.

---

## 10. Bottom-Line Recommendation

**Hybrid, not purist.**

- **Transport/framework:** LiveKit Agents (WebRTC + scaling + sub-75ms semantic turn detection) or Pipecat (full control). WebSocket for signaling/fallback. Do not hand-roll the frame graph.
- **Client:** if hand-building, AudioWorklet capture -> downsample to 16kHz mono -> Int16 -> 20ms frames -> WebCodecs Opus over the internet (PCM on private links); Silero VAD in the worklet; jitter-buffered AudioWorklet ring player; client-first barge-in; `echoCancellation` on.
- **STT:** faster-whisper INT8 on CPU (frees the GPU) as default; Parakeet/Nemotron on Riva/NIM for GPU streaming at scale.
- **LLM:** 8B-class Apache-2.0 model (Qwen 3.5 / Gemma 4), FP8 + FP8 KV cache, served by SGLang or vLLM with prefix caching + session-ID routing, streaming tokens into a sentence aggregator. Dedicated H100 pool, always warm. ~150-250 concurrent voice sessions/H100.
- **TTS:** Orpheus 3B / Qwen3-TTS on vLLM + Kokoro-82M fallback, streaming PCM back to the browser.
- **Infra:** Kubernetes + NVIDIA GPU Operator, Karpenter (spot-first nodes) + KEDA (queue-depth + GPU-memory scaling), vLLM Production Stack with prefix-aware routing, KServe + Argo Rollouts for canary. Keep interactive tiers warm; scale-to-zero only off-hours.
- **Hosting:** neocloud H100 (~$2-4/hr) or L40S (~$0.5-0.9/hr), 75-86% cheaper than hyperscalers; reserved floor for the LLM, spot for batch.
- **Cross-cutting:** JWT-authenticated handshake, mesh mTLS, Redis rate limits, OpenTelemetry GenAI observability with edge redaction, TLS 1.3 + AES-256, explicit biometric consent, VPC isolation.

**Path to production:** start on a managed serverless GPU platform (Modal/RunPod) or per-token API (Together/Fireworks) to validate the product, then migrate the LLM to self-hosted K8s once utilization is steady - which happens quickly for a many-concurrent-user voice product, because neocloud/reserved GPUs are dramatically cheaper than per-token pricing at scale.

**The one thing not to compromise on: stream every stage and keep the LLM/TTS warm.** That is the difference between a natural conversation and a hung-up call.

*2026-08-01 15:17 - Opus 4.8*
