import os

import mock
import pytest

from python_boilerplate.commands import InitJobWriter
from python_boilerplate.config import get_context
from python_boilerplate.tests.test_python_boilerplate import tempdir, config, \
    context, project_config, project_options
from python_boilerplate.utils import visit_dir


@pytest.yield_fixture(scope='session')
def gtempdir():
    temp = tempdir()
    yield next(temp)


@pytest.fixture(scope='session')
def gconfig(gtempdir):
    return config(gtempdir)


@pytest.fixture(scope='session')
def gcontext(gconfig):
    return context(gconfig)


@pytest.fixture(scope='session')
def gproject(gconfig):
    cfg = project_config(gconfig, project_options())
    base = 'python_boilerplate.io.'

    with mock.patch(base + 'grab_input', lambda x: ''):
        with mock.patch(base + 'show', lambda x: ''):
            cfg.ask_options()

    writer = InitJobWriter(cfg)
    with mock.patch(base + 'show', lambda x: ''):
        writer.run()
    return writer


def test_global_job_has_correct_context(gproject):
    context = {k: v for k, v in get_context().items() if v != ''}

    assert context == {
        'author': 'some author',
        'email': 'foo@bar.com',
        'project': 'test-project',
        'pyname': 'test_project',
        'package': 'test_project',
        'pyname_dashed': 'test-project',
        'version': '0.1.0',
        'boilerplate_version': 1,
        'has_script': False,
        'license': 'gpl',
        'python_version': 'both'
    }


def test_all_files_present_in_global_job(gproject, gtempdir):
    default_files = sorted([
        '.gitignore',
        '.travis.yml',
        '.coveragerc',
        'boilerplate.ini',
        'docs',
        'requirements.txt',
        'setup.py',
        'src',
        'tasks.py',
        'tox.ini',
        'LICENSE',
        'MANIFEST.in',
        'INSTALL.rst',
        'README.rst',
        'VERSION',
    ])
    with visit_dir(gtempdir):
        files = sorted(os.listdir(os.getcwd()))
        assert files
        assert files == default_files


def test_readme_file(gproject, gtempdir):
    with visit_dir(gtempdir):
        with open('VERSION') as F:
            assert F.read() == '0.1.0'
