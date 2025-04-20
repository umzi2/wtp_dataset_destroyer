import numpy as np
from numpy import random
from chainner_ext import resize
from pepeline import fast_color_level
from pepedpid import dpid_resize, cubic_resize
from ..constants import INTERPOLATION_MAP
from .utils import probability
from ..utils.random import safe_uniform, safe_randint, safe_arange
from ..utils.registry import register_class
import logging


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
        spread = resize_dict.get("spread", [1])
        self.spread_arange = safe_arange(spread)

        self.lq_algorithm = resize_dict["alg_lq"]
        self.hq_algorithm = resize_dict["alg_hq"]
        self.lq_scale = resize_dict["scale"]
        down_up = resize_dict.get("down_up")
        up_down = resize_dict.get("up_down")
        down_down = resize_dict.get("down_down")
        if down_up:
            self.down_up_spread = down_up["down"]
            self.down_up_alg_up = down_up["alg_up"]
            self.down_up_alg_down = down_up["alg_down"]
        if up_down:
            self.up_down_spread = up_down["up"]
            self.up_down_alg_up = up_down["alg_up"]
            self.up_down_alg_down = up_down["alg_down"]
        if down_down:
            self.down_down_step = down_down["step"]
            self.down_down_alg = down_down["alg_down"]
        self.probability = resize_dict.get("probability", 1.0)
        self.color_fix = resize_dict.get("color_fix")
        self.gamma_correction = resize_dict.get("gamma_correction", False)

    def __real_size(self, size: int) -> int:
        real_size= size // self.lq_scale * self.lq_scale
        if real_size//self.lq_scale%2 !=0:
            return real_size-self.lq_scale
        return real_size
    def __resize(self,x:np.ndarray, width: int, height: int,algorithm:str):
        if algorithm in INTERPOLATION_MAP.keys():
            x = resize(x,(width,height),INTERPOLATION_MAP[algorithm],self.gamma_correction)
        elif algorithm == "mat_cubic":
            x = cubic_resize(x,height,width)
        else:
            x = dpid_resize(x,height,width,float(algorithm.split("_")[-1]))
        return x
    def __up_down(self, lq: np.ndarray, width: int, height: int) -> np.ndarray:
        up = safe_uniform(self.up_down_spread)
        algorithm_up = random.choice(self.up_down_alg_up)
        logging.debug(f"Resize - up_down up: {up:.4f} algorithm_up: {algorithm_up}")
        lq = self.__resize(
            lq,
            int(width * up),
            int(height * up),
            algorithm_up
        )
        return lq

    def __down_up(self, lq: np.ndarray, width: int, height: int) -> np.ndarray:
        down = safe_uniform(self.down_up_spread)
        algorithm_down = random.choice(self.down_up_alg_down)
        logging.debug(
            f"Resize - down_up down: {down:.4f} algorithm_down: {algorithm_down}"
        )
        lq = self.__resize(
            lq,
            int(width / down),
            int(height / down),
            algorithm_down,
        )
        return lq

    def __down_down(self, lq: np.ndarray, width: int, height: int, algorithm_lq: str):
        height_k = width / height
        step = safe_randint(self.down_down_step)
        step = (width - width / self.lq_scale) / step
        for down in list(
            reversed(np.arange(int(width // self.lq_scale), int(width), int(step)))
        )[:-1]:
            lq = self.__resize(
                lq,
                int(down),
                int(down / height_k),
                algorithm_lq,
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
            logging.debug(
                f"Resize - algorithm_lq: {algorithm_lq} algorithm_hq: {algorithm_hq} spread: {spread:.4f}"
            )
            if algorithm_lq == "down_up":
                lq = self.__down_up(lq, width//self.lq_scale, height//self.lq_scale)
                algorithm_lq = random.choice(self.down_up_alg_up)
                logging.debug(f"Resize - down_up new_algorithm_lq: {algorithm_lq}")
            if algorithm_lq == "up_down":
                lq = self.__up_down(lq, width, height)
                algorithm_lq = random.choice(self.up_down_alg_down)
                logging.debug(f"Resize - up_down new_algorithm_lq: {algorithm_lq}")
            if algorithm_lq == "down_down":
                algorithm_lq = random.choice(self.down_down_alg)
                logging.debug(f"Resize - down_down new_algorithm_lq: {algorithm_lq}")
                lq = self.__down_down(lq, width, height, algorithm_lq)

            lq = self.__resize(
                lq,
                int(width // self.lq_scale),
                int(height // self.lq_scale),
                algorithm_lq
            )
            hq = self.__resize(
                hq,
                int(width),
                int(height),
                algorithm_hq,
            )

            if self.color_fix:
                lq = fast_color_level(lq, 0, 254)
                hq = fast_color_level(hq, 0, 254)
            return lq.squeeze().clip(0,1), hq.squeeze().clip(0,1)
        except Exception as e:
            logging.error("Resize error: %s", e)
