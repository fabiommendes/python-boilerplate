class ResourceNotAvailable(Exception):
    """
    Base exception raised when a resource is not available.
    """


class ModuleNotAvailable(ResourceNotAvailable, ImportError):
    """
    Exception raised when python module is not available.
    """