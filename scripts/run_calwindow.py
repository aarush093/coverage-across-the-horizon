"""Calibration-window-length ablation -- EXP_S4_006, and the test that settles Q11.

WHAT THE LOCK ASKS FOR. Idea Lock section 10 lists "calibration window length" among
the required ablations. It was written and lost with the container (FR01); this is the
last outstanding piece of that loss.

WHY IT MATTERS BEYOND box-ticking. Everything the calibration layer does is estimated
from one finite block. A conditional method spends that block across a grid -- 42 cells
on ETT, 300 on Electricity -- so it is the method most exposed to the block being
small. If Proposed only beats the baselines when calibration data is abundant, that is
a deployment limitation and it belongs in the paper. If it degrades gracefully, that is
a claim worth making.

THE DESIGN. The calibration block is truncated from the FRONT, keeping the most recent
paths, because that is what a rolling deployment does -- you keep the freshest window,
not a random sample. Fractions default to 25 / 50 / 75 / 100 percent. Everything is
scored on the fixed K_REF=6 grid so the numbers are comparable across fractions
(the lesson of FR04: never let the scoring grid move with the thing being ablated).

WHAT IT ALSO SETTLES -- Q11. Whole-path coverage under the MaxScore layer decays from
0.944 at H=96 to 0.842-0.895 at H=720 on Electricity, while still costing about ten
times the width. Two explanations were on the table: a real limit on post-hoc
whole-path control at long horizon, or a finite-sample artefact, since n_cal falls
from 106 at H=96 to 80 at H=720 as the longer window eats the block.

Those are separable here, and cheaply. Truncating H=96's calibration block to roughly
H=720's size reproduces the sample size WITHOUT changing the horizon. If joint coverage
at H=96 then falls to the H=720 level, the decay is finite-sample and W3's claim should
be stated in terms of calibration size. If it holds near 0.94, the decay is a genuine
horizon limit and that is the stronger, more interesting result. joint_layers is
therefore computed at every fraction, not just the full block.

Deterministic, CPU only, writes results/calwindow.json, modifies nothing.

Run:  python scripts/run_calwindow.py
      python scripts/run_calwindow.py --surface electricity --fracs 0.25 0.5 0.75 1.0
"""
import argparse
import gc
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from coverage_horizon import run_backbone
from coverage_horizon.calibration import calibrate_with_feedback, metrics, joint_layers
from coverage_horizon.config import (ALPHA, DATASETS, HORIZONS, K_BUCKETS,
                                     GAMMA, SEED, ECL_STRIDE)
from coverage_horizon.data import load_electricity

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
K_REF = K_BUCKETS
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
SCORED = ("Global", "MSCP", "CondC", "Cond", "ACI", "Proposed")


def grid_stats(cell, alpha=ALPHA):
    cell = np.asarray(cell)
    tgt = 1.0 - alpha
    return dict(cell_min=float(cell.min()),
                cell_p05=float(np.percentile(cell, 5)),
                frac_within_5pt=float(np.mean(np.abs(cell - tgt) <= 0.05)),
                frac_below_80=float(np.mean(cell < 0.80)))


def one_config(Rca, Rts, tag, fracs, res, stride, feedback):
    n_full = Rca.shape[0]
    for f in fracs:
        k = max(2, int(round(n_full * f)))
        Rc = Rca[-k:]
        half, _, _ = calibrate_with_feedback(Rc, Rts, stride, feedback=feedback,
                                             alpha=ALPHA, K=K_REF, gamma=GAMMA)
        jl = joint_layers(Rc, Rts, alpha=ALPHA)
        for m in SCORED:
            mt = metrics(Rts, half[m], K_REF, alpha=ALPHA)
            cell = mt.pop("cell")
            mt.pop("cov_by_h", None)
            mt.pop("width_by_h", None)
            res["rows"].append(dict(**tag, frac=f, n_cal=int(k), n_cal_full=int(n_full),
                                    method=m, feedback=feedback, **mt,
                                    **grid_stats(cell)))
        res["joint"].append(dict(**tag, frac=f, n_cal=int(k),
                                 **{key: dict(joint=jl[key]["joint"],
                                              width_ratio=jl[key]["width_ratio"])
                                    for key in jl}))
        del half
        gc.collect()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", choices=["ett", "electricity", "both"], default="both")
    ap.add_argument("--fracs", nargs="+", type=float, default=[0.25, 0.5, 0.75, 1.0])
    ap.add_argument("--backbones", nargs="+", default=["dlinear", "nlinear"])
    ap.add_argument("--horizons", nargs="+", type=int, default=HORIZONS)
    ap.add_argument("--chunk", type=int, default=1200)
    ap.add_argument("--feedback", choices=["realised", "instant"], default="realised",
                    help="realised = protocol of record (D015); instant = oracle bound")
    ap.add_argument("--out", default=None,
                    help="default: calwindow.json for realised, calwindow_instant.json otherwise")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    out_name = args.out or ("calwindow.json" if args.feedback == "realised"
                            else "calwindow_instant.json")
    path = os.path.join(OUT, out_name)
    res = {"config": dict(seed=SEED, alpha=ALPHA, K_ref=K_REF, gamma=GAMMA,
                          fracs=args.fracs, feedback=args.feedback,
                          truncation="most recent paths kept"),
           "rows": [], "joint": []}

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    if args.surface in ("ett", "both"):
        for kind in args.backbones:
            for ds in DATASETS:
                for H in args.horizons:
                    r = run_backbone(ds, H, kind=kind, point_eval=False)
                    one_config(r["Rca"], r["Rts"],
                               dict(surface="ETT", backbone=NICE[kind], dataset=ds, H=H),
                               args.fracs, res, r["stride"], args.feedback)
                    print("ETT %-8s %s H=%-4d n_cal_full=%d" % (NICE[kind], ds, H, r["n_cal"]), flush=True)
                    del r
                    gc.collect()
                    flush()

    if args.surface in ("electricity", "both"):
        arr, tr, ca, te, _ = load_electricity()
        for kind in args.backbones:
            for H in args.horizons:
                r = run_backbone("electricity", H, kind=kind, loaded=(arr, tr, ca, te),
                                 stride=ECL_STRIDE, chunk=args.chunk, point_eval=False)
                one_config(r["Rca"], r["Rts"],
                           dict(surface="Electricity", backbone=NICE[kind],
                                dataset="Electricity", H=H), args.fracs, res,
                           r["stride"], args.feedback)
                print("ECL %-8s H=%-4d n_cal_full=%d" % (NICE[kind], H, r["n_cal"]), flush=True)
                del r
                gc.collect()
                flush()

    import statistics as st
    for surf in sorted({x["surface"] for x in res["rows"]}):
        rows = [x for x in res["rows"] if x["surface"] == surf]
        print("")
        print("%s: mean worst-cell on the fixed K=%d grid" % (surf, K_REF))
        print("  " + "method".ljust(10) + "".join(("%d%%" % int(100 * f)).rjust(10) for f in args.fracs))
        for m in SCORED:
            line = "  " + m.ljust(10)
            for f in args.fracs:
                v = [x["worst_cell"] for x in rows if x["method"] == m and x["frac"] == f]
                line += "%10.4f" % st.mean(v)
            print(line)
        j = [x for x in res["joint"] if x["surface"] == surf]
        print("  " + "MaxScore".ljust(10) + "".join(
            "%10.4f" % st.mean(x["MaxScore"]["joint"] for x in j if x["frac"] == f) for f in args.fracs))
        print("  " + "n_cal".ljust(10) + "".join(
            "%10.0f" % st.mean(x["n_cal"] for x in j if x["frac"] == f) for f in args.fracs))
    print("")
    print("-> " + path)


if __name__ == "__main__":
    main()
