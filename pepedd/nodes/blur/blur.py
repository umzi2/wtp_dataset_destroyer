from functools import partial
from typing import List

import cv2
import numpy as np

from .schemas import BlurOptions
from ..utils.custom_blur.astropy import airy_blur, triangle_blur, ring_blur
from ..utils.custom_blur.box_blur import box_blur
from ..utils.custom_blur.gauss import gauss
from ..utils.custom_blur.lens_blur import lens_blur
from ..utils.custom_blur.motion_blur import motion_blur
from ..utils.custom_blur.rkernel_blur import random_kernel_blur
from pepedd.core.node_register import register_class
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.objects.node_base import Node
from pepedd.core.objects.safe_rng import SafeRNG
from logging import debug


def base_blur(
    img: np.ndarray, rng: SafeRNG, kernel_list: list[float], func
) -> np.ndarray:
    sigma = rng.safe_uniform(kernel_list)
    if sigma == 0:
        return img
    debug(f"   sigma={sigma}\n   kernel_list={kernel_list}\n   func={func.__name__}")
    return func(img, sigma)


def median_blur(img: np.ndarray, kernel_size: float) -> np.ndarray:
    kernel_size = int(np.ceil(kernel_size) * 2 + 1)
    if kernel_size <= 5:
        return cv2.medianBlur(img, kernel_size)
    return (
        cv2.medianBlur((img * 255.0).astype(np.uint8), kernel_size).astype(np.float32)
        / 255.0
    )


def motion(
    img: np.ndarray, rng: SafeRNG, size: List[int], angle: List[float]
) -> np.ndarray:
    size = rng.safe_randint(size)
    angle = rng.safe_uniform(angle)
    debug(f"   size= {size}\n   angle= {angle}\n   func= motion")
    return motion_blur(img, size, angle)


def ring(
    img: np.ndarray, rng: SafeRNG, kernel_size: List[float], thickness: List[int]
) -> np.ndarray:
    kernel_size = rng.safe_uniform(kernel_size)
    thickness = rng.safe_randint(thickness)
    debug(f"   kernel_size= {kernel_size}\n   thickness= {thickness}\n   func= ring")
    return ring_blur(img, kernel_size, thickness)


@register_class("blur")
class Blur(Node):
    def __init__(self, options: BlurOptions | dict):
        if isinstance(options, dict):
            opts = BlurOptions(**options)
        else:
            opts = options
        super().__init__(opts.probability, opts.seed)
        self.blur_list = []
        for blur_filter in opts.filters:
            match blur_filter:
                case "gauss":
                    self.blur_list.append(
                        partial(
                            base_blur, kernel_list=opts.target_kernels.gauss, func=gauss
                        )
                    )
                case "lens":
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.lens,
                            func=lens_blur,
                        )
                    )
                case "random":
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.random,
                            func=random_kernel_blur,
                        )
                    )
                case "median":
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.median,
                            func=median_blur,
                        )
                    )
                case "motion":
                    self.blur_list.append(
                        partial(motion, size=opts.motion_size, angle=opts.motion_angle)
                    )
                #     ,"airy","ring","triangle"
                case "airy":
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.airy,
                            func=airy_blur,
                        )
                    )
                case "triangle":
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.triangle,
                            func=triangle_blur,
                        )
                    )
                case "ring":
                    self.blur_list.append(
                        partial(
                            ring,
                            kernel_size=opts.target_kernels.triangle,
                            thickness=opts.ring_thickness,
                        )
                    )
                case _:
                    self.blur_list.append(
                        partial(
                            base_blur,
                            kernel_list=opts.target_kernels.box,
                            func=box_blur,
                        )
                    )

    def forward(self, data: LQHQState) -> LQHQState:
        debug("blur")
        data.lq = data.rng.choice(self.blur_list)(data.lq, data.rng)
        return data
