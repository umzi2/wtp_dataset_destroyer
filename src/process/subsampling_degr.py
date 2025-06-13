import random
import numpy as np
from pepeline.pepeline import fast_color_level

from .utils import probability
from ..constants import INTERPOLATION_MAP, SUBSAMPLING_MAP, YUV_MAP
from numpy.random import choice
from src.utils.registry import register_class
from chainner_ext import resize, ResizeFilter
import cv2 as cv
import logging

from ..utils.random import safe_uniform
import colour


@register_class("subsampling")
class Subsampling:
    """
    A class to perform subsampling on images with various downscaling and upscaling algorithms,
    different subsampling formats, and optional blurring.

    Attributes:
        down_alg (list): List of algorithms for downscaling.
        up_alg (list): List of algorithms for upscaling.
        format_list (list): List of subsampling formats.
        blur_kernels (list): List of blur kernel sizes for optional blurring.
        ycbcr_type (list): List of YUV types.
        probability (float): Probability of applying subsampling.
    """

    def __init__(self, sub: dict):
        """
        Initializes the Subsampling class with the provided configuration.

        Args:
            sub (dict): Configuration dictionary containing options for downscaling,
                        upscaling, subsampling format, blur kernels, YUV type, and
                        probability.
        """
        self.down_alg = sub.get("down", ["nearest"])
        self.up_alg = sub.get("up", ["nearest"])
        self.format_list = sub.get("sampling", ["4:4:4"])
        self.blur_kernels = sub.get("blur")
        self.ycbcr_type = sub.get("yuv", ["601"])
        self.probability = sub.get("probability", 1.0)

    @staticmethod
    def __down_up(
        lq: np.ndarray,
        shape: [int, int],
        scale: [float, float],
        down_alg: ResizeFilter,
        up_alg: ResizeFilter,
    ) -> np.ndarray:
        """
        Applies downscaling followed by upscaling to an image.

        Args:
            lq (np.ndarray): Low-quality input image.
            shape (tuple): Target shape of the image.
            scale (float): Scaling factor.
            down_alg (ResizeFilter): Downscaling algorithm.
            up_alg (ResizeFilter): Upscaling algorithm.

        Returns:
            np.ndarray: Image after applying downscaling and upscaling.
        """
        return fast_color_level(
            resize(
                resize(
                    lq,
                    (int(shape[1] * scale[1]), int(shape[0] * scale[0])),
                    down_alg,
                    False,
                ).squeeze(),
                (shape[1], shape[0]),
                up_alg,
                False,
            ).squeeze(),
            1,
            254,
        )

    def __sample(self, lq: np.ndarray) -> np.ndarray:
        """
        Applies subsampling to the image according to the specified format.

        Args:
            lq (np.ndarray): Low-quality input image.

        Returns:
            np.ndarray: Image after subsampling.
        """
        shape_lq = lq.shape
        down_alg = INTERPOLATION_MAP[choice(self.down_alg)]
        up_alg = INTERPOLATION_MAP[choice(self.up_alg)]
        scale_list = SUBSAMPLING_MAP[random.choice(self.format_list)]
        logging.debug(
            f"Subsampling: format - {scale_list} down_alg - {down_alg} up_alg - {up_alg}"
        )
        if scale_list != [1, 1, 1]:
            lq[..., 1:3] = self.__down_up(
                lq[..., 1:3], shape_lq, scale_list[1:3], down_alg, up_alg
            )
        return lq

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """
        Runs the subsampling process and optional blurring on the input image.

        Args:
            lq (np.ndarray): Low-quality input image.
            hq (np.ndarray): High-quality reference image.

        Returns:
            tuple: Modified low-quality image and the original high-quality image.
        """
        try:
            if lq.ndim == 2 or lq.shape[2] == 1 or probability(self.probability):
                return lq, hq
            yuv = YUV_MAP[random.choice(self.ycbcr_type)]
            lq = colour.RGB_to_YCbCr(
                lq, in_bits=8, K=colour.models.rgb.ycbcr.WEIGHTS_YCBCR[yuv]
            ).astype(np.float32)  # cv2.cvtColor(lq,cv2.COLOR_RGB2YCrCb)

            lq = self.__sample(lq)
            if self.blur_kernels:
                sigma = safe_uniform(self.blur_kernels)
                if sigma != 0.0:
                    logging.debug(f"Subsampling blur: sigma - {sigma}")
                    lq[..., 1] = cv.GaussianBlur(
                        lq[..., 1],
                        (0, 0),
                        sigmaX=sigma,
                        sigmaY=sigma,
                        borderType=cv.BORDER_REFLECT,
                    )
                    lq[..., 2] = cv.GaussianBlur(
                        lq[..., 2],
                        (0, 0),
                        sigmaX=sigma,
                        sigmaY=sigma,
                        borderType=cv.BORDER_REFLECT,
                    )
            lq = (
                colour.YCbCr_to_RGB(
                    lq,
                    in_bits=8,
                    out_bits=8,
                    K=colour.models.rgb.ycbcr.WEIGHTS_YCBCR[yuv],
                )
                .astype(np.float32)
                .clip(0, 1)
            )
            return lq, hq
        except Exception as e:
            logging.error(f"Subsampling Error: {e}")
