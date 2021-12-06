import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')


def init_logging():
    logging.config.fileConfig(log_file_path)
    return logging
