import time

import ffmpeg
from chainner_ext import resize, ResizeFilter
import numpy as np
import cv2 as cv
from screenton_maker import Screenton
from pepeline import fast_color_level, noise_generate, TypeNoise
import random
from dataset_support import sin_patern, gray_or_color

interpolation_map = {
    'nearest': ResizeFilter.Nearest,
    'box': ResizeFilter.Box,
    'hermite': ResizeFilter.Hermite,
    'hamming': ResizeFilter.Hamming,
    'linear': ResizeFilter.Linear,
    'hann': ResizeFilter.Hann,
    'lagrange': ResizeFilter.Lagrange,
    'cubic_catrom': ResizeFilter.CubicCatrom,
    'cubic_mitchell': ResizeFilter.CubicMitchell,
    'cubic_bspline': ResizeFilter.CubicBSpline,
    'lanczos': ResizeFilter.Lanczos,
    'gauss': ResizeFilter.Gauss
}
noise_map = {
    'perlinsuflet': TypeNoise.PERLINSURFLET,
    'perlin': TypeNoise.PERLIN,
    'opensimplex': TypeNoise.OPENSIMPLEX,
    'simplex': TypeNoise.SIMPLEX,
    'supersimplex': TypeNoise.SUPERSIMPLEX
}


def probability(prob: float):
    if prob > np.random.uniform(0, 1):
        return False
    else:
        return True


def max_min(img):
    max = np.max(img)
    min = np.min(img)
    return max, min


def noise_normalize(img):
    maximum, minimum = max_min(img)
    return (img - minimum) * (1 + 1) / (maximum - minimum) - 1


def graycolor(img):
    if gray_or_color(img, 0.0003):
        return img2gray(img)
    return img


def img2gray(img):
    if img.ndim != 2 and img.shape[2] != 1:
        return np.dot(img[..., :3], [0.114, 0.587, 0.299]).astype(np.float32)
    else:
        return img


class ResizeLogic:
    def __init__(self, resize_dict):
        spread = resize_dict.get("spread", [1, 1, 1])
        self.spread_arange = np.arange(spread[0], spread[1] + spread[2], spread[2])
        self.lq_algorithm = resize_dict["alg_lq"]
        self.hq_algorithm = resize_dict["alg_hq"]
        self.lq_scale = resize_dict["scale"]
        self.down_up_spread = resize_dict["down_up"]["up"]
        self.down_up_alg_up = resize_dict["down_up"]["alg_up"]
        self.down_up_alg_down = resize_dict["down_up"]["alg_down"]
        self.down_down_step = resize_dict["down_down"]["step"]
        self.down_down_alg = resize_dict["down_down"]["alg_down"]
        self.probably = resize_dict.get("prob", 1.0)
        self.color_fix = resize_dict.get("color_fix")
        self.gamma_correction = resize_dict.get("gamma_correction",False)

    def __real_size(self, size):
        return size - (size % (size // self.lq_scale * self.lq_scale))

    def __down_up(self, lq, width, height):
        up = np.random.uniform(self.down_up_spread[0], self.down_up_spread[1])
        algorithm_up = random.choice(self.down_up_alg_up)
        lq = resize(lq, (int(width * up), int(height * up)), interpolation_map[algorithm_up],
                    gamma_correction=self.gamma_correction )
        return lq

    def __down_down(self, lq, width, height, algorithm_lq):
        height_k = width / height
        step = random.randint(1, self.down_down_step)
        step = (width - width / self.lq_scale) / step
        for down in list(reversed(np.arange(int(width // self.lq_scale), int(width), int(step))))[:-1]:
            lq = resize(lq, (int(down), int(down / height_k)), interpolation_map[algorithm_lq],
                        gamma_correction=self.gamma_correction)
        return lq

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            height, width = lq.shape[:2]
            algorithm_lq = random.choice(self.lq_algorithm)
            algorithm_hq = random.choice(self.hq_algorithm)
            spread = np.random.choice(self.spread_arange)
            height = self.__real_size(height // spread)
            width = self.__real_size(width // spread)

            if algorithm_lq == "down_up":
                lq = self.__down_up(lq, width, height)
                algorithm_lq = random.choice(self.down_up_alg_down)
            if algorithm_lq == "down_down":
                algorithm_lq = random.choice(self.down_down_alg)
                lq = self.__down_down(lq, width, height, algorithm_lq)

            lq = resize(lq, (int(width // self.lq_scale), int(height // self.lq_scale)), interpolation_map[algorithm_lq],
                        gamma_correction=self.gamma_correction )
            hq = resize(hq, (int(width), int(height)), interpolation_map[algorithm_hq],
                        gamma_correction=self.gamma_correction )

            if self.color_fix:
                lq = fast_color_level(lq, 0, 250)
                hq = fast_color_level(hq, 0, 250)
            return lq, hq
        except Exception as e:
            print(f"resize error {e}")


class ScreentoneLogic:
    def __init__(self, screentone_dict):
        self.lqhq = screentone_dict.get("lqhq")
        self.dot_range = screentone_dict.get("dot_size", [7])
        color = screentone_dict.get("color")
        if color:
            self.color_b = color.get("b", [0, 0])
            self.color_g = color.get("g", [0, 0])
            self.color_r = color.get("r", [0, 0])
        self.probably = screentone_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq

            lq = np.squeeze(lq).astype(np.float32)
            dot_size = random.choice(self.dot_range)
            if np.ndim(lq) != 2:
                r, g, b = cv.split(lq)
                b = Screenton(dot_size, random.randint(self.color_b[0], self.color_b[1]),
                              random.randint(self.color_b[0], self.color_b[1])).run(b)
                g = Screenton(dot_size, random.randint(self.color_g[0], self.color_g[1]),
                              random.randint(self.color_g[0], self.color_g[1])).run(g)
                r = Screenton(dot_size, random.randint(self.color_r[0], self.color_r[1]),
                              random.randint(self.color_r[0], self.color_r[1])).run(r)
                lq = cv.merge([b, g, r])

            else:
                lq = Screenton(dot_size).run(lq)

            if self.lqhq:
                hq = lq
            return lq, hq
        except Exception as e:
            print(f"screentone error {e}")


class BlurLogic:
    def __init__(self, blur_dict):
        self.filter = blur_dict["filter"]
        self.kernel = blur_dict["kernel"]
        self.median_kernel = blur_dict.get("median_kernel")
        self.probably = blur_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            blur_method = random.choice(self.filter)
            kernel = random.randrange(self.kernel[0], self.kernel[1], self.kernel[2])
            if kernel % 2 == 0:
                kernel += 1
            match blur_method:
                case "gauss":
                    lq = cv.GaussianBlur(lq, (kernel, kernel), 0)

                case "blur":
                    lq = cv.blur(lq, (kernel, kernel))

                case "box":
                    lq = cv.boxFilter(lq, -1, (kernel, kernel))
                case "median":
                    median_kernel = self.median_kernel
                    if median_kernel:
                        median_kernel = random.randrange(median_kernel[0], median_kernel[1], median_kernel[2])
                    else:
                        median_kernel = kernel
                    if median_kernel % 2 == 0:
                        median_kernel += 1
                    lq = cv.medianBlur((lq * 255).astype(np.uint8), median_kernel).astype(np.float32) / 255
            return lq, hq
        except Exception as e:
            print(f"blur error {e}")


class Noice:
    def __init__(self, noice_dict):
        self.type_noise = noice_dict.get("type", ["uniform"])
        self.normalize_noice = noice_dict.get("normalize")
        alpha_rand = noice_dict.get("alpha", [1, 1, 1])
        self.alpha_rand = np.arange(alpha_rand[0], alpha_rand[1] + alpha_rand[2], alpha_rand[2])
        self.close = noice_dict.get("close")
        self.probably = noice_dict.get("prob", 1.0)
        octaves_range = noice_dict.get("octaves", [1, 1, 1])
        self.octaves_rand = np.arange(octaves_range[0], octaves_range[1] + octaves_range[2], octaves_range[2])
        frequency_range = noice_dict.get("frequency", [0.9, 0.9, 0.9])
        self.frequency_rand = np.arange(frequency_range[0], frequency_range[1] + frequency_range[2], frequency_range[2])
        lacunarity_range = noice_dict.get("lacunarity", [0.5, 0.5, 0.5])
        self.lacunarity_rand = np.arange(lacunarity_range[0], lacunarity_range[1] + lacunarity_range[2],
                                         lacunarity_range[2])

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            noise_type = np.random.choice(self.type_noise)

            if noise_type == "uniform":
                noice = np.random.uniform(-1, 1, lq.shape)
            else:
                noice = noise_generate(lq.shape, noise_map[noise_type], np.random.choice(self.octaves_rand),
                                       np.random.choice(self.frequency_rand), np.random.choice(self.lacunarity_rand))
            if self.normalize_noice:
                noice = noise_normalize(noice)
            noice *= np.random.choice(self.alpha_rand)
            if self.close:
                close_to_black = lq < self.close.get("black", 0.)
                close_to_white = lq > self.close.get("white", 1.)
                lq[~close_to_black & ~close_to_white] += noice[~close_to_black & ~close_to_white]
            else:
                lq += noice
            lq = np.clip(lq, 0, 1)
            return lq, hq
        except Exception as e:
            print(f"noise error {e}")


class CompressLogic:
    def __init__(self, compress_dict):
        self.compress_dict = compress_dict
        self.algorithm = compress_dict["algorithm"]
        self.compress = compress_dict.get("comp", [90, 100])
        self.target_compress = compress_dict.get("target_compress")
        self.compress_compress = compress_dict.get("compress_compress")
        self.probably = compress_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            if lq.ndim == 3 and lq.shape[2] == 3:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_RGB2BGR)
            else:
                lq = cv.cvtColor((lq * 255).astype(np.uint8), cv.COLOR_GRAY2BGR)

            if self.compress_compress:
                compress_compress = random.randint(self.compress_compress[0], self.compress_compress[1])
            else:
                compress_compress = 1
            for _ in range(compress_compress):
                algorithm = random.choice(self.algorithm)
                comp = self.compress
                if self.target_compress:
                    comp = self.target_compress.get(algorithm, comp)
                random_comp = random.randint(comp[0], comp[1])
                if algorithm == 'jpeg':
                    quality = random_comp
                    encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
                    result, encimg = cv.imencode('.jpg', lq, encode_param)
                    lq = cv.imdecode(encimg, 1).copy()

                elif algorithm == 'webp':
                    quality = random_comp
                    encode_param = [int(cv.IMWRITE_WEBP_QUALITY), quality]
                    result, encimg = cv.imencode('.webp', lq, encode_param)
                    lq = cv.imdecode(encimg, 1).copy()
                elif algorithm in ['h264', 'hevc', 'mpeg', 'mpeg2', 'vp9']:
                    # Convert image to video format
                    height, width, _ = lq.shape
                    codec = algorithm
                    container = 'mpeg'
                    if algorithm == 'mpeg':
                        codec = 'mpeg1video'

                    elif algorithm == 'mpeg2':
                        codec = 'mpeg2video'

                    elif algorithm == 'vp9':
                        codec = 'libvpx-vp9'
                        container = 'webm'
                        crf_level = random_comp
                        output_args = {'crf': str(crf_level), 'b:v': '0', 'cpu-used': '5'}

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
                    time.sleep(0.1)

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

            lq = cv.cvtColor(lq, cv.COLOR_BGR2RGB)
            return (lq / 255).astype(np.float32), hq
        except Exception as e:
            print(f"Compress error {e}")
            return lq, hq


class SaturationLossLogic:
    def __init__(self, saturation_dict):
        self.rand = saturation_dict["rand"]
        self.probably = saturation_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            random_satur = np.random.uniform(self.rand[0], self.rand[1])
            hsv_image = cv.cvtColor(lq, cv.COLOR_RGB2HSV)
            decreased_saturation = hsv_image.copy()
            decreased_saturation[:, :, 1] = decreased_saturation[:, :, 1] * random_satur
            return cv.cvtColor(decreased_saturation, cv.COLOR_HSV2RGB), hq
        except Exception as e:
            print(f"Saturation loss error {e}")


class HaloLossLogic:
    def __init__(self, halo_loss_dict):
        self.factor = halo_loss_dict["sharpening_factor"]
        self.kernel = halo_loss_dict["kernel"]
        self.laplacian = halo_loss_dict["laplacian"]
        self.probably = halo_loss_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            if np.ndim(lq) != 2:
                img_gray = cv.cvtColor(lq, cv.COLOR_RGB2GRAY)
            else:
                img_gray = lq
            sharpening_factor = random.randint(self.factor[0], self.factor[1])
            kernel_median = random.randint(self.kernel[0], self.kernel[1])
            laplacian = random.choice(self.laplacian)
            img_gray = img_gray * 255
            if kernel_median:
                img_gray = cv.blur(img_gray.astype(np.uint8), ksize=[kernel_median, kernel_median])
            laplacian = cv.Laplacian(img_gray.astype(np.uint8), cv.CV_16S, ksize=laplacian)
            sharpened_image = img_gray - sharpening_factor * laplacian
            _, sharpened_image = cv.threshold(sharpened_image, 254, 255, 0, cv.THRESH_BINARY)
            if np.ndim(lq) != 2:
                sharpened_image = np.stack([sharpened_image] * 3, axis=-1).astype(np.float32) / 255
            else:
                sharpened_image = sharpened_image.astype(np.float32) / 255
            lq = np.clip(lq + sharpened_image, 0, 1)
            return lq, hq
        except Exception as e:
            print(f"halo loss error {e}")


class ColorLossLogic:
    def __init__(self, color_loss_dict):
        self.high_list = color_loss_dict["high"]
        self.low_list = color_loss_dict["low"]
        self.gamma = color_loss_dict["gamma"]
        self.probably = color_loss_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            in_low = 0
            in_high = 255
            high_output = random.randint(self.high_list[0], self.high_list[1])
            low_output = random.randint(self.low_list[0], self.low_list[1])
            gamma_list = self.gamma
            gamma = np.random.uniform(gamma_list[0], gamma_list[1])
            lq = fast_color_level(lq, in_low=in_low, in_high=in_high, out_low=low_output, out_high=high_output,
                                  gamma=gamma)

            return lq, hq
        except Exception as e:
            print(f"Color loss error:{e}")


class SinLossLogic:
    def __init__(self, sin_loss_dict):
        self.sin_loss_dict = sin_loss_dict
        self.shape = sin_loss_dict["shape"]
        self.alpha = sin_loss_dict["alpha"]
        self.bias = sin_loss_dict["bias"]
        self.vertical_prob = sin_loss_dict["vertical"]
        self.probably = sin_loss_dict.get("prob", 1.0)

    def run(self, lq, hq):
        try:
            if probability(self.probably):
                return lq, hq
            lq = np.squeeze(lq).astype(np.float32)
            shape = random.randrange(self.shape[0], self.shape[1], self.shape[2])
            alpha = np.random.uniform(self.alpha[0], self.alpha[1])
            vertical = probability(self.vertical_prob)
            bias = np.random.uniform(self.bias[0], self.bias[1])
            lq = sin_patern(lq, shape_sin=shape, alpha=alpha, vertical=vertical, bias=bias)
            return lq, hq
        except Exception as e:
            print(f"sin loss error {e}")
