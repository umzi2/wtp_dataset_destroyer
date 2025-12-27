from pepeline import ResizesFilter, ResizesAlg

RESIZE_FILTER_MAP = {
    attr.lower(): getattr(ResizesFilter, attr)
    for attr in dir(ResizesFilter)
    if not attr.startswith("_") and not callable(getattr(ResizesFilter, attr))
}
RESIZE_ALG_MAP = {
    attr.lower()[0]: getattr(ResizesAlg, attr)
    for attr in dir(ResizesAlg)
    if not attr.startswith("_")
}

RESIZE_LIST = set()
for alg in RESIZE_ALG_MAP.keys():
    if alg == "n":
        RESIZE_LIST.add("nearest")
    else:
        for r_filter in RESIZE_FILTER_MAP.keys():
            RESIZE_LIST.add(f"{alg}_{r_filter}")
