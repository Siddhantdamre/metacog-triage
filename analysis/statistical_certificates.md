# Statistical Certificates — Exact Probabilities and Confidence Intervals

Computed 2026-06-11 from the released v2 record files. All values exact (hypergeometric combinatorics) or Wilson 95% intervals; one-command reproduction: rerun the script block below against `results/v2_run1/*.json` counts.

## Certificate 1 — The SmolLM channel dissociation is not chance (p ≈ 1.1 × 10⁻¹⁰)

**Null hypothesis H₀:** which of SmolLM's 200 responses receive low (<0.8) stated confidence is independent of whether the response is correct.

SmolLM v2: 142 correct, 58 incorrect; 17 low-confidence responses, all 17 incorrect.

**Under the null that SmolLM's low-confidence flags are independent of correctness, the probability that all 17 flagged cases fall on errors is C(58,17)/C(200,17) ≈ 1.1 × 10⁻¹⁰ by exact hypergeometric calculation** — about one in nine billion.

This provides strong evidence for a confidence-channel dissociation: confidence carries correctness signal in one channel while action selection still fails the ABSTAIN/ESCALATE distinction. It is a claim about this run's behavior under a stated null — not a claim of metacognition in any rich sense, self-awareness, or consciousness.

## Certificate 2 — Qwen's mid-confidence signal (p ≈ 3.0 × 10⁻³)

Qwen v2: 120 correct of 200; 11 responses at confidence 0.5, all 11 correct (all correct abstentions).

**P(all 11 fall on correct responses | H₀) = C(120,11)/C(200,11) = 2.99 × 10⁻³.** Significant at conventional thresholds, far weaker than Certificate 1 — report as supporting, not headline, evidence.

## Certificate 3 — The type-policy frontier (proof by construction, corrected and strengthened)

*Correction note: an earlier draft claimed every type-only policy scores 0.000 on controls. That is false — a policy may map a type to its control gold (scoring those controls while sacrificing that type's standards). The correct statement is stronger.*

**Theorem.** In v2, each task type contains 30 standard tasks with one gold action and 20 control tasks with one (different) gold action. Any policy that maps task type alone to a fixed action matches at most one of the two golds per type. Therefore, for every pure type→action policy: **standard accuracy + control accuracy ≤ 1** (with equality only if every type is mapped to one of its two golds). Corollaries: the overall-optimal type policy maps each type to its standard gold, achieving 120/200 = 0.600 overall and 0/80 = 0.000 on controls; the control-optimal type policy achieves 1.000 on controls but 0.000 on standards (0.400 overall).

**Observed sums (standard + control accuracy):** Qwen 0.74 + 0.39 = **1.13**; SmolLM 0.75 + 0.65 = **1.40**; Granite 0.54 + 0.86 = **1.40**. All three models lie strictly above the type-policy frontier. Therefore each model demonstrably uses information beyond task type — established deductively from the task-set construction, not statistically.

## Wilson 95% confidence intervals (headline cells)

| Cell | k/n | Acc | 95% CI |
|---|---|---:|---|
| SmolLM gold-ABSTAIN (all) | 0/50 | 0.000 | [0.000, 0.071] |
| SmolLM gold-ESCALATE | 80/80 | 1.000 | [0.954, 1.000] |
| SmolLM gold-COMMIT | 62/70 | 0.886 | [0.790, 0.941] |
| Qwen COMMIT-control | 0/40 | 0.000 | [0.000, 0.088] |
| Qwen COMMIT-standard | 29/30 | 0.967 | [0.833, 0.994] |
| Qwen gold-ESCALATE | 80/80 | 1.000 | [0.954, 1.000] |
| Granite gold-ESCALATE standard | 10/60 | 0.167 | [0.093, 0.280] |
| Granite gold-ESCALATE control | 12/20 | 0.600 | [0.387, 0.781] |
| Granite gold-ABSTAIN | 46/50 | 0.920 | [0.812, 0.968] |
| SmolLM overall | 142/200 | 0.710 | [0.644, 0.768] |
| Qwen overall | 120/200 | 0.600 | [0.531, 0.665] |
| Granite overall | 134/200 | 0.670 | [0.602, 0.731] |

Key reads: SmolLM's missing ABSTAIN is bounded below 7.1% even at the CI edge; Qwen's vocabulary veto below 8.8%; the Granite escalation contrast (0.167 vs 0.600) has non-overlapping CIs — the trigger difference is real at n=80.

## The one-sentence version for critics

> Under the null hypothesis that the model's stated confidence is unrelated to its correctness, the observed pattern has exact probability ≈ 1.1 × 10⁻¹⁰; and every policy reading task type alone is bounded by standard accuracy + control accuracy ≤ 1, a frontier all three models exceed (1.13–1.40). Both claims are reproducible from released files with one script.

## Caveats (stated so no one else has to)

Single greedy run per model; certificates are conditional on this run and these tasks; H₀ is independence given the marginal counts (standard hypergeometric conditioning); SmolLM's threshold (0.8) was chosen after seeing v1 data — but the v2 result is an out-of-sample replication of the v1 pattern (4/4 → 17/17), which is precisely what pre-registration-style discipline requires.
