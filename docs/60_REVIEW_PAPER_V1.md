DOC: 60_REVIEW_PAPER_V1 | OWNER: Claude (Reviewer #2 role), Aarush disposes | CADENCE: one-time, per draft
STATUS: active | LAST-UPDATED: 2026-08-31 | SUPERSEDES: none
SCOPE: paper/paper.tex at commit 377e850 ("Draft v1", dated 31 Aug 2026), read against results/*.json, coverage_horizon/*, docs/*, and a delay-aware re-run executed in a clean clone this session.

# REVIEW OF DRAFT v1 — "Coverage Across the Horizon"

## 0. Verdict

The finding survives. The paper does not, as written.

Three things are true at once. (1) The central result — conditioning and adaptation each fail alone, and their combination is worth ~+0.12 worst-cell coverage on ETT — is real, reproduces bit-exactly from a clean clone, and **survives an honest online protocol** that the committed code does not implement (Section 1, item B1). (2) The manuscript misreports its own method and experiments in at least eleven places, including the step size it uses, the surface its ablations were run on, and which dataset two of its headline numbers come from. (3) Two of fifteen references have no authors and paraphrased titles, and one load-bearing negative claim ("no prior work runs the 2×2") is contradicted by a May 2026 preprint that the wedge scan has not yet ingested.

Nothing here kills the contribution. All of it would kill the submission. Every fix below is either a text change or a CPU re-run under four minutes, except the one that matters (B1), which is fourteen minutes and already written.

Tags: [FACT] = checked against the repo or a resolved source this session. [MEASURED] = computed this session from the committed artefacts or from a run in a clean clone (uncommitted; you reproduce). [UNVERIFIED] = not checked; treat as a claim. [ASSUMPTION] / [SPECULATION] as usual.

---

## 1. BLOCKING — the paper cannot go to the guide or to arXiv until these are fixed

### B1. The adaptive arms use future outcomes. The paper's leakage check cannot see it. [FACT, code]

`coverage_horizon/calibration/conditional.py`, both adaptive loops:

```python
for t in range(n_ts):
    half[t] = ...                          # interval for path t
    cov = np.abs(Rts[t]) <= half[t]        # ALL H steps of path t
    for k, c: alpha_t[k, c] += gamma * (alpha - miss_rate)   # update NOW
```

Path t+1 is issued one stride (24 steps) after path t. The tracker that issues it has already consumed path t's outcome at horizon step 720, which in real time is observed 696 steps after path t+1's forecast origin. Every adaptive number in the paper (ACI, Proposed, the rolling traces, the calibration-window curve, the electricity table) was produced with feedback that is not available online. The perturbation test in §3 ("second half of test block perturbed → first-half intervals bit-identical") is correct and irrelevant: the leaked information lies inside the first half.

This is the delayed-feedback problem that AcMCP/MPID [7] exist to handle, and it is the first thing a conformal reviewer will ask. It is also the reason the Lock listed AcMCP as "a comparison, not an oversight" (F3).

**What I did.** `scripts/run_delayed.py` (delivered) re-runs ACI and Proposed with feedback applied only once realised: path t contributes its cell-(k,c) outcome only when the cell's last horizon step has been observed, i.e. lag = ⌈edge_hi(k)/stride⌉ paths (4 / 8 / 14 / 30 paths for the last bucket at H = 96 / 192 / 336 / 720). Same pool, same quantile rule, same γ, same one-update-per-path-per-cell. The only variable is the delay. Static rows reproduce the committed numbers bit-exactly (Global 0.9097 / 0.7667 / 2.0857 / 2.9422), so the clone is a faithful environment.

**Result, ETT, 32 configurations [MEASURED, clean clone, uncommitted]:**

| method | marginal | worst-cell | width | Winkler |
|---|---|---|---|---|
| Global (static, unchanged) | 0.9097 | 0.7667 | 2.0857 | 2.9422 |
| Cond (static, unchanged) | 0.9084 | 0.7588 | 2.1304 | 2.9095 |
| ACI — instant feedback (paper) | 0.9031 | 0.7445 | 1.8742 | 2.8310 |
| **ACI — realised feedback** | 0.9017 | 0.7446 | 1.8906 | 2.8579 |
| Proposed — instant feedback (paper) | 0.9098 | 0.8657 | 1.9245 | 2.6366 |
| **Proposed — realised feedback** | **0.9069** | **0.8591** | **1.9684** | **2.7100** |

- Interaction under realised feedback: 0.8591 − 0.7588 − 0.7446 + 0.7667 = **+0.1224** (paper: +0.1291).
- Sign counts: Proposed-realised > Global **31/32**; > Cond 31/32; > ACI-realised 32/32; > ACI-instant 32/32.
- The cost of honesty is concentrated where it should be: per-H worst-cell 0.8690 / 0.8635 / 0.8562 / 0.8478 (instant: 0.8697 / 0.8661 / 0.8656 / 0.8616). At H = 720 the last bucket waits 30 paths for its first update.
- Per backbone: DLinear 0.8604, NLinear 0.8579 (still within 0.003). Per dataset: 0.8646 / 0.8346 / 0.8800 / 0.8574.
- **One claim does not survive:** "best Winkler of all seven methods." Under realised feedback Proposed's Winkler is 2.7100; Gaussian is 2.6804. Proposed remains the best *conformal* method on Winkler and the best on worst-cell by a wide margin. Rewrite the abstract and §6 accordingly.

**Result, Electricity, 8 configurations [MEASURED, clean clone, uncommitted]:**

| method | marginal | worst-cell | 5th pct. cell | within ±5 | width | Winkler |
|---|---|---|---|---|---|---|
| Global (static, unchanged) | 0.8644 | 0.5757 | 0.7995 | 0.534 | 0.8568 | 1.5263 |
| Cond (static, unchanged) | 0.8610 | 0.4621 | 0.6725 | 0.522 | 0.8702 | 1.5417 |
| ACI — instant (paper) | 0.8921 | 0.6177 | 0.8353 | 0.488 | 0.9568 | 1.5152 |
| **ACI — realised** | 0.8906 | 0.6173 | 0.8340 | 0.493 | 0.9587 | 1.5251 |
| Proposed — instant (paper) | 0.8964 | 0.8306 | 0.8806 | 0.977 | 0.9420 | 1.4083 |
| **Proposed — realised** | **0.8931** | **0.8059** | **0.8768** | **0.972** | **1.0339** | **1.5301** |

- Interaction under realised feedback: **+0.3022** (paper: +0.3264); Proposed-realised > Global, Cond, ACI-realised: 8/8 each.
- H = 96 and 192 are unchanged to four decimals (lag 4 and 8 paths out of ~215); H = 336: 0.8754 → 0.8553; **H = 720: 0.8533 → 0.7748** (lag 30 paths).
- **Width and Winkler no longer favour Proposed on this surface:** width 1.0339 vs Global 0.8568 (1.20×); Winkler 1.5301 vs Global 1.5263 / ACI-realised 1.5251. Under honest feedback the electricity gain is conditional coverage *bought with width*. The abstract's "narrower intervals and the best interval score" is an ETT statement under the oracle protocol; v2 says so.
- Grid-size-invariant interactions (which the paper's own §7 rule requires for cross-surface talk): on p05, ETT +0.0588 / Electricity +0.1698; on within-±5, ETT +0.369 / Electricity +0.491.

**Fix.** (a) Make realised feedback the protocol of record: Table 1, Table 2, §8.1 traces, §8.2 curve, all re-run with the delayed update. (b) Keep the instant-feedback numbers as an explicit *oracle-feedback upper bound* in an appendix, one table, clearly labelled. (c) State the delay rule in §4 in one sentence. (d) Log FR07 (24_FAILURE_REGISTRY) and a Decision (D015: protocol of record = realised feedback). (e) Both surfaces are done in preview (`results/delayed_ett.json`, `results/delayed_ecl.json`, delivered); reproduce them from a committed script before any number goes into the paper of record. (f) Then, and only then, decide whether AcMCP goes in as a baseline. My view: it should — it is the dependence-aware method for exactly this problem, it is NumPy, and its absence is now the second question a reviewer asks.

### B2. "We use γ = 0.05 throughout" is false. The code uses 0.02. [FACT]

`config.py: GAMMA = 0.02`. `results.json`, `casestudy.json`, `cw_*.json`, `bias_check.json` all record `gamma: 0.02`. The γ-ablation row at 0.02 (0.8571) equals the main-run value for that configuration; the row at 0.05 (0.8791) does not appear anywhere else. The paper describes a method it did not run. Fix: γ = 0.02 everywhere; state that it was fixed before the test block was scored (it was — it is in config, dated 16 Aug), and that the ACI baseline uses the same γ (it does).

### B3. Every ablation in §11 was run on ONE configuration and the paper does not say so. [FACT]

`results.json`: `kabl`, `gabl`, `scale_abl` are on DLinear / ETTh1 / H = 720 (`REF` in `run_experiments.py`); `stride_abl` is on DLinear / ETTh1 / H = 96. That is why Proposed appears as 0.8657 (Table 1), 0.8571 (γ and scale ablations), 0.8702 (stride ablation), and why "γ = 0 gives 0.652" contradicts "static conditional = 0.7588". A reviewer reading §11 against Table 1 will conclude the numbers are inconsistent. They are not; they are unlabelled. Fix: state the surface in every ablation sentence, or — better, since the main study runs in under four minutes — re-run γ, scale and K on all 32 configurations and report means with sign counts. The stride ablation stays single-configuration by necessity (only H = 96 has enough paths); say so.

### B4. §9 reports Electricity numbers as if they were the ETT study. [FACT]

"Applying a max-normalised-score layer restores whole-path coverage to 0.9124 at 10.16× the width; a Bonferroni layer gives 0.9130 at 10.19×" — these are `casestudy.json` (Electricity, 8 configs). The ETT joint layers in `results.json` are: MaxScore **0.8772 at 3.25×**, Bonferroni **0.9154 at 3.59×** (per-H MaxScore 0.892 / 0.902 / 0.883 / 0.833; width ratios 3.1–3.9×). The "≈10× width" in the abstract and in Contribution 3 is therefore an Electricity-only figure presented as the price on the main study; on ETT the price is ≈3.3–3.6×. The "62% horizon / 38% sample size" decomposition and the "80 paths" sentence are also Electricity (EXP_S4_006, Q16). Fix: report both surfaces, label both, and show the arithmetic: (0.9259 − 0.8947) / (0.9444 − 0.8947) = 0.0312 / 0.0497 = 62.8%.

### B5. "Conditioning alone makes worst-cell coverage worse" is not supported by the paper's own data. [MEASURED from results.json]

Pairwise on the 32 configurations:

| contrast | mean Δ worst-cell | wins/32 | paired-bootstrap 95% CI |
|---|---|---|---|
| Cond − Global | −0.0079 | **21/32 for Cond** | (−0.042, +0.024) |
| ACI − Global | −0.0222 | 13/32 | (−0.034, −0.011) |
| Proposed − Global | +0.0990 | 31/32 | (+0.082, +0.115) |
| Interaction P−C−A+G | +0.1291 | — | (+0.092, +0.170) |

Static conditioning **wins the majority of configurations** and beats Global on three of four datasets (ETTh2 0.7852 vs 0.7482; ETTm1 0.8611 vs 0.8008; ETTm2 0.7806 vs 0.7499). The mean is dragged below zero by ETTh1 alone (0.6085 vs 0.7680). The abstract's "makes worst-cell coverage worse (0.7588)" is a mean masking a distribution — the exact sin the paper accuses the field of. Correct statement: adaptation alone reliably hurts; conditioning alone is inconsistent (large loss on ETTh1, small gains elsewhere, CI spans zero); neither approaches the combination. The interaction itself is solid (CI excludes zero by a wide margin) and is the claim to lead with. Add the sign counts and CIs to Table 1 (a "wins vs Global" column) — the paper currently gives sign counts only for the comparisons it wins.

### B6. "Canonical LTSF suite" is claimed; ETT ×4 plus 50 of 321 Electricity meters is delivered. [FACT]

Abstract, Contribution 1, §5. The canonical suite (Lock W1) is ETT ×4, Electricity, Traffic, Weather, ILI across Informer, DLinear, PatchTST. The paper covers four ETT sets and a screened Electricity subset on two linear backbones. This is a scope reduction the Lock allows under R5/R6 and DELTA_002 is drafted for it — but DELTA_002 is still "awaiting Aarush approval" and D012 (NLinear substitution) is logged as a deviation, not countersigned. Per 02_OPERATING_RULES a contribution claim cannot change without a Decision Log entry first. Fix: (a) approve DELTA_002 and countersign D012 before this draft circulates; (b) replace "canonical LTSF suite" with "the four ETT benchmarks and a screened Electricity subset" everywhere; (c) the five-item Contributions list in §1 differs from C1–C4 in the Lock — log the re-statement (D016) rather than silently editing.

### B7. Two references have no authors and paraphrased titles; one was cited unread. [FACT, resolved 2026-08-31]

| ref | in paper | actual (resolved today) |
|---|---|---|
| [14] | "DeRegiME: regime mixtures for probabilistic forecasting under shift. arXiv:2605.19231." (no authors) | K. Wood, S. Zohren, S. J. Roberts. *DeRegiME: Deep Regime Mixtures for Probabilistic Forecasting under Distribution Shift.* arXiv:2605.19231 [cs.LG], 19 May 2026. Oxford / Oxford-Man. |
| [15] | "Gate-localized conformal prediction for nonstationary multivariate forecasting. arXiv:2607.23165." (no authors) | Z. Ma, J. Jiang, Á. López-Oriona, Y. Sun, H. Ombao. *Adaptive Multi-Scale Forecasting and Gate-Localized Conformal Prediction for Multivariate Nonstationary Time Series.* arXiv:2607.23165 [stat.ML], 25 Jul 2026. KAUST. |

[15] has no LIT note (only 2508.13362, 2601.18509, 2604.13253 have intake notes in `docs/`); memory says it was "queued for close read". It is cited with a characterisation ("likewise trains its own forecasting module") that its abstract partly contradicts: ABF-T-GLCP is described as a *model-agnostic* framework whose calibration module (GLCP) selects calibration residuals by learned gate state and recency. The honest differentiation is: GLCP localises calibration by a learned, data-driven taxonomy; we condition on a fixed horizon × channel taxonomy and adapt online; GLCP claims approximate local coverage under stability conditions, we claim long-run adaptive coverage. Run both through the intake path (31 schema → 32 matrix) before v2.

### B8. "No prior work runs the 2 × 2" is contradicted at the conceptual level. [FACT at abstract level, 2026-08-31]

Search for [15] surfaced **arXiv:2605.05497, "Online Localized Conformal Prediction" (Y. Lai and one co-author, May 2026)**: online adaptation combined with covariate-dependent localisation, with coverage guarantees for both OLCP and a bandwidth-hedged variant. That *is* conditioning + adaptation, with theory. It is not on LTSF backbones, not horizon × channel, and has no audit — the wedge survives as stated (LTSF scale, the grid, the audit, the decision layer) — but the sentence "which no prior work reports because no prior work runs the 2 × 2" must become "which, to our knowledge, has not been reported on LTSF backbones at this scale". Also pre-cutoff and directly relevant, none cited: **Mondrian conformal prediction** (Vovk, Lindsay, Nouretdinov, Gammerman 2003 — the static conditional arm *is* Mondrian CP with cell = bucket × channel; a reviewer will say so, so say it first); **multivalid / group-conditional online conformal** (Bastani et al., "Practical adversarial multivalid conformal prediction", NeurIPS 2022 — per-group online coverage, the closest ancestor of per-cell ACI); **DtACI** (Gibbs & Candès, JMLR 2024, arXiv:2208.08401 — adaptive step size; answers "why fixed γ?"); **AgACI** (Zaffran et al., ICML 2022). [FACT, pre-cutoff; verify bib fields before use.] Intake OLCP (LIT note + 32 matrix + 14 scan log) this week.

---

## 2. MAJOR — fix before any external reader; none changes the finding

### M1. Section 3 says calibration windows are "strided rather than overlapping"; §11 admits they overlap 97%. [FACT]

Stride 24 with H = 720 → adjacent calibration paths share 696 of 720 targets. The number `n` in ⌈(n+1)(1−α)⌉/n is not a count of exchangeable units; the finite-sample form is a heuristic here. D007 already logs this deviation with the right reason (strict non-overlap leaves 3 paths at H = 720). §3 must say what D007 says; §4 must say the quantile is an empirical quantile of dependent scores; Limitations must carry it. The stride ablation shows the *level* falls with stride (0.8702 / 0.8382 / 0.7500) — the paper attributes this to sample size only; overlap-induced optimism is the competing explanation and cannot be separated at H = 96 with 30 non-overlapping paths. Say so.

### M2. §5 says baselines fail from variance; §8.2 says their failure is structural. Your own data says: it depends on the surface. [FACT, cw_ett.json]

ETT, worst-cell vs calibration fraction (n_cal 28 → 112): Global 0.658 → 0.767; **MSCP 0.549 → 0.725 (+0.176, more than Proposed's +0.120)**; Cond 0.620 → 0.759; ACI 0.669 → 0.745; Proposed 0.746 → 0.866. On ETT every method is data-limited, which *supports* §5's variance mechanism. On Electricity the baselines plateau (Global +0.034, MSCP +0.008) while Proposed gains +0.200. The correct sentence is: "on ETT the baselines' failure is variance and shrinks with data; under the electricity seasonal shift it is structural and does not." Figure 2 should carry the Cond curve on both surfaces (it is in `cw_*.json`).

### M3. §7: on Electricity the horizon axis does NOT help under adaptation. [FACT, ha_ecl.json]

K = 1 → K = 6 on the adaptive arm is −0.0034 (0.8340 → 0.8306). The text says "the horizon axis hurts without adaptation and helps with it … the same structure appears on the electricity surface, more strongly." The interaction (+0.0818) is positive only because the static arm collapses (−0.0853). Honest phrasing: on Electricity adaptation *neutralises* the harm of the horizon axis; it does not convert it into a gain. This also weakens the §12 sentence "margin grows as the grid gets harder."

### M4. Cross-surface comparison of interactions violates the paper's own rule. [FACT]

§7 and §12 forbid comparing minima across grids of different size; the abstract and §13 then compare +0.1291 (42 cells) with +0.3264 (300 cells) and call the second "growth." Report both, do not rank them, and if you want a cross-surface statement use a grid-size-invariant statistic (interaction on `cell_p05` or on `frac_within_5pt`, both in `casestudy.json`; the ETT equivalents need one pass through `metrics.py` — D014 deliberately left it untouched, so add them in a new script, not in place).

### M5. Decision layer: unstated surface, unstated H, missing trivial baselines, single operating point. [FACT, casestudy.json]

The decision table is Electricity, mean over 8 configurations (both backbones, all four H), threshold = 95th percentile of the calibration block. None of this is in §10. `FlagAll` and `FlagNone` are computed and not shown; show them (at 50:1 FlagAll costs 0.108 — the reader needs to see that the interval rules still beat it). The interval rule operates at recall 0.96 / precision 0.44, the point rule at 0.70 / 0.76: these are two operating points, and the interval rule's advantage at ≥5:1 may be an operating-point effect. Add a "point forecast + constant margin tuned on the calibration block" baseline (equal-tuning rule F8); if the conformal margin beats a tuned constant margin, the decision result is real; if not, say the value is in *which* margin, not in gating per se.

### M6. Bias diagnostic wording. [FACT]

(a) "NLinear … no persistence (r = −0.044, −0.595)": r = −0.595 on Electricity is strong *anti*-persistence, not absence; a calibration-block correction would then hurt. Say "no positive persistence." (b) "3.5× the bias": 0.1648 / 0.0421 = 3.9× as a fraction of width; 3.5× is the raw-unit ratio from Q21 (0.1514 / 0.0436). Pick one and say which. (c) "on the worst DLinear configuration it returns 11.2% of width" — say it is one configuration (DLinear / ETTh2 / H = 720) and give the pooled figure (−1.5% width, −0.0009 worst-cell) alongside.

### M7. The method description does not match the implementation in four details. [FACT, code]

- "rolling per-channel scale s_c": the scale is the MAD over the **whole calibration block**, fixed thereafter. Not rolling. (Fixed is fine — it is leakage-free. Say fixed.)
- "α_t + γ(α − 1{miss})": the update uses the **empirical miss fraction over the cell's steps for that path**, one update per path per cell, not a per-step indicator.
- "α_t clamped to [10⁻⁴, 0.5]": the running level is **unclamped**; the clamp is applied when the quantile is read. This preserves ACI's memory and matters for the guarantee; state it correctly.
- "Gaussian residual: H × C": the Gaussian baseline uses per-(h, c) standard deviations — 5040 cells at H = 720, no bucketing. Fine, but label it "per-step × channel".
Also missing from §3/§4: look-back L = 336; ridge λ = 10⁻³·n (bias unpenalised); DLinear kernel 25, shared across channels; bucket-edge rule (`unique(round(logspace(0, log10 H, K+1)))`, which yields fewer than K buckets at small H — e.g. 9 at H = 96, K = 10); test windows use the same one-per-day stride (that is what "one per day" in Fig. 1 means); the seed controls nothing in the deterministic pipeline — say so instead of implying stochastic components.

### M8. Point-forecast sanity is reported for one of eight (backbone, dataset) pairs. [FACT, results.json]

All 32 point MSEs exist. DLinear/ETTh1 is within 1.3% as stated. From memory of Zeng et al. (2023) Table 2 [UNVERIFIED — check the table before quoting], DLinear/ETTm2 at H = 336 / 720 measures 0.3189 / 0.4581 against published ≈0.281 / 0.397 (+13% / +15%), and DLinear/ETTh2 at 336 measures 0.4858 against ≈0.448 (+8%). NLinear tracks its published numbers closely (ETTh1 0.3702 / 0.4034 / 0.4277 / 0.4344 vs ≈0.374 / 0.408 / 0.429 / 0.440). If confirmed, the S1 exit criterion ("within ~5%") is not met for DLinear on ETTm2 and ETTh2 at long horizons, plausibly because closed-form ridge lacks the implicit regularisation of Adam + early stopping. Put the full 32-row table in an appendix with the published column, and rewrite the sanity paragraph to describe the whole table, not the flattering corner.

### M9. Numeric errors in prose (FR03 class). [FACT]

| paper says | source says | note |
|---|---|---|
| "thirteen points below the global baseline" (§8) | 0.5757 − 0.4621 = 0.1136 → **eleven** | hand-typed |
| "γ = 0.05 throughout" | 0.02 | B2 |
| "0.652 at γ = 0" (3 d.p.) | 0.6520, single config | B3; also ≠ 0.7588 because surface differs |
| "3.5× the bias" | 3.9× (width-normalised) or 3.5× (raw) | M6 |
| "≈10× width" (abstract, C3) | ETT 3.25–3.59×; Electricity 10.16–10.19× | B4 |
| "no persistence (…, −0.595)" | anti-persistence | M6 |
| "0.22 µs per interval endpoint" | 102 ms / (91·720·7) ≈ 0.22 µs per *interval*, all seven methods together | define |
| "joint 0.0005 … at most 0.0045" | means over H; at H ≥ 336 every method is 0.0000 | report per H |
| "+0.3264" | +0.32640 from unrounded means (rounded inputs give 0.3265) | fine, but this is why numbers must be injected, not typed |

The paper claims "every number … is generated from the released artefacts by a script, not transcribed." The tables are; the prose is not. `scripts/make_numbers_tex.py` (delivered) emits `paper/numbers.tex` macros for every headline figure; paper_v2.tex uses them.

### M10. Table 1 lacks the distributional statistics Table 2 has. [FACT]

D014 added `cell_p05`, `frac_within_5pt`, `frac_below_80` for Electricity only, deliberately leaving `metrics.py` untouched. Add them for ETT via a separate script (do not edit `metrics.py`), so the two tables have the same columns and the reader can see whether Proposed's ETT gain is a one-cell effect.

---

## 3. MINOR / PRESENTATION

- Abstract: 320 words with nine four-decimal numbers. Cut to ≤ 220; round prose numbers to two decimals; keep four decimals in tables only.
- Title page: co-author affiliations missing; "Correspondence: aarush093 on GitHub" → an email address. Guide's name and affiliation in full.
- "pre-registered plan" (§3): the Idea Lock is a dated private note committed to a public repo, not a registration. Say "our written plan (Idea Lock v1.0, 16 July 2026, in the repository)".
- "Backbone independence" (§6) → "Backbone swap". Two members of one linear family do not establish independence; §12 already says so.
- Figures: remove in-plot editorial titles (Fig. 1's title is an argument; Fig. 2's is truncated in the PDF: "…ctricity -- … not struct"). Captions carry the argument. Add the Cond curve to Fig. 2 (M2). Add per-dataset panels or a supplementary table of the 32 worst-cell values.
- Table 1 caption: "Joint" needs "(per-step intervals; whole-path layers in §9)"; add a wins-vs-Global column (B5).
- §8.1: "below 0.85" threshold — say why 0.85 (5 points under target, the width of the ±5 band used in Table 2).
- §10: which quantity is the "peak threshold" (95th percentile of the calibration block, per meter) and that costs are per meter-hour, normalised per configuration then averaged.
- Related work: "Recent work … is scored the way the point literature is scored: with one aggregate number" — over-general; Stankeviciute et al. (NeurIPS 2021) report per-horizon coverage and use Bonferroni for multi-horizon joint coverage (cite them in §9 too); Zaffran et al. plot coverage traces. Say "commonly".
- Impossibility of exact conditional coverage: cite the primary sources (Vovk 2012; Lei & Wasserman 2014; Foygel Barber, Candès, Ramdas & Tibshirani 2021), not only [10].
- Missing citations: NLinear = [2] (say so); Winkler (1972) for the score; TFB (Qiu et al., VLDB 2024) for the drop_last artefact; split conformal (Papadopoulos et al. 2002; Lei et al. 2018); Electricity source (UCI ElectricityLoadDiagrams20112014; Lai et al. 2018 for the LSTNet release you actually download). [FACT, pre-cutoff — verify bib fields.]
- Spelling: British throughout (normalised, artefact) — consistent already; keep.
- Rhetorical density: "Both of these bit us before they became findings" is good once; "we report the regime where it loses as plainly as the one where it wins" and "not the flattering one" are the same sentence three times. Keep one.
- Reference [13]: Q01 is closed — v2 title is correct. Fine.
- Q02 is still open and the paper does not rely on it. Fine; keep it open in 13.

---

## 4. CLAIMS vs THE LOCK (constitution reconciliation)

| Lock item | Paper | Status |
|---|---|---|
| W1 audit: canonical suite × Informer/DLinear/PatchTST | ETT×4 + 50/321 Electricity × DLinear/NLinear | narrowed; DELTA_002 drafted, **unapproved** |
| W2 layer: bucket × channel conditioning + ACI/PID adaptation | bucket × channel + per-cell ACI; **no PID**; adaptation implemented with instant feedback | B1; PID absent without a stated reason |
| W3 marginal-vs-joint at H ≤ 720 | max-score + Bonferroni; **no copula** (Lock F6 promised three) | state deviation or add CopulaCPTS-style layer |
| W4 decision-level on real building energy | Electricity benchmark (R3 fallback, D011) | fine; state R3 fallback in §10 |
| §10 comparison set: Gaussian, quantile heads, global CP, MSCP, ACI, PID, CopulaCPTS, AcMCP/MPID, Chronos ref | Gaussian, global, MSCP, CondC, Cond, ACI, Proposed | **PID, CopulaCPTS, AcMCP, quantile heads, Chronos all absent, none explained** |
| F3 strided/non-overlapping calibration | one-per-day stride, 97% overlap at H = 720 | D007 deviation; §3 text wrong (M1) |
| F5 theory-scope box | present, correct | ✓ |
| F6 both coverages reported | present | ✓ (B4 mislabel) |
| F7 drop_last off, sequential splits | verified in code | ✓ |
| F8 equal tuning budget | no trained baselines → vacuous; decision-layer point rule untuned | M5 |
| §10 hygiene: 3 seeds | vacuous (deterministic) | say so plainly |
| C1–C4 | five contributions, re-framed | D016 needed |
| Pending P02–P05 | P02 (PatchTST) → Limitations ✓; P04 arXiv timing open; P05 confounded `fig_abl.png` still in `figures/` | delete or rename fig_abl.png before release |

---

## 5. REQUIRED RE-RUNS BEFORE v2 (all CPU; order matters)

1. `git add scripts/run_delayed.py scripts/make_numbers_tex.py && git commit` — D013, before running anything.
2. `python scripts/run_delayed.py --ecl` → `results/delayed_ett.json`, `results/delayed_ecl.json` (~6 min; resumable). Compare with the preview numbers in §1 B1; they must match to 1e-4 (deterministic). Then `python scripts/make_numbers_tex.py` → `paper/numbers.tex` (545 macros) and `paper/table_point.tex`; `paper_v2.tex` builds from these and from nothing typed.
3. Traces (`run_traces.py`) and calibration-window (`run_calwindow.py`) re-run with the delayed update — these scripts call `calibrate`; add a `delayed=True` path or import `calibrate_delayed`. Until done, §8.1 and §8.2 adaptive numbers are [TODO] under the protocol of record.
4. γ / scale / K ablations on all 32 configurations (four minutes each). Stride stays at H = 96.
5. ETT distributional grid statistics (M10) via a new script reading `results.json → cal[*].cell`? No — `cell` is not stored per row in `results.json`; recompute from residuals in the same script as (4).
6. Optional but strongly advised: AcMCP (realised feedback, dependence-aware) and Conformal PID as baselines; a tuned-margin point rule for §10. Each is < 100 lines of NumPy.
7. `python scripts/make_summary.py && python scripts/make_numbers_tex.py` → regenerate; `audit_docs.py` → clean.
8. Rebuild paper_v2.tex; grep for `\todo` — zero hits before it leaves the repo.

---

## 6. ENTRIES TO ADD TO THE OS DOCS (paste-ready)

**24_FAILURE_REGISTRY**
| FR07 | S3–S5 | Adaptive arms updated with outcomes not yet realised (path t's full-horizon miss rate consumed before path t+1 is issued) | online loop written as batch loop; leakage check (second-half perturbation) blind to within-half lookahead | realised-feedback update (`run_delayed.py`); protocol of record changed (D015); instant-feedback retained as labelled oracle bound. Finding survives: ETT worst-cell 0.8591, interaction +0.1224, 31/32 vs Global | 2026-08-31 |
| FR08 | S6 | Manuscript prose numbers hand-typed: γ mis-stated (0.05 vs 0.02), ablation surface unstated (single config), Electricity joint/decomposition numbers attributed to ETT, "thirteen points" (eleven), "3.5×" (3.9×) | prose not macro-injected although tables were | `make_numbers_tex.py`; every prose number is a macro | 2026-08-31 |

**10_DECISION_LOG**
D015 | 2026-08-31 | Online protocol of record | instant feedback (as coded) vs realised feedback | **realised feedback**; instant retained as oracle upper bound in appendix | instant feedback uses up to H−stride future steps; the leak is invisible to the second-half perturbation test; finding survives the fix (FR07) | costly-to-reverse (changes every adaptive number) | 20, 23, 24, 43, paper
D016 | 2026-08-31 | Contribution claims re-stated (C1–C4 → five items incl. the negative methodological result) | keep Lock wording vs paper wording | paper wording, appended as C1–C5 v2 in 41 when instantiated | 02 rule 1: no silent edits | reversible | 41 (deferred), 01 DELTA_002

**13_OPEN_QUESTIONS**
Q24 | Does AcMCP (dependence-aware, realised feedback) close the gap to Proposed-realised at H = 720? | 2026-08-31 | OPEN — it is the baseline the Lock promised and the one B1 makes necessary
Q25 | Does OLCP (arXiv 2605.05497) occupy any part of W2? | 2026-08-31 | OPEN — abstract-level: online + localised with guarantees; not LTSF, not horizon × channel; intake required
Q26 | Is DLinear/ETTm2 at H ≥ 336 (+13–15% vs published, if confirmed) a ridge-vs-early-stopping effect? | 2026-08-31 | OPEN — affects the S1 exit criterion statement
Q27 | Does a calibration-tuned constant margin match the conformal margin in §10? | 2026-08-31 | OPEN — decides whether W4's value is in gating or in the margin

**43_REVIEWER_2 (bank these)**
RV20 "Your online update uses outcomes that are not observed yet." — Yes, it did; FR07; re-run with realised feedback; numbers in v2; instant kept as labelled oracle bound.
RV21 "Your static conditional arm is Mondrian CP." — Yes; cited as such; the contribution is the interaction, not the arm.
RV22 "Per-cell ACI is multivalid/group-conditional online conformal (Bastani 2022) with cells as groups." — Yes; cited; ours is the LTSF instantiation and the audit; no new guarantee claimed.
RV23 "OLCP already combines adaptation and localisation with guarantees." — Different taxonomy (covariate-kernel vs fixed horizon × channel), different regime; no audit; positioned explicitly.
RV24 "Conditioning alone does not 'hurt' — it wins 21/32." — Corrected in v2; abstract now says inconsistent, CI spans zero.
RV25 "Where are PID / AcMCP / CopulaCPTS?" — [TODO decision]: add PID + AcMCP, state CopulaCPTS out of scope with reason, or add all three.
RV26 "Your calibration windows overlap 97%; n is not a sample size." — D007 stated in §3; quantile described as empirical over dependent scores; Limitations.
RV27 "Your decision result is an operating-point artefact." — Tuned-margin baseline [TODO]; FlagAll/FlagNone shown.
RV28 "You compare minima across 42 and 300 cells after telling us not to." — Removed; grid-invariant statistics used for cross-surface statements.
RV29 "Ablations on one configuration." — Re-run on 32; surface stated everywhere.
RV30 "'Best Winkler of seven' is false under realised feedback." — Corrected: best conformal Winkler; Gaussian narrowly ahead.

---

## 7. WHAT IS GOOD (so it is not lost in the rewrite)

The factorial design is the right design and the interaction is real, robust to the honest protocol, robust to backbone swap, and present at every horizon. The Sabashvili contrast is the strongest positioning sentence available and it is earned. The scoring-confound disclosure (§7) is the most reusable paragraph in the paper and should stay verbatim. The calibration-window separation of structural vs statistical failure is a genuinely good experiment; it only needs to be stated per surface. The reproducibility claim (12,625 values, max deviation 0.0) checked out in my clone for every static row. Keep the voice; cut the repetition.
