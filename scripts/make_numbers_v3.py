"""Macros for the artefacts added after Draft v2: online baselines, the
32-configuration ablations, and the tuned-margin decision evaluation.

Kept separate from make_numbers_tex.py so that the original generator, which
the committed v2 build depends on, is not touched. The paper inputs both.
Same rule as before (FR08): nothing in the manuscript is typed.
"""
import json
import os
import statistics as st

ROOT = os.path.join(os.path.dirname(__file__), "..")
RES = os.path.join(ROOT, "results")
OUT = os.path.join(ROOT, "paper", "numbers_v3.tex")

MK = {"Global": "Global", "Cond": "Cond", "ACI": "ACI", "Proposed": "Prop",
      "MSCP-online": "MSCPon", "PID": "PID"}
WORD = {1: "One", 3: "Three", 6: "Six", 10: "Ten",
        0.0: "Zero", 0.005: "Tiny", 0.02: "Default", 0.05: "Mid", 0.1: "Big",
        "mad": "MAD", "std": "SD",
        2.0: "Two", 5.0: "Five", 10.0: "Ten", 20.0: "Twenty", 50.0: "Fifty"}
lines = []


def emit(name, value, fmt="{:.4f}"):
    assert name.isalpha(), name
    lines.append(f"\\newcommand{{\\{name}}}{{{value if isinstance(value, str) else fmt.format(value)}}}")


def J(n):
    with open(os.path.join(RES, n)) as f:
        return json.load(f)


# ------------------------------------------------------- online baselines
rows = J("online_baselines.json")["rows"]
for surf, sel in [("ett", lambda r: r["dataset"] != "electricity"),
                  ("ecl", lambda r: r["dataset"] == "electricity")]:
    sub = [r for r in rows if sel(r)]
    by = {}
    for r in sub:
        by.setdefault((r["backbone"], r["dataset"], r["H"]), {})[r["method"]] = r
    keys = sorted(by)
    emit(f"ob{surf}NumConfigs", len(keys), "{:d}")
    for m, mk in MK.items():
        if m not in by[keys[0]]:
            continue
        f = lambda k: st.mean(by[key][m][k] for key in keys)
        for stat, col in [("Marg", "marginal"), ("Worst", "worst_cell"),
                          ("Pfive", "cell_p05"), ("Width", "width"), ("Wink", "winkler")]:
            emit(f"ob{surf}{mk}{stat}", f(col))
        emit(f"ob{surf}{mk}Within", f("frac_within_5pt"), "{:.3f}")
        emit(f"ob{surf}{mk}WinsG",
             f"{sum(by[k][m]['worst_cell'] > by[k]['Global']['worst_cell'] for k in keys)}/{len(keys)}")
    for b in ["MSCP-online", "PID"]:
        emit(f"ob{surf}PropBeats{MK[b]}",
             f"{sum(by[k]['Proposed']['worst_cell'] > by[k][b]['worst_cell'] for k in keys)}/{len(keys)}")
        emit(f"ob{surf}PropGapOver{MK[b]}",
             st.mean(by[k]["Proposed"]["worst_cell"] - by[k][b]["worst_cell"] for k in keys),
             "{:+.4f}")
    best_wink = min(MK, key=lambda m: st.mean(by[k][m]["winkler"] for k in keys)
                    if m in by[keys[0]] else 9e9)
    emit(f"ob{surf}BestWinklerMethod", {"MSCP-online": "per-horizon online conformal",
                                        "PID": "conformal PID",
                                        "Proposed": "the proposed layer",
                                        "ACI": "ACI", "Global": "global split CP",
                                        "Cond": "static conditional"}[best_wink])

# ------------------------------------------------------- 32-config ablations
ab = J("ablations32.json")["rows"]
cfgs = sorted({(r["backbone"], r["dataset"], r["H"]) for r in ab})
emit("ablNumConfigs", len(cfgs), "{:d}")


def am(abl, setting, method, col="worst_cell"):
    v = [r[col] for r in ab if r["ablation"] == abl and r["setting"] == setting
         and r["method"] == method]
    return st.mean(v)


def acount(abl, s1, s2, method):
    a = {(r["backbone"], r["dataset"], r["H"]): r["worst_cell"] for r in ab
         if r["ablation"] == abl and r["setting"] == s1 and r["method"] == method}
    b = {(r["backbone"], r["dataset"], r["H"]): r["worst_cell"] for r in ab
         if r["ablation"] == abl and r["setting"] == s2 and r["method"] == method}
    return f"{sum(a[k] > b[k] for k in a)}/{len(a)}"


for g in [0.0, 0.005, 0.02, 0.05, 0.1]:
    emit(f"ablGamma{WORD[g]}Worst", am("gamma", g, "Proposed"))
    emit(f"ablGamma{WORD[g]}Width", am("gamma", g, "Proposed", "width"))
    emit(f"ablGamma{WORD[g]}ACI", am("gamma", g, "ACI"))
emit("ablGammaBigBeatsDefault", acount("gamma", 0.1, 0.02, "Proposed"))
for s in ["mad", "std"]:
    for m, mk in [("Global", "Global"), ("Cond", "Cond"), ("Proposed", "Prop")]:
        emit(f"ablScale{WORD[s]}{mk}", am("scale", s, m))
emit("ablScaleMADbeatsSDGlobal", acount("scale", "mad", "std", "Global"))
emit("ablScaleMADbeatsSDProp", acount("scale", "mad", "std", "Proposed"))
for k in [1, 3, 6, 10]:
    emit(f"ablK{WORD[k]}Cond", am("K", k, "Cond"))
    emit(f"ablK{WORD[k]}Prop", am("K", k, "Proposed"))
    emit(f"ablK{WORD[k]}PropWithin", am("K", k, "Proposed", "frac_within_5pt"), "{:.3f}")
emit("ablKSixBeatsKOne", acount("K", 6, 1, "Proposed"))
emit("ablKCondEffect", am("K", 6, "Cond") - am("K", 1, "Cond"), "{:+.4f}")
emit("ablKPropEffect", am("K", 6, "Proposed") - am("K", 1, "Proposed"), "{:+.4f}")
emit("ablKInteraction",
     (am("K", 6, "Proposed") - am("K", 1, "Proposed"))
     - (am("K", 6, "Cond") - am("K", 1, "Cond")), "{:+.4f}")

# ------------------------------------------------------- decision, tuned margin
dm = J("decision_margin.json")["rows"]
RULE = {"FlagAll": "FlagAll", "FlagNone": "FlagNone", "Point": "Point",
        "Point+margin": "Margin", "Interval:Global": "IntGlobal",
        "Interval:Proposed": "IntProp"}
ratios = sorted({r["ratio"] for r in dm})
emit("dmNumConfigs", len({(r["backbone"], r["H"]) for r in dm}), "{:d}")
for ratio in ratios:
    for rule, rk in RULE.items():
        v = [r["norm_cost"] for r in dm if r["rule"] == rule and r["ratio"] == ratio]
        if v:
            emit(f"dm{rk}{WORD[ratio]}", st.mean(v))
    best = min(RULE, key=lambda rr: st.mean(
        [r["norm_cost"] for r in dm if r["rule"] == rr and r["ratio"] == ratio] or [9e9]))
    emit(f"dmBest{WORD[ratio]}", {"Point": "the bare point rule",
                                  "Point+margin": "the tuned-margin point rule",
                                  "Interval:Global": "global-conformal gating",
                                  "Interval:Proposed": "proposed-layer gating",
                                  "FlagAll": "flagging everything",
                                  "FlagNone": "flagging nothing"}[best])
# how often the conformal rule actually beats the tuned margin, per configuration
wins = 0; tot = 0
for ratio in ratios:
    for cfg in {(r["backbone"], r["H"]) for r in dm}:
        g = lambda rr: next(r["norm_cost"] for r in dm if r["rule"] == rr
                            and r["ratio"] == ratio and (r["backbone"], r["H"]) == cfg)
        tot += 1
        wins += g("Interval:Proposed") < g("Point+margin")
emit("dmPropBeatsMargin", f"{wins}/{tot}")
emit("dmMarginMean", st.mean(r["margin_mean"] for r in dm if r["rule"] == "Point+margin"))

with open(OUT, "w") as f:
    f.write("% generated by scripts/make_numbers_v3.py -- do not edit\n")
    f.write("\n".join(lines) + "\n")
print(f"wrote {len(lines)} macros to {OUT}")
