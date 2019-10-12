import argparse
import logging

from tir.settings import load_settings
from tir.tools import build, init

log = logging.getLogger(__name__)


def main():
    load_settings()

    parser = argparse.ArgumentParser(description='Tir CLI')
    parser.add_argument('command', nargs='?', help='command to execute',
                        choices=['init', 'build'])
    args = parser.parse_args()

    if args.command == 'init':
        init()
    if args.command == 'build':
        build()
