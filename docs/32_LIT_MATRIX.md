DOC: 32_LIT_MATRIX | OWNER: Shared | CADENCE: per-paper
STATUS: seeded | LAST-UPDATED: 2026-07-17 | SUPERSEDES: none

# 32 — LITERATURE MATRIX (the connected graph)
Seeded from Idea Lock §4 fence table + 2026-07-17 verification pass. Collision = occupies a CLAIMED wedge component.

| Paper | arXiv | Verified | Nearest wedge | Occupies? | One-line differentiation |
|-------|-------|----------|---------------|-----------|--------------------------|
| Informer P1 | 2012.07436 | (pre-cutoff) | — | anchor | point-only backbone; no UQ |
| DLinear P2 | 2205.13504 | (pre-cutoff) | — | anchor | point-only backbone; no UQ |
| PatchTST P3 | 2211.14730 | (pre-cutoff) | — | anchor | point-only backbone; no UQ |
| ProbTS | 2310.07446 | (pre-cutoff) | W1 | NO | documents the divide; trained models, not post-hoc calibration |
| ACI | 2106.00170 | (pre-cutoff) | W2 | NO | 1-D stream; no horizon/channel structure |
| Conformal PID | 2307.16895 | (pre-cutoff) | W2 | NO | scalar, short horizons; not 96–720 grid |
| AcMCP/MSCP | 2410.13115 | ✓ 2026-07-17 | W2 | NO (baseline) | multi-step CP, small H, no channel cond., no decision layer |
| Bellman CI | 2402.05203 | (pre-cutoff) | W3 | NO | DP joint control; ignores cross-horizon dep.; heavy |
| CopulaCPTS | 2212.03281 | ✓ (ICLR'23) | W3 | NO | small H, fixed calibration; not LTSF backbones |
| DSCP | 2503.21251 | ✓ 2026-07-17 | W2 | NO | multi-step CP; not LTSF regime/backbones |
| O2CP (title: Traj. Ensembles) | 2508.13362 | ⚠ 2026-07-17 name mismatch | W4 | NO | online+optim multi-step; W4-future-work claim UNCONFIRMED (Q02) |
| MultiDimSPCI | 2403.03850 | (pre-cutoff) | W3 | NO | ellipsoidal joint sets; not LTSF conditional audit |
| Cond. Guarantees (GCC) | 2305.12616 | (pre-cutoff) | W2 | NO (machinery) | framework for conditional guarantees; not horizon×channel on LTSF backbones |
| Cond.-Coverage Diagnostics | 2512.11779 | [UNVERIFIED] | W1 | ? | diagnostic method; verify at S0 |
| DeRegiME | 2605.19231 | ✓ 2026-07-17 | W1/shift | NO | **NEAREST**: trained sparse-GP density (NLPD/CRPS) on PatchTST/DLinear encoders + same suite — but NOT distribution-free post-hoc coverage-controlled calibration; different objective |
| Report the Floor | 2606.09473 | ✓ 2026-07-17 | spine | NO | one-step-ahead; supports "mandatory training-free baseline" timing, inverts at multi-step |
| Conformal Seasonal Pools | 2605.03789 | ✓ 2026-07-17 | — | NO | training-free seasonal pooling; not conditional-coverage on backbones |
| CP-for-TS survey | 2601.18509 | ✓ 2026-07-17 | W1 | ? | closest benchmarking; read FIRST at S0 (Q05) |
| iTransformer | 2310.06625 | (pre-cutoff) | out-of-scope | — | architecture, not calibration |
| TimeXer | 2402.19072 | (pre-cutoff) | out-of-scope | — | architecture, not calibration |

WEDGE VERDICT (2026-07-17): INTACT. No paper occupies W1–W4.
