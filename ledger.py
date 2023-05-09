#!/usr/bin/env python3
from utils.args import get_arguments, test_args
from utils.read_file import read_ledger
from utils.register import print_register
from utils.sort import sort_entries
from utils.balance import print_balance
from utils.acc_regex import filter_accounts

def main():
    args = get_arguments()
    test_args(args)

    if args.files:
        result = []
        for file in args.files:
            result += read_ledger(file)

    if len(args.verb) > 1:
        result = filter_accounts(args.verb[1:], result)

    if args.sort:
        sort_entries(result, args.sort)

    if args.verb[0] == 'print':
        for ent in result:
            print(ent)

    elif args.verb[0] in ['register', 'reg', 'r']:
        print_register(result)

    elif args.verb[0] in ['balance', 'bal', 'b']:
        print_balance(result)


if __name__ == '__main__':
    main()
