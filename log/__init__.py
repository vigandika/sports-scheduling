import logging.config

from log.application_logging import LOGGING_CONF

logger = logging.getLogger('sports-time-scheduling')


def init_logging():
    logging.config.fileConfig('log/logging.conf')

    return logging
