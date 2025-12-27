from typing import Literal, Optional, Annotated, List, Any
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
    floydsteinberg: PaletteRange
    jarvisjudiceninke: PaletteRange
    stucki: PaletteRange
    atkinson: PaletteRange
    burkes: PaletteRange
    sierra: PaletteRange
    tworowsierra: PaletteRange
    sierraLite: PaletteRange
    order: PaletteRange
    riemersma: PaletteRange
    quantize: PaletteRange


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

    target_color: TargetColorCh = Field(default_factory=TargetColorCh)
    map_size: List[int] = [2, 4, 8, 16]
    history: List[int] = [10, 15]
    ratio: List[float] = [0.1, 0.9]
    probability: float = 1.0
    seed: Optional[int] = None

    @model_validator(mode="before")
    @classmethod
    def fill_target_color(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        default_color_ch = data.get("color_in_img", [8, 512])

        if "target_color" not in data or data["target_color"] is None:
            data["target_color"] = {}

        target = data["target_color"]

        # Note: You need to access the args of the Literal to get the list of keys
        # AlgorithmType is a typing.Literal, so we use __args__ to get the values
        from typing import get_args

        kernel_fields = get_args(LDAlg)

        for field in kernel_fields:
            if field not in target or target[field] is None:
                target[field] = default_color_ch

        return data
