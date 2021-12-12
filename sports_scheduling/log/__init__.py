import logging.config
from os import path

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')


def get_logger(name: str):
    logging.config.fileConfig(log_file_path)
    return logging.getLogger(name)
