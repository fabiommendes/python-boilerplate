"""
Replicate many useful git CLI commands.
"""


def add(repo, files):
    """
    $ git add FILES
    """
    if isinstance(files, str):
        return repo.git.execute(['git', 'add', files])
    else:
        for file in files:
            return repo.git.execute(['git', 'add', file])


def commit(repo, message=None):
    """
    $ git commit [-m message]
    """

    def contribute(flag, value):
        if value is not None:
            args.extend([flag, value])

    args = []
    contribute('-m', message)

    return repo.git.commit(*args)
