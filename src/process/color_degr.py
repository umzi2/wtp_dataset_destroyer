from pepeline import fast_color_level
from .utils import probability
import numpy as np
from ..utils.registry import register_class
from ..utils.random import safe_uniform, safe_randint


@register_class("color")
class Color:
    """Class for adjusting color levels of images.

    Args:
        color_loss_dict (dict): A dictionary containing color loss adjustment settings.
            It should include the following keys:
                - "high" (list of int, optional): Range of high output values.
                    Defaults to None.
                - "low" (list of int, optional): Range of low output values.
                    Defaults to None.
                - "gamma" (list of float, optional): Range of gamma values for gamma correction.
                    Defaults to [1.0, 1.0].
                - "probably" (float, optional): Probability of applying color loss adjustments.
                    Defaults to 1.0.
    """

    def __init__(self, color_loss_dict: dict):
        self.high_list = color_loss_dict.get("high", [255, 255])
        self.low_list = color_loss_dict.get("low", [0, 0])
        self.gamma = color_loss_dict.get("gamma", [1.0, 1.0])
        self.probability = color_loss_dict.get("probability", 1.0)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Changes levels to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the noisy low-quality image and the corresponding high-quality image.
        """
        try:
            if probability(self.probability):
                return lq, hq
            in_low = 0
            in_high = 255
            high_output = safe_randint(self.high_list)
            low_output = safe_randint(self.low_list)
            gamma = safe_uniform(self.gamma)
            lq = fast_color_level(
                lq,
                in_low=in_low,
                in_high=in_high,
                out_low=low_output,
                out_high=high_output,
                gamma=gamma,
            )

            return lq, hq
        except Exception as e:
            print(f"Color loss error:{e}")
