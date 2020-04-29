---
title: Environment
category: Getting Started
permalink: /getting-started/environment/index.html
order: 5
---

Gridtest supports export of a few environment variables that can drive
testing or other functionality.

## Gridtest Workers

By default, the number of workers will be the number of processes (nproc) multiplied
by 2 plus 1. This isn't some hard defined standard, but what was found to work
relatively well. You can change this by exporting the variable `GRIDTEST_WORKERS`:


```bash
export GRIDTEST_WORKERS=2
```

Note that workers are only relevant for tests run with multiprocessing (the default)
so if you add the `--serial` flag, or if you are using `--interactive` mode (which
also requires running in serial) this variable will not be relevant.

## GridTest Shell

If you use the `gridtest shell` mode to interactively create a gridtest running
in Python, it will default to looking for an ipython installation, and then check
for standard python, and then bpython. If you want to change the default,
just export the string for the python that you want:

```bash
# one of ipython, python, or bpython
export GRIDTEST_SHELL=ipython
```

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
