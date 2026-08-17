"""Run the full experiment grid and write results/results.json.

Two frozen backbones x four datasets x four horizons x seven calibration
methods, plus joint-coverage layers and five ablations. Deterministic
(seed 2026), CPU only, ~3-4 minutes.

Writes results/results.json incrementally after every (backbone, dataset,
horizon) cell, and frees each residual tensor as soon as it is consumed, so
the run completes within a small memory budget and partial progress survives
an interruption.
"""
import gc
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from coverage_horizon import run_backbone, calibrate, joint_layers, metrics
from coverage_horizon.config import SEED, DATASETS, HORIZONS, K_BUCKETS

np.random.seed(SEED)
METHODS = ["Gaussian", "Global", "MSCP", "CondC", "Cond", "ACI", "Proposed"]
BACKBONES = ["dlinear", "nlinear"]
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
OUT = os.path.join(os.path.dirname(__file__), "..", "results")
REF = ("dlinear", "ETTh1", 720)          # cell used for curves and ablations


def main():
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "results.json")
    res = {"point": [], "cal": [], "joint": [], "curves": {},
           "kabl": [], "gabl": [], "scale_abl": [], "stride_abl": []}
    t0 = time.time()

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    for kind in BACKBONES:
        for ds in DATASETS:
            for H in HORIZONS:
                r = run_backbone(ds, H, kind=kind)
                Rca, Rts = r["Rca"], r["Rts"]
                res["point"].append(dict(backbone=NICE[kind], dataset=ds, H=H,
                                         mse=round(r["mse"], 4), mae=round(r["mae"], 4),
                                         n_train=r["n_train"], stride=r["stride"],
                                         n_cal=r["n_cal"], n_test=r["n_test"]))
                half, edges, _ = calibrate(Rca, Rts, K=K_BUCKETS)
                for m in METHODS:
                    mm = metrics(Rts, half[m], K_BUCKETS, edges)
                    res["cal"].append(dict(backbone=NICE[kind], dataset=ds, H=H, method=m,
                                           marginal=round(mm["marginal"], 4),
                                           worst_cell=round(mm["worst_cell"], 4),
                                           cell_err=round(mm["mean_abs_cell_err"], 4),
                                           joint=round(mm["joint"], 4),
                                           width=round(mm["width"], 4),
                                           winkler=round(mm["winkler"], 4)))
                    if (kind, ds, H) == REF:
                        res["curves"][m] = dict(cov=mm["cov_by_h"],
                                                width=mm["width_by_h"], cell=mm["cell"])
                for k, v in joint_layers(Rca, Rts).items():
                    res["joint"].append(dict(backbone=NICE[kind], dataset=ds, H=H, method=k,
                                             joint=round(v["joint"], 4),
                                             marginal=round(v["marginal"], 4),
                                             width_ratio=round(v["width_ratio"], 3)))

                if (kind, ds, H) == REF:
                    for K in [4, 6, 8, 10]:
                        hh, ee, _ = calibrate(Rca, Rts, K=K)
                        mm = metrics(Rts, hh["Proposed"], K, ee)
                        res["kabl"].append(dict(K=K, worst=round(mm["worst_cell"], 4),
                                                cell_err=round(mm["mean_abs_cell_err"], 4),
                                                width=round(mm["width"], 4)))
                    for gm in [0.0, 0.005, 0.02, 0.05, 0.1]:
                        hh, ee, _ = calibrate(Rca, Rts, K=K_BUCKETS, gamma=gm)
                        mm = metrics(Rts, hh["Proposed"], K_BUCKETS, ee)
                        res["gabl"].append(dict(gamma=gm, worst=round(mm["worst_cell"], 4),
                                                marginal=round(mm["marginal"], 4),
                                                width=round(mm["width"], 4)))
                    for how in ["mad", "std"]:
                        hh, ee, _ = calibrate(Rca, Rts, scale_how=how)
                        for m in ["Global", "MSCP", "Proposed"]:
                            mm = metrics(Rts, hh[m], K_BUCKETS, ee)
                            res["scale_abl"].append(dict(scale=how.upper(), method=m,
                                                         worst=round(mm["worst_cell"], 4),
                                                         marginal=round(mm["marginal"], 4),
                                                         width=round(mm["width"], 4),
                                                         winkler=round(mm["winkler"], 4)))
                print(f"{NICE[kind]:8s} {ds} H={H:<4d} mse={r['mse']:.4f}  [{time.time()-t0:.0f}s]",
                      flush=True)
                del r, Rca, Rts, half
                gc.collect()
                flush()

    # stride ablation (open question Q08)
    for st in [24, 48, 96]:
        r = run_backbone("ETTh1", 96, kind="dlinear", stride=st, point_eval=False)
        half, edges, _ = calibrate(r["Rca"], r["Rts"], K=K_BUCKETS)
        label = {24: "1 day (default)", 48: "2 days", 96: "non-overlapping"}[st]
        row = dict(stride=st, label=label, n_cal=r["n_cal"])
        for m in ["Global", "MSCP", "Proposed"]:
            row[m] = round(metrics(r["Rts"], half[m], K_BUCKETS, edges)["worst_cell"], 4)
        res["stride_abl"].append(row)
        del r, half
        gc.collect()
        flush()
        print(f"stride {st}: n_cal={row['n_cal']}  [{time.time()-t0:.0f}s]", flush=True)

    flush()
    print("TOTAL", round(time.time() - t0, 1), "s ->", path)


if __name__ == "__main__":
    main()
