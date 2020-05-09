"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.utils import read_yaml, write_yaml, write_json
from gridtest.main.generate import import_module
from gridtest.main.substitute import expand_args
from copy import deepcopy
from gridtest.logger import bot

import itertools
import re
import shutil
import sys
import os


class Grid:

    def __init__(self, name, params):

        # The key in the yaml grids section
        self.name = name

        # A grid includes variables and functions
        self.variables = params.get('variables', {})
        self.functions = params.get('functions', {})
       
        # Parsing means generating parameter sets
        self.paramsets = {}

    def parse(self):
        """Given input variables, parse into parameter sets
        """
        keys, values = zip(*self.variables.items())
        values = [[v] if not isinstance(v, list) else v for v in values]

        
        for v in itertools.product(*values):
            for fun in self.functions.items():    
                self.paramsets[dict(zip(keys, v))] = None


    def __repr__(self):
        return "[grid|%s]" % self.name

    def __str__(self):
        return "[grid|%s]" % self.name


def get_grids(items, filename="", variables=None):
    """given a loaded items (a grids section from a GridRunner). return 
       the parameterized grids. Provide a lookup to derive other variables
       from, if appropriate.
    """
    grids = {}

    for name, grid in items.items():

        # Create temporary lookup of grids and lookup provided
        if variables:
            lookup = variables.copy()
            lookup.update(grids)
        else:
            lookup = grids

        # Unwrap list of arguments (even if empty)
        args = expand_args(
            entry={"grid": grid.get("grid", {}), "args": grid.get("args", {})},
            lookup=lookup,
        )

        grids[name] = update_gridargs(grid, args, filename)

    return grids


def get_variables(lookup, filename=""):
    """given a loaded lookup (a variables section from a GridRunner). return 
       the parameterized variables.
    """
    variables = {}
    lookup = lookup or {}

    for name, grid in lookup.items():


        # If a value is given directly, use it
        if not isinstance(grid, (dict, list)):
            variables[name] = grid

        # Unwrap list of arguments (even if empty)
        else:
            args = expand_args(
                entry={"grid": {"arg": grid}, "args": {}},
                lookup=variables,
            )

            # Flatten into list
            args = [x["arg"] for x in args]
            variables[name] = update_gridargs(grid, args, filename)

    return variables


def update_gridargs(grid, args, filename):
    """Given a grid lookup (e.g. {"min": 1, "max":2, "count": 10})
       apply advanced modifiers with functions and counts.
    """
    # If there is a count, we need to multiple it by that
    if "count" in grid:
        args = args * grid["count"]

    # If a function is provided, import and run args through it
    if "func" in grid:
        sys.path.insert(0, os.path.dirname(filename))
        funcname = grid.get("func")
        module = ".".join(funcname.split(".")[:-1])
        funcname = funcname.split(".")[-1]
        try:
            module = import_module(module)
            func = getattr(module, funcname)
            if func is None:
                bot.exit(f"Cannot find {funcname}.")
        except:
            bot.exit(f"Cannot import grid function {funcname}")

        # Run the args through the function
        args = [func(**k) for k in args]
    return args
