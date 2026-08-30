DOC: 01_IDEA_LOCK_DELTA_001 | OWNER: Aarush | CADENCE: delta-only
STATUS: CORRECTED-BY 01_IDEA_LOCK_DELTA_002 (2026-08-30) on the "never crosses 0.90" claim and on scope-of-evidence (DLinear-only figures); its periodicity finding stands re-verified. Original text preserved unedited below. Original  active | LAST-UPDATED: 2026-08-16 | SUPERSEDES: none (amends 01_IDEA_LOCK v1.0 §3–§5 emphasis only)

# DELTA NOTE 001 — evidence-driven re-weighting inside W2
Raised by: S2 decision-gate execution, 2026-08-16 (pulled forward from late Sep).
Type: EVIDENCE change, not literature change. The wedge is NOT amended. Emphasis inside W2 is.

## What the Lock says (v1.0 §8, S2 gate)
"If global coverage sags below target at long horizons ... the paper is method-led. If global coverage
is already flat at target, conditioning is cosmetic ... and the paper pivots to audit-led."

## What the evidence actually returned
Neither branch. A third outcome:
- Global conformal coverage DOES decay along the horizon on ETTh1 H=720 (≈0.970 over the first day of
  the path → ≈0.927 over the last) but NEVER crosses the 0.90 target. The horizon axis is real but
  not load-bearing.
- The axis that breaks is the CHANNEL. Worst-cell coverage under global conformal = 0.751 (mean over
  4 datasets × 4 horizons), against a 0.90 target.
- MSCP (per-horizon conditioning ALONE) is WORSE than doing nothing: worst-cell 0.720 vs Global 0.751.
  It sharpens the intact axis while pooling the broken one.
- The horizon term still contributes once channel conditioning is present (Cond+ACI = 0.866 vs
  ACI alone = 0.731), so the interaction is real. The horizon term is not dropped.

## Consequence for the wedge (W1–W4 all UNCHANGED)
W2 still reads "horizon-bucket × channel conditioning with online adaptation". The re-weighting is in
how the paper ARGUES it: the channel term and the conditioning×adaptation INTERACTION carry the claim;
the horizon term is supporting, not headline. Framing "horizon-conditional" first would now be
contradicted by our own Table 11.2.

## Second evidence item (new, not in Lock)
Residual scale is PERIODIC in h (clear daily cycle in per-horizon width), not monotonically growing.
Any monotone-widening assumption is wrong on these benchmarks. Log-spaced buckets + adaptation absorb
this; a smooth parametric widening rule would not. Worth one sentence in the paper.

## Status
Wedge: INTACT. No scope change. No contribution claim (C1–C4) edited. Emphasis note only.
