import os
import numpy as np
import cv2 as cv
from tqdm.contrib.concurrent import process_map
from src.logic import ResizeLogic, BlurLogic, ScreentonLogic, CompressLogic, HaloLossLogic, Noice, ColorLossLogic, \
    SinLossLogic, img2gray, graycolor, NewHaloLossLogic
from pepeline import read, save32, read32
import json

turn = []
all_logic = {
    "resize": ResizeLogic,
    "blur": BlurLogic,
    "screenton": ScreentonLogic,
    "compress": CompressLogic,
    "halo": HaloLossLogic,
    "noise": Noice,
    "color_loss": ColorLossLogic,
    "sin": SinLossLogic,
    "nhalo": NewHaloLossLogic
}


def process(img_fold):
    global all_images, inp, output, gray, gray_or_color, rep
    if gray:
        img = read32(f"{inp}/{img_fold}",0)
    else:
        img = read32(f"{inp}/{img_fold}")
    if img is None:
        return
    if gray:
        img = img2gray(img)
    elif gray_or_color:
        img = graycolor(img)
    n = all_images.index(img_fold)
    lq, hq = img, img
    for loss in turn:
        lq, hq = loss.run(lq, hq)
    if rep:
        save32(lq,f"{output}/lq/{rep}_{n}.png")
        save32(lq, f"{output}/lq/{rep}_{n}.png")
    else:
        save32(hq,f"{output}/lq/{n}.png")
        save32(hq, f"{output}/lq/{n}.png")


def process_tile(img_fold):
    try:
        global all_images, inp, output, gray, gray_or_color, tile_size, tile, rep
        if gray:
            img = read(f"{inp}/{img_fold}",0)
        else:
            img = read(f"{inp}/{img_fold}")
        if img is None:
            return
        img = img.astype(np.float32) / 255

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
                save32(lq, fr"{output}/lq/{rep}_{str(n)}_{Kx}_{Ky}.png")
                save32(hq, fr"{output}/hq/{rep}_{str(n)}_{Kx}_{Ky}.png")
            else:
                save32(lq, fr"{output}/lq/{str(n)}_{Kx}_{Ky}.png")
                save32(hq, fr"{output}/hq/{str(n)}_{Kx}_{Ky}.png")
    except RuntimeError as e:
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
    # np.random.shuffle(all_images)

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
