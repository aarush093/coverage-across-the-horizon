DOC: 12_PROGRESS_TRACKER | OWNER: Aarush | CADENCE: weekly
STATUS: active | LAST-UPDATED: 2026-08-30 | SUPERSEDES: 2026-08-29 version

# 12 — PROGRESS TRACKER (stages from Idea Lock §8)
Current phase: **S5 complete and reproducible. S4 partially rebuilt. S0 still never exited.**

| Stage | Objective | Exit criterion | Status (2026-08-30) |
|-------|-----------|----------------|---------------------|
| SETUP | Build research OS | docs live + scan automated | DONE |
| S0 | Positioning | wedge survives or amended in writing | **NOT EXITED** — no positioning note; four mandated close reads unlogged; Q01–Q05 open; 2604.13253 still unread. This is now the largest single exposure (R8/RV09). |
| S1 | Reproduction | MSE within ~5% of published | **DONE, DEVIATED** — 32 ETT point fits + 8 Electricity fits. DLinear+NLinear, not DLinear+PatchTST (D007). MSE-vs-published Δ still [UNVERIFIED] for ETT; Electricity is a screened 50-meter subset and is **not** comparable to published 321-channel numbers. |
| S2 | Audit + DECISION GATE | gate resolved | **DONE** — method-led. Confirmed twice: ETT pooled marginal 0.910 vs worst-cell 0.767; Electricity 0.864 vs 0.576. |
| S3 | Method | beats baselines on worst-cell | **DONE** — ETT 0.8657 vs best baseline 0.7797. Electricity 0.8306 vs 0.5757. |
| S4 | Shift & robustness | ablation table complete | **PARTIAL** — K, γ, scale, stride ablations in `results.json`. Rolling coverage traces (MET02) and the calibration-window ablation were lost with the container (FR01) and have **not** been rebuilt. |
| S5 | Energy case study | decision-level result exists either way | **DONE** — `results/casestudy.json`, committed `481b90f`. 2 backbones × 4 horizons on Electricity, 300-cell grid, seasonal split. Ran 474 s on the author's machine; W4 answered in both directions (see 20, 43). |
| S6 | Write & release | arXiv preprint live + code; 2 CFPs | NOT STARTED |

## Reproducibility status (claim wording, use this exactly)
> Independently reproduced on a different machine and OS; every reported metric agrees to 4 decimal places, with a maximum absolute deviation of 1.0×10⁻¹³ attributable to floating-point summation order in the linear algebra.

Do **not** write "bit-exact" — it was checked on 2026-08-30 and it is not true.

## Blockers / next actions (ordered):
1. **S0 positioning note.** Everything else is ahead of schedule; this is behind and a reviewer reads it first.
2. Rebuild S4 rolling coverage traces + calibration-window ablation (lost, FR01).
3. Case-study figures in the existing monochrome style.
4. R1: the Lock says arXiv after S3. S3 and S5 are both done. Decide whether to post now (P04).
5. Decide P03 — PatchTST reinstated, or C2 narrowed in writing.
