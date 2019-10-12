import logging
import logging.config
import os

from tir.utils import load_logging

LOGS_DIR = './logs'


def load_settings():
    load_logging()
    log_config = load_logging()
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)
    logging.config.dictConfig(log_config)
