import cv2
from pepeline import screentone, cvt_color, CvtType
import numpy as np
from numpy import random

from .utils import probability, lq_hq2grays
from ..constants import DOT_TYPE
from ..utils.random import safe_uniform, safe_randint
from ..utils.registry import register_class
import logging


@register_class("screentone")
class Screentone:
    """Class for applying screentone effects to images.

    Args:
        screentone_dict (dict): A dictionary containing screentone settings.
            It should include the following keys:
                - "lqhq" (bool, optional): Flag indicating if the high-quality image should be replaced by the low-quality.
                    Defaults to None.
                - "dot_size" (list of int, optional): Range of dot sizes for screentone effects. Defaults to [7].
                - "dot_type" (list of str, optional): List of dot types for screentone effects. Defaults to ["circle"].
                - "angle" (list of int, optional): Range of angles for dot rotation. Defaults to [0, 0].
                - "color" (dict, optional): Dictionary containing color-specific settings.
                    Defaults to None.
                - "probability" (float, optional): Probability of applying screentone effects. Defaults to 1.0.
            The "color" dictionary should include the following keys:
                - "type_halftone" (list of str, optional): List of halftone types to choose from.
                    Defaults to ["rgb"].
                - "c" (list of int, optional): Range of angles for the C (cyan) channel halftone.
                    Defaults to [0, 0].
                - "m" (list of int, optional): Range of angles for the M (magenta) channel halftone.
                    Defaults to [0, 0].
                - "y" (list of int, optional): Range of angles for the Y (yellow) channel halftone.
                    Defaults to [0, 0].
                - "k" (list of int, optional): Range of angles for the K (black) channel halftone.
                    Defaults to [0, 0].
                - "b" (list of int, optional): Range of angles for the B (blue) channel halftone.
                    Defaults to [0, 0].
                - "g" (list of int, optional): Range of angles for the G (green) channel halftone.
                    Defaults to [0, 0].
                - "r" (list of int, optional): Range of angles for the R (red) channel halftone.
                    Defaults to [0, 0].
                - "cmyk_alpha" (list of float, optional): Range of alpha values for the CMYK channels.
                    Defaults to [1, 1].
                - "1_ch_dot_type" (list of str, optional): List of dot types for single-channel halftones.
                    Defaults to the value of "dot_type".
                - "2_ch_dot_type" (list of str, optional): List of dot types for two-channel halftones.
                    Defaults to the value of "dot_type".
                - "3_ch_dot_type" (list of str, optional): List of dot types for three-channel halftones.
                    Defaults to the value of "dot_type".
                - "4_ch_dot_type" (list of str, optional): List of dot types for four-channel halftones.
                    Defaults to the value of "dot_type".
    """

    def __init__(self, screentone_dict: dict):
        self.lqhq = screentone_dict.get("lqhq")
        self.dot_range = screentone_dict.get("dot_size", [7])
        self.dot_type_list = screentone_dict.get("dot_type", ["circle"])
        self.angle = screentone_dict.get("angle", [0, 0])
        color = screentone_dict.get("color")
        if color:
            self.type = color.get("type_halftone", ["rgb"])
            self.color_c = color.get("c", self.angle)
            self.color_m = color.get("m", self.angle)
            self.color_y = color.get("y", self.angle)
            self.color_k = color.get("k", self.angle)
            self.color_b = color.get("b", self.angle)
            self.color_g = color.get("g", self.angle)
            self.color_r = color.get("r", self.angle)
            self.cmyk_alpha = color.get("cmyk_alpha", [1, 1])
            self.one_ch_dot_type_list = color.get("1_ch_dot_type", self.dot_type_list)
            self.two_ch_dot_type_list = color.get("2_ch_dot_type", self.dot_type_list)
            self.three_ch_dot_type_list = color.get("3_ch_dot_type", self.dot_type_list)
            self.four_ch_dot_type_list = color.get("4_ch_dot_type", self.dot_type_list)
        self.probability = screentone_dict.get("probability", 1.0)

    def __cmyk_halftone(
            self, lq: np.ndarray, hq: np.ndarray, dot_size: int
    ) -> (np.ndarray, np.ndarray):
        """Applies CMYK halftone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in CMYK color space.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the CMYK halftoned low-quality image and the corresponding high-quality image.
        """
        c_angle = safe_randint(self.color_c)
        m_angle = safe_randint(self.color_m)
        y_angle = safe_randint(self.color_y)
        k_angle = safe_randint(self.color_k)
        dot_type1 = DOT_TYPE.get(random.choice(self.one_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type2 = DOT_TYPE.get(random.choice(self.two_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type3 = DOT_TYPE.get(random.choice(self.three_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type4 = DOT_TYPE.get(random.choice(self.four_ch_dot_type_list), DOT_TYPE["circle"])
        lq = cvt_color(lq, CvtType.RGB2CMYK)
        lq[..., 0] = screentone(lq[..., 0], dot_size, c_angle, dot_type1)
        lq[..., 1] = screentone(lq[..., 1], dot_size, m_angle, dot_type2)
        lq[..., 2] = screentone(lq[..., 2], dot_size, y_angle, dot_type3)
        lq[..., 3] = screentone(lq[..., 3], dot_size, k_angle, dot_type4)
        if self.cmyk_alpha != [1, 1]:
            alpha = safe_uniform(self.cmyk_alpha)
            lq *= alpha
        logging.debug(
            f"Screentone - type: cmyk dot: {dot_size} cmyk_angle: {c_angle} {m_angle} {y_angle} {k_angle} cmyk_dot_type: {dot_type1} {dot_type2} {dot_type3} {dot_type4}",
        )
        return cvt_color(lq, CvtType.CMYK2RGB), hq

    def __not_rot_halftone(
            self, lq: np.ndarray, hq: np.ndarray, dot_size: int
    ) -> (np.ndarray, np.ndarray):
        """Applies non-rotated halftone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in RGB color space.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the non-rotated halftoned low-quality image and the corresponding high-quality image.
        """
        dot_type1 = DOT_TYPE.get(random.choice(self.one_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type2 = DOT_TYPE.get(random.choice(self.two_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type3 = DOT_TYPE.get(random.choice(self.three_ch_dot_type_list), DOT_TYPE["circle"])
        logging.debug(
            f"Screentone - type: not_rot dot: {dot_size} not_rot dot type: {dot_type1} {dot_type2} {dot_type3}")
        lq[..., 0] = screentone(lq[..., 0], dot_size, dot_type=dot_type1)
        lq[..., 1] = screentone(lq[..., 1], dot_size, dot_type=dot_type2)
        lq[..., 2] = screentone(lq[..., 2], dot_size, dot_type=dot_type3)
        return lq, hq

    def __gray_halftone(
            self, lq: np.ndarray, hq: np.ndarray, dot_size: int
    ) -> (np.ndarray, np.ndarray):
        """Applies grayscale halftone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in grayscale.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the grayscale halftoned low-quality image and the corresponding high-quality image.
        """
        lq, hq = lq_hq2grays(lq, hq)
        dot_type1 = DOT_TYPE.get(random.choice(self.one_ch_dot_type_list), DOT_TYPE["circle"])
        logging.debug(f"Screentone - type: gray dot: {dot_size} gray dot_type: {dot_type1}")
        lq = screentone(lq, dot_size)
        return lq, hq

    def __rgb_halftone(
            self, lq: np.ndarray, hq: np.ndarray, dot_size: int
    ) -> (np.ndarray, np.ndarray):
        """Applies RGB halftone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in RGB color space.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the RGB halftoned low-quality image and the corresponding high-quality image.
        """
        dot_type1 = DOT_TYPE.get(random.choice(self.one_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type2 = DOT_TYPE.get(random.choice(self.two_ch_dot_type_list), DOT_TYPE["circle"])
        dot_type3 = DOT_TYPE.get(random.choice(self.three_ch_dot_type_list), DOT_TYPE["circle"])
        r_angle = safe_randint(self.color_r)
        g_angle = safe_randint(self.color_g)
        b_angle = safe_randint(self.color_b)
        logging.debug(
            f"Screentone - type: rgb dot: {dot_size} rgb_angle: {r_angle} {g_angle} {b_angle} rgb dot_type: {dot_type1} {dot_type2} {dot_type3}",
        )
        lq[..., 0] = screentone(lq[..., 0], dot_size, r_angle, dot_type=dot_type1)
        lq[..., 1] = screentone(lq[..., 1], dot_size, g_angle, dot_type=dot_type2)
        lq[..., 2] = screentone(lq[..., 2], dot_size, b_angle, dot_type=dot_type3)
        return lq, hq

    def __hsv_screentone(self, lq: np.ndarray, hq: np.ndarray, dot_size: int) -> (np.ndarray, np.ndarray):
        """Applies HSV screentone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in RGB color space.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the HSV screentoned low-quality image and the corresponding high-quality image.
        """
        dot_type1 = DOT_TYPE.get(random.choice(self.one_ch_dot_type_list), DOT_TYPE["circle"])
        v_angle = safe_randint(self.angle)
        logging.debug(
            f"Screentone - type: hsv dot: {dot_size} hsv angle: {v_angle} hsv dot_type: {dot_type1}",
        )
        lq = cv2.cvtColor(lq, cv2.COLOR_RGB2HSV)
        from pepeline import fast_color_level
        lq[..., 2] = screentone(fast_color_level(lq[..., 2], 2, 253), dot_size, v_angle, dot_type=dot_type1)
        lq = cv2.cvtColor(lq, cv2.COLOR_HSV2RGB)
        return lq, hq

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Applies the selected screentone effect to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the screentoned low-quality image and the corresponding high-quality image.
        """
        HALFTONE_TYPE_MAP = {
            "cmyk": self.__cmyk_halftone,
            "rgb": self.__rgb_halftone,
            "hsv": self.__hsv_screentone,
            "not_rot": self.__not_rot_halftone,
            "gray": self.__gray_halftone,
        }
        try:
            if probability(self.probability):
                return lq, hq

            dot_size = random.choice(self.dot_range)
            if np.ndim(lq) != 2:
                color_type = random.choice(self.type)
                lq, hq = HALFTONE_TYPE_MAP[color_type](lq, hq, dot_size)
            else:
                angle = safe_randint(self.angle)
                dot_type = DOT_TYPE.get(random.choice(self.dot_type_list), DOT_TYPE["circle"])
                logging.debug(
                    f"Screentone - type: gray dot: {dot_size}  gray angle: {angle} gray dot_type: {dot_type}", )
                lq = screentone(lq, dot_size, angle, dot_type)

            if self.lqhq:
                hq = lq
            return lq, hq

        except Exception as e:
            logging.error("screentone error: %s", e)
