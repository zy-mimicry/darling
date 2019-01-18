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


        self.limit_name = 'testcases' # Maybe get this var from environment better.

        try:
            self.prefix = os.environ["REPORT_PATH"] + '/' \
                + os.environ["PLATFORM"] + '/' \
                + os.environ["ACIS_DIFF"]
        except KeyError as e:
            peer("Can't get vaild environments from master. \nStack info: \n<{}>.\nSo switch to default branch.".format(e))
            if not os.path.exists('/tmp/acis/testlog/' + self.limit_name):
                os.makedirs('/tmp/acis/testlog/' + self.limit_name, mode = 0o744)
            self.prefix = '/tmp/acis/testlog'

        self.at  = None
        self.adb = None

    def deal_log_path(self, case_file):

        dname,fname = os.path.split(case_file)
        dname = dname.split(self.limit_name + '/')[1]
        mprefix = self.prefix + '/' + self.limit_name + '/' + dname + '/'
        self.which_log = mprefix + fname.replace('.py', '.log')
        self.case_output = mprefix + fname.replace('.py', '')
        if not os.path.exists(self.case_output):
            os.makedirs(self.case_output, mode=0o755)
        peer("Case Log Location: {}".format(self.which_log))
        return self.which_log

    def deal_misc(self, log_file, logger_name, port_names, mail_to = "SWI@sierrawireless.com"):
        global hook_log
        hook_log = self.log = Log(self.deal_log_path(log_file), logger_name = logger_name)
        self.mMail = self.register_mail(mail_to)
        self.register_port(port_names)
        import acis.conf.tc_conf as tc
        self.conf = tc
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
