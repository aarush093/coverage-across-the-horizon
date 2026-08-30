DOC: 10_DECISION_LOG (append block) | OWNER: Aarush | CADENCE: per-decision
STATUS: active | LAST-UPDATED: 2026-08-16 (rev3) | SUPERSEDES: rev2

# APPEND TO 10_DECISION_LOG — D006 to D010

D006 | 2026-08-16 | Schedule pull-forward for Review 1 | wait for Sep per Lock §8 vs execute S1–S3 now | executed S1 (partial), S2 (complete), S3 (partial) in August | Review 1 rubric carries Implementation(50%)+Analysis at 10 marks and Design/Methodology at 10; a plan-only document scores badly on 20 of 40 marks. Compute cost was 131s CPU, so the pull-forward cost nothing | reversible (stages re-run at full scope in Sep) | 12_PROGRESS_TRACKER, 20_EXPERIMENT_REGISTRY

D007 | 2026-08-16 | Calibration window stride | strict non-overlap (stride=H) vs stride=1 seasonal day | stride = 24 steps (ETTh) / 96 steps (ETTm), i.e. one day | strict non-overlap gives only 3 calibration paths at H=720 on a 2880-row val block, which is unusable for a 90% quantile. One-day stride decorrelates the daily cycle and yields 91–120 paths. This is a DEVIATION from the strictest reading of Lock F3 and must be stated in the paper, with a stride ablation at H=96 where sample size permits | reversible | 21_DATASET_REGISTRY, 43_REVIEWER_2

D008 | 2026-08-16 | DLinear fitting method | Adam SGD per reference impl vs closed-form least squares | closed-form ridge least squares | DLinear is linear and the loss is MSE, so the normal equations return the GLOBAL optimum of exactly the objective SGD approximates. Removes lr/epoch/early-stopping as confounds and makes the backbone bit-reproducible. Result validates it: ETTh1 within 1.3% of published at all four horizons | reversible | 22_MODEL_REGISTRY

D009 | 2026-08-16 | S2 DECISION GATE resolution | method-led vs audit-led | METHOD-LED, with emphasis re-weighted from horizon axis to channel axis | see 01_IDEA_LOCK_DELTA_001. Global conformal never breaches target along the horizon; it breaches badly across channels (worst-cell 0.751). MSCP alone is worse than nothing | costly-to-reverse (sets paper spine) | 01_IDEA_LOCK_DELTA_001, 43_REVIEWER_2

D010 | 2026-08-16 | Reference list for Review 1 submission | include full Lock §4 fence incl. 2026 preprints vs pre-cutoff-verified only | pre-cutoff-verified only (16 refs) | 02_OPERATING_RULES forbids confirming a reference from memory. DeRegiME/Report the Floor/CP-survey remain [UNVERIFIED] until the S0 web-resolve pass; an unverified citation in a graded document is an unnecessary risk | reversible after S0 verification | 30_READING_QUEUE, 32_LIT_MATRIX

## Pending decisions:
- P01: O2CP / 2508.13362 arXiv-title mismatch. Resolve at S0. (unchanged)
- P02: Does the channel-conditioning gain survive a channel-INDEPENDENT backbone (PatchTST)? If the gain
  shrinks, the claim narrows to channel-mixing backbones. Decide after S3 backbone swap. (see Q09)
