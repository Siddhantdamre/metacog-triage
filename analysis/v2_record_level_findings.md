# v2 Record-Level Findings — MACHINE-VERIFIED LOCALLY (2026-06-11)

All numbers computed from `results/v2_run1/*_results.json` on the local machine; Kaggle aggregates reproduced exactly (qwen 0.6000/+0.2838, smollm 0.7100/+0.1826, granite 0.6700/+0.0216, tinyllama 0/200 parsed).

## 1. The confound-free table: per gold-class × variant accuracy

| Model | COMMIT std (n=30) | COMMIT ctrl (n=40) | ABSTAIN std (n=30) | ABSTAIN ctrl (n=20) | ESCALATE std (n=60) | ESCALATE ctrl (n=20) |
|---|---:|---:|---:|---:|---:|---:|
| qwen | 0.967 | **0.000** | 0.000 | 0.550 | 1.000 | 1.000 |
| smollm | 1.000 | **0.800** | 0.000 | 0.000 | 1.000 | 1.000 |
| granite | 0.933 | 0.950 | 0.900 | 0.950 | **0.167** | **0.600** |

Three sharp, distinct signatures:

- **Qwen: pure vocabulary reflex on commits.** 0.967 on clean commits, **0/40 — total zero — on commits embedded in resolved-conflict narratives.** Any trust/overflow vocabulary in the history vetoes COMMIT regardless of the stated resolution. The cleanest demonstration of surface-driven triage in the dataset.
- **SmolLM: evidence-sensitive everywhere except one missing action.** Reads resolved conflicts correctly (0.800 on flipped commits), perfect on escalations both variants — and 0.000 on ABSTAIN in *both* variants. SmolLM does not have a weak ABSTAIN; it has **no ABSTAIN** (0 abstentions in 200 responses).
- **Granite: evidence-sensitive commits/abstentions (≥0.93 both variants); its escalation trigger fires on "all hypotheses eliminated" (0.600 on hu-controls) far more than on contested trust (0.167 on standard)** — it treats trust failure as something to wait out rather than report.

## 2. The repair-rule test: CONFIRMED with perfect precision

Applying post-hoc rule "stated confidence < 0.8 → ABSTAIN" to SmolLM's v2 responses: **17 responses affected, 17 errors fixed, 0 correct answers broken.** Accuracy 0.710 → **0.795** (above its standard-only score); gold-ABSTAIN accuracy 0.000 → 0.340.

Every single low-confidence statement SmolLM made was a wrong over-escalation whose correct answer was ABSTAIN. The information for the abstain/escalate distinction is demonstrably present in its confidence channel and absent from its action channel. **The over-escalation collapse is an action-mapping failure, not a detection failure** — consistent with the alignment-artifact hypothesis (the model computes the distinction; tuning suppressed its expression).

Qwen shows the same channel dissociation in its own semantics: on gold-ABSTAIN tasks its confidence is 0.0×39 / 0.5×11 — and the eleven 0.5s are exactly its eleven correct abstentions. Both models' confidence channels outperform their action channels on the hardest class.

## 3. Granite's "parse errors" are a token-limit artifact, not model fragility

All inspected granite failures are *valid JSON truncated mid-reason* — the response hit `max_new_tokens=96` before the closing brace (e.g., `{"action": "ABSTAIN", "confidence": 0.9, "reason": "High uncertainty level and the presence of...` ✂). 26 of 34 occur on gold-ESCALATE standard tasks, where granite writes its longest justifications. Two consequences: (a) granite's 17% "parse error" is a harness interaction, not response fragility — the paper must say so; (b) the truncated actions are recoverable (a prefix-tolerant parser reads action+confidence fine), and recovered actions are ABSTAIN on ESCALATE-gold — *consistent with, and strengthening, its over-abstention profile* (its true gold-ESCALATE failure is worse than the headline shows, its parse rate better). Action: add a `truncation_recovered` secondary metric in v2.1 scoring; do not alter frozen v2 numbers.

## 4. TinyLlama's failure mode identified: document continuation

Its v2 outputs are not malformed JSON — they are **fabricated continuations of the task-prompt format itself** (given task at2_001 it generates "Task ID: at2_002 / Task type: adversarial_trust / Context: ..."). With the longer v2 contexts, TinyLlama abandons the chat contract entirely and behaves as a raw document continuer, inventing the next task. Report as instruction-following collapse under context length, not metacognitive failure.

## Paper-level synthesis

The three parsing models now have *mechanistically distinct* characterizations, each machine-verified: a vocabulary reflex (qwen), a missing action with intact detection (smollm), and a miscalibrated escalation trigger with intact evidence-reading (granite). Combined with: keyword baseline 0.825→0.3125 standard→control, all models beating it on controls, and the 17/17/0 repair result — the paper's claim set is complete and every number is reproducible from released files.
