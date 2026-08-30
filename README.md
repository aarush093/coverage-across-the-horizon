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

## Main study -- ETT x4, 42-cell horizon-bucket x channel grid, target 90%

| Method | Conditioning | Adaptive | Marginal | Worst-cell | Winkler (lower = better) |
|---|---|---|---:|---:|---:|
| Gaussian residual | H x C | no | 0.910 | 0.776 | 2.680 |
| Global split CP | none | no | 0.910 | 0.767 | 2.942 |
| Per-horizon (MSCP) | horizon | no | 0.912 | 0.725 | 2.765 |
| Channel-only | channel | no | 0.910 | 0.780 | 2.981 |
| Static conditional | H x C | no | 0.908 | 0.759 | 2.910 |
| Adaptive CI (ACI) | none | yes | 0.903 | 0.745 | 2.831 |
| **Proposed** | **H x C** | **yes** | **0.910** | **0.866** | **2.637** |

Every number above and below is generated from the result files by `scripts/make_summary.py`
(`results/SUMMARY.md`); none is typed by hand.

**The gain is an interaction.** Conditioning alone (0.759) and adaptation alone (0.745) both fail;
their combination reaches 0.866 with narrower intervals and the best Winkler score of the seven.
Interaction term +0.129 on ETT -- and **+0.326 on the harder 300-cell Electricity surface**, where
static conditioning collapses to 0.462 while the combination holds 0.831.

**Marginal coverage is uninformative -- and the closest external benchmark shows why.** The nearest
benchmarking work (arXiv:2601.18509) concludes MSCP is the best method, scoring marginal coverage,
width and Winkler. On this surface MSCP has the *highest* marginal coverage of all seven methods
(0.912) and the *worst* conditional coverage (worst-cell 0.725, below the do-nothing baseline).

**Both halves of the conditioning need the adaptation.** Removing the horizon axis (K=1) costs the
adaptive method 0.039 of worst-cell on ETT (31/32 configs) while *helping* the static one; the
horizon x adaptation interaction is +0.060 on ETT and +0.082 on Electricity (see
`docs/01_IDEA_LOCK_DELTA_002.md` for why the raw minimum on a 300-cell grid misleads here).

**Adaptation is visible, not just averaged** (`results/tr_ecl.json`, `figures/fig_traces.png`).
On Electricity the test block crosses a season. Static global conformal spends 17.5% of it below
0.85 coverage with ~3-week dips, bottoming at 0.775 at H=720; the adaptive conditional layer holds
0.858 through the identical window on identical forecasts. On the same-season ETT split the effect
is small and ACI alone is *worse* than doing nothing -- the interaction again.

**Whole-path coverage is priced, not promised.** Per-step methods give ~0.000 joint whole-path
coverage; restoring ~0.91 whole-path coverage costs ~10x the interval width (MaxScore layer).

**Decision layer.** Interval-gated peak flagging beats the point-forecast rule only when misses cost
>=5x false alarms (normalised cost 0.167 vs 0.362 at 10:1); at 2:1 the point rule is cheaper, and
the worst-channel interval rule is worse than doing nothing. Reported both ways.

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
