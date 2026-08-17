# Coverage Across the Horizon

**Horizon- and channel-conditional adaptive conformal calibration for long-term time-series forecasting.**

The three models that define long-term time-series forecasting — Informer, DLinear, PatchTST — all report point forecasts only. None emits an interval. This repository attaches a lightweight, post-hoc, distribution-free calibration layer on top of a *frozen* forecaster and asks a sharper question than "is it calibrated?": **calibrated where?**

The headline result: marginal coverage is uninformative. Every calibration method lands on the 90% target on average, while the weakest horizon-bucket × channel cell of most of them falls to ~0.72–0.78. Conditioning the conformal quantile on horizon bucket and channel *and* adapting it online lifts worst-cell coverage to 0.866 — with narrower intervals and the best Winkler score of the seven methods.

No new forecaster is trained. The whole study (two backbones, 32 fits) runs on CPU in ~3.5 minutes.

---

## Results (mean over 2 backbones × 4 ETT datasets × 4 horizons, target 90%)

| Method | Conditioning | Adaptive | Marginal | Worst-cell | Winkler ↓ |
|---|---|---|---:|---:|---:|
| Gaussian residual | H × C | no | 0.910 | 0.776 | 2.680 |
| Global split CP | none | no | 0.910 | 0.767 | 2.942 |
| Per-horizon (MSCP) | horizon | no | 0.912 | 0.725 | 2.765 |
| Channel-only | channel | no | 0.910 | 0.780 | 2.981 |
| Static conditional | H × C | no | 0.908 | 0.759 | 2.910 |
| Adaptive CI (ACI) | none | yes | 0.903 | 0.745 | 2.831 |
| **Proposed** | **H × C** | **yes** | **0.910** | **0.866** | **2.637** |

Key findings:
- **The gain is an interaction.** Conditioning alone (0.652 at γ=0) and adaptation alone (0.745) both fail; only the combination reaches 0.866. A fully-conditioned Gaussian interval also fails (0.776).
- **The failing axis is the channel, not the horizon.** Channel-only conditioning (0.780) beats horizon-only (0.725), and horizon-only is worse than no conditioning at all (0.767).
- **Model-independent.** Repeated on a structurally different second backbone (NLinear): ranking unchanged, Proposed scores 0.866 (DLinear) vs 0.865 (NLinear).
- **Whole-path coverage collapses** to 0.0 beyond H=336; restoring it costs ~3× the width.

See `results/results.json` and `figures/`.

> Point-forecast reproduction is within 1.3% of published DLinear/NLinear values across the grid. DLinear ETTh2 H=720 is an open item — published values for that cell disagree across papers (≈0.605–0.831); NLinear on the same cell matches published to 3 decimals, indicating the spread is a DLinear property.

---

## Quick start

```bash
pip install -r requirements.txt
python scripts/download_data.py      # fetches 4 ETT CSVs into ./data (public, no key)
python scripts/run_experiments.py    # writes results/results.json  (~210 s, CPU)
python scripts/make_figures.py       # writes figures/*.png (results + diagrams)
```

Deterministic: fixed seed 2026, sequential splits, `drop_last` disabled. Both backbones are linear and solved in closed form, so there is no gradient-descent variance — results are bit-reproducible.

---

## Layout

```
coverage_horizon/
  config.py            protocol-hygiene constants (seed, splits, stride, K, gamma)
  data/loader.py       sequential split, train-only scaling, windowing
  backbone.py          DLinear + NLinear, closed-form least-squares fit
  pipeline.py          fit -> residual tensors (H x C x t)
  calibration/
    conditional.py     Gaussian, Global, MSCP, CondC, Cond, ACI, Proposed (factorial)
    joint.py           whole-path coverage: max-score, Bonferroni
    metrics.py         marginal, worst-cell, cell-error, joint, width, Winkler
scripts/
  download_data.py  run_experiments.py  make_figures.py
docs/                 method notes
```

## Method set

The comparison is a **factorial** over conditioning (none / horizon / channel / horizon×channel) and adaptation (off / on), plus a parametric Gaussian reference. This lets the contribution be stated as an *interaction effect* rather than a bare comparison.

## Protocol hygiene (binding)

Sequential splits only · `drop_last` disabled · strided calibration windows (one seasonal day) · fixed published seed · worst-cell coverage reported beside every mean.

## Scope of the guarantee

Only two things are claimed: long-run adaptive coverage of the ACI family, and *approximate* conditioning at horizon-bucket × channel resolution. Exact finite-sample conditional coverage is impossible in general and is never claimed.

## Status

Two frozen backbones (DLinear, NLinear), the seven-method audit, the S2 decision gate, the joint-coverage analysis, the backbone-swap model-independence test, and five ablations (K, γ, scale estimator, calibration stride, conditioning grid) are complete. PatchTST and Informer backbones, the wider dataset suite, rolling-shift traces, and the building-energy case study are in progress.

## Citation

Pandit, A. & Jaggi, N. *Coverage Across the Horizon: Horizon- and Channel-Conditional Adaptive Conformal Calibration for Long-Term Time-Series Forecasting.* Working repository, 2026.

## License

MIT — see [LICENSE](LICENSE).
