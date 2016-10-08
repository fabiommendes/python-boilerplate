from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import os
import shlex
import sys

from invoke import run, task

from python_boilerplate.tasks.doc import *
from python_boilerplate.config import get_context
from python_boilerplate.tasks import util


@task
def build(ctx, no_docs=False):
    """
    Build python package and docs.
    """

    util.add_src_to_python_path()
    run("python setup.py build")
    if not no_docs:
        run("python setup.py build_sphinx")


@task(name='bump-version')
def bump_version(ctx, major=False, minor=False, micro=False):
    """
    Bump the version number in the VERSION file.
    """

    from distutils.version import LooseVersion

    if major == minor == micro == False:
        micro = True

    with open('VERSION') as F:
        vdata = F.read()
        version = LooseVersion(vdata).version
        version = dict(enumerate(version))

    # Fix major
    if major:
        version[0] += 1
        for k, v in version.items():
            if isinstance(v, int) and not k == 0:
                version[k] = 0

    # Fix minor
    minor_idx = 1
    if minor:
        while isinstance(version.get(minor_idx), str):
            minor_idx += 1
        version[minor_idx] = version.get(minor_idx, 0) + 1

        for k, v in version.items():
            if isinstance(v, int) and k > minor_idx:
                version[k] = 0

    # Fix micro
    micro_idx = minor_idx + 1
    if micro:
        while isinstance(version.get(micro_idx), str):
            micro_idx += 1
        version[micro_idx] = version.get(micro_idx, 0) + 1

        for k in list(version):
            if k > micro_idx:
                del version[k]

    # Reconstruct version string
    vstring = ''
    for (i, v) in sorted(version.items()):
        if i and isinstance(v, int) and isinstance(version[i - 1], int):
            vstring += '.%s' % v
        else:
            vstring += str(v)
    vstring += '\n'

    # Save version
    with open('VERSION', 'w') as F:
        F.write(vstring)
    print('Version bumped from %s to %s' % (vdata.strip(), vstring.strip()))
    return vstring


@task(help={
    'pyall': 'Same as --py2 --py3 together.',
    'py2': 'Force py.test run with Python 2 interpreter.',
    'py3': 'Force py.test run with Python 3 interpreter.'
})
def test(ctx, keywords=None, matches=None, pyall=False, py2=False, py3=False):
    """
    Run py.test.
    """

    pytest_worker(pyall=pyall, py2=py2, py3=py3,
                  keywords=keywords, matches=matches)


@task
def coverage(ctx):
    """
    Run test code coverage.
    """

    pytest_worker(extra_args='--cov=src')


def pytest_worker(pyall=False, py2=False, py3=False,
                  keywords=None, matches=None, extra_args=None):
    """
    Worker function that activates py.test module.
    """

    # Should we scan src/ or src/<package/tests/?
    # name = get_context()['package']
    # test_path = os.path.join('src', name, 'tests')
    test_path = 'src'

    # Normalize options
    pycurrent = False
    if py2 and py3:
        pyall = True
    if pyall:
        py2 = py3 = True
    if not py2 and not py3:
        pycurrent = True
    if py2 and sys.version_info[0] == 2:
        py2 = False
        pycurrent = True
    if py3 and sys.version_info[0] == 3:
        py3 = False
        pycurrent = True

    # Compute extra arguments
    args = []
    if keywords:
        args.extend(['-k', keywords])
    if matches:
        args.extend(['-m', matches])

    # Run py.test using the current interpreter
    if pycurrent:
        import pytest
        util.add_src_to_python_path()
        if extra_args:
            extra_arglist = shlex.split(extra_args)
        else:
            extra_arglist = []
        pytest.main([test_path] + args + extra_arglist)

    if args:
        args = ''
        if keywords:
            args += ' -k ' + shlex.quote(keywords)
        if matches:
            args += ' -m' + shlex.quote(matches)
        if extra_args:
            args += ' ' + extra_args

    # Invoke an external process
    env = {'PYTHONPATH': 'src'}
    args = ' ' + extra_args if extra_args else ''
    if py2:
        run('python2 -m pytest %s%s' % (test_path, args), env=env)
    if py3:
        run('python3 -m pytest %s%s' % (test_path, args), env=env)


@task(help={
    'keep_docs': 'do not remove built documentation',
    'keep_exts': 'preserve compiled C extensions',
})
def clean(ctx, keep_docs=False, keep_exts=False):
    """
    Clean all build files: docs, C extensions, bytecode, etc.
    """

    # Select bad extensions
    bad_extensions = ['.pyc', '.pyo', '.pyd', '.egg', '.egg-info']
    if not keep_exts:
        bad_extensions.extend(['.dll', '.so'])

    for base, dirs, files in os.walk('src'):
        dirs_and_files = dirs + files

        if '__pycache__' in dirs_and_files:
            path = os.path.join(base, '__pycache__')
            rm(path)

        for file in dirs_and_files:
            _, ext = os.path.splitext(file)
            if ext in bad_extensions:
                rm(os.path.join(base, file))


def rm(path, verbose=True):
    """
    Remove file or directory in path.
    """

    if os.path.exists(path):
        if verbose:
            print('removing', path, end=' ')

        if os.path.isdir(path):
            for base, files, dirs in os.walk(path):
                dirs_and_files = dirs + files
                for path in dirs_and_files:
                    path = os.path.join(base, path)
                    rm(path, verbose=False)
        else:
            os.unlink(path)

        if verbose:
            print('...done!')

# @task
# def lint(ctx):
#     """
#     Run the linter
#     """
#     print('not ready...')
#
#
# @task
# def diagnose(ctx):
#     print('not ready...')
#
#
# @task
# def publish(ctx):
#     print('not ready...')
#
#
# @task
# def release(ctx):
#     print('not ready...')
#
#
# @task
# def release_check(ctx):
#     print('not ready...')
#
#
# @task
# def http_serve(ctx):
#     print('not ready...')
