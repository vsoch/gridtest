# These are functions in my script

from pokemon.master import get_pokemon, catch_em_all
import random


def get_pokemon_id():
    """Return a random pokemon id"""
    return random.choice(list(catch_em_all()))

def generate_numbers(count=10, length=10):
    """If you want to generate a list of lists of something with the intention
       to unwrap and parameterize it in another grid, you can return this list
       of lists and set unwrap to true.
    """
    lists = []
    for c in range(count):
        lists.append([random.choice(range(0,100))] * length)
    return lists

def dosum(numbers):
    """sum a list of numbers, an example run across generate_numbers"""
    return sum(numbers)

def generate_pokemon(pid):
    """Generate a pokemon based on a particular identifier. This is excessive
       because we could just use get_pokemon() to return a random pokemon, but
       we are taking in the pid (pokemon id) as an example for providing a function
       to generate input arguments for a gridtest.
    """
    print(pid)
    catch = get_pokemon(pid=pid)
    catch_id = list(catch.keys())[0]
    return catch[catch_id]["ascii"]


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
