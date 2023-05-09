import argparse
import sys
from os.path import isfile, exists


def get_arguments():
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='A simple implementation of ledger-cli. Supports only the \
            following commands and flags: `balance`, `register`, `print`, \
            `--sort`, `--price-db` and `--file`.',
        epilog='This implementation is inspired in \
            [ledger-cli](https://ledger-cli.org/).')
    parser.add_argument('-v', '--version',
                        action='version', version='%(prog)s 1.0')

    parser.add_argument('verb', metavar='Action',
                        action='store', nargs='+',
                        help='Specify an action between balance, report and \
                            print.')
    parser.add_argument('-S', '--sort', metavar='value-expression',
                        action='store', dest='sort',
                        help='Sort postings by evaluating the given \
                            value-expression.')
    parser.add_argument('--price-db', metavar='FILE',
                        action='store', dest='price_db',
                        help='Set the FILE that is used for recording \
                            downloaded commodity prices')
    parser.add_argument('-f', '--file', metavar='FILE',
                        action='append', dest='files',
                        help='Read journal data from FILE.')

    my_args = parser.parse_args()
    return my_args


def test_args(my_args):
    # Test if verb is valid.
    valid_verbs = [
        'balance', 'bal', 'b',
        'register', 'reg', 'r',
        'print'
    ]
    if my_args.verb[0] not in valid_verbs:
        raise Exception(f'{my_args.verb[0]} is NOT a valid verb! Valid verbs are: {", ".join(valid_verbs)}.')

    # Test if expression for sorting is valid.
    # TODO: How can we validate an expression???

    # Test if price_db file exists and is a file.
    if my_args.price_db and not exists(my_args.price_db):
        raise Exception(f'Command: `--price-db {my_args.price_db}`. File {my_args.price_db} does NOT exist.')
    elif my_args.price_db and not isfile(my_args.price_db):
        raise Exception(f'Command: `--price-db {my_args.price_db}`. {my_args.price_db} is NOT a file.')

    # Test files.
    if my_args.files:
        if len(my_args.files) == 1 and my_args.files[0] == '-':
            # Check if there's data in stdin.
            #
            # https://stackoverflow.com/questions/53541223/read-python-stdin-from-pipe-without-blocking-on-empty-input
            if sys.stdin.isatty():
                raise Exception(f'Command: --file -. No info from STDIN.')

        else:
            for file in my_args.files:
                if not exists(file):
                    raise Exception(f'Command: `--file {file}`. File {file} does NOT exist.')
                elif not isfile(file):
                    raise Exception(f'Command: `--file {file}`. {file} is NOT a file.')
    else:
        if sys.stdin.isatty():
            raise Exception(f'No info from STDIN. Please specify a file with `--file FILE`.')
