# -*- coding: utf-8 -*-

"""

"""

import logging
import logging.config
import os

# You can overwrite this environment argument.
if not os.getenv("Darling_Logs_Path", ""):
    if not os.path.exists("/tmp/darling/logs"):
        print("here??")
        os.makedirs("/tmp/darling/logs", 0o755)
        os.environ["Darling_Logs_Path"] = "/tmp/darling/logs/"
    else:
        os.environ["Darling_Logs_Path"] = "/tmp/darling/logs/"

DEFAULT_LOGGING = {
    'version' : 1,
    'disable_existing_loggers' : False,

    # TBD... Maybe useful
    # 'filters' : {},

    'formatters' : {
        'verbose' : {
            'format' : "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            'style' : "{",

        },
        'simple' : {
            'format' : "{levelname} {asctime} {module} {message}",
            'style' : "{",
        },

    },
    'handlers' : {
        'console' : {
            'level' : "INFO",
            'class' : "logging.StreamHandler",
            'formatter' : "simple",
        },
        'developer_file' : {
            'level' : "INFO",
            'class' : "logging.FileHandler",
            'filename' : os.environ["Darling_Logs_Path"] + "developer_debug_file.log",
            'formatter' : 'simple',
            'mode' : 'w',
        },
        'core_file' : {
            'level' : "DEBUG",
            'class' : "logging.FileHandler",
            'filename' : os.environ["Darling_Logs_Path"] + "core_debug.log",
            'formatter' : 'verbose',
            'mode' : 'w',
        },
    },
    'loggers' : {
        'core' : {
            'handlers' : ["core_file"],
            'level' : "DEBUG",
            'propagate' : True,
        },
        'developer' : {
            'handlers' : ["console", "developer_file"],
            'level' : "INFO",
        }
    }
}


class Peer:
    def __init__(self, logging_conf, logger_name):
        logging.config.dictConfig(DEFAULT_LOGGING)
        self._get_logger(logger_name)
    def _get_logger(self, name):
        self.logger = logging.getLogger(name)
    def __call__(self,*kargs, **kwargs):
        self.logger.error(*kargs, **kwargs)

class Log(Peer):
    def __call__(self,*kargs, **kwargs):
        self.logger.info(*kargs, **kwargs)
        pass

# Provide thos entries for logging.
peer = Peer(DEFAULT_LOGGING, "core")
log  = Log(DEFAULT_LOGGING, "developer")
