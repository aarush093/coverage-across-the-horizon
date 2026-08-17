"""Conditional calibration layers.

Seven methods share one interface via `calibrate`, laid out as a factorial over
conditioning (none / horizon / channel / horizon x channel) and adaptation
(off / on), plus one parametric reference:

  Gaussian  - per-cell residual std x z, assumes normality, NOT conformal
  Global    - one split-conformal quantile for everything
  MSCP      - per-horizon quantile (established baseline, fix F1)
  CondC     - channel-only quantile, static
  Cond      - horizon-bucket x channel, static
  ACI       - unconditional, adaptive (isolates adaptation)
  Proposed  - horizon-bucket x channel, adaptive

Stating the contribution as an interaction rather than a bare comparison is the
point of the factorial: conditioning alone and adaptation alone can then be
shown to fail on their own.
"""
import numpy as np

from ..config import ALPHA, K_BUCKETS, GAMMA

Z90 = 1.6448536269514722          # standard normal 95th percentile


def buckets(H, K):
    """K log-spaced horizon buckets over 1..H."""
    edges = np.unique(np.round(np.logspace(0, np.log10(H), K + 1)).astype(int))
    edges[0], edges[-1] = 1, H
    bid = np.zeros(H, dtype=int)
    for k in range(len(edges) - 1):
        lo = edges[k] - 1 if k == 0 else edges[k]
        bid[lo:edges[k + 1]] = k
    return bid, edges


def cq(scores, alpha):
    """Finite-sample conformal quantile, ceil((n+1)(1-alpha))/n."""
    n = len(scores)
    if n == 0:
        return np.inf
    q = min(1.0, np.ceil((n + 1) * (1 - alpha)) / n)
    return float(np.quantile(scores, q, method="higher"))


def _scale_of(Rca, how="mad"):
    """Robust per-channel scale. MAD by default; std is an ablation."""
    s = Rca.std(axis=(0, 1)) if how == "std" else np.median(np.abs(Rca), axis=(0, 1))
    return np.maximum(s, 1e-8)[None, None, :]


def calibrate(Rca, Rts, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA, scale_how="mad"):
    """Half-widths on the test paths for every method."""
    n_cal, H, C = Rca.shape
    n_ts = Rts.shape[0]
    scale = _scale_of(Rca, scale_how)
    Sca = np.abs(Rca) / scale
    out = {}
    bid, edges = buckets(H, K)
    ks = np.unique(bid)

    # --- parametric reference: per-cell Gaussian, full h x c conditioning ---
    sd = Rca.std(axis=0)                                  # (H, C)
    out["Gaussian"] = np.tile((Z90 * sd)[None, :, :], (n_ts, 1, 1))

    # --- static conformal family ---
    out["Global"] = np.full((n_ts, H, C), cq(Sca.ravel(), alpha)) * scale

    q = np.array([cq(Sca[:, h, :].ravel(), alpha) for h in range(H)])
    out["MSCP"] = np.tile(q[None, :, None], (n_ts, 1, C)) * scale

    qc = np.array([cq(Sca[:, :, c].ravel(), alpha) for c in range(C)])
    out["CondC"] = np.tile(qc[None, None, :], (n_ts, H, 1)) * scale

    qbc = np.zeros((len(ks), C))
    for k in ks:
        for c in range(C):
            qbc[k, c] = cq(Sca[:, bid == k, c].ravel(), alpha)
    out["Cond"] = np.tile(qbc[bid][None, :, :], (n_ts, 1, 1)) * scale

    # --- adaptive, unconditional ---
    flat = np.sort(Sca.ravel()); nf = len(flat)
    a_t = alpha
    hA = np.zeros((n_ts, H, C))
    for t in range(n_ts):
        j = int(np.ceil((nf + 1) * (1 - min(max(a_t, 1e-4), 0.5)))) - 1
        hA[t] = flat[min(max(j, 0), nf - 1)] * scale[0, 0][None, :]
        a_t += gamma * (alpha - (1.0 - (np.abs(Rts[t]) <= hA[t]).mean()))
    out["ACI"] = hA

    # --- proposed: conditioning + per-cell adaptation ---
    alpha_t = np.full(qbc.shape, alpha)
    half = np.zeros((n_ts, H, C))
    pool = {(k, c): np.sort(Sca[:, bid == k, c].ravel()) for k in ks for c in range(C)}
    npool = {key: len(v) for key, v in pool.items()}

    def fast_q(key, a):
        v = pool[key]; n = npool[key]
        j = int(np.ceil((n + 1) * (1 - min(max(a, 1e-4), 0.5)))) - 1
        return v[min(max(j, 0), n - 1)]

    for t in range(n_ts):
        qt = np.array([[fast_q((k, c), alpha_t[k, c]) for c in range(C)] for k in ks])
        half[t] = qt[bid] * scale[0, 0][None, :]
        cov = np.abs(Rts[t]) <= half[t]
        for k in ks:
            m = bid == k
            for c in range(C):
                alpha_t[k, c] += gamma * (alpha - (1.0 - cov[m, c].mean()))
    out["Proposed"] = half
    return out, edges, scale
