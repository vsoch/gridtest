#!/usr/bin/env python
"""

Copyright (C) 2020 Vanessa Sochat.

This Source Code Form is subject to the terms of the
Mozilla Public License, v. 2.0. If a copy of the MPL was not distributed
with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

"""

import os
import pytest

here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def runner():
    from gridtest.main.test import GridRunner

    test_file = os.path.join(here, "modules", "basic-tests.yml")
    return GridRunner(test_file)


def test_gridrunner(runner):
    """Load a gridtest runner and test for a basic file.
    """
    assert "basic" in runner.config
    assert len(runner.config["basic"]) >= 6
    assert runner.run() == 0
    assert runner.run(parallel=False) == 0


def test_returns(runner):
    """Run a test that checks for a return value"""
    tests = runner.get_tests()
    returns_test = tests["basic.add.0"]

    # Test is not successful before run, no result
    assert not returns_test.result
    assert not returns_test.success
    assert "returns" in returns_test.params
    returns_test.run()

    # Result is present, matches returns
    assert returns_test.result == returns_test.params["returns"]
    assert returns_test.success

    # Change result, run again (should fail)
    returns_test.params["returns"] = 2
    returns_test.run()
    assert returns_test.result != returns_test.params["returns"]
    assert not returns_test.success


def test_runs(runner):
    """Run a test that does not checks (other than working)"""
    tests = runner.get_tests()
    returns_test = tests["basic.add.1"]

    # Test is not successful before run, no result
    assert not returns_test.result
    assert not returns_test.success
    returns_test.run()
    assert returns_test.success


def test_broken_func():
    """Run a test for a broken function"""
    from gridtest.main.test import GridTestFunc

    def broken():
        print(1 + "string")

    test = GridTestFunc(broken)
    assert not test.success
    test.run()
    assert not test.success
    assert test.raises == "TypeError"
    assert len(test.err) == 1


def test_broken_func():
    """Run a test for a broken function"""
    from gridtest.main.test import GridTestFunc

    def broken():
        print(1 + "string")

    test = GridTestFunc(broken)
    assert not test.success
    test.run()
    assert not test.success
    assert len(test.err) == 1


def test_return_type():
    """test that a function with typing honors returning that type
    """
    from gridtest.main.test import GridTestFunc

    def return_int(one: int, two: int) -> int:
        return one + two

    test = GridTestFunc(return_int, params={"args": {"one": 1, "two": 2}})
    assert not test.success
    test.run()
    assert test.success
    assert test.result == 3

    # Now add the wrong type
    test = GridTestFunc(return_int, params={"args": {"one": 1, "two": "two"}})
    assert not test.success
    test.run()
    assert not test.success
    assert test.raises == "TypeError"


def test_raises():
    """test that a function that should raise an error raises is
    """
    from gridtest.main.test import GridTestFunc

    def raises_error():
        raise Exception

    test = GridTestFunc(raises_error)
    assert not test.success
    assert not test.raises

    # After run, it should fail and have the error output
    test.run()
    assert not test.success
    assert test.raises == "Exception"
    assert len(test.err) == 1

    # Now it will expect to raise the error, should be success
    test = GridTestFunc(raises_error, params={"raises": "Exception"})
    assert not test.success
    assert not test.raises

    # After run, it should fail and have the error output
    test.run()
    assert test.success
    assert test.raises == "Exception"
    assert len(test.err) == 0
    assert len(test.out) == 1
