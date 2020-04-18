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

    # Generate the testing file
    generate_tests(args.input, output=args.output)
