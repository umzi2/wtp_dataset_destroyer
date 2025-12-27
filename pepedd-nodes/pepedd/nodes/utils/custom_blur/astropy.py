# https://github.com/umzi2/Float-lens-blur
import numpy as np
import cv2
from astropy.convolution import AiryDisk2DKernel, Ring2DKernel
from skimage.draw import polygon


def airy_blur(img: np.ndarray, dimension: float) -> np.ndarray:
    kernel = AiryDisk2DKernel(max(int(round(dimension)), 1)).array.astype(np.float32)
    convolved = cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REFLECT)
    return convolved


def ring_blur(img, kernel_size: float, ring_size: int) -> np.ndarray:
    fraction = kernel_size % 1
    if fraction != 0:
        kernel = np.pad(
            Ring2DKernel(int(kernel_size), ring_size).array.astype(np.float32),
            1,
            mode="constant",
            constant_values=0,
        )
        kernel = (kernel > 0).astype(np.float32)
        min_kernal = Ring2DKernel(int(kernel_size) + 1, ring_size).array.astype(
            np.float32
        )
        min_kernal = (min_kernal > 0).astype(np.float32)
        kernel += min_kernal * fraction
        kernel = kernel.clip(0, 1)
        kernel /= kernel.sum()

    else:
        kernel = Ring2DKernel(kernel_size, ring_size).array.astype(np.float32)
    return cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REFLECT)


def triangle(kernel_size: int):
    kernel = np.zeros((kernel_size, kernel_size), dtype=np.float32)
    r = np.array([0, kernel_size - 1, kernel_size - 1])
    c = np.array([kernel_size // 2, 0, kernel_size - 1])
    rr, cc = polygon(r, c)
    kernel[rr, cc] = 1.0
    return kernel


def triangle_blur(img, kernel_size: float) -> np.ndarray:
    kernel_dim = int(np.ceil(kernel_size) * 2 + 1)
    fraction = kernel_size % 1
    if fraction != 0:
        kernel = np.pad(triangle(kernel_dim), 1, mode="constant", constant_values=0.0)
        kernel += triangle(kernel_dim + 2) * fraction
        kernel = kernel.clip(0, 1)
    else:
        kernel = triangle(kernel_dim)

    return cv2.filter2D(img, -1, kernel / np.sum(kernel), borderType=cv2.BORDER_REFLECT)
