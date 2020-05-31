"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner
from gridtest.utils import write_json
import os
import sys


def main(args, extra):

    # Default file for grids is grids.yml
    if not args.input:
        args.input = ["grids.yml"]
    input_file = args.input.pop(0)

    if not os.path.exists(input_file):
        sys.exit(f"{input_file} does not exist.")

    runner = GridRunner(input_file)
    grids = runner.get_grids()

    # If no name specified, print grid listing
    if args.input:
        name = args.input[0]
        if name in grids:
            grid = grids[name]
        else:
            sys.exit(f"{name} is not a valid grid name in {input_file}")

        if args.arg and args.arg not in grid.args:
            sys.exit(f"{args.arg} is not an argument in grid {grid}.")

        # Print count (length) of a variable, or number o grids
        if args.count and args.arg:
            try:
                print(f"Variable {args.arg} has length {len(grid.args[args.arg])}.")
            except:
                print(f"{grid.args[args.arg]}")

        # Just count of global
        elif args.count:
            print(f"{len(list(grid))} argument sets produced.")

        # Just print the argument
        elif args.arg:
            print(grid.args[args.arg])

        # Export data to file
        elif args.export:
            grids = list(grid)
            write_json(grids, args.export)
        else:
            for argset in grid:
                print(argset)
    else:
        print("\n".join(list(grids.keys())))
