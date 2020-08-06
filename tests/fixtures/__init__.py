import os

import pytest

from tests import DATA_DIR, SAMPLE_PAGE_FILE_PATH


@pytest.fixture
def sample_env_file_path():
    return os.path.join(DATA_DIR, '.env-test')


@pytest.fixture
def load_dummy_file_content():
    with open(SAMPLE_PAGE_FILE_PATH, 'r') as f:
        content = f.read()
    return content
