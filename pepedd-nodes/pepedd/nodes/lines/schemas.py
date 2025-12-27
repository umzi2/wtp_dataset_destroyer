from typing import List, Literal, Annotated, Optional

from pydantic import BaseModel, Field

LinesElementInt = Annotated[int, Field(ge=1)]
LinesElementFloat = Annotated[float, Field(ge=0, le=1)]
LineLiteral = Literal[
    "lines_random",
    "beziers_random",
    "circle_random",
    "circle_uniform",
    "rays_uniform",
    "rays_random",
]


class LinesOptions(BaseModel):
    mode: List[LineLiteral] = [
        "lines_random",
        "beziers_random",
        "circle_random",
        "circle_uniform",
        "rays_uniform",
        "rays_random",
    ]
    n_lines: List[LinesElementInt] = Field(default=[1, 50], min_length=2, max_length=2)
    size0: List[LinesElementInt] = Field(default=[1, 5], min_length=2, max_length=2)
    size1: List[LinesElementInt] = Field(default=[1, 5], min_length=2, max_length=2)
    line_range0: List[LinesElementFloat] = Field(
        default=[0, 0], min_length=2, max_length=2
    )
    line_range1: List[LinesElementFloat] = Field(
        default=[1, 1], min_length=2, max_length=2
    )
    alpha: List[LinesElementFloat] = Field(default=[0.5, 1], min_length=2, max_length=2)
    h: List[LinesElementFloat] = Field(default=[0, 1], min_length=2, max_length=2)
    s: List[LinesElementFloat] = Field(default=[0, 1], min_length=2, max_length=2)
    v: List[LinesElementFloat] = Field(default=[0, 1], min_length=2, max_length=2)
    radius0: List[LinesElementFloat] = Field(
        default=[0, 256], min_length=2, max_length=2
    )
    radius1: List[LinesElementFloat] = Field(
        default=[512, 512], min_length=2, max_length=2
    )
    angle0: List[LinesElementFloat] = Field(
        default=[-360, -1], min_length=2, max_length=2
    )
    angle1: List[LinesElementFloat] = Field(
        default=[0, 360], min_length=2, max_length=2
    )
    probability: float = 1.0
    seed: Optional[int] = None
