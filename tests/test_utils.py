from tests import temporary_folder
from tir.utils import load_env, n_bit_hash


def test_simple():
    with temporary_folder() as tf:
        assert tf is not None, 'Folder object is not None'


def test_load_env(sample_env_file_path):
    path = sample_env_file_path
    env = load_env(path)
    assert isinstance(env, dict)


def test_n_bit_hash(load_dummy_file_content):
    for i in range(1, 256):
        h = n_bit_hash(load_dummy_file_content, i)
        assert isinstance(h, int)
        assert h > 0
