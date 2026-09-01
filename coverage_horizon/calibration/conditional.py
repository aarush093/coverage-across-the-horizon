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


# --------------------------------------------------------------------------
# Realised feedback (FR07 / D015). The loops above update each cell with path
# t's outcomes at ALL horizon steps before path t+1 is issued; with stride s
# and horizon H that consumes outcomes realised up to H - s steps after the
# next forecast origin. The functions below apply a path's outcome only once
# it has actually been observed. Everything else -- pool, quantile rule, gamma,
# clamps, one update per path per cell -- is identical, so the delay is the
# only variable. `calibrate` is deliberately left untouched so that every
# number already committed under the instant-feedback protocol still
# reproduces bit-for-bit.
# --------------------------------------------------------------------------

def calibrate_delayed(Rca, Rts, stride, alpha=ALPHA, K=K_BUCKETS, gamma=GAMMA,
                      scale_how="mad"):
    """Adaptive half-widths using only feedback that has been realised.

    Returns ({"ACI": ..., "Proposed": ...}, edges, lag_by_bucket, lag_full).
    A path's outcome in cell (k, c) reaches the tracker once the cell's last
    horizon step has been observed, i.e. after ceil(edge_hi[k] / stride) paths.
    The unconditional ACI arm waits the full horizon.
    """
    n_cal, H, C = Rca.shape
    n_ts = Rts.shape[0]
    scale = _scale_of(Rca, scale_how)
    Sca = np.abs(Rca) / scale
    bid, edges = buckets(H, K)
    ks = np.unique(bid)
    edge_hi = {k: int(np.max(np.where(bid == k)[0]) + 1) for k in ks}
    lag = {int(k): int(np.ceil(edge_hi[k] / stride)) for k in ks}
    lag_full = int(np.ceil(H / stride))

    def idx_q(v, n, a):
        j = int(np.ceil((n + 1) * (1 - min(max(a, 1e-4), 0.5)))) - 1
        return v[min(max(j, 0), n - 1)]

    flat = np.sort(Sca.ravel()); nf = len(flat)
    a_t = alpha
    hA = np.zeros((n_ts, H, C))
    for t in range(n_ts):
        t_done = t - lag_full
        if t_done >= 0:
            miss = 1.0 - (np.abs(Rts[t_done]) <= hA[t_done]).mean()
            a_t += gamma * (alpha - miss)
        hA[t] = idx_q(flat, nf, a_t) * scale[0, 0][None, :]

    alpha_t = np.full((len(ks), C), alpha)
    half = np.zeros((n_ts, H, C))
    pool = {(k, c): np.sort(Sca[:, bid == k, c].ravel()) for k in ks for c in range(C)}
    npool = {key: len(v) for key, v in pool.items()}
    for t in range(n_ts):
        for k in ks:
            t_done = t - lag[int(k)]
            if t_done < 0:
                continue
            m = bid == k
            cov = np.abs(Rts[t_done][m]) <= half[t_done][m]
            for c in range(C):
                alpha_t[k, c] += gamma * (alpha - (1.0 - cov[:, c].mean()))
        qt = np.array([[idx_q(pool[(k, c)], npool[(k, c)], alpha_t[k, c])
                        for c in range(C)] for k in ks])
        half[t] = qt[bid] * scale[0, 0][None, :]

    return {"ACI": hA, "Proposed": half}, edges, lag, lag_full


def calibrate_with_feedback(Rca, Rts, stride, feedback="realised", **kw):
    """All seven methods, with the adaptive arms under the chosen protocol.

    feedback="realised" is the protocol of record (D015); "instant" reproduces
    the oracle upper bound reported in the paper's appendix. Static methods are
    identical either way, so they always come from `calibrate`.
    """
    half, edges, scale = calibrate(Rca, Rts, **kw)
    if feedback == "instant":
        return half, edges, scale
    if feedback != "realised":
        raise ValueError(f"feedback must be 'realised' or 'instant', got {feedback!r}")
    adaptive, _, _, _ = calibrate_delayed(Rca, Rts, stride, **kw)
    half.update(adaptive)
    return half, edges, scale
