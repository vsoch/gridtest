# Grid Function

This is a derivative of the [custom-decorator](../custom-decorator)
example, except we derive inputs for the grid from a custom function.

### Create your Functions

Originally we started with functions to take some text input and parse it 
(`multiply_sentences`).

```python
# These are functions in my script

def multiply_sentence(sentence, count):
    return sentence * count
```

But since we want to test having a function generate inputs for our test function,
let's change this up a bit. Instead of generating a sentence of some length,
let's return the ascii characters for a pokemon. The input that we need for the
function below is the pokemon id (pid).

```python
# These are functions in my script

from pokemon.master import get_pokemon, catch_em_all

def generate_pokemon(pid):
    """Generate a pokemon based on a particular identifier. This is excessive
       because we could just use get_pokemon() to return a random pokemon, but
       we are taking in the pid (pokemon id) as an example for providing a function
       to generate input arguments for a gridtest.
    """
    catch = get_pokemon(pid=pid)
    catch_id = list(catch.keys())[0]
    return catch[catch_id]['ascii']
```

How will we generate that?

### Create your Yaml

Remember that for the example in the [custom-decorator](../custom-decorator), 
we just provide a list of sentences in our grid:

```yaml
  script.multiply_sentence:
  - metrics:
    - '@script.countwords'
    grid:
      count:
        list: [1, 5, 10]
      sentence:
        list:
          - "He ran for the hills."
          - "Skiddery-a rinky dinky dinky, skittery rinky doo."
          - "You are my sunshine, my only sunshine."
```

This seems reasonable for a dummy example, or small set of inputs, but likely 
isn't reasonable if we want to more programatically generated inputs.
For example, for our current pokemon function we would need to hard
code a specific set of ids (as a list)


```
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  tests:
    script.generate_pokemon:
    - metrics:
      - '@script.countwords'
      grid:
        pid: 
          list: [1, 2, 3]
```

or some range:

```
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  tests:
    script.generate_pokemon:
      grid:
        pid: 
          min: 1
          max: 3
```

What we really want to do is write a function that randomly generates pokemon ids for us.
Let's create another function that we want to run many times to generate
pokemon ids for this function:

```python
def get_pokemon_id():
    """Return a random pokemon id"""
    return random.choice(list(catch_em_all()), 1)
```

A more realistic use case would be having some numerical optimization function
that requires a distribution (an array of numbers) to be generated for some input.
We'd want to generate that array with a function over some grid of parameters.

### Add a grid

We basically need to point the parameter "pid" to be generated from the function. What
does that look like? First we need to add the function under "grids" - a grid
is a general parameterization that can be used to populate sections of your testing
file. We will give it a name, generate_pids for "generate pokemon ids."

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  grids:
    generate_pids:
      func: script.get_pokemon_id    
  tests:
    script.generate_pokemon:
...
```

The function doesn't have any input arguments, so we can just specify it's name
under the "func" key, and a count for the number of times we want it run. 
If we had another grid of arguments to run that function
over, we would define them in a grid just as we are used to for a test. Then we
need to specify our generate_pokemon function to use it:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  grids:
    generate_pids:
      func: script.get_pokemon_id
      count: 10     

  tests:
    script.generate_pokemon:
      grid:
        pid: generate_pids
```

The above says that "for the script.generate_pokemon test, generate the "pid"
variable from "generate_pids", which is a function that should run 10 times."

### Add a Metric

Finally, let's create a metric to simply take the ascii (the result of `generate_pokemon`
and count the number of unique characters:

```python
def uniquechars(func):
    """this is a simple example of a custom decorator - We run the generate
       pokemon function and print the number of unique characters in the ascii.
    """
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        chars = len(set(result))
        print(f"@script.uniquechars {chars} unique chars")
        return result

    return wrapper
```

The final template (with the metric) looks like this:

```yaml
script:
  filename: /home/vanessa/Desktop/Code/gridtest/examples/grid-function/script.py
  grids:
    generate_pids:
      func: script.get_pokemon_id
      count: 10

  tests:
    script.generate_pokemon:
      - metrics:
          - "@script.uniquechars"
        grid:
          pid: generate_pids
```

### Running Tests

Let's run the tests! We should see a count of unique characters for each pokemon generated:

```bash
$ gridtest test
[10/10] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
script.generate_pokemon.0      success                                                      
script.generate_pokemon.1      success                                                      
script.generate_pokemon.2      success                                                      
script.generate_pokemon.3      success                                                      
script.generate_pokemon.4      success                                                      
script.generate_pokemon.5      success                                                      
script.generate_pokemon.6      success                                                      
script.generate_pokemon.7      success                                                      
script.generate_pokemon.8      success                                                      
script.generate_pokemon.9      success                                                      

________________________________________________________________________________________________________________________
script.generate_pokemon.0      @script.uniquechars            11 unique chars               
script.generate_pokemon.1      @script.uniquechars            11 unique chars               
script.generate_pokemon.2      @script.uniquechars            11 unique chars               
script.generate_pokemon.3      @script.uniquechars            11 unique chars               
script.generate_pokemon.4      @script.uniquechars            11 unique chars               
script.generate_pokemon.5      @script.uniquechars            11 unique chars               
script.generate_pokemon.6      @script.uniquechars            11 unique chars               
script.generate_pokemon.7      @script.uniquechars            11 unique chars               
script.generate_pokemon.8      @script.uniquechars            11 unique chars               
script.generate_pokemon.9      @script.uniquechars            11 unique chars               

10/10 tests passed
```

Spoiler alert - they all use the same characters! Notice that we've also successfully
run the unique id generator function 10 times to result in 10 tests.
See the [gridtest.yml](gridtest.yml) for the full test recipe.

### Save to File

If we want to save the complete results, we can add `--save` with a filename:

```bash
$ gridtest test --save results.json
```

You can see the example [results.json](results.json) in this folder, and notice
how the result of each run is the ascii for a complete pokemon (that would
render nicely if printed to the screen).
