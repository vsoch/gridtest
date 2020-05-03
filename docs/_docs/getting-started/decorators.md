---
title: Debugging
category: Getting Started
permalink: /getting-started/deorators/index.html
order: 6
---

### Decorators

Gridtest includes a suite of decorators that can be added to gridtest.yml
test yaml files in order to measure a benchmark or metric to optimize. As 
an example, let's take a look at using the (likely familiar) timeit decorator,
which we can find in `gridtest.decorators`:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/optimize/script.py

  script.add:
    # objectives are each a decorator, we first look to gridtest.decorators then external import
  - objectives:
      - "@timeit"
    args:
      one: 1.0
      two: 2
    istrue: "isinstance({{ result }}, float)"
    isfalse: "isinstance({{ result }}, int)"
```

The recipe above is very simple - we are testing a single function, script.add, and
we've defined one objective, a decorator called "timeit" to measure the total time.
Note that objectives belong on the level of the test, since it's likely we don't want
to use any single decorator across all tests.

### Attributes of a Decorator

Decorators can only work together (meaning multiple applied to the same function,
and collected for the same single run) given that:

 1. they don't interfere with the function input and return of output
 2. they don't add significant processing / computational needs
 3. they must print their name (identifier) to stdout on a single line, followed by their result

Given these three criteria are met, we can apply multiple decorators to one
function run, and easily collect output based on parsing the stdout. We can then
even generate a report for the run that shows the different metrics. 

### Running with a Decorator

So let's first try running with a simple decorator. You'll notice that the objectives
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

A more interactive results view will be developed, along with more real world examples for 
using a decorator.
You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
