"""Figures for the S4 horizon-bucket ablation (EXP_S4_007 / EXP_S5_008).

Writes ONLY new files:
  figures/fig_kabl_fixed.png          own-grid vs fixed-grid worst-cell against K
  figures/fig_horizon_interaction.png static vs adaptive at K=1 vs K=6

`scripts/make_figures.py` is not modified and no existing fig_*.png is
overwritten. Style is matched to it deliberately: DejaVu Serif at 9pt,
grid alpha 0.3, dpi 200, greyscale fills only, target line as a black dashed
axhline at 0.90.

Reads results/horizon_ablation.json, and results/ha_ecl.json if present.
"""
import json
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.family": "serif", "font.serif": ["DejaVu Serif"], "font.size": 9,
                     "axes.grid": True, "grid.alpha": .3, "axes.edgecolor": "black",
                     "savefig.dpi": 200})

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "figures", "fig")
R = json.load(open(os.path.join(ROOT, "results", "horizon_ablation.json")))
ROWS = R["rows"]
KS = R["config"]["K_list"]
K_REF = R["config"]["K_ref"]
NCFG = len({(r["backbone"], r["dataset"], r["H"]) for r in ROWS})

_ECL_PATH = os.path.join(ROOT, "results", "ha_ecl.json")
ECL = json.load(open(_ECL_PATH)) if os.path.exists(_ECL_PATH) else None


def mean_of(rows, method, K, field):
    v = [r[field] for r in rows if r["method"] == method and r["K"] == K]
    return float(np.mean(v)) if v else float("nan")


# ============================================================
# fig_kabl_fixed -- the scoring confound, visible in one picture
# ============================================================
own = [mean_of(ROWS, "Proposed", K, "worst_own") for K in KS]
ref = [mean_of(ROWS, "Proposed", K, "worst_ref") for K in KS]

f, ax = plt.subplots(1, 2, figsize=(8.6, 3.2))

ax[0].plot(KS, own, "s--", color="0.55", label="scored on its own K-grid (confounded)")
ax[0].plot(KS, ref, "o-", color="0.1", label=f"scored on a fixed K={K_REF} grid")
ax[0].axhline(.9, color="k", ls="--", lw=1)
ax[0].set_xlabel("bucket count K")
ax[0].set_ylabel("mean worst-cell coverage")
ax[0].set_xticks(KS)
ax[0].set_ylim(.80, .92)
ax[0].legend(fontsize=6.8, loc="lower right")
ax[0].set_title("(a) Same half-widths, two scorings", fontsize=9)
for x, y in zip(KS, ref):
    ax[0].text(x, y - .009, f"{y:.3f}", ha="center", fontsize=6.2)

# the mechanism: cells on the own-grid rise with K, so its minimum falls
C = int(np.mean([r["C"] for r in ROWS]))
ncell = [K * C for K in KS]
ax[1].plot(ncell, own, "s--", color="0.55")
ax[1].set_xlabel(f"cells on the own-grid  (K x {C} channels)")
ax[1].set_ylabel("mean worst-cell coverage")
ax[1].set_xticks(ncell)
_span = max(own) - min(own)
ax[1].set_ylim(min(own) - .28 * _span, max(own) + .18 * _span)   # headroom for labels
ax[1].set_title("(b) A minimum over more cells is a lower minimum", fontsize=9)
for x, y, K in zip(ncell, own, KS):
    ax[1].text(x, y - .085 * _span, f"K={K}", ha="center", va="top", fontsize=6.2)

f.suptitle(f"Horizon-bucket ablation, mean over {NCFG} ETT configs, target 90%",
           fontsize=10)
f.tight_layout()
f.savefig(f"{OUT}_kabl_fixed.png", bbox_inches="tight")
plt.close(f)
print("wrote fig_kabl_fixed.png")


# ============================================================
# fig_horizon_interaction -- the second interaction
# ============================================================
panels = [("ETT (32 configs)", ROWS, [1, K_REF])]
if ECL is not None:
    panels.append((f"Electricity ({len({(r['backbone'], r['H']) for r in ECL['rows']})} configs)",
                   ECL["rows"], sorted(ECL["config"]["K_list"])))

f, ax = plt.subplots(1, len(panels), figsize=(4.6 * len(panels), 3.4), squeeze=False)
ax = ax[0]

for i, (title, rows, ks) in enumerate(panels):
    k_lo, k_hi = ks[0], ks[-1]
    a = ax[i]
    x = np.arange(2)
    w = .36
    static = [mean_of(rows, "Cond", k_lo, "worst_ref"), mean_of(rows, "Cond", k_hi, "worst_ref")]
    adapt = [mean_of(rows, "Proposed", k_lo, "worst_ref"),
             mean_of(rows, "Proposed", k_hi, "worst_ref")]
    a.bar(x - w / 2, static, w, color="0.72", edgecolor="k", label="static (Cond)")
    a.bar(x + w / 2, adapt, w, color="0.28", edgecolor="k", label="adaptive (Proposed)")
    a.axhline(.9, color="k", ls="--", lw=1)
    for j, (s, d) in enumerate(zip(static, adapt)):
        a.text(j - w / 2, s + .004, f"{s:.4f}", ha="center", fontsize=6.5)
        a.text(j + w / 2, d + .004, f"{d:.4f}", ha="center", fontsize=6.5)
    a.set_xticks(x)
    a.set_xticklabels([f"K={k_lo}\nchannel only", f"K={k_hi}\nhorizon x channel"], fontsize=8)
    a.set_ylim(.40, .95)
    a.set_ylabel("mean worst-cell coverage" if i == 0 else "")
    ds, da = static[1] - static[0], adapt[1] - adapt[0]
    a.set_title(f"{title}\nhorizon axis: static {ds:+.4f}, adaptive {da:+.4f}", fontsize=8.5)

# one shared legend, below the axes, so it cannot sit on top of a bar
h, lb = ax[0].get_legend_handles_labels()
f.legend(h, lb, fontsize=8, ncol=2, loc="lower center", bbox_to_anchor=(.5, -.06),
         frameon=False)
f.suptitle("The horizon axis without adaptation and with it "
           "(fixed scoring grid, target 90%)", fontsize=9.5)
f.tight_layout()
f.savefig(f"{OUT}_horizon_interaction.png", bbox_inches="tight")
plt.close(f)
print("wrote fig_horizon_interaction.png")
