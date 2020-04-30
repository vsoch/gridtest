# GridTest

[![PyPI version](https://badge.fury.io/py/gridtest.svg)](https://badge.fury.io/py/gridtest)

Simple grid testing setup for Python functions and modules.

![docs/assets/img/logo/gridtest.gif](docs/assets/img/logo/gridtest.gif)

## Overview 

GridTest is a small python library that will read in one or more python
scripts or modules, and generate a testing file that can be used to run grid
tests. Take a look at the [examples](examples) folder or the 
[documentation](https://vsoch.github.io/gridtest) for getting started.

## Who is this software for?

Gridtest is intended for quick generation of running tests. It is not intended
to be a robust testing library like pytest or even unittest, but rather a quick
way to write tests for an entire module or set of files, and then have them
run on some CI service. My specific use case is that I wanted a way to quickly
generate tests for the libraries that I "did not have time to write tests for."
This is, at it's core, for the lazy person without a lot of time that at least
wants something. I considered calling it crappytest, but the name was too long :)

**under development**

 * Free software: MPL 2.0 License

## TODO

 - develop gridtest matrix input and documentation
 - add class inspection
 - Add ability to inspect an attribute for a result
 - gridtest test should (by default) look for a gridtest.yml file.
 - Then finish requests use case
