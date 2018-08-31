#! /usr/bin/env python
# coding=utf-8

import logging
import os
from .dynamic_log import DynamicRecorder
from .port.port import Port

class DarlingMiscDealer():
    def __init__(self, prefix_of_log_path):

        self.prefix = prefix_of_log_path
        self.limit_name = 'testcases' # testcases root directory.
        self.mPort = Port()

    def deal_log_path(self, log_file):
        path = log_file.split('/') # Must 'linux' system.
        path = path[path.index(self.limit_name)+1:]
        path[-1] = path[-1].replace('.py', '.log')
        log_path = self.prefix + '/' + '/'.join(path)
        print(log_path)
        return log_path

    def misc_deal(self, log_file, mail_from, port_names = []):
        self.mDynamicRecorder = DynamicRecorder(self.deal_log_path(log_file))
        self.mMail = self.register_mail(mail_from)
        self.echo_port_parser()
        self.register_port(port_names)
        self.echo_port_parser()
        return self

    def echo_port_parser(self):
        self.mPort.parser.display_all()

    def register_port(self, port_names):
        print("Register port name : {}".format(port_names))
        for backend_name in port_names:
            backend = self.mPort.match(backend_name)
            if backend.name == 'AT':
                self.at = backend
            elif backend.name == "ADB":
                self.adb = backend
            else:
                raise Exception("Unknow backend for port.")

    def register_mail(self, mail_from):
        print("From addr(mail): {}".format(mail_from))

    def log(self, *kargs, **kwargs):
        self.mDynamicRecorder.log(*kargs, **kwargs)
