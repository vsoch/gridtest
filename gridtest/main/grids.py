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


def get_grids(lookup, filename=""):
    """given a loaded items (a grids section from a GridRunner). return 
       the parameterized grids.
    """
    grids = {}
    for name, grid in lookup.items():

        # Unwrap list of arguments (even if empty)
        args = expand_args(
            entry={"grid": grid.get("grid", {}), "args": grid.get("args", {})}
        )

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
        grids[name] = args

    return grids
