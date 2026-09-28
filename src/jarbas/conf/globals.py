import getpass

from .. import filesystem
from jarbas.conf.config import Config

CONFIG_FILE_NAME = 'settings.ini'
username = getpass.getuser()


def global_config(defaults=None):
    """
    Return the global configuration object.

    If the global configuration file (located at ~/.config/jarbas/settings.ini)
    does not exist, creates a GlobalConfig instance with default values and
    return it unsaved.

    If a dictionary with default values is supplied, it is used to populate
    variables in the default configuration object. A dictionary of default
    configurations is always supplied by Jarbas. That way, if new versions of
    Jarbas add new configuration variables, it gets updated with the default
    values on loading.

    The default configuration is a .ini file with the following structure::

        [jarbas-author]
        full_name = <Author's full name>
        email = <Author's email>
        gender = <male|female|other>

        [jarbas-accounts]
        pypi_username = <Username of author's PyPI account>
        github_username = <...>
        gitlab_username = <...>
        bitbucket_username = <...>
        dockerhub_username = <...>

        [jarbas-tools]
        diff_editor = <favorite merge editor>
        diff_editor_command = <favorite merge editor>

        [jarbas-project-paths]
        my_project1 = ~/projects/my_project1/
    """

    return GlobalConfig.open_config(defaults)


class GlobalConfig(Config):
    """
    A class that holds the global configuration object.

    Use the global_config() function to retrieve this singleton.
    """

    def get_file(self, mode, **kwargs):
        """
        Return fs path to global configuration file.
        """
        return filesystem.jarbas_root.open(CONFIG_FILE_NAME,
                                           mode=mode,
                                           **kwargs)

    def get_defaults(self, base=None):
        """
        Return default configurations.
        """
        return global_config_defaults(base)


def global_config_defaults(base=None):
    """
    Creates a dictionary with default configurations for the global
    configuration file. User can provide a dictionary with overrides.
    """

    def section(key):
        section = config[key] = dict(base.get(key, {}))
        return section

    def setvalid(section, key, value, validation):
        section[key] = validation(section.get(key, value))

    base = base or {}
    config = {}
    email_stub = '{}@domain.com'.format(username)

    # [jarbas-author]
    author = section('jarbas-author')
    author.setdefault('full_name', username)
    setvalid(author, 'email', email_stub, validate_email)
    setvalid(author, 'gender', 'other', validate_gender)

    # [jarbas-accounts]
    accounts = section('jarbas-accounts')
    services = ['pypi', 'github', 'gitlab', 'dockerhub', 'bitbucket']
    for attr in services:
        accounts.setdefault(attr + '_username', username)

    # [jarbas-tools]
    tools = section('jarbas-tools')
    tools.setdefault('diff_editor', 'meld')
    tools.setdefault('diff_editor_command', 'meld')

    # [jarbas-project-paths]
    projects = section('jarbas-project-paths')
    for name, path in base.get('jarbas-project-paths', {}).items():
        projects[name] = path

    return config


def has_global_config():
    """
    Return True if ~/.config/jarbas/conf.ini exists.
    """
    return filesystem.jarbas_root.exists(CONFIG_FILE_NAME)


#
# Validation functions
#
def validate_gender(value):
    value = (value or 'other').casefold()
    if value not in {'male', 'female', 'other'}:
        raise ValueError('invalid gender: %s' % value)
    return value


def validate_email(value):
    return value
