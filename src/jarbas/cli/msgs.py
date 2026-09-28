# -----------------------------------------------------------------------------
# Config options
#
CONFIG_BANNER = '''Hello!

This seems to be the first time you execute <b>Jarbas</b>. I need to known
a few things about you before we go. I will only ask this once, and this
information will be reused across several projects. If you want to revisit any
configuration information, please check the <b>~/.config/jarbas.ini</b> file
in your home folder.
'''
CONFIG_ALREADY_CONFIGURED = '''

<b><yellow>Already configured.</yellow></b>

Execute <b>"jarbas config --reset"</b> flag to force recreation of the configuration file.'''
GLOBAL_SUCCESSFULLY_UPDATED = '\nGlobal config successfully updated!'


# -----------------------------------------------------------------------------
# New project options
#
UPDATE_PROJECT_BANNER = """Glad to see you here, {developer_name}!

It seems that you already initialized your project. You now may select a
profile to add new features and modules.
"""

JARBAS_SETTINGS_TEMPLATE = """
# Basic info
JARBAS_VERSION = 1
VERSION = {version!r}
PROJECT_NAME = {project_name!r}
PACKAGE_NAME = {package_name!r}
REPOSITORY = {repository!r}
AUTHORS = [{author!r}]
PROFILES = []
"""

LOCAL_README = """This is a private directory that is not shared with other
developers in the git repository. This is the place to put local
configurations, scripts and private data.
"""

GITIGNORE = """# Private files
/local/

# Cached results and packages
__pycache__/
*.egg-info/
node_modules/
bower_components/

# Unwanted file types
*.pyc
*.pyo
*.pyd
*.so
*.dll
*.egg
*.sqlite3

# Build directories
docs/_build/
build/
dist/
htmlcov/

# IDEs and editors
.idea/
.cache/
.vscode/

# Testing and temporary files
.tox/
.coverage
"""

CHOOSE_MODULE = """Most functionality in your project is provided by Jarbas
modules. Using modules makes dealing with a project that grows
with time more scalable. We don't have to put everything upfront, but
it is possible to add more features and complexity when the project
requires it.

The first module you should choose is the one that brings basic support
for your programming language. From that, we can grow gradually.
"""

LAST_REMARKS = """I just finished installing a basic structure for your
application.

Type "jarbas hello" in your project's directory when you want to start
a programming session and "jarbas goodbye" when you are done with it.

Happy programming!
"""