# Machine Verification Report — 2026-06-10

Executed by Claude under delegated authority, in the session sandbox (Python 3.10.12, Linux VM over the mounted project folder).

## Commands run and outcomes

| Step | Command | Result |
|---|---|---|
| Prepare | `python3 prepare_release.py` | **PASS** — 6/6 artifacts copied; v1 validated (40 tasks); v2 generated + validated (200 tasks, 80 controls, decoupling checks passed) |
| Baselines v1 | `baselines.py --tasks tasks/metacog_tasks_v1.jsonl` | **PASS** — analytic rows match predictions exactly (always-escalate 0.50, always-abstain/commit 0.25, random 0.333) |
| Baselines v2 | `baselines.py --tasks tasks/metacog_tasks_v2.jsonl` | **PASS** — pre-registered predictions confirmed (always-escalate 0.40 overall / 0.25 controls; always-commit 0.35 / 0.50) |
| Calibration recompute | `recompute_calibration.py` on 4 result JSONs | **PASS with one correction** (below) |
| Control review | 12/80 controls, seed-42 sample | 12/12 acceptable; two design concerns recorded in `analysis/control_task_manual_review.md` |

## Headline new numbers (machine-produced)

- **Surface-keyword baseline: 0.65 on v1** — beats Granite (0.525), within 0.075 of Qwen (0.725). Models barely exceed a 12-keyword heuristic on v1.
- **Keyword baseline on v2: 0.825 standard vs 0.3125 control** — a 0.51 gap. The control design works: surface policies collapse on controls by construction. The v2 model run's standard-vs-control gap is now the decisive evidence-sensitivity measurement.

## Corrections from verification

1. **SmolLM confident_error_rate: 0.25 → 0.15** (my manual count included four 0.7-confidence errors; the metric is strictly >0.7). Corrected in analysis md, paper §5.6.
2. Rounding alignments ≤0.0002 (qwen ECE 0.5338; smollm mean_conf 0.8912, ECE 0.1412; granite ECE 0.2897). All other values — every accuracy, discrimination gap, bucket row, and action-wise cell — confirmed exactly.
3. Fixed a bug in `baselines.py` random-baseline row (per-class columns were degenerate); random per-class accuracies now ≈0.333 as expected.

## Known environment note

The sandbox mount intermittently served a stale copy of a just-edited file (baselines.py). Worked around by running the corrected script from /tmp; on-disk package version is correct. If any script misbehaves on your machine, compare file sizes first.

## Status

- Package: **ready for Kaggle**. Remaining human steps: (1) optional but recommended — author skims controls personally; (2) run `kaggle_run_v2.ipynb`; (3) run root-level `push_everything.bat` (or let the committed state stand if git commit from sandbox succeeded — see coordinator notes).
- Paper: ready except v2 results + the two recent-work citations to read.
- No v2 model results exist yet; nothing about model behavior on v2 is claimed anywhere.
