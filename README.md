# GridTest

[![PyPI version](https://badge.fury.io/py/gridtest.svg)](https://badge.fury.io/py/gridtest)

Simple grid testing setup for Python functions and modules.

![docs/assets/img/logo/gridtest.gif](docs/assets/img/logo/gridtest.gif)

## Overview 

GridTest is a small python library that will read in one or more python
scripts or modules, and generate a testing file that can be used to run grid
tests. A "gridtest" is one that is run over a grid of environment or parameter
settings that can optionally be optimized for something. For example, you can
run a single function across a grid of its own arguments, and then measure
the time that each one takes, and report the results in a grid for inspection.
Take a look at the [examples](examples) folder or the 
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

## Known Issues 

The following are known to not work, and development will depend on how useful
the average user will assess each of these points. The developer @vsoch has not
added them yet because she doesn't think them overall useful.

 - support for system libraries (e.g., sys) or anything without a filename in site-packages

## TODO

 - develop gridtest matrix input and documentation (need to add ranges for variables)
 - create results report for benchmarks
 - custom decorator with example
