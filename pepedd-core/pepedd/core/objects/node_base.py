from abc import ABC, abstractmethod
from typing import Optional

from ..objects.lq_hq_state import LQHQState
from ..objects.safe_rng import SafeRNG


class Node(ABC):
    def __init__(self, probability: float = 1.0, seed: Optional[int] = None):
        self.seed = seed
        self.probability = probability

    def __call__(self, data: LQHQState) -> LQHQState:
        if self.seed is not None:
            rng_backup = data.rng
            data.rng = SafeRNG(seed=self.seed)
            if self.probability > data.rng.uniform(0, 1):
                data = self.forward(data)
            data.rng = rng_backup
        else:
            if self.probability > data.rng.uniform(0, 1):
                data = self.forward(data)
        return data

    @abstractmethod
    def forward(self, data: LQHQState) -> LQHQState:
        pass
