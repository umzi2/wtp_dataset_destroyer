from logging import debug

import cv2
import numpy as np

from .schemas import HaloOptions
from ..blur.blur import Blur
from pepedd.core.node_register import register_class
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.objects.node_base import Node


@register_class("halo")
class Halo(Node):
    def __init__(self, options: HaloOptions | dict):
        if isinstance(options, dict):
            opts = HaloOptions(**options)
        else:
            opts = options
        super().__init__(opts.probability, opts.seed)
        self.blur = Blur(opts.blur)
        self.amount = opts.amount
        self.threshold = opts.threshold
        self.halo_types = []
        for alg in opts.type_halo:
            if alg == "y":
                self.halo_types.append(self.y_halo)
            else:
                self.halo_types.append(self.rgb_halo)

    def y_halo(self, img: LQHQState) -> LQHQState:
        img_ndim = img.lq.ndim
        debug("  gray_mode")
        if img_ndim == 3:
            lq = cv2.cvtColor(img.lq, cv2.COLOR_RGB2YCrCb)
            img.lq = lq[:, :, 0]
            img = self.rgb_halo(img)
            lq[:, :, 0] = img.lq
            img.lq = cv2.cvtColor(lq, cv2.COLOR_YCrCb2RGB)
        else:
            img = self.rgb_halo(img)
        return img

    def rgb_halo(self, img: LQHQState) -> LQHQState:
        w_o_blur = img.lq
        threshold = img.rng.safe_uniform(self.threshold)
        amount = img.rng.safe_uniform(self.amount)
        debug(f"   amount={amount}\n   threshold={threshold}\nHalo Blur:")
        img = self.blur(img)

        diff = w_o_blur - img.lq

        diff = np.sign(diff) * np.maximum(0, np.abs(diff) - threshold)
        img.lq = img.lq + diff * amount
        return img

    def forward(self, img: LQHQState) -> LQHQState:
        debug("halo")
        return img.rng.choice(self.halo_types)(img)
