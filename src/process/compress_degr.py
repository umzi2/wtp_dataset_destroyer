import numpy as np
from numpy import random
import cv2 as cv
import sys
from .utils import probability
from time import sleep
from ..utils.random import safe_randint

from ..utils.registry import register_class
import logging

if sys.version_info < (3, 12):
    import ffmpeg
else:
    logging.warning("FFmpeg doesn't work with Python 3.12. Use an older version of Python.")

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
    """

    def __init__(self, compress_dict: dict):
        self.algorithm = compress_dict["algorithm"]
        compress = compress_dict.get("comp", [90, 100])
        target = compress_dict.get("target_compress")
        self.probability = compress_dict.get("probability", 1.0)
        if target:
            self.target_compress = {
                "jpeg": target.get("jpeg", compress),
                "webp": target.get("webp", compress),
                "h264": target.get("h264", compress),
                "hevc": target.get("hevc", compress),
                "vp9": target.get("vp9", compress),
                "mpeg": target.get("mpeg", compress),
                "mpeg2": target.get("mpeg2", compress),
            }
        else:
            self.target_compress = {
                "jpeg": compress,
                "webp": compress,
                "h264": compress,
                "hevc": compress,
                "vp9": compress,
                "mpeg": compress,
                "mpeg2": compress,
            }

    def __video_core(
        self, lq: np.ndarray, codec: str, output_args: dict, container: str = "mpeg"
    ) -> np.ndarray:
        if sys.version_info < (3, 12):
            width, height = lq.shape[:2]

            # Encode image using ffmpeg
            process1 = (
                ffmpeg.input(
                    "pipe:", format="rawvideo", pix_fmt="bgr24", s=f"{width}x{height}"
                )
                .output("pipe:", format=container, vcodec=codec, **output_args)
                .global_args(
                    "-loglevel", "fatal"
                )  # Disable error reporting because of buffer errors
                .global_args("-max_muxing_queue_size", "300000")
                .run_async(pipe_stdin=True, pipe_stdout=True)
            )
            process1.stdin.write(lq.tobytes())
            process1.stdin.flush()  # Ensure all data is written
            process1.stdin.close()

            # Add a delay between each image to help resolve buffer errors
            sleep(0.1)

            # Decode compressed video back into image format using ffmpeg
            process2 = (
                ffmpeg.input("pipe:", format=container)
                .output("pipe:", format="rawvideo", pix_fmt="bgr24")
                .global_args(
                    "-loglevel", "fatal"
                )  # Disable error reporting because of buffer errors
                .run_async(pipe_stdin=True, pipe_stdout=True)
            )

            out, _ = process2.communicate(input=process1.stdout.read())

            process1.wait()
            return (
                np.frombuffer(out, np.uint8)[: (height * width * 3)]
                .reshape(lq.shape)
                .copy()
            )
        else:
            return lq

    def __h264(self, lq: np.ndarray, quality: int) -> np.ndarray:
        output_args = {"crf": quality}
        return self.__video_core(lq, "h264", output_args)

    def __hevc(self, lq, quality):
        output_args = {"crf": quality, "x265-params": "log-level=0"}
        return self.__video_core(lq, "hevc", output_args)

    def __mpeg(self, lq: np.ndarray, quality: int) -> np.ndarray:
        output_args = {
            "qscale:v": str(quality),
            "qmax": str(quality),
            "qmin": str(quality),
        }
        return self.__video_core(lq, "mpeg1video", output_args)

    def __mpeg2(self, lq: np.ndarray, quality: int) -> np.ndarray:
        output_args = {
            "qscale:v": str(quality),
            "qmax": str(quality),
            "qmin": str(quality),
        }
        return self.__video_core(lq, "mpeg2video", output_args)

    def __jpeg(self, lq: np.ndarray, quality: int) -> np.ndarray:
        encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
        _, encimg = cv.imencode(".jpg", lq, encode_param)
        return cv.imdecode(encimg, 1).copy()

    def __vp9(self, lq: np.ndarray, quality: int) -> np.ndarray:
        output_args = {"crf": str(quality), "b:v": "0", "cpu-used": "5"}
        return self.__video_core(lq, "libvpx-vp9", output_args, "webm")

    def __webp(self, lq: np.ndarray, quality: int) -> np.ndarray:
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
            "mpeg": self.__mpeg,
            "mpeg2": self.__mpeg2,
            "vp9": self.__vp9,
        }
        try:
            if probability(self.probability):
                return lq, hq
            gray = False
            if lq.ndim == 3 and lq.shape[2] == 3:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_RGB2BGR)
            else:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_GRAY2BGR)
                gray = True

            algorithm = random.choice(self.algorithm)
            random_comp = safe_randint(self.target_compress[algorithm])
            logging.debug(
                "Compress - algorithm: %s compress: %s", algorithm, random_comp
            )
            lq = COMPRESS_TYPE_MAP[algorithm](lq, random_comp)

            if gray:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2GRAY)
            else:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2RGB)
            return (lq / 255).astype(np.float32), hq
        except Exception as e:
            logging.error("Compress error: %s", e)
