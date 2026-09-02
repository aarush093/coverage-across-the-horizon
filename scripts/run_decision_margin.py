"""EXP_S6_004 -- the decision baseline the equal-tuning rule requires (Q27/RV27).

THE OBJECTION THIS ANSWERS. Draft v1 showed interval gating beating a bare
point rule once misses cost about 5x a false alarm. A reviewer's immediate
reply is that the interval rule flags on `forecast + something`, so of course
it catches more peaks -- the comparison is a conformal margin against NO
margin, which is not a fair fight. The honest comparator is a point forecast
plus a CONSTANT margin, with that margin tuned on the calibration block at the
same cost ratio. If the conformal margin still wins, the value is in
conditional calibration. If a tuned constant margin matches it, the value was
in having any margin at all, and the decision claim has to be weakened.

The margin is chosen on calibration actuals and calibration forecasts only,
by direct search over a grid of quantiles of the calibration residual
distribution -- never on the test block, which would answer the question by
assuming it. It is tuned SEPARATELY AT EACH COST RATIO, because that is what
a planner with a known cost ratio would do, and it is the strongest form of
the objection.

Also reports FlagAll and FlagNone, which the case study computed and Draft v1
did not print: without them a reader cannot see that at 50:1 the trivial
"flag everything" rule is already cheap, which bounds how impressive any
method's number can be.

Writes results/decision_margin.json. Electricity only (the decision task lives
there), realised feedback, ~15 min.
"""
import gc
import json
import os
import statistics as st
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from coverage_horizon import run_backbone                               # noqa: E402
from coverage_horizon.calibration import calibrate_with_feedback         # noqa: E402
from coverage_horizon.calibration.decision import (peak_threshold,       # noqa: E402
                                                   DEFAULT_RATIOS, PEAK_Q)
from coverage_horizon.config import (SEED, HORIZONS, ALPHA, K_BUCKETS,   # noqa: E402
                                     GAMMA, ECL_STRIDE)

OUT = os.path.join(os.path.dirname(__file__), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
# Margin grid: quantiles of the calibration residual, per channel. 0.5 is the
# median residual, 0.999 is close to the largest -- wide enough to contain both
# "no margin" and "always flag" as limiting cases.
MARGIN_QS = [0.0, 0.5, 0.7, 0.8, 0.9, 0.95, 0.975, 0.99, 0.999]


def cost_of(peak, flag, ratio, n_peak):
    fn = np.count_nonzero(peak & ~flag)
    fp = np.count_nonzero(~peak & flag)
    return float((ratio * fn + fp) / (ratio * n_peak)) if n_peak else None


def tuned_margin(Yca, pred_ca, tau, ratio):
    """Per-channel constant margin minimising calibration-block cost at `ratio`."""
    peak_ca = Yca > tau[None, None, :]
    C = Yca.shape[2]
    margins = np.zeros(C)
    for c in range(C):
        res_c = np.abs(Yca[:, :, c] - pred_ca[:, :, c])
        pk = peak_ca[:, :, c]
        n_pk = int(np.count_nonzero(pk))
        if n_pk == 0:
            continue
        best, best_cost = 0.0, np.inf
        for q in MARGIN_QS:
            m = float(np.quantile(res_c, q)) if q > 0 else 0.0
            flag = (pred_ca[:, :, c] + m) > tau[c]
            cost = ratio * np.count_nonzero(pk & ~flag) + np.count_nonzero(~pk & flag)
            if cost < best_cost:
                best, best_cost = m, cost
        margins[c] = best
    return margins


def main():
    from coverage_horizon.data import load_electricity
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, "decision_margin.json")
    rows = json.load(open(path))["rows"] if os.path.exists(path) else []
    done = {(r["backbone"], r["H"]) for r in rows}
    arr, tr, ca, te, meta = load_electricity()

    for kind in ["dlinear", "nlinear"]:
        for H in HORIZONS:
            if (NICE[kind], H) in done:
                continue
            r = run_backbone("electricity", H, kind=kind, stride=ECL_STRIDE,
                             point_eval=False, loaded=(arr, tr, ca, te), chunk=1000,
                             keep_paths=True)
            half, _, _ = calibrate_with_feedback(r["Rca"], r["Rts"], r["stride"],
                                                 feedback="realised", alpha=ALPHA,
                                                 K=K_BUCKETS, gamma=GAMMA)
            tau = peak_threshold(r["Yca"])
            pred = r["Yts"] - r["Rts"]
            pred_ca = r["Yca"] - r["Rca"]
            peak = r["Yts"] > tau[None, None, :]
            n_peak = int(np.count_nonzero(peak))

            for ratio in DEFAULT_RATIOS:
                m = tuned_margin(r["Yca"], pred_ca, tau, ratio)
                rules = {
                    "FlagNone": np.zeros_like(peak),
                    "FlagAll": np.ones_like(peak),
                    "Point": pred > tau[None, None, :],
                    "Point+margin": (pred + m[None, None, :]) > tau[None, None, :],
                    "Interval:Global": (pred + half["Global"]) > tau[None, None, :],
                    "Interval:Proposed": (pred + half["Proposed"]) > tau[None, None, :],
                }
                for name, flag in rules.items():
                    rows.append(dict(backbone=NICE[kind], H=H, ratio=float(ratio),
                                     rule=name,
                                     norm_cost=cost_of(peak, flag, ratio, n_peak),
                                     flag_rate=float(np.count_nonzero(flag) / flag.size),
                                     margin_mean=float(m.mean()) if name == "Point+margin" else None))
            del r, half, pred, pred_ca, peak; gc.collect()
            print(f"  {kind:8s} H={H:4d} done", flush=True)
            with open(path, "w") as f:
                json.dump({"config": dict(seed=SEED, alpha=ALPHA, peak_q=PEAK_Q,
                                          feedback="realised", margin_qs=MARGIN_QS,
                                          note="margin tuned per channel on the calibration "
                                               "block at each ratio; no test data used"),
                           "rows": rows}, f, indent=1)

    print(f"\n== Electricity decision, mean over {len(rows)//(len(DEFAULT_RATIOS)*6)} configs ==")
    order = ["FlagAll", "Point", "Point+margin", "Interval:Global", "Interval:Proposed"]
    print(f"{'ratio':>7s} " + " ".join(f"{o:>18s}" for o in order))
    for ratio in DEFAULT_RATIOS:
        cells = []
        for o in order:
            v = [r["norm_cost"] for r in rows if r["rule"] == o and r["ratio"] == ratio]
            cells.append(f"{st.mean(v):18.4f}" if v else f"{'-':>18s}")
        print(f"{ratio:7.0f} " + " ".join(cells))


if __name__ == "__main__":
    main()
