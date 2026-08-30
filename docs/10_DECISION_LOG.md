DOC: 10_DECISION_LOG | OWNER: Aarush | CADENCE: per-decision
STATUS: active | LAST-UPDATED: 2026-08-30 (rev4) | SUPERSEDES: rev3 (2026-08-29)

# 10 — DECISION LOG
Format: ID | date | context | options | decision | rationale | reversibility | affected docs.

D001 | 2026-07-17 | OS build order | full-25 vs MVP-first | MVP-first + lazy instantiation | matches the Lock's own anti-creep discipline | reversible | 00_INDEX
D002 | 2026-07-17 | Wedge-scan automation | calendar vs Cowork task | Cowork scheduled task, monthly, W1–W4 baked in verbatim | prevents the drift seen when the wedge was reconstructed from memory | reversible | 14, 02
D003 | 2026-07-17 | Wedge-scan log location | PK vs Google Drive | Google Drive | Cowork writes to connectors, not chat-PK | costly-to-reverse | 14, 00_INDEX
D004 | 2026-07-17 | Verify post-cutoff arXiv IDs | trust vs verify | verified the load-bearing gap papers | de-risks 8–12 months; wedge INTACT | done | 32, 14, 13
D005 | 2026-07-17 | Wedge-scan log feeding | auto-append vs manual | manual paste; Cowork run-history is the primary audit trail | no in-place Google Docs write tool available | reversible | 14, 00_INDEX
D006 | 2026-08-29 | S5 case-study surface | BDG2 vs Electricity vs drop S5 | **Electricity primary; BDG2 a data-gated extension** | BDG2 meters are Git LFS: raw fetch returns a 134-byte pointer declaring 174,239,039 B, LFS host 403 `host_not_allowed` from the sandbox [FACT, 2026-08-29]. That is an environment limit, not a property of BDG2 — a local `git lfs pull` is untested and expected to work. | reversible on a local LFS checkout | 21, 11 (R3), 12
D007 | 2026-08-29 | Backbone set actually used | Lock names DLinear+PatchTST+Informer | **DLinear + NLinear** | closed-form linear fits made the study reproducible in ~105 s. **Not what R5 authorised** — R5 said drop Informer and keep PatchTST. Logged as a deviation, and it weakens C2 (RV06). | reversible at GPU cost | 22, 43, 12
D008 | 2026-08-29 | Where session-written code lives | push at the end vs hand over first | **commit or hand over BEFORE running** | enforcement after FR01 destroyed a full session of S4/S5 code | binding | 02, 24
D009 | 2026-08-30 | How coverage is reported on wide grids | worst-cell alone vs worst-cell + distribution | **report `cell_p05`, `frac_within_5pt` and `frac_below_80` alongside the raw minimum** | a minimum over a 300-cell grid and a minimum over a 42-cell grid are not comparable quantities; comparing them anyway is the easiest mistake available here, and it cuts both ways — it can flatter or damn the method. Metrics added in the case-study script, `metrics.py` left untouched so the committed ETT numbers cannot move. | reversible | 23, 20, 43 (RV10)

## Pending decisions (surfaced, not yet made):
- P01: Is "O2CP / 2508.13362" the intended paper given the title mismatch? — S0.
- P02: Does S0 get run properly before S6, or is it formally declared skipped?
- P03: PatchTST reinstated as a third backbone, or C2 narrowed in writing? (RV06)
- **P04: The Lock says post to arXiv after S3. S3 and S5 are both complete and R1 has been open since July with no scan since 2026-07-17. Post now, or wait for S4 rebuild + S6?**
