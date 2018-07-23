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


logger_of_core = None
logger_of_devp = None
LOG = None

def configure_logging():
    global logger_of_core, logger_of_devp, LOG
    logging.config.dictConfig(DEFAULT_LOGGING)
    logger_of_core = logging.getLogger("core")
    logger_of_devp = logging.getLogger("developer")
    LOG = logger_of_devp.info

if __name__ == "__main__":
    configure_logging()
    LOG("Just Test the logger {logger_context}".format(logger_context = "Hello logging module."))
