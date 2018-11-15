#! /usr/bin/env python
# coding=utf-8

"""
"""

from .parser import PortConfParser
from .backends import PortFactory
from .port_exceptions import UnsupportBackendErr

class Port:
    def __init__(self):
        self.parser = PortConfParser()
        self.factory = PortFactory()

        self.at = None
        self.adb = None

    def name_split(self, name):
        return tuple([n.strip() for n in name.split('..')])

    def match(self, name):
        backend_name, type_name = self.name_split(name)

        backend_name = backend_name.upper()
        type_name = type_name.lower()

        conf = self.parser.get_conf(backend_name, type_name)

        if backend_name == "AT":
            self.at = self.factory.which_backend(backend_name, type_name, conf)
            return self.at

        elif backend_name == "ADB":
            self.adb = self.factory.which_backend(backend_name, type_name, conf)
            return self.adb
        else:
            raise UnsupportBackendErr("NOT support backend <{backend}>.".format(backend = backend_name))
