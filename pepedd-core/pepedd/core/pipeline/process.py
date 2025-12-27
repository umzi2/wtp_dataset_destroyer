from logging import debug

import numpy as np

from ..objects.lq_hq_state import LQHQState
from ..objects.safe_rng import SafeRNG
from ..pipeline.utils import mix_seed


def node_iterator(nodes, state: LQHQState):
    for node in nodes:
        state = node(state)
    return state


def std_process(
    img_path: str, reader, saver, nodes, seed: int, out_path: str, image_dict: dict
):
    result_name = image_dict[img_path]
    debug(
        f"__________________________________\nImage path: {img_path} ResultName: {result_name}"
    )
    img = reader(img_path)
    state = LQHQState(rng=SafeRNG(mix_seed(seed, img_path)), hq=img, lq=img.copy())
    state = node_iterator(nodes, state)

    saver(state, out_path, result_name)


def tile_process(
    img_path: str,
    reader,
    saver,
    nodes,
    seed: int,
    out_path: str,
    image_dict: dict,
    wb: bool,
):
    for index, img in enumerate(reader(img_path)):
        if wb:
            mean = np.mean(img)
            if mean == 0.0 or mean == 1.0:
                continue
        out_name = f"{image_dict[img_path]}_{index}"
        debug(
            f"__________________________________\nImage path: {img_path} ResultName: {out_name} TileIndex: {index}"
        )
        state = LQHQState(
            rng=SafeRNG(mix_seed(seed, img_path, index)), hq=img, lq=img.copy()
        )
        state = nodes(state)
        saver(state, out_path, out_name)
