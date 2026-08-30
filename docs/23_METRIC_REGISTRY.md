DOC: 23_METRIC_REGISTRY | OWNER: Aarush | CADENCE: rare
STATUS: active | LAST-UPDATED: 2026-08-30 (rev2) | SUPERSEDES: 2026-07-17 seed

# 23 — METRIC REGISTRY (exact definitions so numbers stay comparable across sessions)
| ID | Metric | Definition / note | Reported as |
|----|--------|-------------------|-------------|
| MET01 | Coverage error | empirical minus target | MEAN and WORST-CELL over the horizon-bucket × channel grid (worst-cell mandatory) |
| MET02 | Rolling coverage trace | coverage of each test path in time order, then a trailing rolling mean over a window of paths (default 30; paths are one per day) | **PRODUCED 2026-08-30** -- `scripts/run_traces.py`, `results/tr_ecl.json` + `tr_ett.json`. Reported as worst window, fraction of the test period below 0.85, longest consecutive dip, and where in the block the worst window falls. Traces Global / ACI / Proposed so adaptation is isolated. |
| MET03 | Normalized interval width | width / scale | vs horizon step |
| MET04 | Winkler / interval score | width + (2/α)·shortfall on misses | per method. The answer to "you just widened the intervals" |
| MET05 | Quantile (pinball) loss | for quantile-head baselines | not run (no trained baselines in the contracted MVP) |
| MET06 | Joint whole-path coverage | all-(H×C)-covered rate | per-step methods AND MaxScore/Bonferroni, with the width ratio of each |
| MET07 | Calibration wall-clock overhead | per-step cost of the layer | O(1) claim evidence — **not yet measured** |
| MET08 | Decision cost / regret | interval-gated peak flagging, normalised so "flag nothing" = 1.0 | swept over miss:false-alarm ∈ {2,5,10,20,50}, never a single chosen ratio |
| **MET09** | **cell_p05** | 5th percentile of the per-cell coverage grid | alongside the minimum. A minimum is one order statistic; over 300 cells it is far noisier than over 42 |
| **MET10** | **frac_within_5pt** | fraction of cells within ±0.05 of target | the primary wide-grid summary (D009) |
| **MET11** | **frac_below_80** | fraction of cells under 0.80 coverage | the tail statistic — how many cells are badly broken, not just the single worst |
| **MET12** | **worst-channel decision cost** | highest per-channel normalised decision cost | the decision analogue of worst-cell coverage; a good mean can hide one meter absorbing every miss |

MET09–MET12 were added 2026-08-30 for the Electricity case study and are computed in
`scripts/run_casestudy.py` and `coverage_horizon/calibration/decision.py`. **`metrics.py` was
deliberately not modified** — it produced the committed ETT numbers and editing it would move
them silently.

Point-forecast sanity (S1 exit): MSE within ~5% of published — **still unverified for ETT**.
Not applicable to Electricity: a screened 50-meter subset is not the published 321-channel task.
