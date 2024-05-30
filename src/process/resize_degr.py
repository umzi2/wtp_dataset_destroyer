import numpy as np
from numpy import random
from chainner_ext import resize
from pepeline import fast_color_level
from ..constants import INTERPOLATION_MAP
from .utils import probability
from ..utils.random import safe_uniform, safe_randint, safe_arange

from ..utils.registry import register_class
import picologging as logging


@register_class("resize")
class Resize:
    """
    Class for resizing images.

    Args:
        resize_dict (dict): A dictionary containing parameters for resizing images.
            It should have the following keys:
                - 'spread' (list, optional): Range of spread values. Default is [1, 1, 1].
                - 'alg_lq' (list): List of algorithms for low quality image resizing.
                - 'alg_hq' (list): List of algorithms for high quality image resizing.
                - 'scale' (int): Scaling factor for low quality image resizing.
                - 'down_up' (dict, optional): Dictionary specifying parameters for down-up resizing. Default is None.
                - 'down_down' (dict, optional): Dictionary specifying parameters for down-down resizing. Default is None.
                - 'prob' (float, optional): Probability of applying resizing. Default is 1.0.
                - 'color_fix' (bool, optional): Whether to perform color fixing after resizing. Default is None.
                - 'gamma_correction' (bool, optional): Whether to perform gamma correction after resizing. Default is False.
                - 'olq' (bool, optional): Whether to resize only the low quality image. Default is None.

    Attributes:
        spread_arange (numpy.ndarray): Range of spread values.
        lq_algorithm (list): List of algorithms for low quality image resizing.
        hq_algorithm (list): List of algorithms for high quality image resizing.
        lq_scale (int): Scaling factor for low quality image resizing.
        down_up_spread (list): Spread values for down-up resizing.
        down_up_alg_up (list): List of algorithms for upscaling in down-up resizing.
        down_up_alg_down (list): List of algorithms for downscaling in down-up resizing.
        down_down_step (int): Step value for down-down resizing.
        down_down_alg (list): List of algorithms for downscaling in down-down resizing.
        probability (float): Probability of applying resizing.
        color_fix (bool): Whether to perform color fixing after resizing.
        gamma_correction (bool): Whether to perform gamma correction after resizing.

    """

    def __init__(self, resize_dict: dict):
        spread = resize_dict.get("spread", [1, 1, 1])
        self.spread_arange = safe_arange(spread)

        self.lq_algorithm = resize_dict["alg_lq"]
        self.hq_algorithm = resize_dict["alg_hq"]
        self.lq_scale = resize_dict["scale"]
        down_up = resize_dict.get("down_up")
        down_down = resize_dict.get("down_down")
        if down_up:
            self.down_up_spread = down_up["up"]
            self.down_up_alg_up = down_up["alg_up"]
            self.down_up_alg_down = down_up["alg_down"]
        if down_down:
            self.down_down_step = down_down["step"]
            self.down_down_alg = down_down["alg_down"]
        self.probability = resize_dict.get("probability", 1.0)
        self.color_fix = resize_dict.get("color_fix")
        self.gamma_correction = resize_dict.get("gamma_correction", False)

    def __real_size(self, size: int) -> int:
        return size - (size % (size // self.lq_scale * self.lq_scale))

    def __down_up(self, lq: np.ndarray, width: int, height: int) -> np.ndarray:
        up = safe_uniform(self.down_up_spread)
        algorithm_up = random.choice(self.down_up_alg_up)
        lq = resize(
            lq,
            (int(width * up), int(height * up)),
            INTERPOLATION_MAP[algorithm_up],
            gamma_correction=self.gamma_correction,
        )
        return lq

    def __down_down(self, lq: np.ndarray, width: int, height: int, algorithm_lq: str):
        height_k = width / height
        step = safe_randint(self.down_down_step)
        step = (width - width / self.lq_scale) / step
        for down in list(
                reversed(np.arange(int(width // self.lq_scale), int(width), int(step)))
        )[:-1]:
            lq = resize(
                lq,
                (int(down), int(down / height_k)),
                INTERPOLATION_MAP[algorithm_lq],
                gamma_correction=self.gamma_correction,
            )
        return lq

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Args:
            lq (numpy.ndarray): Low quality image.
            hq (numpy.ndarray): High quality image.
        Returns:
            Tuple of numpy.ndarrays: Resized low quality image and high quality image.
        """
        try:
            if probability(self.probability):
                return lq, hq
            height, width = lq.shape[:2]
            algorithm_lq = random.choice(self.lq_algorithm)
            algorithm_hq = random.choice(self.hq_algorithm)
            spread = random.choice(self.spread_arange)
            height = self.__real_size(height // spread)
            width = self.__real_size(width // spread)
            logging.debug("Resize - algorithm_lq: %s algorithm_hq: %s spread: %.3f", algorithm_lq, algorithm_hq, spread)
            if algorithm_lq == "down_up":
                lq = self.__down_up(lq, width, height)
                algorithm_lq = random.choice(self.down_up_alg_down)
            if algorithm_lq == "down_down":
                algorithm_lq = random.choice(self.down_down_alg)
                lq = self.__down_down(lq, width, height, algorithm_lq)

            lq = resize(
                lq,
                (int(width // self.lq_scale), int(height // self.lq_scale)),
                INTERPOLATION_MAP[algorithm_lq],
                gamma_correction=self.gamma_correction,
            )
            hq = resize(
                hq,
                (int(width), int(height)),
                INTERPOLATION_MAP[algorithm_hq],
                gamma_correction=self.gamma_correction,
            )

            if self.color_fix:
                lq = fast_color_level(lq, 0, 250)
                hq = fast_color_level(hq, 0, 250)
            return lq.squeeze(), hq.squeeze()
        except Exception as e:
            logging.error("Resize error: %s", e)
