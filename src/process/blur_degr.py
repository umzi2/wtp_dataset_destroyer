from numpy import random
import numpy as np

from .custom_blur.rkernel_blur import random_kernel_blur
from .utils import probability
import cv2 as cv
from ..utils.random import safe_uniform, safe_randint

from ..utils.registry import register_class
from .custom_blur import motion_blur, lens_blur, box_blur
import logging


@register_class("blur")
class Blur:
    """Class for applying blur effects to images.

    Args:
        blur_dict (dict): A dictionary containing blur settings.
            It should include the following keys:
                - "filter" (list of str): List of blur filter types to choose from.
                - "kernel" (list of int, optional): Range of kernel sizes for the blur filters.
                    Defaults to [0, 1, 1].
                - "probability" (float, optional): Probability of applying blur effects. Defaults to 1.0.
                - "target_kernel" (dict, optional): Dictionary containing target kernel ranges for specific blur filters.
                    Defaults to None.
    """

    def __init__(self, blur_dict: dict):
        self.filter = blur_dict["filter"]
        kernel = blur_dict.get("kernel", [0, 1])

        # motion
        self.size = blur_dict.get("motion_size", [1, 2])
        self.angle = blur_dict.get("motion_angle", [0, 1])

        self.probability = blur_dict.get("probability", 1.0)
        target = blur_dict.get("target_kernel")
        if target:
            gauss = target.get("gauss", kernel)
            box = target.get("box", kernel)
            median = target.get("median", kernel)
            lens = target.get("lens", kernel)
            random_kernel = target.get("random", kernel)
            self.kernels = {
                "gauss": gauss,
                "box": box,
                "median": median,
                "lens": lens,
                "random": random_kernel,
            }
        else:
            self.kernels = {
                "gauss": kernel,
                "box": kernel,
                "median": kernel,
                "lens": kernel,
                "random": kernel,
            }
        self.kernel = 0

    @staticmethod
    def __kernel_odd(kernel_size: int) -> int:
        if kernel_size % 2 == 0:
            kernel_size += 1
        return kernel_size

    def __gauss(self, lq: np.ndarray) -> np.ndarray:
        sigma = safe_uniform(self.kernels["gauss"])
        if sigma <= 0.0:
            return lq
        logging.debug(f"Blur - type: lens kernel: {sigma:.4f}", sigma)
        return cv.GaussianBlur(
            lq, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
        )

    def __box(self, lq: np.ndarray) -> np.ndarray:
        kernel = safe_uniform(self.kernels["box"])
        if kernel <= 0.0:
            return lq
        logging.debug(f"Blur - type: lens kernel: {kernel:.4f}", kernel)
        return box_blur(lq, kernel)

    def __lens(self, lq: np.ndarray) -> np.ndarray:
        kernel = safe_uniform(self.kernels["lens"])
        if kernel <= 0.0:
            return lq
        logging.debug(f"Blur - type: lens kernel: {kernel:.4f}", kernel)
        return lens_blur(lq, kernel)

    def __motion(self, lq: np.ndarray) -> np.ndarray:
        size = safe_randint(self.size)
        if size <= 0:
            return lq
        angle = safe_randint(self.angle)
        logging.debug(f"Blur - type: motion size: {size} angle: {angle}")
        return motion_blur(lq, size, angle)

    def __random(self, lq: np.ndarray) -> np.ndarray:
        kernel = safe_uniform(self.kernels["random"])
        if kernel <= 0.0:
            return lq
        logging.debug(f"Blur - type: lens kernel: {kernel:.4f}", kernel)
        return random_kernel_blur(lq, kernel)

    def __median(self, lq: np.ndarray) -> np.ndarray:
        kernel_list = self.kernels["median"]
        kernel = safe_randint(kernel_list)
        if kernel == 0:
            return lq
        kernel = self.__kernel_odd(kernel)
        logging.debug(f"Blur - type: lens kernel: {kernel:.4f}", kernel)
        return (
            cv.medianBlur((lq * 255).astype(np.uint8), kernel).astype(np.float32) / 255
        )

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Applies blur effects to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the image with applied blur effects and the corresponding high-quality image.
        """
        try:
            BLUR_MAP = {
                "gauss": self.__gauss,
                "box": self.__box,
                "median": self.__median,
                "lens": self.__lens,
                "motion": self.__motion,
                "random": self.__random,
            }

            if probability(self.probability):
                return lq, hq
            blur_method = random.choice(self.filter)
            lq = BLUR_MAP[blur_method](lq)

            return lq, hq
        except Exception as e:
            logging.error("Blur error: %s", e)
