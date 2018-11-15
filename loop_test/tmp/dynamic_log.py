#! /usr/bin/env python
# coding=utf-8

import logging
import os

class DynamicRecorder:
    """
    """
    def __init__(self,
                 log_path,
                 logger_name = 'darling.testcase',
                 log_level = logging.DEBUG,
                 log_format = "%(asctime)s - %(filename)s[line:%(lineno)d] : %(message)s"):
        self.construct_logger(log_path, logger_name, log_level, log_format)

    def construct_logger(self, log_path, logger_name, log_level, log_format):
        self.logger = logging.getLogger(logger_name)
        print(">>>> logger : id:{}".format(id(self.logger)))
        ch1 = logging.StreamHandler()
        ch2 = logging.FileHandler(log_path)
        formatter = logging.Formatter(log_format)
        ch1.setLevel(log_level)
        ch2.setLevel(log_level)
        ch1.setFormatter(formatter)
        ch2.setFormatter(formatter)
        self.logger.addHandler(ch1)
        self.logger.addHandler(ch2)

    def log(self, *kargs, **kwargs):
        return self.logger.error(*kargs, **kwargs)

