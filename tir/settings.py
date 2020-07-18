import logging
import os

import yaml

logger = logging.getLogger(__name__)

REQUIRED_PATHS = ['tir.yml', 'content', 'content/posts', 'layout']
_DEFAULT_CONF_FILE = 'tir.yml'
_DEFAULT_SETTINGS = {
    'build_dir': 'html',
    'visuals': {
        'theme': 'default'
    }
}


def load_settings(override: dict = None) -> dict:
    cfg = {}
    if os.path.isfile(_DEFAULT_CONF_FILE):
        with open(_DEFAULT_CONF_FILE, 'r', encoding='UTF-8') as file:
            content = file.read()
            logger.debug(_DEFAULT_CONF_FILE, content)
            cfg = yaml.safe_load(content)

    merged_cfg = {**_DEFAULT_SETTINGS, **cfg}

    if override is not None:
        merged_cfg = {**override, **merged_cfg}

    with open(_DEFAULT_CONF_FILE, 'w+', encoding='UTF-8') as f:
        f.write(yaml.dump(merged_cfg, Dumper=yaml.Dumper))

    return merged_cfg
