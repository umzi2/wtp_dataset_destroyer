import subprocess

import numpy as np


def video_core(
    img: np.ndarray,
    codec: str,
    output_args: list,
    container: str = "mpeg",
    sampling="yuv420p_neighbor",
) -> np.ndarray:
    img_ndim = img.ndim
    if img_ndim == 3:
        pix_fmt = "gbrpf32le"
        img = img.transpose(2, 0, 1)
        channel, height, width = img.shape
    else:
        pix_fmt = "grayf32le"
        channel = 1
        height, width = img.shape
    sampling, interp = sampling.split("_")
    process1 = subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-threads",
            "0",
            "-y",
            "-f",
            "rawvideo",
            "-pix_fmt",
            pix_fmt,
            "-s",
            f"{width}x{height}",
            "-r",
            "30/1",
            "-i",
            "pipe:",
            "-c:v",
            codec,
            "-an",
            "-f",
            container,
            "-pix_fmt",
            sampling,
        ]
        + output_args
        + ["pipe:"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
    )

    process1.stdin.write(img.tobytes())
    process1.stdin.flush()
    process1.stdin.close()
    process2 = subprocess.Popen(
        [
            "ffmpeg",
            "-loglevel",
            "quiet",
            "-threads",
            "0",
            "-f",
            container,
            "-i",
            "pipe:",
            "-vf",
            f"scale=iw:ih:flags={interp}",
            "-pix_fmt",
            pix_fmt,
            "-f",
            "image2pipe",
            "-vframes",
            "1",
            "-vcodec",
            "rawvideo",
            "pipe:",
        ],
        stdin=process1.stdout,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    raw_frame = process2.stdout.read()[: (height * width * channel * 4)]
    process2.stdout.close()
    process2.stderr.close()
    process1.wait()
    process2.wait()
    frame_data = (
        np.frombuffer(raw_frame, dtype=np.float32)
        .reshape((channel, height, width))
        .squeeze()
    )
    if img_ndim == 3:
        frame_data = frame_data.transpose(1, 2, 0)
    return frame_data.copy()
