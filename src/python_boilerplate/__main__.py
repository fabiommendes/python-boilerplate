from python_boilerplate import commands


def main(args=None):
    args = commands.parser.parse_args(args)
    try:
        func = args.func
    except AttributeError:
        pass
    else:
        func(args)

if __name__ == '__main__':
    main()