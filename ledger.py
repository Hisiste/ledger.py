#!/usr/bin/env python3
from utils.args import get_arguments, test_args
from utils.read_file import read_ledger
from utils.register import print_register

def main():
    args = get_arguments()
    test_args(args)

    if args.files:
        result = []
        for file in args.files:
            result += read_ledger(file)

    if args.verb == 'print':
        for ent in result:
            print(ent)

    elif args.verb in ['register', 'reg', 'r']:
        print_register(result)


if __name__ == '__main__':
    main()
