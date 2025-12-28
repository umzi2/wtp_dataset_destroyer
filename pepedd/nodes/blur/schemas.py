from typing import List, Literal, Annotated, Optional, get_args

from pydantic import BaseModel, Field, model_validator

KernelElement = Annotated[float, Field(ge=0)]
KernelRange = Annotated[List[KernelElement], Field(min_length=2, max_length=2)]
LiteralBlur = Literal[
    "box", "gauss", "median", "lens", "motion", "random", "airy", "ring", "triangle"
]


class TargetKernels(BaseModel):
    box: Optional[KernelRange] = None
    gauss: Optional[KernelRange] = None
    median: Optional[KernelRange] = None
    lens: Optional[KernelRange] = None
    random: Optional[KernelRange] = None
    airy: Optional[KernelRange] = None
    triangle: Optional[KernelRange] = None
    ring: Optional[KernelRange] = None


class BlurOptions(BaseModel):
    filters: List[LiteralBlur] = ["ring"]
    kernel: KernelRange = [0, 1]
    target_kernels: TargetKernels = TargetKernels()
    motion_size: List[int] = Field(
        default_factory=lambda: [0, 10], min_length=2, max_length=2
    )
    motion_angle: List[float] = Field(
        default_factory=lambda: [-30.0, 30.0], min_length=2, max_length=2
    )
    ring_thickness: List[int] = Field(
        default_factory=lambda: [1, 5], min_length=2, max_length=2
    )
    probability: float = 1.0
    seed: Optional[int] = None

    @model_validator(mode="after")
    def fill_target_kernels(self):
        kernel_fields = set(get_args(LiteralBlur)) - {"motion"}
        target_dict = self.target_kernels.model_dump()
        for field in kernel_fields:
            if target_dict[field] is None:
                target_dict[field] = self.kernel
        self.target_kernels = TargetKernels(**target_dict)
        return self
