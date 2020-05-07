# These are functions in my script

from pokemon.master import get_pokemon, catch_em_all
import random


def get_pokemon_id():
    """Return a random pokemon id"""
    return random.choice(list(catch_em_all()))


def generate_pokemon(pid):
    """Generate a pokemon based on a particular identifier. This is excessive
       because we could just use get_pokemon() to return a random pokemon, but
       we are taking in the pid (pokemon id) as an example for providing a function
       to generate input arguments for a gridtest.
    """
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
