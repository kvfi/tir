import argparse
import logging

from tir import Tir, server

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tir CLI')
    parser.add_argument('command', nargs='?', help='command to execute',
                        choices=['init', 'build', 'watch', 'server'])

    args = parser.parse_args()

    tir = Tir()

    if args.command == 'init':
        tir.init()
    elif args.command == 'build':
        tir.build()
    elif args.command == 'watch':
        tir.watch()
    elif args.command == 'server':
        server.run()
