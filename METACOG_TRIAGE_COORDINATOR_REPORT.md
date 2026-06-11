# MetaCog-Triage Coordinator Report — 2026-06-10

## Session constraint
The sandbox shell failed to start, so **no code was executed**. Everything below is either (a) file-verified, (b) computed by direct record-level extraction from result JSONs, or (c) prepared-but-unexecuted code. Nothing is claimed as tested.

## 1. Verified locally
Frozen v1 task set + harness; 4-model v1 result JSONs (all 160 records read individually); N-series, R.1–R.3, DEIC core, CogBench, Kaggle bundle. **R.4 / P.1 / P.3 / Q.1 / D.1 / W.1: not found locally — marked unverified** (see `../PROJECT_LOCAL_VERIFICATION.md`).

## 2. Generated this session
Release package (`src/`, `tasks/`, `baselines/`, `prepare_release.py`, README/LICENSE/CITATION), v2 generator (200 tasks, gold/type decoupled, 80 controls), validator, baselines script, calibration recompute script, paper §5.5 + §5.6, audit + readiness + external-review + verification docs.

## 3. Analyses completed (manual extraction, pending machine verification)
Full confidence-calibration analysis, 4 models. Key numbers: discrimination gap (conf-correct − conf-wrong): qwen +0.264 (action-conditioned), smollm +0.108, granite +0.012, tinyllama 0.000. Calibration gap: qwen −0.534, smollm +0.141, granite +0.290, tinyllama +0.532. See `analysis/confidence_calibration_analysis.md`.

## 4. Baseline results (analytic, exact)
always-escalate 0.500, always-abstain/commit 0.250, random 0.333. Granite (0.525) ≈ majority baseline; tinyllama (0.175) < random; qwen/smollm beat trivial only via clear-commit class. Keyword baseline needs one run.

## 5. Calibration headline
**In 3 of 4 models, stated confidence carries essentially no information about correctness; high-confidence errors (conf > 0.7, wrong) occur on 25–33% of all tasks for those models, and are invisible to the v1 silent-failure metric because they occur on ABSTAIN/ESCALATE responses.** Qwen uses divergent confidence semantics (0.0 unless committing). No model shows graded uncertainty recognition.

## 6. v2 task set
Designed + generator written; NOT yet generated/validated/label-reviewed. 200 tasks, 70C/50A/80E, controls break type→gold correlation.

## 7. Model results
v1: complete (4 models). v2: blocked on GPU session.

## 8. Paper status
Draft with results through §5.6; needs v2 results, CIs, citation verification (100% of §2 unverified), LaTeX.

## 9. Release readiness
See `RELEASE_READINESS_REPORT.md`. Short version: ~1 hr local + 1 Kaggle session + citation review from GitHub-ready.

## 10. Remaining blockers
No shell this session (everything unexecuted); GPU for v2; your gold-label review; citation verification.

## 11. Exact next commands (your machine, in order)
```bash
cd metacog_triage_release
python prepare_release.py
python baselines/baselines.py --tasks tasks/metacog_tasks_v1.jsonl --output analysis/baseline_results_v1.csv
python baselines/recompute_calibration.py ../results/frontier_local/open_model_expansion/full_40_single/qwen_results.json ../results/frontier_local/open_model_expansion/full_40_single/smollm_results.json ../results/frontier_local/open_model_expansion/full_40_single/granite_results.json ../results/frontier_local/open_model_expansion/full_40_single/tinyllama_results.json
# then read 10+ control tasks in tasks/metacog_tasks_v2.jsonl
# then Kaggle: python src/run_benchmark.py --models qwen smollm granite tinyllama --tasks tasks/metacog_tasks_v2.jsonl --output results/v2_run1/
```
Also: `git status` in the repo root — R-series/N-series files may be untracked; commit them.

## 12. Honest limitations
n=40, single greedy runs, 1–2B models only, synthetic scenarios, verbalized (not logit) confidence, v1 type–gold confound unresolved until v2 runs, all session arithmetic pending machine verification.

## 13. GitHub-ready?
**Mostly** — after the 4 commands above + label review. Not before.

## 14. arXiv/workshop-ready?
**Not yet** — needs v2 results + verified citations. Realistic: days, not months.

## 15. Requires your manual review
v2 control gold labels (you are the label authority); citation verification; the outreach message recipients; final read of paper claims against your own standards.
