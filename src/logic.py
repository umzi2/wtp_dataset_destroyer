from chainner_ext import resize, ResizeFilter
import numpy as np
import cv2 as cv
from screenton_maker import Screenton
from pepeline import fast_color_level
import random
from dataset_support import sin_patern, gray_or_color, bit_or_gray


def graycolor(img):
    if gray_or_color(img, 0.0003):
        return img2gray(img)
    return img


def img2gray(img):
    return cv.cvtColor(img, cv.COLOR_BGR2GRAY)


class ResizeLogic:
    def __init__(self, resize_dict):
        self.resize_dict = resize_dict

    def run(self, lq, hq):
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
        height, width = lq.shape[:2]
        algorithm_lq = random.choice(self.resize_dict["alg_lq"])
        lq_scale = self.resize_dict["scale"]
        algorithm_hq = random.choice(self.resize_dict["alg_hq"])
        rrm = self.resize_dict["rand_scale"]
        rm = np.random.uniform(rrm[0], rrm[1])
        height = height // rm
        width = width // rm
        height = height - (height % (height // lq_scale * lq_scale))
        width = width - (width % (width // lq_scale * lq_scale))
        if algorithm_lq == "down_up":
            up = np.random.uniform(self.resize_dict["down_up"]["up"][0], self.resize_dict["down_up"]["up"][1])
            algorithm_up = random.choice(self.resize_dict["down_up"]["alg_up"])
            lq = resize(lq, (int(width * up), int(height * up)), interpolation_map[algorithm_up],
                        gamma_correction=False)
            algorithm_lq = random.choice(self.resize_dict["down_up"]["alg_down"])
        if algorithm_lq == "down_down":
            height_k = width / height
            step = random.randint(1, self.resize_dict["down_down"]["step"])
            step = (width - width / lq_scale) / step
            algorithm_lq = random.choice(self.resize_dict["down_down"]["alg_down"])
            for down in list(reversed(range(int(width // lq_scale), int(width), int(step))))[:-1]:
                lq = resize(lq, (int(down), int(down / height_k)), interpolation_map[algorithm_lq],
                            gamma_correction=False)
        lq = resize(lq, (int(width // lq_scale), int(height // lq_scale)), interpolation_map[algorithm_lq],
                    gamma_correction=False)
        hq = resize(hq, (int(width), int(height)), interpolation_map[algorithm_hq],
                    gamma_correction=False)
        lq = fast_color_level(lq, 0, 250)
        hq = fast_color_level(hq,0,250)
        return lq, hq


class ScreentonLogic:
    def __init__(self, screenton_dict):
        self.screenton_dict = screenton_dict

    def run(self, img, hq):
        # r = bit_or_gray(img)
        # if not r:
        #     return img,hq
        img = np.squeeze(img).astype(np.float32)
        dot_size = random.choice(self.screenton_dict["dot_size"])
        if np.ndim(img) != 2:
            b, g, r = cv.split(img)
            b = Screenton(dot_size, random.randint(self.screenton_dict["color"].get("b", [0, 0])[0],
                                                   self.screenton_dict["color"].get("b", [0, 0])[1]),
                          random.randint(self.screenton_dict["color"].get("b", [0, 0])[0],
                                         self.screenton_dict["color"].get("b", [0, 0])[1])).run(b)
            g = Screenton(dot_size, random.randint(self.screenton_dict["color"].get("g", [0, 0])[0],
                                                   self.screenton_dict["color"].get("g", [0, 0])[1]),
                          random.randint(self.screenton_dict["color"].get("g", [0, 0])[0],
                                         self.screenton_dict["color"].get("g", [0, 0])[1])).run(g)
            r = Screenton(dot_size, random.randint(self.screenton_dict["color"].get("r", [0, 0])[0],
                                                   self.screenton_dict["color"].get("r", [0, 0])[1]),
                          random.randint(self.screenton_dict["color"].get("r", [0, 0])[0],
                                         self.screenton_dict["color"].get("r", [0, 0])[1])).run(r)
            img = cv.merge([b, g, r])

        else:
            img = Screenton(dot_size).run(img)
        if self.screenton_dict["lqhq"]:
            hq = img
        return img, hq


class BlurLogic:
    def __init__(self, blur_dict):
        self.blur_dict = blur_dict

    def run(self, lq, hq):
        img = np.squeeze(lq).astype(np.float32)
        blur_method = random.choice(self.blur_dict["filter"])
        kernel = self.blur_dict["kernel"]
        kernel = random.randrange(kernel[0], kernel[1], kernel[2])
        if not kernel:
            return img, hq
        match blur_method:
            case "gauss":
                if kernel % 2 == 0:
                    kernel += 1
                img = cv.GaussianBlur(img, (kernel, kernel), 0)

            case "blur":
                img = cv.blur(img, (kernel, kernel))

            case "box":
                img = cv.boxFilter(img, -1, (kernel, kernel))
            case "median":
                median_kernel = self.blur_dict.get("median_kernel")
                if median_kernel:
                    median_kernel = random.randrange(median_kernel[0], median_kernel[1], median_kernel[2])
                else:
                    median_kernel = kernel
                if median_kernel % 2 == 0:
                    median_kernel += 1
                img = cv.medianBlur((img * 255).astype(np.uint8), median_kernel).astype(np.float32) / 255
        return img, hq


class Noice:
    def __init__(self, noice_dict):
        self.noice_dict = noice_dict

    def run(self, img, hq):
        # rr = random.choice([True,False,False,False])
        # if rr:
        #     return img,hq
        img = np.squeeze(img).astype(np.float32)
        high = self.noice_dict["rand"]
        rand_high = np.random.uniform(high[0], high[1])
        noice = np.random.uniform(rand_high * -1, rand_high, img.shape)
        close = self.noice_dict["close"]
        if close:
            close_to_black = img < close.get("black", 0.)
            close_to_white = img > close.get("white", 1.)

            img[~close_to_black & ~close_to_white] += noice[~close_to_black & ~close_to_white]
        else:
            img += noice
        img = np.clip(img, 0, 1)
        return img, hq


class CompressLogic:
    def __init__(self, compress_dict):
        self.compress_dict = compress_dict

    def run(self, img, hq):
        img = (img * 255).astype(np.uint8)
        compress_compress = self.compress_dict.get("compress_compress")
        if compress_compress:
            compress_compress = random.randint(compress_compress[0], compress_compress[1])
        else:
            compress_compress = 1
        for _ in range(compress_compress):
            algorithm = random.choice(self.compress_dict["algorithm"])
            comp = self.compress_dict["comp"]
            random_comp = random.randint(comp[0], comp[1])
            if algorithm == 'jpeg':
                quality = random_comp
                encode_param = [int(cv.IMWRITE_JPEG_QUALITY), quality]
                result, encimg = cv.imencode('.jpg', img, encode_param)
                img = cv.imdecode(encimg, 1).copy()

            elif algorithm == 'webp':
                quality = random_comp
                encode_param = [int(cv.IMWRITE_WEBP_QUALITY), quality]
                result, encimg = cv.imencode('.webp', img, encode_param)
                img = cv.imdecode(encimg, 1).copy()

        return (img / 255).astype(np.float32), hq


class HaloLossLogic:
    def __init__(self, halo_loss_dict):
        self.halo_loss_dict = halo_loss_dict

    def run(self, img, hq):
        img = np.squeeze(img).astype(np.float32)
        factor = self.halo_loss_dict["sharpening_factor"]
        # rr = random.choice([True,False,False,False,False,False,False])
        # if rr:
        #     return img,hq
        if not factor:
            return img, hq
        k_median = self.halo_loss_dict["kernel_median"]
        box_k = self.halo_loss_dict["box_kernel"]
        sharpening_factor = random.randint(factor[0], factor[1])
        kernel_median = random.randint(k_median[0], k_median[1])
        box_kernel = random.randint(box_k[0], box_k[1])
        laplacian = random.choice(self.halo_loss_dict["laplacian"])
        img = img * 255
        if kernel_median:
            if kernel_median % 2 == 0:
                kernel_median += 1

            img = cv.medianBlur(img.astype(np.uint8), ksize=kernel_median)
        laplacian = cv.Laplacian(img.astype(np.uint8), cv.CV_16S, ksize=laplacian)

        sharpened_image = img - sharpening_factor * laplacian

        sharpened_image = np.clip(sharpened_image, 0, 255).astype(np.uint8)
        if not box_kernel:
            return sharpened_image / 255, hq
        return cv.boxFilter(sharpened_image, -1, ksize=(box_kernel, box_kernel)) / 255, hq


class NewHaloLossLogic:
    def __init__(self, halo_loss_dict):
        self.halo_loss_dict = halo_loss_dict

    def run(self, img, hq):
        # rr = random.choice([True,False,False,False])
        # if rr:
        #     return img,hq
        img = np.squeeze(img).astype(np.float32)
        if np.ndim(img) != 2:
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        else:
            img_gray = img
        factor = self.halo_loss_dict["sharpening_factor"]
        if not factor:
            return img, hq
        k_median = self.halo_loss_dict["kernel"]
        sharpening_factor = random.randint(factor[0], factor[1])
        kernel_median = random.randint(k_median[0], k_median[1])
        laplacian = random.choice(self.halo_loss_dict["laplacian"])
        img_gray = img_gray * 255
        if kernel_median:
            img_gray = cv.blur(img_gray.astype(np.uint8), ksize=[kernel_median, kernel_median])
        laplacian = cv.Laplacian(img_gray.astype(np.uint8), cv.CV_16S, ksize=laplacian)
        sharpened_image = img_gray - sharpening_factor * laplacian
        _, sharpened_image = cv.threshold(sharpened_image, 254, 255, 0, cv.THRESH_BINARY)
        if np.ndim(img) != 2:
            sharpened_image = np.stack([sharpened_image] * 3, axis=-1).astype(np.float32) / 255
        else:
            sharpened_image = sharpened_image.astype(np.float32) / 255
        img = np.clip(img + sharpened_image, 0, 1)
        return img, hq


class ColorLossLogic:
    def __init__(self, color_loss_dict):
        self.color_loss_dict = color_loss_dict

    def run(self, img, hq):
        img = np.squeeze(img).astype(np.float32)
        in_low = 0
        in_high = 255
        high_list = self.color_loss_dict["high"]
        high_output = random.randint(high_list[0], high_list[1])

        low_list = self.color_loss_dict["low"]
        low_output = random.randint(low_list[0], low_list[1])

        gamma_list = self.color_loss_dict["gamma"]
        gamma = np.random.uniform(gamma_list[0], gamma_list[1])
        img = fast_color_level(img, in_low=in_low, in_high=in_high, out_high=high_output, out_low=low_output, gamma=gamma)

        return img, hq


class SinLossLogic:
    def __init__(self, sin_loss_dict):
        self.sin_loss_dict = sin_loss_dict

    def run(self, img, hq):
        img = np.squeeze(img).astype(np.float32)
        shape = self.sin_loss_dict["shape"]
        alpha = self.sin_loss_dict["alpha"]
        bias = self.sin_loss_dict["bias"]
        shape = random.randrange(shape[0], shape[1], shape[2])
        alpha = np.random.uniform(alpha[0], alpha[1])
        vertical = random.choice(self.sin_loss_dict["vertical"])
        bias = np.random.uniform(bias[0], bias[1])
        img = sin_patern(img, shape_sin=shape, alpha=alpha, vertical=vertical, bias=bias)
        return img, hq
