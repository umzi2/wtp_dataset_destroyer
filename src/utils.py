import numpy as np
from pepeline import cvt_color, CvtType
from dataset_support import gray_or_color
import cv2 as cv


def probability(prob: float):
    if prob > np.random.uniform(0, 1):
        return False
    else:
        return True


def __max_min(img):
    maximum = np.max(img)
    minimal = np.min(img)
    return maximum, minimal


def normalize(img):
    maximum, minimum = __max_min(img)
    return (img - minimum) * (1 + 1) / (maximum - minimum) - 1


def color_or_gray(img):
    if gray_or_color(img, 0.0003):
        return img2gray(img)
    return img


def img2gray(img):
    if img.ndim != 2 and img.shape[2] != 1:
        return cvt_color(img, CvtType.RGB2GrayBt2020)
    else:
        return img


def lq_hq2grays(lq, hq):
    return img2gray(lq), img2gray(hq)


def laplace_filter(img, mean_min) -> bool:
    gray_img = img2gray(img)
    laplace_img = cv.Laplacian(gray_img, -1)
    return np.mean(np.abs(laplace_img)) < mean_min
