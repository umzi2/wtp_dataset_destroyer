from functools import partial
from typing import Any

import numpy as np

from .comp_funcs import (
    webp_encode,
    j2000_encode,
    h264_encode,
    mpeg2_encode,
    mpeg4_encode,
    vp9_encode,
    avif_encode,
    rust_json_encode,
)
from .comp_maps import JpegSamplings, InterpolationMap, QuantizeTables
from .schemas import (
    CompressOptions,
    H264SPF,
    H264Preset,
    H264Tune,
    H265Preset,
    H265Tune,
    H265SPF,
    MPEG2SPF,
    MPEG4SPF,
    VP9SPF,
    VP9Preset,
    VP9Tune,
    AVIFSPF,
)
from pepedd.core.node_register import register_class
from pepedd.core.objects.lq_hq_state import LQHQState
from pepedd.core.objects.node_base import Node
from pepedd.core.objects.safe_rng import SafeRNG


def base_compress(
    img: np.ndarray,
    rng: SafeRNG,
    quality_range: list[int],
    sampling: Any,
    preset: list[str],
    tune: list[str],
    func: Any,
):
    return func(img, rng, rng.safe_randint(quality_range), sampling, preset, tune)


def validate_video_sampling(samplings: list[str], validate: list[str]):
    result = []
    validate_set = set(validate)
    for s in samplings:
        s_split = s.split("_")
        mode = s_split[0]

        if mode in validate_set:
            interpolate = "neighbor"
            if len(s_split) > 1:
                key = s_split[1]
                interpolate = InterpolationMap.get(key, "neighbor")

            result.append(f"{mode}_{interpolate}")

    if not result:
        return [f"{validate[0]}_neighbor"]
    return result


def validate_video_pt(values: list[str], validate: list[str]):
    result = []
    validate_set = set(validate)
    for v in values:
        if v in validate_set:
            result.append(v)
    if not result:
        return [validate[0]]
    return result


@register_class("compress")
class Compress(Node):
    def __init__(self, options: CompressOptions | dict):
        if isinstance(options, dict):
            opts = CompressOptions(**options)
        else:
            opts = options
        super().__init__(opts.probability, opts.seed)
        self.compress_list = []
        for alg in opts.algorithm:
            match alg:
                case "jpeg":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.jpeg,
                            sampling=[
                                JpegSamplings[sampling] for sampling in opts.samplings
                            ],
                            preset=[QuantizeTables[qt] for qt in opts.quantize_table],
                            tune=[],
                            func=rust_json_encode,
                        )
                    )
                case "webp":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.webp,
                            sampling=[],
                            preset=[],
                            tune=[],
                            func=webp_encode,
                        )
                    )
                case "j2000":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.j2000,
                            sampling=[],
                            preset=[],
                            tune=[],
                            func=j2000_encode,
                        )
                    )
                case "h264":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.h264,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, H264SPF
                            ),
                            preset=validate_video_pt(opts.preset, H264Preset),
                            tune=validate_video_pt(opts.tune, H264Tune),
                            func=h264_encode,
                        )
                    )
                case "hevc":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.hevc,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, H265SPF
                            ),
                            preset=validate_video_pt(opts.preset, H265Preset),
                            tune=validate_video_pt(opts.tune, H265Tune),
                            func=h264_encode,
                        )
                    )
                case "mpeg2":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.mpeg2,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, MPEG2SPF
                            ),
                            preset=[],
                            tune=[],
                            func=mpeg2_encode,
                        )
                    )
                case "mpeg4":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.mpeg4,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, MPEG4SPF
                            ),
                            preset=[],
                            tune=[],
                            func=mpeg4_encode,
                        )
                    )
                case "vp9":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.vp9,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, VP9SPF
                            ),
                            preset=validate_video_pt(opts.preset, VP9Preset),
                            tune=validate_video_pt(opts.tune, VP9Tune),
                            func=vp9_encode,
                        )
                    )
                case "avif":
                    self.compress_list.append(
                        partial(
                            base_compress,
                            quality_range=opts.target_compress.avif,
                            sampling=validate_video_sampling(
                                opts.ffmpeg_samplings, AVIFSPF
                            ),
                            preset=[],
                            tune=[],
                            func=avif_encode,
                        )
                    )

    def forward(self, data: LQHQState) -> LQHQState:
        data.lq = data.rng.choice(self.compress_list)(data.lq.clip(0, 1), data.rng)
        return data
