"""Coverage Across the Horizon.

Horizon- and channel-conditional adaptive conformal calibration for
long-term time-series forecasting.
"""
__version__ = "0.1.0"

from .config import SEED, DATASETS, HORIZONS, ALPHA, K_BUCKETS, GAMMA
from .pipeline import run_backbone
from .calibration import calibrate, joint_layers, metrics, buckets, cq
