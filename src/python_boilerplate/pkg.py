import pip

from python_boilerplate import io
from python_boilerplate.errors import ModuleNotAvailable

NOT_GIVEN = object()


def is_running_on_virtual_env():
    """
    Return True if code is running on a virtual environment
    """

    return False


def has_python():
    pass


def require_cli(command, apt_name=NOT_GIVEN, interactive=False):
    """
    Assure the system has the given command line command installed.

    Args:
        command:
            Name of the command.

    Returns:
        Full path to the requested command.
    """


def require_module(module, pipname=NOT_GIVEN, interactive=False):
    """
    Assure system has the given python module installed.

    Args:
        module (str):
            String for module name
        pipname (str):
            Name of the PyPI package that provides the module. Has the same name
            as module by default.
        interactive (bool):
            If given, operates in the interactive mode and asks the user to
            download the module in pip. The default behavior is to download
            the module, unless ``pipname`` is explicitly set to None.

    Returns:
        The requested module.
    """

    # Return on success
    try:
        return __import__(module)
    except ImportError:
        pass

    # Automatic pip downloader
    def auto_pip_downloader(module, pipname):
        pip_download(module)
        try:
            return __import__(module)
        except ImportError:
            raise ModuleNotAvailable(
                'Module %r was downloaded from %r pip package, but it is '
                'still not available.' % (module, pipname)
            )

    # Error message
    def pip_cancel(module):
        msg = 'Please install the %r manually.' % module
        return ModuleNotAvailable(msg)

    # Normalize pipname
    if pipname is NOT_GIVEN:
        pipname = module

    # Handle import failure. The rule is to ask the user if he/she wants to
    # install the module using pip.
    if interactive:
        print('This command requires the %s module to run.' % module)

        if pipname is None:
            raise pip_cancel(module)

        elif 'yes' == io.yn_input('Do you want to install it using pip? '):
            return auto_pip_downloader(module, pipname)
        else:
            msg = 'You need this module to proceed'
            raise ModuleNotAvailable(msg)
    else:
        if pipname is None:
            raise pip_cancel(module)
        return auto_pip_downloader(module, pipname)


def pip_download(module, update=False):
    """
    Download module in pip
    """
    args = ['install', module]

    if not is_running_on_virtual_env():
        args.append('--user')
    if update:
        args.append('-U')

    pip.main(args)
