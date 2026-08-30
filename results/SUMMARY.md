DOC: SUMMARY | OWNER: generated | CADENCE: regenerate before any writing
STATUS: generated 2026-08-30 by `scripts/make_summary.py` | SUPERSEDES: any hand-typed number
# RESULTS SUMMARY -- every number generated, none typed
Regenerate this file before quoting anything. If a number in the paper disagrees with this file, this file is right.

## 1. Main study -- ETT x4, 42-cell grid, target 0.90
Source: `results/results.json` -> `cal`, mean over 32 configs (2 backbones x 4 datasets x 4 horizons).

| method | marginal | worst-cell | width | Winkler | joint |
| --- | --- | --- | --- | --- | --- |
| Gaussian | 0.9096 | 0.7762 | 2.0254 | 2.6804 | 0.0045 |
| Global | 0.9097 | 0.7667 | 2.0857 | 2.9422 | 0.0034 |
| MSCP | 0.9123 | 0.7251 | 2.0392 | 2.7649 | 0.0018 |
| CondC | 0.9099 | 0.7797 | 2.1711 | 2.9806 | 0.0034 |
| Cond | 0.9084 | 0.7588 | 2.1304 | 2.9095 | 0.0010 |
| ACI | 0.9031 | 0.7445 | 1.8742 | 2.8310 | 0.0016 |
| Proposed | 0.9098 | 0.8657 | 1.9245 | 2.6366 | 0.0005 |

**Conditioning x adaptation interaction:** `P - C - A + G` = 0.8657 - 0.7588 - 0.7445 + 0.7667 = **+0.1291**

## 2. Case study -- Electricity, 50 meters, 300-cell grid
Source: `results/casestudy.json` -> `cal`, mean over 8 configs. Grid statistics per D009.

| method | marginal | worst-cell | p05 | within 5pt | below .80 | width | Winkler |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gaussian | 0.8330 | 0.4270 | 0.6314 | 0.5000 | 0.2471 | 0.8503 | 1.6702 |
| Global | 0.8644 | 0.5757 | 0.7995 | 0.5337 | 0.0488 | 0.8568 | 1.5264 |
| MSCP | 0.8472 | 0.5382 | 0.7158 | 0.5108 | 0.1938 | 0.8402 | 1.5925 |
| CondC | 0.8629 | 0.5473 | 0.7860 | 0.5246 | 0.0675 | 0.8729 | 1.5456 |
| Cond | 0.8610 | 0.4621 | 0.6725 | 0.5217 | 0.1708 | 0.8702 | 1.5417 |
| ACI | 0.8921 | 0.6177 | 0.8353 | 0.4883 | 0.0233 | 0.9568 | 1.5152 |
| Proposed | 0.8964 | 0.8306 | 0.8806 | 0.9771 | 0.0017 | 0.9420 | 1.4083 |

**Interaction on Electricity:** **+0.3264** (ETT: +0.1291)

### Whole-path coverage and its price (W3)

| layer | joint coverage | width ratio |
| --- | --- | --- |
| Marginal | 0.0000 | 1.00x |
| MaxScore | 0.9124 | 10.16x |
| Bonferroni | 0.9130 | 10.19x |

### Decision layer (W4 / MET08) -- normalised cost, 1.0 = flag nothing

| miss:false-alarm | Point | Interval:Global | Interval:Proposed |
| --- | --- | --- | --- |
| 2:1 | 0.4625 / 1.05 | 0.6703 / 8.36 | 0.6919 / 10.23 |
| 5:1 | 0.3872 / 1.00 | 0.2988 / 3.62 | 0.2981 / 4.32 |
| 10:1 | 0.3621 / 1.00 | 0.1749 / 2.04 | 0.1668 / 2.35 |
| 20:1 | 0.3495 / 1.00 | 0.1130 / 1.25 | 0.1012 / 1.37 |
| 50:1 | 0.3420 / 1.00 | 0.0758 / 0.97 | 0.0618 / 1.00 |

Cell format: mean cost / worst-channel cost. **Interval-gating wins only at ratios >=5** -- at 2:1 the point forecast is cheaper.

## 3a. Horizon-axis ablation -- ETT
Source: `results/horizon_ablation.json`, 32 configs, scored on the FIXED K=6 grid (`worst_ref`). K=1 collapses the horizon axis.

| arm | K=1 | K=2 | K=4 | K=6 | K=8 | K=10 |
| --- | --- | --- | --- | --- | --- | --- |
| Cond (static) | 0.7797 | 0.7665 | 0.7637 | 0.7588 | 0.7598 | 0.7611 |
| Proposed (adaptive) | 0.8263 | 0.8198 | 0.8350 | 0.8657 | 0.8560 | 0.8601 |
| own-grid, Proposed | 0.8717 | 0.8710 | 0.8676 | 0.8657 | 0.8640 | 0.8616 |

Horizon axis: **-0.0209 static, +0.0394 adaptive**. The horizon x adaptation interaction is **+0.0603** -- that is the quantity the method claims, not the adaptive column alone.

## 3b. Horizon-axis ablation -- Electricity
Source: `results/ha_ecl.json`, 8 configs, scored on the FIXED K=6 grid (`worst_ref`). K=1 collapses the horizon axis.

| arm | K=1 | K=6 |
| --- | --- | --- |
| Cond (static) | 0.5473 | 0.4621 |
| Proposed (adaptive) | 0.8340 | 0.8306 |
| own-grid, Proposed | 0.8767 | 0.8306 |

Horizon axis: **-0.0853 static, -0.0034 adaptive**. The horizon x adaptation interaction is **+0.0818** -- that is the quantity the method claims, not the adaptive column alone.

## 4. Bias diagnostic (RV16 / EXP_S4_008)
Source: `results/bias_check.json`, `results/bias_ecl.json`. Bias estimated on the calibration block only.

| surface | backbone | abs(bias) / width | persistence r | sign agree | width if re-centred |
| --- | --- | --- | --- | --- | --- |
| ETT | DLinear | 0.1648 | 0.579 | 0.691 | -2.61% |
| ETT | NLinear | 0.0421 | -0.044 | 0.615 | -0.44% |
| Electricity | DLinear | 0.0550 | 0.731 | 0.686 | 0.18% |
| Electricity | NLinear | 0.0235 | -0.595 | 0.337 | 0.49% |

## 5. Rolling coverage traces (MET02 / EXP_S4_005)
Source: `results/tr_ett.json`, `results/tr_ecl.json`. 30-path trailing window; paths are one per day.

| surface | method | mean | worst window | % below .85 | longest dip |
| --- | --- | --- | --- | --- | --- |
| ETT | Global | 0.9097 | 0.8585 | 16.0% | 13.2 |
| ETT | ACI | 0.9031 | 0.8587 | 17.1% | 8.2 |
| ETT | Proposed | 0.9098 | 0.8649 | 11.9% | 7.4 |
| Electricity | Global | 0.8644 | 0.8147 | 17.5% | 21.8 |
| Electricity | ACI | 0.8921 | 0.8588 | 0.0% | 0.0 |
| Electricity | Proposed | 0.8964 | 0.8606 | 0.0% | 0.0 |

## 6. Calibration-window length (EXP_S4_006)
Source: `results/cw_ett.json`, `results/cw_ecl.json`. Block truncated from the front, keeping the most recent paths.

**ETT** -- worst-cell by calibration fraction

| method | 25% | 50% | 75% | 100% |
| --- | --- | --- | --- | --- |
| Global | 0.6577 | 0.7424 | 0.7741 | 0.7667 |
| MSCP | 0.5487 | 0.6254 | 0.7084 | 0.7251 |
| CondC | 0.6676 | 0.7379 | 0.7815 | 0.7797 |
| Cond | 0.6200 | 0.6560 | 0.7511 | 0.7588 |
| ACI | 0.6685 | 0.7247 | 0.7496 | 0.7445 |
| Proposed | 0.7461 | 0.7950 | 0.8611 | 0.8657 |
| _n_cal_ | 28 | 56 | 84 | 112 |

MaxScore whole-path coverage: 25% -> 0.6978, 50% -> 0.8130, 75% -> 0.8860, 100% -> 0.8772
