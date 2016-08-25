from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
import codecs
import hashlib
import os
try:
    import configparser
except ImportError:
    import ConfigParser as configparser
GLOBAL_CONFIG = None


class BoilerplateConfig(configparser.ConfigParser):
    """
    A ConfigParser that exposes contents from boilerplate.ini.
    """

    valid_options = [
        'project', 'author', 'email', 'version', 'license', 'pyname',
        'has_script',
    ]

    def __init__(self, *args, **kwds):
        configparser.ConfigParser.__init__(self, *args, **kwds)
        self.optionxform = str

        if os.path.exists('boilerplate.ini'):
            self.read('boilerplate.ini')

        # Create sessions
        if not self.has_section('options'):
            self.add_section('options')
        for attr in self.valid_options:
            if not self.has_option('options', attr):
                self.set('options', attr, '')

        if  not self.has_section('file hashes'):
            self.add_section('file hashes')

    def register_file(self, filename, data):
        """
        Compute and register the hash value for some file given its textual
        data.
        """

        file_hash = hashlib.md5(data.encode('utf8')).digest()
        file_hash = codecs.encode(file_hash, 'base64').decode()
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

    global GLOBAL_CONFIG

    if GLOBAL_CONFIG is None:
        GLOBAL_CONFIG = BoilerplateConfig()
    return GLOBAL_CONFIG


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
    for option in BoilerplateConfig.valid_options:
        kwargs.setdefault(option, cfg.get('options', option))

    # Additional derived attributes
    pyname_dashed = cfg.get('options', 'pyname').replace('_', '-')
    kwargs.setdefault('pyname_dashed', pyname_dashed)
    return kwargs


def register_file(filename, data):
    """
    Register file in the global config.
    """

    get_config().register_file(filename, data)
