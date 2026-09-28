from collections import deque
from sidekick import Record, field
from lazyutils import lazy


class InstructionsParser(Record):
    """
    A parser for Instruction docstrings.
    """

    def __init__(self, data):
        self.data = data
        self.tokens = deque(data.split())  # better!

    def run(self):
        ...
        return []


def parse_instructions(st):
    """
    Parse a string of instructions.
    """

    parser = InstructionsParser(st)
    return parser.run()


class JobMeta(type):
    def __init__(cls, name, bases, ns):
        if name != 'Job':
            cls.instructions_pipeline = parse_instructions(cls.__doc__)



class Job(metaclass=JobMeta):
    def make_tasks(self):
        pass


class Base(Job):
    """
    Glad to see you here, $info.developer_name|title!

    This basic project template creates a new bare bones Python project. If you
    want to know more and understand the role of each file, please go to
    http://rtfd.org/jarbas/help/base.html.
    
    Developer full name: [full_name = @conf.full_name]
    Email: [email:email = @info.email]
    Project name: [name=str]
    Project version: [version=str:0.1.0]
    Package name: [package=str]
    =if Use virtualenv? [use_virtualenv=bool:True]
    Virtualenv name: [virtualenv=str:@package]
    =endif
    A brief description of your project: [description=str]
    =if Does it have any executable script? [has_scripts=bool:True]
    =endif
    
    Python uses a system of entry points to declare installable scripts during
    installation. Basically, you have to associate each script to a python
    function in the setup.py file. We will create an example for you, that you
    can expand and declare multiple scripts, if necessary (go to http://rtfd.org/jarbas/help/scripts.html)

    = What is the name of the executable command? [entry_point_command=str]
    = To which function it points to? [entry_point_function=str:{{ package + '.__main__:main' }}]
    =endif=

    Congratulations! We are now creating the basic file structure for your
    project. For now on, you can type ``jarbas hello {{ package }}`` to start 
    working with your project and ``jarbas goodbye`` when you are done.
    """

    pre_requisites = ['info']
    

class Package(Job):
    """
    Is your project composed of a single module or do you want to grow it into
    a package? Module-based projects consists of single Python files and are
    recommended only for very simple cases. 
    
    = Do you want to convert your project into a package project? [is_package=bool:True] 

    We moved everything to the src/{{ base.package }} folder. We also created an
    empty __init__.py, to make Python recognize {{ base.package }} as a package
    and a __main__.py file. This script is execute whenever you execute ``python -m <some-module>``.

    This is a nice way to expose your project's functionality and Python uses it
    a lot. (Check, e.g., ``python -m http.server`` or ``python -m pip`` commands.)
    """


class Tests(Job):
    """
    Extensive automatic testing is important to keep the quality and health of 
    your project. If you are new to unit testing and automatic testing, we refer
    to http://rtfd.org/jarbas/help/testing.html.

    I rely on two libraries to automate tests: Pytest and Tox.

    * Install pytest (automate tests)
    * Tox (create isolated enviroment to run tests)

    = Should I proceed? [enable=bool:True]

    Congratulations! I prepared a basic testing infrastructure. You can now 
    edit it and add a few extra tests. In order to run the test suite, simply
    execute the **pytest** command on the command line.   
    """

    pre_requisites = [
        'package',
        'package.is_package',
    ]


class Docs(Job):
    """
    Documentation will live under the /docs/ folder. I will create a basic 
    skeleton there.

    Your documentation requires a few external libraries:

    * Install Sphinx (builds documentation in the ReST format)
    * Install Manuel (tests code fragments on the documentation)
    * Install Sphinx-watch (builds documentation on the "watch" mode)

    = Should I proceed? [enable=bool:True]

    Congratulations! In order to build the documentation, execute::

        $ sphinx build docs/ build/docs/

    If you want further directions and a cheatlist, go to http://rtfd.org/jarbas/help/docs.html 
    """


class Tasks(Job):
    """
    Your project is getting big and could use a bit of automation! 
    
    Check my plan:
    
    * Install the Invoke task runner
    * Create a tasks.py file with tasks a few standard tasks
    * Create a /script/ folder to store more complex scripts 
    
    = Should I proceed? [enable=bool:True]

    Congratulations! Now check http://rtfd.org/jarbas/help/tasks.html to see a
    list of pre-installed tasks. Now that you are at it, execute 
    
        $ inv commit

    in order to commit the changes and push them to the origin repository.
    """

class QA(Job):
    """
    Never too early to care about code quality! I will run a few Python
    that help to keep your code in good shape and style and prevents a lot of
    bugs.

    * Install and prepare flake8 to catch errors
    * Install pylint with a sane default configuration
    * Install doclint? to check for problems with the documentation
    * Install autopep8? to format source code to an specific style  
    
    = Should I continue? [qa_tools=bool:True]

    Lovely! Run all tools and lets fix this mess!

        $ inv qa
    """



class CI(Job):
    """
    There are many free continuous integration services available. I will 
    implement support for the most common ones (check http://rtfd.com/jarbas/help/ci.html):

    Travis (http://travis-ci.com) is the most used continuous integration 
    service for Linux. Travis will run all our tests in several Python
    versions using the tox test runnner. The travis service is free for open 
    source projects and is integrated with github. 

    = Should I run it? [travis=bool:True]
    
    Wonderful! Now register your project at http://travis-ci.com!
    
    ===
    Codecov (http://codecov.io) gathers information about code coverage. This is
    helpful to keep track of lines that are not hit by tests and fix it.
    Codecov is integrated with travis and show nice graphics and statistics
    about code coverage.

    = Should I run it? [codecov=bool:True]

    Wonderful! Now register your project at http://codecov.io!
    
    === 
    Codeclimate (http://codeclimate.io) performs static code analysis to point
    at possible bugs at your code. This is very useful to detect code smells
    and improve the overall quality of your codebase.

    = Should I run it? [codeclimate=bool:True]

    Wonderful! Now register your project at http://codeclimate.io!

    ===
    Appveyor (http://appveyor.com) is a continuous integration service for 
    Windows.

    = Do you want to support Windows? [appveyor=bool:True]
    = Should I prepare your project to automatically build .msi files 
      on passing builds? [msi=bool:True] 
    """


class Docker(Job):
    """
    Docker is useful to create isolated development environments and deployment 
    images. I can do both, shall we?

    Create a development image? [dev:bool = True]
    Create a deployment image? [deploy:bool = True]

    Nice! The next step is to make a the image available at Docker Hub. You can
    tweak a series of parameters and probably should read a little bit about
    the base images I provide at http://rtfd.org/jarbas/help/docker.html.
    """

