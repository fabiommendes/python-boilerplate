import os

import pytest

from jarbas.cli import main
from jarbas.testing import capture_interaction

INTERACTION = (
    "Full name [jarbas_user]: John\n"
    "Email [jarbas_user@domain.com]: john@apple.co.uk\n"
    "PyPI account [jarbas_user]: \n"
    "Github account [jarbas_user]: \n"
    "Dockerhub account [jarbas_user]: \n\n"
    "Global config successfully updated!\n"
)


@pytest.yield_fixture
def project_dir(temp_fs):
    old_cwd = os.getcwd()
    try:
        path = temp_fs.makedir('project')
        os.chdir(path.getsyspath('/'))
        yield path
    finally:
        os.chdir(old_cwd)


def test_new_project_command(project_dir):
    inputs = [''] * 12
    with capture_interaction(inputs, echo=True) as msg:
        main(['new-project', '.'])

    print(msg())
    assert False
