---
title: GridTest
permalink: /
---

**this library and documentaiton is under development**

> What is GridTest?

If you ask any software engineer about best practices, they will undoubtably
tell you about testing. While there are great tools in Python to write tests
(e.g. <a href="https://docs.pytest.org/en/latest/" target="_blank">pytest</a>)
let's be real - writing tests is arduous, and often not a priority when
research needs to be done, papers written, and other activities for the researcher
that are (really) absolutely necessary. Writing tests is hard. But we should
still be able to put testing in place without significant effort.

The developer of this software ran into the same conundrum. Even though she would
take the time to write tests, there were always smaller libraries that she didn't
invest time to do so. Could there be an easier way to quickly write tests? 
This was the purpose of developing GridTest.

> What kind of projects is GridTest for?

If you manage a large open source project with a diverse community, you
probably don't need GridTest. GridTest is designed for smaller or individual-run
Python projects that don't have the bandwidth to invest time into writing tests, as it
makes it easy to generate and fill in a template to run tests,
and run them during continuous integration.

> What makes GridTest easy to use?

GridTest nicely manages small annoyances for writing tests.

### 1. Knowing the tests to write

Whether you write as you go or at the end, you have to look back at your files
to know the functions names and arguments that need to be tested. GridTest solves
this problem by way of discovery - give it a module name, a file name, or
an entire directory with Python files, and it will generate a template for you
to easily fill in that already includes arguments and functions. 

### 2. Knowing new tests to write

Okay great, so you've already written your tests. What if you add a function,
and haven't written tests for it yet? GridTest can tell you this too with it's
`--check` feature. It will let you run it against your previously generated file
and tell you exactly the functions that need to be added. Then remove `--check`
and it will add them.

### 3. Debugging

What programmer hasn't been in the scenario of running a group of tests,
and then having some fail? What do you do in that case? You can start an interactive
shell, import what you need, and try to reproduce, or you can turn up verbosity
and add a bunch of print statements to figure out what is going on. GridTest makes
this much easier with it's `--interactive` mode, which will let you simply
shell into an interpreter right before the function is run, and let you debug 
away.

### 4. Running Reproducible Tests

When you write tests for a file, local, or system module, you store them in
a yaml file that is stored alongside the code, and can be tested with CI.

In summary, GridTest:

 1. Helps you to discover the tests that you need to write, and creates a template to fill in
 2. Provides an easier way to interactively debug
 3. Stores tests in a yaml file that can be stored in version control


> Where do I go from here?

A good place to start is the [getting started]({{ site.baseurl }}/getting-started/) page,
which has links for getting started with writing tests, running tests, and many examples.
