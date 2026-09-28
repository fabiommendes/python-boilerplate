"""
Utilities that helps with testing.
"""

from contextlib import contextmanager

from ezio.testing import capture_io


@contextmanager
def capture_exit():
    """
    Capture any SystemExit exception.

    It re-raises the exception if the exit code is different from zero.
    """
    try:
        yield
    except SystemExit as err:
        if err.args != (0,):
            raise
    finally:
        pass


@contextmanager
def capture_interaction(inputs, echo=True):
    """
    Merges capture_exit with ezio.testing.capture_io.
    """

    with capture_io(inputs, echo=echo) as msg:
        with capture_exit():
            yield msg
