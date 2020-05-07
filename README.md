# GridTest

[![PyPI version](https://badge.fury.io/py/gridtest.svg)](https://badge.fury.io/py/gridtest)

Simple grid testing setup for Python functions and modules.

![docs/assets/img/logo/gridtest.gif](docs/assets/img/logo/gridtest.gif)

## Overview 

GridTest is a small python library that will read in one or more python
scripts or modules, and generate a testing file that can be used to run grid
tests. A "gridtest" is one that is run over a grid of parameter
settings. For each gridtest, you can also measure one or more metrics (Python 
decorators). For example:

 - you might run a function across a grid of arguments, and then measure the time that each combination takes (the metric), and generate a report for inspection.
 - you might be doing text processing and having functions to parse text. Each function might be run over a grid of sentences and counts, and for each result, we want to count the number of unique words, and total words (metrics). This is the [interface example](examples/interface).

Take a look at the [examples](examples) folder or the [documentation](https://vsoch.github.io/gridtest) for getting started. An example report is available to view [here](https://vsoch.github.io/gridtest/templates/report/),
and as we get more real world use cases, the report templates and data export options will be expanded
to use and visualize them beautifully. Please [open an issue](https://github.com/vsoch/gridtest/issues) 
if you have a use case that @vsoch can help with!

## Who is this software for?

Gridtest is intended for quick generation of running tests. It is not intended
to be a robust testing library like pytest or even unittest, but rather a quick
way to write tests for an entire module or set of files, and then have them
run on some CI service. My specific use case is that I wanted a way to quickly
generate tests for the libraries that I "did not have time to write tests for."
This is, at it's core, for the lazy person without a lot of time that at least
wants something. I considered calling it crappytest, but the name was too long :)

 * Free software: MPL 2.0 License

## Known Issues 

The following are known to not work, and development will depend on how useful
the average user will assess each of these points. The developer @vsoch has not
added them yet because she doesn't think them overall useful.

 - support for system libraries (e.g., sys) or anything without a filename in site-packages


## TODO:
 - write tests for grid parsing cases.
 - split grids.py to separate grid generation
 - make tests and examples / docs for grids
 - should func and count be allowed in test grids?
