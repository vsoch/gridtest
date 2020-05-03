"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""


import multiprocessing
import os
import sys


def getenv(variable_key, default=None, required=False, silent=True):
    """ attempt to get an environment variable. If the variable
        is not found, None is returned.

        Arguments:

         - variable_key (str) : the variable name
         - required (bool) : exit with error if not found
         - silent (bool) : Do not print debugging information
    """
    variable = os.environ.get(variable_key, default)
    if variable is None and required:
        bot.error("Cannot find environment variable %s, exiting." % variable_key)
        sys.exit(1)

    if not silent and variable is not None:
        bot.verbose("%s found as %s" % (variable_key, variable))

    return variable


GRIDTEST_NPROC = multiprocessing.cpu_count()
GRIDTEST_WORKERS = int(getenv("GRIDTEST_WORKERS", GRIDTEST_NPROC * 2 + 1))
GRIDTEST_SHELL = getenv("GRIDTEST_SHELL", "ipython")
GRIDTEST_RETURNTYPES = ["raises", "returns", "exists", "istrue", "isfalse"]
GRIDTEST_GRIDEXPANDERS = ["min", "max", "by", "list"]

# Known default functions
GRIDTEST_FUNCS = ["tmp_dir", "tmp_path"]
