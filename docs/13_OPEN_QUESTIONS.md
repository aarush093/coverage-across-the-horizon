DOC: 13_OPEN_QUESTIONS | OWNER: Shared | CADENCE: continuous
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: 2026-07-17 version

# 13 — OPEN QUESTIONS & TECHNICAL DEBT
| ID | Question | Raised | Status |
|----|----------|--------|--------|
| Q01 | Is "O2CP" = arXiv 2508.13362 ("Adaptive CP Intervals Over Trajectory Ensembles")? | 2026-07-17 | OPEN — S0 never run |
| Q02 | Does 2508.13362 actually name decision-coupled calibration as open future work? (W4 evidence rests on it.) | 2026-07-17 | OPEN — S0 never run |
| Q03 | Is MSCP a separately-named method or a paradigm inside 2410.13115 / survey 2601.18509? | 2026-07-17 | OPEN |
| Q04 | CopulaCPTS venue of record. | 2026-07-17 | OPEN |
| Q05 | Dataset/model overlap of survey 2601.18509 with our wedge — could it pre-empt W1? | 2026-07-17 | OPEN — was meant to be read #1 |
| Q06 | Does BDG2 "~50 meters" survive missingness screening? | 2026-07-17 | DEFERRED — BDG2 demoted (D006); reopens only on a local LFS checkout |
| **Q07** | With n_test = 117 windows and a 42-cell grid, how noisy is worst-cell coverage? Does the ranking survive a stride sweep? | 2026-08-29 | OPEN — data already exists in `stride_abl`, just needs analysing |
| **Q08** | Does 2604.13253 (bias-corrected ACI for multi-horizon forecasting) occupy W2? | 2026-08-29 | **OPEN — wedge-critical, unread since it was surfaced on 2026-07-17** |
| **Q09** | Is the smallest log-spaced horizon bucket structurally under-sampled? Should bucket edges carry a minimum-steps floor? | 2026-08-29 | OPEN — suspected mechanism behind RV08 |
| **Q10** | Was the 2026-08-03 first-Monday wedge scan run? Nothing is logged. | 2026-08-29 | OPEN — check Cowork run history |
