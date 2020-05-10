"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.defaults import (
    GRIDTEST_WORKERS,
    GRIDTEST_RETURNTYPES,
)
from gridtest.templates import copy_template
from gridtest.utils import read_yaml, write_yaml, write_json
from gridtest.logger import bot
from gridtest import __version__

from gridtest.main.generate import (
    import_module,
    get_function_typing,
    extract_modulename,
)
from gridtest.main.grids import Grid
from gridtest.main.helpers import test_basic
from gridtest.main.workers import Workers
from gridtest.main.substitute import substitute_func, substitute_args
from copy import deepcopy

import itertools
import re
import shutil
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
        self.success = False
        self.filename = filename or ""
        self.verbose = verbose
        self.cleanup_temp = cleanup
        self.to_cleanup = set()
        self.show_progress = show_progress
        self.result = None
        self.raises = None

        # Catching output and error
        self.out = []
        self.err = []
        self.metrics = {}

        # Parse input arguments
        self.set_params(params)

    def __repr__(self):
        return "[test|%s]" % self.name

    def __str__(self):
        return "[test|%s]" % self.name

    # Templating

    def set_params(self, params):
        """Given params with args that are loaded, making substitutions
           at the onset of generating the test. Also keep track of
           any directories / files defined by tmp_path and tmp_dir
           to clean up after the test is run.
        """
        self.params = params or {}
        for name, value in self.params.get("args", {}).items():
            new_value = self.substitute(value)
            self.params["args"][name] = new_value

            # If the action is a gridtest function, handle cleanup
            if isinstance(value, str) and re.sub("({%|%}| )", "", value) in [
                "tmp_dir",
                "tmp_path",
            ]:
                self.to_cleanup.add(new_value)

        # Set backup params, in case we reset
        self._params = deepcopy(self.params)

    def substitute(self, value):
        """Given an input value, return the appropriate substituted string for
           it. This means that {{ args.x }} references can reference arguments
           in params, or {% func %} can refer to a function in the gridtest
           helpers namespace.
        """
        value = self._substitute_args(value)
        value = self._substitute_func(value)
        return value

    def post_substitute(self):
        """After a run, sometimes we want to check the result (whatever it is)
        """
        # Run substitution for custom sections
        for section in GRIDTEST_RETURNTYPES:
            if section in self.params:
                self.params[section] = self.substitute(self.params[section])

    def _substitute_args(self, value):
        """Given a value, determine if it has variable argument substitutions
           in the format of {{ args.<name> }} and if so, if the argument is present
           return the value with the substitution.
        """
        if not isinstance(value, str):
            return value

        # Returns is a special case, this checks for returns param
        if re.search(r"{{(\s+)?returns(\s)?}}", value) and "returns" in self.params:
            value = substitute_args(value, params=self.params)

        # Result is a special case that works after a test is run
        if re.search(r"{{(\s+)?result(\s)?}}", value) and self.result:
            value = substitute_args(value, params={"result": self.result})

        # We allow for namespacing of args, right now only supports args
        value = re.sub("args[.]", "", value, 1)
        return substitute_args(value, params=self.params.get("args", {}))

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
            return self.summary_success()
        return self.summary_failure()

    # Running

    def get_func(self):
        """Get the function name, meaning we get the module first. This can
           also be used for one off (custom) function and module names.
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
        if cleanup is not None:
            self.cleanup_temp = cleanup

        # [passed, result, out, err, raises]
        passed, result, out, err, raises = test_basic(
            funcname=self.get_funcname(),
            module=self.module,
            func=self.func,
            filename=self.filename,
            metrics=self.params.get("metrics", []),
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
        if self.cleanup_temp:
            self.cleanup()

    # Checking Results

    def check_output(self):
        """Given that self.result is defined, check final output for the test.
           This works (and is called) after self.run(), OR by the multiprocessing
           worker that has updated self.result. Each of the actions below
           does additional parsing of the result, and the client will update
           self.success to be False if there is an issue.
        """
        # Do final substitution
        self.post_substitute()

        # If decorators provided, parse their output
        self.check_metrics()

        # Set 1: test for returns
        if "returns" in self.params:
            self.check_returns(self.params["returns"])

        # Set 2: test raises
        if "raises" in self.params:
            self.check_raises(self.params["raises"])

        # Set 3: test exists
        if "exists" in self.params:
            self.check_exists(self.params["exists"])

        # Set 4: Determine if a statement is true or false
        if "istrue" in self.params:
            self.check_istrue(self.params["istrue"])
        if "isfalse" in self.params:
            self.check_isfalse(self.params["isfalse"])
        if "equals" in self.params:
            self.check_equals(self.params["equals"])
        if "isinstance" in self.params:
            self.check_isinstance(self.params["isinstance"])

        # Set 5: An error was raised (not expected)
        if self.raises and "raises" not in self.params:
            self.err.append(f"Unexpected Exception: {self.raises}.")
            self.success = False

        # If expected success or failure, and got opposite
        if "success" in self.params:
            if not self.params["success"] and not self.success:
                self.out.append("success key set to false, expected failure.")
                self.success = True

    # Checks

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

    def check_isinstance(self, instance):
        """check if the result is of a particular type
        """
        if not type(self.result).__name__ == instance:
            self.err.append(
                f"{type(self.result).__name__} is not instance of {instance}"
            )
            self.success = False

    def check_istrue(self, statement):
        """check if a statement is true.
        """
        if not eval(str(statement)) == True:
            self.success = False

    def check_isfalse(self, statement):
        """check if a statement is false
        """
        if not eval(str(statement)) == False:
            self.success = False

    def check_equals(self, statement):
        """check if a result equals some statement.
        """
        if not eval(str(statement)) == self.result:
            self.success = False

    def check_metrics(self):
        """After runs are complete, given metrics defined in params, parse
           over the list and look for metric output in the output (and remove)
        """
        metrics = self.params.get("metrics")
        if metrics:
            regex = "^(%s)" % "|".join(metrics)
            self.metrics = {k: [] for k in metrics}
            for line in self.out:
                for metric in metrics:
                    if line.startswith(metric):
                        self.metrics[metric].append(line.replace(metric, "", 1).strip())
            self.out = [x for x in self.out if not re.search(regex, x)]

    # Cleanup and reset

    def cleanup(self):
        """Given a list of paths (files or folders) generated by gridtest,
           clean them up with shutil.rm
        """
        if self.cleanup_temp:
            bot.debug("Skipping cleanup.")
        else:
            for path in self.to_cleanup:
                if os.path.isfile(path):
                    bot.debug(f"Cleaning up file {path}")
                    os.remove(path)
                elif os.path.isfile(path):
                    bot.debug(f"Cleaning up directory {path}")
                    shutil.rmtree(path)

    def reset(self):
        """reset a test to it's original state, meaning that original parameters,
           the result, raises, etc. are reset.
        """
        self.params = deepcopy(self._params)
        self.result = None
        self.raises = None
        self.valid = False
        self.success = False
        self.to_cleanup = set()
        self.out = []
        self.err = []

    def _summary(self, out):
        """return summary for specific output (or error) stream
        """
        output = "".join(out) if self.verbose else ""
        for key in [
            "returns",
            "raises",
            "exists",
            "istrue",
            "isfalse",
            "equals",
            "isinstance",
        ]:
            if key in self.params:
                output += " %s %s" % (key, self.params[key])
        return output.strip()

    def summary_success(self):
        return self._summary(self.out)

    def summary_failure(self):
        return self._summary(self.err)


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
        self._fill_classes()
        self.show_progress = True
        self.grids = {}

    def load(self, input_file):
        """load a testing gridtest file.
        """
        input_file = os.path.abspath(input_file)
        if not os.path.exists(input_file):
            sys.exit(f"Cannot find gridtest file {input_file}")
        if not re.search("(yml|yaml)$", input_file):
            sys.exit("Please provide a yaml file (e.g., gridtest.yml) to test.")
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

    def iter_tests(self):
        for _, section in self.config.items():
            for name, tests in section.get("tests", {}).items():
                yield (name, tests)

    def iter_grids(self):
        for name, grid in self.grids.items():
            yield (name, grid)

    def _fill_classes(self):
        """Read in a config, and create a lookup for any instance variables. Then
           substitute arguments (starting with instance) for these variables.
        """
        # First create the lookup
        self.lookup = dict()
        for name, tests in self.iter_tests():
            for test in tests:
                if "instance" in test:
                    self.lookup[test["instance"]] = test

        # Now fill in variables
        for name, tests in self.iter_tests():
            for test in tests:
                if "self" in test.get("args", {}):
                    if not test["args"]["self"]:
                        sys.exit(
                            "%s: please define an instance to use with 'self: {{ instance.name }}'"
                            % name
                        )
                    if re.search("{{.+}}", test["args"]["self"]):
                        instance = re.sub(
                            "({{|}}|instance[.])", "", test["args"]["self"]
                        ).strip()
                        if instance in self.lookup:
                            test["args"]["self"] = self.lookup[instance]

    def run_tests(self, tests, nproc=9, parallel=True, interactive=False, name=None):
        """run tests. By default, we run them in parallel, unless serial
           is selected.

           Arguments:
            - parallel (bool) : run tasks in parallel that are able (default is True)
            - nproc (int) : number of processes to run
            - cleanup (bool) : clean up files/dir generated with tmp_path, tmp_dir
            - name (str) : the name of a test to interact with
            - interactive (bool) : run jobs interactively (for debugging)
              not available for parallel jobs.
        """
        # Parallel tests cannot be interactive
        if parallel and not interactive:
            self._run_parallel(tests, nproc=nproc)

        else:
            total = len(tests)
            progress = 1

            for _, task in tests.items():
                prefix = "[%s:%s/%s]" % (task.name, progress, total)
                if self.show_progress:
                    bot.show_progress(progress, total, length=35, prefix=prefix)
                else:
                    bot.info("Running %s" % prefix)

                # Should this be interactive?
                is_interactive = interactive
                if name is not None and interactive:
                    if not task.name.startswith(name):
                        is_interactive = False

                # Run the task, update results with finished object
                task.run(interactive=is_interactive)
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
            if test.cleanup_temp:
                test.cleanup()

        return tests

    def run(
        self,
        regexp=None,
        parallel=True,
        nproc=None,
        show_progress=True,
        verbose=False,
        interactive=False,
        name=None,
        cleanup=True,
        save=None,
        save_report=None,
        save_compact=False,
        report_template="report",
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
              - name (str) : if specified, a name of a test to interact with
              - cleanup (bool) : cleanup files/directories generated with tmp_path tmp_dir
              - save (str) : a filepath to save results to (must be json)
              - save_report (str) : path to folder (not existing) to save a report to
              - report_template (str) : a template name of a report to generate

        """
        # 1. Generate list of tests and grid functions
        self.show_progress = show_progress
        self.get_grids()

        tests = self.get_tests(regexp=regexp, verbose=verbose, cleanup=cleanup)

        # Pretty print results to screen
        if not tests:
            bot.exit_info("No tests to run.")

        # 2. Run tests (serial or in parallel)
        self.run_tests(
            tests=tests,
            parallel=parallel,
            nproc=nproc or GRIDTEST_WORKERS,
            interactive=interactive,
            name=name,
        )

        self.print_results(tests)

        # Save report?
        if save_report:
            report_dir = self.save_report(save_report, report_template)
            save = os.path.join(report_dir, "results.json")

        # Save to file (required for report)
        if save:
            self.save_results(save, tests, save_compact)

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

    def save(self, testfile):
        """Save the runner.config to an output yaml file.
        """
        bot.info(f"Writing {self} to {testfile}")
        write_yaml(self.config, testfile)

    def save_report(self, report_dir, report_template):
        """save a runner results to file.
        """
        report_dir = os.path.abspath(report_dir)

        # Report directory cannot already exist
        if os.path.exists(report_dir):
            bot.exit(f"{report_dir} already exists, please remove before using.")

        dest = copy_template(report_template, report_dir)
        if not dest:
            bot.exit(f"Error writing to {dest}.")
        return dest

    def save_results(self, filename, tests, save_compact):
        """save a runner results to file.
        """
        filename = os.path.abspath(filename)
        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            bot.exit(f"{dirname} does not exist, skipping save.")

        elif not filename.endswith(".json"):
            bot.warning(f"{dirname} must be extension .json, skipping save.")

        else:
            results = []
            for key, test in tests.items():

                if test.params.get("save", True) == False:
                    continue

                # If the result is instance, convert
                results.append(
                    {
                        "name": key,
                        "function": test.name,
                        "filename": test.filename,
                        "out": test.out,
                        "err": test.err,
                        "result": test.result,
                        "params": test.params,
                        "raises": test.raises,
                        "success": test.success,
                        "metrics": test.metrics,
                        "module": test.module,
                    }
                )
            write_json(results, filename, pretty=not save_compact)
            return filename

    def print_results(self, tests):
        """print the results of the tests, meaning that success is in green,
           and non-success is in red.
        """
        total = 0
        success = 0
        failure = 0
        has_metrics = False

        print("{:<30} {:<30} {:<30}".format("Name", "Status", "Summary"))
        print("{:_<120}".format(""))

        for name, test in tests.items():
            total += 1
            if test.metrics:
                has_metrics = True
            if test.success:
                bot.success(
                    "{:<30} {:<30} {:<30}".format(name, "success", test.summary)
                )
                success += 1
            else:
                bot.failure(f"failure: {name} {test.summary}")
                failure += 1

        if has_metrics:
            print("\n{:_<120}".format(""))
        for name, test in tests.items():
            for metric, result in test.metrics.items():
                print("{:<30} {:<30} {:<30}".format(name, metric, "|".join(result)))

        print(f"\n{success}/{total} tests passed")

    def get_grids(self):
        """a grid is a specification under "grids" that can be run to
           parameterize a set of arguments, optionally run through a function
           or just generated to have combinations. If a count variable is
           included, we multiply by that many times.
        """
        for parent, section in self.config.items():
            filename = extract_modulename(section.get("filename", ""), self.input_dir)
            for name, grid in section.get("grids", {}).items():
                self.grids[name] = Grid(name=name, params=grid, filename=filename)
        return self.grids

    def get_tests(self, regexp=None, verbose=False, cleanup=True):
        """get tests based on a regular expression.

           Arguments:
            - regexp (str) : if provided, only include those tests that match.
        """
        tests = {}

        for parent, section in self.config.items():
            for name, module in section.get("tests", {}).items():

                if regexp and not re.search(regexp, name):
                    continue

                # Get either the file path, module name, or relative path
                filename = extract_modulename(
                    section.get("filename", ""), self.input_dir
                )

                idx = 0

                # Use idx to index each test with parameters
                for entry in module:
                    grid = None

                    # Grid and args cannot both be defined
                    if "args" in entry and "grid" in entry:
                        bot.exit(f"{name} has defined both a grid and args.")

                    # If we find a grid, it has to reference an existing grid
                    if "grid" in entry and entry["grid"] not in self.grids:
                        bot.exit(
                            f"{name} needs grid {entry['grid']} but not found in grids."
                        )

                    # If we find a grid, it has to reference an existing grid
                    if "grid" in entry and entry["grid"] in self.grids:
                        grid = self.grids[entry["grid"]]
                        params = deepcopy(entry)
                        for key in ["grid", "instance"]:
                            if key in params:
                                del params[key]
                        grid.params.update(params)

                    # A class function is tested over it's instance grid
                    instance_grid = [{}]

                    # If entry is defined without a grid, we need to generate it
                    if not grid:
                        grid = Grid(name=name, params=entry, filename=filename)

                        # If the grid has an instance, add the correct args to it
                        if "self" in grid.args and "grid" in grid.args["self"]:
                            instance_grid = self.grids.get(
                                grid.args["self"]["grid"], [{}]
                            )

                    # If the grid is cached, we already have parameter sets
                    argsets = grid
                    if grid.cache:
                        argsets = grid.argsets

                    # iterate over argsets for a grid, get overlapping args
                    for extra_args in instance_grid:
                        for argset in argsets:
                            updated = deepcopy(grid.params)

                            # Add instance args, if needed
                            updated["args"] = argset
                            if extra_args:
                                updated["args"]["self"] = extra_args

                            tests["%s.%s" % (name, idx)] = GridTest(
                                module=parent,
                                name=name,
                                params=updated,
                                verbose=verbose,
                                cleanup=cleanup,
                                filename=filename,
                                show_progress=self.show_progress,
                            )
                            print(f"generating test {idx}", end="\r")
                            idx += 1
        return tests

    def __repr__(self):
        return "[gridtest|%s]" % self.name

    def __str__(self):
        return "[gridtest|%s]" % self.name
