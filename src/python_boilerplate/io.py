from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import six

from .compat import unicode


def yn_input(text, yes='yes', no='no', default='yes'):
    """
    Asks a yes/no question and return the answer.
    """

    suffix = ' [%s/%s] ' % (yes[0].upper(), no[0])
    while True:
        ans = grab_input(text + suffix).lower()
        if ans in (yes, no):
            return ans
        elif not ans:
            return default
        elif ans[0] == yes[0]:
            return yes
        elif ans[0] == no[0]:
            return no
        text = '    - please enter %r or %r' % (yes, no)


def ny_input(text, yes='yes', no='no'):
    """
    Like yn_input, but the default choice is 'no'.
    """

    return yn_input(text, yes, no, default=no)


def default_input(text, default):
    """
    Asks for some input with a default string value.
    """

    default = unicode(default)
    return grab_input('%s [%s] ' % (text, default)) or default


def grab_input(msg=''):
    """
    Asks for user input.

    Like the builtin input() function, but has the same behavior in python 2
    and 3.
    """

    if six.PY2:
        # noinspection PyUnresolvedReferences
        return raw_input(msg)
    else:
        return input(msg)


def show(*args, **kwargs):
    """
    Alias to print() function.

    Can be useful in conjunction with mock() in test cases.
    """

    return print(*args, **kwargs)
