from typing import Literal, Optional, Annotated, List, get_args
from pydantic import BaseModel, Field, model_validator


AlgorithmType = Literal[
    "jpeg", "webp", "h264", "hevc", "mpeg2", "mpeg4", "vp9", "avif", "j2000", "bd"
]
SamplingType = Literal["444", "440", "441", "422", "420", "411", "410"]
QTType = Literal["default", "flat", "mssim", "psnr", "im", "ksc", "dxr", "vdm", "idm"]
CompressRange = Annotated[List[int], Field(min_length=2, max_length=2)]
H264SPF = [
    "yuv420p",
    "yuvj420p",
    "yuv422p",
    "yuvj422p",
    "yuv444p",
    "yuvj444p",
    "nv12",
    "nv16",
    "nv21",
    "yuv420p10le",
    "yuv422p10le",
    "yuv444p10le",
    "nv20le",
    "gray",
    "gray10le",
]
H264Preset = [
    "ultrafast",
    "superfast",
    "veryfast",
    "faster",
    "fast",
    "medium",
    "slow",
    "slower",
    "veryslow",
    "placebo",
]
H264Tune = [
    "film",
    "animation",
    "grain",
    "stillimage",
    "fastdecode",
    "zerolatency",
    "psnr",
    "ssim",
]

H265SPF = [
    "yuv420p",
    "yuvj420p",
    "yuv422p",
    "yuvj422p",
    "yuv444p",
    "yuvj444p",
    "gbrp",
    "yuv420p10le",
    "yuv422p10le",
    "yuv444p10le",
    "gbrp10le",
    "yuv420p12le",
    "yuv422p12le",
    "yuv444p12le",
    "gbrp12le",
    "gray",
    "gray10le",
    "gray12le",
]
H265Preset = [
    "ultrafast",
    "superfast",
    "veryfast",
    "faster",
    "fast",
    "medium",
    "slow",
    "slower",
    "veryslow",
    "placebo",
]
H265Tune = ["psnr", "ssim", "grain", "zerolatency", "fastdecode"]

MPEG2SPF = ["yuv420p", "yuv422p"]
MPEG4SPF = ["yuv420p"]

VP9SPF = [
    "yuv420p",
    "yuva420p",
    "yuv422p",
    "yuv440p",
    "yuv444p",
    "yuv420p10le",
    "yuv422p10le",
    "yuv440p10le",
    "yuv444p10le",
    "yuv420p12le",
    "yuv422p12le",
    "yuv440p12le",
    "yuv444p12le",
    "gbrp",
    "gbrp10le",
    "gbrp12le",
]
VP9Preset = ["best", "realtime", "good"]
VP9Tune = ["default", "screen", "film"]

AVIFSPF = [
    "yuv420p",
    "yuv422p",
    "yuv444p",
    "gbrp",
    "yuv420p10le",
    "yuv422p10le",
    "yuv444p10le",
    "yuv420p12le",
    "yuv422p12le",
    "yuv444p12le",
    "gbrp10le",
    "gbrp12le",
    "gray",
    "gray10le",
    "gray12le",
]


class TargetCompress(BaseModel):
    jpeg: Optional[CompressRange] = None
    webp: Optional[CompressRange] = None
    h264: Optional[CompressRange] = None
    hevc: Optional[CompressRange] = None
    mpeg2: Optional[CompressRange] = None
    mpeg4: Optional[CompressRange] = None
    vp9: Optional[CompressRange] = None
    avif: Optional[CompressRange] = None
    j2000: Optional[CompressRange] = None
    bd: Optional[CompressRange] = None


class CompressOptions(BaseModel):
    algorithm: List[AlgorithmType] = ["avif"]
    samplings: List[SamplingType] = ["444", "440", "422", "420", "411"]
    ffmpeg_samplings: List[str] = [
        "yuv420p_b",
        "yuv420p_c",
        "yuv420p_l",
        "yuv420p_s",
        "yuv420p_g",
        "yuv420p_a",
        "yuv422p_b",
        "yuv422p_c",
        "yuv422p_l",
        "yuv422p_s",
        "yuv422p_g",
        "yuv422p_a",
        "yuv444p_b",
        "yuv444p_c",
        "yuv444p_l",
        "yuv444p_s",
        "yuv444p_g",
        "yuv444p_a",
        "yuv420p10le_b",
        "yuv420p10le_c",
        "yuv420p10le_l",
        "yuv420p10le_s",
        "yuv420p10le_g",
        "yuv420p10le_a",
        "yuv422p10le_b",
        "yuv422p10le_c",
        "yuv422p10le_l",
        "yuv422p10le_s",
        "yuv422p10le_g",
        "yuv422p10le_a",
        "yuv444p10le_b",
        "yuv444p10le_c",
        "yuv444p10le_l",
        "yuv444p10le_s",
        "yuv444p10le_g",
        "yuv444p10le_a",
        "yuv420p12le_b",
        "yuv420p12le_c",
        "yuv420p12le_l",
        "yuv420p12le_s",
        "yuv420p12le_g",
        "yuv420p12le_a",
        "yuv422p12le_b",
        "yuv422p12le_c",
        "yuv422p12le_l",
        "yuv422p12le_s",
        "yuv422p12le_g",
        "yuv422p12le_a",
        "yuv444p12le_b",
        "yuv444p12le_c",
        "yuv444p12le_l",
        "yuv444p12le_s",
        "yuv444p12le_g",
        "yuv444p12le_a",
    ]
    compress: CompressRange = [40, 100]
    quantize_table: List[QTType] = ["default"]
    target_compress: TargetCompress = TargetCompress()
    preset: List[str] = ["faster"]
    tune: List[str] = ["grain"]
    probability: float = 1.0
    seed: Optional[int] = None

    @model_validator(mode="after")
    def fill_target_compress(self):
        alg_fields = set(get_args(AlgorithmType))
        target_dict = self.target_compress.model_dump()
        for field in alg_fields:
            if target_dict[field] is None:
                target_dict[field] = self.compress
        self.target_compress = TargetCompress(**target_dict)
        return self
