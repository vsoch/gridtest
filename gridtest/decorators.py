"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

gridtest.func are short functions that serve as helpers for a gridtest.
Any function in here can be referenced as {% func_name %} or with arguments
{% func_name arg1=1 arg2=2 %}. If you possibly have a namespace
conflict, you can also reference {% gridtest.func.func_name %} and
it will work to reference the function here.

"""


import time
import sys
import os


def timeit(func):
    """timeit is a well known Python decorator that will time the total executio
       time for a function. Any output to return to the calling function should
       be printed to stdout, and prefixed with the name of the objective (e.g.,
       @timeit).
    """

    def timed(*args, **kwargs):
        ts = time.time()
        result = func(*args, **kwargs)
        te = time.time()
        print("@timeit  %2.2f ms" % ((te - ts) * 1000))
        return result

    return timed
