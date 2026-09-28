from ...modules import Module


@Module.from_function(
    suggestions=['pytest'],
)
def setuptools(ask, actions):
    """
    Create a basic python package structure based on setuptools.
    """
    ask.print()


BANNER = """Hello! Let us create a Python package structure for your project.

Python packaging is organized around the setup.py and setup.cfg files.
I
Is your project composed of a single module or do you want to grow it into
    a package? Module-based projects consists of single Python files and are
    recommended only for very simple cases.


You may go to https://jarbas.rtfd.org/latest/python-package/ for more info.
"""

class Package(Job):
    """

    = Do you want to convert your project into a package project? [is_package=bool:True]

    We moved everything to the src/{{ base.package }} folder. We also created an
    empty __init__.py, to make Python recognize {{ base.package }} as a package
    and a __main__.py file. This script is execute whenever you execute ``python -m <some-module>``.

    This is a nice way to expose your project's functionality and Python uses it
    a lot. (Check, e.g., ``python -m http.server`` or ``python -m pip`` commands.)
    """
