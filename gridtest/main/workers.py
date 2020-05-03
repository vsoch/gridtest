"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.logger import bot
from gridtest.defaults import GRIDTEST_WORKERS
from gridtest.main.helpers import test_types, test_basic, Capturing
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

    def run(self, tests, cleanup=True):
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
        to_cleanup = []

        try:
            prefix = "[%s/%s]" % (progress, total)
            if self.show_progress:
                bot.show_progress(0, total, length=35, prefix=prefix)
            pool = multiprocessing.Pool(self.workers, init_worker)

            self.start()
            for name, task in tests.items():

                # If a class is returned, needs to be in path too
                sys.path.insert(0, os.path.dirname(task.filename))

                # Get the function name from the tester
                params = {
                    "funcname": task.get_funcname(),
                    "module": task.module,
                    "filename": task.filename,
                    "metrics": task.params.get("metrics", []),
                    "args": task.params.get("args", {}),
                    "returns": task.params.get("returns"),
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


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def multi_wrapper(func_args):
    function, kwargs = func_args
    return function(**kwargs)


def multi_package(func, kwargs):
    zipped = zip(itertools.repeat(func), kwargs)
    return zipped
