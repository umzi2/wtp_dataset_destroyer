import cv2 as cv
from numpy import random
from ..utils import probability


class SaturationLossLogic:
    """
    Class for applying saturation loss to images.

    Args:
        saturation_dict (dict): A dictionary containing parameters for saturation loss.
            It should have the following keys:
                - 'rand' (list, optional): Range of random values for saturation adjustment. Default is [0.5, 1.0].
                - 'prob' (float, optional): Probability of applying saturation loss. Default is 1.0.

    Attributes:
        rand (list): Range of random values for saturation adjustment.
        probably (float): Probability of applying saturation loss.

    Methods:
        run(lq, hq): Method to run the saturation loss process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Image with adjusted saturation and original high quality image.
    """

    def __init__(self, saturation_dict):
        self.rand = saturation_dict.get("rand", [0.5, 1.0])
        self.probably = saturation_dict.get("probably", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            random_saturation = random.uniform(*self.rand)
            hsv_image = cv.cvtColor(lq, cv.COLOR_RGB2HSV)
            decreased_saturation = hsv_image.copy()
            decreased_saturation[:, :, 1] = decreased_saturation[:, :, 1] * random_saturation
            return cv.cvtColor(decreased_saturation, cv.COLOR_HSV2RGB), hq
        except Exception as e:
            print(f"Saturation loss error {e}")
