import os
import string
from contextlib import contextmanager

from unidecode import unidecode


def python_name(name):
    """
    Converts a string of text into a valid python name.
    """

    name = unidecode(name.strip().lower())
    valid = string.ascii_letters + string.digits + '_'
    char_list = []
    for i, char in enumerate(name):
        if char in valid:
            char_list.append(char)
        elif char in '- \t\n':
            char_list.append('_')

    # Join characters and take precautions against weird names
    name = ''.join(char_list)
    if not name:
        return 'project'
    elif name[0].isdigit():
        return '_' + name
    else:
        return name


@contextmanager
def visit_dir(path):
    """
    Visit directory and come back after the with block is finish.
    """

    current_dir = os.getcwd()

    try:
        if isinstance(path, str):
            os.chdir(path)
        else:
            os.chdir(path.getsyspath('/'))
        yield os.getcwd()
    finally:
        os.chdir(current_dir)


@contextmanager
def temp_dir(path, name='.tmp', keep=False):
    """
    Create a temporary sub-directory within the given path and clean it
    afterwards.
    """