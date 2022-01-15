import pathlib

import marshmallow_dataclass
import yaml
from tir.config import get_config
from tir.schemas.config import Config

from tests import SAMPLE_PAGE_FILE_PATH


def test_config_obj():

    with open(pathlib.Path(__file__).parent.joinpath('data', 'tir.yml')) as f:
        cfg = yaml.safe_load(f.read())
        deployment_schema = marshmallow_dataclass.class_schema(Config)()
        deployment = deployment_schema.load(cfg)
        assert deployment is not None


def test_config_singleton_like():
    n: Config = get_config()
    p: Config = get_config()
    assert n == p


def test_load_config():
    config = get_config()
    assert config.build_dir == 'html'
