def yn_input(text, yes='yes', no='no', default='yes'):
    """Asks a yes/no question and return the answer."""

    suffix = ' [%s/%s] ' % (yes[0].upper(), no[0])
    while True:
        ans = input(text + suffix).lower()
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
    """Like yn_input, but the default choice is 'no'."""

    return yn_input(text, yes, no, default=no)


def default_input(text, default):
    """Asks for some input with a default string value."""

    default = str(default)
    return input('%s [%s] ' % (text, default)) or default
