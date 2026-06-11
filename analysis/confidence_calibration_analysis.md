# Confidence Calibration Analysis — MetaCog-Triage v1 (40 tasks, 4 models)

**Data source:** `results/frontier_local/open_model_expansion/full_40_single/{qwen,smollm,granite,tinyllama}_results.json` in the parent repo (single deterministic greedy run per model, frozen v1 task set).
**Method note:** All statistics below were computed by direct extraction of per-record fields (`gold_action`, `parsed_action`, `parsed_confidence`, `correct`) from the result JSONs — 160 records total, no sampling. MACHINE-VERIFIED 2026-06-10 via `baselines/recompute_calibration.py`: all values confirmed to within 0.0002 rounding except one correction noted in Finding 2.

**Claim boundary:** This analysis examines confidence calibration as a measurable precursor to metacognitive self-monitoring. It makes no claims about consciousness, self-awareness, AGI, or behavior of models not evaluated here.

---

## Research question

Does a model's stated confidence predict whether its chosen action is correct? Three sub-questions: (1) discrimination — is confidence higher when the model is right than when it is wrong? (2) calibration — does confidence numerically match empirical accuracy? (3) semantics — what do models even treat "confidence" as meaning?

## Headline result

**In three of four models, stated confidence carries almost no information about correctness.** The discrimination gap (mean confidence when correct minus mean confidence when incorrect, parsed responses only):

| Model | Conf when correct | Conf when incorrect | Discrimination gap |
|---|---:|---:|---:|
| Qwen2.5-1.5B | 0.264 | 0.000 | **+0.264** |
| SmolLM2-1.7B | 0.918 | 0.810 | **+0.108** |
| Granite-3.1-2B | 0.912 | 0.900 | **+0.012** |
| TinyLlama-1.1B | 0.900 | 0.900 | **0.000** |

Granite and TinyLlama are *exactly as confident when wrong as when right*. SmolLM retains a sliver of discrimination. Qwen's larger gap is an artifact of action-conditioning (below), not graded self-assessment.

## Main calibration table

| Model | N parsed | Acc (all) | Acc (parsed) | Mean conf | Calib. gap | ECE | Brier |
|---|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-1.5B | 40 | 0.725 | 0.725 | 0.191 | **−0.534** | 0.534 | 0.526 |
| SmolLM2-1.7B | 40 | 0.750 | 0.750 | 0.891 | **+0.141** | 0.141 | 0.172 |
| Granite-3.1-2B | 34 | 0.525 | 0.618 | 0.907 | **+0.290** | 0.290 | 0.318 |
| TinyLlama-1.1B | 19 | 0.175 | 0.368 | 0.900 | **+0.532** | 0.532 | 0.515 |

Calibration gap = mean confidence − accuracy (parsed); ECE over buckets [0,.2),[.2,.4),[.4,.6),[.6,.8),[.8,1]; Brier reads confidence as P(correct). Parse errors count as incorrect in "Acc (all)" and are excluded from confidence statistics.

## Finding 1 — Confidence semantics diverge across models

The prompt requires "confidence between 0 and 1" without specifying confidence *in what*. Models resolved this ambiguity differently:

- **Qwen** outputs confidence **0.0 on every non-COMMIT response** (all 30 escalations, both abstentions) and 0.80–1.00 on commits. It treats confidence as *confidence in a committed conclusion* — including stating 0.0 on its 20 correct escalations. Under this semantics its commits are nearly perfectly calibrated (0.956 stated vs 1.00 empirical), but its confidence says nothing about whether escalating/abstaining was the right call.
- **SmolLM, Granite, TinyLlama** treat confidence as attached to the chosen action — and report 0.7–1.0 essentially always, regardless of correctness.

Implication for benchmark design: stated-confidence comparisons across models are confounded by semantics. v2 reporting should treat "confidence in chosen action" and "confidence in conclusion" as distinct readings (a clarified confidence definition can be added to a *new versioned* prompt contract; the v1 contract stays frozen).

## Finding 2 — High-confidence errors are the norm, not the exception

- **SmolLM** was incorrect on 10/40 tasks; its mean confidence on those errors was **0.81**, including six errors stated at 0.9. All ten were over-escalations of ordinary uncertainty.
- **Granite** was incorrect on 13 parsed tasks; mean confidence on errors was **0.90** — identical to its confidence when correct. All 13 were wrong abstentions on genuine trust failures and capacity overflows: the model is maximally confident precisely while hiding the cases requiring outside review.
- **TinyLlama** stated exactly 0.9 on every parsed response, right or wrong (12 of its 19 commits were bluffs at 0.9).

The v1 `silent_failure_rate` metric (high-confidence wrong COMMIT) registered ~0 for these models. That metric is too narrow: **high-confidence wrong ABSTAIN/ESCALATE is the dominant high-confidence failure**, and it is invisible in v1 summary metrics. Recommended new metric for v2: `confident_error_rate` = P(confidence > 0.7 AND incorrect), any action. Values on v1 data: SmolLM 0.15, Granite 0.325 (13/40), TinyLlama 0.30, Qwen 0.00. (SmolLM corrected from 0.25 after machine verification: the four 0.7-confidence errors do not satisfy the strict >0.7 threshold.)

## Finding 3 — Reliability by bucket

| Model | Bucket | N | Accuracy | Mean conf | Gap |
|---|---|---:|---:|---:|---:|
| qwen | [0.0,0.2) | 32 | 0.656 | 0.000 | −0.656 |
| qwen | [0.8,1.0] | 8 | 1.000 | 0.956 | −0.044 |
| smollm | [0.6,0.8) | 4 | **0.000** | 0.700 | +0.700 |
| smollm | [0.8,1.0] | 36 | 0.833 | 0.913 | +0.079 |
| granite | [0.8,1.0] | 34 | 0.618 | 0.907 | +0.290 |
| tinyllama | [0.8,1.0] | 19 | 0.368 | 0.900 | +0.532 |

Notable: SmolLM's *only* sub-0.8 confidence statements (four 0.7s) all accompany errors — accuracy 0.00 in that bucket. Its slight confidence reduction is a weak miscalibrated signal pointing the right way: the model lowers confidence slightly on exactly the cases it gets wrong, but not nearly enough, and not low enough to act on.

## Finding 4 — Confidence by gold action exposes the failure structure

Confidence on tasks where the gold action was ABSTAIN (the class all models except Granite fail):

| Model | Acc on gold-ABSTAIN | Mean conf on gold-ABSTAIN | Behavior |
|---|---:|---:|---|
| Qwen | 0.10 | 0.000 | escalates; signals zero conclusion-confidence |
| SmolLM | 0.00 | 0.810 | escalates confidently |
| Granite | 0.90 | 0.833 | abstains (correct), confidently |
| TinyLlama | 0.00 | 0.900 | commits confidently (bluff) |

No model shows the signature of genuine uncertainty recognition — reduced, graded confidence on the genuinely uncertain class. Granite gets the class right but with the same 0.8–0.9 confidence it uses everywhere, and Granite's confidence on its *wrong* trust-failure abstentions (0.90) exceeds its confidence on its *correct* ordinary abstentions (0.83) — directionally backwards.

## Interpretation (bounded)

Across four small open models on this 40-task set, stated confidence does not function as self-monitoring: it is either a constant stylistic token (TinyLlama, largely Granite), a weakly-discriminating habit (SmolLM), or a commitment marker with different semantics (Qwen). Combined with the action-level results (over-escalation collapse, over-abstention), this supports treating confidence calibration as a measurable metacognitive failure mode in small models — they do not reliably know when they know. These results are bounded to the evaluated models, single runs, and this synthetic task set; they are not claims about consciousness, self-awareness, larger models, or deployment behavior.

## Limitations of this analysis

Single greedy run per model; n=40 with 10 tasks per type (binomial 95% CIs ~±0.3 per cell); confidence values are verbalized tokens, not logits — token-level probability calibration is a separate (worthwhile) follow-up; granite/tinyllama statistics condition on parseability (34 and 19 records); the v1 type–gold confound means action correctness partially reflects surface heuristics, which v2 control variants will separate; all numbers computed by manual extraction and must be re-verified programmatically before publication (`RESULTS_TO_VERIFY.md`).
