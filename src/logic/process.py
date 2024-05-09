import os
from ..utils import img2gray, color_or_gray, lq_hq2grays
from pepeline import read, save
import numpy as np
from os import listdir, cpu_count
from os.path import join
import concurrent.futures
from tqdm import tqdm
from ..process import *

ALL_LOGIC = {
    "resize": ResizeLogic, #готово
    "blur": BlurLogic,#готово
    "screentone": ScreentoneLogic,#готово
    "compress": CompressLogic,#готово
    "noice": Noice,
    "color": ColorLossLogic,#готово
    "sin": SinLossLogic,#готово
    "halo": HaloLossLogic,#готово
    "saturation": SaturationLossLogic#готово
}


class ImgProcess:
    """
    Class for processing images based on specified configurations.

    Args:
        config (dict): A dictionary containing the configuration parameters.
            It should have the following keys:
                - 'input' (str): Path to the input folder containing images.
                - 'output' (str): Path to the output folder for processed images.
                - 'tile' (dict, optional): Dictionary specifying parameters for processing images in tiles.
                - 'replays' (int, optional): Number of repetitions for processing images. Default is 1.
                - 'gray_or_color' (bool, optional): Boolean indicating whether to convert images to grayscale if True, otherwise keep original color. Default is False.
                - 'gray' (bool, optional): Boolean indicating whether to convert images to grayscale. Default is False.
                - 'process' (list): List of dictionaries specifying the image processing steps.
                    Each dictionary should have the following keys:
                        - 'type' (str): Type of image processing logic.
                        - Other parameters specific to the processing logic.
                - 'num_workers' (int, optional): Number of worker threads for parallel processing. Default is the number of CPU cores.

    Attributes:
        input (str): Path to the input folder containing images.
        output (str): Path to the output folder for processed images.
        tile (dict): Dictionary specifying parameters for processing images in tiles.
        rep (int): Number of repetitions for processing images.
        no_wb (bool): Boolean indicating whether to exclude tiles with extreme mean values.
        tile_size (int): Size of tiles for processing images.
        replays (int): Number of repetitions for processing images.
        gray_or_color (bool): Boolean indicating whether to convert images to grayscale or keep original color.
        gray (bool): Boolean indicating whether to convert images to grayscale.
        turn (list): List of image processing logic objects.
        output_lq (str): Path to the output folder for processed low-quality images.
        output_hq (str): Path to the output folder for processed high-quality images.
        num_workers (int): Number of worker threads for parallel processing.

    Methods:
        process(img_fold): Method to process a single image without tiling.
            Args:
                img_fold (str): Name of the image file.
        process_tile(img_fold): Method to process a single image by tiling.
            Args:
                img_fold (str): Name of the image file.
        run(): Method to start the image processing.
    """

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
        num_cpu_count = cpu_count() if cpu_count() is not None else 1
        self.num_workers = config.get("num_workers", num_cpu_count)
        for process_dict in process:
            process_type = process_dict["type"]
            self.turn.append(ALL_LOGIC[process_type](process_dict))

        if not os.path.exists(self.output_lq):
            os.makedirs(self.output_lq)
        if not os.path.exists(self.output_hq):
            os.makedirs(self.output_hq)

    def __img_read(self, img_fold):
        input_folder = join(self.input, img_fold)
        img = read(str(input_folder), 1, 0)
        if self.gray_or_color:
            img = color_or_gray(img)
        if self.gray:
            img = img2gray(img)
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
        total = len(self.all_images)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.num_workers) as executor:
            futures = [executor.submit(process, item) for item in self.all_images]
            with tqdm(total=total) as pbar:
                for _ in concurrent.futures.as_completed(futures):
                    pbar.update(1)
