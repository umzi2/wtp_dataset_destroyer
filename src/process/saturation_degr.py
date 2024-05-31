import cv2 as cv
import numpy as np
from .utils import probability
from ..utils.random import safe_uniform
from ..utils.registry import register_class
import logging


@register_class("saturation")
class Saturation:
    """
    Class for applying saturation loss to images.

    Args:
        saturation_dict (dict): A dictionary containing parameters for saturation loss.
            It should have the following keys:
                - 'rand' (list, optional): Range of random values for saturation adjustment. Default is [0.5, 1.0].
                - 'prob' (float, optional): Probability of applying saturation loss. Default is 1.0.

    Attributes:
        rand (list): Range of random values for saturation adjustment.
        probability (float): Probability of applying saturation loss.

    """

    def __init__(self, saturation_dict: dict):
        self.rand = saturation_dict.get("rand", [0.5, 1.0])
        self.probability = saturation_dict.get("probability", 1.0)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Args:
            lq (numpy.ndarray): Low quality image.
            hq (numpy.ndarray): High quality image.
        Returns:
            Tuple of numpy.ndarrays: Image with adjusted saturation and original high quality image.
        """
        try:
            if lq.ndim == 2:
                return lq, hq
            if probability(self.probability):
                return lq, hq
            random_saturation = safe_uniform(self.rand)
            logging.debug("Saturation - %.4f", random_saturation)
            hsv_image = cv.cvtColor(lq, cv.COLOR_RGB2HSV)
            decreased_saturation = hsv_image.copy()
            decreased_saturation[:, :, 1] = (
                    decreased_saturation[:, :, 1] * random_saturation
            )
            return cv.cvtColor(decreased_saturation, cv.COLOR_HSV2RGB), hq
        except Exception as e:
            logging.error("Saturation error: %s", e)
