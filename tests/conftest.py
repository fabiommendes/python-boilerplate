from contextlib import contextmanager

import pytest
from fs import memoryfs
from fs import tempfs

import jarbas.conf.globals
from jarbas import filesystem

jarbas.conf.globals.username = 'user'


@contextmanager
def empty_fake_fs(constructor=memoryfs.MemoryFS):
    """
    Create a memory fake filesystem and return the CWD path and root.
    """

    cwd = filesystem.cwd
    home = filesystem.home
    root = filesystem.root
    jarbas_root = filesystem.jarbas_root

    try:
        filesystem.root = fs = constructor()
        filesystem.home = filesystem.cwd = fs_home = fs.makedirs('home/user')
        filesystem.jarbas_root = fs_home.makedirs('.config/jarbas')
        yield fs_home, root
    finally:
        filesystem.cwd = cwd
        filesystem.home = home
        filesystem.root = root
        filesystem.jarbas_root = jarbas_root


@pytest.yield_fixture
def empty_fs():
    """
    Create fake memory fs.
    """
    with empty_fake_fs() as (fs, _):
        yield fs


@pytest.yield_fixture
def config_fs():
    """
    Create fake memory fs with global config settings.
    """
    with empty_fake_fs() as (fs, _):
        with fs.open('.config/jarbas/settings.ini', 'w') as F:
            conf = jarbas.conf.globals.global_config()
            conf.save()
        yield fs


@pytest.yield_fixture
def temp_fs():
    """
    Temporary file with global settings config.
    """
    with empty_fake_fs(constructor=tempfs.TempFS) as (fs, _):
        with fs.open('.config/jarbas/settings.ini', 'w') as F:
            conf = jarbas.conf.globals.global_config()
            conf.save()
        yield fs
