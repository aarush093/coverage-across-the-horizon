"""Are our symmetric intervals paying a bias penalty? (RV16 / Q15)

THE ATTACK THIS ANSWERS. BC-ACI (arXiv:2604.13253, Apr 2026) argues that a frozen
forecaster develops persistent bias after a distribution shift, and that intervals
centred on the point forecast must then widen symmetrically to cover an offset they
could instead correct -- a width overhead the authors put at roughly 2|b|.

That premise applies to this project exactly: the backbone is frozen, nothing is
retrained, and the S5 split deliberately puts calibration and test in different
seasons. Our intervals are symmetric about the point forecast. So the question is not
rhetorical, and it is not answerable by intuition.

WHAT IS MEASURED. Two things, in order.

1. How big is the bias? Per grid cell (horizon bucket x channel), the mean residual
   on the calibration block and on the test block, reported relative to the interval
   half-width so the numbers are comparable across surfaces. Also the correlation
   between the two, because a bias only costs width if it PERSISTS -- if the
   calibration-block bias does not predict the test-block bias, no online estimator
   could have exploited it either, and BC-ACI's mechanism has nothing to grip.

2. What would correcting it buy? A leakage-free re-centring. The per-cell mean is
   estimated on the CALIBRATION block only, subtracted from both blocks, and the
   whole existing calibration layer is re-run on the re-centred residuals. Passing
   (R - b) through `calibrate` is exactly an interval centred at (prediction + b),
   because the layer scores |R| and the metric checks |R| <= half. No method is
   modified and `conditional.py` is not touched.

HOW TO READ THE RESULT. If the corrected variant is not meaningfully narrower at
equal coverage, the symmetric choice is vindicated and RV16 costs one sentence. If
it is, that is either a limitation to state or an extension to run -- and BC-ACI is
then the right citation for it, since its correction acts on the score while our
conditioning acts on the quantile, and nothing prevents doing both.

This script writes results/bias_check.json and modifies nothing.

Run:  python scripts/check_bias.py
      python scripts/check_bias.py --surface electricity
"""
import argparse
import gc
import json
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from coverage_horizon import run_backbone
from coverage_horizon.calibration import calibrate, metrics
from coverage_horizon.calibration.conditional import buckets
from coverage_horizon.config import (ALPHA, DATASETS, HORIZONS, K_BUCKETS,
                                     GAMMA, SEED, ECL_STRIDE)
from coverage_horizon.data import load_electricity

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
METHODS = ("Global", "Proposed")


def cell_means(R, bid):
    """Per-(bucket, channel) mean residual, broadcast back to (H, C)."""
    H, C = R.shape[1], R.shape[2]
    ks = np.unique(bid)
    b = np.zeros((len(ks), C))
    for k in ks:
        b[k] = R[:, bid == k, :].mean(axis=(0, 1))
    return b[bid]


def one_config(Rca, Rts, tag):
    bid, _ = buckets(Rca.shape[1], K_BUCKETS)
    b_ca = cell_means(Rca, bid)
    b_ts = cell_means(Rts, bid)

    half_ref, _, _ = calibrate(Rca, Rts, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA)
    scale = float(np.mean(half_ref["Proposed"]))

    row = dict(**tag,
               bias_cal_mean_abs=float(np.abs(b_ca).mean()),
               bias_test_mean_abs=float(np.abs(b_ts).mean()),
               bias_cal_max_abs=float(np.abs(b_ca).max()),
               bias_test_max_abs=float(np.abs(b_ts).max()),
               half_width_mean=scale,
               implied_overhead_frac=float(2 * np.abs(b_ts).mean() / (2 * scale)),
               bias_persistence_r=float(np.corrcoef(b_ca.ravel(), b_ts.ravel())[0, 1]),
               sign_agreement=float(np.mean(np.sign(b_ca) == np.sign(b_ts))))

    half_bc, _, _ = calibrate(Rca - b_ca, Rts - b_ca,
                              alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA)
    for m in METHODS:
        a = metrics(Rts, half_ref[m], K_BUCKETS, alpha=ALPHA)
        c = metrics(Rts - b_ca, half_bc[m], K_BUCKETS, alpha=ALPHA)
        for d in (a, c):
            d.pop("cell", None); d.pop("cov_by_h", None); d.pop("width_by_h", None)
        row[m] = dict(
            plain_worst=a["worst_cell"], bc_worst=c["worst_cell"],
            plain_marginal=a["marginal"], bc_marginal=c["marginal"],
            plain_width=a["width"], bc_width=c["width"],
            plain_winkler=a["winkler"], bc_winkler=c["winkler"],
            width_change_pct=100.0 * (c["width"] / a["width"] - 1.0))
    del half_ref, half_bc
    gc.collect()
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--surface", choices=["ett", "electricity", "both"], default="both")
    ap.add_argument("--backbones", nargs="+", default=["dlinear", "nlinear"])
    ap.add_argument("--horizons", nargs="+", type=int, default=HORIZONS)
    ap.add_argument("--chunk", type=int, default=1200)
    ap.add_argument("--out", default="bias_check.json")
    args = ap.parse_args()

    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    res = {"config": dict(seed=SEED, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                          note="b estimated on the calibration block only"),
           "rows": []}

    def flush():
        with open(path, "w") as f:
            json.dump(res, f, indent=1)

    if args.surface in ("ett", "both"):
        for kind in args.backbones:
            for ds in DATASETS:
                for H in args.horizons:
                    r = run_backbone(ds, H, kind=kind, point_eval=False)
                    res["rows"].append(one_config(
                        r["Rca"], r["Rts"],
                        dict(surface="ETT", backbone=NICE[kind], dataset=ds, H=H)))
                    print("ETT %-8s %s H=%-4d |b|_test=%.4f" % (
                        NICE[kind], ds, H, res["rows"][-1]["bias_test_mean_abs"]), flush=True)
                    del r
                    gc.collect()
                    flush()

    if args.surface in ("electricity", "both"):
        arr, tr, ca, te, _ = load_electricity()
        for kind in args.backbones:
            for H in args.horizons:
                r = run_backbone("electricity", H, kind=kind, loaded=(arr, tr, ca, te),
                                 stride=ECL_STRIDE, chunk=args.chunk, point_eval=False)
                res["rows"].append(one_config(
                    r["Rca"], r["Rts"],
                    dict(surface="Electricity", backbone=NICE[kind],
                         dataset="Electricity", H=H)))
                print("ECL %-8s H=%-4d |b|_test=%.4f" % (
                    NICE[kind], H, res["rows"][-1]["bias_test_mean_abs"]), flush=True)
                del r
                gc.collect()
                flush()

    import statistics as st
    for surf in sorted({x["surface"] for x in res["rows"]}):
        rows = [x for x in res["rows"] if x["surface"] == surf]
        print("")
        print("%s  (mean over %d configs)" % (surf, len(rows)))
        print("  mean |bias| on test, as a fraction of interval width : %.4f"
              % st.mean(x["implied_overhead_frac"] for x in rows))
        print("  does calibration bias predict test bias?  r = %+.3f   sign agreement %.3f"
              % (st.mean(x["bias_persistence_r"] for x in rows),
                 st.mean(x["sign_agreement"] for x in rows)))
        for m in METHODS:
            print("  %-9s width %.4f -> %.4f (%+.2f%%)   worst %.4f -> %.4f" % (
                m,
                st.mean(x[m]["plain_width"] for x in rows),
                st.mean(x[m]["bc_width"] for x in rows),
                st.mean(x[m]["width_change_pct"] for x in rows),
                st.mean(x[m]["plain_worst"] for x in rows),
                st.mean(x[m]["bc_worst"] for x in rows)))
    print("")
    print("-> " + path)


if __name__ == "__main__":
    main()
