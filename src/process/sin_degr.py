from .utils import probability
from dataset_support import sin_patern
import random
import numpy as np
from ..utils.registry import register_class
from ..utils.random import safe_uniform
import logging


@register_class("sin")
class Sin:
    """Class for applying sinusoidal patterns to images.

    Args:
        sin_loss_dict (dict): A dictionary containing sinusoidal pattern settings.
            It should include the following keys:
                - "shape" (list of int, optional): Range of shape values for the sinusoidal pattern.
                    Defaults to [100, 1000, 100].
                - "alpha" (list of float, optional): Range of alpha values for the sinusoidal pattern.
                    Defaults to [0.1, 0.5].
                - "bias" (list of float, optional): Range of bias values for the sinusoidal pattern.
                    Defaults to [0.8, 1.2].
                - "vertical" (float, optional): Probability of applying vertical sinusoidal patterns.
                    Defaults to 0.5.
                - "probability" (float, optional): Probability of applying sinusoidal patterns. Defaults to 1.0.
    """

    def __init__(self, sin_loss_dict: dict):
        self.shape = sin_loss_dict.get("shape", [100, 1000, 100])
        self.alpha = sin_loss_dict.get("alpha", [0.1, 0.5])
        self.bias = sin_loss_dict.get("bias", [0.8, 1.2])
        self.vertical_prob = sin_loss_dict.get("vertical", 0.5)
        self.probability = sin_loss_dict.get("probability", 1.0)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Applies sinusoidal patterns to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the image with sinusoidal patterns applied and the corresponding high-quality image.
        """
        try:
            if probability(self.probability):
                return lq, hq
            shape = random.randrange(*self.shape)
            alpha = safe_uniform(self.alpha)
            vertical = probability(self.vertical_prob)
            bias = safe_uniform(self.bias)
            logging.debug("Sin - shape: %s alpha: %.4f vertical: %s bias: %.4f", shape, alpha, vertical, bias)
            lq = sin_patern(
                lq, shape_sin=shape, alpha=alpha, vertical=vertical, bias=bias
            )
            return lq, hq
        except Exception as e:
            logging.error("Sin error: %s", e)
