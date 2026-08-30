"""Decision-level evaluation -- wedge component W4, metric MET08.

WHY THIS EXISTS. Every metric up to this point scores the calibration layer on
coverage. Coverage is a means, not an end. A planner does not consume a
coverage number; they consume a decision, and they pay asymmetrically for
getting it wrong. This module asks the only question that closes the loop:
given the SAME frozen forecasts, do better-conditioned intervals lead to a
cheaper decision than the bare point forecast?

THE TASK. Interval-gated peak-demand flagging. For each (test path, horizon
step, meter) the planner must decide whether to flag an incoming demand peak.
A peak is an actual reading above that meter's threshold. Missing a peak is
expensive; a false alarm is cheap but not free.

THE RULES COMPARED.
  FlagNone   never flag                       -- the do-nothing floor, cost 1.0
  FlagAll    always flag                      -- the panic ceiling
  Point      flag iff the point forecast crosses the threshold
  Interval:M flag iff the UPPER endpoint of method M's interval crosses it

`Point` is the comparison that matters, because it is exactly what an
uncalibrated LTSF backbone hands a planner today: a single number with no
notion of how wrong it might be. An interval rule flags on the plausible high
end instead of the central guess, so it can only beat the point rule if the
upper endpoint is honestly calibrated -- too narrow and it misses peaks, too
wide and it drowns in false alarms. That is why this is a real test of
calibration rather than a restatement of it.

TWO THINGS DELIBERATELY NOT DONE.
1. The threshold is computed on the CALIBRATION actuals only. Deriving it from
   the test block would leak the answer into the question.
2. The cost ratio is swept, not chosen. A single ratio invites the reply that
   the conclusion was tuned; a sweep either shows the ordering is stable across
   the sweep or shows where it flips, and both are reportable.

WORST-CHANNEL COST is reported alongside the mean for the same reason
worst-cell coverage is reported alongside marginal coverage: a mean decision
cost can look fine while one meter carries every miss.
"""
import numpy as np

# Cost of a missed peak relative to a false alarm. Swept, never chosen.
DEFAULT_RATIOS = (2.0, 5.0, 10.0, 20.0, 50.0)
PEAK_Q = 0.95


def peak_threshold(Yca, q=PEAK_Q):
    """Per-channel peak threshold from the calibration actuals only.

    Yca: (n_cal, H, C) actual values. Returns (C,).
    """
    return np.quantile(Yca, q, axis=(0, 1))


def _rule_stats(peak, flag, ratio, n_peak):
    """Cost and confusion counts for one rule at one cost ratio."""
    tp = int(np.count_nonzero(peak & flag))
    fn = int(np.count_nonzero(peak & ~flag))
    fp = int(np.count_nonzero(~peak & flag))
    cost = ratio * fn + 1.0 * fp
    floor = ratio * n_peak                      # cost of never flagging
    return dict(
        norm_cost=float(cost / floor) if floor > 0 else None,  # undefined for a rule that flags nothing; None keeps the JSON strict-parseable (NaN literals broke jq/JS)
        raw_cost=float(cost),
        recall=float(tp / n_peak) if n_peak > 0 else None,  # undefined for a rule that flags nothing; None keeps the JSON strict-parseable (NaN literals broke jq/JS)
        precision=float(tp / (tp + fp)) if (tp + fp) > 0 else None,  # undefined for a rule that flags nothing; None keeps the JSON strict-parseable (NaN literals broke jq/JS)
        flag_rate=float((tp + fp) / peak.size),
        n_missed=fn, n_false_alarm=fp,
    )


def _worst_channel_norm_cost(peak, flag, ratio):
    """Highest per-channel normalised cost. The decision analogue of
    worst-cell coverage: a good mean can hide one meter absorbing every miss."""
    worst = 0.0
    for c in range(peak.shape[2]):
        pk, fl = peak[:, :, c], flag[:, :, c]
        npk = int(np.count_nonzero(pk))
        if npk == 0:
            continue
        cost = ratio * np.count_nonzero(pk & ~fl) + np.count_nonzero(~pk & fl)
        worst = max(worst, float(cost / (ratio * npk)))
    return worst


def evaluate(Yts, pred, halves, tau, ratios=DEFAULT_RATIOS):
    """Score every decision rule across the cost sweep.

    Yts    (n, H, C) actual test paths
    pred   (n, H, C) frozen point forecasts
    halves {method: (n, H, C) half-width}
    tau    (C,) per-channel peak threshold from peak_threshold()

    Returns {"n_peak", "peak_rate", "by_ratio": {ratio: {rule: stats}}}.
    """
    t = tau[None, None, :]
    peak = Yts > t
    n_peak = int(np.count_nonzero(peak))

    flags = {
        "FlagNone": np.zeros_like(peak),
        "FlagAll": np.ones_like(peak),
        "Point": pred > t,
    }
    for name, h in halves.items():
        flags[f"Interval:{name}"] = (pred + h) > t

    by_ratio = {}
    for r in ratios:
        row = {}
        for rule, flag in flags.items():
            st = _rule_stats(peak, flag, r, n_peak)
            st["worst_channel_norm_cost"] = _worst_channel_norm_cost(peak, flag, r)
            row[rule] = st
        by_ratio[str(r)] = row

    return dict(n_peak=n_peak, peak_rate=float(n_peak / peak.size),
                n_obs=int(peak.size), peak_q=PEAK_Q,
                ratios=list(ratios), by_ratio=by_ratio)
