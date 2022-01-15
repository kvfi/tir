import argparse
import logging

from tir import Tir, server

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tir CLI')
    group = parser.add_argument_group('test')
    group.add_argument('command',  help='command to execute',
                       choices=['init', 'build', 'watch', 'server', 'deploy', 'test'])

    args = parser.parse_args()

    tir = Tir()

    print(args.command)

    match args.command:
        case 'init':
            tir.init()
        case 'build':
            tir.build()
        case 'deploy':
            tir.deploy()
        case 'watch':
            tir.watch()
        case 'test':
            print('ok')
        case 'server':
            server.run()


if __name__ == '__main__':
    main()
