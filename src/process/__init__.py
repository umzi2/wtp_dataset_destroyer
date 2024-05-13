import os
import glob

# Find all Python files in the current directory with names ending in '_degr.py'
modules = [
    os.path.basename(f)[:-3]
    for f in glob.glob(os.path.dirname(__file__) + "/*_degr.py")
]

# Import each module dynamically
for module in modules:
    import importlib

    importlib.import_module(f".{module}", package=__name__)
