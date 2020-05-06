---
title: Installation
category: Installation
permalink: /install/index.html
order: 1
---


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

If you have any questions or issues, please [open an issue]({{ site.repo }}/issues).
