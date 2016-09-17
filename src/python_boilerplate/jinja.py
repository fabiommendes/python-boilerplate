from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import base64
import codecs
import hashlib
import os
import platform

import jinja2
import six

from python_boilerplate import io
from python_boilerplate.io import yn_input


def write_template(template, namespace=None, ignore=False, path=None,
                   verbose=True, hash=None):
    """
    Render jinja template with the given namespace and saves it in the
    desired path
    """

    if path is None:
        path = template

    # We expect POSIX paths, but here we have to translate to the format used
    # in the filesystem
    path = os.path.join(*path.split('/'))

    template = jinja_env.get_template(template)
    data = template.render(**(namespace or {}))

    if os.path.exists(path) and ignore:
        return
    elif os.path.exists(path):
        with open(path) as F:
            file_data = F.read()
            if file_data == data:
                return

        # If hash is compatible with given hash, we simply overwrite
        ask = True
        if hash:
            file_hash = hashlib.md5(file_data.encode('utf8')).digest()
            file_hash = base64.b64encode(file_hash).decode()
            if hash == file_hash:
                os.rename(path, path + '.bak')
                ask = False

        if ask:
            msg = 'File %r exists. Save backup and overwrite?' % path
            response = yn_input(msg)
            if response == 'yes':
                os.rename(path, path + '.bak')
            else:
                return

    abspath = os.path.abspath(path)
    if verbose:
        io.show('    creating %s...' % abspath)

    # Save data as UTF-8
    with codecs.open(abspath, 'w', 'utf8') as F:
        if platform.system() == 'Windows':
            F.write(codecs.BOM_UTF8)
        F.write(data)

    return data


# Jinja filters
def unicode_escape(x):
    r"""
    Escape accents using \xXX unicode code points.
    """

    return six.u(x).encode('unicode-escape').decode()


# Initialize jinja environment
basedir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(basedir))
jinja_env.filters['repr'] = repr
jinja_env.filters['unicode_escape'] = unicode_escape
