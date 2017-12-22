import os

import pytest
import manuel.ignore
import manuel.codeblock
import manuel.doctest
import manuel.testing


def make_manuel_suite(ns):
    """
    Prepare Manuel test suite.

    Test functions are injected in the given namespace.
    """

    # Wrap function so pytest does not expect an spurious "self" fixture.
    def _wrapped(func, name):
        wrapped = lambda: func()
        wrapped.__name__ = name
        return wrapped

    # Collect documentation files
    cd = os.path.dirname
    path = cd(cd(cd(cd(__file__))))
    doc_path = os.path.join(path, 'docs')
    readme = os.path.join(path, 'README.rst')
    files = sorted(os.path.join(doc_path, f) for f in os.listdir(doc_path))
    files = [f for f in files if f.endswith('.rst') or f.endswith('.txt')]
    files.append(readme)

    # Create manuel suite
    m = manuel.ignore.Manuel()
    m += manuel.doctest.Manuel()
    m += manuel.codeblock.Manuel()

    # Copy tests from the suite to the global namespace
    suite = manuel.testing.TestSuite(m, *files)
    for i, test in enumerate(suite):
        name = 'test_doc_%s' % i
        ns[name] = pytest.mark.documentation(_wrapped(test.runTest, name))
    return suite

try:
    make_manuel_suite(globals())
except OSError:
    print('Documentation files not found: disabling tests!')
