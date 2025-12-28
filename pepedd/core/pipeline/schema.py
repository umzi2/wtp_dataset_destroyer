from typing import List, Any, Literal, Optional

from pydantic import BaseModel, model_validator


class Degradation(BaseModel):
    type: str
    options: Any


class TileOptions(BaseModel):
    size: int = 512
    no_wb: bool = True


class PipelineOptions(BaseModel):
    input: str = "input"
    output: str = "output"
    map_type: Literal["simple", "thread", "process"] = "thread"
    degradation: List[Degradation]

    num_workers: Optional[int] = None
    tile: Optional[TileOptions] = None

    dataset_size: Optional[int] = None
    shuffle_dataset: bool = True
    gray: bool = False

    debug: bool = False

    only_lq: bool = False
    real_name: bool = False

    output_clear: bool = True
    seed: Optional[int] = None

    @model_validator(mode="after")
    def apply_debug_and_seed(self):
        if self.debug:
            self.map_type = "simple"
            if self.seed is None:
                self.seed = 1234
        if self.seed is None:
            import secrets

            self.seed = secrets.randbits(64)
        return self
