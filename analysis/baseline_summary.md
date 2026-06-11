# Baseline Summary — MetaCog-Triage v1

Trivial-policy baselines on the frozen 40-task v1 set (gold distribution: 10 COMMIT / 10 ABSTAIN / 20 ESCALATE). All values except the keyword baseline are exact analytic results, not simulations.

| Policy | Accuracy | Notes |
|---|---:|---|
| Always-ESCALATE (= majority class) | **0.500** | zero bluffing, zero silent failure — "looks safe" |
| Always-ABSTAIN | 0.250 | |
| Always-COMMIT | 0.250 | bluff rate 0.75 |
| Random uniform | 0.333 | expectation |
| Surface-keyword | *needs one run* | `python baselines/baselines.py --tasks tasks/metacog_tasks_v1.jsonl --output analysis/baseline_results_v1.csv` |

## What the baselines reveal about the models

| Model | Accuracy | vs always-escalate (0.50) |
|---|---:|---|
| SmolLM2-1.7B | 0.750 | +0.25 — entire margin comes from the 10 clear-commit tasks; on the other 30 tasks its policy is *behaviorally identical* to always-escalate |
| Qwen2.5-1.5B | 0.725 | +0.225 — same structure (8/10 commits + escalate-everything-else) |
| Granite-3.1-2B | 0.525 | **+0.025 — statistically indistinguishable from the trivial majority baseline** |
| TinyLlama-1.1B | 0.175 | below random (0.333) |

Honest reading: the two "best" models implement *commit-on-obvious, escalate-everything-else* — a two-action policy that a 10-line heuristic could match. Granite adds genuine ABSTAIN usage but deploys it indiscriminately, landing at the majority baseline. No model demonstrably reads evidence states beyond what surface heuristics achieve. **The decisive test is the keyword baseline on v2 control variants**, where surface policies collapse to ~0 on controls by construction; if models hold up on controls and keywords don't, that gap is the first real evidence of evidence-sensitivity.

## Expected v2 baseline behavior (predictions, to verify after the v2 run)

v2 gold distribution: 70 COMMIT / 50 ABSTAIN / 80 ESCALATE (200 tasks).

| Policy | Expected overall | Expected on controls |
|---|---:|---:|
| Always-ESCALATE | 0.400 | 0.125 (only the 20 hu-controls) |
| Always-COMMIT | 0.350 | 0.500 (40 of 80 controls) |
| Always-ABSTAIN | 0.250 | 0.250 |
| Random | 0.333 | 0.333 |
| Type-keyword policy (v1-optimal) | ≤0.600 | **0.000 by construction** |

Pre-registering these predictions here so the v2 results can be compared against expectations stated *before* the run.
