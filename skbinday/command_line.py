import argparse
import pkg_resources
from skbinday.skbinday import run


def main():
    arg_parser = argparse.ArgumentParser()

    arg_parser.add_argument(
        '--version', '-v',
        action='version',
        version=pkg_resources.require('skbinday')[0].version
    )

    arg_parser.add_argument(
        '--urn', '-u',
        help="Stockport URN for your address"
    )

    args = arg_parser.parse_args()

    run(args.urn)


if __name__ == '__main__':
    main()
