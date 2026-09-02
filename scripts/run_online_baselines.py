"""EXP_S6_002 -- the two online baselines the comparison set named (Q24/RV25).

Scores MSCP-online (per-horizon ACI) and conformal PID against the four arms of
the 2x2, on the identical grid, from the identical residual tensors, under the
identical realised-feedback protocol (D015). The question is narrow and worth
asking plainly: per-horizon conditioning at FULL resolution plus online
adaptation is a strictly finer horizon axis than our K buckets -- does it reach
the horizon x channel layer's conditional coverage without the channel axis?

Writes results/online_baselines.json. Deterministic, CPU only.

Run:  python scripts/run_online_baselines.py            # ETT
      python scripts/run_online_baselines.py --ecl      # both surfaces
"""
import argparse
import gc
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from coverage_horizon import run_backbone, metrics                        # noqa: E402
from coverage_horizon.calibration import calibrate_with_feedback           # noqa: E402
from coverage_horizon.calibration.online_baselines import online_baselines  # noqa: E402
from coverage_horizon.config import (SEED, DATASETS, HORIZONS, K_BUCKETS,  # noqa: E402
                                     ALPHA, GAMMA)

OUT = os.path.join(os.path.dirname(__file__), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
SHOW = ["Global", "Cond", "ACI", "MSCP-online", "PID", "Proposed"]


def grid_stats(cell, alpha=ALPHA):
    c = np.asarray(cell).ravel()
    return dict(cell_p05=round(float(np.quantile(c, 0.05)), 4),
                frac_within_5pt=round(float(np.mean(np.abs(c - (1 - alpha)) <= 0.05)), 4),
                frac_below_80=round(float(np.mean(c < 0.80)), 4),
                n_cells=int(c.size))


def run(cells, loader, out_path, rows):
    t0 = time.time()
    done = {(r["backbone"], r["dataset"], r["H"]) for r in rows}
    for kind, ds, H in cells:
        if (NICE.get(kind, kind), ds, H) in done:
            continue
        r = loader(kind, ds, H)
        Rca, Rts, st = r["Rca"], r["Rts"], r["stride"]
        half, edges, _ = calibrate_with_feedback(Rca, Rts, st, feedback="realised",
                                                 alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA)
        half.update(online_baselines(Rca, Rts, st, alpha=ALPHA, gamma=GAMMA))
        for m, h in half.items():
            mt = metrics(Rts, h, K=K_BUCKETS, alpha=ALPHA, edges=edges)
            cell = mt.pop("cell"); mt.pop("cov_by_h", None); mt.pop("width_by_h", None)
            rows.append(dict(backbone=NICE.get(kind, kind), dataset=ds, H=H, method=m,
                             stride=st,
                             **{k: (round(v, 4) if isinstance(v, float) else v)
                                for k, v in mt.items()},
                             **grid_stats(cell)))
        del r, Rca, Rts, half; gc.collect()
        print(f"  {kind:8s} {ds:12s} H={H:4d}  done ({time.time()-t0:5.0f}s)", flush=True)
        with open(out_path, "w") as f:
            json.dump({"config": dict(seed=SEED, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                                      feedback="realised",
                                      note="MSCP-online = per-horizon ACI; PID = per-horizon "
                                           "P+I conformal control. AcMCP's multi-step "
                                           "autocorrelation correction is NOT reimplemented; "
                                           "these are a lower bound on that family."),
                       "rows": rows}, f, indent=1)
    return rows


def summarise(rows, surface_rows, label):
    import statistics as st
    by = {}
    for r in surface_rows:
        by.setdefault((r["backbone"], r["dataset"], r["H"]), {})[r["method"]] = r
    keys = sorted(by)
    if not keys:
        return
    print(f"\n== {label}: mean over {len(keys)} configs ==")
    print(f"{'method':14s} {'marginal':>9s} {'worst':>8s} {'p05':>8s} "
          f"{'within5':>8s} {'width':>8s} {'winkler':>8s} {'vs Global':>10s}")
    for m in SHOW:
        if m not in by[keys[0]]:
            continue
        f = lambda k: st.mean(by[key][m][k] for key in keys)
        w = sum(by[k][m]["worst_cell"] > by[k]["Global"]["worst_cell"] for k in keys)
        print(f"{m:14s} {f('marginal'):9.4f} {f('worst_cell'):8.4f} {f('cell_p05'):8.4f} "
              f"{f('frac_within_5pt'):8.4f} {f('width'):8.4f} {f('winkler'):8.4f} "
              f"{w:6d}/{len(keys)}")
    for b in ["MSCP-online", "PID"]:
        wins = sum(by[k]["Proposed"]["worst_cell"] > by[k][b]["worst_cell"] for k in keys)
        d = st.mean(by[k]["Proposed"]["worst_cell"] - by[k][b]["worst_cell"] for k in keys)
        print(f"  Proposed > {b:12s}: {wins}/{len(keys)}   mean gap {d:+.4f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ecl", action="store_true")
    ap.add_argument("--out", default="online_baselines.json")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    rows = json.load(open(path))["rows"] if os.path.exists(path) else []

    cells = [(k, d, H) for k in ["dlinear", "nlinear"] for d in DATASETS for H in HORIZONS]
    run(cells, lambda k, d, H: run_backbone(d, H, kind=k, point_eval=False), path, rows)
    summarise(rows, [r for r in rows if r["dataset"] != "electricity"], "ETT")

    if args.ecl:
        from coverage_horizon.data import load_electricity
        from coverage_horizon.config import ECL_STRIDE
        arr, tr, ca, te, meta = load_electricity()
        cells = [(k, "electricity", H) for k in ["dlinear", "nlinear"] for H in HORIZONS]
        run(cells, lambda k, d, H: run_backbone("electricity", H, kind=k,
                                                stride=ECL_STRIDE, point_eval=False,
                                                loaded=(arr, tr, ca, te), chunk=1000),
            path, rows)
        summarise(rows, [r for r in rows if r["dataset"] == "electricity"], "Electricity")


if __name__ == "__main__":
    main()
