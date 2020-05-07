"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

from gridtest.main.test import GridRunner
from gridtest.main.generate import extract_functions, extract_modulename
import os
import re
import sys


def get_missing_tests(
    testfile, include_private=False, skip_patterns=None, include_classes=True
):
    """Given a testing file, load in as a GridRunner, load the module again,
       and check if new tests need to be generated. Optionally take patterns
       to skip. If no new tests are added, we return 0. Otherwise, we exit with
       1. This is similar to black linting, and is intended for running in CI
       to pass if a user has written all tests to correpond with their module
       (akin to a more rigorous coverage tool).

       Arguments:
          - testfile (str) : the yaml test file
          - include_private (bool) : include "private" functions
          - skip_patterns (list) : list of test keys (patterns) to exclude
    """
    if not os.path.exists(testfile):
        sys.exit(f"{testfile} does not exist.")

    if not re.search("[.](yml|yaml)$", testfile):
        sys.exit("Test file must have yml|yaml extension.")

    skip_patterns = skip_patterns or []
    runner = GridRunner(testfile)

    # The config holds the filename we derive tests from, and tests
    files = []
    existing = set()

    for name, section in runner.config.items():
        # Get either the file path, module name, or relative path
        filename = extract_modulename(
            section.get("filename"), os.path.dirname(testfile)
        )
        files.append(filename)
        [existing.add(x) for x in section.get("tests", {}).keys()]

    # Keep track of new sections seen
    sections = []
    spec = dict()

    # Regular expression for existing takes into account different import paths
    regex = "(%s)$" % "|".join(list(existing) + skip_patterns)

    # Import each file as a module, or a module name, exit on error
    for filename in files:
        functions = extract_functions(
            filename,
            include_private=include_private,
            quiet=True,
            include_classes=include_classes,
        )
        sections += [
            k
            for k, v in functions.get("tests", {}).items()
            if k not in existing and not re.search(regex, k)
        ]
    return sections


def check_tests(
    testfile, include_private=False, include_classes=True, skip_patterns=None
):
    """A wrapper to get_missing_tests, but we return 0 if no new tests are
       to be added, and 1 otherwise.

       Arguments:
          - testfile (str) : the yaml test file
          - include_private (bool) : include "private" functions
          - include_classes (bool) : include classes
          - skip_patterns (list) : list of test keys (patterns) to exclude
    """
    sections = get_missing_tests(
        testfile, include_private, skip_patterns, include_classes
    )

    # If no new sections added, exit with 0
    if sections:
        print("\nNew sections to add:\n%s" % "\n".join(sections))
        sys.exit(1)
    print("\nNo new tests to add!✨ 🥑️ ✨")
    sys.exit(0)
