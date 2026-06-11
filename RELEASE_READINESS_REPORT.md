# Release Readiness Report — updated 2026-06-11

**Current status: MetaCog-Triage v2 executed on Kaggle T4; paper-grade preliminary results available; record-level local verification pending.** Not yet: final paper-ready verified result. GitHub release unblocks when `results/v2_run1/` is copied locally and record-level verification passes.

---
*(Original 2026-06-10 assessment below; v2 rows now superseded by the status line above.)*

| Area | Level | What's left |
|---|---|---|
| Data (v1 frozen tasks) | **mostly ready** | one `prepare_release.py` run to copy into package |
| Data (v2 tasks) | **needs work** | generate (1 cmd) + your gold-label review of controls |
| Code (harness, generator, validator, baselines) | **mostly ready** | statically reviewed, never executed — smoke-run everything once |
| Baselines | **mostly ready** | analytic rows done; keyword baseline needs 1 run |
| Results (v1, 4 models) | **ready** | exists, record-verified; calibration numbers need machine re-verification |
| Results (v2) | **blocked** | needs Kaggle GPU session |
| Calibration analysis | **mostly ready** | re-verify via `recompute_calibration.py` |
| Paper | **needs work** | v2 results, CIs, citation verification (all of §2), LaTeX conversion |
| Citations | **blocked on review** | every citation unverified — see `paper/CITATION_CHECKLIST.md` |
| Reproducibility | **mostly ready** | deterministic by construction; needs one end-to-end rehearsal |
| External-user readiness | **needs work** | one full dry run on a clean machine/Kaggle before announcing |
| Claim discipline | **ready** | boundaries stated in README, paper, analysis files |

**Overall: needs ~1 hour of your machine time + 1 Kaggle session + citation review before GitHub release. arXiv/workshop after v2 results land.**

Critical path (strict order): prepare_release.py → smoke-run baselines + recompute_calibration → review 10+ control labels → Kaggle v2 run → paper update → citation verification → GitHub → arXiv.
