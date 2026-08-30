"""Rolling coverage traces through the test block -- MET02, and the S4 exit criterion.

WHAT THE LOCK ASKS FOR. Idea Lock section 8, stage S4: "rolling coverage traces
through nonstationary segments ... adaptation shown to matter (or not) under shift."
Metric MET02 has read "NOT YET PRODUCED" since the code for it was lost with the
container (FR01). This closes it.

WHY A TRACE AND NOT A NUMBER. Every result so far is a summary over the whole test
block: worst-cell, marginal, width. A summary cannot distinguish a method that holds
target coverage steadily from one that over-covers for months and then collapses,
because the two can average to the same number. Adaptation is a claim about
*recovery* -- that after coverage drops the method climbs back -- and recovery is
invisible to any block-level statistic. It only shows up in time.

THE SURFACE THAT MAKES THIS A REAL TEST. On Electricity the calibration block sits in
late winter and spring and the test block runs from roughly late May through the end
of the year (decision D006). Test paths are strided one per day, so the trace walks
summer into winter -- a genuine seasonal transition rather than a synthetic shift.

WHAT IS COMPARED. Three methods, chosen to isolate one factor:
  Global    static, unconditional -- cannot react to anything
  ACI       unconditional, adaptive -- reacts, but with one global knob
  Proposed  conditional AND adaptive
If adaptation matters, Global drifts away from target and stays away while the two
adaptive methods return. If it does not, all three move together and the S4 criterion
is answered in the negative, which is equally reportable.

WHAT IS REPORTED per method, per config:
  cov_by_path     coverage of each test path, in time order (the raw trace)
  roll_*          the trace smoothed over a window of paths (default 30 = ~1 month)
  min_roll        the worst window -- the failure a block average hides
  frac_below_85   how much of the test period sits under 0.85
  excursion_len   longest run of consecutive windows below 0.85, in paths
  recovery_paths  paths from the worst window back above 0.88, or null if it never
                  recovers. This is the number that decides whether adaptation works:
                  a static method has no mechanism to produce a finite value here.

Deterministic, CPU only, writes results/traces.json, modifies nothing.

Run:  python scripts/run_traces.py
      python scripts/run_traces.py --surface ett --window 20
"""
import argparse
import gc
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from coverage_horizon import run_backbone                                  # noqa: E402
from coverage_horizon.calibration import calibrate                         # noqa: E402
from coverage_horizon.config import (ALPHA, DATASETS, HORIZONS, K_BUCKETS,  # noqa: E402
                                     GAMMA, SEED, ECL_STRIDE)
from coverage_horizon.data import load_electricity                         # noqa: E402

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
TRACED = ("Global", "ACI", "Proposed")
RECOVER_TO = 0.88            # "recovered" threshold, a shade under the 0.90 target
FLOOR = 0.85                 # "in trouble" threshold


def roll(v, w):
    """Trailing rolling mean, full windows only."""
    if len(v) < w:
        return np.array([])
    c = np.cumsum(np.insert(v, 0, 0.0))
    return (c[w:] - c[:-w]) / w


def trace_stats(cov_by_path, w):
    r = roll(cov_by_path, w)
    out = dict(n_paths=int(len(cov_by_path)), window=int(w),
               mean=float(cov_by_path.mean()))
    if len(r) == 0:
        return dict(out, note="test block shorter than the window")
    lo = int(np.argmin(r))
    below = r < FLOOR
    # longest consecutive run below the floor
    best = cur = 0
    for b in below:
        cur = cur + 1 if b else 0
        best = max(best, cur)
    # paths from the worst window back above RECOVER_TO
    after = np.where(r[lo:] >= RECOVER_TO)[0]
    out.update(min_roll=float(r.min()), min_at_path=lo + w,
               max_roll=float(r.max()),
               frac_below_85=float(below.mean()),
               excursion_len=int(best),
               recovery_paths=(int(after[0]) if len(after) else None),
               roll=[round(float(x), 4) for x in r])
    return out


def one_config(Rca, Rts, tag, w):
    half, _, _ = calibrate(Rca, Rts, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA)
    rows = []
    for m in TRACED:
        cov = (np.abs(Rts) <= half[m]).mean(axis=(1, 2))     # coverage per test path
        rows.append(dict(**tag, method=m, **trace_stats(cov, w),
                         cov_by_path=[round(float(x), 4) for x in cov]))
    del half
    gc.collect()
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", choices=["ett", "electricity", "both"], default="both")
    ap.add_argument("--backbones", nargs="+", default=["dlinear", "nlinear"])
    ap.add_argument("--horizons", nargs="+", type=int, default=HORIZONS)
    ap.add_argument("--window", type=int, default=30,
                    help="rolling window in test paths; paths are one per day")
    ap.add_argument("--chunk", type=int, default=1200)
    ap.add_argument("--out", default="traces.json")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    res = {"config": dict(seed=SEED, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                          window=args.window, floor=FLOOR, recover_to=RECOVER_TO,
                          methods=list(TRACED)),
           "rows": []}

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    if args.surface in ("ett", "both"):
        for kind in args.backbones:
            for ds in DATASETS:
                for H in args.horizons:
                    r = run_backbone(ds, H, kind=kind, point_eval=False)
                    res["rows"] += one_config(r["Rca"], r["Rts"],
                                              dict(surface="ETT", backbone=NICE[kind],
                                                   dataset=ds, H=H), args.window)
                    print(f"ETT {NICE[kind]:8s} {ds} H={H:<4d} n_paths={r['n_test']}", flush=True)
                    del r
                    gc.collect()
                    flush()

    if args.surface in ("electricity", "both"):
        arr, tr, ca, te, _ = load_electricity()
        for kind in args.backbones:
            for H in args.horizons:
                r = run_backbone("electricity", H, kind=kind, loaded=(arr, tr, ca, te),
                                 stride=ECL_STRIDE, chunk=args.chunk, point_eval=False)
                res["rows"] += one_config(r["Rca"], r["Rts"],
                                          dict(surface="Electricity", backbone=NICE[kind],
                                               dataset="Electricity", H=H), args.window)
                print(f"ECL {NICE[kind]:8s} H={H:<4d} n_paths={r['n_test']}", flush=True)
                del r
                gc.collect()
                flush()

    import statistics as st
    for surf in sorted({x["surface"] for x in res["rows"]}):
        rows = [x for x in res["rows"] if x["surface"] == surf and "min_roll" in x]
        if not rows:
            continue
        print(f"\n{surf}  rolling window = {args.window} paths")
        print(f"  {'method':<10}{'mean':>8}{'worst window':>15}{'% below .85':>13}"
              f"{'longest dip':>13}{'recovered':>11}")
        for m in TRACED:
            v = [x for x in rows if x["method"] == m]
            rec = [x["recovery_paths"] for x in v if x["recovery_paths"] is not None]
            print(f"  {m:<10}{st.mean(x['mean'] for x in v):>8.4f}"
                  f"{st.mean(x['min_roll'] for x in v):>15.4f}"
                  f"{100*st.mean(x['frac_below_85'] for x in v):>12.1f}%"
                  f"{st.mean(x['excursion_len'] for x in v):>13.1f}"
                  f"{len(rec):>8}/{len(v)}")
    print(f"\n-> {path}")


if __name__ == "__main__":
    main()
