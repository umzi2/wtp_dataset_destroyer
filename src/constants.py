from chainner_ext import ResizeFilter
from pepeline import TypeNoise

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
