import os

from invoke import task


@task
def install(ctx):
    """
    Invoke ``npm install`` command.

    Install all packages listed in package.json.
    """

    assert_package_json()
    print('Installing npm dependencies...')
    ctx.run('npm install')


@task
def build(ctx):
    """
    Invoke the ``npm build`` command.

    You should configure your static assets builder in the package.json file.
    """

    assert_package_json()
    print('Building bundles...')
    ctx.run('npm build')


@task
def test(ctx):
    """
    Invoke ``npm test`` command.

    You should configure your Javascript test suite in the package.json file.
    """

    assert_package_json()
    print('Testing javascript')
    ctx.run('npm test')


@task
def vulcanize(ctx):
    """
    Vulcanize files and produces main Polymer bundle.

    This command only makes sense on Polymer based projects.
    """


def assert_package_json():
    """
    Assert package.json exists.
    """

    if not os.path.exists('package.json'):
        raise SystemExit('your project does not have a package.json file.')
