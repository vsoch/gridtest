# GridTest

[![PyPI version](https://badge.fury.io/py/gridtest.svg)](https://badge.fury.io/py/gridtest)

Simple grid parameterization and testing setup for Python functions and modules.

![docs/assets/img/logo/gridtest.gif](https://raw.githubusercontent.com/vsoch/gridtest/master/docs/assets/img/logo/gridtest.gif)

## Overview 

GridTest is a library that specializes in generating parameter grids. The grids
are most obviously used for testing, but can extend to other use cases.
GridTest can read in one or more python scripts or modules, and generate a 
yaml template file that can be used to run tests, or just to define grids
to programatically use elsewhere. 

## Use Cases

### Testing

A **gridtest**: is one that is run over a grid of parameter settings. Each test
can include an inline grid to define arguments, and optionally functions to run
to generate arguments. A grid can be inline to the test (if not used elsewhere)
or defined globally and shared.

### Parameterization

GridTest makes parameter definitions first class citizens!
A **grid** is a global definition of a parameter matrix. You can define arguments,
and optionally functions to run to derive arguments. Grids do not have to be used in
testing! You might share a repository that only defines grids that people
can use across many different kinds of machine learning models, likely to run metrics.

### Metrics

A **metric** is a Pytho decorator that is paired with a test that will measure some
attribute of a test. For example:
   - you might run a function across a grid of arguments, and then measure the time that each combination takes (the metric), and generate a report for inspection.
   - you might be doing text processing and having functions to parse text. Each function might be run over a grid of sentences and counts, and for each result, we want to count the number of unique words, and total words (metrics). This is the [interface example](examples/interface).

Take a look at the [examples](examples) folder or the [documentation](https://vsoch.github.io/gridtest) for getting started. An example report is available to view [here](https://vsoch.github.io/gridtest/templates/report/),
and as we get more real world use cases, the report templates and data export options will be expanded
to use and visualize them beautifully. Please [open an issue](https://github.com/vsoch/gridtest/issues) 
if you have a use case that @vsoch can help with!

## Who is this software for?

Gridtest is intended for definition and saving of grids for any need that you might have,
or even for quick generation of running tests. It is not intended
to be a robust testing library like pytest or even unittest, but rather a quick
way to write tests for an entire module or set of files, and then have them
run on some CI service.

 * Free software: MPL 2.0 License

## Known Issues 

The following are known to not work, and development will depend on how useful
the average user will assess each of these points. The developer @vsoch has not
added them yet because she doesn't think them overall useful.

 - support for system libraries (e.g., sys) or anything without a filename in site-packages
