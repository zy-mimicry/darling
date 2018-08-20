#! /usr/bin/env python
# coding=utf-8

import logging
import os

class DarlingMiscDealer():
    def __init__(self,
                 log_path,  # passed by __file__
                 mail_from, # passed by case owner
                 log_level = logging.DEBUG,
                 #log_format = "{asctime} [{module}] :{message}"):
                 log_format = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"):

        self.log_path = log_path
        self.log_level = log_level
        self.log_format = log_format
        #self.limit_name = "ACIS"
        self.limit_name = "testcases"

        self.construct_logger()
        self.register_mail(mail_from)

    def construct_logger(self):
        self.logger = logging.getLogger("darling.testcase")
        ch1 = logging.StreamHandler()
        # ch2 = logging.FileHandler(self.deal_log_path())
        ch1.setLevel(self.log_level)
        # ch2.setLevel(self.log_level)
        formatter = logging.Formatter(self.log_format)

        ch1.setFormatter(formatter)
        # ch2.setFormatter(formatter)
        self.logger.addHandler(ch1)
        # self.logger.addHandler(ch2)

    def deal_log_path(self):
        path = self.log_path.split('/') # Must 'linux' system.
        print("stage:[1] {}".format(path))
        path = path[path.index(self.limit_name):]
        print("stage:[2] {}".format(path))
        path[-1] = "hello.log"
        #self.log_path = self.limit_name + '/' + '/'.join(path)
        self.log_path = './' + '/'.join(path)
        print(self.log_path)

    def __call__(self):
        return self.logger.error

    def log(self, *kargs, **kwargs):
        return self.logger.error(*kargs, **kwargs)

    def register_mail(self, mail_from):
        print("From addr(mail): {}".format(mail_from))
        pass

