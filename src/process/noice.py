import numpy as np
from ..utils import probability, normalize
from ..constants import NOISE_MAP
from pepeline import noise_generate



class Noice:
    """
    Class for adding noise to images.

    Args:
        noice_dict (dict): A dictionary containing parameters for noise generation.
            It should have the following keys:
                - 'type' (list, optional): List of noise types to choose from. Default is ["uniform"].
                - 'normalize' (bool, optional): Whether to normalize the generated noise. Default is None.
                - 'alpha' (list, optional): Range of alpha values for noise. Default is [1, 1, 1].
                - 'close' (dict, optional): Dictionary specifying conditions for adding noise. Default is None.
                - 'prob' (float, optional): Probability of applying noise. Default is 1.0.
                - 'octaves' (list, optional): Range of octaves for noise generation. Default is [1, 1, 1].
                - 'frequency' (list, optional): Range of frequencies for noise generation. Default is [0.9, 0.9, 0.9].
                - 'lacunarity' (list, optional): Range of lacunarity values for noise generation. Default is [0.5, 0.5, 0.5].
                - 'lqhq' (bool, optional): Whether to apply the same noise to both low quality and high quality images. Default is False.

    Attributes:
        type_noise (list): List of noise types to choose from.
        normalize_noice (bool): Whether to normalize the generated noise.
        alpha_rand (numpy.ndarray): Range of alpha values for noise.
        close (dict): Dictionary specifying conditions for adding noise.
        probably (float): Probability of applying noise.
        octaves_rand (numpy.ndarray): Range of octaves for noise generation.
        frequency_rand (numpy.ndarray): Range of frequencies for noise generation.
        lacunarity_rand (numpy.ndarray): Range of lacunarity values for noise generation.
        lqhq (bool): Whether to apply the same noise to both low quality and high quality images.

    Methods:
        run(lq, hq): Method to run the noise addition process.
            Args:
                lq (numpy.ndarray): Low quality image.
                hq (numpy.ndarray): High quality image.
            Returns:
                Tuple of numpy.ndarrays: Image with added noise and original high quality image.
    """

    def __init__(self, noice_dict):
        self.type_noise = noice_dict.get("type_noice", ["uniform"])
        self.normalize_noice = noice_dict.get("normalize")
        alpha_rand = noice_dict.get("alpha", [1, 1, 1])
        self.alpha_rand = np.arange(*alpha_rand)
        self.close = noice_dict.get("close")
        self.probably = noice_dict.get("probably", 1.0)
        octaves_range = noice_dict.get("octaves", [1, 1, 1])
        self.octaves_rand = np.arange(*octaves_range)
        frequency_range = noice_dict.get("frequency", [0.9, 0.9, 0.9])
        self.frequency_rand = np.arange(*frequency_range)
        lacunarity_range = noice_dict.get("lacunarity", [0.5, 0.5, 0.5])
        self.lacunarity_rand = np.arange(*lacunarity_range)
        self.lqhq = noice_dict.get("lqhq", False)
        # self.yuv = noice_dict.get("yuv")

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            noise_type = np.random.choice(self.type_noise)
            if noise_type == "uniform":
                noice = np.random.uniform(-1, 1, lq.shape[:2])
            else:
                noice = noise_generate(lq.shape, NOISE_MAP[noise_type], np.random.choice(self.octaves_rand),
                                       np.random.choice(self.frequency_rand), np.random.choice(self.lacunarity_rand),
                                       None)
            if self.normalize_noice:
                noice = normalize(noice)
            noice *= np.random.choice(self.alpha_rand)
            if self.close:
                close_to_black = lq < self.close.get("black", 0.)
                close_to_white = lq > self.close.get("white", 1.)
                lq[~close_to_black & ~close_to_white] += noice[~close_to_black & ~close_to_white]
            else:
                lq += noice
            lq = np.clip(lq, 0, 1)

            if self.lqhq:
                hq = lq
            return lq, hq
        except Exception as e:
            print(f"noise error {e}")
