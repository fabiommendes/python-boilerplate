import os
import datetime

from python_boilerplate.inputs import default_input, yn_input, ny_input
from python_boilerplate.config import get_config, get_context, save_config, \
    register_file
from python_boilerplate.jinja import write_template


class ConfigManager:
    """
    Manage configurations for a FileWriter object.

    It may ask for user input if it cannot find some option in the
    boilerplate.ini file.
    """

    def __init__(self, config_section, **kwargs):
        self.__dict__['config_section'] = config_section
        kwargs = {k: v for k, v in kwargs.items() if v}
        cfg = get_config()
        for k, v in kwargs.items():
            cfg.set(config_section, k, v)

    def __getattr__(self, attr):
        try:
            return get_config().get(self.config_section, attr)
        except KeyError:
            raise AttributeError

    def __setattr__(self, attr, value):
        if attr.startswith('_'):
            self.__dict__[attr] = value
        else:
            get_config().set(self.config_section, attr, value)

    def run(self):
        """
        Subclass must override this method to ask for user input.
        """

    def require(self, name, text, default=None, section=None, action=None):
        """
        Require that the given variable is defined in the config file.
        """

        section = section or self.config_section
        value = get_config().get(section, name)
        if not value:
            if action is None and default is None:
                value = input(text)
            elif action is None:
                value = default_input(text, default)
            elif action == 'yn':
                value = yn_input(text)
            elif action == 'ny':
                value = ny_input(text)
            else:
                raise ValueError('invalid action: %r' % action)

        # Save value
        get_config().set(self.config_section, name, value)
        return value

    def save(self):
        """
        Write changes to boilerplate.ini.
        """

        save_config()

    def get_context(self, **kwargs):
        """
        Return a context dictionary
        """

        return {}


class FileWriter:
    """
    A task that writes files in the disk.

    Attributes:
        basepath:
            Base path where to write files.
        config:
            Reference to the job config object.
        context:
            A dictionary with extra context variables.
    """
    project = property(lambda _: get_config().get('options', 'project'))
    pyname = property(lambda _: get_config().get('options', 'pyname'))

    def __init__(self, config, context=None):
        self.basepath = os.getcwd()
        self.config = config
        self.context = dict(context or {})

    def get_context(self, **kwargs):
        """
        Return a context dictionary for rendering templates.
        """

        kwargs = dict(self.config.get_context(), **self.context)
        kwargs = dict(kwargs, **kwargs)
        return get_context(**kwargs)

    def save(self):
        """
        Saves config file.
        """

        save_config()

    def write(self, template, path=None, ignore=False):
        """
        Process contents of template and write them to the given path.

        If ignore is true, ignore file if it already exist.
        """

        base = os.getcwd()
        file = os.path.join(base, path or template)
        file = file[len(self.basepath) + 1:]

        # Prepare namespace
        context = self.get_context(job=self, date=datetime.datetime.now())

        # Write data and fetch hash
        prepare_path(path or template)
        hash = write_template(template, context, ignore=ignore, path=path)
        if hash is not None:
            register_file(file, hash)


def prepare_path(path):
    """
    Ensure the parent directory to path exists.
    """

    dirs = path.rpartition(os.path.sep)[0].split(os.path.sep)
    base = os.getcwd()
    for dir in dirs:
        base = os.path.join(base, dir)
        if not os.path.exists(base):
            os.mkdir(base)