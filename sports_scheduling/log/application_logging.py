LOGGING_CONF = {
    'version': 1,
    'formatters': {
        'stream': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'stream',
            'stream': 'ext://sys.stdout'
        },
    },
    'loggers': {
        'sports-timetable-scheduling': {
            'level': 'INFO',
        },
    }
}
