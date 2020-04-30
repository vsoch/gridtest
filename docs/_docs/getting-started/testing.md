---
title: Testing
category: Getting Started
permalink: /getting-started/testing/index.html
order: 6
---

You likely want to integrate GridTest into your favorite continuous integration
(CI) service and there are many good ways to do that.

## GridTest Linting

If you add a new function to your testing library, you probably
want to ensure that you've written a test for it. Akin to black for code
formatting, gridtest provides a gridtest check command
to check if a file has all tests written. In the case that all functions
are represented, the return code is 0 (and the CI will pass):

```bash
$ gridtest check tests/modules/temp-tests.yml 

No new tests to add!✨ 🥑️ ✨

# Return code is 0
$ echo $?
0
```

But now let's say that we update the module associated with the testing file
and add a new function.

```python
def new_function():
    print("No test for me!")
```

And then we run checks again:


```bash
$ gridtest check tests/modules/temp-tests.yml 

New sections to add:
tests.modules.temp.new_function
```

Since we have a new test (and missed it) the return code is exit with an error (1):

```bash
echo $?
1
```

If we wanted to skip this test, we could do that by defining a skip pattern:

```bash
$ gridtest check tests/modules/temp-tests.yml --skip-patterns new_function

No new tests to add!✨ 🥑️ ✨
```

And the return code is again 0 (meaning it would pass in CI).

```bash
$ echo $?
0
```

## GridTest Updating

Let's take this same file, and say that we've checked it, and found that a new test
needs to be added. How do we add the function to the template? You can run
the update command:

```bash
$ gridtest update tests/modules/temp-tests.yml 
Adding function temp.new_function
Writing [gridtest|temp-tests.yml] to tests/modules/temp-tests.yml
```

Update is similar to generate, but we already have the filename (for the file
or module) added to the testing file and don't need to specify it again.
The test file is updated with the new function (which is rather boring, it doesn't
have any arguments)

```yaml
temp:
  filename: /home/vanessa/Desktop/Code/gridtest/tests/modules/temp.py
  temp.create_directory:
  - args:
      dirname: '{% raw %}{% tmp_dir %}{% endraw %}'
  temp.new_function:
  - args: {}
  temp.write_file:
  - args:
      filename: '{% raw %}{% tmp_path %}{% endraw %}'
```

## Continuous Integration Recipes

Gridtest will have templates added soon for particular continuous integration
provides. Generally, you can use the above `gridest check <testfile>.yml`
to check for needing to write tests, and then the standard grid runner
(with any options you need) to run the tests, after installing gridtest.
For example, in a run statement you might do:

```bash
pip install gridtest
gridtest run testfile.yml
```

We will have more examples coming shortly!
