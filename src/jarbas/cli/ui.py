import ezio
from ..conf.globals import global_config_defaults, global_config
from ..conf.project import project_config, ProjectConfig


#
# $ jarbas config
#
def config(conf):
    """
    Prompt user for configuration and return a dictionary with the variables
    filled by the user.

    Args:
        conf:
            A jarbas configuration object.
    """
    return Config.run(conf)


class Config(ezio.Interaction):
    def __init__(self, conf):
        super().__init__()
        self.conf = conf
        self.namespace = {
            # jarbas-author
            'full_name': conf['jarbas-author']['full_name'],
            'email': conf['jarbas-author']['email'],
            'gender': conf['jarbas-author']['gender'],

            # jarbas-accounts
            'pypi_username': conf['jarbas-accounts']['pypi_username'],
            'github_username': conf['jarbas-accounts']['github_username'],
            'gitlab_username': conf['jarbas-accounts']['gitlab_username'],
            'bitbucket_username': conf['jarbas-accounts']['bitbucket_username'],
            'dockerhub_username': conf['jarbas-accounts']['dockerhub_username'],

            # jarbas-tools
            'diff_editor': conf['jarbas-tools']['diff_editor'],
            'diff_editor_command': conf['jarbas-tools']['diff_editor_command'],
        }

    def interact(self, ns):
        """
        Please fill in the following information (press ? for help):

        Full name: [full_name = full_name]
        Email: [email = email]
        PyPI account: [pypi_username = pypi_username ? pypi_help()]
        Github account: [github_username = github_username ? github_help()]
        Dockerhub account: [dockerhub_username = dockerhub_username ? dockerhub_help() ]
        """
        defaults = global_config_defaults()
        for section in ['author', 'accounts', 'tools']:
            section_name = 'jarbas-' + section
            section = self.conf[section_name]
            for variable in defaults[section_name]:
                section[variable] = ns[variable]
        return self.conf

    # Validators
    def _default_validator(self, func):
        return func

    name_validator = email_validator = pypi_validator = github_validator = \
        dockerhub_valitador = _default_validator

    # Filters
    # ...

    # Functions
    def username(self, email):
        return email.partition('@')[0]

    def github_help(self):
        return (
            "Github is a platform for collaborative development. You can "
            "create an account for free and host code of your amazing projects "
            "so everybody can see and contribute "
            "(check: http://rtfd.org/jarbas/help/github.html for more info)."
        )

    def pypi_help(self):
        return (
            "PyPI (Python Package Index) is a central repository of Python "
            "packages. Anyone can post a package so it can be easily installed "
            "by third parties. Jarbas prepare the basic structure of a package "
            "so you can post a new package for everyone to see with a simple "
            "command "
            "(check: http://rtfd.org/jarbs/help/PyPI.html for more info)."
        )

    def dockerhub_help(self):
        return (
            "Dockerhub allows you to share docker images."
        )


#
# $ jarbas new-project
#
def new_project(slug, path) -> ProjectConfig:
    """
    Asks the user information to create a new Jarbas project.

    Return the project configuration object.
    """
    return NewProject.run(slug, path)


class NewProject(ezio.Interaction):
    def __init__(self, slug, path):
        self.slug = slug
        self.path = path
        self.conf = project_config(slug, path)
        glob = global_config()
        super().__init__(format=True)

        # Auxiliary variables
        git_username = glob['jarbas-accounts'].get('github_username',
                                                   'git_user')
        default_project_name = slug.replace('-', ' ').replace('_', ' ').title()

        self.namespace.update(
            full_name=glob['jarbas-author', 'full_name'],
            developer=glob['jarbas-author', 'full_name'],
            email=glob['jarbas-author', 'email'],
            project_slug=slug,
            project_url='http://%s.github.io' % slug,
            git_repository='http://github.com/%s/%s.git' % (git_username, slug),
            default_project_name=default_project_name,
        )

    def interact(self, ns):
        """
        Glad to see you here, $developer!

        This basic project template creates a new Jarbas project with the bare
        essentials. If you want to know more and understand the role of each
        part, please go to http://rtfd.org/jarbas/help/base.html.

        <b>First, we need to ask you a few questions.</b> []

        Author's name: [full_name = full_name]
        E-mail: [email = email]

        <b>Tell me about your project</b>

        Project name: [project_name = default_project_name ]
        Main programming language: [programming_language = 'python']
        URL: [project_url = project_url]
        Git respository: [git_repository = git_repository]
        Language = [project_language = 'en']

        <b>Your project has been created!</b>

        Your settings were stored on the conf/jarbas.ini file inside your
        project folder.
        """

        conf = self.conf

        # [jarbas-author]
        conf['jarbas-author', 'full_name'] = ns['full_name']
        conf['jarbas-author', 'email'] = ns['email']

        # [jarbas-project]
        conf['jarbas-project', 'slug'] = self.slug
        conf['jarbas-project', 'name'] = ns['project_name']
        conf['jarbas-project', 'url'] = ns['project_url']
        conf['jarbas-project', 'git_repository'] = ns['git_repository']
        conf['jarbas-project', 'programming_language'] = ns[
            'programming_language']
        conf['jarbas-project', 'language'] = ns['project_language']

        return self.conf
