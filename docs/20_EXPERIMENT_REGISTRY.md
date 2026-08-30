DOC: 20_EXPERIMENT_REGISTRY | OWNER: Aarush | CADENCE: per-experiment
STATUS: active | LAST-UPDATED: 2026-08-30 (rev5) (rev2) | SUPERSEDES: rev1 (2026-08-30)

# 20 — EXPERIMENT REGISTRY
Rule: a stage exit criterion is NOT met until its rows are filled.
ETT rows read from `results/results.json` @ `42be4a5`. Electricity rows read from
`results/casestudy.json` @ `481b90f`, means over 2 backbones × 4 horizons. [FACT, 2026-08-30]
Horizon-ablation rows (EXP_S4_007, EXP_S5_008) read from `results/horizon_ablation.json` @ `f35e429`
and `results/ha_ecl.json` @ `e231c21`. Both are scored on a **fixed K=6 grid** (`worst_ref`); the
own-grid column (`worst_own`) is recorded in the same files only to size the FR04 confound and must
never be compared across K. [FACT, 2026-08-30]

## Main study — ETT ×4, 42-cell grid, target 0.90
| ID | Question | Method | Key result | Status |
|----|----------|--------|------------|--------|
| EXP_S1_001 | point reproduction | closed-form LS | 32 fits; ETTh1/DLinear/96 MSE 0.3702 | ✓ (Δ-vs-published never computed) |
| EXP_S1_002 | PatchTST reproduction -- does the channel gain survive a channel-INDEPENDENT backbone? (Q09, P02) | M02 x DS01/04/07 x {96,336,720} | point + full factorial | [TODO] | **PLANNED -- open since 2026-08-16 and still the single most informative experiment left.** PatchTST treats channels independently by construction; if the channel axis is where calibration breaks, the gain either shrinks (it already separates channels) or grows (it never shares statistical strength). Either answer is publishable and it settles RV06. | [TODO] |
| EXP_S1_003 | Stride sensitivity -- does the audit finding survive strict non-overlap? (Q08) | M01 x DS01 x H=96 | stride in {24, 96} | 1 | **PLANNED -- cheap.** D007 records stride=24 as a deviation from the strictest reading of Lock F3. If the worst-cell ordering flips at stride=96, D007 becomes a threat rather than a documented deviation. | [TODO] |
| EXP_S2_001 | does pooled coverage hide per-cell failure? | Global | marginal 0.9097, worst-cell 0.7667 | ✓ gate → method-led |
| EXP_S2_002 | is per-horizon conditioning enough? | MSCP | 0.7251 — worse than Global | ✓ |
| EXP_S3_001 | 2×2 factorial | Global/Cond/ACI/Proposed | 0.7667 / 0.7588 / 0.7445 / **0.8657** | ✓ core claim |
| EXP_S3_002 | which axis fails? | CondC vs Cond | 0.7797 vs 0.7588 — channel is the stronger axis | ✓ |
| EXP_S3_003 | bought with width? | Proposed vs Global | width 1.9245 vs 2.0857; Winkler 2.6366 vs 2.9422 | ✓ narrower AND better |
| EXP_S3_004 | backbone independence | Proposed by backbone | DLinear 0.8664 / NLinear 0.8651 | ✓ but weak swap (RV06) |
| EXP_S3_005 | whole-path coverage | all 7 | Proposed 0.0005, lowest of all | ✓ collapse (RV07) |
| EXP_S4_001–004 | K / γ / scale / stride ablations | Proposed | 4+5+6+3 rows logged | ✓ |
| EXP_S4_005 | rolling coverage traces (MET02) -- does adaptation matter under shift? | Global vs ACI vs Proposed, coverage per test path, 30-path rolling mean | **Electricity (8 configs): decisive.** Global spends **17.5%** of the test period below 0.85 with dips lasting **~3 weeks**; ACI and Proposed spend **0.0%**, longest dip **0**. Worst window Global 0.8147 vs Proposed 0.8606. **The failure sits at a fixed calendar point** -- Global's worst window falls at path ~163-164 in 7 of 8 configs (75-86% through the test block, both backbones), deepening to **0.7750** at H=720 while Proposed holds **0.8579** in the identical window. **ETT (32 configs): much weaker**, as a same-season split predicts -- Global 16.0% below 0.85, ACI **17.1%** (worse than doing nothing), Proposed 11.9%. | ✓ **S4 criterion answered.** `results/tr_ecl.json`, `tr_ett.json` |
| EXP_S4_006 | calibration-window length -- does the advantage depend on data volume? | block truncated from the front, most recent paths kept, scored on the fixed K=6 grid | **Proposed leads at every size on both surfaces.** ETT at n_cal=28: Proposed 0.7461 vs best baseline 0.6685. **On Electricity every baseline plateaus while Proposed keeps scaling** -- across a fourfold increase in calibration data Global gains +0.034, MSCP +0.008, but Proposed gains **+0.200** (0.6307 -> 0.8306) and has not saturated. Baseline failure is structural; ours is statistical. **Also settles Q16:** holding n_cal at 80, H=96 gives MaxScore joint 0.9259 against H=720's 0.8947, so the 0.944 -> 0.895 decay is ~62% horizon and ~38% sample size. At H=720, n_cal 80 -> 40 halves joint coverage (0.8947 -> 0.5632). | ✓ last FR01 gap closed. `results/cw_ett.json`, `cw_ecl.json` |
| **EXP_S4_007** | **does the horizon axis earn its place once adaptation is present?** | K ∈ {1,2,4,6,8,10} × Cond/Proposed, 32 configs, fixed K=6 scoring grid | `buckets(H,1)` collapses the horizon term, so Cond@K=1 **≡ CondC exactly in 32/32** and Proposed@K=1 is channel-only + adaptation — the arm the factorial never ran. Adding the horizon axis **hurts static (0.7797→0.7588, −0.0209) and helps adaptive (0.8263→0.8657, +0.0394)**; interaction **+0.0603**, sign test **31/32**. Not bought with width: Proposed width 1.9406→1.9245, Winkler 2.6943→2.6366. Full sweep 0.8263/0.8198/0.8350/**0.8657**/0.8560/0.8601. **Reproduces the committed Proposed mean 0.8657 at K=6 to 4 dp** (0.865746). | ✓ **second interaction; corrects DELTA_001 (see DELTA_002)** |

## Case study — Electricity, 50 meters, 300-cell grid, target 0.90
| ID | Question | Method | Key result (mean of 8 configs) | Status |
|----|----------|--------|-------------------------------|--------|
| EXP_S5_001 | does the interaction survive a harder surface? | 2×2 factorial | Global 0.5757 · Cond 0.4621 · ACI 0.6177 · **Proposed 0.8306**. Interaction term **+0.327** on worst-cell, vs **+0.129** on ETT | ✓ **strongest result in the project** |
| EXP_S5_002 | grid-distribution comparison (wide vs narrow grid) | Proposed vs Global | within ±5pt of target **0.98 vs 0.53**; cells below 0.80 **0.0017 vs 0.0488** (≈4 of 2400 cells vs ≈117) | ✓ |
| EXP_S5_003 | does grid calibration degrade with horizon? | Proposed vs Global | Global 0.58→0.45 from H=96 to 720; Proposed 0.98→0.98 | ✓ horizon-invariant |
| EXP_S5_004 | is the width earned? | Winkler, all 7 | Proposed **1.4083** — best of seven (ACI 1.5152, Global 1.5264, Gaussian 1.6702), despite being 7–13% wider than Global | ✓ answers "you just widened it" |
| EXP_S5_005 | whole-path coverage and its price (W3) | joint layers | per-step methods **0.000** whole-path at every H. MaxScore reaches 0.944 (H=96) but decays to **0.842–0.895** at H=720, all at **≈10× width** | ✓ W3 quantified; note the decay (Q16) |
| EXP_S5_006 | decision-level value (W4/MET08) | cost sweep, 5 ratios | at miss:FA = 10, mean normalised cost Point **0.362** → Global 0.175 → Proposed **0.167**; recall 0.663 → 0.949 → 0.964. Proposed cheaper than Global in **8/8** configs. **At ratio 2 the point forecast wins (0.463 vs 0.692).** | ✓ **conditional** result, both directions reported |
| EXP_S5_007 | worst-channel decision cost | same | Point 1.00 · Global 2.04 · Proposed **2.35** at ratio 10 — both interval rules are worse than doing nothing on the worst meter, and Proposed is the worst of the three | ✓ **negative result** (RV13) |
| **EXP_S5_008** | **does the EXP_S4_007 horizon interaction survive the wide surface?** | K ∈ {1,6} × Cond/Proposed, 8 configs, fixed K=6 grid | **Static replicates and is worse: 0.5473→0.4621 (−0.0853)** vs −0.0209 on ETT. **Adaptive does NOT replicate: 0.8340→0.8306 (−0.0034), sign test 4/8.** The mean hides a clean, backbone-consistent **horizon reversal** — K=1 wins at H=96/192 (0.8287·0.8408·0.8333·0.8455 vs 0.7940·0.7995·0.7940·0.7995), K=6 wins at H=336/720 (0.8392·0.8349·0.8427·0.8066 vs 0.8754·0.8649·0.8754·0.8417), 4/4 each way. **But every distributional metric prefers K=6**: within ±5pt **0.625→0.977**, cell_p05 0.8715→0.8806, Winkler 1.4220→**1.4083**, width 0.9451→0.9420. Worst-cell alone is a wash; D014 is exactly why. All six K=6 methods reproduce `casestudy.json` **exactly** (diff 0.000000). | ✓ **partial replication — report the reversal, do not average it away** (Q18) |

## Diagnostics against anticipated attacks
| ID | Question | Method | Key result | Status |
|----|----------|--------|------------|--------|
| EXP_S4_008 | do symmetric intervals pay the bias overhead BC-ACI describes? (RV16 / Q20) | per-cell residual mean estimated on the calibration block only, then a leakage-free re-centring | **Splits by backbone -- the pooled number is misleading.** DLinear: abs(b) = 16.5% of width on ETT, persistent (r = +0.579 ETT, +0.731 ECL), growing 0.076 -> 0.257 across H; worst config DLinear/ETTh2/H=720 returns 11.2% width. NLinear: abs(b) = 4.2%, no persistence (r = -0.044 / -0.595). Pooled: -1.52% width, worst-cell 0.8657 -> 0.8648. **Re-centring buys width, never coverage** -- even on the worst config worst-cell moves the wrong way (0.8547 -> 0.8451). | ✓ closes RV16; strengthens RV06 |
