# MetaCog-Triage Package Audit (Phase 1)

**Date:** 2026-06-10. **Constraint:** no shell available this session — file-level audit only; every "needs execution" item below is one command on your machine.

## Files present

| File | Status |
|---|---|
| `src/prompt_builder.py` (frozen v1 contract) | present, verbatim match to original |
| `src/response_parser.py` | present, verbatim match |
| `src/scoring.py` | present; adds by_gold_action + by_variant grouping (metric definitions unchanged) |
| `src/local_model_configs.py` | present; 4 original + 3 suggested models |
| `src/local_model_runner.py` | present |
| `src/run_benchmark.py` | present, self-contained paths |
| `tasks/generate_tasks_v2.py` | present, deterministic, seed 20260610 |
| `tasks/validate_tasks.py` | present; schema + balance + decoupling checks |
| `baselines/baselines.py` | present; 6 baselines incl. surface-keyword |
| `baselines/recompute_calibration.py` | present; machine-verifies the calibration tables |
| `prepare_release.py` | present; copies frozen artifacts, generates + validates v2 |
| `analysis/` (calibration md + 3 CSVs, baseline csv + md, inventory csv) | present |
| `paper/PAPER.md` (with §5.5 baselines, §5.6 calibration) | present |
| `README.md`, `LICENSE` (MIT), `CITATION.cff`, `requirements.txt`, `RELEASE_CHECKLIST.md` | present |

## Files missing (by design until you run prepare/run)

`tasks/metacog_tasks_v1.jsonl` (copied by prepare_release.py), `tasks/metacog_tasks_v2.jsonl` (generated), `results/v1_two_model/`, `results/v1_four_model/` (copied), `paper/figures/behavior_v1.svg` (copied), `results/v2_run1/` (needs GPU run).

## Audit answers

1. **Self-contained?** Yes after `prepare_release.py` — no imports from the parent repo.
2. **GitHub-ready as standalone repo?** Yes (copy folder contents; checklist step 4).
3. **External dependencies?** transformers/torch/accelerate/sentencepiece for model runs only; generation/validation/baselines/scoring are stdlib-only.
4. **v2 generation works?** Code-reviewed, not executed. **Needs execution.**
5. **Validator checks gold labels/structure?** Schema, enums, uniqueness, balance, decoupling — yes. Semantic correctness of gold labels requires the human review pass (checklist step 1).
6. **Scorer deterministic?** Yes (pure functions of records).
7. **Runner evaluates models?** Yes; greedy decoding; deterministic per model+library version.
8. **Paper matches result files?** §5.1–5.4 and §5.6 cross-checked against record-level data this session; §5.6 numbers manually computed — **must be machine-verified** via `recompute_calibration.py`.
9. **Claims bounded?** Yes; claim-boundary text in README, paper abstract, §5.6, limitations.
10. **Unchecked citations?** Yes — all of paper §2 is from memory, flagged in the paper TODO and `paper/CITATION_CHECKLIST.md`.

## Commands attempted / passed / failed

- Shell unavailable (sandbox VM failed to start) → zero commands executed; all code is statically reviewed only.
- Record-level data extraction from 4 result JSONs: **passed** (160/160 records, 0 ambiguous).

## Blockers and exact next actions

1. `python prepare_release.py` — populates tasks/results, validates v1+v2. (You, ~1 min)
2. `python baselines/baselines.py --tasks tasks/metacog_tasks_v1.jsonl --output analysis/baseline_results_v1.csv` — fills keyword-baseline row. (~1 s)
3. `python baselines/recompute_calibration.py <4 result JSONs>` — verify §5.6 / analysis tables. (~1 s)
4. Manual gold-label review of ≥10 v2 control tasks. (You, ~20 min)
5. Kaggle GPU session for the v2 model run. (~1–2 h)
