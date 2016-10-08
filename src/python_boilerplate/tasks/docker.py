from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os

from invoke import task, run

from python_boilerplate.config import get_option
from python_boilerplate.tasks import util


@task
def clean(ctx):
    """
    Clean unused images and containers.
    """

    run('docker rm $(docker ps -a -q)')
    run('docker rmi $(docker images -q --filter dangling=true')
