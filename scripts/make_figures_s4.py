"""Figures for the S4 evidence: the rolling-coverage trace and the calibration-size curve.

fig_traces.png is the figure the project has been arguing in tables: on Electricity the
test block crosses a season, static global conformal dives for ~3 weeks around test path
163 (both backbones, 7/8 configs), and the adaptive conditional layer holds through the
identical window on identical forecasts. DLinear / H=720 is plotted because it is the
deepest dive (0.7750 vs 0.8579). fig_gate.png, the previous headline gate figure, plots
the smoothed aggregate that DELTA_002 section 1 shows can hide exactly this behaviour;
this figure replaces that role.

fig_calwindow.png shows EXP_S4_006 on Electricity: every baseline flat in calibration
size, Proposed still climbing at the full block -- the sample-limited-not-structurally-
limited argument (Q23) in one panel.

Reads results/tr_ecl.json and results/cw_ecl.json. Writes figures/*.png. Modifies nothing.
"""
import json, os, sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
F = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
os.makedirs(F, exist_ok=True)

tr = json.load(open(os.path.join(R, "tr_ecl.json")))
rows = [x for x in tr["rows"] if x["backbone"].lower() == "dlinear" and x["H"] == 720]
w = tr["config"]["window"]
fig, ax = plt.subplots(figsize=(9, 4.2))
style = {"Global": ("#c0392b", "-"), "ACI": ("#7f8c8d", "--"), "Proposed": ("#1a5276", "-")}
for m in ("Global", "ACI", "Proposed"):
    r = next(x for x in rows if x["method"] == m)
    xs = list(range(w, w + len(r["roll"])))
    ax.plot(xs, r["roll"], style[m][1], color=style[m][0], lw=2, label=m)
g = next(x for x in rows if x["method"] == "Global")
ax.axvline(g["min_at_path"], color="#c0392b", lw=0.8, ls=":", alpha=0.7)
ax.annotate(f"worst window\npath {g['min_at_path']}: {g['min_roll']:.3f}",
            xy=(g["min_at_path"], g["min_roll"]), xytext=(g["min_at_path"] - 62, 0.795),
            fontsize=8, arrowprops=dict(arrowstyle="->", lw=0.8))
ax.axhline(0.90, color="k", lw=0.8, ls="--", alpha=0.6)
ax.axhline(0.85, color="k", lw=0.6, ls=":", alpha=0.5)
ax.set_xlabel(f"test path (one per day), trailing {w}-path window")
ax.set_ylabel("rolling coverage")
ax.set_title("Electricity, DLinear, H=720 -- the seasonal dive static conformal takes and adaptation does not")
ax.legend(frameon=False, loc="lower left"); ax.set_ylim(0.74, 1.0)
fig.tight_layout(); fig.savefig(os.path.join(F, "fig_traces.png"), dpi=160); plt.close(fig)
print("wrote figures/fig_traces.png")

cw = json.load(open(os.path.join(R, "cw_ecl.json")))
fr = sorted({r["frac"] for r in cw["rows"]})
fig, ax = plt.subplots(figsize=(7, 4.2))
for m, c in (("Global", "#c0392b"), ("MSCP", "#b7950b"), ("ACI", "#7f8c8d"), ("Proposed", "#1a5276")):
    ys, ns = [], []
    for f in fr:
        v = [r for r in cw["rows"] if r["method"] == m and r["frac"] == f]
        ys.append(sum(x["worst_cell"] for x in v) / len(v))
        ns.append(sum(x["n_cal"] for x in v) / len(v))
    ax.plot(ns, ys, "o-", color=c, lw=2, label=m)
ax.set_xlabel("calibration paths (most recent kept)")
ax.set_ylabel("worst-cell coverage, fixed K=6 grid")
ax.set_title("Electricity -- baselines plateau; the conditional-adaptive layer is data-limited, not structure-limited")
ax.axhline(0.90, color="k", lw=0.8, ls="--", alpha=0.6)
ax.legend(frameon=False, loc="lower right")
fig.tight_layout(); fig.savefig(os.path.join(F, "fig_calwindow.png"), dpi=160); plt.close(fig)
print("wrote figures/fig_calwindow.png")
