import os
import hashlib
import codecs
import configparser
import datetime
import subprocess
import string
from contextlib import contextmanager
import unidecode
import jinja2
from python_boilerplate.inputs import *

__all__ = ['make_new']
basedir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(basedir))
license_alias = {
    'gpl': 'gpl3',
}


def pyname(name):
    """
    Converts a string of text into a valid python name.
    """

    name = unidecode.unidecode(name.strip().lower())
    valid = string.ascii_letters + string.digits + '_'
    char_list = []
    for i, char in enumerate(name):
        if char in valid:
            char_list.append(char)
        elif char in '- \t\n':
            char_list.append('_')

    # Join characters and take precautions against weird names
    name = ''.join(char_list)
    if not name:
        return 'project'
    elif name[0].isdigit():
        return 'py' + name
    else:
        return name


def write_template(template: str, namespace=None, ignore=False, path=None,
                   verbose=True, hash=None):
    """
    Render jinja template with the given namespace and saves it in the
    desired path
    """

    if path is None:
        path = template

    template = jinja_env.get_template(template)
    data = template.render(**(namespace or {}))

    if os.path.exists(path) and ignore:
        return
    elif os.path.exists(path):
        with open(path) as F:
            file_data = F.read()
            if file_data == data:
                return

        # If hash is compatible with given hash, we simply overwrite
        ask = True
        if hash:
            file_hash = hashlib.md5(file_data.encode('utf8')).digest()
            file_hash = codecs.encode(file_hash, 'base64').decode()
            if hash == file_hash:
                os.rename(path, path + '.bak')
                ask = False

        if ask:
            msg = 'File %r exists. Save backup and overwrite?' % path
            response = yn_input(msg)
            if response == 'yes':
                os.rename(path, path + '.bak')
            else:
                return

    if verbose:
        print('    creating %s...' % os.path.abspath(path))

    with open(path, 'w') as F:
        F.write(data)

    return data


@contextmanager
def visit_dir(path):
    """Visit directory and come back after the with block is finish."""

    current_dir = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(current_dir)


class BoilerplateConfig(configparser.ConfigParser):
    """A ConfigParser specialized in boilerplate.ini."""

    valid_attrs = ['project', 'author', 'email', 'version', 'license']

    def __init__(self, *args, **kwds):
        super().__init__(*args, **kwds)
        self.optionxform = str

        if os.path.exists('boilerplate.ini'):
            with open('boilerplate.ini') as F:
                self.read_file(F)

        # Create sessions
        if 'options' not in self:
            self.add_section('options')

        if 'file hashes' not in self:
            self.add_section('file hashes')

    def register_file(self, filename, data):
        """Compute and register the hash value for some file given its textual
        data."""

        file_hash = hashlib.md5(data.encode('utf8')).digest()
        file_hash = codecs.encode(file_hash, 'base64').decode()
        self.set('file hashes', filename, file_hash)

    def save(self):
        """Saves content to boilerplate.ini."""

        with open('boilerplate.ini', 'w') as F:
            self.write(F)


# noinspection PyAttributeOutsideInit
class ProjectFactory:
    """A new project job.

    Interacts with the user and keeps a common namespace for all sub-routines
    """
    def __init__(self, **kwds):
        self.basepath = os.getcwd()
        self.basepath_len = len(self.basepath)
        self.config = BoilerplateConfig()

        # Save values and use the default config
        for attr in BoilerplateConfig.valid_attrs:
            value = kwds.pop(attr, None)
            if value is None:
                value = self.config.get('options', attr, fallback=None)
            setattr(self, attr, value)

        if kwds:
            raise TypeError('invalid attribute: %s' % kwds.popitem()[0])

        # This is the project name as a valid python name
        self.pyname = self.project and pyname(self.project)

    def write_template(self, template, ignore=False, path=None):
        base = os.getcwd()
        file = os.path.join(base, path or template)
        file = file[self.basepath_len + 1:]

        # Prepare namespace
        namespace = vars(self).copy()
        del namespace['config']
        del namespace['basepath']
        del namespace['basepath_len']
        namespace['job'] = self
        namespace['date'] = datetime.datetime.now()
        namespace['dashed_pyname'] = self.pyname.replace('_', '-')

        # Write data and fetch hash
        data = write_template(template, namespace, ignore=ignore, path=path)
        if data is not None:
            self.config.register_file(file, data)

    def update(self, **kwargs):
        for arg, value in kwargs.items():
            if arg not in BoilerplateConfig.valid_attrs:
                raise AttributeError('invalid attribute: %r' % arg)
            setattr(self, arg, value)

    #
    # New project and new sections
    #
    def new_project(self, ask_editor=None):
        # Asks basic info
        if self.project is None:
            self.project = input("Project's name: ")
        if self.author is None:
            self.author = input("Author's name: ")
        if self.email is None:
            self.email = input("Author's email: ")
        if not self.pyname:
            self.pyname = default_input("Python name: ", pyname(self.project))

        # Fetch version from existing VERSION file or asks the user
        if self.version is None and os.path.exists('VERSION'):
            self.version = open('VERSION').read().strip()
        self.version = self.version or default_input("Version: ", '0.1.0')

        # Ask other input
        self.license = self.license or default_input('License: ', 'gpl')

        # Save config file
        if ask_editor is None:
            ask_editor = not os.path.exists('boilerplate.ini')

        self.save_config()
        if ask_editor:
            print('Your config file was saved as boilerplate.ini. You can '
                  'review  this file before proceeding. Please tell your '
                  'favorite editor or leave blank to continue.')
            editor = input('Editor: ').strip()
            if editor:
                subprocess.call([editor, 'boilerplate.ini'])
                self.__init__()
                return self.new_project(ask_editor=False)

        # Make each part of the source tree
        self.make_base(ignore=False)
        self.make_setup_py(ignore=False)
        self.make_package(ignore=False)
        self.make_docs(ignore=False)
        self.make_license(ignore=False)
        self.make_invoke(ignore=False)
        self.save_config()

    def make_base(self, ignore=True):
        self.write_template('VERSION.txt', ignore=True, path='VERSION')
        self.write_template('gitignore.txt', ignore=ignore, path='.gitignore')

    def make_setup_py(self, ignore=True):
        self.write_template('setup.pyt', ignore=ignore, path='setup.py')
        self.write_template('MANIFEST.in', ignore=ignore)
        self.write_template('requirements.txt', ignore=ignore)
        self.write_template('requirements-dev.txt', ignore=ignore)

    def make_package(self, ignore=True):
        current_dir = os.getcwd()
        try:
            # Make src/project directory
            for directory in ['src', self.pyname]:
                if not os.path.exists(directory):
                    os.mkdir(directory)
                os.chdir(directory)

            self.write_template('package/init.pyt', True, '__init__.py')
            self.write_template('package/main.pyt', ignore, '__main__.py')
            self.write_template('package/meta.pyt', True, '__meta__.py')

            # Make test folder
            if not os.path.exists('tests'):
                os.mkdir('tests')
            os.chdir('tests')

            if not os.path.exists('__init__.py'):
                with open('__init__.py', 'w') as F:
                    F.write('\n')
            self.write_template(
                'package/test_project.pyt', ignore, 'test_%s.py' % self.pyname)

        finally:
            os.chdir(current_dir)

    def make_readme(self, ignore=True):
        self.write_template('README.rst', ignore=True)
        self.write_template('INSTALL.rst', ignore=ignore)

    def make_docs(self, ignore=True):
        self.make_readme(ignore=True)

        # Make src/project directory
        if not os.path.exists('docs'):
            os.mkdir('docs')
        self.write_template('docs/conf.pyt', ignore=ignore, path='docs/conf.py')
        self.write_template('docs/index.rst', ignore=ignore)
        self.write_template('docs/install.rst', ignore=ignore)
        self.write_template('docs/license.rst', ignore=ignore)
        self.write_template('docs/apidoc.rst', ignore=ignore)
        self.write_template('docs/warning.rst', ignore=ignore)
        self.write_template('docs/make.bat', ignore=True)
        self.write_template('docs/makefile.txt', ignore=True, path='Makefile')

        # Make sphinx folders
        with visit_dir('docs'):
            for folder in ['_static', '_build', '_templates']:
                if not os.path.exists(folder):
                    os.mkdir(folder)

    def make_license(self, ignore=True):
        license = license_alias.get(self.license, self.license)
        license_path = 'license/%s.txt' % license
        self.write_template(license_path, ignore=ignore, path='LICENSE')

    #
    # Features
    #
    def enable_feature(self, feature, **kwds):
        if not self.has_feature(feature):
            raise ValueError('invalid feature: %s' % feature)

        return getattr(self, 'make_' + feature)()

    def has_feature(self, feature):
        return feature in ['basic', 'docs', 'django']

    def make_basic(self, ignore=True):
        self.make_base(ignore)
        self.make_readme(ignore)
        self.make_setup_py(ignore)
        self.make_package(ignore)
        self.make_license(ignore)

    def make_django(self, ignore=True):
        pass

    def make_invoke(self, ignore=True):
        self.write_template('tasks.pyt', ignore=ignore, path='tasks.py')

    def save_config(self):
        for attr in BoilerplateConfig.valid_attrs:
            value = getattr(self, attr)
            if value is None:
                self.config.remove_option('options', attr)
            else:
                self.config.set('options', attr, value)
        self.config.save()


# noinspection PyPep8Naming
class attrdict(dict):
    """Dictionary with attribute access to keys."""

    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, value):
        self[attr] = value

    def sub(self, keys):
        if isinstance(keys, str):
            keys = keys.split()
        return attrdict({k: self[k] for k in keys})


if __name__ == '__main__':
    dirname = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    root = os.path.dirname(dirname)
    os.chdir(os.path.join(root, 'playground'))
    print(os.listdir(os.getcwd()))

    if yn_input('clean?') == 'yes':
        os.system('rm * -Rv')

    factory = ProjectFactory(
        author='Chips', email='foo@bar', project='foobar', version='0.1',
        license='gpl')
    factory = ProjectFactory()
    print(dir(factory))
    factory.new_project()
