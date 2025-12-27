from typing import Any, List

import numpy as np
from logging import debug
from pepeline import jpeg_encode

from .video import video_core
from pepedd.core.objects.safe_rng import SafeRNG
import cv2


def rust_json_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    preset: List[str],
    _tune: List[str],
):
    sampling = rng.choice(sampling)
    preset = rng.choice(preset)
    debug(
        f"   Compress= jpeg\n   quality= {quality} img_shape = {preset} sampling = {sampling}"
    )
    return jpeg_encode(img.clip(0, 1), quality, preset, sampling)


def webp_encode(
    img: np.ndarray,
    _rng: SafeRNG,
    quality: int,
    _sampling: Any,
    _preset: List[str],
    _tune: List[str],
):
    encode_param = [
        int(cv2.IMWRITE_WEBP_QUALITY),
        quality,
    ]
    debug(f"   Compress= webp\n   quality= {quality}")
    img_ndim = img.ndim
    img = (img * 255.0).astype(np.uint8)
    if img_ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, encimg = cv2.imencode(".webp", img, encode_param)
    img = cv2.imdecode(encimg, 1).astype(np.float32)
    img_ndim = img.ndim
    if img_ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img.astype(np.float32) / 255.0


def j2000_encode(
    img: np.ndarray,
    _rng: SafeRNG,
    quality: int,
    _sampling: Any,
    _preset: List[str],
    _tune: List[str],
):
    encode_param = [int(cv2.IMWRITE_JPEG2000_COMPRESSION_X1000), quality * 10]
    debug(f"   Compress= j2000\n   quality= {quality}")
    img_ndim = img.ndim
    img = (img * 255.0).astype(np.uint8)
    if img_ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    _, encimg = cv2.imencode(".jp2", img, encode_param)
    img = cv2.imdecode(encimg, 1).astype(np.float32)
    # img_ndim = img.ndim
    # print(img_ndim)
    if img_ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img.astype(np.float32) / 255.0


def h264_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    preset: List[str],
    tune: List[str],
):
    output_args = [
        "-crf",
        str(quality),
        "-preset",
        rng.choice(preset),
        "-tune",
        rng.choice(tune),
    ]
    sampling = rng.choice(sampling)
    debug(f"   Compress= h264\n   args= {output_args}\n   sampling= {sampling}")
    img = video_core(img, "h264", output_args, sampling=sampling)
    return img


def h265_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    preset: List[str],
    tune: List[str],
):
    output_args = [
        "-crf",
        str(quality),
        "-preset",
        rng.choice(preset),
        "-tune",
        rng.choice(tune),
        "-x265-params",
        "log-level=0",
    ]
    sampling = rng.choice(sampling)
    debug(f"   Compress= h264\n   args= {output_args}\n   sampling= {sampling}")
    return video_core(img, "libx265", output_args, sampling=sampling)


def mpeg2_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    _preset: List[str],
    _tune: List[str],
):
    output_args = [
        "-qscale:v",
        str(quality),
        "-qmax",
        str(quality),
        "-qmin",
        str(quality),
    ]
    sampling = rng.choice(sampling)
    debug(f"   Compress= mpeg2\n   quality= {quality}\n   sampling= {sampling}")
    return video_core(img, "mpeg2video", output_args, sampling=sampling)


def mpeg4_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    _preset: List[str],
    _tune: List[str],
):
    output_args = [
        "-qscale:v",
        str(quality),
        "-qmax",
        str(quality),
        "-qmin",
        str(quality),
    ]
    sampling = rng.choice(sampling)
    debug(f"   Compress= mpeg4\n   quality= {quality}\n   sampling= {sampling}")
    return video_core(img, "mpeg4", output_args, sampling=sampling)


def vp9_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    preset: List[str],
    tune: List[str],
):
    output_args = [
        "-crf",
        str(quality),
        "-b:v",
        "0",
        "-deadline",
        str(rng.choice(preset)),
        "-tune-content",
        str(rng.choice(tune)),
    ]
    sampling = rng.choice(sampling)
    debug(f"   Compress= vp9\n   args= {output_args}\n   sampling= {sampling}")
    return video_core(
        img, "libvpx-vp9", output_args, container="webm", sampling=sampling
    )


def avif_encode(
    img: np.ndarray,
    rng: SafeRNG,
    quality: int,
    sampling: Any,
    _preset: List[str],
    _tune: List[str],
):
    output_args = ["-crf", str(quality), "-still-picture", "true"]
    sampling = rng.choice(sampling)
    debug(f"   Compress= avif\n   args= {output_args}\n   sampling= {sampling}")
    return video_core(
        img, "libaom-av1", output_args, container="ivf", sampling=sampling
    )
