DOC: 14_WEDGE_SCAN_LOG | OWNER: Aarush (scan executed by scheduled task) | CADENCE: monthly, first Monday
STATUS: active | LAST-UPDATED: 2026-07-17 | SUPERSEDES: none

# 14 — Wedge-Collision Scan Log
Idea Lock Change-Control standing rule: on the first Monday of each month, re-run the wedge-collision
scan and log the result in ONE line. This file is the audit trail.

FED BY: Cowork scheduled task "Wedge Scan" (self-contained prompt; carries the locked W1–W4 verbatim).
LOCATION DECISION (pending): [ ] Google Drive file (Cowork can auto-append via connector — full automation)
                             [ ] chat-Project Knowledge (manual paste from the task's run output)
Reason this matters: a Cowork scheduled task writes to files/folders/connectors, NOT to chat-Project
Knowledge. If this log lives in PK, appends are manual. If it lives in Drive, appends are automatic.

## LINE SCHEMA (one line per scan)
YYYY-MM-DD | reviewed: N | closest: <arXiv ID | "none"> — <=10 words | status: INTACT / AT-RISK (W#) / COLLIDED (W#) | action: none / shift-W3W4+audit-spine / arXiv-now / SUPERSEDE

## CHANGE-CONTROL DECODE (verbatim from Idea Lock)
- A new work occupies W1–W2  → shift weight to W3–W4 and the audit spine; if past Stage S3, post to arXiv immediately (R1).
- All four wedge components occupied → this document is superseded; begin a fresh gap search. Do NOT sunk-cost a dead wedge.
- Any scope OR cadence change → write a delta note against Idea Lock §3–5.

## THE FOUR WEDGE COMPONENTS (locked reference, so the log is self-explaining)
W1 — conditional-coverage audit of the canonical LTSF suite (ETT ×4, Electricity, Traffic, Weather, ILI), H 96–720, across Informer/DLinear/PatchTST.
W2 — post-hoc distribution-free calibration layer, horizon-bucket × channel conditioning + online (ACI/PID-family) adaptation, at that scale.
W3 — explicit marginal-vs-joint (whole-path) coverage analysis at H up to 720.
W4 — decision-level evaluation of calibrated intervals on real building-energy data under temporal shift.
Conceded as prior art (never a collision): split conformal; per-horizon split conformal (MSCP); online adaptive conformal in general.

## LOG
2026-07-17 | SETUP | log created; scan automation to be configured in Cowork; first live scan due first Monday of Aug 2026 (S0 window). No scan run yet. | status: INTACT (as of lock date 2026-07-16) | action: none

<!-- Add ONLY if you fall back to weekly-Monday + date-gate instead of true monthly scheduling:
2026-07-17 | CADENCE-DELTA | literal "first Monday" implemented as weekly-Monday schedule + in-prompt date-gate due to scheduler limits; non-substantive, no change to §3–5 scope. | action: none
-->

## NOTE
Authoritative live copy = Google Doc in Drive ("14_WEDGE_SCAN_LOG — Coverage Across the Horizon").
This bundle copy is a snapshot. 2026-07-17 independent verification of fence papers: wedge INTACT (see 50 + 32).
