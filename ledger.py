#!/usr/bin/env python3
from utils.args import get_arguments, test_args

def main():
    args = get_arguments()
    test_args(args)

    print(args)


if __name__ == '__main__':
    main()
