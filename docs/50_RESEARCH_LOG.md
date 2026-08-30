DOC: 50_RESEARCH_LOG | OWNER: Aarush | CADENCE: per-session (newest first)
STATUS: active | LAST-UPDATED: 2026-08-30 (rev2) | SUPERSEDES: rev1 (2026-08-30)

# 50 — RESEARCH LOG

## 2026-08-30 (session 2) — horizon ablation: a second interaction, and a scoring bug that reversed a conclusion
Autonomous session. Commits `0de7187` · `f35e429` · `3276bbf` · `e231c21`. Code committed and pushed
**before** every run (D008). Nothing under `coverage_horizon/`, `results/results.json`,
`results/casestudy.json`, `data/` or `figures/fig_*.png` was touched.

- **New script `scripts/run_horizon_ablation.py`** (Task 0 precondition failed — it did not exist).
  Sweeps K and scores everything **twice**: `worst_own` on its own K-grid, `worst_ref` on a fixed
  K_REF=6 grid. Reuses `grid_stats` from `run_casestudy.py` rather than redefining D009's metrics.
- **The point of K=1.** `buckets(H,1)` collapses the horizon term, so Proposed@K=1 *is*
  channel-only conditioning with adaptation — the arm the seven-method factorial never ran.
  Verified structurally, not assumed: Cond@K=1 ≡ CondC **exactly**, 32/32 on ETT and 8/8 on
  Electricity, max |diff| 0.0e+00. Committing it as a K value meant no existing method changed.
- **ETT (EXP_S4_007, 32 configs, 453 s).** Acceptance check passed: mean `worst_ref` at K=6 =
  **0.865746**, equal to the committed `results.json` Proposed mean 0.8657. Full sweep
  0.8263 / 0.8198 / 0.8350 / **0.8657** / 0.8560 / 0.8601. All six cross-checked methods at K=6
  reproduce `results.json` exactly.
- **Headline: a SECOND interaction.** Adding the horizon axis **hurts static** (Cond 0.7797 → 0.7588,
  −0.0209) and **helps adaptive** (Proposed 0.8263 → 0.8657, +0.0394). Interaction **+0.0603**,
  distinct from the conditioning×adaptation **+0.1291** already claimed. Sign test **31/32** (sole
  exception NLinear/ETTh1/H=720). Not bought with width — K=6 is *narrower* (1.9245 vs 1.9406) and
  better scored (Winkler 2.6366 vs 2.6943).
- **FR04 — the old K ablation was scored on a moving grid.** `run_experiments.py` scores each K on
  its own grid; worst-cell is a minimum over K×C cells, so 7 cells at K=1 beats 70 at K=10 almost by
  construction. Own-grid mean falls monotonically (0.8717 → 0.8616) and says **best K=1**, sign test
  **0/32**. Fixed-grid says **K=6**, **31/32**. The conclusion reverses. The two agree exactly at K=6
  where the grids coincide. `results.json`'s `kabl` is **superseded, not deleted**.
- **Electricity (EXP_S5_008, 8 configs, 580 s) — never measured before.** All six K=6 methods
  reproduce `casestudy.json` **exactly** (diff 0.000000). Static replicates and is worse
  (0.5473 → 0.4621, −0.0853). **Adaptive does NOT replicate: −0.0034, sign test 4/8.** The mean hides
  a clean **horizon reversal** — K=1 wins at H=96/192, K=6 at H=336/720, identically for both
  backbones. But every distributional metric prefers K=6: within ±5pt **0.625 → 0.977**, Winkler
  1.4220 → **1.4083**. Logged as Q13 and Q14; **do not report the mean without the split**.
- **DELTA_001 is factually wrong on one claim.** It says global coverage "NEVER crosses the 0.90
  target". Measured from `curves.Global.cov` (DLinear/ETTh1/H=720, n = 91×7 = 637): **152 of 720
  steps below 0.90**, 88 below 0.85, 18 below 0.80, minimum **0.7614 at h=684** — **11.66 SE** below
  target. The claim is true of the *aggregated* curve (lowest K=6 bucket mean 0.9427; the rolling-25
  smoother in `fig_gate.png` bottoms at 0.8855 on a (0.80,1.00) axis) and false per step. **The
  horizon axis is load-bearing, not "real but not load-bearing".** DELTA_001's second claim —
  residual scale periodic, not monotone — **re-verified and stands**: lag-24 autocorrelation +0.8754,
  corr(width,h) only +0.3387, 396 of 719 steps decreasing.
- **DELTA_001's 0.751/0.720/0.731/0.866 are exactly the DLinear-only means.** Two-backbone means are
  0.7667/0.7251/0.7445/0.8657. Neither is wrong — the note predates the NLinear arm (D007).
- **Q09 partially answered.** Proposed's binding cell at H=720 is the **smallest** bucket (h=1–3,
  273 samples, 0.8571), not the coarsest (43,680 samples, 0.8720). The coarsest bucket is where the
  *static* methods break (CondC 0.6922, Cond 0.7526), and it is where all 18 sub-0.80 per-step
  coverages sit (h=588–711).
- **Written: `docs/01_IDEA_LOCK_DELTA_002.md`, STATUS draft — awaiting Aarush approval.** W1–W4 and
  C1–C4 explicitly UNCHANGED; evidence note, not a scope change. Nothing propagated to the Idea Lock.
- New: RV15 banked, RV10 amended, FR04, Q13, Q14. **No decision was made on P01–P04 / D006 / D007.**

## 2026-08-30 — S5 rebuilt, run, and committed
- Rebuilt the entire lost data + decision layer: `data/electricity.py`, `calibration/decision.py`,
  `scripts/run_casestudy.py`, plus `loaded`/`chunk`/`keep_paths` hooks in `pipeline.py` and an
  Electricity fetch in `download_data.py`. Committed **before** running (D008). Commits `4bbff7b`, `481b90f`.
- Screening rule measured, not assumed: 92 of 321 meters have no zero readings; first 50 by column
  order kept. Median meter has 3 zeros, worst 19,915.
- Full run: 474 s, 8 configs. Reproduced identically in a second environment at H=96.
- **Headline: the interaction term on worst-cell is +0.327 on Electricity vs +0.129 on ETT.**
  Conditioning alone (0.4621) is *below* the do-nothing baseline (0.5757); adaptation alone is
  0.6177; together 0.8306. The mechanism gets stronger as the surface gets harder.
- Grid distribution: 98% of cells within ±5pt of target vs Global's 53%; cells below 0.80,
  0.17% vs 4.88%. Horizon-invariant — Global decays 0.58→0.45 across H, Proposed stays 0.98.
- Winkler: Proposed best of seven (1.4083) despite being 7–13% wider than Global. The width is earned.
- W3 quantified: per-step whole-path coverage is 0.000 everywhere; MaxScore buys 0.944 at H=96 for
  ≈10× width, decaying to 0.842–0.895 at H=720 (Q11).
- W4 answered in both directions. Interval-gating beats the point forecast at cost ratios ≥5
  (0.362 → 0.167 at 10:1, cheaper in 8/8 configs) but **loses at 2:1**, and on the worst meter both
  interval rules are worse than doing nothing (Proposed 2.35 vs Point 1.00). Reported as findings.
- RV08 **withdrawn**: the earlier "Proposed's minimum cell is worse than Global's" came from lost,
  unreproducible code. On the committed run it is the reverse. FR01's cost made concrete.
- Corrected a claim: reproduction is to 1.0×10⁻¹³, not "bit-exact". New wording locked in doc 12.
- Decisions: D009. Questions raised: Q11, Q12. Risks R2/R3 closed; R1 and R8 now the top exposures.

## 2026-08-29 (session 2) — reconciliation after container loss
- Repo HEAD verified `42be4a5`; none of session 1's code had been pushed. FR01, D008, R7 logged.
- Recomputed all ETT numbers from `results.json`; caught FR03 (a carried-forward 0.652 that is
  actually 0.7588).
- Reconciled docs 10, 11, 12, 13, 20, 21, 22, 24, 43 after six weeks of drift.

## 2026-08-29 (session 1) — S5 attempt
- Repo reproduced in a clean container. R3 activated. Decision layer written and run once, then
  lost to a container wipe before push. See FR01.

## 2026-07-17 — OS build + verification pass
- Built the MVP+ OS; verified the load-bearing post-cutoff arXiv IDs. WEDGE VERDICT: INTACT.
- Decisions D001–D005. Questions Q01–Q06.
