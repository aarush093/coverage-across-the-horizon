DOC: 50_RESEARCH_LOG | OWNER: Aarush | CADENCE: per-session (newest first)
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: none

# 50 — RESEARCH LOG

## 2026-08-29 (session 2) — reconciliation after container loss
- Verified repo HEAD = `42be4a5`. **None of session 1's new code was ever pushed.** `decision.py`, `shift.py`, `data/electricity.py`, `data/bdg2.py`, `merge_results.py`, `run_casestudy.py` and the sharding edits are gone. Logged FR01 + D008 + R7.
- Re-verified BDG2 independently: raw fetch → 134-byte LFS pointer, declared 174,239,039 B; LFS media host → HTTP 403 `host_not_allowed`. Corrected D006's framing — this is a sandbox egress limit, **not** proof BDG2 is unusable on Aarush's own machine.
- Recomputed all headline numbers straight from `results.json`. Caught FR03: a carried-forward "0.652" for conditioning-alone; the true value is **0.7588**.
- Reconciled 10, 11, 12, 13, 20, 21, 22, 24, 43. Tracker had been stale for six weeks.
- **Verified 2×2 (mean over 2 backbones × 4 ETT × 4 H, target 0.90):** Global 0.7667 · Cond 0.7588 · ACI 0.7445 · **Proposed 0.8657**. Also CondC 0.7797, MSCP 0.7251, Gaussian 0.7762. Marginal for Proposed 0.9098. Width 1.9245 (vs Global 2.0857). Winkler 2.6366 (best). Joint 0.0005 (worst).
- New Reviewer-#2 exposures banked: RV06 (linear-only backbone swap), RV07 (Proposed has the worst joint coverage), RV08 (Electricity min-cell regression), RV09 (no S0 / no related work), RV10 (n_test = 117).

## 2026-08-29 (session 1) — S5 attempt
- Repo reproduced bit-exactly in a clean Linux container; all seven headline numbers matched.
- R3 activated, Electricity chosen as S5 surface. Decision layer written and run once. Reported cost 0.391 vs point-forecast 0.641; peaks caught 82.8% vs 38.6%.
- Session ended at a tool limit before push. See FR01 — those numbers are [UNVERIFIED] until rebuilt.

## 2026-07-17 — OS build + verification pass
- Built MVP+ OS; 14_WEDGE_SCAN_LOG created in Drive.
- arXiv verification pass: Report the Floor 2606.09473 ✓; CP survey 2601.18509 ✓; CSP 2605.03789 ✓; DeRegiME 2605.19231 ✓; O2CP 2508.13362 ✓ with title mismatch (Q01); AcMCP 2410.13115 ✓; DSCP 2503.21251 ✓; CopulaCPTS 2212.03281 ✓.
- WEDGE VERDICT: INTACT. Decisions D001–D005. Questions Q01–Q06.
