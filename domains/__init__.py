from os import listdir
from os.path import dirname, isdir, isfile
# List of modules to load.
__all__ = []
# Check all directories in the current directory.
for entry in listdir(dirname(__file__)):
    entry_path = dirname(__file__) + "/" + entry
    if isdir(entry_path) and not entry.startswith(".") and not entry.startswith("_") :
        # Add directory name to modules list.
        __all__.append(entry)
        # Check all files in the sub directory.
        #for sub_entry in listdir(entry_path):
            #sub_entry_path = entry_path + "/" + sub_entry
            # Check if the file is a python file.
            #if isfile(sub_entry_path) and not sub_entry.startswith('__') and sub_entry.endswith('.py'):
                # Load the module.
                #__all__.append(sub_entry[:-3])
