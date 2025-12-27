from typing import List, Literal, Annotated, Optional, Any

from pydantic import BaseModel, Field, model_validator

KernelElement = Annotated[float, Field(ge=0)]
KernelRange = Annotated[List[KernelElement], Field(min_length=2, max_length=2)]
literal_blur = Literal[
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
    filters: List[literal_blur] = ["ring"]
    kernel: KernelRange = [0, 1]
    target_kernels: TargetKernels = Field(default_factory=lambda: TargetKernels())
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

    @model_validator(mode="before")
    @classmethod
    def fill_target_kernels(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        default_kernel = data.get("kernel", [0.0, 10.0])

        if "target_kernels" not in data or data["target_kernels"] is None:
            data["target_kernels"] = {}

        target = data["target_kernels"]

        kernel_fields = [
            "box",
            "gauss",
            "median",
            "lens",
            "random",
            "airy",
            "triangle",
            "ring",
        ]
        for field in kernel_fields:
            if field not in target or target[field] is None:
                target[field] = default_kernel

        return data
