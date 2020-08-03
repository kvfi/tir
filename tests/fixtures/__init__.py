import os

import pytest


@pytest.fixture
def sample_env_file_path():
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', '.env-test')
