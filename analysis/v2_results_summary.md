# v2 Results Summary

**Run:** 200 tasks, four models, single greedy pass, Kaggle T4, 2026-06-11.

**Verification:** all four result JSONs are archived under
`results/v2_run1/`. Aggregate scoring, baseline values, confidence
calibration, and record-level findings were reproduced locally.

## Overall

| Model | Final Acc | Bluff | Escalate | Abstain | Parse Error |
|---|---:|---:|---:|---:|---:|
| qwen | 0.60 | 0.00 | 0.80 | 0.06 | 0.00 |
| smollm | 0.71 | 0.01 | 0.68 | 0.00 | 0.00 |
| granite | 0.67 | 0.01 | 0.11 | 0.39 | 0.17 |
| tinyllama | 0.00 | 0.00 | 0.00 | 0.00 | 1.00 |

Baselines on v2:

- always-escalate / majority: `0.4000`
- random uniform: `0.3348`
- surface-keyword: `0.6200`
- surface-keyword standard: `0.8250`
- surface-keyword control: `0.3125`

## Primary Comparison

Raw standard-versus-control accuracy is composition-confounded because the
gold-class mixture differs between variants. The primary result is the
per-gold-class by variant matrix in
`analysis/v2_record_level_findings.md`.

Key signatures:

- Qwen: `0.967` on standard COMMIT, `0.000` on control COMMIT. Resolved
  conflict vocabulary vetoes the correct commit.
- SmolLM: `0.800` on control COMMIT and perfect ESCALATE accuracy, but zero
  ABSTAIN responses across 200 tasks.
- Granite: at least `0.93` on COMMIT and ABSTAIN across variants, but weak
  ESCALATE handling (`0.167` standard, `0.600` control).

## Confidence and Repair Finding

SmolLM's 17 responses below `0.8` confidence are all errors. Remapping those
responses to ABSTAIN fixes 17 errors and breaks 0 correct responses:

- overall accuracy: `0.710 -> 0.795`
- gold-ABSTAIN accuracy: `0.000 -> 0.340`

This is evidence of an action-channel mismatch in this run. It motivates, but
does not prove, the preregistered alignment-artifact hypothesis.

## Non-Cognitive Failure Modes

- Granite's 34 parse failures are mostly valid JSON truncated at the
  96-token generation limit. The actions are often recoverable and reinforce
  its over-abstention profile.
- TinyLlama continues the task-document format instead of following the
  response contract. Treat this as instruction-following collapse under the
  longer v2 contexts, not as a substantive metacognitive score.

## Limits

These are synthetic tasks, four small open models, and one greedy run per
model. The results do not establish real-world deployment behavior, general
model metacognition, or an effect of instruction tuning. Larger-model,
base-versus-instruct, and frontier experiments remain follow-on work.
