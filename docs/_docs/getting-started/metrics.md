---
title: Metrics
category: Getting Started
permalink: /getting-started/metrics/index.html
order: 6
---

### Metrics

Gridtest includes a suite of decorators that can be added to gridtest.yml
test yaml files in order to measure a benchmark or metric.  These include:

| Name   | Description                            | Usage    |
|--------|----------------------------------------|----------|
| timeit | print time (ms) for function execution | @timeit  |

This namespace of decorators will be looked for in the `gridtest.decorators`
module and you don't need to specify this path. If you define a custom decorator, 
you can simply define the module and function to import (e.g., `@script.mydecorator`).

<a id="an-example-decorator">
### An Example Decorator

As an example, let's take a look at using the (likely familiar) timeit decorator,
which we can find in `gridtest.decorators`:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/optimize/script.py
  tests:
    script.add:
      # metrics are each a decorator, we first look to gridtest.decorators then external import
    - metrics:
        - "@timeit"
      args:
        one: 1.0
        two: 2
      istrue: "isinstance(self.result, float)"
      isfalse: "isinstance(self.result, int)"
```

The recipe above is very simple - we are testing a single function, script.add, and
we've defined one metric, a decorator called "timeit" to measure the total time.
Note that metrics belong on the level of the test, since it's likely we don't want
to use any single decorator across all tests.

<a id="attributes-of-a-metric-decorator">
### Attributes of a Metric Decorator

Decorators can only work together (meaning multiple applied to the same function,
and collected for the same single run) given that:

 1. they don't interfere with the function input and return of output
 2. they don't add significant processing / computational needs
 3. they must print their name (identifier) to stdout on a single line, followed by their result

Given these three criteria are met, we can apply multiple decorators to one
function run, and easily collect output based on parsing the stdout. We can then
even generate a report for the run that shows the different metrics. 

<a id="running-with-a-decorator">
### Running with a Decorator

So let's first try running with a simple metric to record time. You'll notice that the metrics
is printed in a second table to the screen!

```bash
$ gridtest test
[4/4] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
script.add.0                   success                        istrue isinstance(self.result, float) isfalse isinstance(self.result, int)
script.add.1                   success                        equals 1+2                    
script.add_with_type.0         success                        returns 3                     
script.add_with_type.1         success                        raises TypeError              

________________________________________________________________________________________________________________________
script.add.0                   @timeit                        0.00 ms                       

4/4 tests passed
```

<a id="adding-a-grid">
### Adding a Grid

Great - so we've measured time for one function. What if we want to measure the time for
a function, but across a parameter grid? We might want to adopt our recipe to allow for this:

```yaml
    # A grid specification of a parameter - min 0, max 5, increment by 1, also add 10 and 15
    grid:
      one:
        min: 0
        max: 5
        list: [10, 15]
    args:
      two: 2
```

but this won't produce a very interesting result, because the result is just adding
two numbers. Let's try something that will work with out timeit function, namely
write a function that will sleep for some number of input seconds. 
Our goal is to see that the timeout output increases to match the input seconds.
That might look like this:

```python
from time import sleep
def gotosleep(seconds):
    """sleep for whatever specified number of seconds are provided"""
    sleep(seconds)
```

We would then use `gridtest check` to detect the new function:

```bash
$ gridtest check test.yml 

New sections to add:
script.script.gotosleep
```

And add the template to work with.

```bash
$ gridtest update gridtest.yml
Adding function script.gotosleep
Writing [gridtest|test.yml] to test.yml
```

And then fill in the template to add the metrics `timeit` and also define a grid
of parameters to run it over. That might look like this:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/optimize/script.py
  script.gotosleep:
  - metrics:
    - '@timeit'
    grid:
      seconds:
        list: [10, 15]
        max: 5
        min: 0
```

Before we run the test, let's talk about the formatting of the yaml.
Notice that we've moved the "one" argument up from the "args" section into the grid
section. This tells gridtest that we want to run a grid of tests for some 
parameterization of our argument "one." In the example above, we want to include
a range from 0 to 5 (default increment is by 1) and also add the one off values of 10 and 15 
(provided in list). This gives us the following allowable keys for a grid
parameter:

**min** and **max** are to be used when specifying a range. When unset, **by** 
would be 1. If you want to decrease, set a negative value for by.

**list** is for when you want to include a list of values, even in addition to a
range already specified as in the example above.

<a id="run-the-gridtest">
## Run the GridTest

Now let's run the test!

```bash
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
script.gotosleep.0             success                                                      
script.gotosleep.1             success                                                      
script.gotosleep.2             success                                                      
script.gotosleep.3             success                                                      
script.gotosleep.4             success                                                      
script.gotosleep.5             success                                                      
script.gotosleep.6             success                                                      
script.add.0                   success                        istrue isinstance(self.result, float) isfalse isinstance(self.result, int)
script.add.1                   success                        equals 1+2                    
script.add_with_type.0         success                        returns 3                     
script.add_with_type.1         success                        raises TypeError              

________________________________________________________________________________________________________________________
script.gotosleep.0             @timeit                        0.01 ms                       
script.gotosleep.1             @timeit                        1000.77 ms                    
script.gotosleep.2             @timeit                        2001.84 ms                    
script.gotosleep.3             @timeit                        3001.72 ms                    
script.gotosleep.4             @timeit                        4003.81 ms                    
script.gotosleep.5             @timeit                        10009.59 ms                   
script.gotosleep.6             @timeit                        15013.49 ms                   

11/11 tests passed
```

Awesome! We've run a grid of tests over the different values for seconds, and have 
reported the total time taken via the timeit decorator. See the [gridtest.yml](gridtest.yml)
for the full test recipe.

A more interactive results view will be developed, along with more real world examples for 
using a decorator, and custom decorator.

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
