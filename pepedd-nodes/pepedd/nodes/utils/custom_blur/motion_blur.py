import numpy as np
import cv2


def motion_blur(img: np.ndarray, size: int, angle: float) -> np.ndarray:
    if size == 0:
        return img
    k = np.zeros((size, size), dtype=np.float32)
    k[(size - 1) // 2, :] = np.ones(size, dtype=np.float32)
    k = cv2.warpAffine(
        k,
        cv2.getRotationMatrix2D((size / 2 - 0.5, size / 2 - 0.5), angle, 1.0),
        (size, size),
    )
    k *= 1.0 / np.sum(k)

    return cv2.filter2D(img, -1, k)
