import hashlib
import os
import platform
import sys
import warnings
from datetime import datetime
from os import listdir
from os.path import dirname, join
from urllib.parse import urlparse

import yaml
from babel.dates import format_date as fd


def load_env(path='default'):
    directory = dirname(__file__)
    if path == 'default':
        name = join(directory, '../.env')
    else:
        name = path
    with open(name, encoding='utf-8') as f:
        env = f.readlines()
    env_vars = {}
    for var in env:
        n = var.split('=')
        env_vars.update({n[0]: n[1].rstrip()})
    return env_vars


def app_config():
    try:
        with open('tir.yml', encoding='utf-8') as f:
            config = yaml.safe_load(f.read().encode('utf-8'))
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
    if extensions is not None:
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


def _(text):
    translations = {
        'created': 'créé',
        'updated': 'mis à jour',
        'modified': 'modifié',
        'status': 'statut',
        'confidence': 'confiance',
        'difficulty': 'difficulté'
    }
    if text in translations:
        return translations[text]
    return text


def url_for(route, slug=None, filename=''):
    if route == 'index':
        return '/'
    if route == 'post':
        return slug + '.html'
    elif route == 'static':
        return '{}/{}'.format('static', filename)


def format_date(value):
    try:
        d = datetime.strptime(value, '%Y-%m-%d')
        return fd(d, locale='fr')
    except (ValueError, TypeError):
        return value


def n_bit_hash(string: str, n: int) -> int:
    return int(hashlib.blake2b(string.encode('utf-8')).hexdigest(), 16) % 10 ** n


def get_domain(url: str, include_ext=True) -> str:
    domain = urlparse(url).netloc
    if domain.startswith('wwww.'):
        domain.strip('www.')
    domain_l = domain.split('.')
    if len(domain_l) > 2:
        domain_l.pop(0)
        if not include_ext:
            domain_l.pop(1)
        domain = '.'.join(domain_l)
    return domain
