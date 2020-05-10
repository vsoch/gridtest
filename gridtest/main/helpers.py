"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.generate import import_module, get_function_typing
from gridtest.main.grids import intersect_args
from io import StringIO
import re
import sys
import time
import os


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


def print_interactive(**kwargs):
    """A helper function to print locals that are relevant to test_basic for 
       the user.
    """
    print(f"\n\nGridtest interactive mode! Press Control+D to cycle to next test.")
    print("\n\033[1mVariables\033[0m")
    print(f"   func: {kwargs['func']}")
    print(f" module: {kwargs['module']}")
    print(f"   args: {kwargs['args']}")
    print(f"returns: {kwargs['returns']}")
    print("\n\033[1mHow to test\033[0m")
    print("passed, error = test_types(func, args, returns)")
    print("result = func(**args)\n")


def test_basic(
    funcname,
    module,
    filename,
    func=None,
    args=None,
    returns=None,
    interactive=False,
    metrics=None,
):
    """test basic is a worker version of the task.test_basic function.
       If a function is not provided, funcname, module, and filename are
       required to retrieve it. A function can only be provided directly
       if it is pickle serializable (multiprocessing would require this).
       It works equivalently but is not attached to a class, and returns
       a list of values for [passed, result, out, err, raises]

       Arguments:
         - funcname (str) : the name of the function to import
         - module (str) : the base module to get the function from
         - func (Function) : if running serial, function can be directly provided
         - args (dict) : dictionary of arguments
         - returns (type) : a returns type to test for
         - interactive (bool) : run in interactive mode (giving user shell)
         - metrics (list) : one or more metrics (decorators) to run.
    """
    metrics = metrics or []

    if not func:
        sys.path.insert(0, os.path.dirname(filename))
        func = get_function(
            module=module, funcname=funcname, args=args, filename=filename
        )

    # Figure out how to apply multiple
    originalfunc = func
    passed = False
    result = None
    raises = None
    out = []
    err = []

    # import the decorators here (currently only support decorators from gridtest
    for metric in metrics:
        if not metric.startswith("@"):
            continue
        metric = re.sub("^[@]", "", metric)
        try:
            gt = import_module("gridtest.decorators")
            decorator = getattr(gt, metric)

            # Update func to include wrapper
            func = decorator(func)

        # Fallback to support for custom modules
        except:
            try:
                metric_module = metric.split(".")[0]
                mm = import_module(metric_module)
                for piece in metric.split(".")[1:]:
                    decorator = getattr(mm, piece)

                # Update func to include wrapper
                func = decorator(func)
            except:
                out.append(f"Warning, unable to import decorator @{metric}")

    # Interactive mode means giving the user console control
    if interactive:
        print_interactive(**locals())
        try:
            import IPython

            IPython.embed()
        except:
            import code

            code.interact(local=locals())

    if not func:
        err = [f"Cannot find function {funcname}"]

    else:
        # Subset arguments down to those allowed
        args = intersect_args(originalfunc, args)
        passed, error = test_types(originalfunc, args, returns)
        err += error

        # if type doesn't pass, TypeError, otherwise continue
        if not passed:
            raises = "TypeError"

        else:

            # Run and capture output and error
            try:
                with Capturing() as output:
                    result = func(**args)
                if output:
                    std = output.pop(0)
                    out += std.get("out")
                    err += std.get("err")
                passed = True
            except Exception as e:
                raises = type(e).__name__
                message = str(e)
                if message:
                    err.append(message)

    return [passed, result, out, err, raises]


def get_function(module, funcname, args, filename):
    """given a module name, function name, argument, and filename, derive
       a function, optionally deriving an instance first that it might
       belong to
    """
    sys.path.insert(0, os.path.dirname(filename))
    module = import_module(module)

    if "self" in args:

        # If args provided for instance
        instance = getattr(module, funcname.split(".")[0])
        instanceargs = {}
        if "self" in args:
            instanceargs = intersect_args(instance, args["self"])
        instance = instance(**instanceargs)

        for piece in funcname.split(".")[1:]:
            func = getattr(instance, piece)
            instance = func

        # func = getattr(instance, funcname.split(".")[-1])
        del args["self"]
    else:
        for piece in funcname.split("."):
            func = getattr(module, piece)
            module = func
    return func


def test_types(func, args=None, returns=None):
    """Given a loaded function, get it's types and ensure that they are
       correct. Returns a boolean to indicate correct/ passing (True)
    """
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
