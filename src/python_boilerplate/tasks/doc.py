from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import

import os

from invoke import task, run

from python_boilerplate.config import get_option
from python_boilerplate.tasks import util


@task
def doc_build(ctx, show=True, browser=''):
    """
    Builds documentation.
    """

    util.add_src_to_python_path()
    util.setup_py('build_sphinx')

    if show:
        path = os.path.join('build', 'sphinx', 'html', 'index.html')
        if not browser:
             browser = default_browser()
        run('%s %s' % (browser, path))


@task
def doc_upload(ctx, build=True):
    """
    Upload documentation to PyPI.
    """

    # Build documentation first
    if build:
        doc_build(ctx, show=False)
    path = os.path.join('build', 'sphinx', 'html')
    run('python2 setup.py upload_docs --upload-dir %s' % path)


def default_browser():
    """
    Return the name of the default Browser for this system.
    """

    return 'firefox'