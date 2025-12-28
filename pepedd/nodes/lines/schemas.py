from typing import List, Literal, Annotated, Optional

from pydantic import BaseModel, Field

LinesElementInt = Annotated[int, Field(ge=1)]
LinesElementFloat = Annotated[float, Field(ge=0, le=1)]
LinesRangeFloat = Annotated[List[LinesElementFloat], Field(min_length=2, max_length=2)]
LinesRangeInt = Annotated[List[LinesElementInt], Field(min_length=2, max_length=2)]
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
    n_lines: LinesRangeInt = [1, 50]
    size0: LinesRangeInt = [1, 5]
    size1: LinesRangeInt = [1, 5]
    line_range0: LinesRangeFloat = [0, 0]
    line_range1: LinesRangeFloat = [1, 1]
    alpha: LinesRangeFloat = [0.5, 1]
    h: LinesRangeFloat = [0, 1]
    s: LinesRangeFloat = [0, 1]
    v: LinesRangeFloat = [0, 1]
    radius0: LinesRangeFloat = [0, 256]
    radius1: LinesRangeFloat = [512, 512]
    angle0: LinesRangeFloat = [-360, -1]
    angle1: LinesRangeFloat = [0, 360]
    probability: float = 1.0
    seed: Optional[int] = None
