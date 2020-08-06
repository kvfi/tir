import os
from contextlib import contextmanager
from shutil import rmtree
from tempfile import mkdtemp

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
SAMPLE_PAGE_FILE_PATH = os.path.join(DATA_DIR, 'page.md')


@contextmanager
def temporary_folder():
    """
    Creates a temporary folder, return it and delete it afterwards.
    This allows to do something like this in tests:
        >>> with temporary_folder() as d:
            # do whatever you want
    """
    tempdir = mkdtemp()
    try:
        yield tempdir
    finally:
        rmtree(tempdir)
