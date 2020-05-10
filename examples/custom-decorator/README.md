# Custom Decorator

If you want to run a gridtest that uses a custom metric, you can easily
do this by defining your own decorator. For example, let's say we have a function
to do some kind of text processing. It takes some number of inputs, and
returns raw text. We would then want to count the unique words in the raw text.
Let's go!

### Create your Functions

Let's first write our functions. We will write a simple function to take
some text input and parse it (`multiply_sentences`) and a decorator
to run any function that returns a string of text, and count the unique
words (`countwords`)

```python
# These are functions in my script

def multiply_sentence(sentence, count):
    return sentence * count

def countwords(func):
    """this is a simple example of a custom decorator - the idea would be that
       the function we are decorating returns some texty value, and we split
       this value by a blank space and then count the number of tokens (words).
    """
    def counter(*args, **kwargs):
        result = func(*args, **kwargs)
        words = len(set(result.split(' ')))
        print(f"@script.countwords {words} words")
        return result

    return counter
```
An important note about the decorator - it needs to be importable, meaning either
the module is already on your Python path, or it's included somewhere in the library
that you are testing. Also note that in order for gridtest to parse the result, you
need to print something to stdout that is prefixed **exactly** with the name of
the decorator defined under metrics. E.g., if we changed `script.countwords` to just
`countwords` the result wouldn't be properly parsed, because gridtest is looking
for the the first.


### Generate your Template

Let's generate a simple template that we can fill in to include a grid. We can
first preview it:

```bash
$ gridtest generate script.py

script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/custom-decorator/script.py
  tests:
    script.countwords:
    - args:
        func: null
    script.multiply_sentence:
    - args:
        count: null
        sentence: null
```

We don't want a test for the decorator, so we will write this to file, and remove it.

```bash
$ gridtest generate script.py gridtest.yml

script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/custom-decorator/script.py
  tests:
    script.multiply_sentence:
    - args:
        count: null
        sentence: null
```

Next, let's better refine our arguments.

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/custom-decorator/script.py
  tests:
    script.multiply_sentence:
    - metrics:
      - '@script.countwords'
      args:
        count: [1, 5, 10]
        sentence:
          - "He ran for the hills."
          - "Skiddery-a rinky dinky dinky, skittery rinky doo."
          - "You are my sunshine, my only sunshine."
```

Just for your FYI - if you had wanted to have some set of arguments shared
between tests, you could have defined them as a named grid:

```yaml
grids:
  script_inputs:
    args:
      count: [1, 5, 10]
      sentence:
        - "He ran for the hills."
        - "Skiddery-a rinky dinky dinky, skittery rinky doo."
        - "You are my sunshine, my only sunshine."
```

and then instead pointed to it for your test:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/custom-decorator/script.py
  tests:
    script.multiply_sentence:
    - metrics:
      - '@script.countwords'
      grid: script_inputs
```

By default, a grid is generated at the test creation time. However, if you have 
a grid shared by many functions that you want to calculate once and cache,
just set the cache variable to true:


```yaml
grids:
  script_inputs:
    cache: true
    args:
      count: [1, 5, 10]
      sentence:
        - "He ran for the hills."
        - "Skiddery-a rinky dinky dinky, skittery rinky doo."
        - "You are my sunshine, my only sunshine."
```

Regardless of how we specify our grid (globally or inline) the grid says that
for each sentence under the list of sentences, we will run the function
`multiply_sentence` with counts of 1,5, and 10. This would come down to 3x3 or 9 total tests.

### Running Tests

Let's run the tests! We should see a count of words for each function.

```bash
$ gridtest test
[9/9] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
script.multiply_sentence.0     success                                                      
script.multiply_sentence.1     success                                                      
script.multiply_sentence.2     success                                                      
script.multiply_sentence.3     success                                                      
script.multiply_sentence.4     success                                                      
script.multiply_sentence.5     success                                                      
script.multiply_sentence.6     success                                                      
script.multiply_sentence.7     success                                                      
script.multiply_sentence.8     success                                                      

________________________________________________________________________________________________________________________
script.multiply_sentence.0     @script.countwords             5 words                       
script.multiply_sentence.1     @script.countwords             7 words                       
script.multiply_sentence.2     @script.countwords             7 words                       
script.multiply_sentence.3     @script.countwords             21 words                      
script.multiply_sentence.4     @script.countwords             31 words                      
script.multiply_sentence.5     @script.countwords             31 words                      
script.multiply_sentence.6     @script.countwords             41 words                      
script.multiply_sentence.7     @script.countwords             61 words                      
script.multiply_sentence.8     @script.countwords             61 words                      

9/9 tests passed
```

Awesome! We've run a grid of tests over a grid of inputs, and measured some metric with
our custom decorators. See the [gridtest.yml](gridtest.yml)
for the full test recipe.

### Save to File

If we want to save the complete results, we can add `--save` with a filename:

```bash
$ gridtest test --save results.json
```

You can see the example [results.json](results.json) in this folder.
