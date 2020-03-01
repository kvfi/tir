import logging
import os
import warnings

from yaml import Dumper, FullLoader, load, dump

logger = logging.getLogger(__name__)

_DEFAULT_CONF_FILE = 'tir.yml'
_DEFAULT_SETTINGS = {
    'build_dir': 'html',
    'visuals': {
        'theme': 'default'
    },
}


def load_settings(override: dict = None) -> dict:
    cfg = {}
    if os.path.isfile(_DEFAULT_CONF_FILE):
        with open(_DEFAULT_CONF_FILE, 'r', encoding='UTF-8') as file:
            content = file.read()
            logger.debug(_DEFAULT_CONF_FILE, content)
            cfg = load(content, Loader=FullLoader)

    merged_cfg = {**_DEFAULT_SETTINGS, **cfg}

    if override is not None:
        merged_cfg = {**override, **merged_cfg}

    with open(_DEFAULT_CONF_FILE, 'w+', encoding='UTF-8') as f:
        f.write(dump(merged_cfg, Dumper=Dumper))

    return merged_cfg
