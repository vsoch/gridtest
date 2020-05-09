"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.generate import import_module
from gridtest.defaults import GRIDTEST_FUNCS, GRIDTEST_GRIDEXPANDERS

from gridtest.logger import bot
import itertools
import os
import re
import sys


def custom_range(start, stop, by=1.0, precision=2):
    """the range function only accepts integers, and user's will likely
       want to provide float. Thus we use custom_range to provide this

       Arguments:
        - start (int or float) : the starting value
        - stop (int or float) : go up to this value
        - by (float or int) : increment by this value (default 1.0)
        - precision (int) : decimals to round to (default 2)
    """
    start = float(start)
    count = 0
    values = []
    while True:
        value = round(float(start + count * by), precision)
        if by > 0 and value >= stop:
            break
        elif by < 0 and value <= stop:
            break
        values.append(value)
        count += 1
    return values


def unpack_args(arglist):
    """given a list of dictionaries, unpack into tuples
    """
    args = []
    for argset in arglist:
        newset = ()
        for key, value in argset.items():
            pass

def expand_args(entry, lookup=None):
    return list(iter_expand_args(entry, lookup))

def iter_expand_args(entry, lookup=None):
    """Given a test yaml entry, convert the grid specifications and 
       arguments into a longer list of arguments to each run as a test.
       E.g., convert an entry with these keys:
 
       'grid': {'one': {'min': 0, 'max': 5, 'list': [10, 15]}},
       'args': {'two': 2},

       into:

        [{'two': 2, 'one': 0},
         {'two': 2, 'one': 1},
         {'two': 2, 'one': 2},
         {'two': 2, 'one': 3},
         {'two': 2, 'one': 4},
         {'two': 2, 'one': 10},
         {'two': 2, 'one': 15}]

       In the case that a grid has a string identifier to point to a key
       in the lookup, we use that listing of values instead that should
       already be calculated.
    """
    # Create list of all args to iterate through
    args = {}
    lookup = lookup or {}

    # First add existing args, ensure we have a list
    for param, values in entry.get("args", {}).items():
        args[param] = [values]

    for param, settings in entry.get("grid", {}).items():

        # If settings is a key, it must reference a grid name
        if isinstance(settings, str):

            # Case 1: user has provided a key to another grid
            if settings in lookup:
                value = lookup[settings]
                if not isinstance(value, list):
                    value = [value]
                args[param] = value
            else:
                bot.exit(f"{settings} must exist in grids or variables.")

        elif isinstance(settings, list):
            args[param] = settings

        elif isinstance(settings, dict):
            # If any settings defined not allowed, do not continue
            if set(settings.keys()).difference(GRIDTEST_GRIDEXPANDERS):
                bot.exit(f"Invalid key in grid settings {settings}")

            # List of values just for param
            values = []

            # Case 1: min, max, and by
            if "min" in settings and "max" in settings and "by" in settings:
                values += custom_range(settings["min"], settings["max"], settings["by"])
            elif "min" in settings and "max" in settings:
                values += custom_range(settings["min"], settings["max"])
            if "list" in settings:
                values += settings["list"]

            args[param] = values

        else:
            args[param] = settings

    # Now generate a list of dicts (the args) with all possible combinations
    if args:
        keys, values = zip(*args.items())
        for v in itertools.product(*values):
            yield dict(zip(keys, v))

    return [args]


def substitute_args(value, params=None):
    """Given a value, determine if it has variable argument substitutions
       in the format of {{ args.<name> }} and if so, if the argument is present
       return the value with the substitution.
    """
    params = params or {}

    # Numbers cannot have replacement
    if not isinstance(value, str):
        return value

    # First do substitutions of variables
    for template in re.findall("{{.+}}", value):
        varname = re.sub("({|}| )", "", template)

        # Variable name (when we get here) has to be in args
        if varname not in params:
            value = re.sub(template, "", value)
        else:
            value = re.sub(template, str(params[varname]), str(value))

    return value


def substitute_func(value, funcs=None):
    """Given a value, determine if it contains a function substitution,
       and if it's one an important function (e.g., one from gridtest.helpers)
       return the value with the function applied. 

       Arguments:
         - value (str) : the value to do the substitution for.
         - funcs (dict) : lookup dictionary of functions to be used

       Notes: 
         A function should be in the format: {% tempfile.mkdtemp %} 
         (global import) or a function in gridtest.func in the format 
         {% tmp_path %}. If arguments are supplied, they should be in 
         the format {% tmp_path arg1=1 arg2=2 %}
    """
    # Numbers cannot have replacement
    if not isinstance(value, str):
        return value

    # First do substitutions of variables
    for template in re.findall("{%.+%}", value):
        varname = re.sub("({%|%})", "", template)
        params = [x.strip() for x in varname.split(" ") if x]

        # Split module.name.func into module.name func
        modulename = params.pop(0).rsplit(".", 1)[0]
        funcpath = modulename[1:]
        func = None

        # Case 1: we have a known gridtest function
        if modulename in GRIDTEST_FUNCS:
            funcpath = modulename
            modulename = "gridtest.func"

        # Case 2: a function is supplied directly in the lookup
        elif funcs and modulename in funcs:
            func = funcs.get(modulename)

        # Case 3: Custom module provided by the user
        else:
            funcpath = funcpath[0]

        # The function path needs to be provided
        if not funcpath and not func:
            sys.exit(f"A function name must be provided for {varname}")

        # If used from within Python, the function might be supplied
        if not func:
            try:
                module = import_module(modulename)
                func = getattr(module, funcpath)
            except:
                sys.exit(f"Cannot import module {modulename}")

        # If function is found, get value
        if not func:
            sys.exit(f"Cannot import function {funcpath} from module {modulename}")

        kwargs = {}
        params = {x.split("=")[0]: x.split("=")[1] for x in params}

        # Clean up parameters based on intuited types
        for paramname, paramvalue in params.items():
            if paramvalue == "None":
                paramvalue = None

            # Booleans
            elif paramvalue == "True":
                paramvalue = True
            elif paramvalue == "False":
                paramvalue = False

            # No quotes and all numeric, probably int
            elif re.search("^[0-9]+$", paramvalue):
                paramvalue = int(paramvalue)

            # One decimal, all numbers, probably float
            elif re.search("^[0-9]+[.]([0-9]+)?$", paramvalue):
                paramvalue = float(paramvalue)

            # Explicitly a string with quotes
            elif re.search('^(".+")$', paramvalue):
                paramvalue = paramvalue.strip('"')
            elif re.search("^('.+')$", paramvalue):
                paramvalue = paramvalue.strip("'")
            kwargs[paramname] = paramvalue

        new_value = func(**kwargs)
        value = re.sub(template, value, new_value)

    return value
