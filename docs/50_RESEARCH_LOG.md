DOC: 50_RESEARCH_LOG | OWNER: Aarush | CADENCE: per-session (newest first)
STATUS: active | LAST-UPDATED: 2026-08-30 | SUPERSEDES: 2026-08-29 version

# 50 — RESEARCH LOG

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
