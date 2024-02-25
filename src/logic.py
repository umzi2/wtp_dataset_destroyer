from chainner_ext import resize, ResizeFilter
import numpy as np
import cv2 as cv
from screenton_maker import Screenton
import random


class ResizeLogic:
    def __init__(self, resize_dict):
        self.resize_dict = resize_dict

    def run(self, hq, lq):
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
            algoritm_up = random.choice(self.resize_dict["down_up"]["alg_up"])
            lq = resize(lq, (int(width * up), int(height * up)), interpolation_map[algoritm_up],
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


class ScreentonLogic:  # TODO
    def __init__(self, dot_size):
        self.dot_size = dot_size

    def run(self, img, colored):
        if colored:
            self.dot_size=random.randint(5,9)
            b, g, r = cv.split(img)
            b = Screenton(self.dot_size, random.randint(0, self.dot_size), random.randint(0, self.dot_size)).run(b)
            g = Screenton(self.dot_size, random.randint(0, self.dot_size), random.randint(0, self.dot_size)).run(g)
            r = Screenton(self.dot_size, random.randint(0, self.dot_size), random.randint(0, self.dot_size)).run(r)
            img = cv.merge([b, g, r])

            return img

        else:
            return Screenton(self.dot_size).run(img)


class SinPaternLogic:
    def __init__(self):
        pass


class BlurLogic:
    def __init__(self, blur_dict):
        self.blur_dict = blur_dict

    def run(self, img):
        img = np.squeeze(img).astype(np.float32)
        blur_method = random.choice(self.blur_dict["method"])
        kernel = self.blur_dict["kernel"]
        kernel = random.randrange(kernel[0], kernel[1], kernel[2])
        if not kernel:
            return img
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
                kernel= kernel//6
                if kernel % 2 == 0:
                    kernel += 1
                img = cv.medianBlur((img*255).astype(np.uint8), kernel).astype(np.float32)/255
        return img


class CompresLogic:
    def __init__(self, compress_dict):
        self.compress_dict = compress_dict

    def run(self, img):
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

        return img


class Halo:
    def __init__(self):
        pass

    def run(self, img):
        threshold_index = np.random.uniform(20 / 255, 51 / 255)
        kernel = random.randint(0, 8)
        gamma = np.random.uniform(0.5, 2)
        img = np.squeeze(img)

        if img.ndim != 2:
            img_gr = np.dot(img[..., :3], [0.114, 0.587, 0.299])
        else:
            img_gr = img

        _, threshold = cv.threshold(img_gr, threshold_index, 1, cv.THRESH_BINARY_INV)

        if kernel != 0:
            if kernel % 2 == 0:
                kernel += 1
            gaus = cv.GaussianBlur(threshold, (kernel, kernel), 0)
        else:
            gaus = threshold
        threshold_rash = np.clip(gaus * gamma, 0, 1)

        mask = np.clip(threshold_rash - threshold, 0, 1)

        if img.ndim != 2:
            mask = np.stack([mask] * 3, axis=-1)

        out = np.clip(img + mask, 0, 1)
        return out


class ColorLossLogic:  # TODO
    def __init__(self):
        pass

class SinLossLogic:
    def __init__(self): # TODO
        pass
