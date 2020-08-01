import argparse
import logging

from tir import Tir
from tir.settings import load_settings

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tir CLI')
    parser.add_argument('command', nargs='?', help='command to execute',
                        choices=['init', 'build', 'watch'])

    args = parser.parse_args()

    config = load_settings()
    tir = Tir(config)

    if args.command == 'init':
        tir.init()
    if args.command == 'build':
        tir.build()
    if args.command == 'watch':
        tir.watch()
