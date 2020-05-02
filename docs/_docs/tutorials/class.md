---
title: Class Tutorial
category: Tutorials
permalink: /tutorials/class/index.html
order: 5
---

## Classes

If you haven't [installed]({{ site.baseurl }}/install/) gridtest, you should do this first.

### Write Functions

Let's say we start with these functions, and save them to a file called car.py

```python
# Example car class to run tests for

valid_colors = ["red", "black", "white", "blue"]

# An example of raising a custom exception
class ColorException(Exception):
    pass

class WheelsException(Exception):
    pass


class Car:

    def __init__(self, wheels:int=4, color:str="red", lights:bool=False):
        """a new car must have an even number of wheels, and be a valid color
        """
        if color not in valid_colors:
            raise ColorException
        if wheels % 2 != 0:
            raise WheelsException
        self.wheels = wheels
        self.color = color
        self.lights = lights

    def __str__(self):
        return (f"[car][wheels:{self.wheels}][color:{self.color}]")
    def __repr__(self):
        return self.__str__()

    def honk(self):
        print("Honk, Honk!")

    @property
    def axels(self) -> int:
        return int(wheels/2)

    def switch_lights(self) -> bool:
        self.lights = not self.lights
```

We can first generate a testing config for preview - if we use gridtest generate without
an output file, it will print to the screen:


```bash
$ gridtest generate car.py
Extracting Car from car
Extracting honk from car
Extracting lights from car

car:
  car.Car:
  - args:
      color: red
      lights: false
      wheels: 4
  car.Car.honk:
  - args:
      self: null
  car.Car.lights:
  - args:
      self: null
  filename: /home/vanessa/Desktop/Code/gridtest/examples/class/car.py
```

We can then write to file, and we'll use the default name that gridtest can easily discover.

```bash
$ gridtest generate car.py gridtest.yml
```

Notice that we would want to be able to define an instance of a class to be
used for the subsequent testing functions of the class. To do this, take the 
section you want to use, for example this one:


```yaml
  car.Car:
  - args:
      color: red
      lights: false
      wheels: 4
```

and add an "instance" key to it.


```yaml
  car.Car:
  - instance: thisone
    args:
      color: red
      lights: false
      wheels: 4
```


We now want to reference "thisone" as the instance to
use. Just update the "self" variable in each of the class test cases.

```yaml
car:
  car.Car:
  - args:
      color: notacolor
      lights: false
      wheels: 4
    raises: ColorException
  - instance: thisone
    args:
      color: red
      lights: false
      wheels: 4
    isinstance: car.Car 
  car.Car.honk:
  - args:
      self: "{% raw %}{{ instance.thisone }}{% endraw %}"
  car.Car.switch_lights:
  - args:
      self: "{% raw %}{{ instance.thisone }}{% endraw %}"
  filename: /home/vanessa/Desktop/Code/gridtest/examples/class/car.py
```

And then the instance of the Car named as instance "this one" (the second block)
will be used for those tests. This is a very basic usage for a class, and we 
expect more complex cases to be written up when they are determined.

### Testing

Now, we can run tests! Since we've named the testing file `gridtest.yml` we can
just run:

```bash
$ gridtest test
[4/4] |===================================| 100.0% 
success: car.Car.0 raises ColorException 
success: car.Car.1 isinstance car.Car
success: car.Car.honk.0 
success: car.Car.switch_lights.0 
4/4 tests passed
```

You might next want to browse other [tutorials]({{ site.baseurl }}/tutorials/) available.
