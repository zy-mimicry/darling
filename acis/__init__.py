#! /usr/bin/env python
# coding=utf-8

"""
"""

#import logging
from acis.utils.log import Log
from acis.core.port import Port
import os

ports = ["master..AT",
         "slave..AT",
         "master..ADB",
         "slave..ADB"]

ports = ["any..AT",
         "any..ADB"]

class ACISMiscer():
    """
    This is a manager for acis package.
    """
    def __init__(self, prefix_of_log_path):

        self.prefix = prefix_of_log_path
        self.limit_name = 'testcases' # testcases root directory.
        self.mPort = Port()

    def deal_log_path(self, log_file):
        path = log_file.split('/') # Must 'linux' system.
        print("path: {}".format(path))
        path = path[path.index(self.limit_name)+1:]
        print("after path: {}".format(path))
        path[-1] = path[-1].replace('.py', '.log')
        log_path = self.prefix + '/' + self.limit_name + '/' + '/'.join(path)
        print("log path: ",log_path)
        return log_path

    def misc_deal(self, log_file, logger_name, mail_to, port_names = []):
        self.mDynamicRecorder = DynamicRecorder(self.deal_log_path(log_file), logger_name = logger_name)
        self.mMail = self.register_mail(mail_to)
        self.echo_port_parser()
        self.register_port(port_names)
        self.echo_port_parser()
        return self

    def echo_port_parser(self):
        self.mPort.parser.display_all()

    def register_port(self, port_names):
        """
        port_names: This should be a sequeue like 'list'
        """
        print("Register port name : {}".format(port_names))
        for backend_name in port_names:
            backend = self.mPort.match(backend_name)
            if backend.name == 'AT':
                self.at = backend
            elif backend.name == "ADB":
                self.adb = backend
            else:
                raise Exception("Unknow backend for port.")

    def register_mail(self, mail_to):
        print("From addr(mail): {}".format(mail_to))

    def log(self, *kargs, **kwargs):
        self.mDynamicRecorder.log(*kargs, **kwargs)
