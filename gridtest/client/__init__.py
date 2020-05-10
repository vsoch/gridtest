#!/usr/bin/env python

"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import gridtest
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(description="Python Grid Testing")

    parser.add_argument(
        "--version",
        dest="version",
        help="suppress additional output.",
        default=False,
        action="store_true",
    )

    description = "actions for gridtest"
    subparsers = parser.add_subparsers(
        help="gridtest actions",
        title="actions",
        description=description,
        dest="command",
    )

    # print version and exit
    subparsers.add_parser("version", help="show software version")

    # Run a grid test
    test = subparsers.add_parser("test", help="run a grid test.")

    test.add_argument(
        "filename",
        help="gridtest file to run tests for",
        type=str,
        default="gridtest.yml",
        nargs="?",
    )

    test.add_argument(
        "--nproc",
        help="number of processes for running tests (defaults to 2*ncores + 1)",
        type=int,
    )

    test.add_argument(
        "-v",
        "--verbose",
        dest="verbose",
        help="also print output for success",
        default=False,
        action="store_true",
    )

    test.add_argument(
        "--serial",
        dest="serial",
        help="run tests in serial (instead of parallel), uses --nproc",
        default=False,
        action="store_true",
    )

    test.add_argument(
        "--save", dest="save", help="save a json export of test results.", default=None,
    )

    test.add_argument(
        "--compact",
        dest="save_compact",
        help="save compact json",
        default=False,
        action="store_true",
    )

    test.add_argument(
        "--save-web",
        dest="save_report",
        help="save a full web report to directory specified (cannot exist)",
        default=None,
    )

    test.add_argument(
        "--report-template",
        dest="report_template",
        help="report template to use",
        default="report",
        choices=["report"],
    )

    test.add_argument(
        "--no-cleanup",
        dest="no_cleanup",
        help="Do not clean up paths generated with tmp_path or tmp_dir",
        default=False,
        action="store_true",
    )

    test.add_argument(
        "-i",
        "--interactive",
        dest="interactive",
        help="interactively debug a test with code.interact or IPython.embed",
        default=False,
        action="store_true",
    )

    test.add_argument(
        "-n",
        "--name",
        dest="name",
        help="the name of the test to interactive with",
        default=None,
    )

    test.add_argument(
        "--pattern", help="match a pattern to filter testing", type=str, default=None,
    )

    # Shell into interactive environment to run tests
    shell = subparsers.add_parser(
        "shell", help="shell into an interactive console with gridtest"
    )
    shell.add_argument(
        "input",
        help="name of input file, folder, or module to write tests for",
        type=str,
        nargs="?",
        default=None,
    )

    # View a grid
    gridview = subparsers.add_parser(
        "gridview", help="view an entire set of grids, or a named grid"
    )
    gridview.add_argument(
        "input",
        help="name of grids.yml file (or equivalent) to view",
        type=str,
        nargs="*",
        default=None,
    )

    gridview.add_argument(
        "--count",
        "-n",
        dest="count",
        help="count the number of results that will be produced",
        default=False,
        action="store_true",
    )

    gridview.add_argument(
        "--export",
        dest="export",
        help="export a parameterized grid to json.",
        type=str,
        default=None,
    )

    # Check (lint) a gridtest
    check = subparsers.add_parser(
        "check", help="check a gridtest yaml file to ensure all tests written."
    )
    check.add_argument(
        "input", help="name of test yaml file to check.", type=str, nargs="?",
    )

    check.add_argument(
        "--skip-patterns",
        help="skip patterns for tests names",
        type=str,
        default=None,
        nargs="*",
        dest="skip_patterns",
    )

    # Generate a grid test
    generate = subparsers.add_parser("generate", help="generate a grid test yaml file.")

    generate.add_argument(
        "input",
        help="name of input file, folder, or module to write tests for",
        type=str,
        nargs="*",
    )

    generate.add_argument(
        "--force",
        dest="force",
        help="if the output yaml exists, force overwrite with new test templates",
        default=False,
        action="store_true",
    )

    # Update a grid test
    update = subparsers.add_parser(
        "update", help="update a gridtest file with new tests."
    )

    update.add_argument(
        "input",
        help="name of input file, folder, or module to write tests for",
        type=str,
    )

    # Both generate and check groups have --include-private
    for group in [generate, check, update]:
        group.add_argument(
            "--include-private",
            dest="include_private",
            help="suppress additional output.",
            default=False,
            action="store_true",
        )
        group.add_argument(
            "--skip-classes",
            dest="skip_classes",
            help="don't include classes (defaults to False)",
            default=False,
            action="store_true",
        )

    return parser


def main():
    """main entrypoint for gridtest
    """

    parser = get_parser()

    def help(return_code=0):
        """print help, including the software version and active client 
           and exit with return code.
        """

        version = gridtest.__version__

        print("\nGridTest Python v%s" % version)
        parser.print_help()
        sys.exit(return_code)

    # If the user didn't provide any arguments, show the full help
    if len(sys.argv) == 1:
        help()

    # If an error occurs while parsing the arguments, the interpreter will exit with value 2
    args, extra = parser.parse_known_args()

    # Show the version and exit
    if args.command == "version" or args.version:
        print(gridtest.__version__)
        sys.exit(0)

    # Does the user want a shell?
    if args.command == "test":
        from .test import main
    elif args.command == "generate":
        from .generate import main
    elif args.command == "gridview":
        from .gridview import main
    elif args.command == "shell":
        from .shell import main
    elif args.command == "check":
        from .check import main
    elif args.command == "update":
        from .update import main

    # Pass on to the correct parser
    return_code = 0
    # try:
    main(args=args, extra=extra)
    sys.exit(return_code)
    # except UnboundLocalError:
    #    return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
