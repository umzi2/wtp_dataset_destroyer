import numpy as np
from ..utils import probability, normalize
from ..constants import NOISE_MAP
from pepeline import noise_generate, cvt_color, CvtType


class Noice:
    """Class for adding noise to images.

        Args:
            noice_dict (dict): A dictionary containing noise settings.
                It should include the following keys:
                    - "probably" (float, optional): Probability of adding noise. Defaults to 1.0.
                    - "type_noice" (list of str, optional): List of noise types to choose from.
                        Defaults to ["uniform"].
                    - "alpha" (list of int, optional): Range of alpha values for noise intensity.
                        Defaults to [1, 2, 1].
                    - "lqhq" (bool, optional): Flag indicating if the low-quality image should be replaced by the noisy one.
                        Defaults to False.
                    - "y_noice" (bool, optional): Flag indicating if noise should be added to the Y channel only (for YUV images).
                        Defaults to None.
                    - "uv_noice" (bool, optional): Flag indicating if noise should be added to the UV channels only (for YUV images).
                        Defaults to None.
                    - "normalize" (bool, optional): Flag indicating if the generated noise should be normalized. Defaults to None.
                    - "octaves" (list of int, optional): Range of octaves for procedural noises.
                        Defaults to [1, 2, 1].
                    - "frequency" (list of float, optional): Range of frequencies for procedural noises.
                        Defaults to [0.8, 0.9, 0.9].
                    - "lacunarity" (list of float, optional): Range of lacunarity values for procedural noises.
                        Defaults to [0.4, 0.5, 0.5].
                    - "probably_salt_or_pepper" (list of float, optional): Range of probabilities for salt-and-pepper noise.
                        Defaults to [0, 0.5].
        """

    def __init__(self, noice_dict):

        # common
        self.probably = noice_dict.get("probably", 1.0)
        self.type_noise = noice_dict.get("type_noice", ["uniform"])
        alpha_rand = noice_dict.get("alpha", [1, 2, 1])
        self.alpha_rand = np.arange(*alpha_rand)
        self.lqhq = noice_dict.get("lqhq", False)
        self.y_noice = noice_dict.get("y_noice")
        self.uv_noice = noice_dict.get("uv_noice")
        self.noise_type = "perlin"

        # procedural_noises
        self.normalize_noice = noice_dict.get("normalize")
        octaves_range = noice_dict.get("octaves", [1, 2, 1])
        self.octaves_rand = np.arange(*octaves_range)
        frequency_range = noice_dict.get("frequency", [0.8, 0.9, 0.9])
        self.frequency_rand = np.arange(*frequency_range)
        lacunarity_range = noice_dict.get("lacunarity", [0.4, 0.5, 0.5])
        self.lacunarity_rand = np.arange(*lacunarity_range)
        # salt_or_pepper
        self.probably_salt_or_pepper = noice_dict.get("probably_salt_or_pepper", [0, 0.5])

    def __procedural_noises(self, lq):
        noice = noise_generate(lq.shape, NOISE_MAP[self.noise_type],
                               np.random.choice(self.octaves_rand),
                               np.random.choice(self.frequency_rand),
                               np.random.choice(self.lacunarity_rand),
                               None)
        if self.normalize_noice:
            noice = normalize(noice)
        noice *= np.random.choice(self.alpha_rand)
        return lq + noice

    def __gauss(self, lq):
        noice = np.random.normal(0, 0.25, lq.shape)
        noice *= np.random.choice(self.alpha_rand)
        return (lq + noice).astype(np.float32)

    def __uniform_noice(self, lq):
        noice = np.random.uniform(-1, 1, lq.shape)
        noice *= np.random.choice(self.alpha_rand)
        return (lq + noice).astype(np.float32)

    # Salt_and_pepper noices
    def __salt_and_pepper_core(self, img_shape):
        noice = np.random.uniform(0, 1, img_shape)
        probably = np.random.uniform(*self.probably_salt_or_pepper)
        return noice, probably

    def __salt_and_pepper(self, lq):
        noice, probably = self.__salt_and_pepper_core(lq.shape)
        lq = np.where(noice > probably, lq, 1)
        return np.where(noice < 1 - probably, lq, 0).astype(np.float32)

    def __salt(self, lq):
        noice, probably = self.__salt_and_pepper_core(lq.shape)
        return np.where(noice > probably, lq, 1).astype(np.float32)

    def __pepper(self, lq):
        noice, probably = self.__salt_and_pepper_core(lq.shape)
        return np.where(noice < 1 - probably, lq, 0).astype(np.float32)

    # Run module
    def run(self, lq, hq):
        """Adds noise to the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the noisy low-quality image and the corresponding high-quality image.
        """
        NOICE_TYPE_MAP = {

            "perlinsuflet": self.__procedural_noises,
            "perlin": self.__procedural_noises,
            "opensimplex": self.__procedural_noises,
            "simplex": self.__procedural_noises,
            "supersimplex": self.__procedural_noises,
            "uniform": self.__uniform_noice,
            "gauss": self.__gauss,
            "salt": self.__salt,
            "pepper": self.__pepper,
            "salt_and_pepper": self.__salt_and_pepper

        }
        try:
            if probability(self.probably):
                return lq, hq
            yuv = False
            if lq.ndim == 3:

                if self.y_noice:
                    yuv = True
                    yuv_img = cvt_color(lq, CvtType.RGB2YCvCrBt2020)
                    lq = yuv_img[:, :, 0]
                    uv = yuv_img[:, :, 1:]
                elif self.uv_noice:
                    yuv = True
                    yuv_img = cvt_color(lq, CvtType.RGB2YCvCrBt2020)
                    lq = yuv_img[:, :, 1:]
                    y = yuv_img[:, :, 0]
            self.noise_type = np.random.choice(self.type_noise)
            lq = NOICE_TYPE_MAP[self.noise_type](lq)
            lq = np.clip(lq, 0, 1)
            if yuv:
                if self.y_noice:
                    lq = np.stack((lq, uv[:, :, 0], uv[:, :, 1]), axis=-1)
                    lq = cvt_color(lq, CvtType.YCvCr2RGBBt2020)
                elif self.uv_noice:
                    lq = np.stack((y, lq[:, :, 0], lq[:, :, 1]), axis=-1)
                    lq = cvt_color(lq, CvtType.YCvCr2RGBBt2020)

            if self.lqhq:
                hq = lq
            return lq, hq
        except Exception as e:
            print(f"noise error {e}")
