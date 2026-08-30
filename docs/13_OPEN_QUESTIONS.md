DOC: 13_OPEN_QUESTIONS (append block) | OWNER: Shared | CADENCE: continuous
STATUS: active | LAST-UPDATED: 2026-08-16

# APPEND TO 13_OPEN_QUESTIONS — Q07 to Q11 (raised by the 2026-08-16 execution)

| ID | Question | Raised | Owner | Status |
|----|----------|--------|-------|--------|
| Q07 | ETTh2 @ H=720: we measure MSE 0.7407. Published DLinear values for this exact cell disagree across papers (≈0.605 to ≈0.831). Which is the canonical reference, and is the spread a seq_len (336 vs 96) difference? | 2026-08-16 | Aarush | OPEN — resolve before claiming S1 exit |
| Q08 | Stride sensitivity: does the audit finding survive stride = H (strict non-overlap) at H=96, where sample size still permits it? If worst-cell ordering flips, D007 becomes a threat not a deviation. | 2026-08-16 | Aarush | OPEN — cheap, run at S1 |
| Q09 | PatchTST is channel-INDEPENDENT by construction. If the channel axis is where calibration breaks, does a channel-independent backbone shrink the gain (because it already treats channels separately) or grow it (because it never shares statistical strength)? This is now the single most informative experiment left. | 2026-08-16 | Aarush | OPEN — S3, top priority |
| Q10 | MaxScore joint coverage OVER-covers (0.876–0.892 vs 0.90 target at short H, 1.000 on ETTh1@720). Is the calibration block systematically more volatile than the test block, or is n_cal ≈ 91 paths simply too few for a max-statistic quantile? | 2026-08-16 | Aarush | OPEN — S4 |
| Q11 | Residual scale is periodic in h with a daily cycle. Would seasonal-phase buckets (hour-of-day) beat log-spaced horizon buckets, or is that a third conditioning axis and therefore scope creep? | 2026-08-16 | Aarush | OPEN — test at S4; check against Lock §3–5 before adopting |
