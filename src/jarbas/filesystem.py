from click import get_app_dir
from fs import osfs

#
# Global handlers for special directories on the filesystem. Those can be
# easily mocked in tests.
#
root = osfs.OSFS('/')
home = osfs.OSFS('~/')
jarbas_root = osfs.OSFS(get_app_dir('jarbas') + '/', create=True)
cwd = osfs.OSFS('.')
