"""EXP_S6_003 -- the gamma, scale and K ablations on all 32 configurations.

WHY THIS EXISTS. Draft v1 reported each of these from a single configuration
(DLinear / ETTh1 / H=720) without saying so, which is why its ablation numbers
did not line up with Table 1 and why "gamma = 0 gives 0.652" appeared to
contradict "static conditional = 0.7588". They were different surfaces. The
main study runs in minutes, so there is no reason not to run the ablations
over the same 32 configurations the main table averages over, and report
means with sign counts like everything else.

All arms use realised feedback (D015) and a FIXED K = 6 scoring grid, so the
K sweep cannot be confounded by the grid-size artefact of Section 7 (FR04).

Writes results/ablations32.json. Deterministic, CPU only, ~10 min.
"""
import argparse
import gc
import json
import os
import statistics as st
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from coverage_horizon import run_backbone, metrics                      # noqa: E402
from coverage_horizon.calibration import calibrate_with_feedback         # noqa: E402
from coverage_horizon.calibration.conditional import buckets             # noqa: E402
from coverage_horizon.config import (SEED, DATASETS, HORIZONS, K_BUCKETS,  # noqa: E402
                                     ALPHA, GAMMA)

OUT = os.path.join(os.path.dirname(__file__), "..", "results")
NICE = {"dlinear": "DLinear", "nlinear": "NLinear"}
GAMMAS = [0.0, 0.005, 0.02, 0.05, 0.1]
SCALES = ["mad", "std"]
KS = [1, 3, 6, 10]
ARMS = ["Global", "Cond", "Proposed"]


def score(Rts, half, edges_ref):
    mt = metrics(Rts, half, K=K_BUCKETS, alpha=ALPHA, edges=edges_ref)
    cell = np.asarray(mt.pop("cell")).ravel()
    return dict(worst_cell=round(mt["worst_cell"], 4),
                marginal=round(mt["marginal"], 4),
                width=round(mt["width"], 4),
                winkler=round(mt["winkler"], 4),
                cell_p05=round(float(np.quantile(cell, 0.05)), 4),
                frac_within_5pt=round(float(np.mean(np.abs(cell - (1 - ALPHA)) <= 0.05)), 4))


def one_config(Rca, Rts, stride, tag, rows):
    _, edges_ref = buckets(Rts.shape[1], K_BUCKETS)   # fixed scoring grid for every arm

    for g in GAMMAS:
        half, _, _ = calibrate_with_feedback(Rca, Rts, stride, feedback="realised",
                                             alpha=ALPHA, K=K_BUCKETS, gamma=g)
        for m in ["ACI", "Proposed"]:
            rows.append(dict(**tag, ablation="gamma", setting=g, method=m,
                             **score(Rts, half[m], edges_ref)))
        # gamma = 0 is the static arm by construction; record it once as the check
        if g == 0.0:
            rows.append(dict(**tag, ablation="gamma", setting=g, method="Cond",
                             **score(Rts, half["Cond"], edges_ref)))

    for s in SCALES:
        half, _, _ = calibrate_with_feedback(Rca, Rts, stride, feedback="realised",
                                             alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                                             scale_how=s)
        for m in ARMS:
            rows.append(dict(**tag, ablation="scale", setting=s, method=m,
                             **score(Rts, half[m], edges_ref)))

    for k in KS:
        half, _, _ = calibrate_with_feedback(Rca, Rts, stride, feedback="realised",
                                             alpha=ALPHA, K=k, gamma=GAMMA)
        for m in ["Cond", "Proposed"]:
            rows.append(dict(**tag, ablation="K", setting=k, method=m,
                             **score(Rts, half[m], edges_ref)))


def report(rows):
    by = {}
    for r in rows:
        by.setdefault((r["ablation"], r["setting"], r["method"]), []).append(r)
    keys = {(r["backbone"], r["dataset"], r["H"]) for r in rows}
    print(f"\n== mean over {len(keys)} configurations, realised feedback, "
          f"fixed K={K_BUCKETS} scoring grid ==")
    for abl, settings in [("gamma", GAMMAS), ("scale", SCALES), ("K", KS)]:
        print(f"\n{abl}:")
        print(f"  {'setting':>8s} {'method':10s} {'worst':>8s} {'width':>8s} "
              f"{'winkler':>8s} {'within5':>8s}")
        for s in settings:
            for m in ARMS + ["ACI"]:
                v = by.get((abl, s, m))
                if not v:
                    continue
                print(f"  {str(s):>8s} {m:10s} {st.mean(x['worst_cell'] for x in v):8.4f} "
                      f"{st.mean(x['width'] for x in v):8.4f} "
                      f"{st.mean(x['winkler'] for x in v):8.4f} "
                      f"{st.mean(x['frac_within_5pt'] for x in v):8.4f}")
    # sign counts that decide whether a default is defensible
    def per_cfg(abl, s, m):
        return {(r["backbone"], r["dataset"], r["H"]): r["worst_cell"]
                for r in rows if r["ablation"] == abl and r["setting"] == s
                and r["method"] == m}
    a, b = per_cfg("gamma", GAMMA, "Proposed"), per_cfg("gamma", 0.1, "Proposed")
    print(f"\n  gamma=0.1 beats gamma={GAMMA} on worst-cell in "
          f"{sum(b[k] > a[k] for k in a)}/{len(a)} configurations")
    a, b = per_cfg("K", 6, "Proposed"), per_cfg("K", 1, "Proposed")
    print(f"  K=6 beats K=1 (adaptive, fixed grid) in {sum(a[k] > b[k] for k in a)}/{len(a)}")
    a, b = per_cfg("scale", "mad", "Proposed"), per_cfg("scale", "std", "Proposed")
    print(f"  MAD beats std (Proposed) in {sum(a[k] > b[k] for k in a)}/{len(a)}; "
          f"(Global) "
          f"{sum(per_cfg('scale','mad','Global')[k] > per_cfg('scale','std','Global')[k] for k in a)}/{len(a)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="ablations32.json")
    args = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, args.out)
    rows = json.load(open(path))["rows"] if os.path.exists(path) else []
    done = {(r["backbone"], r["dataset"], r["H"]) for r in rows}

    t0 = time.time()
    for kind in ["dlinear", "nlinear"]:
        for ds in DATASETS:
            for H in HORIZONS:
                tag = dict(backbone=NICE[kind], dataset=ds, H=H)
                if (tag["backbone"], ds, H) in done:
                    continue
                r = run_backbone(ds, H, kind=kind, point_eval=False)
                one_config(r["Rca"], r["Rts"], r["stride"], tag, rows)
                del r; gc.collect()
                print(f"  {kind:8s} {ds:7s} H={H:4d} done ({time.time()-t0:5.0f}s)",
                      flush=True)
                with open(path, "w") as f:
                    json.dump({"config": dict(seed=SEED, alpha=ALPHA, feedback="realised",
                                              scoring_grid=f"fixed K={K_BUCKETS}",
                                              gammas=GAMMAS, scales=SCALES, Ks=KS),
                               "rows": rows}, f, indent=1)
    report(rows)


if __name__ == "__main__":
    main()
