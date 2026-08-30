DOC: SESSION_REPORT | OWNER: Aarush | CADENCE: per-autonomous-session
STATUS: active | LAST-UPDATED: 2026-08-30 | SUPERSEDES: none

# SESSION REPORT — 2026-08-30, autonomous horizon-ablation session

Base commit `b2a3683` → head **`c473c5f`**, pushed to `origin/main`. Seven commits, all additive.
Working tree clean. No history rewritten (no force-push, rebase, reset --hard, or amend).

**Every Hard Rule 2 file verified unchanged by `git diff b2a3683..HEAD`:** `metrics.py`,
`conditional.py`, `backbone.py`, `config.py`, `run_experiments.py`, `results.json`, `casestudy.json`.
`data/` untouched. `figures/` additions only — all nine pre-existing `fig_*.png` verified
byte-identical by md5 before and after generating the new ones.

**No STOP condition was hit.**

---

## 1. Tasks attempted and outcomes

| Task | Outcome |
|------|---------|
| **0 — precondition** | **Precondition FAILED as written: `scripts/run_horizon_ablation.py` did not exist.** Wrote it to the given spec. Committed and pushed (`0de7187`) **before** running, per D008/FR01. |
| **1 — ETT ablation** | ✅ **Done.** 32 configs × K ∈ {1,2,4,6,8,10}, 453 s → `results/horizon_ablation.json` (`f35e429`). **Acceptance check PASSED.** |
| **2 — Electricity ablation** | ✅ **Done.** 8 configs × K ∈ {1,6}, 580 s → `results/ha_ecl.json` (`e231c21`). Never measured before. **Adaptive arm did not replicate ETT — reported as it landed.** |
| **3 — verify DELTA_001** | ✅ **Done.** Claim 1 ("never crosses 0.90") is **false**. Claim 2 (periodic, not monotone) is **true and re-verified**. |
| **4 — draft DELTA_002** | ✅ **Done.** `docs/01_IDEA_LOCK_DELTA_002.md`, STATUS `draft — awaiting Aarush approval` (`3276bbf`). All five required items (a)–(e) covered. |
| **5 — living documents** | ✅ **Done** (`e4f709c`). Docs 20, 43, 13, 24, 50, 12 updated; 00_INDEX also updated to register the two delta notes. |
| **6 — figures** | ✅ **Done** (`c473c5f`). `scripts/make_figures_horizon.py` → `fig_kabl_fixed.png`, `fig_horizon_interaction.png`. `make_figures.py` not modified; no existing figure overwritten. |

---

## 2. Every number measured

### 2.1 Task 1 — ETT, `results/horizon_ablation.json`, key `rows`, 32 configs

**Acceptance check.** Mean `worst_ref` at K=6, method `Proposed` = **0.865746** → **0.8657**.
Committed `results.json` Proposed mean = **0.8657**. **Match to 4 dp. PASSED.**

Mean `worst_ref` (fixed K_REF=6 grid) and `worst_own` (own K-grid), by K:

| K | Cond `worst_ref` | Proposed `worst_ref` | Proposed `worst_own` | Cond `worst_own` |
|---|---|---|---|---|
| 1 | 0.7797 | 0.8263 | 0.8717 | 0.8357 |
| 2 | 0.7665 | 0.8198 | 0.8710 | 0.8197 |
| 4 | 0.7637 | 0.8350 | 0.8676 | 0.7748 |
| 6 | 0.7588 | **0.8657** | 0.8657 | 0.7588 |
| 8 | 0.7598 | 0.8560 | 0.8640 | 0.7463 |
| 10 | 0.7611 | 0.8601 | 0.8616 | 0.7386 |

| Quantity | Value | Source |
|---|---|---|
| Cond (static) K=1 → K=6 | 0.7797 → 0.7588, **−0.0209** | `horizon_ablation.json` `rows[].worst_ref` |
| Proposed (adaptive) K=1 → K=6 | 0.8263 → 0.8657, **+0.0394** | same |
| horizon × adaptation interaction | **+0.0603** | derived |
| conditioning × adaptation interaction (K=6) | **+0.1291** (P−C−A+G) | same |
| **Sign test, Proposed, K=6 > K=1** | **31 / 32** | same |
| — sole exception | NLinear/ETTh1/H=720, 0.8685 → 0.8571 | same |
| Sign test, Cond, K=6 > K=1 | 23 / 32 | same |
| **Same sign test on `worst_own`** | **0 / 32** (both arms) | `rows[].worst_own` |
| Proposed width K=1 → K=6 | 1.9406 → **1.9245** | `rows[].width` |
| Proposed Winkler K=1 → K=6 | 2.6943 → **2.6366** | `rows[].winkler` |
| Cond width K=1 → K=6 | 2.1711 → 2.1304 | `rows[].width` |
| Cond Winkler K=1 → K=6 | 2.9806 → 2.9095 | `rows[].winkler` |
| Proposed marginal K=1 / K=6 | 0.9099 / 0.9098 | `rows[].marginal` |
| Proposed `frac_within_5pt` K=1 → K=6 | 0.3125 → 0.8876 | `rows[].frac_within_5pt` |
| Proposed `frac_below_80` K=1 → K=6 | 0.0119 → 0.0000 | `rows[].frac_below_80` |
| **Cond@K=1 ≡ CondC** | **exact, 32/32, max abs diff 0.0e+00** | derived |

Cross-check at K=6 against committed `results.json` `cal[].worst_cell` — all six exact:
Global 0.7667 · MSCP 0.7251 · CondC 0.7797 · Cond 0.7588 · ACI 0.7445 · Proposed 0.8657.
(Only discrepancy anywhere: ACI Winkler 2.8309 here vs 2.8310 committed — a rounding-order artefact,
committed rounds per-config to 4 dp before averaging, this file to 6 dp.)

### 2.2 Task 2 — Electricity, `results/ha_ecl.json`, key `rows`, 8 configs

| Method | K=1 | K=6 | Δ | sign test K=6>K=1 |
|---|---|---|---|---|
| **Cond (static)** | 0.5473 | 0.4621 | **−0.0853** | 3 / 8 |
| **Proposed (adaptive)** | 0.8340 | 0.8306 | **−0.0034** | **4 / 8** |
| Proposed `worst_own` | 0.8767 | 0.8306 | — | 0 / 8 |

**The mean hides a clean, backbone-consistent horizon reversal** (`rows[].worst_ref`, Proposed):

| backbone | H=96 | H=192 | H=336 | H=720 |
|---|---|---|---|---|
| dlinear K=1 | 0.8287 | 0.8408 | 0.8392 | 0.8349 |
| dlinear K=6 | 0.7940 | 0.7995 | **0.8754** | **0.8649** |
| nlinear K=1 | 0.8333 | 0.8455 | 0.8427 | 0.8066 |
| nlinear K=6 | 0.7940 | 0.7995 | **0.8754** | **0.8417** |

K=1 wins at H=96/192 (4/4), K=6 wins at H=336/720 (4/4). Logged as **Q13**.

| Quantity | K=1 | K=6 | Source |
|---|---|---|---|
| Proposed width | 0.9451 | **0.9420** | `rows[].width` |
| Proposed Winkler | 1.4220 | **1.4083** | `rows[].winkler` |
| Proposed marginal | 0.8959 | 0.8964 | `rows[].marginal` |
| Proposed `cell_p05` | 0.8715 | **0.8806** | `rows[].cell_p05` |
| Proposed `frac_within_5pt` | 0.6250 | **0.9771** | `rows[].frac_within_5pt` |
| Proposed `frac_below_80` | 0.0000 | 0.0017 | `rows[].frac_below_80` |
| Cond@K=1 ≡ CondC | exact, 8/8 | — | derived |

Cross-check at K=6 against committed `casestudy.json` `cal[].worst_cell` — **all six exactly 0.000000
difference**: Global 0.5757 · MSCP 0.5382 · CondC 0.5473 · Cond 0.4621 · ACI 0.6177 · Proposed 0.8306.

### 2.3 Task 3 — DELTA_001 claim 1, `results/results.json` key `curves.Global.cov`

Config DLinear/ETTh1/H=720, identified because curve mean **0.948308** matches that `cal` row's
`marginal` 0.9483. `n_test` = **91** from `point[]`, C = 7 → **n = 637**.

| Quantity | Value |
|---|---|
| steps below 0.90 | **152 / 720 (21.1%)** |
| steps below 0.85 | **88 / 720 (12.2%)** |
| steps below 0.80 | **18 / 720 (2.5%)** |
| minimum | **0.761381**, at step **h = 684** |
| first / last step below 0.90 | h = 12 / h = 712 |
| first-24-step mean | **0.969846** |
| last-24-step mean | **0.910911** |
| binomial SE at p=0.90, n=637 | 0.011886 |
| **minimum, in SE below 0.90** | **11.662** |

**Verdict: the claim "NEVER crosses the 0.90 target" is FALSE.**

Why it was believed — the claim is true of the *aggregated* curve: lowest K=6 bucket mean **0.9427**
(h=241–720), and the rolling-25 centred smoother that `fig_gate.png` plots bottoms at **0.885512** on
an axis whose limits are (0.80, 1.00). DELTA_001's "≈0.970 first day" reproduces exactly (0.9698).

### 2.4 Task 3 — DELTA_001 claim 2, `results/results.json` key `curves.MSCP.width`

`curves.Global.width` confirmed constant by construction (min = max = 3.380496), which is why MSCP is
used instead.

| Quantity | Value |
|---|---|
| **lag-24 autocorrelation** | **+0.8754** |
| lag-12 / lag-48 / lag-168 | +0.3095 / +0.7829 / +0.4729 |
| **corr(width, h)** | **+0.3387** |
| monotonically increasing? | **No** — 323 of 719 steps increase, **396 decrease** |
| argmax / argmin | h = 205 / h = 1 |

**Verdict: claim 2 is TRUE and stands.** Periodic (daily), not monotone.

### 2.5 Q09 by-horizon breakdown, `results.json` `curves.*.cell`, DLinear/ETTh1/H=720

K=6 edges [1,3,9,27,80,240,720]; bucket sizes [3,6,18,53,160,480] steps = [273,546,1638,4823,14560,43680] samples.

| Method | b1 (1–3) | b2 (4–9) | b3 (10–27) | b4 (28–80) | b5 (81–240) | b6 (241–720) |
|---|---|---|---|---|---|---|
| Global | 0.9817 | 0.9707 | 0.8590 | 0.8999 | 0.8549 | 0.8697 |
| CondC | 1.0000 | 0.9963 | 0.8571 | 0.8953 | 0.8509 | **0.6922** |
| Cond | 0.6557 | 0.8022 | 0.8449 | 0.8706 | 0.8545 | **0.7526** |
| **Proposed** | **0.8571** | 0.8571 | 0.8730 | 0.8826 | 0.8725 | 0.8720 |

Proposed's binding cell is the **smallest** bucket (273 samples), not the coarsest. The coarsest is
where the **static** methods break, and all 18 sub-0.80 per-step coverages sit inside it (h=588–711).

### 2.6 Task 4(b) — DELTA_001's figures are DLinear-only

| Method | DELTA_001 | DLinear-only (16) | Both backbones (32) |
|---|---|---|---|
| Global | 0.751 | **0.7510** | 0.7667 |
| MSCP | 0.720 | **0.7200** | 0.7251 |
| ACI | 0.731 | **0.7307** | 0.7445 |
| Proposed | 0.866 | **0.8664** | 0.8657 |

---

## 3. Expectations from the prompt that my run did NOT match

**On Task 1: none. Every reference value reproduced exactly.**

| Expectation | Mine | Match |
|---|---|---|
| K=1 0.8263 · K=2 0.8198 · K=4 0.8350 · K=6 0.8657 · K=8 0.8560 · K=10 0.8601 | identical, all six | ✅ |
| Cond static 0.7797 → 0.7588 | identical | ✅ |
| Proposed adaptive 0.8263 → 0.8657 | identical | ✅ |
| sign test 31/32 | 31/32 | ✅ |
| K=6 must equal 0.8657 (STOP condition) | 0.865746 | ✅ **passed** |

Three prompt statements that turned out not to hold, none of them a STOP condition:

1. **Task 0's precondition.** The prompt's primary branch assumed `run_horizon_ablation.py` might
   already exist. It did not, so the fallback branch (write it) was taken.
2. **`metrics()` ignores its `edges` argument.** The spec says to call
   `metrics(Rts, half, K, edges)`. `metrics` re-derives buckets from `K` and never reads `edges`
   (`coverage_horizon/calibration/metrics.py`). I pass it positionally anyway to match
   `run_experiments.py`, and noted it in the docstring. **No effect on any number** — but it means
   "score on its own grid" is achieved by the `K` argument alone.
3. **`load_electricity()` returns 5 values, not 4.** The spec writes `loaded=(arr,tr,ca,te)`; the
   function returns `(arr, tr, ca, te, meta)`. I unpack five and pass the first four, as
   `run_casestudy.py` does. No effect on any number.

**On Task 2 there was no expectation to compare against, as stated — and it is as well, because the
ETT result did not replicate.** The adaptive arm's horizon gain is **−0.0034 (4/8)** on Electricity
against **+0.0394 (31/32)** on ETT. I have reported this as a partial replication rather than
smoothing it, and raised **Q13**. This is the single most important caveat in the session.

---

## 4. What I chose not to do, and why

- **Did not resolve P01–P04, D006 or D007.** Instructed to note, not decide. DELTA_002 is `draft —
  awaiting Aarush approval` and nothing was propagated to the Idea Lock.
- **Did not edit `results.json`, or delete its `kabl` block.** FR04 shows `kabl` is confounded, but
  it is Hard Rule 2 and deleting it would move committed output. Reported as **superseded, not
  deleted**, in DELTA_002 §5, FR04 and RV10. **No Hard Rule 2 file was even a temptation** — the
  fixed-grid scoring is achievable entirely from a new script.
- **Did not regenerate `fig_abl.png`**, whose panel (b) plots the confounded own-grid `kabl` curve
  and is therefore now misleading. It is an existing `fig_*.png` (Hard Rule 3). The correction lives
  in the new `fig_kabl_fixed.png`. **You will want to decide what happens to `fig_abl.png` panel (b)
  before S6.**
- **Did not chase DELTA_001's "≈0.927".** It matches neither the raw last-24 (0.9109), the smoothed
  last-24 (0.9047), the trailing-168 (0.9229) nor the final bucket (0.9427). Tagged **[UNVERIFIED]**
  rather than guessed at, per the epistemic rules.
- **Did not sweep K finely on Electricity** to locate the Q13 crossover, or test a minimum-steps floor
  on bucket edges for Q09. Both are method changes / new experiments beyond the task list.
- **Did not rebuild the FR01 losses** (MET02 rolling traces, calibration-window ablation). Out of scope
  for this list; still flagged in doc 12.

---

## 5. What to look at first

1. **`docs/01_IDEA_LOCK_DELTA_002.md` — approve or reject.** It corrects a factual claim in DELTA_001
   and re-weights the horizon term back up. W1–W4 and C1–C4 explicitly unchanged. Everything else this
   session hangs off it.
2. **The Electricity non-replication (Q13), §2.2 above.** K=1 beats K=6 at H≤192 and loses at H≥336,
   identically for both backbones. It is the sharpest form of **RV15**, and the 8-config mean
   (−0.0034) is the least informative summary of it. **Do not let that mean into a paper unsplit.**
3. **`FR04` in `docs/24_FAILURE_REGISTRY.md`.** A minimum over K×C cells is not comparable across K.
   It reversed a conclusion we had already drawn. Worth checking whether the same pattern is hiding in
   `gabl`, `scale_abl` or `stride_abl` — I did not audit those.
4. **`figures/fig_kabl_fixed.png`** — the confound in one picture, and **`fig_abl.png` panel (b)**,
   which plots the old confounded curve and now needs a decision.
5. **`docs/13_OPEN_QUESTIONS.md` Q14** — worst-cell and grid distribution disagree on Electricity
   (0.8340 vs 0.8306 while `frac_within_5pt` moves 0.625 → 0.977). D009 biting in the direction that
   favours us, which is when to be most careful. Needs a call before S6 drafting.
