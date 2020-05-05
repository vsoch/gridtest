"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import shutil
import os

here = os.path.abspath(os.path.dirname(__file__))


def get_template(name):
    """Given the name of a template (an entire folder in the directory here)
       Return the full path to the folder, with the intention to copy it somewhere.
    """
    template = os.path.join(here, name)
    if os.path.exists(template):
        return template


def copy_template(name, dest):
    """Given a template name and a destination directory, copy the template
       to the desination directory.
    """
    template = get_template(name)
    dest_dir = os.path.dirname(dest)
    if template and os.path.exists(dest_dir):
        shutil.copytree(template, dest)
        return dest
