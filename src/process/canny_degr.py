from .utils import probability
import numpy as np
from ..utils.registry import register_class
from ..utils.random import safe_arange
import logging
import cv2


@register_class("canny")
class Canny:
    """
    Class for applying Canny edge detection to images with optional probability-based modifications.

    Args:
        canny_loss_dict (dict): A dictionary containing configuration settings for the Canny edge detection.
            It should include the following keys:
                - "thread1" (list of int, optional): List of possible values for the first threshold of Canny edge detection.
                  Defaults to [10, 10, 1].
                - "thread2" (list of int, optional): List of possible values for the second threshold of Canny edge detection.
                  Defaults to [0, 10, 1].
                - "aperture_size" (list of int, optional): List of possible values for the aperture size of the Sobel operator.
                  Defaults to [3, 5].
                - "white" (float, optional): Probability of replacing detected edges with a white background. Defaults to 0.0.
                - "probability" (float, optional): Probability of applying the Canny edge detection. Defaults to 1.0.
                - "lq_hq" (bool, optional): If True, use the processed low-quality image as the high-quality image. Defaults to False.
    """

    def __init__(self, canny_loss_dict: dict):
        thread1_list = canny_loss_dict.get("thread1", [10, 10, 1])
        self.thread1_list = safe_arange(thread1_list)
        thread2_list = canny_loss_dict.get("thread2", [0, 10, 1])
        self.thread2_list = safe_arange(thread2_list)
        self.aperture_size = canny_loss_dict.get("aperture_size", [3, 5])
        self.white = canny_loss_dict.get("white", 0.0)
        self.probability = canny_loss_dict.get("probability", 1.0)
        self.scale = canny_loss_dict.get("scale")
        self.lq_hq = canny_loss_dict.get("lq_hq", False)

    def black_scale(self, img, scale):
        if scale == 0:
            return img
        kernel = np.ones([int(np.round(scale)),int(np.round(scale))])#create_linse_kernel(np.round(scale),False)
        dilated_image = cv2.dilate(1-img, kernel.astype(np.uint8)).clip(0,1)
        return 1-dilated_image

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Applies the Canny edge detection algorithm to the low-quality image, with optional white background replacement.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The high-quality image.

        Returns:
            tuple: A tuple containing the processed low-quality image and the corresponding high-quality image.
        """
        try:
            if probability(self.probability):
                return lq, hq
            thread1 = np.random.choice(self.thread1_list)
            thread2 = thread1 + np.random.choice(self.thread2_list)
            aperture_size = np.random.choice(self.aperture_size)
            if lq.ndim == 3:
                gray = cv2.cvtColor(lq, cv2.COLOR_RGB2GRAY)
            else:
                gray = lq
            lq_masc = (
                1
                - cv2.Canny(
                    (gray * 255).astype(np.uint8),
                    thread1,
                    thread2,
                    apertureSize=aperture_size,
                    L2gradient=True,
                )
                // 255
            )
            if self.scale:
                lq_masc = self.black_scale(
                    lq_masc, np.random.choice(safe_arange(self.scale))
                )
            white = not probability(self.white)
            if lq.ndim == 3:
                lq = np.where(cv2.cvtColor(lq_masc, cv2.COLOR_GRAY2RGB), lq, white)
            else:
                lq = np.where(lq_masc, lq, white)
            logging.debug(
                f"Canny - thread1: {thread1} thread2: {thread2} aperture_size: {aperture_size} white: {bool(white)}",
            )
            if self.lq_hq:
                hq = lq
            return lq, hq
        except Exception as e:
            logging.error(f"Canny error: {e}")
