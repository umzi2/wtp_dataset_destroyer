from chainner_ext import resize, ResizeFilter
import numpy as np
import cv2 as cv
from screenton_maker import Screenton
import random
from dataset_support import sin_patern, color_levels


def graycolor(img):
    r, g, b = cv.split(img)

    rg = np.mean(r - g)
    gb = np.mean(g - b)
    if rg == gb:
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
            'linear': ResizeFilter.Linear,
            'catrom': ResizeFilter.CubicCatrom,
            'mitchell': ResizeFilter.CubicMitchell,
            'bspline': ResizeFilter.CubicBSpline,
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
        return lq, hq


class ScreentonLogic:
    def __init__(self, screenton_dict):
        self.screenton_dict = screenton_dict

    def run(self, img, hq):
        img = np.squeeze(img).astype(np.float32)
        dot_size = self.screenton_dict["dot_size"]
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
                if kernel % 2 == 0:
                    kernel += 1
                img = cv.medianBlur((img * 255).astype(np.uint8), median_kernel).astype(np.float32) / 255
        return img, hq


class Noice:
    def __init__(self, noice_dict):
        self.noice_dict = noice_dict

    def run(self, img, hq):
        img = np.squeeze(img).astype(np.float32)
        high = self.noice_dict["rand"]
        rand_high = np.random.uniform(high[0], high[1])
        noice = np.random.uniform(rand_high * -1, rand_high, img.shape)

        # close_to_black = img < 0.1
        # close_to_white = img > 0.9
        #
        # img[~close_to_black & ~close_to_white] += noice[~close_to_black & ~close_to_white]
        img = np.clip(img + noice, 0, 1)
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
        img = np.squeeze(img)
        factor = self.halo_loss_dict["sharpening_factor"]
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
            return sharpened_image / 255
        return cv.boxFilter(sharpened_image, -1, ksize=(box_kernel, box_kernel)) / 255, hq


class ColorLossLogic:
    def __init__(self, color_loss_dict):
        self.color_loss_dict = color_loss_dict

    def run(self, img, hq):
        img = np.squeeze(img)
        in_low = 0.
        in_high = 1.
        high_list = self.color_loss_dict["high"]
        high_output = random.randint(high_list[0], high_list[1]) / 255

        low_list = self.color_loss_dict["low"]
        low_output = random.randint(low_list[0], low_list[1]) / 255

        gamma_list = self.color_loss_dict["gamma"]
        gamma = np.random.uniform(gamma_list[0], gamma_list[1])
        img = color_levels(img, in_low=in_low, in_high=in_high, out_high=high_output, out_low=low_output, gamma=gamma)
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
