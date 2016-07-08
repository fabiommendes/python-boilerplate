from invoke import run, task


@task
def build(no_docs=False):
    """
    Build python package and docs.
    """

    run("python setup.py build")
    if not no_docs:
        run("python setup.py build_sphinx")


@task
def bump_version(major=False, minor=False, micro=False):
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


#
# Incomplete tasks
#
@task
def tests():
    """Run the pytest test suit"""
    print('not ready...')


@task
def coverage():
    """Run test code coverage"""
    print('not ready...')


@task
def lint():
    """
    Run the linter
    """
    print('not ready...')


@task
def diagnose():
    print('not ready...')


@task
def publish():
    print('not ready...')


@task
def release():
    print('not ready...')

@task
def release_check():
    print('not ready...')


@task
def clean(no_docs=False, no_ext=False):
    """Clean all build files: docs, C extensions, bytecode, etc"""

    print('not ready...')


@task
def http_serve():
    print('not ready...')
