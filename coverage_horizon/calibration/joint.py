"""Joint (whole-path) calibration.

max-score  - calibrate the per-path MAX normalised score (exact joint control)
Bonferroni - per-cell level alpha/(H*C), a union bound
Marginal   - the per-step baseline, for the width-price comparison
"""
import numpy as np

from ..config import ALPHA
from .conditional import cq


def joint_layers(Rca, Rts, alpha=ALPHA):
    """Whole-path (joint) coverage at target 1-alpha, and the width price.
    max-score: calibrate the per-path MAX normalised score (exact joint control).
    Bonferroni: per-cell level alpha/(H*C)."""
    n_cal, H, C = Rca.shape
    scale = np.maximum(np.median(np.abs(Rca), axis=(0, 1))[None, None, :], 1e-8)
    Sca, Sts = np.abs(Rca) / scale, np.abs(Rts) / scale
    res = {}
    qm = cq(Sca.max(axis=(1, 2)), alpha)
    res["MaxScore"] = np.full(Rts.shape, qm) * scale
    qb = cq(Sca.ravel(), alpha / (H * C))
    res["Bonferroni"] = np.full(Rts.shape, qb) * scale
    qmar = cq(Sca.ravel(), alpha)
    res["Marginal"] = np.full(Rts.shape, qmar) * scale
    stats = {}
    for k, hw in res.items():
        cov = np.abs(Rts) <= hw
        stats[k] = dict(joint=float(cov.all(axis=(1, 2)).mean()),
                        marginal=float(cov.mean()), width=float(np.mean(2 * hw)))
    base = stats["Marginal"]["width"]
    for k in stats:
        stats[k]["width_ratio"] = stats[k]["width"] / base
    return stats