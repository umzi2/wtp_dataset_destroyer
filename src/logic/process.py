import os

from tqdm.contrib.concurrent import process_map, thread_map
from ..utils import color_or_gray, lq_hq2grays
from pepeline import read, save
import numpy as np
from os import listdir
from os.path import join
from ..process import *
from tqdm import tqdm

ALL_LOGIC = {
    "resize": ResizeLogic,
    "blur": BlurLogic,
    "screentone": ScreentoneLogic,
    "compress": CompressLogic,
    "noice": Noice,
    "color": ColorLossLogic,
    "sin": SinLossLogic,
    "halo": HaloLossLogic,
    "saturation": SaturationLossLogic,
    "dithering": Dithering
}


class ImgProcess:
    def __init__(self, config):
        self.input = config["input"]
        self.output = config["output"]
        self.tile = config.get("tile")
        if self.tile:
            self.no_wb = self.tile.get("no_wb")
            self.tile_size = self.tile.get("size", 512)
        self.replays = config.get("replays")
        self.gray_or_color = config.get("gray_or_color")
        self.gray = config.get("gray")
        process = config["process"]
        self.all_images = listdir(self.input)
        self.turn = []
        self.output_lq = join(self.output, "lq")
        self.output_hq = join(self.output, "hq")
        self.map_type = config.get("map_type", "process")

        self.num_workers = config.get("num_workers")
        for process_dict in process:
            process_type = process_dict["type"]
            self.turn.append(ALL_LOGIC[process_type](process_dict))

        if not os.path.exists(self.output_lq):
            os.makedirs(self.output_lq)
        if not os.path.exists(self.output_hq):
            os.makedirs(self.output_hq)

    def __img_read(self, img_fold):
        input_folder = join(self.input, img_fold)
        if self.gray:
            img = read(str(input_folder), 0, 0)
        else:
            img = read(str(input_folder), 1, 0)
        if self.gray_or_color:
            img = color_or_gray(img)
        return img

    def __img_save(self, lq, hq, output_name):
        if self.gray:
            lq, hq = lq_hq2grays(lq, hq)

        save(lq, join(self.output_lq, output_name))
        save(hq, join(self.output_hq, output_name))

    def process(self, img_fold):
        try:
            img = self.__img_read(img_fold)
            n = self.all_images.index(img_fold)
            lq, hq = img, img
            for loss in self.turn:
                lq, hq = loss.run(lq, hq)
            output_name = f"{n}.png"
            self.__img_save(lq, hq, output_name)


        except Exception as e:
            print(e)

    def process_tile(self, img_fold):
        try:
            img = self.__img_read(img_fold)
            h, w = img.shape[:2]
            n = self.all_images.index(img_fold)
            for Kx, Ky in np.ndindex(h // self.tile_size, w // self.tile_size):
                img_tile = img[self.tile_size * Kx:self.tile_size * (Kx + 1),
                           self.tile_size * Ky:self.tile_size * (Ky + 1)]
                if self.no_wb:
                    mean = np.mean(img_tile)
                    if mean == 0.0 or mean == 1.0:
                        continue
                lq, hq = img_tile, img_tile
                for loss in self.turn:
                    lq, hq = loss.run(lq, hq)
                output_name = f"{str(n)}_{Kx}_{Ky}.png"
                self.__img_save(lq, hq, output_name)

        except Exception as e:
            print(e)

    def run(self):
        process = self.process_tile if self.tile else self.process
        if self.map_type == "process":
            process_map(process, self.all_images, max_workers=self.num_workers)
        elif self.map_type == "thread":
            thread_map(process, self.all_images, max_workers=self.num_workers)
        else:
            for img in tqdm(self.all_images):
                process(img)
