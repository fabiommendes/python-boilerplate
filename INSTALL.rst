=========================
Installation instructions
=========================

python-boilerplate can be installed using pip::

    $ python -m pip install python-boilerplate

This command will fetch the archive and its dependencies from the internet and
install them. 

If you've downloaded the tarball, unpack it, and execute::

    $ python setup.py install --user

You might prefer to install it as system-wide. In this case, skip the ``--user``
option and execute as superuser by prepending the command with ``sudo``.


Troubleshoot
------------

Windows users may find that these command will only works if typed from Python's
installation directory.

Some Linux distributions (e.g. Ubuntu) install Python without installing pip.
Please install it before. If you don't have root privileges, download the
get-pip.py script at https://bootstrap.pypa.io/get-pip.py and execute it as
``python get-pip.py --user``.