DOC: 24_FAILURE_REGISTRY | OWNER: Shared | CADENCE: per-failure
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: template (2026-07-17)

# 24 — FAILURE REGISTRY (what broke & why)
| ID | Stage | What failed | Root cause | Fix / verdict | Date |
|----|-------|-------------|-----------|---------------|------|
| FR01 | S4/S5 | An entire session's code layer was lost: `coverage_horizon/decision.py`, `shift.py`, `data/electricity.py`, `data/bdg2.py`, `scripts/merge_results.py`, `scripts/run_casestudy.py`, sharding edits to `run_experiments.py`, and the new `cell_p05` / `frac_within_5pt` metrics. | Work was done inside an ephemeral sandbox and never committed or handed to the user. The session hit a tool limit before the push step, and the container was wiped. [FACT — repo HEAD verified as `42be4a5` on 2026-08-29, none of the files present.] | **D008 is now binding: hand over or commit code BEFORE running it, every time.** The S5 numbers produced in that session are downgraded to [UNVERIFIED] until regenerated from pushed code. | 2026-08-29 |
| FR02 | docs | `12_PROGRESS_TRACKER` read "S1–S6 NOT STARTED" for ~6 weeks while S1–S3 were completed and Review 1 was delivered. | Cadence is "weekly"; it was never run. Doc drift is silent by construction. | Tracker rebuilt 2026-08-29. Treat any doc whose LAST-UPDATED is >3 weeks old as untrusted until reconciled. | 2026-08-29 |
| FR03 | recall | A working summary carried "conditioning alone = 0.652". The committed `results.json` gives Cond = **0.7588**. | A number was carried in prose across sessions instead of being re-read from the artefact. | Any headline number must be recomputed from `results.json` before it enters a document. Correct 2×2: Global 0.7667 / Cond 0.7588 / ACI 0.7445 / Proposed 0.8657. | 2026-08-29 |

Watch-list from Lock F-log: drop_last truncation (F7) corrupts coverage silently; overlapping calibration windows (F3) bias optimistically; 720 independent quantiles (F4) explode variance.
