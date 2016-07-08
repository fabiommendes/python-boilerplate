import codecs
import hashlib
import os

import jinja2

from python_boilerplate.inputs import yn_input

basedir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(basedir))


def write_template(template: str, namespace=None, ignore=False, path=None,
                   verbose=True, hash=None):
    """
    Render jinja template with the given namespace and saves it in the
    desired path
    """

    if path is None:
        path = template

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
            file_hash = codecs.encode(file_hash, 'base64').decode()
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

    if verbose:
        print('    creating %s...' % os.path.abspath(path))

    with open(path, 'w') as F:
        F.write(data)

    return data