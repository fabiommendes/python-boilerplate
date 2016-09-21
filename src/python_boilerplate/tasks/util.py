from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import sys


def add_src_to_python_path():
    """
    Adds the source directory to the Python path.
    """

    src = os.path.join(os.getcwd(), 'src')
    src = os.path.abspath(src)
    if src not in sys.path:
        sys.path.insert(0, src)


def setup_py(*args):
    """
    Execute a setup.py command with the given args
    """

    setup_path = os.path.join(os.getcwd(), 'setup.py')
    with open(setup_path) as F:
        setup_source = F.read()

    old_args = sys.argv
    try:
        sys.argv = ['setup.py'] + list(args)
        exec(setup_source, {
            '__file__': setup_path,
        })
    finally:
        sys.argv = old_args
