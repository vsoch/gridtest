"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.logger import bot
from gridtest.defaults import GRIDTEST_WORKERS
import multiprocessing
import itertools
from io import StringIO
import time
import signal
import sys
import os


class Workers(object):
    def __init__(self, workers=None, show_progress=False):

        if workers is None:
            workers = GRIDTEST_WORKERS
        self.workers = workers
        self.show_progress = show_progress
        bot.debug("Using %s workers for multiprocess." % (self.workers))

    def start(self):
        bot.debug("Starting multiprocess")
        self.start_time = time.time()

    def end(self):
        self.end_time = time.time()
        self.runtime = self.runtime = self.end_time - self.start_time
        bot.debug("Ending multiprocess, runtime: %s sec" % (self.runtime))

    def run(self, tests):
        """run will execute a test for each entry in the list of tests.
           the result of the test, and error codes, are saved with the test.
        
           Arguments:
               - tests (gridtest.main.test.GridTest) : the GridTest object
        """

        # Keep track of some progress for the user
        total = len(tests)
        progress = 1

        # Cut out early if no tests
        if not tests:
            return

        results = []

        try:
            prefix = "[%s/%s]" % (progress, total)
            if self.show_progress:
                bot.show_progress(0, total, length=35, prefix=prefix)
            pool = multiprocessing.Pool(self.workers, init_worker)

            self.start()
            for name, task in tests.items():

                # Get the function name from the tester
                params = {
                    "gridtest_funcname": task.get_funcname(),
                    "gridtest_module": task.module,
                    "gridtest_filename": task.filename,
                    "gridtest_args": task.params.get("args", {}),
                    "gridtest_returns": task.params.get("returns"),
                }
                if not self.show_progress:
                    bot.info(f"Running test {name}")
                result = pool.apply_async(
                    multi_wrapper, multi_package(test_basic, [params])
                )

                # result returns [passed, result, out, error]
                # Store the test with the result
                results.append((task, result))

            while results:
                pair = results.pop()
                test, result = pair
                result.wait()
                if self.show_progress:
                    bot.show_progress(progress, total, length=35, prefix=prefix)
                progress += 1
                prefix = "[%s/%s]" % (progress, total)

                # Update the task with the result
                passed, result, out, err, raises = result.get()
                test.out = out
                test.err = err
                test.success = passed
                test.result = result
                test.raises = raises

            self.end()
            pool.close()
            pool.join()

        except (KeyboardInterrupt, SystemExit):
            bot.error("Keyboard interrupt detected, terminating workers!")
            pool.terminate()
            sys.exit(1)

        except:
            bot.exit("Error running task.")


# Supporting functions for MultiProcess Worker
class Capturing(list):
    """capture output from stdout and stderr into capture object"""

    def __enter__(self):
        self.set_stdout()
        self.set_stderr()
        return self

    def set_stdout(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio_out = StringIO()

    def set_stderr(self):
        from io import StringIO

        self._stderr = sys.stderr
        sys.stderr = self._stringio_err = StringIO()

    def __exit__(self, *args):
        self.append(
            {
                "out": self._stringio_out.getvalue().splitlines(),
                "err": self._stringio_err.getvalue().splitlines(),
            }
        )
        del self._stringio_out

        # Restore previous stdout, stderr
        sys.stdout = self._stdout
        sys.stderr = self._stderr


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def multi_wrapper(func_args):
    function, kwargs = func_args
    return function(**kwargs)


def multi_package(func, kwargs):
    zipped = zip(itertools.repeat(func), kwargs)
    return zipped


def test_basic(
    gridtest_funcname,
    gridtest_module,
    gridtest_filename,
    gridtest_args=None,
    gridtest_returns=None,
):
    """test basic is a worker version of the task.test_basic function.
       It works equivalently but is not attached to a class, and returns
       a list of values for [passed, result, out, err, raises]
    """
    from gridtest.main.workers import test_types, Capturing
    from gridtest.main.generate import import_module

    sys.path.insert(0, os.path.dirname(gridtest_filename))
    module = import_module(gridtest_module)
    func = getattr(module, gridtest_funcname)

    passed = False
    result = None
    raises = None
    out = []
    err = []

    if not func:
        err = [f"Cannot find function {gridtest_funcname}"]

    else:
        passed, error = test_types(func, gridtest_args, gridtest_returns)
        err += error

        # if type checking passes
        if passed:

            # Run and capture output and error
            with Capturing() as output:
                try:
                    result = func(**args)
                    if output:
                        std = output.pop(0)
                        out += std.get("out")
                        err += std.get("err")
                    passed = True
                except Exception as e:
                    raises = type(e).__name__

    return [passed, result, out, err, raises]


def test_types(func, args=None, returns=None):
    """Given a loaded function, get it's types and ensure that they are
       correct. Returns a boolean to indicate correct/ passing (True)
    """
    from gridtest.main.generate import get_function_typing

    args = args or {}
    err = []

    # Check arguments first
    types = get_function_typing(func)
    for argname, argtype in types.items():
        if argname in args:
            value = args[argname]
            if not isinstance(value, argtype):
                err.append(
                    "TypeError %s (%s) is %s, should be %s"
                    % (argname, value, type(value), argtype)
                )
                return False, err

    # Check return type
    if "return" in types and returns:
        if not isinstance(returns, types["return"]):
            err.append(
                "TypeError return value %s should be %s" % (returns, types["return"])
            )
            return False, err

    return True, err
