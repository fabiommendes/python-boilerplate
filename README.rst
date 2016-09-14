.. image:: https://travis-ci.org/fabiommendes/python-boilerplate.svg?branch=master
    :target: https://travis-ci.org/fabiommendes/python-boilerplate

.. image:: https://coveralls.io/repos/github/fabiommendes/python-boilerplate/badge.svg?branch=master
    :target: https://coveralls.io/github/fabiommendes/python-boilerplate?branch=master


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

We start a python-boilerplate skeleton by calling the ``python-boilerplate init``
command on the root directory of your project. It creates the following tree::

    .
    |- .gitignore
    |- LICENSE
    |- MANIFEST.in
    |- INSTALL.rst
    |- README.rst
    |- VERSION
    |- requirements.txt
    |- setup.py
    |- docs/
    |   |- index.rst
    |   |- apidoc.rst
    |   |- changelog.rst
    |   |  ...
    |   |- conf.py
    |   |- make.bat
    |   |- Makefile
    |   |- _static/*
    |   \- _templates/*
    \- src/
        \- <project>
            |- __init__.py
            |- __meta__.py
            |- <project>.py
            \- tests/
                |- __init__.py
                |- __meta__.py
                \- test_<project>.py


setup.py
--------

The main entry point for installation and management of your project. We provide
a minimum working script based on setuptools. In order to avoid duplication of
work, the setup.py script reuses the project description from the README.rst
file and versioning is controlled by a separate VERSION file. Users still have
to edit this file and provide the short description of the project.

Don't forget to ``python setup.py register`` your project to PyPI before it is
too late!


src/*
-----

python-boilerplate separates the source code for your project under the ``src/``
folder. This contrasts with another typical approach of leaving the python
packages directly in the root of the the source tree. We believe that this
approach creates projects that are more organized and manageable in the long
run.

We also create a "<package>.tests" module for the unit tests and distribute it
with the main package. The drawback of this approach is a slightly larger
distribution. In most systems, this small price is greatly offset by the ability
to ask users to easily run tests in bug reports. python-boilerplate creates a
``__main__.py`` file in the tests package so users can run the test suite simply
by  calling ``python -m <package>.tests``.

docs/*
------

python-boilerplate creates the skeleton for a Sphinx_-based documentation. The
documentation reuses both the README.rst and INSTALL.rst files. In most cases,
it is probably a good idea to create a relatively small README.rst file with a
small overview of your project and leave most details of the documentation to
specific files inside the ``docs/`` directory.

The README.rst file in python-boilerplate itself is perhaps too big ;-)

_ Sphinx: https://sphinx-doc.org


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
the correct version in the <package>.__version__ attribute in your module.

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

Defines files to be included in the source distributions created by setuptools.

LICENSE
-------

Python boilerplate accepts the most common open source licenses (or at least it
should). If the license you want to use is not supported, we gladly accept
patches!

.gitignore
----------

The default .gitignore excludes python bytecode and all build directories.


