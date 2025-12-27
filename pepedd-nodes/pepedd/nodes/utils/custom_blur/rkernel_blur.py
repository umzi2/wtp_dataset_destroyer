import numpy as np
import cv2

from pepedd.core.objects.safe_rng import SafeRNG


def random_kernel_blur(img: np.ndarray, kernel_size: float, rng: SafeRNG) -> np.ndarray:
    kernel_size = int(np.ceil(kernel_size) * 2 + 1)
    kernel = rng.uniform(0, 1, [kernel_size, kernel_size])
    kernel /= np.sum(kernel)
    return cv2.filter2D(img, -1, kernel, borderType=cv2.BORDER_REFLECT)
