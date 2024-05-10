from ..utils import probability
from dataset_support import sin_patern
import random


class SinLossLogic:
    """
    Class for applying sinusoidal pattern loss to images.

    Args:
        sin_loss_dict (dict): A dictionary containing parameters for sinusoidal pattern loss.
            It should have the following keys:
                - 'shape' (tuple): Range of values for shape parameter of sinusoidal pattern.
                - 'alpha' (tuple): Range of values for alpha parameter of sinusoidal pattern.
                - 'bias' (tuple): Range of values for bias parameter of sinusoidal pattern.
                - 'vertical' (float): Probability of applying vertical sinusoidal pattern.
                - 'prob' (float, optional): Probability of applying sinusoidal pattern loss. Default is 1.0.

    Attributes:
        shape (tuple): Range of values for shape parameter of sinusoidal pattern.
        alpha (tuple): Range of values for alpha parameter of sinusoidal pattern.
        bias (tuple): Range of values for bias parameter of sinusoidal pattern.
        vertical_prob (float): Probability of applying vertical sinusoidal pattern.
        probably (float): Probability of applying sinusoidal pattern loss.

    Methods:
        run(lq, hq): Method to run the sinusoidal pattern loss process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Image with sinusoidal pattern loss applied and original high quality image.
    """

    def __init__(self, sin_loss_dict):
        self.shape = sin_loss_dict.get("shape", [100, 1000, 100])
        self.alpha = sin_loss_dict.get("alpha", [0.1, 0.5])
        self.bias = sin_loss_dict.get("bias", [0.8, 1.2])
        self.vertical_prob = sin_loss_dict.get("vertical", 0.5)
        self.probably = sin_loss_dict.get("probably", 1.0)

    def run(self, lq, hq):
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
