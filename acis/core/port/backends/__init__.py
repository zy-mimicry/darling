#! /usr/bin/env python
# coding=utf-8


"""
"""
from .at  import AT
from .adb import ADB

class PortFactory():

    backends = {
        'AT' : AT,
        'ADB': ADB,
    }

    def __init__(self):

        self.records = {}
        self.port_obj = None

    def which_backend(self, name, obj, conf):

        if name not in self.records.keys():
            self.port_obj = PortFactory.backends.get(name)(obj, conf)
            self.records[name] = [].append(obj)
        else:
            self.port_obj.reinit(obj,conf)
            self.records[name].append(obj)
        return self.port_obj
