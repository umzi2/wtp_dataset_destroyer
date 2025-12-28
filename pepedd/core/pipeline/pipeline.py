from datetime import datetime
import logging
from logging import debug
import os

import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from functools import partial

from tqdm import tqdm
from tqdm.contrib.concurrent import thread_map

from pepeline import read, read_tiler, ImgFormat, ImgColor
from ..objects.safe_rng import SafeRNG
from ..node_register import registered_classes
from ..pipeline.process import std_process, tile_process
from ..pipeline.utils import (
    save_lq,
    save_hq_lq,
    out_clear,
    digits_count,
    get_best_context,
)
from ..pipeline.schema import PipelineOptions

from pathlib import Path


def init_worker(opts, img_names):
    global FORWARD
    from ..node_register import registered_classes

    nodes = [registered_classes[deg.type](deg.options) for deg in opts.degradation]
    if opts.tile:
        FORWARD = partial(
            tile_process,
            reader=partial(
                read_tiler,
                color_mode=ImgColor.GRAY if opts.gray else ImgColor.RGB,
                img_format=ImgFormat.F32,
                tile_size=opts.tile.size,
            ),
            saver=save_lq if opts.only_lq else save_hq_lq,
            nodes=nodes,
            seed=opts.seed,
            out_path=opts.output,
            image_dict=img_names,
            wb=opts.tile.no_wb,
        )

    else:
        FORWARD = partial(
            std_process,
            reader=partial(
                read,
                color_mode=ImgColor.GRAY if opts.gray else ImgColor.RGB,
                img_format=ImgFormat.F32,
            ),
            saver=save_lq if opts.only_lq else save_hq_lq,
            nodes=nodes,
            seed=opts.seed,
            out_path=opts.output,
            image_dict=img_names,
        )


def process_image(img_path):
    FORWARD(img_path)


class PipeLine:
    def __init__(self, options: PipelineOptions | dict):
        if isinstance(options, dict):
            opts = PipelineOptions(**options)
        else:
            opts = options
        if opts.debug:
            debug_folder = Path("debug")
            debug_folder.mkdir(exist_ok=True)

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_file = debug_folder / f"{timestamp}.log"

            # Настраиваем логирование: пишем и в файл, и в консоль
            logging.basicConfig(
                level=logging.DEBUG,
                format="%(message)s",
                handlers=[
                    logging.FileHandler(log_file, encoding="utf-8"),
                    # logging.StreamHandler(),
                ],
            )
        self.in_path = opts.input
        img_names = os.listdir(self.in_path)
        if opts.dataset_size:
            img_names = img_names[: opts.dataset_size]
        if opts.shuffle_dataset:
            rng = SafeRNG(opts.seed)
            rng.shuffle(img_names)
        self.img_names = {}

        if opts.real_name:
            for index, img_name in enumerate(img_names):
                self.img_names[os.path.join(self.in_path, img_name)] = Path(
                    img_name
                ).stem
        else:
            z_fill = digits_count(len(img_names))
            for index, img_name in enumerate(img_names):
                self.img_names[os.path.join(self.in_path, img_name)] = str(index).zfill(
                    z_fill
                )

        self.out_path = opts.output
        self.num_workers = opts.num_workers
        self.map_type = opts.map_type

        if opts.output_clear:
            out_clear(self.out_path)
        os.makedirs(os.path.join(self.out_path, "lq"), exist_ok=True)
        if not opts.only_lq:
            os.makedirs(os.path.join(self.out_path, "hq"), exist_ok=True)
        self.opts = opts
        if not opts.map_type == "process":
            nodes = [
                registered_classes[deg.type](deg.options) for deg in opts.degradation
            ]
            if opts.tile:
                self.forward = partial(
                    tile_process,
                    reader=partial(
                        read_tiler,
                        color_mode=ImgColor.GRAY if opts.gray else ImgColor.RGB,
                        img_format=ImgFormat.F32,
                        tile_size=opts.tile.size,
                    ),
                    saver=save_lq if opts.only_lq else save_hq_lq,
                    nodes=nodes,
                    seed=opts.seed,
                    out_path=opts.output,
                    image_dict=self.img_names,
                    wb=opts.tile.no_wb,
                )

            else:
                self.forward = partial(
                    std_process,
                    reader=partial(
                        read,
                        color_mode=ImgColor.GRAY if opts.gray else ImgColor.RGB,
                        img_format=ImgFormat.F32,
                    ),
                    saver=save_lq if opts.only_lq else save_hq_lq,
                    nodes=nodes,
                    seed=opts.seed,
                    out_path=opts.output,
                    image_dict=self.img_names,
                )

        debug(f"Start\nSeed: {opts.seed}")

    def _run_simple(self):
        img_paths = list(self.img_names.keys())
        for img_path in tqdm(img_paths, desc="Processing images", unit="img"):
            self.forward(img_path)

    def _run_thread(self, num_workers=None):
        if num_workers is None:
            num_workers = mp.cpu_count()

        img_paths = list(self.img_names.keys())
        thread_map(
            self.forward,
            img_paths,
            max_workers=num_workers,
            desc="Processing images",
            unit="img",
        )

    def _run_process(self, num_workers=None):
        if num_workers is None:
            num_workers = mp.cpu_count()

        tasks = list(self.img_names.keys())
        ctx = get_best_context()

        with ProcessPoolExecutor(
            initializer=init_worker,
            initargs=(self.opts, self.img_names),
            max_workers=num_workers,
            mp_context=ctx,
        ) as executor:
            futures = {executor.submit(process_image, task): task for task in tasks}
            with tqdm(total=len(futures), desc="Processing images", unit="img") as pbar:
                for future in as_completed(futures):
                    try:
                        future.result()
                    except Exception as e:
                        print(f"\nError processing {futures[future]}: {e}")
                    pbar.update(1)

    def __call__(
        self,
    ):
        if self.map_type == "simple":
            print("Using simple sequential processing (for loop)")
            self._run_simple()
        elif self.map_type == "thread":
            print(
                f"Using thread-based parallelism ({self.num_workers or mp.cpu_count()} workers)"
            )
            self._run_thread(self.num_workers)
        elif self.map_type == "process":
            print(
                f"Using process-based parallelism ({self.num_workers or mp.cpu_count()} workers)"
            )
            self._run_process(self.num_workers)
        else:
            raise ValueError(
                f"Unknown map_type: {self.map_type}. Use 'simple', 'thread', or 'process'"
            )

        return
