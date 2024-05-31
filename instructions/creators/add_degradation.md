# Instructions for adding new degradations

To add a new degradation, simply create a file `*_degr.py` along the path `src.process`

In it you must import `from ..utils.registry import register_class`.

Create a minimal class in it like so:

```py
import numpy as np
from ..utils.registry import register_class


@register_class("color")  # the key by which degradation will be activated.
class Color:
    def __init__(self, color_dict: dict):  # the class must accept a dictionary containing the parameters we need
        pass

    def run(self, lq: np.ndarray, hq: np.ndarray) -> (np.ndarray,np.ndarray):
        # the class must contain a run method in which the degradation process is initialized; 
        # it must accept 2 np.ndarrays as input and also return 2 in the same order.

        return lq, hq
```
