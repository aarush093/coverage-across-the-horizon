"""Global configuration and protocol-hygiene constants.

Every value here is binding across the whole study (Idea Lock section 10):
sequential splits only, drop_last disabled, strided calibration windows,
one fixed and published seed.
"""

SEED = 2026
SEQ_LEN = 336          # input window length L
KERNEL = 25            # DLinear moving-average kernel for trend extraction

# Target miscoverage and calibration defaults
ALPHA = 0.10           # 90% target coverage
K_BUCKETS = 6          # log-spaced horizon buckets (ablated over {4,6,8,10})
GAMMA = 0.02           # ACI adaptation step size

# One calibration window start per seasonal day, to control the residual
# dependence between adjacent stride-1 windows (fix F3).
STRIDE = {"ETTh1": 24, "ETTh2": 24, "ETTm1": 96, "ETTm2": 96}

# Standard LTSF protocol split in rows: 12 / 4 / 4 months.
# (train_end, val_end, test_end)
SPLITS = {
    "ETTh1": (12 * 30 * 24, 12 * 30 * 24 + 4 * 30 * 24, 12 * 30 * 24 + 8 * 30 * 24),
    "ETTh2": (12 * 30 * 24, 12 * 30 * 24 + 4 * 30 * 24, 12 * 30 * 24 + 8 * 30 * 24),
    "ETTm1": (12 * 30 * 24 * 4, 12 * 30 * 24 * 4 + 4 * 30 * 24 * 4, 12 * 30 * 24 * 4 + 8 * 30 * 24 * 4),
    "ETTm2": (12 * 30 * 24 * 4, 12 * 30 * 24 * 4 + 4 * 30 * 24 * 4, 12 * 30 * 24 * 4 + 8 * 30 * 24 * 4),
}

DATASETS = ["ETTh1", "ETTh2", "ETTm1", "ETTm2"]
HORIZONS = [96, 192, 336, 720]

# Where the raw ETT CSVs live. Overridden by download_data.py; kept relative
# so the repo is portable.
import os
_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.environ.get("CH_DATA_DIR", os.path.join(_REPO_ROOT, "data"))
