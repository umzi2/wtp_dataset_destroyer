from numpy import random
import numpy as np
from ..utils import probability
import cv2 as cv


class BlurLogic:
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

    def __init__(self, blur_dict):
        self.filter = blur_dict["filter"]
        kernel = blur_dict.get("kernel", [0, 1, 1])
        self.probably = blur_dict.get("probably", 1.0)
        target = blur_dict.get("target_kernel")
        if target:
            gauss = target.get("gauss", kernel)
            blur = target.get("blur", kernel)
            box = target.get("box", kernel)
            median = target.get("median", kernel)
            self.kernels = {
                "gauss": np.arange(*gauss),
                "blur": np.arange(*blur),
                "box": np.arange(*box),
                "median": np.arange(*median),
            }
        else:
            self.kernels = {
                "gauss": np.arange(*kernel),
                "blur": np.arange(*kernel),
                "box": np.arange(*kernel),
                "median": np.arange(*kernel),
            }

    def run(self, lq, hq):
        """Applies blur effects to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the image with applied blur effects and the corresponding high-quality image.
        """
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            blur_method = random.choice(self.filter)
            kernel = random.choice(self.kernels[blur_method])
            if kernel == 0:
                return lq, hq
            match blur_method:
                case "gauss":
                    if kernel % 2 == 0:
                        kernel += 1
                    lq = cv.GaussianBlur(lq, (kernel, kernel), 0)

                case "blur":
                    if kernel % 2 == 0:
                        kernel += 1
                    lq = cv.blur(lq, (kernel, kernel))

                case "box":
                    lq = cv.boxFilter(lq, -1, (kernel, kernel))
                case "median":
                    if kernel % 2 == 0:
                        kernel += 1
                    lq = (
                        cv.medianBlur((lq * 255).astype(np.uint8), kernel).astype(
                            np.float32
                        )
                        / 255
                    )
            return lq, hq
        except Exception as e:
            print(f"blur error {e}")
