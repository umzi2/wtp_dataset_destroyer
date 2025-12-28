import hashlib
import math
import os
import shutil
import sys
import multiprocessing as mp
from ..objects.lq_hq_state import LQHQState
from pepeline import save


def save_lq(state: LQHQState, out_path: str, img_name: str):
    save(
        state.lq.clip(0, 1),
        os.path.join(out_path, "lq", f"{img_name}.png"),
    )


def save_hq_lq(state: LQHQState, out_path: str, img_name: str):
    save(
        state.lq.clip(0, 1),
        os.path.join(out_path, "lq", f"{img_name}.png"),
    )
    save(
        state.hq.clip(0, 1),
        os.path.join(out_path, "hq", f"{img_name}.png"),
    )


def digits_count(n: int) -> int:
    if n == 0:
        return 1
    return int(math.log10(abs(n))) + 1


def get_best_context():
    if sys.platform == "win32":
        return mp.get_context("spawn")

    try:
        return mp.get_context("forkserver")
    except ValueError:
        return mp.get_context("fork")


def mix_seed(*parts, bits=64) -> int:
    h = hashlib.blake2b(digest_size=bits // 8)
    for p in parts:
        if isinstance(p, bytes):
            h.update(p)
        else:
            h.update(str(p).encode("utf-8"))
        h.update(b"|")  # разделитель
    return int.from_bytes(h.digest(), "little")


def out_clear(folder):
    if os.path.exists(folder):
        shutil.rmtree(folder)
