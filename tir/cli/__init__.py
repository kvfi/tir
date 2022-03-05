import argparse
import logging

from tir import Tir, server

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tir CLI')
    group = parser.add_argument_group('test')
    group.add_argument('command', help='command to execute',
                       choices=['init', 'build', 'watch', 'server', 'deploy', 'test'])

    args = parser.parse_args()

    tir = Tir()

    print(args.command)

    if args.command == 'init':
        tir.init()
    elif args.command == 'build':
        tir.build()
    elif args.command == 'deploy':
        tir.deploy()
    elif args.command == 'watch':
        tir.watch()
    elif args.command == 'server':
        server.run()
    else:
        print('Command not found')


if __name__ == '__main__':
    main()
