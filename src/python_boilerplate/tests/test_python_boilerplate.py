import os
import tempfile
from collections import OrderedDict

import mock
import pytest
import six

from python_boilerplate import compat
from python_boilerplate import config as config_mod
from python_boilerplate.commands import InitJobConfig, InitJobWriter
from python_boilerplate.config import get_config, get_context


@pytest.yield_fixture
def tempdir():
    if six.PY3:
        tempdir = tempfile.TemporaryDirectory()
    else:
        tempdir = compat.TemporaryDirectory()
    oldpath = os.getcwd()

    with tempdir as path:
        os.chdir(path)
        try:
            yield path
        finally:
            os.chdir(oldpath)
        tempdir.cleanup()


@pytest.yield_fixture
def config(tempdir):
    yield get_config()
    config_mod.GLOBAL_CONFIG = None
    config_mod.CONFIG_DIR = None


@pytest.fixture
def context(config):
    return get_context()


@pytest.fixture
def project_config(config, project_options):
    return InitJobConfig(**project_options)


@pytest.fixture
def project_writer(project_config):
    return InitJobWriter(project_config)


@pytest.fixture
def project_options():
    return OrderedDict([
        ('project', 'test-project'),
        ('pyname', 'test_project'),
        ('author', 'some author'),
        ('email', 'foo@bar.com'),
        ('version', '0.1.0'),
        ('license', 'gpl'),
        ('has_script', 'yes'),
    ])


def mock_inputs(inputs):
    """
    Mock user input by using the values in the given list.
    """

    func_path = 'python_boilerplate.io.grab_input'
    return mock.patch(func_path, site_effect=inputs)


# Context
def test_default_config_context(context):
    context = {k: v for k, v in context.items() if v != ''}

    assert context == {
        'version': '0.1.0',
        'boilerplate_version': 1,
        'has_script': False,
        'license': 'mit',
        'python_version': 'both'
    }


def test_context_is_modified_by_config(config):
    config.set('options', 'project', 'foo-bar')
    config.set('options', 'pyname', 'foo_bar')
    ctx = config_mod.get_context(ham='spam')
    assert ctx['ham'] == 'spam'
    assert ctx['project'] == 'foo-bar'
    assert ctx['pyname'] == 'foo_bar'


# Global job
def _test_init_command_context(config):
    inputs = [
        'test-project',  # project name
        'some author',  # author
        'foo@bar.com',  # email
        '',  # pyname
        '',  # version
        '',  # license
        '',  # editor
        '',  # has_script
    ]
    with mock_inputs(inputs):
        cfg = InitJobConfig()
        cfg.run()
        ctx = get_context()

    assert ctx == {
        'project': 'test-project',
        'author': 'some author',
        'email': 'foo@bar.com',
        'pyname': 'test_project',
        'pyname_dashed': 'test-project',
        'version': '0.1.0',
        'license': 'gpl',
        'has_script': 'yes'
    }

# File creation
# def test_repeated_creation_of_project(job, jobdir):
#     with visit_dir(jobdir):
#         # Change file and revert
#         data = open('setup.py').read()
#         with open('setup.py', 'w') as F:
#             F.write('corrupted')
#
#         # Revert file and create backup
#         with mock_inputs(['']):
#             main(['init'])
#
#         with open('setup.py') as F:
#             assert F.read().strip() == data
#
#         # Check backup
#         assert os.path.exists('setup.py.bak')
#         os.unlink('setup.py.bak')
