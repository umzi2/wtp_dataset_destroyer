# https://github.com/umzi2/Float-lens-blur
import numpy as np
import cv2
from astropy.convolution import TrapezoidDisk2DKernel


def lens_blur(image: np.ndarray, dimension: float) -> np.ndarray:
    if dimension == 0:
        return image
    kernel = disk_kernel(dimension)
    convolved = cv2.filter2D(image, -1, kernel, borderType=cv2.BORDER_REFLECT)
    return convolved


def disk_kernel(kernel_size: float) -> np.ndarray:
    kernel_dim = int(np.ceil(kernel_size) * 2 + 1)
    kernel = TrapezoidDisk2DKernel(kernel_size).array.astype(np.float32)
    h = kernel.shape[0]
    x = (h - kernel_dim) // 2
    kernel = kernel[x : kernel_dim - x + 2, x : kernel_dim - x + 2]
    kernel /= np.sum(kernel)
    return kernel
