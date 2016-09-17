from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import base64
import hashlib
import os

try:
    import configparser
except ImportError:
    import ConfigParser as configparser

GLOBAL_CONFIG = None
CONFIG_DIR = None
NOT_GIVEN = object()

# Transformation in the context variables
TRANSFORMATIONS = {
    ('options', 'boilerplate_version'): int,
    ('options', 'has_script'): lambda x: True if x.lower() == 'true' else False,
}


class BoilerplateConfig(configparser.ConfigParser):
    """
    A ConfigParser that exposes contents from boilerplate.ini.
    """

    valid_options = {
        'boilerplate_version': '1',
        'project': '',
        'author': '',
        'email': '',
        'version': '0.1.0',
        'license': 'mit',
        'pyname': '',
        'has_script': 'false',
        'python_version': 'both',
    }

    def __init__(self, *args, **kwds):
        configparser.ConfigParser.__init__(self, *args, **kwds)
        self.optionxform = str

        if os.path.exists('boilerplate.ini'):
            self.read('boilerplate.ini')

        # Create sessions
        if not self.has_section('options'):
            self.add_section('options')
        for attr, default in self.valid_options.items():
            if not self.has_option('options', attr):
                self.set('options', attr, default)

        if not self.has_section('file hashes'):
            self.add_section('file hashes')

    def register_file(self, filename, data):
        """
        Compute and register the hash value for some file given its textual
        data.
        """

        file_hash = hashlib.md5(data.encode('utf8')).digest()
        file_hash = base64.b64encode(file_hash).decode()
        self.set('file hashes', filename, file_hash)

    def save(self):
        """
        Saves content to boilerplate.ini.
        """

        with open('boilerplate.ini', 'w') as F:
            self.write(F)


def get_config():
    """
    Returns an instance of BoilerplateConfig
    """

    global GLOBAL_CONFIG, CONFIG_DIR

    if GLOBAL_CONFIG is None or CONFIG_DIR != os.getcwd():
        GLOBAL_CONFIG = BoilerplateConfig()
        CONFIG_DIR = os.getcwd()
    return GLOBAL_CONFIG


def get_option(section, option, default=NOT_GIVEN):
    """
    Return the chosen configuration option from .boilerplate.ini.

    Section and option must be provided. If configuration is not present, it
    returns the provided default value or raise a ValueError.
    """

    try:
        return get_config().get(section, option)
    except KeyError:
        if default is NOT_GIVEN:
            raise ValueError('invalid config option: %s/%s' % (section, option))
        else:
            return default


def save_config():
    """
    Saves the global config on disk.
    """

    get_config().save()


def refresh_config():
    """
    Forces the global config object to reload options from boilerplate.ini.
    """

    global GLOBAL_CONFIG
    GLOBAL_CONFIG = None
    return get_config()


def get_context(**kwargs):
    """
    Return a dictionary with common context variables extracted from the global
    config.
    """

    cfg = get_config()
    for option, default in BoilerplateConfig.valid_options.items():
        value = cfg.get('options', option)
        if value is None:
            value = default
        if ('options', option) in TRANSFORMATIONS:
            value = TRANSFORMATIONS[('options', option)](value)
        kwargs.setdefault(option, value)

    # Additional derived attributes
    pyname = cfg.get('options', 'pyname')
    pyname_dashed = pyname.replace('_', '-')
    kwargs.setdefault('pyname_dashed', pyname_dashed)
    kwargs.setdefault('package', pyname)
    return kwargs


def register_file(filename, data):
    """
    Register file in the global config.
    """

    get_config().register_file(filename, data)
