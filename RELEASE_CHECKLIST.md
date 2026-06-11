# Release Checklist

Work top to bottom. Each step is small; stop at any point and the package is still coherent.

## 1. Prepare locally (10 minutes)

- [ ] `cd metacog_triage_release`
- [ ] `pip install -r requirements.txt` (only needed for model runs; prepare/validate need nothing)
- [ ] `python prepare_release.py`
      — copies the frozen v1 tasks + published results from the parent repo, generates the 200-task v2 set, validates both. All steps must print OK.
- [ ] Open `tasks/metacog_tasks_v2.jsonl` and read ~10 tasks, especially control variants. You are the gold-label author: confirm every control's gold action follows from its evidence state. Edit `generate_tasks_v2.py` and regenerate if any feel wrong — *before* any model sees them.

## 2. Run v2 (one Kaggle session)

- [ ] Upload the package folder to a Kaggle notebook (GPU: T4 is enough).
- [ ] `python src/run_benchmark.py --models qwen smollm granite tinyllama --tasks tasks/metacog_tasks_v2.jsonl --output results/v2_run1/`
- [ ] Check `results/v2_run1/comparison_table.md` — the **By Variant** section is the key new table: standard vs control accuracy gap measures surface pattern-matching.
- [ ] Optional: add `qwen3b` and `phi` to the run for a scale probe.

## 3. Update paper

- [ ] Add v2 results to `paper/PAPER.md` (Section 5; the by-variant table directly tests the Section 5.4 hypothesis).
- [ ] Add a random-policy baseline row (expected accuracy = gold-class frequency of most common action).
- [ ] Verify EVERY citation in Section 2 — they are from memory and must be checked against the actual papers before anything goes public.
- [ ] Delete the TODO section once done.

## 4. Publish the benchmark

- [ ] Create a fresh GitHub repo (suggested name: `metacog-triage`). Copy this folder's contents (not the parent repo).
- [ ] Confirm `LICENSE`, `CITATION.cff`, `README.md` render correctly on GitHub.
- [ ] Tag `v1.0.0`.
- [ ] Optional: upload task sets to Hugging Face Datasets with a dataset card pointing to the repo.

## 5. Get outside contact (the actual point)

- [ ] Post the repo + headline finding where benchmark people will see it (e.g., an alignment/evals forum, X, the Kaggle discussion of your original submission).
- [ ] Convert `PAPER.md` to LaTeX and submit to arXiv (cs.CL or cs.AI).
- [ ] Pick one workshop with an open deadline (agent evaluation / safety / trustworthy NLP at NeurIPS, ICLR, ACL venues) and submit. A rejection with reviews is a *success* at this stage — reviews are the external signal the project has never had.
- [ ] Invite critique of the gold-action rules specifically; if someone breaks a control variant, fix and re-release as v2.1. That exchange is the benchmark becoming real.

## Honesty rails (keep these)

- Never edit `tasks/metacog_tasks_v1.jsonl` or `src/prompt_builder.py` — published v1 numbers depend on them.
- Report v2 control-variant results even if (especially if) they make the models — or the benchmark — look worse.
- The paper claims nothing about models that were not run. Keep it that way.
