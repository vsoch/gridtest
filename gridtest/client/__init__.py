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

    test.add_argument("filename", help="gridtest file to run tests for", type=str)

    test.add_argument(
        "--cores", help="number of cores for multiprocessing to use", type=int
    )

    # Run a grid test
    generate = subparsers.add_parser("generate", help="generate a grid test yaml file.")

    generate.add_argument(
        "input",
        help="name of input file, folder, or module to write tests for",
        type=str,
    )

    generate.add_argument(
        "output", help="name of output file to write grid test (.yml|.yaml)", type=str
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

    # Pass on to the correct parser
    return_code = 0
    try:
        main(args=args, extra=extra)
        sys.exit(return_code)
    except UnboundLocalError:
        return_code = 1

    help(return_code)


if __name__ == "__main__":
    main()
