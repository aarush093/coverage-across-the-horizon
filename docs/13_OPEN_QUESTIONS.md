DOC: 13_OPEN_QUESTIONS | OWNER: Shared | CADENCE: continuous
STATUS: active | LAST-UPDATED: 2026-08-30 | SUPERSEDES: 2026-08-29 version

# 13 — OPEN QUESTIONS & TECHNICAL DEBT
| ID | Question | Raised | Status |
|----|----------|--------|--------|
| Q01 | Is "O2CP" = arXiv 2508.13362? Title mismatch. | 2026-07-17 | OPEN — S0 |
| Q02 | Does 2508.13362 name decision-coupled calibration as future work? (W4 evidence rests on it) | 2026-07-17 | OPEN — S0 |
| Q03 | Is MSCP a named method or a paradigm inside 2410.13115 / 2601.18509? | 2026-07-17 | OPEN — S0 |
| Q04 | CopulaCPTS venue of record | 2026-07-17 | OPEN |
| Q05 | Dataset/model overlap of survey 2601.18509 with our wedge — could it pre-empt W1? | 2026-07-17 | OPEN — was meant to be read #1 |
| Q06 | Does BDG2 "~50 meters" survive missingness screening? | 2026-07-17 | DEFERRED — reopens only on a local `git lfs pull` |
| Q07 | How noisy is worst-cell at n_test 190–216? Does the ranking survive a stride sweep? | 2026-08-29 | **PARTIALLY ANSWERED** — mitigated by reporting MET09–MET11 (D009). The `stride_abl` sensitivity still needs pulling forward. |
| Q08 | Does 2604.13253 occupy W2? | 2026-08-29 | **OPEN — wedge-critical, unread since 2026-07-17** |
| Q09 | Is the smallest log-spaced bucket structurally under-sampled? Should bucket edges carry a minimum-steps floor? | 2026-08-29 | OPEN — Proposed now has only ~0.17% of cells below 0.80, so the effect is small, but **where** the surviving failures sit has not been located. Needs a per-cell map. |
| Q10 | Was the 2026-08-03 wedge scan run? | 2026-08-29 | OPEN — check Cowork run history |
| **Q11** | MaxScore whole-path coverage decays 0.944 (H=96) → 0.842–0.895 (H=720) while still costing ≈10× width. Is that a finite-sample effect of n_cal falling to 80, or a real limit on post-hoc whole-path control at long horizon? | 2026-08-30 | OPEN — separable by varying the calibration stride; matters because it bounds what W3 can claim |
| **Q12** | Electricity's 50 kept meters correlate at median r = 0.844 (143 of 1225 pairs above 0.90). "300 cells" is therefore not 300 independent tests. How should the effective grid width be described in the paper? | 2026-08-30 | OPEN — affects wording of the C1 audit claim, not the numbers |
