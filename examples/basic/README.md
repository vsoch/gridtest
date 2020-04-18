# Basic Example

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

then you can cd into this folder, and test generating a gridtest file for the
[script.py](script.py) included here:

```bash
$ gridtest generate script.py script-tests.yml
```

The first argument is the input for the generate command, and this can be
a filename, a folder name (that might contain multiple scripts) or a python
module string (.e.g, requests.get). The second argument is the gridtest
output file that will be produced with your tests. After you finish,
the [script-tests.yml](script-tests.yml) will have a list of tests that
you can add values for. You can delete sections that aren't relevant, or copy
paste new entries to each list for another testing case.
