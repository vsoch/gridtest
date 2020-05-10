"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.logger import bot
from gridtest.defaults import GRIDTEST_GRIDEXPANDERS
import os


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


def expand_args(args):
    """Given a grid of arguments, expand special cases into longer lists
       of arguments.
       E.g., convert an entry with these keys:
 

       into:

       In the case that a grid has a string identifier to point to a key
       in the lookup, we use that listing of values instead that should
       already be calculated.
    """
    for param, settings in args.items():

        # If settings is a dictionary, it has to be special case
        if isinstance(settings, dict):

            # If any settings defined not allowed, do not continue
            if (
                set(settings.keys()).difference(GRIDTEST_GRIDEXPANDERS)
                and param != "self"
            ):
                bot.exit(f"Invalid key in grid settings {settings}")

            # List of values just for param
            values = []

            # Case 1: min, max, and by
            if "min" in settings and "max" in settings and "by" in settings:
                values += custom_range(settings["min"], settings["max"], settings["by"])
            elif "min" in settings and "max" in settings:
                values += custom_range(settings["min"], settings["max"])

            # Case 2: Add a custom listing to the values
            elif "list" in settings:
                values += settings["list"]

            # Case 3: self refers to a previously generated object (dict allowed)
            elif param == "self":
                values = settings

            args[param] = values
        else:
            args[param] = settings

    return args
