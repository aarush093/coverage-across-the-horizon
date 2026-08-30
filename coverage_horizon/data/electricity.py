"""Electricity loader -- the S5 case-study surface.

WHY THIS FILE EXISTS. Everything up to S4 scores the calibration layer on the
ETT benchmark: four datasets, seven channels each, 42 cells in the
horizon-bucket x channel grid. That is a small grid, and a method can look good
on a small grid for uninteresting reasons. The case study moves to a surface
that is wider (50 channels, 300 cells), longer, and split so that calibration
and test sit in different seasons -- which is the temporal shift the study is
supposed to survive.

This is the fallback surface named in Idea Lock section 12, risk R3, promoted
to primary by decision D006. BDG2 remains the stated extension; its loader is
data-gated rather than silently guessed at.

THE DATA. The LTSF Electricity set as standardised by the LSTNet release:
26,304 hourly rows x 321 client meters, comma-separated, no header and no date
column. [FACT, verified 2026-08-30: shape (26304, 321).]

MISSINGNESS AND THE SCREENING RULE. Meters that came online partway through
the record are padded with exact zeros, and a long run of zeros is missingness
wearing a number's clothing -- it would be standardised, windowed, and scored
as if it were a real reading. The rule here is deliberately blunt and stated in
one line so a reviewer can check it:

    keep a meter only if it contains NO zero reading anywhere in the record,
    then take the first 50 such meters in original column order.

[FACT, measured 2026-08-30] 92 of the 321 meters pass that test, so 50 are
available without reaching into the partially-zero tail; the median meter has 3
zeros and the worst has 19,915. Taking the first 50 in column order rather than
the "cleanest" 50 matters: every candidate is equally clean, so ordering by any
quality score would only invite the question of what else was ranked.

SPLIT. Sequential 70/10/20 on rows, matching the protocol used for ETT:
train 0:18412, calibration 18412:21043, test 21043:26304. Each block's input
window may reach back by SEQ_LEN, which is the boundary rule of the standard
LTSF protocol and is why the ranges below overlap by exactly SEQ_LEN.

[ASSUMPTION] The file carries no timestamps, so calendar dates cannot be read
off it. Under the documented LSTNet start of 2012-01-01 the blocks land at
train -> 2014-02-06, calibration -> 2014-05-26, test -> end of 2014, i.e.
calibrate in late winter and spring, audit through summer into winter. The
seasonal-shift claim does not actually depend on that start date: the
calibration block is ~110 days and the test block ~219 days, so they cannot
occupy the same season whatever the record begins.

KNOWN WEAKNESS, stated here rather than discovered by a reviewer. At H=720 the
calibration block yields ~80 strided windows against a 300-cell grid. The
smallest log-spaced horizon bucket holds the fewest horizon steps and therefore
the fewest samples, and that is the most likely mechanism behind the
minimum-cell regression seen on this surface (43_REVIEWER_2 RV08, open question
Q09). Report cell_p05 and the fraction of cells within 5 points of target
alongside the raw minimum, and do not let the minimum carry the argument alone.
"""
import os

import numpy as np

from ..config import DATA_DIR, ECL_FILE, ECL_METERS, ECL_SPLIT_FRAC, SEQ_LEN

_FETCH_HINT = (
    "Electricity data not found at {path}\n"
    "Fetch it with:  python scripts/download_data.py\n"
    "or directly from https://raw.githubusercontent.com/laiguokun/"
    "multivariate-time-series-data/master/electricity/electricity.txt.gz"
)


def screen(raw):
    """Return the kept column indices and a screening report.

    Separated from load() so the rule can be tested and quoted on its own.
    """
    zeros = (raw == 0).sum(axis=0)
    clean = [j for j in range(raw.shape[1]) if zeros[j] == 0]
    kept = clean[:ECL_METERS]
    report = dict(
        n_meters_total=int(raw.shape[1]),
        n_meters_clean=len(clean),
        n_kept=len(kept),
        kept=kept,
        zeros_median=int(np.median(zeros)),
        zeros_max=int(zeros.max()),
        zeros_in_kept=int(zeros[kept].sum()),
    )
    return kept, report


def load_electricity(path=None):
    """Return (arr, train_range, cal_range, test_range, meta).

    Same contract as data.loader.load, plus a meta dict, so the array can be
    handed straight to data.windows and pipeline.run_backbone. Standardisation
    is fit on the training block only -- no future information reaches it.
    """
    path = path or os.path.join(DATA_DIR, ECL_FILE)
    if not os.path.exists(path):
        raise FileNotFoundError(_FETCH_HINT.format(path=path))

    raw = np.loadtxt(path, delimiter=",", dtype=np.float64)
    if raw.ndim != 2:
        raise ValueError(f"expected a 2-D table, got shape {raw.shape}")

    kept, report = screen(raw)
    if len(kept) < ECL_METERS:
        raise ValueError(
            f"screening kept only {len(kept)} meters with no zero readings; "
            f"{ECL_METERS} were required. Do not silently proceed on a "
            f"different surface than the one that is documented."
        )
    arr = raw[:, kept]

    n = arr.shape[0]
    f_tr, f_va = ECL_SPLIT_FRAC
    tr, va = int(n * f_tr), int(n * f_va)

    mu = arr[:tr].mean(axis=0)
    sd = arr[:tr].std(axis=0)
    if not np.all(sd > 0):
        raise ValueError("a kept meter is constant over the training block")
    arr = (arr - mu) / sd

    meta = dict(report, n_rows=int(n), split_rows=(0, tr, va, int(n)),
                source=os.path.basename(path))
    return arr, (0, tr), (tr - SEQ_LEN, va), (va - SEQ_LEN, int(n)), meta
