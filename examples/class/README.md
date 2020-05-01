# Class Testing

The example here [car.py](car.py) provides a script file with a simple class definition.
We can first generate a testing config for preview - if we use gridtest generate without
an output file, it will print to the screen:


```bash
$ gridtest generate car.py
Extracting Car from car
Extracting honk from car
Extracting lights from car
```
```yaml
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

We can then write to file:

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
  car.Car.honk:
  - args:
      self: "{{ instance.thisone }}"
  car.Car.switch_lights:
  - args:
      self: "{{ instance.thisone }}"
  filename: /home/vanessa/Desktop/Code/gridtest/examples/class/car.py
```

And then the instance of the Car named as instance "this one" (the second block)
will be used for those tests. This is a very basic usage for a class, and we 
expect more complex cases to be written up when they are determined.

