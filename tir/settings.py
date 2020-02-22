import logging
import warnings

from yaml import Dumper, FullLoader, load, dump

logger = logging.getLogger(__name__)

_DEFAULT_SETTINGS = {
    'build_dir': 'html',
    'visuals': {
        'theme': 'default'
    },
}


def load_settings(override: dict = None) -> dict:
    try:
        with open('tir.yml', 'r', encoding='UTF-8') as f:
            content = f.read()
            cfg = load(content, Loader=FullLoader) or {}
    except FileNotFoundError:
        warnings.warn('No configuration file was found.')

    merged_cfg = {**cfg, **_DEFAULT_SETTINGS}

    print(merged_cfg)

    if override is not None:
        merged_cfg = {**merged_cfg, **override}

    with open('tir.yml', 'w+', encoding='UTF-8') as f:
        f.write(dump(merged_cfg, Dumper=Dumper))

    return merged_cfg
