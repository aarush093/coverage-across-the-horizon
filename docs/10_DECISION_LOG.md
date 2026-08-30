DOC: 10_DECISION_LOG | OWNER: Aarush | CADENCE: per-decision
STATUS: active | LAST-UPDATED: 2026-08-30 (rev5) | SUPERSEDES: rev3 of 2026-08-16 (append block) AND rev4 of 2026-08-30; this is the first file to contain BOTH lineages

# 10 - DECISION LOG
Format: ID | date | context | options | decision | rationale | reversibility | affected docs.

**RENUMBERING NOTICE, 2026-08-30.** Two decision logs existed in parallel and their IDs
collided. The 2026-08-16 session (S1-S3 pull-forward, Review 1) issued D006-D010. The
2026-08-29/30 sessions issued their own D006-D009 without sight of that block, because
the copy in Project Knowledge was still the 2026-07-17 version ending at D005. Both sets
are real. The 2026-08-16 block keeps D006-D010 by seniority; the later four are
renumbered **D006->D011, D007->D012, D008->D013, D009->D014** and every reference across
docs/ has been updated. Logged as FR06. Nothing was discarded.

D001 | 2026-07-17 | OS build order | full-25 vs MVP-first | MVP-first + lazy instantiation | matches the Lock's own anti-creep discipline | reversible | 00_INDEX
D002 | 2026-07-17 | Wedge-scan automation | calendar vs Cowork task | Cowork scheduled task, monthly, W1–W4 baked in verbatim | prevents the drift seen when the wedge was reconstructed from memory | reversible | 14, 02
D003 | 2026-07-17 | Wedge-scan log location | PK vs Google Drive | Google Drive | Cowork writes to connectors, not chat-PK | costly-to-reverse | 14, 00_INDEX
D004 | 2026-07-17 | Verify post-cutoff arXiv IDs | trust vs verify | verified the load-bearing gap papers | de-risks 8–12 months; wedge INTACT | done | 32, 14, 13
D005 | 2026-07-17 | Wedge-scan log feeding | auto-append vs manual | manual paste; Cowork run-history is the primary audit trail | no in-place Google Docs write tool available | reversible | 14, 00_INDEX

D006 | 2026-08-16 | Schedule pull-forward for Review 1 | wait for Sep per Lock §8 vs execute S1–S3 now | executed S1 (partial), S2 (complete), S3 (partial) in August | Review 1 rubric carries Implementation(50%)+Analysis at 10 marks and Design/Methodology at 10; a plan-only document scores badly on 20 of 40 marks. Compute cost was 131s CPU, so the pull-forward cost nothing | reversible (stages re-run at full scope in Sep) | 12_PROGRESS_TRACKER, 20_EXPERIMENT_REGISTRY

D007 | 2026-08-16 | Calibration window stride | strict non-overlap (stride=H) vs stride=1 seasonal day | stride = 24 steps (ETTh) / 96 steps (ETTm), i.e. one day | strict non-overlap gives only 3 calibration paths at H=720 on a 2880-row val block, which is unusable for a 90% quantile. One-day stride decorrelates the daily cycle and yields 91–120 paths. This is a DEVIATION from the strictest reading of Lock F3 and must be stated in the paper, with a stride ablation at H=96 where sample size permits | reversible | 21_DATASET_REGISTRY, 43_REVIEWER_2

D008 | 2026-08-16 | DLinear fitting method | Adam SGD per reference impl vs closed-form least squares | closed-form ridge least squares | DLinear is linear and the loss is MSE, so the normal equations return the GLOBAL optimum of exactly the objective SGD approximates. Removes lr/epoch/early-stopping as confounds and makes the backbone bit-reproducible. Result validates it: ETTh1 within 1.3% of published at all four horizons | reversible | 22_MODEL_REGISTRY

D009 | 2026-08-16 | S2 DECISION GATE resolution | method-led vs audit-led | METHOD-LED, with emphasis re-weighted from horizon axis to channel axis | see 01_IDEA_LOCK_DELTA_001. Global conformal never breaches target along the horizon; it breaches badly across channels (worst-cell 0.751). MSCP alone is worse than nothing | costly-to-reverse (sets paper spine) | 01_IDEA_LOCK_DELTA_001, 43_REVIEWER_2

D010 | 2026-08-16 | Reference list for Review 1 submission | include full Lock §4 fence incl. 2026 preprints vs pre-cutoff-verified only | pre-cutoff-verified only (16 refs) | 02_OPERATING_RULES forbids confirming a reference from memory. DeRegiME/Report the Floor/CP-survey remain [UNVERIFIED] until the S0 web-resolve pass; an unverified citation in a graded document is an unnecessary risk | reversible after S0 verification | 30_READING_QUEUE, 32_LIT_MATRIX

D011 | 2026-08-29 | S5 case-study surface | BDG2 vs Electricity vs drop S5 | **Electricity primary; BDG2 a data-gated extension** | BDG2 meters are Git LFS: raw fetch returns a 134-byte pointer declaring 174,239,039 B, LFS host 403 `host_not_allowed` from the sandbox [FACT, 2026-08-29]. That is an environment limit, not a property of BDG2 — a local `git lfs pull` is untested and expected to work. | reversible on a local LFS checkout | 21, 11 (R3), 12

D012 | 2026-08-29 | Backbone set actually used | Lock names DLinear+PatchTST+Informer | **DLinear + NLinear** | closed-form linear fits made the study reproducible in ~105 s. **Not what R5 authorised** — R5 said drop Informer and keep PatchTST. Logged as a deviation, and it weakens C2 (RV06). | reversible at GPU cost | 22, 43, 12

D013 | 2026-08-29 | Where session-written code lives | push at the end vs hand over first | **commit or hand over BEFORE running** | enforcement after FR01 destroyed a full session of S4/S5 code | binding | 02, 24

D014 | 2026-08-30 | How coverage is reported on wide grids | worst-cell alone vs worst-cell + distribution | **report `cell_p05`, `frac_within_5pt` and `frac_below_80` alongside the raw minimum** | a minimum over a 300-cell grid and a minimum over a 42-cell grid are not comparable quantities; comparing them anyway is the easiest mistake available here, and it cuts both ways — it can flatter or damn the method. Metrics added in the case-study script, `metrics.py` left untouched so the committed ETT numbers cannot move. | reversible | 23, 20, 43 (RV10)

## Pending decisions (surfaced, not yet made):
- P01 | O2CP / 2508.13362 arXiv-title mismatch. **RESOLVED 2026-08-30** - the paper was
  retitled between v1 and v2; same authors, same ID. Cite v2. See LIT_2508.13362_o2cp.
- P02 | Does the channel-conditioning gain survive a channel-INDEPENDENT backbone
  (PatchTST)? If it shrinks, the claim narrows to channel-mixing backbones. **Open since
  2026-08-16 and still the single most informative experiment left** (see Q14). This
  supersedes the vaguer P03 raised on 2026-08-29; they are the same question and P02 is
  the sharper form.
- P04 | The Lock says post to arXiv after S3. S3, S4 and S5 are all complete and R1 has
  been open since July with no wedge scan logged since 2026-07-17. Post now, or wait for S6?
- P05 | `figures/fig_abl.png` plots the own-grid K curve that FR04 shows is confounded,
  and it was shown at Review 1. Replace with `fig_kabl_fixed.png`, or caption it?
