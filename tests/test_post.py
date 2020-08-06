from tests import SAMPLE_PAGE_FILE_PATH
from tir.posts import Post


def test_post_reader():
    p = Post(SAMPLE_PAGE_FILE_PATH)
    assert isinstance(p, Post)
    assert p.meta['title'] == 'Sample page'
