import numpy as np
from chainner_ext import (
    UniformQuantization as UQ,
    quantize,
    error_diffusion_dither,
    ordered_dither,
    riemersma_dither,
)
from ..constants import DITHERING_MAP
from .utils import probability
from numpy import random
from ..utils.registry import register_class
from ..utils.random import safe_uniform, safe_randint
import logging


@register_class("dithering")
class Dithering:
    """Class for applying dithering algorithms to images.

    Args:
        dithering_dict (dict): A dictionary containing dithering settings.
            It should include the following keys:
                - "dithering_type" (list of str, optional): List of dithering algorithms to be used.
                    Defaults to ["quantize"].
                - "color_ch" (list of int, optional): Range of color channels for quantization.
                    Defaults to [2, 10].
                - "map_size" (list of int, optional): Range of map sizes for ordered dithering.
                    Defaults to [4, 8].
                - "history" (list of int, optional): Range of history values for Riemersma dithering.
                    Defaults to [10, 15].
                - "ratio" (list of float, optional): Range of decay ratio values for Riemersma dithering.
                    Defaults to [0.1, 0.9].
                - "probability" (float, optional): Probability of applying dithering. Defaults to 1.0.
    """

    def __init__(self, dithering_dict: dict):
        self.dithering_type_list = dithering_dict.get("dithering_type", ["quantize"])
        self.quantize = dithering_dict.get("color_ch", [2, 10])
        self.map_size = dithering_dict.get("map_size", [4, 8])
        self.history = dithering_dict.get("history", [10, 15])
        self.ratio = dithering_dict.get("ratio", [0.1, 0.9])
        self.probability = dithering_dict.get("probability", 1.0)
        self.dithering_type = "Burkes"
        self.unif_quantiz = 8

    def __error(self, lq: np.ndarray, quantization: UQ) -> np.ndarray:
        logging.debug("Dithering - type: %s quantization %s", self.dithering_type,
                      self.unif_quantiz)
        return error_diffusion_dither(
            lq, quantization, DITHERING_MAP[self.dithering_type]
        )

    def __quantize(self, lq: np.ndarray, quantization: UQ) -> np.ndarray:
        return quantize(lq, quantization)

    def __order(self, lq: np.ndarray, quantization: UQ) -> np.ndarray:
        map_size = random.choice(self.map_size)
        logging.debug("Dithering - type: %s map_size: %s quantization %s", self.dithering_type, map_size,
                      self.unif_quantiz)
        return ordered_dither(lq, quantization, map_size)

    def __riemersma(self, lq: np.ndarray, quantization: UQ) -> np.ndarray:
        history = safe_randint(self.history)
        decay_ratio = safe_uniform(self.ratio)
        logging.debug("Dithering - type: %s history: %s decay_ratio: %.4f quantization %s", self.dithering_type, history, decay_ratio,
                      self.unif_quantiz)
        return riemersma_dither(lq, quantization, history, decay_ratio)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Applies the selected dithering algorithm to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the dithered low-quality image and the corresponding high-quality image.
        """
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
            "quantize": self.__quantize,
        }
        try:
            if probability(self.probability):
                return lq, hq
            self.dithering_type = random.choice(self.dithering_type_list)
            self.unif_quantiz = safe_randint(self.quantize)
            lq = DITHERING_TYPE_MAP[self.dithering_type](lq, UQ(self.unif_quantiz))
            return np.squeeze(lq), hq
        except Exception as e:
            logging.error("Dithering error: %s", e)
