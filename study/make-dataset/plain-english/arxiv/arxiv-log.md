# arXiv Blur-to-Original Dataset - Build Log

Training data for a prompt-compression study: each pair teaches a model to recover a sharp original from a blurred paraphrase, but only where the blur provably dropped nothing.

## Source and method

- Source: arXiv abstracts across cs, math, physics, q-bio, econ, and stat categories, pulled from the arXiv Atom API sorted by most recent submission. Abstracts are dense and meaning-complete, which makes them good sharp originals.
- Category pool: cs.CL, cs.LG, math.NA, math.PR, q-bio.NC, econ.EM, stat.ME, physics.optics, astro-ph.GA, cond-mat.soft. This run reached the 100-passage target within the first six categories (cs.CL, cs.LG, math.NA, math.PR, q-bio.NC, econ.EM), so the later categories did not contribute passages in this run.
- Blur: each original was blurred over 3 passes with blur-gen, producing softened paraphrases that trade precise wording for looser phrasing.
- Kept pairs: (blurred -> original) pairs where the directional gate gate1(original, blurred) returned PASS, meaning the blurred text still entails the original and the blur dropped nothing. Pairs where gate1 returned FAIL (the blur lost or altered meaning) were discarded.

## Counts

- Passages fetched: 100
- Blur records: 300 (100 passages x 3 passes)
- Gate control records: 300 (one directional gate1 check per blur record)

## Gate result

- Gate PASS rate (kept / total): 137 / 300 = 45.7 percent (the finalize step floors this to 45 percent)
- Gate FAIL: 163 / 300
- Kept pairs: 137

## Length stats

- Blur-expansion (original -> blurred, mean word ratio): 1.03x, so the blurred input runs about 3 percent longer than the original on average
- Median input (blurred) words: 182
- Median target (original) words: 180

## Sample kept pairs (blurred input -> original target)

- Pair 1 - arxiv-p1-12 (blurred 134 words -> original 229 words)
  - input (blurred): "In Greek mythology, Hermes defeated Argus Panoptes, a giant with countless eyes, by disguising himself as a shepherd and systematically closing the creature's eyes through deception and interference..."
  - target (original): "What did it take for Hermes, the devout messenger of the Olympian gods, to slay Argus Panoptes, the multi-eyed giant of Greek myth? As the perfect guardian, Panoptes' legion of ever-watchful eyes prov..."
- Pair 2 - arxiv-p3-20 (blurred 161 words -> original 160 words)
  - input (blurred): "The Deep Galerkin Method (DGM) and Physics-Informed Neural Networks (PINNs) have emerged as increasingly important tools in scientific machine learning for solving partial differential equations (PDEs..."
  - target (original): "The Deep Galerkin Method (DGM) and Physics Informed Neural Networks (PINNs) have become widely-used methods for solving partial differential equations (PDEs) in the rapidly growing field of scientific..."
- Pair 3 - arxiv-p1-24 (blurred 176 words -> original 248 words)
  - input (blurred): "Large-scale Bayesian nonparametric (BNP) learning methods, including Stochastic Variational Inference (SVI), efficiently process datasets with numerous classes and large sample sizes. Like SVI, these..."
  - target (original): "Large scale Bayesian nonparametrics (BNP) learner such as Stochastic Variational Inference (SVI) can handle datasets with large class number and large training size at fractional cost. Like its predec..."

## Sample gate-FAIL drops (meaning loss the gate rejected)

- arxiv-p1-0: "Blinded evaluation by board-certified radiologists" (A) becomes "Independent assessment by certified radiologists" (B) - dropping the specific "blinded" methodology and weakening "board-certified" to "certified," which would change any answer that reports the study's evaluation protocol or reviewer credentials.
- arxiv-p2-4: A claims Kimi K3 "achieves frontier-level performance," while B downgrades this to "competitive results" - a materially weaker performance claim (with "perfectly balanced" also softened to "balanced" and "persistent" to "stable").
- arxiv-p3-8: Prompt B adds a new quantitative claim - "nearly three times larger" - comparing ELMOD's 2.7B to the 7B models, which is absent in A; a model asked about the size ratio would answer from B but not from A.

*Generated 2026-07-27*
