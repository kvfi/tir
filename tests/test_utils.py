from tests import temporary_folder
from tir.utils import n_bit_hash


def test_simple():
    with temporary_folder() as tf:
        assert tf is not None, 'Folder object is not None'


def test_n_bit_hash(load_dummy_file_content):
    for i in range(1, 256):
        h = n_bit_hash(load_dummy_file_content, i)
        assert isinstance(h, int)
        assert h > 0
