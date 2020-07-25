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
<<<<<<< HEAD
import os
import shutil
from datetime import datetime

=======
import ntpath
import os

from csscompressor import compress

from tir.settings import REQUIRED_PATHS
from tir.utils import n_bit_hash

>>>>>>> 0.5.0
log = logging.getLogger(__name__)


def url_for(route, slug=None, filename=''):
    if route == 'index':
        return '/'
    if route == 'post':
        return slug + '.html'
    elif route == 'static':
        return '{}/{}'.format('static', filename)


<<<<<<< HEAD
def format_date(date, date_format="%d/%m/%Y", suffix=False):
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime(date_format)


def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(s).st_mtime - os.stat(d).st_mtime > 1:
                shutil.copy2(s, d)


=======
>>>>>>> 0.5.0
def mktree(path):
    if not os.path.exists(path):
        os.makedirs(path)


def _(text):
    translations = {
        'created': 'créé',
        'updated': 'mis à jour'
    }
    if text in translations:
        return translations[text]
    return text


<<<<<<< HEAD
def is_init():
    return os.path.exists('tir.yml')
=======
def is_init() -> bool:
    paths = all([os.path.exists(el) for el in REQUIRED_PATHS])
    if paths:
        return True
    else:
        log.info('A Tir project already exists at this location.')
        return False


def minify_file(path: str) -> str:
    with open(path, 'r') as f:
        content = f.read()

    css = compress(content)
    h = str(n_bit_hash(content, 8))

    minified_file_path = '%s.%s.css' % (path.replace('.css', ''), h)
    with open(minified_file_path, 'w+') as f:
        f.write(css)

    os.remove(path)

    return ntpath.basename(minified_file_path)
>>>>>>> 0.5.0
