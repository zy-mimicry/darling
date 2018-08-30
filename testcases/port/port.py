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

    def name_split(self, name):
        """ name: 'slavename..AT' """
        return tuple(name.split('..'))

    def match(self, name):
        slave_name, backend_name = name_split(name)
        conf = self.parser.get_conf(slave_name)
        return self.factory.which_backend(backend_name, conf)
