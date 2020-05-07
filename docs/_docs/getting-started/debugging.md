---
title: Debugging
category: Getting Started
permalink: /getting-started/debugging/index.html
order: 2
---

### Why Debugging?

For most testing frameworks, when you hit an error there is a flash of red across the
screen, and at best you can stop execution on the first error (e.g., with pytest you would
add the -x flag) or add print statements to the test to see what might be going on. 
You might start an interactive shell to import modules and functions needed to debug,
and then need to exit and run again to re-run the test. Instead of these approaches,
gridtest gives you an ability to run a test with `--interactive`, meaning that you
can open an interactive shell at the onset of each test.

### An example Python script

Let's say that we have this script, called "script.py"

```python
# These are functions in my script
# Typing is here, so Python 

def add(one, two):
    """add will add two numbers, one and two. There is no typing here"""
    return one + two

def add_with_type(one: int, two: int) -> int:
    """add_with_type will add two numbers, one and two, with typing for ints."""
    return one + two

def hello(name):
    """print hello to a name, with no typing"""
    print(f"hello {name}!")

def hello_with_default(name="Dinosaur"):
    """print hello to a name with a default"""
    print(f"hello {name}!")

def hello_with_type(name: str) -> None:
    """print hello to a name, with typing"""
    print(f"hello {name}!")
```

And from it we've produced this testing file "script-tests.yml" in the same directory:

```yaml
script:
  filename: script.py
  tests:
    script.add:
    - args:
        one: 1
        two: 2
      returns: 3
    - args:
        one: 1
        two: null
      raises: TypeError
    script.add_with_type:
    - args:
        one: 1
        two: 2
      returns: 3
    script.hello:
    - args:
        name: Vanessa
    script.hello_with_default:
    - args:
        name: Dinosaur
    script.hello_with_type:
    - args:
        name: 1
      success: false
```

### Running Tests

We would run it with gridtest as follows:

```bash
$ gridtest test script-tests.yml 
[6/6] |===================================| 100.0% 
success: script.add.0 returns 3 
success: script.add.1 raises TypeError 
success: script.add_with_type.0 returns 3 
success: script.hello.0 
success: script.hello_with_default.0 
success: script.hello_with_type.0 
6/6 tests passed
```

Now let's say there is an error in a script. Let's randomly raise an exception:

```python
def hello(name):
    """print hello to a name, with no typing"""
    raise Exception('ruhroh')
```

If we run tests again, we see a failure with an unexpected exception:

```bash
$ gridtest test script-tests.yml 
[6/6] |===================================| 100.0% 
success: script.add.0 returns 3 
success: script.add.1 raises TypeError 
success: script.add_with_type.0 returns 3 
failure: script.hello.0 ruhroh Unexpected Exception: Exception.
success: script.hello_with_default.0 
success: script.hello_with_type.0 
5/6 tests passed
```

### Adding Interactivity

If we add the `--interactive` flag, it's going to allow us to cycle through
*every single test* and press Control+d to jump to the next test:

```python
$ gridtest test script-tests.yml --interactive
[script.add:1/6] |=====|-----------------------------|  16.7% 

Gridtest interactive mode! Press Control+D to cycle to next test.

Variables
   func: <function add at 0x7fe4c0a44200>
 module: <module 'script' from '/home/vanessa/Desktop/Code/gridtest/examples/basic/script.py'>
   args: {'one': 1, 'two': 2}
returns: 3

How to test
passed, error = test_types(func, args, returns)
result = func(**args)

Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:                                                                     
```

But that's not really what we want - we know the failing test is `script.hello.0`
so let's run the tests, but only this particular test for interactive:

```python
$ gridtest test script-tests.yml --interactive --name script.hello

[script.add:1/6] |=====|-----------------------------|  16.7% False
[script.add:2/6] |===========|-----------------------|  33.3% False
[script.add_with_type:3/6] |=================|-----------------|  50.0% False
[script.hello:4/6] |=======================|-----------|  66.7% True


Gridtest interactive mode! Press Control+D to cycle to next test.

Variables
   func: <function hello at 0x7fc118e8c680>
 module: <module 'script' from '/home/vanessa/Desktop/Code/gridtest/examples/basic/script.py'>
   args: {'name': 'Vanessa'}
returns: None

How to test
passed, error = test_types(func, args, returns)
result = func(**args)

Python 3.7.4 (default, Aug 13 2019, 20:35:49) 
Type 'copyright', 'credits' or 'license' for more information
IPython 7.8.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]:
```

In the example above, we show that the function, module, and arguments for
the test are loaded, and you are shown how to run the tests. For example,
here is how we would inspect arguments and then test typing:

```python
In [1]: args                                                                                                                                 
Out[1]: {'name': 'Vanessa'}

In [2]: passed, error = test_types(func, args, returns)                                                                                      

In [3]: passed                                                                                                                               
Out[3]: True

In [4]: error                                                                                                                                
Out[4]: []
```

And then run the actual test to trigger the full error:

```python
In [6]: result = func(**args)                                                                                                                
hello Vanessa!
---------------------------------------------------------------------------
Exception                                 Traceback (most recent call last)
~/Desktop/Code/gridtest/gridtest/main/helpers.py in <module>
----> 1 result = func(**args)

~/Desktop/Code/gridtest/examples/basic/script.py in hello(name)
     18     """print hello to a name, with no typing"""
     19     print(f"hello {name}!")
---> 20     raise Exception('ruhroh')
     21 
     22 def hello_with_default(name="Dinosaur"):

Exception: ruhroh
```

At this point, you can interact with your arguments or the function to debug further.

### Specifying Names

In the case of a file with multiple tests (the typical case) You can also specify the name of the test you want
to interact with:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add
```

For the above, this would interact with all tests that start with script.add. If you
want to limit to the script.add module, you might want to do:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add.
```

Or a specific indexed text for the module:

```python
$ gridtest test examples/basic/script-tests.yml --interactive --name script.add.0
```

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
