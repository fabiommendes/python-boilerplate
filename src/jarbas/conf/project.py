from jarbas import filesystem
from jarbas.conf import global_config
from jarbas.conf.config import Config
from jarbas.conf.globals import validate_email

PROJECT_CONFIG_FILE = 'conf/jarbas.ini'


def project_config(slug, path, defaults=None):
    """
    Create a default instantiation of the local config.

    Config is equivalent to:

        [jarbas-author]
        full_name = <Author>
        email = <Email>

        [jarbas-project]
        slug = <Project slug>
        name = <Project name>
        programming_language = <Main programming language used on the project>
        language = <(natural) language>
        url = <Project url>
        git_repository = <Github project's repository>

        [jarbas-packages]
        installed = ,
        suggests = ,
        recommends = package, repo-info
    """
    defaults = dict(defaults or {})
    project = defaults.setdefault('jarbas-project', {})
    project.setdefault('project_slug', slug)
    return ProjectConfig.open_config(path, defaults)


class ProjectConfig(Config):
    """
    Class that represents local project configuration.
    """

    path = '/'

    @classmethod
    def open_config(cls, path, defaults):
        config = super().open_config(defaults)
        config.path = path.rstrip('/')
        return config

    @property
    def project_path(self):
        return filesystem.cwd.opendir(self.path)

    def makedir(self, path):
        return self.project_path.makedirs(path, recreate=True)

    def get_file(self, mode='r', **kwargs):
        """
        Return fs path to project configuration file.
        """
        if 'w' in mode:
            filesystem.cwd.makedirs(self.path + '/conf/', recreate=True)

        path = filesystem.cwd.opendir(self.path)
        path.makedir('conf/', recreate=True)
        return path.open(PROJECT_CONFIG_FILE, mode=mode, **kwargs)

    def get_defaults(self, base=None):
        """
        Return default configurations.
        """
        return project_config_defaults(base)


def project_config_defaults(base=None):
    """
    Creates a dictionary with default configurations for the project
    configuration file. User can provide a dictionary with overrides.
    """

    global_conf = global_config()

    def section(key):
        section = config[key] = dict(base.get(key, {}))
        return section

    def setvalid(section, key, value, validation):
        section[key] = validation(section.get(key, value))

    base = base or {}
    config = {}

    # [jarbas-author]
    author = section('jarbas-author')
    glob_author = global_conf['jarbas-author']
    author.setdefault('full_name', glob_author['full_name'])
    setvalid(author, 'email', glob_author['email'], validate_email)

    # [jarbas-project]
    project = section('jarbas-project')
    project.setdefault('slug', 'slug')
    project.setdefault('name', 'name')
    project.setdefault('programming_language', 'python')
    project.setdefault('language', 'en')
    project.setdefault('url', 'http://project-url/')
    project.setdefault('git_repository', 'http://project-git-repo.git')

    # [jarbas-packages]
    packages = section('jarbas-packages')
    packages.setdefault('installed', [])
    packages.setdefault('suggests', [])
    packages.setdefault('recommends', ['package', 'repo-info'])

    return config


def has_project_config(path=None):
    """
    Return True if ~/.config/jarbas/conf.ini exists.
    """
    if path is None:
        path = filesystem.cwd
    return path.exists(PROJECT_CONFIG_FILE)
