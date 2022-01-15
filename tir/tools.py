"""
todos:
* create html directory if doesn't exist
* format date in meta
* check if toc is rendered
* get stats at the end of build
* make configurable options: github, website, url, http/https, templates
* remove personal files and replace with samples (logo, ...)
* don't remove tir.yml if it already exists
"""

import logging
import ntpath
import os

from csscompressor import compress

from tir.config import REQUIRED_PATHS

log = logging.getLogger(__name__)


def is_init() -> bool:
    if all([os.path.exists(el) for el in REQUIRED_PATHS]):
        return True
    else:
        log.info('A Tir project already exists at this location.')
        return False


def minify_file(path: str) -> str:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    css = compress(content)

    with open(path, 'w+') as f:
        f.write(css)

    return ntpath.basename(path)
