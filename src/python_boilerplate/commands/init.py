import os
import subprocess

from python_boilerplate.config import refresh_config, save_config
from python_boilerplate.core import ConfigManager, FileWriter
from python_boilerplate.utils import pyname, visit_dir
from python_boilerplate.commands import subparsers, register
license_alias = {
    'gpl': 'gpl3',
}


# Define Config/FileWriter classes
class InitProjectConfig(ConfigManager):
    """
    Config options for the `python-boilerplate init` command
    """

    def __init__(self, **kwargs):
        self._has_ini_file = not os.path.exists('boilerplate.ini')
        super().__init__('options', **kwargs)

    def run(self):
        require = self.require

        # Asks basic info
        project = require('project', "Project's name: ")
        require('author', "Author's name: ")
        require('email', "Author's email: ")
        require('pyname', "Python name: ", default=pyname(project))

        # Fetch version from existing VERSION file or asks the user
        if os.path.exists('VERSION'):
            self.version = open('VERSION').read().strip()
        else:
            self.version = require('version', "Version: ", default='0.1.0')

        # License
        require('license', 'License: ', default='gpl')

        # Save config file
        self.save()
        if self._has_ini_file:
            editor = input(
                '\nYour config file was saved as boilerplate.ini. Leave blank '
                'to continue or specify a text editor.\n'
                'Editor: '
            ).strip()

            if editor:
                subprocess.call([editor, 'boilerplate.ini'])
                refresh_config()


class InitProjectWriter(FileWriter):
    """
    File writer for the `python-boilerplate init` command
    """

    has_scripts = True

    def run(self, ignore=None):
        if ignore is False:
            ignore = not self.config._has_ini_file

        # Version and setup files
        self.write('VERSION.txt', 'VERSION', ignore=True)
        self.write('gitignore.txt', '.gitignore', ignore=ignore)

        # Readme
        self.write('README.rst', ignore=True)
        self.write('INSTALL.rst', ignore=ignore)

        # License
        license = license_alias.get(self.config.license, self.config.license)
        license_path = 'license/%s.txt' % license
        self.write(license_path, ignore=ignore, path='LICENSE')

        # Tasks
        self.write('tasks.pyt', 'tasks.py', ignore=ignore)

        # setup.py and friends
        self.write('setup.pyt', 'setup.py', ignore=ignore)
        self.write('MANIFEST.in', ignore=ignore)
        self.write('requirements.txt', ignore=ignore)
        self.write('requirements-dev.txt', ignore=ignore)

        # Package structure
        basedir = 'src/%s' % self.pyname
        self.write('package/init.pyt',
                   '%s/__init__.py' % basedir, ignore=True)
        self.write('package/meta.pyt',
                   '%s/__meta__.py' % basedir, ignore=ignore)
        if self.has_scripts:
            self.write('package/main.pyt',
                       '%s/__main__.py' % basedir, ignore=ignore)

        # Tests
        self.write('package/test_project.pyt',
                   '%s/tests/test_%s.py' % (basedir, self.pyname),
                   ignore=ignore)

        # Documentation
        self.write('docs/conf.pyt', 'docs/conf.py', ignore=ignore)
        self.write('docs/index.rst', ignore=ignore)
        self.write('docs/install.rst', ignore=ignore)
        self.write('docs/license.rst', ignore=ignore)
        self.write('docs/apidoc.rst', ignore=ignore)
        self.write('docs/warning.rst', ignore=ignore)
        self.write('docs/make.bat', ignore=True)
        self.write('docs/makefile.txt', 'docs/Makefile', ignore=True)

        # Make sphinx folders
        with visit_dir('docs'):
            for folder in ['_static', '_build', '_templates']:
                if not os.path.exists(folder):
                    os.mkdir(folder)

# Setup the "init" subparser
cmd = subparsers.add_parser('init', help='create a new project')
cmd.add_argument('project', nargs='?', help='Your Python Boilerplate project\' name')
cmd.add_argument('--author', '-a', help='author\'s name')
cmd.add_argument('--email', '-e', help='author\'s e-mail')
cmd.add_argument('--license', '-l', help='project\'s license')
cmd.add_argument('--version', '-v', help='project\'s version')
register(cmd, InitProjectConfig, InitProjectWriter)
