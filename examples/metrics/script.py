# These are functions in my script
# Typing is here, so Python

from time import sleep


def add(one, two):
    """add will add two numbers, one and two. There is no typing here"""
    return one + two


def gotosleep(seconds):
    """sleep for whatever specified number of seconds are provided"""
    sleep(seconds)


def add_with_type(one: int, two: int) -> int:
    """add_with_type will add two numbers, one and two, with typing for ints."""
    return one + two
