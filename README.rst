.. image:: https://travis-ci.org/fabiommendes/python-boilerplate.svg?branch=master
    :target: https://travis-ci.org/fabiommendes/python-boilerplate

.. image:: https://coveralls.io/repos/github/fabiommendes/python-boilerplate/badge.svg?branch=master
    :target: https://coveralls.io/github/fabiommendes/python-boilerplate?branch=master


Starting a new Python project from the scratch is boring and error prone:
* First create a setup.py script
* Create documentation
* Provide installation instructions
* A README file
* Write tests
* etc, etc, etc.

This time-consuming and error prone work gives little satisfaction, but is
necessary to make your project a good citizen in the open source community.

python-boilerplate produces skeletons for your Python projects so you can get
up and running fast. It is influenced by this blog post:
http://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/,
although we do not follow these recommendations by the letter.


The filesystem structure
========================

We start a python-boilerplate skeleton by calling the ``python-boilerplate init``
command on the root directory of your project. It creates the following tree::

    .
    |- .coveragerc
    |- .gitignore
    |- .travis.yml
    |- LICENSE
    |- MANIFEST.in
    |- INSTALL.rst
    |- README.rst
    |- VERSION
    |- requirements.txt
    |- setup.py
    |- tasks.py
    |- tox.ini
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
        \- <package>
            |- __init__.py
            |- __main__.py
            |- __meta__.py
            |- <package>.py
            \- tests/
                |- __init__.py
                |- __main__.py
                \- test_<package>.py


setup.py
--------

The main entry point for installation and management of your project. We provide
a minimum working script based on setuptools. In order to avoid duplication of
work, the setup.py script reuses the project description from README.rst and
uses the version string in a separate VERSION file. Users still have
to edit this file and provide the short description of the project.

Don't forget to ``python setup.py register`` your project to PyPI before someone
takes it name!


src/*
-----

python-boilerplate puts all source code for your project under the ``src/<package>``
folder. This contrasts with the other typical approach of leaving the python
packages directly in the root of the the source tree. We believe that a separate
src folder is more organized and manageable in the long run.


src/<package>/tests/*
---------------------

We also create a "<package>.tests" module for unit testing and distribute it
with the main package. The drawback of this approach is a slightly larger
distribution. In most systems, this small price is greatly offset by the ability
to ask users to easily run the test suite when dealing with bug reports.
python-boilerplate creates a ``__main__.py`` file in the tests package that
enable anyone can run the test suite simply by calling ``python -m <package>.tests``.

docs/*
------

python-boilerplate creates the skeleton for a Sphinx_-based documentation. The
documentation reuses both the README.rst and INSTALL.rst files. In most cases,
it is probably a good idea to create a relatively small README.rst with a
succinct overview of your project and leave most details of the documentation to
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

You may bump version numbers using an invoke task::

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
environments such as a Django project running in it own virtualenv or docker
container. Avoid freezing package versions in your main Python installation.

MANIFEST.in
-----------

Define files to be included in the source distributions created by setuptools.

LICENSE
-------

Python boilerplate accepts the most common open source licenses (or at least it
should). If the license you want to use is not supported, we gladly accept
patches!

.gitignore
----------

The default .gitignore excludes python bytecode and all build directories.


Tasks
-----

The ``tasks.py`` define some invoke tasks for your project. You can define new
tasks by defining python functions just as the example given in this file. Think
of ``tasks.py`` as a Python replacement of a Makefile: it is used to define
commands that automate repetitive tasks and chores. We define a few general
purpose tasks. They are executed using the inv(oke) command.

``inv test``:
    Runs py.test with the main test suite.
``inv coverage``:
    Runs py.test and display a coverage report.
``inv build``:
    Calls setup.py build and also builds the documentation.
``inv bump-version``:
    Controls the version number in the VERSION file.



Continuous integration
----------------------

python-boilerplate ships a working ``.travis.yml`` file and a ``tox.ini``. You
can use tox to run the test suite for different Python versions locally (but
you'll need several working interpreters simultaneously installed  in your
system).

Assuming that you are hosting your code at Github, enable Travis-CI integration
under "Settings > Integrations and services" option in your main repository
page. Also enable "Coveralls" integration to have good quality reports on code
coverage evolution.

You need to enable support for your repository both in `Travis-CI<https://travis-ci.org>`
and `Coveralls<http://coveralls.io>` websites. Continuous integration tasks
will run every time you *push* something new to Github.
