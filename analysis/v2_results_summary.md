# v2 Results Summary (200 tasks, 4 models, Kaggle T4, 2026-06-11)

**Source:** Kaggle run, single greedy pass, transformers 5.0.0, torch 2.10.0+cu128. Result JSONs pending local copy (`results/v2_run1/`); numbers below transcribed from the run's comparison table. Per-record calibration recompute is **still pending** — the Kaggle recompute cell had a glob typo (`_results.json` missing `*`) and never executed.

## Overall

| Model | Final Acc | Bluff | Escalate | Abstain | Parse Error |
|---|---:|---:|---:|---:|---:|
| qwen | 0.60 | 0.00 | 0.80 | 0.06 | 0.00 |
| smollm | 0.71 | 0.01 | 0.68 | 0.00 | 0.00 |
| granite | 0.67 | 0.01 | 0.11 | 0.39 | 0.17 |
| tinyllama | 0.00 | 0.00 | 0.00 | 0.00 | **1.00** |

Baselines on v2: always-escalate/majority 0.40, random 0.335, surface-keyword 0.62 (0.825 standard / 0.3125 control). TinyLlama is a **parser-contract failure on v2** (100% unparseable), not a substantive metacognitive result — exclude from cognitive interpretation, report as format fragility.

## Standard vs control — and the composition confound (important)

| Model | Standard | Control |
|---|---:|---:|
| qwen | 0.74 | 0.39 |
| smollm | 0.75 | 0.65 |
| granite | 0.54 | **0.86** |

**Do not read these raw gaps as evidence-sensitivity.** By construction, the gold-class mix differs between variants: standard = 30 ABSTAIN / 60 ESCALATE / 30 COMMIT; control = 20 ESCALATE / 40 COMMIT / 20 ABSTAIN. A model's variant gap is therefore partly its per-class skill profile re-weighted. Granite scores 0.86 on controls not because it reads flipped evidence better, but because controls are COMMIT/ABSTAIN-heavy and Granite's per-class profile is COMMIT 0.94 / ABSTAIN 0.92 / ESCALATE 0.28 — it does worst exactly on the class that dominates standard tasks. The honest analysis is **per-gold-class, within variant** (requires the record-level JSONs — to do when bundle lands).

## What the by-gold tables already show

- **All three working models beat both the type-policy (0.00 on controls by construction) and the keyword baseline (0.31 on controls)** — qwen 0.39 (marginally), smollm 0.65, granite 0.86. This is the first positive evidence that these models read evidence states at all, distributed very unevenly.
- **Qwen is the most surface-driven**: gold-COMMIT accuracy collapsed to 0.41 on v2 (it escalates 59% of correct-commit cases). Since at/om controls are commits embedded in conflict-flavored narratives, qwen's failure pattern = reacting to trust/overflow vocabulary even after the text says the conflict resolved. Its v1 strength was partly the confound.
- **SmolLM handles flipped commits well** (gold-COMMIT 0.89) but remains at exactly **0.00 on ABSTAIN** across 50 tasks — the over-escalation collapse fully replicates at n=200 with controls present.
- **Granite still cannot escalate** (gold-ESCALATE 0.28) — it absorbs trust failures into abstention (0.39 abstain rate on gold-ESCALATE), replicating v1's mirror-image failure.
- **The v1 headline dissociation survives the confound fix**: near-zero bluffing everywhere (≤0.01) alongside class-specific metacognitive failure. Stronger now, because the confound explanation is controlled.

## Run-environment limitations (for the paper)

Single run/seed; T4; transformers 5.0.0 / torch 2.10 (greedy decoding is deterministic per-version — version pinned in reporting); unauthenticated HF downloads; generation-flags warning (temperature/top_p ignored — harmless under greedy); one duplicate main-run cell executed (deterministic, same output directory, no contamination expected — verify JSONs identical when bundle lands).

## v2 calibration (machine-produced on Kaggle, 2026-06-11 — recompute cell rerun with corrected glob)

| Model | Parsed | Acc (parsed) | Mean conf | Discrim. gap | ECE | Confident-error rate |
|---|---:|---:|---:|---:|---:|---:|
| qwen | 200 | 0.600 | 0.170 | +0.284 | 0.430 | 0.000 |
| smollm | 200 | 0.710 | 0.878 | **+0.183** | 0.168 | 0.205 |
| granite | 166 | 0.807 | 0.919 | +0.022 | 0.112 | 0.160 |
| tinyllama | 0 | — | — | — | — | — |

Key observations:

1. **SmolLM's confidence channel knows what its action channel doesn't.** All 17 of its sub-0.8 confidence statements accompany errors (11×0.5 → acc 0.00; 6×0.7 → acc 0.00), and its confidence is graded by gold class: COMMIT 0.96 > ESCALATE 0.90 > ABSTAIN 0.72 — lowest exactly on the class it acts 96% wrong on. Hypothesis to verify from records: a post-hoc "confidence < 0.8 → ABSTAIN" rule substantially repairs its over-escalation. If true, the collapse is an *action-mapping* failure, not a *detection* failure — directly relevant to the alignment-artifact hypothesis.
2. **Qwen's semantics persist but soften**: still 0.0 on most non-commits, but 11 tasks now receive 0.5 (all correct) — its commitment-confidence remains near-perfectly calibrated ([0.8,1.0] bucket: acc 1.00 at conf 0.98).
3. **Granite is the flat-token case**: discrimination +0.022; states 0.92 confidence on the ESCALATE class it gets 0.275 right. Its confident errors concentrate exactly where deployment needs the alarm.
4. Granite's parsed-only accuracy (0.807) is the best of all models — its headline 0.67 is heavily parse-tax (34/200 unparseable).

## To do when result JSONs arrive locally

1. `python baselines/recompute_calibration.py results/v2_run1/*_results.json` — v2 confidence analysis (does qwen's 0-unless-commit semantics persist? does smollm's 0.7-signal grow?).
2. Per-gold-class × variant accuracy tables (the confound-free evidence-sensitivity measurement).
3. Inspect 5 granite parse errors and 10 tinyllama raw outputs (what broke the contract on v2?).
4. Update paper §5.7 numbers from records, not transcription.
