"""Metrics over the horizon-bucket x channel grid.

Worst-cell coverage is mandatory alongside every mean: averages hide exactly
the failures this project is about. The Winkler (interval) score is reported
because coverage alone can always be bought by widening without limit.
"""
import numpy as np

from ..config import ALPHA, K_BUCKETS
from .conditional import buckets


def winkler(R, half, alpha=ALPHA):
    """Winkler / interval score. Width, plus a miss penalty of 2/alpha times
    the shortfall. Lower is better. Proper scoring rule for intervals."""
    w = 2.0 * half
    miss = np.abs(R) - half
    pen = np.where(miss > 0, (2.0 / alpha) * miss, 0.0)
    return float(np.mean(w + pen))


def metrics(Rts, half, K=K_BUCKETS, edges=None, alpha=ALPHA):
    n, H, C = Rts.shape
    cov = (np.abs(Rts) <= half)
    bid, _ = buckets(H, K)
    cell = np.zeros((len(np.unique(bid)), C))
    for k in np.unique(bid):
        for c in range(C):
            cell[k, c] = cov[:, bid == k, c].mean()
    tgt = 1 - alpha
    return dict(
        marginal=float(cov.mean()),
        worst_cell=float(cell.min()),
        mean_abs_cell_err=float(np.mean(np.abs(cell - tgt))),
        joint=float(np.mean(cov.all(axis=(1, 2)))),
        width=float(np.mean(2 * half)),
        winkler=winkler(Rts, half, alpha),
        cov_by_h=cov.mean(axis=(0, 2)).tolist(),
        width_by_h=(2 * half).mean(axis=(0, 2)).tolist(),
        cell=cell.tolist(),
    )
