from chainner_ext import ResizeFilter
from pepeline import TypeNoise
from chainner_ext import DiffusionAlgorithm
INTERPOLATION_MAP = {
    'nearest': ResizeFilter.Nearest,
    'box': ResizeFilter.Box,
    # 'hermite': ResizeFilter.Hermite,#strong artifacts can cause
    'hamming': ResizeFilter.Hamming,
    'linear': ResizeFilter.Linear,
    # 'hann': ResizeFilter.Hann,#strong artifacts can cause
    'lagrange': ResizeFilter.Lagrange,
    'cubic_catrom': ResizeFilter.CubicCatrom,
    'cubic_mitchell': ResizeFilter.CubicMitchell,
    'cubic_bspline': ResizeFilter.CubicBSpline,
    'lanczos': ResizeFilter.Lanczos,
    'gauss': ResizeFilter.Gauss
}
NOISE_MAP = {
    'perlinsuflet': TypeNoise.PERLINSURFLET,
    'perlin': TypeNoise.PERLIN,
    'opensimplex': TypeNoise.OPENSIMPLEX,
    'simplex': TypeNoise.SIMPLEX,
    'supersimplex': TypeNoise.SUPERSIMPLEX
}
DITHERING_MAP = {
            "floydsteinberg": DiffusionAlgorithm.FloydSteinberg,
            "jarvisjudiceninke": DiffusionAlgorithm.JarvisJudiceNinke,
            "stucki": DiffusionAlgorithm.Stucki,
            "atkinson": DiffusionAlgorithm.Atkinson,
            "burkes": DiffusionAlgorithm.Burkes,
            "sierra": DiffusionAlgorithm.Sierra,
            "tworowsierra": DiffusionAlgorithm.TwoRowSierra,
            "sierraLite": DiffusionAlgorithm.SierraLite,

        }
