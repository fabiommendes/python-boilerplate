import sys
from invoke import run, task

# Import some boilerplate tasks (see http://... for references)
from python_boilerplate.tasks.default import *


@task
def configure(ctx):
    """
    Instructions for preparing package for development.
    """

    run("%s -m pip install .[dev] -r requirements.txt" % sys.executable)
