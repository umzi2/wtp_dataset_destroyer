from colorsys import hsv_to_rgb
from functools import partial

from typing import List
from logging import debug
import numpy as np
from pepeline import line

from pepedd.core.node_register import register_class
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.objects.node_base import Node
from pepedd.core.objects.safe_rng import SafeRNG
from ..lines.lines_funcs import (
    random_lines,
    random_beziers,
    random_circle,
    uniform_rays,
    uniform_circle,
    random_rays,
)
from ..lines.schemas import LinesOptions
from pepeline import resize, ResizesAlg, ResizesFilter


def hue_to_rgb(rng: SafeRNG, h: List[float], s: List[float], v: List[float]):
    h, s, v = rng.safe_uniform(h), rng.safe_uniform(s), rng.safe_uniform(v)
    rgb = np.array(hsv_to_rgb(h, s, v), dtype=np.float32)
    debug(f"    line_color: rgb={rgb} hsv=[{h}, {s}, {v}]")
    return rgb


@register_class("lines")
class Lines(Node):
    def __init__(self, options: LinesOptions | dict):
        if isinstance(options, dict):
            opts = LinesOptions(**options)
        else:
            opts = options
        super().__init__(opts.probability, opts.seed)
        self.line_types = []
        self.alpha = opts.alpha
        self.h2r = partial(hue_to_rgb, h=opts.h, s=opts.s, v=opts.v)
        self.v = opts.v
        for lines_type in opts.mode:
            match lines_type:
                case "lines_random":
                    self.line_types.append(
                        partial(
                            random_lines,
                            s0=opts.size0,
                            s1=opts.size1,
                            n_lines=opts.n_lines,
                        )
                    )
                case "beziers_random":
                    self.line_types.append(
                        partial(
                            random_beziers,
                            s0=opts.size0,
                            s1=opts.size1,
                            n_lines=opts.n_lines,
                        )
                    )
                case "circle_random":
                    self.line_types.append(
                        partial(
                            random_circle,
                            r0=opts.radius0,
                            r1=opts.radius1,
                            n_lines=opts.n_lines,
                            s0=opts.size0,
                            s1=opts.size1,
                            a0=opts.angle0,
                            a1=opts.angle1,
                        )
                    )
                case "circle_uniform":
                    self.line_types.append(
                        partial(
                            uniform_circle,
                            r0=opts.radius0,
                            r1=opts.radius1,
                            n_lines=opts.n_lines,
                            s0=opts.size0,
                            s1=opts.size1,
                            a0=opts.angle0,
                            a1=opts.angle1,
                        )
                    )
                case "rays_uniform":
                    self.line_types.append(
                        partial(
                            uniform_rays,
                            l0=opts.line_range0,
                            l1=opts.line_range1,
                            n_lines=opts.n_lines,
                            s0=opts.size0,
                            s1=opts.size1,
                            a0=opts.angle0,
                        )
                    )
                case "rays_random":
                    self.line_types.append(
                        partial(
                            random_rays,
                            l0=opts.line_range0,
                            l1=opts.line_range1,
                            n_lines=opts.n_lines,
                            s0=opts.size0,
                            s1=opts.size1,
                            a0=opts.angle0,
                        )
                    )

    def forward(self, data: LQHQState) -> LQHQState:
        h, w = data.hq.shape[:2]
        ndim = data.hq.ndim
        alpha = data.rng.safe_uniform(self.alpha)
        debug(f"  Lines: alpha= {alpha}")
        mask = line(data.rng.choice(self.line_types)(h, w, data.rng), h + 1, w + 1)[
            :h, :w
        ].astype(np.float32)
        if data.lq.shape[0] != h:
            lh, lw = data.lq.shape[:2]
            mask_lq = resize(
                mask,
                lh,
                lw,
                resize_alg=ResizesAlg.Conv(ResizesFilter.Mitchell),
                alpha=False,
            )
        else:
            mask_lq = mask
        if ndim == 3:
            color = self.h2r(data.rng)[None, None, ...]
            mask = mask[:, :, None] * alpha
            mask_lq = mask_lq[:, :, None] * alpha
        else:
            mask = mask * alpha
            mask_lq = mask_lq * alpha
            color = data.rng.safe_uniform(self.v)

        data.hq = (data.hq - mask).clip(0, 1) + (mask * color)
        data.lq = (data.lq - mask_lq).clip(0, 1) + (mask_lq * color)
        return data
