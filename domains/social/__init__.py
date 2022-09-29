from os import listdir
from os.path import dirname
# Define modules to load for each .py file in the directory.
__all__ = [file[:-3] for file in listdir(dirname(__file__)) if not file.startswith('__') and file.endswith('.py')]