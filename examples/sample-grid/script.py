# Example functions to generate lists to parameterize

import colorsys
import random


def generate_rgb_color():
    """return a randomly selected color
    """
    N = int(random.choice(range(1, 100)))
    HSV_tuple = (N * 1.0 / N, 0.5, 0.5)
    return colorsys.hsv_to_rgb(*HSV_tuple)


def generate_shape():
    return random.choice(
        ["square", "triangle", "circle", "ellipsis", "rectangle", "octagon"]
    )


def generate_age():
    return random.choice(range(0, 100))


def generate_animal():
    return random.choice(["dog", "cat", "bird", "cow", "chicken"])


## These are the same functions, but will return a list of length N
def generate_rgb_colors(N=10):
    return [generate_rgb_color() for x in range(N)]


def generate_shapes(N=10):
    return [generate_shape() for x in range(N)]


def generate_ages(N=10):
    return [generate_age() for x in range(N)]


def generate_animals(N=10):
    return [generate_animal() for x in range(N)]
