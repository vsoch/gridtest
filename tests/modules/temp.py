# Basic functions for testing custom functions in format {% tmp_path %}

import os


def write_file(filename):
    """write a file with some random nonsense"""
    with open(filename, "w") as filey:
        filey.write("I heard there was an octupus living in that Christmas tree.")


def create_directory(dirname):
    """create a directory named according to input variable dirname"""
    if not os.path.exists(dirname):
        os.mkdir(dirname)
