import numpy as np
import cv2


def box_blur(img: np.ndarray, kernel_size: float) -> np.ndarray:
    return cv2.filter2D(
        img, -1, __box_kernel(kernel_size), borderType=cv2.BORDER_REPLICATE
    )


def __box_kernel(kernel_size: float) -> np.ndarray:
    kernel_dim = int(np.ceil(kernel_size) * 2 + 1)
    kernel = np.ones((kernel_dim, kernel_dim), dtype=np.float32)
    fraction = kernel_size % 1
    if fraction != 0:
        kernel[0, :] *= fraction
        kernel[-1, :] *= fraction
        kernel[:, 0] *= fraction
        kernel[:, -1] *= fraction
    kernel /= np.sum(kernel)
    return kernel
