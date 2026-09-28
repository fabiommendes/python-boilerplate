=========================
Installation instructions
=========================

{{ project }} can be installed using pip::

    $ {% if PY2_ONLY -%}
        python2
      {%- elif PY3_ONLY -%}
        python3
      {%- else -%}
        python
      {%- endif %} -m pip install {{ project }}

This command will fetch the archive and its dependencies from the internet and
install them. {% if PY_BOTH %}You may need to pick either ``python2``` or ``python3`` in
order to select the correct python version.{% endif %}

If you've downloaded the tarball, unpack it, and execute::

    $ python setup.py install --user

You might prefer to install it system-wide. In this case, skip the ``--user``
option and execute as superuser by prepending the command with ``sudo``.


Troubleshoot
------------

Windows users may find that these command will only works if typed from Python's
installation directory.

Some Linux distributions (e.g. Ubuntu) install Python without installing pip.
Please install it before. If you don't have root privileges, download the
get-pip.py script at https://bootstrap.pypa.io/get-pip.py and execute it as
``python get-pip.py --user``.


Development
-----------

If you want to develop for {{ project }}, first clone the git repository with the
command

::

    $ git clonte {{ git_repository }}

After cloning, install the dependencies with::

    $ pip install -e .[dev]

It may also be convenient to install {{ project }} in your system. For doing so,
please use the command

::

    $ python setup.py develop
