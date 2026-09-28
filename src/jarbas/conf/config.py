import abc
import json

import configobj
import fs.errors

from jarbas.types import SingletonMeta


class Config(metaclass=SingletonMeta):
    """
    Base class for project and global configs.
    """

    def __init__(self):
        try:
            file = self.get_file(mode='r')
        except fs.errors.ResourceNotFound:
            file = None
        self.conf = configobj.ConfigObj(file, encoding='utf-8')

    def __getitem__(self, item):
        root = self.conf

        if isinstance(item, (tuple, list)):
            for path in item:
                root = root[path]
            return root

        return root[item]

    def __setitem__(self, item, value):
        root = self.conf

        if isinstance(item, (tuple, list)):
            for path in item[:-1]:
                root = root[path]
            root[item[-1]] = value
        else:
            root[item] = value

    @classmethod
    def open_config(cls, defaults):
        """
        Return properly initialized config object.
        """
        conf = cls()
        defaults = conf.get_defaults(defaults)
        conf.update(defaults)
        return conf

    def save(self):
        """
        Saves global configuration.
        """
        with self.get_file('wb', encoding='utf-8') as F:
            self.conf.write(F)

    def update(self, data):
        """
        Updates configuration with the supplied data.
        """
        conf = self.conf

        for section, values in data.items():
            config_section = conf.setdefault(section, {})
            for var, value in values.items():
                config_section.setdefault(var, value)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def to_json_data(self, indent=4):
        """
        Convert object to JSON string.
        """
        return json.dumps(self.conf, indent=indent)

    def to_json(self):
        """
        Return configuration as a JSON data structure.
        """
        return dict({k: dict(v) for k, v in self.conf.items()})

    @abc.abstractmethod
    def get_file(self, mode='r', **kwargs):
        """
        Return the config file object.
        """
        raise NotImplementedError('Must be implemented on a subclass.')

    @abc.abstractmethod
    def get_defaults(self, base=None):
        """
        Return the config file object.
        """
        raise NotImplementedError('Must be implemented on a subclass.')