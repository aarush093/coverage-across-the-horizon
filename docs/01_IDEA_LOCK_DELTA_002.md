DOC: 01_IDEA_LOCK_DELTA_002 | OWNER: Aarush | CADENCE: delta-only
STATUS: draft — awaiting Aarush approval | LAST-UPDATED: 2026-08-30 | SUPERSEDES: none (corrects and annotates 01_IDEA_LOCK_DELTA_001; does not supersede it)

# DELTA NOTE 002 — the horizon axis is load-bearing after all
Raised by: S4 horizon-bucket ablation, 2026-08-30 (`scripts/run_horizon_ablation.py`, commits `0de7187` / `f35e429`).
Type: EVIDENCE change, not literature change. The wedge is NOT amended. DELTA_001's *emphasis* conclusion is.

Every number below was measured in this session from `results/horizon_ablation.json` (32 ETT configs,
2 backbones × 4 datasets × 4 horizons) or from `results/results.json` `curves.*`. Nothing is carried
forward in prose (FR03). [FACT] unless tagged otherwise.

## 1. Correction — "never crosses the 0.90 target" is false
DELTA_001 states that global conformal coverage decays along the horizon "but NEVER crosses the 0.90
target", and concludes "the horizon axis is real but not load-bearing."

Measured from `results/results.json` → `curves.Global.cov`, 720 per-horizon-step coverages. The config
is DLinear / ETTh1 / H=720, identified because the curve mean **0.948308** matches that row's
`marginal` (0.9483) exactly. `n_test` = 91 from the corresponding `point` row, C = 7 channels, so
n = 91 × 7 = **637** per step.

| Quantity | Measured |
|----------|----------|
| steps below 0.90 | **152 of 720 (21.1%)** |
| steps below 0.85 | **88 of 720 (12.2%)** |
| steps below 0.80 | **18 of 720 (2.5%)** |
| minimum | **0.7614**, at step **h = 684** |
| first step below 0.90 | h = 12 |
| last step below 0.90 | h = 712 |
| first-24-step mean | 0.9698 |
| last-24-step mean | 0.9109 |
| binomial SE at p = 0.90, n = 637 | 0.011886 |
| minimum, in SE below 0.90 | **11.66 SE** |

The claim is not marginally wrong. The minimum sits **11.7 standard errors** below target, and a fifth
of the path is under it.

**Where the error came from.** The claim is true of the *aggregated* curve and false of the *per-step*
curve. On the K=6 log-spaced reporting grid every bucket mean stays above target — the lowest is
**0.9427** (bucket h = 241–720) — and the rolling-25 smoother that `scripts/make_figures.py` plots in
`fig_gate.png` bottoms out at **0.8855** on an axis whose limits are (0.80, 1.00) with the target line
at 0.90. At that aggregation the crossing is invisible. DELTA_001's own "≈0.970 over the first day"
reproduces exactly (0.9698); its "≈0.927 over the last" does not (raw last-24 is 0.9109, smoothed
0.9047). [UNVERIFIED] I could not reproduce 0.927 from any obvious window — the closest are the
trailing-168 mean (0.9229) and the final bucket mean (0.9427) — so the provenance of that specific
figure is unresolved and it should not be requoted.

**Consequence.** The horizon axis is **load-bearing**, not "real but not load-bearing". DELTA_001's
§"What the evidence actually returned", first bullet, is corrected. The 18 sub-0.80 steps all sit at
h = 588–711, i.e. inside the coarsest bucket, which is exactly where bucket averaging hides them.

## 2. Annotation — DELTA_001's figures are DLinear-only
DELTA_001 quotes 0.751 (Global), 0.720 (MSCP), 0.731 (ACI) and 0.866 (Cond+ACI, i.e. Proposed).
Verified this session: those are exactly the **DLinear-only** means over 16 configs.

| Method | DELTA_001 quotes | DLinear-only (16) | Both backbones (32) |
|--------|------------------|-------------------|---------------------|
| Global | 0.751 | **0.7510** | 0.7667 |
| MSCP | 0.720 | **0.7200** | 0.7251 |
| ACI | 0.731 | **0.7307** | 0.7445 |
| Proposed | 0.866 | **0.8664** | 0.8657 |

Neither set is wrong. DELTA_001 was written 2026-08-16, before the NLinear arm existed (D007).
The note simply predates it. Papers and tables must quote the two-backbone column; DELTA_001's
numbers should be read as a DLinear slice and labelled as such wherever they are reused.

## 3. New evidence — a SECOND interaction: the horizon axis hurts without adaptation and helps with it
`buckets(H, 1)` returns a single horizon bucket spanning 1..H, so at K=1 the horizon term vanishes and
the cell index degenerates to the channel index. Verified structurally, not assumed: **Cond at K=1
equals CondC exactly in 32/32 configs, max |diff| = 0.0e+00.** So "Proposed at K=1" *is* channel-only
conditioning with adaptation — the arm the seven-method factorial never ran.

Sweeping K on a **fixed** K_REF=6 scoring grid (mean `worst_ref`, 32 configs):

| | K=1 (channel only) | K=6 (horizon × channel) | effect of adding the horizon axis |
|---|---|---|---|
| **static** (Cond) | 0.7797 | 0.7588 | **−0.0209** |
| **adaptive** (Proposed) | 0.8263 | 0.8657 | **+0.0394** |

Horizon × adaptation interaction term: **+0.0603**. Sign test on the adaptive arm: K=6 beats K=1 on
`worst_ref` in **31 of 32** configs (the single exception is NLinear / ETTh1 / H=720, 0.8685 → 0.8571).
For the static arm the same test is only 23/32.

Full sweep, mean `worst_ref` over 32 configs:

| K | 1 | 2 | 4 | 6 | 8 | 10 |
|---|---|---|---|---|---|---|
| Cond (static) | 0.7797 | 0.7665 | 0.7637 | 0.7588 | 0.7598 | 0.7611 |
| Proposed (adaptive) | 0.8263 | 0.8198 | 0.8350 | **0.8657** | 0.8560 | 0.8601 |

Width and Winkler at the two ends (mean, 32 configs): Proposed width 1.9406 → 1.9245, Winkler
2.6943 → 2.6366; Cond width 2.1711 → 2.1304, Winkler 2.9806 → 2.9095. Marginal coverage is flat at
0.9098–0.9099. **The horizon axis is not bought with width** — K=6 is both narrower and better scored
than K=1 on the adaptive arm.

**This is a second interaction, distinct from the one already claimed.** The existing claim is
conditioning × adaptation, worth **+0.1291** on ETT (Global 0.7667, Cond 0.7588, ACI 0.7445,
Proposed 0.8657; P − C − A + G). The new one is horizon-granularity × adaptation, worth **+0.0603**.
They are different contrasts: the first asks whether conditioning and adaptation need each other, the
second asks whether the *horizon* half of the conditioning needs adaptation specifically.

**How DELTA_001 reached the wrong emphasis.** It read the static evidence correctly and generalised it
to the adaptive case, which had not been run. On static conditioning the horizon axis genuinely does
hurt (−0.0209 here; MSCP 0.7251 below Global 0.7667 there). DELTA_001 concluded the horizon term was
"supporting, not headline". The adaptive arm was never measured across K, and it moves the opposite
way. The inference was sound on the evidence available; the evidence was incomplete.

## 4. Consequence for the wedge — W1–W4 UNCHANGED, C1–C4 UNCHANGED
Stated explicitly: **this is an evidence note, not a scope change.** No wedge component is amended,
no contribution claim is edited, and nothing here requires a Decision Log entry under Hard Rule 1.

W2 still reads "horizon-bucket × channel conditioning with online adaptation" and the method is
unchanged — K=6 was already the default (`config.K_BUCKETS`). What changes is how the paper *argues*
it. DELTA_001 demoted the horizon term to "supporting, not headline" on the strength of the static
evidence; that demotion is now withdrawn. The horizon term earns its place in the method name, and
the honest framing is that **both halves of the conditioning require adaptation to pay off** — which
strengthens rather than weakens the interaction story that already carries the claim.

## 5. Also recorded — the prior K ablation was scored on a moving grid
`scripts/run_experiments.py` scores each K with `metrics(Rts, half, K, edges)`, i.e. on **its own**
K-bucket grid. Worst-cell coverage is a minimum over cells; a coarser grid has fewer and larger cells
and therefore a higher minimum almost by construction. K=1 is scored over 1 × 7 = 7 cells, K=10 over
10 × 7 = 70. That compares two estimators, not two methods, and the bias runs in the direction that
flatters small K.

Same run, same half-widths, two scorings (mean over 32 configs, Proposed):

| K | cells on own grid | own-grid `worst_own` | fixed-grid `worst_ref` | gap |
|---|---|---|---|---|
| 1 | 7 | 0.8717 | 0.8263 | +0.0454 |
| 2 | 14 | 0.8710 | 0.8198 | +0.0511 |
| 4 | 28 | 0.8676 | 0.8350 | +0.0326 |
| 6 | 42 | 0.8657 | 0.8657 | 0.0000 |
| 8 | 56 | 0.8640 | 0.8560 | +0.0080 |
| 10 | 70 | 0.8616 | 0.8601 | +0.0016 |

**It reverses the conclusion.** Own-grid scoring is monotonically decreasing in K and says the best
setting is **K=1** — drop the horizon axis. Fixed-grid scoring says **K=6**. The sign test flips
completely: K=6 beats K=1 in **31/32** configs on the fixed grid and **0/32** on the own grid. The two
scorings agree exactly at K=6, where the grids coincide, which is the check that the new path is
consistent with the old one (mean 0.865746, equal to the committed `results.json` Proposed mean 0.8657).

`results.json`'s existing `kabl` block should be reported as **superseded, not deleted**. It is
single-config (DLinear / ETTh1 / H=720 only), covers K ∈ {4,6,8,10} only, and is own-grid scored. Its
four rows (0.8571 / 0.8571 / 0.8571 / 0.8516) are not wrong for what they are; they are simply not
comparable across K and not a basis for choosing K. `results.json` is untouched — the new evidence
lives in `results/horizon_ablation.json`. Logged as **FR04**.

## Status
Wedge: INTACT. No scope change. No contribution claim (C1–C4) edited.
DELTA_001 is **corrected on one factual claim** (§1) and **annotated on one scope-of-evidence point**
(§2); its second evidence item (residual scale periodic rather than monotone) is **re-verified and
stands** — from `curves.MSCP.width`, lag-24 autocorrelation **+0.8754**, corr(width, h) only **+0.3387**,
and width is not monotone (396 of 719 steps decrease; max at h = 205, not h = 720). Global's width
curve is constant by construction (min = max = 3.380496), which is why the check is read off MSCP.

**Awaiting Aarush approval.** Nothing in this note has been propagated to the Idea Lock.
