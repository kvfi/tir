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
        with open(_DEFAULT_CONF_FILE, 'r') as file:
            content = file.read()
            logger.debug(_DEFAULT_CONF_FILE, content)
            cfg = yaml.safe_load(content)

    merged_cfg = {**_DEFAULT_SETTINGS, **cfg}

    if override is not None:
        merged_cfg = {**override, **merged_cfg}

    # TODO: create backup file in case something bad happens

    with open(_DEFAULT_CONF_FILE, 'w+') as f:
        f.write(yaml.safe_dump(merged_cfg, allow_unicode=True))

    return merged_cfg
