"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import yaml
import fnmatch
import os


def recursive_find(base, pattern="*.py"):
    """recursive find will yield python files in all directory levels
       below a base path.

       Arguments:
         - base (str) : the base directory to search
         - pattern: a pattern to match, defaults to *.py
    """
    for root, _, filenames in os.walk(base):
        for filename in fnmatch.filter(filenames, pattern):
            yield os.path.join(root, filename)


def read_yaml(filename, mode="r", quiet=False):
    """read a yaml file, only including sections between dashes
    """
    stream = read_file(filename, mode, readlines=False)
    return yaml.load(stream, Loader=yaml.FullLoader)


def write_yaml(yaml_dict, filename, mode="w"):
    """write a dictionary to yaml file
 
       Parameters
       ==========
       yaml_dict: the dict to print to yaml
       filename: the output file to write to
       pretty_print: if True, will use nicer formatting
    """
    with open(filename, mode) as filey:
        filey.writelines(yaml.dump(yaml_dict))
    return filename
