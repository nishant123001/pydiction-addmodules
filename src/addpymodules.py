#!/usr/bin/env python
# Last modified: September 11th, 2012
"""

addpymodules.py 1.2 by Nishant (nishant123001 AT gmail DOT com).

Description: Adds custom module to pydict

Usage: addpymodules.py <folder> ... 
Example: The following will append all the modules in folder 
            $ python addpymodules.py folder1

License: BSD.
"""


__author__ = "Nishant Yadav (nishant123001 AT gmail DOT com)"
__version__ = "1.0"
__copyright__ = "Copyright (c) 2011-2012 Nishant Yadav"


import os
import sys
import stat
import types
import shutil


# NEW bat file with modules_dict
MODULE_BAT = r'complete-dict-modules.bat'

# Final Module List
MODULE_LIST = []

def my_import(name):
    """Make __import__ import "package.module" formatted names."""
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def get_mode(apath):
    st = os.lstat(apath)
    if stat.S_ISDIR(st.st_mode):
        return stat.S_IFDIR
    return stat.S_IFREG

def try_import_module(module_name):
    ret = False
    try:
        imported_module = my_import(module_name)
        print "IMPORTED MODULE %s"%(module_name)
        ret = True
    except ImportError, err:
        print "Couldn't import: %s. %s" % (module_name, err)
        ret = False
    except Exception, err:
        print "Unknown error. Couldn't import: %s. %s" % (module_name, err)
        pass
    return ret

def create_module_list(path, prepend_str):
    for f_name in os.listdir(path):
        apath = os.path.join(path, f_name)
        if prepend_str:
            aprepend_str = "%s.%s"%(prepend_str, f_name)
        else:
            aprepend_str = f_name

        if get_mode(apath) == stat.S_IFDIR:
            create_module_list(apath, aprepend_str)
        elif not f_name.endswith(".py") or f_name == "__init__.py":
            continue

        aprepend_str = aprepend_str.rstrip(".py")
        
        if not(aprepend_str in MODULE_LIST) and try_import_module(aprepend_str):
            MODULE_LIST.append(aprepend_str)

def create_batfile():
    f = open(MODULE_BAT, 'w')
    mod_list = ' '.join(MODULE_LIST)
    f.write("python pydiction.py %s"%mod_list)
    f.close()


def main():
    """Generate a List of modules for Vim of python module attributes."""

    for folder_path in sys.argv[1:]:
        try:
            if get_mode(folder_path) == stat.S_IFDIR:
                if try_import_module(os.path.split(folder_path)[1]):
                    prepend_str = os.path.split(folder_path)[1]
                else:
                    prepend_str = ''
                create_module_list(folder_path, prepend_str)
            else:
                print "Path %s is not a folder so ignoring it"%(folder_path)
        except ImportError, err:
            print "Error occured for path: %s. %s" % (module_name, err)

    create_batfile()
    print "Done."

if __name__ == '__main__':
    """Process the command line."""

    if sys.version_info[0:2] < (2, 3):
        sys.exit("You need a Python 2.x version of at least Python 2.3")

    if len(sys.argv) <= 1:
        sys.exit("%s requires at least one argument. None given." % 
                  sys.argv[0])

    main()
