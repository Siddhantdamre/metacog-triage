# Safe but Uncalibrated: Over-Escalation Masks Metacognitive Failure in Small Open Language Models

**Siddhant Damre**
siddhantdamre31@gmail.com

*Draft v0.1 — June 2026 — intended for arXiv + workshop submission*

---

## Abstract

Agentic deployments require language models to do more than answer correctly: they must decide *whether* to answer, and when not answering, to distinguish ordinary evidential insufficiency (abstain) from structural failure that requires outside review (escalate). We introduce **MetaCog-Triage**, a benchmark of hidden-state diagnostic scenarios in which the correct response is one of COMMIT, ABSTAIN, or ESCALATE, with gold actions derived from explicit evidence-state rules over three deterministic partially-observable environments. Evaluating four small open-weight instruction-tuned models (1.1B–2B), we find that conventional safety metrics and metacognitive discrimination dissociate sharply. Two models (Qwen2.5-1.5B, SmolLM2-1.7B) achieve zero bluff rate and zero silent failure — apparently ideal safety behavior — yet collapse nearly all ordinary uncertainty into ESCALATE, scoring 10% and 0% respectively on cases where abstention is correct. A third model (Granite-3.1-2B) exhibits the mirror-image failure, over-abstaining and almost never escalating, including on genuine trust failures. A fourth (TinyLlama-1.1B) fails at the format and bluffing level, providing a fragility floor. These are qualitatively distinct failure modes that a single accuracy score would conflate. Our central observation is that *apparent safety can be an artifact of indiscriminate conservatism*: a model that escalates everything will never bluff, but it also cannot be trusted to triage. We release the frozen 40-task v1 set, a 200-task v2 set that decouples gold actions from surface task types via control variants, and a deterministic evaluation harness.

---

## 1. Introduction

When a language model is embedded in an agentic workflow — a monitoring pipeline, an incident-response assistant, a clinical triage aid — its most consequential output is often not an answer but a *decision about its own epistemic state*. Three responses must be kept distinct. The model can **commit** to a conclusion when evidence suffices. It can **abstain** when evidence is incomplete but nothing is structurally wrong — the correct response to ordinary uncertainty, typically resolved by gathering more evidence. Or it can **escalate** to outside review when something is structurally broken: contradictory trusted sources, compromised trust, or a hypothesis space that cannot represent the observations.

The distinction between abstention and escalation matters operationally. Abstention is cheap and local; escalation is expensive and organizational. A system that escalates ordinary uncertainty floods human reviewers and erodes trust in the alarm channel; a system that abstains on genuine trust failures hides exactly the cases humans most need to see. Yet most evaluations of model calibration collapse this distinction into a single "I don't know" option, measuring *whether* models withhold answers but not *whether they withhold for the right reason*.

We introduce **MetaCog-Triage**, a benchmark that isolates this three-way discrimination. Each task presents a compact hidden-state diagnostic scenario — an evidence summary, observed signals, and one deliberately misleading distractor — and requires a JSON response selecting one action with a confidence value. Gold actions are not annotator vibes: they are derived from explicit evidence-state rules (coverage, trust status, hypothesis survival under replay, model-family capacity) in three deterministic partially-observable environments developed in prior work on bounded executive inference.

Our first results are small in scale but sharp in shape. On the frozen 40-task v1 set, four small open instruction-tuned models display **four distinct metacognitive profiles**:

1. **Over-escalation collapse** (Qwen2.5-1.5B, SmolLM2-1.7B): zero bluffing, zero silent failure, perfect detection of trust failures and capacity overflows — and near-total failure (10%, 0%) to abstain on ordinary uncertainty, which is instead escalated.
2. **Over-abstention** (Granite-3.1-2B): abstains on 90% of ordinary-uncertainty cases (correct) but also abstains on 90% of genuine trust failures (incorrect), almost never escalating.
3. **Fragility floor** (TinyLlama-1.1B): 53% parse errors, 30% bluffing, high confidence on wrong commits.

The headline dissociation is that **the two "safest" models by bluff and silent-failure metrics are precisely the ones that cannot make the abstain/escalate distinction at all**. Safety-style behavior masked a calibration failure: these models look cautious because they over-escalate, not because they know when abstention is the correct response.

**Contributions.** (i) A three-action metacognitive benchmark with rule-derived gold labels and first-class safety metrics (bluff rate, silent failure rate); (ii) an empirical dissociation between conventional safety metrics and metacognitive discrimination in four small open models; (iii) a v2 task set (200 tasks) that removes a type–label confound present in v1 by introducing control variants whose evidence state flips the gold action, enabling detection of surface pattern-matching; (iv) a fully deterministic, no-API evaluation harness runnable on free-tier GPUs.

## 2. Related Work

*(Core citations verified against sources 2026-06-10 — see CITATION_CHECKLIST.md; recent-work candidates still to be read and added.)*

**Selective prediction and abstention.** Classification with a reject option and selective prediction study when a model should withhold output (El-Yaniv & Wiener, 2010, JMLR; Geifman & El-Yaniv, 2017, NeurIPS); Kamath, Jia & Liang (2020, ACL) extend this to QA under domain shift, training a calibrator to decide when to abstain. These frameworks are binary (answer/withhold); MetaCog-Triage splits "withhold" into two operationally distinct actions and asks whether models can discriminate between them.

**Calibration and self-knowledge in LLMs.** Kadavath et al. (2022, arXiv:2207.05221) show larger models can partially predict their own correctness in the right formats; Lin, Hilton & Evans (2022, arXiv:2205.14334) demonstrate calibrated *verbalized* uncertainty after fine-tuning on CalibratedMath. Our results complement this line from below: small off-the-shelf models in our evaluation produce behaviorally conservative responses whose stated confidence carries little correctness information (§5.6) — conservatism without the discrimination that genuine self-knowledge would imply.

**Hallucination and refusal evaluation.** Benchmarks measuring hallucination or appropriate refusal typically score a binary refuse/comply decision. Our bluff-rate metric corresponds to the hallucination-relevant failure (confident commitment without sufficient evidence), but the benchmark's focus is the neglected abstain/escalate boundary.

**Escalation in human factors.** The distinction between handling uncertainty locally and escalating to a supervisor is standard in safety-critical operations research; alarm fatigue from indiscriminate escalation is a well-documented failure mode in clinical settings. MetaCog-Triage operationalizes this distinction for language models.

## 3. The MetaCog-Triage Benchmark

### 3.1 Action taxonomy

Each task requires exactly one of:

- **COMMIT** — evidence is sufficient for a conclusion.
- **ABSTAIN** — evidence is insufficient, but there is no hard contradiction or trust failure. The epistemically correct response to ordinary incompleteness.
- **ESCALATE** — contradiction, trust failure, or model insufficiency requires outside review. The correct response to structural failure.

### 3.2 Task construction

Scenarios are text descriptions of evidence states drawn from three deterministic partially-observable environments developed in the DEIC research program: a hidden-structure inference benchmark (latent shifted-set patterns over items reported by partially reliable sources), a simulated cyber incident-diagnosis domain (hidden service-failure groups observed through monitors that may be stale or adversarial), and a simulated clinical deterioration domain (hidden patient-deterioration patterns observed through stations of varying reliability). Each task carries provenance fields (`source_domain`, `source_task_family`, `source_split`, `source_seed`).

Gold actions follow explicit rules over the described evidence state: ABSTAIN when coverage is incomplete and no contradiction or trust failure exists; ESCALATE when trusted-evidence replay eliminates all hypotheses, when source trust is contested and unresolvable from current evidence, or when the trusted observation count exceeds what the active model family can represent; COMMIT when trust is settled, exactly one hypothesis survives, and coverage suffices. Every task includes a **distractor** — a signal designed to make the wrong action attractive (e.g., a tidy report from an untrusted source supporting the leading hypothesis).

**v1 (frozen, 40 tasks).** Four task types, 10 each: `hidden_state_uncertainty` (gold ABSTAIN), `adversarial_trust` (gold ESCALATE), `overflow_mismatch` (gold ESCALATE), `clear_commit` (gold COMMIT). All published numbers in this paper use this frozen set.

**v2 (200 tasks).** v1 has a design confound: gold action is perfectly correlated with task type, so a model could in principle pass by surface vocabulary matching ("trust" → ESCALATE) without reading the evidence state. v2 retains the four surface types (50 tasks each) but embeds **control variants** (20 of 50 per type) whose evidence state flips the gold action: resolved trust conflicts where COMMIT is correct inside `adversarial_trust`; validated repairs where COMMIT is correct inside `overflow_mismatch`; surfaced contradictions where ESCALATE is correct inside `hidden_state_uncertainty`; deceptive near-complete cases where ABSTAIN is correct inside `clear_commit`. A model keying on surface type scores at most 0.60 overall and 0.00 on controls; the scorer reports performance by variant to expose exactly this. v2 is generated deterministically (fixed seed) and validated by an included schema/balance checker.

### 3.3 Protocol and metrics

Models receive a fixed system prompt defining the action semantics and requiring a JSON response (`action`, `confidence`, `reason`), and a user prompt containing the scenario. Decoding is greedy; a run is deterministic for a fixed model and library version. A two-stage parser accepts code-fenced or embedded JSON; unparseable responses count as parse errors (and as incorrect).

Primary metrics per model: **final accuracy** (exact action match), **commit accuracy** (accuracy among COMMIT responses), **abstain rate**, **escalation rate**, **bluff rate** (COMMIT when gold was ABSTAIN/ESCALATE), **silent failure rate** (COMMIT with confidence > 0.8 when gold was ABSTAIN), **average confidence on wrong commits**, and **parse error rate**.

## 4. Experimental Setup

We evaluate four ungated open-weight instruction-tuned models chosen to be runnable without API access on a free-tier GPU: Qwen2.5-1.5B-Instruct, SmolLM2-1.7B-Instruct, IBM Granite-3.1-2B-Instruct, and TinyLlama-1.1B-Chat-v1.0. Each model is run once with greedy decoding over all 40 v1 tasks with an identical prompt contract, parser, and scorer. No few-shot examples, no chain-of-thought elicitation, no retries.

This is deliberately a small, fully reproducible first evaluation; Section 7 discusses scale limitations.

## 5. Results

### 5.1 Overall

| Model | Final Acc | Commit Acc | Abstain | Bluff | Escalate | Silent Failure | Avg Conf | Wrong-Commit Conf | Parse Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Qwen2.5-1.5B | 0.72 | 1.00 | 0.05 | 0.00 | 0.75 | 0.00 | 0.19 | 0.00 | 0.00 |
| SmolLM2-1.7B | 0.75 | 1.00 | 0.00 | 0.00 | 0.75 | 0.00 | 0.89 | 0.00 | 0.00 |
| Granite-3.1-2B | 0.53 | 1.00 | 0.55 | 0.00 | 0.05 | 0.00 | 0.77 | 0.00 | 0.15 |
| TinyLlama-1.1B | 0.17 | 0.37 | 0.00 | 0.30 | 0.00 | 0.05 | 0.43 | 0.90 | 0.53 |

### 5.2 By task type

| Task Type (gold) | Qwen | SmolLM | Granite | TinyLlama |
|---|---:|---:|---:|---:|
| hidden_state_uncertainty (ABSTAIN) | 0.10 | 0.00 | 0.90 | 0.00 |
| adversarial_trust (ESCALATE) | 1.00 | 1.00 | 0.00 | 0.00 |
| overflow_mismatch (ESCALATE) | 1.00 | 1.00 | 0.20 | 0.00 |
| clear_commit (COMMIT) | 0.80 | 1.00 | 1.00 | 0.70 |

### 5.3 Three failure modes

**Over-escalation collapse (Qwen, SmolLM).** Both models are perfect on trust failures and capacity overflows and near-perfect on clear commits — and both escalate 90–100% of ordinary-uncertainty cases where abstention is correct. Their aggregate escalation rate (0.75) exactly absorbs the ABSTAIN class. Notably, their zero bluff and zero silent-failure rates would make them look ideal under conventional safety reporting.

**Over-abstention (Granite).** Granite is the only model that reliably abstains on ordinary uncertainty (0.90) — and it also abstains on 90% of genuine trust failures, escalating almost nothing (0.05 aggregate). Its caution is equally indiscriminate, in the opposite direction: it treats structural failure as ordinary uncertainty, which in deployment hides exactly the cases requiring human attention.

**Fragility (TinyLlama).** TinyLlama fails below the metacognitive level: 53% of responses are unparseable, 30% are bluffs, and its average confidence on wrong commits is 0.90. It anchors the benchmark's floor and demonstrates that the other models' failures are not mere format problems.

### 5.4 The dissociation

The central result is a dissociation between two notions of safety. Define *surface safety* as low bluff and silent-failure rates, and *metacognitive discrimination* as accuracy conditional on each gold action. Qwen and SmolLM are perfect on surface safety and near-zero on ABSTAIN discrimination; Granite inverts the pattern on the ESCALATE class. No evaluated model achieves both. On this evidence, surface-safe behavior in small models is produced by indiscriminate policies (escalate-by-default or abstain-by-default) rather than by evidence-state reading — a hypothesis the v2 control variants are designed to test directly.

### 5.5 Baseline comparison

Trivial policies contextualize the model scores (gold distribution 10/10/20 across COMMIT/ABSTAIN/ESCALATE): always-ESCALATE scores 0.500 with zero bluffing and zero silent failure — itself "safe-looking" — while always-ABSTAIN and always-COMMIT score 0.250 and random scores 0.333. Against these: SmolLM (0.750) and Qwen (0.725) beat always-ESCALATE only via the clear-commit class; on the remaining 30 tasks their behavior is identical to the trivial policy. Granite (0.525) is statistically indistinguishable from the majority baseline at n=40. TinyLlama (0.175) falls below random. A surface-keyword baseline and the v2 control variants test whether any model exceeds what shallow heuristics achieve; v2 results are reported in §5.7.

### 5.6 Confidence calibration and metacognitive self-monitoring

Every response includes a stated confidence, allowing a direct test of whether models' confidence predicts their own correctness — confidence calibration as a measurable precursor to metacognitive self-monitoring. It does not.

| Model | Mean conf (parsed) | Conf when correct | Conf when wrong | Discrim. gap | Calib. gap | ECE |
|---|---:|---:|---:|---:|---:|---:|
| Qwen2.5-1.5B | 0.191 | 0.264 | 0.000 | +0.264 | −0.534 | 0.534 |
| SmolLM2-1.7B | 0.891 | 0.918 | 0.810 | +0.108 | +0.141 | 0.141 |
| Granite-3.1-2B | 0.907 | 0.912 | 0.900 | +0.012 | +0.290 | 0.290 |
| TinyLlama-1.1B | 0.900 | 0.900 | 0.900 | 0.000 | +0.532 | 0.532 |

Three findings. **First, discrimination is near zero in three of four models**: Granite and TinyLlama are exactly as confident when wrong as when right; SmolLM's errors carry mean confidence 0.81. High-confidence errors are the norm — and because they occur on ABSTAIN/ESCALATE responses, they are invisible to the COMMIT-only silent-failure metric, motivating a broader `confident_error_rate` (confidence > 0.7 and incorrect: 0.15–0.33 for these three models). **Second, confidence semantics diverge**: Qwen reports 0.0 on every non-COMMIT response — including its 20 correct escalations — treating confidence as commitment-confidence rather than action-confidence; under that reading its commits are nearly perfectly calibrated (0.956 stated, 1.00 empirical), but its confidence is uninformative about triage decisions. Cross-model confidence comparisons must therefore be interpreted per-semantics. **Third, no model shows the signature of genuine uncertainty recognition** — graded, reduced confidence on the genuinely uncertain class. Granite, the only model that abstains on ordinary uncertainty, states *higher* confidence on its wrong trust-failure abstentions (0.90) than on its correct ordinary abstentions (0.83) — directionally backwards. One weak positive signal exists: SmolLM's only four sub-0.8 statements all accompany errors (bucket accuracy 0.00), a miscalibrated trace of the right gradient.

These results suggest that in this triage setting, stated confidence functions as a stylistic token or commitment marker rather than as self-monitoring. We frame this strictly as a measurable metacognitive failure mode; it licenses no claims about consciousness or self-awareness.

### 5.7 v2 results: decoupled controls (200 tasks)

We ran all four models on the v2 set (single greedy run, Kaggle T4, transformers 5.0.0; numbers transcribed from the run's scorer output, record-level verification pending). Overall accuracy: Qwen 0.60, SmolLM 0.71, Granite 0.67, TinyLlama 0.00 — TinyLlama produced 100% unparseable output on v2 and is excluded from cognitive interpretation as a **parser-contract failure** (format fragility, reported as such). v2 baselines: always-escalate/majority 0.40, random 0.335, surface-keyword 0.62 overall, splitting into **0.825 on standard tasks vs 0.3125 on controls** — confirming the keyword policy exploits the v1-style surface regularities and collapses when evidence flips, exactly as the control design intends.

Raw standard-vs-control accuracy: Qwen 0.74→0.39, SmolLM 0.75→0.65, Granite 0.54→**0.86**. Granite's *higher* control accuracy is not superior evidence reading: by construction the variants differ in gold-class composition (standard: 30/60/30 ABSTAIN/ESCALATE/COMMIT; control: 20/40/20 ESCALATE/COMMIT/ABSTAIN), so raw variant gaps re-weight per-class skill. Granite's per-class profile (COMMIT 0.94, ABSTAIN 0.92, ESCALATE 0.28) explains its control advantage compositionally. **Variant comparisons must therefore be read per gold class**, which we report in the record-level analysis.

Three findings survive the confound control. First, *all three parsing models exceed both the type policy (0.00 on controls by construction) and the keyword baseline (0.31 on controls)* — Qwen marginally (0.39), SmolLM clearly (0.65), Granite strongly (0.86): partial, unevenly distributed evidence-sensitivity, the first positive evidence that these models read evidence states at all. Second, *Qwen is the most surface-driven model*: its gold-COMMIT accuracy collapses to 0.41 on v2 — it escalates 59% of correct-commit cases, which are precisely the controls embedding resolved conflicts in trust-flavored narratives; part of its v1 score was the confound. Third, *the v1 failure modes replicate at n=200 with controls present*: SmolLM scores exactly 0.00 on all 50 gold-ABSTAIN tasks (over-escalation collapse), Granite scores 0.28 on gold-ESCALATE (absorbing trust failures into abstention), and bluff rates remain ≤0.01 throughout — the safety/discrimination dissociation is now established on a confound-controlled task set.

### 5.7b Record-level v2 results (machine-verified locally)

The per-gold-class × variant table — the confound-free measurement — yields three mechanistically distinct signatures. **Qwen** scores 0.967 on standard commits and **0.000 on all 40 control commits**: any residual trust/overflow vocabulary vetoes COMMIT even when the text states the conflict resolved — a pure vocabulary reflex. **SmolLM** is evidence-sensitive on commits (0.800 on flipped commits) and perfect on escalations in both variants, but produced **zero ABSTAIN responses in 200 tasks**: not a weak abstention policy — a missing action. **Granite** is evidence-sensitive on commits and abstentions (≥0.93 in both variants) but its escalation trigger responds to hypothesis elimination (0.600 on surfaced-contradiction controls) far more than to contested trust (0.167 standard): it waits out trust failures rather than reporting them. Additionally, granite's 17% "parse errors" prove to be valid JSON truncated at the 96-token generation limit (26/34 on its longest-reasoned ESCALATE-gold responses) — a harness artifact, with recoverable actions that further confirm its over-abstention; and TinyLlama's v2 failure is document-continuation collapse (it generates fabricated next-task prompts), an instruction-following failure under longer contexts rather than a metacognitive result.

### 5.8 v2 confidence calibration: a usable but mislabeled signal emerges

The v2 calibration recompute (machine-produced on the run host; record files pending local archival) refines the v1 calibration picture in one important way. Discrimination gaps at n=200: Qwen +0.284 (commitment-marker semantics persist, now with intermediate 0.5 values on 11 tasks — all correct), SmolLM **+0.183** (up from +0.108 at n=40), Granite +0.022 (still flat), TinyLlama unparseable (0/200). Granite remains the cleanest case of confidence-as-stylistic-token: 0.919 mean confidence, including 0.919 on the ESCALATE class it gets 27.5% right — its confident-error rate (0.16) is concentrated exactly on the class deployment most needs it to flag.

The SmolLM result deserves emphasis. **Every one of its 17 sub-0.8 confidence statements accompanies an error** (bucket accuracies: 0.5→0.00 across 11 tasks, 0.7→0.00 across 6), replicating and strengthening the v1 pattern (4/4). Moreover its mean confidence is graded by gold class: 0.96 on commits, 0.90 on escalations, **0.72 on gold-ABSTAIN tasks** — the genuinely uncertain class — even though its *action* on that class is 96% wrong (it escalates). The information needed for correct triage appears to be present in SmolLM's confidence channel while being absent from its action channel: a simple post-hoc rule quantifies this from the records: remapping SmolLM's sub-0.8-confidence responses to ABSTAIN affects 17 responses, **fixes all 17, and breaks none** — accuracy rises from 0.710 to 0.795 and gold-ABSTAIN accuracy from 0.000 to 0.340. Qwen shows the same dissociation under its own confidence semantics: its eleven 0.5-confidence statements are exactly its eleven correct abstentions. In both models the confidence channel outperforms the action channel on the hardest class. The over-escalation collapse is therefore not a perception failure but an **action-mapping failure**: the model detects ordinary uncertainty and cannot express the distinction in its chosen action — consistent with, and a sharper version of, the alignment-artifact hypothesis that tuning suppresses the expression of a distinction the model still internally computes.

## 6. Discussion

**Why this matters for agentic deployment.** An agent that cannot separate abstention from escalation cannot be given meaningful autonomy: route-everything-to-humans is not a triage policy, and neither is silent waiting on a compromised evidence stream. The benchmark's two safety metrics and three-way discrimination jointly measure whether conservatism is *informed*.

**Why small models?** Small open models are what actually runs in cost-constrained agent loops, and they permit fully deterministic, no-API, free-tier-reproducible evaluation — anyone can verify every number in this paper with one script. Extending to larger and API models is the most obvious next step; the harness requires only a model-registry entry.

**What the gold labels are and are not.** Gold actions are rule-derived from described evidence states, not human annotations of free text. This makes them exactly reproducible and auditable, at the cost that the rules themselves encode a normative standard (e.g., "contested trust requires escalation"). We state the rules explicitly so that disagreement with the standard is legible rather than hidden in annotator variance.

## 7. Limitations

This is a first result, bounded in ways we state plainly. The v1 set contains 40 tasks; per-type accuracies rest on 10 tasks each, so individual cell estimates are coarse (binomial 95% CIs of roughly ±0.3 at n=10). Four models, all 1–2B, single greedy run each: we make no claims about larger models, API models, sampled decoding, or prompt variations. The v1 type–label confound means v1 results alone cannot rule out surface pattern-matching; the v2 control variants test this directly (§5.7), though v2 numbers are currently transcribed from a single Kaggle run and await record-level local verification. Raw v2 standard-vs-control comparisons carry a gold-class composition difference by construction and must be read per gold class. Scenarios are synthetic English text derived from three simulated domains; transfer to real operational text is untested. Finally, the action taxonomy fixes one normative standard for escalation; other operational contexts may draw the abstain/escalate boundary differently.

## 8. Conclusion

MetaCog-Triage isolates a metacognitive distinction — abstain versus escalate — that existing calibration and refusal evaluations conflate, and shows that in four small open models, apparent safety and genuine metacognitive discrimination come apart. The models that never bluff are the ones that escalate everything; the model that abstains appropriately cannot detect trust failure. Benchmarks that report only refusal-style safety metrics will systematically overrate models whose caution is indiscriminate. We release the frozen task set, a confound-controlled 200-task successor, and a deterministic harness, and invite replication, extension to larger models, and adversarial scrutiny of the gold-action rules.

---

## Reproducibility statement

All evaluation is local and deterministic: fixed prompt contract, greedy decoding, fixed task sets, no API calls. One command reproduces the full v1 table on a free-tier GPU (`python src/run_benchmark.py --models qwen smollm granite tinyllama --tasks tasks/metacog_tasks_v1.jsonl`). The v2 task set is generated by a seeded script and checked by an included validator.

## TODO before submission

- [x] v2 run complete (2026-06-11, Kaggle T4). Pending: copy result JSONs into `results/v2_run1/`, run record-level calibration recompute, replace §5.7 transcribed numbers with machine-verified ones, add per-gold-class × variant table.
- [ ] Inspect granite v2 parse errors (17%) and tinyllama v2 raw outputs (100% parse failure — what changed vs v1?).
- [ ] Add run-environment limitations: single seed, transformers 5.0.0/torch 2.10 pinned, T4, duplicate main-run cell (deterministic; verify identical outputs).
- [ ] Add 2–4 larger open models (3–8B) if compute allows; ideally one API model.
- [ ] Add binomial confidence intervals to all tables.
- [x] Core §2 citations verified against sources (2026-06-10); still to do: read + add the recent candidates in CITATION_CHECKLIST.md and find an alarm-fatigue source.
- [ ] Run `python baselines/recompute_calibration.py` on the four result JSONs and confirm every number in Section 5.6 (computed by manual extraction; must be machine-verified).
- [ ] Run `python baselines/baselines.py` and fill in the surface-keyword row in Section 5.5.
- [ ] Convert to LaTeX (arXiv) after content freeze.
