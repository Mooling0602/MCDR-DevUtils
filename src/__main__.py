#!/usr/bin/env python3
import argparse
import sys

from dev_utils.logger import SimpleLogger


logger = SimpleLogger(prefix="DevUtils")

logger.info("DevUtils is loading as a pyz package.")

def main():
    parser = argparse.ArgumentParser(
        prog='dev_utils',
        description='DevUtils pyz mode.'
    )

    subparsers = parser.add_subparsers(dest='command')

    meta_parser = subparsers.add_parser('meta', help='Generate meta file in json.')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == 'meta':
        from dev_utils.cli import meta
        try:
            meta.main()
        except KeyboardInterrupt:
            print("用户取消输入！")
    else:
        parser.print_help()

if __name__ == '__main__':
    main()