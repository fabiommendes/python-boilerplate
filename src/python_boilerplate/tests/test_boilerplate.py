import pytest
import boilerplate


def test_boilerplate_script_help():
    from boilerplate.__main__ import main
    main(['-h'])


if __name__ == '__main__':
    pytest.main()