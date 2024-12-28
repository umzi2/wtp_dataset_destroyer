import cv2
from chainner_ext import ResizeFilter
from pepeline import TypeNoise, CvtType, TypeDot
from chainner_ext import DiffusionAlgorithm

INTERPOLATION_MAP = {
    "nearest": ResizeFilter.Nearest,
    "box": ResizeFilter.Box,
    "hermite": ResizeFilter.Hermite,  # strong artifacts can cause
    # "hamming": ResizeFilter.Hamming,
    "linear": ResizeFilter.Linear,
    # 'hann': ResizeFilter.Hann,#strong artifacts can cause
    "lagrange": ResizeFilter.Lagrange,
    "cubic_catrom": ResizeFilter.CubicCatrom,
    "cubic_mitchell": ResizeFilter.CubicMitchell,
    "cubic_bspline": ResizeFilter.CubicBSpline,
    "lanczos": ResizeFilter.Lanczos,
    "gauss": ResizeFilter.Gauss,
}
NOISE_MAP = {
    "perlinsuflet": TypeNoise.PERLINSURFLET,
    "perlin": TypeNoise.PERLIN,
    "opensimplex": TypeNoise.OPENSIMPLEX,
    "simplex": TypeNoise.SIMPLEX,
    "supersimplex": TypeNoise.SUPERSIMPLEX,
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

SUBSAMPLING_MAP = {
    "4:4:4": [1, 1, 1],
    "4:2:2": [1, 0.5, 1],
    "4:2:1": [1, 0.5, 0.5],
    "4:1:1": [1, 0.25, 1],
    "4:2:0": [1, 0.5, 0.5],
    "4:1:0": [1, 0.25, 0.5],
    "3:1:1": [0.75, 0.25, 0.75],
}
YUV_MAP = {
    "2020": [CvtType.RGB2YCvCrBt2020, CvtType.YCvCr2RGBBt2020],
    "601": [CvtType.RGB2YCbCr, CvtType.YCbCr2RGB],
    "709": [CvtType.RGB2YCvCrBt709, CvtType.YCvCr2RGBBt709],
}
JPEG_SUBSAMPLING = {
    "4:4:4": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_444,
    "4:4:0": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_440,
    "4:2:2": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_422,
    "4:2:0": cv2.IMWRITE_JPEG_SAMPLING_FACTOR_420,
}
VIDEO_SUBSAMPLING = {"444": "yuv444p", "422": "yuv422p", "420": "yuv420p"}
DOT_TYPE = {
    "line": TypeDot.LINE,
    "cross": TypeDot.CROSS,
    "circle": TypeDot.CIRCLE,
    "ellipse": TypeDot.ELLIPSE,
}
