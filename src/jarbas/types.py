import abc


class SingletonMeta(abc.ABCMeta):
    """
    Base class for singleton types.
    """

    def __call__(cls, *args, **kwargs):
        try:
            return cls._instance
        except AttributeError:
            cls._instance = super().__call__(*args, **kwargs)
            return cls._instance
