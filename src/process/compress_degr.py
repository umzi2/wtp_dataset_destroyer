import subprocess

import numpy as np
from numpy import random
import cv2 as cv
from .utils import probability

from ..constants import JPEG_SUBSAMPLING, VIDEO_SUBSAMPLING
from ..utils.random import safe_randint
from ..utils.registry import register_class
import logging


@register_class("compress")
class Compress:
    """Class for compressing images or videos using various algorithms and parameters.

    Args:
        compress_dict (dict): A dictionary containing compression settings.
            It should include the following keys:
                - "algorithm" (list of str): List of compression algorithms to be used.
                - "comp" (list of int, optional): Range of compression values for algorithms. Defaults to [90, 100].
                - "target_compress" (dict, optional): Target compression values for specific algorithms.
                    Defaults to None.
                - "probability" (float, optional): Probability of applying compression. Defaults to 1.0.
                - "jpeg_sampling" (list of str, optional): List of JPEG subsampling factors. Defaults to ["4:2:2"].
    """

    def __init__(self, compress_dict: dict):
        self.algorithm = compress_dict["algorithm"]
        compress = compress_dict.get("compress", [90, 100])
        target = compress_dict.get("target_compress")
        self.probability = compress_dict.get("probability", 1.0)
        self.jpeg_sampling = compress_dict.get("jpeg_sampling", ["4:2:2"])
        self.video_sampling = compress_dict.get("video_sampling", ["444", "422", "420"])
        if target:
            self.target_compress = {
                "jpeg": target.get("jpeg", compress),
                "webp": target.get("webp", compress),
                "h264": target.get("h264", compress),
                "hevc": target.get("hevc", compress),
                "vp9": target.get("vp9", compress),
                "mpeg2": target.get("mpeg2", compress),
                "mpeg4": target.get("mpeg4", compress),
            }
        else:
            self.target_compress = {
                "jpeg": compress,
                "webp": compress,
                "h264": compress,
                "hevc": compress,
                "vp9": compress,
                "mpeg2": compress,
                "mpeg4":  compress,
            }

    def __video_core(
        self, lq: np.ndarray, codec: str, output_args: list, container: str = "mpeg"
    ) -> np.ndarray:
        height, width, channel = lq.shape
        sampling = VIDEO_SUBSAMPLING[random.choice(self.video_sampling)]
        process1 = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-threads", "0",
                "-y",
                "-f",
                "rawvideo",
                "-pix_fmt",
                "rgb24",
                "-s",
                f"{width}x{height}",
                "-r",
                "30",
                "-i",
                "pipe:",
                "-vcodec",
                codec,
                "-an",
                "-f",
                container,
                "-pix_fmt",
                f"{sampling}",
            ]
            + output_args
            + ["pipe:"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

        process1.stdin.write(lq.tobytes())
        process1.stdin.flush()
        process1.stdin.close()

        process2 = subprocess.Popen(
            [
                "ffmpeg",
                "-loglevel",
                "error",
                "-threads", "0",
                "-f",
                container,
                "-i",
                "pipe:",
                "-pix_fmt",
                "rgb24",
                "-f",
                "image2pipe",
                "-vcodec",
                "rawvideo",
                "pipe:",
            ],
            stdin=process1.stdout,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        raw_frame = process2.stdout.read()[:(height * width * channel)]
        process2.stdout.close()
        process2.stderr.close()
        process1.wait()
        process2.wait()
        frame_data = np.frombuffer(raw_frame, dtype=np.uint8).reshape(
            (height, width, channel)
        )
        logging.debug(f"Blur - {codec} subsampling: {sampling}")
        return frame_data

    def __h264(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using H.264 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = ["-crf", str(quality)]
        output_img = self.__video_core(lq, "h264", output_args)
        return output_img

    def __hevc(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using HEVC codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image, or the original if an error occurs.
        """
        output_args = ["-crf", str(quality), "-x265-params", "log-level=0"]

        return self.__video_core(lq, "hevc", output_args)

    def __mpeg2(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using MPEG-2 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = [
            "-qscale:v",
            str(quality),
            "-qmax",
            str(quality),
            "-qmin",
            str(quality),
        ]
        output_img = self.__video_core(lq, "mpeg2video", output_args)
        return output_img
    def __mpeg4(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using MPEG-2 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = [
            "-qscale:v",
            str(quality),
            "-qmax",
            str(quality),
            "-qmin",
            str(quality),
        ]
        output_img = self.__video_core(lq, "mpeg4", output_args)
        return output_img
    def __vp9(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using VP9 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = ["-crf", str(quality), "-b:v", "0"]
        output_img = self.__video_core(lq, "libvpx-vp9", output_args, "webm")
        return output_img

    def __jpeg(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using JPEG format.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        jpeg_sampling = random.choice(self.jpeg_sampling)
        encode_param = [
            int(cv.IMWRITE_JPEG_QUALITY),
            quality,
            cv.IMWRITE_JPEG_SAMPLING_FACTOR,
            JPEG_SUBSAMPLING[jpeg_sampling],
        ]
        logging.debug(f"Compress - jpeg sampling: {jpeg_sampling}")
        _, encimg = cv.imencode(".jpg", lq, encode_param)
        return cv.imdecode(encimg, 1).copy()

    def __webp(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using WebP format.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        encode_param = [int(cv.IMWRITE_WEBP_QUALITY), quality]
        _, encimg = cv.imencode(".webp", lq, encode_param)
        return cv.imdecode(encimg, 1).copy()

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray, np.ndarray):
        """Compresses the input image.

        Args:
            lq (numpy.ndarray): The low-quality image.
            hq (numpy.ndarray): The corresponding high-quality image.

        Returns:
            tuple: A tuple containing the compressed low-quality image
                and the corresponding high-quality image.
        """
        COMPRESS_TYPE_MAP = {
            "jpeg": self.__jpeg,
            "webp": self.__webp,
            "h264": self.__h264,
            "hevc": self.__hevc,
            "mpeg2": self.__mpeg2,
            "mpeg4": self.__mpeg4,
            "vp9": self.__vp9,
        }
        try:
            if probability(self.probability):
                return lq, hq
            gray = False
            if lq.ndim == 3 and lq.shape[2] == 3:
                lq = (lq * 255.0).astype(np.uint8)
                lq = cv.cvtColor(lq, cv.COLOR_RGB2BGR)
            else:
                lq = cv.cvtColor((lq * 255.0).astype(np.uint8), cv.COLOR_GRAY2BGR)
                gray = True

            algorithm = random.choice(self.algorithm)
            random_comp = safe_randint(self.target_compress[algorithm])
            logging.debug(f"Compress - algorithm: {algorithm} compress: {random_comp}")
            lq = COMPRESS_TYPE_MAP[algorithm](lq, random_comp)

            if gray:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2GRAY)
            else:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2RGB)
            return lq.astype(np.float32) / 255.0, hq
        except Exception as e:
            logging.error(f"Compress error: {e}")
