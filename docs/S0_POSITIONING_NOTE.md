DOC: S0_POSITIONING_NOTE | OWNER: Aarush | CADENCE: once, at S0
STATUS: draft — partial, see §5 | LAST-UPDATED: 2026-08-30 | SUPERSEDES: none

# S0 — POSITIONING NOTE
Idea Lock §8 exit criterion: *"Wedge statement survives unchanged, or is amended in writing."*
**Verdict: the wedge survives unchanged.** W1–W4 are all unoccupied as of 2026-08-30.
This note is **partial** — three of the mandated close reads are done, one is not (§5).

---

## 1. The one-sentence position

> The closest benchmarking work in this literature (Sabashvili, arXiv:2601.18509, Jan 2026) concludes
> that multi-step split conformal prediction is the best available method. It reaches that conclusion
> using AutoARIMA on monthly sales data, scored on marginal coverage, interval width and the Winkler
> score. On the canonical LTSF suite with frozen DLinear and NLinear backbones, MSCP has the **highest
> marginal coverage of the seven methods we compare (0.9123)** and the **worst conditional coverage
> (worst-cell 0.7251)** — below the do-nothing global-conformal baseline at 0.7667. The method that a
> marginal-coverage benchmark ranks first is the method that fails hardest per cell.

That contrast *is* wedge component W1, and it is now stated against a named, dated, external benchmark
rather than against a strawman. It should be cited approvingly: 2601.18509 is careful work within its
declared scope. The gap is in the evaluation contract, not in the execution.

## 2. Prior-art fence, re-verified 2026-08-30

| Work | What it does | Nearest wedge | Occupies? |
|------|--------------|---------------|-----------|
| **2601.18509** — CP-for-TS survey + benchmark (Sabashvili, Jan 2026) | AutoARIMA on monthly sales; marginal coverage, width, Winkler; concludes MSCP is best | W1 | **NO — Q05 CLOSED.** No dataset overlap, no backbone overlap, no conditional-coverage metric |
| **2604.13253** — BC-ACI (Lade, Krishna, Kumar, Apr 2026) | per-horizon online EWMA bias estimate; corrects scores and re-centres intervals | W2 | **NO — Q08 CLOSED.** Nearest neighbour on the W2 axis, but it moves the interval *centre* while we condition the interval *width* on horizon-bucket × channel. No channel dimension, no bucketing, no worst-cell audit, no decision layer |
| **2508.13362** — O2CP (Li, Menacho, Rodríguez; v2 Jun 2026) | online CP modelling inter-horizon error dependence on trajectory ensembles | W3 | **NO — Q01 CLOSED** (the paper was retitled between v1 and v2; there was no citation error). Short horizons, trajectory ensembles, no channel conditioning, no LTSF backbones |
| **2410.13115** — AcMCP (Wang & Hyndman) | autocorrelation-aware multi-step CP; asymptotic marginal coverage | W2 baseline | NO — small H, ARIMA/ETS/NN, no channel conditioning |
| **2605.19231** — DeRegiME | trained sparse-GP density model on the LTSF suite with DLinear/PatchTST encoders | W1 | NO — different objective: density quality (NLPD/CRPS) vs distribution-free coverage control |

## 3. What the two closest papers each cost us

**2601.18509 costs us nothing and gives us the framing.** It formalises MSCP as a named baseline
paradigm, which is exactly what fix F1 already assumed, and its headline result is the foil for W1.

**2604.13253 costs us one banked defence.** BC-ACI's premise is that a frozen forecaster develops
persistent bias after a shift, and that symmetric intervals then pay a width overhead of roughly
twice the bias magnitude. **Our intervals are symmetric around the frozen point forecast.** If the
per-cell residual mean is materially non-zero on our test blocks — and our S5 split is deliberately
across seasons, which is exactly the shift BC-ACI describes — then we are paying that overhead and
have not measured it. This is Reviewer #2 item **RV16** and open question **Q15**. It is one pass
over the archived residual tensors to settle.

## 4. Consequence for the wedge — no amendment

W1–W4 stand as written in Idea Lock §3. No component is amended, narrowed or withdrawn. The two
2026 papers closest to W2 and W1 respectively both fail to occupy, and for reasons that are
substantive rather than technicalities: one has no channel dimension and no conditional metric, the
other has neither LTSF backbones nor a conditional metric.

Standing caution from the Lock, unchanged: the wedge survives only while unoccupied, and the monthly
scan is overdue — no scan has been logged since 2026-07-17 and the 2026-08-03 first-Monday run
appears to have been missed (Q10).

## 5. What is NOT done — this note is partial

Idea Lock §8 mandates four close reads at S0. Status:

| Mandated read | Status |
|---|---|
| 2601.18509 — CP-for-TS benchmark | **DONE** — abstract, method, data, metrics, headline result all verified |
| 2604.13253 — BC-ACI (added by the 2026-07-17 scan as closest to W2) | **DONE at abstract/intro depth.** The PDF returned no machine-readable text; the full empirical suite was not read and **whether it touches the LTSF suite is unconfirmed** |
| 2508.13362 — O2CP | **PARTIAL** — identity, retitling and method verified. **Q02 not resolved:** the Lock's fence table asserts this paper's conclusion names decision-coupled calibration as open future work, and that sentence has still not been read. Confirm it or strike it |
| 2410.13115 — AcMCP | **NOT READ** at S0 depth (abstract only) |
| 2307.16895 — Conformal PID | **NOT READ** |

Also outstanding: Q03 (partially answered — treat Wang & Hyndman as MSCP's canonical source, this
survey as corroboration) and Q04 (CopulaCPTS venue of record, unconfirmed).

**S0 is therefore not formally exited.** What has changed is that the two wedge-critical unknowns —
Q05 (could the survey pre-empt W1) and Q08 (does BC-ACI occupy W2) — are both closed, and both
closed favourably. The remaining reads are Related-Work completeness, not existential risk.
