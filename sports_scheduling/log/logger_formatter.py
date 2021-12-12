import logging


class LoggingFormatter(logging.Formatter):
    # https://gist.github.com/vratiu/9780109

    grey = "\x1b[0;20m"
    yellow = "\x1b[0;33m"
    cyan = "\x1b[0;36m"
    red = "\x1b[0;50m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = '%(asctime)s %(name)s %(levelname)s: %(message)s'

    FORMATS = {
        logging.DEBUG: yellow + format + reset,
        logging.INFO: grey + format + reset,
        logging.WARNING: red + format + reset,
        logging.ERROR: bold_red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        formatter.datefmt = '%Y-%m-%d %H:%M:%S'
        return formatter.format(record)
