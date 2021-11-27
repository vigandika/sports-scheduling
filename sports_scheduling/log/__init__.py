import logging.config

logger = logging.getLogger('sports-time-scheduling')


def init_logging():
    logging.config.fileConfig('log/logging.conf')
    return logging
