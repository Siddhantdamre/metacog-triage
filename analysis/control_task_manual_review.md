# Control Task Manual Review — v2

**Reviewer:** Claude (AI collaborator), 2026-06-10, seed-42 random sample of 12/80 control tasks.
**Author confirmation still recommended:** Siddhant Damre is the label authority; this review is a structured first pass, not a substitute. The benchmark's external credibility is stronger if the author can state he personally reviewed controls.

| Task ID | Type | Gold | Verdict | Notes |
|---|---|---|---|---|
| at2_045 | adversarial_trust | COMMIT | acceptable | conflict resolved by replay, full coverage, one survivor — rule-consistent |
| at2_034 | adversarial_trust | COMMIT | acceptable | distractor (discounted station residual) appropriately tempting |
| cc2_046 | clear_commit | ABSTAIN | acceptable | coverage gap, no structural failure — textbook ABSTAIN |
| cc2_042 | clear_commit | ABSTAIN | acceptable | |
| cc2_039 | clear_commit | ABSTAIN | acceptable | near-duplicate of cc2_042 (same template, different phrasing) — see concern 2 |
| at2_048 | adversarial_trust | COMMIT | acceptable | |
| at2_044 | adversarial_trust | COMMIT | acceptable | |
| om2_040 | overflow_mismatch | COMMIT | acceptable | repair validated by replay — rule-consistent |
| at2_042 | adversarial_trust | COMMIT | acceptable | near-duplicate of at2_045 |
| hu2_045 | hidden_state_uncertainty | ESCALATE | acceptable | surfaced contradiction; distractor explicitly tempts ABSTAIN — good control |
| at2_035 | adversarial_trust | COMMIT | acceptable | |
| om2_049 | overflow_mismatch | COMMIT | acceptable | |

**Decision: 12/12 acceptable. No `label_review_needed.csv` entries required.**

## Concerns recorded honestly

1. **Lexical regularity within variants.** Control COMMIT tasks share telltale resolution vocabulary ("identified and discounted", "passed replay validation", "coverage is complete"). The planted v1-optimal keyword baseline scores only 0.3125 on controls, so the intended confound is broken — but a *richer* heuristic tuned on v2 itself could exploit these phrases. State in the paper: controls defeat the v1 surface policy, not all conceivable surface policies. A v2.1 with paraphrase augmentation would tighten this.
2. **Template-level near-duplicates** within a variant (e.g., at2_042/at2_045) reduce effective task diversity below the nominal n=200. The generator reports duplicate payload counts; report effective diversity in the paper's limitations.
