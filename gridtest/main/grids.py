"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.generate import import_module
from gridtest.main.expand import expand_args
from gridtest.logger import bot

from copy import deepcopy
import itertools
import inspect
import re
import sys
import os


class Grid:
    def __init__(self, name, params, filename=""):
        """A Grid is a defined parameterization over a set of arguments, for
           any use case (testing, measuring metrics from models, etc.)

           Arguments:
             - name (str) : the name of the grid, an identifier
             - params (dict) : the args and functions
             - filename (str) : if relevant, a filename to import modules from

           If argument sets are reasonably sized, you should be able to 
           set yield_args to False and interact with self.paramsets. Otherwise,
           you can instantiate the Grid and iterate through it at the same time.
        """
        # The key in the yaml grids section
        self.name = name

        # A grid includes variables and functions
        self.params = params
        self.args = expand_args(params.get("args", {}))
        self.functions = params.get("functions", {})

        # Cache set to True will pre-calculate grid
        self.cache = params.get("cache", False)
        self.filename = filename

        # Run grid of tests an arbitrary number of times
        self.count = self.params.get("count", 1)

        # Parameter sets are generated when needed unless asked for cache
        self.argsets = []
        if self.cache:
            self.argsets = list(self)

    def __iter__(self):
        """Given input variables, parse into parameter sets. If a variable
           is not provided as a list, we put into list. If a list is desired
           as the variable, it would be provided as a list of lists.
        """
        # If a function has no arguments, won't return values
        try:
            keys, values = zip(*self.args.items())
        except:
            keys = []
            values = []

        values = [[v] if not isinstance(v, list) else v for v in values]

        # Generate parameter sets

        for count in range(self.count):
            for v in itertools.product(*values):
                args = dict(zip(keys, v))
                for varname, funcname in self.functions.items():
                    args[varname] = self.apply_function(funcname, args)
                yield args

    # Functions

    def apply_function(self, funcname, args):
        """Given a function (a name, or a dictionary to derive name and other
           options from) run some set of input variables (that are taken by
           the function) through it to derive a result. The result returned
           is used to set another variable. If a count is defined, we
           run the function (count) times and return a list. Otherwise, we
           run it once.

           Arguments:
            - funcname (str or dict) : the function name or definition
            - args (dict) : lookup of arguments for the function
        """
        # Default count is 1, args == args piped into function
        count = 1
        args = deepcopy(args or {})

        # If funcname is a dictionary, derive values from it
        if isinstance(funcname, dict):

            # If there is a count, we need to multiple it by that
            if "count" in funcname:
                count = funcname["count"]

            # The user wants to map some defined arg to a different argument
            if "args" in funcname:
                for oldkey, newkey in funcname["args"].items():
                    if oldkey in args:
                        args[newkey] = args[oldkey]

            # The function name is required
            if "func" not in funcname:
                bot.exit(f"{funcname} is missing func key with function name.")
            funcname = funcname["func"]

        # Get function and args that are allowed for the function
        func = (
            funcname if not isinstance(funcname, str) else self.get_function(funcname)
        )
        funcargs = intersect_args(func, args)

        # Run the args through the function
        if count == 1:
            return func(**funcargs)
        return [func(**funcargs) for c in range(count)]

    def get_function(self, funcname):
        """Given a function name, return it. Exit on error if not found.
        """
        # Import the function
        sys.path.insert(0, os.path.dirname(self.filename))
        module = ".".join(funcname.split(".")[:-1])
        funcname = funcname.split(".")[-1]
        try:
            module = import_module(module)
            func = getattr(module, funcname)
            if func is None:
                bot.exit(f"Cannot find {funcname}.")
        except:
            bot.exit(f"Cannot import grid function {funcname}")

        return func

    def __repr__(self):
        return "[grid|%s]" % self.name

    def __str__(self):
        return "[grid|%s]" % self.name


# Arguments


def intersect_args(func, args):
    """Given a loaded function and a dictionary of args, return the
       overlapping set (those that are allowed to be given to the 
       function
    """
    argspec = inspect.getfullargspec(func)
    allowed_args = set(argspec.args).intersection(set(args))
    kwargs = {}
    for allowed_arg in allowed_args:
        if allowed_arg in args:
            kwargs[allowed_arg] = args[allowed_arg]

    return kwargs
