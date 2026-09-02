DOC: 61_SESSION_CLOSEOUT_2026-09-02 | OWNER: Aarush | CADENCE: one-time
STATUS: active | LAST-UPDATED: 2026-09-02 | SUPERSEDES: none
SCOPE: paste-ready entries for 01_IDEA_LOCK_DELTA_002, 10_DECISION_LOG, 24_FAILURE_REGISTRY,
13_OPEN_QUESTIONS and 43_REVIEWER_2, from the work of 1-2 September 2026.

# CLOSE-OUT — realised feedback, online baselines, 32-config ablations, tuned-margin decision

## 0. What moved, in one table

| claim | Draft v1 | now | why it changed |
|---|---|---|---|
| ETT worst-cell, Proposed | 0.8657 | **0.8591** | realised feedback (FR07) |
| ETT interaction | +0.1291 | **+0.1224** | same |
| ECL worst-cell, Proposed | 0.8306 | **0.8059** | same |
| ECL interaction | +0.3264 | **+0.3022** | same |
| ECL adaptive % below 0.85 | "0.0%, never" | **6.3% / 6.5%** | same |
| ETT trace advantage | Proposed 11.9% vs global 16.0% | **16.3% vs 16.0% — none** | same |
| "best Winkler of all methods" | Proposed 2.6366 | **false**: per-horizon online 2.5840, PID 2.5861 | baselines added |
| gamma default | "0.05 throughout" | **0.02**, and 0.1 is better in 29/32 | B2 + 32-config ablation |
| scale: MAD vs SD for the baseline | "MAD much better" | **reversed**: SD better, MAD wins 7/32 | 32-config ablation |
| decision: intervals beat point rule | "from 5:1 the ordering reverses and widens" | **holds vs bare point; dissolves vs tuned margin (18/40)** | tuned-margin baseline |

Five reported conclusions moved. Four of them moved against us. The interaction — the
paper's central claim — survived every one of these tests, which is the only reason the
paper still exists in this form.

---

## 1. 01_IDEA_LOCK_DELTA_002 — APPROVAL BLOCK (append at the end of the delta note)

APPROVAL | 2026-09-02 | Aarush Pandit
DELTA_002 is approved as written. The scope reduction it records — ETT x4 plus a screened
50-meter Electricity subset, on DLinear and NLinear, in place of the canonical suite across
Informer/DLinear/PatchTST — is accepted as the study's delivered scope under the Lock's own
R5/R6 contraction rule. What the reduction costs the W1 audit claim and the model-agnosticism
claim is stated in the manuscript's Limitations rather than absorbed silently: two members of
one linear family do not establish architectural independence, and the paper says so and names
PatchTST as the decisive missing test. The wedge is not re-scoped; W1 is delivered narrower
than claimed, and the narrower claim is the one the paper makes.

## 2. 10_DECISION_LOG — entries to append

D012 | COUNTERSIGNED 2026-09-02 | NLinear substituted for the dropped Transformer backbones.
Originally logged as a deviation without authorisation. Countersigned now on the evidence that
the substitution turned out to be load-bearing in an unplanned way: NLinear and DLinear have
materially different error processes (bias 4.2% vs 16.5% of width; persistence r = -0.044 vs
+0.579), so the backbone-swap agreement of 0.0013 in worst-cell is stronger evidence than two
architecturally similar backbones would have given. The substitution remains a contraction, not
a design choice, and Limitations says so.

D015 | 2026-09-02 | Online protocol of record | instant feedback (as originally coded) vs
realised feedback | **realised feedback**; instant retained in Appendix A as a labelled oracle
upper bound | the original loop consumed a path's outcomes at all horizon steps before the next
path was issued, i.e. up to H - stride steps of future information, and the second-half
perturbation test could not see it because the leak lay inside the first half. Finding survives:
ETT 0.8591, interaction +0.1224, 31/32 vs global | costly-to-reverse (moves every adaptive
number) | 20, 23, 24, 43, paper

D016 | 2026-09-02 | Contribution claims re-stated | keep Lock C1-C4 wording vs the paper's five
items | paper wording, to be appended as C1-C5 v2 in doc 41 when it is instantiated | rule 1 of
02_OPERATING_RULES forbids silent edits; the fifth item (the two negative methodological
results) did not exist when C1-C4 were written | reversible | 41 (deferred), DELTA_002

D017 | 2026-09-02 | Online multi-step baselines | omit and state the gap vs implement what can
be implemented faithfully | implement per-horizon online conformal (MSCP-online) and conformal
PID; do NOT reimplement AcMCP's autocorrelation correction | both implemented methods are
specified well enough to reproduce honestly; AcMCP's distinguishing mechanism is not, and a
half-correct reimplementation scored against our own layer would be worse than a stated gap.
The two baselines bound that family from below and the paper says exactly that | reversible |
paper Sections 2, 5, 6, 12

D018 | 2026-09-02 | Decision claim | keep the v1 framing (intervals win from 5:1) vs weaken to
what the tuned-margin baseline supports | **weaken** | a point rule with a per-channel margin
tuned on the calibration block at each cost ratio matches or beats conformal gating in 22 of 40
configuration-ratio pairs. The decision value is in having a calibrated margin, not specifically
a conformal one. W4 is delivered, but its claim is narrower than the Lock anticipated |
costly-to-reverse | paper Section 10, 41, 43

## 3. 24_FAILURE_REGISTRY — entries to append

FR07 | S3-S5 | Adaptive arms updated with outcomes not yet realised: path t's full-horizon miss
rate consumed before path t+1 was issued | an online loop written as a batch loop; the leakage
check (perturb the second half of the test block) is blind to within-half lookahead | realised-
feedback update in `calibration/conditional.py::calibrate_delayed`; protocol of record changed
(D015); instant retained as a labelled oracle bound. Cost: ETT 0.8657 -> 0.8591, ECL 0.8306 ->
0.8059, and the "adaptive methods never dip below 0.85" claim was lost entirely | 2026-08-31

FR08 | S6 | Manuscript prose numbers hand-typed while tables were generated: gamma mis-stated
(0.05 vs 0.02), ablation surface unstated (one configuration, not 32), Electricity joint and
decomposition figures attributed to ETT, "thirteen points" for eleven, "3.5x" for 3.9x | prose
was not macro-injected although tables were | `make_numbers_tex.py` + `make_numbers_v3.py`;
every figure in the manuscript is now a macro and a re-run changes the paper | 2026-08-31

FR09 | S4/S6 | Two ablation conclusions read off a single configuration were wrong on the full
surface: the scale-estimator comparison had the SIGN reversed for the baseline (SD is better,
not MAD), and the gamma default was reported as optimal when 0.1 beats it in 29/32 | a
single-configuration ablation was treated as an ablation | all three ablations re-run over the
32 configurations of the main study (`run_ablations32.py`); rule adopted: an ablation is not an
ablation until it runs on the surface the main table averages over | 2026-09-02

## 4. 13_OPEN_QUESTIONS — entries to append

Q24 | Would a dependence-aware AcMCP close the gap our two online baselines leave open? | 2026-09-02 | OPEN — D017 states why we did not attempt it; this is the honest residual risk to the "no prior work" framing
Q25 | Does OLCP (arXiv 2605.05497) occupy any part of W2? Online + covariate-localised with guarantees, but not LTSF and not horizon x channel | 2026-09-02 | OPEN — intake required (LIT note + 32 matrix + 14 scan log)
Q26 | Is DLinear/ETTm2 at H >= 336 (above published values) a ridge-vs-early-stopping effect? | 2026-09-02 | OPEN — affects the S1 exit criterion statement
Q27 | RESOLVED 2026-09-02 — a calibration-tuned constant margin matches conformal gating (18/40). Decision claim weakened per D018
Q28 | Should gamma be re-defaulted to 0.1, or is the pre-committed 0.02 worth keeping for protocol hygiene? | 2026-09-02 | OPEN — leaning keep-and-report; changing a pre-committed hyperparameter after seeing test scores is the thing the hygiene rules exist to prevent

## 5. 43_REVIEWER_2 — defences to bank

RV20 "Your online update uses outcomes that are not observed yet." — It did. FR07; realised-feedback re-run; every adaptive number in the paper is under the corrected protocol; instant kept as a labelled oracle bound in Appendix A.
RV21 "Your static conditional arm is Mondrian conformal prediction." — Yes, with cells = bucket x channel. Cited as such. The contribution is the interaction, not the arm.
RV22 "Per-cell ACI is group-conditional online conformal (Bastani et al. 2022)." — Yes. Cited. Ours is the LTSF instantiation and the audit; no new guarantee is claimed.
RV23 "OLCP already combines adaptation and localisation with guarantees." — Different taxonomy (covariate kernel vs fixed horizon x channel), different regime, no audit. Positioned explicitly; Q25 tracks the intake.
RV24 "Conditioning alone does not hurt — it wins 21/32." — Corrected. The paper now says adaptation alone reliably hurts and conditioning alone is inconsistent with a CI spanning zero.
RV25 "Where are PID and the multi-step online family?" — Both reported now (D017). AcMCP's autocorrelation correction is explicitly not reimplemented and the paper states the gap.
RV26 "Your calibration windows overlap 97%; n is not a sample size." — D007 stated in Setup; the quantile is described as empirical over dependent scores; Limitations carries it.
RV27 "Your decision result is an operating-point artefact." — Largely correct, and now reported: a tuned constant margin matches conformal gating. The decision claim is weakened accordingly (D018).
RV28 "You compare minima across 42 and 300 cells after telling us not to." — Removed; grid-invariant statistics (5th-percentile cell, within +-5) used for any cross-surface statement.
RV29 "Ablations on one configuration." — All three now on 32 configurations, and two v1 conclusions reversed; reported as FR09 rather than quietly fixed.
RV30 "'Best Winkler of all seven methods' is false." — Corrected: per-horizon online conformal and PID both beat us on Winkler, and the paper says so in the same paragraph as the width result.
RV31 "Adaptive methods 'never' dip below 0.85." — Oracle-feedback artefact. Now 6.3% against global's 17.5% on electricity, and no advantage at all on ETT.
RV32 "gamma was tuned." — The opposite: gamma = 0.1 beats our pre-committed 0.02 in 29/32. We report the pre-committed value and flag it as a floor (Q28).

## 6. What is still open, honestly

- Institutional email and full author affiliations (manuscript title block).
- The published-MSE column for the 32-row point-forecast table: needs Zeng et al. (2023)
  Table 2 read at look-back 336. Deliberately NOT filled from memory.
- OLCP intake (Q25); AcMCP (Q24); PatchTST (the decisive backbone test).
- Bibliography fields for the pre-cutoff entries added this session — verify before submission.
