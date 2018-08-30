#! /usr/bin/env python
# coding=utf-8


"""
"""
from . import AT,ADB

class PortFactory():
    backends = {
        'AT' : AT,
        'ADB': ADB,
    }
    def __init__(self):
        pass

    def which_backend(self, name, conf):
        return backends.get(name)(conf)
