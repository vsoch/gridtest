"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner, GridTest
import os
import sys


def main(args, extra):

    lookup = {"ipython": ipython, "python": python, "bpython": bpython}
    shells = ["ipython", "python", "bpython"]

    from gridtest.defaults import GRIDTEST_SHELL as shell

    # If the user asked for a specific shell via environment
    shell = shell.lower()
    if shell in lookup:
        try:
            return lookup[shell](args)
        except ImportError:
            pass

    # Otherwise present order of liklihood to have on system
    for shell in shells:
        try:
            return lookup[shell](args)
        except ImportError:
            pass


def get_runner(args):
    """if the user provides a gridtest file to load, return a runner
    """
    runner = None
    if args.input is not None:
        if not os.path.exists(args.input):
            sys.exit(f"Input file {args.input} does not exist.")
        try:
            runner = GridRunner(args.input)
        except:
            sys.exit(
                "Error creating GridRunner, try running shell without test yaml file to debug."
            )
    return runner


def print_runner(runner, testfile):
    """If a runner is provided, print instructions for using it. Otherwise
       show instructions for adding a test file.
    """
    print("\n\033[1mGridtest Interactive Shell\033[0m")
    if testfile:
        print(f"testfile: {testfile}")
    if runner:
        print(f"  runner: {runner}")

    if not runner and testfile:
        print("runner = GridRunner({testfile})")
    elif not runner and not testfile:
        print("runner = GridRunner('tests.yml')")


def ipython(args):
    """give the user an ipython shell, optionally with an endpoint of choice.
    """
    from gridtest.main.test import GridRunner, GridTest

    testfile = args.input
    runner = get_runner(args)
    print_runner(runner, testfile)
    import IPython

    IPython.embed()


def bpython(args):
    from gridtest.main.test import GridRunner, GridTest
    import bpython

    runner = get_runner(args)
    print_runner(runner, args.input)
    bpython.embed(locals_={"runner": runner, "testfile": args.input})


def python(args):
    from gridtest.main.test import GridRunner, GridTest
    import code

    runner = get_runner(args)
    print_runner(runner, args.input)
    code.interact(local={"runner": runner, "testfile": args.input})
