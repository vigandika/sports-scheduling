import logging.config


def init_logging():
    logging.config.fileConfig('log/logging.conf')
    return logging
