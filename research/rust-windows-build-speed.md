---
produced: 2026-09-17
title: Faster Rust compile link test cycles on Windows 11 MSVC for large Cargo workspaces (rust-lld, Defender exclusions, WSL2, Dev Drive, debuginfo)
---

# Rust Windows build performance research

Context: 46-crate Cargo workspace, heavy native deps (mlua vendored Lua, candle, tokenizers/onig, turso), Windows 11, 192 cores, 1TB RAM, NVMe. Baseline: MSVC toolchain, link.exe, crt-static, no sccache, no custom linker.

## 1. rust-lld on x86_64-pc-windows-msvc (2026 status)

- Still opt-in, not default. Metabug: https://github.com/rust-lang/rust/issues/71520 (active through 2026; Anki, Firezone, openjd-rs all switched CI to rust-lld in 2025-2026).
- Enable via `.cargo/config.toml`: `[target.x86_64-pc-windows-msvc] linker = "rust-lld"` or RUSTFLAGS `-Clinker=rust-lld`. `-Clinker-features=+lld` is NOT stable for the MSVC target (Linux only) per https://harnlang.com/dev/windows-ci-experiments.html and the unstable book.
- Measured: flow PR https://github.com/andrewdavidmackenzie/flow/pull/2908 - CI build 23m baseline, 18.4m with Defender exclusion + rust-lld (-20%). Harn page cites ~2x full-build and ~5x incremental-link wins swapping link.exe for LLD.
- LLD links production Chromium/Firefox on Windows: https://llvm.googlesource.com/llvm-project/+/992210aa3c8f76d71996172597ca902dadff2a36/lld/docs/windows_support.rst
- Known issues:
  - No /DEBUG:FASTLINK support (lld docs).
  - Crates spawning separate cargo invocations may ignore config `linker=`; use RUSTFLAGS `-Clinker=lld-link` instead (rustc book, linker-plugin-lto page).
  - C deps must be compiled with cl or clang-cl, never GNU-syntax clang: clang emits no MSVC linker directives, missing oldnames/libcmt/msvcrt at link time: https://github.com/rust-lang/cc-rs/pull/811 and https://github.com/corrosion-rs/corrosion/issues/395. cc-rs derives /MT vs /MD from CARGO_CFG_TARGET_FEATURE, so crt-static is compatible (RFC 1721).
  - embed-resource is not a linker problem; on msvc it uses llvm-rc by default, override via RC_$TARGET / RC env vars: https://docs.rs/embed-resource/latest/embed_resource/

## 2. Defender / antivirus exclusions

- Add-MpPreference -ExclusionPath for target/ and %USERPROFILE%\.cargo: https://learn.microsoft.com/en-us/powershell/module/defender/add-mppreference
- Measured: clean cargo test 3m17s -> 1m22s (https://swatinem.de/blog/windows-security/); -8% CI build (flow PR above); full rebuild 143s -> 92s, incremental 4.6s -> 2.8s, plus rustup proxy overhead in .cargo\bin (https://github.com/rust-lang/cargo/issues/5028). Consider ExclusionProcess for rustc.exe/cargo.exe and putting the toolchain bin dir ahead of .cargo\bin in PATH.

## 3. Process spawn / WSL2

- Measured hyperfine benchmark, same machine: cargo build 52.9s native Win11 (Dev Drive) vs 30.8s WSL2; release 136.4s vs 76.9s; cargo check 31.1s vs 19.1s: https://www.reddit.com/r/rust/comments/1gef1of/
- Critical caveat: sources must live on the WSL ext4 filesystem. Building from /mnt/c (NTFS via 9P) is ~4x slower: https://markentier.tech/posts/2022/01/speedy-rust-builds-under-wsl2/
- Per-crate rustc itself is slower on Windows MSVC than Linux even with equal hardware: https://github.com/rust-lang/rust/issues/66192
- WSL2 produces Linux binaries; useless if the deliverable is a Windows MSVC artifact. Cross-check value only.

## 4. Other Windows-specific wins

- Dev Drive (ReFS): Microsoft claims 20-30% build speedup; move CARGO_HOME, target/, sources: https://corrode.dev/blog/tips-for-faster-rust-compile-times/ (note: reddit benchmark above shows Dev Drive still loses badly to WSL2).
- split-debuginfo: "unpacked" is NOT supported on Windows; only "packed" (PDB): https://doc.rust-lang.org/nightly/nightly-rustc/rustc_target/spec/enum.SplitDebuginfo.html
- debug="line-tables-only": mixed evidence. Harn measured it REGRESSED Windows compile time (warm 6:21 -> 9:47+): https://harnlang.com/dev/windows-ci-experiments.html. Benchmark before adopting.
- debug=0 / strip="debuginfo": speeds linking, shrinks target/ (corrode blog). On Windows test both.
- RAM disk for target/: no credible measured benchmark found. UNVERIFIED. With 1TB RAM it is feasible; risk is data loss on crash and no proven win over fast NVMe + Dev Drive.
- cargo-nextest for faster test execution; separate rust-analyzer targetDir to avoid lock contention (corrode blog, rust-pc.github.io guide).
- Cranelift backend (nightly, -Zcodegen-backend=cranelift) reported to cut a debug build to 3m23s in one forum report: https://users.rust-lang.org/t/slow-compile-times-on-windows/119144 - UNVERIFIED for candle/onig/mlua compatibility.
