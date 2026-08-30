"""Horizon-bucket ablation, scored on a FIXED reference grid.

WHY THIS SCRIPT EXISTS -- TWO REASONS.

1. K = 1 IS A MISSING ARM OF THE FACTORIAL, NOT A NEW METHOD.
   `buckets(H, 1)` returns a single horizon bucket covering 1..H, so the
   horizon term collapses and the cell index degenerates to the channel index.
   That makes "Cond" at K=1 exactly channel-only STATIC conditioning (already
   in the factorial as CondC), and -- the point here -- "Proposed" at K=1
   exactly channel-only conditioning WITH online adaptation. That arm is
   missing from the seven-method factorial in `run_experiments.py`: the
   factorial crosses conditioning with adaptation, but only ever at the full
   horizon-bucket x channel grid. Sweeping K therefore isolates what the
   HORIZON axis contributes once adaptation is already present.

   Committing it as a K value rather than as an eighth method is deliberate:
   no existing method changes, no committed number moves, and the arm comes
   out of the same `calibrate` call that produces every other method.

2. THE PRIOR K ABLATION WAS SCORED ON A MOVING GRID.
   `run_experiments.py` scores each K with `metrics(Rts, half, K, edges)` --
   that is, on ITS OWN K-bucket grid. Worst-cell coverage is a minimum over
   cells, and a coarser grid has fewer and larger cells, so its minimum is
   higher almost by construction. Comparing K=1 against K=10 that way compares
   two different estimators, not two different methods, and the confound runs
   in the direction that flatters small K.

   Everything here is therefore scored TWICE:

       worst_own = metrics(Rts, half, K,     edges)["worst_cell"]
       worst_ref = metrics(Rts, half, K_REF)["worst_cell"]      K_REF = 6

   Only `worst_ref` is comparable across K -- one fixed 6-bucket x channel
   grid for every K, so the grid is held constant and only the calibration
   layer varies. `worst_own` is recorded alongside it precisely so the size of
   the confound can be shown rather than asserted.

Nothing under `coverage_horizon/` is modified by this script, and it writes
only `results/<--out>`. The committed `results.json` and `casestudy.json` are
read by nobody here and cannot move.

Run:  python scripts/run_horizon_ablation.py --out horizon_ablation.json
      python scripts/run_horizon_ablation.py --surface electricity --K 1 6 --out ha_ecl.json
"""
import argparse
import gc
import json
import os
import sys
import time

import numpy as np

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, ".."))

from coverage_horizon import run_backbone                                  # noqa: E402
from coverage_horizon.calibration import calibrate, metrics                # noqa: E402
from coverage_horizon.config import (SEED, ALPHA, K_BUCKETS, GAMMA,        # noqa: E402
                                     DATASETS, HORIZONS, ECL_STRIDE)
from coverage_horizon.data import load_electricity                         # noqa: E402

# D009's grid statistics, imported rather than re-implemented so the repo keeps
# one definition of cell_p05 / frac_within_5pt / frac_below_80.
sys.path.insert(0, _HERE)
from run_casestudy import grid_stats                                       # noqa: E402

OUT = os.path.join(_HERE, "..", "results")

K_REF = K_BUCKETS                 # the fixed scoring grid: 6 log-spaced buckets
ARMS = ("Cond", "Proposed")       # same conditioning, adaptation off / on
EXTRA = ("Global", "MSCP", "CondC", "ACI")   # scored once, at K == K_REF


def score(Rts, half, K, edges):
    """Score one half-width tensor on its own K-grid and on the fixed K_REF grid.

    `metrics` ignores `edges` (it re-derives the buckets from K); it is passed
    positionally only to match the call used in run_experiments.py.
    """
    own = metrics(Rts, half, K, edges)
    worst_own = float(own["worst_cell"])
    ref = own if K == K_REF else metrics(Rts, half, K_REF)
    cell = ref["cell"]
    row = dict(
        worst_own=round(worst_own, 6),
        worst_ref=round(float(ref["worst_cell"]), 6),
        marginal=round(float(ref["marginal"]), 6),
        width=round(float(ref["width"]), 6),
        winkler=round(float(ref["winkler"]), 6),
        cell_err=round(float(ref["mean_abs_cell_err"]), 6),
    )
    for k, v in grid_stats(cell, alpha=ALPHA).items():
        row[k] = round(v, 6) if isinstance(v, float) else v
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", choices=["ett", "electricity", "both"], default="ett")
    ap.add_argument("--K", nargs="+", type=int, default=[1, 2, 4, 6, 8, 10])
    ap.add_argument("--backbones", nargs="+", default=["dlinear", "nlinear"])
    ap.add_argument("--horizons", nargs="+", type=int, default=list(HORIZONS))
    ap.add_argument("--chunk", type=int, default=1200,
                    help="normal-equation chunk; lower it if memory is tight")
    ap.add_argument("--out", default="horizon_ablation.json")
    args = ap.parse_args()

    np.random.seed(SEED)
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    t_all = time.time()

    surfaces = ["ett", "electricity"] if args.surface == "both" else [args.surface]
    Ks = sorted(set(args.K))
    res = {"config": dict(seed=SEED, alpha=ALPHA, gamma=GAMMA, K_list=Ks,
                          K_ref=K_REF, backbones=list(args.backbones),
                          horizons=list(args.horizons), surfaces=surfaces,
                          chunk=args.chunk, arms=list(ARMS), extra=list(EXTRA)),
           "rows": []}

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    ecl = None
    if "electricity" in surfaces:
        print("loading Electricity ...", flush=True)
        arr, tr, ca, te, meta = load_electricity()
        ecl = (arr, tr, ca, te)
        res["ecl_data"] = {k: v for k, v in meta.items() if k != "kept"}
        print("  %d rows x %d meters" % (arr.shape[0], arr.shape[1]), flush=True)

    jobs = []
    for surface in surfaces:
        dss = DATASETS if surface == "ett" else ["electricity"]
        for kind in args.backbones:
            for ds in dss:
                for H in args.horizons:
                    jobs.append((surface, kind, ds, H))

    for i, (surface, kind, ds, H) in enumerate(jobs, 1):
        t0 = time.time()
        if surface == "ett":
            r = run_backbone(ds, H, kind=kind, point_eval=False)
        else:
            r = run_backbone("electricity", H, kind=kind, loaded=ecl,
                             stride=ECL_STRIDE, chunk=args.chunk, point_eval=False)
        Rts = r["Rts"]
        fit_s = time.time() - t0

        base = dict(surface=surface, backbone=kind, dataset=ds, H=H,
                    n_cal=r["n_cal"], n_test=r["n_test"], C=int(Rts.shape[2]))
        got = {}
        for K in Ks:
            half, edges, _ = calibrate(r["Rca"], Rts, alpha=ALPHA, K=K, gamma=GAMMA)
            todo = list(ARMS) + (list(EXTRA) if K == K_REF else [])
            for m in todo:
                row = dict(base, method=m, K=K)
                row.update(score(Rts, half[m], K, edges))
                res["rows"].append(row)
                if m in ARMS:
                    got[(m, K)] = row["worst_ref"]
            del half
            gc.collect()

        msg = "  ".join("K=%d:%.4f" % (K, got[("Proposed", K)]) for K in Ks)
        print("[%d/%d] %-8s %-12s H=%-4d n_test=%-4d fit=%.0fs  "
              "Proposed worst_ref  %s  [%.0fs]"
              % (i, len(jobs), kind, ds, H, r["n_test"], fit_s, msg,
                 time.time() - t_all), flush=True)

        del r, Rts
        gc.collect()
        flush()

    flush()

    # --- summary: the only cross-K comparable quantity is worst_ref ---
    print("\nmean worst_ref by K over %d configs (fixed K_REF=%d grid):"
          % (len(jobs), K_REF), flush=True)
    print("  %4s  %14s  %20s  %18s"
          % ("K", "Cond (static)", "Proposed (adaptive)", "Proposed own-grid"))
    for K in Ks:
        vals = []
        for m in ARMS:
            v = [x["worst_ref"] for x in res["rows"]
                 if x["method"] == m and x["K"] == K]
            vals.append(float(np.mean(v)))
        vo = [x["worst_own"] for x in res["rows"]
              if x["method"] == "Proposed" and x["K"] == K]
        print("  %4d  %14.4f  %20.4f  %18.4f"
              % (K, vals[0], vals[1], float(np.mean(vo))), flush=True)

    print("\ndone in %.0fs -> %s" % (time.time() - t_all, path))


if __name__ == "__main__":
    main()
