from functools import partial
from typing import List

import numpy as np

from .schemas import ResizeOptions, DownUpOptions, DownDownOptions, UpDownOptions
from ..utils.constants import RESIZE_ALG_MAP, RESIZE_FILTER_MAP
from ..utils.custom_random import safe_arange
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.node_register import register_class
from pepedd.core.objects.node_base import Node
from logging import debug
from pepeline import resize, ResizesAlg, ResizesFilter
from pepedpid import dpid_resize

from pepedd.core.objects.safe_rng import SafeRNG


def adjust_number(
    original_num: int, divider: int, second_num_divisor: int
) -> tuple[int, int]:
    second_num = original_num // divider
    adjusted_second_num = second_num - (second_num % second_num_divisor)
    new_original_num = adjusted_second_num * divider
    return new_original_num, adjusted_second_num


def st_resize(
    img: np.ndarray, h: int, w: int, _rng: SafeRNG, resize_alg: ResizesAlg, _filter: str
):
    oh, ow = img.shape[:2]
    if oh == h and ow == w:
        return img
    debug(
        f"    Resize alg= {resize_alg.__class__.__name__}\n    filter= {_filter}\n    ih= {oh} iw={ow}\n    oh= {h} ow={w}"
    )
    return resize(img, h, w, resize_alg=resize_alg, alpha=False)


def sts_resize(
    img: np.ndarray,
    h: int,
    w: int,
    rng: SafeRNG,
    resize_filter: ResizesFilter,
    ss: List[int],
):
    oh, ow = img.shape[:2]
    if oh == h and ow == w:
        return img
    ss = rng.safe_randint(ss)
    debug(
        f"    Resize alg= ResizeAlg_SuperSampling\n    filter = {repr(resize_filter)}\n    sampling= {ss}    ih= {oh} iw={ow}\n    oh= {h} ow={w}"
    )
    return resize(
        img,
        h,
        w,
        resize_alg=ResizesAlg.SuperSampling(resize_filter, rng.safe_randint(ss)),
        alpha=True,
    )


def d_resize(img, h, w, _rng: SafeRNG, lamda: float):
    oh, ow = img.shape[:2]
    if oh == h and ow == w:
        return img
    debug(
        f"    Resize alg= Dpid\n    lamda= {lamda}\n    ih= {oh} iw={ow}\n    oh= {h} ow={w}"
    )
    return dpid_resize(img, h, w, lamda)


def down_up_resize(
    img: np.ndarray, h: int, w: int, rng: SafeRNG, down_algs, up_algs, scale: List[int]
):
    scale = rng.safe_randint(scale)
    debug(f"   Method= down_up\n   stage= down\n   down= {scale}")
    img = rng.choice(down_algs)(img, h // scale, w // scale, rng)
    debug(f"   Method= down_up\n   stage= up\n   scale= {scale}")
    return rng.choice(up_algs)(img, h, w, rng)


def down_down_resize(
    img: np.ndarray,
    h: int,
    w: int,
    rng: SafeRNG,
    down_algs,
    step: List[int],
):
    step = rng.safe_randint(step)
    oh, ow = img.shape[:2]
    if oh == h and ow == w:
        return img
    down_alg = rng.choice(down_algs)
    if step < 2:
        return down_alg(img, h, w, rng)

    h_steps = np.linspace(oh, h, step)
    w_steps = np.linspace(ow, w, step)
    debug(f"   Method= down_down\n   step= {step}")
    for index in range(step):
        img = down_alg(img, int(h_steps[index]), int(w_steps[index]), rng)
    return img


def up_down_resize(
    img: np.ndarray, h: int, w: int, rng: SafeRNG, down_algs, up_algs, scale: List[int]
):
    scale = rng.safe_randint(scale)
    if scale < 2:
        return rng.choice(down_algs)(img, h, w, rng)
    oh, ow = img.shape[:2]
    debug(f"   Method= up_down\n   stage= up\n   up= {scale}")
    img = rng.choice(up_algs)(img, oh * scale, ow * scale, rng)
    debug(f"   Method= up_down\n   stage= down\n   down= {scale}")
    return rng.choice(down_algs)(img, h, w, rng)


def get_resize(
    name: str,
    ss: List[int],
    down_up: DownUpOptions,
    down_down: DownDownOptions,
    up_down: UpDownOptions,
):
    if name == "down_up":
        alg_up = []
        alg_down = []
        for alg in set(down_up.alg_up) - {"down_up"}:
            alg_up.append(get_resize(alg, ss, down_up, down_down, up_down))
        for alg in set(down_up.alg_down) - {"down_up"}:
            alg_down.append(get_resize(alg, ss, down_up, down_down, up_down))
        return partial(
            down_up_resize, down_algs=alg_down, up_algs=alg_up, scale=down_up.down
        )
    elif name == "down_down":
        alg_down = []
        for alg in set(down_up.alg_down) - {"down_down"}:
            alg_down.append(get_resize(alg, ss, down_up, down_down, up_down))
        return partial(down_down_resize, down_algs=alg_down, step=down_down.step)
    elif name == "up_down":
        alg_up = []
        alg_down = []
        for alg in set(up_down.alg_up) - {"up_down"}:
            alg_up.append(get_resize(alg, ss, down_up, down_down, up_down))
        for alg in set(up_down.alg_down) - {"up_down"}:
            alg_down.append(get_resize(alg, ss, down_up, down_down, up_down))
        return partial(
            up_down_resize, down_algs=alg_down, up_algs=alg_up, scale=up_down.up
        )

    prefix = name[0]
    if prefix == "d":
        return partial(d_resize, lamda=float(name.split("_")[-1]))
    elif prefix == "s":
        return partial(
            sts_resize, ss=ss, resize_filter=RESIZE_FILTER_MAP[name.split("_")[-1]]
        )
    elif prefix == "n":
        return partial(st_resize, resize_alg=ResizesAlg.Nearest(), _filter="nearest")
    else:
        alg = RESIZE_ALG_MAP[prefix]
        return partial(
            st_resize,
            resize_alg=alg(RESIZE_FILTER_MAP[name.split("_")[-1]]),
            _filter=name.split("_")[-1],
        )


@register_class("resize")
class Resize(Node):
    def __init__(self, options: ResizeOptions | dict):
        if isinstance(options, dict):
            opts = ResizeOptions(**options)
        else:
            opts = options
        self.resizes_lq = []
        self.resizes_hq = []
        for alg in set(opts.alg_lq):
            self.resizes_lq.append(
                get_resize(
                    alg, opts.s_samplings, opts.down_up, opts.down_down, opts.up_down
                )
            )
        for alg in set(opts.alg_hq):
            self.resizes_hq.append(
                get_resize(
                    alg, opts.s_samplings, opts.down_up, opts.down_down, opts.up_down
                )
            )
        self.scale = opts.scale
        self.divider = opts.divider
        self.olq = opts.olq
        self.spread = safe_arange(opts.spread)
        super().__init__(opts.probability, opts.seed)

    def forward(self, state: LQHQState) -> LQHQState:
        debug("Resize:")
        hq_h, hq_w = state.hq.shape[:2]
        spread = state.rng.choice(self.spread)

        rhq_h, rlq_h = adjust_number(int(hq_h * spread), self.scale, self.divider)
        rhq_w, rlq_w = adjust_number(int(hq_w * spread), self.scale, self.divider)
        if not self.olq:
            debug("  Hq:")
            state.hq = state.rng.choice(self.resizes_hq)(
                state.hq, rhq_h, rhq_w, state.rng
            )
        debug("  Lq:")
        state.lq = state.rng.choice(self.resizes_lq)(state.lq, rlq_h, rlq_w, state.rng)
        return state
