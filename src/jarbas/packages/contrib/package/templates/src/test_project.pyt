import pytest
import {{ package }}


def test_project_defines_author_and_version():
    assert hasattr({{ package }}, '__author__')
    assert hasattr({{ package }}, '__version__')

