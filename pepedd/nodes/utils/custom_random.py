import numpy as np


def safe_arange(range_list: list) -> np.ndarray:
    count = len(range_list)

    if count == 0:
        return np.array([])

    if count == 1 or range_list[0] >= range_list[1]:
        return np.array([range_list[0]])

    start = range_list[0]
    stop = range_list[1]
    step = range_list[2] if count > 2 else 1

    return np.arange(start, stop, step)
