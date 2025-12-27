import os
import importlib


def import_inits_recursively(path, package, ignore_dirs=None):
    ignore_dirs = set(ignore_dirs or [])

    for entry in os.scandir(path):
        if entry.is_dir() and entry.name not in ignore_dirs:
            init_file = os.path.join(entry.path, "__init__.py")
            if os.path.isfile(init_file):
                subpackage = f"{package}.{entry.name}"
                importlib.import_module(f".{entry.name}", package=package)
                import_inits_recursively(
                    entry.path, subpackage, ignore_dirs=ignore_dirs
                )


current_dir = os.path.dirname(__file__)
import_inits_recursively(current_dir, __name__, ignore_dirs=["utils"])
