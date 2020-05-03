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
