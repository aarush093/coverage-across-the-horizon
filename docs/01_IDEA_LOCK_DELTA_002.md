DOC: 01_IDEA_LOCK_DELTA_002 | OWNER: Aarush | CADENCE: delta-only
STATUS: draft — awaiting Aarush approval | LAST-UPDATED: 2026-08-30 | SUPERSEDES: the 2026-08-30 draft at commit 3276bbf (which was written before the Electricity arm had run); corrects and annotates 01_IDEA_LOCK_DELTA_001 without superseding it

# DELTA NOTE 002 — the horizon axis is load-bearing, and only adaptation makes it pay
Raised by: S4/S5 horizon-bucket ablation, 2026-08-30 (`scripts/run_horizon_ablation.py`; commits `0de7187`, `f35e429`, `e231c21`).
Type: EVIDENCE change, not literature change. The wedge is NOT amended. DELTA_001's *emphasis* conclusion is.

Every number below was measured this session from `results/horizon_ablation.json` (32 ETT configs:
2 backbones × 4 datasets × 4 horizons), `results/ha_ecl.json` (8 Electricity configs: 2 backbones ×
4 horizons), or `results/results.json` `curves.*`. Nothing is carried forward in prose (FR03).
[FACT] unless tagged otherwise.

**Read §4 before quoting §3.** The ETT result in §3 does not survive unqualified on the 300-cell
Electricity grid, and the reason is itself the interesting part.

---

## 1. Correction — "never crosses the 0.90 target" is false

DELTA_001 states that global conformal coverage decays along the horizon "but NEVER crosses the 0.90
target", and concludes that "the horizon axis is real but not load-bearing."

Measured from `results/results.json` → `curves.Global.cov`, 720 per-horizon-step coverages. The config
is DLinear / ETTh1 / H=720, identified because the curve mean **0.948308** matches that row's
`marginal` (0.9483) exactly. `n_test` = 91 from the corresponding `point` row, C = 7 channels, so
n = 91 × 7 = **637** samples per step.

| Quantity | Measured |
|----------|----------|
| steps below 0.90 | **152 of 720 (21.1%)** |
| steps below 0.85 | **88 of 720 (12.2%)** |
| steps below 0.80 | **18 of 720 (2.5%)** |
| minimum | **0.7614**, at step **h = 684** |
| first / last step below 0.90 | h = 12 / h = 712 |
| first-24-step mean | 0.9698 |
| last-24-step mean | 0.9109 |
| binomial SE at p = 0.90, n = 637 | 0.011886 |
| minimum, in SE below 0.90 | **11.66 SE** |

The claim is not marginally wrong. The minimum sits **11.7 standard errors** below target and a fifth
of the path lies under it.

**Where the error came from.** The claim is true of the *aggregated* curve and false of the *per-step*
curve. On the K=6 log-spaced reporting grid every bucket mean stays above target — the lowest is
**0.9427** (bucket h = 241–720) — and the rolling-25 smoother that `scripts/make_figures.py` plots in
`fig_gate.png` bottoms out at **0.8855** on an axis running (0.80, 1.00) with the target line at 0.90.
At that aggregation the crossing is invisible. DELTA_001's "≈0.970 over the first day" reproduces
exactly (0.9698); its "≈0.927 over the last" does not (raw last-24 is 0.9109, smoothed 0.9047).
[UNVERIFIED] The 0.927 figure could not be reproduced from any obvious window — closest are the
trailing-168 mean (0.9229) and the final bucket mean (0.9427) — so its provenance is unresolved and it
should not be requoted.

**Consequence.** The horizon axis is **load-bearing**. DELTA_001's first evidence bullet is corrected.
The 18 sub-0.80 steps all sit at h = 588–711, inside the coarsest bucket — precisely where bucket
averaging hides them, which is why the aggregated view was reassuring and wrong.

---

## 2. Annotation — DELTA_001's figures are DLinear-only

| Method | DELTA_001 quotes | DLinear-only (16 configs) | Both backbones (32) |
|--------|------------------|---------------------------|---------------------|
| Global | 0.751 | **0.7510** | 0.7667 |
| MSCP | 0.720 | **0.7200** | 0.7251 |
| ACI | 0.731 | **0.7307** | 0.7445 |
| Proposed | 0.866 | **0.8664** | 0.8657 |

Neither set is wrong. DELTA_001 was written 2026-08-16, before the NLinear arm existed (D007); it
simply predates it. Papers and tables must quote the two-backbone column, and DELTA_001's numbers
should be labelled as a DLinear slice wherever they are reused.

---

## 3. New evidence — a second interaction, on ETT: the horizon axis hurts without adaptation and helps with it

`buckets(H, 1)` returns a single horizon bucket spanning 1..H, so at K=1 the horizon term vanishes and
the cell index degenerates to the channel index. Verified structurally rather than assumed:
**Cond at K=1 equals CondC exactly in 32/32 configs, max |diff| = 0.0e+00.** So "Proposed at K=1" *is*
channel-only conditioning with adaptation — the arm the seven-method factorial never contained.

Sweeping K on a **fixed** K_REF=6 scoring grid (mean `worst_ref`, 32 ETT configs):

| | K=1 (channel only) | K=6 (horizon × channel) | effect of the horizon axis |
|---|---|---|---|
| **static** (Cond) | 0.7797 | 0.7588 | **−0.0209** |
| **adaptive** (Proposed) | 0.8263 | 0.8657 | **+0.0394** |

Horizon × adaptation interaction: **+0.0603**. Sign test on the adaptive arm: K=6 beats K=1 in
**31 of 32** configs (sole exception NLinear / ETTh1 / H=720, 0.8685 → 0.8571). On the static arm the
same test is 23/32.

Full ETT sweep, mean `worst_ref`:

| K | 1 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| Cond (static) | 0.7797 | 0.7665 | 0.7637 | 0.7588 | 0.7598 | 0.7611 |
| Proposed (adaptive) | 0.8263 | 0.8198 | 0.8350 | **0.8657** | 0.8560 | 0.8601 |

Not bought with width: on the adaptive arm K=6 is both narrower (1.9245 vs 1.9406) and better scored
(Winkler 2.6366 vs 2.6943) than K=1, with marginal coverage flat at 0.9098–0.9099.

**This is a second interaction, distinct from the one already claimed.** The existing claim is
conditioning × adaptation, worth **+0.1291** on ETT (Global 0.7667, Cond 0.7588, ACI 0.7445,
Proposed 0.8657; P − C − A + G). The new one is horizon-granularity × adaptation, worth **+0.0603**.
The first asks whether conditioning and adaptation need each other; the second asks whether the
*horizon half* of the conditioning specifically needs adaptation.

**How DELTA_001 reached the wrong emphasis.** It read the static evidence correctly and generalised it
to the adaptive case, which had not been run. On static conditioning the horizon axis genuinely does
hurt (−0.0209 here; MSCP 0.7251 below Global 0.7667 there). The adaptive arm across K was never
measured, and it moves the opposite way. The inference was sound on the evidence available; the
evidence was incomplete.

---

## 4. Replication on Electricity -- the horizon axis needs adaptation MORE on a wide grid

Read on the adaptive arm alone, the same sweep on the S5 surface (50 meters, 300-cell
grid, K in {1,6}, 8 configs) looks like a non-replication: mean effect **-0.0034**, K=6
winning 4/8, split cleanly by horizon (K=1 wins at H<=192 by 0.035-0.046, K=6 wins at
H>=336 by 0.030-0.036, identically for both backbones).

**But the adaptive column is not the quantity this note is about.** Section 3 measures
an interaction, and the interaction is LARGER here than on ETT:

| | K=1 (channel only) | K=6 (horizon x channel) | effect |
|---|---|---|---|
| **static** (Cond) | 0.5473 | 0.4621 | **-0.0853** |
| **adaptive** (Proposed) | 0.8340 | 0.8306 | **-0.0034** |

Horizon x adaptation interaction: **+0.0818 on Electricity, against +0.0603 on ETT.**
Without adaptation, adding horizon buckets to a 300-cell grid costs 0.085 of worst-cell
coverage. With adaptation, it costs nothing. The adaptation is doing more work here, not
less, which is the opposite of a failed replication.

**Every other statistic also favours K=6, at every horizon.** Mean over 8 configs:
worst-cell 0.8340 -> 0.8306, but cell_p05 0.8715 -> **0.8806**, within +/-5pt 0.625 ->
**0.977**, width 0.9451 -> **0.9420**, Winkler 1.4220 -> **1.4083**. And cell_p05 does
not flip with horizon the way the raw minimum does (+0.0094, +0.0084, +0.0103, +0.0086
at H = 96, 192, 336, 720).

**The mechanism, measured.** The calibration-window ablation (EXP_S4_006) shows why. On
Electricity, every baseline plateaus as calibration data grows -- Global gains only
+0.034 of worst-cell across a fourfold increase, MSCP +0.008 -- because their failure is
structural. Proposed gains **+0.200** (0.6307 at n_cal=24 to 0.8306 at n_cal=96) and has
still not saturated. Its failure is statistical: it is estimating a 300-cell grid from
under a hundred paths. K=6 asks for six times as many cells as K=1, so wherever the
block is thin the extra granularity costs more than it returns. That single mechanism
accounts for this section, for Q13's horizon crossover, and for Q14's disagreement
between the minimum and the distribution.

**Honest statement.** The horizon axis improves calibration on both surfaces and at
every horizon on every distributional statistic. On the raw minimum over a wide grid it
appears to hurt at short horizons; that appearance is a sample-size artefact of the
statistic, not a property of the method. This is exactly the failure mode **D009** was
adopted to prevent, one day before it occurred. Section 3's headline (+0.0394, 31/32)
is **an ETT result and must be labelled as one**; the interaction, which is the claim,
replicates and strengthens.

## 5. Consequence for the wedge — W1–W4 UNCHANGED, C1–C4 UNCHANGED

Stated explicitly: **this is an evidence note, not a scope change.** No wedge component is amended, no
contribution claim is edited, and nothing here requires a Decision Log entry under Hard Rule 1.

W2 still reads "horizon-bucket × channel conditioning with online adaptation", and the method itself is
untouched — K=6 was already `config.K_BUCKETS`. What changes is how the paper argues it. DELTA_001
demoted the horizon term to "supporting, not headline" on static evidence; that demotion is
**withdrawn**. The horizon term earns its place in the method name, and the honest framing is that
**both halves of the conditioning require adaptation to pay off**, which strengthens rather than
weakens the interaction story that already carries the claim.

---

## 6. Also recorded — the prior K ablation was scored on a moving grid (FR04)

`scripts/run_experiments.py` scores each K with `metrics(Rts, half, K, edges)`, i.e. on **its own**
K-bucket grid. Worst-cell coverage is a minimum over cells; a coarser grid has fewer, larger cells and
therefore a higher minimum almost by construction. K=1 is scored over 1 × 7 = 7 cells, K=10 over
10 × 7 = 70. That compares two estimators, not two methods, and the bias flatters small K.

Same run, same half-widths, two scorings (mean over 32 ETT configs, Proposed):

| K | cells on own grid | `worst_own` | `worst_ref` | gap |
|---|---|---|---|---|
| 1 | 7 | 0.8717 | 0.8263 | +0.0454 |
| 2 | 14 | 0.8710 | 0.8198 | +0.0511 |
| 4 | 28 | 0.8676 | 0.8350 | +0.0326 |
| 6 | 42 | 0.8657 | 0.8657 | 0.0000 |
| 8 | 56 | 0.8640 | 0.8560 | +0.0080 |
| 10 | 70 | 0.8616 | 0.8601 | +0.0016 |

**It reverses the conclusion.** Own-grid scoring decreases monotonically in K and names **K=1** best —
drop the horizon axis. Fixed-grid scoring names **K=6**. The sign test flips completely: K=6 beats K=1
in **31/32** configs on the fixed grid and **0/32** on the own grid. The two agree exactly at K=6,
where the grids coincide, and that agreement is the consistency check: mean **0.865746**, equal to the
committed `results.json` Proposed mean of 0.8657.

Scope of the defect, checked this session: **only `kabl` is affected.** `gabl`, `scale_abl` and
`stride_abl` all score with `K_BUCKETS` held fixed and are sound. `results.json`'s `kabl` block should
be reported as **superseded, not deleted** — it is single-config (DLinear / ETTh1 / H=720), covers
K ∈ {4,6,8,10} only, and is own-grid scored. Its rows are not wrong for what they are; they are simply
not comparable across K and not a basis for choosing K. `results.json` is untouched; the new evidence
lives in `results/horizon_ablation.json`. Logged as **FR04**.

Consequence for the deck: `figures/fig_abl.png` plots the own-grid curve and has already been shown at
Review 1. It needs either replacing with `fig_kabl_fixed.png` or an explicit caption. Aarush's call.

---

## 7. What this opens (not decided here)

**K should probably not be a constant.** The cost of the horizon axis scales with the cell count and
therefore with the channel count; its benefit scales with horizon heterogeneity and therefore with H.
A fixed K=6 is well chosen for a 7-channel benchmark at long horizons and is not obviously right for a
50-channel surface at H=96. A rule that adapts K to (H, C, n_cal) is a natural extension. Raised as an
open question, **not** proposed as a scope change — it would need a decision entry of its own.

## Status
Wedge: INTACT. No scope change. No contribution claim (C1–C4) edited.

DELTA_001 is **corrected on one factual claim** (§1) and **annotated on one scope-of-evidence point**
(§2). Its second evidence item — residual scale periodic rather than monotone — is **re-verified and
stands**, from `curves.MSCP.width`: lag-24 autocorrelation **+0.9810** raw and **+0.9756** after
removing the linear trend, against lag-12 **+0.3337**; corr(width, h) only **+0.3387**; and width is
not monotone (396 of 719 steps decrease, maximum at h = 205, not h = 720). Global's width curve is
constant by construction (min = max = 3.380496), which is why this check is read off MSCP.

Note: the 3276bbf draft recorded this autocorrelation as +0.8754. Recomputed independently as
`corrcoef(w[:-24], w[24:])` = **+0.9810**. The lower figure could not be reproduced and should not be
used.

**Awaiting Aarush approval.** Nothing in this note has been propagated to the Idea Lock.
