.. image:: https://travis-ci.org/fabiommendes/python-boilerplate.svg?branch=master
    :target: https://travis-ci.org/fabiommendes/python-boilerplate

.. image:: https://coveralls.io/repos/github/fabiommendes/python-boilerplate/badge.svg?branch=master
    :target: https://coveralls.io/github/fabiommendes/python-boilerplate?branch=master

======
Jarbas
======

Jarbas is a workflow automation tool that takes care of many of your projects
chores so that you can spend more time doing things that matter:

* Coding new features;
* Writing more tests;
* Creating great documentation;
* Investigating new algorithms and possibilities;

instead of the "necessary evils" of software development, such as

* Writing repetitive boilerplate to support tools;
* Writing readmes, changelogs, and other info that makes your project a good
citizen in the open source community;
* Searching for obscure git command options to fix a messed up commit;
* Spend an hour going through a long manual "checklist" because you want to
to make a bugfix release, then discoverd you missed an important step and will
have to do another release;
* Tweaking Dockerfiles and continuous integration configurations until
they finally work;
* etc, etc, etc...

With Jarbas, we can automate many chores and minimize the chance of errors
during a project lifecycle. The goal is to be sufficiently opinionated that we
can expect a predictable workflow amenable to automation, but is still be
lightweight enough that users can do things by themselves, if they want. Most of
Jarbas functionality is implemented using plugins, so if you want things to behave
a little bit differently, you can implement your own plugins or modify existing
ones.


Getting started
===============

The first step as a Jarbas user is to configure the global settings

.. code-block:: shell

    $ jarbas config

The tool will ask you a few questions and it will store the answers for later use.

After the global configuration is done, you can create Jarbas new projects. Go
to the folder where the project is located (or create one if the project does
not exist) and type the command

.. code-block:: shell

    $ jarbas new-project .

After you fill up a few questions, you will have a bare-bones Jarbas project.
It provides a very basic structure, with configurations, a task.py script and
a git repository. It does not even provide a basic Python package structure (as
Jarbas can also be used to manage projects written in other programming languages).

You probably will want to provide a little more structure to your project.
Jarbas has a plugin system in which each plugin is responsible to add some
specific functionality to a working project. Say we want to start a Python
project, hence we want a basic package structure that is compatible with PyPI.
Jarbas provides the scaffold via the core/python-package plugin:

.. code-block:: shell

    $ jarbas install core/python-package

Just as before, it will ask a few questions and create the necessary files under
your project structure.

The default scaffold is intentionally very minimalistic and provides a basic
configuration for Python packaging and does not do much more. Jarbas has the
philosophy that things should **Just Work (tm)** with minimal effort. After the
initial setup of the core/python-package plugin, for instance, your package should
be ready to be deployed to PyPI with a simple command. Add the Docker plugin,
and it will provide working Docker images. Add the CI package, and you project
will successfully build on Travis.

Jarbas assumes that project management tasks are controlled by invoke, which is
a neat Python tool similar to the venerable Unix **Make**. Most functionality
is provided by invoke tasks, for instance,

.. code-block:: shell

    $ inv publish

should run a series of sanity checks and, if everything goes well, will publish
your package on Git. We provide a series of standard tasks when a project is
created, and each plugin can add its own set of tasks.


Jarbas workflow
===============




How does it work on practice?

Let us start with a working session of a Jarbas project. Open a terminal window
and hit ``$ jarbas hello <project name>``. That will put you on the correct
folder and initialize a few things such as activating the correct virtualenv
and maybe setting a few environment variables and executing other small chores.
Code, code, code.  When you are done with work, type ``$ jarbas goodbye``. It
will make sure you don't have any pending activities and, if so, it will direct
you to quick solutions (such as making a pending commit and running tests to
ensure everything is still working).


What Jarbas can do for me?
~~~~~~~~~~~~~~~~~~~~~~~~~~

On its own, not very much ;)

Jarbas is built on top of a few great tools and tries its best to integrate
them:

* Git for version control;
* Docker for making predictable runtimes;
* Cookiecutter for creating scaffolds;
* Invoke for running tasks;
* A plugin system to make things extensible;

So must of work is actually done by Jarbas plugins and it depends heavily in
what the plugin aims to support. Plugins can create new scaffolds, expose
specific tasks and point to specially created docker images that guarantees
that tools behave as expected.

Since all Jarbas projects depend on those tools let us cover some of those
generic tasks:

**inv setup**
This will fetch all required dependencies (e.g., by using pip install) and will
configure the project for starting development.


**inv run**
This will run the main executable of your project. If there is no natural
executable, it will fire the test suite.


**inv sync-remote**
This task assumes that the project has (possibly equal) origin and upstream
repositories. It will fetch from origin ???


**inv publish**
This will commit the last changes and push them to origin.


**inv release**
This will commit the last changes and push them to origin.




Jarbas vs. cookiecutter
-----------------------

Since Jarbas helps you to scaffold the basic structure of your package, it is
natural to compare it to the excellent cookiecutter library. As a matter of fact,
Jarbas depends on cookiecutter and uses it internally to scaffold projects. It
however differs from cookiecutter in some significant aspects:

* Jarbas provides a way to increment your project gradually by composing
different jarbas-aware cookiecutters. We call those cookiecutters "nibs".
* While Jarbas strives to be reasonably flexible and generic, it assumes more
about your project structure than cookiecutter. For instance, Jarbas requires
a configuration file and largely assumes that git is used for version control,
and invoke is used for task management.
* Nibs are distributed as regular Python packages and have well defined
cookiecutter and Python interfaces. Each nib registers hooks using setuptools's
entry_points that can specify custom behavior and dependencies. Differently from
cookicutters, NIbs are not directly fetched from git repos, but must be
installed with pip.
* Jarbas can (and often) provide multiple nibs in a single repository.
* We don't like very much how cookiecutter gathers information from the users,
so we reworked this part in Jarbas.
* More to the point, Jarbas helps you to manage your workflow after the project
is created while cookiecutter just creates the initial scaffold.


**Jarbas packages**

A package is a Python package that can produce a cookiecutter scaffold. Packages
are designed to be freely combinable inside an existing project.

When developing a new package, the author must pay attention to some key
differences compared with cookiecutter:

**Packages are more strict**

Cookiecutter provides a lot of flexibility that Jarbas packages do not support.
A few important points should be kept in mind:

* The root folder of your project should always be called '{{cookiecutter.project_slug}}'
* The cookiecutter.json file must contain a field named ``"_jinja2_ext": ["jarbas.jinja2"]``
(you can require additional extensions, but jarbas.jinja2 must be always present).
* pre_install and post_install hooks must always be Python 3.4+ scripts.
* Jarbas does not necessarely use information from cookiecutter.json.
* The pre and post install hooks are declared in the Python package part of
the package and not as standalone scripts. You can provide those scripts, but
they will be ignored during the scaffold creation.

**Packages require additional files**

Your

**Packages can provide extra hooks**

Cookiecutter provides a pre_install_hook.py and a


**Packages declare dependencies**

sdfsdf


**Groups of packages must be distributed as python packages**


**package execution workflow**

Think of a package as an scaffold for producing cookiecutters (which will then
produce resources to your project). The package engine starts by loading a Python
package that has a ``cookiecutter-data`` subfolder. This folder is mostly a
regular cookiecutter project which you can even use independently from Jarbas.

However, Jarbas never execute this cookiecutter directly. Instead, it creates a
temporary folder (usually under <project>/build/tmp/<package name>-package/) and
starts the process of generating a customized cookiecutter.

* First, it calls the ``<package>.prepare_empty(project_conf, tmp_folder)``
function inside your package that may execute any number of arbitrary
preparations for the empty temporary build project. The default behavior is to
do nothing in this stage.

* It then calls the ``<package>.prompt_user(initial_conf, project_conf, tmp_folder)``
function which will ask any number of questions to the user and return a
dict used to construct the cookiecutter.json file in the destination folder.

* Jarbas calls the ``<package>.prepare_cookiecutter(package_conf, project_conf, tmp_folder)``
hook for finalizing the cookiecutter template. This function can take any number
of actions based on the user input stored in the package_conf dictionary.

* Finally, Jarbas creates the ``<project>/build/tmp/<package name>-build/`` folder
and run cookiecutter with the ``--no-input`` flag to create the scaffold that
should be merged into your project.

* Jarbas replaces the pre_build_hook.py and post_build_hook.py files to call
the ``<package>.pre_build_hook(package_conf, project_conf, tmp_folder)`` and
``<package>.post_build_hook(package_conf, project_conf, tmp_folder)`` functions in
your package package.

* When the scaffold is ready, Jarbas starts the task of merging each file
generated into the project main tree. The process proceeds as follows:
    - It starts by doing all safe merges, which include all files that either
    do not exist or are identical to existing files in the project.
    -  If there are some unsafe merges to be done, Jarbas will call
    ``<package>.merge_hints(package_conf, project_conf, tmp_folder)``, which must
    return a dictionary from file names to the hint object that should be
    applied to them. Hints are declared in the jarbas.merge_hints package.
    - The default merging strategy is to show a diff of both files and prompt
    the user if he/she wants to keep the current file, replace by the new one or
    use a merge tool to merge both.

* After all files are merged, it updates the config in ``<project>/conf/jarbas.ini``.
and remove the temporary files.



#####

Jarbas is a helpful tool that happily do many code-related chores for you. This
is a brief list of what it can do:

* Create a project boilerplate that can grow with time.
* Suggest tools and ways in which you can improve your code.
* Automate your development pipeline with good tools practices (tests, continuous 
  integration, containerization, continuous deploy, etc)
* And case you are lost, teach you what those buzzwords are and when/why you 
  should care about them :)

Jarbas is both a practical tool and a research project in which can we explore
the limits of automation in software production.


**What do I need?**

Jarbas is Python-based technology and is primarily focused on Python projects.
Partial support for other languages may be provided using plugins, but we focus
only on languages that are likely to be integrated on Python projects (such as C,
Cython, and a bit of Javascript for web development). Jarbas assumes a basic
POSIX tooling and integrates with common Linux specific technologies such as
Docker. Neither have we tested it on Windows or Mac, nor we have the resources
or inclination to maintain a port.

In order to begin a project with Jarbas, simply type the command::

    $ jarbas init

It will ask you a few questions and create a basic skeleton for your project.
It is intentionally a very simple skeleton with only a few files:

* A setup.py script with a few configuration files.
* README.rst and INSTALL.rst files.
* A /src/ folder where you can start your project.

It also initializes a git repository and ask if you want to create a virtualenv.
You will notice that Jarbas is very polite and always explain which steps it is
going to execute and it will even point you to external resources with further
explanations.



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

https://blog.ionelmc.ro/presentations/packaging/#slide:6


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
