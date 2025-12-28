from functools import partial
from typing import List

import cv2
import numpy as np
from logging import debug

from pepedd.core.node_register import register_class
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.objects.node_base import Node
from pepedd.core.objects.safe_rng import SafeRNG
from ...nodes.dithering.quantizer import PaletteAndUniform
from ...nodes.dithering.schemas import DitheringOptions
from chainner_ext import (
    DiffusionAlgorithm,
    error_diffusion_dither,
    quantize,
    ordered_dither,
    riemersma_dither,
)


def quantize_warp(img: np.ndarray, _rng, qc):
    return quantize(img, qc)


def error_warp(img: np.ndarray, _rng, qc, da: DiffusionAlgorithm):
    debug(f"      {da.__repr__()}")
    return error_diffusion_dither(img, qc, da)


def order_warp(img: np.ndarray, rng, qc, order: List[int]):
    order = rng.choice(order)
    debug(f"      order_dither: order={order}")
    return ordered_dither(img, qc, order)


def riemersma_warp(
    img: np.ndarray,
    rng: SafeRNG,
    qc,
    history: List[int],
    ratio: List[float],
):
    ratio = rng.safe_uniform(ratio)
    history = rng.safe_randint(history)
    debug(f"      riemersma_dither: ratio={ratio} history= {history}")
    return riemersma_dither(img, qc, history, ratio)


def base_dither(
    img: np.ndarray, rng: SafeRNG, palette: PaletteAndUniform, func
) -> np.ndarray:
    return func(img, rng, palette(img, rng)).squeeze()


@register_class("dithering")
class Dithering(Node):
    def __init__(self, options: DitheringOptions | dict):
        if isinstance(options, dict):
            opts = DitheringOptions(**options)
        else:
            opts = options
        super().__init__(opts.probability, opts.seed)
        self.dithers = []
        for dither in opts.types:
            match dither:
                case "floydsteinberg":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.floydsteinberg
                            ),
                            func=partial(
                                error_warp, da=DiffusionAlgorithm.FloydSteinberg
                            ),
                        )
                    )
                case "jarvisjudiceninke":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.jarvisjudiceninke
                            ),
                            func=partial(
                                error_warp, da=DiffusionAlgorithm.JarvisJudiceNinke
                            ),
                        )
                    )
                case "stucki":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.stucki
                            ),
                            func=partial(error_warp, da=DiffusionAlgorithm.Stucki),
                        )
                    )
                case "atkinson":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.atkinson
                            ),
                            func=partial(error_warp, da=DiffusionAlgorithm.Atkinson),
                        )
                    )
                case "burkes":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.burkes
                            ),
                            func=partial(error_warp, da=DiffusionAlgorithm.Burkes),
                        )
                    )
                case "sierra":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.sierra
                            ),
                            func=partial(error_warp, da=DiffusionAlgorithm.Sierra),
                        )
                    )
                case "tworowsierra":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.tworowsierra
                            ),
                            func=partial(
                                error_warp, da=DiffusionAlgorithm.TwoRowSierra
                            ),
                        )
                    )
                case "sierraLite":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.sierraLite
                            ),
                            func=partial(error_warp, da=DiffusionAlgorithm.SierraLite),
                        )
                    )
                case "order":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                ["uniform"], opts.target_color.order
                            ),
                            func=partial(order_warp, order=opts.map_size),
                        )
                    )
                case "riemersma":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.riemersma
                            ),
                            func=partial(
                                riemersma_warp, history=opts.history, ratio=opts.ratio
                            ),
                        )
                    )
                case "quantize":
                    self.dithers.append(
                        partial(
                            base_dither,
                            palette=PaletteAndUniform(
                                opts.palette, opts.target_color.quantize
                            ),
                            func=quantize_warp,
                        )
                    )

    def forward(self, data: LQHQState) -> LQHQState:
        debug("  Dithering")
        img_ndim = data.lq.ndim
        if img_ndim == 2:
            data.lq = cv2.cvtColor(data.lq, cv2.COLOR_GRAY2RGB)
        data.lq = data.rng.choice(self.dithers)(data.lq, data.rng)
        if img_ndim == 2:
            data.lq = data.lq[..., 0]
        return data
