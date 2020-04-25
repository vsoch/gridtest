"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

gridtest.func are short functions that serve as helpers for a gridtest.
Any function in here can be referenced as {% func_name %} or with arguments
{% func_name arg1=1 arg2=2 %}. If you possibly have a namespace
conflict, you can also reference {% gridtest.func.func_name %} and
it will work to reference the function here.

"""

import tempfile
import sys
import os


def tmp_path(requested_tmpdir=None, prefix="", create=False, ext=""):
    """get a temporary file with an optional prefix. By default will be
       created in /tmp, and the file is closed (and just a name returned).

       Arguments:
         - requested_tmpdir (str) : an optional requested temporary directory
         - prefix (str) : prefix the filename with this string.
         - create (bool) : create the file (empty) defaults to False
         - ext (str) : the extension to use, should include .
    """
    tmpdir = requested_tmpdir or tempfile.gettempdir()
    prefix = prefix or "gridtest-file-"
    prefix = os.path.join(tmpdir, os.path.basename(prefix))

    # If an extension is provided but without a .
    if ext and not ext.startswith("."):
        ext = ".%s" % ext

    fd, tmp_file = tempfile.mkstemp(prefix=prefix, suffix=ext)
    os.close(fd)
    if not create:
        os.remove(tmp_file)
    return tmp_file


def tmp_dir(requested_tmpdir=None, prefix="", create=True):
    """get a temporary directory for an operation. Default creates it.

       Arguments:
         - prefix (str) : prefix the filename with this string.
         - requested_tmpdir (str) : an optional requested temporary directory
         - create (bool) : create the temporary directory
    """
    tmpdir = requested_tmpdir or tempfile.gettempdir()
    prefix = prefix or "gridtest-dir"
    prefix = "%s.%s" % (prefix, next(tempfile._get_candidate_names()))
    tmpdir = os.path.join(tmpdir, prefix)

    if not os.path.exists(tmpdir) and create:
        os.mkdir(tmpdir)

    return tmpdir
