
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

