import numpy as np
from numpy import random
import cv2 as cv
from ..utils import probability


class HaloLossLogic:
    """
    Class for applying halo loss to images using different techniques.

    Args:
        halo_loss_dict (dict): A dictionary containing parameters for halo loss.
            It should have the following keys:
                - 'sharpening_factor' (int, optional): Range of sharpening factors. Default is None.
                - 'kernel' (list, optional): Range of kernel sizes. Default is [0, 2].
                - 'laplacian' (list): List of Laplacian filter sizes.
                - 'prob' (float, optional): Probability of applying halo loss. Default is 1.0.
                - 'type_halo' (list, optional): List of halo loss types to choose from. Default is ["laplacian"].
                - 'amount' (list, optional): Range of amounts for unsharp masking. Default is [1, 1].
                - 'threshold' (list, optional): Range of thresholds for unsharp masking. Default is [0, 0].

    Attributes:
        factor (int): Range of sharpening factors.
        kernel (list): Range of kernel sizes.
        laplacian (list): List of Laplacian filter sizes.
        probably (float): Probability of applying halo loss.
        type (list): List of halo loss types to choose from.
        amount (list): Range of amounts for unsharp masking.
        threshold (list): Range of thresholds for unsharp masking.

    Methods:
        run(lq, hq): Method to run the halo loss process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Processed low quality image and original high quality image.
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
