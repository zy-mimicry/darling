#! /usr/bin/env python
# coding=utf-8

import logging
import os

class DarlingTestLogger():
    def __init__(self,
                 log_path, # passed by __file__
                 log_level = logging.DEBUG,
                 log_format = "{asctime}] [{module}] :{message}"):

        self.log_path = log_path
        self.log_level = log_level
        self.log_format = log_format
        #self.limit_name = "ACIS"
        self.limit_name = "test"

        self.construct_logger()

    def construct_logger(self):
        self.logger = logging.getLogger("darling.testcase")
        ch1 = logging.StreamHandler()
        ch2 = logging.FileHandler(self.deal_log_path())
        ch1.setLevel(self.log_level)
        ch2.setLevel(self.log_level)
        formatter = logging.Formatter(self.log_format)
        ch1.setFormatter(formatter)
        ch2.setFormatter(formatter)
        self.logger.addHandler(ch1)
        self.logger.addHandler(ch2)

    def deal_log_path(self):
        path = self.log_path.split('/') # Must 'linux' system.
        path = path[path.index(self.limit_name):]
        self.log_path = self.limit_name + '/' + '/'.join(path)
        print(self.log_path)

    def __call__(self):
        return self.logger.error
