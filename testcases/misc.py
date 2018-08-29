#! /usr/bin/env python
# coding=utf-8

import logging
import os
from .dynamic_log import DynamicRecorder

class DarlingMiscDealer():
    def __init__(self, prefix_of_log_path):

        self.prefix = prefix_of_log_path
        self.limit_name = 'testcases' # testcases root directory.

    def deal_log_path(self, log_file):
        path = log_file.split('/') # Must 'linux' system.
        path = path[path.index(self.limit_name)+1:]
        path[-1] = path[-1].replace('.py', '.log')
        log_path = self.prefix + '/' + '/'.join(path)
        print(log_path)
        return log_path

    def misc_deal(self, log_file, mail_from, port_name):
        self.mDynamicRecorder = DynamicRecorder(self.deal_log_path(log_file))
        self.mMail = self.register_mail(mail_from)
        self.mPort = self.register_port(port_name)
        return self

    def register_port(self, port_name):
        print("Register port name : {}".format(port_name))

    def register_mail(self, mail_from):
        print("From addr(mail): {}".format(mail_from))

    def log(self, *kargs, **kwargs):
        self.mDynamicRecorder.log(*kargs, **kwargs)
