DOC: 12_PROGRESS_TRACKER | OWNER: Aarush | CADENCE: weekly
STATUS: active | LAST-UPDATED: 2026-08-16 | SUPERSEDES: 2026-07-17 version

# 12 — PROGRESS TRACKER (stages from Idea Lock §8)
Current phase: S1–S3 partially executed early (D006). Next hard date: Review 1, 19 Aug 2026.

| Stage | Window | Objective | Exit criterion | Status |
|-------|--------|-----------|----------------|--------|
| SETUP | Jul 2026 | Build research OS | all MVP docs live + scan automated | DONE |
| S0 | mid–late Aug | Positioning | wedge survives or amended in writing | IN PROGRESS — 4 mandated close-reads not yet done |
| S1 | Sep wk1–3 | Reproduction | point MSE within ~5% of published; residual tensors archived | PARTIAL — DLinear × 4 ETT × 4 H done, within 1.3% on ETTh1/m1/m2; ETTh2@720 open (Q07). PatchTST + Informer NOT started. Weather/ECL/Traffic/ILI NOT started |
| S2 | late Sep–early Oct | Audit + DECISION GATE | gate resolved: method-led vs audit-led | DONE (DLinear only) — resolved METHOD-LED, emphasis re-weighted to channel axis. See D009 + DELTA_001 |
| S3 | Oct | Method | conditional-adaptive beats baselines on worst-cell, or audit spine adopted | PARTIAL — layer built; beats all 4 baselines on worst-cell (0.866 vs 0.720–0.757) at 7.5% NARROWER width, on all 4 datasets. Backbone-swap half NOT started |
| S4 | early Nov | Shift & robustness | ablation table complete | PARTIAL — K and gamma ablations done; conditioning-mode grid, calibration-window length, MAD-vs-std, strided-vs-overlapping NOT done. Rolling shift traces NOT done |
| S5 | mid Nov–early Dec | Energy case study | decision-level result exists either way | NOT STARTED |
| S6 | Dec 2026 | Write & release | arXiv preprint live + code; 2 CFPs identified | NOT STARTED |

## Evidence in hand (2026-08-16)
- 16 backbone fits, 131 s total CPU. Residual tensors regenerable from `pipeline.py` (seed 2026).
- Headline: marginal coverage 0.901–0.910 for ALL five methods; worst-cell 0.720–0.866. Marginal hides
  an 18-point conditional failure.
- Proposed layer: worst-cell 0.751→0.866, cell-error 0.077→0.026, width −7.5%.
- Interaction is real: conditioning-only 0.652 (gamma=0), adaptation-only 0.731, both 0.866.
- Joint whole-path coverage of per-step intervals: 0.008 @H=96, 0.000 @H≥336. Restoring costs 3.1–3.9× width.

## Blockers / next actions:
- [YOU] Submit Review 1, 19 Aug.
- [YOU] Fill reg numbers + Nayan Jaggi on the cover before submitting (currently 23BIT0000 placeholder).
- [S0] Four mandated close-reads still outstanding; wedge scan for August still outstanding.
- [S1] PatchTST next — it is the load-bearing test of P02/Q09, not just a third data point.
