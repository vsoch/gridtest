# GridTest

[![PyPI version](https://badge.fury.io/py/gridtest.svg)](https://badge.fury.io/py/gridtest)
[![DOI](https://zenodo.org/badge/256346804.svg)](https://zenodo.org/badge/latestdoi/256346804)

Simple grid parameterization and testing setup for Python functions and modules.
See [Documentation](https://vsoch.github.io/gridtest/) to get started.

![docs/assets/img/logo/gridtest.gif](https://raw.githubusercontent.com/vsoch/gridtest/master/docs/assets/img/logo/gridtest.gif)

## Overview 

GridTest is a library that specializes in generating [parameter grids](https://vsoch.github.io/gridtest/#parameterization). The grids are most obviously used for testing, but can extend to other use cases.
In the context of testing, GridTest makes it easy to discover functions,
classes, and arguments for your python scripts or modules, and then generate
a template for you to easily populate. Outside of testing, you can define
grids that are version controlled, programatically defined with functions,
and easy to interact with from the command line or Python interpreter.
You might be interested in GridTest if you need:

   - low overhead tests for Python scripts and small packages
   - to generate input data for reproducible computations

To learn more, it's recommended to reference the [documentation](https://vsoch.github.io/gridtest/),
take a look at the [getting started](https://vsoch.github.io/gridtest/getting-started/index.html) pages,
or browse one of the many [tutorials](https://vsoch.github.io/gridtest/tutorials/index.html) available.

 * Free software: MPL 2.0 License

## Support

If you have any questions or requests for examples or tutorials, please don't hesitate
to [open an issue](https://github.com/vsoch/gridtest/issues).

## Contributing

Please see the [documentation contributing guide](https://vsoch.github.io/gridtest/contributing/index.html)
for details on how to contribute to documentation or code, or the GitHub [CONTRIBUTING.md](.github/CONTRIBUTING.md) 
for a list of checks when opening a pull request.

## Known Issues 

The following are known to not work, and development will depend on how useful
the average user will assess each of these points. The developer @vsoch has not
added them yet because she doesn't think them overall useful.

 - support for system libraries (e.g., sys) or anything without a filename in site-packages
