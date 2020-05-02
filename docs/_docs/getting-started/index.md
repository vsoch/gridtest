---
title: Introduction
category: Getting Started
permalink: /getting-started/index.html
order: 1
---

You should first [install]({{ site.baseurl }}/install/) gridtest.
This will place the executable `gridtest` in your bin folder, which is the client
for generating and running tests. 

## Getting Started

 - [How does it work?](#how-does-it-work): How does gridtest work?
 - [Concepts](#concepts): What are common gridtest concepts?
 - [Debugging](#debugging): is easy with the interactive interpreter.
 - [Templates](templates/): for test yaml files, including function and argument substitution
 - [Testing](testing/): via continuous integration, or checking if tests need updating.
 - [Python](python/): interacting with a GridRunner from within Python
 - [Environment](environment/): variables to change defaults for gridtest behavior
 - [Grid](grid/): Adding a grid of environment and other parameters to run grid tests
 - [Optimize](optimize/): some set of parameters for your report

<a id="#how-does-it-work">
### How does it work?

GridTest takes advantage of the <a href="https://docs.python.org/3/library/inspect.html">inspect
module</a> in Python so that you can provide any Python file, local, or system installed module
and extract not only a list of functions and classes, but also arguments. By way of providing
a file, module name, or folder path, GridTest can first generate for you a "test template," 
which comes down to a yaml file that you can easily fill in and customize for your tests.
For example, I might generate a test yaml file for my script like this:

```bash
$ gridtest generate script.py gridtest.yml
```

And you would then open the file and customize the default template to your liking.
The testing file can then be run, in the same way, using gridtest:

```bash
$ gridtest test gridtest.yml
```

Or since gridtest.yml is the default, just leave it out to find the file in
the present working directory:

```bash
$ gridtest test
```

The tests are run in parallel with multiprocessing to be efficient, but if you want
you can specify running in serial:

```bash
$ gridtest test --serial
```

Along with testing the conditions that you specify in the testing file, GridTest will also run type checking
if you have defined types in your code. You can also check if you need to add
more tests:

```bash
# exit code is 0 if all tests written, 1 otherwise
$ gridtest check gridtest.yml

No new tests to add!✨ 🥑️ ✨
```

And if there are new tests (meaning new functions or classes in the file that aren't
tested) you can update your testing file with those missing:

```bash
$ gridtest update gridtest.yml
```

**below not implemented yet**

And once your tests are written, you might add a new component (what the library
is named for) - a grid of environment and other parameters to run the tests with:

```bash
$ gridtest update --grid gridtest.yml
```

And finally, some set of optimizations to assess each grid test in:


```bash
$ gridtest update --optimize gridtest.yml
```

The rest of this getting started guide will review overall functionality. 
You should look at [tutorials]({{ site.baseurl }}/tutorials/) 
if you have never done this before, and would like to
walk through basic examples.

<a id="#concepts">
### What are gridtest concepts

A gridtest is a yaml file that is executed using the software described here,
GridTest. It's called a GridTest because of the GridTest "matrix" type, which
makes it easy to run a grid of tests. GridTest's main convention is that 
it will look for a yaml file, `gridtest.yml` to run tests by default. This means
that if you write your testing file in the root of a repository with Python
software like:

```
setup.py
requirements.txt
gridtest.yml
mymodule/
  subfolder/
  __init__.py
```

You can easily run `gridtest test` in the root of that folder to discover the
file. This is similar to a Dockerfile, or Singularity recipe file.

<a id="#debugging">
### Debugging

For most testing frameworks, when you hit an error there is a flash of red across the
screen, and at best you can stop execution on the first error (e.g., with pytest you would
add the -x flag) or add print statements to the test to see what might be going on. 
You might start an interactive shell to import modules and functions needed to debug,
and then need to exit and run again to re-run the test. Instead of these approaches,
gridtest gives you an ability to run a test with `--interactive`, meaning that you
can open an interactive shell at the onset of each test.

```python
$ gridtest test examples/basic/script-tests.yml --interactive
[script.add:1/6] |=====|-----------------------------|  16.7% 

Gridtest interactive mode! Press Control+D to cycle to next test.

Variables
   func: <function add at 0x7fe4c0a44200>
 module: <module 'script' from '/home/vanessa/Desktop/Code/gridtest/examples/basic/script.py'>
   args: {'one': 1, 'two': 2}
returns: 3

How to test
passed, error = test_types(func, args, returns)
result = func(**args)

Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:                                                                     
```

In the example above, we show that the function, module, and arguments for
the test are loaded, and you are shown how to run the tests. By way of having
the interactive terminal, you can of course interact with functions and variables
directly, and debug what might be the issue for a test. In the case of a file
with multiple tests (the typical case) You can also specify the name of the test you want
to interact with:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add
```

For the above, this would interact with all tests that start with script.add. If you
want to limit to the script.add module, you might want to do:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add.
```

Or a specific indexed text for the module:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add.0
```

For a more detailed debugging example, see the [debugging]({{ site.baseurl }}/getting-started/debugging/)
documentation.

## Licenses

This code is licensed under the Mozilla, version 2.0 or later [LICENSE](LICENSE).

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
