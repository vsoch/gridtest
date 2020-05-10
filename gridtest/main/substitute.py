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
