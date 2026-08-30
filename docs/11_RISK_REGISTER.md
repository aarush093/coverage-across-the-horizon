DOC: 11_RISK_REGISTER | OWNER: Shared | CADENCE: monthly + on trigger
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: 2026-07-17 version

# 11 — RISK REGISTER (seeded from Idea Lock §12)
| ID | Risk | Trigger | Response | Status (2026-08-29) |
|----|------|---------|----------|---------------------|
| R1 | Scooped mid-project | new preprint occupies W1–W2 | arXiv immediately after S3; shift to W3–W4 + audit spine; monthly scan | **OPEN — and overdue.** S3 is complete, which per the Lock is the arXiv trigger. No scan logged since 2026-07-17; the 2026-08-03 first-Monday scan appears to have been missed. 2604.13253 (closest to W2) is still unread. |
| R2 | Global conformal already flat at target | S2 gate output | pivot to audit-led spine | **CLOSED — did not fire.** Global is flat on POOLED marginal (0.910) but sags to 0.767 worst-cell. Conditioning is not cosmetic. Spine stays method-led. |
| R3 | BDG2 messiness sinks case study | excess missingness/outliers | fallback to Electricity benchmark; BDG2 → appendix | **ACTIVATED — but on a different trigger than written.** Fired on data *reachability* in the working environment, not on missingness (D011). The Lock's prescribed response was taken. Note the register's own trigger wording was wrong: reachability was never listed as a failure mode. |
| R4 | Reviewer flags guarantee overclaim | any finite-sample/exact conditional-coverage claim | Theory-Scope box; claim only long-run adaptive + approx bucketed conditioning | OPEN — pre-empted by F5; see 43 RV02. No Theory-Scope box drafted yet (S6 item). |
| R5 | Compute/time overrun | stage slips > 3 weeks | drop Informer; MVP = S1+S2+S3 on 4 datasets | **PARTIALLY ACTIVATED, out of spec.** MVP shape achieved (S1+S2+S3 on ETT×4). But the contraction taken was DLinear+NLinear, not the prescribed DLinear+PatchTST — see D012 and RV06. |
| R6 | Placement-season squeeze | TCS NQT window / drive spikes | same MVP contraction as R5; S5 → v2/journal | OPEN — still live. |
| **R7** | **Session-only artefacts lost** | code or results exist in a chat/sandbox and not in git | commit-or-hand-over BEFORE running (D013) | **NEW, FIRED ONCE.** 2026-08-29: full S4/S5 code layer lost to a container wipe. See 24_FAILURE_REGISTRY FR01. |
| **R8** | **S0 skipped, related work thin at write-up** | S6 drafting begins with no positioning note | write the positioning note before drafting; log the six close reads | **NEW, OPEN — high.** S0 was never exited while S1–S3 completed. Q01–Q05 remain unresolved and 2604.13253 is unread. |
