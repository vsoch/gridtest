"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

__version__ = "0.0.14"
AUTHOR = "Vanessa Sochat"
AUTHOR_EMAIL = "vsochat@stanford.edu"
NAME = "gridtest"
PACKAGE_URL = "http://www.github.com/vsoch/gridtest"
KEYWORDS = "python,testing,grid,ci"
DESCRIPTION = "generate grid testing for Python modules and functions"
LICENSE = "LICENSE"

################################################################################
# Global requirements


INSTALL_REQUIRES = (
    ("pyaml", {"min_version": "20.3.1"}),
    ("json-tricks", {"min_version": "3.15.2"}),
)

TESTS_REQUIRES = (("pytest", {"min_version": "4.6.2"}),)
