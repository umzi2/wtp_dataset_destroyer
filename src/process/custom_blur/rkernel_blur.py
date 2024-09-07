import numpy as np
import cv2


def random_kernel_blur(img: np.ndarray, kernel_size: float) -> np.ndarray:
    kernel_size = int(np.ceil(kernel_size) * 2 + 1)
    kernel = np.random.uniform(0, 1, [kernel_size, kernel_size])
    kernel /= np.sum(kernel)
    return cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REFLECT)
