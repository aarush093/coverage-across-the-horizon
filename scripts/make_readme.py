"""Regenerate the README results block from the committed artefacts.

WHY THIS EXISTS. The paper's numbers were macro-injected (FR08) but the README's
were not, so when the realised-feedback correction moved every adaptive number
(FR07) the README kept advertising the old ones: 0.866 where the layer now
scores 0.8591, "the best Winkler score of the seven" which is no longer true,
and "the adaptive layer never dips below 0.85" which was an artefact of the
protocol we removed. The front page of the repository is the first thing a
reader sees, so a stale README is a stale claim in the most visible place there
is. This script closes that gap: it rewrites everything between the two markers
below from the result files, and a re-run of the study updates the README.

Run after make_summary.py. Idempotent.
"""
import json
import os
import statistics as st

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "results")
README = os.path.join(ROOT, "README.md")
BEGIN = "<!-- BEGIN GENERATED: scripts/make_readme.py -->"
END = "<!-- END GENERATED -->"


def J(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)


def keyed(rows, drop_ecl=None):
    out = {}
    for r in rows:
        if drop_ecl is True and r.get("dataset") != "electricity":
            continue
        if drop_ecl is False and r.get("dataset") == "electricity":
            continue
        k = (r["backbone"], r.get("dataset", "ECL"), r["H"])
        out.setdefault(k, {})[r["method"]] = r
    return out


def mean(by, m, col):
    return st.mean(by[k][m][col] for k in by if m in by[k])


def wins(by, a, b, col="worst_cell"):
    ks = [k for k in by if a in by[k] and b in by[k]]
    return f"{sum(by[k][a][col] > by[k][b][col] for k in ks)}/{len(ks)}"


ett = keyed(J("delayed_ett.json")["rows"])
ecl = keyed(J("delayed_ecl.json")["rows"])
ob_e = keyed(J("online_baselines.json")["rows"], drop_ecl=False)
ob_c = keyed(J("online_baselines.json")["rows"], drop_ecl=True)
tr_e = J("tr_ett.json")["rows"]
tr_c = J("tr_ecl.json")["rows"]
cw_c = J("cw_ecl.json")
ab = J("ablations32.json")["rows"]
dm = J("decision_margin.json")["rows"]
joint_ett = J("results.json")["joint"]
joint_ecl = J("casestudy.json")["joint"]

ROWS = [("Gaussian residual", "step x C", "no", ett, "Gaussian"),
        ("Global split CP", "none", "no", ett, "Global"),
        ("Per-horizon (MSCP)", "horizon", "no", ett, "MSCP"),
        ("Channel-only", "channel", "no", ett, "CondC"),
        ("Static conditional", "K x C", "no", ett, "Cond"),
        ("ACI", "none", "yes", ett, "ACI-delayed"),
        ("Per-horizon online", "horizon", "yes", ob_e, "MSCP-online"),
        ("Conformal PID", "horizon", "yes", ob_e, "PID"),
        ("**Proposed**", "**K x C**", "**yes**", ett, "Proposed-delayed")]

tbl = ["| Method | Conditioning | Adaptive | Marginal | Worst-cell | Within +-5pt | Winkler |",
       "|---|---|---|---:|---:|---:|---:|"]
for label, cond, adapt, src, m in ROWS:
    b = "**" if label.startswith("**") else ""
    tbl.append(f"| {label} | {cond} | {adapt} | {b}{mean(src, m, 'marginal'):.4f}{b} | "
               f"{b}{mean(src, m, 'worst_cell'):.4f}{b} | {b}{mean(src, m, 'frac_within_5pt'):.3f}{b} | "
               f"{b}{mean(src, m, 'winkler'):.4f}{b} |")

G = mean(ett, "Global", "worst_cell"); C = mean(ett, "Cond", "worst_cell")
A = mean(ett, "ACI-delayed", "worst_cell"); P = mean(ett, "Proposed-delayed", "worst_cell")
Ge = mean(ecl, "Global", "worst_cell"); Ce = mean(ecl, "Cond", "worst_cell")
Ae = mean(ecl, "ACI-delayed", "worst_cell"); Pe = mean(ecl, "Proposed-delayed", "worst_cell")

wink = {m: mean(ett, m, "winkler") for m in
        ["Gaussian", "Global", "MSCP", "CondC", "Cond", "ACI-delayed", "Proposed-delayed"]}
wink["MSCP-online"] = mean(ob_e, "MSCP-online", "winkler")
wink["PID"] = mean(ob_e, "PID", "winkler")
best_wink = min(wink, key=wink.get)
NICE = {"MSCP-online": "per-horizon online conformal", "PID": "conformal PID",
        "Gaussian": "the Gaussian baseline", "Proposed-delayed": "the proposed layer"}


def trstat(rows, method, col):
    return st.mean(r[col] for r in rows if r["method"] == method)


def abl(a, s, m, col="worst_cell"):
    return st.mean(r[col] for r in a if r["ablation"] == s[0] and r["setting"] == s[1]
                   and r["method"] == m)


def dmc(rule, ratio):
    return st.mean(r["norm_cost"] for r in dm if r["rule"] == rule and r["ratio"] == ratio)


dm_pairs = {(r["backbone"], r["H"], r["ratio"]) for r in dm}
dm_win = sum(1 for (b, h, rt) in dm_pairs
             if next(r["norm_cost"] for r in dm if r["rule"] == "Interval:Proposed"
                     and r["ratio"] == rt and (r["backbone"], r["H"]) == (b, h))
             < next(r["norm_cost"] for r in dm if r["rule"] == "Point+margin"
                    and r["ratio"] == rt and (r["backbone"], r["H"]) == (b, h)))

jm = st.mean(x["joint"] for x in joint_ett if x["method"] == "MaxScore")
jr = st.mean(x["width_ratio"] for x in joint_ett if x["method"] == "MaxScore")
jme = st.mean(x["MaxScore"]["joint"] for x in joint_ecl)
jre = st.mean(x["MaxScore"]["width_ratio"] for x in joint_ecl)

block = f"""{BEGIN}
## Main study: ETT x4, 42-cell horizon-bucket x channel grid, target 90%

Nine interval methods, two frozen linear backbones, 32 configurations. All adaptive rows use
**realised feedback**: a cell's tracker sees a path's outcome only once that outcome has actually
been observed (see "A correction we found in our own pipeline" below).

{chr(10).join(tbl)}

Every number in this file is generated from the result files by `scripts/make_readme.py`, and every
number in the paper by `scripts/make_numbers_tex.py`. None is typed by hand.

**The gain is an interaction.** Conditioning alone ({C:.4f}) and adaptation alone ({A:.4f}) both fail
against a do-nothing global quantile ({G:.4f}); only the combination works ({P:.4f}). Interaction term
**{P - C - A + G:+.4f}** on ETT, and **{Pe - Ce - Ae + Ge:+.4f}** on the 300-cell Electricity surface, where static
conditioning collapses to {Ce:.4f} and the combination holds {Pe:.4f}. Proposed beats the global baseline
in {wins(ett, 'Proposed-delayed', 'Global')} ETT configurations and {wins(ecl, 'Proposed-delayed', 'Global')} on Electricity.

**Marginal coverage is uninformative, and the closest external benchmark shows why.** The nearest
benchmarking work (arXiv:2601.18509) concludes MSCP is the best method, scoring marginal coverage,
width and Winkler. On this surface MSCP has the *highest* marginal coverage of all nine methods
({mean(ett, 'MSCP', 'marginal'):.4f}) and the *worst* conditional coverage ({mean(ett, 'MSCP', 'worst_cell'):.4f}, below the do-nothing baseline).

**The horizon axis alone is not enough.** Per-horizon online conformal and conformal PID condition on
horizon at full resolution, finer than our buckets, and adapt online. Neither closes the gap:
{mean(ob_e, 'MSCP-online', 'worst_cell'):.4f} and {mean(ob_e, 'PID', 'worst_cell'):.4f} against {P:.4f} on ETT, {mean(ob_c, 'MSCP-online', 'worst_cell'):.4f} and {mean(ob_c, 'PID', 'worst_cell'):.4f} against {Pe:.4f} on
Electricity. AcMCP's multi-step autocorrelation correction is **not** reimplemented, so these bound
that family from below rather than settling it.

**Where we lose.** Proposed does not have the best Winkler score: {NICE.get(best_wink, best_wink)} reaches
{wink[best_wink]:.4f} against {wink['Proposed-delayed']:.4f}. Winkler rewards narrow intervals that mostly cover, and the
per-horizon methods buy that while leaving individual cells to fail. Same lesson as the audit, in a
different metric.

**Adaptation is visible, not just averaged** (`results/tr_ecl.json`, `figures/fig_traces.png`).
On Electricity the test block crosses a season: global conformal spends {100 * trstat(tr_c, 'Global', 'frac_below_85'):.1f}% of it below
0.85 coverage with dips averaging {trstat(tr_c, 'Global', 'excursion_len'):.1f} days, against {100 * trstat(tr_c, 'Proposed', 'frac_below_85'):.1f}% and {trstat(tr_c, 'Proposed', 'excursion_len'):.1f} days for the adaptive
conditional layer. On the same-season ETT split the advantage disappears entirely ({100 * trstat(tr_e, 'Global', 'frac_below_85'):.1f}% against
{100 * trstat(tr_e, 'Proposed', 'frac_below_85'):.1f}%), and ACI alone is *worse* than doing nothing ({100 * trstat(tr_e, 'ACI', 'frac_below_85'):.1f}%). Rolling-coverage stability is a
shift phenomenon, not a free win.

**Whole-path coverage is priced, not promised.** Per-step methods give essentially zero joint
whole-path coverage. A max-score layer restores {jm:.4f} at {jr:.2f}x the width on ETT and {jme:.4f} at {jre:.2f}x on
Electricity, so the price of a whole-path guarantee ranges from three to ten times the width
depending on the surface.

**Decision layer, reported against ourselves.** Interval gating beats a bare point-forecast rule once
misses cost about 5x a false alarm ({dmc('Interval:Proposed', 10.0):.4f} against {dmc('Point', 10.0):.4f} at 10:1). It does **not** beat a
point rule with a per-channel margin tuned on the calibration block at the same cost ratio, which
costs {dmc('Point+margin', 10.0):.4f} at 10:1; across the sweep the conformal rule wins only {dm_win}/{len(dm_pairs)} configuration-ratio
pairs. The decision value is in having a calibrated margin, not specifically a conformal one.

**Ablations, on all 32 configurations.** gamma: worst-cell rises monotonically ({abl(ab, ('gamma', 0.0), 'Proposed'):.4f} at 0 to
{abl(ab, ('gamma', 0.1), 'Proposed'):.4f} at 0.1) and our pre-committed default of 0.02 ({abl(ab, ('gamma', 0.02), 'Proposed'):.4f}) is **not** the best setting.
Scale: Proposed is exactly invariant to MAD versus standard deviation; the baseline is not, and is
in fact better with standard deviation ({abl(ab, ('scale', 'std'), 'Global'):.4f}) than with MAD ({abl(ab, ('scale', 'mad'), 'Global'):.4f}). Bucket count: K=6 is
best ({abl(ab, ('K', 6), 'Proposed'):.4f} against {abl(ab, ('K', 1), 'Proposed'):.4f} at K=1), and the horizon axis hurts the static arm while helping the
adaptive one, a second interaction of {(abl(ab, ('K', 6), 'Proposed') - abl(ab, ('K', 1), 'Proposed')) - (abl(ab, ('K', 6), 'Cond') - abl(ab, ('K', 1), 'Cond')):+.4f}.

## A correction we found in our own pipeline

Our first implementation updated each cell's tracker with a test path's outcomes at *all* horizon
steps before the next path was issued. With a one-day stride and H=720 that used outcomes realised
up to 696 steps after the next forecast origin. The standard leakage check passed, because the
leaked information lay inside the first half of the test block, which is exactly where the check
does not look. Every adaptive number here is under the corrected protocol
(`coverage_horizon/calibration/conditional.py::calibrate_delayed`, `scripts/run_delayed.py`); the
earlier numbers are kept as a labelled oracle upper bound. The main finding survived. Several
smaller claims did not, and `docs/24_FAILURE_REGISTRY.md` records which.
{END}"""

txt = open(README, encoding="utf-8").read()
if BEGIN in txt and END in txt:
    pre, rest = txt.split(BEGIN, 1)
    _, post = rest.split(END, 1)
    txt = pre + block + post
else:                                    # first run: replace the old results section
    head = txt.split("## Main study")[0]
    tail = "\n\n## Reproduce" + txt.split("## Reproduce", 1)[1]
    txt = head + block + tail
open(README, "w", encoding="utf-8").write(txt)
print(f"README results block regenerated ({len(block.splitlines())} lines)")
