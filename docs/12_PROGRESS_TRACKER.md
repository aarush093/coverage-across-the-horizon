DOC: 12_PROGRESS_TRACKER | OWNER: Aarush | CADENCE: weekly
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: 2026-07-17 version

# 12 — PROGRESS TRACKER (stages from Idea Lock §8)
Current phase: **S5 in progress, S0 never exited.** The 2026-07-17 version of this file said S1–S6 "NOT STARTED"; that was six weeks stale and is corrected below.

| Stage | Window | Objective | Exit criterion | Status (2026-08-29) |
|-------|--------|-----------|----------------|---------------------|
| SETUP | Jul 2026 | Build research OS | all MVP docs live + scan automated | DONE |
| S0 | mid–late Aug | Positioning | wedge survives or amended in writing | **NOT EXITED** — no 1-page positioning note exists; the four mandated close reads (2601.18509, 2410.13115, 2307.16895, 2508.13362) are unlogged; Q01–Q05 all still OPEN. Implementation went ahead of positioning. |
| S1 | Sep wk1–3 | Reproduction | point MSE within ~5% of published; residual tensors archived | **DONE, DEVIATED** — 32 point fits (2 backbones × 4 ETT × 4 H) in `results.json`. Deviations: DLinear+NLinear not DLinear+PatchTST (D007); ETT×4 not ETTh1/ETTm2/Weather. MSE-vs-published check is [UNVERIFIED] — never written down. |
| S2 | late Sep–early Oct | Audit + DECISION GATE | gate resolved: method-led vs audit-led | **DONE** — gate resolved **method-led**. Global split conformal does NOT hold up per-cell: mean worst-cell 0.767 against a 0.90 target while pooled marginal reads 0.910. |
| S3 | Oct | Method | conditional-adaptive beats baselines on worst-cell | **DONE** — Proposed 0.8657 worst-cell vs best baseline 0.7797 (CondC), at *narrower* mean width (1.92 vs 2.09 Global) and best Winkler (2.64). |
| S4 | early Nov | Shift & robustness | ablation table complete | **PARTIAL** — K, γ, scale-estimator, calibration-stride ablations are in `results.json`. Rolling coverage traces (MET02) and the calibration-window ablation were written on 2026-08-29 and then **lost with the container** (D008). Not in git. |
| S5 | mid Nov–early Dec | Energy case study | decision-level result exists either way | **STARTED, NOT REPRODUCIBLE** — an Electricity decision-layer result was produced on 2026-08-29 but the code that produced it no longer exists. Numbers survive only as chat text. Treat as [UNVERIFIED] until rebuilt and pushed. |
| S6 | Dec 2026 | Write & release | arXiv preprint live + code; 2 CFPs identified | NOT STARTED |

## Ahead of schedule, and that is the actual risk
S1–S3 landed ~6 weeks early because the linear backbones are cheap. That bought time, and the time got spent on S5 instead of on S0. The unpaid debt is positioning and related work, which is what Reviewer #2 reads first.

## Blockers / next actions (ordered):
1. **Rebuild the lost S5/S4 code and push it to git before running it again.** Nothing else in S5 counts until this is done (D008).
2. Re-run the case study from the pushed code; only then are the decision numbers citable.
3. Write the S0 positioning note. It is the cheapest remaining item and the one a reviewer will miss most.
4. Decide P03 (PatchTST back in, or narrow the C2 model-agnosticism claim in writing).
