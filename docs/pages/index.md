---
title: GridTest
permalink: /
---

> What is GridTest?

GridTest is a library that specializes in generating parameter grids. The grids
are most obviously used for testing, but can extend to other use cases.
In the context of testing, GridTest makes it easy to discover functions,
classes, and arguments for your python scripts or modules, and then generate
a template for you to easily populate. Outside of testing, you can define
grids that are version controlled, programatically defined with functions,
and easy to interact with from the command line or Python interpreter.
Gridtest treats grids as first class citizens, and not as "the other thing
I need when I write tests."

> How might I use gridtest?

GridTest has use cases well beyond testing, because parameterization is used
widely across data science, and version control for reproducibility of those
parameterization is essential for reproducible, sustainable science.
This means that you might use GridTest for...

<a id="testing">
### Testing

A **gridtest**: is one that is run over a grid of parameter settings. Each test
can include a set of argument specifications, and optionally mapping these arguments
to functions so they can be programatically defined. 
A grid can be inline to the test (if not used elsewhere) or defined globally and shared.

<a id="grids">
### Parameterization

A **grid** is a global definition of a parameter matrix. You can define arguments,
and optionally functions to run to be mapped to arguments. Grids are generated
on demand, meaning when you iterate over a grid object so that they are more
optimal to use because we don't save any single, large list to memory.
Grids do not have to be used in testing! You might share a repository that only defines grids that people
can use across many different kinds of machine learning models, likely to run metrics.

<a id="metrics">
### Metrics

A **metric** is a Python decorator that is paired with a test that will measure some
attribute of a test. For example:
   - you might run a function across a grid of arguments, and then measure the time that each combination takes (the metric), and generate a report for inspection.
   - you might be doing text processing and having functions to parse text. Each function might be run over a grid of sentences and counts, and for each result, we want to count the number of unique words, and total words (metrics). This is the [interface example](examples/interface).

Take a look at the [examples](examples) folder or the [documentation](https://vsoch.github.io/gridtest) for getting started. An example report is available to view [here](https://vsoch.github.io/gridtest/templates/report/),
and as we get more real world use cases, the report templates and data export options will be expanded
to use and visualize them beautifully. Please [open an issue](https://github.com/vsoch/gridtest/issues) 
if you have a use case that @vsoch can help with!

<a id="kind-of-projects">

> What kind of projects is GridTest for?

If you manage a large open source project with a diverse community, and you
are looking for a testing framework, you probably don't need GridTest. 
<a href="https://docs.pytest.org/en/latest/" target="_blank">pytest</a> is
really good at this. GridTest is designed for smaller or individual-run
Python projects that don't have the bandwidth to invest time into writing tests, as it
makes it easy to generate and fill in a template to run tests,
and run them during continuous integration.

<a id="just-for-testing">
> Is gridtest just for testing?

As mentioned above, one of the powerful features of GridTest is the 
ability to define [grids](https://vsoch.github.io/gridtest/getting-started/grids/index.html) 
that can be used within gridtests, but also outside of them. For example, you can easily define sets of named
parameterizations over sets of variables, and even map arguments to functions. 
The result can be an expanded list of arguments, or of results.

> What makes GridTest easy to use?

GridTest nicely manages small annoyances for writing tests, or generating grids of parameters.
The author has listed these in the order that she finds interesting:

<a id="grids-as-first-class-citizens">
### 1. Grids as First Class Citizens

Parameters always come as a second thought when writing tests, and this is
why they are commonly applied as decorators. The author of this software
realized that she might want to define just sets of parameters that expand
into matrices that can be useful across many use cases. This makes
the grids first class citizens.

<a id="capturing-metrics">
### 2. Capturing Metrics

How long does your function take when you provide parameter X as one value, versus
another? By way of allowing you to specify one or more metrics alongside tests,
you can easily capture metrics (Python decorators to your functions to test)
to output in an interactive report.

<a id="generating-reports">
### 3. Generating Reports

If you need to save results to a data file (e.g., results.json) or generate
an interactive report for GitHub pages, this is easy to do do with running
Gridtest with the `--save` or `--save-web` flags. An example report is 
available to view [here](https://vsoch.github.io/gridtest/templates/report/),
and as we get more real world use cases, the report templates and data export 
options can be expanded to use and visualize them beautifully. Please [open an issue](https://github.com/vsoch/gridtest/issues) if you have a use case that @vsoch can help with!

<a id="debugging">
### 4. Debugging

What programmer hasn't been in the scenario of running a group of tests,
and then having some fail? What do you do in that case? You can start an interactive
shell, import what you need, and try to reproduce, or you can turn up verbosity
and add a bunch of print statements to figure out what is going on. GridTest makes
this much easier with it's `--interactive` mode, which will let you simply
shell into an interpreter right before the function is run, and let you debug 
away.

<a id="reproducible-tests">
### 5. Running Reproducible Tests

When you write tests for a file, local, or system module, you store them in
a yaml file that is stored alongside the code, and can be tested with CI.
The yaml file can have grids of parameters defined so you can easily test many
different combinations.

<a id="knowing-tests">
### 6. Knowing the tests to write

Whether you write as you go or at the end, you have to look back at your files
to know the functions names and arguments that need to be tested. GridTest solves
this problem by way of discovery - give it a module name, a file name, or
an entire directory with Python files, and it will generate a template for you
to easily fill in that already includes arguments and functions. 

<a id="knowing-new-tests">
### 7. Knowing new tests to write

Okay great, so you've already written your tests. What if you add a function,
and haven't written tests for it yet? GridTest can tell you this too with it's
`--check` feature. It will let you run it against your previously generated file
and tell you exactly the functions that need to be added. Then remove `--check`
and it will add them.


In summary, GridTest:

 1. Let's you define grids to be generated programatically, version controlled, and used for multiple purposes
 2. Allows measuring of metrics alongside tests
 3. Stores tests in a yaml file that can be stored in version control
 4. Generates data exports and interactive reports for results
 5. Provides an easier way to interactively debug
 6. Helps you to discover the tests that you need to write, and creates a template to fill in
 7. Makes it easy to define and interact with expanded parameter grids


> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page,
which has links for getting started with writing tests, running tests, and many examples.
