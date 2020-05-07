---
title: Templates
category: Getting Started
permalink: /getting-started/templates/index.html
order: 3
---

The power of your recipe comes down to your template. Knowing how input
and return types work is thus essential for writing awesome templates! The basic
recipe format has a module name as the first key, and then a list of [tests](#testing-types),
a filename, and [grids](#grids).

```yaml
script:
  filename: script.py
  tests:
     ...
  grids:
     ...
```

Each of these sections will be discussed below.

<a id="testing-types">
## Testing Types

<a id="basic-test">
### Basic Test

The default (most basic kind of test) that gridtest can run is to take some function
name, a set of arguments, and then just test that it runs:

```yaml
  script.write:
    args:
    - name: "dinosaur"
```

In the above snippet, if `script.write` runs with the
input "dinosaur" as name, this test will be successful. The next type is what
gives gridtest it's name, the "grid" specification. This is when we don't want
to define a single argument, but some set of parameters for gridtest to iterate
over. As an example, let's say that we have a function that takes an input, `seconds`, and sleeps
for that many seconds. Our default might start like this:

```yaml
  script.gotosleep:
    args:
      - seconds: 1
```

The above would run one test, and sleep for 1 second. But that's not really so
useful. We would want to define a range of values between 0 and 5, 
and then a few explicit higher values, 10 and 11. How would that look?

<a id="grid-test">
### Grid Test

We can accomplish better parameterization by using a grid in our test. That
looks like this:

```yaml
  script.gotosleep:
    grid:
      seconds:
        max: 5
        min: 0
        list: [10, 15]
```

In the example above, the previous argument (arg) has been moved to a section
called "grid" to indicate to gridtest that this is a grid of parameters to run
over, and not a one off value. Under grid we have an equivalent entry for
seconds, but this time, we define a min (0), a max (5), and a list to include
10 and 15. Gridtest would parse this to run tests over our sleep function
for all of these argument sets:

```python
[{'seconds': 0}, {'seconds': 1}, {'seconds': 2}, {'seconds': 3}, {'seconds': 4}, {'seconds': 10}, {'seconds': 15}]
```

And if we had other grid parameters defined, we'd build a matrix over them too.
Single values can remain in the args section, but **you are not allowed to have
the same parameter defined under both args and grid**. To be explicit about the
grid section:

**min** and **max** are to be used when specifying a range. When unset, **by** 
would be 1. If you want to decrease, set a negative value for by. You can assume
the values are going into range like `range(min, max, by)`.

**list** is for when you want to include a list of values, even in addition to a
range already specified as in the example above.

An interactive result report is planned to better illustrate the output here.

## Input Types

Gridtest can support multiple different kinds of input types that correspond
with common use cases. For example, many tests want to use a temporary
file as input. We might do something like:

```yaml
  script.write:
    args:
    - name: "dinosaur"
    - outfile: {% raw %}{% tmp_path %}{% endraw %}
    returns: {% raw %}{{ args.outfile }}{% endraw %}
```

In the above, the double `{% raw %}{{}}{% endraw %}` refers to a variable, in this case which is
an argument name. The `{% raw %}{% %}{% endraw %}` refers to a function that is known natively
to grid test. This syntax is based on [jinja2](https://jinja.palletsprojects.com/en/2.11.x/).
You could also check that the file exists (and it might not be returned).

```yaml
  script.write:
    args:
    - name: vanessa
    - outfile: {% raw %}{% tmp_path %}{% endraw %}
    exists: {% raw %}{{ args.outfile }}{% endraw %}
```

### Input Variables

An input variable is distinguished by being in the format `{% raw %}{{ <name> }}{% endraw %}`
where `<name>` would be some named variable, referenced below.

| Name        | Description | Syntax | Example |
|-------------|-------------|--------|---------|
| args.<name> | Refer to a named argument under args. |`{% raw %}{{ args.<name> }}{% endraw %}` | `{% raw %}{{ args.name }}{% endraw %}` |
| returns | Refer to the returns value you defined. |`{% raw %}{{ returns }}{% endraw %}` | `{% raw %}{{ returns }}{% endraw %}` |

If you want to refer to a results object just refer to the GridTest instance (self) directly. 
For example, to test that a requests.response_code is equal to a certain value, we can do:

```yaml
  requests.api.head:
  - args:
      url: https://google.com
    istrue: "self.result.status_code == 301"
```



### Function Variables

In addition to input variables, gridtest provides a few functions to make testing easier. Functions
are distinguished based on being in the format `{% raw %}{% <func> %}{% endraw %}`,
where "func" refers to the name of the function. Gridtest currently supports the following functions:

| Name        | Description | Syntax |
|-------------|-------------|--------|
| tmp_dir | Create (and cleanup) a temporary directory for testing. |`{% raw %}{% tmp_dir %}{% endraw %}` |
| tmp_path | Create (and cleanup) a temporary filename for testing. |`{% raw %}{% tmp_path %}{% endraw %}`|

For specifics about tmp_dir and tmp_path, see the [temp tutorial]({{ site.baseurl }}/tutorials/temp/).


### Return Types

For basic testing, there are typically a few obvious cases we want to test for:

 - returns: meaning that a function returns a specific value
 - raises: meaning that the function raises an error
 - exists: meaning that some output file is deemed to exist.
 - success: boolean to indicate if success (no error) is desired.
 - istrue: determine if a custom evaluated statement is true
 - isfalse: determine if a custom evaluated statement is false
 - equals: determine if a custom evaluated statement is equal to the result

If you see another simple testing case that you want added, please 
[open an issue](https://github.com/vsoch/gridtest/issues). Highly complex testing needs
probably should use a more substantial testing library. Let's look through how each of
these examples might be used for our add function.

**returns**

If we want to ensure that the correct value is returned, we would do:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    returns: 3
```

**raises**

If we wanted to ensure that an exception was raised, we would do:

```yaml
  script.add:
  - args:
      one: 1
      two: null
    raises: TypeError
```

**istrue**

istrue is used when we want to check if something is True.
You usually would want to refer to an input or output variable:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    istrue: isinstance({% raw %}{% returns %}{% endraw %}, int)
```

**isfalse**

or you might want the opposite, isfalse:


```yaml
  script.add:
  - args:
      one: 1
      two: 2
    isfalse: not isinstance({% raw %}{% returns %}{% endraw %}, float)
```

**equals**

or you might want to evaluate a statement. In the example below, we want to 
make sure an attribute of the value returned is equal to 200.

```yaml
  requests.get:
  - args:
      url: https://google.com
      data: null
      json: null
    eval: {% raw %}{% returns %}{% endraw %}.status_code == 200
```

This is different from providing an explicit value.

**success**

You might just want to run something, and be sure that the success status is False.
For example, if you give the wrong type as input to a function, it will by default
exit with an error:

```bash
$ gridtest test examples/basic/script-tests.yml 
[script.hello_with_type:6/6] |===================================| 100.0% 3% 
success: script.add.0 returns 3 
success: script.add.1 raises TypeError 
success: script.add_with_type.0 returns 3 
success: script.hello.0 
success: script.hello_with_default.0 
failure: script.hello_with_type.0 TypeError name (1) is <class 'int'>, should be <class 'str'>
```

However, if we update the test config from this:

```yaml
  script.hello_with_type:
  - args:
      name: 1
```

to this (to indicate that we expect failure):

```yaml
  script.hello_with_type:
  - args:
      name: 1
  success: false
```

the tests will pass!

**exists**

And finally, if our function saved a file, we'd want to check for that like this.
The following example checks that whatever filename is returned does exist:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    exists: {% raw %}{% returns %}{% endraw %}
```

A previous example showed how you could reference a specific input variable,
"outfile" existing. Since we also used the function `{% raw %}{% tmp_path %}{% endraw %}` this output
file will be cleaned up after the fact.

```yaml
  script.write:
    args:
    - name: vanessa
    - outfile: {% raw %}{% tmp_path %}{% endraw %}
    exists: {% raw %}{{ args.outfile }}{% endraw %}
```

**isinstance**

To check that a result is of a particular instance type, you can use `isinstance`
and provide the name of the class that would be returned as a string with `type(self.result).__name__`.
For example, to test if a custom Car instance is of type car.Car, we would do:

```yaml
  car.Car:
  - instance: thisone
    args:
      color: red
      lights: false
      wheels: 4
    isinstance: car.Car 
```

### Grids

If you've already read about [grids](../grids), you know that grids can be defined
in the context of testing to run tests across a grid of input arguments. A good
example of adding a grid is provided in the 
[metrics example](https://vsoch.github.io/gridtest/getting-started/metrics/#adding-a-grid).



You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
