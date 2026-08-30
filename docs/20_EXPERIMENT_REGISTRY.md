DOC: 20_EXPERIMENT_REGISTRY | OWNER: Aarush | CADENCE: per-experiment
STATUS: active (was: template) | LAST-UPDATED: 2026-08-16 | SUPERSEDES: 2026-07-17 template

# 20 — EXPERIMENT REGISTRY
Rule: a stage exit criterion is NOT met until its rows are filled. An experiment isn't "done", it's "logged".
Common config: seq_len=336, seed=2026, sequential 12/4/4 split, train-only scaling, drop_last DISABLED,
calibration stride = 1 day (D007), alpha=0.10, K=6, gamma=0.02, scale = per-channel MAD.

| ID | Stage | Question | Backbone×Dataset×H | Method | Seeds | Key result | Artifact | Date | Status |
|----|-------|----------|--------------------|--------|-------|------------|----------|------|--------|
| EXP_S1_001 | S1 | Reproduce DLinear point error | M01 × DS01/02/03/04 × {96,192,336,720} | closed-form LS (D008) | 1 (deterministic) | ETTh1 0.3702/0.4041/0.4334/0.4714 — within 1.3% of published. ETTm1 0.2993/0.3340/0.3684/0.4233. ETTm2 0.1723/0.2410/0.3189/0.4581. ETTh2 0.3018/0.3972/0.4858/0.7407 (720 open, Q07) | code/pipeline.py, results.json["point"] | 2026-08-16 | DONE |
| EXP_S2_001 | S2 | Does marginal coverage hide conditional failure? | M01 × 4 DS × 4 H | Global, MSCP, ACI, Cond, Proposed | 1 | Marginal 0.901–0.910 for ALL five. Worst-cell 0.720–0.866. Gap up to 18 pts | results.json["cal"] | 2026-08-16 | DONE |
| EXP_S2_002 | S2 | DECISION GATE: coverage vs horizon step | M01 × DS01 × 720 | Global vs MSCP | 1 | Global decays 0.970→0.927 but never breaches 0.90. Failure axis = channel, not horizon. MSCP worst-cell 0.720 < Global 0.751 | fig_gate.png | 2026-08-16 | DONE — gate resolved (D009) |
| EXP_S3_001 | S3 | Does conditioning+adaptation beat all baselines? | M01 × 4 DS × 4 H | Proposed | 1 | Worst-cell 0.866 (best on all 4 datasets); cell-error 0.026 (3× better); width 1.929 vs Global 2.085 (−7.5%) | results.json["cal"] | 2026-08-16 | DONE for DLinear |
| EXP_S3_002 | S3 | Is the gain from conditioning, adaptation, or the interaction? | M01 × DS01 × 720 | gamma sweep {0,.005,.02,.05,.1} | 1 | gamma=0 → 0.652 (worse than Global). ACI-only → 0.731. Both → 0.866. Interaction confirmed; width also falls 3.57→2.36 | results.json["gabl"], fig_abl.png | 2026-08-16 | DONE |
| EXP_S3_003 | S3 | Bucket-count sensitivity (F4) | M01 × DS01 × 720 | K ∈ {4,6,8,10} | 1 | Worst-cell 0.857→0.852, width Δ<0.2%. Insensitive; K=6 default | results.json["kabl"] | 2026-08-16 | DONE |
| EXP_S3_004 | S3 | Marginal vs joint whole-path (F6/W3) | M01 × 4 DS × 4 H | Marginal, MaxScore, Bonferroni | 1 | Marginal joint 0.008@96 → 0.000@≥336. MaxScore 0.818–0.892 @3.1–3.3×. Bonferroni 0.844–0.964 @3.2–3.9× | results.json["joint"] | 2026-08-16 | DONE |
| EXP_S1_002 | S1 | PatchTST reproduction + does channel gain survive channel-independence? (Q09) | M02 × DS01/04/07 × {96,336,720} | — | [≥3 TODO] | [TODO] | [TODO] | | PLANNED — top priority |
| EXP_S1_003 | S1 | Stride sensitivity (Q08) | M01 × DS01 × 96 | stride ∈ {24, 96} | 1 | [TODO] | [TODO] | | PLANNED — cheap |
