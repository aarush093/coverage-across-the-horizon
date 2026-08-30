DOC: 12_PROGRESS_TRACKER | OWNER: Aarush | CADENCE: weekly
STATUS: active | LAST-UPDATED: 2026-08-30 (rev4) | SUPERSEDES: rev1 (2026-08-30)

# 12 — PROGRESS TRACKER (stages from Idea Lock §8)
Current phase: **S5 complete and reproducible. S4 advanced but still partial. S0 still never exited.**

| Stage | Objective | Exit criterion | Status (2026-08-30) |
|-------|-----------|----------------|---------------------|
| SETUP | Build research OS | docs live + scan automated | DONE |
| S0 | Positioning | wedge survives or amended in writing | **NOT EXITED** — no positioning note; four mandated close reads unlogged; Q01–Q05 open; 2604.13253 still unread. This is now the largest single exposure (R8/RV09). |
| S1 | Reproduction | point MSE within ~5% of published | **DONE, DEVIATED -- and the published-MSE check WAS recorded; an earlier version of this tracker wrongly called it unverified.** D008 (2026-08-16) reports ETTh1 within **1.3%** of published at all four horizons using closed-form ridge least squares. **The open item is narrower:** Q07 records ETTh2 @ H=720 measured at MSE 0.7407 against published values that disagree with each other (~0.605 to ~0.831), possibly a seq_len 336-vs-96 difference. That must be resolved before claiming S1 exit. Backbone deviation (DLinear+NLinear, not PatchTST) is D012. |
| S2 | Audit + DECISION GATE | gate resolved | **DONE** — method-led. Confirmed twice: ETT pooled marginal 0.910 vs worst-cell 0.767; Electricity 0.864 vs 0.576. |
| S3 | Method | beats baselines on worst-cell | **DONE** — ETT 0.8657 vs best baseline 0.7797. Electricity 0.8306 vs 0.5757. |
| S4 | Shift & robustness | ablation table complete | **COMPLETE 2026-08-30.** K, gamma, scale, stride ablations in `results.json`; horizon-bucket ablation on a fixed scoring grid, both surfaces (EXP_S4_007 / EXP_S5_008); bias diagnostic (EXP_S4_008); **rolling coverage traces (MET02 / EXP_S4_005) and the calibration-window ablation (EXP_S4_006) both rebuilt** -- the last two things FR01 destroyed. EXP_S4_006 also settled Q16. Nothing from FR01 is now outstanding. |
| S5 | Energy case study | decision-level result exists either way | **DONE** — `results/casestudy.json`, committed `481b90f`. 2 backbones × 4 horizons on Electricity, 300-cell grid, seasonal split. Ran 474 s on the author's machine; W4 answered in both directions (see 20, 43). |
| S6 | Write & release | arXiv preprint live + code; 2 CFPs | NOT STARTED |

## Reproducibility status (claim wording, use this exactly)
> Independently reproduced on a different machine and OS; every reported metric agrees to 4 decimal places, with a maximum absolute deviation of 1.0×10⁻¹³ attributable to floating-point summation order in the linear algebra.

Do **not** write "bit-exact" — it was checked on 2026-08-30 and it is not true.

## Blockers / next actions (ordered):
1. **Approve or reject DELTA_002** (`docs/01_IDEA_LOCK_DELTA_002.md`, STATUS draft). It corrects a factual claim in DELTA_001 and re-weights the horizon term back up. Nothing has been propagated to the Idea Lock and no C-claim was touched, but the emphasis argument for W2 depends on it.
2. **S0 positioning note.** Everything else is ahead of schedule; this is behind and a reviewer reads it first.
3. Rebuild S4 rolling coverage traces + calibration-window ablation (lost, FR01).
4. Resolve Q18 — the Electricity horizon crossover (K=1 wins at H≤192, K=6 at H≥336). It is the sharpest form of RV15 and the mean must not be reported without the split.
5. Case-study figures in the existing monochrome style.
6. R1: the Lock says arXiv after S3. S3 and S5 are both done. Decide whether to post now (P04).
7. Decide P03 — PatchTST reinstated, or C2 narrowed in writing.
