from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import subprocess

from python_boilerplate import io
from python_boilerplate.commands import subparsers, register
from python_boilerplate.config import refresh_config
from python_boilerplate.core import JobConfig, JobWriter
from python_boilerplate.utils import pyname, visit_dir

license_alias = {
    'gpl': 'gpl3',
}


# Define Config/FileWriter classes
class InitJobConfig(JobConfig):
    """
    Config options for the `python-boilerplate init` command
    """

    def __init__(self, **kwargs):
        self._has_ini_file = not os.path.exists('boilerplate.ini')
        JobConfig.__init__(self, 'options', **kwargs)

    def ask_options(self):
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

        # Scripts
        require('has_script', 'Has scripts? ', default='False', action='yn')

        # Save config file
        self.save()
        if self._has_ini_file:
            io.show(
                '\nYour config file was saved as boilerplate.ini. Leave blank '
                'to continue or specify a text editor.'
            )
            editor = io.grab_input('Editor: ').strip()

            if editor:
                subprocess.call([editor, 'boilerplate.ini'])
                refresh_config()


class InitJobWriter(JobWriter):
    """
    File writer for the `python-boilerplate init` command
    """

    has_scripts = True

    def __init__(self, config):
        super(InitJobWriter, self).__init__(config, {
            'requirements': '',
        })

    def get_context(self, **kwargs):
        if isinstance(self.has_scripts, str):
            self.has_scripts = self.has_scripts.lower() == 'yes'
        return JobWriter.get_context(self, has_scripts=self.has_scripts, **kwargs)

    def run(self, ignore=None):
        if ignore is False:
            ignore = not self.config._has_ini_file

        # Version and setup files
        self.write('VERSION.txt', 'VERSION')
        self.write('gitignore.txt', '.gitignore')

        # Readme
        self.write('README.rst')
        self.write('INSTALL.rst')

        # License
        license = license_alias.get(self.config.license, self.config.license)
        license_path = 'license/%s.txt' % license
        self.write(license_path, ignore=ignore, path='LICENSE')

        # Best practices and configurations
        self.write('tox.ini')
        self.write('travis.yml', '.travis.yml')
        self.write('coveragerc.txt', '.coveragerc')

        # Tasks
        self.write('tasks.pyt', 'tasks.py', ignore=ignore)

        # setup.py and friends
        self.write('setup.pyt', 'setup.py', ignore=ignore)
        self.write('MANIFEST.in')
        self.write('requirements.txt')

        # Package structure
        basedir = 'src/%s' % self.pyname
        self.write('package/init.pyt', '%s/__init__.py' % basedir)
        self.write('package/main.pyt', '%s/__main__.py' % basedir)
        self.write('package/meta.pyt', '%s/__meta__.py' % basedir)

        # Tests
        test_dir = '%s/tests/' % basedir
        self.write('package/test_init.pyt', test_dir + '__init__.py')
        self.write('package/test_main.pyt', test_dir + '__main__.py')
        self.write('package/test_project.pyt',
                   test_dir + 'test_%s.py' % self.pyname)
        self.write('package/test_documentation.pyt',
                   test_dir + 'test_documentation.py')

        # Documentation
        self.write('docs/conf.pyt', 'docs/conf.py')
        self.write('docs/apidoc.rst')
        self.write('docs/faq.rst')
        self.write('docs/index.rst')
        self.write('docs/install.rst')
        self.write('docs/license.rst')
        self.write('docs/warning.rst')
        self.write('docs/make.bat')
        self.write('docs/makefile.txt', 'docs/Makefile')

        # Make sphinx folders
        with visit_dir('docs'):
            for folder in ['_static', '_build', '_templates']:
                if not os.path.exists(folder):
                    os.mkdir(folder)


# Setup the "init" subparser
cmd = subparsers.add_parser('init', help='create a new project')
cmd.add_argument('project', nargs='?',
                 help='Your Python Boilerplate project\' name')
cmd.add_argument('--author', '-a', help='author\'s name')
cmd.add_argument('--email', '-e', help='author\'s e-mail')
cmd.add_argument('--license', '-l', help='project\'s license')
cmd.add_argument('--version', '-v', help='project\'s version')
register(cmd, InitJobConfig, InitJobWriter)
