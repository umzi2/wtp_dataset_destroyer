from numpy.random import uniform, randint
import numpy as np


def safe_uniform(rand_list: list[float] | float) -> float:
    if list != type(rand_list):
        return rand_list
    if len(rand_list) == 1:
        return rand_list[0]
    if rand_list[0] >= rand_list[1]:
        return rand_list[0]
    return uniform(rand_list[0], rand_list[1])


def safe_randint(rand_list: list[int] | int) -> int:
    if list != type(rand_list):
        return rand_list
    if len(rand_list) == 1:
        return rand_list[0]
    if rand_list[0] >= rand_list[1]:
        return rand_list[0]
    return randint(rand_list[0], rand_list[1])


def safe_arange(range_list: list) -> np.ndarray:
    if len(range_list) == 1:
        return [range_list[0]]
    if range_list[0] >= range_list[1]:
        return [range_list[0]]
    return np.arange(*range_list)
