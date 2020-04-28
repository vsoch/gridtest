---
title: Templates
category: Getting Started
permalink: /getting-started/templates/index.html
order: 3
---

The power of your recipe comes down to your template. Knowing how input
and return types work is thus essential for writing awesome templates!

## Testing Types

The default (most basic kind of test) that gridtest can run is to take some function
name, a set of arguments, and then just test that it runs:

```yaml
  script.write:
    args:
    - name: "dinosaur"
```

If the script "write" runs in the file or module "script" simply runs with the
input "dinosaur" as name, this test will be successful. We plan to add a matrix
type that will look something like this:

```yaml
  script.write:
    matrix:
       ...
```

More detail will be added as this is developed. This will make it easy to run
a grid of tests for a function.

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

### Return Types

For basic testing, there are typically a few obvious cases we want to test for:

 - returns: meaning that a function returns a specific value
 - raises: meaning that the function raises an error
 - exists: meaning that some output file is deemed to exist.
 - success: boolean to indicate if success (no error) is desired.

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

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
