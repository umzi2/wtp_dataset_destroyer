from numpy import random
from pepeline import fast_color_level
from ..utils import probability


class ColorLossLogic:
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

    def __init__(self, color_loss_dict):
        self.high_list = color_loss_dict.get("high")
        self.low_list = color_loss_dict.get("low")
        self.gamma = color_loss_dict.get("gamma", [1.0, 1.0])
        self.probably = color_loss_dict.get("probably", 1.0)

    def run(self, lq, hq):
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
        try:
            if probability(self.probably):
                return lq, hq
            in_low = 0
            in_high = 255
            high_output = 255
            low_output = 0
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
