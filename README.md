# Coverage Across the Horizon

**Horizon- and channel-conditional adaptive conformal calibration for long-term time-series forecasting.**

The standard LTSF backbones report point forecasts only; none emits an interval. This repository
attaches a lightweight, post-hoc, distribution-free calibration layer to a *frozen* forecaster and
asks a sharper question than "is it calibrated?": **calibrated where?**

No forecaster is trained. The main study (2 backbones x 4 datasets x 4 horizons, 32 fits) runs on
CPU in under 4 minutes, and a clean-clone rerun reproduces the committed `results/results.json`
value-for-value (12,625 numeric leaves, max deviation 0.0 on the reference machine; across
machines, agreement to 4 decimal places with deviations at the 1e-13 level from floating-point
summation order).

<!-- BEGIN GENERATED: scripts/make_readme.py -->
## Main study: ETT x4, 42-cell horizon-bucket x channel grid, target 90%

Nine interval methods, two frozen linear backbones, 32 configurations. All adaptive rows use
**realised feedback**: a cell's tracker sees a path's outcome only once that outcome has actually
been observed (see "A correction we found in our own pipeline" below).

| Method | Conditioning | Adaptive | Marginal | Worst-cell | Within +-5pt | Winkler |
|---|---|---|---:|---:|---:|---:|
| Gaussian residual | step x C | no | 0.9096 | 0.7762 | 0.461 | 2.6804 |
| Global split CP | none | no | 0.9097 | 0.7667 | 0.226 | 2.9422 |
| Per-horizon (MSCP) | horizon | no | 0.9123 | 0.7251 | 0.431 | 2.7649 |
| Channel-only | channel | no | 0.9099 | 0.7797 | 0.237 | 2.9806 |
| Static conditional | K x C | no | 0.9084 | 0.7588 | 0.520 | 2.9095 |
| ACI | none | yes | 0.9017 | 0.7446 | 0.209 | 2.8579 |
| Per-horizon online | horizon | yes | 0.9056 | 0.7732 | 0.626 | 2.5840 |
| Conformal PID | horizon | yes | 0.8989 | 0.7958 | 0.726 | 2.5861 |
| **Proposed** | **K x C** | **yes** | **0.9069** | **0.8591** | **0.872** | **2.7100** |

Every number in this file is generated from the result files by `scripts/make_readme.py`, and every
number in the paper by `scripts/make_numbers_tex.py`. None is typed by hand.

**The gain is an interaction.** Conditioning alone (0.7588) and adaptation alone (0.7446) both fail
against a do-nothing global quantile (0.7667); only the combination works (0.8591). Interaction term
**+0.1224** on ETT, and **+0.3022** on the 300-cell Electricity surface, where static
conditioning collapses to 0.4621 and the combination holds 0.8059. Proposed beats the global baseline
in 31/32 ETT configurations and 8/8 on Electricity.

**Marginal coverage is uninformative, and the closest external benchmark shows why.** The nearest
benchmarking work (arXiv:2601.18509) concludes MSCP is the best method, scoring marginal coverage,
width and Winkler. On this surface MSCP has the *highest* marginal coverage of all nine methods
(0.9123) and the *worst* conditional coverage (0.7251, below the do-nothing baseline).

**The horizon axis alone is not enough.** Per-horizon online conformal and conformal PID condition on
horizon at full resolution, finer than our buckets, and adapt online. Neither closes the gap:
0.7732 and 0.7958 against 0.8591 on ETT, 0.6032 and 0.6137 against 0.8059 on
Electricity. AcMCP's multi-step autocorrelation correction is **not** reimplemented, so these bound
that family from below rather than settling it.

**Where we lose.** Proposed does not have the best Winkler score: per-horizon online conformal reaches
2.5840 against 2.7100. Winkler rewards narrow intervals that mostly cover, and the
per-horizon methods buy that while leaving individual cells to fail. Same lesson as the audit, in a
different metric.

**Adaptation is visible, not just averaged** (`results/tr_ecl.json`, `figures/fig_traces.png`).
On Electricity the test block crosses a season: global conformal spends 17.5% of it below
0.85 coverage with dips averaging 21.8 days, against 6.3% and 9.0 days for the adaptive
conditional layer. On the same-season ETT split the advantage disappears entirely (16.0% against
16.3%), and ACI alone is *worse* than doing nothing (22.8%). Rolling-coverage stability is a
shift phenomenon, not a free win.

**Whole-path coverage is priced, not promised.** Per-step methods give essentially zero joint
whole-path coverage. A max-score layer restores 0.8772 at 3.25x the width on ETT and 0.9124 at 10.16x on
Electricity, so the price of a whole-path guarantee ranges from three to ten times the width
depending on the surface.

**Decision layer, reported against ourselves.** Interval gating beats a bare point-forecast rule once
misses cost about 5x a false alarm (0.1773 against 0.3621 at 10:1). It does **not** beat a
point rule with a per-channel margin tuned on the calibration block at the same cost ratio, which
costs 0.1867 at 10:1; across the sweep the conformal rule wins only 18/40 configuration-ratio
pairs. The decision value is in having a calibrated margin, not specifically a conformal one.

**Ablations, on all 32 configurations.** gamma: worst-cell rises monotonically (0.7570 at 0 to
0.8739 at 0.1) and our pre-committed default of 0.02 (0.8591) is **not** the best setting.
Scale: Proposed is exactly invariant to MAD versus standard deviation; the baseline is not, and is
in fact better with standard deviation (0.7805) than with MAD (0.7667). Bucket count: K=6 is
best (0.8591 against 0.8187 at K=1), and the horizon axis hurts the static arm while helping the
adaptive one, a second interaction of +0.0613.

## A correction we found in our own pipeline

Our first implementation updated each cell's tracker with a test path's outcomes at *all* horizon
steps before the next path was issued. With a one-day stride and H=720 that used outcomes realised
up to 696 steps after the next forecast origin. The standard leakage check passed, because the
leaked information lay inside the first half of the test block, which is exactly where the check
does not look. Every adaptive number here is under the corrected protocol
(`coverage_horizon/calibration/conditional.py::calibrate_delayed`, `scripts/run_delayed.py`); the
earlier numbers are kept as a labelled oracle upper bound. The main finding survived. Several
smaller claims did not, and `docs/24_FAILURE_REGISTRY.md` records which.
<!-- END GENERATED -->

## Reproduce

```
pip install -r requirements.txt
python scripts/download_data.py          # ETT x4 + LTSF Electricity (LSTNet release)
python scripts/run_experiments.py        # main study      -> results/results.json
python scripts/run_casestudy.py          # S5 Electricity  -> results/casestudy.json
python scripts/run_horizon_ablation.py   # K sweep, fixed scoring grid
python scripts/run_traces.py             # rolling coverage traces (MET02)
python scripts/run_calwindow.py          # calibration-window ablation
python scripts/check_bias.py             # bias diagnostic vs BC-ACI premise
python scripts/make_summary.py           # regenerates results/SUMMARY.md
python scripts/audit_docs.py             # doc/claim integrity gate
```

Seed 2026, sequential splits, drop_last disabled, strided calibration windows (`coverage_horizon/config.py`).

## Research OS

`docs/` is the project's full research operating system: Idea Lock deltas, decision log (D001-D014),
open questions (Q01-Q23), experiment/metric/failure registries, an adversarial reviewer file
(RV01-RV19), and literature notes. Failures are logged, not hidden: FR01-FR06 in
`docs/24_FAILURE_REGISTRY.md` include two lost-work incidents and a scoring confound that reversed
an ablation's conclusion before it was caught.
