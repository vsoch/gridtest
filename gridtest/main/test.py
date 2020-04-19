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

from .generate import import_module
from .workers import Capturing, Workers

import logging
import re
import sys
import os

logger = logging.getLogger(__name__)


class GridTest:
    def __init__(self, module, name, filename=None, params=None, **kwargs):

        self.name = name
        self.module = module
        self.valid = False
        self.params = params or {}
        self.success = False
        self.filename = filename or ""

        # Catching output and error
        self.out = []
        self.err = []

    def __repr__(self):
        return "[task|%s]" % self.name

    def __str__(self):
        return "[task|%s]" % self.name

    # Templating

    def substitute(self, value):
        """Given an input value, return the appropriate substituted string for
           it. This means that {{ args.x }} references can reference arguments
           in params, or {% func %} can refer to a function in the gridtest
           helpers namespace.
        """
        value = self._substitute_args(value)
        value = self._substitute_func(value)

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

    # Running

    def run(self):
        """run an isolated test, and store the return code and result with
           the tester here.
        """
        # Add filename folder to the path
        # TODO: the folder name (and fullpath to file) of the module needs
        # to be stored with the test, in case run from different spot
        sys.path.insert(0, os.path.dirname(self.filename))
        module = import_module(self.module)

        # The function name is the name absent the module
        funcname = re.sub("^%s[.]" % self.module, "", self.name)
        func = getattr(module, funcname)

        if func is None:
            bot.error("Cannot find function.")

        # Case 1: test for returns
        if "returns" in self.params:
            self.test_returns(func, self.params["returns"])

        # Case 2: test raises
        elif "raises" in self.params:
            self.test_raises(func, self.params["raises"])

        # Case 3: test exists
        elif "exists" in self.params:
            self.test_exists(func, self.params["exists"])

        # Case 4: runs just without error
        else:
            self.test_basic(func)

    # Testing

    def test_returns(self, func, value):
        """test that a function returns a particular value. The value might
           reference an input variable, so we use the args dictionary to
           substitute
        """
        self.test_basic(func)
        value = self.substitute(value)
        if value == self.result:
            self.success = True

    def test_runs(self, func):
        """test runs only checks that the function runs without generating
           an error. We don't check for a return value, but we set success to
           be True.
        """
        self.test_basic(func)
        self.success = True

    def test_raises(self, func, exception):
        """Ensure that running a function raises a particular error.
        """
        try:
            self.test_basic(func)
        except Exception as e:
            print(e)
            self.success = True

    def test_basic(self, func):
        """test basic only checks that the function runs without generating
           an error. We don't check for a return value.
        """
        # Run and capture output and error
        with Capturing() as output:
            self.result = func(**self.params["args"])
            if output:
                std = output.pop(0)
                self.out += std.get("out")
                self.err += std.get("err")


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

    def load(self, input_file):
        """load a testing gridtest file.
        """
        input_file = os.path.abspath(input_file)
        if not os.path.exists(input_file):
            sys.exit(f"Cannot find gridtest file {input_file}")
        self.config = read_yaml(input_file)
        self.input_file = input_file

    def set_name(self, name=None):
        """set a custom name. If the user provides a name to the GridRunner,
           this name will be used. Otherwise we use the basename of the input
           file.

           Arguments:
            - name (str): the name of the input file
        """
        self.name = name or os.path.basename(self.input_file)

    def run_tests(self, tests, nproc=9, parallel=True, show_progress=True):
        """run tests. By default, we run them in parallel, unless serial
           is selected.

           Arguments:
            - parallel (bool) : run tasks in parallel (default is True)
            - show_progress (bool) : show progress for tasks
            - nproc (int) : number of processes to run
        """
        if parallel:
            return self._run_parallel(tests, show_progress, nproc=nproc)

        # Otherwise, run in serial
        results = {}

        # Progressbar
        total = len(tests)
        progress = 1

        for name, task in tests.items():
            prefix = "[%s:%s/%s]" % (task.name, progress, total)
            if show_progress:
                bot.show_progress(progress, total, length=35, prefix=prefix)
            else:
                bot.info("Running %s" % prefix)
            results[task.name] = task.run()
            progress += 1

        return results

    def _run_parallel(self, queue, show_progress=True):
        """ run tasks in parallel using the Workers class. Returns a dictionary
            (lookup) wit results, with the key being the task name
            Parameters
            ==========
            queue: the list of task objects to run
        """
        # Run with multiprocessing
        funcs = {}
        tasks = {}

        for task in queue:

            # Export parameters and functions
            funcs[task.name] = task.export_func()
            tasks[task.name] = task.export_params()

        workers = Workers(show_progress=show_progress)
        return workers.run(funcs, tasks)

    def run(self, regexp=None, parallel=True, nproc=None, show_progress=True):
        """run the grid runner, meaning that we turn each function and set of
           tests into a single test, and then run with multiprocessing. 
           This is the function called by the user that also does filtering
           of tests based on a regular expression before calling them.

           Arguments:
              - regexp (str) : if supplied, filter to this pattern 
              - parallel (bool) : use multiprocessing to run tasks (default True)
              - show_progress (bool) : show progress instead of task information
              - nproc (int) : number of processes to use for parallel testing
        """
        # 1. Get filtered list of tests
        tests = self.get_tests(regexp=regexp)

        # 2. Run tests (serial or in parallel)
        results = self.run_tests(
            tests=tests,
            parallel=parallel,
            show_progress=show_progress,
            nproc=nproc or GRIDTEST_WORKERS,
        )

        # TODO how to print to console results? Save to file?
        # TODO check for failed, print failed only if failed

    def get_tests(self, regexp=None):
        """get tests based on a regular expression.

           Arguments:
            - regexp (str) : if provided, only include those tests that match.
        """
        tests = {}
        for parent, section in self.config.items():
            for name, module in section.items():
                if regexp and not re.search(regexp, name):
                    continue
                if name.startswith(parent):

                    # Each module can have a list of tests
                    for idx in range(len(module)):
                        tests[name + ".%s" % idx] = GridTest(
                            module=parent,
                            name=name,
                            params=module[idx],
                            filename=section.get("filename"),
                        )

        return tests

    def __repr__(self):
        return "[gridtest|%s]" % self.name

    def __str__(self):
        return "[gridtest|%s]" % self.name
