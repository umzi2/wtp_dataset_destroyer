import numpy as np
from .utils import probability
from ..constants import INTERPOLATION_MAP, SUBSAMPLING_MAP, YUV_MAP
from numpy.random import choice
from src.utils.registry import register_class
from pepeline import cvt_color
from chainner_ext import resize, ResizeFilter
import cv2 as cv
import logging

from ..utils.random import safe_uniform


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
    def __down_up(lq: np.ndarray, shape: [int, int], scale: float, down_alg: ResizeFilter,
                  up_alg: ResizeFilter) -> np.ndarray:
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
        return resize(
            resize(
                lq, (int(shape[1] * scale), int(shape[0] * scale)), down_alg, False
            ).squeeze(),
            (shape[1], shape[0]), up_alg, False
        ).squeeze()

    def __sample(self, lq: np.ndarray, format_sampling: str) -> np.ndarray:
        """
        Applies subsampling to the image according to the specified format.

        Args:
            lq (np.ndarray): Low-quality input image.
            format_sampling (str): Subsampling format.

        Returns:
            np.ndarray: Image after subsampling.
        """
        shape_lq = lq.shape
        down_alg = INTERPOLATION_MAP[choice(self.down_alg)]
        up_alg = INTERPOLATION_MAP[choice(self.up_alg)]
        scale_list = SUBSAMPLING_MAP[format_sampling]
        logging.debug(f"Subsampling: format - {format_sampling} down_alg - {down_alg} up_alg - {up_alg}")
        for index in range(3):
            scale = scale_list[index]
            if scale != 1:
                lq[..., index] = self.__down_up(
                    lq[..., index], shape_lq, scale, down_alg, up_alg
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

            format_type = choice(self.format_list)
            yuv = YUV_MAP.get(choice(self.ycbcr_type), YUV_MAP["601"])
            lq = cvt_color(lq, yuv[0])

            if format_type in SUBSAMPLING_MAP.keys() and format_type != "4:4:4":
                lq = self.__sample(lq, format_type)

            if self.blur_kernels:
                sigma = safe_uniform(self.blur_kernels)
                if sigma != 0.0:
                    logging.debug(f"Subsampling blur: sigma - {sigma}")
                    lq[..., 1] = cv.GaussianBlur(
                        lq[..., 1], (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
                    )
                    lq[..., 2] = cv.GaussianBlur(
                        lq[..., 2], (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
                    )

            lq = cvt_color(lq, yuv[1])
            return lq, hq
        except Exception as e:
            logging.error(f"Subsampling Error: {e}")
