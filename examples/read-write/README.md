# Read and Write Example

This simple example will show you how to use the functions `{% tmp_path %}`
and `{% tmp_dir %}` to create and then reference a temporary file path or
directory, respectively.

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

We generated the initial template for the script [temp.py](temp.py)
included here like this:

```bash
$ gridtest generate temp.py gridtest.yml
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
each testing condition (or leave null for None). For more detail about
templating, see [the templating documentation](https://vsoch.github.io/gridtest/getting-started/templating). 
We ultimately updated the template to include the following:

```yaml
temp:
  filename: temp.py
  temp.create_directory:
  - args:
      dirname: "{% tmp_dir %}"
    returns: "{{ args.dirname }}"
  temp.write_file:
  - args:
      filename: "{% tmp_path %}"
    exists: "{{ args.filename }}"
```

The above recipe says that we want to test the function `create_directory`
in [temp.py](temp.py), and we want gridtest to generate a temporary directory
(the variable `{% tmp_dir %}` and then test that whatever name is generated
(`{{ args.dirname }}`) is returned by the function. For the function write_file,
the input "filename" will have a randomly generated temporary file created
for it with `{% tmp_path %}` that will want to ensure exists. Both will be 
cleaned up at the completion of the test.

## Test

We can run the tests as follows:

```bash
$ gridtest test gridtest.yml
[2/2] |===================================| 100.0%
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
temp.create_directory.0        success                        returns /tmp/gridtest-dir.ok6x5kiy
temp.write_file.0              success                        exists /tmp/gridtest-file-flp_cmi4

2/2 tests passed
```

And the directory mentioned, `/tmp/gridtest-dir.j0aio0l6` will be cleaned up
upon completion. If we don't want to clean it up, we can add `--no-cleanup`:

```bash
$ gridtest test gridtest.yml --no-cleanup
[2/2] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
temp.create_directory.0        success                        returns /tmp/gridtest-dir.n1devo3f
temp.write_file.0              success                        exists /tmp/gridtest-file-iqff2y__

2/2 tests passed
``` 

And then the directory generated would still exist after the run:

```bash
$ ls -l /tmp/gridtest-dir.e1c4gbr8/
total 0
```

Also, since gridtest.yml is the default, you don't need to specify it to
find the file in the present working directory:

```bash
gridtest gridtest.yml
```

The same is true for the testing file.
