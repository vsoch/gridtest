---
title: Temporary Tutorial
category: Tutorials
permalink: /tutorials/temp/index.html
order: 3
---

## Temporary Paths

In this tutorial we will show you how to use the functions `{% raw %}{% tmp_path %}{% endraw %}` and `{% raw %}{% tmp_dir %}{% endraw %}` to  create and then reference a temporary file path or directory, respectively.
If you want to see how to generate tests you might see the [basic](basic) tutorial instead.
If you haven't [installed]({{ site.baseurl }}/install/) gridtest, you should do this first.

### Generate Testing Template

Let's say that we have this script, called "temp.py"

```python
# Basic functions for testing custom functions in format {% raw %}{% tmp_path %}{% endraw %}

import os


def write_file(filename):
    """write a file with some random nonsense"""
    with open(filename, "w") as filey:
        filey.write("I heard there was an octupus living in that Christmas tree.")


def create_directory(dirname):
    """create a directory named according to input variable dirname"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)
    return dirname
```

Notice that the first function writes a temporary file that comes from
an input, and the second creates a directory and returns it. For
this gridtest, we will want to test these functions. We thus
generated the initial template for the script temp.py shown above
like this:

```bash
$ gridtest generate temp.py temp-tests.yml
Extracting write_file from temp
Extracting create_directory from temp
```

The first argument is the input for the generate command, and this can be
a filename, a folder name (that might contain multiple scripts) or a python
module string (.e.g, requests.get). The second argument is the gridtest
output file that will be produced with your tests. After you finish,
the "temp-tests.yml" file will have a list of tests that
you can add values for. You can delete sections that aren't relevant, or copy
paste new entries to each list for another testing case.

### Customize

You can then open the file in a text editor, and add arguments to each.
If your library uses typing, the typing will be checked at testing time,
and it's not specified here. You'll generally want to fill in args for
each testing condition (or leave null for None). For more detail about
templating, see [the templating documentation](https://vsoch.github.io/gridtest/getting-started/templating). 
We ultimately updated the template to include the following:

```yaml
temp:
  filename: temp.py
  temp.create_directory:
  - args:
      dirname: "{% raw %}{% tmp_dir %}{% endraw %}"
    returns: "{% raw %}{{ args.dirname }}{% endraw %}"
  temp.write_file:
  - args:
      filename: "{% raw %}{% tmp_path %}{% endraw %}"
    exists: "{% raw %}{{ args.filename }}{% endraw %}"
```

The above recipe says that we want to test the function `create_directory`
temp.py, and we want gridtest to generate a temporary directory
(the variable `{% raw %}{% tmp_dir %}{% endraw %}` and then test that whatever name is generated
(`{% raw %}{{ args.dirname }}{% endraw %}`) is returned by the function. For the function write_file,
the input "filename" will have a randomly generated temporary file created
for it with `{% raw %}{% tmp_path %}{% endraw %}`, and we will test that it exists by referencing it
with `{% raw %}{{ args.filename }}{% endraw %}`. Both will also be cleaned up at the completion of the test.


## Test

Once we have our testing file and the original script, we can run the tests as follows:

```bash
$ gridtest test temp-tests.yml 
[2/2] |===================================| 100.0% 
success: temp.create_directory.0 returns /tmp/gridtest-dir.j0aio0l6 
success: temp.write_file.0 exists /tmp/gridtest-file-ped8_9zl
2/2 tests passed
```

And the directory mentioned, `/tmp/gridtest-dir.j0aio0l6` will be cleaned up
upon completion. If we don't want to clean it up, we can add `--no-cleanup`:

```bash
$ gridtest test temp-tests.yml --no-cleanup
[2/2] |===================================| 100.0% 
success: temp.create_directory.0 returns /tmp/gridtest-dir.e1c4gbr8 
success: temp.write_file.0 exists /tmp/gridtest-file-abd8-4yt
2/2 tests passed
``` 

And then the directory generated would still exist after the run:

```bash
$ ls -l /tmp/gridtest-dir.e1c4gbr8/
total 0
```

The same would be true for the testing file.

You might next want to browse [tutorials]({{ site.baseurl }}/tutorials/) available.
