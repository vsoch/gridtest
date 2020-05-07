"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.utils import recursive_find, write_yaml, read_yaml
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


def generate_tests(
    module, output=None, include_private=False, force=False, include_classes=True
):
    """Generate a test output file for some input module. If an output file 
       is specified and already has existing content, in the case that check is 
       used, we only print section names that have not been written. If check
       is used and the file doesn't exist, we print the tests to create to the
       screen. If an existing file is found and check isn't used, we only
       update it with tests not yet written. This functionality is provided
       so that the user can easily update a testing file without erasing old
       tests. A "module" input variable can be:
        - a script path explitly
        - a directory path with files to be recursively discovered
        - a module name
       By default, if a testing file is provided that already has sections defined,
       they will not be overwritten (but new sections will be added). If the
       user wants to produce a new (reset) template, the file should be deleted
       and generate run freshly.

       Arguments:
          - module (str) : a file, directory, or module name to parse
          - output (str) : a path to a yaml file to save to
          - include_private (bool) : include "private" functions
          - force (bool) : force overwrite existing functions (default False)
          - include_classes (bool) : extract classes to write tests too
    """
    if output and not re.search("[.](yml|yaml)$", output):
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

    # We will build up a test specification (or read in existing) based on filename
    spec = {}

    # Update the old test yaml
    if output and os.path.exists(output) and not force:
        sys.exit(
            f"{output} exists! use --force to overwrite, or gridtest update instead."
        )

    # Import each file as a module, or a module name, exit on error
    for filename in files:
        name = re.sub("[.]py$", "", filename.replace("/", "."))
        spec[name] = extract_functions(
            filename, include_private=include_private, include_classes=include_classes
        )

    # Write to output file
    if output:
        write_yaml(spec, output)
    else:
        print("\n" + yaml.dump(spec))
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


def extract_functions(
    filename, include_private=False, quiet=False, include_classes=True,
):
    """Given a filename, extract a module and associated functions with it
       into a grid test. This means creating a structure with function
       names and (if provided) default inputs. The user will fill in
       the rest of the file. The function can be used easily recursively by calling
       itself to get metadata for a subclass, and passing along the (already
       imported) module.

       Arguments:
          - filename (str) : a filename or module name to parse
          - include_private (bool) : include "private" functions
          - quiet (bool) : suppress additional output
          - include_classes (bool) : extract classes
    """
    sys.path.insert(1, os.getcwd())

    meta = {}
    tests = {}

    # Try importing the module, fall back to relative path
    try:
        name = re.sub(".py$", "", filename).replace("/", ".")
        module = import_module(name)
    except:
        name = re.sub(".py$", "", os.path.relpath(filename)).replace("/", ".")
        module = import_module(name)

    # Generate tuples with (name, module, fullname)
    functions = [(name, module, name)]
    meta["filename"] = inspect.getfile(module)
    module_dir = os.path.dirname(meta["filename"])

    # Don't re-add functions that are seen
    seen = set()

    while functions:
        funcname, func, fullname = functions.pop(0)

        if funcname.startswith("_") and not include_private:
            continue

        # Skip over functions / modules that aren't a part of original module
        try:
            if module_dir not in inspect.getfile(func):
                continue
        except:
            continue

        # If it's a module, add functions to list (first pop)
        if isinstance(func, types.ModuleType):
            for member in inspect.getmembers(func):
                if member[0] not in seen:
                    functions.append(member + ("%s.%s" % (funcname, member[0]),))
                    seen.add(member[0])
            continue

        if not include_function(
            funcname,
            func,
            include_classes=include_classes,
            include_private=include_private,
        ):
            continue

        # Extract arguments for function or class, add to matrix
        try:
            args = inspect.getfullargspec(func)

            if not quiet:
                logger.info(f"Extracting {funcname} from {name}")
                if funcname.startswith("_"):
                    print(f"Extracting {funcname} from {name}")

            tests[fullname] = []
            defaults = args.defaults or []
            argdict = {}

            # self is specific to classes, add reference to original class
            if args.args and args.args[0] == "self":
                if defaults and defaults[0] != "self":
                    args.args.pop(0)

            for idx in range(len(args.args)):
                default = None
                if len(defaults) > idx:
                    default = defaults[idx]
                argdict.update(formulate_arg(args.args[idx], default))
            tests[fullname].append({"args": argdict})

        # Exceptions will throw type errors
        except TypeError:
            continue

        # If it's a class and we are including classes
        if isinstance(func, object):
            try:
                for member in inspect.getmembers(func):
                    if member[0] not in seen:
                        functions.append(member + ("%s.%s" % (funcname, member[0]),))
                        seen.add(member[0])
            except:
                print(f"Cannot get members for {func}")

    # Add the tests to the final meta object
    meta["tests"] = tests
    return meta


def include_function(funcname, func, include_classes=True, include_private=False):
    """A helper to determine if a function (or class) should be included.
       Returns True for yes, False otherwise.
    """
    if funcname.startswith("__"):
        return False

    if funcname.startswith("_") and not include_private:
        return False

    if not isinstance(func, types.FunctionType) and not include_classes:
        return False

    if isinstance(func, types.FunctionType):
        return True

    if isinstance(func, object) and not include_classes:
        return False

    if isinstance(func, (int, float, bytes, str, list)):
        return False

    return True
