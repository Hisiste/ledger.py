#!/usr/bin/env python3
from utils.args import get_arguments, test_args
from utils.read_file import read_ledger

def main():
    args = get_arguments()
    test_args(args)

    if args.files:
        for file in args.files:
            result = read_ledger(file)

    if args.verb == 'print':
        for ent in result:
            print(ent)


if __name__ == '__main__':
    main()
