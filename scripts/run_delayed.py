"""Delay-aware re-run of the two adaptive arms (EXP_S6_001 / RV20 / FR07).

WHY THIS EXISTS. In `calibration/conditional.py` the ACI and Proposed loops
update every cell with path t's outcomes at ALL horizon steps before path t+1
is issued. With a one-day stride and H=720 that uses outcomes realised up to
H - stride = 696 steps after the next forecast origin. The perturbation test in
the paper (second half of test block -> first-half intervals bit-identical)
cannot detect this, because the leaked information lies inside the first half.

WHAT THIS DOES. Re-runs ACI and Proposed with feedback delayed until it is
realised, via `coverage_horizon.calibration.calibrate_delayed`. Path t (forecast
origin at t*stride) contributes its cell-(k,c)
outcome to the tracker only when the cell's LAST horizon step has been
observed, i.e. when (t' - t) * stride >= edge_hi[k] for the path t' about to
be issued. Everything else (pool, quantile, gamma, clamps, one update per path
per cell) is identical to the committed implementation, so the only variable
is the delay. The unconditional ACI arm is delayed by the full horizon H.

OUTPUT. results/delayed_ett.json (ETT, 32 configs) and, with --ecl, results/
delayed_ecl.json (Electricity, 8 configs). Prints a comparison table with the
committed (delay-free) numbers recomputed on the same residual tensors.

Run AFTER committing (D013). Deterministic; CPU only.
"""
import argparse
import gc
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from coverage_horizon import run_backbone, calibrate, metrics
from coverage_horizon.calibration import calibrate_delayed
from coverage_horizon.config import (SEED, DATASETS, HORIZONS, K_BUCKETS, ALPHA,
                                     GAMMA, STRIDE)

np.random.seed(SEED)
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}


def run_surface(cells, out_path, loader):
    rows = []
    if os.path.exists(out_path):                     # resume: cells already written are kept
        rows = json.load(open(out_path)).get("rows", [])
    done = {(r["backbone"], r["dataset"], r["H"]) for r in rows}
    t0 = time.time()
    for (kind, ds, H) in cells:
        if (NICE.get(kind, kind), ds, H) in done:
            print(f"  {kind:8s} {ds:7s} H={H:4d}  (resumed from file)", flush=True)
            continue
        r = loader(kind, ds, H)
        Rca, Rts, st = r["Rca"], r["Rts"], r["stride"]
        half0, edges, _ = calibrate(Rca, Rts, K=K_BUCKETS)
        delayed, _, lag, lag_full = calibrate_delayed(Rca, Rts, st, K=K_BUCKETS)
        allh = {**{m: half0[m] for m in ["Gaussian", "Global", "MSCP", "CondC", "Cond",
                                          "ACI", "Proposed"]},
                "ACI-delayed": delayed["ACI"], "Proposed-delayed": delayed["Proposed"]}
        for m, h in allh.items():
            mm = metrics(Rts, h, K_BUCKETS, edges)
            cell = np.array(mm["cell"]).ravel()             # D014 grid statistics
            rows.append(dict(backbone=NICE.get(kind, kind), dataset=ds, H=H, method=m,
                             stride=st, lag_paths_last_bucket=int(lag[max(lag)]),
                             lag_paths_full=int(lag_full),
                             marginal=round(mm["marginal"], 4),
                             worst_cell=round(mm["worst_cell"], 4),
                             cell_p05=round(float(np.quantile(cell, 0.05)), 4),
                             frac_within_5pt=round(float(np.mean(np.abs(cell - (1 - ALPHA)) <= 0.05)), 4),
                             frac_below_80=round(float(np.mean(cell < 0.80)), 4),
                             n_cells=int(cell.size),
                             cell_err=round(mm["mean_abs_cell_err"], 4),
                             width=round(mm["width"], 4),
                             winkler=round(mm["winkler"], 4)))
        del Rca, Rts, half0, delayed; gc.collect()
        print(f"  {kind:8s} {ds:7s} H={H:4d}  done  ({time.time()-t0:5.0f}s)", flush=True)
        with open(out_path, "w") as f:
            json.dump({"config": dict(seed=SEED, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                                      note="feedback delayed until realised; one update "
                                           "per path per cell, same pool/quantile/clamps"),
                       "rows": rows}, f, indent=1)
    return rows


def summarise(rows, label):
    ms = ["Global", "Cond", "ACI", "ACI-delayed", "Proposed", "Proposed-delayed"]
    by = {}
    for r in rows:
        by.setdefault((r["backbone"], r["dataset"], r["H"]), {})[r["method"]] = r
    keys = sorted(by)
    print(f"\n== {label}: mean over {len(keys)} configs ==")
    ms = ["Gaussian", "Global", "MSCP", "CondC", "Cond", "ACI", "ACI-delayed",
          "Proposed", "Proposed-delayed"]
    print(f"{'method':18s} {'marginal':>9s} {'worst':>8s} {'p05':>8s} {'within5':>8s} {'below80':>8s} {'width':>8s} {'winkler':>8s}")
    for m in ms:
        f = lambda k: np.mean([by[key][m][k] for key in keys])
        print(f"{m:18s} {f('marginal'):9.4f} {f('worst_cell'):8.4f} {f('cell_p05'):8.4f} "
              f"{f('frac_within_5pt'):8.4f} {f('frac_below_80'):8.4f} {f('width'):8.4f} {f('winkler'):8.4f}")
    def wins(a, b):
        return sum(by[k][a]["worst_cell"] > by[k][b]["worst_cell"] for k in keys)
    print("sign counts on worst-cell:")
    for a, b in [("Proposed-delayed", "Global"), ("Proposed-delayed", "Cond"),
                 ("Proposed-delayed", "ACI-delayed"), ("Proposed", "Proposed-delayed"),
                 ("ACI-delayed", "Global"), ("Proposed-delayed", "ACI")]:
        print(f"  {a} > {b}: {wins(a, b)}/{len(keys)}")
    G = np.mean([by[k]["Global"]["worst_cell"] for k in keys])
    Cc = np.mean([by[k]["Cond"]["worst_cell"] for k in keys])
    A = np.mean([by[k]["ACI-delayed"]["worst_cell"] for k in keys])
    P = np.mean([by[k]["Proposed-delayed"]["worst_cell"] for k in keys])
    print(f"delayed 2x2 interaction P-C-A+G = {P:.4f}-{Cc:.4f}-{A:.4f}+{G:.4f} = {P-Cc-A+G:+.4f}")
    for H in sorted(set(k[2] for k in keys)):
        sub = [k for k in keys if k[2] == H]
        print(f"  H={H:4d}: Proposed {np.mean([by[k]['Proposed']['worst_cell'] for k in sub]):.4f}"
              f"  Proposed-delayed {np.mean([by[k]['Proposed-delayed']['worst_cell'] for k in sub]):.4f}"
              f"  Global {np.mean([by[k]['Global']['worst_cell'] for k in sub]):.4f}"
              f"  (lag {by[sub[0]]['Proposed-delayed']['lag_paths_last_bucket']} paths for last bucket)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ecl", action="store_true", help="also run the Electricity surface")
    ap.add_argument("--skip-ett", action="store_true", help="skip ETT (already done)")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)

    if not args.skip_ett:
        cells = [(k, d, H) for k in ["dlinear", "nlinear"] for d in DATASETS for H in HORIZONS]
        rows = run_surface(cells, os.path.join(OUT, "delayed_ett.json"),
                           lambda k, d, H: run_backbone(d, H, kind=k, point_eval=False))
        summarise(rows, "ETT")

    if args.ecl:
        from coverage_horizon.data.electricity import load_electricity
        from coverage_horizon.config import ECL_STRIDE
        arr, tr, ca, te, meta = load_electricity()
        loaded = (arr, tr, ca, te)
        cells = [(k, "ECL", H) for k in ["dlinear", "nlinear"] for H in HORIZONS]
        rows = run_surface(cells, os.path.join(OUT, "delayed_ecl.json"),
                           lambda k, d, H: run_backbone("electricity", H, kind=k,
                                                        stride=ECL_STRIDE, point_eval=False,
                                                        loaded=loaded, chunk=1000))
        summarise(rows, "Electricity")


if __name__ == "__main__":
    main()
