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
    return_code = runner.run(
        nproc=args.nproc,
        parallel=not args.serial,
        verbose=args.verbose,
        regexp=args.pattern,
        name=args.name,
        interactive=args.interactive,
        cleanup=not args.no_cleanup,
        save=args.save,
        save_compact=args.save_compact,
        save_report=args.save_report,
        report_template=args.report_template,
    )
    sys.exit(return_code)
