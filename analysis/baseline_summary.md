# Baseline Summary - MetaCog-Triage

All values below were regenerated from the released task files. The committed
CSV files are:

- `analysis/baseline_results_v1.csv`
- `analysis/baseline_results_v2.csv`

## v1: 40 Tasks

Gold distribution: 10 COMMIT, 10 ABSTAIN, 20 ESCALATE.

| Policy | Accuracy | Important behavior |
|---|---:|---|
| Always-ESCALATE / majority | `0.5000` | Zero bluffing, but over-escalates all ABSTAIN cases |
| Always-ABSTAIN | `0.2500` | Misses every structural failure |
| Always-COMMIT | `0.2500` | Bluff rate `0.7500` |
| Random uniform | `0.3326` | Mean over 1,000 seeded trials |
| Surface-keyword | `0.6500` | Strong evidence that v1 contains exploitable surface regularities |

The v1 surface baseline beats Granite (`0.525`) and comes within `0.075` of
Qwen (`0.725`). Therefore v1 scores alone do not establish evidence-state
reading.

## v2: 200 Tasks

Gold distribution: 70 COMMIT, 50 ABSTAIN, 80 ESCALATE. Variant distribution:
120 standard, 80 control.

| Policy | Overall | Standard | Control |
|---|---:|---:|---:|
| Always-ESCALATE / majority | `0.4000` | `0.5000` | `0.2500` |
| Always-ABSTAIN | `0.2500` | `0.2500` | `0.2500` |
| Always-COMMIT | `0.3500` | `0.2500` | `0.5000` |
| Random uniform | `0.3348` | `0.3343` | `0.3357` |
| Surface-keyword | `0.6200` | `0.8250` | `0.3125` |

The surface-keyword standard-to-control drop is `0.5125`. This confirms that
the controls break the shallow vocabulary policy. Model variant results must
still be interpreted within gold class because standard and control variants
have different class mixtures.

## Interpretation Rule

Use the per-gold-class by variant table as the primary comparison. Aggregate
standard-versus-control gaps can be caused by class reweighting and should not
be presented as a standalone evidence-sensitivity score.
