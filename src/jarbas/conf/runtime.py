class Error:
    """
    Represents a configuration error
    """

    def __init__(self, msg, fix=None, is_fatal=False, autofix=False, help=None):
        self.msg = msg
        self.fixit = fix
        self.fixable = fix is not None
        self.is_fatal = is_fatal
        self.autofix = autofix
        self.help = help

    def __repr__(self):
        return self.msg


def get_environment_errors():
    """
    Return a list of environment errors.
    """
    errors = [
        check_python_is_in_path(),
        check_scripts_bin_is_in_path(),
    ]
    return [e for e in errors if e]


def check_python_is_in_path():
    if not is_in_path(os.path.dirname(sys.executable)):
        return Error(
            'your Python executable is not in path.',
            add_python_executable_to_path,
        )


def check_scripts_bin_is_in_path():
    if not is_in_path('~/.local/bin/'):
        return Error(
            'the .local/bin/ not in your PATH.',
            add_local_bin_to_path,
            help=(
                'Python scripts installed with pip or setup.py using the\n'
                '--user option are copied to this folder. The folder must be\n'
                'in the path in order to make those scripts available.'
            )
        )


def normalize_path(path):
    path = os.path.abspath(os.path.expanduser(path))
    if path.endswith(os.sep):
        return path[:-1]
    return path


def is_in_path(path, memo=None):
    """
    Checks if path is in the PATH environment variable.

    This function tracks symlinks in case either path is a symbolic link or
    if any component of $PATH is also a symlink.
    """
    memo = memo or {}
    path = normalize_path(path)

    for part in os.environ.get('PATH', '').split(':'):
        part = normalize_path(part)

        if part == path:
            return True
        elif os.path.islink(part):
            expanded = normalize_path(os.readlink(part))
            if expanded == path:
                return True

    if os.path.islink(path) and path not in memo:
        return is_in_path(os.readlink(path), memo)

    return False


def add_python_executable_to_path():
    add_to_path(os.path.dirname(sys.executable))


def add_local_bin_to_path():
    if config.POSIX:
        add_to_path(os.path.expanduser('~/.local/bin/'))
    else:
        raise not_implemented_in_platform()


def add_to_path(path):
    if config.POSIX:
        with open(os.path.expanduser('.profile'), 'a') as F:
            F.write('PATH=$PATH:%s' % path)
    else:
        raise not_implemented_in_platform()


def not_implemented_in_platform():
    msg = 'command not available for your platform: %r' % sys.platform
    return NotImplementedError(msg)
