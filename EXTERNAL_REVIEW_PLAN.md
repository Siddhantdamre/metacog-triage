# External Review Plan

Goal, stated plainly: **one stranger runs the benchmark and tells us whether the result survives.** Everything here serves that.

## 1. GitHub release
Fresh repo `metacog-triage` (this folder's contents only, not the parent repo). Tag `v1.0.0` after the v2 run lands. Issues enabled; add a `results-replication` issue template asking for: model, transformers version, GPU/CPU, comparison_table.md output.

## 2. Hugging Face (optional, after GitHub)
Upload `metacog_tasks_v1.jsonl` + `metacog_tasks_v2.jsonl` as a dataset with a card linking the repo. Benefit: discoverability + one-line loading for others.

## 3. arXiv
After v2 results + citation verification: convert PAPER.md to LaTeX, submit to cs.CL (cross-list cs.AI). An arXiv ID makes the work citable and shareable before any review.

## 4. Workshop targets
One submission, not three. Look for current CFPs in: evaluation/benchmarking workshops, safe/trustworthy agents workshops, or uncertainty-in-NLP workshops at NeurIPS / ICLR / ACL venues. Fit criterion: the workshop welcomes negative/measurement results on small models. **Verify deadlines and scope on the workshop pages — do not rely on memory or this file.**

## 5. Direct outreach (after repo is public)
Send to ~5 people who work on calibration/abstention/selective prediction (find current authors via the citation-verification step — the people whose papers you cite are exactly the right recipients). Template:

> Hi —, I built a small benchmark testing whether LLMs can distinguish abstention from escalation under partial observability, and found that small open models that never bluff still collapse all uncertainty into one conservative action, with stated confidence carrying almost no information about correctness (discrimination gap ≤ 0.11 in 3 of 4 models). Repo with one-command reproduction: <link>. I'd value criticism of the gold-action rules — the design stands or falls on whether you buy the abstain/escalate boundary.

Asking for criticism of the rules (not praise of the result) is what gets researchers to engage.

## 6. Public announcement (X/LinkedIn, after repo + arXiv)
One honest paragraph: what was measured, the dissociation finding, what it does NOT claim, link. No AGI framing, no consciousness framing — the restraint *is* the credibility.

## 7. Feedback handling
- Bug in harness/scoring → fix, add regression note in CHANGELOG, thank publicly.
- Gold-label disagreement → treat as the most valuable feedback type; if the critique holds, revise rules, re-release as v2.1, credit the critic.
- Replication with different numbers → ask for transformers/torch versions first (greedy decoding is deterministic only per-version); document version sensitivity honestly.

## 8. Versioning
v1 task set: frozen forever. v2: frozen at first public release; label changes → v2.1 with changelog. Published numbers always cite task-set version + model + library versions.

## 9. External-run log
Keep `EXTERNAL_RUNS.md`: date, person/handle, model(s), version, headline numbers, link. The first entry by someone you've never met is the project's first real external validation — the success condition for this whole phase.
