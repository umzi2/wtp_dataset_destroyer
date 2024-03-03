import os
import numpy as np
import cv2 as cv
from tqdm.contrib.concurrent import process_map
from src.logic import ResizeLogic, BlurLogic, ScreentonLogic, CompressLogic, HaloLossLogic, Noice, ColorLossLogic, \
    SinLossLogic, img2gray, graycolor
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
    "sin": SinLossLogic
}


def process(img_fold):
    global all_images, input, output, gray, gray_or_color
    img = np.array(cv.imread(f"{input}/{img_fold}"))
    if img is None:
        return
    img = img.astype(np.float32) / 255
    if gray:
        img = img2gray(img)
    elif gray_or_color:
        img = graycolor(img)
    n = all_images.index(img_fold)
    lq, hq = img, img
    for loss in turn:
        lq, hq = loss.run(lq, hq)
    cv.imwrite(f"{output}/lq/{n}.png", lq * 255)
    cv.imwrite(f"{output}/hq/{n}.png", hq * 255)


def process_tile(img_fold, tile_size=512):
    global all_images, input, output, gray, gray_or_color, tile
    img = np.array(cv.imread(f"{input}/{img_fold}"))
    if img is None:
        return
    img = img.astype(np.float32) / 255
    if gray:
        img = img2gray(img)
    elif gray_or_color:
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

        cv.imwrite(f"{output}/lq/{n}_{Kx}_{Ky}.png", lq * 255)
        cv.imwrite(f"{output}/hq/{n}_{Kx}_{Ky}.png", hq * 255)


if __name__ == "__main__":
    with open('config.json') as f:
        dict = json.load(f)
    input = dict["input"]
    output = dict["output"]
    tile = dict.get("tile")
    gray_or_color = dict.get("gray_or_color")
    gray = dict.get("gray")
    if not os.path.exists(f"{output}/hq"):
        os.makedirs(f"{output}/hq")
    if not os.path.exists(f"{output}/lq"):
        os.makedirs(f"{output}/lq")

    for dict_key in dict["process"].keys():
        logic = all_logic[dict_key]
        turn.append(logic(dict["process"][dict_key]))

    all_images = os.listdir(input)
    # np.random.shuffle(all_images)
    if tile:
        process_map(process_tile, all_images)
    else:
        process_map(process, all_images)
