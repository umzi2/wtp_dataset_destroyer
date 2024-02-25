import os
import random

import cv2
import numpy as np
import cv2 as cv
from tqdm.contrib.concurrent import process_map
from src.logic import ResizeLogic, BlurLogic, ScreentonLogic, CompresLogic,Halo

def process(img_fold):
    global s,r,b,c,ha
    global inp, out
    img = np.array(cv.imread(f"{inp}/{img_fold}").astype(np.float32) / 255)
    array1 = img[:, :, 1].flatten()
    array2 = img[:, :, 2].flatten()


    if np.mean(array1-array2)==0:
        img=np.dot(img[..., :3], [0.114, 0.587, 0.299]).astype(np.float32)
        img2 = s.run(img,False)
    else:
        img2 = s.run(img,True)
    meat=np.mean(img)
    if meat == 0 or meat==1:
        return

    ss, s2 = r.run(img, img2)

    cv.imwrite(f"{out}/hq/{img_fold}", s2*255)
    ram2 = random.randint(0, 3)
    if ram2:
        ss = b.run(ss)
    ram=random.randint(0,1)
    if ram ==1:
        ss = ha.run(ss)
    ss = c.run(ss * 255)
    cv.imwrite(f"{out}/lq/{img_fold}", ss)


res_dict = {
    "alg_lq": ['linear','catrom','bspline','mitchell','lanczos','gauss',"down_up",'down_down'],
    "alg_hq": ['catrom'],
    "down_up": {
        "up": [1, 3],
        "alg_up": ['nearest','linear','catrom','bspline','mitchell','lanczos','gauss'],
        "alg_down": ['linear','catrom','bspline','mitchell','lanczos','gauss','down_down']
    },
    "down_down": {
        "step": 10,
        "alg_down": ['linear','catrom','bspline','mitchell','gauss']

    },
    "rand_scale": [1, 2, .25],
    "scale": 4
}
blure_dict = {
    "method": ["box","gauss","box","median"],
    "kernel": [0, 8, 3]

}
comp_dict = {
    "algorithm": ["jpeg","webp"],
    "comp": [40, 90]

}
s = ScreentonLogic(7)
r = ResizeLogic(res_dict)
b = BlurLogic(blure_dict)
c = CompresLogic(comp_dict)
ha = Halo()
inp = r"/media/umzo/009C2B839C2B7278/чб/цвет3/hq_tile"
out = r"/media/umzo/009C2B839C2B7278/чб/цвет3/hq_tile12423"
if not os.path.exists(f"{out}/hq"):
    os.makedirs(f"{out}/hq")
if not os.path.exists(f"{out}/lq"):
    os.makedirs(f"{out}/lq")
immm = os.listdir(inp)
process_map(process,immm)

