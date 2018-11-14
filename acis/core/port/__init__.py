#! /usr/bin/env python
# coding=utf-8

"""
"""

from .parser import PortConfParser
from .backends import PortFactory

class Port:
    def __init__(self):
        self.parser = PortConfParser()
        self.factory = PortFactory()

        self.at = None
        self.adb = None

    def name_split(self, name):
        return tuple(name.split('..'))

    def match(self, name):

        backend_name, type_name = self.name_split(name)
        conf = self.parser.get_conf(backend_name, type_name)
        # print("return conf type: ", type(conf), backend_name, type_name)
        # print("Get conf from rules: <{}>".format(conf))

        if backend_name == "AT":
            print("match : AT backend")
            self.at = self.factory.which_backend(backend_name, type_name, conf)
            print("match : AT return :{}".format(self.at))
            return self.at

        elif backend_name == "ADB":
            print("match : ADB backend")
            self.adb = self.factory.which_backend(backend_name, type_name, conf)
            print("match : ADB return :{}".format(self.adb))
            return self.adb
