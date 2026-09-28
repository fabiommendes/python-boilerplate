from .install_package import install_package_from_module


def install_package(package, conf, clean=True):
    """
    Install Jarbas package with the given name or module.

    Args:
        package (str):
            Name of the jarbas package to be installed.
        conf (jarbas.conf.ProjectConf):
            Configuration object for the current project.
        clean (bool):
            If True (default), cleans temporary files after a successful
            execution.
    """

    if isinstance(package, str):
        mod = load_package_module(package)
    else:
        mod = package
    return install_package_from_module(mod, conf, clean=clean)


def load_package_module(name):
    """
    Return a Python module that implements the package from the package name.
    """

    if name == 'core/jarbas':
        import jarbas.packages.jarbas as mod
        return mod
    else:
        raise NotImplementedError
