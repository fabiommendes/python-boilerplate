import os
import sys

from invoke import task, run

EXEC_HELP = 'uses exec() syscall to keep same pid as the invoke task'


@task(help={
    'python': 'executes Python shell instead of bash.',
    'ipython': 'executes IPython shell, if available.',
    'django': 'executes `manage.py shell` command'
})
def shell(ctx, python=False, ipython=False, django=False):
    """
    Executes the interpreter.
    """

    if ipython:
        try:
            import IPython
        except ImportError:
            print('IPython not available, running regular Python shell.')
            os.execlp(sys.executable, '-i')
        else:
            os.execlp('ipython3', '-i')
    elif django:
        os.execlp(sys.executable, 'manage.py', 'shell')
    elif python:
        os.execlp(sys.executable, '-i')
    else:
        os.execlp('bash', '-i')


@task(help={
    'exec': EXEC_HELP
})
def nginx(ctx, exec=True):
    """
    Start Nginx proxy server.
    """

    run('nginx -p /var/www/ -c /etc/nginx/nginx.conf')
    if exec:
        os.execlp('nginx', '-p', '/var/www/', '-c', '/etc/nginx/nginx.conf')
    else:
        run('nginx -p /var/www/ -c /etc/nginx/nginx.conf')


@task(help={
    'exec': EXEC_HELP
})
def gunicorn(ctx, exec=True):
    """
    Starts Gunicorn application server.
    """

    if exec:
        wsgi_application = os.environ['WSGI_APPLICATION']
        sock = 'unix:/tmp/gunicorn.sock'
        os.execlp('gunicorn', '-b', sock, wsgi_application, '--reload')
    else:
        cmd = 'gunicorn $WSGI_APPLICATION -b unix:/tmp/webapp.sock --reload'
        ctx.run(cmd, pty=True)


@task(help={
    'exec': EXEC_HELP
})
def start(ctx, system=True):
    """
    Start both Nginx and Gunicorn under Circus supervision (#TODO!).
    """

    # os.execlp('circusd', '--daemon', '/etc/circus.ini')
    #os.spawnlp(os.P_NOWAIT, 'nginx', '-p', '/var/www', '-c', '/etc/nginx/nginx.conf')
    wsgi = os.environ.get('WSGI_APPLICATION', 'app')
    if system:
        ctx.run('nginx -p /var/www -c /etc/nginx/nginx.conf')
        ctx.run('gunicorn -b unix:/tmp/webapp.sock %s --reload' % wsgi, pty=True)
    else:
        ctx.run('nginx -p /var/www -c /etc/nginx/nginx.conf')
        sock = 'unix:/tmp/gunicorn.sock'
        os.execlp('gunicorn', '-b', sock, wsgi, '--reload')

@task
def dev(ctx):
    """
    Runs Django's development server.
    """

    os.execlp(sys.executable, 'manage.py', 'runserver', '0.0.0.0:80')
