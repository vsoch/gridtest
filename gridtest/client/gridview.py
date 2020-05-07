"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner, GridTest
import os
import json
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

    # If no name specified, print all grids
    if args.input:
        name = args.input[0]
        if name in grids:
            content = grids[name]
        else:
            sys.exit(f"{name} is not a valid grid name in {input_file}")
    else:
        content = grids

    if args.count:
        print(f"{len(content)} lists produced.")
    elif args.list:
        print("\n".join(grids.keys()))
    else:
        if args.compact:
            print(content)
        else:
            print(json.dumps(content, indent=4))
