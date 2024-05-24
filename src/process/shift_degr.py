import numpy as np
import cv2 as cv
from pepeline import cvt_color, CvtType
from src.process.utils import probability
from numpy import random

from ..utils.random import safe_uniform, safe_randint
from src.utils.registry import register_class


def shift(img, amount_x: int, amount_y: int, fill_color: list | float) -> np.ndarray:
    """
    Shifts the image by the specified amounts in the x and y directions.

    Parameters:
    img (np.ndarray): The input image.
    amount_x (int): The amount to shift the image along the x-axis.
    amount_y (int): The amount to shift the image along the y-axis.
    fill_color (list | float): The color used to fill the empty space after the shift.

    Returns:
    np.ndarray: The shifted image.
    """
    h, w = img.shape[:2]
    translation_matrix = np.asarray(
        [[1, 0, amount_x], [0, 1, amount_y]], dtype=np.float32
    )
    return cv.warpAffine(
        img,
        translation_matrix,
        (w, h),
        borderMode=cv.BORDER_CONSTANT,
        borderValue=fill_color,
    )


def shift_int(
        img: np.ndarray, amount_channel: list[list[int]], fill_color: list[float]
) -> (int, int):
    """
    Shifts the image by random integer amounts within the specified ranges.

    Parameters:
    img (np.ndarray): The input image.
    amount_channel (list[list[int]]): The ranges for random shifts in x and y directions.
    fill_color (list[float]): The color used to fill the empty space after the shift.

    Returns:
    np.ndarray: The shifted image.
    """
    amount_x = 0
    amount_y = 0
    if amount_channel[0] != [0, 0]:
        amount_x = safe_randint(amount_channel[0])
    if amount_channel[1] != [0, 0]:
        amount_y = safe_randint(amount_channel[1])
    if amount_x == 0 and amount_y == 0:
        return img
    return shift(img, amount_x, amount_y, fill_color)


def shift_percent(
        img: np.ndarray, amount_channel: list[list[int]], fill_color: list[float]
) -> (int, int):
    """
    Shifts the image by random percentages of its dimensions within the specified ranges.

    Parameters:
    img (np.ndarray): The input image.
    amount_channel (list[list[int]]): The ranges for random percentage shifts in x and y directions.
    fill_color (list[float]): The color used to fill the empty space after the shift.

    Returns:
    np.ndarray: The shifted image.
    """
    amount_x = 0
    amount_y = 0
    shape_img = img.shape
    if amount_channel[0] != [0, 0]:
        amount_x = int(shape_img[0] * safe_uniform(amount_channel[0]) / 100)
    if amount_channel[1] != [0, 0]:
        amount_y = int(shape_img[1] * safe_uniform(amount_channel[1]) / 100)
    if amount_x == 0 and amount_y == 0:
        return img
    return shift(img, amount_x, amount_y, fill_color)


@register_class("shift")
class Shift:
    """
    Class for applying random shifts to an image based on specified configurations.

    Attributes:
    type_list (list[str]): The list of color spaces to apply the shifts.
    probability (float): The probability of applying the shift.
    shift_channel (function): The function to apply the shift (either by integer or percentage).
    rgb_amount_list (list[list[int]]): The shift ranges for the RGB color space.
    yuv_amount_list (list[list[int]]): The shift ranges for the YUV color space.
    cmyk_amount_list (list[list[int]]): The shift ranges for the CMYK color space.
    """

    def __init__(self, shift_dict: dict):
        """
        Initializes the Shift class with the given configuration dictionary.

        Parameters:
        shift_dict (dict): The configuration dictionary for the shifts.
        """
        self.type_list = shift_dict.get("shift_type", ["rgb"])
        self.probability = shift_dict.get("probability", 1.0)
        percent = shift_dict.get("percent")
        if percent:
            self.shift_channel = shift_percent
        else:
            self.shift_channel = shift_int
        not_target = shift_dict.get("not_target", [[0, 0], [0, 0]])
        rgb = shift_dict.get("rgb")
        if rgb:
            r_amount = rgb.get("r", not_target)
            g_amount = rgb.get("g", not_target)
            b_amount = rgb.get("b", not_target)
            self.rgb_amount_list = [r_amount, g_amount, b_amount]
        else:
            self.rgb_amount_list = [not_target, not_target, not_target]
        yuv = shift_dict.get("yuv")
        if yuv:
            y_yuv_amount = yuv.get("y", not_target)
            u_amount = yuv.get("u", not_target)
            v_amount = yuv.get("v", not_target)
            self.yuv_amount_list = [y_yuv_amount, u_amount, v_amount]
        else:
            self.yuv_amount_list = [not_target, not_target, not_target]
        cmyk = shift_dict.get("cmyk")
        if cmyk:
            c_amount = cmyk.get("c", not_target)
            m_amount = cmyk.get("m", not_target)
            y_amount = cmyk.get("y", not_target)
            k_amount = cmyk.get("k", not_target)
            self.cmyk_amount_list = [c_amount, m_amount, y_amount, k_amount]
        else:
            self.cmyk_amount_list = [not_target, not_target, not_target, not_target]

    def __rgb_chanel_shift(self, img: np.ndarray) -> np.ndarray:
        """
        Applies the shift to the RGB channels of the image.

        Parameters:
        img (np.ndarray): The input image.

        Returns:
        np.ndarray: The shifted image.
        """
        for c in range(3):
            channel_amount = self.rgb_amount_list[c]
            img[:, :, c] = self.shift_channel(img[:, :, c], channel_amount, [1])

        return img

    def __yuv_chanel_shift(self, img: np.ndarray) -> np.ndarray:
        """
        Applies the shift to the YUV channels of the image.

        Parameters:
        img (np.ndarray): The input image.

        Returns:
        np.ndarray: The shifted image.
        """
        yuv_img = cvt_color(img, CvtType.RGB2YCvCrBt2020)
        for c in range(3):
            channel_amount = self.yuv_amount_list[c]
            yuv_img[:, :, c] = self.shift_channel(yuv_img[:, :, c], channel_amount, [1])
        return cvt_color(yuv_img, CvtType.YCvCr2RGBBt2020)

    def __cmyk_chanel_shift(self, img: np.ndarray) -> np.ndarray:
        """
        Applies the shift to the CMYK channels of the image.

        Parameters:
        img (np.ndarray): The input image.

        Returns:
        np.ndarray: The shifted image.
        """
        cmyk_img = cvt_color(img, CvtType.RGB2CMYK)
        for c in range(4):
            channel_amount = self.cmyk_amount_list[c]
            cmyk_img[:, :, c] = self.shift_channel(cmyk_img[:, :, c], channel_amount, [0])
        return cvt_color(cmyk_img, CvtType.CMYK2RGB)

    def run(self, lq: np.ndarray, hq: np.ndarray) -> np.ndarray:
        """
        Runs the shift transformation on the low-quality (lq) image, optionally returns high-quality (hq) image.

        Parameters:
        lq (np.ndarray): The low-quality input image.
        hq (np.ndarray): The high-quality input image.

        Returns:
        tuple[np.ndarray, np.ndarray]: The transformed low-quality image and the high-quality image.
        """
        try:
            SHIFT_TYPE_MAP = {
                "rgb": self.__rgb_chanel_shift,
                "cmyk": self.__cmyk_chanel_shift,
                "yuv": self.__yuv_chanel_shift,
            }
            if lq.ndim == 2:
                return lq, hq
            if probability(self.probability):
                return lq, hq
            type_shift = random.choice(self.type_list)
            lq = SHIFT_TYPE_MAP[type_shift](lq)
            return lq, hq
        except Exception as e:
            print(f"shift error {e}")
