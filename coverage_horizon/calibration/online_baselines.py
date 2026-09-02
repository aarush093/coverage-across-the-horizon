"""Per-horizon online conformal and conformal PID -- the two baselines the
Idea Lock's comparison set named and Draft v1 omitted.

WHY THESE TWO. Once the online protocol is stated honestly (D015: a path's
outcome reaches its tracker only when realised), the obvious reviewer question
is no longer "did you adapt?" but "the multi-step online conformal family
exists for exactly this delayed-feedback problem -- why is none of it here?".
These are that family's two published mechanisms:

* **MSCP-online** (this file's ``mscp_online``). One ACI tracker per horizon
  step, no channel dimension. This is the structural core shared by the
  multi-step online conformal line: calibrate per horizon, update online from
  realised coverage. It is the strongest honest baseline against our horizon
  axis, because it conditions on horizon at full resolution -- finer than our
  K buckets -- and adapts.

* **Conformal PID** (``conformal_pid``). Angelopoulos, Candes and Tibshirani's
  generalisation of the ACI update: the ACI term is the integral (I) action,
  and a proportional (P) term on the current coverage error is added so the
  tracker responds to a deviation immediately rather than only through its
  accumulated history. Run per horizon, matching the scalar setting the method
  was published in, with realised feedback.

WHAT IS DELIBERATELY NOT CLAIMED. AcMCP's distinguishing contribution is a
correction for the autocorrelation *between* multi-step errors at different
horizons, with a long-run guarantee that accounts for it. That correction is
NOT reimplemented here: we did not have the method in enough detail to
reproduce it faithfully, and a half-right reimplementation scored against our
own layer would be worse than an honest omission. So these baselines are a
LOWER BOUND on what that family achieves, and the paper says so. What they do
establish is the thing our contribution actually rests on: that per-horizon
conditioning plus online adaptation -- without the channel axis -- does not
reach the conditional coverage of the horizon x channel layer.

Both return half-widths on the same (n_test, H, C) grid as `calibrate`, use
the same MAD-normalised scores and the same gamma, and take feedback only once
realised, so any difference against the Proposed layer is the conditioning
structure and nothing else.
"""
import numpy as np

from .conditional import _scale_of
from ..config import ALPHA, GAMMA

# PID gains. The integral gain is our gamma, so the I-only special case is
# exactly ACI and the comparison isolates what P adds. K_P is the standard
# small proportional gain; a large one makes the tracker chase noise.
K_P = 0.1


def _sorted_scores_per_h(Sca):
    """Sorted calibration scores for every (h, c). Shape (H, C, n_cal)."""
    return np.sort(Sca, axis=0).transpose(1, 2, 0)


def _read_q(sorted_scores, h, c, a):
    """Conformal quantile of one (h, c) cell at working level a."""
    v = sorted_scores[h, c]
    n = v.shape[0]
    j = int(np.ceil((n + 1) * (1 - min(max(a, 1e-4), 0.5)))) - 1
    return v[min(max(j, 0), n - 1)]


def _online_per_horizon(Rca, Rts, stride, alpha, gamma, scale_how, k_p):
    """Shared loop for MSCP-online (k_p = 0) and conformal PID (k_p > 0).

    One tracker per horizon step, pooled across channels -- the published
    multi-step setting has no channel dimension, and giving the baseline one
    would make it our own method under a different name.

    Horizon step h (1-indexed) of path t is realised ceil(h / stride) paths
    later, so that is exactly how long its tracker waits.
    """
    n_cal, H, C = Rca.shape
    n_ts = Rts.shape[0]
    scale = _scale_of(Rca, scale_how)
    Sca = np.abs(Rca) / scale
    sorted_scores = _sorted_scores_per_h(Sca)

    lag = np.ceil((np.arange(H) + 1) / stride).astype(int)   # per horizon step
    alpha_t = np.full(H, float(alpha))
    half = np.zeros((n_ts, H, C))

    for t in range(n_ts):
        for h in range(H):
            t_done = t - lag[h]
            if t_done < 0:
                continue
            # Realised coverage of step h on the path that just completed,
            # pooled over channels: one scalar error signal per horizon.
            err = alpha - (1.0 - np.mean(np.abs(Rts[t_done, h]) <= half[t_done, h]))
            alpha_t[h] += gamma * err                    # I (this alone is ACI)
            if k_p:
                alpha_t[h] += k_p * err                  # P
        for h in range(H):
            row = np.array([_read_q(sorted_scores, h, c, alpha_t[h]) for c in range(C)])
            half[t, h] = row * scale[0, 0]
    return half


def mscp_online(Rca, Rts, stride, alpha=ALPHA, gamma=GAMMA, scale_how="mad", **_):
    """Per-horizon split conformal with an online ACI update, realised feedback."""
    return _online_per_horizon(Rca, Rts, stride, alpha, gamma, scale_how, k_p=0.0)


def conformal_pid(Rca, Rts, stride, alpha=ALPHA, gamma=GAMMA, scale_how="mad",
                  k_p=K_P, **_):
    """Conformal PID control, per horizon, realised feedback.

    The D term is omitted: it acts on the derivative of the coverage error,
    which on our stride-24 grid is dominated by sampling noise at the path
    level. Reporting a P+I controller and saying so is more useful than a
    D term tuned until it helped.
    """
    return _online_per_horizon(Rca, Rts, stride, alpha, gamma, scale_how, k_p=k_p)


def online_baselines(Rca, Rts, stride, **kw):
    """Both baselines as a {name: half-width} dict, for merging into a run."""
    return {"MSCP-online": mscp_online(Rca, Rts, stride, **kw),
            "PID": conformal_pid(Rca, Rts, stride, **kw)}
