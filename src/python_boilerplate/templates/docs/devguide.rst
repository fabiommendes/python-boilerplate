=================
Developer's guide
=================

.. topic:: Abstract

   This document describes the development process of {{ project }}. You can
   make a local copy of the repository with::

      git clone git://github.com/{{ github_user }}/{{ github_name }}

.. rubric:: Community

   Please go to https://github.com/{{ github_page }}/ to
   participate.

.. If your project is large enough, you might want to create an structure like
   the one bellow. Until then, all action can take place at Github.
   {% set slug = pyname|replace('_', '-') %}

.. {{slug}}-users <{{slug}}-users@googlegroups.com>
       Mailing list for user support.

.. {{slug}}-dev <{{slug}}-dev@googlegroups.com>
       Mailing list for development related discussions.

.. #{{slug}}-doc on irc.freenode.net
      IRC channel for development questions and user support.


Bug Reports and Feature Requests
--------------------------------

If you have encountered a problem with {{ project }} or have an idea for a new
feature, please submit it to the `issue tracker`_ on Github.

For bug reports, please execute the command ``python -m {{ pyname }}.tests`` and
check if all tests fail. You must have all development dependencies installed,
which can be obtained through pip executing ``pip install {{project}}[dev]``.
Of course, you might want to adapt these commands to the correct python/pip
versions installed in you system.

.. _`issue tracker`: https://github.com/{{ github_page }}/issues


Non coding contributions
------------------------

Besides code and bug reports, you can also contribute with this project by
writing documentation.

Contributing to {{project}}
----------------{{project|line('-')}}

The recommended way for new contributors to submit code is to fork
the repository on Github and then submit a pull request after
committing the changes.  The pull request will then need to be approved by one
of the core developers before it is merged into the main repository.

#. Check for open issues or open a fresh issue to start a discussion around a
   feature idea or a bug.
#. If you feel uncomfortable or uncertain about an issue or your changes, feel
   free to contact us on git.
#. Fork `the repository`_ on Github to start making your changes to the
   **master** branch for next major version, or **stable** branch for next
   minor version.
#. Write a test which shows that the bug was fixed or that the feature works
   as expected.
#. Send a pull request and bug the maintainer until it gets merged and
   published. Make sure to add yourself to AUTHORS_ and the change to
   CHANGES_.

.. _`the repository`: https://github.com/{{ github_page }}/
.. _AUTHORS: https://github.com/{{ github_page }}/blob/master/AUTHORS
.. _CHANGES: https://github.com/{{ github_page }}/blob/master/CHANGES


Getting Started
~~~~~~~~~~~~~~~

These are the basic steps needed to start developing on {{project}}.

#. Create an account on Github.

#. Fork the main repository (`{{ github_page }}
   <https://github.com/{{ github_page }}/>`_) using the Github interface.

#. Clone the forked repository to your machine. ::

       git clone https://github.com/USERNAME/{{ github_name }}
       cd {{ github_name }}

#. Checkout the appropriate branch.

   For changes that should be included in the next minor release (namely bug
   fixes), use the ``stable`` branch. ::

       git checkout stable

   For new features or other substantial changes that should wait until the
   next major release, use the ``master`` branch.

#. Optional: setup a virtual environment. ::

       virtualenv ~/{{ pyname }}env
       . ~/{{ pyname }}env/bin/activate
       pip install -e .

#. Create a new working branch.  Choose any name you like. ::

       git checkout -b feature-xyz

#. Hack, hack, hack.

   For tips on working with the code, see the `Coding Guide`_.

#. Test, test, test.  Possible steps:

   * Run the unit tests::

       pip install pytest mock
       inv test.run

   * Build the documentation and check the output for different builders::

       inv doc.build

   * Run the unit tests under different Python environments using
     :program:`tox`::

       pip install tox
       tox -v

   * Add a new unit test in the ``tests`` directory if you can.

   * For bug fixes, first add a test that fails without your changes and passes
     after they are applied.

#. Please add a bullet point to :file:`CHANGES` if the fix or feature is not
   trivial (small doc updates, typo fixes).  Then commit::

       git commit -m '#42: Add useful new feature that does this.'

   Github recognizes certain phrases that can be used to automatically
   update the issue tracker.

   For example::

       git commit -m 'Closes #42: Fix invalid markup in docstring of Foo.bar.'

   would close issue #42.

#. Push changes in the branch to your forked repository on Github. ::

       git push origin feature-xyz

#. Wait for a core developer to review your changes.


Core Developers
~~~~~~~~~~~~~~~

The core developers of {{ project }} have write access to the main repository.  They
can commit changes, accept/reject pull requests, and manage items on the issue
tracker.

You do not need to be a core developer or have write access to be involved in
the development of {{ project }}.  You can submit patches or create pull requests
from forked repositories and have a core developer add the changes for you.

The following are some general guidelines for core developers:

* Questionable or extensive changes should be submitted as a pull request
  instead of being committed directly to the main repository.  The pull
  request should be reviewed by another core developer before it is merged.

* Trivial changes can be committed directly but be sure to keep the repository
  in a good working state and that all tests pass before pushing your changes.

* When committing code written by someone else, please attribute the original
  author in the commit message and any relevant :file:`CHANGES` entry.


Coding Guide
------------

* Try to use the same code style as used in the rest of the project.  See the
  `Pocoo Styleguide`__ for more information.

  __ http://flask.pocoo.org/docs/styleguide/

* For non-trivial changes, please update the :file:`CHANGES` file.  If your
  changes alter existing behavior, please document this.

* New features should be documented.  Include examples and use cases where
  appropriate.  If possible, include a sample that is displayed in the
  generated output.

* Add appropriate unit tests.


Debugging Tips
~~~~~~~~~~~~~~

* Set the debugging options in the `Docutils configuration file
  <http://docutils.sourceforge.net/docs/user/config.html>`_.
