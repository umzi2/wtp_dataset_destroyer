import importlib.util
from . import core

if importlib.util.find_spec("pepedd.nodes"):
    from contextlib import suppress

    with suppress(ImportError):
        from . import nodes  # noqa: F401
__all__ = ["core"]
