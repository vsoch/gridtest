"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner
from gridtest.main.generate import extract_modulename, extract_functions
import os
import re
import sys


def update_tests(
    testfile, include_private=False, skip_patterns=None, include_classes=True
):
    """Given a testing file, load in as a GridRunner, load the module again,
       and update with new tests not found. Optionally take patterns
       to skip. This is akin to check_tests in check.py, but instead we
       update the runner and save the file.

       Arguments:
          - testfile (str) : the yaml test file
          - include_private (bool) : include "private" functions
          - skip_patterns (list) : list of test keys (patterns) to exclude
          - include_classes (bool) : include classes in update (True)
    """
    if not os.path.exists(testfile):
        sys.exit(f"{testfile} does not exist.")

    if not re.search("[.](yml|yaml)$", testfile):
        sys.exit("Test file must have yml|yaml extension.")

    skip_patterns = skip_patterns or []
    runner = GridRunner(testfile)

    # The config holds the filename we derive tests from, and tests, keep a lookup
    files = []
    existing = set()

    for name, section in runner.config.items():
        # Get either the file path, module name, or relative path
        filename = extract_modulename(
            section.get("filename"), os.path.dirname(testfile)
        )
        files.append(filename)
        [existing.add(x) for x in section.get("tests", {}).keys()]
        functions = extract_functions(
            filename, include_private, quiet=True, include_classes=include_classes
        )

        # Regular expression for existing takes into account different import paths
        regex = "(%s)$" % "|".join(list(existing) + skip_patterns)
        for key, params in functions.items():

            # Make sure functions start with same name as previous level
            if name in key:
                key = name + ".".join([x for x in key.split(name)[1:] if x != "."])

            if not re.search(regex, key):
                print(f"Adding function {key}")
                runner.config[name][key] = params

    # Save back to file
    runner.save(testfile)
    return runner
