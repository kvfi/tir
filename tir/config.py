import logging
import sys
from pathlib import Path

import marshmallow_dataclass
import yaml

from tir.schemas.config import Config

logger = logging.getLogger(__name__)

REQUIRED_PATHS = ['tir.yml', 'content', 'content/posts', 'layout']
_DEFAULT_CONF_FILE = 'tir.yml'


def get_config(override: dict = None) -> Config:
    if Path.cwd().joinpath(_DEFAULT_CONF_FILE).exists():
        with open(_DEFAULT_CONF_FILE, 'r', encoding='utf-8') as f:
            content = f.read()
            cfg = yaml.safe_load(content)
            config_schema = marshmallow_dataclass.class_schema(Config)()
            config: Config = config_schema.load(cfg)
        return config
    else:
        sys.exit('Config file does not exist.')
