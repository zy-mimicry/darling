#! /usr/bin/env python
# coding=utf-8

import logging
import os

class DarlingMiscDealer():
    def __init__(self,
                 prefix_of_log_path,  # passed by __file__
                 ):

        self.prefix = prefix_of_log_path
        self.limit_name = 'testcases' # testcases root directory.

    def log(self, *kargs, **kwargs):
        return self.logger.error(*kargs, **kwargs)

    def deal_log_path(self, log_file):
        path = log_file.split('/') # Must 'linux' system.
        path = path[path.index(self.limit_name)+1:]
        path[-1] = path[-1].replace('.py', '.log')
        log_path = self.prefix + '/' + '/'.join(path)
        return log_path

    def misc_deal(self, log_file, mail_from):
        self.logger_init(log_file)
        self.register_mail(mail_from)
        return self

    def register_mail(self, mail_from):
        print("From addr(mail): {}".format(mail_from))

    def logger_init(self,
                    log_file,
                    log_level = logging.DEBUG,
                    log_format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"):
                    #log_format = "{asctime} [{module}] :{message}"):
        logger_log_path = self.deal_log_path(log_file)
        self.construct_logger(logger_log_path,
                              log_level = log_level,
                              log_format = log_format)

    def construct_logger(self,
                         logger_log_path,
                         log_level,
                         log_format,
                         ):
        self.logger = logging.getLogger("darling.testcase")
        ch1 = logging.StreamHandler()
        ch2 = logging.FileHandler(logger_log_path)
        ch1.setLevel(log_level)
        ch2.setLevel(log_level)
        formatter = logging.Formatter(log_format)
        ch1.setFormatter(formatter)
        ch2.setFormatter(formatter)
        self.logger.addHandler(ch1)
        self.logger.addHandler(ch2)
