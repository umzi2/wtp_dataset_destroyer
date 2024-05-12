import numpy as np
from numpy import random
import cv2 as cv
from ..utils import probability


class HaloLossLogic:
    """Class for applying halo loss reduction techniques to images.

    Args:
        halo_loss_dict (dict): A dictionary containing halo loss reduction settings.
            It should include the following keys:
                - "sharpening_factor" (list of int, optional): Range of sharpening factors.
                    Defaults to [0, 2].
                - "kernel" (list of int, optional): Range of kernel sizes.
                    Defaults to [0, 2].
                - "laplacian" (list of int, optional): List of Laplacian kernel sizes.
                    Defaults to [3].
                - "probably" (float, optional): Probability of applying halo loss reduction. Defaults to 1.0.
                - "type_halo" (list of str, optional): List of halo loss reduction types.
                    Defaults to ["laplacian"].
                - "amount" (list of float, optional): Range of amounts for unsharp mask.
                    Defaults to [1, 1].
                - "threshold" (list of float, optional): Range of thresholds for unsharp mask.
                    Defaults to [0, 0].
    """

    def __init__(self, halo_loss_dict):
        self.factor = halo_loss_dict.get("sharpening_factor", [0, 2])
        self.kernel = halo_loss_dict.get("kernel", [0, 2])
        self.laplacian = halo_loss_dict.get("laplacian", [3])
        self.probably = halo_loss_dict.get("probably", 1.0)
        self.type = halo_loss_dict.get("type_halo", ["laplacian"])
        self.amount = halo_loss_dict.get("amount", [1, 1])
        threshold = halo_loss_dict.get("threshold", [0, 0])
        self.threshold = [threshold[0] / 255, threshold[1] / 255]

    def __laplacian(self, lq):

        lq = np.squeeze(lq).astype(np.float32)
        if np.ndim(lq) != 2:
            img_gray = cv.cvtColor(lq, cv.COLOR_RGB2GRAY)
        else:
            img_gray = lq
        sharpening_factor = random.randint(*self.factor)
        kernel = random.randint(*self.kernel)[0]
        laplacian = random.choice(self.laplacian)
        img_gray = img_gray
        if kernel:
            img_gray = cv.blur(img_gray, ksize=[kernel, kernel])
        laplacian = cv.Laplacian(img_gray, cv.CV_32F, ksize=laplacian)
        sharpened_image = img_gray - sharpening_factor * laplacian
        _, sharpened_image = cv.threshold(sharpened_image, 0.98, 1, 0, cv.THRESH_BINARY)
        if np.ndim(lq) != 2:
            sharpened_image = np.stack([sharpened_image] * 3, axis=-1)
        return np.clip(lq + sharpened_image, 0, 1).astype(np.float32)

    def __unsharp_mask(self, lq):
        kernel_size = np.random.randint(*self.kernel)[0]
        amount = np.random.uniform(*self.amount)
        threshold = np.random.uniform(*self.threshold)
        if kernel_size % 2 == 0:
            kernel_size += 1

        blurred = cv.GaussianBlur(lq, (kernel_size, kernel_size), 0)
        sharpened = np.clip(float(amount + 1) * lq - float(amount) * blurred, 0, 1)
        if threshold > 0:
            low_contrast_mask = np.absolute(lq - blurred) < threshold
            np.copyto(sharpened, lq, where=low_contrast_mask)
        return sharpened

    def run(self, lq, hq):
        """Applies the selected halo loss reduction technique to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the halo loss reduced low-quality image and the corresponding high-quality image.
        """
        try:
            if probability(self.probably):
                return lq, hq
            type_halo = np.random.choice(self.type)
            if type_halo == "laplacian":
                lq = self.__laplacian(lq)
            elif type_halo == "unsharp_mask":
                lq = self.__unsharp_mask(lq)

            return lq, hq
        except Exception as e:
            print(f"halo loss error {e}")
