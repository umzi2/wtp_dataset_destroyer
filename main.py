import os
import numpy as np
from tqdm.contrib.concurrent import process_map
from src.logic import ResizeLogic, BlurLogic, ScreentoneLogic, CompressLogic, Noice, ColorLossLogic, \
    SinLossLogic, graycolor, HaloLossLogic,SaturationLossLogic
from pepeline import read, save
import json

turn = []
all_logic = {
    "resize": ResizeLogic,
    "blur": BlurLogic,
    "screenton": ScreentoneLogic,
    "compress": CompressLogic,
    "noise": Noice,
    "color_loss": ColorLossLogic,
    "sin": SinLossLogic,
    "halo": HaloLossLogic,
    "satur": SaturationLossLogic
}


def process(img_fold):
    try:
        global all_images, inp, output, gray, gray_or_color, rep
        if gray:
            img = read(f"{inp}/{img_fold}",0,0)
        else:
            img = read(f"{inp}/{img_fold}",1,0)
        if gray_or_color:
            img = graycolor(img)
        n = all_images.index(img_fold)
        lq, hq = img, img
        for loss in turn:
            lq, hq = loss.run(lq, hq)
        if rep:
            save(lq,f"{output}/lq/{rep}_{n}.png")
            save(lq, f"{output}/lq/{rep}_{n}.png")
        else:
            save(hq,f"{output}/lq/{n}.png")
            save(hq, f"{output}/lq/{n}.png")
    except Exception as e:
        print(e)

def process_tile(img_fold):
    try:
        global all_images, inp, output, gray, gray_or_color, tile_size, tile, rep
        if gray:
            img = read(f"{inp}/{img_fold}",0,0)
        else:
            img = read(f"{inp}/{img_fold}",1,0)
        if gray_or_color:
            img = graycolor(img)
        h, w = img.shape[:2]
        n = all_images.index(img_fold)
        for Kx, Ky in np.ndindex(h // tile_size, w // tile_size):
            img_tile = img[tile_size * Kx:tile_size * (Kx + 1), tile_size * Ky:tile_size * (Ky + 1)]
            if tile.get("no_wb"):
                mean = np.mean(img_tile)
                if mean == 0.0 or mean == 1.0:
                    continue
            lq, hq = img_tile, img_tile
            for loss in turn:
                lq, hq = loss.run(lq, hq)
            if rep:
                save(lq.astype(np.float32), fr"{output}/lq/{rep}_{str(n)}_{Kx}_{Ky}.png")
                save(hq.astype(np.float32), fr"{output}/hq/{rep}_{str(n)}_{Kx}_{Ky}.png")
            else:
                save(lq.astype(np.float32), fr"{output}/lq/{str(n)}_{Kx}_{Ky}.png")
                save(hq.astype(np.float32), fr"{output}/hq/{str(n)}_{Kx}_{Ky}.png")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    rep = None
    with open('config.json') as f:
        config = json.load(f)
    inp = config["input"]
    output = config["output"]
    tile = config.get("tile")
    replays = config.get("replays")
    gray_or_color = config.get("gray_or_color")
    gray = config.get("gray")
    if not os.path.exists(f"{output}/hq"):
        os.makedirs(f"{output}/hq")
    if not os.path.exists(f"{output}/lq"):
        os.makedirs(f"{output}/lq")

    for dict_key in config["process"].keys():
        logic = all_logic[dict_key]
        turn.append(logic(config["process"][dict_key]))

    all_images = os.listdir(inp)

    if replays and replays > 1:
        rep = 0
        for n_rep in range(replays):
            rep = str(n_rep)
            if tile:
                tile_size = tile.get("size", 512)
                process_map(process_tile, all_images, desc=str(n_rep + 1))
            else:
                process_map(process, all_images, desc=str(n_rep + 1))
    else:
        if tile:
            tile_size = tile.get("size", 512)
            process_map(process_tile, all_images)
        else:
            process_map(process, all_images)
