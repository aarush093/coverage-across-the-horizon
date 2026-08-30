DOC: 14_WEDGE_SCAN_LOG | OWNER: Aarush (scan executed by scheduled task) | CADENCE: monthly, first Monday
STATUS: active | LAST-UPDATED: 2026-08-30 | SUPERSEDES: none

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

## SCAN 2026-08-30 (out-of-cycle; the 2026-08-03 first-Monday scan never ran -- Q15)
Queries: CP + LTSF + conditional coverage; CP multivariate per-channel / worst-case; 2607/2608 window.
| Found | Verdict |
|---|---|
| **2607.23165** ABF-T-GLCP, Gate-Localized Conformal Prediction (25 Jul 2026) | **NEW NEAREST NEIGHBOUR to W2 -- closer than BC-ACI.** Multivariate, nonstationary, horizon-specific experts, calibration coupled to a learned gate state. Does NOT occupy: it trains its own forecasting module (not post-hoc on frozen standard backbones), selects residuals by learned representation rather than conditioning a quantile on horizon-bucket x channel, and its guarantee is "approximate local coverage under stability conditions", not distribution-free/ACI long-run. **[UNVERIFIED beyond abstract -- close read is now the top S0 item.]** |
| 2507.20941 Braun/Berta/Jordan/Bach, Multivariate Standardized Residuals for CP | Conditional coverage across output dimensions via whitening/Mahalanobis. Regression, not time series, not online. Related Work for the channel axis. |
| 2607.11470 climate-invariant group-conditional CP for solar/wind | Group-conditional x multi-horizon in energy. Trains XGBoost ensemble; groups are sites, not channels; 1-12h horizons; no online adaptation. Related Work. |
| 2509.02844 CPTC (Sun & Yu), CP with change points | Directly relevant to the traces/shift section (MET02). Related Work. |
| 2511.13608 gentle-introduction survey | Related Work framing citation. |
**Wedge verdict: W1-W4 INTACT.** R1 downgraded from "unmonitored since 17 Jul" to "monitored; one close read pending".
