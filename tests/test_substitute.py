#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import pytest
import tempfile


def test_substitute_args():
    """Test that argument substitution works
    """
    from gridtest.main.substitute import substitute_args

    # A missing argument is valid, but returns replaced with nothing.
    assert substitute_args("{{ name }}") == ""
    assert substitute_args("echo hello {{ name }}") == "echo hello "

    # A substitution with a matching parameter returns it
    assert substitute_args("{{ name }}", {"name": "vanessa"}) == "vanessa"
    assert (
        substitute_args("echo hello {{ name }}", {"name": "vanessa"})
        == "echo hello vanessa"
    )


def test_substitute_func(tmp_path):
    """Run a test that checks gridtest provided substitution functions"""
    from gridtest.main.substitute import substitute_func

    tmpdir = os.path.join(str(tmp_path))

    # Known gridtest functions in func: get a temporary path
    assert substitute_func("{% tmp_path %}").startswith(tempfile.gettempdir())
    assert "pancakes" in substitute_func("{% tmp_path prefix=pancakes %}")
    assert tmpdir in substitute_func("{% tmp_path requested_tmpdir=" + tmpdir + "%}")

    # request a temporary directory
    assert os.path.exists(substitute_func("{% tmp_dir %}"))
    assert not os.path.exists(substitute_func("{% tmp_dir create=False %}"))
    assert tmpdir in substitute_func(
        "{% tmp_dir requested_tmpdir=" + tmpdir + " create=False%}"
    )


def test_substitute_func_custom(tmp_path):
    """Test that any module (and function) substitution works"""
    from gridtest.main.substitute import substitute_func

    # TODO: need some actual use cases for this
    pass
