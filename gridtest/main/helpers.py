"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.generate import import_module, get_function_typing
from io import StringIO
import sys
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


def test_basic(
    funcname, module, filename, func=None, args=None, returns=None,
):
    """test basic is a worker version of the task.test_basic function.
       If a function is not provided, funcname, module, and filename are
       required to retrieve it. A function can only be provided directly
       if it is pickle serializable (multiprocessing would require this).
       It works equivalently but is not attached to a class, and returns
       a list of values for [passed, result, out, err, raises]
    """
    if not func:
        sys.path.insert(0, os.path.dirname(filename))
        module = import_module(module)
        func = getattr(module, funcname)

    passed = False
    result = None
    raises = None
    out = []
    err = []

    if not func:
        err = [f"Cannot find function {gridtest_funcname}"]

    else:
        passed, error = test_types(func, args, returns)
        err += error

        # if type doesn't pass, TypeError, otherwise continue
        if not passed:
            raises = "TypeError"

        else:
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


# Substitution


def substitute_func(value):
    """Given a value, determine if it contains a function substitution,
       and if it's one an important function (e.g., one from gridtest.helpers)
       return the value with the function applied. 

       Arguments:
         - value (str) : the value to do the substitution for.

       Notes: 
         A function should be in the format: {% tempfile.mkdtemp %} 
         (global import) or a function in gridtest.func in the format 
         {% tmp_path %}. If arguments are supplied, they should be in 
         the format {% tmp_path arg1=1 arg2=2 %}
    """
    # Numbers cannot have replacement
    if not isinstance(value, str):
        return value

    # First do substitutions of variables
    for template in re.findall("{%.+%}", value):
        varname = re.sub("({%|%})", "", template)
        params = [x.strip() for x in varname.split(" ") if x]
        modulename = params.pop(0).split(".", 1)
        funcpath = modulename[1:]

        try:
            module = import_module(modulename[0])
        except:

            # The module is gridtest.func
            module = import_module("gridtest.func")
            funcpath = modulename[0]

        if not funcpath:
            sys.exit(f"A function name must be provided for {varname}")
        func = getattr(module, funcpath)

        # If function is found, get value
        if func:
            kwargs = {}
            params = {x.split("=")[0]: x.split("=")[1] for x in params}

            # Clean up parameters based on intuited types
            for paramname, paramvalue in params.items():
                if paramvalue == "None":
                    paramvalue = None

                # No quotes and all numeric, probably int
                elif re.search("^[0-9]+$", paramvalue):
                    paramvalue = int(paramvalue)

                # One decimal, all numbers, probably float
                elif re.search("^[0-9]+[.]([0-9]+)?$", paramvalue):
                    paramvalue = float(paramvalue)

                # Explicitly a string with quotes
                elif re.search('^(".+")$', paramvalue):
                    paramvalue = paramvalue.strip('"')
                elif re.search("^('.+')$", paramvalue):
                    paramvalue = paramvalue.strip("'")
                kwargs[paramname] = paramvalue

            new_value = func(**kwargs)
            value = re.sub(template, value, new_value)

    return value
