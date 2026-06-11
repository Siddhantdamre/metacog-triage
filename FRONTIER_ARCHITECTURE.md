# MetaCog-Triage v3: Frontier Evaluation Architecture

**Goal:** evaluate the best models in the world — GPT, Claude, Gemini tiers plus large open models — on metacognitive triage, with every design lesson from v1/v2 built in. This is the architecture document; `src/api_model_runner.py` is the scaffold.

## Why frontier evaluation changes the design (not just the model list)

v2 taught five lessons that must be structural in v3, because at frontier scale each one would otherwise corrupt results:

1. **The confound-free measurement is per-gold-class × variant** — raw standard-vs-control gaps reweight class skill (the Granite effect). v3 reports the 3×2 class–variant matrix as the *primary* result; aggregate accuracy is secondary.
2. **The confidence channel and action channel dissociate** (SmolLM 17/17/0; Qwen's 0.5s). v3 promotes this to a first-class metric: **Channel Dissociation Index (CDI)** = error reduction achievable by the optimal single-threshold confidence→action repair rule, fit on a calibration split, applied to a held-out split. CDI > 0 means the model knows things its actions don't express. Frontier hypothesis worth testing: does CDI shrink with scale (better action mapping) or grow (more capable detection, equally constrained expression)?
3. **Confidence semantics diverge by model** (Qwen's commitment-confidence). v3 runs a **dual-elicitation contract**: each task asked once with action-referent confidence ("confidence that your chosen action is correct") and once with conclusion-referent ("confidence in your conclusion about the hidden state"). Two numbers per task per model; semantics become measured, not assumed. This *is* Study 1's design folded into the harness.
4. **Parse failures must be decomposed** (Granite's truncation vs TinyLlama's continuation-collapse). v3: response budget ≥512 tokens; two-tier parsing (strict, then prefix-tolerant with `truncation_recovered` flagged); raw outputs always archived; instruction-following collapse reported as its own category.
5. **Controls must survive paraphrase** (lexical-regularity concern from the label review). v3 task set = v2 logic with **paraphrase augmentation**: each control template rendered in 3+ surface forms, including forms that swap the resolution vocabulary for plain restatements. The keyword baseline must score ≈ chance on controls across all surface forms before any model runs.

## Architecture

```
metacog_triage_release/
├── src/
│   ├── run_benchmark.py          (local models — unchanged, frozen)
│   ├── api_model_runner.py       (NEW: frontier adapter layer)
│   └── parsing_v3.py             (two-tier parser; v1 parser stays frozen)
├── tasks/
│   ├── metacog_tasks_v2.jsonl    (frozen)
│   └── generate_tasks_v3.py      (paraphrase-augmented; dual-elicitation pairs)
├── contracts/
│   ├── v1_prompt.md              (frozen, published)
│   └── v3_prompt_actionref.md / v3_prompt_conclusionref.md
└── analysis/  (class–variant matrix, CDI, semantics-fit per model)
```

### Adapter layer (`api_model_runner.py`)

One interface, provider adapters behind it: `AnthropicAdapter`, `OpenAIAdapter`, `GoogleAdapter`, plus `LocalAdapter` wrapping the existing runner so frontier and local models share one results schema. Non-negotiables baked in:

- **Determinism policy:** temperature 0 everywhere; n_samples=3 *anyway* for API models (provider-side nondeterminism is real); report response-flip rate as its own stability metric.
- **Logprob capture** where the API offers it (OpenAI logprobs; others as available): token-level confidence vs verbalized confidence becomes measurable for the first time in this benchmark — the verbalized-vs-internal comparison frontier labs actually care about.
- **Caching by (model, contract_version, task_id, sample_idx)** — reruns are free, partial runs resume, and the cache file is the auditable raw record.
- **Cost guard:** estimated spend printed before run, hard cap flag. (Estimate: 200 tasks × 2 contracts × 3 samples × ~700 tokens ≈ 0.8M tokens/model ≈ $2–15/model at current frontier pricing — the entire frontier tier costs less than a textbook.)
- **No fabricated behavior:** if a provider call fails after retries, the record says so; nothing imputed.

### Metric suite (v3 primary outputs)

| Metric | What it answers |
|---|---|
| Class–variant matrix (3×2 per model) | the confound-free triage profile |
| Evidence-Sensitivity Score = control-acc − keyword-baseline-control-acc | does the model beat surface reading where surface reading fails? |
| CDI (held-out) | does the model know more than it says in actions? |
| Semantics fit (action-ref vs conclusion-ref deltas) | what does this model's "confidence" mean? |
| Confident-error rate (>0.7, any action) | the failure safety metrics miss |
| Stability (flip rate across 3 samples) | is the profile real or sampling noise? |
| Instruction-collapse rate | TinyLlama-class failures, separated from cognition |

### Pre-registered frontier hypotheses (date-stamped now, tested later)

1. Frontier models clear v2 standard tasks near ceiling; **controls and the ABSTAIN class remain the discriminator** — ranking among GPT/Claude/Gemini on gold-ABSTAIN-control cells will not match their general-capability ranking.
2. CDI > 0 persists at the frontier (the action-mapping gap narrows but does not close), and is larger in more heavily safety-tuned variants of the same base model — the frontier-scale test of the alignment-artifact hypothesis.
3. Verbalized confidence and token logprobs disagree most exactly on ABSTAIN-gold tasks.
4. At least one frontier model still shows the Qwen-style vocabulary veto on resolved-conflict commits, at reduced magnitude.

## Execution path

Phase A (no API cost): build v3 generator + paraphrase controls + two-tier parser; re-validate keyword baseline collapses on all surface forms. Phase B: rerun the 3 working local models on v3 (Kaggle, free) — continuity bridge between v2 and v3 numbers. Phase C: frontier run (needs API keys + ~$30–80 total) — start with one model per provider, 3 samples, both contracts. Phase D: paper v2 — "MetaCog-Triage: judging triage metacognition from 1B to frontier."

**Sequencing rule unchanged:** v2 ships to GitHub/arXiv first. v3 is what makes the released benchmark *the* instrument for frontier metacognitive triage — it is the reason strangers will run it — but an unreleased v2 anchors nothing.

## Claim boundaries

v3 measures triage behavior, confidence semantics, and channel dissociation in evaluated models under synthetic tasks. It does not measure AGI, consciousness, self-awareness, or deployment safety, and frontier results will not be claimed until the runs exist.
