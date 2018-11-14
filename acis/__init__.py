#! /usr/bin/env python
# coding=utf-8

"""
"""

from acis.utils.log import Log,peer
from acis.core.port import Port
import os

class ACISMiscer():
    """
    This is a manager for acis package.
    """
    #def __init__(self, prefix_of_log_path):
    def __init__(self):

        # self.prefix = prefix_of_log_path
        self.limit_name = 'ACIS_TESTCASES' # testcases root directory.

        self.at  = None
        self.adb = None

    def deal_log_path(self, case_file):
        path = case_file.split('/')
        print("path: {}".format(path))

        path = path[path.index(self.limit_name)+1:]
        print("after path: {}".format(path))

        path[-1] = path[-1].replace('.py', '.log')
        #log_path = self.prefix + '/' + self.limit_name + '/' + '/'.join(path)
        log_path = ""
        if not os.path.basename(os.environ["ACIS_LOG_PATH"]):
            log_path = os.environ["ACIS_LOG_PATH"] + '/' + self.limit_name + '/' + '/'.join(path)
        log_path = os.environ["ACIS_LOG_PATH"] + self.limit_name + '/' + '/'.join(path)
        print("log path: ",log_path)
        return log_path

    def misc_deal(self, log_file, logger_name, mail_to, port_names = []):
        #self.log   = Log(self.deal_log_path(log_file), logger_name = logger_name)
        #self.mMail = self.register_mail(mail_to)
        self.register_port(port_names)
        return self

    def register_mail(self, mail_to):
        print("From addr(mail): {}".format(mail_to))

    def register_port(self, port_names):
        self.mPort = Port()
        port_names.sort()
        print("Register port name : {}".format(port_names))

        for backend_cookie in port_names:
            print("\n\n Loop is <{}>".format(backend_cookie))
            backend = self.mPort.match(backend_cookie)

            if backend.name == 'AT':
                self.at = backend
            elif backend.name == "ADB":
                self.adb = backend

def setup():
    pass