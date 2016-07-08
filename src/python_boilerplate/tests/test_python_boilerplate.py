import os
import tempfile
from collections import OrderedDict

import mock
import pytest

from python_boilerplate import config as config_mod
from python_boilerplate.config import get_config, get_context
from python_boilerplate.commands import InitProjectConfig, InitProjectWriter
from python_boilerplate.__main__ import main
from python_boilerplate.utils import visit_dir


@pytest.yield_fixture
def tempdir():
    tempdir = tempfile.TemporaryDirectory()
    oldpath = os.getcwd()
    with tempdir as path:
        os.chdir(path)
        try:
            yield path
        finally:
            os.chdir(oldpath)
        tempdir.cleanup()


@pytest.yield_fixture(scope='session')
def jobdir():
    yield from tempdir()


@pytest.yield_fixture
def config(tempdir):
    yield get_config()
    config_mod.GLOBAL_CONFIG = None


@pytest.fixture
def context(config):
    return get_context()


@pytest.fixture
def init_config(config, project_options):
    return InitProjectConfig(**project_options)


@pytest.fixture
def project_options():
    return OrderedDict([
        ('project', 'test-project'),
        ('pyname', 'test_project'),
        ('author', 'some author'),
        ('email', 'foo@bar.com'),
        ('version', '0.1.0'),
        ('license', 'gpl'),
    ])


@pytest.fixture(scope='session')
def job(jobdir):
    inputs = list(project_options().values())
    inputs.append('')  # skip editor
    del inputs[0]

    with mock.patch('builtins.input', side_effect=inputs):
        main(['init', 'test-project'])



#
# Context
#
def test_default_config_context(context, project_options):
    ctx = {k: '' for k in project_options}
    ctx['pyname_dashed'] = ''


def test_modified_context(config):
    config.set('options', 'project', 'foo-bar')
    config.set('options', 'pyname', 'foo_bar')
    ctx = config_mod.get_context(ham='spam')
    assert ctx['ham'] == 'spam'
    assert ctx['project'] == 'foo-bar'
    assert ctx['pyname'] == 'foo_bar'


def test_init_command_context(config):
    inputs = [
        'test-project',  # project name
        'some author',   # author
        'foo@bar.com',   # email
        '',              # pyname
        '',              # version
        '',              # license
        '',              # editor
    ]
    with mock.patch('builtins.input', side_effect=inputs):
        cfg = InitProjectConfig()
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
    }


#
# File creation
#
def test_create_files(init_config):
    writer = InitProjectWriter(init_config)
    writer.run()


#
# Main function
#
def test_files_were_created(job, jobdir):
    with visit_dir(jobdir):
        default_files = {
            'boilerplate.ini',
            '.gitignore',
            'docs',
            'src',
            'requirements-dev.txt',
            'requirements.txt',
            'setup.py',
            'tasks.py',
            'LICENSE',
            'MANIFEST.in',
            'INSTALL.rst',
            'README.rst',
            'VERSION',
        }
        assert set(os.listdir(os.getcwd())) == default_files


def test_creted_file_contents(job, jobdir):
    with visit_dir(jobdir):
        with open('VERSION') as F:
            assert F.read() == '0.1.0'


def test_repeated_creation_of_project(job, jobdir):
    with visit_dir(jobdir):
        # Change file and revert
        data = open('setup.py').read()
        with open('setup.py', 'w') as F:
            F.write('corrupted')

        # Revert file and create backup
        with mock.patch('builtins.input', return_value=''):
            main(['init'])

        with open('setup.py') as F:
            assert F.read().strip() == data

        # Check backup
        assert os.path.exists('setup.py.bak')
        os.unlink('setup.py.bak')