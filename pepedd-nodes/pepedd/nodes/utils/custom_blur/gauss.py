import cv2
import numpy as np


def gauss(img, sigma: float) -> np.ndarray:
    return cv2.GaussianBlur(
        img, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv2.BORDER_REFLECT
    )
