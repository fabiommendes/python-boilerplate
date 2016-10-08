from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shlex
import sys

from invoke import task, run

from python_boilerplate import io
from python_boilerplate.config import get_option

PATH = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(PATH, 'src')))
IS_DJANGO_STARTED = False


@task
def configure(ctx, username='root', password='root',
              email='root@codeschool.com'):
    """
    Initial configuration of a Django project.

    Run migrations, and create the superuser.
    """

    migrate(make=True)
    createsuperuser(username=username, password=password, email=email)


@task(help={
    'make': 'Enable the makemigrations command.',
    'app': 'If given, apply migrations to an specific app.',
    'runserver': 'If true, executes the runserver command after migrations',
})
def migrate(ctx, make=False, app=None, runserver=False):
    """
    Run manage.py makemigrations/migrate commands.
    """

    app_suffix = ' %s' % app if app else ''
    if make or io.yn_input('Execute makemigrations? ') == 'yes':
        run("python src/manage.py makemigrations" + app_suffix)
    run("python src/manage.py migrate" + app_suffix)
    if runserver or io.yn_input('Execute runserver? ') == 'yes':
        run('python src/manage.py runserver')


@task
def createsuperuser(ctx, username='root', password='root',
                    email='root@codeschool.com'):
    """
    Create createsuperuser for django.

    The default username/password is "root/root".
    """

    django_start()
    from django.contrib.auth.models import User
    root = User.objects.create(username=username,
                               email=email,
                               is_staff=True,
                               is_active=True,
                               is_superuser=True)
    root.set_password(password)
    root.save()


@task(help={
    'bind': 'ip address to bind',
    'port': 'list to this port (default 8000).'
})
def run(ctx, bind='localhost', port=8000):
    """
    Starts the development server for local testing.
    """

    tail = ''
    if bind and port:
        tail = '%s:%s' % (bind, port)
    elif bind:
        tail = str(bind)
    elif port:
        tail = str(port)
    django_manage('runserver' + tail)


@task
def gunicorn(ctx, bind='localhost:8000', workers=13, collectstatic=True):
    """
    Starts Gunicorn server. This is not an optimal deployment, since you should
    serve static files with a proxy such as nginx. However, Gunicorn is much
    more robust than the development server that comes bundled with Django.
    """

    if collectstatic:
        django_manage('collectstatic')
    ctx.run('gunicorn {project_root}.wsgi -b {bind} '
            '--workers {workers} '
            '--name {project}-server'.format(
        project_root=project_root(),
        bind=bind,
        workers=workers,
        project=get_option('options', 'pyname').replace('_', '-')
    ))


@task(help={
    'auto': 'remove all migrations named XXXX_auto...',
    'all': 'remove all migration files.',
    'initial': 'remove all 0001_initial.py migration files.',
    'db': 'remove all contents of the database.',
})
def rmmigrations(ctx, auto=False, initial=False, all=False, db=False):
    """
    Remove migration files. You must pass a flag telling the category of
    migrations that should be removed.
    """

    import os
    import re

    regex = re.compile(r'^[0-9]{4}_\w+.py$')

    def is_migration(path):
        return len(path) >= 4 and path[:4].isdigit() and path.endswith('.py')

    for base, subdirs, files in os.walk(os.getcwd()):
        if os.path.basename(base) == 'migrations':
            migrations = [f for f in files if regex.match(f)]
            for f in migrations:
                remove = all
                if auto and '_auto_' in f:
                    remove = True
                if initial and f.endswith('_initial.py'):
                    remove = True

                if remove:
                    path = os.path.join(base, f)
                    print('removing %s' % path)
                    os.unlink(path)


#
# Auxiliary functions
#
def django_manage(cmd):
    """
    Runs a django management command in the local interpreter.
    """

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "codeschool.site.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(shlex.split('manage.py ' + cmd))


def django_module():
    """
    Runs a django management command in the local interpreter.
    """

    django_start()
    mod_name = get_option('options', 'pyname')
    mod = __import__(mod_name)
    return mod


def django_start():
    """
    Initializes django.
    """

    global IS_DJANGO_STARTED

    if not IS_DJANGO_STARTED:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", django_settings())
        from django import setup
        setup()
        IS_DJANGO_STARTED = True


def django_settings():
    """
    Return a string with the contents of the DJANGO_SETTINGS_MODULE.
    """

    try:
        return os.environ['DJANGO_SETTINGS_MODULE']
    except KeyError:
        from python_boilerplate.config import get_config

        try:
            return get_option('django', 'settings_module')
        except ValueError:
            return project_root() + '.settings'


def project_root():
    """
    Return the project root.
    """

    try:
        return get_option('django', 'project_root')
    except ValueError:
        pass

    # No configuration was found. We need to search for a django project in the
    # package tree. The first option is that the project adopts the
    # python-boilerplate layout for a django project:
    pyname = get_option('options', 'pyname')
    if os.path.exists(os.path.join('src', pyname, 'site')):
        return pyname + '.site'

    # Secondly, it might be a layout for a django app. In this case, the
    # project root points to the test project inside the "tests" folder
    if os.path.exists(os.path.join('src', pyname, 'tests', 'site')):
        return pyname + '.tests.site'

    # Everything fails! Quit!
    raise RuntimeError(
        'Could not determine the project root. Is this a really django '
        'project? Please run `python-boilerplate django-project` or '
        '`python-boilerplate django-app` in order to create a project '
        'structure.'
    )
