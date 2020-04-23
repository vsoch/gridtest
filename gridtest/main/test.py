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

from .generate import import_module, get_function_typing, extract_modulename
from .workers import Workers
from .helpers import test_basic

import logging
import re
import sys
import os

logger = logging.getLogger(__name__)


class GridTest:
    def __init__(
        self,
        module,
        name,
        filename=None,
        params=None,
        verbose=False,
        show_progress=True,
    ):

        self.name = name
        self.module = module
        self.valid = False
        self.params = params or {}
        self.success = False
        self.filename = filename or ""
        self.verbose = verbose
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
        # Valid indices into self.params to substitute
        valid_subs = "^(%s)[.]" % "|".join(["args"])

        # Numbers cannot have replacement
        if not isinstance(value, str):
            return value

        # First do substitutions of variables
        for template in re.findall("{{.+}}", value):
            varname = re.sub("({|}| )", "", template)

            # Varname needs to be in valid namespace (args)
            if not re.search(valid_subs, varname):
                continue

            varname = re.sub(valid_subs, "", varname)

            # Variable name must be in args
            if varname in self.params:
                value = re.sub(template, self.params[varname], value)

        return value

    def _substitute_func(self, value):
        """Given a value, determine if it contains a function substitution,
           and if it's one from gridtest.helpers, return the value with
           the function applied.
        """
        # TODO write me
        return value

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

    def run(self):
        """run an isolated test, and store the return code and result with
           the tester here.
        """
        if not self.show_progress:
            bot.info(f"Running test {name}")

        # [passe, result, out, err, raises]
        passed, result, out, err, raises = test_basic(
            funcname=self.get_funcname(),
            module=self.module,
            filename=self.filename,
            args=self.params.get("args", {}),
            returns=self.params.get("returns"),
        )

        self.success = passed
        self.result = result
        self.out = out
        self.err = err
        self.raises = raises

        # Finish by checking output
        self.check_output()

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

        # If expected success or failure, and got opposite
        if "success" in self.params:
            if not self.params["success"] and not self.success:
                self.out.append("success key set to false, expected failure.")
                self.success = True

    def check_returns(self, value):
        """test that a function returns a particular value. The value might
           reference an input variable, so we use the args dictionary to
           substitute
        """
        value = self.substitute(value)
        if value == self.result:
            self.success = True

    def check_raises(self, exception):
        """Ensure that running a function raises a particular error. If the
           function runs successfully, this is considered a failure.
        """
        # Case 1: no exception thrown
        if not self.raises:
            self.success = False
            self.err.append(f"Expected exception {exception} not raised")

        # Case 2: correct exception thrown
        elif self.raises == exception:
            self.success = True
        else:
            self.err.append(
                f"Expected exception {exception}, instead raised {self.raises}"
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

    def run_tests(self, tests, nproc=9, parallel=True):
        """run tests. By default, we run them in parallel, unless serial
           is selected.

           Arguments:
            - parallel (bool) : run tasks in parallel (default is True)
            - nproc (int) : number of processes to run
        """
        if parallel:
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
                task.run()
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
        self, regexp=None, parallel=True, nproc=None, show_progress=True, verbose=False
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
        """
        # 1. Get filtered list of tests
        tests = self.get_tests(regexp=regexp, verbose=verbose)
        self.show_progress = show_progress

        # 2. Run tests (serial or in parallel)
        self.run_tests(
            tests=tests, parallel=parallel, nproc=nproc or GRIDTEST_WORKERS,
        )

        # Pretty print results to screen
        self.print_results(tests)

        # Exit with correct error code
        if self.failed(tests):
            sys.exit(1)

        # TODO add param to save to file
        sys.exit(0)

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

    def get_tests(self, regexp=None, verbose=False):
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
                            filename=filename,
                            show_progress=self.show_progress,
                        )

        return tests

    def __repr__(self):
        return "[gridtest|%s]" % self.name

    def __str__(self):
        return "[gridtest|%s]" % self.name
