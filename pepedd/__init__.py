import importlib.util
from . import core

if importlib.util.find_spec("pepedd.nodes"):
    from contextlib import suppress

    with suppress(ImportError):
        from . import nodes

        __all__ = ["core", "nodes"]
        # __all__ = ["core","*"]
else:
    __all__ = ["core"]
