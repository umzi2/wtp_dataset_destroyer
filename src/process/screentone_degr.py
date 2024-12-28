import cv2
from pepeline import screentone, cvt_color, CvtType
import numpy as np
from numpy import random

from .utils import probability, lq_hq2grays
from ..constants import DOT_TYPE
from ..utils.random import safe_uniform, safe_arange
from ..utils.registry import register_class
import logging


@register_class("screentone")
class Screentone:
    def __init__(self, screentone_dict: dict):
        self.lqhq = screentone_dict.get("lqhq")
        self.dot_range = screentone_dict.get("dot_size", [7])
        self.dot_type_list = screentone_dict.get("dot_type", ["circle"])
        angle = screentone_dict.get("angle", [0, 0])
        self.angle = safe_arange(angle)
        color = screentone_dict.get("color")
        if color:
            color = color[0]
            self.type = color.get("type_halftone", ["rgb"])
            self.dot_types_list = []
            self.dot_angle_list = []
            if "dot" in color:
                color_dot_dicts = color["dot"]
                dot_dict_len = len(color_dot_dicts)
                for index in range(4):
                    color_dot_dict = color_dot_dicts[index % dot_dict_len]
                    self.dot_types_list.append(color_dot_dict.get("type", self.type))
                    self.dot_angle_list.append(
                        safe_arange(color_dot_dict.get("angle", angle))
                    )
            else:
                for index in range(4):
                    self.dot_types_list.append(self.type)
                    self.dot_angle_list.append(self.angle)
            self.cmyk_alpha = color.get("cmyk_alpha")

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
        c_angle = int(random.choice(self.dot_angle_list[0]))
        m_angle = int(random.choice(self.dot_angle_list[1]))
        y_angle = int(random.choice(self.dot_angle_list[2]))
        k_angle = int(random.choice(self.dot_angle_list[3]))
        dot_type1 = DOT_TYPE.get(
            random.choice(self.dot_types_list[0]), DOT_TYPE["circle"]
        )
        dot_type2 = DOT_TYPE.get(
            random.choice(self.dot_types_list[1]), DOT_TYPE["circle"]
        )
        dot_type3 = DOT_TYPE.get(
            random.choice(self.dot_types_list[2]), DOT_TYPE["circle"]
        )
        dot_type4 = DOT_TYPE.get(
            random.choice(self.dot_types_list[3]), DOT_TYPE["circle"]
        )
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
        dot_type1 = DOT_TYPE.get(
            random.choice(self.dot_types_list[0]), DOT_TYPE["circle"]
        )
        dot_type2 = DOT_TYPE.get(
            random.choice(self.dot_types_list[1]), DOT_TYPE["circle"]
        )
        dot_type3 = DOT_TYPE.get(
            random.choice(self.dot_types_list[2]), DOT_TYPE["circle"]
        )
        logging.debug(
            f"Screentone - type: not_rot dot: {dot_size} not_rot dot type: {dot_type1} {dot_type2} {dot_type3}"
        )
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
        dot_type1 = DOT_TYPE.get(
            random.choice(self.dot_types_list[0]), DOT_TYPE["circle"]
        )
        logging.debug(
            f"Screentone - type: gray dot: {dot_size} gray dot_type: {dot_type1}"
        )
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
        dot_type1 = DOT_TYPE.get(
            random.choice(self.dot_types_list[0]), DOT_TYPE["circle"]
        )
        dot_type2 = DOT_TYPE.get(
            random.choice(self.dot_types_list[1]), DOT_TYPE["circle"]
        )
        dot_type3 = DOT_TYPE.get(
            random.choice(self.dot_types_list[2]), DOT_TYPE["circle"]
        )
        r_angle = int(random.choice(self.dot_angle_list[0]))
        g_angle = int(random.choice(self.dot_angle_list[1]))
        b_angle = int(random.choice(self.dot_angle_list[2]))
        logging.debug(
            f"Screentone - type: rgb dot: {dot_size} rgb_angle: {r_angle} {g_angle} {b_angle} rgb dot_type: {dot_type1} {dot_type2} {dot_type3}",
        )
        lq[..., 0] = screentone(lq[..., 0], dot_size, r_angle, dot_type=dot_type1)
        lq[..., 1] = screentone(lq[..., 1], dot_size, g_angle, dot_type=dot_type2)
        lq[..., 2] = screentone(lq[..., 2], dot_size, b_angle, dot_type=dot_type3)
        return lq, hq

    def __hsv_screentone(
        self, lq: np.ndarray, hq: np.ndarray, dot_size: int
    ) -> (np.ndarray, np.ndarray):
        """Applies HSV screentone effect to the image.

        Args:
            lq (numpy.ndarray): The low-quality image in RGB color space.
            hq (numpy.ndarray): The high-quality image.
            dot_size (int): The size of the halftone dots.

        Returns:
            tuple: A tuple containing the HSV screentoned low-quality image and the corresponding high-quality image.
        """
        dot_type1 = DOT_TYPE.get(
            random.choice(self.dot_types_list[0]), DOT_TYPE["circle"]
        )
        v_angle = int(random.choice(self.angle))
        logging.debug(
            f"Screentone - type: hsv dot: {dot_size} hsv angle: {v_angle} hsv dot_type: {dot_type1}",
        )
        lq = cv2.cvtColor(lq, cv2.COLOR_RGB2HSV)
        lq[..., 2] = screentone(lq[..., 2], dot_size, v_angle, dot_type=dot_type1)
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
                angle = int(random.choice(self.angle))
                dot_type = DOT_TYPE.get(
                    random.choice(self.dot_type_list), DOT_TYPE["circle"]
                )
                logging.debug(
                    f"Screentone - type: gray dot: {dot_size}  gray angle: {angle} gray dot_type: {dot_type}",
                )
                lq = screentone(lq, dot_size, angle, dot_type)

            if self.lqhq:
                hq = lq
            return lq, hq

        except Exception as e:
            logging.error("screentone error: %s", e)
