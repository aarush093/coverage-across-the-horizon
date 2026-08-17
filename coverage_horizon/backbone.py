"""Frozen point-forecasting backbones.

Two structurally different linear backbones from the DLinear paper:

  DLinear - series decomposition (moving-average trend + seasonal remainder),
            then a shared linear map on the concatenated components.
  NLinear - subtract the last observed value, apply a linear map, add it back.
            The level subtraction is its whole mechanism.

Both are linear with a squared-error loss, so both are solved in closed form by
least squares. That returns the global optimum of exactly the objective SGD
approximates, so there is no learning rate or epoch schedule to tune and the
fits are bit-reproducible. Weights are frozen after fitting.
"""
import numpy as np

from .config import SEQ_LEN, KERNEL


def decompose(x):
    """DLinear decomposition. x: (N, L, C) -> (trend, seasonal).

    Trend is a moving average with replicate padding, kernel=25; seasonal is
    the remainder.
    """
    pad = (KERNEL - 1) // 2
    xp = np.concatenate([np.repeat(x[:, :1], pad, axis=1), x,
                         np.repeat(x[:, -1:], pad, axis=1)], axis=1)
    csum = np.cumsum(xp, axis=1)
    csum = np.concatenate([np.zeros_like(csum[:, :1]), csum], axis=1)
    trend = (csum[:, KERNEL:] - csum[:, :-KERNEL]) / KERNEL
    return trend, x - trend


def feat_dim(kind):
    return SEQ_LEN if kind == "nlinear" else 2 * SEQ_LEN


def featurise(X, kind="dlinear"):
    """(N, L, C) -> (features (N*C, D), offset (N*C, 1)).

    dlinear: D = 2L, features [seasonal | trend], offset 0.
    nlinear: D = L,  features (x - x[-1]), offset x[-1].
    """
    N, L, C = X.shape
    if kind == "nlinear":
        last = X[:, -1:, :]                                   # (N,1,C)
        f = (X - last).transpose(0, 2, 1).reshape(-1, SEQ_LEN)
        off = last.transpose(0, 2, 1).reshape(-1, 1)
        return f, off
    trend, seas = decompose(X)
    f = np.concatenate([seas.transpose(0, 2, 1), trend.transpose(0, 2, 1)], axis=2)
    return f.reshape(-1, 2 * SEQ_LEN), np.zeros((N * C, 1))


def fit(arr, tr_lo, tr_hi, pred_len, ridge=1e-3, chunk=4000, kind="dlinear"):
    """Closed-form ridge least squares. Accumulates the normal equations in
    chunks to bound memory. Returns (W, n_train)."""
    d = feat_dim(kind)
    XtX = np.zeros((d + 1, d + 1))
    XtY = np.zeros((d + 1, pred_len))
    n_tot = tr_hi - tr_lo - SEQ_LEN - pred_len + 1
    for s in range(0, n_tot, chunk):
        idx = np.arange(s, min(s + chunk, n_tot))
        X = np.stack([arr[tr_lo + i: tr_lo + i + SEQ_LEN] for i in idx])
        Y = np.stack([arr[tr_lo + i + SEQ_LEN: tr_lo + i + SEQ_LEN + pred_len] for i in idx])
        F, off = featurise(X, kind)
        T = Y.transpose(0, 2, 1).reshape(-1, pred_len)
        if kind == "nlinear":
            T = T - off                                       # predict the delta
        F = np.concatenate([F, np.ones((F.shape[0], 1))], axis=1)   # bias
        XtX += F.T @ F
        XtY += F.T @ T
    XtX[np.arange(d), np.arange(d)] += ridge * n_tot          # no penalty on bias
    W = np.linalg.solve(XtX, XtY)
    return W, n_tot


def predict(W, X, pred_len, kind="dlinear"):
    """Apply the frozen map. X: (n, L, C) -> (n, H, C)."""
    F, off = featurise(X, kind)
    F = np.concatenate([F, np.ones((F.shape[0], 1))], axis=1)
    P = F @ W
    if kind == "nlinear":
        P = P + off                                           # add the level back
    n, _, C = X.shape
    return P.reshape(n, C, pred_len).transpose(0, 2, 1)
