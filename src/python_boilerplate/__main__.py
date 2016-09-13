import argparse
import python_boilerplate
from python_boilerplate import __version__


def get_parser():
    """
    Creates a new argument parser.
    """

    parser = argparse.ArgumentParser('python-boilerplate')
    parser.add_argument('--version', '-v', action='version',
                        version='%(prog)s ' + __version__)
    return parser

def main(args=None):
    """
    Main entry point for your project.

    Args:
        args : list
            A of arguments as if they were input in the command line. Leave it None
            use sys.argv.
    """

    parser = get_parser()
    args = parser.parse_args(args)

    # Put your main script logic here
    print('List of arguments:')
    print(args)


if __name__ == '__main__':
    main(['-h'])