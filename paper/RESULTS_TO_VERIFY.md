**STATUS: VERIFIED 2026-06-10.** recompute_calibration.py was run; all values matched within 0.0002 except smollm confident_error_rate (0.25 -> corrected to 0.15 everywhere). Kept below for audit trail.

# Results To Verify Before Publication

Every number below was computed by manual record-level extraction (160 records read directly from the four result JSONs). The arithmetic was done carefully, but the standard is machine verification.

**One command verifies all of it:**

```bash
python baselines/recompute_calibration.py \
  ../results/frontier_local/open_model_expansion/full_40_single/qwen_results.json \
  ../results/frontier_local/open_model_expansion/full_40_single/smollm_results.json \
  ../results/frontier_local/open_model_expansion/full_40_single/granite_results.json \
  ../results/frontier_local/open_model_expansion/full_40_single/tinyllama_results.json
```

Compare output against:

- `analysis/confidence_calibration_tables.csv` (all columns)
- `analysis/confidence_bucket_table.csv`
- `analysis/actionwise_confidence_matrix.csv`
- Paper §5.6 table

Anchor values that must match (spot-checks against the runner's own summaries, already confirmed): qwen final_acc 0.725, avg conf 0.1913 (runner reported 0.19); smollm 0.750 / 0.8913 (0.89); granite 0.525, avg conf over all 40 incl. nulls 0.7713 (runner reported 0.77); tinyllama 0.175, parse error 21/40 = 0.525 (runner reported 0.53).

Manually derived values with no runner cross-check (verify with extra care): all discrimination gaps, ECE, Brier, bucket rows, per-gold-action confidence means, granite parsed-only accuracy 0.6176, tinyllama parsed-only accuracy 0.3684, confident_error_rate values (smollm 0.25, granite 0.325, tinyllama 0.30, qwen 0.00).

If any number disagrees: the recompute script wins; update the CSVs and paper, and note the correction in the coordinator report.
