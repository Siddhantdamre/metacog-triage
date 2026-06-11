# Release Readiness Report

**Updated:** 2026-06-11

**Current status:** MetaCog-Triage is public at
`https://github.com/Siddhantdamre/metacog-triage`. The canonical release
repository contains the frozen v1 set, validated 200-task v2 set, four-model v1
and v2 records, regenerated baselines, machine-recomputed calibration results,
and the paper draft.

## Readiness

| Area | Level | Current evidence / remaining work |
|---|---|---|
| v1 data and prompt contract | **frozen** | Published artifacts are present; do not edit |
| v2 data | **ready** | 200 tasks, 80 controls; schema, balance, and decoupling validation pass |
| Harness and scoring | **ready** | Self-contained local runner, parser, scorer, and validators |
| Baselines | **verified** | Committed CSVs reproduce exactly |
| v1 results | **verified** | Four 40-task result files present |
| v2 results | **verified** | Four 200-record result files present and locally recomputed |
| Calibration analysis | **verified** | Record-level recomputation matches the documented headline values |
| Paper content | **needs editorial work** | Add confidence intervals, finish citation review, record final environment, convert to LaTeX |
| Citations | **partially ready** | Five core references verified; recent candidates and alarm-fatigue source still require reading |
| Reproducibility | **ready with bounded caveat** | Deterministic scripts and records are present; a clean external reproduction is still valuable |
| External release | **live** | GitHub `main` at initial public release commit |
| Claim discipline | **ready** | Synthetic-task and non-deployment boundaries are explicit |

## Remaining Release Work

1. Commit the post-release documentation cleanup and standalone
   `prepare_release.py` behavior.
2. Tag `v1.0.0` and create a GitHub Release if not already done.
3. Add binomial confidence intervals and the final run-environment statement.
4. Read the remaining candidate citations before adding them.
5. Convert the paper to LaTeX after content freeze.
6. Obtain one external run or substantive gold-label critique.

## Work After v1.0

- Base-versus-instruct alignment-artifact test.
- v3 paraphrase controls and two-tier parsing.
- Frontier API evaluation only after the v2 paper/release is stable.

These are preregistered follow-ons, not published findings.
