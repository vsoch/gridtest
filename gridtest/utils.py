"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from json_tricks import dumps
import yaml
import fnmatch
import json
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


def read_file(filename, readlines=True):
    """write_file will open a file, "filename" and write content
       and properly close the file.

       Arguments:
         - filename (str) : the filename to read
         - readlines (bool) : read lines of the file (vs all raw)
    """
    with open(filename, "r") as filey:
        if readlines is True:
            content = filey.readlines()
        else:
            content = filey.read()
    return content


def read_yaml(filename):
    """read a yaml file, only including sections between dashes

       Arguments:
         - filename (str) : the filename to read
    """
    stream = read_file(filename, readlines=False)
    return yaml.load(stream, Loader=yaml.FullLoader)


def write_yaml(yaml_dict, filename):
    """write a dictionary to yaml file
 
       Arguments:
        - yaml_dict (dict) : the dict to print to yaml
        - filename (str) : the output file to write to
        - pretty_print (bool): if True, will use nicer formatting
    """
    with open(filename, "w") as filey:
        filey.writelines(yaml.dump(yaml_dict))
    return filename


def write_json(json_obj, filename, pretty=True):
    """write_json will write a json object to file, pretty printed

       Arguents:
        - json_obj (dict) : the dict to print to json
        - filename (str) : the output file to write to
    """
    with open(filename, "w") as filey:
        if pretty:
            filey.writelines(dumps(json_obj, indent=4, separators=(",", ": ")))
        else:
            filey.writelines(dumps(json_obj))
    return filename
