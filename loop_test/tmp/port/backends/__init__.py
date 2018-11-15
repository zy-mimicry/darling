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
        pass

    def which_backend(self, name, conf):
        return PortFactory.backends.get(name)(conf)
