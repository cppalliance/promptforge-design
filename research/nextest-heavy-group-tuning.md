---
produced: 2026-09-17
title: cargo-nextest heavy-group tuning for ML/FFI test suites on high core-count machines
---

# Nextest heavy-group tuning research

Context: workspace with `heavy = { max-threads = 2 }` applied to an ML tool-picker (candle, tokenizers), an STT crate, and a whisper.cpp FFI backend. Machine: 192 cores, 1TB RAM.

## Recommendation: max-threads = 8 (up to 16) plus threads-required = 4

- max-threads is a logical semaphore around tests in the group only; ungrouped tests still run under the global test-threads limit (default num-cpus). threads-required weights each test against both the group and global limits. The nextest docs' recommended pattern for heavy suites is exactly this combination. Groups are not globally exclusive (nextest#2310, discussion #2054): heavy tests can overlap light tests.
- Failure modes at higher parallelism: thread oversubscription (N tests x M internal threads exceeding core count, causing rayon/ggml scheduling contention), fixture races over shared model files or temp dirs, port collisions if tests bind sockets. Detection: flaky timeouts, EAGAIN thread-spawn failures, nondeterministic transcription output. The patchbay project documents this failure class.
- Public examples are sparse: n0-computer/patchbay uses test-threads = 8 globally and a serial-heavy group at max-threads = 1 (network-namespace tests on 2-vCPU CI, not ML). Nextest docs use 4 and 8 as illustrative caps.
- Internal threading: whisper.cpp n_threads defaults to min(4, hardware_concurrency) per whisper_full call; candle CPU ops run on a rayon pool sized to CANDLE_NUM_THREADS / RAYON_NUM_THREADS / all cores. A single candle test can try to use all cores.
- Suggested: heavy = { max-threads = 8 } with threads-required = 4 on the overrides; 8 x ~4-8 internal threads = 32-64 busy cores, leaving headroom for the other global slots. Optionally set CANDLE_NUM_THREADS=8 in the test environment to bound candle's pool. Bump toward 16 if clean.

Sources: nexte.st/docs/configuration/test-groups/, nexte.st/docs/configuration/threads-required/, nexte.st/docs/configuration/reference/, github.com/nextest-rs/nextest/issues/2310, github.com/ggml-org/whisper.cpp/issues/3194, docs.rs/crate/candle-core/latest/source/src/utils.rs, github.com/huggingface/candle/issues/3134, github.com/n0-computer/patchbay/blob/main/.config/nextest.toml
