import logging

import numpy as np
from .utils import probability
from ..utils.registry import register_class
from ..utils.random import safe_uniform
from chainner_ext import resize, ResizeFilter


@register_class("pixelate")
class Pixelate:
    """
    The `Pixelate` class is designed to apply a pixelation effect to an image based on specified parameters.
    The pixelation effect is controlled by the size of the pixel blocks and the probability of applying the effect.
    """

    def __init__(self, noise_dict: dict):
        """
        Initializes the Pixelate class with specified configuration.

        Args:
            noise_dict (dict): A dictionary containing the configuration for the pixelation effect.
                - `size` (list): A list with two elements representing the range of pixel block sizes. Default is [1, 1].
                - `probability` (float): The probability of applying the pixelation effect. Default is 1.0.
        """
        self.size_range = noise_dict.get("size", [1, 1])
        self.probability = noise_dict.get("probability", 1.0)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Applies the pixelation effect to the low-quality (LQ) image based on the specified parameters.

        Args:
            lq (np.ndarray): The low-quality (LQ) image to be pixelated.
            hq (np.ndarray): The high-quality (HQ) image to remain unchanged.

        Returns:
            (np.ndarray, np.ndarray): A tuple containing the pixelated LQ image and the unchanged HQ image.
        """
        try:
            # Check if the pixelation should be applied based on the given probability.
            if probability(self.probability):
                return lq, hq

            # Determine the shape of the input LQ image.
            shape_img = lq.shape

            # Select a pixel block size within the specified range.
            pixel_size = safe_uniform(self.size_range)
            if pixel_size <= 1:
                return lq, hq

            logging.debug("Pixelate - size: %.4f", pixel_size)

            # Apply the pixelation effect by resizing the image to a smaller size and then back to the original size.
            lq = resize(
                lq,
                (int(shape_img[1] / pixel_size), int(shape_img[0] / pixel_size)),
                ResizeFilter.Linear,
                False,
            )
            lq = resize(lq, (shape_img[1], shape_img[0]), ResizeFilter.Nearest, False).squeeze()

            return lq, hq
        except Exception as e:
            logging.error("Pixelate error: %s", e)
