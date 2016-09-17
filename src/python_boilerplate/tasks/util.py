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
        sys.path.append(src)
