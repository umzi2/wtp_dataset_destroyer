from typing import Literal, Optional, Annotated, List, get_args
from pydantic import BaseModel, Field, model_validator

PaletteElement = Annotated[int, Field(ge=8, le=255 * 255 * 255)]
PaletteRange = Annotated[List[PaletteElement], Field(min_length=2, max_length=2)]
LDAlg = Literal[
    "floydsteinberg",
    "jarvisjudiceninke",
    "stucki",
    "atkinson",
    "burkes",
    "sierra",
    "tworowsierra",
    "sierraLite",
    "order",
    "riemersma",
    "quantize",
]

LDPalette = Literal[
    "oc_tree",
    "median_cut",
    "wu",
    "min_max_uniform",
    "l_oc_tree",
    "l_median_cut",
    "l_wu",
    "l_min_max_uniform",
    "l_popular",
    "uniform",
]


class TargetColorCh(BaseModel):
    floydsteinberg: PaletteRange = None
    jarvisjudiceninke: PaletteRange = None
    stucki: PaletteRange = None
    atkinson: PaletteRange = None
    burkes: PaletteRange = None
    sierra: PaletteRange = None
    tworowsierra: PaletteRange = None
    sierraLite: PaletteRange = None
    order: PaletteRange = None
    riemersma: PaletteRange = None
    quantize: PaletteRange = None


class DitheringOptions(BaseModel):
    types: list[LDAlg] = [
        "floydsteinberg",
        "jarvisjudiceninke",
        "stucki",
        "atkinson",
        "burkes",
        "sierra",
        "tworowsierra",
        "sierraLite",
        "riemersma",
        "quantize",
    ]
    palette: list[LDPalette] = [
        "oc_tree",
        "median_cut",
        "wu",
        "l_oc_tree",
        "l_median_cut",
        "l_wu",
        "l_popular",
    ]
    color_in_img: PaletteRange = [32, 1024]

    target_color: TargetColorCh = TargetColorCh()
    map_size: List[int] = [2, 4, 8, 16]
    history: List[int] = [10, 15]
    ratio: List[float] = [0.1, 0.9]
    probability: float = 1.0
    seed: Optional[int] = None

    @model_validator(mode="after")
    def fill_target_compress(self):
        alg_fields = set(get_args(LDAlg))
        target_dict = self.target_color.model_dump()
        for field in alg_fields:
            if target_dict[field] is None:
                target_dict[field] = self.color_in_img
        self.target_color = TargetColorCh(**target_dict)
        return self
