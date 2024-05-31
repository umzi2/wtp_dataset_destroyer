import numpy as np
from .utils import probability, normalize_noise as normalize
from ..constants import NOISE_MAP
from pepeline import noise_generate, cvt_color, CvtType
from ..utils.random import safe_uniform, safe_arange

from ..utils.registry import register_class
import logging


@register_class("noise")
class Noise:
    """Class for adding noise to images.

    Args:
        noise_dict (dict): A dictionary containing noise settings.
            It should include the following keys:
                - "probability" (float, optional): Probability of adding noise. Defaults to 1.0.
                - "type_noise" (list of str, optional): List of noise types to choose from.
                    Defaults to ["uniform"].
                - "alpha" (list of int, optional): Range of alpha values for noise intensity.
                    Defaults to [1, 2, 1].
                - "lqhq" (bool, optional): Flag indicating if the low-quality image should be replaced by the noisy one.
                    Defaults to False.
                - "y_noise" (bool, optional): Flag indicating if noise should be added
                to the Y channel only (for YUV images).
                    Defaults to None.
                - "uv_noise" (bool, optional): Flag indicating if noise should be added
                to the UV channels only (for YUV images).
                    Defaults to None.
                - "normalize" (bool, optional): Flag indicating if the generated noise should be normalized.
                Defaults to None.
                - "octaves" (list of int, optional): Range of octaves for procedural noises.
                    Defaults to [1, 2, 1].
                - "frequency" (list of float, optional): Range of frequencies for procedural noises.
                    Defaults to [0.8, 0.9, 0.9].
                - "lacunarity" (list of float, optional): Range of lacunarity values for procedural noises.
                    Defaults to [0.4, 0.5, 0.5].
                - "probability_salt_or_pepper" (list of float, optional): Range of probabilities for salt-and-pepper noise.
                    Defaults to [0, 0.5].
    """

    def __init__(self, noise_dict: dict):
        # common
        self.probability = noise_dict.get("probability", 1.0)
        self.type_noise = noise_dict.get("type_noise", ["uniform"])
        alpha_rand = noise_dict.get("alpha", [1, 2, 1])
        self.alpha_rand = safe_arange(alpha_rand)
        self.lqhq = noise_dict.get("lqhq", False)
        self.y_noise = noise_dict.get("y_noise", 0)
        self.uv_noise = noise_dict.get("uv_noise", 0)
        self.noise_type = "perlin"

        # procedural_noises
        self.normalize_noise = noise_dict.get("normalize")
        octaves_range = noise_dict.get("octaves", [1, 2, 1])
        self.octaves_rand = safe_arange(octaves_range)
        frequency_range = noise_dict.get("frequency", [0.8, 0.9, 0.9])
        self.frequency_rand = safe_arange(frequency_range)
        lacunarity_range = noise_dict.get("lacunarity", [0.4, 0.5, 0.5])
        self.lacunarity_rand = safe_arange(lacunarity_range)

        self.bias = noise_dict.get("bias", [0, 0])
        # salt_or_pepper
        self.percentage_salt_or_pepper = noise_dict.get(
            "probability_salt_or_pepper", [0, 0.5]
        )
        self.default_debug = "Noise - color_type: gray"

    def __procedural_noises(self, lq: np.ndarray) -> np.ndarray:
        octaves = np.random.choice(self.octaves_rand)
        frequency = np.random.choice(self.frequency_rand)
        lacunarity = np.random.choice(self.lacunarity_rand)
        noise = noise_generate(
            lq.shape,
            NOISE_MAP[self.noise_type],
            octaves,
            frequency,
            lacunarity,
            None,
        )
        if self.normalize_noise:
            noise = normalize(noise)
        bias = 0
        if self.bias != [0, 0]:
            bias = safe_uniform(self.bias)
            noise += bias
            noise.clip(-1, 1)
        alpha = np.random.choice(self.alpha_rand)
        noise *= alpha
        logging.debug("%s noise_type: %s alpha: %.4f bias: %.4f octaves: %s frequency: %.4f lacunarity: %.4f",
                      self.default_debug, self.noise_type, alpha, bias, octaves, frequency, lacunarity)
        return lq + noise

    def __gauss(self, lq: np.ndarray) -> np.ndarray:
        noise = np.random.normal(0, 0.25, lq.shape)
        bias = 0
        if self.bias != [0, 0]:
            bias = safe_uniform(self.bias)
            noise += bias
            noise.clip(-1, 1)
        alpha = np.random.choice(self.alpha_rand)
        noise *= alpha
        logging.debug("%s noise_type: %s alpha: %.4f bias: %.4f",
                      self.default_debug, self.noise_type, alpha, bias)
        return (lq + noise).astype(np.float32)

    def __uniform_noise(self, lq: np.ndarray) -> np.ndarray:
        noise = np.random.uniform(-1, 1, lq.shape)
        bias = 0
        if self.bias != [0, 0]:
            bias = safe_uniform(self.bias)
            noise += bias
            noise.clip(-1, 1)
        alpha = np.random.choice(self.alpha_rand)
        noise *= alpha
        logging.debug("%s noise_type: %s alpha: %.4f bias: %.4f",
                      self.default_debug, self.noise_type, alpha, bias)

        return (lq + noise).astype(np.float32)

    # Salt_and_pepper noises
    def __salt_and_pepper_core(self, img_shape: tuple) -> (np.ndarray, float):
        noise = np.random.uniform(0, 1, img_shape)
        probability_sp = safe_uniform(self.percentage_salt_or_pepper)
        return noise, probability_sp

    def __salt_and_pepper(self, lq: np.ndarray) -> np.ndarray:
        noise, probability_sp = self.__salt_and_pepper_core(lq.shape)
        logging.debug("%s noise_type: %s probability: %.4f",
                      self.default_debug, self.noise_type, probability_sp)
        lq = np.where(noise > probability_sp, lq, 1)
        return np.where(noise < 1 - probability_sp, lq, 0).astype(np.float32)

    def __salt(self, lq: np.ndarray) -> np.ndarray:
        noise, probability_sp = self.__salt_and_pepper_core(lq.shape)
        logging.debug("%s noise_type: %s probability: %.4f",
                      self.default_debug, self.noise_type, probability_sp)
        return np.where(noise > probability_sp, lq, 1).astype(np.float32)

    def __pepper(self, lq: np.ndarray) -> np.ndarray:
        noise, probability_sp = self.__salt_and_pepper_core(lq.shape)
        logging.debug("%s noise_type: %s probability: %.4f",
                      self.default_debug, self.noise_type, probability_sp)
        return np.where(noise < 1 - probability_sp, lq, 0).astype(np.float32)

    # Run module
    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Adds noise to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the noisy low-quality image and the corresponding high-quality image.
        """
        NOISE_TYPE_MAP = {
            "perlinsuflet": self.__procedural_noises,
            "perlin": self.__procedural_noises,
            "opensimplex": self.__procedural_noises,
            "simplex": self.__procedural_noises,
            "supersimplex": self.__procedural_noises,
            "uniform": self.__uniform_noise,
            "gauss": self.__gauss,
            "salt": self.__salt,
            "pepper": self.__pepper,
            "salt_and_pepper": self.__salt_and_pepper,
        }
        try:
            if probability(self.probability):
                return lq, hq
            y = False
            uv = False
            if lq.ndim == 3:

                if not probability(self.y_noise):
                    y = True
                    yuv_img = cvt_color(lq, CvtType.RGB2YCvCrBt2020)
                    lq = yuv_img[:, :, 0]
                    uv_array = yuv_img[:, :, 1:]
                    self.default_debug = "Noise - color_type: y"
                elif not probability(self.uv_noise):
                    uv = True
                    yuv_img = cvt_color(lq, CvtType.RGB2YCvCrBt2020)
                    lq = yuv_img[:, :, 1:]
                    y_array = yuv_img[:, :, 0]
                    self.default_debug = "Noise - color_type: uv"
                else:
                    self.default_debug = "Noise - color_type: rgb"
            self.noise_type = np.random.choice(self.type_noise)
            lq = NOISE_TYPE_MAP[self.noise_type](lq)
            lq = np.clip(lq, 0, 1)
            if y:
                lq = np.stack((lq, uv_array[:, :, 0], uv_array[:, :, 1]), axis=-1)
                lq = cvt_color(lq, CvtType.YCvCr2RGBBt2020)
            elif uv:
                lq = np.stack((y_array, lq[:, :, 0], lq[:, :, 1]), axis=-1)
                lq = cvt_color(lq, CvtType.YCvCr2RGBBt2020)

            if self.lqhq:
                hq = lq
            return lq, hq
        except Exception as e:
            logging.error("Noise error: %s", e)
