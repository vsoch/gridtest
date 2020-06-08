---
title: Installation
category: Installation
permalink: /install/index.html
order: 1
---

<a id="install">
## Install

GridTest can be installed natively (python 3 recommended) with pip:

```bash
pip install gridtest
```

or via conda-forge:

```bash
conda install --channel conda-forge gridtest
```

or you can clone and install from source:

```bash
$ git clone https://github.com/vsoch/gridtest
$ cd gridtest
$ python setup.py install
```

or

```bash
$ pip install -e .
```

When you have installed GridTest, there will be an executable "gridtest"
placed in your bin folder:

```bash
which gridtest
/home/vanessa/anaconda3/bin/gridtest
```

and you should be able to run the executable and see the usage:

```bash
$ gridtest

GridTest Python v0.0.0
usage: gridtest [-h] [--version] {version,test,generate} ...

Python Grid Testing

optional arguments:
  -h, --help            show this help message and exit
  --version             suppress additional output.

actions:
  actions for gridtest

  {version,test,generate}
                        gridtest actions
    version             show software version
    test                run a grid test.
    generate            generate a grid test yaml file.
```

<a id="running-tests">
## Running Tests

Once you've installed gridtest, you can run the test suite with pytest, and
install a dependency for testing, the pokemon library:

```bash
pip install pokemon
pytest -sv tests/*py
```

The test suite is also run during continuous integration for GitHub actions,
and will run on pull requests if you don't want to run these commands locally.


If you have any questions or issues, please [open an issue]({{ site.repo }}/issues).
