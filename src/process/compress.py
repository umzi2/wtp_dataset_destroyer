import numpy as np
from numpy import random
import cv2 as cv
import ffmpeg
from ..utils import probability
from time import sleep


class CompressLogic:
    """
    Class for compressing images or videos using various algorithms and target compressions.

    Args:
        compress_dict (dict): A dictionary containing compression parameters.
            It should have the following keys:
                - 'algorithm' (list): List of compression algorithms to be used.
                - 'comp' (list, optional): Range of compression values. Default is [90, 100].
                - 'target_compress' (dict, optional): Dictionary specifying target compressions for each algorithm.
                    Default is None.
                - 'compress_compress' (list, optional): Range of compression compression. Default is None.
                - 'prob' (float, optional): Probability of applying compression. Default is 1.0.

    Attributes:
        compress_dict (dict): Dictionary containing compression parameters.
        algorithm (list): List of compression algorithms to be used.
        target_compress (dict): Dictionary specifying target compressions for each algorithm.
        compress_compress (list): Range of compression compression.
        probably (float): Probability of applying compression.

    Methods:
        run(lq, hq): Method to run the compression process.
            Args:
                lq (numpy.ndarray): Low quality image or video.
                hq (numpy.ndarray): High quality image or video.
            Returns:
                Tuple of numpy.ndarrays: Compressed low quality image or video and high quality image or video.
    """
    def __init__(self, compress_dict):
        self.compress_dict = compress_dict
        self.algorithm = compress_dict["algorithm"]
        compress = compress_dict.get("comp", [90, 100])
        target = compress_dict.get("target_compress")
        self.compress_compress = compress_dict.get("compress_compress")
        self.probably = compress_dict.get("probably", 1.0)
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

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            gray = False
            if lq.ndim == 3 and lq.shape[2] == 3:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_RGB2BGR)
            else:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_GRAY2BGR)

            if self.compress_compress:
                compress_compress = random.randint(*self.compress_compress)
            else:
                compress_compress = 1
            for _ in range(compress_compress):
                algorithm = random.choice(self.algorithm)
                random_comp = random.randint(*self.target_compress[algorithm])
                if algorithm == 'jpeg':
                    quality = random_comp
                    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
                    _, encimg = cv.imencode('.jpg', lq, encode_param)
                    lq = cv.imdecode(encimg, 1).copy()

                elif algorithm == 'webp':
                    quality = random_comp
                    encode_param = [int(cv.IMWRITE_WEBP_QUALITY), quality]
                    _, encimg = cv.imencode('.webp', lq, encode_param)
                    lq = cv.imdecode(encimg, 1).copy()
                elif algorithm in ['h264', 'hevc', 'mpeg', 'mpeg2', 'vp9']:
                    # Convert image to video format
                    height, width, _ = lq.shape
                    codec = algorithm
                    container = 'mpeg'
                    if algorithm == 'h264':
                        crf_level = random_comp
                        output_args = {'crf': crf_level}

                    elif algorithm == 'hevc':
                        crf_level = random_comp
                        output_args = {'crf': crf_level, 'x265-params': 'log-level=0'}

                    elif algorithm == 'mpeg':
                        qscale_level = str(random_comp)
                        output_args = {'qscale:v': str(qscale_level), 'qmax': str(qscale_level),
                                       'qmin': str(qscale_level)}

                    elif algorithm == 'mpeg2':
                        qscale_level = str(random_comp)
                        output_args = {'qscale:v': str(qscale_level), 'qmax': str(qscale_level),
                                       'qmin': str(qscale_level)}

                    elif algorithm == 'vp9':
                        codec = 'libvpx-vp9'
                        container = 'webm'
                        crf_level = random_comp
                        output_args = {'crf': str(crf_level), 'b:v': '0', 'cpu-used': '5'}
                    else:
                        raise ValueError(f"Unknown algorithm: {algorithm}")

                        # Encode image using ffmpeg
                    process1 = (
                        ffmpeg
                        .input('pipe:', format='rawvideo', pix_fmt='bgr24', s=f'{width}x{height}')
                        .output('pipe:', format=container, vcodec=codec, **output_args)
                        .global_args('-loglevel', 'fatal')  # Disable error reporting because of buffer errors
                        .global_args('-max_muxing_queue_size', '300000')
                        .run_async(pipe_stdin=True, pipe_stdout=True)
                    )
                    process1.stdin.write(lq.tobytes())
                    process1.stdin.flush()  # Ensure all data is written
                    process1.stdin.close()

                    # Add a delay between each image to help resolve buffer errors
                    sleep(0.1)

                    # Decode compressed video back into image format using ffmpeg
                    process2 = (
                        ffmpeg
                        .input('pipe:', format=container)
                        .output('pipe:', format='rawvideo', pix_fmt='bgr24')
                        .global_args('-loglevel', 'fatal')  # Disable error reporting because of buffer errors
                        .run_async(pipe_stdin=True, pipe_stdout=True)
                    )

                    out, err = process2.communicate(input=process1.stdout.read())

                    process1.wait()

                    lq = np.frombuffer(out, np.uint8)[:(height * width * 3)].reshape(lq.shape).copy()
            if gray:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2GRAY)
            else:
                lq = cv.cvtColor(lq, cv.COLOR_BGR2RGB)
            return (lq / 255).astype(np.float32), hq
        except Exception as e:
            print(f"Compress error {e}")
            return lq, hq
