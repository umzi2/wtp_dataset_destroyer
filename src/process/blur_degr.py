from numpy import random
import numpy as np
from .utils import probability
import cv2 as cv

from ..utils.registry import register_class
from .custom_blur import motion_blur, lens_blur


@register_class("blur")
class Blur:
    """Class for applying blur effects to images.

    Args:
        blur_dict (dict): A dictionary containing blur settings.
            It should include the following keys:
                - "filter" (list of str): List of blur filter types to choose from.
                - "kernel" (list of int, optional): Range of kernel sizes for the blur filters.
                    Defaults to [0, 1, 1].
                - "probably" (float, optional): Probability of applying blur effects. Defaults to 1.0.
                - "target_kernel" (dict, optional): Dictionary containing target kernel ranges for specific blur filters.
                    Defaults to None.
    """

    def __init__(self, blur_dict: dict):
        self.filter = blur_dict["filter"]
        kernel = blur_dict.get("kernel", [0, 1, 1])

        # motion
        self.size = blur_dict.get("motion_size", [1, 2])
        self.angle = blur_dict.get("motion_angle", [0, 1])

        self.probably = blur_dict.get("probably", 1.0)
        target = blur_dict.get("target_kernel")
        if target:
            gauss = target.get("gauss", kernel)
            blur = target.get("blur", kernel)
            box = target.get("box", kernel)
            median = target.get("median", kernel)
            lens = target.get("lens", kernel)
            self.kernels = {
                "gauss": np.arange(*gauss),
                "blur": np.arange(*blur),
                "box": np.arange(*box),
                "median": np.arange(*median),
                "lens": lens,
            }
        else:
            self.kernels = {
                "gauss": np.arange(*kernel),
                "blur": np.arange(*kernel),
                "box": np.arange(*kernel),
                "median": np.arange(*kernel),
                "lens": kernel,
            }

    def __kernel_odd(self, kernel_size: int) -> int:
        if kernel_size % 2 == 0:
            kernel_size += 1
        return kernel_size

    def __gauss(self, lq: np.ndarray) -> np.ndarray:
        kernel = random.choice(self.kernels["gauss"])
        if kernel == 0:
            return lq
        kernel = self.__kernel_odd(kernel)
        return cv.GaussianBlur(lq, (kernel, kernel), 0)

    def __blur(self, lq: np.ndarray) -> np.ndarray:
        kernel = random.choice(self.kernels["blur"])
        if kernel == 0:
            return lq
        kernel = self.__kernel_odd(kernel)
        return cv.blur(lq, (kernel, kernel))

    def __box(self, lq: np.ndarray) -> np.ndarray:
        kernel = random.choice(self.kernels["box"])
        if kernel == 0:
            return lq
        return cv.blur(lq, (kernel, kernel))

    def __lens(self, lq: np.ndarray) -> np.ndarray:
        kernel = random.uniform(*self.kernels["lens"])
        if kernel < 1.0:
            return lq
        return lens_blur(lq, kernel)

    def __motion(self, lq: np.ndarray) -> np.ndarray:
        size = random.randint(*self.size)
        if size <= 0:
            return lq
        angle = random.randint(*self.angle)
        return motion_blur(lq, size, angle)

    def __median(self, lq: np.ndarray) -> np.ndarray:
        kernel = random.choice(self.kernels["median"])
        if kernel == 0:
            return lq
        kernel = self.__kernel_odd(kernel)
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
                "blur": self.__blur,
                "box": self.__box,
                "median": self.__median,
                "lens": self.__lens,
                "motion": self.__motion,
            }

            if probability(self.probably):
                return lq, hq
            blur_method = random.choice(self.filter)
            lq = BLUR_MAP[blur_method](lq)

            return lq, hq
        except Exception as e:
            print(f"blur error {e}")
