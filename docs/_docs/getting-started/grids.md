---
title: Grids
category: Getting Started
permalink: /getting-started/grids/index.html
order: 6
---

GridTest isn't just for testing! In fact, you can write a file of grid
specifications that can be loaded and used for parameterization, or your own
custom functions. The description here will follow example the files in the
[grids](https://github.com/vsoch/gridtest/tree/master/examples/grids) examples folder.
Here is a peek at the top of this file, where we define two grids:

```yaml
mygrids:
  grids:

    # A grid that will generate 10 empty set of arguments
    generate_empty:
      count: 10

    # A grid that will generate each cross of x and y (total of 9)
    generate_matrix:
      grid:
        x: [1, 2, 3] 
        y: [1, 2, 3] 
```

This documentation will discuss how to interact with and customize your grids.

## Loading via a GridRunner

Let's say that we have a grids.yml file with grids defined. We can load with
gridtest easily via the GridRunner:

```python
from gridtest.main.test import GridRunner
runner = GridRunner('grids.yml')
# [gridtest|grids.yml]
```

We can easily generate the grids as follows:

```python
runner.get_grids()
{'generate_pids': ['645',
  '393',
  '511',
  '481',
  '142',
  '709',
  '344',
  '496',
  '820',
  '725'],
 'generate_empty': [{}, {}, {}, {}, {}, {}, {}, {}, {}, {}],
 'generate_matrix': [{'x': 1, 'y': 1},
  {'x': 1, 'y': 2},
  {'x': 1, 'y': 3},
  {'x': 2, 'y': 1},
  {'x': 2, 'y': 2},
  {'x': 2, 'y': 3},
  {'x': 3, 'y': 1},
  {'x': 3, 'y': 2},
  {'x': 3, 'y': 3}],
 'generate_lists_matrix': [{'x': [1, 2, 3], 'y': [1, 2, 3]},
  {'x': [1, 2, 3], 'y': [4, 5, 6]},
  {'x': [4, 5, 6], 'y': [1, 2, 3]},
  {'x': [4, 5, 6], 'y': [4, 5, 6]}],
 'generate_by_min_max': [{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}],
 'generate_by_min_max_twovars': [{'x': 0, 'y': 10},
  {'x': 0, 'y': 12},
  {'x': 0, 'y': 14},
  {'x': 0, 'y': 16},
  {'x': 0, 'y': 18},
  {'x': 2, 'y': 10},
  {'x': 2, 'y': 12},
  {'x': 2, 'y': 14},
  {'x': 2, 'y': 16},
  {'x': 2, 'y': 18},
  {'x': 4, 'y': 10},
  {'x': 4, 'y': 12},
  {'x': 4, 'y': 14},
  {'x': 4, 'y': 16},
  {'x': 4, 'y': 18},
  {'x': 6, 'y': 10},
  {'x': 6, 'y': 12},
  {'x': 6, 'y': 14},
  {'x': 6, 'y': 16},
  {'x': 6, 'y': 18},
  {'x': 8, 'y': 10},
  {'x': 8, 'y': 12},
  {'x': 8, 'y': 14},
  {'x': 8, 'y': 16},
  {'x': 8, 'y': 18}]}
```

<a id="viewing-on-the-command-line">
## Viewing on the Command Line

You can also preview the grids generated from the command line. Here is how
to list the names for the grids found in a file:

```bash
$ gridtest gridview grids.yml --list
generate_empty
generate_matrix
generate_lists_matrix
generate_by_min_max
generate_by_min_max_twovars
```

Here is how to print all grids:

```bash
gridtest gridview grids.yml
```

or a specific named grid that we found with `--list`:

```bash
$ gridtest gridview grids.yml generate_empty
[
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {},
    {}
]
```

You can also opt for a more compact view:

```bash
$ gridtest gridview grids.yml generate_empty --compact
[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
```

or even just count the number generated:

```bash
$ gridtest gridview grids.yml generate_empty --count
10 lists produced.
```

Each of the grids above will be explained below in more detail.

<a id="writing-grids">
## Writing Grids

Let's start with the most basic of grids, which are those that don't import any
special functions. 

<a id="header">
### Header

The header should have a named section for the grids that you want to define
(e.g. `mygrids`) and then a `grids` index, under which we will write each
of our named grids. Here is the start:

```
mygrids:
  grids:
  ...
```

Then each grid is added as a named section below that:

```
mygrids:
  grids:

    # A grid that will generate 10 empty set of arguments
    generate_empty:
      count: 10
```

The full content of this file will be written to the [grids.yml](grids.yml)
example here. Each example grid is discussed below. For each example,
you can preview the grid in the terminal with `gridtest gridview` or
obtain the grid by instantiating the `GridRunner` as shown above.

<a id="empty">
### Empty

It could be that you need to generate empty lists of arguments for a function,
in which case the `count` variable will be useful to you. Here is
how to specify a grid that will generate 10 empty set of arguments

```yaml
generate_empty:
  count: 10
```

The result comes out to be:

```bash
$ gridtest gridview grids.yml generate_empty --compact
[{}, {}, {}, {}, {}, {}, {}, {}, {}, {}]
```

<a id="parameterize-variables">
### Parameterize Variables

Let's say that we have two variables, x and y, and we want to generate a grid
of all possible combinations for a listing of each. That would look like this:

```yaml
    generate_matrix:
      grid:
        x: [1, 2, 3] 
        y: [1, 2, 3]
```

And the resulting grid will have 3x3 or 9 total combinations of x and y:

```bash
$ gridtest gridview grids.yml generate_matrix --compact
[{'x': 1, 'y': 1}, {'x': 1, 'y': 2}, {'x': 1, 'y': 3}, {'x': 2, 'y': 1}, {'x': 2, 'y': 2}, {'x': 2, 'y': 3}, {'x': 3, 'y': 1}, {'x': 3, 'y': 2}, {'x': 3, 'y': 3}]
```

<a id="parameterize-lists">
### Parameterize Lists

If you want to do similar but instead have a list of values be paramaterized, just 
specify a list of lists instead.

```yaml
    generate_lists_matrix:
      grid:
        x: [[1, 2, 3], [4, 5, 6]] 
        y: [[1, 2, 3], [4, 5, 6]] 
```

The result will have 2x2 or 4 entries:

```bash
$ gridtest gridview grids.yml generate_lists_matrix --compact
[{'x': [1, 2, 3], 'y': [1, 2, 3]}, {'x': [1, 2, 3], 'y': [4, 5, 6]}, {'x': [4, 5, 6], 'y': [1, 2, 3]}, {'x': [4, 5, 6], 'y': [4, 5, 6]}]
```

Here is an easier way to check the count:

```bash
$ gridtest gridview grids.yml generate_lists_matrix --count
4 lists produced.
```

<a id="range-of-values">
### Range of Values

For most use cases, you'll want to generate a list of values over a range. You
can do that with **min** and **max** and (optionally) **by** that defaults to 1.

```yaml
    generate_by_min_max:
      grid:
        x:
          min: 0
          max: 10
          by: 2
```

```bash
$ gridtest gridview grids.yml generate_by_min_max --compact
[{'x': 0}, {'x': 2}, {'x': 4}, {'x': 6}, {'x': 8}]
```

Here is an example with two variables:

```yaml
    generate_by_min_max_twovars:
      grid:
        x:
          min: 0
          max: 10
          by: 2
        y:
          min: 10
          max: 20
          by: 2
```

```bash
$ gridtest gridview grids.yml generate_by_min_max_twovars --compact
[{'x': 0, 'y': 10}, {'x': 0, 'y': 12}, {'x': 0, 'y': 14}, {'x': 0, 'y': 16}, {'x': 0, 'y': 18}, {'x': 2, 'y': 10}, {'x': 2, 'y': 12}, {'x': 2, 'y': 14}, {'x': 2, 'y': 16}, {'x': 2, 'y': 18}, {'x': 4, 'y': 10}, {'x': 4, 'y': 12}, {'x': 4, 'y': 14}, {'x': 4, 'y': 16}, {'x': 4, 'y': 18}, {'x': 6, 'y': 10}, {'x': 6, 'y': 12}, {'x': 6, 'y': 14}, {'x': 6, 'y': 16}, {'x': 6, 'y': 18}, {'x': 8, 'y': 10}, {'x': 8, 'y': 12}, {'x': 8, 'y': 14}, {'x': 8, 'y': 16}, {'x': 8, 'y': 18}]
```

Logically there are the previous number of tests, but squared.

```bash
$ gridtest gridview grids.yml generate_by_min_max_twovars --count
25 lists produced.
```
<a id="grids-with-functions">
## Grids with Functions

> What does it mean to use a function?

When you add a function to a grid, meaning the `func` key that maps
to a custom or system installed module and function (e.g. `random.choice`)
you are generating the same grid of parameters, but at the end passing them through
the function. This means that we get a list of results instead of a list of 
arguments.

> How do I use a function?

If you want to use functions that are importable (installed in your system python
or site-packages) then you can add the `func` variable. For example, the grid
below will call `random.choice` ten times across the sequence of values `[1, 2, 3]`.

```yaml
    random_choice:
      func: random.choice
      count: 10
      grid:
         seq: [[1, 2, 3]]
```

However, notice that we are no longer returning function inputs (e.g., dictionaries with
arguments) but rather the result of running the function specified with the arguments.
This is the main difference between having a function vs. not - provide a function
adds an extra step of running the arguments through it, and returning the result.

<a id="grids-with-custom-functions">
## Grids with Custom Functions

If you are using a script for any of your grids that isn't a system installed
module, then (akin to a standard gridtest) it needs to be included under a section 
header that is named by the relevant module, and that includes the filename to import.
For example, the file `script.py` in the present working directory has
a function, `get_pokemon_id` that I want to use. Here is how I'd write the recipe:

script:
  filename: script.py 
  grids:

    # A grid that will generate 10 random values using a function
    generate_pids:
      func: script.get_pokemon_id
      count: 10
```

Now let's run it!

```bash
$ gridtest gridview grids-with-function.yml generate_pids --compact
['296', '722', '490', '538', '71', '332', '869', '537', '222', '369']
```

Akin to the previous example, since we've provided a function to pass our grid
arguments into, the results are returned. This is how gridtest can
use a grid specified under a test to generate a list of values for an argument.

Next you might want to read about how gridtest grids can be 
[used in tests](https://vsoch.github.io/gridtest/getting-started/metrics/#adding-a-grid).
