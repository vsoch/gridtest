---
title: Python
category: Getting Started
permalink: /getting-started/python/index.html
order: 4
---

GridTest can be interacted with from within a python shell. We do this
by way of the GridRunner.

## GridTest Shell

You can start a gridtest shell with a run by doing the following. In the command
below, we don't have a particular test file in mind to load, so we just issue
the `gridtest shell` command:

```bash
$ gridtest shell

Gridtest Interactive Shell
runner = GridRunner('tests.yml')
Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:      
```

Note that it's detected not having a testing file, and showed us how to load
a generic one:

```python
runner = GridRunner('tests.yml')
```

In fact, GridRunner is already loaded in the workspace, so we could just use it
on (an existing) test file.

```python
runner = GridRunner("temp-tests.yml")

runner                                                                  
# [gridtest|temp-tests.yml]
```

If you want to have this preloaded (and the runner available) just provide the
test file back when you originally do `gridtest shell`:

```bash
$ gridtest shell temp-tests.yml

Gridtest Interactive Shell
testfile: temp-tests.yml
  runner: [gridtest|temp-tests.yml]
Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.
```

You'll notice that now the interpreter shows us that we have the runner loaded,
and the testfile defined! Either way, once you are here, the easiest thing to do is just run the tests.

```python
runner.run()
runner.run(parallel=False)
```

And you can look at the function docstrings to see how to customize this command.
At this point we might want to get the tests, which are each of type
GridTest. This is a dictionary with keys corresponding to the test name,
and values the instantiation of a GridTest.

```python
tests = runner.get_tests()                                                      
{'temp.create_directory.0': [test|temp.create_directory],
 'temp.write_file.0': [test|temp.write_file]}
```

Let's say we wanted to interact with the first, we would inspect it as follows:

```python
test = tests['temp.create_directory.0']
test                                                                   
[test|temp.create_directory]
```

You can inspect parameters, run the test, or directly interact with many of the individual
functions for the class:

```python
test.params                                                            
{'args': {'dirname': '/tmp/gridtest-dir.ho18j_29'}}

test.run()
test.result
test.name                                                              
# 'temp.create_directory'
```

Please [open an issue](https://github.com/{{ site.repo }}/issues) if you would like specific help for using the classes
interactively.

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
