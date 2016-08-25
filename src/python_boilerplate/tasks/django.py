from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from invoke import task, run


@task(help={
    'make': 'Disable/enable the makemigrations command.',
    'app': 'If given, apply migrations to an specific app.',
    'runserver': 'If true, executes the runserver command after migrations',
})
def migrate(ctx, make=False, app=None, runserver=False):
    """
    Run django manage.py makemigrations/migrate commands.
    """

    app_suffix = ' %s' % app if app else ''
    if make:
        run("python src/manage.py makemigrations" + app_suffix)
    run("python src/manage.py migrate" + app_suffix)
    if runserver:
        run('python src/manage.py runserver')


@task
def rmmigrations(ctx, keep_data=False, fake=False):
    """
    Remove all migration files. If --keep-data is set, it does not remove
    migrations named as XXXX_data_*.py.
    """

    import os
    import re

    regex = re.compile(r'^[0-9]{4}_\w+.py$')

    def is_migration(path):
        return len(path) >= 4 and path[:4].isdigit() and path.endswith('.py')

    for dir, subdirs, files in os.walk(os.getcwd()):
        if os.path.basename(dir) == 'migrations':
            migrations = [f for f in files if regex.match(f)]
            for f in migrations:
                path = os.path.join(dir, f)
                if keep_data and f[5:].startswith('initial_data'):
                    continue

                print('removing %s' % path, end='')
                if not fake:
                    os.unlink(path)
                    print(' ..OK')
                else:
                    print()

@task
def configure(ctx, ):
    os.chdir('src')
    from django.core import management
    management.call_command('makemigrations')
    management.call_command('migrate')
    management.call_command('createsuperuser')


@task
def syncdb(ctx, ):
    os.chdir('src')
    from django.core import management
    management.call_command('makemigrations')
    management.call_command('migrate')


@task
def gunicorn(ctx, bind='localhost:8000', collectstatic=False):
    if collectstatic:
        run('python src/manage.py collectstatic')
    os.chdir('src')
    run('gunicorn codeschool.wsgi -b %s --workers 13 --name codeschool-server' % bind)


@task
def serve(ctx, collectstatic=True):
    if collectstatic:
        run('python src/manage.py collectstatic')
    os.chdir('src')
    run('gunicorn codeschool.wsgi -b unix:/tmp/gunicorn.sock --workers 13 --name codeschool-server')



@task
def reset_migrations(keep_data=False):
    """
    Remove all migration files. If --keep-data is set, it does not remove
    migrations named as XXXX_data_*.py.
    """

    import os

    for x in os.walk(os.getcwd()):
        print(x)