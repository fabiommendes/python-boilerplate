import argparse
from python_boilerplate import __version__
from python_boilerplate.config import save_config

parser = argparse.ArgumentParser('python-boilerplate')
parser.add_argument('--version', '-v', action='version',
                    version='%(prog)s ' + __version__)
subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='sub-command help',
)


def register(parser, config_class=None, writer_class=None):
    """
    Decorator that associates a sub-parser command to a function.

        @register(cmd_parser)
        def handler(**kwargs):
            ...
    """

    if config_class or writer_class:
        if not config_class and writer_class:
            raise TypeError('both config_class and writer_class must be given')

        def handler(**kwargs):
            config = config_class(**kwargs)
            writer = writer_class(config)
            config.run()
            writer.run()
            save_config()

        register(parser)(handler)

    def decorator(func):
        def handler(args):
            kwargs = vars(args)
            kwargs.pop('func', None)
            func(**kwargs)

        parser.set_defaults(func=handler)
        return func

    return decorator