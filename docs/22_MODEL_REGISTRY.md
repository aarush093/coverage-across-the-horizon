DOC: 22_MODEL_REGISTRY | OWNER: Aarush | CADENCE: per-model
STATUS: active | LAST-UPDATED: 2026-08-29 | SUPERSEDES: 2026-07-17 seed

# 22 — MODEL REGISTRY (frozen point forecasters — no new forecaster trained)
| ID | Backbone | Role | Impl | Seed | Status |
|----|----------|------|------|------|--------|
| M01 | DLinear | anchor P2 | own closed-form least squares, `coverage_horizon/backbone.py` | 2026 | **USED** — 16 fits |
| M02 | NLinear | second backbone (model-agnosticism evidence) | same module | 2026 | **USED** — 16 fits. **Not in the Idea Lock.** Substituted for PatchTST without an authorised delta — see D012. |
| M03 | PatchTST | anchor P3, Lock-mandated | yuqinie98/PatchTST | — | **NOT RUN.** Dropping it was not what R5 authorised. |
| M04 | Informer | anchor P1 | TSLib | — | NOT RUN (R5 permits) |
| REF | Chronos | uncalibrated zero-shot reference only | arXiv 2403.07815 | n/a | NOT RUN |

**Deviation, stated plainly:** the Lock's model-agnosticism claim (C2) was to be demonstrated by a backbone swap. The swap actually performed is DLinear→NLinear, two one-layer linear maps from the same paper (Zeng et al. 2023). Δ worst-cell 0.0013 is a real result, but it is close to the weakest possible test of the claim. Either M03 is reinstated before S6 or C2 is narrowed in writing (P03). Deterministic closed-form fits mean the ≥3-seeds rule is vacuous here — state that explicitly rather than reporting one seed as if seeds were sampled.
