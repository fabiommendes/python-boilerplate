Starting a new Python project from the scratch is boring and error prone:
    * Create a setup.py script
    * Configure documentation
    * Provide installation instructions
    * A README file
    * etc...

This time-consuming and error prone work gives little satisfaction, but is
necessary to make your project a good citizen in the open source community.

Boilerplate produces skeletons for your Python projects so you can get up and
running fast. It is influenced by this blog post:
http://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/,
although we do not follow these recommendations by the letter.


The filesystem structure
========================

The ``python-boilerplate init [<project>]`` command will create the following
tree under the current directory::

    .
    |- .gitignore
    |- LICENSE
    |- MANIFEST.in
    |- INSTALL.rst
    |- README.rst
    |- VERSION
    |- requirements.txt
    |- requirements-dev.txt
    |- setup.py
    |- docs/
    |   |- conf.py
    |   |- index.rst
    |   |- make.bat
    |   |- Makefile
    |   |- _static/*
    |   \- _templates/*
    \- src/
        \- <project>
            |- __init__.py
            |- __meta__.py
            |- <project>.py
            \- test/
                |- __init__.py
                \- test_<project>.py


setup.py
--------

...


src/*
-----

...

docs/*
------

...

README.rst and INSTALL.rst
--------------------------

We provide a default INSTALL.rst file with generic installation instructions for
Python packages. Unless your project requires something fancy, this probably can
be left as is.

The README.rst file, however, provides a detailed overview of your project.
You should edit this file to provide a meaningful description, otherwise a not so
flattering default will be used. The contents of README.rst are also displayed in
the index page of the project's documentation.


VERSION
-------

Your project's version is conveniently centralized in a single file. The
setup.py script uses this value to register you package and it also saves
the correct version in the package.__version__ attribute in your module.

You may bump versions using an invoke task::

    $ inv bump-version

This method assumes that the version string is in the form "<major>.<minor>.<micro>".

requirements.txt
----------------

The requirements.txt uses the ``- e .`` directive to tell pip to search for the
requirements in the setup.py script. As a general rule, dependencies should be
specified only in the ``install_requires`` flag in your setup.py.

You may want to use your requirements.txt to freeze packages to specific
versions by adding lines such as::

    my-package==1.2.3

Freezing makes sense for packages that are meant to run only on their own private
environments such as a Django project running in it own virtualenv or docker container.

MANIFEST.in
-----------

...

LICENSE
-------

...

.gitignore
----------

...


