import git


def ensure_repo(path, origin=None, upstream=None):
    """
    Ensure that a git repository exists on the given path and have the given
    origin and upstream refs.

    Args:
        path:
            Path to search for the git repository.
        origin/upstream:
            Url for the origin/upstream repo.
    """
    if not path.exists('.git'):
        return init_repo(path, origin, upstream)

    repo = git.Repo(path.getsyspath('/'))
    remotes = {remote.name: remote for remote in repo.remotes}

    # Fix origin and upstream remotes
    for name, url in [('origin', origin), ('upstream', 'upstream')]:
        if url:
            remote = remotes.get(name)
            if remote is None:
                repo.create_remote(name, url)
            elif url not in remote.urls:
                remote.add_url(url)
    return repo


def init_repo(path, origin=None, upstream=None):
    """
    Equivalent to git init on the given path.

    Args:
        origin/upstream:
            If given, sets the origin and upstream refs.

    Return:
        A git.Repo instance.
    """
    repo = git.Repo.init(path.getsyspath('/'))

    if origin:
        repo.create_remote('origin', origin)
    if upstream:
        repo.create_remote('upstream', upstream)

    return repo
