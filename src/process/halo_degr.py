import numpy as np
from chainner_ext import binary_threshold
import cv2 as cv
from .utils import probability
from ..utils.random import safe_uniform
from ..utils.registry import register_class
import logging


@register_class("halo")
class Halo:
    """Class for applying halo loss reduction techniques to images.

    Args:
        halo_loss_dict (dict): A dictionary containing halo loss reduction settings.
            It should include the following keys:
                - "kernel" (list of int, optional): Range of kernel sizes.
                    Defaults to [0, 2].
                - "probability" (float, optional): Probability of applying halo loss reduction. Defaults to 1.0.
                - "type_halo" (list of str, optional): List of halo loss reduction types.
                    Defaults to ["laplacian"].
                - "amount" (list of float, optional): Range of amounts for unsharp mask.
                    Defaults to [1, 1].
                - "threshold" (list of float, optional): Range of thresholds for unsharp mask.
                    Defaults to [0, 0].
    """

    def __init__(self, halo_loss_dict: dict):
        self.kernel = halo_loss_dict.get("kernel", [0, 2])
        self.probability = halo_loss_dict.get("probability", 1.0)
        self.amount = halo_loss_dict.get("amount", [1, 1])
        threshold = halo_loss_dict.get("threshold", [0, 0])
        self.threshold = [threshold[0] / 255, threshold[1] / 255]
        self.type = halo_loss_dict.get("type_halo", ["unsharp_mask"])

    # Removed because unsharp_halo produces similar results

    # def __laplacian(self, lq: np.ndarray) -> np.ndarray:
    #     if np.ndim(lq) != 2:
    #         img_gray = cv.cvtColor(lq, cv.COLOR_RGB2GRAY)
    #     else:
    #         img_gray = lq
    #     sharpening_factor = safe_uniform(self.factor)
    #     kernel = safe_uniform(self.kernel)
    #     laplacian = random.choice(self.laplacian)
    #     logging.debug(
    #         "Halo: type: laplacian sharpening_factor: %.4f kernel: %.4f laplacian_size: %s",
    #         sharpening_factor,
    #         kernel,
    #         laplacian,
    #     )
    #     if kernel:
    #         img_gray = box_blur(img_gray, kernel)
    #     laplacian = cv.Laplacian(img_gray, cv.CV_32F, ksize=laplacian)
    #     sharpened_image = img_gray - sharpening_factor * laplacian
    #     _, sharpened_image = cv.threshold(sharpened_image, 0.98, 1, 0, cv.THRESH_BINARY)
    #     if np.ndim(lq) != 2:
    #         sharpened_image = np.stack([sharpened_image] * 3, axis=-1)
    #     return np.clip(lq + sharpened_image, 0, 1).astype(np.float32)
    def __unsharp_gray(self, lq: np.ndarray) -> np.ndarray:
        rgb = False
        if lq.ndim == 3:
            lq_gray = cv.cvtColor(lq, cv.COLOR_RGB2GRAY)
            rgb = True
        sigma = safe_uniform(self.kernel)
        amount = safe_uniform(self.amount)

        blurred = cv.GaussianBlur(
            lq_gray, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
        )
        diff = lq_gray - blurred
        diff = np.maximum(0, np.sign(diff) * np.abs(diff)) * amount
        if rgb:
            lq[..., 0] = lq[..., 0] + diff
            lq[..., 1] = lq[..., 1] + diff
            lq[..., 2] = lq[..., 2] + diff
        else:
            lq = lq + diff
        return np.clip(lq, 0, 1)

    def __unsharp_mask(self, lq: np.ndarray) -> np.ndarray:
        sigma = safe_uniform(self.kernel)
        amount = safe_uniform(self.amount)
        threshold = safe_uniform(self.threshold)
        logging.debug(
            "Halo: type: unsharp_mask amount: %.4f kernel: %.4f  threshold: %.4f",
            amount,
            sigma,
            threshold,
        )
        blurred = cv.GaussianBlur(
            lq, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
        )
        if threshold == 0:
            lq = cv.addWeighted(lq, amount + 1, blurred, -amount, 0)
        else:
            diff = lq - blurred
            diff = np.sign(diff) * np.maximum(0, np.abs(diff) - threshold)
            lq = lq + diff * amount

        return lq

    def __unsharp_halo(self, lq):
        rgb = False
        if lq.ndim == 3:
            lq_gray = cv.cvtColor(lq, cv.COLOR_RGB2GRAY)
            rgb = True
        sigma = safe_uniform(self.kernel)
        amount = safe_uniform(self.amount)
        logging.debug(
            "Halo: type: unsharp_halo amount: %.4f kernel: %.4f ",
            amount,
            sigma,
        )
        blurred = cv.GaussianBlur(
            lq_gray, (0, 0), sigmaX=sigma, sigmaY=sigma, borderType=cv.BORDER_REFLECT
        )
        diff = lq_gray - blurred
        diff = np.maximum(0, np.sign(diff) * np.abs(diff))
        diff = binary_threshold(diff * amount, 254 / 255, False).squeeze()
        if rgb:
            lq[..., 0] = np.minimum(1, lq[..., 0] + diff)
            lq[..., 1] = np.minimum(1, lq[..., 1] + diff)
            lq[..., 2] = np.minimum(1, lq[..., 2] + diff)
        else:
            lq = np.minimum(1, lq + diff)
        return lq

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Applies the selected halo loss reduction technique to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the halo loss reduced low-quality image and the corresponding high-quality image.
        """
        try:
            if probability(self.probability):
                return lq, hq
            type_halo = np.random.choice(self.type)
            if type_halo == "unsharp_mask":
                lq = self.__unsharp_mask(lq)
            elif type_halo == "unsharp_gray":
                lq = self.__unsharp_gray(lq)
            else:
                lq = self.__unsharp_halo(lq)

            return lq, hq
        except Exception as e:
            logging.error("Halo error: %s", e)
