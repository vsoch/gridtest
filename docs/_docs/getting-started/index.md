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

### Introduction

 - [How does it work?](#how-does-it-work): How does gridtest work?
 - [Concepts](#concepts): What are common gridtest concepts?

### Writing Tests

 - [Templates](templates/): for test yaml files, including function and argument substitution
 - [Grids](grids/): can be used to programatically generate inputs for tests, or outside of testing when you want to parameterize some values, optionally over a function.
 - [Metrics](metrics/): decorators to measure metrics across a grid of tests.

### Running Tests

 - [Environment](environment/): variables to change defaults for gridtest behavior
 - [Debugging](#debugging): is easy with the interactive interpreter.
 - [Testing](testing/): via continuous integration, or checking if tests need updating.
 - [Python](python/): interacting with a GridRunner from within Python
 - [Results](results/) are available via a json export or interactive web report.

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

If you don't care about testing, you can use GridTest to generate a yaml specification
of parameterizations. Let's say we have a set of grids defined in grids.yml.
We can list the named grids that are defined in the file:

```bash
$ gridtest gridview grids.yml --list
generate_empty
generate_matrix
generate_lists_matrix
generate_by_min_max
generate_by_min_max_twovars
```

And then either print them all to the screen:

```bash
$ gridtest gridview grids.yml
```

or just print a specific grid we found with `--list`.

```bash
$ gridtest gridview grids.yml generate_by_min_max --compact
[{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]
```

For larger grids, it's nice to be able to get a count. The "twovars"
variant of the function above adds another variable (also with 5 values)
so we get 5x5:

```bash
$ $ gridtest gridview grids.yml generate_by_min_max_twovars --count
25 lists produced.
```

The rest of this getting started guide will review overall functionality. 
You should look at [tutorials]({{ site.baseurl }}/tutorials/) 
if you have never done this before, and would like to
walk through basic examples.

<a id="#concepts">
### What are gridtest concepts

#### GridTest

A gridtest is a yaml file that is executed using the software described here,
GridTest. It's called a GridTest because of the ability to define grids of tests.
For example, let's say that we want to measure the time it takes to run a function
over a set of variables. We do this by way of adding an optimization, which
comes down to a decorator function that will measure the value and return it to
gridtest. We then might specify a range of numbers for one or more function
variables. This will ultimately generate a grid of tests for the function,
each with a set of results from the function itself and decorators. 
GridTest also will make it easy to run over a grid of different environments,
although this is not developed yet.

#### gridtest.yml

GridTest's main convention is that  it will look for a yaml file, `gridtest.yml` to run tests by default. This means
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

#### grids

Gridtest does parameterization by way of grids, which is a section of the gridtest.yml
(alongside tests) that has definitions for one or more named grids. For example,
if we wanted to use a function (`script.get_pokemon_id`) to generate a list of
values for the argument `pid` for a test called `script.generate_pokemon`, we might
write a recipe like this. 

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  grids:
    generate_pids:
      func: script.get_pokemon_id
      count: 10

  tests:
    script.generate_pokemon:
        grid:
          pid: generate_pids
```

The reference to "generate_pids" for the argument "pid" is referenced under
grids, and we know to use the `scripts.get_pokemon_id`, run 10 times, to
generate it. We could also define arguments for the parameterization. For
a simple example, see the [grid-function](https://github.com/vsoch/gridtest/tree/master/examples/grid-function) 
example, or read more in the getting started [templates](https://vsoch.github.io/gridtest/getting-started/templates/index.html) guide.

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
the test are loaded, and you are shown how to run the tests. If you have added any
decorators (optimizations to measure) they will be applied already to the variable 
func. By way of having the interactive terminal, you can of course interact with functions and variables
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
