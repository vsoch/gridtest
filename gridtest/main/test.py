"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.defaults import GRIDTEST_WORKERS
from gridtest.utils import read_yaml
from gridtest.logger import bot
from gridtest import __version__

from gridtest.main.generate import (
    import_module,
    get_function_typing,
    extract_modulename,
)
from gridtest.main.workers import Workers
from gridtest.main.helpers import test_basic
from gridtest.main.substitute import substitute_func, substitute_args

import re
import sys
import os


class GridTest:
    def __init__(
        self,
        module,
        name,
        func=None,
        filename=None,
        params=None,
        verbose=False,
        cleanup=True,
        show_progress=True,
    ):

        self.name = name
        self.func = func
        self.module = module
        self.valid = False
        self.params = params or {}
        self.success = False
        self.filename = filename or ""
        self.verbose = verbose
        self.cleanup = cleanup
        self.show_progress = show_progress
        self.result = None
        self.raises = None

        # Catching output and error
        self.out = []
        self.err = []

    def __repr__(self):
        return "[test|%s]" % self.name

    def __str__(self):
        return "[test|%s]" % self.name

    # Templating

    def substitute(self, value):
        """Given an input value, return the appropriate substituted string for
           it. This means that {{ args.x }} references can reference arguments
           in params, or {% func %} can refer to a function in the gridtest
           helpers namespace.
        """
        value = self._substitute_args(value)
        value = self._substitute_func(value)
        return value

    def _substitute_args(self, value):
        """Given a value, determine if it has variable argument substitutions
           in the format of {{ args.<name> }} and if so, if the argument is present
           return the value with the substitution.
        """
        if not isinstance(value, str):
            return value

        # We allow for namespacing of args, right now only supports args
        value = re.sub("args[.]", "", value, 1)
        return substitute_args(value, params=self.params["args"])

    def _substitute_func(self, value):
        """Given a value, determine if it contains a function substitution,
           and do it. See gridtest.main.helpers.substitute_func. for details.
        """
        return substitute_func(value)

    # Summary
    @property
    def summary(self):
        """print a summary of the test, including if it is supposed to
           return, raise, or check existance.
        """
        if self.success:
            return self._summary_success()
        return self._summary_failure()

    def _summary_success(self):
        """return successful summary
        """
        output = "".join(self.out) if self.verbose else ""

        if "returns" in self.params:
            return "returns %s %s" % (self.params["returns"], output)
        elif "raises" in self.params:
            return "raises %s %s" % (self.params["raises"], output)
        elif "exists" in self.params:
            return "exists %s %s" % (self.params["exists"], output)
        return output

    def _summary_failure(self):
        """Return a failure message, including error
        """
        error = " ".join(self.err)
        if "returns" in self.params:
            return "returns %s %s" % (self.params["returns"], error)
        elif "raises" in self.params:
            return "raises %s %s" % (self.params["raises"], error)
        elif "exists" in self.params:
            return "exists %s %s" % (self.params["exists"], error)
        return error

    # Running

    def get_func(self):
        """Get the function name, meaning we get the module first.
        """
        sys.path.insert(0, os.path.dirname(self.filename))
        module = import_module(self.module)
        func = getattr(module, self.get_funcname())
        if func is None:
            bot.error("Cannot find function.")
        return func

    def get_funcname(self):
        """Get the function name, meaning we get the module first.
        """
        # The function name is the name absent the module
        return re.sub("^%s[.]" % self.module, "", self.name)

    def run(self, interactive=False, cleanup=None):
        """run an isolated test, and store the return code and result with
           the tester here. 

           Arguments:
            - interactive (bool) : run interactively for shell to debug
            - cleanup (bool) : remove any temporary directories or files (True)
        """
        if not self.show_progress:
            bot.info(f"Running test {name}")

        # Should we clean up temporary files produced?
        if cleanup:
            self.cleanup = cleanup
        to_cleanup = []

        # Handle argument substitution
        for name, value in self.params.get("args", {}).items():
            new_value = self.substitute(value)
            self.params["args"][name] = new_value

            # If the action is a gridtest function, handle cleanup
            if re.sub("({%|%}| )", "", value) in ["tmp_dir", "tmp_path"]:
                to_cleanup.append(new_value)

        # [passed, result, out, err, raises]
        passed, result, out, err, raises = test_basic(
            funcname=self.get_funcname(),
            module=self.module,
            func=self.func,
            filename=self.filename,
            args=self.params.get("args", {}),
            returns=self.params.get("returns"),
            interactive=interactive,
        )

        self.success = passed
        self.result = result
        self.out = out
        self.err = err
        self.raises = raises

        # Finish by checking output
        self.check_output()
        if self.cleanup:
            self.cleanup(to_cleanup)

    # Checking Results

    def check_output(self):
        """Given that self.result is defined, check final output for the test.
           This works (and is called) after self.run(), OR by the multiprocessing
           worker that has updated self.result. Each of the actions below
           does additional parsing of the result, and the client will update
           self.success to be False if there is an issue.
        """
        # Case 1: test for returns
        if "returns" in self.params:
            self.check_returns(self.params["returns"])

        # Case 2: test raises
        elif "raises" in self.params:
            self.check_raises(self.params["raises"])

        # Case 3: test exists
        elif "exists" in self.params:
            self.check_exists(self.params["exists"])

        # Case 4: An error was raised (not expected)
        if self.raises and "raises" not in self.params:
            self.err.append(f"Unexpected Exception: {self.raises}.")
            self.success = False

        # If expected success or failure, and got opposite
        if "success" in self.params:
            if not self.params["success"] and not self.success:
                self.out.append("success key set to false, expected failure.")
                self.success = True

    def cleanup(self, paths):
        """Given a list of paths (files or folders) generated by gridtest,
           clean them up with shutil.rm
        """
        for path in paths:
            if os.path.isfile(path):
                print(f"Cleaning up file {path}")
            elif os.path.isfile(path):
                print(f"Cleaning up directory {path}")

    def check_exists(self, filename):
        """check if a filename exists.
        """
        self.success = False
        if os.path.exists(filename):
            self.success = True

    def check_returns(self, value):
        """test that a function returns a particular value. The value might
           reference an input variable, so we use the args dictionary to
           substitute
        """
        self.success = False
        value = self.substitute(value)
        if value == self.result:
            self.success = True

    def check_raises(self, exception):
        """Ensure that running a function raises a particular error. If the
           function runs successfully, this is considered a failure.
        """
        self.success = False

        # Case 1: no exception thrown
        if not self.raises:
            self.success = False
            self.err.append(f"Expected exception {exception} not raised")

        # Case 2: correct exception thrown
        elif self.raises == exception:
            self.success = True
            self.out.append(f"Exception: {self.raises} raised as desired.")
        else:
            self.err.append(
                f"Expected exception {exception}, instead raised {self.raises}"
            )


class GridTestFunc(GridTest):
    """a function can be loaded from within Python with GridTestFunc.
    """

    def __init__(
        self, func, params=None, verbose=False, show_progress=True,
    ):
        super().__init__(
            module=func.__module__,
            func=func,
            name=func.__name__,
            params=params,
            verbose=verbose,
            show_progress=show_progress,
        )


class GridRunner:
    def __init__(self, input_file, **kwargs):
        """the grid tester loads a gridtest specification file,
           and then deploys testing workers to run the tests.

           Arguments:

           input_file (str) : the watcher name, defaults to github
           kwargs: should include command line arguments from the client.
        """
        self.config = {}
        self._version = __version__
        self.load(input_file)
        self.set_name(kwargs.get("name"))
        self.show_progress = True

    def load(self, input_file):
        """load a testing gridtest file.
        """
        input_file = os.path.abspath(input_file)
        if not os.path.exists(input_file):
            sys.exit(f"Cannot find gridtest file {input_file}")
        self.config = read_yaml(input_file)
        self.input_file = input_file
        self.input_dir = os.path.dirname(input_file)

    def set_name(self, name=None):
        """set a custom name. If the user provides a name to the GridRunner,
           this name will be used. Otherwise we use the basename of the input
           file.

           Arguments:
            - name (str): the name of the input file
        """
        self.name = name or os.path.basename(self.input_file)

    def run_tests(self, tests, nproc=9, parallel=True, interactive=False):
        """run tests. By default, we run them in parallel, unless serial
           is selected.

           Arguments:
            - parallel (bool) : run tasks in parallel that are able (default is True)
            - nproc (int) : number of processes to run
            - cleanup (bool) : clean up files/dir generated with tmp_path, tmp_dir
            - interactive (bool) : run jobs interactively (for debugging)
              not available for parallel jobs.
        """
        # Parallel tests cannot be interactive
        if parallel and not interactive:
            self._run_parallel(tests, nproc=nproc)

        else:
            total = len(tests)
            progress = 1

            for name, task in tests.items():
                prefix = "[%s:%s/%s]" % (task.name, progress, total)
                if self.show_progress:
                    bot.show_progress(progress, total, length=35, prefix=prefix)
                else:
                    bot.info("Running %s" % prefix)

                # Run the task, update results with finished object
                task.run(interactive=interactive)
                progress += 1

        return tests

    def _run_parallel(self, tests, nproc=GRIDTEST_WORKERS):
        """run tasks in parallel using the Workers class. Returns the same
           tests results, but after running.

           Arguments:
              - queue: the list of task objects to run
        """
        workers = Workers(show_progress=self.show_progress, workers=nproc)
        workers.run(tests)

        # Run final checks
        for name, test in tests.items():
            test.check_output()

        return tests

    def run(
        self,
        regexp=None,
        parallel=True,
        nproc=None,
        show_progress=True,
        verbose=False,
        interactive=False,
        cleanup=True,
    ):
        """run the grid runner, meaning that we turn each function and set of
           tests into a single test, and then run with multiprocessing. 
           This is the function called by the user that also does filtering
           of tests based on a regular expression before calling them.

           Arguments:
              - regexp (str) : if supplied, filter to this pattern 
              - parallel (bool) : use multiprocessing to run tasks (default True)
              - show_progress (bool) : show progress instead of task information
              - nproc (int) : number of processes to use for parallel testing
              - verbose (bool) : print success output too
              - interactive (bool) : interactively debug functions
              - cleanup (bool) : cleanup files/directories generated with tmp_path tmp_dir
        """
        # 1. Get filtered list of tests
        tests = self.get_tests(regexp=regexp, verbose=verbose, cleanup=cleanup)
        self.show_progress = show_progress

        # 2. Run tests (serial or in parallel)
        self.run_tests(
            tests=tests,
            parallel=parallel,
            nproc=nproc or GRIDTEST_WORKERS,
            interactive=interactive,
        )

        # Pretty print results to screen
        self.print_results(tests)

        # return correct error code
        if self.failed(tests):
            return 1
        return 0

    def success(self, tests):
        """Given a test of tests, return True if all are successful.
        """
        return all([test.success for name, test in tests.items()])

    def failed(self, tests):
        """Given a test of tests, return True if any are not successful.
        """
        return not self.success(tests)

    def print_results(self, tests):
        """print the results of the tests, meaning that success is in green,
           and non-success is in red.
        """
        total = 0
        success = 0
        failure = 0

        for name, test in tests.items():
            total += 1
            if test.success:
                bot.success(f"success: {name} {test.summary}")
                success += 1
            else:
                bot.failure(f"failure: {name} {test.summary}")
                failure += 1

        print(f"{success}/{total} tests passed")

    def get_tests(self, regexp=None, verbose=False, cleanup=True):
        """get tests based on a regular expression.

           Arguments:
            - regexp (str) : if provided, only include those tests that match.
        """
        tests = {}
        for parent, section in self.config.items():
            for name, module in section.items():
                if regexp and not re.search(regexp, name):
                    continue

                # Each module can have a list of tests
                if name.startswith(parent):

                    # Get either the file path, module name, or relative path
                    filename = extract_modulename(
                        section.get("filename"), self.input_dir
                    )

                    for idx in range(len(module)):
                        tests["%s.%s" % (name, idx)] = GridTest(
                            module=parent,
                            name=name,
                            params=module[idx],
                            verbose=verbose,
                            cleanup=cleanup,
                            filename=filename,
                            show_progress=self.show_progress,
                        )

        return tests

    def __repr__(self):
        return "[gridtest|%s]" % self.name

    def __str__(self):
        return "[gridtest|%s]" % self.name
