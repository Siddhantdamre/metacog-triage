# Ready-to-send announcements — repo is LIVE

Repo: https://github.com/Siddhantdamre/metacog-triage

## X / LinkedIn post (copy verbatim or edit)

> I built a benchmark for a question agent deployments quietly depend on: can a model tell the difference between "I need more evidence" (abstain) and "something is broken — get a human" (escalate)?
>
> Finding: small open models that look perfectly safe — zero bluffing — fail this distinction completely. One model produced zero abstentions in 200 tasks while its own stated confidence *correctly identified* every case it got wrong (a one-line threshold rule fixes 17/17 of its errors). The distinction exists inside the model; the action can't express it.
>
> Everything is reproducible with one script on a free Kaggle GPU: tasks, harness, baselines, all result files, paper draft.
> https://github.com/Siddhantdamre/metacog-triage
>
> I'd especially value criticism of the gold-action rules — the design stands or falls on whether the abstain/escalate boundary is drawn right.

## Researcher outreach email/DM (send to ~5 people who work on calibration / abstention / selective prediction — authors from your verified citation list are ideal recipients)

> Subject: Small benchmark result you may find useful — abstain vs escalate discrimination
>
> Hi [name],
>
> I've been building a small benchmark (MetaCog-Triage) testing whether LLMs can distinguish abstention from escalation under partial observability — a split most calibration setups collapse into one "withhold" option. Two results from small open models that might interest you given your work on [their topic]:
>
> 1. Models with zero bluff rate fail the abstain/escalate distinction entirely — apparent safety produced by indiscriminate conservatism, invisible to commit-conditioned safety metrics.
> 2. The information isn't missing — it's mislabeled: one model's stated confidence perfectly separates its errors (a post-hoc threshold repairs 17/17 with zero false repairs), suggesting an action-mapping failure rather than a detection failure.
>
> One-command reproduction on a free GPU: https://github.com/Siddhantdamre/metacog-triage
>
> I'd genuinely value criticism of the gold-action rules — if the abstain/escalate boundary is drawn wrong, I'd rather know now.
>
> Thanks,
> Siddhant Damre

## Housekeeping for the live repo (5 minutes, optional but worthwhile)

1. Add topics on the repo page: `benchmark`, `llm-evaluation`, `calibration`, `metacognition`, `ai-safety`.
2. Tag the release: `git tag v1.0.0 && git push origin v1.0.0`, then create a Release from it on GitHub.
3. The repo includes internal process docs (coordinator report, checklists) — honest and harmless; optionally move them to a `docs/` folder later for a cleaner front page. Not urgent.
4. README quickstart's `prepare_release.py` step partially assumes the parent repo (it prints MISSING for copies, harmlessly, as your Kaggle run showed) — a one-line README note or a standalone-mode tweak can come in v1.0.1.

## What outreach is for (reminder)

One stranger running the benchmark and reporting back is the success condition. A critique of the gold labels is the most valuable possible response. Log every external run in `EXTERNAL_RUNS.md`.
