import pytest

from tests import temporary_folder


def test_simple():
    with temporary_folder() as tf:
        assert tf is not None, "Folder object is not None"
