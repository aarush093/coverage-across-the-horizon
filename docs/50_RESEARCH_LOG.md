DOC: 50_RESEARCH_LOG (append block, newest first) | OWNER: Aarush | CADENCE: per-session
STATUS: active | LAST-UPDATED: 2026-08-16

## 2026-08-16 — Review 1 build: S1/S2/S3 executed early, gate resolved
- TRIGGER: Review 1 on 19 Aug. Rubric = Lit/Rationale 5, Gap 5, Objectives 5, Plan 5,
  Implementation(50%)+Analysis 10, Design/Methodology 10. Plan-only doc forfeits 20/40.
- BUILT: full pipeline from scratch on real public ETT data (raw.githubusercontent, zhouhaoyi/ETDataset).
  DLinear from decomposition upward, closed-form LS fit (D008). 16 fits, 131 s CPU total.
- Five calibration methods implemented: Global split CP, MSCP, ACI (adaptive/unconditional),
  Cond (conditional/static), Proposed (conditional+adaptive). The 2×2 factorial was added deliberately
  so that the contribution claim is an interaction effect and not a bare comparison — this is what
  makes RV04 ("MSCP relabeled") unanswerable by a reviewer.
- HEADLINE: marginal coverage is uninformative. All five methods 0.901–0.910 vs 0.90 target;
  worst-cell 0.720–0.866. C1 (audit) is now MEASURED, not asserted.
- METHOD: Proposed 0.866 worst-cell, cell-error 0.026, width −7.5% vs Global. Pareto-dominant.
  Best on all four datasets independently.
- GATE (S2): resolved METHOD-LED but with the failure axis re-identified as CHANNEL not HORIZON.
  MSCP (horizon-only) is WORSE than doing nothing. Wrote DELTA_001 per Lock change-control.
  This was not a predicted branch. Logged rather than smoothed.
- JOINT (W3): per-step 90% intervals cover 0.000 of whole paths at H≥336. Restoration costs ~3×.
  F6 was correct and the magnitude is larger than expected.
- NEW OBSERVATION (not in Lock): residual scale is PERIODIC in h (daily cycle), not monotone.
  Kills any smooth parametric widening assumption. → Q11.
- DEVIATION LOGGED: calibration stride = 1 day, not strict non-overlap (D007). Strict non-overlap
  gives 3 paths at H=720. Must be disclosed in the paper + ablated (Q08).
- REFERENCE DISCIPLINE: Review 1 cites only the 16 pre-cutoff-verified works (D010). 2026 preprints
  stay out until the S0 web-resolve pass. Published DLinear ETTh1 row verified live against an AAAI
  proceedings table before being used as the reproduction benchmark.
- OPEN: Q07 (ETTh2@720 published-value spread), Q08 (stride), Q09 (PatchTST channel-independence —
  now the single most informative remaining experiment), Q10 (MaxScore over-coverage), Q11 (phase buckets).
- NEXT: submit 19 Aug. Then S0 close-reads + August wedge scan, both still outstanding. Then PatchTST.
