import hashlib
import os
import platform
import shutil
import warnings
from datetime import datetime
from os import listdir
from os.path import dirname, join

<<<<<<< HEAD
=======
from babel.dates import format_date as fd

>>>>>>> 0.5.0
import yaml

import sys


def load_env(path='default'):
    directory = dirname(__file__)
    if path == 'default':
        name = join(directory, '../.env')
    else:
        name = join(directory, 'path')
    with open(name) as f:
        env = f.readlines()
    env_vars = {}
    for var in env:
        n = var.split('=')
        env_vars.update({n[0]: n[1].rstrip()})
    return env_vars


def app_config():
    try:
        with open('tir.yml') as f:
<<<<<<< HEAD
            config = yaml.load(f.read().encode('utf-8'), Loader=yaml.FullLoader)
=======
            config = yaml.safe_load(f.read().encode('utf-8'))
>>>>>>> 0.5.0
        return config
    except FileNotFoundError:
        warnings.warn('No configuration file was found.')


def remove_list_meta(meta):
    """ Extract first and single element of list from meta dic
    :rtype: dict
    """
    if isinstance(meta, dict):
        for mk, mv in meta.items():
            if isinstance(mv, list) and len(mv) == 1:
                meta[mk] = mv[0]
    return meta


def is_windows():
    return sys.platform.startswith("win") or (sys.platform == "cli" and os.name == "nt")


def is_linux():
    return platform.system() == 'Linux'


def scan_dir(directory=None, extensions=None):
    """
    Scan a directory for files with a specific or list of extensions then return matching results

    :param directory: absolute path to directory to scan
    :type directory: str
    :param extensions: extensions to search for
    :type extensions: list
    """
    matches = []
    extensions = ['.' + ext for ext in extensions]
    files = listdir(directory)
    for file in files:
        if extensions is not None:
            for extension in extensions:
                if file.endswith(extension):
                    matches.append(join(directory, file))
        else:
            matches.append(join(directory, file))
    return matches


def mktree(path):
    if not os.path.exists(path):
        os.makedirs(path)


def url_for(route, slug=None, filename=''):
    if route == 'index':
        return '/'
    if route == 'post':
        return slug + '.html'
    elif route == 'static':
        return '{}/{}'.format('static', filename)


def format_date(value):
    d = datetime.strptime(value, '%Y-%m-%d')
    return fd(d, locale='fr')


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
<<<<<<< HEAD
=======


def n_bit_hash(string: str, n: int) -> int:
    return int(hashlib.blake2b(string.encode('utf-8')).hexdigest(), 16) % 10 ** n
>>>>>>> 0.5.0
