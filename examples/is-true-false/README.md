# istrue and isfalse

This is-true-false example will show how to generate and run a grid test
to use the istrue and isfalse conditional checks.

## Install

After you've installed gridtest:

```bash
git clone git@github.com:vsoch/gridtest
cd gridtest
pip install -e .
```

or

```bash
pip install gridtest
```

## Generate

then you can cd into this folder, and test generating a gridtest file for the
[truefalse.py](truefalse.py) included here:

```bash
$ gridtest generate truefalse.py gridtest.yml
Extracting add from truefalse
Extracting add_with_type from truefalse
```

The first argument is the input for the generate command, and this can be
a filename, a folder name (that might contain multiple scripts) or a python
module string (.e.g, requests.get). The second argument is the gridtest
output file that will be produced with your tests. After you finish,
the [gridtest.yml](gridtest.yml) will have a list of tests that
you can add values for. You can delete sections that aren't relevant, or copy
paste new entries to each list for another testing case.

## Customize

You can then open the file in a text editor, and add arguments to each.
If your library uses typing, the typing will be checked at testing time,
and it's not specified here. You'll generally want to fill in args for
each testing condition (or leave null for None). For example, we might want to 
change:

```yaml
  script.add:
    args:
    - one: null
    - two: null
```

to instead be:

```yaml
  script.add:
    args:
    - one: 1
    - two: 2
```

To test adding 1+2. 

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
    istrue: isinstance({% returns %}, int)
```

**isfalse**

or you might want the opposite, isfalse:


```yaml
  script.add:
  - args:
      one: 1
      two: 2
    isfalse: not isinstance({% returns %}, float)
```

This means that we can edit our script from this:

```yaml
truefalse:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/is-true-false/truefalse.py
  tests:
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
  tests:
    truefalse.add:
    - args:
        one: 1.0
        two: 2
      istrue: "isinstance({{ result }}, float)"
      isfalse: "isinstance({{ result }}, int)"
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

For typing, given that a function uses typing, that will be tested. For example,
the last function "add_with_type" would raise a TypeError if we give it a float.
This is why we have added a test case for it. Finally, the template strings `{{ result }}`
and `{{ returns }}` are spceial cases. Returns references what you specify your
test to return, and result specifies the result that is actually returned.
We use "result" above because we didn't do any checks for return values for
the same function.

## Test

Finally, you'll have your test file, and an environment where you want to
test. You can run tests like this:

```bash
$ gridtest test gridtest.yml
[4/4] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
truefalse.add.0                success                        istrue isinstance(3.0, float) isfalse isinstance(3.0, int)
truefalse.add.1                success                        equals 1+2                    
truefalse.add_with_type.0      success                        returns 3                     
truefalse.add_with_type.1      success                        raises TypeError              

4/4 tests passed
```

Or since gridtest.yml is the default, just do:

```bash
$ gridtest test
```
