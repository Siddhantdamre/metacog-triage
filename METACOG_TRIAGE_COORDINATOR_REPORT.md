# MetaCog-Triage Coordinator Report

**Updated:** 2026-06-11

## Canonical State

The canonical project is this standalone repository, not the parent
Emotion_and_AI tree and not `metacog_triage_public/`.

- Remote: `https://github.com/Siddhantdamre/metacog-triage`
- Published branch: `main`
- Initial public commit: `5fc6e86`
- Frozen v1 tasks: 40
- Validated v2 tasks: 200, including 80 controls
- Model records: four v1 files and four v2 files

## Verification Completed

- v1 and v2 schema validation
- v2 balance and type-to-gold decoupling checks
- v1 and v2 trivial/surface baseline regeneration
- four-model v1 calibration recomputation
- four-model v2 record-level calibration recomputation
- 12-control manual review sample
- exact reproduction of committed baseline CSVs

## Headline v2 Results

| Model | Accuracy | Primary observed failure mode |
|---|---:|---|
| Qwen2.5-1.5B-Instruct | 0.600 | Resolved-conflict vocabulary vetoes correct commits |
| SmolLM2-1.7B-Instruct | 0.710 | Zero abstentions; confidence exposes a repairable action-mapping gap |
| Granite-3.1-2B-Instruct | 0.670 | Strong commit/abstain discrimination but weak escalation |
| TinyLlama-1.1B-Chat | 0.000 | Document-continuation/instruction-following collapse on v2 |

The surface-keyword baseline scores `0.620` overall on v2, with `0.825` on
standard cases and `0.3125` on controls. The class-by-variant matrix, rather
than the raw standard/control aggregate gap, is the primary evidence-sensitive
comparison.

## Strongest Bounded Finding

Small open models can avoid bluffing while still failing to distinguish
ordinary uncertainty from structural failure. The models exhibit different
mechanisms rather than one generic low-capability pattern.

For SmolLM, remapping its 17 sub-0.8 confidence responses to ABSTAIN fixes
17 errors and breaks 0 correct responses. This supports an action-channel
dissociation in this run. It does not yet prove the broader alignment-artifact
hypothesis.

## Current Uncommitted Work

- `kaggle_run_v2.ipynb`: base-versus-instruct hypothesis-run cell
- `ANNOUNCEMENTS.md`: outreach copy
- documentation and standalone-preparation cleanup

## Remaining Human Decisions

1. Final paper claim review.
2. Remaining citation reading.
3. Whether to tag `v1.0.0` now or after the documentation cleanup.
4. Outreach recipients and external-review venue.

## Claim Boundaries

The benchmark covers synthetic, text-described tasks and four small open
models under single greedy runs. It does not establish deployment safety,
general model metacognition, AGI, consciousness, or real-world transfer.
