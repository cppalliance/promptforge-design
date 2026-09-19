---
produced: 2026-09-17
title: Eliminating duplicate full-graph compilation passes in a Cargo verify pipeline (46-crate workspace, high core count)
---

# Cargo verify-pipeline dedup research

Context: 46-crate workspace; verification ran cargo check, two clippy partitions, fmt, doc, nextest partitions, mdbook, deny. Heavy native deps: mlua (vendored Lua), candle, tokenizers (onig).

1. Drop `cargo check`; run clippy as the check. Clippy deliberately does not share artifacts with check (separate fingerprints since rust-clippy#6687); cross-mode rmeta reuse is an open design problem (cargo#3501, WIP cargo#15627, 2026 goal "Incremental Systems Rethought"). Clippy is a superset of check. Sources: github.com/rust-lang/cargo/issues/3501, github.com/rust-lang/rust-clippy/pull/6687, goals.rust-lang.org/2026/incremental-system-rethought.html
2. Merge clippy partitions run on one machine; separate feature/target sets force re-fingerprinting per partition. Keep features and RUSTFLAGS identical across steps. Source: github.com/spiceai/spiceai/pull/11679
3. `cargo doc` already reuses check-mode rmeta for dependencies (deps emit Check rmeta only; proc-macros still fully built). Use --no-deps. Nightly -Zrustdoc-depinfo (cargo#17020) fixes spurious doc rebuilds. Sources: github.com/rust-lang/cargo/pull/4976, github.com/rust-lang/cargo/issues/15370
4. Nextest: build once, partition via `cargo nextest archive` + `--archive-file` + `--partition slice:m/n`; zero rebuilds across partitions. Tune -j/--test-threads separately from --build-jobs. Sources: nexte.st/docs/ci-features/archiving/, nexte.st/docs/ci-features/partitioning/
5. cargo-hakari workspace-hack: 1.7x cumulative on Omicron (717s -> 418s), 20-25% on Diem/guppy; check benefits most. Sources: github.com/guppy-rs/hakari-on-omicron-perf, docs.rs/cargo-hakari
6. Profile tuning (stable): codegen-units = 256 is dev default; debug = "line-tables-only" cuts debuginfo cost; [profile.dev.package."*"] opt-level = 1 keeps cross-crate generic sharing (2/3 disables it). Source: doc.rust-lang.org/cargo/reference/profiles.html
7. Linker and cache: mold 3-5x over lld, 10-20x over GNU ld (Linux); sccache remote backend gives 70%+ hit rates in CI with CARGO_INCREMENTAL=0; sccache cannot cache bins/proc-macros/links; RUSTFLAGS changes invalidate sccache keys. Sources: kunalganglani.com/blog/reduce-rust-compile-time, microsoft.github.io/RustTraining
8. -Zshare-generics: nightly-only, mixed results (Zed incremental 12.4s -> 10.4s in one PR; default-enable attempt regressed). Not recommended on stable. Sources: github.com/rust-lang/rust/pull/138522, github.com/rust-lang/rust/pull/123610
9. Pipelining is on by default since 1.38 (10-20% on clean parallel builds). On high core counts, read `cargo build --timings` for serializing crates; C deps build single-threaded per crate.

Biggest wins ordered: 1+2 (delete a full pass), 4 (delete N-1 test builds), 5, 7.
