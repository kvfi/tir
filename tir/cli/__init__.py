import argparse
import logging

from tir import Tir, init
from tir.settings import load_settings

log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Tir CLI')
    parser.add_argument('command', nargs='?', help='command to execute',
                        choices=['init', 'build'])

    args = parser.parse_args()

    config = load_settings()
    tir = Tir(config)

    if args.command == 'init':
        init()
    if args.command == 'build':
        tir.build()
