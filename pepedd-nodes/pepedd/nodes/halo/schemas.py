from typing import List, Optional

from pydantic import BaseModel, Field

from ..blur.schemas import BlurOptions


class HaloOptions(BaseModel):
    type_halo: List[str] = ["rgb", "y"]
    blur: BlurOptions = Field(default_factory=lambda: BlurOptions())
    threshold: List[float] = [0, 0]
    amount: List[float] = [1, 3]
    probability: float = 1.0
    seed: Optional[int] = None
