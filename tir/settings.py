import logging
import logging.config
import os

from tir.utils import load_logging, app_config

LOGS_DIR = './logs'


def load_settings():
    log_config = load_logging()
    if not os.path.exists(LOGS_DIR):
        os.mkdir(LOGS_DIR)
    logging.config.dictConfig(log_config)


config = app_config()
