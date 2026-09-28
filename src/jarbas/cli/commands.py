import os
import sys

import click
from fs.errors import NoSysPath

import ezio
import jarbas.scaffold.base
from . import msgs
from . import ui
from .. import __version__
from .. import filesystem
from .. import scaffold
from .. import git
from ..conf.globals import has_global_config, global_config
from ..conf.project import has_project_config
from ..io import fancy_print
from ..utils import visit_dir


def version_msg():
    python_version = sys.version[:3]
    message = 'Jarbas {} (Python {})'
    return message.format(__version__, python_version)


# ------------------------------------------------------------------------------
# Jarbas main entry point
#
@click.group(context_settings={'help_option_names': ['-h', '--help']})
@click.version_option(__version__, '-v', '--version', message=version_msg())
def main():
    pass


# ------------------------------------------------------------------------------
# jarbas config [--json] [--reset]
#
@main.command()
@click.option('--json', is_flag=True,
              help='Output global configuration as JSON')
@click.option('--reset', is_flag=True,
              help='Recreate configuration from scratch')
def config(reset, json):
    """
    Manages global configuration.
    """

    # Print configuration as JSON
    if json:
        return ezio.print(global_config().to_json_data())

    # Main interaction loop: we ask input for the user and write info to
    # the global configuration file.
    fancy_print(msgs.CONFIG_BANNER, format=True, max_width=80)
    ezio.pause()

    if not has_global_config() or reset:
        conf = ui.config(global_config())
        conf.save()
        fancy_print(msgs.GLOBAL_SUCCESSFULLY_UPDATED)
    else:
        fancy_print(msgs.CONFIG_ALREADY_CONFIGURED)


# ------------------------------------------------------------------------------
# jarbas new SLUG [--json] [--reset]
#
@main.command(name='new-project')
@click.argument('slug')
def new_project(slug):
    """
    Creates a new Jarbas project.

    The slug is the name of the sub-folder in which your project lives. You can
    create a project in the CWD, by typing

        $ jarbas new .
    """

    slug = slug.rstrip(os.path.sep)
    cwd = filesystem.cwd

    # Get the topmost directory name. Most shells expand "." to the current
    # directory, so we will not know if user has typed "." or the current
    # directory name. We must match path against it in a way that works both
    # with real sys paths and with fs.memoryfs.MemoryFS instances used in
    # tests.
    try:
        curr_path = (
            cwd.getsyspath('/')
                .rstrip(os.path.sep)
                .rpartition(os.path.sep)[-1]
        )
    except NoSysPath:
        curr_path = (
            cwd._sub_dir
                .rstrip(os.path.sep)
                .rpartition(os.path.sep)[-1]
        )

    # Select the slug and the path components
    if slug == '.' or slug == curr_path:
        path = '/'
        slug = os.path.split(os.getcwd())[-1]
    else:
        path = slug
    if cwd.exists(path) and has_project_config(cwd.opendir(path)):
        raise SystemExit('Project already initialized on the given path.')

    # Ask information about the project.
    conf = ui.new_project(slug, path)
    conf.save()

    # Configure git
    repo = git.ensure_repo(
        conf.project_path,
        origin=conf.get(['jarbas-project', 'git_repository']),
        upstream=conf.get(['jarbas-project', 'git_upstream']),
    )

    # Start cookiecutter scaffold
    jarbas.scaffold.base.install_package('core/jarbas', conf)

    # Commit changes
    # TODO: use git.Repo methods instead of going to the cli
    with visit_dir(cwd.opendir(path)):
        msg = 'Create Jarbas project structure.'
        print(git.add(repo, '.'))
        print(git.commit(repo, message=msg))


# ------------------------------------------------------------------------------
# jarbas hello PROJECT
#
@main.command()
def hello():
    """
    Performs basic checks before you start your day.
    """

    ezio.print('Hello Sir!')


# ------------------------------------------------------------------------------
# jarbas goodbye
#
@main.command()
def goodbye():
    """
    Ends your development session.
    """

    ezio.print('Goodbye!')


if __name__ == '__main__':
    main()
