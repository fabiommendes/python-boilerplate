If you are like me, starting a new Python project from the scratch can be
boring: create a setup.py, documentation, installation instructions, forget a
file or two in the manifest, etc. This all is a time-consuming and error prone
work, which gives no intellectual satisfaction. Yet, this is necessary to make
your project a good citizen in the open source community.

Boilerplate produces beautiful skeletons for your Python projects so you can
get up and running fast. It is influenced by this blog post:
http://jeffknupp.com/blog/2013/08/16/open-sourcing-a-python-project-the-right-way/,
although we do not follow these recommendations by the letter.


The filesystem structure
========================

The ``boilerplate start <project>`` command will create the following tree
under the current directory::

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

src/*
-----

docs/*
------

README.rst and INSTALL.rst
--------------------------


VERSION
-------

requirements.txt
----------------


MANIFEST.in
-----------


LICENSE
-------


.gitignore
----------




