import re
from typing import List

from ..utils.constants import RESIZE_LIST


def validate_resize_algorithms(v: List[str]) -> List[str]:
    for alg in v:
        if alg in RESIZE_LIST or re.match(r"^dpid_.*$", alg):
            continue

        if alg in ["down_down", "down_up", "up_down"]:
            continue

        available = ", ".join(list(RESIZE_LIST)[:5])
        raise ValueError(
            f"Invalid algorithm: '{alg}'. "
            f"Allowed values: [{available}...] or 'dpid_*.*' pattern."
        )
    return v


if __name__ == "__main__":
    for i in RESIZE_LIST:
        print('"', end="")
        print(i, end="")
        print('"', end=", ")
