import sys
from invoke import run, task
from jarbas.tasks import *


@task
def configure(ctx):
    """
    Instructions for preparing package for development.
    """

    run("%s -m pip run .[dev] -r requirements.txt" % sys.executable)