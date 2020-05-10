# These are functions in my script
# Typing is here, so Python


def add(one, two):
    """add will add two numbers, one and two. There is no typing here"""
    return one + two


def add_with_type(one: int, two: int) -> int:
    """add_with_type will add two numbers, one and two, with typing for ints."""
    return one + two


def hello(name):
    """print hello to a name, with no typing"""
    print(f"hello {name}!")


def hello_with_default(name="Dinosaur"):
    """print hello to a name with a default"""
    print(f"hello {name}!")


def hello_with_type(name: str) -> None:
    """print hello to a name, with typing"""
    print(f"hello {name}!")
