import logging
from pathlib import Path

import yaml

from tir.schemas.config import Config

logger = logging.getLogger(__name__)

REQUIRED_PATHS = ['tir.yml', 'content', 'content/posts', 'layout']
_DEFAULT_CONF_FILE = 'tir.yml'


def get_config(path: str = None) -> Config:
    config_file_path: Path = Path.cwd().joinpath(path or _DEFAULT_CONF_FILE)
    if config_file_path.exists():
        with open(config_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            cfg = yaml.safe_load(content)
            config: Config = Config(**cfg)
    else:
        config: Config = Config(**{})
    return config
