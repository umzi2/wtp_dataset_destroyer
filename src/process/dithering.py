import numpy as np
from chainner_ext import UniformQuantization as UQ, quantize, error_diffusion_dither, ordered_dither, \
    riemersma_dither
from ..constants import DITHERING_MAP
from ..utils import probability
from numpy import random




class Dithering:
    def __init__(self, dithering_dict):
        self.dithering_type_list = dithering_dict.get("dithering_type", ["quantize"])
        self.quantize = dithering_dict.get("color_ch", [2, 10])
        self.map_size = dithering_dict.get("map_size", [4, 8])
        self.history = dithering_dict.get("history", [10, 15])
        self.ratio = dithering_dict.get("ratio", [0.1, 0.9])
        self.probably = dithering_dict.get("probably", 1.0)
        self.dithering_type = "Burkes"

    def __error(self, lq, quantization):
        return error_diffusion_dither(lq, quantization, DITHERING_MAP[self.dithering_type])

    def __quantize(self, lq, quantization):
        return quantize(lq, quantization)

    def __order(self, lq, quantization):
        map_size = random.choice(self.map_size)
        return ordered_dither(lq, quantization, map_size)

    def __riemersma(self, lq, quantization):
        history = random.randint(*self.history)
        decay_ratio = random.uniform(self.ratio[0], self.ratio[1])
        return riemersma_dither(lq, quantization, history, decay_ratio)

    def run(self, lq, hq):
        DITHERING_TYPE_MAP = {
            "floydsteinberg": self.__error,
            "jarvisjudiceninke": self.__error,
            "stucki": self.__error,
            "atkinson": self.__error,
            "burkes": self.__error,
            "sierra": self.__error,
            "tworowsierra": self.__error,
            "sierraLite": self.__error,
            "order": self.__order,
            "riemersma": self.__riemersma,
            "quantize": self.__quantize
        }
        try:
            if probability(self.probably):
                return lq, hq
            self.dithering_type = random.choice(self.dithering_type_list)
            unif_quantiz = random.randint(*self.quantize)
            lq = DITHERING_TYPE_MAP[self.dithering_type](lq, UQ(unif_quantiz))
            return np.squeeze(lq), hq
        except Exception as e:
            print(f"dithering error: {e}")
