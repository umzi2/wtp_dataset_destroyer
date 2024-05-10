import numpy as np
from numpy import random
from pepeline import fast_color_level
from ..utils import probability


class ColorLossLogic:
    """
    Class for applying color level adjustment to images.

    Args:
        color_loss_dict (dict): A dictionary containing parameters for color level adjustment.
            It should have the following keys:
                - 'high' (list): Range of values for high output level.
                - 'low' (list): Range of values for low output level.
                - 'gamma' (list): Range of values for gamma correction.
                - 'prob' (float, optional): Probability of applying color level adjustment. Default is 1.0.

    Attributes:
        high_list (list): Range of values for high output level.
        low_list (list): Range of values for low output level.
        gamma (list): Range of values for gamma correction.
        probably (float): Probability of applying color level adjustment.

    Methods:
        run(lq, hq): Method to run the color level adjustment process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Image with color level adjustment applied and original high quality image.
    """

    def __init__(self, color_loss_dict):
        self.high_list = color_loss_dict.get("high")
        self.low_list = color_loss_dict.get("low")
        self.gamma = color_loss_dict.get("gamma",[1.0,1.0])
        self.probably = color_loss_dict.get("probably", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            in_low = 0
            in_high = 255
            high_output =255
            low_output =0
            if self.high_list:
                high_output = random.randint(*self.high_list)
            if self.low_list:
                low_output = random.randint(*self.low_list)
            gamma = random.uniform(*self.gamma)
            lq = fast_color_level(lq, in_low=in_low, in_high=in_high, out_low=low_output, out_high=high_output,
                                  gamma=gamma)

            return lq, hq
        except Exception as e:
            print(f"Color loss error:{e}")
