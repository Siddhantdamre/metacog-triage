# Demo Upgrade Roadmap

Goal: turn the current project surface into an interactive benchmark leaderboard that a reviewer can understand without reading the full codebase.

## Current State

- GitHub Pages surface is live.
- README explains the benchmark, task contract, and current open-model findings.
- Result artifacts and release notes are already in the repository.

## Highest-Impact Improvements

| Priority | Upgrade | Recruiter value |
| --- | --- | --- |
| P0 | Add a public leaderboard table generated from checked-in result JSON/CSV. | Makes the benchmark instantly inspectable. |
| P0 | Add model filters for commit, abstain, escalate, bluff, and parse error rates. | Shows this is an evaluation product, not only a writeup. |
| P1 | Add downloadable sample task cards with expected labels. | Helps reviewers understand the evaluation design. |
| P1 | Add a small browser chart for failure-mode comparison. | Makes the main result visual and memorable. |
| P2 | Add CI that regenerates static leaderboard data from `results/`. | Improves reproducibility and maintenance. |

## Suggested Demo Shape

- Static GitHub Pages app.
- Data source: checked-in JSON/CSV exported from benchmark results.
- Frontend: plain HTML/JS or lightweight React.
- Views: leaderboard, task examples, failure modes, reproduction commands.

## Definition Of Done

- Reviewer can open one URL and see the benchmark claim, models tested, metrics, and failure-mode breakdown.
- README links directly to the leaderboard.
- The demo includes at least one task example for `COMMIT`, `ABSTAIN`, and `ESCALATE`.
