---
title: Sample Grid Tutorial
category: Tutorials
permalink: /tutorials/samplegrid/index.html
order: 7
---

Gridtest can easily be used to generate random samplies for some number of inputs,
where each input is returned via a function as a list of options to select from.

## Write your Functions

Let's start by writing a set of functions. Each of these will return a list
of attributes that we might want to parameterize. For our first example,
we will generate cohorts with all possible combinations. Let's create functions
to return colors, ages, shapes, and animals.

```python
# Example functions to generate lists to parameterize

import colorsys
import random

def generate_rgb_color():
    """return a randomly selected color
    """
    N = int(random.choice(range(0,100)))
    HSV_tuple = (N*1.0/N, 0.5, 0.5)
    return colorsys.hsv_to_rgb(*HSV_tuple)

def generate_shape():
    return random.choice(["square", "triangle", "circle", "ellipsis", "rectangle", "octagon"])
        

def generate_age():
    return random.choice(range(0,100))

def generate_animal():
    return random.choice(["dog", "cat", "bird", "cow", "chicken"])
```

It's fairly simple - each one spits out a random value. You could also
imagine loading data from some other source.

## Generate the Grids

We next want to generate grids for each! This is fairly simple to do too -
each grid is named based on what it selects, and uses the appropriate function
to be run:

```yaml
script:
  grids:

    # Each grid below generates one randomly selected value
    select_color:
      functions:
        color: script.generate_rgb_color

    select_shape:
      functions:
        shape: script.generate_shape

    select_animal:
      functions:
        animal: script.generate_animal

    select_age:
      functions:
        age: script.generate_age
```

We can also verify that each one generates what we would expect with `gridview`:

```bash
$ gridtest gridview cohort-grids.yml select_color
{'color': (0.5, 0.25, 0.25)}

$ gridtest gridview cohort-grids.yml select_animal
{'animal': 'bird'}

$ gridtest gridview cohort-grids.yml select_age
{'age': 47}

$ gridtest gridview cohort-grids.yml select_shape
{'shape': 'triangle'}
```

But that's not very interesting! Let's instead create a full set of data
for a single sample of a cohort:

```yaml
    generate_cohort:
      functions:
        age: script.generate_age
        animal: script.generate_animal
        shape: script.generate_shape
        color: script.generate_rgb_color
```

and generate it:

```yaml
$ gridtest gridview cohort-grids.yml generate_cohort
{'age': 54, 'animal': 'dog', 'shape': 'ellipsis', 'color': (0.5, 0.25, 0.25)}
```

We could run it again to get a different result, but why not just add a
count for the number of samples that we need?

```yaml
    generate_cohort:
      count: 10
      functions:
        age: script.generate_age
        animal: script.generate_animal
        shape: script.generate_shape
        color: script.generate_rgb_color
```

```bash
{'age': 71, 'animal': 'dog', 'shape': 'triangle', 'color': (0.5, 0.25, 0.25)}
{'age': 18, 'animal': 'bird', 'shape': 'circle', 'color': (0.5, 0.25, 0.25)}
{'age': 17, 'animal': 'bird', 'shape': 'square', 'color': (0.5, 0.25, 0.25)}
{'age': 24, 'animal': 'chicken', 'shape': 'rectangle', 'color': (0.5, 0.25, 0.25)}
{'age': 14, 'animal': 'bird', 'shape': 'octagon', 'color': (0.5, 0.25, 0.25)}
{'age': 82, 'animal': 'cow', 'shape': 'square', 'color': (0.5, 0.25, 0.25)}
{'age': 4, 'animal': 'cat', 'shape': 'rectangle', 'color': (0.5, 0.25, 0.25)}
{'age': 55, 'animal': 'cat', 'shape': 'square', 'color': (0.5, 0.25, 0.25)}
{'age': 48, 'animal': 'bird', 'shape': 'square', 'color': (0.5, 0.25, 0.25)}
{'age': 84, 'animal': 'chicken', 'shape': 'triangle', 'color': (0.5, 0.25, 0.25)}
```

We can see that we have ten results:

```bash
$ gridtest gridview cohort-grids.yml generate_cohort --count
10 argument sets produced.
```

Great! Let's save this to file. We don't need gridtest anymore, we can just keep
our parameters for use.

```bash
$ gridtest gridview cohort-grids.yml generate_cohort --export samples.json
```

The results are saved to json.

```json
[
    {
        "age": 88,
        "animal": "bird",
        "shape": "ellipsis",
        "color": [
            0.5,
            0.25,
            0.25
        ]
    },
    {
        "age": 94,
        "animal": "cat",
        "shape": "rectangle",
        "color": [
            0.5,
            0.25,
            0.25
        ]
    },
...
]
```

## Combination Grids

The above works, but it calls the same functions many times. We would do much
better to, for some number of samples that we need, run each function once with
that number (returning a list of lists) and then unwrap it into a grid. For this
first example, we want all possible combinations of the parameters. Let's again
write our functions, and this time, we return a list:

```python
def generate_rgb_color(N=10):
    return generate_rgb_color() * N

def generate_shapes(N):
    return generate_shape() * N
        
def generate_ages(N=10):
    return generate_age() * N

def generate_animals(N=10):
    return generate_animal() * N
```

We can now use "unwrap" to make sure that each argument is represented on its own.
This way, we can parameterize them each over a larger grid. We can check to see this
in the output:

```bash
$ gridtest gridview grids.yml select_shapes
{'shapes': ['octagon']}
{'shapes': ['circle']}
{'shapes': ['rectangle']}
{'shapes': ['square']}
{'shapes': ['square']}
{'shapes': ['rectangle']}
{'shapes': ['ellipsis']}
{'shapes': ['octagon']}
{'shapes': ['ellipsis']}
{'shapes': ['rectangle']}

$ gridtest gridview grids.yml select_colors
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}
{'colors': (0.5, 0.25, 0.25)}

$ gridtest gridview grids.yml select_ages
{'ages': [59]}
{'ages': [44]}
{'ages': [52]}
{'ages': [78]}
{'ages': [78]}
{'ages': [12]}
{'ages': [82]}
{'ages': [40]}
{'ages': [64]}
{'ages': [66]}

$ gridtest gridview grids.yml select_animals
{'animals': ['chicken']}
{'animals': ['cow']}
{'animals': ['cat']}
{'animals': ['chicken']}
{'animals': ['cow']}
{'animals': ['cow']}
{'animals': ['cat']}
{'animals': ['dog']}
{'animals': ['chicken']}
{'animals': ['cow']}
```

Finally, let's make our grid that will generate many combinations of each. Just
a heads up ... it's every possible combination, so we will have 10 x 10 x 10 x 10...
10,000!

```bash
$ gridtest gridview grids.yml generate_cohort --count
10000 argument sets produced.
```
```bash
$ gridtest gridview grids.yml generate_cohort --count
...
{'age': [56], 'animal': ['cow'], 'shape': ['octagon'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['octagon'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['octagon'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['circle'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
{'age': [56], 'animal': ['cow'], 'shape': ['ellipsis'], 'color': (0.5, 0.25, 0.25)}
```

And you could save this to file again:

```bash
$ gridtest gridview grids.yml generate_cohort --save combinations.json
```

## Overview

Hopefully you can see the two use cases here - the first is to generate a
specific set of samples, given some input functions that generate values.
The second is to produce all possible combinations, and we take
advantage of unwrapping lists. For this dummy example, we are actually
calling the same function many times for the generation of lists of lists.
However, you could imagine having a single computationally intensive function
or maybe an API call that generates a list that you want to use the items
across another grid. You can see all files for these grids and scripts
in the repository [here](https://github.com/vsoch/gridtest/tree/master/examples/sample-grid).

You might next want to browse other [tutorials]({{ site.baseurl }}/tutorials/) available.
