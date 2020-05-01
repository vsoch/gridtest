"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import sys
import os

from gridtest.main.update import update_tests


def main(args, extra):

    if not args.input:
        sys.exit("Please provide a yaml test file to update.")

    # Update the testing file
    update_tests(
        args.input,
        include_private=args.include_private,
        include_classes=not args.skip_classes,
    )
