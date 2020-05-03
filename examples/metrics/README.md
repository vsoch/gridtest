# Metrics

The most simple case of creating a GridTest is to do so by running a set of 
metrics (which are actually Python decorators) for a testing
file, and then setting ranges of variables to run within tests. For example,
let's start with the [is-true-false](../is-true-false/) example that has functions
for addition, and customize the file to have metric.

## Adding Metrics

The first thing to do is to add a metrics section. A metric can be any
custom python decorator that you can easily import. As a good starting example,
we can use a custom timeit provided in `gridtest.decorators`.
We would add this to the functions we want to measure:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/optimize/script.py

  script.add:
    # metrics are each a decorator, we first look to gridtest.decorators then external import
  - metrics:
      - "@timeit"
```

The `@` indicates that we are using a decorator, which is the current convention
in case other kinds of metrics might be used. Once we do this, when we run gridtest
with the file, it will by default detect the metric, and then run the functions
through it.

When you run the test, you'll see the results for metric decorators at the bottom.



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

## Adding a Grid

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
write a function that will sleep for some number of input seconds. We would then want to see
that the timeout output increases to match the input seconds.

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
