import click

from jarbas.cli import main
from jarbas.conf.globals import global_config
from jarbas.testing import capture_interaction

INTERACTION = (
    "Full name [user]: John\n"
    "Email [user@domain.com]: john@apple.co.uk\n"
    "PyPI account [user]: \n"
    "Github account [user]: \n"
    "Dockerhub account [user]: \n\n"
    "Global config successfully updated!\n"
)


def test_conf_command(empty_fs):
    inputs = [
        'John',  # name
        'john@apple.co.uk',  # email
        '',  # PyPI
        '',  # Github
        '',  # Dockerhub
        '',
    ]

    with capture_interaction(inputs, echo=True) as msg:
        main(['config'])

    conf = global_config()
    assert conf.to_json() == {
        'jarbas-accounts': {
            'bitbucket_username': 'user',
            'dockerhub_username': 'user',
            'github_username': 'user',
            'gitlab_username': 'user',
            'pypi_username': 'user'
        },
        'jarbas-author': {
            'email': 'john@apple.co.uk',
            'full_name': 'John',
            'gender': 'other'
        },
        'jarbas-project-paths': {},
        'jarbas-tools': {'diff_editor': 'meld', 'diff_editor_command': 'meld'}
    }

    pre, sep, msg = msg().partition('Full name')
    msg = click.unstyle(sep + msg)

    assert msg == INTERACTION
