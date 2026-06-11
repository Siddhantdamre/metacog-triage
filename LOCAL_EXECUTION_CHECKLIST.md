# Local Execution Checklist (corrected, copy-paste accurate)

Sequence: **inspect → backup → run scripts → verify → label review → Kaggle.**
Actions are COMMIT / ABSTAIN / ESCALATE (never PROCEED). All commands are PowerShell.

## Corrections to the checklist you were given

1. `push_everything.bat` lives in the **repo root** (`C:\Users\siddh\Projects\Emotion_and_AI\`), not in this package folder.
2. `baselines.py` **requires arguments** — running it bare exits with an error. Exact command in Step 5.
3. `recompute_calibration.py` **takes result-JSON paths as arguments** and prints to the screen for you to compare against the existing tables. It does **not** generate the analysis files — those already exist; its job is to confirm or refute their numbers.
4. The calibration md/csv files listed as "expected outputs" of Step 6 are already in `analysis/` — Step 6 verifies them, it doesn't create them.

## Steps

**1. Inspect the push script (do not run yet)**
```powershell
Get-Content C:\Users\siddh\Projects\Emotion_and_AI\push_everything.bat
```
What you will find (so you can verify): it stages all changes, force-adds this package + two result folders that .gitignore would exclude, shows `git status -s`, commits, creates branch `metacog-triage-release`, pushes to the `targetrepo` remote. It does not delete, move, or switch branches. Run it only after this whole checklist passes — pushing verified work beats pushing unverified work.

**2. Safety backup**
```powershell
$src = "C:\Users\siddh\Projects\Emotion_and_AI\metacog_triage_release"
$backup = "C:\Users\siddh\Desktop\metacog_triage_release_backup_$(Get-Date -Format yyyyMMdd-HHmmss).zip"
Compress-Archive -Path $src -DestinationPath $backup -Force
Write-Host "Backup created at: $backup"
```

**3. Prepare the package** (copies frozen v1 artifacts, generates v2, validates both)
```powershell
cd C:\Users\siddh\Projects\Emotion_and_AI\metacog_triage_release
python prepare_release.py
```
Every step must print OK / copied. If anything fails, stop and capture the full error.

**4. Baselines (exact command — arguments are required)**
```powershell
python baselines\baselines.py --tasks tasks\metacog_tasks_v1.jsonl --output analysis\baseline_results_v1.csv
python baselines\baselines.py --tasks tasks\metacog_tasks_v2.jsonl --output analysis\baseline_results_v2.csv
```
Check the analytic rows match `analysis\baseline_results.csv` (always-escalate 0.50 on v1, etc.) and note the surface-keyword score — on v1 it should be HIGH (that's the confound), on v2 controls it should collapse.

**5. Machine-verify the calibration numbers (exact command)**
```powershell
python baselines\recompute_calibration.py `
  ..\results\frontier_local\open_model_expansion\full_40_single\qwen_results.json `
  ..\results\frontier_local\open_model_expansion\full_40_single\smollm_results.json `
  ..\results\frontier_local\open_model_expansion\full_40_single\granite_results.json `
  ..\results\frontier_local\open_model_expansion\full_40_single\tinyllama_results.json
```
Compare the printed values against `analysis\confidence_calibration_tables.csv` and paper §5.6. Anchors: qwen acc 0.7250 / mean_conf 0.1913; smollm 0.7500 / 0.8913; granite parsed acc 0.6176; tinyllama discrimination gap 0.0000. **If anything disagrees, the script wins** — update the CSV and paper, note the correction.

**6. Confirm outputs exist**
```powershell
dir analysis\*.csv; dir analysis\*.md
```

**7. Control-task review (your judgment, ≥10 tasks)**
Open `tasks\metacog_tasks_v2.jsonl`, read at least 10 tasks with `"variant":"control"`. For each: does the gold action follow from the evidence state? any label leakage in the text? Record task IDs + verdicts in `analysis\control_task_manual_review.md`; uncertain labels go to `analysis\label_review_needed.csv` (fix the generator and re-run step 3 if needed — before any model sees the tasks).

**8. Paper sanity pass**
`paper\PAPER.md`: COMMIT/ABSTAIN/ESCALATE only; §5.6 present; no v2 numbers claimed; no consciousness/AGI/deployment claims; citations marked per `paper\CITATION_CHECKLIST.md`.

**9. Write `MACHINE_VERIFICATION_REPORT.md`** — date, commands run, pass/fail, any corrected numbers, control-review verdict, ready-for-Kaggle yes/no.

**10. Now run the push script** (root folder) — backup of verified state.

**11. Kaggle** — upload this folder as a dataset, open `kaggle_run_v2.ipynb`, set `PKG_INPUT`, Run All, download `v2_results_bundle.zip`. No paper updates until the bundle exists.

## Paper framing (agreed)

Headline claim stays as §5.6 + the title already state it: *small models can avoid unsafe COMMIT behavior while failing metacognitive calibration — confidence does not track correctness, especially on ABSTAIN/ESCALATE decisions.* The over-escalation result is the supporting behavioral evidence, not the headline.
