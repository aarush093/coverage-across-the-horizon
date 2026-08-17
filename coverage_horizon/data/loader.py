"""Dataset loading and windowing.

Sequential split, train-only standardisation, drop_last disabled: every
window that fits is kept.
"""
import numpy as np
import pandas as pd

from ..config import SEQ_LEN, SPLITS, DATA_DIR
import os


def load(name):
    """Return (standardised array, train_range, cal_range, test_range).

    The scaler is fit on the training block only; no future information
    reaches it. Each split's input window may reach back by SEQ_LEN, which
    is the boundary rule of the standard LTSF protocol.
    """
    df = pd.read_csv(os.path.join(DATA_DIR, f"{name}.csv"))
    arr = df.iloc[:, 1:].to_numpy(dtype=np.float64)      # 7 channels, drop date col
    tr, va, te = SPLITS[name]
    mu, sd = arr[:tr].mean(0), arr[:tr].std(0)
    arr = (arr - mu) / sd
    return arr, (0, tr), (tr - SEQ_LEN, va), (va - SEQ_LEN, te)


def windows(arr, lo, hi, pred_len, stride=1):
    """Sliding windows over arr[lo:hi]. drop_last disabled."""
    n = hi - lo - SEQ_LEN - pred_len + 1
    if n <= 0:
        return None, None
    idx = np.arange(0, n, stride)
    X = np.stack([arr[lo + i: lo + i + SEQ_LEN] for i in idx])
    Y = np.stack([arr[lo + i + SEQ_LEN: lo + i + SEQ_LEN + pred_len] for i in idx])
    return X, Y
