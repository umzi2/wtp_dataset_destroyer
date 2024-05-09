from pepeline import screentone, TypeDot, cvt_color, CvtType
import numpy as np
from numpy import random

from ..utils import probability


class ScreentoneLogic:
    """
    Class for applying screentone effect to images.

    Args:
        screentone_dict (dict): A dictionary containing parameters for screentone effect.
            It should have the following keys:
                - 'lqhq' (bool, optional): Whether to apply the same effect to both low quality and high quality images. Default is None.
                - 'dot_size' (list, optional): Range of dot sizes for screentone effect. Default is [7].
                - 'color' (dict, optional): Dictionary specifying color parameters for screentone effect. Default is None.
                - 'prob' (float, optional): Probability of applying screentone effect. Default is 1.0.

    Attributes:
        lqhq (bool): Whether to apply the same effect to both low quality and high quality images.
        dot_range (list): Range of dot sizes for screentone effect.
        type (list): List of color types for screentone effect.
        color_c (list): Range of angles for C color channel.
        color_m (list): Range of angles for M color channel.
        color_y (list): Range of angles for Y color channel.
        color_k (list): Range of angles for K color channel.
        color_b (list): Range of angles for B color channel.
        color_g (list): Range of angles for G color channel.
        color_r (list): Range of angles for R color channel.
        probably (float): Probability of applying screentone effect.
        dot_type (TypeDot): Type of dot for screentone effect.

    Methods:
        run(lq, hq): Method to run the screentone effect process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Image with screentone effect applied and original high quality image.
    """

    def __init__(self, screentone_dict):
        self.lqhq = screentone_dict.get("lqhq")
        self.dot_range = screentone_dict.get("dot_size", [7])
        color = screentone_dict.get("color")
        if color:
            self.type = color.get("type_halftone", ["rgb"])
            self.color_c = color.get("c", [0, 0])
            self.color_m = color.get("m", [0, 0])
            self.color_y = color.get("y", [0, 0])
            self.color_k = color.get("k", [0, 0])
            self.color_b = color.get("b", [0, 0])
            self.color_g = color.get("g", [0, 0])
            self.color_r = color.get("r", [0, 0])
        self.probably = screentone_dict.get("probably", 1.0)
        self.dot_type = TypeDot.CIRCLE

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq

            lq = np.squeeze(lq).astype(np.float32)
            dot_size = random.choice(self.dot_range)
            if np.ndim(lq) != 2:
                color_type = random.choice(self.type)
                if color_type == "cmyk":
                    c_angle = random.randint(*self.color_c)
                    m_angle = random.randint(*self.color_m)
                    y_angle = random.randint(*self.color_y)
                    k_angle = random.randint(*self.color_k)
                    lq = cvt_color(lq, CvtType.RGB2CMYK)
                    lq[..., 0] = screentone(lq[..., 0], dot_size, c_angle, self.dot_type)
                    lq[..., 1] = screentone(lq[..., 1], dot_size, m_angle, self.dot_type)
                    lq[..., 2] = screentone(lq[..., 2], dot_size, y_angle, self.dot_type)
                    lq[..., 3] = screentone(lq[..., 3], dot_size, k_angle, self.dot_type)

                    lq = cvt_color(lq, CvtType.CMYK2RGB)
                elif color_type == "not_rot":
                    lq[..., 0] = screentone(lq[..., 0], dot_size, 0, self.dot_type)
                    lq[..., 1] = screentone(lq[..., 1], dot_size, 0, self.dot_type)
                    lq[..., 2] = screentone(lq[..., 2], dot_size, 0, self.dot_type)
                elif color_type == "gray":
                    lq = cvt_color(lq, CvtType.RGB2GrayBt709)
                    hq = cvt_color(hq, CvtType.RGB2GrayBt709)
                    lq = screentone(lq, dot_size, 0, self.dot_type)
                else:
                    r_angle = random.randint(*self.color_r)
                    g_angle = random.randint(*self.color_g)
                    b_angle = random.randint(*self.color_b)
                    lq[..., 0] = screentone(lq[..., 0], dot_size, r_angle, self.dot_type)
                    lq[..., 1] = screentone(lq[..., 1], dot_size, g_angle, self.dot_type)
                    lq[..., 2] = screentone(lq[..., 2], dot_size, b_angle, self.dot_type)
            else:
                lq = screentone(lq, dot_size, 0, self.dot_type)

            if self.lqhq:
                hq = lq
            return lq, hq
        except Exception as e:
            print(f"screentone error {e}")
