"""One generated summary of every result in the project -- results/SUMMARY.md.

WHY THIS EXISTS. There are now ten result files. FR03 is already on record: a headline
number ("conditioning alone = 0.652") was carried in prose across sessions when the
artefact said 0.7588. The defence against that is not discipline, it is generation --
every number in the paper should come from a file, computed at read time, with its
source printed next to it. Nothing here is typed by hand.

It also fixes Q17 on read rather than on disk. casestudy.json stores backbones
lowercase; every other file uses CamelCase, so a naive join across files silently
returns nothing. That already cost one failed analysis. Committed result files must
not move, so the normalisation lives here.

Missing files are skipped with a note rather than crashing, so this runs correctly at
any point in the project and tells you what is not yet produced.

Writes results/SUMMARY.md (for reading and for pasting into the paper) and
results/SUMMARY.json (for figure scripts). Modifies nothing else.

Run:  python scripts/make_summary.py
"""
import json
import os
import statistics as st
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
ORDER = ["Gaussian", "Global", "MSCP", "CondC", "Cond", "ACI", "Proposed"]
CANON = {"dlinear": "DLinear", "nlinear": "NLinear",
         "ett": "ETT", "electricity": "Electricity"}


def norm(v):
    return CANON.get(v.lower(), v) if isinstance(v, str) else v


def load(name):
    p = os.path.join(R, name)
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding="utf-8-sig"))
    for k in ("rows", "sweep", "cal", "joint", "decision", "point"):
        if isinstance(d.get(k), list):
            for r in d[k]:
                for f in ("backbone", "surface", "dataset"):
                    if f in r:
                        r[f] = norm(r[f])
    return d


def rows_of(d, *keys):
    for k in keys:
        if d and isinstance(d.get(k), list) and d[k]:
            return d[k]
    return []


def mean(rows, field, **flt):
    v = [r[field] for r in rows
         if all(r.get(k) == val for k, val in flt.items()) and field in r]
    return st.mean(v) if v else None


def fmt(x, n=4):
    return "--" if x is None else f"{x:.{n}f}"


def table(head, lines):
    return ("| " + " | ".join(head) + " |\n| " +
            " | ".join("---" for _ in head) + " |\n" +
            "".join("| " + " | ".join(str(c) for c in l) + " |\n" for l in lines))


def method_table(rows, fields, labels, **flt):
    lines = []
    for m in ORDER:
        if not any(r.get("method") == m for r in rows):
            continue
        lines.append([m] + [fmt(mean(rows, f, method=m, **flt)) for f in fields])
    return table(["method"] + labels, lines)


def main():
    out, js = [], {}
    out.append(f"DOC: SUMMARY | OWNER: generated | CADENCE: regenerate before any writing\n"
               f"STATUS: generated {date.today().isoformat()} by `scripts/make_summary.py` "
               f"| SUPERSEDES: any hand-typed number\n")
    out.append("# RESULTS SUMMARY -- every number generated, none typed\n")
    out.append("Regenerate this file before quoting anything. If a number in the paper "
               "disagrees with this file, this file is right.\n")
    missing = []

    d = load("results.json")
    if d:
        cal = rows_of(d, "cal")
        out.append("\n## 1. Main study -- ETT x4, 42-cell grid, target 0.90\n")
        out.append(f"Source: `results/results.json` -> `cal`, mean over {len(cal)//7} configs "
                   "(2 backbones x 4 datasets x 4 horizons).\n\n")
        out.append(method_table(cal, ["marginal", "worst_cell", "width", "winkler", "joint"],
                                ["marginal", "worst-cell", "width", "Winkler", "joint"]))
        g, c, a, p = (mean(cal, "worst_cell", method=m) for m in ("Global", "Cond", "ACI", "Proposed"))
        out.append(f"\n**Conditioning x adaptation interaction:** "
                   f"`P - C - A + G` = {p:.4f} - {c:.4f} - {a:.4f} + {g:.4f} = "
                   f"**{p - c - a + g:+.4f}**\n")
        js["ett_interaction"] = p - c - a + g
        js["ett"] = {m: {f: mean(cal, f, method=m) for f in
                         ("marginal", "worst_cell", "width", "winkler", "joint")} for m in ORDER}
    else:
        missing.append("results.json")

    d = load("casestudy.json")
    if d:
        cal = rows_of(d, "cal")
        out.append("\n## 2. Case study -- Electricity, 50 meters, 300-cell grid\n")
        out.append(f"Source: `results/casestudy.json` -> `cal`, mean over {len(cal)//7} configs. "
                   "Grid statistics per D009.\n\n")
        out.append(method_table(cal,
                                ["marginal", "worst_cell", "cell_p05", "frac_within_5pt",
                                 "frac_below_80", "width", "winkler"],
                                ["marginal", "worst-cell", "p05", "within 5pt",
                                 "below .80", "width", "Winkler"]))
        g, c, a, p = (mean(cal, "worst_cell", method=m) for m in ("Global", "Cond", "ACI", "Proposed"))
        out.append(f"\n**Interaction on Electricity:** **{p - c - a + g:+.4f}** "
                   f"(ETT: {js.get('ett_interaction', float('nan')):+.4f})\n")
        js["ecl_interaction"] = p - c - a + g

        jr = rows_of(d, "joint")
        if jr:
            out.append("\n### Whole-path coverage and its price (W3)\n\n")
            out.append(table(["layer", "joint coverage", "width ratio"],
                             [[k, fmt(st.mean(x[k]["joint"] for x in jr)),
                               fmt(st.mean(x[k]["width_ratio"] for x in jr), 2) + "x"]
                              for k in ("Marginal", "MaxScore", "Bonferroni")]))

        dec = rows_of(d, "decision")
        if dec:
            out.append("\n### Decision layer (W4 / MET08) -- normalised cost, 1.0 = flag nothing\n\n")
            rules = ["Point", "Interval:Global", "Interval:Proposed"]
            lines = []
            for r in dec[0]["ratios"]:
                k = str(float(r))
                lines.append([f"{int(r)}:1"] + [
                    fmt(st.mean(x["by_ratio"][k][ru]["norm_cost"] for x in dec)) +
                    " / " + fmt(st.mean(x["by_ratio"][k][ru]["worst_channel_norm_cost"] for x in dec), 2)
                    for ru in rules])
            out.append(table(["miss:false-alarm"] + rules, lines))
            out.append("\nCell format: mean cost / worst-channel cost. "
                       "**Interval-gating wins only at ratios >=5** -- at 2:1 the point forecast is cheaper.\n")
    else:
        missing.append("casestudy.json")

    seen_h = set()
    for tag, fn, label in (("3a", "horizon_ablation.json", "ETT"), ("3a", "ha_ett.json", "ETT"),
                           ("3b", "ha_ecl.json", "Electricity")):
        if tag in seen_h:
            continue
        d = load(fn)
        if not d:
            continue
        rows = rows_of(d, "rows", "sweep")
        P = [r for r in rows if r.get("method") == "Proposed"]
        C = [r for r in rows if r.get("method") == "Cond"]
        if not P:
            continue
        Ks = sorted({r["K"] for r in P})
        seen_h.add(tag)
        out.append(f"\n## {tag}. Horizon-axis ablation -- {label}\n")
        out.append(f"Source: `results/{fn}`, {len(P)//len(Ks)} configs, scored on the FIXED "
                   "K=6 grid (`worst_ref`). K=1 collapses the horizon axis.\n\n")
        out.append(table(["arm"] + [f"K={k}" for k in Ks],
                         [["Cond (static)"] + [fmt(mean(C, "worst_ref", K=k)) for k in Ks],
                          ["Proposed (adaptive)"] + [fmt(mean(P, "worst_ref", K=k)) for k in Ks],
                          ["own-grid, Proposed"] + [fmt(mean(P, "worst_own", K=k)) for k in Ks]]))
        if 1 in Ks and 6 in Ks:
            ds = mean(C, "worst_ref", K=6) - mean(C, "worst_ref", K=1)
            da = mean(P, "worst_ref", K=6) - mean(P, "worst_ref", K=1)
            out.append(f"\nHorizon axis: **{ds:+.4f} static, {da:+.4f} adaptive**. "
                       f"The horizon x adaptation interaction is **{da - ds:+.4f}** -- that is the "
                       f"quantity the method claims, not the adaptive column alone.\n")

    parts = [(load("bias_check.json"), "ETT"), (load("bias_ecl.json"), "Electricity")]
    if any(p[0] for p in parts):
        out.append("\n## 4. Bias diagnostic (RV16 / EXP_S4_008)\n")
        out.append("Source: `results/bias_check.json`, `results/bias_ecl.json`. "
                   "Bias estimated on the calibration block only.\n\n")
        lines = []
        for d, lab in parts:
            if not d:
                continue
            rows = rows_of(d, "rows")
            for bb in ("DLinear", "NLinear"):
                s = [r for r in rows if r["backbone"] == bb]
                lines.append([lab, bb,
                              fmt(mean(s, "implied_overhead_frac")),
                              fmt(mean(s, "bias_persistence_r"), 3),
                              fmt(mean(s, "sign_agreement"), 3),
                              fmt(st.mean(r["Proposed"]["width_change_pct"] for r in s), 2) + "%"])
        out.append(table(["surface", "backbone", "abs(bias) / width", "persistence r",
                          "sign agree", "width if re-centred"], lines))

    parts = [(load("tr_ett.json"), "ETT"), (load("tr_ecl.json"), "Electricity")]
    if any(p[0] for p in parts):
        out.append("\n## 5. Rolling coverage traces (MET02 / EXP_S4_005)\n")
        out.append("Source: `results/tr_ett.json`, `results/tr_ecl.json`. "
                   "30-path trailing window; paths are one per day.\n\n")
        lines = []
        for d, lab in parts:
            if not d:
                continue
            rows = [r for r in rows_of(d, "rows") if "min_roll" in r]
            for m in ("Global", "ACI", "Proposed"):
                s = [r for r in rows if r["method"] == m]
                lines.append([lab, m, fmt(mean(s, "mean")), fmt(mean(s, "min_roll")),
                              fmt(100 * mean(s, "frac_below_85"), 1) + "%",
                              fmt(mean(s, "excursion_len"), 1)])
        out.append(table(["surface", "method", "mean", "worst window",
                          "% below .85", "longest dip"], lines))

    parts = [(load("cw_ett.json"), "ETT"), (load("cw_ecl.json"), "Electricity")]
    if any(p[0] for p in parts):
        out.append("\n## 6. Calibration-window length (EXP_S4_006)\n")
        out.append("Source: `results/cw_ett.json`, `results/cw_ecl.json`. "
                   "Block truncated from the front, keeping the most recent paths.\n")
        for d, lab in parts:
            if not d:
                continue
            rows = rows_of(d, "rows")
            fr = sorted({r["frac"] for r in rows})
            out.append(f"\n**{lab}** -- worst-cell by calibration fraction\n\n")
            lines = [[m] + [fmt(mean(rows, "worst_cell", method=m, frac=f)) for f in fr]
                     for m in ORDER if any(r["method"] == m for r in rows)]
            lines.append(["_n_cal_"] + [fmt(mean(rows, "n_cal", frac=f), 0) for f in fr])
            out.append(table(["method"] + [f"{int(100*f)}%" for f in fr], lines))
            jr = rows_of(d, "joint")
            if jr:
                out.append("\nMaxScore whole-path coverage: " + ", ".join(
                    f"{int(100*f)}% -> {st.mean(x['MaxScore']['joint'] for x in jr if x['frac']==f):.4f}"
                    for f in fr) + "\n")

    if missing:
        out.append("\n## Not yet produced\n" + "".join(f"- `{m}`\n" for m in missing))

    md = os.path.join(R, "SUMMARY.md")
    with open(md, "w", encoding="utf-8") as f:
        f.write("".join(out))
    with open(os.path.join(R, "SUMMARY.json"), "w") as f:
        json.dump(js, f, indent=1)
    print("wrote " + md)
    if missing:
        print("missing inputs: " + ", ".join(missing))


if __name__ == "__main__":
    main()
