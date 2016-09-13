from . import core as _core
from invoke import Collection as _Collection, task as _task

ns = _Collection.from_module(_core)


def task(*args, **kwargs):
    if not kwargs and len(args) == 1 and callable(args[0]):
        task = _task(args[0])
        ns.add_task(task)
    else:
        def decorator(func):
            task = _task(func)
            ns.add_task(task)
            return task
        return decorator