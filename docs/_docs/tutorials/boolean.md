---
title: Boolean Logic Tutorial
category: Tutorials
permalink: /tutorials/boolean/index.html
order: 4
---

## Boolean Logic

If you haven't [installed]({{ site.baseurl }}/install/) gridtest, you should do this first.

### Write Functions

Let's say we start with these functions, and save them to a file called truefalse.py

```python
# These are functions in my script
# Typing is here, so Python 

def add(one, two):
    """add will add two numbers, one and two. There is no typing here"""
    return one + two

def add_with_type(one: int, two: int) -> int:
    """add_with_type will add two numbers, one and two, with typing for ints."""
    return one + two
```

We would first generate a gridtest template like the following:

```bash
$ gridtest generate truefalse.py truefalse-tests.yml
Extracting add from truefalse
Extracting add_with_type from truefalse
```

The first argument is the input for the generate command, and this can be
a filename, a folder name (that might contain multiple scripts) or a python
module string (.e.g, requests.get). The second argument is the gridtest
output file that will be produced with your tests. After you finish,
the file "truefalse-tests.yml" will have a list of tests that
you can add values for. You can delete sections that aren't relevant, or copy
paste new entries to each list for another testing case.

### Return Types

Since we are primarily interested with the `istrue` and `isfalse` return
types, let's just look at examples for each of those.

**istrue**

istrue is used when we want to check if something is True.
You usually would want to refer to an input or output variable:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    istrue: isinstance({% raw %}{{{ result }}{% endraw %}, int)
```

**isfalse**

or you might want the opposite, isfalse:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    isfalse: not isinstance({% raw %}{{{ result }}{% endraw %}, float)
```

**equals**

Equals is similar to returns, but implies some custom code or logic that
needs to be evaluated first:

```yaml
  script.add:
  - args:
      one: 1
      two: 2
    equals: 1+2
```

### Customize

You can then open the file in a text editor, and add arguments to each.
Since in this tutorial we want to test boolean logic, I'll show you what
my final testing yaml file looks like. I went from this starting template:

```yaml
truefalse:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/is-true-false/truefalse.py
  truefalse.add:
  - args:
      one: null
      two: null
  truefalse.add_with_type:
  - args:
      one: null
      two: null
```

to be something more reasonable to test:

```yaml
truefalse:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/is-true-false/truefalse.py
  truefalse.add:
  - args:
      one: 1.0
      two: 2
    istrue: "isinstance({% raw %}{{ result }}{% endraw %}, float)"
    isfalse: "isinstance({% raw %}{{ result }}{% endraw %}, int)"
  - args:
      one: 1.0
      two: 2
    equals: 1+2
  truefalse.add_with_type:
  - args:
      one: 1
      two: 2
    returns: 3
  - args:
      one: 1.0
      two: 2
    raises: TypeError
```

Notice that we are using istrue and isfalse conditional checks.
For typing, given that a function uses typing, that will be tested. For example,
the last function "add_with_type" would raise a TypeError if we give it a float.
This is why we have added a test case for it. Finally, the template strings `{% raw %}{{ result }}{% endraw %}`
and `{% raw %}{{ returns }}{% endraw %}` are spceial cases. Returns references what you specify your
test to return, and result specifies the result that is actually returned.
We use "result" above because we didn't do any checks for return values for
the same function.

## Test

Finally, you'll have your test file, and an environment where you want to
test. You can run tests like this:

```bash
$ gridtest test truefalse-tests.yml 
[4/4] |===================================| 100.0% 
success: truefalse.add.0 istrue isinstance(3.0, float) 
success: truefalse.add.1 equals 1+2 
success: truefalse.add_with_type.0 returns 3 
success: truefalse.add_with_type.1 raises TypeError 
4/4 tests passed
```

You might next want to browse other [tutorials]({{ site.baseurl }}/tutorials/) available.
