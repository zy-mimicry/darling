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

        backend_name, obj_name = self.name_split(name)
        conf = self.parser.get_conf(slave_name)

        if backend_name == "AT":
            self.at = self.factory.which_backend(backend_name, obj_name, conf)
            return self.at
        elif backend_name == "ADB":
            self.adb = self.factory.which_backend(backend_name, obj_name, conf)
            return self.adb

        #return self.factory.which_backend(backend_name, obj_name, conf)
