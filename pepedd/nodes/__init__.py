import os
import importlib

__all__ = []


def import_inits_recursively(path, package, ignore_dirs=None):
    ignore_dirs = set(ignore_dirs or [])
    local_all = []

    for entry in os.scandir(path):
        if entry.is_dir() and entry.name not in ignore_dirs:
            init_file = os.path.join(entry.path, "__init__.py")
            if os.path.isfile(init_file):
                subpackage = f"{package}.{entry.name}"
                importlib.import_module(f".{entry.name}", package=package)

                # Добавляем имя подмодуля в локальный __all__
                local_all.append(entry.name)

                # Рекурсивно импортируем подмодули и получаем их __all__
                child_all = import_inits_recursively(
                    entry.path, subpackage, ignore_dirs=ignore_dirs
                )
                local_all.extend(child_all)
    return local_all


current_dir = os.path.dirname(__file__)
__all__ = import_inits_recursively(current_dir, __name__, ignore_dirs=["utils"])
