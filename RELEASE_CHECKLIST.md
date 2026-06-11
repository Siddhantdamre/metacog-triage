# Release Checklist

## Completed

- [x] Package is self-contained.
- [x] Frozen v1 tasks and results are included.
- [x] v2 generated and validated: 200 tasks, 80 controls.
- [x] Baselines regenerated for v1 and v2.
- [x] Four-model v2 run completed on Kaggle T4.
- [x] Result JSONs copied into `results/v2_run1/`.
- [x] Record-level calibration recomputed.
- [x] Per-gold-class by variant analysis produced.
- [x] Granite truncation and TinyLlama continuation failures inspected.
- [x] GitHub repository created and initial release pushed.
- [x] Core Section 2 references checked for existence and abstract-level fit.

## Before Tagging v1.0.0

- [ ] Commit the post-release documentation cleanup.
- [ ] Confirm README quickstart from a clean standalone checkout.
- [ ] Decide whether `ANNOUNCEMENTS.md` belongs in the release.
- [ ] Confirm the GitHub repository contains all four v2 result JSONs.
- [ ] Create and push the `v1.0.0` tag.

## Before arXiv or Workshop Submission

- [x] Remove completed items from the paper TODO section.
- [ ] Add binomial confidence intervals.
- [ ] Record the final hardware/library environment.
- [ ] Read the remaining candidate citations before adding them.
- [ ] Find and verify an alarm-fatigue/escalation-cost source if that framing
      remains in the paper.
- [ ] Convert `paper/PAPER.md` to LaTeX.
- [ ] Perform a final claim-to-artifact audit.

## External Validation

- [ ] Ask for criticism of the gold-action rules.
- [ ] Record external runs in an external-run log.
- [ ] Treat label disagreement as high-value evidence.
- [ ] Version any task-label change as a new release; never rewrite frozen v1.

## Honesty Rails

- Never edit `tasks/metacog_tasks_v1.jsonl` or `src/prompt_builder.py`.
- Report control results and parse/instruction failures even when unfavorable.
- Do not generalize beyond the evaluated models and synthetic task contract.
- Keep preregistered follow-on hypotheses separate from published findings.
