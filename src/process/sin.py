from ..utils import probability
from dataset_support import sin_patern
import random


class SinLossLogic:
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
                - "probably" (float, optional): Probability of applying sinusoidal patterns. Defaults to 1.0.
    """

    def __init__(self, sin_loss_dict):
        self.shape = sin_loss_dict.get("shape", [100, 1000, 100])
        self.alpha = sin_loss_dict.get("alpha", [0.1, 0.5])
        self.bias = sin_loss_dict.get("bias", [0.8, 1.2])
        self.vertical_prob = sin_loss_dict.get("vertical", 0.5)
        self.probably = sin_loss_dict.get("probably", 1.0)

    def run(self, lq, hq):
        """Applies sinusoidal patterns to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the image with sinusoidal patterns applied and the corresponding high-quality image.
        """
        try:
            if probability(self.probably):
                return lq, hq
            shape = random.randrange(*self.shape)
            alpha = random.uniform(*self.alpha)
            vertical = probability(self.vertical_prob)
            bias = random.uniform(*self.bias)
            lq = sin_patern(lq, shape_sin=shape, alpha=alpha, vertical=vertical, bias=bias)
            return lq, hq
        except Exception as e:
            print(f"sin loss error {e}")
