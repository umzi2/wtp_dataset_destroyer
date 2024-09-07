import io
import numpy as np
from av import AVError
from numpy import random
import cv2 as cv
import av
from .utils import probability

from ..constants import JPEG_SUBSAMPLING
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
        compress = compress_dict.get("comp", [90, 100])
        target = compress_dict.get("target_compress")
        self.probability = compress_dict.get("probability", 1.0)
        self.jpeg_sampling = compress_dict.get("jpeg_sampling", ["4:2:2"])
        if "hevc" in self.algorithm:
            logging.warning(
                'HEVC encoding in pyav often causes errors such as pts<dts or memory segmentation errors. '
                'If you have solutions or insights, please let us know.'
            )
        if target:
            self.target_compress = {
                "jpeg": target.get("jpeg", compress),
                "webp": target.get("webp", compress),
                "h264": target.get("h264", compress),
                "hevc": target.get("hevc", compress),
                "av1": target.get("av1", compress),
                "vp9": target.get("vp9", compress),
                "mpeg": target.get("mpeg", compress),
                "mpeg2": target.get("mpeg2", compress),
            }
        else:
            self.target_compress = {
                "jpeg": compress,
                "webp": compress,
                "av1": compress,
                "h264": compress,
                "hevc": compress,
                "vp9": compress,
                "mpeg": compress,
                "mpeg2": compress,
            }

    def __video_core(
            self, lq: np.ndarray, codec: str, output_args: dict, container: str = "mpeg"
    ) -> np.ndarray:
        """Compresses a video frame using the specified codec and parameters.

        Args:
            lq (numpy.ndarray): The input video frame in RGB format.
            codec (str): The codec to use for compression (e.g., "h264", "hevc").
            output_args (dict): Additional parameters for the codec.
            container (str, optional): The container format. Defaults to "mpeg".

        Returns:
            numpy.ndarray: The compressed video frame in RGB format.
        """
        frame = av.VideoFrame.from_ndarray(lq, format="bgr24")
        encoded_buffer = io.BytesIO()
        output_container = av.open(encoded_buffer, 'w', format=container)
        stream = output_container.add_stream(codec, rate=1)
        stream.width = frame.width
        stream.height = frame.height
        stream.pix_fmt = 'yuv420p'
        stream.options = output_args
        for packet in stream.encode(frame):
            output_container.mux(packet)
        for packet in stream.encode():
            output_container.mux(packet)
        output_container.close()
        encoded_buffer.seek(0)
        input_container = av.open(encoded_buffer, 'r')
        input_stream = input_container.streams.video[0]
        for frame in input_container.decode(input_stream):
            numpy_frame = frame.to_ndarray(format='bgr24')
        input_container.close()
        return numpy_frame

    def __h264(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using H.264 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = {"crf": str(quality)}
        return self.__video_core(lq, "h264", output_args)

    def __hevc(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using HEVC codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image, or the original if an error occurs.
        """
        output_args = {"crf": str(quality), "x265-params": "log-level=0"}
        try:
            return self.__video_core(lq, "hevc", output_args)
        except AVError:
            return lq

    def __av1(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using AV1 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = {"crf": str(quality), "preset": "0"}
        return self.__video_core(lq, 'av1', output_args, 'webm')

    def __mpeg2(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using MPEG-2 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = {
            "qscale:v": str(quality),
            "qmax": str(quality),
            "qmin": str(quality),
        }
        return self.__video_core(lq, "mpeg2video", output_args)

    def __jpeg(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using JPEG format.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        jpeg_sampling = random.choice(self.jpeg_sampling)
        encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality, cv.IMWRITE_JPEG_SAMPLING_FACTOR,
                        JPEG_SUBSAMPLING[jpeg_sampling]]
        logging.debug(
            f"Compress - jpeg sampling: {jpeg_sampling}"
        )
        _, encimg = cv.imencode(".jpg", lq, encode_param)
        return cv.imdecode(encimg, 1).copy()

    def __vp9(self, lq: np.ndarray, quality: int) -> np.ndarray:
        """Compresses an image using VP9 codec.

        Args:
            lq (numpy.ndarray): The input image in RGB format.
            quality (int): The quality level for compression.

        Returns:
            numpy.ndarray: The compressed image.
        """
        output_args = {"crf": str(quality), "b:v": "0", "cpu-used": "5"}
        return self.__video_core(lq, "libvpx-vp9", output_args, "webm")

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
            "av1": self.__av1,
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
