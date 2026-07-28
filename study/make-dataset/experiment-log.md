# Pairgen Experiment Log

Append-only record of the experiment battery. Each experiment tests one variable in the sharpen-strip-gate pipeline to find the configuration that maximizes training-pair yield while preserving Gate 1 (execution-equivalence) discrimination. This file is the reload point: a fresh session reads it to see which experiments are done and resumes from the first incomplete one.

Baseline from the prior validation run (`pairgen-validation.md`): 20 bloated inputs, Gate 1 PASS 13/20, Gate 2 PASS 2/13, kept 2/20 (10%). Gate 1 caught 5/5 negative controls. The two kept pairs were the smallest inputs (57w, 71w).

Each entry uses this format:

- **Hypothesis**: one sentence
- **Started** / **Completed**: ISO timestamps
- **Inputs**: count and source
- **Configuration**: model, effort, gate2 mode
- **Results**: gate1 pass X/N, gate2 pass Y/Z, kept K/N
- **Compression**: median input words to output words
- **Key finding**: one sentence
- **Commit**: hash

---

## E0: Initialize experiment infrastructure

- **Started**: 2026-07-27
- **Actions**: Built and tested pairgen (4/4 unit tests pass), verified ANTHROPIC_API_KEY present, created `experiments/` scratch dirs, added experiment output patterns to `.gitignore`, initialized this log.
- **Configuration**: pairgen defaults model=claude-opus-4-8, effort=high, gate2=strict.
- **Key finding**: infrastructure ready; baseline is 10% yield under strict both-gates.
- **Completed**: 2026-07-27

---
