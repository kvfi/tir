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
import os
from datetime import datetime

from tir.settings import REQUIRED_PATHS

log = logging.getLogger(__name__)


def url_for(route, slug=None, filename=''):
    if route == 'index':
        return '/'
    if route == 'post':
        return slug + '.html'
    elif route == 'static':
        return '{}/{}'.format('static', filename)


def format_date(date, date_format="%d/%m/%Y", suffix=False):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(date_format)


def mktree(path):
    if not os.path.exists(path):
        os.makedirs(path)


def _(text):
    return text


def is_init() -> bool:
    paths = all([os.path.exists(el) for el in REQUIRED_PATHS])
    if paths:
        return True
    else:
        log.info('A Tir project already exists at this location.')
        return False
