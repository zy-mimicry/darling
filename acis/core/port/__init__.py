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

        self.master = None
        self.slave = None
        self.anyone = None

    def name_split(self, name):
        return tuple(name.split('..'))

    def match(self, name):
        obj_name, backend_name = self.name_split(name)
        conf = self.parser.get_conf(slave_name)
        return self.factory.which_backend(backend_name, conf)
