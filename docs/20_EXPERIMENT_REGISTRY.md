DOC: 20_EXPERIMENT_REGISTRY | OWNER: Aarush | CADENCE: per-experiment
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: template (2026-07-17)

# 20 — EXPERIMENT REGISTRY
Rule: a stage exit criterion is NOT met until its rows are filled. An experiment isn't "done", it's "logged".
All rows below marked ✓ were read directly out of `results/results.json` at repo commit `42be4a5` on 2026-08-29. [FACT]
Grid: 2 backbones × 4 ETT datasets × H ∈ {96,192,336,720} = 32 cells; 7 methods = 224 calibration rows.

| ID | Stage | Question | Backbone×Dataset×H | Method | Seed | Key result (mean over all 32 cells) | Artifact | Date | Status |
|----|-------|----------|--------------------|--------|------|--------------------------------------|----------|------|--------|
| EXP_S1_001 | S1 | point reproduction | {DLinear,NLinear}×{ETTh1,h2,m1,m2}×{96,192,336,720} | point (closed-form LS) | 2026 | 32 fits logged; ETTh1/DLinear/96 MSE 0.3702, MAE 0.3915 | results.json `point` | 2026-08 | ✓ logged — **MSE-vs-published Δ never computed; S1 exit criterion NOT formally met** |
| EXP_S2_001 | S2 | does pooled coverage hide per-cell failure? | full grid | Global split conformal | 2026 | marginal **0.9097**, worst-cell **0.7667** → ~14 pt gap at a 0.90 target | results.json `cal` | 2026-08 | ✓ gate resolved: method-led |
| EXP_S2_002 | S2 | is per-horizon conditioning enough? | full grid | MSCP | 2026 | worst-cell **0.7251** — *worse than Global* | results.json `cal` | 2026-08 | ✓ |
| EXP_S3_001 | S3 | 2×2 factorial: conditioning × adaptation | full grid | Global / Cond / ACI / Proposed | 2026 | 0.7667 / 0.7588 / 0.7445 / **0.8657** — neither factor alone beats the do-nothing baseline; only the interaction does | results.json `cal` | 2026-08 | ✓ **core claim** |
| EXP_S3_002 | S3 | which axis actually fails? | full grid | CondC (channel-only) vs Cond (horizon+channel) | 2026 | CondC **0.7797** vs Cond 0.7588 — channel-only conditioning is the stronger single axis | results.json `cal` | 2026-08 | ✓ contradicts the horizon-first hypothesis |
| EXP_S3_003 | S3 | is the gain bought with width? | full grid | Proposed vs Global | 2026 | **No.** width 1.9245 vs 2.0857 and Winkler 2.6366 vs 2.9422 — Proposed is narrower *and* better scored | results.json `cal` | 2026-08 | ✓ strongest single line in the paper |
| EXP_S3_004 | S3 | backbone independence (C2) | Proposed, split by backbone | 2026 | DLinear 0.8664 vs NLinear 0.8651 (Δ 0.0013) | results.json `cal` | 2026-08 | ✓ but see RV06 — two linear backbones is a weak swap |
| EXP_S3_005 | S3 | whole-path (joint) coverage | full grid | all 7 | Gaussian 0.0045, Global 0.0034, Proposed **0.0005** | results.json `joint` | 2026-08 | ✓ collapse confirmed (F6); **Proposed is the WORST here** — see RV07 |
| EXP_S4_001 | S4 | bucket count K | full grid | Proposed | 2026 | 4 rows logged | results.json `kabl` | 2026-08 | ✓ |
| EXP_S4_002 | S4 | adaptation step size γ | full grid | Proposed | 2026 | 5 rows logged | results.json `gabl` | 2026-08 | ✓ |
| EXP_S4_003 | S4 | scale estimator (MAD vs std) | full grid | Proposed | 2026 | 6 rows logged | results.json `scale_abl` | 2026-08 | ✓ |
| EXP_S4_004 | S4 | calibration stride (F3 hygiene) | full grid | Proposed | 2026 | 3 rows logged | results.json `stride_abl` | 2026-08 | ✓ |
| EXP_S4_005 | S4 | rolling coverage traces (MET02) | — | Proposed vs Global | 2026 | — | **NONE — code lost (D008)** | 2026-08-29 | ✗ REBUILD |
| EXP_S4_006 | S4 | calibration-window-length ablation | — | Proposed | 2026 | — | **NONE — code lost (D008)** | 2026-08-29 | ✗ REBUILD |
| EXP_S5_001 | S5 | interval-gated peak flagging on Electricity (W4/MET08) | DLinear×Electricity(50 meters) | none/point/Global/Proposed | 2026 | reported normalised cost 1.000 / 0.641 / 0.454 / **0.391**; peaks caught 0% / 38.6% / 75.3% / **82.8%** | **NONE — code lost (D008)** | 2026-08-29 | ✗ **[UNVERIFIED] — numbers exist only as chat text. Do not cite until reproduced from pushed code.** |
| EXP_S5_002 | S5 | conditional coverage on a 300-cell grid | DLinear×Electricity | Global vs Proposed | 2026 | reported: within ±0.05 of target 274/300 vs 142/300; below 0.80 10 vs 40; **min cell 0.236 vs 0.340 (Proposed worse)** | **NONE — code lost (D008)** | 2026-08-29 | ✗ [UNVERIFIED] — same caveat |
