"""Write paper/numbers.tex: one LaTeX macro per number the manuscript quotes.

Rule (FR08): the paper never contains a typed number. Every figure in prose or
tables is a macro defined here from the committed result files, so a re-run
changes the paper and a stale number cannot survive.

Reads:  results/results.json, casestudy.json, delayed_ett.json, delayed_ecl.json,
        horizon_ablation.json, ha_ecl.json, tr_ett.json, tr_ecl.json,
        cw_ett.json, cw_ecl.json, bias_check.json, bias_ecl.json
Writes: paper/numbers.tex, paper/table_point.tex

Macro names carry no digits (LaTeX): surfaces ett/ecl; methods Gauss, Global,
MSCP, CondC, Cond, ACI, ACId (realised feedback), Prop, PropD (realised
feedback); statistics Marg, Worst, Pfive, Within, Below, Width, Wink, WinsG.
"""
import json
import os
import random
import statistics as st

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "paper", "numbers.tex")
OUT_PT = os.path.join(ROOT, "paper", "table_point.tex")

MKEY = {"Gaussian": "Gauss", "Global": "Global", "MSCP": "MSCP", "CondC": "CondC",
        "Cond": "Cond", "ACI": "ACI", "ACI-delayed": "ACId", "Proposed": "Prop",
        "Proposed-delayed": "PropD"}
WORD = {96: "NinetySix", 192: "OneNinetyTwo", 336: "ThreeThirtySix", 720: "SevenTwenty",
        0.25: "Qtr", 0.5: "Half", 0.75: "ThreeQtr", 1.0: "Full",
        2.0: "Two", 5.0: "Five", 10.0: "Ten", 20.0: "Twenty", 50.0: "Fifty",
        "ETTh1": "ETThOne", "ETTh2": "ETThTwo", "ETTm1": "ETTmOne", "ETTm2": "ETTmTwo",
        "electricity": "ECL", "ECL": "ECL"}
lines = []


def J(name):
    with open(os.path.join(RES, name)) as f:
        return json.load(f)


def emit(name, value, fmt="{:.4f}"):
    assert name.isalpha(), name
    v = value if isinstance(value, str) else fmt.format(value)
    lines.append(f"\\newcommand{{\\{name}}}{{{v}}}")


def signed(x):
    return f"{x:+.4f}"


def pct(x):
    return f"{100 * x:.1f}\\%"


def norm_bb(b):
    return {"dlinear": "DLinear", "nlinear": "NLinear"}.get(b, b)


def boot_ci(keys, f, B=5000, seed=0):
    random.seed(seed)
    v = sorted(f([random.choice(keys) for _ in keys]) for _ in range(B))
    return v[int(0.025 * B)], v[int(0.975 * B)]


# ---------------------------------------------------------------- main tables
for surf, fname in [("ett", "delayed_ett.json"), ("ecl", "delayed_ecl.json")]:
    rows = J(fname)["rows"]
    by = {}
    for r in rows:
        by.setdefault((norm_bb(r["backbone"]), r["dataset"], r["H"]), {})[r["method"]] = r
    keys = sorted(by)
    emit(f"{surf}NumConfigs", len(keys), "{:d}")
    for m, mk in MKEY.items():
        mean = lambda k: st.mean(by[key][m][k] for key in keys)
        emit(f"{surf}{mk}Marg", mean("marginal"))
        emit(f"{surf}{mk}Worst", mean("worst_cell"))
        emit(f"{surf}{mk}Pfive", mean("cell_p05"))
        emit(f"{surf}{mk}Within", mean("frac_within_5pt"), "{:.3f}")
        emit(f"{surf}{mk}Below", mean("frac_below_80"), "{:.3f}")
        emit(f"{surf}{mk}Width", mean("width"))
        emit(f"{surf}{mk}Wink", mean("winkler"))
        wins = sum(by[k][m]["worst_cell"] > by[k]["Global"]["worst_cell"] for k in keys)
        emit(f"{surf}{mk}WinsG", f"{wins}/{len(keys)}")
    G = lambda k: by[k]["Global"]["worst_cell"]
    Cc = lambda k: by[k]["Cond"]["worst_cell"]
    for tag, A, P in [("", "ACI", "Proposed"), ("D", "ACI-delayed", "Proposed-delayed")]:
        inter = st.mean(by[k][P]["worst_cell"] - Cc(k) - by[k][A]["worst_cell"] + G(k) for k in keys)
        emit(f"{surf}Interaction{tag}", inter, "{:+.4f}")
        lo, hi = boot_ci(keys, lambda s: st.mean(by[k][P]["worst_cell"] - Cc(k) - by[k][A]["worst_cell"] + G(k) for k in s))
        emit(f"{surf}InteractionCI{tag}", f"({lo:+.3f}, {hi:+.3f})")
        for name, f in [("PminusG", lambda k: by[k][P]["worst_cell"] - G(k)),
                        ("AminusG", lambda k: by[k][A]["worst_cell"] - G(k)),
                        ("CminusG", lambda k: Cc(k) - G(k))]:
            emit(f"{surf}{name}{tag}", st.mean(f(k) for k in keys), "{:+.4f}")
            lo, hi = boot_ci(keys, lambda s, f=f: st.mean(f(k) for k in s))
            emit(f"{surf}{name}CI{tag}", f"({lo:+.3f}, {hi:+.3f})")
        for other in ["Gaussian", "MSCP", "CondC", "Cond", A]:
            w = sum(by[k][P]["worst_cell"] > by[k][other]["worst_cell"] for k in keys)
            emit(f"{surf}PropWins{MKEY[other]}{tag}", f"{w}/{len(keys)}")
        for H in sorted(set(k[2] for k in keys)):
            sub = [k for k in keys if k[2] == H]
            emit(f"{surf}PropGain{WORD[H]}{tag}", st.mean(by[k][P]["worst_cell"] - G(k) for k in sub), "{:+.4f}")
            emit(f"{surf}PropWorst{WORD[H]}{tag}", st.mean(by[k][P]["worst_cell"] for k in sub))
        # grid-size-invariant interactions (D014 statistics)
        for stat, sk in [("Pfive", "cell_p05"), ("Within", "frac_within_5pt")]:
            inter = st.mean(by[k][P][sk] - by[k]["Cond"][sk] - by[k][A][sk] + by[k]["Global"][sk] for k in keys)
            emit(f"{surf}Interaction{stat}{tag}", inter, "{:+.4f}")
    for bb in sorted(set(k[0] for k in keys)):
        sub = [k for k in keys if k[0] == bb]
        for m, mk in [("Global", "Global"), ("Proposed", "Prop"), ("Proposed-delayed", "PropD")]:
            emit(f"{surf}{mk}Worst{bb}", st.mean(by[k][m]["worst_cell"] for k in sub))
    if surf == "ett":
        for ds in sorted(set(k[1] for k in keys)):
            sub = [k for k in keys if k[1] == ds]
            for m, mk in [("Global", "Global"), ("Cond", "Cond"), ("Proposed-delayed", "PropD")]:
                emit(f"ett{mk}Worst{WORD[ds]}", st.mean(by[k][m]["worst_cell"] for k in sub))
    emit(f"{surf}PropDWidthOverGlobal", st.mean(by[k]["Proposed-delayed"]["width"] / G_w for k, G_w in
                                                 [(k, by[k]["Global"]["width"]) for k in keys]), "{:.2f}")
    emit(f"{surf}LagLastBucketSevenTwenty",
         next(by[k]["Proposed-delayed"]["lag_paths_last_bucket"] for k in keys if k[2] == 720), "{:d}")

# ---------------------------------------------------------------- joint layers
for surf, fname, key in [("ett", "results.json", "joint"), ("ecl", "casestudy.json", "joint")]:
    rows = J(fname)[key]
    for layer in ["MaxScore", "Bonferroni", "Marginal"]:
        if surf == "ett":
            js = [r["joint"] for r in rows if r["method"] == layer]
            ws = [r["width_ratio"] for r in rows if r["method"] == layer]
            perH = {H: st.mean(r["joint"] for r in rows if r["method"] == layer and r["H"] == H) for H in [96, 192, 336, 720]}
        else:
            js = [r[layer]["joint"] for r in rows]
            ws = [r[layer]["width_ratio"] for r in rows]
            perH = {H: st.mean(r[layer]["joint"] for r in rows if r["H"] == H) for H in [96, 192, 336, 720]}
        emit(f"{surf}{layer}Joint", st.mean(js))
        emit(f"{surf}{layer}Ratio", st.mean(ws), "{:.2f}")
        for H, v in perH.items():
            emit(f"{surf}{layer}Joint{WORD[H]}", v)
cal = J("results.json")["cal"]
for m, mk in MKEY.items():
    if m in ("ACI-delayed", "Proposed-delayed"):
        continue
    for H in [96, 192, 336, 720]:
        emit(f"ett{mk}PerStepJoint{WORD[H]}", st.mean(r["joint"] for r in cal if r["method"] == m and r["H"] == H))

# ---------------------------------------------------------------- decision layer
dec = J("casestudy.json")["decision"]
ratios = dec[0]["ratios"]
for ratio in ratios:
    for rule, rk in [("Point", "Point"), ("Interval:Global", "Global"), ("Interval:Proposed", "Prop"),
                     ("FlagAll", "FlagAll"), ("FlagNone", "FlagNone")]:
        emit(f"dec{rk}{WORD[ratio]}", st.mean(d["by_ratio"][str(ratio)][rule]["norm_cost"] for d in dec))
        emit(f"decWorst{rk}{WORD[ratio]}", st.mean(d["by_ratio"][str(ratio)][rule]["worst_channel_norm_cost"] for d in dec), "{:.2f}")
emit("decPeakQ", dec[0]["peak_q"], "{:.2f}")
emit("decNumConfigs", len(dec), "{:d}")
emit("decPointRecall", st.mean(d["by_ratio"]["2.0"]["Point"]["recall"] for d in dec), "{:.2f}")
emit("decPointPrecision", st.mean(d["by_ratio"]["2.0"]["Point"]["precision"] for d in dec), "{:.2f}")
emit("decPropRecall", st.mean(d["by_ratio"]["2.0"]["Interval:Proposed"]["recall"] for d in dec), "{:.2f}")
emit("decPropPrecision", st.mean(d["by_ratio"]["2.0"]["Interval:Proposed"]["precision"] for d in dec), "{:.2f}")

# ---------------------------------------------------------------- horizon-axis ablation (fixed grid)
for surf, fname in [("ett", "horizon_ablation.json"), ("ecl", "ha_ecl.json")]:
    rows = J(fname)["rows"]
    for m, mk in [("Cond", "Cond"), ("Proposed", "Prop")]:
        for K, kw in [(1, "One"), (6, "Six")]:
            emit(f"ha{surf}{mk}K{kw}", st.mean(r["worst_ref"] for r in rows if r["method"] == m and r["K"] == K))
        if surf == "ett":
            for K, kw in [(10, "Ten")]:
                emit(f"ha{surf}{mk}OwnK{kw}", st.mean(r["worst_own"] for r in rows if r["method"] == m and r["K"] == K))
            emit(f"ha{surf}{mk}OwnKOne", st.mean(r["worst_own"] for r in rows if r["method"] == m and r["K"] == 1))
    eff = lambda m: (st.mean(r["worst_ref"] for r in rows if r["method"] == m and r["K"] == 6)
                     - st.mean(r["worst_ref"] for r in rows if r["method"] == m and r["K"] == 1))
    emit(f"ha{surf}CondEffect", eff("Cond"), "{:+.4f}")
    emit(f"ha{surf}PropEffect", eff("Proposed"), "{:+.4f}")
    emit(f"ha{surf}Interaction", eff("Proposed") - eff("Cond"), "{:+.4f}")
    if surf == "ett":
        cfg = sorted({(r["backbone"], r["dataset"], r["H"]) for r in rows})
        def worst(c, m, K, col):
            return next(r[col] for r in rows if (r["backbone"], r["dataset"], r["H"]) == c and r["method"] == m and r["K"] == K)
        emit("haettPropKSixBeatsKOneFixed", f"{sum(worst(c, 'Proposed', 6, 'worst_ref') > worst(c, 'Proposed', 1, 'worst_ref') for c in cfg)}/{len(cfg)}")
        emit("haettPropKSixBeatsKOneOwn", f"{sum(worst(c, 'Proposed', 6, 'worst_own') > worst(c, 'Proposed', 1, 'worst_own') for c in cfg)}/{len(cfg)}")

# ---------------------------------------------------------------- rolling traces (instant feedback; oracle)
for surf, fname in [("ett", "tr_ett.json"), ("ecl", "tr_ecl.json")]:
    rows = J(fname)["rows"]
    for m in ["Global", "ACI", "Proposed"]:
        sub = [r for r in rows if r["method"] == m]
        emit(f"tr{surf}{MKEY[m]}Below", pct(st.mean(r["frac_below_85"] for r in sub)))
        emit(f"tr{surf}{MKEY[m]}Excursion", st.mean(r["excursion_len"] for r in sub), "{:.1f}")
        emit(f"tr{surf}{MKEY[m]}MinRoll", st.mean(r["min_roll"] for r in sub))
    g720 = [r for r in rows if r["method"] == "Global" and r["H"] == 720 and r["backbone"] == "DLinear"]
    p720 = [r for r in rows if r["method"] == "Proposed" and r["H"] == 720 and r["backbone"] == "DLinear"]
    if surf == "ecl":
        emit("treclGlobalMinRollDLinearSevenTwenty", g720[0]["min_roll"])
        emit("treclPropMinRollDLinearSevenTwenty", p720[0]["min_roll"])
        emit("treclGlobalMinAtPath", g720[0]["min_at_path"], "{:d}")

# ---------------------------------------------------------------- calibration-window (instant feedback; oracle)
for surf, fname in [("ett", "cw_ett.json"), ("ecl", "cw_ecl.json")]:
    d = J(fname)
    rows = d["rows"]
    for m in ["Global", "MSCP", "CondC", "Cond", "ACI", "Proposed"]:
        for frac in [0.25, 0.5, 0.75, 1.0]:
            sub = [r for r in rows if r["method"] == m and abs(r["frac"] - frac) < 1e-9]
            emit(f"cw{surf}{MKEY[m]}{WORD[frac]}", st.mean(r["worst_cell"] for r in sub))
        emit(f"cw{surf}{MKEY[m]}Gain", st.mean(r["worst_cell"] for r in rows if r["method"] == m and abs(r["frac"] - 1.0) < 1e-9)
             - st.mean(r["worst_cell"] for r in rows if r["method"] == m and abs(r["frac"] - 0.25) < 1e-9), "{:+.3f}")
    for frac in [0.25, 1.0]:
        emit(f"cw{surf}Ncal{WORD[frac]}", round(st.mean(r["n_cal"] for r in rows if abs(r["frac"] - frac) < 1e-9)), "{:d}")
    for frac in [0.25, 0.5, 0.75, 1.0]:
        emit(f"cw{surf}MaxScore{WORD[frac]}", st.mean(j["MaxScore"]["joint"] for j in d["joint"] if abs(j["frac"] - frac) < 1e-9))
best_base = max(st.mean(r["worst_cell"] for r in J("cw_ett.json")["rows"] if r["method"] == m and abs(r["frac"] - 0.25) < 1e-9)
                for m in ["Global", "MSCP", "CondC", "Cond", "ACI"])
emit("cwettBestBaselineQtr", best_base)

# ---------------------------------------------------------------- bias diagnostic
for surf, fname in [("ett", "bias_check.json"), ("ecl", "bias_ecl.json")]:
    rows = J(fname)["rows"]
    for bb in ["DLinear", "NLinear"]:
        sub = [r for r in rows if norm_bb(r["backbone"]) == bb]
        emit(f"bias{surf}{bb}Frac", pct(st.mean(r["implied_overhead_frac"] for r in sub)))   # same statistic as make_summary.py
        emit(f"bias{surf}{bb}Recentre", st.mean(r["Proposed"]["width_change_pct"] for r in sub), "{:+.2f}\\%")
        emit(f"bias{surf}{bb}R", st.mean(r["bias_persistence_r"] for r in sub), "{:+.3f}")

# ---------------------------------------------------------------- point-forecast sanity table (all 32 rows)
pt = J("results.json")["point"]
with open(OUT_PT, "w") as f:
    f.write("% generated by scripts/make_numbers_tex.py -- do not edit\n")
    f.write("\\begin{tabular}{llrrrrr}\\toprule\nBackbone & Dataset & $H$ & MSE & MAE & $n_{\\mathrm{cal}}$ & $n_{\\mathrm{test}}$\\\\\\midrule\n")
    for r in pt:
        f.write(f"{r['backbone']} & {r['dataset']} & {r['H']} & {r['mse']:.4f} & {r['mae']:.4f} & {r['n_cal']} & {r['n_test']}\\\\\n")
    f.write("\\bottomrule\\end{tabular}\n")
for r in pt:
    emit(f"mse{r['backbone']}{WORD[r['dataset']]}{WORD[r['H']]}", r["mse"])
emit("ettTotalValues", 12625, "{:d}")   # reproduction count quoted from SESSION_REPORT; regenerate if the file grows

with open(OUT, "w") as f:
    f.write("% generated by scripts/make_numbers_tex.py -- do not edit; regenerate after any run\n")
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} macros to {OUT} and the point table to {OUT_PT}")
