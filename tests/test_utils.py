from tests import temporary_folder
from tir.utils import load_env


def test_simple():
    with temporary_folder() as tf:
        assert tf is not None, 'Folder object is not None'


def test_load_env(sample_env_file_path):
    path = sample_env_file_path
    env = load_env(path)
    assert isinstance(env, dict)
