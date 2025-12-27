from functools import partial
from typing import List

import cv2
from pepeline import PaletteAlg, get_palette
import numpy as np
from chainner_ext import UniformQuantization, PaletteQuantization

from pepedd.core.objects.safe_rng import SafeRNG
from logging import debug


def to_std_lab(img_rgb_f32):
    lab = cv2.cvtColor(img_rgb_f32, cv2.COLOR_RGB2Lab)
    lab[..., 0] /= 100.0
    lab[..., 1] = (lab[..., 1] + 128) / 255.0
    lab[..., 2] = (lab[..., 2] + 128) / 255.0
    return lab


def from_std_lab(lab_f32):
    res = lab_f32.copy()
    res[..., 0] *= 100.0
    res[..., 1] = res[..., 1] * 255.0 - 128
    res[..., 2] = res[..., 2] * 255.0 - 128
    img_rgb = cv2.cvtColor(res, cv2.COLOR_Lab2RGB)
    return np.clip(img_rgb, 0, 1)


def get_popularity_palette(img: np.ndarray, img_colors: int):
    debug(f"   colors_in_img: {img_colors} palette_alg: popularity")
    pixels = img.reshape(-1, 3)
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    popular_indices = np.argsort(-counts)
    actual_k = min(len(colors), img_colors)
    top_indices = popular_indices[:actual_k]
    return PaletteQuantization(colors[top_indices].reshape(1, -1, 3))


def get_l_popularity_palette(img: np.ndarray, img_colors: int):
    debug(f"   colors_in_img: {img_colors} palette_alg: lab popularity")
    img = to_std_lab(img)
    pixels = img.reshape(-1, 3)
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    popular_indices = np.argsort(-counts)
    actual_k = min(len(colors), img_colors)
    top_indices = popular_indices[:actual_k]
    return PaletteQuantization(from_std_lab(colors[top_indices].reshape(1, -1, 3)))


def palette(img: np.ndarray, img_colors: int, palette_alg: PaletteAlg):
    debug(f"   colors_in_img: {img_colors} palette_alg: {palette_alg.__repr__()}")
    return PaletteQuantization(get_palette(img, img_colors, palette_alg))


def l_palette(img: np.ndarray, img_colors: int, palette_alg: PaletteAlg):
    debug(f"   colors_in_img: {img_colors} palette_alg: lab {palette_alg.__repr__()}")
    return PaletteQuantization(
        from_std_lab(get_palette(to_std_lab(img), img_colors, palette_alg))
    )


def uniform_quantize(_img: np.ndarray, img_colors: int):
    img_color = int(img_colors ** (1 / 3))
    debug(f"   colors_in_ch: {img_colors} palette_alg: uniform")
    return UniformQuantization(img_color)


ModeToPalette = {
    "oc_tree": partial(palette, palette_alg=PaletteAlg.OcTree),
    "median_cut": partial(palette, palette_alg=PaletteAlg.MedianCut),
    "wu": partial(palette, palette_alg=PaletteAlg.Wu),
    "min_max_uniform": partial(palette, palette_alg=PaletteAlg.MinMaxUniform),
    "uniform": uniform_quantize,
    "l_oc_tree": partial(l_palette, palette_alg=PaletteAlg.OcTree),
    "l_median_cut": partial(l_palette, palette_alg=PaletteAlg.MedianCut),
    "l_wu": partial(l_palette, palette_alg=PaletteAlg.Wu),
    "l_min_max_uniform": partial(l_palette, palette_alg=PaletteAlg.MinMaxUniform),
    "popular": get_popularity_palette,
    "l_popular": get_l_popularity_palette,
}


class PaletteAndUniform:
    def __init__(self, modes: List[str], img_colors: List[int]):
        self.models = []
        self.img_colors = img_colors
        for mode in modes:
            self.models.append(ModeToPalette[mode])

    def __call__(
        self, img: np.ndarray, rng: SafeRNG
    ) -> PaletteQuantization | UniformQuantization:
        return self.forward(img, rng)

    def forward(
        self, img: np.ndarray, rng: SafeRNG
    ) -> PaletteQuantization | UniformQuantization:
        img_color = rng.safe_randint(self.img_colors)
        return rng.choice(self.models)(img, img_color)
