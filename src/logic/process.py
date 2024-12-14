import os

from tqdm.contrib.concurrent import process_map, thread_map
from ..process.utils import laplace_filter, lq_hq2grays, color_or_gray, img2gray
from pepeline import read, save, ImgColor, ImgFormat
import numpy as np
from os import listdir
from os.path import join
from tqdm import tqdm
import psutil
import gc

from ..utils.process import del_all_file
from ..utils.registry import get_class
import logging


class ImgProcess:
    """Class for processing images using various image processing techniques.

    Args:
        config (dict): A dictionary containing configuration settings for image processing.
            It should include the following keys:
                - "input" (str): Path to the input folder containing images.
                - "output" (str): Path to the output folder where processed images will be saved.
                - "tile" (dict, optional): Dictionary containing settings for tile-based processing. Defaults to None.
                - "gray_or_color" (bool, optional): Flag indicating whether to process images in grayscale or color.
                    Defaults to None.
                - "gray" (bool, optional): Flag indicating whether to convert images to grayscale. Defaults to None.
                - "process" (list of dict): List containing dictionaries specifying the processing techniques to apply.
                - "num_workers" (int, optional): Number of worker threads to use for parallel processing.
                Defaults to None.
                - "map_type" (str, optional): Type of mapping to use for processing images. Can be "process",
                "thread", or None.
                    Defaults to "thread".

    Attributes:
        input (str): Path to the input folder containing images.
        output (str): Path to the output folder where processed images will be saved.
        tile (dict): Dictionary containing settings for tile-based processing.
        no_wb (bool): Flag indicating whether to exclude white or black tiles during tile-based processing.
        tile_size (int): Size of each tile for tile-based processing.
        gray_or_color (bool): Flag indicating whether to process images in grayscale or color.
        gray (bool): Flag indicating whether to convert images to grayscale.
        all_images (list): List of all image filenames in the input folder.
        turn (list): List of image processing techniques to apply.
        output_lq (str): Path to the folder where low-quality processed images will be saved.
        output_hq (str): Path to the folder where high-quality processed images will be saved.
        map_type (str): Type of mapping to use for processing images.
        num_workers (int): Number of worker threads to use for parallel processing.

    Methods:
        process(img_fold): Processes an image using the specified image processing techniques.
        process_tile(img_fold): Processes an image in tiles using the specified image processing techniques.
        run(): Executes the image processing workflow.
    """

    def __init__(self, config: dict):
        """Initialize the image processor with configuration validation."""
        # Setup logging
        self.log_file = "image_processing.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file, mode='w'),
                logging.StreamHandler(stream=open(os.devnull, 'w'))  # Suppress terminal output
            ]
        )
        
        self._validate_config(config)
        self.input = config["input"]
        self.output = config["output"]
        self.tile = config.get("tile")
        if self.tile:
            self._validate_tile_config(self.tile)
            self.no_wb = self.tile.get("no_wb")
            self.tile_size = self.tile.get("size", 512)
        self.gray_or_color = config.get("gray_or_color")
        self.gray = config.get("gray")
        process = config["process"]
        del_out_dir = config.get("out_clear")
        self.all_images = [
            file
            for file in listdir(self.input)
            if os.path.isfile(os.path.join(self.input, file))
        ]
        if config.get("shuffle_dataset"):
            np.random.shuffle(self.all_images)
        if config.get("size"):
            self.all_images = self.all_images[: config.get("size")]
        self.turn = []
        self.output_lq = join(self.output, "lq")
        self.output_hq = join(self.output, "hq")
        self.map_type = config.get("map_type", "thread")
        self.laplace_filter = config.get("laplace_filter")
        self.num_workers = config.get("num_workers")
        self.only_lq = config.get("only_lq", False)
        self.real_name = config.get("real_name")
        debug = config.get("debug")
        if debug:
            if not os.path.exists("debug"):
                os.makedirs("debug")
            logging.basicConfig(
                level=logging.DEBUG,
                filename="debug/debug.log",
                filemode="w",
                format="%(message)s",
            )
            self.map_type = "for"
        for process_dict in process:
            process_type = process_dict["type"]
            self.turn.append(get_class(process_type)(process_dict))

        if not os.path.exists(self.output_lq):
            os.makedirs(self.output_lq)
        if not os.path.exists(self.output_hq) and not self.only_lq:
            os.makedirs(self.output_hq)
        if del_out_dir:
            lq_fold = join(self.output, "lq")
            lq_folds = os.listdir(lq_fold)
            del_all_file(lq_fold, lq_folds)
            hq_fold = join(self.output, "hq")
            hq_folds = os.listdir(hq_fold)
            del_all_file(hq_fold, hq_folds)

    def _validate_config(self, config: dict) -> None:
        """Validate the configuration dictionary."""
        required_keys = ["input", "output", "process"]
        if not all(key in config for key in required_keys):
            raise ValueError(f"Missing required configuration keys: {required_keys}")
        if not os.path.exists(config["input"]):
            raise ValueError(f"Input directory does not exist: {config['input']}")

    def _validate_tile_config(self, tile_config: dict) -> None:
        """Validate tile-specific configuration."""
        if "size" in tile_config and not isinstance(tile_config["size"], int):
            raise ValueError("Tile size must be an integer")
        if tile_config.get("size", 512) <= 0:
            raise ValueError("Tile size must be positive")

    def __img_read(self, img_fold: str) -> np.ndarray:
        input_folder = join(self.input, img_fold)
        if self.gray:
            img = read(str(input_folder), ImgColor.GRAY, ImgFormat.F32)
        else:
            img = read(str(input_folder), ImgColor.RGB, ImgFormat.F32)
        if self.gray_or_color:
            img = color_or_gray(img)
        return img

    def __img_save(self, lq: np.ndarray, hq: np.ndarray, output_name: str) -> None:
        if self.gray:
            lq, hq = lq_hq2grays(lq, hq)

        save(lq, join(self.output_lq, output_name))
        save(hq, join(self.output_hq, output_name))

    def __only_lq_save(self, lq: np.ndarray, output_name: str) -> None:
        if self.gray:
            lq = img2gray(lq)
        save(lq, join(self.output_lq, output_name))

    def process(self, img_fold: str) -> None:
        """Processes an image using the specified image processing techniques.

        Args:
            img_fold (str): Filename of the image to process.

        Raises:
            IOError: If image reading or writing fails
            ValueError: If image validation fails
            RuntimeError: If processing pipeline fails
        """
        try:
            # Input validation
            if not isinstance(img_fold, str) or not img_fold:
                raise ValueError("Invalid image folder name")

            # Memory tracking
            initial_memory = psutil.Process().memory_info().rss

            # Image reading with validation
            img = self.__img_read(img_fold)
            if img is None or img.size == 0:
                raise ValueError(f"Failed to read image: {img_fold}")

            # Laplace filter check
            if self.laplace_filter and laplace_filter(img, self.laplace_filter):
                logging.info(f"Skipping {img_fold} due to laplace filter")
                return

            # Setup processing
            n = self.all_images.index(img_fold)
            seed = np.random.randint(2**30) + n
            np.random.seed(seed)

            # Initialize with proper shape checking
            if not (isinstance(img, np.ndarray) and img.ndim in [2, 3]):
                raise ValueError(f"Invalid image format for {img_fold}")
            lq, hq = img.copy(), img.copy()

            # Output name generation
            output_name = img_fold if self.real_name else f"{n}.png"
            logging.debug(
                "Processing image - Real name: %s, Output name: %s",
                img_fold,
                output_name,
            )

            # Process through pipeline with validation
            for loss in self.turn:
                try:
                    lq, hq = loss.run(lq, hq)
                    if lq is None or hq is None:
                        raise RuntimeError(f"Processing step {loss.__class__.__name__} failed")

                    # Validate array bounds
                    if not (0 <= lq.min() <= lq.max() <= 1):
                        logging.warning(f"Array bounds violated in {loss.__class__.__name__}, clipping values")
                        lq = np.clip(lq, 0, 1)
                    if not (0 <= hq.min() <= hq.max() <= 1):
                        logging.warning(f"Array bounds violated in {loss.__class__.__name__}, clipping values")
                        hq = np.clip(hq, 0, 1)

                except Exception as step_error:
                    logging.error("Processing step failed: %s", step_error)
                    raise RuntimeError(f"Processing pipeline failed at {loss.__class__.__name__}") from step_error

            # Save results
            if self.only_lq:
                self.__only_lq_save(lq, output_name)
            else:
                self.__img_save(lq, hq, output_name)

            # Memory cleanup
            del img, lq, hq
            current_memory = psutil.Process().memory_info().rss
            if current_memory - initial_memory > 100 * 1024 * 1024:  # 100MB
                logging.warning("High memory usage detected: %d MB", (current_memory - initial_memory) / (1024 * 1024))
                gc.collect()

        except Exception as e:
            logging.error("Processing failed for %s: %s", img_fold, str(e))
            raise RuntimeError(f"Failed to process {img_fold}") from e

    def process_tile(self, img_fold: str) -> None:
        """Processes an image in tiles using the specified image processing techniques."""
        try:
            initial_memory = psutil.Process().memory_info().rss
            img = self.__img_read(img_fold)
            if img is None:
                raise ValueError(f"Failed to read image: {img_fold}")

            h, w = img.shape[:2]
            if h < self.tile_size or w < self.tile_size:
                raise ValueError(f"Image {img_fold} is smaller than tile size")

            n = self.all_images.index(img_fold)
            seed = np.random.randint(2**30) + n
            np.random.seed(seed)

            total_tiles = (h // self.tile_size) * (w // self.tile_size)
            with tqdm(total=total_tiles, desc=f"Processing {img_fold}") as pbar:
                for Kx, Ky in np.ndindex(h // self.tile_size, w // self.tile_size):
                    try:
                        self._process_single_tile(img, Kx, Ky, n)
                        pbar.update(1)
                    except Exception as tile_error:
                        logging.error(f"Tile processing failed at ({Kx}, {Ky}): {str(tile_error)}")
                        continue

            current_memory = psutil.Process().memory_info().rss
            if current_memory - initial_memory > 100 * 1024 * 1024:  # 100MB
                logging.warning("High memory usage in tile processing: %d MB", 
                              (current_memory - initial_memory) / (1024 * 1024))
                gc.collect()

        except Exception as e:
            logging.error(f"Failed to process image {img_fold}: {str(e)}")
            raise

    def _process_single_tile(self, img: np.ndarray, Kx: int, Ky: int, n: int) -> None:
        """Process a single tile of the image."""
        img_tile = img[
            self.tile_size * Kx : self.tile_size * (Kx + 1),
            self.tile_size * Ky : self.tile_size * (Ky + 1),
        ]

        if self.laplace_filter and laplace_filter(img_tile, self.laplace_filter):
            return
        if self.no_wb:
            mean = np.mean(img_tile)
            if mean == 0.0 or mean == 1.0:
                return

        lq, hq = img_tile.copy(), img_tile.copy()
        output_name = f"{str(n)}_{Kx}_{Ky}.png"
        
        seed = np.random.randint(2**30) + Kx + Ky
        np.random.seed(seed)
        
        for loss in self.turn:
            lq, hq = loss.run(lq, hq)
            if lq is None or hq is None:
                raise RuntimeError(f"Processing step {loss.__class__.__name__} failed")
            lq = np.clip(lq, 0, 1)
            hq = np.clip(hq, 0, 1)

        self.__img_save(lq, hq, output_name)

    def run(self):
        """Executes the image processing workflow."""
        process = self.process_tile if self.tile else self.process
        try:
            if self.map_type == "process":
                process_map(
                    process, self.all_images, max_workers=self.num_workers, chunksize=1
                )
            elif self.map_type == "thread":
                thread_map(process, self.all_images, max_workers=self.num_workers)
            else:
                for img in tqdm(self.all_images):
                    process(img)
                    
            # Check if log file was modified and has content
            if os.path.exists(self.log_file) and os.path.getsize(self.log_file) > 0:
                print(f"\nWarning: Processing completed with logged messages. Please check {self.log_file} for details.")
                
        except Exception as e:
            logging.error(f"Processing failed: {str(e)}")
            print(f"\nError: Processing failed. Please check {self.log_file} for details.")
            raise
