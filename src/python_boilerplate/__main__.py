import argparse

parser = argparse.ArgumentParser('boilerplate')
parser.add_argument('--version', '-v', action='version')
subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='sub-command help',
)

# Decorator sets the function as a handler for the given command
setfunc = lambda P: (lambda func:  P.set_defaults(func=func) or func)

# python-boilerplate new <project>
cmd_new = subparsers.add_parser('new', help='create a new project')
cmd_new.add_argument('project', help='Your Python Boilerplate project\' name')
cmd_new.add_argument('--author', '-a', help='author\'s name')
cmd_new.add_argument('--email', '-e', help='author\'s e-mail')
cmd_new.add_argument('--license', '-l', help='project\'s license')
cmd_new.add_argument('--version', '-v', help='project\'s version')


@setfunc(cmd_new)
def command_new(args):
    from python_boilerplate.core import ProjectFactory

    kwargs = vars(args)
    del kwargs['func']

    factory = ProjectFactory()
    factory.update(**{k: v for k, v in kwargs.items() if v is not None})
    factory.new_project()


# python-boilerplate enable <feature>
cmd_enable = subparsers.add_parser('enable',
                                   help='enable features in your projects')
cmd_enable.add_argument('feature', help='feature name')


@setfunc
def command_enable(args):
    from python_boilerplate.core import ProjectFactory

    kwargs = vars(args)
    del kwargs['func']

    factory = ProjectFactory()
    factory.enable_feature(**kwargs)


def main(args=None):
    args = parser.parse_args(args)
    try:
        func = args.func
    except AttributeError:
        pass
    else:
        func(args)

if __name__ == '__main__':
    main()