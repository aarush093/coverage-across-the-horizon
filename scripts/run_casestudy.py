"""S5 energy case study: does better conditional coverage buy a better decision?

SURFACE. The LTSF Electricity benchmark, 50 client meters screened by the fixed
rule in coverage_horizon/data/electricity.py, sequential 70/10/20 split. This
is the fallback surface named in Idea Lock section 12, risk R3, promoted to
primary by decision D006. BDG2 remains the stated extension.

WHY A SECOND SURFACE AT ALL. ETT gives a 6 x 7 = 42-cell grid. Electricity
gives 6 x 50 = 300 cells over meters whose mean loads span roughly fifty-fold,
and it splits so that the calibration block and the test block sit in different
seasons. A calibration layer that only works on a narrow, same-season grid is
not the layer this project claims to have built.

WHAT IS MEASURED. Three things, in order:
  1. the same coverage metrics as the main study, so the two surfaces are
     directly comparable;
  2. two extra grid statistics -- the 5th-percentile cell and the fraction of
     cells within 5 points of target -- because a raw minimum over 300 cells
     and a raw minimum over 42 cells are not comparable quantities, and
     comparing them anyway would be the easiest mistake to make here;
  3. the decision evaluation (calibration/decision.py), which is wedge
     component W4.

The extra grid statistics are computed HERE from the cell grid that
calibration/metrics.py already returns, rather than by editing metrics.py. That
file produced the committed ETT numbers; changing it would silently move them.

REPRODUCIBILITY. Deterministic, CPU only, seed fixed in config. Writes
results/casestudy.json. Nothing in this script tunes anything toward a desired
answer: the cost ratio is swept rather than chosen, the peak threshold comes
from calibration data only, and a negative result is reported as it lands.

Run:  python scripts/run_casestudy.py
      python scripts/run_casestudy.py --horizons 96 --backbones dlinear
"""
import argparse
import gc
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from coverage_horizon import run_backbone                                # noqa: E402
from coverage_horizon.calibration import (calibrate, metrics, joint_layers,  # noqa: E402
                                          peak_threshold, decision_eval,
                                          DEFAULT_RATIOS)
from coverage_horizon.config import (ALPHA, K_BUCKETS, GAMMA, HORIZONS,   # noqa: E402
                                     ECL_STRIDE, SEED)
from coverage_horizon.data import load_electricity                        # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
DECISION_METHODS = ("Global", "Proposed")   # rules the planner could actually deploy


def grid_stats(cell, alpha=ALPHA):
    """Distributional summary of the per-cell coverage grid.

    A minimum is a single order statistic; over 300 cells it is far more
    exposed to sampling noise than over 42. These summarise the whole grid so
    that surfaces of different width can be compared honestly.
    """
    cell = np.asarray(cell)
    tgt = 1.0 - alpha
    return dict(
        n_cells=int(cell.size),
        cell_min=float(cell.min()),
        cell_p05=float(np.percentile(cell, 5)),
        cell_median=float(np.median(cell)),
        frac_within_5pt=float(np.mean(np.abs(cell - tgt) <= 0.05)),
        frac_below_80=float(np.mean(cell < 0.80)),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--backbones", nargs="+", default=["dlinear", "nlinear"])
    ap.add_argument("--horizons", nargs="+", type=int, default=HORIZONS)
    ap.add_argument("--chunk", type=int, default=1200,
                    help="normal-equation chunk; lower it if memory is tight")
    ap.add_argument("--out", default="casestudy.json")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    t_all = time.time()

    print("loading Electricity ...", flush=True)
    arr, tr, ca, te, meta = load_electricity()
    print(f"  {arr.shape[0]} rows x {arr.shape[1]} meters "
          f"(kept {meta['n_kept']} of {meta['n_meters_clean']} clean, "
          f"{meta['n_meters_total']} total)", flush=True)

    res = {"config": dict(seed=SEED, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                          stride=ECL_STRIDE, ratios=list(DEFAULT_RATIOS),
                          backbones=args.backbones, horizons=args.horizons),
           "data": {k: v for k, v in meta.items() if k != "kept"},
           "kept_meters": meta["kept"],
           "point": [], "cal": [], "joint": [], "decision": [], "curves": {}}

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    for kind in args.backbones:
        for H in args.horizons:
            t0 = time.time()
            r = run_backbone("electricity", H, kind=kind, loaded=(arr, tr, ca, te),
                             stride=ECL_STRIDE, chunk=args.chunk, keep_paths=True)
            tag = f"{kind}/H={H}"
            print(f"[{tag}] fit {time.time()-t0:.0f}s  mse={r['mse']:.4f}  "
                  f"n_cal={r['n_cal']} n_test={r['n_test']}", flush=True)
            res["point"].append({k: r[k] for k in
                                 ("kind", "H", "mse", "mae", "n_train",
                                  "n_cal", "n_test", "stride", "fit_s")})

            halves, edges, _ = calibrate(r["Rca"], r["Rts"],
                                         alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA)

            for m, h in halves.items():
                mt = metrics(r["Rts"], h, K=K_BUCKETS, alpha=ALPHA)
                cell = mt.pop("cell")
                res["curves"].setdefault(m, {})[f"{kind}_{H}"] = {
                    "cov_by_h": mt.pop("cov_by_h"), "width_by_h": mt.pop("width_by_h")}
                row = dict(backbone=kind, H=H, method=m, **mt, **grid_stats(cell))
                res["cal"].append(row)
                print(f"    {m:9s} worst={row['worst_cell']:.3f} "
                      f"p05={row['cell_p05']:.3f} within5={row['frac_within_5pt']:.2f} "
                      f"marg={row['marginal']:.3f} width={row['width']:.3f}", flush=True)

            res["joint"].append(dict(backbone=kind, H=H,
                                     **joint_layers(r["Rca"], r["Rts"], alpha=ALPHA)))

            pred = r["Yts"] - r["Rts"]
            tau = peak_threshold(r["Yca"])
            dec = decision_eval(r["Yts"], pred,
                                {m: halves[m] for m in DECISION_METHODS}, tau)
            res["decision"].append(dict(backbone=kind, H=H, **dec))
            mid = str(float(DEFAULT_RATIOS[len(DEFAULT_RATIOS) // 2]))
            print(f"    decision @ratio {mid}: " + "  ".join(
                f"{k}={v['norm_cost']:.3f}" for k, v in dec["by_ratio"][mid].items()
                if k != "FlagNone"), flush=True)

            del r, halves, pred
            gc.collect()
            flush()

    print(f"\ndone in {time.time()-t_all:.0f}s -> {path}")


if __name__ == "__main__":
    main()
