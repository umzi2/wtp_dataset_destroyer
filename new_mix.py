import os
import random
import shutil

in_dir = "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/train/train"
out_dir = "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/train/val"
img_name_list = os.listdir(in_dir)
random.shuffle(img_name_list)
img_name_list = img_name_list[:250]
for img_name in img_name_list:
    shutil.move(os.path.join(in_dir, img_name), os.path.join(out_dir, img_name))
# in_dir = "/run/media/umzi/H/dat/df2k/digital_art_v3/train/train/"
# img_list = os.listdir(in_dir)
# gg = []
# for i in img_list:
#     st_name = i.split("_")
#     class_label = int(st_name[1].split(".")[0])
#     os.rename(os.path.join(in_dir,i),os.path.join(in_dir,f"{st_name[0]}_{class_label//2}.png"))
#     clss_squize = f"{class_label}_{class_label//2}"
#     if clss_squize not in gg:
#         gg.append(clss_squize)
# gg.sort()
# print(gg)

# zero = 0
# circle = 1
# cross = 2
# line = 3
# noise = 4
# dirs = [
# "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/zero/lq",
#     "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/circle/lq",
#     "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/cross/lq",
#     "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/line/lq"
#
#
# ]
# out_dir = "/run/media/umzi/H/dat/df2k/digital_art_v2_ab/train/train"
# nn=0
# n = 0
# for dir in dirs:
#     img_names = os.listdir(dir)
#     for img_name in img_names:
#         shutil.copy(os.path.join(dir,img_name),os.path.join(out_dir,f"{nn}_{n}.png"))
#         nn+=1
#     n+=1
