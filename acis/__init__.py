#! /usr/bin/env python
# coding=utf-8

"""
pytest version == 3.7.1
allure version == 2.5.0
"""

from acis.utils.log import Log,peer
from acis.core.port import Port
import os, re

hook_log = None

class ACISMiscer():
    """
    """

    def __init__(self):

        self.limit_name = 'ACIS_TESTCASES' # Maybe get this var from environment better.

        self.prefix = os.environ["REPORT_PATH"] + '/' \
            + os.environ["PLATFORM"] + '/' \
            + os.environ["ACIS_DIFF"]

        self.at  = None
        self.adb = None

    def deal_log_path(self, case_file):

        path = case_file.split('/')
        path = path[path.index(self.limit_name)+1:]
        path[-1] = path[-1].replace('.py', '.log')
        self.which_log = log_path = self.prefix + '/' + self.limit_name + '/' + '/'.join(path)
        peer("Case Log Location: {}".format(log_path))
        return log_path

    def misc_deal(self, log_file, logger_name, mail_to, port_names, conf_file = None):
        global hook_log
        hook_log = self.log = Log(self.deal_log_path(log_file), logger_name = logger_name)
        self.mMail = self.register_mail(mail_to)
        self.register_port(port_names)
        return self

    def register_mail(self, mail_to):
        peer("[Mail] From: {}".format(mail_to))

    def order_port_list(self,port_names):
        """
        Note: the order of ports register is important!
        At port should be in front.
        """
        AT_front = []
        other_behind = []

        for p in port_names:
            if re.search('AT..', p):
                AT_front.append(p)
            else:
                other_behind.append(p)
        AT_front.extend(other_behind)
        return AT_front

    def register_port(self, port_names):

        self.mPort = Port()
        port_names = self.order_port_list(port_names)

        for backend_cookie in port_names:
            peer("\n\n Loop is <{}>".format(backend_cookie))
            backend = self.mPort.match(backend_cookie)

            if backend.name == 'AT':
                self.at = backend
            elif backend.name == "ADB":
                self.adb = backend
            else:
                pass
