"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner
import json
import sys
import re


def main(args, extra):

    runner = GridRunner(args.filename)
    runner.run(nproc=args.cores, parallel=False)
