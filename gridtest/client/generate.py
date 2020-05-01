"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import sys
import os

from gridtest.main.generate import generate_tests


def main(args, extra):

    if not args.input:
        sys.exit("Please provide an input file, folder, or module to parse.")

    # The output file is optional, input file is not
    outputfile = None
    input_file = args.input.pop(0)
    if args.input:
        outputfile = args.input.pop(0)

    # Generate the testing file
    generate_tests(
        input_file,
        output=outputfile,
        include_private=args.include_private,
        include_classes=not args.skip_classes,
        force=args.force,
    )
