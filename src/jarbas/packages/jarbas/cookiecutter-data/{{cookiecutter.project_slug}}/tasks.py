from invoke import task

try:
    from jarbas.tasks import discover_tasks
except ImportError:
    from warnings import warn

    warn('Jarbas is not installed in your system.')
    discover_tasks = lambda x: None


@task
def custom(ctx):
    """
    An example task.
    """
    ctx.run('echo hello world!')


discover_tasks(globals())
