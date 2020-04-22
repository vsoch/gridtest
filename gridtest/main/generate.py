"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.utils import recursive_find, write_yaml
import importlib
import inspect
import os
import logging
import re
import sys
import types
import yaml

logger = logging.getLogger(__name__)


def get_function_typing(func):
    """Given a function that is inspected or otherwise present, return
       a lookup of arguments with any expected default types. This is
       done at runtime and done as a check, and done here so we don't need
       to install mypy.

       Arguments:
        - func (function) : loaded function to return types for
       Returns: lookup dictionary of variable names and types. Return
         is in the lookup and corresponds to the value of the return.
    """
    return inspect.getfullargspec(func).annotations


def import_module(name):
    """Import module will try import of a module based on a name. If import
       fails and there are no ., we expect that it could be a script in the
       present working directory and add .<script>

       Arguments:
        - name (str) : the name of the module to import
    """
    try:
        module = importlib.import_module(name)
    except:
        sys.exit(f"Unrecognizable file, directory, or module name {name}")
    return module


def generate_tests(module, output=None, include_private=False):
    """Generate a test output file for some input module, which can be:
        - a script path explitly
        - a directory path with files to be recursively discovered
        - a module name

        Arguments:
          - module (str) : a file, directory, or module name to parse
          - output (str) : a path to a yaml file to save to
          - include_private (bool) : include "private" functions
    """
    if not re.search("[.](yml|yaml)$", output):
        sys.exit("Output file must have yml|yaml extension.")

    files = []

    # Case 1: the module is a filename
    if os.path.isfile(module):
        files.append(os.path.relpath(module))

    # Case 2: Recursively add python files
    elif os.path.isdir(module):
        files += list(recursive_find(module))

    # Case 3: assume it's a module name
    else:
        files = [module]

    # We will build up a test specification
    spec = {}

    # Import each file as a module, or a module name, exit on error
    for filename in files:
        # name replaces / with .
        name = filename.replace("/", ".").strip(".py")
        spec[name] = extract_functions(filename, include_private)

    # Write to output file
    if output:
        write_yaml(spec, output)
    return spec


def formulate_arg(arg, default=None):
    """Return a data structure (dictionary) with the argument as key,
       and a default defined, along with a random value to test.
    """
    return {arg: default}


def extract_modulename(filename, input_dir=None):
    """Extract a module, file, or relative path for a filename. First

       Arguments:
          - filename (str) : a filename or module name to parse
          - input_dir (str) : an input directory with the recipe, in case
                              of a local file.
    """
    input_dir = input_dir or ""

    # Case 1: the filename already exists
    if os.path.exists(filename):
        return filename

    # Case 2: It's a module installed, return module name
    if "site-packages" in filename:
        return [x for x in filename.split("site-packages")[-1].split("/") if x][0]

    # Case 3: It's a local file in some input directory
    filename = os.path.join(input_dir, os.path.basename(filename))
    if not os.path.exists(filename):
        sys.exit(f"Cannot find module {filename}")
    return filename


def extract_functions(filename, include_private=False):
    """Given a filename, extract a module and associated functions with it
       into a grid test. This means creating a structure with function
       names and (if provided) default inputs. The user will fill in
       the rest of the file.

       Arguments:
          - filename (str) : a filename or module name to parse
          - include_private (bool) : include "private" functions
    """
    sys.path.insert(1, os.getcwd())

    meta = {}
    name = re.sub(".py$", "", filename).replace("/", ".")
    module = import_module(name)

    # For each function,
    for funcname in dir(module):
        if not isinstance(getattr(module, funcname), types.FunctionType):
            continue

        # If it's a "private" function and we aren't including private
        if funcname.startswith("_") and not include_private:
            continue

        key = name + "." + funcname
        logger.info(f"Extracting {funcname} from {name}")
        print(f"Extracting {funcname} from {name}")

        # Extract arguments for function, add to matrix
        func = getattr(module, funcname)
        meta["filename"] = inspect.getfile(func)
        args = inspect.getfullargspec(func)
        meta[key] = []

        defaults = args.defaults or []
        argdict = {}
        for idx in range(len(args.args)):
            default = None
            if len(defaults) > idx:
                default = defaults[idx]
            argdict.update(formulate_arg(args.args[idx], default))
        meta[key].append({"args": argdict})

    return meta
