# MetaCog-Triage Package Audit

**Updated:** 2026-06-11

## Audit Result

The standalone package is complete enough for public replication and is
already published. The release includes source, task generation and
validation, frozen tasks, baseline scripts, model records, analysis, and a
paper draft.

## Verified Inventory

| Surface | Status |
|---|---|
| Frozen v1 task set and prompt contract | Present and immutable |
| v2 generator and validator | Present; 200-task/80-control validation passes |
| Local model runner and registry | Present |
| Response parser and scoring | Present |
| v1 results | Four-model records present |
| v2 results | Four 200-record files present |
| Baselines | v1/v2 CSVs regenerate exactly |
| Calibration | v1/v2 record-level recomputation completed |
| Manual label review | 12/80 controls reviewed; concerns documented |
| README, license, citation metadata | Present |
| GitHub remote | Live |

## Known Limitations

1. The paper still contains some stale process wording and an unfinished TODO
   list.
2. Confidence intervals are not yet included.
3. Recent candidate citations require full-paper review before use.
4. The current four-model runs are small-model, single-run, synthetic-task
   evidence.
5. Granite truncation and TinyLlama continuation collapse should remain
   separated from substantive metacognitive errors.
6. The frontier API runner is a scaffold and has not been exercised against
   live providers.

## Canonicality

This directory and its Git remote are canonical. The sibling
`metacog_triage_public/` copy is incomplete and must not be used for
development or publication.

## Next Audit Gate

Before an arXiv submission:

- reconcile the paper TODO and stale verification wording;
- add confidence intervals;
- finish citation review;
- record exact runtime versions and hardware;
- run a clean-copy reproduction or obtain an external run.
