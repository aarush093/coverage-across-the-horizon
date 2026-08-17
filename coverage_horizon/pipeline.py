"""End-to-end: fit a frozen backbone on one (dataset, horizon), then produce
the calibration and test residual tensors that feed the calibration layers.
"""
import time
import numpy as np

from .config import SEQ_LEN, STRIDE
from .data import load, windows
from . import backbone


def run_backbone(name, pred_len, kind="dlinear", stride=None, point_eval=True):
    """Fit a backbone, evaluate point error, and return residual tensors.

    Point-forecast error uses stride-1 windows (drop_last disabled), chunked
    for memory. Calibration and test residuals use STRIDED windows so that
    whole-path coverage is counted over near-independent paths (fix F3).
    """
    arr, (tl, th), (vl, vh), (sl, sh) = load(name)
    t0 = time.time()
    W, ntr = backbone.fit(arr, tl, th, pred_len, kind=kind)
    fit_s = time.time() - t0

    mse = mae = float("nan")
    if point_eval:
        n_te = sh - sl - SEQ_LEN - pred_len + 1
        se = sa = cnt = 0.0
        for s in range(0, n_te, 512):
            idx = np.arange(s, min(s + 512, n_te))
            Xb = np.stack([arr[sl + i: sl + i + SEQ_LEN] for i in idx])
            Yb = np.stack([arr[sl + i + SEQ_LEN: sl + i + SEQ_LEN + pred_len] for i in idx])
            d = backbone.predict(W, Xb, pred_len, kind=kind) - Yb
            se += float((d ** 2).sum()); sa += float(np.abs(d).sum()); cnt += d.size
        mse, mae = se / cnt, sa / cnt

    st = STRIDE[name] if stride is None else stride
    Xca, Yca = windows(arr, vl, vh, pred_len, stride=st)
    Rca = Yca - backbone.predict(W, Xca, pred_len, kind=kind)
    Xts, Yts = windows(arr, sl, sh, pred_len, stride=st)
    Rts = Yts - backbone.predict(W, Xts, pred_len, kind=kind)

    return dict(name=name, H=pred_len, kind=kind, mse=mse, mae=mae,
                n_train=int(ntr), fit_s=fit_s, stride=st,
                n_cal=int(Rca.shape[0]), n_test=int(Rts.shape[0]),
                Rca=Rca, Rts=Rts)
