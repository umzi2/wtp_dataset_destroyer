from pydantic import BaseModel, field_validator, Field
from typing import List, Optional

from ..utils.validate import validate_resize_algorithms


class DownUpOptions(BaseModel):
    down: List[int] = [2, 2]
    alg_up: List[str] = ["c_catmullrom"]
    alg_down: List[str] = ["c_catmullrom"]

    @field_validator("alg_down", "alg_up")
    @classmethod
    def check_algs(cls, v):
        return validate_resize_algorithms(v)


class UpDownOptions(BaseModel):
    up: List[int] = [2, 2]
    alg_up: List[str] = ["c_catmullrom"]
    alg_down: List[str] = ["c_catmullrom"]

    @field_validator("alg_down", "alg_up")
    @classmethod
    def check_algs(cls, v):
        return validate_resize_algorithms(v)


class DownDownOptions(BaseModel):
    step: List[int] = [2, 6]
    alg_down: List[str] = ["s_catmullrom"]

    @field_validator("alg_down")
    @classmethod
    def check_algs(cls, v):
        return validate_resize_algorithms(v)


class ResizeOptions(BaseModel):
    alg_lq: List[str] = ["up_down", "down_up", "down_down"]
    alg_hq: List[str] = ["s_catmullrom", "nearest", "dpid_0.5"]

    @field_validator("alg_lq", "alg_hq")
    @classmethod
    def check_algs(cls, v):
        return validate_resize_algorithms(v)

    down_up: DownUpOptions = Field(default_factory=DownUpOptions)
    up_down: UpDownOptions = Field(default_factory=UpDownOptions)
    down_down: DownDownOptions = Field(default_factory=DownDownOptions)
    spread: List[float] = [0.25, 1, 0.1]
    scale: int = 4
    s_samplings: List[int] = [2, 8]
    divider: int = 2
    olq: bool = False
    probability: float = 1.0
    seed: Optional[int] = None
