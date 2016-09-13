import sys
from invoke import run, task
from python_boilerplate.tasks import *


@task
def configure(ctx):
    """
    Instructions for preparing package for development.
    """

    run("%s -m pip install .[dev] -r requirements.txt" % sys.executable)