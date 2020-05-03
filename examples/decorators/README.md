# Objectives

The most simple case of creating a GridTest is to do so by running a set of 
benchmarks (which are actually Python decorators) for a testing
file, and then setting ranges of variables to run within tests. For example,
let's start with the [is-true-false](../is-true-false/) example that has functions
for addition, and customize the file to have benchark.

## Adding Benchmarks

The first thing to do is to add a benchmarks section. A benchmark can be any
custom python decorator that you can easily import. As a good starting example,
we can use the function [timeit](https://docs.python.org/3/library/timeit.html) 
that is built into modern Python installations. We would add this to the top of the
file:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/optimize/script.py

  # objectives are each a decorator
  objectives:
    - "@timeit"
```

The `@` indicates that we are using a decorator, which is the current convention
in case other kinds of benchmarks might be used. Once we do this, when we run gridtest
with the file, it will by default detect the objective, and then run the functions
through it.


When you run the test, you'll see the results for decorators at the bottom.



```bash
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
