from dataclasses import dataclass
import numpy as np
from ..objects.safe_rng import SafeRNG


@dataclass
class LQHQState:
    rng: SafeRNG
    lq: np.ndarray
    hq: np.ndarray
